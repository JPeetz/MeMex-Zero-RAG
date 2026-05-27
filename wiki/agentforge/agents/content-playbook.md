# Content Pipeline — Playbook

_Lessons that carry forward across pipeline runs. Read before each run, update after._

## Architecture (as of 2026-05-27)
- **Part A (08:30):** keyword → article → image prompt only. Article .md + artifacts written to MeMex.
- **Part B (09:15):** image generation → pipeline copy → PDF → SEO audit → git commit. Tool-heavy, must complete all steps.
- Split because single cron failed at image generation — the model writes the full article then considers task "done."
- Never put image_generate + article writing in the same cron — tool generation commands need their own isolated run.

## What Works
- Keyword research with SEO API produces strong clusters
- Series format (Orchestration → Governance → Evaluation → Deployment) builds editorial momentum and internal link equity
- GEO blocks (definition, FAQ, quotable summary, featured image) consistently met
- Article quality: 2,800-3,000 words, 10-11 H2s, 15+ hyperlinks, 2+ tables

## What Failed
- Run #4 (May 27): image generation, SEO audit, PDF all skipped — cron completed after writing article draft
- Root cause: single cron asking for 6 tool-heavy stages in one prompt. Model writes 3,000 words then returns.
- Fix: split into Part A (text) + Part B (tools). Effective immediately.

## Image Prompts That Scored Well
- Run #4: "Enterprise AI agent deployment infrastructure visualization. Dark blue technological dashboard, glowing nodes, Kubernetes-style cluster, central holographic globe, blue and teal gradients." — Generated well on gemini-3.1-flash-image-preview.

## SEO Patterns
- FLAG (50-69): auto-revision typically 1 cycle to PASS. Common fixes: add meta description, hyperlinks, improve Flesch score.
- Title <60 chars for SERP. Meta description 150-160 chars with keyword + CTA.
- B2B enterprise articles naturally score Flesch 24-35 — this is acceptable for technical/CTO audience

## Keyword Clusters That Performed
- "AI agent production deployment scaling enterprise" — Run #4, high commercial intent, 4,800-7,200/mo combined
- Series cross-linking boosts cluster authority across runs

## Pipeline Timings
- Part A: ~6-8 minutes (keyword research + article writing)
- Part B: ~8-12 minutes (image gen + PDF + SEO + git)
- Total pipeline: ~15-20 minutes fully automated