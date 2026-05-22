# Research: RedPlanetHQ CORE — Personal AI Operating System

**Date:** 2026-05-19
**Status:** ✅ Complete
**Relevance:** Architecture patterns for CEO/Marvin agent, persistent memory implementation, multi-app integration

---

## Executive Summary

CORE is an open-source, self-hosted personal AI operating system that functions as a persistent digital assistant rather than a traditional chatbot. It monitors digital activity across 50+ integrated applications, maintains temporal knowledge graphs across sessions, and autonomously delegates work to specialized agents (Claude Code, Codex) with human-in-loop approval workflows.

**Key Differentiator:** CORE distinguishes itself through persistent memory architecture (88.24% accuracy on LoCoMo benchmark), proactive app automation via webhooks, and explicit accountability through audit logs and approval flows.

---

## Architecture Overview

### Core Components

#### 1. **Memory System** (Knowledge Graph)
- **Temporal reasoning** across all tasks and conversations
- Tracks context, decisions, timing, and reasoning
- Benchmark performance: 88.24% accuracy (LoCoMo - single-hop, multi-hop, open-domain, temporal reasoning)
- Persists across unrelated tasks and session resets
- Semantic understanding of task relationships and dependencies

**Implementation Insight for AgentForge:**
- The Hive Mind signals system should be extended with temporal tracking
- Agent outputs should be stored with temporal metadata
- Cross-agent learning benefits from understanding *when* decisions were made, not just *what* was decided

#### 2. **Task Management**
- Structured work units with explicit state tracking
- Planning phase before execution
- Spawns specialized agents (Claude Code, browser automation)
- Escalation to human when blockers occur
- Audit logs for all decisions and delegations

**Implementation Insight:**
- Mission tasks structure is aligned with CORE's approach
- Should add explicit escalation paths when agents encounter blockers
- Audit trail in hive_mind is analogous to CORE's audit logs

#### 3. **Multi-App Connectors** (50+ Services)
Connected via MCP endpoints and webhooks:
- **Developer Tools:** GitHub, Linear, Sentry, LaunchDarkly
- **Communication:** Slack, Gmail, WhatsApp (via bot gateways)
- **Productivity:** Notion, Airtable, Asana
- **Cloud:** AWS, GCP, Azure (via provider SDKs)
- **Custom APIs:** Webhook ingestion for any service

**Pattern:**
- Services push events → CORE processes webhooks → Agents take action
- Approval workflows prevent autonomous mistakes
- Context is fetched from multiple sources before delegating

**For AgentForge:**
- Mission Queue system is already event-driven (via polling)
- Could extend to webhook-driven dispatch when agents are overloaded
- Multi-app context loading for research missions (pull from GitHub, Notion, Slack before research starts)

#### 4. **Gateway & Runtime**
- Executes agents via Claude Code or Codex
- Supports local terminal execution or remote (Docker/Railway)
- Environment variables for secrets and config
- Timeout and resource management
- Output capture and error handling

**Technical Detail:**
- Similar to our native executor that polls mission_tasks and spawns agents
- CORE's approach is webhook-driven (push) while ours is polling-based (pull)
- Both support async agent execution with result persistence

### Access Methods

1. **Voice Control** (Ctrl+Option hotkey on Mac)
2. **Scratchpad** (Daily task list, auto-executes within 3 minutes)
3. **Messaging** (WhatsApp, Slack, Telegram via bot interfaces)
4. **Dashboard Chat** (Web interface)

**AgentForge Alignment:**
- ClaudeClaw Telegram bot is analogous to messaging interface
- Mission CLI is analogous to Scratchpad
- Dashboard would be a future web interface

---

## Key Insights for AgentForge

### 1. **Persistent Memory is Non-Negotiable**
CORE's 88.24% benchmark accuracy shows that temporal knowledge graphs outperform simple conversation logs. AgentForge should:
- Extend hive_mind with temporal tracking (not just latest state)
- Store decision rationale, not just outputs
- Link related missions across time

### 2. **Approval Workflows Prevent Chaos**
CORE uses human-in-loop approval by default:
- Agent proposes action → Audit log created → Human approval → Action executed → Outcome logged
- Escalation paths for high-impact decisions (e.g., financial, security)

**For AgentForge Marvin/CEO Agent:**
- Should generate "approval requests" for high-priority decisions
- Should escalate when confidence is low or impact is high
- Should maintain audit trail of all major decisions

### 3. **Webhook-Driven > Polling-Based**
CORE uses webhooks for event ingestion (apps push to CORE) rather than continuous polling:
- More efficient (no wasted queries)
- Real-time responsiveness
- Lower CPU/bandwidth footprint

**For AgentForge:**
- Current polling every 5 seconds is acceptable for MVP
- Future optimization: Switch to webhook-driven dispatch when mission volume justifies it
- GitHub events → missions (e.g., PR opened → code review agent)
- Slack mentions → missions (e.g., @research question → research agent)

### 4. **Multi-Hop Context Loading**
CORE fetches context from multiple connected apps before delegating:
- "Research this market" → Pull GitHub repos + Slack discussions + Notion docs + recent emails
- Agent sees unified context, not just the raw question

