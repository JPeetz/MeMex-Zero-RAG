# Project: SkillForge

> Open-source skill lifecycle management platform. Combines SkillClaw + Skill Foundry.
> **Status:** 📝 Design stage (Superpowers methodology)
> **Related:** [[Research]], [[Lessons-Learned]]

---

## Architecture

```
Capture → Evolve → Quality Gate → Publish
             ↓
         Skill Foundry Review
```

## Components

| Phase | SkillClaw Module | Skill Foundry Phase |
|-------|-----------------|---------------------|
| DISCOVER | skill_hub.py, nacos_skill_hub.py | — |
| EVALUATE | prm_scorer.py, validation_store.py, session_judge.py | — |
| SELECT | — | Skill Foundry gates |
| IMPROVE | pipeline/summarizer.py, aggregation.py, execution.py | — |
| PACKAGE | skill_bundle.py, agent_workspace.py | — |
| VALIDATE | validation_worker.py, skill_verifier.py, prm_scorer.py | — |
| PUBLISH | — | GitHub ops |
| MAINTAIN | Proxy + evolve server | Continuous loop |

## Decision (2026-07-14)

**Enhance, don't replace.** SkillClaw drafts proposals → Skill Foundry reviews/approves. Complementary.

## Three-Layer Integration

1. **Light** — SkillClaw pipeline on existing sessions → draft proposals → Skill Foundry reviews
2. **Medium** — Proxy on CEO agent → real session data → evolution
3. **Full** — Proxy on all agents → continuous improvement loop

## Design Doc

`docs/superpowers/specs/2026-07-14-skillforge-design.md` (12.9KB)
