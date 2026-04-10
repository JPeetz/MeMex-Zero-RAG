---
title: "Associative Trails"
type: concept
created: 2026-04-09
updated: 2026-04-09
status: active
source_count: 1
tags: [knowledge-management, memex, hypertext, history]
---

# Associative Trails

User-defined links between related pieces of information, mirroring how human memory works by association rather than hierarchical indexing.

## Origin

Conceived by [[vannevar-bush]] in his 1945 essay "As We May Think":

> "The process of tying two items together is the important thing... thereafter, at any time, when one of these items is in view, the other can be instantly recalled."

[Source: raw/memex-history.md]

## Core Insight

Human memory doesn't work like a filing cabinet (alphabetical, hierarchical). It works by **association** — one thought triggers another through learned connections.

Traditional information systems force us into artificial hierarchies:
- Folders within folders
- Alphabetical indexes
- Categorical taxonomies

Associative trails let the user define connections that matter to *them*. [Source: wiki/sources/memex-history.md]

## Modern Implementation

In a Memex wiki, associative trails manifest as:

- **[[Wikilinks]]**: Direct connections between pages
- **Cross-references**: "See also" sections
- **Backlinks**: Automatic reverse links
- **Graph views**: Visual representation of connections

The LLM creates and maintains these trails automatically during ingest. [Source: wiki/sources/karpathy-llm-wiki-gist.md]

## Why LLMs Matter

Bush's unsolved problem: who maintains the trails? Manual linking is tedious; people abandon their wikis.

LLMs don't get bored. They can:
- Detect implicit connections
- Create links automatically
- Update when new sources arrive
- Flag broken or stale trails

[Source: wiki/sources/memex-history.md]

## Related

- [[vannevar-bush]] — Originated the concept
- [[zero-rag]] — Modern implementation approach
- [[andrej-karpathy]] — Made it practical with LLMs

---

*Last updated: 2026-04-09*
