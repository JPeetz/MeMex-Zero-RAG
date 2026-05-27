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

## Underserved Categories (prioritize these)
- OpenAPI / API specification generation
- Docker Compose patterns (production-grade)
- Testing methodology expansion (property-based, mutation, snapshot)
- AI/ML pipeline development (training, evaluation, deployment)
- WordPress theme/plugin development
- Accessibility beyond web (mobile, native apps)

## Discovery Sources Ranked
1. ✅ **SkillsMP API** — highest signal-to-noise, structured data
2. ✅ **Web search (Tavily)** — good for emerging trends and Reddit discussions
3. ◐ **GitHub direct** — useful for reference implementations, low for discovery
4. ❌ **Raw community repos** — too much noise to parse efficiently