# Changelog

All notable changes to Memex will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [1.0.0] - 2026-04-09

### Added

- **Core Architecture**
  - L1/L2 cache hierarchy (private context + wiki)
  - Zero-RAG approach — compile once, query many
  - Git-native versioning with branch strategy

- **Anti-Hallucination Protocol**
  - Mandatory `[Source: path]` citations
  - Quarantine mode for unsourced pages
  - Hallucination tracking log

- **Human-in-the-Loop Conflict Resolution**
  - Contradictions flagged, never auto-resolved
  - `wiki/contradictions.md` for pending decisions
  - Resolution logging with rationale

- **Documentation**
  - `SCHEMA.md` — Complete wiki conventions
  - `PROMPTS.md` — Copy-paste prompt library
  - `GUIDE.md` — Deep dive tutorial
  - `RESEARCH.md` — Competitive analysis

- **Templates**
  - L1 templates (identity, rules, credentials)
  - Wiki structure (index, log, contradictions)
  - Example content demonstrating the pattern

### Credits

- Inspired by [Andrej Karpathy's LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- L1/L2 architecture from [MehmetGoekce/llm-wiki](https://github.com/MehmetGoekce/llm-wiki)
- Lifecycle patterns from [rohitg00's LLM Wiki v2](https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2)
- Original Memex concept by [Vannevar Bush](https://en.wikipedia.org/wiki/Memex) (1945)

---

## [1.3.0] - 2026-04-10

### Added

- **Hybrid Search** (`mcp/search.py`)
  - BM25 keyword search via SQLite FTS5
  - Semantic search via sentence-transformers or fastembed
  - Configurable weighting (default: 40% BM25, 60% semantic)
  - Incremental indexing (only re-index changed files)
  - CLI: `python mcp/search.py --index && python mcp/search.py "query"`

- **Confidence Scoring** (`mcp/confidence.py`)
  - Track claim certainty (high/medium/low/uncertain)
  - Source count analysis
  - Contradiction detection across pages
  - Staleness tracking (pages not verified in 90+ days)
  - Generate confidence reports: `python mcp/confidence.py --report`

- **Batch API** (`mcp/batch.py`)
  - 50% cost reduction via Anthropic/OpenAI batch APIs
  - Bulk source ingestion
  - Queue, submit, poll, and retrieve results
  - `MemexBatchIngest` helper for wiki ingestion

---

## [1.2.0] - 2026-04-10

### Added

- **Unified CLI** (`scripts/memex`)
  - `memex ingest <file>` - Auto-detect and ingest PDF, markdown, audio, or URL
  - `memex clip <url>` - Clip web pages
  - `memex voice [file]` - Record or transcribe voice
  - `memex search <query>` - Search the wiki
  - `memex lint [--fix]` - Check wiki health
  - `memex graph` - Generate knowledge graph
  - `memex serve` - Start MCP server

- **PDF Ingestion** (`scripts/ingest-pdf.py`)
  - PyMuPDF extraction with OCR fallback
  - Academic paper metadata (DOI, arXiv, abstract)
  - Auto-generates frontmatter and citations

- **Voice Capture** (`scripts/ingest-voice.py`)
  - Local Whisper transcription (no cloud API)
  - Live recording from microphone
  - Timestamped segments
  - Supports tiny/base/small/medium/large models

- **Web Clipper** (`scripts/clip-web.py`)
  - Readability + trafilatura extraction
  - Open Graph metadata
  - Clean markdown output
  - Auto-slugified filenames

- **Markdown Ingestion** (`scripts/ingest-md.py`)
  - Preserves or generates YAML frontmatter
  - Extracts title from H1 or filename
  - Converts Obsidian [[wikilinks]] ↔ [markdown](links)
  - Auto-detects page type (sources/entities/concepts/synthesis)
  - Bulk directory ingestion with `--recursive`

---

## [1.1.0] - 2026-04-10

### Added

- **MCP Server** (`mcp/server.py`)
  - 8 tools: search, read, list, query, ingest, lint, graph, stats
  - stdio transport for Claude Code integration
  - Full wiki operations via MCP protocol

- **GitHub Actions** (`.github/workflows/wiki-lint.yml`)
  - Automated wiki health checks on PR
  - Broken wikilink detection
  - Missing citation warnings
  - Orphan page detection
  - Markdown linting via markdownlint

- **Interactive Knowledge Graph** (`graph/graph.html`)
  - vis.js force-directed visualization
  - Color-coded by page type
  - Search and filter
  - Click to view connections
  - Build script: `scripts/build-graph.sh`

---

## [1.4.0] - 2026-04-21

### Added

- **SSE Transport** (`mcp/server.py`)
  - Implements `SseServerTransport` from the MCP Python SDK
  - Starlette + uvicorn server, SSE endpoint at `/sse`, POST handler at `/messages/`
  - Lazy imports: uvicorn/starlette only loaded when `--transport sse` is used; stdio users unaffected
  - Deploy: `python mcp/server.py --transport sse --port 3001`
  - Expose via Tailscale Funnel or ngrok for cross-machine access
  - Enables **multi-agent shared wiki**: multiple AI agents (Hermes, OpenClaw, Claude Code) can connect to one hosted wiki instance
  - New deps: `uvicorn>=0.27.0`, `starlette>=0.36.0`, `sse-starlette>=1.8.0`

### Changed

- `mcp/README.md`: Full rewrite — documents both stdio and SSE transports, multi-agent hosting pattern, OpenClaw/Hermes MCP config snippets, Tailscale Funnel setup
- `requirements.txt`: Added SSE transport dependencies
- `README.md`: Updated MCP Server section and Dependencies section to reflect SSE support

---


Copyright (c) 2026 Joerg Peetz. All rights reserved.
