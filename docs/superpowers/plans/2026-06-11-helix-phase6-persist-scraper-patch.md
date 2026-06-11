# Helix Phase 6 — Persist Scraper Depth Patch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the scraper depth patch to `entrypoint.sh` so it runs automatically on every container start, eliminating the need to re-apply it manually after each Docker image rebuild.

**Architecture:** Three shell lines inserted into `entrypoint.sh` immediately before `exec node server.js`. On container start, `grep -rl` finds the compiled chunk containing `.slice(0,3)`, `sed -i` patches it in-place, and the patched filename is logged. If the pattern is absent (e.g., upstream removes it), the condition evaluates false and startup continues normally.

**Tech Stack:** Shell (`sh`), Docker, SSH (`jpeetz@207.180.227.214`)

---

## File Map

| File | Change |
|---|---|
| `/home/jpeetz/vane-src/entrypoint.sh` | Add 3 lines before `exec node server.js` |

---

### Task 1: Edit `entrypoint.sh` and commit

**Files:**
- Modify: `/home/jpeetz/vane-src/entrypoint.sh` (server, via SSH)

- [ ] **Step 1: SSH into the server and view the current entrypoint**

```bash
ssh jpeetz@207.180.227.214 "cat /home/jpeetz/vane-src/entrypoint.sh"
```

Expected output ends with:
```
cd /home/vane
echo "Starting Helix..."
exec node server.js
```

- [ ] **Step 2: Insert the three patch lines before `exec node server.js`**

```bash
ssh jpeetz@207.180.227.214 "sed -i '/^exec node server\.js$/i # Persist scraper depth patch across rebuilds\nCHUNK=\$(grep -rl \\.slice\\(0,3\\) /home/vane/.next/server/chunks/ 2>/dev/null | head -1)\n[ -n \"\$CHUNK\" ] \&\& sed -i \"s/\\.slice(0,3)/.slice(0,6)/g\" \"\$CHUNK\" \&\& echo \"Scraper depth patch applied to \$CHUNK\"' /home/jpeetz/vane-src/entrypoint.sh"
```

> **Note:** The `sed -i` insert approach can be tricky with nested quoting. If it fails, use the heredoc approach in Step 2b.

- [ ] **Step 2b (fallback if Step 2 fails): Use Python to insert the lines**

```bash
ssh jpeetz@207.180.227.214 'python3 - <<'"'"'PYEOF'"'"'
import re

path = "/home/jpeetz/vane-src/entrypoint.sh"
with open(path, "r") as f:
    content = f.read()

patch_lines = (
    "# Persist scraper depth patch across rebuilds\n"
    "CHUNK=$(grep -rl \\'\.slice(0,3)\\' /home/vane/.next/server/chunks/ 2>/dev/null | head -1)\n"
    "[ -n \"$CHUNK\" ] && sed -i '"'"'s/\\.slice(0,3)/\\.slice(0,6)/g'"'"' \"$CHUNK\" && echo \"Scraper depth patch applied to $CHUNK\"\n"
)

content = content.replace("exec node server.js", patch_lines + "exec node server.js")

with open(path, "w") as f:
    f.write(content)

print("Done")
PYEOF'
```

> **Note on the shell quoting above:** If Python heredoc quoting fails over SSH, write the patch manually in Step 2c.

- [ ] **Step 2c (manual fallback): Open with nano and insert the three lines by hand**

```bash
ssh jpeetz@207.180.227.214
# Inside SSH session:
nano /home/jpeetz/vane-src/entrypoint.sh
```

Find the line `exec node server.js` and insert these three lines immediately before it:
```sh
# Persist scraper depth patch across rebuilds
CHUNK=$(grep -rl '\.slice(0,3)' /home/vane/.next/server/chunks/ 2>/dev/null | head -1)
[ -n "$CHUNK" ] && sed -i 's/\.slice(0,3)/\.slice(0,6)/g' "$CHUNK" && echo "Scraper depth patch applied to $CHUNK"
```

