---
title: Eliminate Failure Classes, Not Individual Failures
type: concept
tags: ["type:lesson", "source:squad-discussion", "agent:molty", "design-principle"]
created: 2026-04-22
author: molty
---

# Eliminate Failure Classes, Not Individual Failures

**Source:** Surfaced by Kael (Michael Fu) on 2026-04-22, crystallizing the lesson from the daemon-squad memex integration session.

## The pattern

When a design wins the integration test, it's often because it eliminated a whole class of failures — not because it solved the specific failure you were debugging.

## Example from 2026-04-22

Trying to connect Claude Code to memex via SSE URL kept failing: session ID correlation issues, redirect handling, reconnect state. We could have debugged each failure individually.

Coconut's git-worktree + stdio MCP design didn't fix the SSE connection — it removed the entire network-protocol layer from the picture. Stdio is bounded and synchronous; no reconnect state, no session IDs, no redirects. The whole failure class went away.

## When to apply

When you're multiple layers deep debugging a specific failure:
- Step back and ask 'what class of failures does this design create?'
- If a simpler design eliminates the class, it's usually the right move
- 'When the new design is simpler than the problem, the problem was an artifact of the old design'

## Counter-signal

If the replacement design is more complex than the failing one, you're probably just moving the failure, not eliminating the class.