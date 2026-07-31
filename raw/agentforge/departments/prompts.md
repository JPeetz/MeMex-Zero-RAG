# Department: Prompt Development

> **Lead:** Prompts CMO
> **Created:** 2026-06-09 (Board directive)
> **Related:** [[Departments]]

---

## Structure (7 Agents)

| Agent | Model | Role |
|-------|-------|------|
| Researcher | Gemma4 | Finds prompt patterns, techniques |
| Curator | Gemma4 | Filters and categorizes |
| Analyst | V4 Pro | Scores and evaluates |
| Optimizer | V4 Pro | Improves prompts |
| Tool-builder | Qwen3.6 35B | Builds prompt tools |
| Archivist | Gemma4 | Documents and archives |
| Reports | — | Weekly summary |

## Weekly Cycle

| Day | Activity |
|-----|----------|
| Tuesday | Research |
| Wednesday | Curation |
| Thursday | Analysis |
| Friday | Optimization |
| Saturday | Archival |
| Monday | Report |

## Scoring System

- 5 dimensions, 0-15 scale
- Score ≥10 triggers optimization pipeline
- Dimensions: clarity, specificity, structure, creativity, effectiveness

## Revenue Model

1. **Content dept** — prompts used in articles
2. **Bundles** — 50+ prompts → WooCommerce product → €19-49
3. **GitHub** — open-source repos for recognition

## Cost

~$2.40/month on current $40 OpenRouter budget.

## Flywheel Projection

Week 1: 10 raw → Week 24: 200+ optimized → 4-5 bundles live → recognized source

---

## AdForge System Prompt v2.0 — Advertising Creative Workflow (2026-06-19)

A superhuman system prompt replicating Foreplay.co's complete ad creative workflow. Candidate for the prompts department — could be productized as an agent skill or bundled prompt.

### 8-Part Structure
1. **Classification Engine** — Format, Angle, Hook Type, Persona, Emotional Arc
2. **Longevity Weighting Formula** — Runtime-based performance proxy for competitor ads
3. **Creative Test Detection** — Clustering algorithm to detect A/B test variables
4. **Hook Extraction Reasoning Chain** — Verbatim → classify → score → extract → adapt
5. **Performance Scoring Heuristics (Lens)** — Account baseline → funnel diagnostic → break point → performance tiers
6. **Reasoning Chains** — Competitor analysis, What to test next, Find inspiration
7. **Brief Generation Intelligence** — 5-Beat Script Structure + Hook Generation Algorithm
8. **Integrated Workflow** — Research → Analytics → Brief → Close the Loop

### Key Principles
- Runtime = spend signal (longevity as performance proxy)
- Simplicity + specificity = longevity (conversational outlasts copywriter-crafted)
- One variable per test
- Break point first, solution second
- Always 5 hook options, never 1
- Every recommendation cites evidence (Longevity Score or Performance Tier)

**Source:** MeMex `concepts/adforge-system-prompt-v2.md`
**Full document:** `~/workspace/SecondBrain/Concepts.md`

---

## Full Prompt Development Department Spec (MeMex)

### Core Focus Areas
- **Tool-specific:** OpenClaw, Hermes, Claude Code, Codex CLI
- **Use-case:** YouTube automation, AI social media, content creation, agent swarms, coding, research, trading, image gen, voice/TTS, video gen, customer support, email/calendar, project mgmt

### Department Org Chart (Detailed)
```
MARVIN (CEO) → prompts-cmo (Dept Head — DeepSeek V4 Flash)
 ├── prompt-researcher (Gemma4 9B local) — Reddit, GitHub, X, forums
 ├── prompt-curator (Gemma4 9B local) — dedup, categorise, tag
 ├── prompt-analyst (DeepSeek V4 Pro) — assess value, use case fit, QA
 ├── prompt-optimizer (DeepSeek V4 Pro) — A/B testing, iterative improvement
 ├── prompt-tool-builder (Qwen3.6 35B A3B) — custom tools
 └── prompt-archivist (Gemma4 9B local) — final storage, GitHub publish
```

**Cooperation:** prompts-cmo ↔ agentforge-cmo (article requests) | prompts-cmo ↔ wpmd-cmo (bundles)

**Output streams:** Articles (for content dept) + Bundles (WooCommerce, €19-49) + Open-source repos (GitHub)
