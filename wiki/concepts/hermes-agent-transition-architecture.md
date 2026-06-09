---
title: Hermes Agent Transition Architecture — Board Directive
type: concept
tags: []
created: 2026-06-09
author: marvin
---

# Hermes Agent Transition Architecture

**Source:** Board directive, 2026-06-09
**Status:** Future reference — applies when transitioning departments from OpenClaw to Hermes Agent

---

## Architecture Overview

```
Agency gBrain
  → Orchestrator Hermes Agent
    → Department verticals
      → Specialist agents
        → Scoped sub-agents
```

---

## gBrain — The Company Brain

Ingested data and experience:
- Transcripts
- Chats
- Previous campaigns
- Client learnings
- Strategy docs
- Internal workflows
- Examples of what good looks like

Maintained by a human champion + orchestrator Hermes Agent.

---

## Agent Hierarchy

### Orchestrator (Hermes Agent)
Top-level coordination across all department verticals.

### Department Verticals
Each vertical has its own specialist agents.

### Specialist Agents
Narrow, domain-specific agents. Examples:
- Lifecycle email agent (campaigns, voice rules, approval gates, examples)
- Technical SEO agent (tools, checklists, source standards)
- Content research agent (narrow inputs, clear definition of done)

### Scoped Sub-Agents
Even narrower agents under specialists.

---

## Core Principle: Narrow Scope

> A general "marketing agent" is too vague.
> The narrower the job, the easier it is to improve the agent.

- Narrow scope improves output quality
- Narrow scope reduces drift
- Bad agents don't become good by connecting more tools
- Vague agents just create vague output faster

---

## Harnesses

Multiple harnesses used depending on the job:
- **Hermes Agent** — primary orchestration
- **Codex CLI** — code-heavy work
- **Claude Code** — development work
- **TBD** — bare-bones harness for model routers

---

## Org Chart Tracking

Maintained inside company gBrain:

| Field | Description |
|---|---|
| Top-level orchestrator | Hermes agent structure |
| Department verticals | Which departments exist |
| Specialist agents | Agent registry per department |
| Scoped sub-agents | Nested agent registry |
| Brain access | Which brain each agent reads from |
| Tool access | Which tools each agent is allowed to use |
| Approval requirements | Where human approval is required |

---

## Client Pods (Downstream Isolation)

Client pods are isolated agent companies that can communicate with agency agents when needed.

Each client pod has its own:
- Client gBrain
- Client orchestrator
- Client specialist agents
- Client-specific workflows
- Client-specific approvals
- Client-specific memory

**Rule:** Do NOT let client context bleed across accounts. No agent with every client's data, every tool, and every permission. Scope is what keeps the system useful.

---

## Fork Pattern

Once a vertical agent is built well, fork it (not copy-paste blindly):
- 75% of the agent may be done already
- Customize: context, examples, approvals, voice, tools, workflows
- Not starting from zero

This changes the agency model — one or two strong marketing engineers can run an output surface that used to require a much larger team.

**Caveat:** This only works if agents are actually good. Requires iteration, taste, source material, QA, workflow design, and real marketing experience.

---

## TLDR

1. Turn the agency's knowledge into a brain
2. Turn repeated work into scoped agents
3. Turn each client into an isolated pod
4. Let skilled operators run the system
