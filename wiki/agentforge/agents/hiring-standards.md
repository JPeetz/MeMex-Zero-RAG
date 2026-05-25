# AgentForge Agent Design Standards — Quality Benchmarks

_Inspired by pguso/ai-agents-from-scratch. Approved by CEO 2026-05-24._

## Core Principle

Every AgentForge agent must be built from first principles. No agent deploys without the hiring department understanding what happens under the hood. The `ai-agents-from-scratch` repository (pguso) defines the learning path: raw LLM calls → tool calling → ReAct patterns → production frameworks. AgentForge agents follow this same progression.

## Design Checklist (Adversarial Review Requirement)

Before any agent is approved for deployment, the hiring department must verify:

### Level 0 — Fundamentals
- [ ] Agent understands its system prompt, not just obeys it. It can state its role, constraints, and when it should escalate.
- [ ] Agent's model choice is justified. Not just "use DeepSeek V4 Pro by default" — why this model for this agent? Latency, cost, reasoning depth?
- [ ] Agent's temperature/top-p settings are deliberate, not defaulted.

### Level 1 — Tool Architecture (ai-agents-from-scratch: intro → translation)
- [ ] Every tool the agent has access to is documented — what it does, when it should be used, when it should NOT be used.
- [ ] The agent knows which tools it has. It never tries to call a tool it doesn't have. It never avoids calling a tool it does have.
- [ ] Tool output parsing is resilient. The agent doesn't crash on unexpected output format.

### Level 2 — Agent Loop (ai-agents-from-scratch: react-agent)
- [ ] Multi-step task execution works. Agent can plan → execute → observe → replan without getting stuck in loops.
- [ ] Agent knows when to stop. It doesn't continue searching/refining past the point of diminishing returns.
- [ ] Agent can handle tool failures gracefully. If a web_search returns empty, it tries a different query. If a file read fails, it checks if the path exists.
- [ ] Agent has explicit timeout/iteration limits. No infinite loops.

### Level 3 — Memory (ai-agents-from-scratch: scaling)
- [ ] Agent writes its outputs to the correct location (MeMex artifacts, Obsidian, or both).
- [ ] Agent reads from MeMex + Obsidian before making decisions, not after.
- [ ] Consultation order: MeMex → Obsidian → External. Never skip steps.
- [ ] Agent logs significant decisions. Future instances of the same agent can learn from past decisions.

### Level 4 — Production Readiness (ai-agents-from-scratch: coding → tools)
- [ ] Agent's pipeline is idempotent. Running it twice on the same day produces consistent results, not duplicated/conflicting output.
- [ ] Agent has a defined failure mode. What does "no winner today" look like? What does "I can't complete this" look like? Not just silence — explicit, actionable status.
- [ ] Agent's output is machine-readable where needed. Downstream agents can parse its artifacts without guessing formats.
- [ ] Agent's cron schedule is justified. Why this time? Why this frequency? What happens if it's delayed by 2 hours?

### Level 5 — Local-First Capability (ai-agents-from-scratch: entire philosophy)
- [ ] Agent's critical functions work without external API calls where possible. Local inference > cloud inference for privacy and cost.
- [ ] Agent's fallback behavior when external services are down is defined and tested. SearXNG goes down → what does the agent do?
- [ ] Agent doesn't leak private data to external services unnecessarily. Consult the privacy boundary before every external call.

## Adversarial Review Process

1. **Design document** → Hiring department receives the proposed agent design.
2. **Self-review** → The design document must include a self-assessment against this checklist.
3. **Adversarial review** → A separate hiring agent role-plays as a hostile user/environment, attempting to break the agent's pipeline.
4. **CEO sign-off** → Marvin reviews the adversarial report and approves or sends back.

## Reference Architecture: BiteSaver AI (App Discovery → Production)

The BiteSaver scaffold (2026-05-24) applies ai-agents-from-scratch principles to a real production app:

| ai-agents-from-scratch Example | BiteSaver Feature |
|---|---|
| `intro/` — Model loading | Local LLM (Phi-4-mini) initialization on app launch |
| `translation/` — Specialized prompts | Recipe extraction system prompt |
| `react-agent/` — Tool calling loop | AI meal planning: read saved recipes → generate plan |
| `coding/` — Structured generation | Recipe scaling calculations |
| `scaling/` — Concurrent execution | Multiple recipe extraction in parallel |

## Tools for Agent Building

- **llama.cpp:** Local LLM inference for agent decision-making (no cloud API dependency)
- **node-llama-cpp:** Node.js bindings for agents that run in OpenClaw environment
- **MediaPipe LLM Inference:** Google's on-device inference for Android-based agents
- **MLX Swift:** Apple-native on-device inference for iOS-based agents
- **ai-agents-from-scratch:** The canonical learning path — every hiring agent must complete the examples before designing production agents

---

_Updated: 2026-05-24. Source: pguso/ai-agents-from-scratch (GitHub). Applies to all current and future AgentForge agents._