---
title: BetterLife.care — X (Twitter) API Credentials
type: concept
tags: ["betterlife", "x-api", "twitter", "credentials", "social-media", "verified"]
created: 2026-06-23
author: marvin
---

# BetterLife.care — X (Twitter) API Credentials

**Created:** 2026-06-23 by Marvin (Board: Joerg)  
**Updated:** 2026-06-23 — access tokens generated, test tweet posted ✅  
**Visibility:** AgentForge internal — all agents

---

## X Developer Application

- **App name:** BetterLifeAI
- **X Handle:** @BetterLifeatjl
- **Platform:** X (Twitter) API v2
- **Status:** ✅ Live — test tweet posted 2026-06-23

## Credentials (Full Set)

### OAuth 1.0a (Posting & Full Access)

| Key | Value |
|---|---|
| Consumer Key (API Key) | `TBYzLVILUmbT8DnU4sCkT6EjN` |
| Secret Key (API Secret) | `ytT8SdJwYd0fQvUEVXNfNUbtaJY2oFoCc8Gf3a0UlySNJZSOTR` |
| Access Token | `2069423281115910144-7pRk1gMfbRGHdxFjfVn5xXjMZ0xVvG` |
| Access Token Secret | `wbCAICBfH4cVcFcZa6PxRd2Ksp4A0VPZXCh6W4ZL5HmJy` |
| Bearer Token | `AAAAAAAAAAAAAAAAAAAAACQu%2BQEAAAAAfnmZK%2BDon9G%2B347ZCRhGImN7sGY%3DHqh0M6vDhaWIUBkcruhoZzikPOa84lhG0MzzycGpfqtosmVxQw` |

### OAuth 2.0

| Key | Value |
|---|---|
| Client ID | `RGFuUGF6NW01ZS02d0djV2dkZkw6MTpjaQ` |
| Client Secret | `lLrwClWkVNZ-hGClvMZMye9kjcZfFMYzXsAOWfLKs882q9nB2c` |

## Authentication Methods

- **OAuth 1.0a User Context:** ✅ Full access — posting tweets, media upload, account management
- **OAuth 2.0:** Client ID + Secret for v2 endpoints
- **Bearer Token:** Read-only (requires credits on paid tier)

## Test Results (2026-06-23)

- ✅ Auth verified — @BetterLifeatjl recognized
- ✅ Tweet posted — ID: 2069438277480780276
- 🔗 https://x.com/BetterLifeatjl/status/2069438277480780276

## Use Cases

- Social media posting automation (n8n workflows)
- Image/media tweets (v1.1 upload + v2 tweet with media_ids)
- Engagement tracking and analytics
- X Bot automation (reply filtering, auto-engagement)
- Cross-platform content distribution

## See Also

- TOOLS.md: `~/.openclaw/workspace/TOOLS.md`
- Obsidian: `~/obsidian-vault/AgentForge/infrastructure/credentials.md`
- MeMex infrastructure: `concepts/infrastructure-credentials`
- Social media strategy: `synthesis/betterlife-social-media-research`