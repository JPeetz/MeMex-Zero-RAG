# Prime Directive: Failure Auto-Resolution

**Board Directive** | 2026-07-15 | Status: Active

## The Directive

"Whatever fails in the future, research in the memory and try to find a previous fix, if none can be found, analyze the issue and automatically resolve the issue, then finish the task at hand successfully."

## Protocol

1. **Research memory** — MEMORY.md, MeMex (wiki_search), Obsidian (brain/Gotchas.md, brain/Patterns.md), daily notes
2. **Previous fix exists** → apply immediately
3. **No previous fix** → analyze, trace root cause, implement fix
4. **Finish successfully** — failure is not terminal

## Scope

All automated processes: cron jobs, pipelines, scripts, API calls, tool calls, image generation.

## Related Directives

- [[marketing-image-review-protocol]] — present images to Board, brand audit is advisory
- [[memory-architecture]] — sync decisions across all surfaces

## Exception

3 consecutive failures → escalate to Board.