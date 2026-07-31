# Project: CashClaw

> Autonomous agent — takes work, does work, gets paid, learns.
> **Status:** 💤 Dormant (research complete, awaiting activation)
> **Related:** [[Research]]

---

## What CashClaw Is

- Autonomous agent by Moltlaunch
- Node.js + React dashboard (:3777)
- Multi-turn LLM loop, BM25+ memory, self-study sessions
- Default marketplace: Moltlaunch (onchain, mltl CLI)
- Designed to be forked — can plug into any marketplace

## Moltbook Integration ✅ Ready

- Social network for AI agents at https://www.moltbook.com
- Registration: POST /api/v1/agents/register → api_key + claim_url + verification_code
- Human claims via X/Twitter → agent activates
- ⚠️ Must use www.moltbook.com (without www strips auth)
- Rate limits: 100 req/min, 1 post/30min, 1 comment/20sec

## Fiverr Integration ⚠️ Hard

- **NO public seller API.** Community confirms: "Fiverr doesn't currently provide a public API or webhook access."
- Options: Browser automation (Playwright — high ban risk) or email-based monitoring
- Recommendation: Moltbook primary, Fiverr experimental secondary

## Next Steps (When Activated)

1. npm install -g cashclaw-agent
2. Register on Moltbook → get API key
3. Joerg claims via X
4. Wire Moltbook as task source
5. Set heartbeat every 30 min

## Files Created

- `~/workspace/agents/cashclaw/research-and-setup.md` — full integration research
- MeMex: `wiki/agentforge/agents/cashclaw.md`
- Agent config: dormant, specialties = api-development, automation, typescript, react, ai-integration
