# Content Agent

- **Agent ID:** content
- **Role:** Keyword research → article writing (Part A). Image gen/PDF/SEO handled by Part B.
- **Position:** Stage 1 — initiates daily content pipeline
- **Trigger:** 
  - Cron Part A: Mon-Fri 08:30 IE (content_pipeline_part_a)
  - Cron Part B: Mon-Fri 09:15 IE (content_pipeline_part_b)
- **Handoff:** 
  - Part A → Part B (via artifacts with status 'draft_pending_image')
  - Part B → Documents/AgentForge (PDF output)
- **Model:** Part A: deepseek-v4-pro (thinking: medium), Part B: deepseek-v4-pro
- **Skills:** superpowers, keyword-research (Tier 2), article-writer (Tier 2)
- **Source:** OpenClaw native
- **Pipeline split reason:** Single cron failed at tool stages (image gen, PDF, SEO). Text-heavy article writing and tool-heavy finishing split into A/B for reliability. As of 2026-05-27.

*Last updated: 2026-05-27*