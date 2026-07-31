---
title: AgentForge Content Pipeline — operations manual
tags: [project, agentforge, seo, pipeline, content]
created: 2026-05-21
updated: 2026-07-31
status: active
---

# AgentForge Content Pipeline — Operations Manual

> Daily article pipeline — keyword to published article with SEO/GEO quality gate.
> **Source:** SecondBrain (merged into HermesVault 2026-07-31)
> **Related:** [[Departments]], [[Operations]], [[seo-content-pipeline]], [[seo-gate]]

---

## Pipeline Stages

| Stage | Description | Gate |
|-------|-------------|------|
| 1. Keyword | Research from cluster, SEO API | — |
| 2. Article | Write 3,000+ word article | — |
| 3. SEO Audit | Score 0-100 | PASS ≥70 |
| 4. GEO Audit | Entity density, answer structure, quotability, E-E-A-T | Advisory |
| 5. Revision | Auto-revision if FLAG (50-69) | Max 3 cycles |
| 6. PDF | Generate print-ready PDF | — |
| 7. Social | 5-platform distribution | CEO review if <80 |
| 8. WordPress | Publish to site | — |

## FLAG Protocol (Auto-Revision)

- **Score 50-69:** Auto-revision cycle triggered
- Content Agent revises based on audit feedback
- Re-audit. Loop until PASS (≥70)
- Escalate to Board only after 3 consecutive FLAGs
- **Proven:** 1 cycle, +14 points (65→79 on 2026-05-23)

## Content Agent Self-Improvement (Positive)

From Run #2 onward, content agent self-applies pre-SEO checks WITHOUT external gate:
- Meta descriptions
- Hyperlinks
- Readability interludes
- GEO blocks

## Known Issues

| Issue | Status | Note |
|-------|--------|------|
| SEO API single-point-of-failure | 🔴 Recurring | API down May 29 — 6 articles un-audited |
| Part B fragmentation | 🟡 Ongoing | Image/PDF/SEO/git stages consistently skipped |
| Dual-write decay | 🟡 Ongoing | MeMex→Obsidian mirror degrades between reports |

## Pipeline History

| Date | Article | SEO | Status |
|------|---------|-----|--------|
| 2026-05-23 | AI Agent Orchestration | 65→79 (PASS) | ✅ Published |
| 2026-05-29 | AI Agent Security 2026 | 89 (PASS) | ✅ Published |
| 2026-05-23-29 | 6 articles total | 65→78→90% avg | ✅ 5/5 runs |
