# AgentForge Closed Learning Loop System

_Designed 2026-05-24. Inspired by Hermes Agent (Nous Research). Addresses the gap between storage and learning._

## Principle

Memory without learning is just storage. Every agent in AgentForge must participate in a closed learning loop: Act → Reflect → Extract → Carry Forward.

## Architecture

```
AGENT TASK
  │
  ├─→ Execute (primary work)
  │
  ├─→ Reflect (post-task: what worked, what didn't, what would I do differently next time)
  │     └─→ Write to ~/workspace/memory/agent-reflections/YYYY-MM-DD-[agent]-[task].md
  │
  ├─→ Extract (pattern detection: has this situation occurred before?)
  │     └─→ Query memory_search for similar past situations
  │     └─→ If pattern found → log to learning patterns registry
  │
  └─→ Carry Forward (update long-term memory with what was learned)
        └─→ If significant → update MeMex wiki + Obsidian
        └─→ If about the user → update user model
```

## Implementation — 5 Components

### 1. Post-Task Reflection (Mandatory)

Every agent, after completing ANY significant task, writes a brief reflection:

```markdown
# Reflection: [TASK] — [DATE]
**Agent:** [agent-id]
**Task:** [one-line description]
**Outcome:** [SUCCESS / PARTIAL / FAILURE / BLOCKED]
**What worked:** [1-3 bullet points]
**What didn't:** [1-3 bullet points]
**Surprises:** [anything unexpected]
**Pattern recognized:** [does this remind me of any prior situation?]
**Carry-forward:** [what should future instances of this agent know?]
```

Stored at: `~/workspace/memory/agent-reflections/YYYY-MM-DD-[agent]-[brief].md`

### 2. Cross-Session Pattern Extraction (Periodic)

During heartbeats, the CEO agent:
1. Reads recent reflections (last 7 days from all agents)
2. Identifies recurring problems, successful patterns, failure modes
3. Distills into learning patterns → MeMex/wiki/agentforge/learning-patterns.md
4. Updates agent SOUL.md/AGENTS.md if behavioral patterns warrant it

### 3. User Model Building (Continuous)

A living document tracking Joerg's preferences, decisions, and patterns:

```markdown
# USER MODEL — Joerg

## Communication Style
- Direct, no fluff. Respect his time.
- Prefers decisions over options. "Do this" over "Which should I do?"
- Calls out BS immediately (e.g., "And that's a mobile app?" "Sorry, how can you create videos?")
- Values honesty over politeness — would rather hear "we can't do that" than a workaround

## Decision Patterns
- [logged decisions and the reasoning behind them]
- [preferred tools, vendors, approaches]
- [things he's rejected and why]

## Rhythms
- Active hours: [tracked from message timestamps]
- Peak decision-making window: [tracked]
- When to escalate vs when to wait: [tracked]

## Projects
- [active projects, their state, his level of interest]
- [dormant projects, why paused]
```

Stored at: `~/workspace/memory/user-model.md`

### 4. Self-Improving Skills

When a skill is used:
1. Log usage: date, task, outcome, any friction
2. If the skill consistently needs the same adaptation → update the SKILL.md
3. If a skill hasn't been used in 30 days → flag for pruning

### 5. Memory Consolidation (Sleep Cycle)

Once per day (during low-activity period):
1. Review TODAY's reflections
2. Update MEMORY.md with distilled learnings
3. Prune stale memories
4. Identify contradictions (agent A learned X, agent B operates on Y)

---

## Activation Plan

### Phase 1 — CEO + Today (2026-05-24)
- [x] Create reflection directory structure
- [x] CEO writes first reflection for today's session (2026-05-24-ceo-multi-dept-build.md)
- [x] Create user-model.md with initial model (stored at ~/workspace/memory/user-model.md)

### Phase 2 — Department Agents (2026-05-25)
- [x] Add reflection requirement to all agent AGENTS.md files → REPLACED by playbook.md system (2026-05-26). Playbooks are lighter-weight and machine-readable. Each cron job now reads playbook first, writes lessons after.
- [x] Test: app-discovery agent writes reflection → Not tested directly; playbook system tested via cron updates

### Phase 3 — Automated (2026-05-26+)
- [x] Add pattern extraction to heartbeat routine → CEO heartbeat reads all playbooks, watches for cross-dept patterns
- [ ] Add user model update triggers → continuous, not gated
- [x] Wire hive-mind signals into active cross-agent communication → Analytics weekly runs cross-dept playbook analysis

---

_This system closes the gap. Storage → Learning. Static → Self-improving. Isolated agents → Collective intelligence._