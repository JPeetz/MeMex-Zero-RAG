#!/usr/bin/env python3
"""
PostgreSQL + pgvector search engine for Memex (enterprise backend).

Mirrors the SQLite `HybridSearch` interface (index / search / get_stats / close)
so the server can treat it identically to the local engine. Markdown + git stay
the source of truth; Postgres is a queryable index built from that markdown.

Schema matches the enterprise learning-store pattern: a `pages` relation + a
pgvector embedding column (semantic recall) + a tsvector column (keyword rank).

Requires:  pip install 'psycopg[binary]'  and  Postgres running with pgvector.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

try:
    import psycopg
    from psycopg.rows import dict_row
    HAS_PSYCOPG = True
except ImportError:  # pragma: no cover - backend factory guards this
    psycopg = None
    HAS_PSYCOPG = False

try:
    from sentence_transformers import SentenceTransformer
    _model_backend = "sentence-transformers"
except ImportError:
    SentenceTransformer = None
    _model_backend = None

import numpy as np


@dataclass
class PGSearchResult:
    path: str
    title: str
    snippet: str
    score: float
    page_type: str

    @property
    def combined_score(self) -> float:
        return self.score


class PostgresSearchEngine:
    name = "postgres"

    def __init__(self, wiki_path: str = "wiki", dsn: str = "",
                 model_name: str = "all-MiniLM-L6-v2",
                 table: str = "mcp_pages", bm25_weight: float = 0.4,
                 semantic_weight: float = 0.6, embed_dim: int = 384):
        self.wiki_path = Path(wiki_path)
        self.dsn = dsn
        self.model_name = model_name
        self.table = table
        self.bm25_weight = bm25_weight
        self.semantic_weight = semantic_weight
        self.embed_dim = embed_dim
        self._conn = None
        self._model = None

    # ── connectivity ────────────────────────────────────────────────
    @property
    def conn(self):
        if self._conn is None or self._conn.closed:
            self._conn = psycopg.connect(self.dsn, row_factory=dict_row)
            self._conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
            self._init_db()
        return self._conn

    def ping(self) -> None:
        """Ensure the DB is reachable (called by the factory before use)."""
        self.conn.execute("SELECT 1")

    def close(self) -> None:
        if self._conn and not self._conn.closed:
            self._conn.close()
        self._conn = None

    def _init_db(self) -> None:
        self.conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.table} (
                id        SERIAL PRIMARY KEY,
                path      TEXT UNIQUE NOT NULL,
                title     TEXT,
                page_type TEXT,
                content   TEXT NOT NULL,
                body_tsv  tsvector GENERATED ALWAYS AS
                          (to_tsvector('english', content)) STORED,
                embedding vector({self.embed_dim}),
                indexed_at TEXT,
                file_mtime DOUBLE PRECISION
            )
        """)
        self.conn.execute(f"""
            CREATE INDEX IF NOT EXISTS {self.table}_tsv_idx
              ON {self.table} USING gin (body_tsv)
        """)
        self.conn.execute(f"""
            CREATE INDEX IF NOT EXISTS {self.table}_embed_idx
              ON {self.table} USING hnsw (embedding vector_cosine_ops)
        """)
        self.conn.commit()

    @property
    def model(self):
        """Lazy embedding model — same families as the SQLite engine."""
        if self._model is None and _model_backend is not None:
            self._model = SentenceTransformer(self.model_name) \
                if _model_backend == "sentence-transformers" else None
        return self._model

    def _embed(self, texts: List[str]) -> Optional["np.ndarray"]:
        if self.model is None:
            return None
        return self.model.encode(texts, show_progress_bar=False).astype(np.float32)

    # ── indexing (markdown is the source of truth) ─────────────────
    def index(self, force: bool = False) -> dict:
        stats = {"indexed": 0, "skipped": 0, "removed": 0}
        existing = dict(self.conn.execute(
            f"SELECT path, file_mtime FROM {self.table}").fetchall())

        current_paths = set()
        pages = []
        for md_file in self.wiki_path.rglob("*.md"):
            if md_file.name.startswith("."):
                continue
            rel = str(md_file.relative_to(self.wiki_path))
            current_paths.add(rel)
            mtime = md_file.stat().st_mtime
            if not force and rel in existing and existing[rel] == mtime:
                stats["skipped"] += 1
                continue
            content = md_file.read_text(encoding="utf-8")
            title, page_type = self._extract_metadata(content, md_file)
            pages.append((rel, title, page_type, content, mtime))

        if pages:
            texts = [f"{t}\n\n{c}" for _, t, _, c, _ in pages]
            embeds = self._embed(texts)
            embeds_list = ([[float(x) for x in v] for v in embeds]
                           if embeds is not None
                           else [[0.0] * self.embed_dim for _ in pages])
            for i, (rel, title, pt, content, mtime) in enumerate(pages):
                self.conn.execute(
                    f"INSERT INTO {self.table} (path,title,page_type,content,embedding,indexed_at,file_mtime) "
                    f"VALUES (%s,%s,%s,%s,%s,%s,%s) "
                    f"ON CONFLICT (path) DO UPDATE SET title=EXCLUDED.title, "
                    f"page_type=EXCLUDED.page_type, content=EXCLUDED.content, "
                    f"embedding=EXCLUDED.embedding, indexed_at=EXCLUDED.indexed_at, "
                    f"file_mtime=EXCLUDED.file_mtime",
                    (rel, title, pt, content, embeds_list[i], datetime.now().isoformat(), mtime))
                stats["indexed"] += 1

        for path in existing:
            if path not in current_paths:
                self.conn.execute(f"DELETE FROM {self.table} WHERE path=%s", (path,))
                stats["removed"] += 1

        self.conn.commit()
        return stats

    def _extract_metadata(self, content: str, path: Path) -> Tuple[str, str]:
        title = path.stem.replace("-", " ").title()
        page_type = "other"
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                fm = parts[1]
                m = re.search(r"^title:\s*[\"']?(.+?)[\"']?\s*$", fm, re.MULTILINE)
                if m:
                    title = m.group(1)
                m = re.search(r"^type:\s*(\w+)", fm, re.MULTILINE)
                if m:
                    page_type = m.group(1)
        if page_type == "other":
            parts = path.relative_to(self.wiki_path).parts
            if len(parts) > 1 and parts[0] in ("sources", "entities", "concepts", "synthesis"):
                page_type = parts[0].rstrip("s")
        return title, page_type

    # ── search ─────────────────────────────────────────────────────
    def search(self, query: str, limit: int = 10,
               page_types: Optional[List[str]] = None) -> List[PGSearchResult]:
        """Hybrid: normalize ts_rank (keyword) + pgvector cosine (semantic)."""
        # Keyword scores (ts_rank_cd), best picked here / refined in memory.
        rows = self.conn.execute(
            f"""
            SELECT path, title, page_type, content,
                   ts_rank_cd(body_tsv, plainto_tsquery('english', %s)) AS kw
            FROM {self.table}
            WHERE body_tsv @@ plainto_tsquery('english', %s)
               OR embedding IS NOT NULL
            ORDER BY kw DESC
            LIMIT %s
            """, (query, query, limit * 3)).fetchall()

        # Semantic scores: cosine similarity via pgvector (<#> = -cosine).
        sem = {}
        if self.model is not None:
            emb = self._embed([query])
            if emb is not None:
                vec = [float(x) for x in emb[0]]
                srows = self.conn.execute(
                    f"SELECT path, 1 - (embedding <#> %s::vector) AS sim "
                    f"FROM {self.table} WHERE embedding IS NOT NULL ORDER BY sim DESC LIMIT %s",
                    (vec, limit * 3)).fetchall()
                sem = {r["path"]: float(r["sim"]) for r in srows}

        results = []
        for r in rows:
            kw = float(r["kw"] or 0)
            sim = sem.get(r["path"], 0.0)
            score = self.bm25_weight * kw + self.semantic_weight * sim
            if score <= 0 and not (kw or sim):
                continue
            if page_types and r["page_type"] not in page_types:
                continue
            results.append(PGSearchResult(
                path=r["path"], title=r["title"], snippet=self._snippet(r["content"], query),
                score=round(score, 5), page_type=r["page_type"]))

        results.sort(key=lambda x: x.score, reverse=True)
        return results[:limit]

    def _snippet(self, content: str, query: str, context: int = 150) -> str:
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                content = parts[2]
        content = content.strip()
        ql = query.lower()
        idx = content.lower().find(ql)
        if idx == -1:
            idx = 0
        start = max(0, idx - context)
        end = min(len(content), idx + len(query) + context)
        snippet = content[start:end].replace("\n", " ").strip()
        if start > 0:
            snippet = "..." + snippet
        if end < len(content):
            snippet = snippet + "..."
        return snippet

    def get_stats(self) -> dict:
        row = self.conn.execute(
            f"SELECT COUNT(*) AS n, COUNT(embedding) AS with_embed FROM {self.table}").fetchone()
        by_type = dict(self.conn.execute(
            f"SELECT page_type, COUNT(*) FROM {self.table} GROUP BY page_type").fetchall())
        return {
            "total_pages": row["n"], "by_type": by_type,
            "with_embedding": row["with_embed"], "backend": "postgres",
        }


