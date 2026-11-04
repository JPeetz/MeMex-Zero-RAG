#!/usr/bin/env python3
"""Apply Section 4: wiki_confidence tool + search.py graceful import + SCHEMA.md update."""
import re

# ============================================================
# 1. SERVER.PY — Add wiki_confidence tool definition
# ============================================================
server_path = "mcp/server.py"
with open(server_path) as f:
    content = f.read()

# 1a. Tool definition: insert after wiki_stats tool block, before wiki_write
tool_def_marker = '                Tool(\n                    name="wiki_write",'
tool_def_insert = '''                Tool(
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
'''
if 'name="wiki_confidence"' not in content and tool_def_marker in content:
    content = content.replace(tool_def_marker, tool_def_insert + tool_def_marker)
    print("✅ Tool definition added")
elif 'name="wiki_confidence"' in content:
    print("⚠️ Tool definition already present")
else:
    print("❌ Could not find tool_def_marker")

# 1b. Tool handler: insert after wiki_stats handler, before wiki_write handler
handler_marker = '                elif name == "wiki_write":'
handler_insert = '''                elif name == "wiki_confidence":
                    result = await self._confidence(arguments.get("page", None))
'''
if '_confidence(' not in content and handler_marker in content:
    content = content.replace(handler_marker, handler_insert + handler_marker)
    print("✅ Tool handler added")
elif '_confidence(' in content:
    print("⚠️ Tool handler already present")
else:
    print("❌ Could not find handler_marker")

# 1c. _confidence method: insert after _stats method (after "Run wiki_lint for detailed health check.")
stats_end_marker = 'Run `wiki_lint` for detailed health check.\n"""'
confidence_method = '''
    
    async def _confidence(self, page: str = None) -> str:
        """Analyze wiki confidence: distribution, stale pages, contradictions."""
        try:
            from memex_mcp.confidence import ConfidenceAnalyzer
            analyzer = ConfidenceAnalyzer(str(self.wiki_path))
            stats = analyzer.analyze()

            output = "# Wiki Confidence Report\\n\\n"
            output += f"**Total pages analyzed:** {stats.get('total_pages', 0)}\\n\\n"
            output += "## Confidence Distribution\\n"
            output += "| Level | Count |\\n|-------|-------|\\n"
            for level in ["high", "medium", "low", "uncertain"]:
                output += f"| {level} | {stats.get(level, 0)} |\\n"
            output += f"\\n**Stale pages (>90 days unverified):** {stats.get('stale', 0)}\\n"
            output += f"**With contradictions:** {stats.get('with_contradictions', 0)}\\n"

            if page:
                pages = stats.get('pages', {})
                if page in pages:
                    p = pages[page]
                    output += f"\\n## Page: {page}\\n"
                    output += f"- Confidence: {p.get('confidence', 'unknown')}\\n"
                    output += f"- Verified: {p.get('verified', 'never')}\\n"
                    output += f"- Contradictions: {p.get('has_contradictions', False)}\\n"
                else:
                    output += f"\\nPage '{page}' not found in wiki.\\n"

            return output
        except ImportError:
            return "Confidence analysis requires mcp.confidence module (install dependencies)."
        except Exception as e:
            return f"Confidence analysis error: {e}"
'''
if 'async def _confidence' not in content and stats_end_marker in content:
    content = content.replace(stats_end_marker, stats_end_marker + confidence_method)
    print("✅ _confidence method added")
elif 'async def _confidence' in content:
    print("⚠️ _confidence method already present")
else:
    print("❌ Could not find stats_end_marker")

with open(server_path, "w") as f:
    f.write(content)

# ============================================================
# 2. SEARCH.PY — Add graceful ImportError for sentence-transformers
# ============================================================
search_path = "mcp/search.py"
with open(search_path) as f:
    search_content = f.read()

# Check top-level import of sentence_transformers
if "from sentence_transformers import SentenceTransformer" in search_content:
    # Wrap in try/except to make it optional
    old_import = "from sentence_transformers import SentenceTransformer"
    new_import = "try:\n    from sentence_transformers import SentenceTransformer\n    _sentence_transformers_available = True\nexcept ImportError:\n    SentenceTransformer = None\n    _sentence_transformers_available = False"
    search_content = search_content.replace(old_import, new_import)
    
    # Also guard usage of SentenceTransformer
    if "SentenceTransformer(" in search_content:
        search_content = search_content.replace(
            "SentenceTransformer(",
            "SentenceTransformer("
        )
        # Add a check where SentenceTransformer is used
        old_usage = "self.model = SentenceTransformer("
        if old_usage in search_content:
            new_usage = "if SentenceTransformer is not None:\n            self.model = SentenceTransformer("
            search_content = search_content.replace(old_usage, new_usage)
    
    with open(search_path, "w") as f:
        f.write(search_content)
    print("✅ search.py: graceful ImportError added")
else:
    print("⚠️ No direct SentenceTransformer import in search.py")

# ============================================================
# 3. SCHEMA.md — Document L1/ setup step
# ============================================================
schema_path = "SCHEMA.md"
with open(schema_path) as f:
    schema_content = f.read()

l1_doc = """

## L1/ — Private Context Setup

The `L1/` directory holds per-install private context (credentials, identity, rules).
It is git-ignored. To set up:

1. Copy the example templates:
   ```bash
   cp L1/credentials.md.example L1/credentials.md
   cp L1/identity.md.example L1/identity.md
   cp L1/rules.md.example L1/rules.md
   ```

2. Fill in your values in each `.md` file.

3. Verify the files are ignored by git:
   ```bash
   git status --short L1/
   ```
   (Should show nothing — the `.md` files are excluded by `.gitignore`.)

**Never commit `L1/*.md` files.** The `.example` templates are tracked; your filled-in
copies are not.
"""

# Insert after any existing L1 section or before Quick Start
if "L1/ — Private Context" not in schema_content:
    # Insert before "## Directory Structure" or at end
    dir_struct = '## Directory Structure'
    if dir_struct in schema_content:
        schema_content = schema_content.replace(dir_struct, l1_doc + "\n" + dir_struct)
    else:
        schema_content += l1_doc
    
    with open(schema_path, "w") as f:
        f.write(schema_content)
    print("✅ SCHEMA.md: L1/ setup documented")
else:
    print("⚠️ SCHEMA.md already has L1/ documentation")

print("\n=== DONE ===")
