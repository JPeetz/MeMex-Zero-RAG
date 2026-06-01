---
title: "The AI Agent Security Gap — How AgentForge Closes It"
meta_description: "OpenClaw gives agents full host access. Hermes has CVEs. OpenHuman gets OAuth to 118 services. AgentForge uses capability-based security — zero by default."
target_keyword: "AI agent security"
status: draft
date: 2026-06-02
author: "AgentForge Team"
---

# The AI Agent Security Gap — How AgentForge Closes It

## Executive Summary

Every major AI agent framework on the market today treats security as an afterthought. They ship with full host access, trust every plugin by default, and rely on the user — not the architecture — to figure out the security model. The result: credential theft, remote code execution, and persistent backdoors on production machines. This is not theoretical. Four CVEs in one chain can compromise an OpenClaw deployment. A path traversal bug in Hermes Agent lets attackers read arbitrary files. OpenHuman asks you to hand OAuth tokens for 118 services to a single desktop process.

**AgentForge is different.** Built from first principles on **capability-based security** (OCap), every agent spawns with zero permissions. It compiles to a 6 MB static binary — a **Go agent framework** with no Node.js runtime, no Python venv, no Tauri webview. This article is a technical audit of where the incumbents fail and how AgentForge solves the security problem at the architectural level.

---

## 1. The Three Frameworks, Audited

Before we can talk about solutions, we need to understand the problem. Here's what a security-minded evaluation of the three leading agent frameworks reveals.

### OpenClaw: Full Host Access, Full Blast Radius

OpenClaw is the most deployed AI agent framework. Every installation runs with the user's full host privileges — a fundamental **agent framework security** failure that cascades into every layer of the system.

**The Claw Chain.** On May 17, 2026, Cyera researchers disclosed four vulnerabilities in OpenClaw — collectively named "Claw Chain" — that enable a single foothold to escalate to credential theft, privilege escalation, and persistent backdoor placement on the host system. The most severe, **CVE-2026-44112**, carries a CVSS score of **9.6 (Critical)**. It exploits a time-of-check/time-of-use (TOCTOU) race condition in the OpenShell sandbox to redirect write operations outside the intended isolation boundary.

The Cloud Security Alliance's research note is blunt:

> "Organizations running any OpenClaw version prior to 2026.4.22 should treat all credentials, API keys, and secrets reachable by their OpenClaw process as potentially compromised and initiate rotation."

The **OpenClaw security** model treats full host access as the default. A 2026 systematic taxonomy on arXiv analysed 190 security advisories, identifying attack surfaces across seven architectural layers. MCP servers extend this reach to Google Calendar, Notion, Jira, Confluence, Stripe, and GitHub — making any compromise functionally equivalent to a privileged service account breach.

**Cisco's assessment** (Amy Chang, Vineeth Sai Narajala, Idan Habler):

> "From a security perspective, it's an absolute nightmare. Granting an AI agent high-level privileges enables it to do harmful things if misconfigured or if a user downloads a skill that is injected with malicious instructions. Security for OpenClaw is an option, but it is not built in."

Barracuda Networks independently classified agentic AI as a "threat multiplier" and OpenClaw deployments as "functionally equivalent to a privileged service account." Bitsight found exposed OpenClaw instances discoverable on the public internet.

**The npm supply chain.** OpenClaw is a Node.js application with a dependency tree running into thousands of packages. Each one is a potential entry point. The framework's trust model explicitly states it is "not designed as a shared multi-tenant boundary between adversarial users," meaning any compromise of the Node.js runtime is outside the project's stated security boundary.

### Hermes Agent: One CVE, 35 Vulnerabilities, 18 Attack Chains

Hermes Agent (NousResearch, v0.8.0) is positioned as a "secure" alternative to OpenClaw. The documentation markets it as working on Linux and mobile with sandboxing. The reality is less reassuring.

**CVE-2026-7396.** A path traversal vulnerability in the WeChat Work platform adapter (`gateway/platforms/wecom.py`). CVSS 4.0 vector: `AV:N/AC:L/AT:N/PR:N/UI:N/VC:L/VI:N/VA:N/SC:N/SI:N/SA:N`. Remote, unauthenticated, with a publicly available exploit. The CNA analysis classifies this as CWE-22 — Improper Limitation of a Pathname to a Restricted Directory.

**35 vulnerabilities, 18 exploitable attack chains.** Repello AI's red-team engagement identified 35 total **Hermes Agent vulnerabilities** and 18 independently exploitable attack chains in Hermes Agent. Their threat model identifies three primary attack surfaces:

