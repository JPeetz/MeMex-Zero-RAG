# MeMex-Zero-RAG Fix Plan

## Priority & Ordering

### Phase 1 — Ship-stopper fixes (any new user hits these immediately)

| # | Issue | Fix | Why now |
|---|-------|-----|---------|
| 1 | `mcp>=0.9.0` installs v2.x → Server API removed | Pin `mcp>=0.9.0,<2.0` | Server won't start |
| 2 | `.mcp.json` has absolute path | Use `python` or `python3`, remove hardcoded path | MCP config broken |
| 3 | `wiki/` directory missing | Create `wiki/` with starter `index.md` + `log.md` | Server has nothing to serve |
| 4 | No venv guidance in README | Update Quick Start with `python3 -m venv .venv` | Dep pollution, confusion |
| 7 | `.gitignore` missing `.venv/`, `graph/`, `examples/` | Add standard Python ignores | Accidental commits |

### Phase 2 — Infrastructure & polish

| # | Issue | Fix | Why now |
|---|-------|-----|---------|
| 5 | `pyproject.toml` is a stub | Full `[build-system]` + `[project]` + `[project.scripts]` | uv/pip-sync support |
| 6 | Tests can't run | `pip install 'mcp<2.0'` + separate test requirements | No CI validation |
| 8 | `scripts/memex` UX unclear | Add `--help` / setup command | First-run confusion |

## Design Decisions

### 1. requirements.txt — pin `mcp>=0.9.0,<2.0`
- The old Server API (`Server.list_tools()`, `stdio_server`, `SseServerTransport`) is present in `mcp>=0.9.0,<2.0` and removed in `mcp>=2.0`.
- Keep `requirements.txt` as-is for `pip install -r requirements.txt` compat.
- Also declare in `pyproject.toml` under `[project.dependencies]` (Phase 2).

### 2. .mcp.json — portable command
- Replace `"/Users/joergpeetz/workspace/MeMex-Zero-RAG/.venv/bin/python"` with `"python3"`.
- Add `"cwd": "."` so it resolves relative to project root.
- Document that users should `cd` into the project before starting Claude Code.
- Also add `.mcp.json.example` if users need a venv path template.

### 3. wiki/ starter
- Create `wiki/index.md` — minimal master catalog pointing to itself.
- Create `wiki/log.md` — minimal operation log.
- Do NOT populate entities/concepts/... — the LLM builds those from sources. The Quick Start says to drop a source and ask the LLM to ingest it.
- The server already handles empty wiki gracefully (returns empty lists from tools).

### 4. README venv guidance
- Update Step 5 (MCP server): add `python3 -m venv .venv && source .venv/bin/activate && pip install 'mcp>=0.9.0,<2.0'` before `python mcp/server.py`.
- Keep it brief — one extra line in the Quick Start.

### 5. pyproject.toml
- `[build-system]` with `setuptools`.
- `[project]` with name, version, description, license, requires-python.
- `[project.dependencies]` with `mcp>=0.9.0,<2.0`.
- `[project.optional-dependencies]` for dev/test/SSE/search extras.
- `[project.scripts]` with `memex = memex:run` (if we add a package entrypoint).
- `[tool.pytest.ini_options]` — preserve existing.

### 6. Tests runnable
- The conftest.py is already well-designed (handles mcp shadowing via importlib).
- Main blocker: `mcp` not installed in venv.
- Solution: `pip install 'mcp>=0.9.0,<2.0' pytest` is enough to run core tests.
- Create `requirements-test.txt` with only `mcp>=0.9.0,<2.0` and `pytest>=7.4.0`.
- Add test instruction to README.

### 7. .gitignore
- Add: `.venv/`, `graph/`, `*.egg-info/`, `dist/`, `build/`, `.pytest_cache/`, `examples/.mcp_search.db`
- Already has `__pycache__/`, `*.pyc`, `.memex/search.db`

### 8. scripts/memex
- Keep as-is, it works. Add `--help` flag and `setup` command that prints venv + install instructions.
- Document in README's CLI section.

## Implementation Order

1. `.gitignore` (add missing entries)
2. `requirements.txt` (pin mcp)
3. `.mcp.json` (portable command)
4. `wiki/index.md` + `wiki/log.md` (starter)
5. README (venv guidance + test + CLI docs)
6. `pyproject.toml` (full config)
7. `scripts/memex` (--help + setup)
8. `requirements-test.txt` (tests runnable)