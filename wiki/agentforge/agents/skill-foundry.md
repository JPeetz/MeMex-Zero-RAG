# Skill Foundry — Agent Registry

_Registered 2026-05-24. OpenClaw native._

## Agent Profile

- **ID:** skill-foundry
- **Name:** Forge
- **Role:** Director — Skill Foundry Department
- **Type:** Autonomous skill development, evaluation, packaging, and distribution
- **Activation:** Cron-scheduled, Tue/Thu 06:00 Dublin
- **Output:** Production-ready Agent Skills (SKILL.md + scripts + references + evals) published to GitHub + cross-client directories

## Pipeline

```
DISCOVER → EVALUATE → SELECT → IMPROVE → PACKAGE → VALIDATE → PUBLISH → MAINTAIN
```

8 phases per run.

### Phase 1 — Discovery
Web search across GitHub, community marketplaces, pain-point threads. Sources: GitHub search for SKILL.md repos, anthropics/skills, agent skill directories, developer pain-point analysis.

### Phase 2 — Evaluation
10-dimension scoring: Demand 15%, Pain 15%, Quality Gap 10%, Platform Portability 10%, Reusability 10%, Maintainability 10%, SEO/GEO 10%, Business Value 5%, Distinctiveness 10%, Safety 5%. Kill floor: 5/10 per dimension.

### Phase 3 — Selection + Taxonomy
Select top 5 (or fewer). Classify by: primary domain, secondary specialization, workflow type, platform targets, maturity, complexity, discoverability metadata, relationship graph.

### Phase 4 — Improvement
Analyze best existing examples → identify weaknesses → study deeply → apply best practices → document delta. Checklist: optimized description, body <500 lines, references with triggers, scripts for deterministic computation, evals (5+ test cases), corrections log, cross-platform notes.

### Phase 5 — Packaging
Full skill directory: SKILL.md + scripts/ + references/ + evals/ + LICENSE + CHANGELOG.md. Validate with validate_skill.py.

### Phase 6 — GitHub Operations
Review repo state, triage issues, create commits/PRs, update README/documentation. GitHub token routing through OpenClaw GitHub skill.

### Phase 7 — Discoverability
GitHub SEO (topics, descriptions), agent trigger keywords, cross-platform install paths. Distribution to ~/.agents/skills/ for cross-client portability.

### Phase 8 — Report
Run report to MeMex + Obsidian. Skills to MeMex artifacts + ~/.agents/skills/.

## Skill Quality Gate (Non-Negotiable)
- [ ] SKILL.md validates (frontmatter, name match, description <1024 chars, body <500 lines)
- [ ] Eval suite present (5+ test cases, mixed trigger/not-trigger, near-miss negatives)
- [ ] Corrections log present (real failures documented)
- [ ] Scripts self-contained (PEP 723 inline deps or equivalent)
- [ ] Cross-platform compatibility checked
- [ ] License file present
- [ ] Materially improved over source — never ship unimproved copies

## Cron
- **Job ID:** c8d17aac-f5c3-4020-b3a0-66af4eaf3f90
- **Schedule:** Tue/Thu 06:00 Europe/Dublin
- **Next run:** Tuesday May 26, 2026

## Integration
- **Input:** GitHub ecosystem, community skill repositories, pain-point analysis
- **Output:** Agent Skills → MeMex artifacts + ~/.agents/skills/ + GitHub repo
- **Upstream:** agentskills.io specification, Anthropic skills repo, community repos
- **Downstream:** All AgentForge agents (consumers), external platforms (distribution)