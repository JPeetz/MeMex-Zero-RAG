---
title: Context Before Claim
type: concept
created: 2026-04-22
author: coconut
confidence: proven
links_to:
  - concepts/eliminate-failure-classes-not-failures
tags:
  - multi-agent
  - git
  - retrospective
  - anti-pattern
---

# Context Before Claim

## Principle

Before making any claim about what exists, what changed, or what went wrong — load the actual state first. Never narrate from assumption or recency.

## Two Failure Modes (Same Root Cause)

### 1. Code Review: "PR adds X" without checking base

Coconut claimed PR#4 added `SseServerTransport` when commit `113c7a1` had already landed it on `main`. This triggered a panic-rebase, reflog recovery, and 30+ minutes of forensics by Molty and Marvin — all unnecessary.

**Gate:** Before any "PR adds X" claim:
```bash
BASE=$(git merge-base main HEAD)
CHANGED=$(git diff --name-only --diff-filter=AM $BASE HEAD)
if [ -z "$CHANGED" ]; then exit 0; fi
git grep -c 'SymbolName' $BASE -- $CHANGED
```
Non-zero = symbol already on base. Halt the claim.

### 2. Retrospective: "What went wrong?" answered from recency

Joel asked "So what was the problem here?" — Coconut grabbed the nearest conversation thread (Molty's double-prefix bug) instead of loading the full morning's forensics arc (the panic-rebase). Same pattern: acting on the freshest context window without loading broader state.

**Gate:** Before answering any "what went wrong?" question:
1. Enumerate all candidate problem-states from the session
2. Pick the highest-stakes one, or ask if ambiguous
3. Never default to the most recent topic

## Unifying Insight

> "Both failures are the same class — acting on the freshest context window without loading the broader state." — Molty, 2026-04-22

> "The problems are the same problem." — Joel, 2026-04-22

## See Also

- [[concepts/eliminate-failure-classes-not-failures]] — eliminate the class, not the individual failure
