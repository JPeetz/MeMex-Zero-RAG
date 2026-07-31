# OpenClaw Knowledge Adoption

Board directive: locally installed **OpenClaw** is a core memory source for Hermes/Marvin. Its knowledge should be read and adopted when relevant, especially for AgentForge history, agents, departments, memory, gateway state, task/cron history, and migration continuity.

## Primary local sources

| Surface | Path | Purpose |
|---|---|---|
| OpenClaw runtime | `/Users/joergpeetz/.openclaw/` | Installed OpenClaw state, agents, config, plugins, runtime databases |
| OpenClaw config | `/Users/joergpeetz/.openclaw/openclaw.json.last-good` | Model policy, 73 configured agents, workspaces, memory search config |
| OpenClaw gateway DB | `/Users/joergpeetz/.openclaw/state/openclaw.sqlite` | Gateway state, plugins, audit events, cron/task history, channel ingress, task runs |
| Main agent DB | `/Users/joergpeetz/.openclaw/agents/main/agent/openclaw-agent.sqlite` | Main agent memory index; 1,088 indexed chunks / 163 sources at discovery time |
| OpenClaw workspace memory | `/Users/joergpeetz/.openclaw/workspace/MEMORY.md` | Curated long-term OpenClaw/Marvin memory |
| OpenClaw daily memory | `/Users/joergpeetz/.openclaw/workspace/memory/*.md` | Raw daily logs and operational continuity |

## Adoption rules

1. Treat OpenClaw's local files and SQLite state as part of durable institutional memory, not as an unrelated legacy install.
2. For AgentForge, department, memory, gateway, model-policy, cron/task, plugin, or migration questions, consult OpenClaw sources before guessing or rediscovering.
3. Do not print secrets from OpenClaw config/env files. Redact tokens and API keys by default.
4. Prefer human-readable notes first, then config files, then SQLite inspection for exact runtime facts.
5. When significant OpenClaw-derived knowledge is written down, sync it across HermesVault, SecondBrain, MeMex Zero RAG, and OpenClaw memory surfaces according to the Prime Directive.