1. **Skill marketplace as a supply-chain surface** — same vector as OpenClaw's ClawHub, but Hermes' own marketplace has no mandatory code review.
2. **Memory injection through retrieved context** — a Hermes-specific class of attack where retrieved memory documents are used as prompt injection vectors.
3. **Sync bottlenecks** — Hermes Agent's Python process model creates single-threaded execution paths where a blocked agent blocks the entire system.

**The security policy tells the story.** Hermes Agent's own security documentation states:

> "The only security boundary against an adversarial LLM is the OS-level isolation wrapper around the entire process. A malicious or buggy plugin is not a vulnerability in Hermes Agent."

Translation: if a skill is malicious, that's your problem, not theirs. There is no capability restriction, no sandboxed plugin execution, and no permission model within the agent itself. The only protection is "run the whole thing in a container" — which is advice, not architecture.

### OpenHuman: 118 OAuth Tokens, One Desktop Process

OpenHuman (TinyHumans AI) is an open-source (GPL-3.0) desktop AI agent. **OpenHuman privacy** concerns center on the OAuth surface area — 118 services means 118 bearer tokens in a single process's memory space.

**The OAuth surface area.** 118 connected services means 118 bearer tokens living in a single process's memory space. If any component of that process — the Rust core, the Tauri shell, the embedded Chromium runtime, or any of the React dependencies — is compromised, all 118 tokens are exfiltratable in one operation. This is not a hypothetical: the QuickJS skills runtime was removed from OpenHuman, but the architecture still loads community skill metadata from `tinyhumansai/openhuman-skills` on GitHub, and the desktop app processes that metadata with CEF's full DOM privileges.

**Desktop-only, GPL-3.0.** OpenHuman cannot run headless. It cannot run on a server. It cannot run in CI/CD. GPL-3.0 is a non-starter for most enterprise legal teams. These aren't security issues per se, but they are architectural constraints that limit where security-conscious organisations can deploy it.

---

## 2. The Secret No One's Talking About: Agent Skills Are a Supply Chain Disaster

Every major framework has a skill marketplace. Every skill marketplace is a supply chain attack surface the size of npm in 2016. And the data is worse than anyone expected.

### The Numbers

| Source | Finding | Date |
|---|---|---|
| Koi Security / ClawHavoc | 341 malicious skills on ClawHub | Feb 1, 2026 |
| Expansion audit | 820+ malicious skills across 25+ attack categories | Feb-Mar 2026 |
| Cisco AI Skill Scanner | 26% of 31,000 agent skills contain ≥1 vulnerability | Apr 2026 |
| Snyk ToxicSkills | 13.4% (534 skills) had critical security issues; 36% prompt injection rate | Apr 2026 |
| Snyk credential report | 10.9% of skills exposed hardcoded secrets | Mar 2026 |

### How the Attacks Work

On February 1, 2026, Koi Security researcher Oren Yomtov published findings from a complete audit of ClawHub, the official skill marketplace for OpenClaw. The ClawHavoc campaign had planted 341 malicious skills distributing the Atomic macOS Stealer, bypassing curation with week-old GitHub accounts. Attack vectors included:

1. **Staged downloads** — the SKILL.md instructs the agent to download and execute a secondary payload
2. **Prompt injection in skill descriptions** — an agent reading a skill's capabilities gets instructions to exfiltrate environment variables
3. **Obfuscated Base64 payloads** embedded in "example code" blocks within skill documentation
4. **Fake security-scanning skills** — the attackers literally impersonated security tools to gain trust

The ClawHavoc campaign expanded from 341 to 1,184+ skills across 25 attack categories: browser automation agents, coding assistants, LinkedIn integrations, WhatsApp bots, PDF tools, and fake security scanners.

### Reactive Patching Cannot Fix This

OpenClaw's response was a VirusTotal partnership announced February 7, 2026. Every skill published to ClawHub is now scanned. But this is signature-based detection — reactive, not architectural. It cannot catch novel attacks, and it cannot prevent a skill that passes initial scan from becoming malicious later (a known technique in package manager attacks, mirrored from npm/PyPI).

**The fundamental problem is not curation. It's that any skill runs with the agent's full permissions.** A PDF reader skill doesn't need filesystem write access. A weather skill doesn't need network access beyond one API endpoint. But in every current framework, skills inherit the agent's full ambient authority.

### How AgentForge Solves This

AgentForge skills run as **WASM agent plugins** inside WebAssembly sandboxes with explicitly granted capabilities. Every skill is verified by SHA-256 hash before execution. A skill cannot request permissions at runtime — it receives them at spawn time, and they cannot be escalated.

