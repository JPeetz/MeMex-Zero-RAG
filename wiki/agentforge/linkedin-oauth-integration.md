# LinkedIn OAuth — Integration Lessons (2026-07-06)

## The Process That Works

### Prerequisites
1. LinkedIn App with **Share on LinkedIn** + **Sign In with LinkedIn (OIDC)** products provisioned
2. Company Page must exist and be verified
3. Redirect URL `http://localhost:9999/callback` registered in app Auth settings
4. OAuth scopes: `openid profile w_organization_social`

### Reliable OAuth Flow (Manual 3-Legged)

```
1. Generate authorization URL:
   https://www.linkedin.com/oauth/v2/authorization
   ?response_type=code
   &client_id=<CLIENT_ID>
   &redirect_uri=http://localhost:9999/callback
   &state=<RANDOM_STATE>
   &scope=openid%20profile%20w_organization_social

2. Start local HTTP server on port 9999 to catch redirect

3. User opens URL → clicks Allow → redirects to localhost:9999/callback?code=...

4. Server captures code, immediately exchanges for token:
   POST https://www.linkedin.com/oauth/v2/accessToken
   Body (form-urlencoded):
     grant_type=authorization_code
     &code=<CODE>
     &redirect_uri=http://localhost:9999/callback
     &client_id=<CLIENT_ID>
     &client_secret=<PRIMARY_SECRET>

5. Store token — 2 month expiry (5,184,000 seconds)
```

## Critical Gotchas

### ❌ PKCE BREAKS IT
- **Do NOT include `code_verifier`** in the token exchange
- LinkedIn's app doesn't support PKCE
- Including it returns: `{"error": "invalid_client", "error_description": "Client authentication failed"}`
- This cost 45 minutes of debugging — the error message is completely misleading

### ❌ LinkedIn's Built-in OAuth Tools Are Broken
- The "OAuth 2.0 tools" token generator at `linkedin.com/developers/tools/oauth` loops on:
  `"Oops. We can't verify the authenticity of your request because the state parameter was modified."`
- This is a known LinkedIn bug — even incognito windows don't fix it
- **Never rely on LinkedIn's built-in token generator**

### ❌ Basic Auth Header Doesn't Work
- LinkedIn requires `client_id` and `client_secret` as POST body parameters
- Using `Authorization: Basic base64(client_id:secret)` returns: `"client_id is missing"`

### ✅ What Works
- POST body with `client_id` and `client_secret` as form-urlencoded parameters
- Primary Client Secret (not Secondary) for token exchange
- `openid profile w_organization_social` scopes together
- Token lasts 2 months — refresh before expiry via same flow

## Credentials (Synced to TOOLS.md)
- **Client ID:** `775zrppl9vp2nh`
- **Primary Secret:** `REDACTED_linkedin_secret`
- **Org ID:** `135134648`
- **Org URN:** `urn:li:organization:135134648`
- **Token stored:** `credentials/linkedin_token.json`
- **Posting script:** `scripts/linkedin_post.py <text>`
- **API endpoint:** `POST https://api.linkedin.com/rest/posts`
