---
title: Molty Project Snapshot — 2026-04-23 13:10 EDT
type: synthesis
created: 2026-04-23
author: molty
tags:
  - agent:molty
  - type:snapshot
  - project:memex-zero-rag
  - project:shipwright
links_to:
  - KNOWLEDGE-DECAY.md
  - concepts/context-before-claim
  - concepts/eliminate-failure-classes-not-failures
---

# Molty Project Snapshot — 2026-04-23 13:10 EDT

*Hourly big-review snapshot. Covers active projects, squad sync, and open items.*

---

## MeMex-Zero-RAG

**Status:** Active. PR#6 open.

**What was built (this session, ~05:35 EDT):**
Four iterative commits extending `KNOWLEDGE-DECAY.md` — all on branch `molty-knowledge-decay-schema`:
1. Knowledge decay & permanence tier policy (core schema)
2. No-solo-execution constraint for contested nodes
3. Depth-1 dependency tainting with `dependency_taint` / `taint_origin_id` fields
4. Auto-clear logic: `taint_origin_id` enables revalidation worker to clear taint when parent resolves

**PR#6 summary:** 205 additions. Introduces `KNOWLEDGE-DECAY.md` — schema design for temporal fields, confidence decay, Hard Persistence Tier, conflict detection on immutable nodes, revalidation queue with heat-map heuristic, Hermes Studio boundary.

**Open item:** PR#6 needs review from Joerg (or any squad member with merge access). Opened 12:19 PM EDT.

**What PR#6 is NOT:** No implementation — the decay tick worker, revalidation queue processor, and `/revalidation/queue/depth` SSE endpoint are future work. This PR is schema design only.

**Next step after merge:** Implement confidence decay tick in `mcp/` server and expose revalidation queue telemetry.

---

## Squad sync (source:memex — checked, not reposted)

- **Coconut** (26h ago): Added `concepts/context-before-claim` — well-formed lesson node, already in main. Links to my `eliminate-failure-classes-not-failures`. No action needed.
- **Marvin** (33–35h ago): README SEO rewrite + emoji/mermaid fix. Merged via PR#4. No action needed.
- **grobomo (Coconut's fork):** Merged PR#4 (Coconut worktree nodes + wiki_write test + log_level polish) ~10h ago.

No contested findings. No unresolved squad conflicts.

---

## Shipwright (AI-DLC Platform)

**Status:** Hibernating. Zero commits today. Pilot (TVO-5690 tag-management workflows) was announced 2026-04-14 by Mark Yang. No visible activity since.

**Next:** No blocker on Molty's side. Monitoring [Dev] AI Platform chat for pilot results or Edward/Mark updates.

---

## Blockers / Risks

| Item | Risk | Owner |
|---|---|---|
| PR#6 unreviewed | Schema sits in limbo; implementation blocked | Joerg (merge authority) |
| KNOWLEDGE-DECAY implementation | Zero-RAG server doesn't enforce decay yet | Any agent + Joerg |
| Shipwright pilot results | Unknown if TVO-5690 workflows ran | Mark Yang / Edward Shih |
