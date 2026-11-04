#!/usr/bin/env python3
"""
Search-backend abstraction for Memex.

Markdown + git remain the single source of truth for every wiki page. The
search layer is a selectable SQL engine built by indexing that markdown:
  - "sqlite"   -> SQLite FTS5 + BLOB embeddings (local, memex_mcp/search.py)
  - "postgres" -> PostgreSQL + pgvector (enterprise, memex_mcp/pg_backend.py)

This lets the CLI `--search-backend` flag actually select an engine and keeps
the zero-RAG wiki workflow unchanged — SQL accelerates search, it never owns
the knowledge.

drivers are loaded lazily; if a required client library (psycopg) is missing,
the factory degrades gracefully to the SQLite engine and returns a warning so
the server can log the degradation instead of crashing.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple


class SearchEngine:
    """Duck-typed interface every backend implements.

    `search()` returns a list of results each exposing `.path`, `.title`,
    `.snippet`, `.score` and `.page_type` (both the SQLite `SearchResult` and
    the Postgres `PGSearchResult` provide these). Markdown remains the truth;
    the engine is purely a queryable index.
    """

    name: str = "base"

    def index(self, force: bool = False) -> dict:
        raise NotImplementedError

    def search(self, query: str, limit: int = 10,
               page_types: Optional[List[str]] = None) -> list:
        raise NotImplementedError

    def get_stats(self) -> dict:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError


def get_backend(name: str, wiki_path: str,
                **kwargs) -> Tuple[SearchEngine, Optional[str]]:
    """Factory: return (engine, warning_or_None).

    Never raises for a missing client lib — returns the SQLite fallback with a
    warning string so the server can log the degradation instead of dying.
    """
    if name == "sqlite":
        from memex_mcp.search import HybridSearch
        return HybridSearch(wiki_path=wiki_path), None

    if name in ("postgres", "supabase"):
        try:
            import psycopg  # noqa: F401  import-time probe
        except ImportError as exc:
            return _sqlite_fallback(wiki_path), (
                f"postgres/supabase backend requested but 'psycopg' is not "
                f"installed; fell back to sqlite. Install: pip install "
                f"'psycopg[binary]' ({exc})"
            )
        from memex_mcp.pg_backend import PostgresSearchEngine
        dsn = kwargs.get("pg_dsn") or kwargs.get("supabase_url")
        if not dsn:
            return _sqlite_fallback(wiki_path), (
                "postgres/supabase backend requested but no --pg-dsn / "
                "connection URL provided; fell back to sqlite."
            )
        eng = PostgresSearchEngine(wiki_path=wiki_path, dsn=dsn)
        try:
            eng.ping()
        except Exception as exc:
            eng.close()
            return _sqlite_fallback(wiki_path), (
                f"postgres/supabase backend unreachable ({exc}); fell back to sqlite."
            )
        return eng, None

    # Unknown backend -> safe SQLite default.
    return _sqlite_fallback(wiki_path), (
        f"unknown search backend '{name}'; using sqlite."
    )


def _sqlite_fallback(wiki_path: str) -> SearchEngine:
    from memex_mcp.search import HybridSearch
    return HybridSearch(wiki_path=wiki_path)