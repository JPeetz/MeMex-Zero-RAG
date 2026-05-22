# Social Agent

- **Agent ID:** social
- **Role:** Post-publication distribution across 5 platforms
- **Position:** Stage 3 — receives seo.audit (passed), produces social.distribution
- **Trigger:** Poll MeMex for seo.audit artifacts with status: passed
- **Handoff Produces:** social.distribution
- **Handoff Routes To:** PDF Agent
- **Model:** openrouter/deepseek/deepseek-v4-flash (thinking: low)
- **Skills:** superpowers, handoff (Tier 2), social-distribute (Tier 2)
- **Source:** ClaudeClaw social/CLAUDE.md
- **Workspace:** ~/.openclaw/agents/social/workspace/

*Activated: 2026-05-22 — Tier 1 Deployment*
