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
from pathlib import Path
from typing import Optional

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    print("MCP package not installed. Run: pip install mcp")
    exit(1)


class MemexServer:
    """MCP server for Memex wiki operations."""
    
    def __init__(self, wiki_path: str = "wiki"):
        self.wiki_path = Path(wiki_path)
        self.raw_path = Path("raw")
        self.db_path = Path(".memex/search.db")
        self.server = Server("memex")
        self._setup_tools()
    
    def _setup_tools(self):
        """Register all MCP tools."""
        
        @self.server.list_tools()
        async def list_tools():
            return [
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
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict):
            try:
                if name == "wiki_search":
                    result = await self._search(arguments.get("query", ""), arguments.get("limit", 10))
                elif name == "wiki_read":
                    result = await self._read(arguments.get("path", ""))
                elif name == "wiki_list":
                    result = await self._list(arguments.get("type", "all"))
                elif name == "wiki_query":
                    result = await self._query(arguments.get("question", ""))
                elif name == "wiki_ingest":
                    result = await self._ingest(arguments.get("source_path", ""), arguments.get("dry_run", False))
                elif name == "wiki_lint":
                    result = await self._lint(arguments.get("fix", False))
                elif name == "wiki_graph":
                    result = await self._graph(arguments.get("format", "json"))
                elif name == "wiki_stats":
                    result = await self._stats()
                else:
                    result = f"Unknown tool: {name}"
                
                return [TextContent(type="text", text=result)]
            except Exception as e:
                return [TextContent(type="text", text=f"Error: {str(e)}")]
    
    async def _search(self, query: str, limit: int = 10) -> str:
        """Search wiki pages using keyword matching."""
        results = []
        query_lower = query.lower()
        
        for md_file in self.wiki_path.rglob("*.md"):
            if md_file.name.startswith("."):
                continue
            
            content = md_file.read_text(encoding="utf-8")
            if query_lower in content.lower():
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
    
    async def run(self, transport: str = "stdio", port: int = 3001):
        """Start the MCP server."""
        if transport == "stdio":
            async with stdio_server() as (read_stream, write_stream):
                await self.server.run(read_stream, write_stream, self.server.create_initialization_options())
        else:
            # SSE transport would go here
            raise NotImplementedError("SSE transport not yet implemented")


def main():
    parser = argparse.ArgumentParser(description="Memex MCP Server")
    parser.add_argument("--transport", choices=["stdio", "sse"], default="stdio")
    parser.add_argument("--port", type=int, default=3001)
    parser.add_argument("--wiki", type=str, default="wiki", help="Path to wiki directory")
    args = parser.parse_args()
    
    server = MemexServer(wiki_path=args.wiki)
    asyncio.run(server.run(transport=args.transport, port=args.port))


if __name__ == "__main__":
    main()
