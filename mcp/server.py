#!/usr/bin/env python3
# Copyright (c) 2026 Joerg Peetz. All rights reserved.
"""
Memex MCP Server

Exposes your Memex wiki to Claude Code, Codex, and other MCP-compatible agents.

Usage:
    # stdio transport (default, for Claude Code)
    python server.py
    
    # SSE transport (for web clients)
    python server.py --transport sse --port 3001

Requires:
    pip install mcp sqlite3

Optional (for advanced features):
    pip install sentence-transformers  # Hybrid search
    pip install anthropic              # Batch API
"""

import argparse
import asyncio
import json
import os
import re
import sqlite3
import sys
from pathlib import Path
from typing import Optional

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.server.sse import SseServerTransport
    from mcp.types import Tool, TextContent
except ImportError:
    print("MCP package not installed. Run: pip install mcp")
    exit(1)


class InvalidStateError(Exception):
    """Raised when a lifecycle-transition tool is called against a page
    whose current ``status`` doesn't permit that transition (e.g.
    wiki_revalidate against a page that was never wiki_flag'd into
    quarantine)."""


class AmbiguousSlugError(Exception):
    """Raised by wiki_read_by_slug when a bare slug matches pages in more
    than one type directory (e.g. both concepts/marvin and
    entities/marvin exist). Callers must disambiguate using wiki_read
    with a full type-prefixed path instead."""

    def __init__(self, slug: str, candidates: list):
        self.slug = slug
        self.candidates = candidates
        super().__init__(
            f"Ambiguous slug '{slug}': matches multiple pages: "
            f"{', '.join(candidates)}. Use wiki_read with a full path instead."
        )


