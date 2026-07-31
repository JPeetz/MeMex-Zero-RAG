# SkillForge — Combined SkillClaw + Skill Foundry Repo

**Status:** Design stage (Board review pending)
**Date:** 2026-07-14
**Design doc:** `~/workspace/docs/superpowers/specs/2026-07-14-skillforge-design.md`

## Overview

Open-source skill lifecycle management platform combining:
- **SkillClaw** (AMAP-ML) — session capture via proxy, auto-evolution pipeline
- **Skill Foundry** (AgentForge) — quality gate, adversarial review, GitHub publishing

## Architecture

```
Capture → Evolve → Quality Gate → Publish
 (proxy)  (pipeline)   (review)     (GitHub)
```

## Three Integration Layers

1. **Light** — SkillClaw pipeline on archived sessions → drafts → Skill Foundry reviews
2. **Medium** — Proxy on CEO agent → real session data → evolution
3. **Full** — Proxy on all agents → continuous improvement loop

## Module Map

| Layer | SkillClaw Sources | Skill Foundry Sources |
|---|---|---|
| Capture | api_server.py, claw_adapter.py, session_store.py | — |
| Evolve | pipeline/*, engines/*, skill_manager.py | — |
| Quality | prm_scorer.py, validation_store.py, validation_worker.py | 10-dim eval, adversarial review, skill_workshop |
| Publish | — | GitHub ops, README/CHANGELOG/DEVLOG, SEO/GEO |

## Key Links

- SkillClaw GitHub: https://github.com/AMAP-ML/SkillClaw
- Design doc: `~/workspace/docs/superpowers/specs/2026-07-14-skillforge-design.md`
- arXiv paper: https://arxiv.org/abs/2604.08377

## Migration Phases

| Phase | Duration | Action |
|---|---|---|
| Phase 1 — Packaging | Week 1 | Fork repo, structure, wire CLI |
| Phase 2 — Validation | Week 2 | Run Layer 1, compare output |
| Phase 3 — Launch | Week 3 | Open-source, Layer 2 proxy |
| Phase 4 — Scale | Ongoing | All agents, dashboard, Nacos |