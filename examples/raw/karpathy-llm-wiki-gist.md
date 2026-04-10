# Karpathy's LLM Wiki Pattern

Source: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
Author: Andrej Karpathy
Date: April 2026

## Core Idea

Most people's experience with LLMs and documents looks like RAG: you upload a collection of files, the LLM retrieves relevant chunks at query time, and generates an answer. This works, but the LLM is rediscovering knowledge from scratch on every question. There's no accumulation.

The idea here is different. Instead of just retrieving from raw documents at query time, the LLM incrementally builds and maintains a persistent wiki — a structured, interlinked collection of markdown files that sits between you and the raw sources.

## Three Layers

1. **Raw sources** — your curated collection of source documents. Articles, papers, images, data files. These are immutable — the LLM reads from them but never modifies them.

2. **The wiki** — a directory of LLM-generated markdown files. Summaries, entity pages, concept pages, comparisons, an overview, a synthesis. The LLM owns this layer entirely.

3. **The schema** — a document (e.g. CLAUDE.md) that tells the LLM how the wiki is structured, what the conventions are, and what workflows to follow.

## Key Operations

- **Ingest**: Process a new source, create summary, update relevant pages
- **Query**: Search wiki, synthesize answer with citations
- **Lint**: Health-check for contradictions, orphans, stale content

## The Key Insight

"The wiki is a persistent, compounding artifact. The cross-references are already there. The contradictions have already been flagged. The synthesis already reflects everything you've read."

## Quote

"The human's job is to curate sources, direct the analysis, ask good questions, and think about what it all means. The LLM's job is everything else."
