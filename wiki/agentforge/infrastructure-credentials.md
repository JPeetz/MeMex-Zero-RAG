# Infrastructure Credentials (Shared Across All Agents)

**Last updated:** 2026-05-22 by Marvin (Board directive)  
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

## Usage

These credentials are **shared institutional knowledge** for all agents:
- Agents can use these to access infrastructure directly
- No need to ask Joerg for credentials — this is the source of truth
- Update this file when credentials rotate

## See Also

- **Obsidian:** ~/obsidian-vault/AgentForge/infrastructure/credentials.md
- **TOOLS.md:** ~/.openclaw/workspace/TOOLS.md
- **MEMORY.md:** ~/.openclaw/workspace/MEMORY.md
