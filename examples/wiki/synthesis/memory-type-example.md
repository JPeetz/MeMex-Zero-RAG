# Memory Type Taxonomy — Example Pages

This file shows what the optional `memory_type` frontmatter field looks like for each of the three memory types. Copy any of these blocks as a starting point. See [`SCHEMA.md`](../../SCHEMA.md#memory-type-taxonomy-memory_type) for the full rules.

## Episodic — a specific event / outcome

```yaml
---
title: BetterLife Posts — 2026-08-11
type: synthesis
memory_type: episodic
created: 2026-08-11
updated: 2026-08-11
status: active
tags: [betterlife, social, tip-tuesday]
---
```

*Episodic records **what happened** and **when** (a publish, an incident, a decision, a log).*

## Semantic — durable knowledge

```yaml
---
title: Redis Caching Strategy
type: concept
memory_type: semantic
created: 2026-05-01
updated: 2026-06-15
status: active
tags: [architecture, caching]
---
```

*Semantic records **what is known** — concepts, entities, and relations that hold over time.*

## Procedural — a repeatable method

```yaml
---
title: Marketing Image Review Protocol
type: governance
memory_type: procedural
created: 2026-07-15
updated: 2026-07-15
status: active
tags: [process, review, protocol]
---
```

*Procedural records **how to do it** — playbooks, workflows, SOPs, and heuristics.*

> **Note — retrieval guard:** older pages without `memory_type` remain fully queryable and equally weighted. Adding the label is optional and forward-looking; it never down-ranks or excludes untagged content.
