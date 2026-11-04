<div align="center">

# 🧠 MeMex — Zero-RAG Personal Knowledge Base

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Zero-RAG](https://img.shields.io/badge/Zero--RAG-No%20Embeddings-blue)](https://github.com/JPeetz/MeMex-Zero-RAG)
[![MCP Server](https://img.shields.io/badge/MCP-Server%20Included-purple)](mcp/)
[![LLM Agnostic](https://img.shields.io/badge/LLM-Agnostic-green)](https://github.com/JPeetz/MeMex-Zero-RAG)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-green)](https://www.python.org)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

**The Karpathy LLM Wiki pattern, production-ready.**

*No embeddings required. No vector database required. No infrastructure. Just markdown, git, and your LLM — with optional SQL search backends when you grow.*

[Quick Start](#quick-start) • [Why Zero-RAG](#why-not-rag) • [Directory](#directory-structure) • [MCP Server](mcp/) • [Prompts](PROMPTS.md) • [Schema](SCHEMA.md) • [Examples](examples/) • [SQL Backends](#sql-search-backends) • [Troubleshooting](#troubleshooting)

</div>

---

> *"The human's job is to curate sources, direct the analysis, ask good questions, and think about what it all means. The LLM's job is everything else."*
> — Andrej Karpathy

Based on [Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f), extended with:
- 🚫 **Zero hallucination enforcement** — every claim must cite a source
- 🤖 **MCP server** — expose your wiki to Claude Code, Codex, OpenClaw, Cursor, Hermes, any MCP agent
- 👥 **Multi-agent support** — multiple AI agents, one shared wiki, git handles conflicts
- 🔒 **Human-in-the-loop conflict resolution** — the LLM flags contradictions, you decide truth
- 📊 **Confidence tracking** — per-claim certainty scores, quarantine mode for low-confidence pages
- 🌐 **Knowledge graph** — interactive force-directed visualization of all [[wikilinks]] (optional)
- 🗄️ **Optional SQL search backends** — SQLite (local) or PostgreSQL + pgvector (enterprise) when you outgrow plain crawl-search

---

## Why Not RAG?

Traditional RAG retrieves document chunks on every query. Your LLM rediscovers knowledge from scratch. Every. Single. Time. Nothing compounds.

**MeMex compiles knowledge once.** Your LLM reads your sources and builds a structured, interlinked wiki. Every new source makes the whole wiki richer. Knowledge grows — it doesn't reset.

```
RAG:   Source → [retrieve] → LLM → Answer    (rediscovers every time)
MeMex: Source → [compile]  → Wiki → LLM       (compounds over time)
```

```mermaid
flowchart LR
    subgraph Input
        R["raw/ sources"]
    end
    subgraph Processing
        L["LLM reads & extracts"]
    end
    subgraph Knowledge
        W["wiki/ compiled knowledge"]
    end
    subgraph Output
        O["outputs/ reports"]
    end
    R --> L
    L --> W
    W --> O
    W -->|compounds over time| W
```

## Key Principles

| Principle | What it means |
|-----------|---------------|
| **LLM-agnostic** | Works with Claude, GPT, Gemini, Llama, Codex, OpenClaw, Hermes — any agent that reads/writes files |
| **Zero required infrastructure** | No database, no embeddings, no server needed. Markdown + git only |
| **Git-native** | Full version history, branching, rollback, multi-agent worktrees |
| **Zero hallucination** | Every claim cites a source. Unsourced = lint ERROR. Enforced on every PR |
| **Human-in-the-loop** | Conflicting sources get flagged and paused — you decide truth, not the LLM |
| **Memory taxonomy** | Optional `memory_type` (episodic/semantic/procedural). See [SCHEMA.md](SCHEMA.md#memory-type-taxonomy-memory_type) |
| **Markdown is the truth** | The wiki (`wiki/*.md`) + git is the single source of truth; SQL is only a search index on top of it |

---

## Quick Start

### 1. Clone

```bash
git clone https://github.com/JPeetz/MeMex-Zero-RAG.git my-wiki
cd my-wiki
```

That's it for the wiki itself — **no setup, no API keys, no database.** The repo ships with a neutral starter wiki (`wiki/index.md` + `wiki/log.md` + example entity/concept/source pages).

### 2. Add a source

Drop any document into `raw/`:

```bash
cp ~/Downloads/interesting-article.md raw/
```

Anything the LLM can read works: markdown, PDF, EPUB, an article URL, a voice note. Use the [CLI tools](#cli-tooling) to convert PDF/URL/voice, or drop a `.md` directly.

### 3. Tell your LLM to ingest it

Open Claude Code, Cursor, Codex, OpenClaw, Hermes, or any AI coding agent and paste:

```text
Read SCHEMA.md. Then ingest raw/interesting-article.md following the ingest workflow.
```

The LLM will:
- Read the source and discuss key takeaways with you first
- Create a summary page in `wiki/sources/`
- Create or update entity pages (`wiki/entities/`) and concept pages (`wiki/concepts/`)
- Cross-link everything with [[wikilinks]]
- Update `wiki/index.md`
- Log the operation in `wiki/log.md`

**You approve before it writes.** The LLM proposes the pages it will create and waits.

### 4. Query your knowledge base

```text
Read wiki/index.md. Based on the knowledge base, answer: [YOUR QUESTION].
Cite which wiki pages informed your answer.
```

### 5. Run the MCP server (optional — for agent tooling)

Expose your wiki as MCP tools so any compatible agent can search/read/write directly:

```bash
# Create and activate a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate

# Install dependencies
pip install 'mcp>=0.9.0,<2.0'        # MCP SDK (version-pinned — v2 removed APIs this server uses)

# Start in stdio mode (for Claude Code / local agents)
python mcp/server.py --wiki wiki/

# SSE mode (for remote / multi-agent access)
pip install uvicorn starlette sse-starlette
python mcp/server.py --transport sse --port 3001 --wiki wiki/
```

**First search autobuilds the SQLite index** (`.memex/search.db`) — no manual migration. Or pre-build it:
```bash
python mcp/search.py -i --wiki wiki/
```

---

## Directory Structure

```
your-wiki/
├── L1/                      # 🔒 Auto-loaded, git-ignored (private)
│   ├── identity.md          # Your preferences, context
│   ├── rules.md             # Hard constraints, gotchas
│   └── credentials.md       # API keys (NEVER committed)
│
├── raw/                     # 📥 Source documents (immutable)
│
├── wiki/                    # 📚 LLM-maintained knowledge base
│   ├── index.md             # Master catalog
│   ├── log.md               # Operation history
│   ├── contradictions.md    # Pending conflict resolutions (created on demand)
│   ├── sources/             # One summary per ingested source
│   ├── entities/            # People, orgs, tools, projects
│   ├── concepts/            # Ideas, frameworks, patterns
│   └── synthesis/           # Analyses, comparisons, insights
│
├── outputs/                 # 📤 Generated reports, slides
├── mcp/                     # 🔌 MCP server (stdio + SSE)
├── scripts/                 # CLI tools (memex ingest/search/lint/graph/serve)
├── .venv/                   # 🔒 Python virtual environment (git-ignored)
├── graph/                   # 🌐 Generated knowledge-graph HTML (git-ignored)
├── SCHEMA.md                # 🧠 The brain — how the wiki works
├── PROMPTS.md               # 📋 Copy-paste prompts for all operations
├── GUIDE.md                 # 🧭 Deep-dive guide (setup, scaling, maintenance)
└── README.md                # This file
```

---

## The L1/L2 Architecture

Inspired by CPU cache hierarchy:

| Layer | What | Loaded When | Contains |
|-------|------|-------------|----------|
| **L1** | `L1/` directory | Every session (auto-loaded by your agent) | Identity, rules, credentials |
| **L2** | `wiki/` directory | On-demand via queries | Deep knowledge, cross-references |

**L1 is git-ignored** — it holds sensitive context that must never be committed. Copy the `.example` files to `.md` to use it:
```bash
cp L1/identity.md.example L1/identity.md
cp L1/rules.md.example     L1/rules.md
cp L1/credentials.md.example L1/credentials.md
```

**L2 is the wiki** — versioned, shareable, grows over time.

---

## Zero Hallucination Protocol

MeMex enforces citation discipline at every level:

1. **Every claim must have a source**: `[Source: filename.md]`
2. **Lint catches violations**: unsourced claims are 🔴 ERROR, not warnings
3. **Quarantine mode**: pages with >20% unsourced claims get `status: quarantine`
4. **GitHub Actions**: broken links, missing citations, orphan pages checked on every PR

```markdown
✅ Correct:  "Project X uses Redis [Source: architecture.md]"
❌ Rejected: "Project X uses Redis" (no source → lint error)
```

## Conflict Resolution

When sources contradict each other:
1. The LLM flags the conflict in `wiki/contradictions.md`
2. The LLM stops and asks you which claim is authoritative
3. **You** decide — the LLM never auto-resolves truth
4. The decision is logged with rationale

---

## MCP Tools

When running `python mcp/server.py`, your agent gets these tools:

| Tool | Description |
|------|-------------|
| `wiki_search` | Hybrid search (SQL backend) across all pages |
| `wiki_read` | Read a specific page by path |
| `wiki_read_by_slug` | Read a page by bare slug (no type prefix); scans all four type dirs |
| `wiki_list` | List pages by type (entities/concepts/sources/synthesis) |
| `wiki_query` | Natural-language query with source attribution |
| `wiki_write` | Write a page with git attribution (returns commit SHA); accepts lifecycle fields |
| `wiki_flag` | Mark a page for revalidation → `status: quarantine` + reason/timestamp |
| `wiki_revalidate` | Close a revalidation: `confirm` / `update` / `retire` |
| `wiki_ingest` | Ingest a raw source into the wiki |
| `wiki_lint` | Run health checks on the wiki |
| `wiki_graph` | Generate wikilink relationship graph |
| `wiki_stats` | Summary statistics |

### Lifecycle management

Pages carry a `status` field (`draft` \| `active` \| `stale` \| `quarantine`):

- **`wiki_flag(page, reason)`** — sets `status: quarantine`, stamps reason + UTC timestamp. Refuses on `is_immutable: true` pages.
- **`wiki_revalidate(page, outcome, new_body?, new_sources?, rationale?)`**:
  - `confirm` → clears quarantine → `active` (keeps content)
  - `update` → replaces body with `new_body` → `active`
  - `retire` → sets `status: stale`, clears flag metadata
- **`wiki_read_by_slug(slug)`** — resolves a bare slug across `entities/ concepts/ sources/ synthesis/`. Returns `{"found": false}` or `{"found": false, "ambiguous": true, "candidates": [...]}`.

Full field reference: [`SCHEMA.md`](SCHEMA.md#lifecycle-mapping-plugin--backend).

---

## SQL Search Backends

Markdown + git **remain the single source of truth**. The search layer is a selectable SQL engine indexing that markdown — SQL makes search fast and queryable at scale, it never owns the knowledge.

| Backend | Engine | When to use |
|---------|--------|-------------|
| `sqlite` (**default**) | SQLite FTS5 + BLOB embeddings (local) | Single machine, zero setup — `.memex/search.db` |
| `postgres` | PostgreSQL + pgvector (`mcp/pg_backend.py`) | Enterprise / multi-agent, relational + vector queries |
| `supabase` | Supabase (Postgres under the hood) | Managed cloud Postgres |

### SQLite (default, zero config)

```bash
python mcp/server.py --wiki wiki/ --search-backend sqlite
# first search auto-builds .memex/search.db; or pre-build:
python mcp/search.py -i --wiki wiki/
```

### Postgres + pgvector (enterprise)

```bash
pip install 'psycopg[binary]'     # optional dependency
python mcp/server.py --wiki wiki/ --search-backend postgres \
  --pg-dsn "postgresql://user:pass@host:5432/memex"
```

Schema (auto-created by `mcp/pg_backend.py`): a `mcp_pages` table with a
tsvector column (keyword rank) + a `vector` embedding column with an HNSW index
(semantic). Hybrid score = `bm25_weight × keyword + semantic_weight × cosine`.

### Supabase (managed Postgres)

```bash
python mcp/server.py --wiki wiki/ --search-backend supabase \
  --supabase-url "postgresql://..." --supabase-key "..."
```

### Backend selection & graceful degradation

- `--search-backend` selects the engine; `--pg-dsn` / `--supabase-url` / `--supabase-key` configure it.
- If a requested backend's dependency is missing (`psycopg`) or unreachable, the server **degrades gracefully to SQLite** and logs a warning — it never crashes.
- Pre-build/refresh the Postgres index: `python mcp/pg_backend.py -i -d "<dsn>" --wiki wiki/`.

> **Design note.** This is the same schema pattern used by the OpenText AgentOps *Learning Engineer* platform (`learning-store.sql`): one SQL knowledge-store pattern, portable across projects.

---

## Client Configuration

### Claude Code (project-scoped `.mcp.json` — checked into version control)

```json
{
  "mcpServers": {
    "memex": {
      "command": "python3",
      "args": ["mcp/server.py", "--wiki", "wiki/"],
      "cwd": "."
    }
  }
}
```

Or via CLI:
```bash
claude mcp add --scope project memex -- python3 mcp/server.py --wiki wiki/
```

### OpenClaw

```json
{
  "plugins": {
    "mcp": {
      "servers": [{ "name": "memex", "transport": "stdio", "command": "python3 mcp/server.py --wiki wiki/" }]
    }
  }
}
```

### Remote SSE client (Hermes, OpenClaw, any MCP client)

```json
{
  "mcpServers": {
    "memex": { "transport": "sse", "url": "https://<your-tunnel-url>/sse" }
  }
}
```

---

## Knowledge Graph Visualization

Optional interactive force-directed graph of every [[wikilink]]:

```bash
python3 mcp/server.py --enable-graph --wiki wiki/
```

- `wiki_graph` MCP tool builds `graph/graph.html` — open in any browser (dark theme, vis-network).
- Auto-rebuilds on every `wiki_write` when enabled.
- Nodes = pages, edges = [[wikilinks]], filters by type, live search, type-coded colors.
- Fully optional — MeMex works without it.

---

## Multi-Agent Support

Multiple agents can write the same wiki simultaneously via git worktrees:

```bash
git worktree add ../wiki-agent-1 feat/agent-1
git worktree add ../wiki-agent-2 feat/agent-2
```

- `wiki_write` commits with attribution: `wiki(agent-name): add/update type/slug`.
- Git handles authorship, history, and conflict detection natively.
- See [GUIDE.md](GUIDE.md) for the full multi-agent setup.

---

## CLI Tooling

```bash
# Add scripts/ to your PATH once
export PATH="$PATH:/path/to/memex/scripts"

memex setup                      # Print setup & install instructions
memex ingest paper.pdf           # PDF with academic metadata
memex ingest https://example.com # Web page
memex search "machine learning"  # Hybrid SQL search
memex lint --fix                 # Check wiki health (fix optional)
memex graph                      # Generate wikilink graph
memex serve                      # Start MCP server
memex --help                     # Show all commands
```

---

## Requirements

- **Any AI coding agent**: Claude Code, Cursor, Codex, OpenClaw, Hermes, Gemini CLI, etc.
- **Git** for version control.
- **Python 3.9+** for the MCP server + CLI (wiki itself needs none).
- Optional: `sentence-transformers` or `fastembed` for dense semantic search;
  `psycopg[binary]` for the Postgres backend.

---

## Testing

```bash
pip install -r requirements-test.txt
pytest tests/
```

43 tests cover lifecycle management (`wiki_flag`/`wiki_revalidate`), slug
resolution, frontmatter injection, SQL backend factory, and MCP tool registration.

---

## Scaling Up

| Size | Strategy |
|------|----------|
| 0–50 pages | `wiki/index.md` is enough; crawl-search works |
| 50–200 pages | Add the SQLite search backend (default) for FTS5 + optional embeddings |
| 200+ pages | Postgres/pgvector backend, or split into multiple wikis (`ml-wiki/`, `project-wiki/`) |

---

## Optional Enhancements

| Tool | What it does | When to add |
|------|--------------|-------------|
| [Obsidian](https://obsidian.md) | Graph view, backlinks, visual navigation | From day one |
| [qmd](https://github.com/tobi/qmd) | Local hybrid search | 100+ pages |
| [Marp](https://marp.app) | Slide decks from wiki content | When presenting |
| [Batch API](mcp/batch.py) | ~50% cost reduction for bulk ingests | Large ingest sessions |

---

## Troubleshooting

| Symptom | Cause & fix |
|---------|-------------|
| `MCP package not installed` | `mcp` SDK missing. Run `pip install 'mcp>=0.9.0,<2.0'` (v2 removed APIs). Do NOT `pip install mcp` unpinned |
| Server won't start | Check `mcp<2.0` pin — v2.x broke `Server.list_tools()` / `stdio_server` |
| `ModuleNotFoundError: numpy` | Install dep: `pip install numpy` (used by the search index) |
| Postgres backend "fell back to sqlite" | `psycopg` not installed or DB unreachable. Install `pip install 'psycopg[binary]'` and check `--pg-dsn` |
| `wiki/index.md` says "empty" after ingest | Ingest created pages but missed the index update — ask the LLM to re-run index catalog |
| LLM isn't citing sources | Reinforce: "every factual claim MUST have [Source: path]. No exceptions." |
| Pages not cross-referenced | Ask explicitly to add [[wikilinks]] both directions |
| L1 accidentally committed | `git filter-branch` to purge, then rotate any keys that were in it (see GUIDE.md) |
| `import mcp` inside repo root is ambiguous | The local `mcp/` dir shadows the installed SDK only when *you* `import mcp` from repo root. Run the server as `python mcp/server.py` (works) or from a neutral cwd |
| Wiki search returns substring-only | Dense embeddings need `sentence-transformers`/`fastembed`; without them it's FTS5/keyword (still works) |

---

## Contributing

PRs welcome. Please:
1. Run `pytest tests/` before opening a PR.
2. Don't commit real credentials or live private wikis — this is a public framework.
3. Match the existing JSON-schema + frontmatter conventions (see `SCHEMA.md`).

---

## Credits

- [Vannevar Bush](https://en.wikipedia.org/wiki/Memex) — Original Memex concept (1945)
- [Andrej Karpathy](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — LLM Wiki pattern
- [MehmetGoekce/llm-wiki](https://github.com/MehmetGoekce/llm-wiki) — L1/L2 cache architecture inspiration
- [rohitg00's LLM Wiki v2](https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2) — Lifecycle and consolidation patterns

## Author

[Joerg Peetz](https://github.com/JPeetz) — with contributions from Molty, Coconut, Marvin (AI collaborators on the MeMex team)

## License

MIT — Use it, fork it, adapt it, share it.

---

*Start small. Ingest one source. Ask one question. Watch the wiki grow.*

---

*Part of the [AgentForge Ecosystem](https://github.com/JPeetz/agentforge)*

Copyright (c) 2026 Joerg Peetz. All rights reserved.