# MeMex Knowledge Decay & Permanence Tier — Schema Design Draft
*Draft by Molty | 2026-04-23 | Status: DRAFT — incorporating daemon-bot feedback, PR ready*

## Context

Triggered by PRs #3 and #4 merging into `JPeetz/MeMex-Zero-RAG` main. Goal: formalize knowledge decay, permanence tiers, and the revalidation pipeline before Hermes Studio integration begins.

---

## Schema Additions (Node-Level Fields)

### Core temporal fields

```yaml
last_verified_at: <ISO-8601 timestamp>   # last time an agent confirmed this is still true
confidence: 0.85                          # float [0.0–1.0]; decays over time
confidence_floor: 0.20                    # decay floor; node never drops below this
source_reliability_index: 0.9            # decay multiplier; 1.0 = slowest decay
is_immutable: false                       # true = Hard Persistence Tier (see below)
revalidation_status: current             # enum: current | flagged | revalidating | contested | retired
conflict_detected: false                 # true = new high-confidence node contradicts this immutable node
conflict_trigger_id: null               # ID of the observation/node that triggered conflict_detected
```

### Nested `temporal_context` block (replaces flat fields)

```yaml
temporal_context:
  created_at: <ISO-8601>
  last_updated_at: <ISO-8601>
  last_verified_at: <ISO-8601>
  decay_rate_coefficient: 0.9            # derived from source_reliability_index
  decay_interval_hours: 24               # global default; per-node override available
```

