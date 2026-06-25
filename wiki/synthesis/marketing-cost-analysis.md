---
title: Marketing Department Cost Analysis
type: synthesis
tags: ["cost", "marketing", "video", "lessons-learned", "model-tiers"]
created: 2026-06-25
author: marvin
---

# Marketing Department Cost Analysis — BetterLife Video Production

**Date:** 2026-06-25 | **Author:** Marvin (CEO)  
**Trigger:** $30 burned across 5 failed video production attempts

## What Happened

5 video production attempts ($28-30 total) all failed to produce the quality Joerg wanted. The approach — spawning expensive Claude Sonnet subagents to do full video production (FLUX + Remotion + FFmpeg) — was fundamentally wrong.

## Root Cause

Video production tasks (FFmpeg, image compositing, rendering) are **EXECUTION** tasks, not reasoning tasks. Paying Claude Sonnet $8-15/M tokens to "think about" how to run ffmpeg is wasteful.

## The Fix: $0-First Rule

1. Can I write a shell/Python script? → Do it myself. $0.
2. Can a cheap model (Gemini Flash, $0.15/M) do it? → Use that.
3. Only spawn expensive models for genuine reasoning tasks.

## Model Tier System

| Tier | Cost/M output | Models | Use For |
|---|---|---|---|
| 1 — Local | $0 | shell, python, ffmpeg | All execution tasks |
| 2 — Cheap | $0.05-0.30 | Gemini Flash, Llama 8B | Captions, prompts, formatting |
| 3 — Medium | $2-5 | DeepSeek V4 Pro, GPT-4.1 | Strategy, complex scripts |
| 4 — Expensive | $8-15 | Claude Sonnet/Opus | Architecture, deep debugging only |

## Subagent Rules

1. Briefs ≤500 words
2. Single task per subagent
3. Cheapest capable model
4. No reasoning about shell commands — run them directly

## Video Strategy Going Forward

- Kling/Runway API for real video clips ($1-2 each)
- FFmpeg assembly ($0, local)
- macOS `say` for narration ($0, local)
- Target: $2-4 per promo video, not $30