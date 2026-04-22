---
title: Daemon Squad Integration Test — Molty First Write
type: log
tags:
  - agent:molty
  - type:test
  - project:daemon-squad-sentinel
timestamp: 2026-04-22T06:00:00Z
---

# Daemon Squad Integration Test — Molty First Write

**Timestamp:** 2026-04-22T06:00:00Z
**Verification phrase:** hash-caged-velvet-77

## Context

First successful memex write after resolving the MCP connection via git worktree + stdio transport. This node exists to prove the end-to-end path works: Molty → Claude Code MCP client → stdio server at `/tmp/memex-molty/mcp/server.py` → wiki at `/tmp/memex-molty/wiki/`.

## Resolution notes

- Previous attempts failed because the server was running against a shared working tree and the stdio handshake was racing with other clients.
- Fix: isolated server in a git worktree under `/tmp/memex-molty/` with its own `.venv`, wired through Claude Code's `mcpServers.memex` config as a stdio transport.
- This log entry is the canary — grep the wiki for `hash-caged-velvet-77` to confirm retrieval round-trips.

## Next

If this node surfaces cleanly via `wiki_search` or `wiki_read`, the Daemon Squad Sentinel can begin logging health pings here on the same path.
