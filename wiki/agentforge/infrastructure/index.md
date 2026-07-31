---
title: Infrastructure
type: reference
tags: [infrastructure, servers, credentials, tools]
sources: [raw/agentforge/infrastructure/]
created: 2026-07-31
updated: 2026-07-31
status: active
confidence: high
---

# Infrastructure

## Local Machine
- macOS 15.7.5 (x64), Node v26.0.0
- OpenClaw runtime at `~/.openclaw/`
- Obsidian vaults: HermesVault (`~/HermesVault/`), SecondBrain (`~/workspace/SecondBrain/` — archive)

## Remote Server (Vane)
- IP: 207.180.227.214
- Hostname: vmi1593174.contaboserver.net
- DDNS: vane.sytes.net (No-IP, ddclient daemon)
- Services: SearXNG (port 8080), Vane (port 3000), NGINX reverse proxy

## Key Services

| Service | URL | Purpose |
|---------|-----|---------|
| n8n | jpeetzn8n.xyz | 101 workflows, 26 MCP tools |
| Vane | vane.sytes.net | AI research engine (Perplexica + SearXNG) |
| MeMex | ~/workspace/MeMex-Zero-RAG/ | Zero-RAG knowledge base |
| Supabase (TaskForge) | oltlnbxchdnavocpqgyc.supabase.co | RaceIntel DB (~514K rows) |
| Supabase (BetterLife) | dxvktbhwrkzywpukvqne.supabase.co | Video ads workflow |

## Hermes Agent Transition
Blueprint: gBrain → Orchestrator (Hermes) → Department Verticals → Specialist Agents → Scoped Sub-agents. Narrow scope improves quality. Client pods isolated with own gBrain, orchestrator, agents, memory.

## See Also
- [[projects/index]] — active projects
- [[board-directives]] — governance

> **Sources:** SecondBrain Infrastructure.md, Infrastructure-Hermes.md, Infrastructure-OpenClaw.md, Infrastructure-Vane.md, Infrastructure-n8n.md