---
title: "Karpathy's LLM Wiki Pattern"
type: source
created: 2026-04-09
updated: 2026-04-09
status: active
source_count: 1
tags: [llm, knowledge-management, wiki, ai-agents]
---

# Karpathy's LLM Wiki Pattern

A pattern for building personal knowledge bases using LLMs, published as a GitHub gist in April 2026. The gist went viral (5,000+ stars in days) and spawned multiple implementations.

## Core Insight

Traditional RAG retrieves document chunks on every query — the LLM rediscovers knowledge from scratch each time. The LLM Wiki approach is different: the LLM **compiles** sources into a persistent, interlinked wiki. Knowledge accumulates instead of resetting. [Source: raw/karpathy-llm-wiki-gist.md]

## Three-Layer Architecture

| Layer | Purpose | Ownership |
|-------|---------|-----------|
| raw/ | Immutable source documents | Human curates |
| wiki/ | Compiled knowledge pages | LLM maintains |
| schema | Wiki conventions & workflows | Co-evolved |

[Source: raw/karpathy-llm-wiki-gist.md]

## Key Operations

- **Ingest**: Process source → create summary → update entity/concept pages
- **Query**: Search wiki → synthesize answer → optionally file back
- **Lint**: Check for contradictions, orphans, stale content

[Source: raw/karpathy-llm-wiki-gist.md]

## The Famous Quote

> "The human's job is to curate sources, direct the analysis, ask good questions, and think about what it all means. The LLM's job is everything else."

[Source: raw/karpathy-llm-wiki-gist.md]

## Related

- [[andrej-karpathy]] — Author
- [[zero-rag]] — The underlying approach
- [[vannevar-bush]] — Historical inspiration (Memex, 1945)

---

*Ingested: 2026-04-09*