**For AgentForge Research Agent:**
- Should pre-load Obsidian vault knowledge
- Should fetch recent Hive Mind signals related to topic
- Should gather related missions (similar topics) for context

### 5. **Custom Agent Workflows**
CORE allows TypeScript-based custom agents that can:
- Spawn subagents
- Branch on conditions
- Run multi-step processes

**For AgentForge:**
- Agent.js classes should support subagent spawning (e.g., content agent spawning seo-agent for keyword research)
- Conditional routing based on mission type
- This is already partially supported via executeMission() parameters

---

## CORE vs. AgentForge: Comparison

| Aspect | CORE | AgentForge |
|--------|------|-----------|
| **Memory** | Temporal knowledge graph (88.24% benchmark) | Hive Mind (basic cross-session) |
| **Dispatch** | Webhook-driven + polling | Polling-based (5s interval) |
| **Agents** | Claude Code, Codex (external) | Native agents (14 departments) |
| **Approval** | Human-in-loop by default | Escalation on blockers (planned) |
| **Audit Trail** | Explicit logs for all decisions | Hive Mind signals (implicit) |
| **Integration** | 50+ apps via MCP/webhooks | 14 internal agents + mission queue |
| **Access** | Voice, chat, scratchpad, dashboard | Telegram, CLI, dashboard (future) |

---

## Implementation Recommendations for Marvin/CEO Agent

Based on CORE's architecture, the CEO/Marvin agent should:

1. **Maintain Decision Audit Trail**
   - Every strategic decision logged with rationale, timestamp, and outcome
   - Reference other agents' outputs and confidence levels
   - Track reversals and corrections

2. **Implement Escalation Logic**
   - Low confidence → Request human approval
   - High impact (financial/strategy) → Escalate to board
   - Time-sensitive → Auto-decide with post-hoc review

3. **Multi-Source Context Loading**
   - Pull recent mission results from all agents
   - Fetch relevant Hive Mind signals (trends, patterns)
   - Load strategic context from Obsidian (board docs, strategy)

4. **Spawn Subagents for Complex Decisions**
   - Market decision → Trigger research agent
   - Financial → Trigger analytics agent
   - People → Trigger hiring manager agent
   - Wait for results → Synthesize → Decide

5. **Adaptive Workflow Based on Decision Type**
   - Routine (vendor selection) → Quick decision
   - Strategic (pivot direction) → Deep analysis + approval
   - Crisis (security incident) → Immediate + audit

---

## Technical Integration Points

### 1. **Temporal Knowledge Graph Migration**
Current: hive_mind stores latest state
Future: Add temporal dimension (decision timeline)
```sql
ALTER TABLE hive_mind ADD COLUMN (
  temporal_sequence INTEGER,  -- order of decisions in a process
  decision_rationale TEXT,    -- why this decision was made
  confidence_score REAL,      -- how certain is the agent
  reversal_of_id TEXT         -- if this reverses a prior decision
);
```

### 2. **Webhook Integration Points**
For future scalability:
- GitHub webhooks → Code review missions
- Slack mentions → Quick research missions
- Notion updates → Content pipeline triggers
- Email ingestion → Customer feedback synthesis

### 3. **Approval Workflow Schema**
```sql
CREATE TABLE approval_requests (
  id TEXT PRIMARY KEY,
  mission_id TEXT,
  agent_id TEXT,
  decision_type TEXT,  -- 'routine', 'strategic', 'crisis'
  description TEXT,
  proposed_action TEXT,
  impact_level INTEGER,  -- 1-10 scale
  confidence_score REAL,
  status TEXT,  -- 'pending', 'approved', 'rejected'
  approved_by TEXT,
  created_at INTEGER,
  resolved_at INTEGER
);
```

---

## CORE Ecosystem Modules (Relevant for Extensibility)

CORE's open-source structure provides inspiration for AgentForge modularity:
- `skills/` — Reusable automation rules (analogous to agent tools)
- `agents/` — Agent definitions with custom logic (analogous to our agent.js files)
- `connectors/` — App integration modules (analogous to MCP endpoints)
- `memory/` — Knowledge graph implementation (analogous to Hive Mind)

Each is self-contained, testable, and can be extended independently.

---

## Key Statistics & Community

- **GitHub Stars:** Growing community interest in self-hosted AI OS
- **Open Source:** Fully available, self-hostable, no vendor lock-in
- **Model Agnostic:** Works with Claude, OpenAI, local models
- **Deployment:** Docker-based, local setup in minutes

---

## References

- **GitHub:** [RedPlanetHQ/core](https://github.com/RedPlanetHQ/core)
- **Official Website:** https://redplanethq.com
- **Blog Post:** [CORE: Build Your Digital Brain for AI Tools](https://www.blog.brightcoding.dev/2026/03/15/core-build-your-digital-brain-for-ai-tools)
- **Benchmark:** LoCoMo (Temporal Reasoning: 88.24% accuracy)

---

**Completed:** 2026-05-19 18:30 UTC
**Next Action:** Apply temporal reasoning insights to Hive Mind schema + implement approval workflows for CEO agent

