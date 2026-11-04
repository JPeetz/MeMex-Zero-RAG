# Memex MCP Server

Expose your Memex wiki to Claude Code, Codex, OpenClaw, and any MCP-compatible agent — locally via stdio or remotely via SSE.

## Installation

```bash
# Core (required)
pip install mcp

# SSE transport (required for remote/multi-agent access)
pip install uvicorn starlette sse-starlette
```

## Transport Modes

### stdio (default) — local agents

For Claude Code, Codex, or any agent running on the same machine:

```bash
cd /path/to/your/memex-wiki
python /path/to/memex/mcp/server.py
# or: memex serve
```

### SSE — remote/multi-agent access

For cross-machine access, shared wikis, or multi-agent setups (e.g. a team of AI agents sharing one wiki):

```bash
cd /path/to/your/memex-wiki
python /path/to/memex/mcp/server.py --transport sse --port 3001
```

Expose the port via Tailscale Funnel or ngrok, then connect any agent to:
`https://<your-tunnel-url>/sse`

## Configuration

### Claude Code (stdio)

Add to `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "memex": {
      "command": "python",
      "args": ["/path/to/memex/mcp/server.py"],
      "cwd": "/path/to/your/memex-wiki"
    }
  }
}
```

### Remote SSE client (OpenClaw, Hermes, or any MCP client)

Add to your agent's MCP config:

```json
{
  "mcpServers": {
    "memex": {
      "transport": "sse",
      "url": "https://<your-tunnel-url>/sse"
    }
  }
}
```

### OpenClaw (mcp.json)

```json
{
  "mcpServers": {
    "trio-wiki": {
      "transport": "sse",
      "url": "https://<host-tailscale-funnel-url>/sse"
    }
  }
}
```

## Multi-Agent Wiki Hosting

The SSE transport enables a shared knowledge base for teams of AI agents:

1. **One agent hosts** the wiki + MCP server (persistent machine recommended — server, always-on laptop, VPS)
2. **Expose via tunnel**: Tailscale Funnel (preferred — stable HTTPS, no account needed for clients) or ngrok
3. **All agents connect** as SSE clients using the public URL
4. **Concurrency**: `wiki_lock.py` (in `/mcp/`) provides advisory locking for safe concurrent writes

```
Agent A (writer) ──┐
                   ├──► MCP SSE Server ──► wiki/ (shared)
Agent B (reader) ──┘
Agent C (reader) ──┘
```

## Open Knowledge Format (OKF) export

MeMex ships an **OKF v0.2 exporter** so any OKF-aware agent or tool can read your
knowledge — interop without migrating your canonical store (which stays markdown
+ git, independent).

```bash
python memex_mcp/okf_export.py --wiki wiki --out /tmp/okf-bundle
```

- Emits a conformant OKF bundle: every page has frontmatter + a non-empty `type`,
  `[Source: X]` citations become OKF `sources`, `status: active` → `verified`,
  §8 grouped `index.md` + §9 `log.md`, and the root index declares `okf_version: "0.2"`.
- **Private content is excluded by default** (`agentforge/`, `L1/`, `raw/`, etc.) —
  an OKF bundle contains only clean, shareable knowledge. Override with `--exclude`.

## Search Backends

Markdown + git remain the single source of truth for every wiki page. The search
layer is a **selectable SQL engine** built by indexing that markdown — SQL makes
search fast and queryable, it never owns the knowledge.

| Backend | Engine | When to use |
|---------|--------|-------------|
| `sqlite` (default) | SQLite FTS5 + BLOB embeddings (local) | Single machine, zero setup — `.memex/search.db` |
| `postgres` | PostgreSQL + pgvector (`memex_mcp/pg_backend.py`) | Enterprise / multi-agent, relational + vector queries |
| `supabase` | Supabase (Postgres under the hood) | Managed cloud Postgres |

```bash
# Local (default)
python memex_mcp/server.py --wiki wiki/ --search-backend sqlite

# Enterprise (needs Postgres + pgvector)
pip install 'psycopg[binary]'
python memex_mcp/server.py --wiki wiki/ --search-backend postgres --pg-dsn "postgresql://user:pass@host:5432/memex"

# Supabase (managed)
python memex_mcp/server.py --wiki wiki/ --search-backend supabase --supabase-url "postgresql://..." --supabase-key "..."
```

If a requested backend's dependency (e.g. `psycopg`) is missing or unreachable,
the server degrades gracefully to the SQLite engine and logs a warning — it
never crashes. Build/refresh the index with `python memex_mcp/search.py -i` (SQLite)
or `python memex_mcp/pg_backend.py -i -d "<dsn>"` (Postgres), or let the server build
it lazily on first search.

## Available Tools

| Tool | Description |
|------|-------------|
| `wiki_search` | Keyword search across all wiki pages |
| `wiki_read` | Read a specific page by path |
| `wiki_list` | List all pages, optionally by type |
| `wiki_query` | Natural language Q&A (retrieval + context) |
| `wiki_ingest` | Ingest a new source document |
| `wiki_lint` | Health check: broken links, missing citations, orphans |
| `wiki_graph` | Export knowledge graph (JSON, Mermaid, or DOT) |
| `wiki_stats` | Page counts and link density metrics |

## Example Prompts

Once connected, ask your agent:

- "Search my wiki for 'zero-rag'"
- "Read the page about Karpathy"
- "List all concept pages"
- "What's the wiki health status?"
- "Show me the knowledge graph in Mermaid format"

## Roadmap

- [x] SSE transport for remote/multi-agent access
- [x] Hybrid search (BM25 + embeddings)
- [x] SQL backends: SQLite (default) + Postgres/pgvector (enterprise) via `--search-backend`
- [ ] Full ingest automation with LLM
- [ ] Real-time file watching

---

Copyright (c) 2026 Joerg Peetz. All rights reserved.
