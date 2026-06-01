# Skill Foundry — Playbook

_Lessons that carry forward across runs._

## What Works
- **SkillsMP API** is the best discovery source — structured metadata, star counts, GitHub links. Use 5-7 keyword queries covering different categories.
- **10-dimension scoring** effectively separates wheat from chaff. Kill floor of 5/dim works well; no false positives survived.
- **Decision tables** ("When to use / When not to use") in every skill — dramatically reduces false-trigger risk and keeps SKILL.md under 500 lines.
- **Script reference in SKILL.md** required to pass the validation gate; always add a `## Scripts` section listing each script with a one-liner example.
- **Legal/regulatory context** (EU Accessibility Act) adds urgency and SEO lift to skills that support it.

## What Failed (First Run)
- **No prior runs existed** — playbook was blank. First run was full discovery. Future runs can reference patterns.
- **Validator stricter than expected** — missing `version`, `license`, `compatibility`, `platforms` frontmatter fields fail validation. Add these proactively.
- **Section naming matters** — validator expects `## Platform Notes` not `## Cross-Platform Notes`.

## Improvement Patterns That Stick
1. **Build from existing community skills** — remix + improve rather than writing from scratch. Quality delta of +40-60% is achievable.
2. **Scripts should be deterministic** — Python for computation (contrast ratios, EXPLAIN analysis), bash for orchestration. PEP 723 inline deps preferred.
3. **7 test cases minimum** — mix of triggers (3), non-triggers (2-3), and near-miss boundaries (1-2).
4. **CHANGELOG.md documents the delta** — makes review and versioning clear.
5. **Cross-platform notes** required for all skills — list agent hosts and OS compatibility.

## Lessons from nightly-2026-05-28
1. **10 test cases with broader categories** (trigger, positive, violation, warning, boundary, stability, flaky-fix) provide better coverage than 7 test cases with only trigger/non-trigger/boundary. The flaky-snapshot fix pattern in advanced-testing-toolkit was particularly effective.
2. **Pairing competing community skills** (e.g., CybLow test-advanced 1★ + PramodDutta mutation-testing-advanced 122★) produces stronger unified skills than either source individually. The unified approach with a decision table covering all 4 testing methodologies is a distinct value-add no single community skill offers.
3. **204 No Content edge case** matters for spec validation — tools that penalize 2XX without body miss this pattern. Always add the 204 exception in validation logic.
4. **SkillsMP AI-search** produced much better results than keyword search for all categories tested. Use AI-search by default, fall back to keyword search.
5. **Deeper gap analysis before killing** — MLOps and WordPress were the strongest killed candidates but overlapped too much with existing skills. Future runs should check existing skills directory first and calculate delta potential before final score.

## Underserved Categories (prioritize these)
- ~~OpenAPI / API specification generation~~ ✅ Done (openapi-spec-generator 1.0.0)
- ~~Docker Compose patterns (production-grade)~~ ✅ Done (docker-compose-patterns 1.0.0)
- ~~Testing methodology expansion (property-based, mutation, snapshot)~~ ✅ Done (advanced-testing-toolkit 1.0.0)
- AI/ML pipeline development (training, evaluation, deployment) — **revisit after gap analysis**
- WordPress theme/plugin development — **revisit after gap analysis**
- ~~Accessibility beyond web (mobile, native apps)~~ ✅ Done (mobile-accessibility-native 1.0.0)

## Discovery Sources Ranked
1. ✅ **SkillsMP API (AI-search)** — highest signal-to-noise, structured data
2. ✅ **SkillsMP API (keyword search)** — good fallback, lower recall
3. ✅ **Web search (Tavily)** — good for emerging trends and community discussion context
4. ◐ **GitHub direct** — useful for reference implementations, low for discovery
5. ❌ **Raw community repos** — too much noise to parse efficiently

## Lessons from nightly-2026-05-30
1. **Unify — never write from scratch.** The nlp-engineering skill unified 4 top community skills (815★+159★+135★+115★) into one pipeline. The unified result is stronger than any single source because each had different strengths (sentiment vs NER vs semantic search vs traditional NLP). Pair complementary strengths from different authors.
2. **Kill on overlap, not quality.** The CI/CD skill (227★ source, high scoring) was killed because AgentForge already has `devops-cloud-infrastructure` and `deployment-automation`. Check existing skills directory explicitly before final selection — a 90-point skill that duplicates existing coverage is worse than a 70-point skill that fills a genuine gap.
3. **AI/ML is the highest-value category in 2026.** MLOps is ranked the #1 skill for 2026 AI engineers, and the NLP market is $34.8B. Skills in this category score higher on Demand (14-15/15) than DevOps categories (10-12/15). Prioritize AI/ML categories when multiple options score similarly.
4. **The validator wants specific section names.** `## Overview`, `## Instructions`, and `## Examples` are required after the frontmatter. Adding these retroactively is easy but pre-building them saves a fix cycle. Always write: Overview → Instructions → When to Use/Not → Examples → main content.
5. **10-dim scoring with overlap penalization** — added explicit overlap check before final score. A skill that fills a genuine gap gets a +5 distinctiveness bonus; a skill that overlaps with existing skills gets a -5 penalty. This prevents filling the skills directory with overlapping near-duplicates.

## New Underserved Categories (prioritize for next run)
- ~~Data visualization~~ ✅ Done (data-visualization 1.0.0)
- ~~ML pipeline / MLOps~~ ✅ Done (ml-pipeline 1.0.0)
- ~~NLP engineering~~ ✅ Done (nlp-engineering 1.0.0)
- RAG system architecture (community gap, high demand)
- Time-series forecasting (emerging 2026 trend)
- Observability/monitoring (Prometheus, Grafana, Datadog — thin market)