# Infrastructure: Vane Research Engine

> AI research engine — Vane (Perplexica) + SearXNG + OpenRouter, deployed at vane.sytes.net.
> **Related:** [[Infrastructure]]

---

## Stack

| Component | Technology | Details |
|-----------|------------|---------|
| Frontend | Vane (Perplexica Docker) | Port 3000, itzcrazykns1337/vane:slim-latest |
| Search | SearXNG | Port 8080, 70+ engines, searxng/searxng:latest |
| Cache | Valkey | valkey/valkey:9-alpine, rate limiting |
| LLM | OpenRouter | sk-or-v1-...8dc4 |
| Reverse Proxy | NGINX | Bound to 207.180.227.214:443 |
| SSL | Let's Encrypt | Auto-renewing, expires 2026-09-05 |
| Domain | vane.sytes.net | No-IP DDNS, ddclient every 10 min |

## URLs

| URL | Purpose |
|-----|---------|
| https://vane.sytes.net | Vane research interface |
| http://207.180.227.214:8080 | SearXNG direct |
| https://vane.sytes.net/robots.txt | AI crawler access policy |
| https://vane.sytes.net/llms.txt | AI agent discovery doc |
| https://vane.sytes.net/sitemap.xml | Site index |

## SEO/Discovery Configuration

- **robots.txt:** 15 AI crawlers allowed (GPTBot, Claude-Web, PerplexityBot, Google-Extended, etc.)
- **llms.txt:** AI agent discovery document
- **sitemap.xml:** 2 URLs indexed

## Server Details

| Field | Value |
|-------|-------|
| IP | 207.180.227.214 |
| Hostname | vmi1593174.contaboserver.net |
| Provider | Contabo (via No-IP DDNS) |
| SSH | jpeetz@207.180.227.214 / Buddy-2019 |

## Still Needed

| Item | Status | Notes |
|------|--------|-------|
| API endpoints | 📝 Planned | /v1/search, /v1/ask, /v1/research |
| Developer console | 📝 Planned | Phase 2, Vercel React app |
| Domain upgrade | 🟡 Nice-to-have | research.agentforge.com or agentforge.ai |