```
# AgentForge skill spawn
$ agentforge skill run weather-checker \
    --capability net:api.weather.gov:443 \
    --capability fs:read:./config \
    --hash sha256:a3f2b8c1...
```

No `--capability` flags? The skill can't touch the network. It can't read the filesystem. It can't spawn subprocesses. It's not a setting — it's enforced by the WASM runtime at the instruction level.

---

## 3. How AgentForge Thinks Differently

AgentForge is built on three principles that no other framework currently implements:

### Principle 1: Object-Capability (OCap) Security Model

An OCap system grants capabilities by reference, not by ambient authority. An agent cannot do anything unless it holds a reference to an object that can do that thing. There is no global `fs`, no global `net`, no global `process`. Every capability is:

- **Explicit** — granted in the agent's spawn manifest
- **Attenuable** — a capability can be restricted (e.g., "read one directory, not the whole filesystem")
- **Non-forgeable** — references are cryptographic, not guessable
- **Revocable** — capabilities can be withdrawn at any time

This is the same model that underpins seL4, the only OS kernel with a formal proof of correctness. It's the model that the Chrome sandbox and AWS IAM aspire to. AgentForge is the first agent framework with **capability-based security** (OCAP agents) as the core security primitive.

### Principle 2: MeMex Memory — No Vector Black Boxes

Every other agent framework that implements "memory" uses vector embeddings stored in an opaque database (Chroma, Pinecone, Qdrant, pgvector). These are black boxes — you cannot audit what was stored, what was retrieved, or whether a retrieved document is a prompt injection payload.

MeMex (Memory MExican standoff) is AgentForge's memory system. It stores all memories as **plaintext Markdown files** in a directory tree. You can `grep` them. You can `git diff` them. You can audit every byte. No vector database. No embeddings drift. No "what did the agent actually remember?" mystery.

For GDPR compliance — relevant to our Dublin-based development team and European enterprise customers — MeMex provides full Article 15 (right of access), Article 17 (right to erasure), and Article 30 (records of processing) compliance out of the box. You can prove what data your agent holds because it's all in files you control.

### Principle 3: CSP Goroutine Concurrency

AgentForge is written in Go. Every agent is a goroutine. Every inter-agent message is typed over a Go channel. This is not a Python `asyncio` loop or a Node.js event loop — it's true concurrent execution with the Go scheduler handling millions of goroutines across multiple OS threads.

- **No GIL** — unlike Python (Hermes Agent), Go has no Global Interpreter Lock
- **No callback hell** — unlike Node.js (OpenClaw), control flow is synchronous channels, not promise chains
- **No CEF** — unlike Tauri/OpenHuman, there's no embedded browser runtime

The entire AgentForge runtime — forge daemon, capability engine, memory system, WASM runtime, agent scheduler, MCP bridge — compiles to a single **6 MB static binary**. No runtime dependencies. No Python venv. No npm install. No webview. Ship it anywhere.

---

## 4. Capability-Based Security in Practice

Here's what spawning an agent looks like in AgentForge vs. the alternatives.

### AgentForge

```yaml
# agent.yaml — an AgentForge agent manifest
name: code-review-bot
model: claude-sonnet-4
capabilities:
  - type: filesystem
    paths: ["/home/project/src"]
    permissions: [read]
  - type: network
    hosts: ["api.github.com:443"]
    permissions: [connect]
  - type: process
    commands: ["git", "go", "golangci-lint"]
    permissions: [read-only]
  - type: memory
    namespace: "code-review"
    permissions: [append]
memory:
  provider: memex
  path: /var/agentforge/memory/code-review-bot
```

This agent can:
- Read source files in `/home/project/src`
- Connect to GitHub's API
- Run `git diff`, `go vet`, and `golangci-lint` in read-only mode
- Append to its own memory namespace

It cannot:
- Write any file anywhere
- Open outbound connections to any other host
- Spawn arbitrary processes
- Read any other agent's memory
- Access environment variables

### OpenClaw (equivalent configuration)

```json
{
  "name": "code-review-bot",
  "model": "claude-sonnet-4",
  "skills": ["git", "github", "code-review", "golang"]
}
```

This agent can do anything your user account can do. Every installed skill inherits your full shell access, filesystem access, and API keys. If any of those four skills contains a malicious instruction — and Cisco's data says there's a 26% chance that at least one does — the attacker has your keys.

### Hermes Agent (equivalent)

```python
# No capability model exists. The agent runs with full Python process permissions.
# The security policy says: run the whole thing in a container. That's it.
```

### The Compliance Angle

For enterprises in the DACH region, UK/Ireland, and the US, this isn't just a security preference — it's a regulatory requirement.

