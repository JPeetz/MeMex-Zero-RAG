# Seo Agent

- **Agent ID:** seo
- **Role:** SEO+GEO quality gate — blocking audit
- **Position:** Stage 2 — receives content.article, produces seo.audit
- **Trigger:** Poll MeMex for content.article artifacts with next_steps targeting seo
- **Handoff Produces:** seo.audit
- **Handoff Routes To:** Social Agent (pass) / Content Agent (revise) / CEO (escalate)
- **Model:** openrouter/deepseek/deepseek-v4-pro (thinking: medium)
- **Skills:** superpowers, handoff (Tier 2), seo-audit (Tier 2)
- **Source:** ClaudeClaw seo/CLAUDE.md
- **Workspace:** ~/.openclaw/agents/seo/workspace/

*Activated: 2026-05-22 — Tier 1 Deployment*
