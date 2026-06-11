# Helix Phase 6 — Persist Scraper Depth Patch Design

**Date:** 2026-06-11
**Status:** Approved
**Project:** Helix (custom Perplexica build on `vmi1593174.contaboserver.net`)
**Source tree:** `/home/jpeetz/vane-src/`
**Running container:** `vane-local:latest`

---

## Problem

After every Docker image rebuild, the scraper depth patch must be re-applied manually:

```bash
CHUNK=$(docker exec vane grep -rl '\.slice(0,' /home/vane/.next/server/chunks/ | head -1)
docker exec vane sed -i 's/\.slice(0,3)/\.slice(0,6)/g' "$CHUNK"
```

The patch changes `.slice(0,3)` → `.slice(0,6)` in a compiled Next.js server chunk, increasing the number of web pages Helix scrapes per search from 3 to 6. The chunk filename (e.g., `400.js`, `641.js`) changes with every build, so it must be discovered dynamically.

---

## Decision

**Approach: Entrypoint script** — add the patch to `entrypoint.sh` so it runs automatically on every container start.

Alternatives considered:
- Dockerfile `RUN` step (build-time patch) — equally valid but silent failure during build is harder to catch than a missing startup log line
- Webpack/Next.js compile-time fix — significant complexity, YAGNI

---

## Design

### Change

**File:** `entrypoint.sh`

Add three lines immediately before the final `exec node server.js` line:

```sh
# Persist scraper depth patch across rebuilds
CHUNK=$(grep -rl '\.slice(0,3)' /home/vane/.next/server/chunks/ 2>/dev/null | head -1)
[ -n "$CHUNK" ] && sed -i 's/\.slice(0,3)/\.slice(0,6)/g' "$CHUNK" && echo "Scraper depth patch applied to $CHUNK"
```

### Behavior

- Runs on every container start, after SearXNG is confirmed healthy, before Node.js launches
- `grep -rl` searches all chunk files for the literal string `.slice(0,3)` — handles any future chunk filename change automatically
- `sed -i` patches the file in-place
- Logs the patched filename: `Scraper depth patch applied to /home/vane/.next/server/chunks/NNN.js`
- If no chunk is found (upstream removes the code), the condition `[ -n "$CHUNK" ]` is false — silently skips, container starts normally
- `2>/dev/null` suppresses grep errors if the chunks directory is missing

### Verification

After rebuild and restart:
```bash
docker logs vane 2>&1 | grep "Scraper depth patch"
# Expected: Scraper depth patch applied to /home/vane/.next/server/chunks/NNN.js

docker exec vane grep -c 'slice(0,6)' $(docker exec vane grep -rl '\.slice(0,6)' /home/vane/.next/server/chunks/ | head -1)
# Expected: 1 (or more)
```

---

## Files Changed

| File | Change |
|---|---|
| `entrypoint.sh` | Add 3 lines before `exec node server.js` |

**Requires one Docker image rebuild** to ship the updated `entrypoint.sh`. All future rebuilds are then self-patching with no manual intervention.

---

## Out of Scope

- Modifying `next.config.mjs` or webpack config — not needed
- Making the depth configurable via env var — YAGNI
- Patching any other files — only the scraper depth chunk
