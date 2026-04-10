---
title: "Zero-RAG"
type: concept
created: 2026-04-09
updated: 2026-04-09
status: active
source_count: 2
tags: [architecture, llm, knowledge-management]
---

# Zero-RAG

An approach to LLM knowledge management where sources are **compiled** into structured knowledge rather than **retrieved** as chunks at query time.

## The Problem with RAG

Traditional RAG (Retrieval Augmented Generation):
1. Chunk documents into pieces
2. Embed chunks as vectors
3. On query, retrieve relevant chunks
4. Generate answer from chunks

**The issue**: The LLM rediscovers knowledge from scratch every time. Nothing compounds. Ask a subtle question requiring 5 documents, and it pieces together fragments anew. [Source: wiki/sources/karpathy-llm-wiki-gist.md]

## The Zero-RAG Alternative

Instead of retrieving at query time:
1. LLM reads source **once**
2. Extracts entities, concepts, relationships
3. Writes structured wiki pages
4. Cross-references everything
5. Flags contradictions

On query, the LLM reads the **compiled wiki**, not raw chunks. The synthesis is already done. [Source: wiki/sources/karpathy-llm-wiki-gist.md]

## Trade-offs

| Aspect | RAG | Zero-RAG |
|--------|-----|----------|
| Setup cost | Low (just embed) | Higher (compile wiki) |
| Query cost | Per-query retrieval | Read compiled pages |
| Accumulation | None | Compounds over time |
| Contradictions | Discovered per-query | Flagged once |
| Maintenance | None | Requires lint/updates |

## When to Use Zero-RAG

✅ Deep research on one topic over time  
✅ Personal knowledge base you'll query repeatedly  
✅ When synthesis matters more than raw retrieval  

❌ One-off questions against large doc sets  
❌ Rapidly changing source material  
❌ Need for exact quotes from originals  

## Related

- [[andrej-karpathy]] — Coined the approach
- [[associative-trails]] — Historical precursor (Bush, 1945)

---

*Last updated: 2026-04-09*