def main() -> None:
    import argparse
    parser = argparse.ArgumentParser(description="Memex Postgres/pgvector search")
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument("--index", "-i", action="store_true", help="Rebuild index")
    parser.add_argument("--force", "-f", action="store_true", help="Force full reindex")
    parser.add_argument("--stats", "-s", action="store_true", help="Show stats")
    parser.add_argument("--limit", "-l", type=int, default=10)
    parser.add_argument("--wiki", "-w", type=str, default="wiki")
    parser.add_argument("--dsn", "-d", type=str, default=os.environ.get("MEMEX_PG_DSN", ""),
                        help="Postgres connection string")
    args = parser.parse_args()

    if not args.dsn:
        print("❌ --dsn / MEMEX_PG_DSN required for the postgres backend")
        return
    eng = PostgresSearchEngine(wiki_path=args.wiki, dsn=args.dsn)
    if args.index or args.force:
        print("🔄 Indexing wiki into Postgres...")
        s = eng.index(force=args.force)
        print(f"✅ Indexed: {s['indexed']}, Skipped: {s['skipped']}, Removed: {s['removed']}")
    if args.stats:
        print(f"\n📊 {eng.get_stats()}")
    if args.query:
        for r in eng.search(args.query, limit=args.limit):
            print(f"[{r.score:.3f}] {r.path}\n        {r.snippet}\n")
    eng.close()


if __name__ == "__main__":
    main()