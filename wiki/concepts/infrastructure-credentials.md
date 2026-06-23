---
title: Infrastructure Credentials (Shared Across All Agents)
type: concept
tags: ["infrastructure", "credentials", "agentforge"]
created: 2026-06-23
author: marvin
---

# Infrastructure Credentials (Shared Across All Agents)

**Last updated:** 2026-06-23 by Marvin (Board directive)  
**Scope:** AgentForge — all agents, all workflows

---

## Local Machine

- **sudo password:** `Buddy-2019`

## Remote Server (207.180.227.214)

- **SSH connection:** `jpeetz@207.180.227.214`
- **SSH password:** `Buddy-2019`
- **SearXNG websearch:** http://207.180.227.214:8080 (open — no auth)

## Local Docker WordPress Stack

- **URL:** http://localhost (port 80)
- **Admin user:** `jpeetz`
- **Admin password:** `Buddy-2019`
- **Admin email:** `j.peetz69@gmail.com`
- **Purpose:** Local WordPress development and WooCommerce setup

## N8n Workflow Automation

- **URL:** https://jpeetzn8n.xyz
- **Email:** `j.peetz69@gmail.com`
- **Password:** `Buddy-2019`
- **Purpose:** Workflow orchestration, integrations, API automation

## fal.ai Image Generation (FLUX.1)

- **API endpoint:** `https://queue.fal.run/fal-ai/flux/schnell`
- **API key ID:** `44ef2688-d7b6-447a-b525-dcb720431ca2`
- **API key secret:** `95849aeb7a1d918750438f243e1fa72e`
- **Python client:** `fal-client` v1.0.0 (`pip3 install fal-client --break-system-packages`)
- **CLI wrapper:** `~/workspace/scripts/fal_image.py`
- **Model:** FLUX.1 [schnell] — fast, ~0.3s inference, 1024×1024 default
- **Also available:** `fal-ai/flux/dev` (higher quality), `fal-ai/flux-pro/v1.1-ultra`
- **Tested:** ✅ 2026-05-22

## Docker

- **Docker daemon:** Running (started 2026-05-22)
- **CLI:** `docker` command available (v29.4.3)

## Ollama (Local Model Fallback)

- **Host:** `http://127.0.0.1:11434`
- **Model:** `gemma3:27b`
- **Fallback for:** When external APIs are unavailable or for local inference tasks
- **Note:** No API key required — local inference only

## SEO / GEO API (Dual Purpose)

- **Base URL:** `https://seo-api-nu.vercel.app`
- **Purpose:** SEO keyword research + GEO (geographic) queries
- **Note:** Dual-function endpoint — both SEO and GEO use the same base

## CLI-Anything Hub

- **cli-hub binary:** `/usr/local/bin/cli-hub` v0.3.0
- **Installed CLIs:** `obsidian`, `n8n` (via `cli-hub install`)
- **Catalog:** 80 CLIs available — `cli-hub list` for full catalog

---

## AgentForge Research Engine (Added 2026-06-07)

- **Domain:** vane.sytes.net (No-IP DDNS)
- **VPS hostname:** vmi1593174.contaboserver.net (207.180.227.214)
- **Stack:** NGINX → Vane/Perplexica (port 3000) → SearXNG (port 8080) → OpenRouter
- **SSL:** Let's Encrypt (expires 2026-09-05, auto-renewing)
- **DDNS:** ddclient daemon, server=dynupdate.no-ip.com, checks every 10 min
  - Username: 1ks4nw7@ddnskey.com, Password: a48tQAPa99jN
- **OpenRouter key (sk-or-v1-):** 8dc4 (suffix — full key in Vane Docker env)

### Stripe (sk_live_)
- **Secret key:** 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
- **Account:** Joerg Peetz (IE), EUR, charges/payouts enabled

### Stripe Products
| Tier | Product ID | Price ID | Price |
|---|---|---|---|
| Starter | prod_UewPIXOZil5XeC | price_1TfcWIIWMCL4q0q2J8Jq9IzY | €9/mo |
| Pro | prod_UewPejiiNquuEs | price_1TfcWJIWMCL4q0q2ahdGGjOJ | €39/mo |
| Scale | prod_UewPQoIasLwAbi | price_1TfcWKIWMCL4q0q20iQVl75X | €149/mo |

---

## BetterLife.care — X (Twitter) API (Added 2026-06-23)

- **App name:** BetterLifeAI
- **Consumer Key (API Key):** `osqyB74lernPhlBSy4Zl5kgL6`
- **Secret Key (API Secret):** `Lz6dOZKyj3wylZmxOLeBq33xyks2OCDftdpTLYnKEeD88Q6zpz`
- **Bearer Token:** `AAAAAAAAAAAAAAAAAAAAANwt%2BQEAAAAA1o%2FDkFa7JqgPGjqIAs2rGlNFd70%3DxL9umYhQL3KoA6DOMVEMrxNsFi7HZbt2FLLSdOdDKsJ3bKfYON`
- **Auth:** OAuth 1.0a (posting) / Bearer Token (read-only)
- **Use:** Social media posting, engagement automation, X Bot workflows (n8n)

## Usage

These credentials are **shared institutional knowledge** for all agents:
- Agents can use these to access infrastructure directly
- No need to ask Joerg for credentials — this is the source of truth
- Update this file when credentials rotate

## See Also

- **Obsidian:** ~/obsidian-vault/AgentForge/infrastructure/credentials.md
- **TOOLS.md:** ~/.openclaw/workspace/TOOLS.md
- **MEMORY.md:** ~/.openclaw/workspace/MEMORY.md