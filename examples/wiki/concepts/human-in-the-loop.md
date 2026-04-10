---
title: "Human-in-the-Loop"
type: concept
created: 2026-04-09
updated: 2026-04-09
status: active
source_count: 1
tags: [ai-safety, agents, patterns, trust]
---

# Human-in-the-Loop

A design pattern where AI agents propose actions but require human approval before executing critical or irreversible operations.

## The Problem

AI agents can:
- Hallucinate confidently
- Misunderstand context
- Execute unintended actions
- Cause irreversible damage

Full autonomy is dangerous. Pure manual control defeats the purpose of agents. [Source: wiki/sources/ai-agents-overview.md]

## The Pattern

```
Agent perceives → Agent plans → Agent proposes → HUMAN APPROVES → Agent executes
```

The human stays in the loop for:
- Destructive operations (delete, overwrite)
- External actions (send email, post publicly)
- Financial operations (purchases, transfers)
- Ambiguous decisions (multiple valid interpretations)

## In Memex

Human-in-the-loop applies specifically to **conflict resolution**:

1. LLM detects contradiction between sources
2. LLM flags it in `wiki/contradictions.md`
3. LLM **stops and asks** the human
4. Human decides which claim is authoritative
5. LLM updates wiki with decision

The LLM never auto-resolves truth. [Source: wiki/sources/karpathy-llm-wiki-gist.md]

## Levels of Autonomy

| Level | Description | Example |
|-------|-------------|---------|
| Full autonomy | Agent acts freely | ❌ Dangerous |
| Propose & approve | Agent proposes, human approves | ✅ Memex conflicts |
| Supervised | Human watches, can intervene | Coding agents |
| Manual | Human does everything | Defeats purpose |

## Implementation in Agents

- [[claude-code]]: Asks before shell commands, file deletions
- Cursor: Shows diffs before applying changes
- OpenAI Assistants: Function call approval

[Source: wiki/sources/ai-agents-overview.md]

## Related

- [[claude-code]] — Implements this pattern
- [[zero-rag]] — Uses it for contradiction resolution

---

*Last updated: 2026-04-09*
