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
- [ ] Hybrid search (BM25 + embeddings)
- [ ] Full ingest automation with LLM
- [ ] Real-time file watching

---

Copyright (c) 2026 Joerg Peetz. All rights reserved.
