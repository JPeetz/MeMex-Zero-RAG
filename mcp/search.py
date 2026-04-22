#!/usr/bin/env python3
# Copyright (c) 2026 Joerg Peetz. All rights reserved.
"""
Hybrid Search for Memex

Combines BM25 keyword search with semantic embeddings for best-of-both-worlds retrieval.
Uses SQLite FTS5 + local embeddings (no external API required).

Usage:
    from search import HybridSearch
    
    search = HybridSearch(wiki_path="wiki")
    search.index()  # Build/update index
    
    results = search.search("machine learning agents", limit=10)
    for r in results:
        print(f"{r['score']:.2f} {r['path']}: {r['snippet']}")

Requires:
    pip install sentence-transformers  # For embeddings
    # Or for smaller/faster:
    pip install fastembed
"""

import json
import os
import re
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple

try:
    from sentence_transformers import SentenceTransformer
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False

try:
    from fastembed import TextEmbedding
    HAS_FASTEMBED = True
except ImportError:
    HAS_FASTEMBED = False

import numpy as np


@dataclass
class SearchResult:
    """Single search result."""
    path: str
    title: str
    snippet: str
    bm25_score: float
    semantic_score: float
    combined_score: float
    page_type: str


class HybridSearch:
    """
    Hybrid BM25 + semantic search over wiki pages.
    
    Stores:
    - SQLite FTS5 index for BM25
    - Embeddings in SQLite BLOB columns
    - Page metadata and content
    """
    
    def __init__(
        self,
        wiki_path: str = "wiki",
        db_path: str = ".memex/search.db",
        model_name: str = "all-MiniLM-L6-v2",
        bm25_weight: float = 0.4,
        semantic_weight: float = 0.6
    ):
        self.wiki_path = Path(wiki_path)
        self.db_path = Path(db_path)
        self.model_name = model_name
        self.bm25_weight = bm25_weight
        self.semantic_weight = semantic_weight
        
        self._model = None
        self._db = None
        
        # Ensure db directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
    
    @property
    def model(self):
        """Lazy-load embedding model."""
        if self._model is None:
            if HAS_FASTEMBED:
                self._model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
            elif HAS_SENTENCE_TRANSFORMERS:
                self._model = SentenceTransformer(self.model_name)
            else:
                raise ImportError("No embedding library found. Install: pip install sentence-transformers")
        return self._model
    
    @property
    def db(self) -> sqlite3.Connection:
        """Get database connection."""
        if self._db is None:
            self._db = sqlite3.connect(str(self.db_path))
            self._db.row_factory = sqlite3.Row
            self._init_db()
        return self._db
    
    def _init_db(self):
        """Initialize database schema."""
        self.db.executescript("""
            -- Main pages table
            CREATE TABLE IF NOT EXISTS pages (
                id INTEGER PRIMARY KEY,
                path TEXT UNIQUE NOT NULL,
                title TEXT,
                page_type TEXT,
                content TEXT,
                embedding BLOB,
                indexed_at TEXT,
                file_mtime REAL
            );
            
            -- FTS5 virtual table for BM25 search
            CREATE VIRTUAL TABLE IF NOT EXISTS pages_fts USING fts5(
                path,
                title,
                content,
                content='pages',
                content_rowid='id'
            );
            
            -- Triggers to keep FTS in sync
            CREATE TRIGGER IF NOT EXISTS pages_ai AFTER INSERT ON pages BEGIN
                INSERT INTO pages_fts(rowid, path, title, content)
                VALUES (new.id, new.path, new.title, new.content);
            END;
            
            CREATE TRIGGER IF NOT EXISTS pages_ad AFTER DELETE ON pages BEGIN
                INSERT INTO pages_fts(pages_fts, rowid, path, title, content)
                VALUES ('delete', old.id, old.path, old.title, old.content);
            END;
            
            CREATE TRIGGER IF NOT EXISTS pages_au AFTER UPDATE ON pages BEGIN
                INSERT INTO pages_fts(pages_fts, rowid, path, title, content)
                VALUES ('delete', old.id, old.path, old.title, old.content);
                INSERT INTO pages_fts(rowid, path, title, content)
                VALUES (new.id, new.path, new.title, new.content);
            END;
            
            -- Index metadata
            CREATE TABLE IF NOT EXISTS index_meta (
                key TEXT PRIMARY KEY,
                value TEXT
            );
        """)
        self.db.commit()
    
    def _embed(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for texts."""
        if HAS_FASTEMBED:
            # fastembed returns generator
            embeddings = list(self.model.embed(texts))
            return np.array(embeddings)
        else:
            # sentence-transformers
            return self.model.encode(texts, show_progress_bar=False)
    
    def _extract_metadata(self, content: str, path: Path) -> Tuple[str, str]:
        """Extract title and type from page content."""
        title = path.stem.replace("-", " ").title()
        page_type = "other"
        
        # Extract from frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                
                title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', frontmatter, re.MULTILINE)
                if title_match:
                    title = title_match.group(1)
                
                type_match = re.search(r'^type:\s*(\w+)', frontmatter, re.MULTILINE)
                if type_match:
                    page_type = type_match.group(1)
        
        # Infer from path
        if page_type == "other":
            parts = path.relative_to(self.wiki_path).parts
            if len(parts) > 1 and parts[0] in ["sources", "entities", "concepts", "synthesis"]:
                page_type = parts[0].rstrip("s")  # sources -> source
        
        return title, page_type
    
    def index(self, force: bool = False) -> dict:
        """
        Index all wiki pages.
        
        Args:
            force: Re-index all pages even if unchanged
            
        Returns:
            Stats dict with indexed/skipped/removed counts
        """
        stats = {"indexed": 0, "skipped": 0, "removed": 0}
        
        # Get existing pages
        existing = {row["path"]: row["file_mtime"] for row in 
                   self.db.execute("SELECT path, file_mtime FROM pages").fetchall()}
        
        current_paths = set()
        pages_to_index = []
        
        # Scan wiki directory
        for md_file in self.wiki_path.rglob("*.md"):
            if md_file.name.startswith("."):
                continue
            
            rel_path = str(md_file.relative_to(self.wiki_path))
            current_paths.add(rel_path)
            
            mtime = md_file.stat().st_mtime
            
            # Skip if unchanged
            if not force and rel_path in existing and existing[rel_path] == mtime:
                stats["skipped"] += 1
                continue
            
            content = md_file.read_text(encoding="utf-8")
            title, page_type = self._extract_metadata(content, md_file)
            
            pages_to_index.append({
                "path": rel_path,
                "title": title,
                "page_type": page_type,
                "content": content,
                "mtime": mtime
            })
        
        # Generate embeddings in batch
        if pages_to_index:
            texts = [f"{p['title']}\n\n{p['content']}" for p in pages_to_index]
            embeddings = self._embed(texts)
            
            for page, embedding in zip(pages_to_index, embeddings):
                self.db.execute("""
                    INSERT OR REPLACE INTO pages (path, title, page_type, content, embedding, indexed_at, file_mtime)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    page["path"],
                    page["title"],
                    page["page_type"],
                    page["content"],
                    embedding.tobytes(),
                    datetime.now().isoformat(),
                    page["mtime"]
                ))
                stats["indexed"] += 1
        
        # Remove deleted pages
        for path in existing:
            if path not in current_paths:
                self.db.execute("DELETE FROM pages WHERE path = ?", (path,))
                stats["removed"] += 1
        
        # Update metadata
        self.db.execute("""
            INSERT OR REPLACE INTO index_meta (key, value)
            VALUES ('last_indexed', ?)
        """, (datetime.now().isoformat(),))
        
        self.db.commit()
        return stats
    
    def search(
        self,
        query: str,
        limit: int = 10,
        page_types: Optional[List[str]] = None
    ) -> List[SearchResult]:
        """
        Hybrid search combining BM25 and semantic similarity.
        
        Args:
            query: Search query
            limit: Max results
            page_types: Filter by types (source, entity, concept, synthesis)
            
        Returns:
            List of SearchResult ordered by combined score
        """
        # BM25 search
        bm25_results = {}
        fts_query = query.replace('"', '""')  # Escape quotes
        
        rows = self.db.execute("""
            SELECT p.path, p.title, p.page_type, p.content, p.embedding,
                   bm25(pages_fts) as bm25_score
            FROM pages_fts f
            JOIN pages p ON f.rowid = p.id
            WHERE pages_fts MATCH ?
            ORDER BY bm25_score
            LIMIT ?
        """, (fts_query, limit * 2)).fetchall()
        
        for row in rows:
            bm25_results[row["path"]] = {
                "title": row["title"],
                "page_type": row["page_type"],
                "content": row["content"],
                "embedding": np.frombuffer(row["embedding"], dtype=np.float32),
                "bm25_score": -row["bm25_score"]  # BM25 returns negative
            }
        
        # Semantic search
        query_embedding = self._embed([query])[0]
        
        semantic_results = {}
        rows = self.db.execute("SELECT path, title, page_type, content, embedding FROM pages").fetchall()
        
        for row in rows:
            embedding = np.frombuffer(row["embedding"], dtype=np.float32)
            similarity = np.dot(query_embedding, embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(embedding)
            )
            semantic_results[row["path"]] = {
                "title": row["title"],
                "page_type": row["page_type"],
                "content": row["content"],
                "semantic_score": float(similarity)
            }
        
        # Combine scores
        all_paths = set(bm25_results.keys()) | set(semantic_results.keys())
        combined = []
        
        # Normalize BM25 scores
        if bm25_results:
            max_bm25 = max(r["bm25_score"] for r in bm25_results.values())
            min_bm25 = min(r["bm25_score"] for r in bm25_results.values())
            bm25_range = max_bm25 - min_bm25 if max_bm25 != min_bm25 else 1
        
        for path in all_paths:
            bm25_data = bm25_results.get(path, {})
            semantic_data = semantic_results.get(path, {})
            
            # Normalize BM25 to 0-1
            bm25_score = bm25_data.get("bm25_score", 0)
            if bm25_results:
                bm25_norm = (bm25_score - min_bm25) / bm25_range
            else:
                bm25_norm = 0
            
            semantic_score = semantic_data.get("semantic_score", 0)
            
            # Combined score
            combined_score = (
                self.bm25_weight * bm25_norm +
                self.semantic_weight * semantic_score
            )
            
            # Get metadata
            data = bm25_data or semantic_data
            page_type = data.get("page_type", "other")
            
            # Filter by type
            if page_types and page_type not in page_types:
                continue
            
            # Generate snippet
            content = data.get("content", "")
            snippet = self._generate_snippet(content, query)
            
            combined.append(SearchResult(
                path=path,
                title=data.get("title", path),
                snippet=snippet,
                bm25_score=bm25_score,
                semantic_score=semantic_score,
                combined_score=combined_score,
                page_type=page_type
            ))
        
        # Sort by combined score
        combined.sort(key=lambda x: x.combined_score, reverse=True)
        return combined[:limit]
    
    def _generate_snippet(self, content: str, query: str, context: int = 150) -> str:
        """Generate snippet with query context."""
        # Remove frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                content = parts[2]
        
        content = content.strip()
        query_lower = query.lower()
        
        # Find best match position
        idx = content.lower().find(query_lower)
        if idx == -1:
            # Try individual words
            for word in query.split():
                idx = content.lower().find(word.lower())
                if idx != -1:
                    break
        
        if idx == -1:
            # Return beginning
            snippet = content[:context * 2]
        else:
            start = max(0, idx - context)
            end = min(len(content), idx + len(query) + context)
            snippet = content[start:end]
        
        # Clean up
        snippet = snippet.replace("\n", " ").strip()
        if len(snippet) > context * 2:
            snippet = snippet[:context * 2]
        
        # Add ellipsis
        if not content.startswith(snippet):
            snippet = "..." + snippet
        if not content.endswith(snippet):
            snippet = snippet + "..."
        
        return snippet
    
    def get_stats(self) -> dict:
        """Get index statistics."""
        row = self.db.execute("SELECT COUNT(*) as count FROM pages").fetchone()
        page_count = row["count"]
        
        types = self.db.execute("""
            SELECT page_type, COUNT(*) as count 
            FROM pages 
            GROUP BY page_type
        """).fetchall()
        
        last_indexed = self.db.execute("""
            SELECT value FROM index_meta WHERE key = 'last_indexed'
        """).fetchone()
        
        return {
            "total_pages": page_count,
            "by_type": {r["page_type"]: r["count"] for r in types},
            "last_indexed": last_indexed["value"] if last_indexed else None,
            "db_size_kb": self.db_path.stat().st_size // 1024 if self.db_path.exists() else 0
        }
    
    def close(self):
        """Close database connection."""
        if self._db:
            self._db.close()
            self._db = None