class MemexServer:
    """MCP server for Memex wiki operations."""
    
    def __init__(self, wiki_path: str = "wiki", enable_graph: bool = False,
                 search_backend: str = "sqlite", pg_dsn: str = "",
                 supabase_url: str = "", supabase_key: str = ""):
        self.wiki_path = Path(wiki_path)
        self.raw_path = Path("raw")
        self.db_path = Path(".memex/search.db")
        self.enable_graph = enable_graph
        self.search_backend = search_backend
        self.pg_dsn = pg_dsn
        self.supabase_url = supabase_url
        self.supabase_key = supabase_key
        self.server = Server("memex")
        self._setup_tools()
    
    def _setup_tools(self):
        """Register all MCP tools."""
        
        @self.server.list_tools()
        async def list_tools():
            tools = [
                Tool(
                    name="wiki_search",
                    description="Search the Memex wiki using keywords. Returns matching pages with snippets.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query (keywords or phrase)"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Max results (default 10)",
                                "default": 10
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="wiki_read",
                    description="Read a wiki page by path (e.g., 'concepts/zero-rag' or 'entities/karpathy').",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "Page path relative to wiki/ (without .md extension)"
                            }
                        },
                        "required": ["path"]
                    }
                ),
                Tool(
                    name="wiki_read_by_slug",
                    description="Read a wiki page by bare slug (no type prefix), searching entities/concepts/sources/synthesis for a match. Returns found=false if missing, or an error listing candidates if the slug is ambiguous across type dirs.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "slug": {
                                "type": "string",
                                "description": "URL-safe page slug without type prefix or .md extension (e.g. 'zero-rag')"
                            }
                        },
                        "required": ["slug"]
                    }
                ),
                Tool(
                    name="wiki_list",
                    description="List all pages in the wiki, optionally filtered by type (sources, entities, concepts, synthesis).",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "type": {
                                "type": "string",
                                "description": "Filter by page type: sources, entities, concepts, synthesis, or 'all'",
                                "enum": ["all", "sources", "entities", "concepts", "synthesis"]
                            }
                        }
                    }
                ),
                Tool(
                    name="wiki_query",
                    description="Ask a natural language question. Searches wiki and synthesizes an answer with citations.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "question": {
                                "type": "string",
                                "description": "Natural language question about the wiki contents"
                            }
                        },
                        "required": ["question"]
                    }
                ),
                Tool(
                    name="wiki_ingest",
                    description="Ingest a new source document into the wiki. Creates summary and updates relevant pages.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "source_path": {
                                "type": "string",
                                "description": "Path to source file in raw/ directory"
                            },
                            "dry_run": {
                                "type": "boolean",
                                "description": "Preview changes without writing (default false)",
                                "default": False
                            }
                        },
                        "required": ["source_path"]
                    }
                ),
                Tool(
                    name="wiki_lint",
                    description="Check wiki health: broken links, missing citations, orphan pages, contradictions.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "fix": {
                                "type": "boolean",
                                "description": "Auto-fix simple issues (default false)",
                                "default": False
                            }
                        }
                    }
                ),
                Tool(
                    name="wiki_graph",
                    description="Get the wiki knowledge graph as nodes and edges for visualization.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "format": {
                                "type": "string",
                                "description": "Output format: json, mermaid, or dot",
                                "enum": ["json", "mermaid", "dot"],
                                "default": "json"
                            }
                        }
                    }
                ),
                Tool(
                    name="wiki_stats",
                    description="Get wiki statistics: page counts, link density, health metrics.",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="wiki_confidence",
                    description="Analyze wiki confidence: distribution, stale pages, contradictions.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "page": {
                                "type": "string",
                                "description": "Optional: specific page slug to analyze"
                            }
                        }
                    }
                ),
                Tool(
                    name="wiki_write",
                    description="Write a new wiki page (or overwrite existing). Creates file at wiki/{type}/{slug}.md and commits with agent attribution.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "type": {
                                "type": "string",
                                "description": "Page type: entities, concepts, sources, or synthesis",
                                "enum": ["entities", "concepts", "sources", "synthesis"]
                            },
                            "slug": {
                                "type": "string",
                                "description": "URL-safe filename without .md (e.g. 'marvin' or 'zero-rag-design')"
                            },
                            "title": {
                                "type": "string",
                                "description": "Human-readable page title"
                            },
                            "content": {
                                "type": "string",
                                "description": "Full markdown body (excluding frontmatter)"
                            },
                            "tags": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of tags",
                                "default": []
                            },
                            "agent": {
                                "type": "string",
                                "description": "Agent name for commit attribution (e.g. 'marvin', 'molty', 'coconut')",
                                "default": "unknown"
                            },
                            "overwrite": {
                                "type": "boolean",
                                "description": "Overwrite if page already exists (default false)",
                                "default": False
                            },
                            "status": {
                                "type": "string",
                                "description": "Lifecycle status of this page. One of draft, active, stale, quarantine. Defaults to active.",
                                "enum": ["draft", "active", "stale", "quarantine"],
                                "default": "active"
                            },
                            "source_reliability_index": {
                                "type": "number",
                                "description": "Optional Source Reliability Index in [0.0, 1.0] describing how trustworthy this page's underlying sources are.",
                                "minimum": 0.0,
                                "maximum": 1.0
                            },
                            "is_immutable": {
                                "type": "boolean",
                                "description": "If true, this page represents a locked/immutable fact and downstream tools should refuse to mutate it.",
                                "default": False
                            }
                        },
                        "required": ["type", "slug", "title", "content"]
                    }
                ),
                Tool(
                    name="wiki_flag",
                    description="Mark a wiki page for revalidation. Sets status: quarantine and records a reason and timestamp.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "page": {
                                "type": "string",
                                "description": "Page path relative to wiki/ without .md extension (e.g. 'concepts/foo')"
                            },
                            "reason": {
                                "type": "string",
                                "description": "Why the page needs revalidation"
                            }
                        },
                        "required": ["page", "reason"]
                    }
                ),
                Tool(
                    name="wiki_revalidate",
                    description="Complete a revalidation cycle for a quarantined page. Outcome: confirm (-> active), update (-> active with new content), or retire (-> stale).",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "page": {
                                "type": "string",
                                "description": "Page path relative to wiki/ without .md extension (e.g. 'concepts/foo')"
                            },
                            "outcome": {
                                "type": "string",
                                "description": "Revalidation outcome",
                                "enum": ["confirm", "update", "retire"]
                            },
                            "new_body": {
                                "type": "string",
                                "description": "Replacement markdown body. Required when outcome=update."
                            },
                            "new_sources": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Optional list of new/updated [Source: ...] citations",
                                "default": []
                            },
                            "rationale": {
                                "type": "string",
                                "description": "Why this outcome was chosen",
                                "default": ""
                            }
                        },
                        "required": ["page", "outcome"]
                    }
                ),
                Tool(
                    name="wiki_graph",
                    description="Build and return path to the interactive knowledge graph visualization (graph/graph.html). Requires --enable-graph.",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ) if self.enable_graph else None
            ]
            return [t for t in tools if t is not None]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict):
            try:
                if name == "wiki_search":
                    result = await self._search(arguments.get("query", ""), arguments.get("limit", 10))
                elif name == "wiki_read":
                    result = await self._read(arguments.get("path", ""))
                elif name == "wiki_read_by_slug":
                    try:
                        lookup = await self._read_by_slug(arguments.get("slug", ""))
                    except AmbiguousSlugError as e:
                        result = json.dumps({
                            "found": False,
                            "ambiguous": True,
                            "candidates": e.candidates,
                        })
                    else:
                        if lookup["found"]:
                            result = lookup["content"]
                        else:
                            result = json.dumps({"found": False})
                elif name == "wiki_list":
                    result = await self._list(arguments.get("type", "all"))
                elif name == "wiki_query":
                    result = await self._query(arguments.get("question", ""))
                elif name == "wiki_ingest":
                    result = await self._ingest(arguments.get("source_path", ""), arguments.get("dry_run", False))
                elif name == "wiki_lint":
                    result = await self._lint(arguments.get("fix", False))
                elif name == "wiki_graph":
                    if not self.enable_graph:
                        result = "Error: wiki_graph requires --enable-graph flag on server startup"
                    else:
                        result = await self._build_graph()
                elif name == "wiki_stats":
                    result = await self._stats()
                elif name == "wiki_confidence":
                    result = await self._confidence(arguments.get("page", None))
                elif name == "wiki_write":
                    result = await self._write(
                        page_type=arguments.get("type", "concepts"),
                        slug=arguments.get("slug", ""),
                        title=arguments.get("title", ""),
                        content=arguments.get("content", ""),
                        tags=arguments.get("tags", []),
                        agent=arguments.get("agent", "unknown"),
                        overwrite=arguments.get("overwrite", False),
                        status=arguments.get("status", "active"),
                        source_reliability_index=arguments.get("source_reliability_index"),
                        is_immutable=arguments.get("is_immutable", False),
                    )
                elif name == "wiki_flag":
                    result = await self._flag(
                        page=arguments.get("page", ""),
                        reason=arguments.get("reason", ""),
                    )
                elif name == "wiki_revalidate":
                    result = await self._revalidate(
                        page=arguments.get("page", ""),
                        outcome=arguments.get("outcome", ""),
                        new_body=arguments.get("new_body"),
                        new_sources=arguments.get("new_sources", []),
                        rationale=arguments.get("rationale", ""),
                    )
                else:
                    result = f"Unknown tool: {name}"
                
                return [TextContent(type="text", text=result)]
            except Exception as e:
                return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    async def _search(self, query: str, limit: int = 10, min_confidence: str = "low") -> str:
        """Search wiki pages. Uses hybrid BM25+dense search if available, falls back to substring."""
        results = []
        query_lower = query.lower()
        hybrid_available = False

        # Tier 1: Try the configured SQL search backend (markdown stays the source
        # of truth; the backend is a queryable index). Degrades to substring below.
        if not hasattr(self, '_search_backend_engine'):
            from mcp.backend import get_backend
            engine, warn = get_backend(
                self.search_backend, str(self.wiki_path),
                pg_dsn=getattr(self, 'pg_dsn', ''),
                supabase_url=getattr(self, 'supabase_url', ''),
            )
            self._search_backend_engine = engine
            self._search_backend_warn = warn
            if warn:
                import logging
                logging.getLogger(__name__).warning("memex search backend: %s", warn)
            # Build/refresh the index (idempotent; skips unchanged pages).
            try:
                engine.index()
            except Exception as exc:
                import logging
                logging.getLogger(__name__).warning(
                    "memex search index build failed: %s", exc)

        engine = self._search_backend_engine
        try:
            hybrid_results = engine.search(query, limit=limit * 2)
            if hybrid_results:
                hybrid_available = True
                for result in hybrid_results[:limit * 2]:
                    try:
                        path = result.path
                        score = result.score
                        full_path = self.wiki_path / path
                        if not full_path.exists():
                            continue
                        content_raw = full_path.read_text(encoding="utf-8")
                        # Confidence filter
                        if min_confidence and min_confidence != "none":
                            conf_match = __import__('re').search(
                                r'\[confidence:\s*(high|medium|low|uncertain)\]', content_raw)
                            conf_levels = {"high": 4, "medium": 3, "low": 2, "uncertain": 1}
                            page_conf = conf_levels.get(conf_match.group(1) if conf_match else "medium", 3)
                            min_conf_val = conf_levels.get(min_confidence, 2)
                            if page_conf < min_conf_val:
                                continue
                        snippet = content_raw[:300] + ("..." if len(content_raw) > 300 else "")
                        results.append(
                            f"## {path}\n**Score:** {score:.3f}\n\n{snippet}\n")
                    except Exception:
                        continue
                results = results[:limit]
        except Exception:
            pass  # fall through to substring

        # Tier 2: Substring search (always available as fallback)
        if not hybrid_available:
            for md_file in self.wiki_path.rglob("*.md"):
                if md_file.name.startswith("."):
                    continue

                import re as _re
                content = md_file.read_text(encoding="utf-8")
                if query_lower in content.lower():
                    # Confidence filter
                    if min_confidence and min_confidence != "none":
                        conf_match = _re.search(
                            r'\[confidence:\s*(high|medium|low|uncertain)\]', content)
                        conf_levels = {"high": 4, "medium": 3, "low": 2, "uncertain": 1}
                        page_conf = conf_levels.get(conf_match.group(1) if conf_match else "medium", 3)
                        min_conf_val = conf_levels.get(min_confidence, 2)
                        if page_conf < min_conf_val:
                            continue
                    # Extract snippet around match
                    idx = content.lower().find(query_lower)
                    start = max(0, idx - 100)
                    end = min(len(content), idx + len(query) + 100)
                    snippet = content[start:end].replace("\n", " ").strip()
                    if start > 0:
                        snippet = "..." + snippet
                    if end < len(content):
                        snippet = snippet + "..."

                    rel_path = md_file.relative_to(self.wiki_path)
                    results.append({
                        "path": str(rel_path).replace(".md", ""),
                        "snippet": snippet
                    })

                    if len(results) >= limit:
                        break

        if not results:
            return f"No results found for: {query}"
        
        output = f"Found {len(results)} result(s) for '{query}':\n\n"
        for r in results:
            output += f"- **{r['path']}**: {r['snippet']}\n\n"
        return output
    
    async def _read(self, path: str) -> str:
        """Read a wiki page."""
        # Normalize path
        path = path.strip("/").replace(".md", "")
        file_path = self.wiki_path / f"{path}.md"
        
        if not file_path.exists():
            # Try searching in subdirectories
            for subdir in ["sources", "entities", "concepts", "synthesis"]:
                alt_path = self.wiki_path / subdir / f"{path}.md"
                if alt_path.exists():
                    file_path = alt_path
                    break
        
        if not file_path.exists():
            return f"Page not found: {path}\n\nUse wiki_list to see available pages."
        
        return file_path.read_text(encoding="utf-8")

    async def _read_by_slug(self, slug: str) -> dict:
        """Find a page by bare slug across all type dirs and delegate to _read().

        Returns a dict:
          - {"found": False} when no page matches the slug
          - {"found": True, "path": "<type>/<slug>", "content": "<full page text>"}
            when exactly one page matches

        Raises:
          ValueError: if ``slug`` is empty or contains a '/' (i.e. is not a
            bare slug — callers with a full path should use wiki_read instead).
          AmbiguousSlugError: if the slug matches pages in more than one type
            directory. The error carries ``candidates`` (list of "type/slug"
            paths) for the caller to disambiguate with.
        """
        slug = slug.strip().strip("/")
        if slug.endswith(".md"):
            slug = slug[: -len(".md")]

        if not slug:
            raise ValueError("slug must not be empty")
        if "/" in slug:
            raise ValueError(
                f"'{slug}' is not a bare slug (contains '/'); "
                "use wiki_read with a full path instead"
            )

        candidates = []
        for type_dir in ("entities", "concepts", "sources", "synthesis"):
            candidate_path = self.wiki_path / type_dir / f"{slug}.md"
            if candidate_path.exists():
                candidates.append(f"{type_dir}/{slug}")

        if not candidates:
            return {"found": False}

        if len(candidates) > 1:
            raise AmbiguousSlugError(slug, candidates)

        path = candidates[0]
        content = await self._read(path)
        return {"found": True, "path": path, "content": content}
    
    async def _list(self, page_type: str = "all") -> str:
        """List wiki pages."""
        pages = {"sources": [], "entities": [], "concepts": [], "synthesis": [], "other": []}
        
        for md_file in self.wiki_path.rglob("*.md"):
            if md_file.name.startswith("."):
                continue
            
            rel_path = md_file.relative_to(self.wiki_path)
            parts = rel_path.parts
            
            if len(parts) > 1 and parts[0] in pages:
                pages[parts[0]].append(str(rel_path).replace(".md", ""))
            else:
                pages["other"].append(str(rel_path).replace(".md", ""))
        
        output = "# Wiki Pages\n\n"
        
        categories = ["sources", "entities", "concepts", "synthesis", "other"] if page_type == "all" else [page_type]
        
        for cat in categories:
            if cat in pages and pages[cat]:
                output += f"## {cat.title()} ({len(pages[cat])})\n\n"
                for p in sorted(pages[cat]):
                    output += f"- {p}\n"
                output += "\n"
        
        return output
    
    async def _query(self, question: str) -> str:
        """Natural language query (simplified - just searches and returns context)."""
        # This is a simplified version - in production, you'd call an LLM
        search_results = await self._search(question, limit=5)
        
        return f"""## Question: {question}

### Relevant Pages

{search_results}

---

*Note: For full Q&A synthesis, use this context with your LLM. The MCP server provides retrieval; synthesis happens in your agent.*
"""
    
    async def _ingest(self, source_path: str, dry_run: bool = False) -> str:
        """Ingest a source document (stub - returns instructions)."""
        source_file = self.raw_path / source_path
        
        if not source_file.exists():
            return f"Source not found: {source_path}\n\nPlace files in raw/ directory first."
        
        return f"""## Ingest: {source_path}

To ingest this source, follow these steps:

1. **Read the source**: Use your file reading capability to read `raw/{source_path}`

2. **Create summary page**: Write to `wiki/sources/{source_file.stem}.md` with:
   - Frontmatter (title, type: source, created, tags)
   - Summary of key points
   - `[Source: raw/{source_path}]` citations

3. **Extract entities**: Create/update pages in `wiki/entities/` for people, companies, projects

4. **Extract concepts**: Create/update pages in `wiki/concepts/` for ideas, methods, frameworks

5. **Update index**: Add new pages to `wiki/index.md`

6. **Update log**: Append operation to `wiki/log.md`

{"[DRY RUN - No changes made]" if dry_run else ""}

See SCHEMA.md for detailed conventions.
"""
    
    async def _lint(self, fix: bool = False) -> str:
        """Check wiki health."""
        issues = {"broken_links": [], "missing_citations": [], "orphans": []}
        all_pages = set()
        linked_pages = set()
        
        # Collect all pages and links
        for md_file in self.wiki_path.rglob("*.md"):
            if md_file.name.startswith("."):
                continue
            
            rel_path = str(md_file.relative_to(self.wiki_path)).replace(".md", "")
            all_pages.add(rel_path)
            
            content = md_file.read_text(encoding="utf-8")
            
            # Find wikilinks [[page]]
            links = re.findall(r'\[\[([^\]]+)\]\]', content)
            for link in links:
                linked_pages.add(link)
                # Check if target exists
                target_exists = False
                for subdir in ["", "sources/", "entities/", "concepts/", "synthesis/"]:
                    if (self.wiki_path / f"{subdir}{link}.md").exists():
                        target_exists = True
                        break
                if not target_exists:
                    issues["broken_links"].append(f"{rel_path} → [[{link}]]")
            
            # Check for citations
            if "/sources/" in str(md_file) or "/entities/" in str(md_file) or "/concepts/" in str(md_file):
                if "[Source:" not in content and "source_count: 0" not in content:
                    # Check if it's a stub or has actual content
                    lines = [l for l in content.split("\n") if l.strip() and not l.startswith("#") and not l.startswith("---")]
                    if len(lines) > 5:  # Has substantial content
                        issues["missing_citations"].append(rel_path)
        
        # Find orphans (pages not linked from anywhere)
        for page in all_pages:
            page_name = page.split("/")[-1]
            if page_name not in ["index", "log", "contradictions"] and page_name not in linked_pages:
                issues["orphans"].append(page)
        
        # Build report
        output = "# Wiki Health Check\n\n"
        
        total_issues = sum(len(v) for v in issues.values())
        if total_issues == 0:
            output += "✅ **All checks passed!**\n\n"
        else:
            output += f"⚠️ **{total_issues} issue(s) found**\n\n"
        
        if issues["broken_links"]:
            output += f"## Broken Links ({len(issues['broken_links'])})\n\n"
            for link in issues["broken_links"]:
                output += f"- {link}\n"
            output += "\n"
        
        if issues["missing_citations"]:
            output += f"## Missing Citations ({len(issues['missing_citations'])})\n\n"
            for page in issues["missing_citations"]:
                output += f"- {page}\n"
            output += "\n"
        
        if issues["orphans"]:
            output += f"## Orphan Pages ({len(issues['orphans'])})\n\n"
            for page in issues["orphans"]:
                output += f"- {page}\n"
            output += "\n"
        
        output += f"---\n\n{'[DRY RUN]' if not fix else '[AUTO-FIX NOT YET IMPLEMENTED]'}"
        
        return output
    
    async def _graph(self, format: str = "json") -> str:
        """Generate knowledge graph."""
        nodes = []
        edges = []
        
        for md_file in self.wiki_path.rglob("*.md"):
            if md_file.name.startswith("."):
                continue
            
            rel_path = str(md_file.relative_to(self.wiki_path)).replace(".md", "")
            parts = rel_path.split("/")
            node_type = parts[0] if len(parts) > 1 else "root"
            node_id = parts[-1]
            
            nodes.append({"id": node_id, "label": node_id.replace("-", " ").title(), "type": node_type})
            
            content = md_file.read_text(encoding="utf-8")
            links = re.findall(r'\[\[([^\]]+)\]\]', content)
            for link in links:
                edges.append({"source": node_id, "target": link})
        
        if format == "json":
            return json.dumps({"nodes": nodes, "edges": edges}, indent=2)
        
        elif format == "mermaid":
            output = "graph TD\n"
            for node in nodes:
                output += f"    {node['id']}[\"{node['label']}\"]\n"
            for edge in edges:
                output += f"    {edge['source']} --> {edge['target']}\n"
            return output
        
        elif format == "dot":
            output = "digraph wiki {\n    rankdir=LR;\n"
            for node in nodes:
                shape = {"sources": "box", "entities": "ellipse", "concepts": "diamond", "synthesis": "hexagon"}.get(node["type"], "box")
                output += f'    "{node["id"]}" [label="{node["label"]}", shape={shape}];\n'
            for edge in edges:
                output += f'    "{edge["source"]}" -> "{edge["target"]}";\n'
            output += "}"
            return output
        
        return "Unknown format"
    
    async def _stats(self) -> str:
        """Get wiki statistics."""
        stats = {"sources": 0, "entities": 0, "concepts": 0, "synthesis": 0, "other": 0}
        total_links = 0
        total_citations = 0
        
        for md_file in self.wiki_path.rglob("*.md"):
            if md_file.name.startswith("."):
                continue
            
            rel_path = str(md_file.relative_to(self.wiki_path))
            parts = rel_path.split("/")
            
            if len(parts) > 1 and parts[0] in stats:
                stats[parts[0]] += 1
            else:
                stats["other"] += 1
            
            content = md_file.read_text(encoding="utf-8")
            total_links += len(re.findall(r'\[\[([^\]]+)\]\]', content))
            total_citations += len(re.findall(r'\[Source:', content))
        
        total_pages = sum(stats.values())
        
        return f"""# Wiki Statistics

## Page Counts
- **Sources**: {stats['sources']}
- **Entities**: {stats['entities']}
- **Concepts**: {stats['concepts']}
- **Synthesis**: {stats['synthesis']}
- **Other**: {stats['other']}
- **Total**: {total_pages}

## Link Density
- **Total wikilinks**: {total_links}
- **Total citations**: {total_citations}
- **Links per page**: {total_links / max(total_pages, 1):.1f}
- **Citations per page**: {total_citations / max(total_pages, 1):.1f}

## Health
Run `wiki_lint` for detailed health check.
"""
    
    async def _confidence(self, page: str = None) -> str:
        """Analyze wiki confidence: distribution, stale pages, contradictions."""
        try:
            from mcp.confidence import ConfidenceTracker
            tracker = ConfidenceTracker(str(self.wiki_path))
            stats = tracker.get_stats()

            output = "# Wiki Confidence Report\n\n"
            output += f"**Total pages analyzed:** {stats.get('total_pages', 0)}\n"
            output += f"**Avg confidence score:** {stats.get('avg_confidence', 0)}\n\n"
            output += "## Confidence Distribution\n"
            output += "| Level | Count |\n|-------|-------|\n"
            output += f"| high | {stats.get('high_confidence', 0)} |\n"
            output += f"| medium | {stats.get('medium_confidence', 0)} |\n"
            output += f"| low | {stats.get('low_confidence', 0)} |\n"
            output += f"\n**Stale pages:** {stats.get('stale_pages', 0)}\n"
            output += f"**With contradictions:** {stats.get('with_contradictions', 0)}\n"

            if page:
                pages = stats.get('pages', {})
                if page in pages:
                    p = pages[page]
                    output += f"\n## Page: {page}\n"
                    output += f"- Confidence: {p.get('confidence', 'unknown')}\n"
                    output += f"- Verified: {p.get('verified', 'never')}\n"
                    output += f"- Contradictions: {p.get('has_contradictions', False)}\n"
                else:
                    output += f"\nPage '{page}' not found in wiki.\n"

            return output
        except ImportError:
            return "Confidence analysis requires mcp.confidence module (install dependencies)."
        except Exception as e:
            return f"Confidence analysis error: {e}"

    async def _build_graph(self) -> str:
        """Build knowledge graph from wiki pages."""
        try:
            import graph_builder as gb
            stats = gb.build_graph(
                wiki_dir=str(self.wiki_path),
                output_dir=str(self.wiki_path.parent / "graph")
            )
            return (
                f"# Knowledge Graph Built\n\n"
                f"**Nodes:** {stats['nodes']}\n"
                f"**Edges:** {stats['edges']}\n"
                f"**Data:** `{stats['data_path']}`\n"
                f"**Open in browser:** `{stats['graph_html']}`\n"
            )
        except ImportError:
            return "Error: mcp.graph_builder module not found. Is --enable-graph set?"
        except Exception as e:
            return f"Graph build error: {e}"

    
    async def _write(self, page_type: str, slug: str, title: str, content: str,
                       tags: list = None, agent: str = "unknown", overwrite: bool = False,
                       status: str = "active",
                       source_reliability_index: Optional[float] = None,
                       is_immutable: bool = False) -> str:
        """Write a new wiki page and git commit with agent attribution."""
        import re as _re
        import subprocess
        from datetime import date

        if not slug:
            return "Error: slug is required"
        if not title:
            return "Error: title is required"

        # Sanitise slug
        slug = _re.sub(r'[^a-z0-9-]', '-', slug.lower()).strip('-')
        if not slug:
            return "Error: slug contains no valid characters"

        type_dir = self.wiki_path / page_type
        type_dir.mkdir(parents=True, exist_ok=True)
        dest = type_dir / f"{slug}.md"

        # Determine action before writing (for commit message)
        action = "update" if dest.exists() else "add"

        if dest.exists() and not overwrite:
            return f"Error: {page_type}/{slug}.md already exists. Pass overwrite=true to replace."

        # Citation enforcement: derived pages must cite at least one source
        EXEMPT_PAGES = {"index", "log", "contradictions"}
        EXEMPT_TYPES = {"sources"}
        if slug not in EXEMPT_PAGES and page_type not in EXEMPT_TYPES:
            if "[Source:" not in content:
                return "❌ Rejected: page has no [Source: ...] citation. Every wiki page must cite at least one source (e.g., [Source: raw/article.md])."

        # Bug fix: use explicit type map instead of naive trailing-s strip
        TYPE_SINGULAR = {
            "entities": "entity",
            "concepts": "concept",
            "sources": "source",
            "synthesis": "synthesis",
        }
        type_singular = TYPE_SINGULAR.get(page_type, page_type)

        today = date.today().isoformat()

        # Lifecycle fields (plugin-compat vocabulary).
        # `status` always emitted; `source_reliability_index` and
        # `is_immutable` are only emitted when non-default so we don't
        # bloat frontmatter on legacy pages.
        allowed_status = {"draft", "active", "stale", "quarantine"}
        if status not in allowed_status:
            return (
                f"Error: invalid status '{status}'. Must be one of "
                f"{sorted(allowed_status)}."
            )

        sri_val = None
        if source_reliability_index is not None:
            try:
                sri_val = float(source_reliability_index)
            except (TypeError, ValueError):
                return (
                    "Error: source_reliability_index must be a number in "
                    "[0.0, 1.0]."
                )
            if not (0.0 <= sri_val <= 1.0):
                return (
                    "Error: source_reliability_index must be in [0.0, 1.0]."
                )

        # Build frontmatter as a dict and serialize with yaml.safe_dump()
        # rather than f-string interpolation. `title` and `agent` are
        # user-supplied strings and could otherwise inject arbitrary
        # frontmatter keys (e.g. an embedded newline forging
        # "is_immutable: true"). safe_dump correctly quotes/escapes any
        # value containing YAML-significant characters.
        import yaml as _yaml

        frontmatter_dict = {
            "title": title,
            "type": type_singular,
            "tags": tags or [],
            "created": today,
            "author": agent,
            "status": status,
        }
        if sri_val is not None:
            frontmatter_dict["source_reliability_index"] = sri_val
        if is_immutable:
            frontmatter_dict["is_immutable"] = True

        frontmatter_yaml = _yaml.safe_dump(
            frontmatter_dict, default_flow_style=False, sort_keys=False
        )
        frontmatter = f"---\n{frontmatter_yaml}---\n"
        dest.write_text(frontmatter + "\n" + content, encoding="utf-8")

        # Git commit — parse SHA from 'git rev-parse HEAD' for reliability
        try:
            subprocess.run(["git", "add", str(dest)], cwd=str(self.wiki_path.parent), check=True, capture_output=True)
            commit_msg = f"wiki({agent}): {action} {page_type}/{slug}"
            result = subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd=str(self.wiki_path.parent), capture_output=True, text=True
            )
            if result.returncode == 0:
                sha_result = subprocess.run(
                    ["git", "rev-parse", "HEAD"],
                    cwd=str(self.wiki_path.parent), capture_output=True, text=True
                )
                sha = sha_result.stdout.strip()[:12] if sha_result.returncode == 0 else "unknown"
                # Operation log: append entry to wiki/log.md
                try:
                    from datetime import datetime as _dt
                    entry = f"- {_dt.now().strftime('%Y-%m-%d %H:%M')}: {action} {page_type}/{slug}.md (agent: {agent})\n"
                    log_path = self.wiki_path / "log.md"
                    log_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(log_path, "a", encoding="utf-8") as lf:
                        lf.write(entry)
                except Exception:
                    pass  # logging failure is non-fatal
                # Auto-rebuild knowledge graph
                if self.enable_graph:
                    try:
                        import graph_builder as gb
                        gs = gb.build_graph(
                            wiki_dir=str(self.wiki_path),
                            output_dir=str(self.wiki_path.parent / "graph")
                        )
                        graph_note = f"\nGraph rebuilt: {gs['nodes']} nodes, {gs['edges']} edges"
                    except Exception:
                        graph_note = ""  # non-fatal
                else:
                    graph_note = ""
                return f"✅ Written: {page_type}/{slug}.md\nCommit: {sha}\nAgent: {agent}{graph_note}"
            else:
                return f"⚠️ Written to disk but git commit failed: {result.stderr.strip()}. Run 'git commit' manually."
        except Exception as e:
            return f"✅ Written: {page_type}/{slug}.md (git error: {e})"

    async def _flag(self, page: str, reason: str) -> str:
        """Mark a wiki page for revalidation: status -> quarantine, with reason + timestamp.

        Frontmatter is read with yaml.safe_load, mutated as a dict, and
        rewritten with yaml.safe_dump — never via string/regex surgery —
        so we can't corrupt or become vulnerable to injection through
        existing frontmatter values (mirrors the _write() hardening).
        """
        import re as _re
        import subprocess
        import yaml as _yaml
        from datetime import datetime, timezone

        if not page:
            raise ValueError("page is required")
        if not reason:
            raise ValueError("reason is required")

        page = page.strip("/")
        if page.endswith(".md"):
            page = page[:-3]
        page_path = self.wiki_path / f"{page}.md"

        if not page_path.exists():
            raise FileNotFoundError(f"Page not found: {page}")

        raw = page_path.read_text(encoding="utf-8")
        fm_match = _re.match(r"^---\n(.*?)\n---\n(.*)$", raw, _re.DOTALL)
        if not fm_match:
            raise ValueError(f"Page {page} has no valid YAML frontmatter block")

        frontmatter_dict = _yaml.safe_load(fm_match.group(1)) or {}
        body = fm_match.group(2)

        # SCHEMA.md §Lifecycle Mapping: is_immutable=true pages are the
        # backend-side lock corresponding to the plugin's locked-fact
        # semantics; wiki_flag (and any other edit tool) MUST refuse to
        # mutate them rather than silently quarantining a locked fact.
        if frontmatter_dict.get("is_immutable") is True:
            raise PermissionError(
                f"Page {page} is immutable (is_immutable: true); refusing to flag it."
            )

        frontmatter_dict["status"] = "quarantine"
        frontmatter_dict["flagged_reason"] = reason
        frontmatter_dict["flagged_at"] = (
            datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        )

        frontmatter_yaml = _yaml.safe_dump(
            frontmatter_dict, default_flow_style=False, sort_keys=False
        )
        page_path.write_text(f"---\n{frontmatter_yaml}---\n{body}", encoding="utf-8")

        # Git commit — best-effort, mirrors _write()'s non-fatal handling.
        try:
            subprocess.run(
                ["git", "add", str(page_path)],
                cwd=str(self.wiki_path.parent), check=True, capture_output=True,
            )
            subprocess.run(
                ["git", "commit", "-m", f"flag: {page} ({reason})"],
                cwd=str(self.wiki_path.parent), capture_output=True, text=True,
            )
        except Exception:
            pass  # non-fatal; page is already written to disk

        return json.dumps({"page": page, "status": "quarantine", "reason": reason})

    async def _revalidate(
        self,
        page: str,
        outcome: str,
        new_body: Optional[str] = None,
        new_sources: Optional[list] = None,
        rationale: str = "",
    ) -> str:
        """Complete a revalidation cycle for a quarantined page.

        outcome=confirm: status -> active, flag fields cleared.
        outcome=update:  body replaced with new_body, status -> active,
                          flag fields cleared.
        outcome=retire:  status -> stale, retired_at + retire_rationale
                          recorded.

        Frontmatter is read with yaml.safe_load, mutated as a dict, and
        rewritten with yaml.safe_dump — never via string/regex surgery —
        mirroring _write() and _flag()'s injection-hardening.
        """
        import re as _re
        import subprocess
        import yaml as _yaml
        from datetime import datetime, timezone

        if not page:
            raise ValueError("page is required")
        if not outcome:
            raise ValueError("outcome is required")

        page = page.strip("/")
        if page.endswith(".md"):
            page = page[:-3]
        page_path = self.wiki_path / f"{page}.md"

        if not page_path.exists():
            raise FileNotFoundError(f"Page not found: {page}")

        raw_text = page_path.read_text(encoding="utf-8")
        fm_match = _re.match(r"^---\n(.*?)\n---\n(.*)$", raw_text, _re.DOTALL)
        if not fm_match:
            raise ValueError(f"Page {page} has no valid YAML frontmatter block")

        frontmatter_dict = _yaml.safe_load(fm_match.group(1)) or {}
        body_str = fm_match.group(2)

        # SCHEMA.md §Lifecycle Mapping: is_immutable=true pages MUST NOT be
        # mutated by wiki_revalidate. Checked before the quarantine-state
        # guard so a locked fact can never be confirmed/updated/retired
        # even if it somehow ended up with status: quarantine.
        if frontmatter_dict.get("is_immutable") is True:
            raise PermissionError(
                f"Page {page} is immutable (is_immutable: true); refusing to revalidate it."
            )

        current_status = frontmatter_dict.get("status")
        if current_status != "quarantine":
            raise InvalidStateError(
                f"Page {page} has status={current_status!r}; can only "
                f"revalidate pages with status='quarantine' (flag it first)."
            )

        if outcome == "confirm":
            frontmatter_dict["status"] = "active"
            frontmatter_dict.pop("flagged_reason", None)
            frontmatter_dict.pop("flagged_at", None)
        elif outcome == "update":
            if not new_body:
                raise ValueError("outcome='update' requires new_body")
            body_str = f"\n{new_body}"
            frontmatter_dict["status"] = "active"
            frontmatter_dict.pop("flagged_reason", None)
            frontmatter_dict.pop("flagged_at", None)
        elif outcome == "retire":
            frontmatter_dict["status"] = "stale"
            frontmatter_dict["retired_at"] = (
                datetime.now(timezone.utc).replace(microsecond=0).isoformat()
            )
            frontmatter_dict["retire_rationale"] = rationale
            # A3.5 fix: retire must clear the flag lifecycle fields too,
            # for consistency with confirm/update — the flag has been
            # resolved (by retirement) either way.
            frontmatter_dict.pop("flagged_reason", None)
            frontmatter_dict.pop("flagged_at", None)
        else:
            raise ValueError(f"unknown outcome: {outcome!r}; must be one of confirm, update, retire")

        # A3.5 fix: new_sources was accepted but never wired up — append
        # the citations as a new [Source: ...] line on the body so they
        # actually land on disk (mirrors _write()'s citation format).
        if new_sources:
            citation_line = f"\n\n[Source: {', '.join(new_sources)}]"
            body_str = f"{body_str}{citation_line}"

        frontmatter_yaml = _yaml.safe_dump(
            frontmatter_dict, default_flow_style=False, sort_keys=False
        )
        page_path.write_text(f"---\n{frontmatter_yaml}---\n{body_str.lstrip(chr(10)) if outcome == 'update' else body_str}", encoding="utf-8")

        # Git commit — best-effort, mirrors _write()/_flag()'s non-fatal handling.
        try:
            subprocess.run(
                ["git", "add", str(page_path)],
                cwd=str(self.wiki_path.parent), check=True, capture_output=True,
            )
            subprocess.run(
                ["git", "commit", "-m", f"revalidate({outcome}): {page}"],
                cwd=str(self.wiki_path.parent), capture_output=True, text=True,
            )
        except Exception:
            pass  # non-fatal; page is already written to disk

        return json.dumps({"page": page, "outcome": outcome, "rationale": rationale})

    async def run(self, transport: str = "stdio", port: int = 3001):
        """Start the MCP server."""
        if transport == "stdio":
            async with stdio_server() as (read_stream, write_stream):
                await self.server.run(read_stream, write_stream, self.server.create_initialization_options())
        else:
            try:
                import uvicorn
                from starlette.applications import Starlette
                from starlette.requests import Request
                from starlette.responses import Response
                from starlette.routing import Mount, Route
            except ImportError:
                raise ImportError("SSE transport requires: pip install uvicorn starlette sse-starlette")

            sse_transport = SseServerTransport("/messages/")

            async def handle_sse(request: Request) -> Response:
                async with sse_transport.connect_sse(
                    request.scope, request.receive, request._send
                ) as streams:
                    await self.server.run(
                        streams[0], streams[1],
                        self.server.create_initialization_options()
                    )
                return Response()

            starlette_app = Starlette(routes=[
                Route("/sse", endpoint=handle_sse, methods=["GET"]),
                Mount("/messages/", app=sse_transport.handle_post_message),
            ])

            print(f"Starting Memex MCP SSE server on port {port}")
            print(f"Connect via: http://localhost:{port}/sse")
            uvicorn.run(starlette_app, host="0.0.0.0", port=port)


