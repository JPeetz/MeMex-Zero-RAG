# Prompts Foundry — Playbook

_Lessons that carry forward across runs._

## What Works

## What Failed
- (none yet — all five runs successful)

## Prompt Structures That Perform

### Value-15 Prompts Still Benefit from Structural Refactoring
Even a 15/15 prompt (soul-md-template-official) with excellent content can gain significant value from TOML handoff, three-mode architecture, and constraint tables — the improvement is in usability and discoverability rather than the content itself. Mode labels should reflect the *agent's action domain* not the prompt category: AUDIT/FORGE/EVOLVE for identity work, AUDIT/OPTIMISE/MAINTAIN for cost engineering, INSTALL/CURATE/EVOLVE for memory systems.

### Token Ceiling Tables are the New Pattern
Cost-control and memory-refactoring prompts both benefit from hard token ceilings per section with pruning order. This is the natural extension of constraint tables into quantitative guardrails — agents can compute rather than guess. Budgetary prompts (cost, memory, context) should always include a token ceiling table with priority-ordered pruning rules.

### Three Skeleton Archetypes
Three types of skeleton prompts identified across the vault:
1. **Core insight skeletons** (like cost-control, stop-engineering) — have one genuinely good idea, wrapped in generic structure. Best ROI: extract the insight, rebuild everything else.
2. **Already-complete content** (like soul-md, ten-soul-md-templates) — need structural packaging, not content changes. Quick wins.
3. **Practical tool skeletons** (like memory hack, awesome-openclaw-skills) — correct mechanics, missing architectural depth. Add priority matrices, escalation paths, and evaluation criteria.

### Domain-Adapted Mode Labels are the Stable Pattern
AUDIT/OPTIMISE/MAINTAIN (cost control/resource prompts), DESIGN/EVALUATE/DEPLOY (identity/template prompts), SEARCH/EVALUATE/INSTALL (catalog/discovery prompts) — the three-mode pattern is a constant across all categories, but vocabulary must adapt to the domain. Catalog prompts map to the user journey (find → compare → use).

### OpenClaw Category Complete (14 prompts, 5 runs)
The category had 8 of 14 prompts with value_score ≤12 (skeleton/catalog type). Real ROI came from transforming core-insight skeletons into production systems. Moving to coding category next.

## What Works
- **Role-naming agents** (Savings, Soulsmith, Mnemosyne) makes prompts deeply memorable. The identity-first approach anchors the behavior.
- **Token ceiling tables with pruning order** are the highest-value addition for any resource-constrained prompt type (memory, cost, context).
- **Provider-specific caching rules** (Anthropic vs OpenAI vs OpenClaw-native) make cost prompts actionable rather than theoretical.

## Seed Progress Notes
- 52 existing prompts in Obsidian vault to refactor across 12 categories
- Run 1 (2026-05-27): 3 prompts published from openclaw — all scored 12-14/15 original, rebuilt to 15/15
- Run 2 (2026-05-28): 3 more from openclaw (indices 3-5) — clawsec-security-suite (14→15), hardened-openclaw-setup (13→15), founder-automation-workflows (12→15)
- Run 3 (2026-05-29): 3 more from openclaw (indices 6-8) — agent-prompts-researcher-writer-coder (14→15), bootstrap-files-design-guide (14→15), heartbeat-soul-memory-config-guide (14→15)
- Run 4 (2026-05-30): 3 more from openclaw (indices 9-11) — prompt-caching-cost-control (10→15), soul-md-template-official (15→15), recursive-memory-hack (10→14)
- Run 5 (2026-05-31): Final 3 from openclaw (indices 12-14) — stop-engineering (10→15), ten-soul-md-templates (14→15), awesome-openclaw-skills (13→15)
  - **OpenClaw category complete** (14/14 prompts published in 5 runs)
  - stop-engineering: core-insight skeleton (cognitive RAM concept) → full AUDIT/OPTIMISE/MAINTAIN cost-control system with token ceiling table + ordered pruning rules
  - ten-soul-md-templates: meta-schema + 10 production-ready archetypes (CEO, Writer, Developer, Analyst, Support, Researcher, Teacher, Creative, Strategist, QA) with DESIGN/EVALUATE/DEPLOY mode architecture
  - awesome-openclaw-skills: catalog search → SEARCH/EVALUATE/INSTALL user-journey modes with evaluation criteria and 3 installation methods
- Next run: coding category (10 prompts, indices 0-2)

## Prompt Structures That Work
- **Three-mode architecture** (QuickMatch / SolutionBuild / Explore) maps naturally to discovery agents — user can browse, solve, or get fast answers
- **Handoff protocol** (input_from / output_to in TOML) prevents silent failures in multi-agent swarms. Must be bidirectional — if A outputs to B, B must input_from A.
- **Constraint tables** (Anti-Patterns, Escalation, Language-Specific) reduce ambiguity better than narrative paragraphs. Column format = easier for agents to parse at inference time.
- **Domain-adapted mode labels** — three-mode architecture works, but mode names should adapt to category: DESIGN/EVALUATE/DEPLOY (agents), GENERATE/AUDIT/MERGE (bootstrap files), DESIGN/OPTIMIZE/MAINTAIN (runtime config). The pattern is the constant; the vocabulary is the variable.

## Cross-Platform Adaptation Patterns
- Original prompts all have generic placeholder titles ("O", "A", "C", "H") and generic descriptions — refactoring adds specific, searchable slugs and real use-case descriptions
- Obsidian vault prompts mix two states: (1) proper system prompts with actual agent behavior, and (2) catalog skeletons with only schema placeholders. The skeletons need complete category-level content — not just structure
- Platform-specific constraints (Discord tables, Twitter char limits, LinkedIn tone) should be baked into the prompt, not left as reader assumptions

## What Works
- **7-step process** (IDENTIFY → ANALYZE → BENCHMARK → REDESIGN → VALIDATE → PACKAGE → PUBLISH) correctly catches skeleton prompts that have inflated value scores
- **Parallel file reads** (read 3-5 prompts upfront) reveals patterns before redesign — the "agent-based prompt catalog pattern" (title O/A/C, generic description, placeholder table) appears in ~30% of vault prompts
- **Templates-as-code** (TOML in the prompt itself) reduces ambiguity — agents can grep the format rather than parse narrative
- **Three-mode architecture** (QuickMatch/SolutionBuild/Explore) works particularly well for prompts that had linear protocols — restructuring to modes adds 1-3 value points by giving agents mode-switching behavior
- **Vault prompts with value_score 12-14** (non-skeleton) have real agent behavior that just needs better packaging — not a full rewrite, but a restructuring and TOML enrichment. These are the most productive targets.
- **Category-abstracted mode labels work best** — instead of forcing QuickMatch/SolutionBuild/Explore on every category, adapt mode names to the domain: DESIGN/EVALUATE/DEPLOY for agent templates, GENERATE/AUDIT/MERGE for bootstrap files, DESIGN/OPTIMIZE/MAINTAIN for runtime config. The pattern holds, the vocabulary adapts.
- **Constraint tables (Anti-Patterns, Decision Matrices) are the highest-value addition** — they directly prevent failure modes the agent would otherwise discover at runtime. Every published prompt now includes one.
- **Bidirectional handoff in TOML** (input_from + output_to) prevents silent failures in multi-agent contexts. This is now standard in all role-archetype prompts.
