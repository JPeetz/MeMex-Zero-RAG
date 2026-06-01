# Project Nemesis — Counter-Project Blueprint v1.0

**Classification:** BOARD ONLY  
**Date:** 2026-06-01  
**Author:** AgentForge CEO (Marvin)  
**Status:** Draft → Board Review  
**Input:** 4 sub-agent intelligence reports + 11-day AgentForge operational learnings  
**Output:** Definitive counter-project design — Go/Rust agent orchestration hub

---

## Table of Contents

1. [Competition Gap Matrix](#section-1-competition-gap-matrix)
2. [Architecture Decision](#section-2-architecture-decision)
3. [Technical Architecture](#section-3-technical-architecture)
4. [SEO/GEO Strategy](#section-4-seogeo-strategy)
5. [Viral Names](#section-5-viral-names)
6. [Monetization Model](#section-6-monetization-model)
7. [30-Day Launch Plan](#section-7-30-day-launch-plan)

---

## Section 1: Competition Gap Matrix

### Feature-by-Feature Attack Surface

| Feature Domain | OpenClaw | Hermes Agent | OpenHuman | Huginn | **Our Gap → Attack Vector** |
|---|---|---|---|---|---|
| **Runtime Language** | TypeScript (Node.js) | Python (85%) | Rust + Tauri | Ruby | **Go binary** — single static binary, no runtime deps, 10x startup speed |
| **Memory Model** | JSON files, no DB | Honcho user modeling | SQLite + Obsidian vault | N/A (event queue) | **MeMex Zero RAG** — deterministic, git-tracked, grep-able, no vector soup |
| **Agent Loop** | Lane queue (serial only) | Sync-only (no async) | Desktop event loop | Event graph | **CSP-based concurrent pool** — goroutine-per-agent, true parallelism |
| **Tool System** | Skills ecosystem (700+) | 70+ tools (complexity tax) | 118+ integrations | Event agents | **Plugin SDK (WASM + gRPC)** — sandboxed, language-agnostic, auditable |
| **Orchestration** | Gateway hub-and-spoke | Single agent loop | Desktop-only | Event graph | **Fleet orchestration** — subagent trees, pipeline DAGs, department isolation |
| **Security Model** | Full host access by default | CVEs in the wild (CVE-2026-7396) | OAuth to everything | Script agents | **Capability-based security** — agent permissions as compile-time tokens |
| **Deployment** | Node.js daemon | Python venv/pip | Desktop app (Tauri) | Ruby server | **Single Go binary + Docker 6MB image** — cloud, edge, Raspberry Pi |
| **Learning Loop** | Manual skill creation | GEPA (autonomous) — best feature | None | None | **Closed Learning Loop (CLL)** — AgentForge-proven, automatic, git-versioned |
| **Concurrency** | Event loop (single-threaded) | Sync-only | Tauri async | Event graph | **Goroutine native** — 100K concurrent agents on one machine |
| **Observability** | File logs | FTS5 search | None structured | Event trace | **OpenTelemetry native** — traces, metrics, logs, distributed context propagation |
| **API Redundancy** | ClawHub (single marketplace) | Model provider list | TokenJuice | Webhooks | **Multi-backend with circuit breakers** — learned from SEO API outage |
| **Offline Capability** | No (gateway required) | Partial | Yes (desktop) | Yes (local) | **Full offline mode** — local LLMs via Ollama, all state local, sync when online |
| **Enterprise Features** | None structured | None | None | Event webhooks | **RBAC, audit logging, SSO, air-gapped deploy, SLA contracts** |
| **Codebase Size** | ~50K lines TypeScript | run_agent.py 16K lines, cli.py 14K lines | Young beta | Mature | **Target: <30K lines Go** — 60% less code than Hermes, 40% less than OpenClaw |
| **Supply Chain** | npm ecosystem (attack surface) | pip dependencies | cargo + Tauri webview | Ruby gems | **Go stdlib-first** — minimize third-party deps, reproducible builds |
| **Documentation** | Community-driven | Young/docs light | Beta | Mature | **Literate programming docs + executable examples + video walkthroughs** |

### Attack Summary

**Exploitable Weaknesses:**

1. **OpenClaw**: TypeScript runtime bloat, full-privilege agents (security nightmare), JSON-file persistence crumbles at scale, npm supply chain is a known attack vector, monolithic gateway is a single point of failure
2. **Hermes**: Python monolith (30K+ lines in two files), sync-only means one slow tool blocks the entire loop, 10 weeks old and already has CVEs, Nous Research is a small team — velocity will slow
3. **OpenHuman**: Desktop-only is a ceiling, OAuth-to-everything is a privacy disaster waiting to happen, Tauri webview dependency is brittle, no headless/CI mode kills enterprise adoption
4. **Huginn**: Event-driven but Ruby-based (performance ceiling), no native LLM integration, IFTTT replacement — not an agent framework

**Our Attack:** Go-based, capability-secured, concurrent-native, offline-capable, enterprise-ready. File-based memory that actually works (proven by AgentForge). Pipeline DAGs instead of monolithic loops. 6MB Docker image vs. OpenClaw's 200MB+ Node.js blob.

---

## Section 2: Architecture Decision

### Verdict: **Go**

### Why Go Over Rust

| Dimension | Go | Rust | Winner |
|---|---|---|---|
| **Team accessibility** | 2-4 week ramp for competent devs | 4-8 week ramp, borrow checker learning curve | Go |
| **Concurrency model** | Goroutines + channels (CSP) — natural fit for agent orchestration | async/await + tokio — powerful but complex | Go |
| **Compile speed** | Sub-second for medium projects | 30s-2min for medium projects | Go |
| **Binary size** | 6-12MB static | 4-8MB static (slightly smaller) | Tie |
| **Ecosystem for agents** | net/http, database/sql, encoding/json in stdlib | serde, tokio, reqwest all external | Go |
| **WASM support** | TinyGo → WASM, mature | wasm-bindgen, wasm-pack — excellent | Rust (slight edge) |
| **Learning curve for contributors** | Gentle — Python/TS devs can read Go in a week | Steep — ownership model is genuinely hard | Go |
| **Embedding** | Go can be embedded as a C library (cgo) | Rust FFI is first-class | Rust |
| **Enterprise adoption** | Kubernetes, Docker, Terraform, Consul — proven track record | Firefox, ripgrep, fd — newer in enterprise | Go |
| **Cross-compilation** | GOOS/GOARCH — trivial | cross + target triples — good but more setup | Go |

### Decision Rationale

Go wins because:

1. **The concurrency model is the product.** Goroutines and channels map almost 1:1 to the agent orchestration model we're building. An agent is a goroutine. A department is a channel-bounded pool. A pipeline is a DAG of goroutines with channel communication. This isn't metaphor — it's literally how Go was designed.

2. **We need contributors, not just users.** The agent framework war will be won by ecosystem. Rust's steep learning curve limits contributor growth. Go is the Python of compiled languages — readable, learnable, hireable.

3. **Enterprise needs boring technology that scales.** Go is boring in the best way. It's what Kubernetes, Docker, and every major cloud-native project is built on. IT departments approve Go. They debate Rust.

4. **The TinyClaw precedent.** OpenClaw already has a Go component. They know Go. We need to out-execute them in their own language — or at least match them where they've already placed a bet.

### Rust's Role

Rust is not out. It has two specific roles:

1. **WASM plugin sandbox** — Rust compiles to WASM better than anything. If we offer a WASM-based plugin SDK (for third-party tools that need sandboxed execution), Rust is the natural language for plugin authors.
2. **Performance-critical paths** — If any component needs zero-cost abstractions (e.g., the memory indexing engine, the tokenizer for context compression), we can write that in Rust and link via FFI or compile to a shared library.

**Hybrid approach:** Go for the framework. Rust for the plugin SDK. WASM as the bridge.

### Key Design Decisions

| Decision | Choice | Rationale |
|---|---|---|
| **Database** | SQLite (embedded) + file-based overlay | No external dependency, git-trackable, proven by OpenHuman + AgentForge |
| **Serialization** | JSON (human-readable) + MessagePack (wire format) | Grep-able for debugging, compact for transport |
| **Plugin system** | WASM (WASI preview 2) | Sandboxed, language-agnostic, 15-year standard |
| **Messaging** | gRPC + Protobuf | Strongly typed contracts, bi-directional streaming, enterprise standard |
| **HTTP layer** | net/http (stdlib) + chi router | Minimal deps, battle-tested |
| **WebSocket** | gorilla/websocket or nhooyr.io/websocket | Real-time agent status streaming |
| **LLM integration** | Vendor-agnostic adapter pattern | Same interface for OpenAI, Anthropic, Ollama, Groq, etc. |
| **Configuration** | HCL (same as Terraform) | Declarative, familiar to DevOps, git-ops ready |
| **Observability** | OpenTelemetry (OTLP) | Industry standard, every observability platform supports it |
| **Testing** | Go's testing package + testify | Table-driven tests, race detector built-in |
| **Build system** | Go modules + goreleaser | Cross-compilation Matrix, Homebrew, Docker, .deb/.rpm |

---

## Section 3: Technical Architecture

### 3.1 Runtime Model

```
┌─────────────────────────────────────────────────────────────┐
│                    NEMESIS DAEMON (Go Binary)                │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Agent Pool   │  │  Department  │  │ Pipeline     │       │
│  │ (goroutines) │  │   Managers   │  │  Scheduler   │       │
│  │              │  │  (channels)  │  │  (DAG exec)  │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                 │                 │                │
│  ┌──────┴─────────────────┴─────────────────┴───────┐       │
│  │              CSP Message Bus                      │       │
│  │         (buffered channels + select)              │       │
│  └──────┬─────────────────┬─────────────────┬───────┘       │
│         │                 │                 │                │
│  ┌──────┴───────┐  ┌──────┴───────┐  ┌──────┴───────┐       │
│  │ Memory Store │  │  Tool Host   │  │  Message     │       │
│  │ (SQLite+FS)  │  │  (WASM+gRPC) │  │  Bridge      │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Capability Security Layer                │   │
│  │    (per-agent permission tokens, compile-time)        │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

**Core concept:** Every agent is a goroutine. Every department is a channel-bounded goroutine pool. Every pipeline is a DAG where nodes are goroutines and edges are channels. The CSP message bus routes everything.

**Agent lifecycle:**
1. `nemesis agent spawn --role "content-writer" --department "content" --capabilities "fs:read,http:outbound,llm:anthropic"`
2. Daemon creates goroutine with capability token set
3. Agent joins department channel pool
4. Messages flow via buffered channels
5. Agent terminates on completion or timeout
6. All state persisted to Memory Store

**Why CSP over actor model (Erlang/Elixir):** CSP is simpler. Channels are typed pipes. Select provides non-deterministic choice. No supervision trees, no OTP complexity. For an agent framework, CSP maps to "agents communicating over typed channels" perfectly. The Go runtime handles scheduling — 100K goroutines is a $10/month VM.

### 3.2 Memory Architecture

```
┌─────────────────────────────────────────────────────────┐
│              DETERMINISTIC MEMORY ARCHITECTURE            │
│                                                          │
│  ┌──────────────────┐    ┌──────────────────┐           │
│  │   MeMex Zero RAG │    │  Obsidian Vault  │           │
│  │   (Canonical)    │◄──►│  (Narrative)     │           │
│  │                  │    │                  │           │
│  │  - Structured    │    │  - Linked notes  │           │
│  │  - Git-tracked   │    │  - Daily logs    │           │
│  │  - Grep-able     │    │  - Zettelkasten  │           │
│  │  - Markdown      │    │  - Markdown      │           │
│  └────────┬─────────┘    └────────┬─────────┘           │
│           │                       │                      │
│           └───────────┬───────────┘                      │
│                       │                                  │
│              ┌────────┴────────┐                         │
│              │   SQLite WAL    │                         │
│              │  (Fast Index)   │                         │
│              └────────┬────────┘                         │
│                       │                                  │
│              ┌────────┴────────┐                         │
│              │  Context Engine │                         │
│              │  (TokenJuice    │                         │
│              │   compression)  │                         │
│              └────────┬────────┘                         │
│                       │                                  │
│              ┌────────┴────────┐                         │
│              │   LLM Context   │                         │
│              │   (injection)   │                         │
│              └─────────────────┘                         │
└─────────────────────────────────────────────────────────┘
```

**Key principles:**

1. **Files are the source of truth.** Not vectors. Not embeddings. Files. Markdown files in a git repo. Why? Because files are grep-able, cat-able, diff-able, and every developer already knows how to work with them. AgentForge proved this: MeMex Zero RAG (file-based, git-tracked) outperformed every vector database approach we tried.

2. **SQLite as a fast index, not the canonical store.** SQLite indexes the file tree for fast lookups (FTS5 full-text search). But the files are always the master. Delete SQLite, regenerate from files. This means backups are `git push`, not database dumps.

3. **Dual-write with automatic reconciliation.** Write to MeMex → SQLite index updates → Obsidian mirror syncs within 100ms. If mirror fails, queue and retry. AgentForge's dual-write decay problem (mirror degrading between weekly reports) is fixed by making it synchronous and monitored.

4. **Context compression is a first-class feature.** OpenHuman's TokenJuice is clever but desktop-only. We build context compression into the engine: extract relevant snippets from MeMex → compress via summarization → inject into LLM context. This is what AgentForge's agents do manually today. Automate it.

5. **Memory = learning, not storage.** Hermes got this right. The GEPA cycle (Gather → Execute → Proceduralize → Apply) is their best feature. We implement it as the Closed Learning Loop (CLL) — every agent interaction that produces a lesson is written to MeMex → becomes available to all future agents → reduces token usage over time.

### 3.3 Agent Orchestration

```
┌────────────────────────────────────────────────────────────┐
│                   ORCHESTRATION ENGINE                      │
│                                                             │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐       │
│  │  Department  │   │  Department  │   │  Department  │       │
│  │   Content    │   │     SEO      │   │   Social     │       │
│  │              │   │              │   │              │       │
│  │ ┌──┐ ┌──┐   │   │ ┌──┐ ┌──┐   │   │ ┌──┐ ┌──┐   │       │
│  │ │A1│ │A2│   │   │ │B1│ │B2│   │   │ │C1│ │C2│   │       │
│  │ └──┘ └──┘   │   │ └──┘ └──┘   │   │ └──┘ └──┘   │       │
│  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘       │
│         │                 │                 │                │
│         └─────────────────┼─────────────────┘                │
│                           │                                  │
│                  ┌────────┴────────┐                         │
│                  │  Pipeline DAG   │                         │
│                  │   Scheduler     │                         │
│                  │                 │                         │
│                  │  Content → SEO  │                         │
│                  │    ↓       ↓    │                         │
│                  │  PDF ← Social   │                         │
│                  └────────┬────────┘                         │
│                           │                                  │
│                  ┌────────┴────────┐                         │
│                  │  Subagent Tree  │                         │
│                  │   Manager       │                         │
│                  │                 │                         │
│                  │  Parent spawns  │                         │
│                  │  children,      │                         │
│                  │  collects       │                         │
│                  │  results,       │                         │
│                  │  merges output  │                         │
│                  └─────────────────┘                         │
└────────────────────────────────────────────────────────────┘
```

**Department model (proven by AgentForge):**
- Each department is a goroutine pool with bounded concurrency
- Departments communicate via typed channels (not shared memory)
- Department failure is isolated — Content going down doesn't kill SEO
- Each department has its own AGENTS.md (configuration as code)

**Pipeline DAG (fixing the Part B fragmentation problem):**
- Pipelines are DAGs defined in HCL
- Each node is a department operation
- Edges define data flow and dependencies
- The scheduler topologically sorts and executes
- Failed nodes trigger retry with backoff
- Skipped stages (AgentForge's chronic Part B problem) are detected and alarmed

**Subagent tree (fixing manual sessions_spawn):**
- Parent agent spawns child goroutines
- Children run with inherited-but-restricted capability tokens
- Results flow back via channels
- Parent merges, synthesizes, and completes
- Built-in, not bolted-on

### 3.4 Tool System

```
┌─────────────────────────────────────────────────────────┐
│                    TOOL SYSTEM                           │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │              Plugin SDK (WASM + gRPC)              │   │
│  │                                                    │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐        │   │
│  │  │ WASM     │  │ gRPC     │  │ Built-in  │        │   │
│  │  │ Plugin   │  │ Service  │  │ Tools     │        │   │
│  │  │          │  │          │  │           │        │   │
│  │  │ Sandbox  │  │ External │  │ fs, http, │        │   │
│  │  │ WASI P2  │  │ Process  │  │ exec, llm │        │   │
│  │  └──────────┘  └──────────┘  └──────────┘        │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │              Tool Marketplace                      │   │
│  │                                                    │   │
│  │  - Signed WASM binaries (content-addressed)        │   │
│  │  - Capability declarations (manifest)              │   │
│  │  - Reputation system (not just star count)         │   │
│  │  - Sandbox verification before install             │   │
│  │  - Supply chain audit (SBOM, provenance)           │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

**Design philosophy:** OpenClaw's ClawHub (700+ community skills) is both their strength and their attack surface. We learn from it:

- **WASM sandboxing:** Every plugin runs in a WASI preview 2 sandbox. Declared capabilities only. No filesystem access unless explicitly granted. No network unless declared. This eliminates the "full host access" problem that plagues OpenClaw.
- **Content-addressed binaries:** Plugins are identified by SHA-256 hash, not name. No dependency confusion attacks.
- **Manifest system:** Every plugin declares its capabilities upfront. The agent framework enforces them. This is compile-time security, not runtime hope.
- **Marketplace with provenance:** SBOM (Software Bill of Materials) for every plugin. Signed by author. Verified by marketplace. The npm/pip supply chain attack doesn't apply.

### 3.5 Messaging / Multi-Surface

```
┌──────────────────────────────────────────────────────────┐
│                  MESSAGING BRIDGE                         │
│                                                           │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐        │
│  │ Discord │ │ Telegram│ │  Slack  │ │  WhatsApp│        │
│  │         │ │         │ │         │ │          │        │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬─────┘        │
│       │           │           │           │               │
│       └───────────┴───────────┴───────────┘               │
│                       │                                   │
│              ┌────────┴────────┐                          │
│              │  Surface Router │                          │
│              │                 │                          │
│              │  - Inbound:     │                          │
│              │    route to     │                          │
│              │    correct      │                          │
│              │    agent        │                          │
│              │  - Outbound:    │                          │
│              │    format for   │                          │
│              │    target       │                          │
│              └────────┬────────┘                          │
│                       │                                   │
│              ┌────────┴────────┐                          │
│              │   Web Dashboard │                          │
│              │   (HTMX + SSE)  │                          │
│              └─────────────────┘                          │
└──────────────────────────────────────────────────────────┘
```

**Approach:** OpenClaw's hub-and-spoke gateway is elegant but monolithic. Hermes has 20 messaging platforms. We take a different approach:

- **Surface adapters as WASM plugins.** Each messaging platform is a plugin. Discord plugin, Telegram plugin, etc. They implement a standard interface: `Receive() → Message`, `Send(Message) → error`.
- **Surface router is a goroutine.** Inbound messages arrive on channels. Router inspects → routes to correct agent/department. Outbound messages are formatted per-platform (no markdown tables on Discord, proper WhatsApp formatting).
- **Web dashboard is HTMX + Server-Sent Events.** No React SPA bloat. HTMX gives us reactive UI with 14KB of JavaScript. SSE gives us real-time agent status streaming. This is the "boring technology" choice that enterprises love.

### 3.6 Security Model

```
┌──────────────────────────────────────────────────────────┐
│              CAPABILITY-BASED SECURITY                    │
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │              Agent Capability Token                │   │
│  │                                                    │   │
│  │  {                                                 │   │
│  │    "agent_id": "content-writer-01",                │   │
│  │    "department": "content",                        │   │
│  │    "capabilities": {                               │   │
│  │      "fs:read": ["/workspace/content/"],           │   │
│  │      "fs:write": ["/workspace/content/",           │   │
│  │                    "/workspace/artifacts/"],        │   │
│  │      "http:outbound": ["api.anthropic.com",        │   │
│  │                         "seo-api.example.com"],    │   │
│  │      "http:inbound": [],                           │   │
│  │      "exec": [],                                   │   │
│  │      "network:raw": []                             │   │
│  │    },                                              │   │
│  │    "expires": "2026-06-02T00:00:00Z",              │   │
│  │    "max_tokens": 100000,                           │   │
│  │    "max_duration_seconds": 3600                    │   │
│  │  }                                                 │   │
│  └──────────────────────────────────────────────────┘   │
│                                                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │              Enforcement Layer                      │   │
│  │                                                    │   │
│  │  - Every tool call checked against capability token │   │
│  │  - File paths validated against allowlist           │   │
│  │  - URLs validated against domain allowlist          │   │
│  │  - Token budget enforced (per-agent, per-dept)      │   │
│  │  - Timeout enforced at goroutine level              │   │
│  │  - Audit log of all capability checks               │   │
│  └──────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────┘
```

**The OpenClaw problem:** Agents run with full host access. Every agent can read every file, make every network call, execute every command. This is the #1 security gap in the entire agent framework ecosystem. Nobody has solved it.

**Our solution:** Capability-based security inspired by WASI and Capsicum (FreeBSD). Every agent gets a capability token at spawn time. Every tool call goes through the enforcement layer. An agent that only needs to read `/workspace/content/` and call `api.anthropic.com` cannot read `/etc/passwd` or call `evil.com`.

**Enterprise implications:** This is the feature that gets us past infosec review. "Yes, your agents have guardrails. Yes, we can prove what each agent can and cannot do. Yes, there's an audit log." No other framework can say this.

### 3.7 Deployment Model

```
┌────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT MATRIX                        │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Local Dev  │  │  Cloud       │  │  Enterprise   │      │
│  │              │  │              │  │  (Air-Gapped) │      │
│  │  nemesis     │  │  Docker      │  │               │      │
│  │  dev         │  │  Compose     │  │  nemesis      │      │
│  │              │  │              │  │  enterprise   │      │
│  │  1 binary    │  │  docker run  │  │               │      │
│  │  no deps     │  │  nemesis:    │  │  Offline LLM  │      │
│  │              │  │  latest      │  │  (Ollama)     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Kubernetes  │  │  Raspberry   │  │  Edge         │      │
│  │              │  │  Pi          │  │              │      │
│  │  Helm chart  │  │              │  │  Fly.io       │      │
│  │  StatefulSet │  │  arm64       │  │  Railway      │      │
│  │  + SQLite    │  │  binary      │  │  Render       │      │
│  │  + PVC       │  │  (6MB)       │  │               │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────────────────────────────────────────┘
```

**Deployment tiers:**

| Tier | Target | Distribution | Support |
|---|---|---|---|
| **Local** | Developer laptop | `go install`, Homebrew, direct download | Community |
| **Cloud** | VM/Docker | Docker Hub, GitHub Container Registry | Community + Docs |
| **K8s** | Kubernetes cluster | Helm chart, Operator | Paid |
| **Edge** | Raspberry Pi, ARM SBCs | ARM64 binary, apt repo | Paid |
| **Enterprise** | Air-gapped DC | Signed .rpm/.deb, SBOM, offline docs | Enterprise |

**Key advantage:** Because it's a single Go binary with SQLite, deployment is trivial. No MongoDB cluster. No Redis. No PostgreSQL. Just one binary and a data directory. This is what HashiCorp does and it's why enterprises love their tools.

---

## Section 4: SEO/GEO Strategy

### 4.1 Primary Keyword Cluster

**Core keywords:**
- "agent orchestration framework"
- "autonomous agent platform"
- "LLM agent framework Go"
- "agent memory architecture"
- "multi-agent orchestration"
- "agent deployment security"
- "enterprise agent framework"
- "WASM agent plugins"
- "capability-based security agents"
- "agent pipeline automation"

**Long-tail keywords:**
- "how to orchestrate multiple AI agents"
- "secure agent framework for enterprise"
- "agent memory that doesn't use vector database"
- "Go-based LLM agent framework vs Python"
- "air-gapped AI agent deployment"
- "agent framework with git-tracked memory"
- "WASM sandbox for LLM tools"

**Competitor keywords to capture:**
- "OpenClaw alternative"
- "Hermes Agent alternative"
- "OpenClaw vs [our name]"
- "self-hosted agent framework"
- "open source agent orchestration"

### 4.2 Content Strategy for Launch

**Phase 1: Technical Blog Posts (Pre-Launch, Week 1-2)**
1. "Why Go, Not Python: A Systems Programming Approach to Agent Orchestration"
2. "Files Are the Best Vector Database: A Memory Architecture Manifesto"
3. "Capability-Based Security for AI Agents: Why Your Agents Shouldn't Have Root"
4. "The 10 Problems With Current Agent Frameworks (And How We Fixed Them)"

**Phase 2: Comparison Content (Launch Week, Week 3)**
1. "[Our Name] vs OpenClaw: Go vs TypeScript, Security vs Convenience"
2. "[Our Name] vs Hermes Agent: Concurrency vs Synchronous Loops"
3. "[Our Name] vs OpenHuman: Server vs Desktop, Universal vs Personal"
4. "Migrating from OpenClaw to [Our Name]: A 15-Minute Guide"

**Phase 3: Tutorial Content (Post-Launch, Week 4)**
1. "Building Your First Agent Pipeline in 5 Minutes"
2. "Deploying Agent Orchestration on Kubernetes"
3. "Running Agents on a Raspberry Pi: Edge AI Done Right"
4. "Air-Gapped Enterprise Agents: Compliance-Ready From Day One"

**Phase 4: Thought Leadership (Ongoing)**
1. "The Agent Framework War: 2026 Edition"
2. "Memory Architecture for Autonomous Agents: What We Learned From 11 Days of Production"
3. "Why Supply Chain Security Matters for Agent Plugins"

### 4.3 GEO Optimization (Ireland/Europe Angle)

**Why Ireland/Europe matters:**
- GDPR compliance as a selling point (all data local, no cloud dependency)
- EU AI Act readiness (capability-based security = built-in risk management)
- Dublin as a tech hub (we're based here, use it)
- European enterprises prefer European-hosted infrastructure
- Data sovereignty: "Your agents, your data, your servers — nothing leaves your jurisdiction"

**GEO keywords:**
- "GDPR-compliant AI agent framework"
- "EU-hosted agent orchestration"
- "European AI agent platform"
- "Ireland-based agent framework"
- "EU AI Act compliant agent deployment"
- "data-sovereign AI agents"

**GEO content:**
- "Why European Enterprises Are Choosing [Our Name] for GDPR-Compliant Agent Orchestration"
- "EU AI Act: What It Means for Agent Frameworks and How We're Ready"
- Case study: "How [Irish Company] Deployed Agent Pipelines Without Cloud Dependency"

**European tech event strategy:**
- Submit to FOSDEM 2027 (Brussels, February)
- Submit to Dublin Tech Summit
- Target WeAreDevelopers World Congress
- Propose talk: "Agent Orchestration in Go: Lessons From the Trenches"

---

## Section 5: Viral Names

### 5+ Names With Full Analysis

#### 1. **Forge**

**Tagline:** "Forge your agents in Go. Run them anywhere."

**Why Viral:**
- Single word, verb-noun, memorable
- Evokes craftsmanship, creation, strength
- Already has AgentForge equity — Board knows it, community will follow
- Go developers love tool-related names (Terraform, Docker, Kubernetes)
- Short, tweetable, domain-able

**Domain:** forge.dev (check availability), forgeagent.com, goforge.dev
**SEO keywords:** forge agent framework, forge AI orchestration, goforge, forge dev

**Risk:** "Forge" is common. Need to verify it's not taken by a major project.

---

#### 2. **Sentinel**

**Tagline:** "Sentinel watches your agents. Your agents watch everything else."

**Why Viral:**
- Evokes security, protection, watchfulness — our #1 differentiator
- Single word, three syllables, dramatic
- Conveys the capability-based security model implicitly
- "Sentinel" is already used in security contexts — borrows credibility
- Memorable, logo-friendly (watchtower, eye, shield)

**Domain:** sentinel.dev, sentinelagents.com, runsentinel.com
**SEO keywords:** sentinel agent security, sentinel agent framework, secure AI agents

**Risk:** HashiCorp Sentinel (policy-as-code). Different space but brand confusion possible.

---

#### 3. **Covenant**

**Tagline:** "Covenant AI: Agents that keep their promises."

**Why Viral:**
- Conveys trust, agreement, the capability contract
- Biblical/weighty — stands out from "cute" tech names
- Directly maps to capability-based security: "an agent's covenant is its permission set"
- Unique in tech — no major project uses this name
- Two syllables, pronounceable, spellable

**Domain:** covenant.ai, covenant.dev, covenantagents.com
**SEO keywords:** covenant agent framework, covenant AI security, covenant agent orchestration

---

#### 4. **Anvil**

**Tagline:** "Anvil: Forge agents. Strike hard. Ship fast."

**Why Viral:**
- Complements Forge — Anvil is where forging happens
- Short, punchy, single word
- Evokes strength, impact, blacksmithing/hardware
- No major tech project called "Anvil" (there was a Python full-stack framework, defunct)
- Go developers will appreciate the metaphor: compile = strike, binary = forged product

**Domain:** anvil.dev, anvilagents.com, useanvil.com
**SEO keywords:** anvil agent framework, anvil AI, anvil Go agents

---

#### 5. **Provenance**

**Tagline:** "Provenance AI: Every decision, tracked. Every action, auditable."

**Why Viral:**
- Uniquely positions around audit trails and determinism
- SBOM/provenance is a hot topic in supply chain security
- Maps to our MeMex memory architecture (git-tracked, immutable history)
- Enterprise procurement teams love "provenance" — it's literally what they ask for
- Sophisticated name for the enterprise tier

**Domain:** provenance.ai, provenance.dev, provenancedev.com
**SEO keywords:** provenance agent framework, auditable AI agents, agent decision tracking

---

#### 6. **Legion**

**Tagline:** "Legion: One command. A thousand agents."

**Why Viral:**
- Evokes armies, orchestration, scale
- Perfect metaphor: a legion is a coordinated military unit (department → legion)
- Dramatic, memorable, logo-friendly (Roman eagle, standard)
- "We are Legion" meme potential (but manageable)
- Conveys the concurrent goroutine model: spawning agents like raising a legion

**Domain:** legion.dev, legionagents.com, runlegion.com
**SEO keywords:** legion agent framework, legion AI orchestration, legion concurrent agents

---

#### 7. **Crucible** ⭐ (CEO Pick)

**Tagline:** "Crucible: Where agents are forged, tested, and hardened."

**Why Viral:**
- Direct line from AgentForge → Crucible (forge → crucible = container where metal is melted and refined)
- Evokes testing, heat, pressure, quality — exactly what the CLL does
- Unique in tech — no major project uses this name
- Beautiful metaphor: agents enter the crucible, are tested by fire (our pipelines), emerge hardened
- Three syllables, memorable, logo-friendly (flame, vessel, molten metal)
- The "crucible" is the process — the Closed Learning Loop is literally the crucible

**Domain:** crucible.dev, crucible.ai, crucibleagents.com, thecrucible.dev
**SEO keywords:** crucible agent framework, crucible AI, crucible agent testing, crucible AI orchestration

**Why this wins:** It's the perfect bridge between AgentForge (our origin story) and the new product. "AgentForge built the forge. Crucible is the vessel where agents are refined." It's aspirational, technical, and emotional.

---

### Name Ranking

| Rank | Name | Brand Strength | SEO Potential | Uniqueness | Domain Viability | Overall |
|---|---|---|---|---|---|---|
| 1 | **Crucible** | 9/10 | 8/10 | 9/10 | 7/10 | **8.5/10** |
| 2 | Forge | 8/10 | 9/10 | 6/10 | 6/10 | 7.5/10 |
| 3 | Sentinel | 8/10 | 8/10 | 7/10 | 7/10 | 7.5/10 |
| 4 | Legion | 7/10 | 7/10 | 8/10 | 8/10 | 7.5/10 |
| 5 | Covenant | 7/10 | 7/10 | 8/10 | 8/10 | 7.5/10 |
| 6 | Provenance | 6/10 | 6/10 | 9/10 | 6/10 | 7/10 |
| 7 | Anvil | 7/10 | 6/10 | 6/10 | 7/10 | 6.5/10 |

**Recommendation:** Crucible as primary. Hold Forge and Sentinel as backups.

---

## Section 6: Monetization Model

### 6.1 Tier Structure

| Tier | Price | What You Get |
|---|---|---|
| **Community (Free)** | $0/month | Single node, 5 agents, 2 departments, Community plugins only, Documentation, GitHub Discussions |
| **Pro** | $29/month | 50 agents, 10 departments, Plugin marketplace access, Email support, Advanced observability, CI/CD integrations |
| **Team** | $99/month (5 seats) | 250 agents, Unlimited departments, RBAC, Shared pipelines, SSO (Google/GitHub), Priority support, Audit logging |
| **Enterprise** | $499/month (20 seats) | Unlimited agents, Air-gapped deploy, Custom plugin registry, SLA (99.9%), Dedicated support, Compliance reports (GDPR, EU AI Act), SSO (SAML/OIDC), On-premise deployment support, SBOM for every release |
| **Enterprise+** | Custom/$2K+/month | Everything in Enterprise + Custom integrations, White-glove onboarding, Training workshops, Priority feature requests, Co-marketing, Dedicated Slack channel |

### 6.2 Revenue Projections

**Conservative (Year 1):**

| Month | Community | Pro | Team | Enterprise | MRR |
|---|---|---|---|---|---|
| 1 (Launch) | 500 | 20 | 5 | 0 | $1,075 |
| 3 | 2,000 | 100 | 25 | 2 | $5,400 |
| 6 | 5,000 | 300 | 75 | 10 | $18,615 |
| 12 | 15,000 | 800 | 200 | 30 | $58,000 |

**Year 1 ARR target:** $696,000

**Optimistic (Year 1):**

| Month | Community | Pro | Team | Enterprise | MRR |
|---|---|---|---|---|---|
| 1 (Launch) | 1,000 | 50 | 15 | 2 | $3,525 |
| 3 | 5,000 | 300 | 80 | 8 | $17,690 |
| 6 | 12,000 | 800 | 200 | 30 | $51,720 |
| 12 | 30,000 | 2,000 | 500 | 80 | $143,420 |

**Year 1 ARR target (optimistic):** $1,721,040

**Assumptions:**
- Conversion rate: 2-3% Community → Pro
- Churn: 5% monthly (improving to 3% by month 6)
- CAC: $0 initially (organic/content marketing), then $50-100 through paid
- Enterprise sales cycle: 60-90 days

### 6.3 Distribution Channels

| Channel | Strategy | Timeline |
|---|---|---|
| **GitHub** | Open source, README-first, star growth | Day 1 |
| **Go ecosystem** | pkg.go.dev, Go Weekly newsletter, GopherCon proposals | Week 1-4 |
| **Hacker News** | "Show HN" launch post | Launch day |
| **r/golang, r/MachineLearning** | Technical deep dives, not ads | Week 1-4 |
| **Dev.to, Medium** | Cross-post technical blog posts | Ongoing |
| **YouTube** | Tutorial videos, architecture walkthroughs | Month 1-3 |
| **Comparison content** | "[Name] vs OpenClaw" SEO landing pages | Launch week |
| **Enterprise direct** | Cold outreach to OpenClaw enterprise users looking for security | Month 3+ |
| **Conferences** | CFP submissions to GopherCon, FOSDEM, KubeCon | Month 2-6 |
| **Newsletters** | Go Weekly, Golang Weekly, TLDR AI, The Batch | Monthly sponsorship |

---

## Section 7: 30-Day Launch Plan

### Week 1: Foundation (Days 1-7)

| Day | Milestone | Deliverable |
|---|---|---|
| **Day 1** | Project scaffold | Go module, directory structure, CI/CD (GitHub Actions), goreleaser config |
| **Day 2** | Core daemon | `nemesis` binary starts, health endpoint, graceful shutdown, config loading (HCL) |
| **Day 3** | Agent goroutine model | Agent spawn/kill, capability token parsing, agent lifecycle management |
| **Day 4** | CSP message bus | Typed channels, message routing, department registration, select-based dispatcher |
| **Day 5** | Memory store v0 | SQLite schema, MeMex Zero RAG integration (file read/write/git), FTS5 indexing |
| **Day 6** | Tool system v0 | Built-in tool execution (fs, http, exec), capability enforcement, audit logging |
| **Day 7** | Integration test | End-to-end: spawn agent, send message, tool call, memory write, audit log entry |

**Week 1 Go/No-Go:** Agent can spawn, receive a message, call a tool, write to memory, and terminate. Capability enforcement works.

### Week 2: Features (Days 8-14)

| Day | Milestone | Deliverable |
|---|---|---|
| **Day 8** | Department system | Department goroutine pools, AGENTS.md parsing, inter-department channels |
| **Day 9** | Pipeline DAG engine | HCL pipeline definitions, topological sort, DAG execution with channels |
| **Day 10** | LLM adapter v0 | Multi-provider interface, OpenAI + Anthropic + Ollama adapters, streaming support |
| **Day 11** | Closed Learning Loop v0 | GEPA implementation, lesson extraction, MeMex writeback, skill versioning |
| **Day 12** | Subagent tree | Parent spawn → child results → merge, capability inheritance, timeout handling |
| **Day 13** | Messaging bridge v0 | Discord + Telegram adapters, surface router, format normalization |
| **Day 14** | Docker deployment | 6MB Docker image, docker-compose.yaml, healthcheck, volume mounts for MeMex |

**Week 2 Go/No-Go:** Multi-agent pipeline runs end-to-end. Content agent → SEO agent → PDF agent in a DAG. Results in MeMex.

### Week 3: Polish & Launch Prep (Days 15-21)

| Day | Milestone | Deliverable |
|---|---|---|
| **Day 15** | Observability | OpenTelemetry integration, agent traces, pipeline metrics, Prometheus endpoint |
| **Day 16** | Web dashboard v0 | HTMX + SSE, agent status, pipeline DAG visualization, MeMex browser |
| **Day 17** | WASM plugin SDK v0 | Plugin interface spec, example plugin (weather), sandbox verification |
| **Day 18** | Tool marketplace v0 | JSON registry, SHA-256 content addressing, capability manifest, install/verify |
| **Day 19** | Documentation v0 | README.md, docs/ with mkdocs, API reference, Quickstart guide (5 min) |
| **Day 20** | Comparison landing pages | "vs OpenClaw", "vs Hermes", "vs OpenHuman" — honest, detailed, SEO-optimized |
| **Day 21** | Launch checklist | GitHub repo public, social media accounts, Docker Hub, Homebrew formula |

**Week 3 Go/No-Go:** Repo is public-ready. Documentation is complete. Landing pages are live. Docker image is published.

### Week 4: Launch & Respond (Days 22-30)

| Day | Milestone | Deliverable |
|---|---|---|
| **Day 22** | **LAUNCH DAY** | "Show HN" post, r/golang post, Twitter/X announcement, Discord community open |
| **Day 23** | Community response | Answer every GitHub issue, every HN comment, every Reddit thread within 2 hours |
| **Day 24** | First tutorial published | "Build Your First Agent Pipeline in 5 Minutes" — blog, video, gist |
| **Day 25** | Enterprise landing page | "Enterprise Agent Orchestration" — security, compliance, air-gapped, SLA |
| **Day 26** | Plugin contest announced | "Build a Crucible plugin, win $500" — drives ecosystem growth |
| **Day 27** | First user story collected | Reach out to early adopters, get quotes, publish case study |
| **Day 28** | Week 1 retrospective | What broke? What surprised us? What do users want next? |
| **Day 29** | v0.2 roadmap published | Based on community feedback, transparent, prioritized |
| **Day 30** | v0.2.0 release | Bug fixes from launch feedback, first community PRs merged |

**Week 4 Success Metric:** 1,000+ GitHub stars, 50+ Pro signups, 5+ Team signups, active Discord community.

---

## Appendix A: Relationship to AgentForge

**Crucible IS NOT AgentForge.** AgentForge is our internal production system — 14 departments, content pipeline, SEO automation. It runs on OpenClaw (TypeScript).

**Crucible is the productization of AgentForge's learnings.** Every lesson in this blueprint came from 11 days of running AgentForge in production:
- The memory architecture (MeMex) → Crucible's Memory Store
- The department model → Crucible's Department System
- The pipeline DAG (and the Part B problem) → Crucible's Pipeline Scheduler
- The dual-write decay problem → Crucible's synchronous mirror
- The SEO API single-point-of-failure → Crucible's circuit breaker pattern
- The learning loop atrophy → Crucible's CLL execution

**AgentForge will be Crucible's first enterprise customer.** We dogfood our own product. AgentForge migrates from OpenClaw to Crucible. This is both the ultimate proof and the best case study.

---

## Appendix B: Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| OpenClaw adds Go agent SDK | Medium | High | First-mover advantage. Go is our differentiator; they'd be catching up |
| Hermes adds async/concurrency | Medium | Medium | Their Python monolith is hard to refactor. Go's concurrency model is superior |
| OpenHuman ships headless mode | High | Medium | We ship first. Their desktop DNA makes headless an afterthought |
| Community doesn't materialize | Low-Medium | Critical | Pre-build content pipeline. Hacker News launch is make-or-break |
| Enterprise sales cycle too long | Medium | Medium | Start with self-serve Pro/Team. Enterprise is month 3+ |
| Burnout (solo/small team) | High | High | Scope ruthlessly. Ship MVP in 30 days. No feature creep. This blueprint is the contract |
| Go talent hard to hire | Low | Low | Go is the #3 language on GitHub. Remote-first. Dublin + EU talent pool |

---

## Appendix C: Open Source Strategy

**License:** BUSL-1.1 (Business Source License) → Apache 2.0 after 4 years

**Rationale:** BUSL prevents AWS/GCP from offering Crucible-as-a-service without paying us. Converts to fully open Apache 2.0 after 4 years (like HashiCorp, Sentry, CockroachDB). This is the enterprise-approved open source model.

**Dual-licensing:** Enterprise tier gets Apache 2.0 immediately (for compliance/audit).

**CLA:** No CLA required. DCO (Developer Certificate of Origin) instead. Lower friction for contributors.

---

## Appendix D: Success Metrics

| Metric | 30-Day Target | 90-Day Target | 1-Year Target |
|---|---|---|---|
| GitHub Stars | 1,000 | 5,000 | 20,000 |
| Community Users | 500 | 2,000 | 15,000 |
| Pro Subscribers | 20 | 100 | 800 |
| Team Subscribers | 5 | 25 | 200 |
| Enterprise Customers | 0 | 8 | 30 |
| MRR | $1,075 | $5,400 | $58,000 |
| Community Plugins | 5 | 30 | 200 |
| Contributors | 3 | 15 | 100 |
| Blog Posts Published | 8 | 20 | 50 |
| Docker Pulls | 1,000 | 10,000 | 100,000 |

---

*End of Blueprint v1.0. Submitted for Board review 2026-06-01.*