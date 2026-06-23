---
title: BetterLife.care — X (Twitter) API Credentials
type: concept
tags: ["betterlife", "x-api", "twitter", "credentials", "social-media", "oauth2"]
created: 2026-06-23
author: marvin
---

# BetterLife.care — X (Twitter) API Credentials

**Created:** 2026-06-23 by Marvin (Board: Joerg)  
**Updated:** 2026-06-23 — recreated with OAuth 2.0 credentials  
**Visibility:** AgentForge internal — all agents

---

## X Developer Application

- **App name:** BetterLifeAI
- **Platform:** X (Twitter) API v2
- **Created:** 2026-06-23 (recreated same day with new keys)

## Credentials

### OAuth 1.0a (App-level)

| Key | Value |
|---|---|
| Consumer Key (API Key) | `TBYzLVILUmbT8DnU4sCkT6EjN` |
| Secret Key (API Secret) | `ytT8SdJwYd0fQvUEVXNfNUbtaJY2oFoCc8Gf3a0UlySNJZSOTR` |
| Bearer Token | `AAAAAAAAAAAAAAAAAAAAACQu%2BQEAAAAAfnmZK%2BDon9G%2B347ZCRhGImN7sGY%3DHqh0M6vDhaWIUBkcruhoZzikPOa84lhG0MzzycGpfqtosmVxQw` |

### OAuth 2.0 (User-level)

| Key | Value |
|---|---|
| Client ID | `RGFuUGF6NW01ZS02d0djV2dkZkw6MTpjaQ` |
| Client Secret | `lLrwClWkVNZ-hGClvMZMye9kjcZfFMYzXsAOWfLKs882q9nB2c` |

## Authentication Methods

- **OAuth 1.0a User Context:** Consumer Key + Secret + Access Token + Access Token Secret → posting tweets, media upload, account actions. Access tokens must be generated from the X Developer Portal.
- **OAuth 2.0 (Authorization Code with PKCE):** Client ID + Client Secret → v2 API endpoints. Requires user authorization flow.
- **Bearer Token (App-only):** Read-only access — search, user lookup. Limited on free tier (no credits).

## Blockers for Posting

- [ ] **Access Token + Access Token Secret** — Must generate from X Developer Portal → App → Keys and Tokens → "Generate Access Token and Secret" with Read+Write permissions
- [ ] **API tier credits** — Free tier posts 1,500 tweets/month; read/search needs Basic tier ($100/mo)

## Use Cases

- Social media posting automation (n8n workflows)
- Engagement tracking and analytics
- X Bot automation
- Cross-platform content distribution

## See Also

- TOOLS.md: `~/.openclaw/workspace/TOOLS.md`
- Obsidian: `~/obsidian-vault/AgentForge/infrastructure/credentials.md`
- MeMex infrastructure: `concepts/infrastructure-credentials`
- Social media strategy: `synthesis/betterlife-social-media-research`