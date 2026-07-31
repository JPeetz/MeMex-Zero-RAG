# Semantica — Analysis for MeMex Revamp

**Date:** 2026-07-08
**Repo:** https://github.com/semantica-agi/semantica
**Version:** 0.5.1 (latest PyPI)
**License:** MIT

## What Semantica Is

Semantica is a Python library that acts as a **Context & Accountability Layer** for AI systems. It sits alongside your existing stack (not replacing it) and adds:

- **Context Graphs** — structured, queryable graph of agent knowledge, decisions, and reasoning
- **Decision Intelligence** — every decision is a first-class object with causal chains
- **AI Governance** — SHACL constraints, policy enforcement, conflict detection (5 resolution strategies)
- **Full Auditability** — W3C PROV-O provenance on every fact, exportable to JSON/CSV/RDF
- **Reasoning Engines** — Forward chaining, Rete networks, Datalog, SPARQL (explainable, not black box)
- **Bi-temporal graphs** — point-in-time snapshots, time travel queries
- **Entity Resolution** — blocking + semantic deduplication

### Architecture

```
Sources (files, web, DBs, cloud, streams, dev)
  → Ingest → Parse → Normalize → Split (5 strategies)
  → Extract (NER, relations, events, triplets)
  → Conflict Detection → Deduplication
  → KG Construction → Knowledge Graph
  → Intelligence Layer (Ontology, Reasoning, Provenance, Context/Decisions)
  → Storage (FAISS/Qdrant/Neo4j/FalkorDB/...)
  → Export (RDF, JSON-LD, Cypher, CSV, HTML, ...)
```

### Integration Surface
- `pip install semantica` (Python library)
- 12-tool MCP server
- 109 REST endpoints
- 50+ CLI commands
- Agno native integration
- Plugins for 8 editors

### Key Differentiator from LangChain/LlamaIndex/Mem0/Zep
Semantica is built for **accountability**, not retrieval. It answers: "Prove what your AI decided, why, and whether it complied with policy." Traditional frameworks answer: "Find relevant chunks and generate an answer."

## Where MeMex Excels (Semantica Doesn't)

1. **Zero infrastructure.** MeMex is markdown + git. No Python, no torch, no Neo4j, no Docker. It works anywhere an LLM can read/write files.

2. **Git-native.** Full version history, branching, worktrees for multi-agent. Semantica uses graph databases for history — powerful but not as universally understood as git.

3. **Human-first.** Markdown files are readable by any human, any editor, any diff tool. Semantica's KGs require specialized tooling to inspect.

4. **Portable.** Clone a repo and you have the full knowledge base. Semantica needs database backends running.

5. **Proven simplicity.** MeMex has ~300k lines across 80 files. The pattern is understood by every LLM: read SCHEMA.md, read source, write wiki page.

## Where Semantica Excels (MeMex Doesn't)

1. **Decision Intelligence.** MeMex stores decisions as text in markdown. Semantica makes decisions first-class objects — queryable by precedent, causally linked, with impact analysis.

2. **Provenance.** MeMex requires *manual* source citation. Semantica tracks W3C PROV-O provenance automatically on every fact.

3. **Reasoning.** MeMex has no reasoning engine — the LLM does the thinking. Semantica has deterministic reasoning (Rete, Datalog, SPARQL) that can explain every inference path.

4. **Conflict Detection.** MeMex flags contradictions in text. Semantica detects, categorizes, and offers 5 resolution strategies (not just "human decides").

5. **Ontology Governance.** MeMex has SCHEMA.md (human convention). Semantica has OWL/SHACL with policy enforcement.

6. **Entity Resolution.** MeMex relies on human cross-referencing. Semantica has blocking + semantic deduplication.

7. **API surface.** MeMex has an MCP server with ~6 tools. Semantica has 109 REST endpoints, 50+ CLI commands, 12 MCP tools.

## Compatibility Issues