- **EU AI Act (effective August 2026):** High-risk AI systems require "appropriate levels of robustness, security, and accuracy." An agent framework without capability restrictions cannot demonstrate this.
- **GDPR Article 25:** Data protection by design and by default. An agent that has access to all user data by default is non-compliant by design.
- **ISO 27001 / SOC 2:** The principle of least privilege is audit requirement A.9.1.2. "Full host access" fails this control on its face.

---

### The MCP Agent Framework Advantage: Server *and* Client

The Model Context Protocol (MCP) is becoming the standard for connecting LLMs to external tools. AgentForge is the only **MCP agent framework** that operates as both server and client.

### What This Means

**As an MCP server:** Connect Claude Desktop, Cursor, or any MCP-compatible client directly to AgentForge. The forge daemon exposes your agents, capabilities, and memory as MCP tools and resources.

```
claude_desktop_config.json:
{
  "mcpServers": {
    "agentforge": {
      "command": "agentforge",
      "args": ["serve", "--mcp"]
    }
  }
}
```

Claude Desktop can now discover and interact with your AgentForge agents through a typed, secure protocol. Each agent's capabilities are exposed as MCP tool descriptions — Claude knows exactly what each agent can do before it calls it.

**As an MCP client:** AgentForge agents can connect to any MCP server — databases, APIs, file systems, SaaS tools — through the same capability-gated channel. An agent granted `mcp:postgres://readonly` can query a database but cannot write. An agent with `mcp:github://issues` can read and create issues but cannot access repositories.

**No other framework does this.** OpenClaw integrates with MCP servers as a client but does not expose itself as an MCP server. Hermes Agent's MCP support is experimental and client-only. OpenHuman has no MCP support at all.

---

## 6. Why Go?

Every major agent framework uses Python or Node.js/TypeScript. AgentForge uses Go. This is not an aesthetic choice — it's a security decision.

### Concurrency Without Compromise

```go
// AgentForge spawns agents as goroutines
func (f *Forge) DeployAgent(spec AgentSpec) (*Agent, error) {
    agent := &Agent{
        id:           uuid.New(),
        capabilities: spec.Capabilities,
        memex:        f.memex.Namespace(spec.MemoryNS),
        inbox:        make(chan Message, 64),
        outbox:       make(chan Message, 64),
        shutdown:     make(chan struct{}),
    }
    go agent.Run()
    return agent, nil
}
```

Each goroutine costs ~2 KB of stack space. You can run thousands of concurrent agents on a Raspberry Pi. The Go scheduler distributes goroutines across all available OS threads — no GIL bottleneck, no async/await fragmentation, no callback chains.

### Channels = Inter-Agent Communication

```go
// Agents communicate through typed channels
type AgentBus struct {
    subscribers map[string]chan Message
    mu          sync.RWMutex
}

func (b *AgentBus) Publish(topic string, msg Message) {
    b.mu.RLock()
    defer b.mu.RUnlock()
    if ch, ok := b.subscribers[topic]; ok {
        select {
        case ch <- msg:
        default:
            // Backpressure — agent is overloaded, message is dropped
        }
    }
}
```

Channels are typed, bounded, and provide natural backpressure. No message broker. No Redis. No Kafka. Just Go's CSP model, which is proven in production at Google, Uber, and Cloudflare.

### One Binary, Everywhere

```bash
# Build for any target
GOOS=linux GOARCH=amd64 go build -o agentforge
GOOS=linux GOARCH=arm64 go build -o agentforge  # Raspberry Pi
GOOS=darwin GOARCH=amd64 go build -o agentforge  # macOS

# Ship it
docker build -t agentforge:latest .
kubectl apply -f deploy/agentforge-daemonset.yaml

# Or air-gapped
scp agentforge airgapped-server:/usr/local/bin/
```

6 MB. No runtime. No package manager. No virtual environment. No browser engine. No npm audit nightmare.

---

## 7. What's Shipping

AgentForge is in active development. Here's where we are and where we're going.

### ✅ Ready Now (v0.1.0)

- **Core runtime:** Capability engine, agent lifecycle management, forge daemon
- **MeMex memory:** Plaintext Markdown memory with namespace isolation
- **Agent spawning:** OCap-gated agent creation with explicit capability manifests
- **Documentation:** Architecture docs, API reference, security model whitepaper
- **HTML help:** Complete offline help system shipped in the binary

### 🚧 In Development

- **TUI (Terminal UI):** A Bubble Tea-based terminal dashboard for managing agents, viewing memory, and inspecting capabilities
- **Web GUI:** A lightweight web interface for agent management and monitoring
- **MCP bridge:** Full MCP server+client implementation
- **Desktop app:** A standalone application for local agent deployment
- **WASM plugin SDK:** The toolchain for building and signing AgentForge skills