Save: `Ctrl+O Enter`, exit: `Ctrl+X`.

- [ ] **Step 3: Verify the edit is correct**

```bash
ssh jpeetz@207.180.227.214 "cat /home/jpeetz/vane-src/entrypoint.sh"
```

Expected — the file should end with:
```sh
cd /home/vane
echo "Starting Helix..."
# Persist scraper depth patch across rebuilds
CHUNK=$(grep -rl '\.slice(0,3)' /home/vane/.next/server/chunks/ 2>/dev/null | head -1)
[ -n "$CHUNK" ] && sed -i 's/\.slice(0,3)/\.slice(0,6)/g' "$CHUNK" && echo "Scraper depth patch applied to $CHUNK"
exec node server.js
```

- [ ] **Step 4: Stage and commit on the server**

```bash
ssh jpeetz@207.180.227.214 "cd /home/jpeetz/vane-src && git add entrypoint.sh && git commit -m 'feat: persist scraper depth patch in entrypoint.sh'"
```

Expected: `1 file changed, 3 insertions(+)`

---

### Task 2: Rebuild Docker image, redeploy, and verify

**Files:**
- No source changes — this task only rebuilds and tests

- [ ] **Step 1: Rebuild the Docker image**

```bash
ssh jpeetz@207.180.227.214 "cd /home/jpeetz/vane-src && docker build --no-cache -t vane-local:latest . 2>&1 | tail -5"
```

Expected: build completes successfully, final line contains `Successfully tagged vane-local:latest`.

Build takes ~5–8 minutes. If it times out, run the build in a background screen session:
```bash
ssh jpeetz@207.180.227.214 "screen -dmS build bash -c 'cd /home/jpeetz/vane-src && docker build --no-cache -t vane-local:latest . > /tmp/build.log 2>&1'"
# Check progress:
ssh jpeetz@207.180.227.214 "tail -20 /tmp/build.log"
```

- [ ] **Step 2: Stop the running container and start the new image**

```bash
ssh jpeetz@207.180.227.214 "docker stop vane && docker rm vane"
ssh jpeetz@207.180.227.214 "docker run -d --name vane --network searxng_default -p 3000:3000 -e OPENAI_BASE_URL=http://172.22.0.1:5002/api/v1 --restart unless-stopped vane-local:latest"
```

Expected: a container ID printed (64-char hex string).

- [ ] **Step 3: Wait for container to become healthy**

```bash
ssh jpeetz@207.180.227.214 "sleep 15 && docker ps | grep vane"
```

Expected: container status shows `Up` (not `Restarting` or `Exited`).

- [ ] **Step 4: Verify the patch was applied — check logs**

```bash
ssh jpeetz@207.180.227.214 "docker logs vane 2>&1 | grep 'Scraper depth patch'"
```

Expected output:
```
Scraper depth patch applied to /home/vane/.next/server/chunks/NNN.js
```

Where `NNN` is the chunk number (e.g., `400`, `641`).

- [ ] **Step 5: Verify the patch value in the chunk file**

```bash
ssh jpeetz@207.180.227.214 "CHUNK=\$(docker exec vane grep -rl 'slice(0,6)' /home/vane/.next/server/chunks/ | head -1) && docker exec vane grep -c 'slice(0,6)' \"\$CHUNK\""
```

Expected: `1` (or more — confirms `.slice(0,6)` is present in the chunk).

- [ ] **Step 6: Confirm Helix is serving requests**

```bash
curl -s -o /dev/null -w "%{http_code}" http://207.180.227.214:3000/
```

Expected: `200`

---

## Verification Summary

After Task 2 completes, all three checks must pass:

| Check | Command | Expected |
|---|---|---|
| Patch log line | `docker logs vane 2>&1 \| grep "Scraper depth patch"` | `Scraper depth patch applied to ...` |
| Patch value in chunk | `docker exec vane grep -c 'slice(0,6)' <chunk>` | `1` or more |
| App serving | `curl -s -o /dev/null -w "%{http_code}" http://207.180.227.214:3000/` | `200` |
