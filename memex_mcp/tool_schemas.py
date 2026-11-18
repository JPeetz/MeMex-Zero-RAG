"""MCP tool schemas, kept as data rather than buried inside a handler.

Extracted from MemexServer._setup_tools because a tool schema is a *contract*:

  * a change to any description or inputSchema now shows up as a small, reviewable diff —
    a changed schema is a security event (rug pull), not a version bump;
  * the set can be hashed and compared across releases;
  * the handler stays about behaviour instead of ~260 lines of JSON Schema.
"""

from mcp.types import Tool


def build_tools(enable_graph: bool = False) -> list[Tool]:
    """All advertised tools. wiki_graph is conditional on --enable-graph."""
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
        ) if enable_graph else None
    ]
