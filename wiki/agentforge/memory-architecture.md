---
title: Memory Architecture
type: policy
created: 2026-05-21
updated: 2026-05-21
owner: CEO (Marvin)
---

# Memory Architecture Policy

**Decision (2026-05-21):** Obsidian + MeMex Zero RAG are the canonical long-term memory for ALL agents going forward.

## The Two Systems

### MeMex Zero RAG
- **Location:** `~/workspace/MeMex-Zero-RAG/wiki/agentforge/`
- **Purpose:** Structured, searchable institutional knowledge wiki
- **Maintenance:** Automated staleness sweeps + agent writes after tasks
- **Git-backed:** Yes — full version history

### Obsidian Vault
- **Location:** `~/obsidian-vault/AgentForge/`
- **Purpose:** Narrative, linked second brain
- **Structure:** decisions/, departments/, protocols/, research/, weekly-reports/
- **Linked notes:** Agents should use `[[wiki-links]]` for cross-referencing

## Consultation Order (Mandatory)

Every agent, before ANY external query:
1. **MeMex Zero RAG** — search the wiki first
2. **Obsidian vault** — check narrative notes second  
3. **External** (web search / AI query) — only if 1 and 2 yield nothing

## Why This Matters

- Reduces token usage over time (knowledge compounds locally)
- Prevents redundant research across agents
- Ensures consistent decisions based on prior context
- Enables agents to build on each other's work

## For New Agent Onboarding

When creating a new agent:
1. Include the consultation order in their CLAUDE.md
2. Give them write access to relevant MeMex wiki sections
3. Create a department folder in Obsidian vault
4. Reference this policy in their agent config

## Staleness Protocol

If MeMex content is outdated (>30 days for fast-moving topics):
- Adjust query and retry (max 3 attempts)
- After 3 failures: proceed externally, write result back to MeMex
- Flag stale entries with `stale: true` frontmatter

## Secondary Memory

`MEMORY.md` files in agent workspaces are **secondary convenience caches**.
They supplement but do not replace MeMex + Obsidian.

---

## Board Directives (2026-05-21)

### CEO Ownership
The CEO (Marvin) has full ownership to extend Obsidian and MeMex Zero RAG proactively as needed. No waiting for permission — build ahead of demand.

### Independence from Backup Directories
- ClaudeClaw backup (`/Users/joergpeetz/Documents/claudeclaw-agent-backup/agents/`) and Hermes backup (`/Users/joergpeetz/Documents/hermes-backup/hermes-agent/`) are **review-only references**
- Nothing in OpenClaw runtime depends on paths in those directories
- Everything is built fresh in the OpenClaw environment
- Those files show methodology/architectural thinking, not runtime dependencies

### What This Means
When asked to recreate something from those directories in OpenClaw:
1. Read the reference to understand the *approach*
2. Design and build the new version fresh for OpenClaw
3. Do NOT import, symlink, or depend on those paths