### 🗺️ Roadmap

- Q3 2026: TUI release, MCP bridge alpha
- Q4 2026: Web GUI, desktop app beta, WASM SDK public preview
- Q1 2027: Plugin marketplace with mandatory SHA-256 verification, enterprise SSO

---

## 8. What This Means for You

If you're evaluating AI agent frameworks for your organisation — especially if you operate under GDPR, the EU AI Act, SOC 2, or ISO 27001 — here's the checklist:

| Requirement | OpenClaw | Hermes Agent | OpenHuman | AgentForge |
|---|---|---|---|---|
| Capability-based security | ❌ | ❌ | ❌ | ✅ |
| Zero permissions by default | ❌ | ❌ | ❌ | ✅ |
| WASM sandbox for plugins | ❌ | ❌ | ❌ | ✅ |
| Auditable memory (plaintext) | ❌ | ❌ | ❌ | ✅ |
| MCP server + client | ❌ (client only) | ❌ (client only) | ❌ | ✅ |
| Static binary, no runtime | ❌ (Node.js) | ❌ (Python) | ❌ (Tauri/CEF) | ✅ (6 MB Go) |
| Headless deployment | ✅ | ✅ | ❌ (desktop only) | ✅ |
| Air-gapped capable | ❌ | ⚠️ | ❌ | ✅ |
| GDPR Article 25 by design | ❌ | ❌ | ❌ | ✅ |

**AgentForge is the only framework where security is an architectural invariant, not a configuration option.**

---

## 9. Join the Forge

AgentForge is open source, Apache 2.0 licensed, and developed in Dublin, Ireland by a team that has spent years watching agent frameworks ship features without security — and decided to build one where those two things are the same.

- **GitHub:** [github.com/JPeetz/agentforge](https://github.com/JPeetz/agentforge)
- **Star the repo** — it helps others find an agent framework that takes their security seriously
- **Open an issue** — tell us what capability primitives your use case needs
- **Contribute** — the WASM SDK, MCP bridge, and TUI are all in active development
- **Discuss** — security model feedback, architecture questions, deployment war stories

Agent frameworks are about to become infrastructure as fundamental as databases. We can't afford to build them with 2016 npm's security model. AgentForge proves it's possible to do better.

---

*AgentForge is an Irish-founded, Dublin-based open-source project. Built in Go. Secured by OCap. Auditable by design.*

---

## References

1. Cloud Security Alliance, "Claw Chain: Four CVEs Enable Full AI Agent Compromise," May 17, 2026. [CSA Research Note](https://labs.cloudsecurityalliance.org/wp-content/uploads/2026/05/CSA_research_note_openclaw-claw-chain-cve_20260517-csa-styled.pdf)
2. CVE-2026-44112 — OpenClaw OpenShell TOCTOU Race Condition, CVSS 9.6
3. CVE-2026-7396 — NousResearch Hermes Agent Path Traversal, CWE-22
4. "A Systematic Taxonomy of Security Vulnerabilities in the OpenClaw AI Agent Framework," arXiv:2603.27517, 2026.
5. Cisco AI Threat & Security Research, "Personal AI Agents like OpenClaw Are a Security Nightmare," blogs.cisco.com, April 2026.
6. Barracuda Networks, "OpenClaw Security Risks: What Security Teams Need to Know About Agentic AI," blog.barracuda.com, April 2026.
7. Bitsight, "OpenClaw Security: Risks of Exposed AI Agents Explained," bitsight.com, 2026.
8. Repello AI, "Hermes Agent Security: A Threat Model for Enterprise Workstation Agents," repello.ai, 2026.
9. Snyk, "ToxicSkills: Malicious AI Agent Skills on ClawHub," snyk.io, April 2026.
10. Koi Security / Oren Yomtov, "ClawHavoc: 341 Malicious Clawed Skills Found by the Bot They Were Targeting," koi.ai, February 2026.
11. eSecurity Planet, "Hundreds of Malicious Skills Found in OpenClaw's ClawHub," esecurityplanet.com, February 2026.
12. Termdock, "ClawHub Incident: 341 Malicious Skills Exposed," termdock.com, 2026.
13. PurpleBox Security, "AI Agent Skills: The New Supply Chain Risk," prplbx.com, February 2026.
14. EU AI Act, Regulation (EU) 2024/1689, effective August 2026.
15. GDPR, Regulation (EU) 2016/679, Articles 15, 17, 25, 30.