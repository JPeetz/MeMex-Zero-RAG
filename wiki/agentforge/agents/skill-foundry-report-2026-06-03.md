# Skill Foundry — Nightly Run Report 2026-06-03

**Date:** 2026-06-03 02:00 IST (Europe/Dublin)
**Director:** Forge

## Summary

3 skills produced, 0 killed. All three categories were clean gaps — no overlap with existing skills directory (checked explicitly).

## Discovery

12 candidates surfaced across 5 categories using SkillsMP keyword search + web search:
- **RAG Architecture**: borghei/rag-architect (204★), neverinfamous/rag-pipelines (17★), Miaoge-Ge/rag-expert (4★), yonatangross/rag-retrieval
- **LLM Guardrails**: mukul975 (12,624★), xalgord (526★), AgentFlocks (351★)
- **Observability**: yonatangross/monitoring-observability (179★), ahmedasmar (165★), Tibsfox (62★)
- **Time-Series Forecasting**: jeremylongshore (2,267★), anthropics (674★), pjt222 (20★)
- **CI/CD Pipeline**: rohitg00 (1,895★), revfactory (838★), LambdaTest (299★)

## Evaluation & Selection

Killed categories after gap analysis:
- **CI/CD Pipeline** → AgentForge already has `deployment-automation` and `devops-cloud-infrastructure`. Overlap is >60%. Score was high (84/100) but -5 overlap penalty and +0 distinctiveness.
- **Time-Series Forecasting** → jeremylongshore source is 2,267★ but the SKILL.md itself is weak (3.8KB, generic content). The anthropics source is better (674★) but narrow (SKU demand only). Gap exists but quality delta from community sources is low. Score 62/100.

Top 3 selected (all passed 10-dim scoring with kill floor 5/10):

| Skill | Score | Distinctiveness | Overlap Penalty | Final |
|-------|-------|----------------|-----------------|-------|
| **rag-system-architecture** | 93/100 | +5 (RAG gap) | 0 | **98** |
| **llm-guardrails-security** | 94/100 | +5 (AI security gap) | 0 | **99** |
| **observability-monitoring** | 87/100 | +5 (observability gap) | 0 | **92** |

## Skills Produced

### 1. rag-system-architecture (1.0.0)
- **Sources**: borghei/rag-architect (204★) + neverinfamous/rag-pipelines (17★) + Miaoge-Ge/rag-expert (4★)
- **Size**: 14.5KB
- **Key additions over source**: Decision table (when to use/not), CI-embedded eval pattern, resilience case for corrupted index, cross-platform notes, integration points
- **Test coverage**: 9 cases (3 trigger, 3 non-trigger, 2 boundary, 1 resilience)

### 2. llm-guardrails-security (1.0.0)
- **Sources**: mukul975 (12,624★) + xalgord (526★) + AgentFlocks (351★)
- **Size**: 13.3KB
- **Key additions**: OWASP LLM Top 10 mapping table (every guardrail → security category), multilingual injection handling, fail-closed pattern, benchmark script
- **Test coverage**: 9 cases

### 3. observability-monitoring (1.0.0)
- **Sources**: yonatangross/monitoring-observability (179★) + ahmedasmar (165★) + Tibsfox (62★)
- **Size**: 14.6KB
- **Key additions**: Cardinality management, alert fatigue prevention, Langfuse cost optimization with sampling, 200-service architecture template, stack self-health monitoring
- **Test coverage**: 9 cases

## What Worked
1. **Gap-first discovery**: Starting with underserved categories from playbook + scanning existing skills before scoring eliminated false positives early. Zero false starts this run.
2. **Unifying 3 complementary sources per skill**: RAG combined architect-level design (borghei) + practical pipeline patterns (neverinfamous) + chunking/embedding details (Miaoge-Ge). Each source contributed a different strength.
3. **SkillsMP keyword search + web_fetch on raw GitHub**: Directly reading source SKILL.md files from GitHub was the fastest quality assessment method. No need for AI-search endpoint now.

## What Failed
1. **SkillsMP AI-search endpoint dead**: The `/api/v1/skills/ai-search` endpoint previously documented has been removed. Only `/api/v1/skills/search` (keyword) is available. The playbook should be updated to reflect this.
2. **Time-Series category still weak**: Despite being flagged as underserved, community skills are either generic/low-effort or hyper-specific (SKU demand only). No strong source exists to unify. Skip until a better source emerges.

## What's Next
- RAG system architecture can integrate with `ml-pipeline` and `nlp-engineering` for combined ML+RAG workflows
- LLM guardrails complements `security-auditing` — consider a combined audit workflow
- Observability should be wired into deployment automation for new services