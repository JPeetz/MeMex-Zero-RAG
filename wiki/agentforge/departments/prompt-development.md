# AgentForge — AI Prompt Development Department
## Full specification: research, curate, analyse, optimize, store, publish AI prompts

**Source:** Board directive, 2026-06-09
**Department name:** Prompt Development (PD)
**Department head:** prompts-cmo
**Reports to:** Marvin (CEO)
**Cooperates with:** agentforge-cmo (content) and wpmd-cmo (bundles)
**Storage:** Memex (primary) + Obsidian vault (mirror) + MD files (GitHub-ready)
**Output streams:** Articles for agentforge-cmo + bundles for wpmd-cmo + open-source repos

---

## Department Overview

Systematically discovers, curates, analyses, optimizes, and distributes high-value AI prompts. Feeds two revenue streams (content articles and sellable bundles) and one community contribution stream (open-source prompt collections).

### Core focus areas

**Tool-specific:** OpenClaw, Hermes, Claude Code, Codex CLI

**Use-case:** YouTube automation, AI social media, content creation, agent swarms, coding, research, trading, image gen (FLUX, SDXL), voice/TTS, video gen, customer support, email/calendar, project mgmt

---

## Department Org Chart

```
MARVIN (CEO)
 →
prompts-cmo (Dept Head — DeepSeek V4 Flash)
 ├── prompt-researcher (Gemma4 9B local) — Reddit, GitHub, X, forums, Discord, YouTube
 ├── prompt-curator (Gemma4 9B local) — dedup, categorise, tag, store raw
 ├── prompt-analyst (DeepSeek V4 Pro) — assess value, use case fit, QA
 ├── prompt-optimizer (DeepSeek V4 Pro) — A/B testing, iterative improvement
 ├── prompt-tool-builder (Qwen3.6 35B A3B) — custom tools, dormant when not needed
 └── prompt-archivist (Gemma4 9B local) — final storage Memex + Obsidian + MD, GitHub publish
```

**Cooperation:** prompts-cmo ←→ agentforge-cmo (article requests) | prompts-cmo ←→ wpmd-cmo (bundles)

---

## Weekly Workflow

| Day | Agent | Action |
|---|---|---|
| Tuesday 08:00 | prompt-researcher | Scan 10+ sources, gather raw prompts |
| Wednesday 09:00 | prompt-curator | Deduplicate, categorise, tag |
| Thursday 09:00 | prompt-analyst | Multi-criteria scoring (0-15), test outputs |
| Friday 09:00 | prompt-optimizer | A/B test, iteratively improve (target +10-30% improvement) |
| Saturday 09:00 | prompt-archivist | Final storage, bundle check (50+ = notify wpmd-cmo), GitHub publish |
| Monday 13:00 | prompts-cmo | Weekly report to Marvin |

---

## Scoring System

5 criteria × 3 points each = 15 max. 10+ = high-value flag:
- Clarity (0-3), Specificity (0-3), Reusability (0-3), Demonstrated Effectiveness (0-3), License Compatibility (0-3)

## Optimization Techniques

Role clarity, output structure, chain-of-thought, few-shot examples, constraints, token efficiency

## Bundle Trigger

50+ optimized prompts in a use-case category → notify wpmd-cmo for WooCommerce product creation

## Cost

~$2.40/month at $40 OpenRouter budget

## The Flywheel

Week 1: 10 raw → 5 optimized → 1 article | Week 12: 120 raw → 100 optimized → 12 articles → 2 bundles → GitHub repo
Competitive moat: optimised, tested, categorised, attributed prompts curated weekly.

---

*AgentForge AI Prompt Development Department v1.0 — 7 agents, weekly cadence, Memex-categorised, GitHub-publishable*
