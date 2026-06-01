# Project Nemesis — Executive Summary

**Classification:** BOARD ONLY  
**Date:** 2026-06-01  
**Author:** AgentForge CEO (Marvin)  
**Full Blueprint:** [counter-project-blueprint.md](./counter-project-blueprint.md)

---

## Core Thesis

The agent framework market has three dominant players — OpenClaw (376K ★, TypeScript), Hermes Agent (175K ★, Python), and OpenHuman (Rust, early beta) — and all three share critical weaknesses: **no capability-based security, monolithic architectures, and vendor-locked memory models.** Our 11 days of production experience with AgentForge prove that a Go-based, security-first, file-memory-native agent framework can beat all of them on the dimensions that matter: security, concurrency, deployability, and enterprise readiness.

## The Attack Vector

| Competitor | Key Weakness | Our Attack |
|---|---|---|
| **OpenClaw** | Full host access (security nightmare), TypeScript runtime bloat (200MB+ node_modules), npm supply chain, macOS-only desktop app | Capability-based security, Go static binary (6MB), WASM-sandboxed plugins, native desktop app for Windows + macOS + Linux |
| **Hermes Agent** | Python monolith (synchronicity ceiling), CVEs already, single-agent loop, no native desktop | Goroutine-native concurrency (true parallelism), <30K lines Go, desktop app with system tray |
| **OpenHuman** | Desktop-only (no headless/CI), OAuth attack surface, Tauri webview dependency, closed-source managed backend | Server-first + desktop-optional, no OAuth sprawl, fully open, headless-native |

## Architecture Decision: **Go**

Goroutines + channels map 1:1 to our agent orchestration model. Go's concurrency is the product — 100K agents on a $10/month VM. Rust is reserved for the WASM plugin SDK. Single static binary, no runtime dependencies, cross-compiles to everything from Raspberry Pi to Kubernetes.

## Five Pillars

1. **Deterministic Memory (MeMex Zero RAG)** — Files + git + SQLite index. No vector soup. Grep-able, cat-able, git-trackable. Proven in AgentForge production.

2. **Capability-Based Security** — Every agent gets a permission token at spawn. Filesystem allowlists, domain allowlists, token budgets, timeout enforcement. Infosec-reviewable. No other framework has this.

3. **CSP-Concurrent Orchestration** — Goroutines for agents, channels for communication, DAG scheduler for pipelines, tree manager for subagents. Not bolted on — native to the runtime.

4. **WASM Plugin Sandbox** — Plugins run in WASI preview 2 sandboxes. Content-addressed (SHA-256). Manifest-declared capabilities. SBOM-verified. No npm/pip supply chain attacks.

5. **Enterprise-Grade Deployment** — Single 6MB binary. Linux, macOS, Windows, Docker, K8s, Raspberry Pi, air-gapped. SQLite (no external DB). RBAC, SSO, audit logging, SLA contracts. Native desktop app for Windows/macOS via Wails (Go + web frontend).

## Recommended Name: Crucible ⭐ → BOARD REJECTED. New proposals below.

| Rank | Name | Tagline | Vibe | Domain |
|---|---|---|---|---|
| 1 | **Apex** ⭐ | "Apex: The peak of agent intelligence." | Dominant, unbeatable, short | apexagents.dev |
| 2 | **Vanguard** | "Vanguard: Leading the agent revolution." | Military, forward position, competitive | vanguardagents.dev |
| 3 | **Gauntlet** | "Gauntlet: Test. Harden. Deploy." | Challenge, security, pressure | gauntlet.dev |
| 4 | **Foundry** | "Foundry: Where intelligent agents are cast." | Industrial, professional, bridges AgentForge | foundryagents.dev |
| 5 | **Axiom** | "Axiom: Self-evident agent intelligence." | Foundational, mathematical, trust | axiomagents.dev |
| 6 | **Arsenal** | "Arsenal: The complete agent weapons platform." | Military, comprehensive, no-compromise | arsenalagents.dev |

## Monetization: $696K ARR Target (Year 1)

| Tier | Price | Target by Month 12 |
|---|---|---|
| Community (Free) | $0 | 15,000 users |
| Pro | $29/mo | 800 subscribers |
| Team | $99/mo (5 seats) | 200 subscribers |
| Enterprise | $499/mo (20 seats) | 30 customers |

BUSL-1.1 license → Apache 2.0 after 4 years. Prevents cloud providers from hosting-as-a-service without paying.

## 30-Day Launch Plan

- **Week 1:** Core daemon, agent goroutine model, CSP bus, memory store, capability enforcement
- **Week 2:** Departments, pipeline DAG, LLM adapters, CLL, subagent trees, messaging bridge, Docker
- **Week 3:** Observability, web dashboard, WASM SDK, marketplace, docs, landing pages
- **Week 4:** Launch (Show HN), community, tutorials, enterprise page, plugin contest, v0.2 roadmap

Target: 1,000+ GitHub stars, 50+ Pro signups by Day 30.

## The AgentForge Connection

Crucible productizes everything AgentForge proved in production: MeMex memory, department isolation, pipeline DAGs, closed learning loops. AgentForge will be Crucible's first enterprise customer — migrating off OpenClaw onto our own stack. This is the ultimate proof and the best case study.

## Key Risks

- Burnout (solo/small team) → mitigated by ruthless scoping, 30-day MVP contract
- Community doesn't materialize → mitigated by pre-built content pipeline + HN launch
- OpenClaw adds Go → they'd be catching up; our design choices are Go-native, not ported
- Enterprise sales cycle → start with self-serve Pro/Team; Enterprise is month 3+

## Bottom Line

We have 30 days of intelligence, 11 days of production learnings, and a clear attack surface against three frameworks that are collectively 551K stars but share the same fatal flaw: **they treat security as an afterthought.** Crucible makes security the foundation. In a world where every enterprise is asking "how do we deploy AI agents safely?", that's the winning bet.

---

**Decision Required:** Board approval to proceed with Week 1 development. Budget: €0 (open source, solo development). Only cost is time — 30 days to MVP launch.

**Full Blueprint:** [counter-project-blueprint.md](./counter-project-blueprint.md) — 17 pages, competition gap matrix, full architecture, viral names analysis, monetization projections, SEO/GEO strategy, risk register, open source strategy.

---

*Submitted for Board review 2026-06-01.*