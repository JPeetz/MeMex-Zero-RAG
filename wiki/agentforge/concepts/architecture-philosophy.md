---
title: Concepts — Architecture & Philosophy
type: reference
tags: [concepts, architecture, zero-rag, philosophy]
sources: [raw/agentforge/board/concepts.md]
created: 2026-07-31
updated: 2026-07-31
status: active
confidence: high
---

# Core Concepts — AgentForge Architecture & Philosophy

## Zero-RAG (Knowledge Compilation)
An approach where sources are compiled into structured knowledge rather than retrieved as chunks at query time. The LLM reads a source once, extracts entities and relationships, and writes a structured wiki page. On query, the LLM reads the compiled wiki — synthesis is already done.

**Key difference from RAG:**
- RAG: Source → [retrieve] → LLM → Answer (rediscovers every time)
- Zero-RAG: Source → [compile] → Wiki → LLM (compounds over time)

## Associative Trails
Based on Vannevar Bush's Memex concept (1945) — knowledge is organized by association, not hierarchy. Every wiki page links to related concepts, entities, and projects. The LLM follows these trails during query time.

## Memory Architecture
- **HermesVault** (`~/HermesVault/`) — human-readable Obsidian vault, PARA-structured, synced to Google Drive
- **MeMex Zero RAG** (`~/workspace/MeMex-Zero-RAG/`) — LLM-readable compiled wiki, git-tracked, queryable via MCP
- **MEMORY.md** — hot-path facts for short-term context injection
- **Session DB** — running record of conversations

## Closed Learning Loop
Act → Reflect → Extract → Carry Forward. Every task produces a reflection, patterns are extracted cross-session, and reusable knowledge is written back to the wiki.

## See Also
- [[north-star]] — goals
- [[board-directives]] — prime directives

> **Source:** SecondBrain Concepts.md