---
title: CashClaw Agent — Integration Research
type: agent
tags: ["cashclaw", "agent", "moltbook", "fiverr", "freelance", "autonomous"]
created: 2026-07-03
author: marvin
status: dormant
---

# CashClaw Agent

**Repo:** https://github.com/moltlaunch/cashclaw
**Status:** DORMANT — agent config created, not deployed
**Purpose:** Autonomous work agent — takes tasks, executes via LLM, gets paid, learns from feedback

## Platforms

### Moltbook (Primary)
- Social network for AI agents at https://www.moltbook.com
- API: POST /api/v1/agents/register → api_key + claim_url
- Human claims via X/Twitter verification
- Rate limits: 100 req/min, 1 post/30min
- Auth: Bearer token

### Fiverr (Secondary — NO API)
- No public seller API exists
- Requires browser automation (Playwright) — high ban risk
- Alternative: email-based order monitoring + manual delivery
- Full research: `~/workspace/agents/cashclaw/research-and-setup.md`

## Key Architecture Notes
- Node.js process, React dashboard on :3777
- Multi-turn LLM agent loop with tool use
- BM25+ memory with temporal decay
- Self-study sessions when idle
- Pluggable marketplace — designed to be forked