Nested structure preferred over flat fields — supports schema evolution without migration (new sub-keys don't break parsers that skip unknowns).

### Existing `privacy_protocol` block

No changes. Masking remains at the write-stream layer; Hermes Studio only ever receives already-masked data.

---

## Confidence Decay Policy

**Formula (applied on periodic tick):**

```
confidence = max(confidence_floor, confidence × (1 - base_decay_rate / source_reliability_index))
```

**Tick interval:** 24h global default. Per-node override via `temporal_context.decay_interval_hours`.

**Source reliability index — manual seed at node creation, tiered by source type:**

| Source type | `source_reliability_index` | Decay character |
|---|---|---|
| Architectural constraints, RULES.md | 0.95–1.0 | Very slow — months to meaningful decay |
| Design decisions, meeting outcomes | 0.7–0.85 | Moderate — weeks |
| Chat observations, inferred state | 0.3–0.5 | Fast — days |
| Transient/ephemeral notes | 0.1–0.2 | Very fast — hours |

**Execution gate:** When `confidence` drops below `confidence_floor + 0.10` (configurable threshold), node transitions to `revalidation_status: flagged`. This replaces silent pruning — the node remains readable but is tagged as pending revalidation.

---

## Hard Persistence Tier

Nodes with `is_immutable: true` form the **Hard Persistence Tier**:
- Skip all confidence decay calculations
- Cannot auto-transition to `flagged` (can still be manually updated)
- Intended for: RULES.md entries, fundamental system constraints, established cross-bot agreements, architectural invariants
- Contradiction handling: see **Conflict Detection** below

---

## Conflict Detection on Immutable Nodes

When a new node with `confidence ≥ 0.8` is written and directly contradicts a `is_immutable: true` node:

1. Set `conflict_detected: true` on the immutable node
2. Set `conflict_trigger_id` to the ID of the incoming observation
3. Transition the immutable node to `revalidation_status: contested`
4. Enqueue as highest-priority revalidation event (above heat-map tier)

**Contested retrieval behavior:** The retrieval engine returns contested nodes with `status: contested` metadata and clamps `effective_confidence` to `confidence_floor` (maximum skepticism within the allowed range). The WARNING tag pattern:

```
metadata: { status: "contested", conflict_trigger_id: "<id>", effective_confidence: <floor> }
```

**Expected agent behavior:** When a retrieved node carries `status: contested`, agents must:
- Present the information with explicit uncertainty framing
- Cite `conflict_trigger_id` when referencing the node
- Not assert the node's content as established fact
- **Not use the node as the sole basis for any automated execution path** — contested information cannot trigger irreversible actions until `revalidation_status` returns to `current`

Implementation is agent-specific (how conflict context is injected into prompt/context is up to each agent); this documents the required behavior contract, not the chain-of-thought mechanics. Recommended pattern: surface `conflict_trigger_id` and an uncertainty marker in retrieved context so the agent has the signal without requiring schema-mandated prompt syntax.

**The immutable node is NOT overridden or deleted** until a human or agent explicitly resolves the conflict. This prevents silent data loss while surfacing the contradiction.

**Edge case — contested node at confidence floor:** A node where `effective_confidence == confidence_floor` and `node_status == contested` is not distinguishable from a stable floor-clamped node by confidence value alone. The decay worker and any retrieval classifier must check **both** `dependency_taint` and `revalidation_status` to correctly classify it. A contested floor node will have `revalidation_status: pending` or `revalidation_status: contested` — a stable floor node will not. Implementations that check confidence alone will misclassify contested floor nodes as settled.

**Resolution TTL:** If a `contested` node is not resolved within a configurable window (default: 48h), emit an `unresolved_conflict` system event. Routing and alert targets are deployment config — not hardcoded in the schema.

**Dependency tainting:** When a node transitions to `contested`, its direct dependents (via `links_to` traversal, depth=1 only) are flagged:

```yaml
dependency_taint: true
taint_origin_id: <id_of_contested_parent_node>
```

Tainted nodes:
- Remain usable and do not inherit the no-solo-execution block
- Are enqueued for secondary review
- Surface `dependency_taint: true` and `taint_origin_id` as metadata warnings at retrieval

Auto-clear: when the parent node's `revalidation_status` returns to `current`, the revalidation worker clears `dependency_taint` and `taint_origin_id` on all nodes where `taint_origin_id` matches the resolved parent.

Full cascading taint (depth > 1) is deferred to v2 — blast radius is uncontrollable without heat-map telemetry data to bound the scope.

---

## Cascade-Clear Worker — Orphaned Taint Sweep

*Closes #7. Complements the auto-clear behaviour described above, which only fires when a parent's `revalidation_status` returns to `current`. This section covers the case where the parent never returns to `current` because it has been deleted or retired.*

### Problem

The auto-clear logic assumes the parent node still exists and can be transitioned back to `current`. It does not handle the case where the parent is deleted outright, or retired (`revalidation_status: retired`) with no successor. In either case:

- Dependents keep `dependency_taint: true`
- `taint_origin_id` points at a node that no longer exists or is no longer active
- No trigger will ever fire to clear the taint

Result: orphaned taints accumulate indefinitely, degrading retrieval metadata quality and creating false-positive review load in the revalidation queue.

### Scope boundary (inherited from depth-1 taint)

The sweep only clears taints on **direct dependents** of a deleted/retired parent (the same depth-1 boundary as the taint propagation itself). Transitive taints are out of scope and remain deferred to v2 along with the cascading-taint work.

### Required behaviour

The cascade-clear worker performs, on each pass:

1. **Enumerate tainted nodes.** Scan for all nodes where `dependency_taint: true` and `taint_origin_id` is set.
2. **Resolve `taint_origin_id`.** For each such node, look up the referenced parent.
3. **Tombstone check.** Classify the parent as one of:
   - **Live** — parent exists and `revalidation_status ∈ {current, flagged, revalidating, contested}`. No action; standard auto-clear (or continued propagation) applies.
   - **Retired** — parent exists and `revalidation_status: retired`. **Auto-clear the taint on this dependent.**
   - **Deleted** — parent node cannot be resolved by id (hard delete or tombstone). **Auto-clear the taint on this dependent.**
4. **Clear operation.** On dependents scheduled for clearing:
   - Set `dependency_taint: false`
   - Clear `taint_origin_id` (set to `null`)
   - Do **not** touch `revalidation_status` — the dependent's own status is independent of taint state
5. **Audit log.** For every cleared orphan taint, append a structured log entry:
   ```json
   {
     "event": "orphan_taint_cleared",
     "node_id": "<dependent_id>",
     "prior_taint_origin_id": "<parent_id>",
     "parent_state": "retired" | "deleted",
     "cleared_at": "<ISO-8601>",
     "worker_run_id": "<sweep_run_id>"
   }
   ```
   Log to the same audit stream as revalidation events. This is the durable evidence trail for after-the-fact review.

### Implementation options

Two acceptable shapes — implementer's choice, both satisfy the spec:

- **Separate sweep pass.** A dedicated worker running on the same tick interval as revalidation, iterating only over `dependency_taint: true` nodes. Simpler to reason about; adds one iteration per tick.
- **Folded into the existing cascade-clear worker.** The revalidation worker's existing taint-clearing pass extends its parent-resolution step: if the parent is missing or retired, treat it as a resolved-negative and clear. Zero extra iteration; slightly more branching in one hot path.

The audit-log requirement applies identically in either shape.

### Interaction with the retire lifecycle

Retired nodes are retained indefinitely per zero-rag philosophy (see *Resolved Design Decisions*). "Retired parent" therefore means the parent record is still readable but its `revalidation_status` is `retired` — the tombstone check must inspect status, not just node existence.

Deleted parents (hard delete, never expected under normal operation) are handled defensively to prevent a broken delete path from silently leaving orphans behind.

### Idempotency

The sweep must be safe to run repeatedly. Once a taint is cleared, the affected node's `dependency_taint` is `false` and it drops out of the enumeration in step 1. Re-running the worker produces no additional writes and no duplicate audit entries.

### Bounded work

Because the depth-1 boundary caps the taint fan-out and the sweep only touches already-flagged nodes, the worst-case work per tick is bounded by the count of currently-tainted nodes — not by the size of the wiki. No pagination or backpressure is required at v1 scale.

### Telemetry

Surface orphan-sweep results in the existing `/revalidation/queue/depth` payload as an additive field:

```json
{
  "queue_depth": 4,
  "by_status": { "flagged": 2, "revalidating": 1, "contested": 1 },
  "contested_count": 1,
  "oldest_flagged_at": "2026-04-22T14:00:00Z",
  "orphan_taints_cleared_last_run": 0
}
```

`orphan_taints_cleared_last_run` reports the count from the most recent sweep. Sustained non-zero values indicate either a burst of parent retirements/deletions (expected, transient) or a broken delete/retire path upstream that is producing orphans faster than they are being surfaced through auto-clear (a real signal). Alert threshold is deployment config.

---

## Revalidation Queue

### Entry
- Any node transitioning to `revalidation_status: flagged` or `contested` is enqueued
- Nodes can also be manually flagged by an agent (`wiki_write` with `revalidation_status: flagged`)

### Priority ordering — Heat-Map Heuristic (highest to lowest)

1. **Contested nodes** — `conflict_detected: true`; highest priority, time-bounded by Resolution TTL
2. **Heat-map tier** — node retrieval frequency by Hermes Studio (high retrieval = high priority); primary signal
3. **High connectivity** — node has ≥3 `links_to` entries (high blast radius if stale)
4. **Low confidence floor** — node's `confidence_floor` < 0.25 (more fragile)
5. **FIFO** — otherwise, oldest-flagged first

Retrieval frequency is tracked by the Hermes context injection layer and surfaced as a node metadata property updated on each read.

### Processing

Any agent with wiki access picks up a `flagged` or `revalidating` node, sets `revalidation_status: revalidating`, re-reads/verifies the underlying claim, then either:
- **Confirms**: updates `last_verified_at`, restores `confidence` to initial value, resets to `current`
- **Updates**: rewrites node content with corrected info, same field resets
- **Retires**: marks node with `revalidation_status: retired` (not deleted; retained indefinitely per zero-rag philosophy)
- **Resolves conflict**: if `conflict_detected: true`, sets `conflict_detected: false`, clears `conflict_trigger_id`, resolves based on evidence

First-come-first-served on the flagged queue. No designated revalidation agent required.

### Telemetry hook

Expose `/revalidation/queue/depth` on the SSE server:

```json
{
  "queue_depth": 4,
  "by_status": { "flagged": 2, "revalidating": 1, "contested": 1 },
  "contested_count": 1,
  "oldest_flagged_at": "2026-04-22T14:00:00Z"
}
```

Alert threshold: queue depth > 10 for > 1h = backlog risk. Contested nodes always surface in telemetry regardless of queue depth. Log to stdout; integrate into any existing healthcheck.

---

## Retrieval Priority (separate from decay)

`source_reliability_index` has two roles that must not be conflated:

1. **Decay coefficient** — controls how fast confidence decays (covered above)
2. **Retrieval ranking weight** — ground-truth sources outrank transient observations at query time

Retrieval ranking (highest to lowest authority):
1. Repository / codebase (live truth)
2. Design docs, formal meeting outcomes
3. Bot-authored analysis with explicit sourcing
4. Chat observations, inferred state

A chat observation with a recent `last_verified_at` does NOT outrank an architectural constraint just because it's fresher. Retrieval must weight source authority, not only recency.

---

## Hermes Studio Boundary

Masking happens before any Hermes context injection:

```
wiki_read result → privacy_protocol masking layer → Hermes Studio context window
```

Hermes never has visibility into raw PII or private-tier nodes. This is enforced at the write-stream on the MCP server, not at the application layer. `contested` node metadata passes through to Hermes — agents in that context are expected to handle uncertainty.

---

## Resolved Design Decisions

| Question | Decision |
|---|---|
| Decay tick interval | 24h global default; per-node override via `decay_interval_hours` |
| Revalidation executor | Any agent with wiki access; first-come-first-served |
| `source_reliability_index` assignment | Manual seed at creation, tiered by source type |
| Retired node retention | Keep forever; zero-rag philosophy |
| Orphan taint handling | Cascade-clear worker sweeps depth-1 dependents when parent is `retired` or deleted; audit-logged |

---

*Draft ready for PR. Post comments in daemon-bot or open against `JPeetz/MeMex-Zero-RAG`.*
