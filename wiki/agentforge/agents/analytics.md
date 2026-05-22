# Analytics Agent

- **Agent ID:** analytics
- **Role:** Weekly performance analysis, niche refresh, cluster map
- **Position:** Weekly cycle — reads all pipeline artifacts, produces intelligence
- **Trigger:** Cron: Monday 09:00 IE (job: analytics_weekly_report)
- **Handoff Produces:** analytics.weekly-report
- **Handoff Routes To:** CEO (recommendations)
- **Model:** openrouter/deepseek/deepseek-v4-pro (thinking: high)
- **Skills:** superpowers, handoff (Tier 2), writing-plans
- **Source:** ClaudeClaw analytics/CLAUDE.md
- **Workspace:** ~/.openclaw/agents/analytics/workspace/

*Activated: 2026-05-22 — Tier 1 Deployment*