def main():
    """CLI for hybrid search."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Memex hybrid search")
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument("--index", "-i", action="store_true", help="Rebuild index")
    parser.add_argument("--force", "-f", action="store_true", help="Force full reindex")
    parser.add_argument("--stats", "-s", action="store_true", help="Show index stats")
    parser.add_argument("--limit", "-l", type=int, default=10, help="Max results")
    parser.add_argument("--wiki", "-w", type=str, default="wiki", help="Wiki path")
    args = parser.parse_args()
    
    search = HybridSearch(wiki_path=args.wiki)
    
    if args.index or args.force:
        print("🔄 Indexing wiki...")
        stats = search.index(force=args.force)
        print(f"✅ Indexed: {stats['indexed']}, Skipped: {stats['skipped']}, Removed: {stats['removed']}")
    
    if args.stats:
        stats = search.get_stats()
        print(f"\n📊 Index Statistics:")
        print(f"   Total pages: {stats['total_pages']}")
        print(f"   By type: {stats['by_type']}")
        print(f"   Last indexed: {stats['last_indexed']}")
        print(f"   DB size: {stats['db_size_kb']} KB")
    
    if args.query:
        results = search.search(args.query, limit=args.limit)
        if not results:
            print(f"No results for: {args.query}")
        else:
            print(f"\n🔍 Results for '{args.query}':\n")
            for r in results:
                print(f"[{r.combined_score:.2f}] {r.path}")
                print(f"        {r.snippet}")
                print()
    
    search.close()


if __name__ == "__main__":
    main()
