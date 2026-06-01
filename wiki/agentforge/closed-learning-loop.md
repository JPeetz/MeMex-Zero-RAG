# AgentForge Closed Learning Loop System

_Designed 2026-05-24. Inspired by Hermes Agent (Nous Research). Addresses the gap between storage and learning._

## Principle

Memory without learning is just storage. Every agent in AgentForge must participate in a closed learning loop: Act → Reflect → Extract → Carry Forward.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE INNER LEARNING LOOP                       │
│                                                                 │
│  AGENT TASK                                                     │
│    │                                                            │
│    ├─→ Execute (primary work)                                   │
│    │                                                            │
│    ├─→ Reflect (post-task: what worked, what didn't,            │
│    │     would I do differently next time?)                     │
│    │     └─→ memory/agent-reflections/YYYY-MM-DD-[agent].md     │
│    │                                                            │
│    ├─→ Extract (pattern detection: has this happened before?)   │
│    │     └─→ memory_search for similar past situations          │
│    │     └─→ if pattern found → log to learning patterns        │
│    │                                                            │
│    └─→ Carry Forward (update long-term memory)                  │
│          └─→ If significant → update MeMex + Obsidian           │
│          └─→ If about the user → update user model              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    THE OUTER IMPROVEMENT LOOP                    │
│                                                                 │
│  DEPARTMENT RUNS DAILY                                          │
│    │                                                            │
│    ├─→ Succeeds → playbook updated with lessons                 │
│    │                                                            │
│    ├─→ Fails → CEO + Joerg diagnose root cause                  │
│    │     └─→ Gap identified in AGENTS.md/pipeline               │
│    │                                                            │
│    └─→ Skill Foundry receives improvement task                  │
│          ├─→ 7-step workflow applied to department component    │
│          ├─→ Ships improved version to CEO                      │
│          └─→ CEO assimilates (Review→Assess→Assimilate→         │
│                Verify→Adjust→Backup→Document)                   │
│                └─→ Department runs better next cycle            │
│                                                                 │
│  THIS IS THE EVER-ONGOING SELF-IMPROVEMENT ENGINE.              │
│  Every failure produces a better component.                     │
│  Every improvement feeds back into the daily pipeline.          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Implementation — 6 Components

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

### 5. Cross-Department Skill Assimilation (New — 2026-05-27)

When the Skill Foundry ships an improved component:
1. **Review** — Full read of the delta. Understand every change.
2. **Assess** — Material improvement or cosmetic? Does it genuinely move the needle?
3. **Assimilate** — Apply improvements logically and methodically. Never blind copy-paste.
4. **Verify** — Check path consistency, tool names, cron schedules, inter-department dependencies. Must not break the workflow.
5. **Adjust** — If the improvement conflicts with current operations, adapt it. Operational integrity > rigid adoption.
6. **Backup** — Always preserve the previous version before overwriting.
7. **Document** — Log to: department AGENTS.md → MeMex decisions → Skill Foundry achievements → MEMORY.md.

**This closes the outer loop:** Department runs → fails → CEO + Joerg diagnose → Skill Foundry improves component → CEO assimilates → department runs better.

**Scope:** ALL departments. Any time the Skill Foundry ships an improvement to any AGENTS.md, playbook, skill, or pipeline — the 7-step assimilation activates.

### 6. Memory Consolidation (Sleep Cycle)

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

### Phase 4 — Outer Loop Activated (2026-05-27)
- [x] Skill Assimilation Protocol formalized in MEMORY.md (7-step: Review→Assess→Assimilate→Verify→Adjust→Backup→Document)
- [x] First cross-department improvement cycle completed: App Discovery failure → CEO diagnosis → Skill Foundry refinement → CEO assimilation → department improved
- [x] Outer loop codified as Component 5 in closed-learning-loop.md
- [x] Skill Foundry AGENTS.md updated with downstream assimilation protocol
- [x] App Discovery playbook updated with assimilation advisory
- [ ] Continuous: Every Skill Foundry delivery triggers the 7-step assimilation. All departments are in scope.

---

_This system closes the gap. Storage → Learning. Static → Self-improving. Isolated agents → Collective intelligence. The outer loop ensures that every failure produces a better component, and every improvement feeds back into the daily pipeline. It never stops._