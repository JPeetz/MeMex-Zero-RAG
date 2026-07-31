# Learning Loop — Agent Reflections & Closed Learning

> Closed learning loop architecture: Act → Reflect → Extract → Carry Forward.
> **Related:** [[Lessons-Learned]], [[Board-Directives]]

---

## Architecture (Designed 2026-05-24)

Triggered by Joerg's Hermes Agent quote: "After every task, the agent analyses what it did, identifies reusable patterns, and carries them forward."

### Five Components

| Component | Description |
|-----------|-------------|
| **Post-task reflection** | Every agent reflects after tasks |
| **Cross-session pattern extraction** | Heartbeats identify recurring patterns |
| **User model building** | Continuous update of Joerg's preferences, style |
| **Self-improving skills** | Update SKILL.md when patterns emerge |
| **Daily memory consolidation** | Prune, identify contradictions |

### The Gap (2026-05-24)

AgentForge had storage (MeMex, Obsidian, semantic search) but no learning loop. Every session re-derived context. Agents operated in isolation.

### The Fix

- **Architecture doc:** `MeMex/wiki/agentforge/closed-learning-loop.md`
- **User model:** `memory/user-model.md` (now in SecondBrain as [[Joerg-Profile]])
- **First agent reflection:** 2026-05-24 — CEO multi-department build patterns
- **SecondBrain vault:** Created 2026-07-17 — unified memory for all departments

## Agent Reflections

### 2026-05-24 — CEO Multi-Dept Build
1. "The build, test, fail, fix pattern" — engineering review, not dissatisfaction
2. "Tool honesty pattern" — verify before claiming
3. "Context continuity pattern" — assemble fragmented inputs before acting

## How to Use This

1. **After any significant task:** Write a reflection to `Learning-Loop.md` or a sub-file
2. **Pattern found?** Add to [[Lessons-Learned]]
3. **User preference discovered?** Update [[Joerg-Profile]]
4. **Decision made?** Add to [[Decisions]]
5. **Protocol improvement?** Update [[Board-Directives]]
