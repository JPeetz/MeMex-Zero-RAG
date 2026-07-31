# Infrastructure — Credentials & Tools

> Central reference for all credentials, servers, APIs, and tools.
> **Related:** [[Board-Directives]], [[Infrastructure-OpenClaw]], [[Infrastructure-Vane]]
> **Also stored in:** TOOLS.md, MeMex wiki, Obsidian mind-vault

---

## Local Machine
- **sudo password:** Buddy-2019
- **Shell:** zsh | **OS:** macOS 15.7.5 (x64)
- **Node:** v26.0.0

## Remote Server (Vane)
- **IP:** 207.180.227.214
- **SSH:** jpeetz@207.180.227.214 / Buddy-2019
- **Hostname:** vmi1593174.contaboserver.net
- **SearXNG:** http://207.180.227.214:8080
- **DDNS:** vane.sytes.net (No-IP, ddclient daemon)

### Vane Stack
- **NGINX** → **Vane** (Perplexica Docker, port 3000) → **SearXNG** (port 8080, 70+ engines) → **OpenRouter**
- **SSL:** Let's Encrypt for vane.sytes.net, auto-renewing
- **Valkey:** valkey/valkey:9-alpine (SearXNG rate limiting)

## Local Docker WordPress
- **Port:** 80
- **Admin:** jpeetz / Buddy-2019
- **Email:** j.peetz69@gmail.com

## Supabase — TaskForge/RaceIntel
- **URL:** https://oltlnbxchdnavocpqgyc.supabase.co
- **Project ref:** oltlnbxchdnavocpqgyc
- **Anon key:** sb_publishable_vL7rS5xqsa2tyZcPimuzZw_2hPMSU39
- **Service role key:** REDACTED_supabase_key
- **DB:** 19 tables, ~514K rows

## n8n Automation
- **URL:** https://jpeetzn8n.xyz
- **Email:** j.peetz69@gmail.com
- **Password:** Buddy-2019
- **API Key:** REDACTED_jwt
- **MCP:** Enabled — 26 tools, 101 workflows

## SEO / GEO API
- **Base URL:** https://seo-api-nu.vercel.app
- **Repos:** JPeetz/SEO-API (fixed stale deploy 2026-05-23)
- **11 endpoints** — keyword research + GEO queries

## SkillsMP API
- **URL:** https://skillsmp.com
- **Base:** https://skillsmp.com/api/v1
- **Auth:** Bearer sk_live_skillsmp_6K8oyRhTNLrVA7pMYgPFC08ZVIuUW_7ht2b8FbdtU1o
- **Rate limit:** 500 req/day, 30/min

## Ollama (Local Model Fallback)
- **Host:** http://127.0.0.1:11434
- **Model:** gemma3:27b
- **Use:** Local inference fallback, no API key

## Notion
- **Access Token:** REDACTED_notion_token

## Image Generation — kie.ai (PRIMARY)
- **Provider:** https://kie.ai
- **API Key:** 9730a3130c3216d7d80cb3a1e44e7760
- **Base URL:** https://api.kie.ai/api/v1
- **Model:** nano-banana-2 (Gemini Flash Image) — $0.02/image
- **CLI:** ~/workspace/scripts/kie_image.py
- **Deprecated:** fal.ai (migrated 2026-07-08)

## Stripe (AgentForge Research Engine)
- **Secret key:** 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
- **Products:** Starter €9/mo, Pro €39/mo, Scale €149/mo

## BetterLife.care — Infrastructure

### Hostinger Email API
- **Domain:** betterlife.care
- **API:** https://api.mail.hostinger.com/
- **API Key:** 3991ab2efb3fc7ba8515d25329021fe304022a616d1d71731142e2b5ea2fc899
- **Emails:** j.peetz@, app@, info@, social@, support@

### BetterLife FTP
- **Host:** ftp://betterlife.care (IP: 145.14.152.32)
- **User:** u689536553
- **Path:** public_html
- **Password:** Buddy-2019
- **⚠️ Known issue:** Passive FTP timeout (Hostinger)

### Social Media Credentials
- **Instagram:** @better_life_ai_coaching — social@betterlife.care / Buddy-2019
- **Facebook:** social@betterlife.care / Buddy-2019
- **Meta App ID:** 998362096164262 | **Secret:** f99b8e544506eaaa56f7c66dde7177a3
- **Threads App ID:** 3352364111613215 | **Secret:** 48c30447113abc69ea0ed3bbad6ef719
- **FB Page ID:** 1124600237410474 — "Better Life AI Coaching"
- **IG Business ID:** 17841420275969728 — @better_life_ai_coaching

### X (Twitter) API
- **Consumer Key:** TBYzLVILUmbT8DnU4sCkT6EjN
- **Consumer Secret:** ytT8SdJwYd0fQvUEVXNfNUbtaJY2oFoCc8Gf3a0UlySNJZSOTR
- **Bearer Token:** AAAAAAAAAAAAAAAAAAAAACQu%2BQEAAAAAfnmZK%2BDon9G%2B347ZCRhGImN7sGY%3D...
- **Access Token:** 2069423281115910144-7pRk1gMfbRGHdxFjfVn5xXjMZ0xVvG
- **Access Secret:** wbCAICBfH4cVcFcZa6PxRd2Ksp4A0VPZXCh6W4ZL5HmJy
- **Handle:** @BetterLifeatjl

### LinkedIn API
- **Client ID:** 775zrppl9vp2nh
- **Primary Secret:** REDACTED_linkedin_secret
- **Company Page ID:** 135134648
- **⚠️ Known issue:** Token scope needs w_media_upload for image posts

### CLI-Anything Hub
- **Repo:** https://github.com/HKUDS/CLI-Anything
- **Installed CLIs:** obsidian, n8n
- **Use:** Bridge agents with external software

### Antigravity (Google AI Agent Platform)
- **App:** /Applications/Antigravity.app (v1.107.0)
- **CLI:** ~/.antigravity/antigravity/bin/antigravity (alias: agy)
- **Chat:** antigravity chat [prompt]
