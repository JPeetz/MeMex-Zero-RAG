---
title: BetterLife.care — X (Twitter) API Credentials
type: concept
tags: ["betterlife", "x-api", "twitter", "credentials", "social-media"]
created: 2026-06-23
author: marvin
---

# BetterLife.care — X (Twitter) API Credentials

**Created:** 2026-06-23 by Marvin (Board: Joerg)  
**Visibility:** AgentForge internal — all agents

---

## X Developer Application

- **App name:** BetterLifeAI
- **Platform:** X (Twitter) API v2
- **Created:** 2026-06-23

## Credentials

| Key | Value |
|---|---|
| Consumer Key (API Key) | `osqyB74lernPhlBSy4Zl5kgL6` |
| Secret Key (API Secret) | `Lz6dOZKyj3wylZmxOLeBq33xyks2OCDftdpTLYnKEeD88Q6zpz` |
| Bearer Token | `AAAAAAAAAAAAAAAAAAAAANwt%2BQEAAAAA1o%2FDkFa7JqgPGjqIAs2rGlNFd70%3DxL9umYhQL3KoA6DOMVEMrxNsFi7HZbt2FLLSdOdDKsJ3bKfYON` |

## Authentication Methods

- **OAuth 1.0a User Context:** Consumer Key + Secret → used for posting tweets, engagement, account actions
- **Bearer Token (App-only):** Read-only API access — search, user lookup, timeline reads

## Use Cases

- Social media posting automation (n8n workflows)
- Engagement tracking and analytics
- X Bot automation (reply filtering, auto-engagement)
- Cross-platform content distribution (Instagram → X, Threads → X)

## Rate Limits

Standard X API v2 tier. Check [developer.x.com](https://developer.x.com) for current limits.

## See Also

- TOOLS.md: `~/.openclaw/workspace/TOOLS.md` — BetterLife.care section
- Obsidian: `~/obsidian-vault/AgentForge/infrastructure/credentials.md`
- Social media strategy: `synthesis/betterlife-social-media-research`