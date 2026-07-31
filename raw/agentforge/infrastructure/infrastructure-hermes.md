# Infrastructure: Hermes Agent Transition Architecture

> Blueprint for migrating AgentForge from OpenClaw to Hermes Agent.
> **Created:** 2026-06-09 (Board directive)
> **Related:** [[Board-Directives]], [[Infrastructure-OpenClaw]]

---

## Hierarchy

```
gBrain → Orchestrator (Hermes) → Department Verticals → Specialist Agents → Scoped Sub-agents
```

## Key Principles

| Principle | Description |
|-----------|-------------|
| Narrow scope | Improves output quality and reduces drift |
| Client pod isolation | Own gBrain, orchestrator, agents, memory |
| Fork pattern | Build well once, customize per client (not copy-paste) |
| Multiple harnesses | Hermes, Codex, Claude Code |

## Org Chart Tracks

- Brains per agent
- Tools per agent
- Approvals per agent

## Architecture Documentation

- **MeMex:** `concepts/hermes-agent-transition-architecture.md`
- **Obsidian (mind-vault):** `brain/Hermes Agent Transition Architecture.md`
- **Obsidian (AgentForge):** `hermes-agent-transition-architecture.md`

## Migration Plan (Comprehensive)

### Inventory of OpenClaw Assets to Migrate
| Asset | Details |
|-------|---------|
| Agents | `~/.openclaw/agents/` — each has SOUL.md, AGENTS.md, workspace |
| Workspaces | `~/.openclaw/workspace/` — AGENTS.md, SOUL.md, MEMORY.md |
| Persona Files | SOUL.md, IDENTITY.md, USER.md |
| Workspace Scripts | TOOLS.md, HEARTBEAT.md, BOOTSTRAP.md |
| Skills | `workspace/skills/`, `~/.openclaw/skills/` |
| Memory Stores | `workspace/memory/*.md`, SQLite session DBs |
| Configs | `~/.openclaw/openclaw.json`, `~/.openclaw/gateway.env` |
| Integrations | Telegram, Discord, Slack, WhatsApp, Signal, CLI — all tokens inventoried |
| Cron/Tasks | Re-created via `hermes cron create` — no automatic mapping |

### Key Migration Principles
- **MeMex + Obsidian are permanent gBrain** — Hermes reads from and writes back to them
- **Second brain skill** + Hermes self-learning loop compound value over time
- **Narrow scope agents** — OpenClaw model (scoped specialists) maps directly to Hermes
- **Isolated client pods** — downstream pods with own gBrain, orchestrator, agents, memory
- **Fork pattern:** build well once, customize per client, start at ~75%

### Related Directives
- [[Concepts#zero-rag]] — Knowledge compilation architecture (permanent gBrain)
- [[Home]] — Navigation

## Status

| Phase | Status |
|-------|--------|
| Architecture design | ✅ Complete |
| Migration planning | 📝 Draft (comprehensive inventory done) |
| Department migration | 📝 Pending |
| Client pod creation | 📝 Pending |
