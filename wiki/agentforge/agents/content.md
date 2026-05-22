# Content Agent

- **Agent ID:** content
- **Role:** Keyword research → article writing
- **Position:** Stage 1 — initiates daily content pipeline
- **Trigger:** Cron: Mon–Fri 08:30 IE (job: content_pipeline_daily)
- **Handoff Produces:** content.keyword → content.article
- **Handoff Routes To:** SEO Agent
- **Model:** openrouter/deepseek/deepseek-v4-pro (thinking: medium)
- **Skills:** superpowers, handoff (Tier 2), keyword-research (Tier 2), article-writer (Tier 2)
- **Source:** ClaudeClaw content/CLAUDE.md
- **Workspace:** ~/.openclaw/agents/content/workspace/

*Activated: 2026-05-22 — Tier 1 Deployment*
