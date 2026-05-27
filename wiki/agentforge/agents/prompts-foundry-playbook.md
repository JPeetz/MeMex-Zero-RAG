# Prompts Foundry — Playbook

_Lessons that carry forward across runs._

## What Works
- (pending — seed phase begins Run 1)

## What Failed
- (pending)

## Prompt Structures That Perform
- (pending)

## Seed Progress Notes
- 52 existing prompts in Obsidian vault to refactor across 12 categories
- Run 1 (2026-05-27): 3 prompts published from openclaw — all scored 12-14/15 original, rebuilt to 15/15
- Next: openclaw index 3 → continue until category exhausted (14 total), then coding (10), then hermes (7)

## Prompt Structures That Work
- **Three-mode architecture** (QuickMatch / SolutionBuild / Explore) maps naturally to discovery agents — user can browse, solve, or get fast answers
- **Handoff protocol** (input_from / output_to in TOML) prevents silent failures in multi-agent swarms. Must be bidirectional — if A outputs to B, B must input_from A.
- **Constraint tables** (Anti-Patterns, Escalation, Language-Specific) reduce ambiguity better than narrative paragraphs. Column format = easier for agents to parse at inference time.

## Cross-Platform Adaptation Patterns
- Original prompts all have generic placeholder titles ("O", "A", "C", "H") and generic descriptions — refactoring adds specific, searchable slugs and real use-case descriptions
- Obsidian vault prompts mix two states: (1) proper system prompts with actual agent behavior, and (2) catalog skeletons with only schema placeholders. The skeletons need complete category-level content — not just structure
- Platform-specific constraints (Discord tables, Twitter char limits, LinkedIn tone) should be baked into the prompt, not left as reader assumptions

## What Works
- **7-step process** (IDENTIFY → ANALYZE → BENCHMARK → REDESIGN → VALIDATE → PACKAGE → PUBLISH) correctly catches skeleton prompts that have inflated value scores
- **Parallel file reads** (read 3-5 prompts upfront) reveals patterns before redesign — the ", agent-based prompt catalog pattern" (title O/A/C, generic description, placeholder table) appears in ~30% of vault prompts
- **Templates-as-code** (TOML in the prompt itself) reduces ambiguity — agents can grep the format rather than parse narrative
