# Memex MCP Server

Expose your Memex wiki to Claude Code, Codex, and other MCP-compatible AI agents.

## Installation

```bash
pip install mcp
```

## Usage

### With Claude Code

Add to your Claude Code MCP config (`~/.claude/mcp.json`):

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

### Standalone

```bash
cd /path/to/your/memex-wiki
python /path/to/memex/mcp/server.py
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

Once connected, ask Claude:

- "Search my wiki for 'zero-rag'"
- "Read the page about Karpathy"
- "List all concept pages"
- "What's the wiki health status?"
- "Show me the knowledge graph in Mermaid format"

## Roadmap

- [ ] SSE transport for web clients
- [ ] Hybrid search (BM25 + embeddings)
- [ ] Full ingest automation with LLM
- [ ] Real-time file watching

---

Copyright (c) 2026 Joerg Peetz. All rights reserved.
