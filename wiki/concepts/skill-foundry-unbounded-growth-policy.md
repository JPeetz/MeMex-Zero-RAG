---
title: Skill Foundry — Unbounded Growth Policy (2026-06-16)
type: concept
tags: ["skill-foundry", "board-directive", "scaling", "policy", "2026-06-16"]
created: 2026-06-16
author: marvin
---

# Skill Foundry — Unbounded Growth Policy

**Board Directive — 2026-06-16** | Agent: Marvin (CEO) | Department: Skill Foundry

## Decision

The Skill Foundry repository (JPeetz/agent-skills) has **NO skill count cap**. The repository grows unbounded — continuously, indefinitely. Target trajectory: 12 → 50 → 100 → 500 → 1000+ skills.

## Background

Run 003 reported "Topics rotated: 5 out, 5 in (20/20 limit maintained)" — which was referencing GitHub's built-in 20-topic metadata limit, but the language implied a skill rotation cap. Board clarified: there is no cap, and the report language must reflect that.

## Policy

1. **Skill count is unbounded.** No rotation, no removal, no ceiling. Every skill shipped stays shipped.
2. **GitHub Topics are metadata only.** GitHub's 20-topic limit applies to repository tags, not content. Curate the 20 most important broad-category topics permanently. Do not rotate.
3. **Report language must be accurate.** Say "GitHub topics curated" or "topics refreshed" — never "topics rotated" or "limit maintained."
4. **README scales with the repo.** Flat catalog table works for ≤20 skills. Beyond that: category directories per the scaling strategy.
5. **Scaling strategy:** Phase 1 (0-20 flat), Phase 2 (20-50 category dirs), Phase 3 (50+ search manifest).
   - Reference pattern: https://github.com/seb1n/awesome-ai-agent-skills (90+ skills)

## Implementation

- AGENTS.md updated with Repo Scaling Policy section
- MEMORY.md updated: rotation strategy removed, unbounded count added
- Daily memory (2026-06-16) corrected

## References

- Board examples: https://mcpservers.org/agent-skills, https://github.com/seb1n/awesome-ai-agent-skills
- Repository: https://github.com/JPeetz/agent-skills
