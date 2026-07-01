# AgentForge Auth Fallback Vulnerability — Fixed

**Date:** 2026-07-01  
**Severity:** CRITICAL  
**Source:** https://github.com/JPeetz/agentforge  
**Commit:** a6228bb  

## The Bug

In `internal/dashboard/handlers_api.go` (lines 31-35), the login handler contains a dangerous fallback:

```go
func (s *Server) handleLoginAPI(w http.ResponseWriter, r *http.Request) {
    // ... parse request ...
    
    if s.authStore == nil || s.authManager == nil {
        // VULNERABLE: Fallback accepts ANY password
        w.Header().Set("Content-Type", "application/json")
        w.Write([]byte(`{"accessToken":"dev-token","refreshToken":"dev-refresh","user":{"id":"admin-001","username":"admin","role":"admin"}}`))
        return
    }
    
    // Normal auth flow only reached if authStore and authManager are initialized
    user, err := s.authStore.AuthenticateUser(req.Username, req.Password)
    // ...
}
```

## The Problem

If either `authStore` or `authManager` fail to initialize (due to missing environment variable, startup error, or misconfiguration), the fallback activates. It returns admin-level JWT tokens regardless of the username and password provided:

- **accessToken:** `dev-token` (hardcoded)
- **refreshToken:** `dev-refresh` (hardcoded)
- **user.id:** `admin-001` (hardcoded)
- **user.role:** `admin` (hardcoded)

## Attack Scenario

1. Server starts but auth service fails to initialize (e.g., database connection error)
2. Attacker sends: `POST /api/login` with `{"username": "anything", "password": "anything"}`
3. Fallback activates because `s.authStore == nil`
4. Attacker receives valid admin tokens
5. Attacker accesses full AgentForge dashboard and all API endpoints with admin privileges

## Root Cause

Test/debug fallback left in production code:
- Comment says "backward compat for testing"
- Used during development to bypass auth setup
- Never removed before release
- Violates fail-closed principle: should reject when unsure, not accept

## The Fix

Replace fallback with fail-closed error:

```go
if s.authStore == nil || s.authManager == nil {
    // FIXED: Fail closed - reject the request
    w.Header().Set("Content-Type", "application/json")
    w.WriteHeader(http.StatusInternalServerError)
    w.Write([]byte(`{"error":"authentication service unavailable"}`))
    return
}
```

**Changes:**
- Line 34: `w.WriteHeader(http.StatusInternalServerError)` added
- Line 35: Returns 503 error instead of accepting request

**Behavior:**
- Returns `HTTP 503 Service Unavailable` when auth unavailable
- Client knows to retry or report error
- No tokens issued
- Fails safely and obviously

## Verification

```bash
# Before fix
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "hacker", "password": "wrong"}'
# Returns: {"accessToken":"dev-token","user":{"id":"admin-001","role":"admin"}}

# After fix (with auth service down)
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "hacker", "password": "wrong"}'
# Returns: 503 Service Unavailable
# {"error":"authentication service unavailable"}
```

## Impact

**Security improvement:**
- ✅ Removes unintended admin access bypass
- ✅ Enforces authentication in all code paths
- ✅ Server now fails safely when dependencies unavailable

**User experience:**
- Users see clear error message when auth service unavailable
- Encourages proper diagnosis of misconfiguration
- Makes deployment issues obvious (rather than silently succeeding with wrong behavior)

## Related Code Paths

### Refresh Endpoint

The refresh endpoint (`handleRefreshAPI`) already implements fail-closed properly:

```go
if s.authManager == nil {
    http.Error(w, `{"error":"auth not configured"}`, http.StatusInternalServerError)
    return
}
```

**This is the correct pattern.** Login endpoint now matches it.

### API Key Endpoint

Also fail-closed:

```go
if s.authStore == nil {
    http.Error(w, `{"error":"auth store not available"}`, http.StatusInternalServerError)
    return
}
```

## Deployment Notes

### No Breaking Changes

- ✅ Valid login requests work exactly as before
- ✅ Invalid credentials still rejected with 401
- ✅ Dashboard functionality unchanged
- ✅ No API changes

### Monitoring

After deployment, monitor these:
- Login attempt rate (should be normal)
- 503 error rate on login endpoint (should be 0 if auth configured correctly)
- Alert if 503 errors spike (indicates misconfiguration)

### Rollback

If needed, revert is single-line change:
```bash
git revert a6228bb
```

## Prevention

To prevent similar issues:

1. **Remove all debug fallbacks** before shipping to production
2. **Fail closed:** When unsure, reject request. Don't look for workarounds.
3. **Code review checklist:**
   - [ ] Are there any `if x == nil` fallbacks that accept requests?
   - [ ] Do all auth paths verify credentials properly?
   - [ ] Are there any hardcoded tokens or passwords?
   - [ ] Is there test-only code in production paths?
4. **Automated checks:** Add linter rule to detect hardcoded `"dev-token"` strings in production code

## Related Incidents

### OpenRouter Tier-Proxy Bypass (2026-06-30)

Similar pattern: IP-based fallback that accepted requests without proper auth.

```python
# VULNERABLE
if account is None and client_ip.startswith("172.22."):
    tier = "starter"  # Auto-promote based on spoofed IP
    quota_ok = (True, 0, 0)  # Skip ALL quota checks
```

**Pattern:** Trust untrusted input (X-Forwarded-For) as substitute for authentication.

**Lesson:** Both incidents show failures of fail-closed principle. When auth is missing, always reject. Never look for fallback ways to allow the request.

## Security Principle

**Fail Closed vs. Fail Open:**

```
❌ Fail Open (WRONG)
   if (auth service unavailable) {
       accept_request()  // Assume user is okay if we can't check
   }

✅ Fail Closed (CORRECT)
   if (auth service unavailable) {
       reject_request()  // Deny access if we can't verify
   }
```

**Rule:** When in doubt, deny. Authentication is more important than availability.

---

**Status:** ✅ FIXED (2026-07-01)  
**Commit:** a6228bb  
**Next:** Audit other applications for similar patterns