**Python 3.14 incompatibility:** Semantica depends on `torch>=1.12.0`. PyTorch does not yet have wheels for Python 3.14.5 (the system Python on this Mac). Semantica installs successfully on Python 3.12 via venv.

**Infrastructure requirements:** While Semantica works with local storage (SQLite, file-based), its full power requires Neo4j/FalkorDB (graph store) and FAISS/Qdrant (vector store). This contradicts MeMex's zero-infrastructure philosophy.

**Dependency weight:** Torch alone is ~2GB. This is a significant dependency for what MeMex currently does with zero Python packages.

## Revamp Options

### Option A: Semantica as Backend, MeMex as Frontend (Hybrid)

Keep MeMex's markdown wiki as the **human interface** and **source of truth**. Add Semantica as an **intelligence backend** that:
- Ingests MeMex wiki pages into a Context Graph
- Tracks agent decisions with provenance
- Provides advanced querying via SPARQL/Datalog
- Enforces SHACL constraints on wiki structure

This preserves zero-infra for reads while adding intelligence for analysis.

**Pro:** Best of both worlds. Markdown stays portable. Semantica adds power.
**Con:** Two systems to maintain. Sync between markdown and KG.
**Effort:** Medium. MCP server enhancement + Semantica ingestion pipeline.

### Option B: Full Semantica-Powered MeMex v2

Replace the markdown wiki with Semantica's KG as the primary knowledge store. The "wiki" becomes a view exported from the KG. All agent knowledge lives in nodes, edges, facts, and provenance records.

**Pro:** Maximum power. Decision intelligence, reasoning, provenance, governance.
**Con:** Loses zero-infra. Requires Python + torch + database. Higher barrier for new agents.
**Effort:** High. Complete rewrite of MeMex's core pattern.

### Option C: Side-by-Side (Recommended)

Keep MeMex as-is for knowledge management. Add Semantica as a separate **AgentForge Decision Intelligence System** that:
- Tracks all CEO/agent decisions with provenance and causal chains
- Provides audit trails for regulatory compliance
- Powers multi-agent shared context with graph-based reasoning
- Exports to W3C PROV-O for external audits

MeMex = knowledge (what we know). Semantica = accountability (what we decided and why).

**Pro:** Clear separation of concerns. MeMex doesn't break. Semantica adds missing capability.
**Con:** Not a unified system.
**Effort:** Low. Install Semantica, wire up decision tracking, document.

## Recommendation: Option C (Side-by-Side)

MeMex Zero RAG is a **documentation pattern**. Semantica is an **intelligence infrastructure**. They solve different problems.

The revamp shouldn't replace MeMex — it should extend it. MeMex continues as the canonical knowledge store (markdown + git). Semantica becomes the decision intelligence and accountability layer for AgentForge operations.

Specifically:
1. Install Semantica (Python 3.12 venv) for decision tracking
2. Wire `record_decision()` into CEO protocols — every major decision gets a first-class record
3. Use Semantica's MCP server alongside MeMex's MCP server
4. Build a bridge script: MeMex wiki → Semantica ingestion (wiki pages as source documents)
5. Keep MeMex's zero-infra promise for the core wiki — Semantica is optional power

## Next Steps
- [ ] Complete Python 3.12 venv install of Semantica
- [ ] Test Semantica MCP server + core ContextGraph API
- [ ] Design the MeMex→Semantica bridge (wiki pages as ingest sources)
- [ ] Wire decision tracking into CEO protocols
- [ ] Document in agent onboarding

## Sources
- https://github.com/semantica-agi/semantica — README and ARCHITECTURE.md
- https://raw.githubusercontent.com/semantica-agi/semantica/main/README.md
- https://raw.githubusercontent.com/semantica-agi/semantica/main/ARCHITECTURE.md
- https://docs.getsemantica.ai/ — official docs
- ~/workspace/MeMex-Zero-RAG/README.md — current MeMex architecture
- ~/workspace/MeMex-Zero-RAG/GUIDE.md — MeMex guide
