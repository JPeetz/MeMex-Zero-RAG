---
title: Operations
type: process
tags: [operations, pipeline, cron, health]
sources: [raw/agentforge/departments/]
created: 2026-07-31
updated: 2026-07-31
status: active
confidence: high
---

# Operations — Pipeline Runs, Cron Jobs, Health

## Active Cron Jobs
| Job | Schedule | Purpose |
|-----|----------|---------|
| content_pipeline_daily | Mon-Fri 08:30 | Article pipeline |
| analytics_weekly_report | Mon 09:00 | Weekly analytics |
| app_discovery_daily | Mon-Fri 06:00 | App scouting |
| BetterLife Daily Social | Daily 08:00 | Social media posting |
| Skill Foundry | Tue/Thu 06:00 | Skill development |

## Pipeline Health
```bash
# Check pipeline artifacts
ls ~/workspace/MeMex-Zero-RAG/wiki/agentforge/artifacts/content/2026/
ls ~/workspace/MeMex-Zero-RAG/wiki/agentforge/artifacts/seo/2026/
ls ~/workspace/MeMex-Zero-RAG/wiki/agentforge/artifacts/social/2026/

# Check cron health
openclaw task list
```

## Known Issues
- Part B fragmentation (image/PDF/SEO/git stages skipped)
- SEO API single-point-of-failure (recurring)
- Pipeline auto-post trigger missing (Phase 3 gap)
- Dual-write decay (MeMex↔HermesVault mirror)

## See Also
- [[departments/index]] — department operations
- [[board-directives]] — governance

> **Source:** SecondBrain Operations.md