def main():
    parser = argparse.ArgumentParser(description="Memex MCP Server")
    parser.add_argument("--transport", choices=["stdio", "sse"], default="stdio")
    parser.add_argument("--port", type=int, default=3001)
    parser.add_argument("--wiki", type=str, default="wiki", help="Path to wiki directory")
    parser.add_argument("--enable-graph", action="store_true", default=False,
                        help="Enable the wiki_graph MCP tool (builds knowledge graph from [[wikilinks]])")
    parser.add_argument("--search-backend", choices=["sqlite", "supabase"], default="sqlite",
                        help="Search backend: sqlite (local FTS5) or supabase (remote, requires --supabase-url and --supabase-key)")
    parser.add_argument("--supabase-url", type=str, default="",
                        help="Supabase project URL (required when --search-backend supabase)")
    parser.add_argument("--supabase-key", type=str, default="",
                        help="Supabase service role key (required when --search-backend supabase)")
    parser.add_argument("--pg-dsn", type=str, default="",
                        help="Postgres/pgvector connection string (for --search-backend postgres)")
    args = parser.parse_args()
    
    server = MemexServer(wiki_path=args.wiki, enable_graph=args.enable_graph,
                         search_backend=args.search_backend,
                         pg_dsn=args.pg_dsn, supabase_url=args.supabase_url,
                         supabase_key=args.supabase_key)
    asyncio.run(server.run(transport=args.transport, port=args.port))


if __name__ == "__main__":
    main()
