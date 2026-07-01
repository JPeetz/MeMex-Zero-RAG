# Hermes-Studio Issue #5: Sessions API 500 Error Fix

**Date:** 2026-07-01  
**Issue:** #5  
**Severity:** HIGH  
**Status:** FIXED  
**Commit:** e0b9edf  
**Source:** https://github.com/JPeetz/Hermes-Studio  

## Problem Statement

The `/api/sessions` endpoint returns 500 Internal Server Error with message: `Cannot read properties of undefined (reading 'map')`

This occurs when:
1. User is logged in with valid session token
2. User tries to view session history
3. Frontend calls `GET /api/sessions`
4. Response is 500 error instead of session list

## Root Cause Analysis

### Response Format Mismatch

Hermes gateway returns sessions in OpenAI-compatible list format:
```json
{
  "object": "list",
  "data": [
    {
      "id": "session-1",
      "source": "telegram",
      "model": "gpt-5.5",
      "title": "User conversation",
      "message_count": 125
    }
  ]
}
```

But Hermes-Studio handler expected the response to be an array or have a different structure:

```typescript
// File: src/routes/api/sessions.ts (lines 43-54)
// BROKEN CODE:
const sessions = await listSessions(50, 0)
return json({ sessions: sessions.map(toSessionSummary) })

// If listSessions() returns { object: "list", data: [...] }
// Then sessions.map() fails with:
// TypeError: Cannot read properties of undefined (reading 'map')
```

The error occurs because:
- `sessions` = `{object: "list", data: [...]}`
- `sessions.map` = `undefined`
- Calling `undefined.map()` throws TypeError

## Solution

Defensive response parsing that handles multiple formats:

```typescript
const response = await listSessions(50, 0)

// Handle OpenAI-format response: { object: "list", data: [...] }
const sessionList = Array.isArray(response) 
  ? response 
  : (response?.data ?? [])

return json({ 
  ok: true, 
  sessions: sessionList.map(toSessionSummary), 
  source: 'gateway' 
})
```

### Changes Made

**File:** `src/routes/api/sessions.ts`  
**Lines:** 43-54  

**Before:**
```typescript
try {
  const sessions = await listSessions(50, 0)
  return json({ sessions: sessions.map(toSessionSummary) })
} catch (err) {
  return json(
    {
      error: err instanceof Error ? err.message : String(err),
    },
    { status: 500 },
  )
}
```

**After:**
```typescript
try {
  const response = await listSessions(50, 0)
  // Handle OpenAI-format response: { object: "list", data: [...] }
  const sessionList = Array.isArray(response) ? response : (response?.data ?? [])
  return json({ ok: true, sessions: sessionList.map(toSessionSummary), source: 'gateway' })
} catch (err) {
  return json(
    {
      ok: false,
      error: err instanceof Error ? err.message : String(err),
    },
    { status: 500 },
  )
}
```

### Key Improvements

1. **Defensive unpacking:** Handles both array and object response formats
2. **Consistent responses:** Always includes `ok: true/false` field
3. **Source identification:** Includes `source: 'gateway'` to distinguish from local sessions
4. **Graceful fallback:** Returns `[]` if response is neither array nor has `.data`
5. **Error consistency:** Error responses also include `ok: false`

## Testing

### Manual Test

```bash
# 1. Set environment variables
export HERMES_API_URL=http://127.0.0.1:8642
export HERMES_API_TOKEN=your-valid-token
export HERMES_PASSWORD=your-password

# 2. Start Hermes gateway v0.15.1
./hermes --api-enabled

# 3. Start Hermes-Studio
npm run dev

# 4. Log in with password
curl -X POST http://localhost:3000/api/auth \
  -H "Content-Type: application/json" \
  -d '{"password":"your-password"}' \
  -c cookies.txt

# 5. Request sessions
curl -b cookies.txt http://localhost:3000/api/sessions
# Expected: 200 { ok: true, sessions: [...] }
# Before fix: 500 { error: "Cannot read properties of undefined..." }
```

### Frontend Flow

**Before:**
1. User clicks "Session History"
2. Frontend: `fetch('/api/sessions')`
3. Status: 500 with error message
4. UI displays: "Failed to load sessions"

**After:**
1. User clicks "Session History"
2. Frontend: `fetch('/api/sessions')`
3. Status: 200 with sessions list
4. UI displays: Session list with titles, models, message counts

## Response Examples

### Success Response (After Fix)

```json
{
  "ok": true,
  "sessions": [
    {
      "id": "session-1",
      "source": "telegram",
      "model": "gpt-5.5",
      "title": "Support conversation",
      "messageCount": 125,
      "createdAt": "2026-06-01T10:00:00Z"
    },
    {
      "id": "session-2",
      "source": "slack",
      "model": "claude-3",
      "title": "Team discussion",
      "messageCount": 43,
      "createdAt": "2026-06-15T14:30:00Z"
    }
  ],
  "source": "gateway"
}
```

### Error Response (Unchanged)

```json
{
  "ok": false,
  "error": "Failed to connect to gateway"
}
```

## Root Cause Summary

**Why it happened:**
- Hermes gateway returns OpenAI-format responses
- Hermes-Studio handler wasn't updated to parse OpenAI format
- Assumption: `listSessions()` returns array (incorrect)

**Why it wasn't caught:**
- No tests for OpenAI-format response parsing
- Integration only tested with specific response format
- No type safety on external API responses

## Prevention

For future API integrations:

1. **Type safety:** Define types for all external API responses
2. **Parsing tests:** Test against actual gateway response format
3. **Defensive code:** Always check response structure before accessing properties
4. **Response format docs:** Document expected format in comments
5. **Integration tests:** Test with real gateway responses

---

**Status:** ✅ FIXED and deployed (2026-07-01)  
**Next:** Monitor for additional gateway compatibility issues
