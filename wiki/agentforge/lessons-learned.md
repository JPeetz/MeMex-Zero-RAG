---
title: Lessons Learned
type: reference
tags: [lessons, gotchas, patterns, failures]
sources: [raw/agentforge/departments/lessons-learned.md]
created: 2026-07-31
updated: 2026-07-31
status: active
confidence: high
---

# Lessons Learned — Gotchas, Patterns, Failures

## Critical Patterns

### Always Use Absolute Paths (2026-07-17)
Script file arguments must use absolute paths — exec may not have the expected CWD. Relative paths silently fail.

### Failure Auto-Resolution (2026-07-15)
When anything fails: research memory → fix → finish. Escalate only after 3 consecutive failures.

### Duplicate Posts Due to Cron Timeout Loop (2026-07-13)
- Root cause: 600s timeout inadequate; cron marks "error" and retries → duplicate posts
- Fix: 600s → 900s + idempotency guard

### Pipeline Gap — No Auto-Post After Approval (2026-07-06)
Cron generates images + submits for review but stops. No Phase 3 picking up approval to trigger posting. Still needs a mechanism.

### SEO API Single-Point-of-Failure (2026-06-01)
API down → 6 articles un-audited. Fixed by redeploying stale Vercel build.

### Caption CLI Leak Bug (2026-07-29)
Old `bl-post-everywhere.py` used single `CAPTION = sys.argv[2]` — passing `--ig "text"` set CAPTION to `--ig`, posting that literal string everywhere. Fixed with `--captions-md FILE --variant N` mode.

### Marketing Image Generation (2026-07-31)
- ALWAYS image-to-image with Mira references — never text-to-image
- "Not Mira!!!!" means the woman doesn't look like Mira — not "remove the person"
- All 20 reference images in selection pool; prompt decides which 8 fit each variant
- If Mira is not alone, others must be random/not recognizable

## See Also
- [[learning-loop]] — reflection process
- [[board-directives]] — protocols
- [[decisions]] — decision log

> **Source:** SecondBrain Lessons-Learned.md