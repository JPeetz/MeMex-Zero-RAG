---
title: "From Memex to LLM Wiki: 80 Years in the Making"
type: synthesis
created: 2026-04-09
updated: 2026-04-09
status: active
source_count: 3
tags: [synthesis, history, memex, llm-wiki, analysis]
---

# From Memex to LLM Wiki: 80 Years in the Making

A synthesis exploring how [[vannevar-bush]]'s 1945 vision became [[andrej-karpathy]]'s 2026 reality.

## The Vision (1945)

Bush imagined a "memex" — a personal device storing all books, records, and communications with mechanized speed and flexibility. The key innovation: [[associative-trails]] linking information the way human memory works. [Source: wiki/sources/memex-history.md]

## The Problem

Bush described the **what** but couldn't solve the **how**. Creating and maintaining associative trails required tedious manual work. Every link had to be made by hand. As the collection grew, maintenance became impossible.

> "The web became something different — public, chaotic, organized by search engines rather than personal association."

[Source: raw/memex-history.md]

## The Failed Intermediaries

Between 1945 and 2026, several attempts got partway there:

| System | Contribution | Limitation |
|--------|--------------|------------|
| Hypertext (1960s) | Links between documents | Manual creation |
| Personal wikis | User-owned knowledge | Maintenance burden |
| Roam/Obsidian | Bidirectional links | Still manual |
| RAG systems | AI-powered retrieval | No accumulation |

All required humans to do the tedious work, or gave up on structure entirely.

## The Solution (2026)

LLMs changed the equation. They can:

1. **Read** sources and extract structure
2. **Write** summaries, entity pages, concept pages
3. **Link** related information automatically
4. **Maintain** cross-references without getting bored
5. **Flag** contradictions and stale content

The [[zero-rag]] approach compiles knowledge once, then keeps it current. The LLM is the librarian Bush needed but couldn't build. [Source: wiki/sources/karpathy-llm-wiki-gist.md]

## What Changed

| 1945 Problem | 2026 Solution |
|--------------|---------------|
| Manual link creation | LLM extracts & links |
| Maintenance burden | LLM maintains & lints |
| Contradiction detection | LLM flags, [[human-in-the-loop]] resolves |
| Cross-reference updates | Automatic on ingest |

## The Remaining Gap

Bush envisioned **sharing** trails — passing your research path to others. Current LLM wikis are mostly personal. Future work: collaborative Memex with multi-user trails.

## Conclusion

It took 80 years, but the Memex is finally buildable. The core insight was always right: associative trails beat hierarchical filing. We just needed a tireless librarian.

> "The human's job is to curate sources, direct the analysis, ask good questions, and think about what it all means. The LLM's job is everything else."
> — [[andrej-karpathy]]

[Source: raw/karpathy-llm-wiki-gist.md]

---

*Synthesized: 2026-04-09*
