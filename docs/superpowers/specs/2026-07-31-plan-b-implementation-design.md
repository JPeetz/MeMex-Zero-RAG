# MeMex Zero-RAG — Plan B Implementation Design

**Date:** 2026-07-31
**Context:** Agent Memory Atlas audit of MeMex Zero-RAG identified gaps between README claims and code enforcement.
**Scope:** Sections 1-4 (Quick wins + trust). Sections 5-6 (tombstones, conflict gate) deferred for later review.

## Background

The [Agent Memory Atlas](https://neoneye.github.io/agent-memory-atlas/systems/memex-zero-rag/) reviewed MeMex Zero-RAG at commit `e2a1ec7`. Key finding: "Every gap is the same gap — an invariant expressed as a sentence to a model rather than a check in a code path."

Three of four advertised features had no code enforcement. Search was unranked substring matching that degrades as the wiki grows. A hybrid BM25+dense searcher existed in `memex_mcp/search.py` (505 lines, complete) but was never imported by `memex_mcp/server.py`.

## Section 1: L1/ Credentials Security Fix

### Problem
`.gitignore` contains `L1/` but `L1/credentials.md`, `L1/identity.md`, and `L1/rules.md` are tracked in git. A downstream user who clones the repo, fills in credentials, and pushes their fork commits their API keys — despite `credentials.md` explicitly stating "NEVER commit credentials."

### Design
- `git rm --cached` all three L1/ files
- Ship as `L1/*.md.example` templates
- Add `L1/*.md` pattern to `.gitignore`
- Document the copy step in `SCHEMA.md`

### Impact
Zero code changes. 4 git commands. Eliminates the "finding that can cost a reader something."

## Section 2: Citation Enforcement + Operation Log + Honest Commits

### Problem
- "Zero hallucination enforcement" is a manual substring report (`wiki_lint`) whose fix mode returns `[AUTO-FIX NOT YET IMPLEMENTED]`, never runs automatically
- `wiki/log.md` exists but no code appends to it — only a text instruction to the model
- `wiki_write` returns `✅ Written` even when git commit fails

### Design

**2a. Citation enforcement in `wiki_write` (server.py)**
Before writing a page, check content contains `[Source: ...]`. Skip check for:
- Pages under `wiki/sources/` (they ARE sources, not derived claims)
- Pages named `index.md` or `log.md`
- Pages under `wiki/log.md`, `wiki/index.md`, `wiki/contradictions.md`

On failure: return `❌ Rejected: page has no [Source: ...] citation. Every wiki page must cite at least one source.`

**2b. Operation log in `wiki_write`**
After successful write, append to `wiki/log.md`:
```
- YYYY-MM-DD: wrote <page_type>/<slug>.md (agent: <agent>)
```
Code does the logging, not the model.

**2c. Honest commit status**
Change:
```python
return f"✅ Written: {page_type}/{slug}.md (git commit failed: {result.stderr.strip()})"
```
To:
```python
return f"⚠️ Written to disk but git commit failed: {result.stderr.strip()}. Run 'git commit' manually."
```

### Impact
~25 lines in `server.py:_write`. No new files, no new dependencies.

## Section 3: Wire Hybrid Searcher

### Problem
`_search` in `server.py` is 15 lines of unranked substring matching. Results arrive in `Path.rglob` order, with an early break at `limit`. As the wiki grows, recall degrades — the opposite of "knowledge compounds."

`memex_mcp/search.py` (505 lines) contains a complete hybrid BM25 + dense embedding searcher with cosine similarity over BAAI/bge-small-en-v1.5. It is documented, working, and never imported.

### Design

**Fallback chain, not replacement:**

```
Tier 1 (hybrid): Import HybridSearcher from mcp.search
  → Lazy init on first call, cached as self._hybrid_searcher
  → BM25 score + cosine similarity, ranked results
  → Falls back to Tier 2 if: import fails, index build fails, no sentence-transformers

Tier 2 (substring): Current _search implementation
  → Unchanged, kept as the floor
```

**Why both arms?** The "Zero-RAG — No Embeddings" banner is honest about the default path. The hybrid path is an opt-in upgrade — install `sentence-transformers`, get ranked search. No dependency required.

**Changes:**
- `server.py:_search`: lazy import `HybridSearcher`, two-tier dispatch, ~15 lines
- `memex_mcp/search.py`: graceful ImportError on missing `sentence-transformers`, accept `wiki_dir` param, ~5 lines

### Impact
~20 lines total. Search goes from "first 10 hits in directory order" to "BM25 + semantic ranked" when embeddings are available.

## Section 4: Confidence-Aware Retrieval

### Problem
`mcp/confidence.py` (407 lines) parses `[confidence: high|medium|low|uncertain]` tags, weights them, flags stale pages (>90 days unverified), detects contradictions. It has a CLI `main()` and no caller in the tree. Confidence levels exist in the data model but nothing on the read path consults them.

### Design

**4a. Confidence filter in `wiki_search`**
New parameter: `min_confidence` (default: `"low"`).
Post-retrieval filter: parse confidence from each result page, strip any below threshold.
- `"high"` → only high-confidence pages
- `"medium"` → medium and above
- `"low"` → all except uncertain (default)
- None → all pages unfiltered

**4b. New MCP tool: `wiki_confidence`**
Runs `ConfidenceAnalyzer` on the wiki, returns:
- Distribution: high/medium/low/uncertain counts
- Stale pages: anything unverified >90 days
- Contradiction count
- Optional: per-page breakdown for `page=<name>`

Lazy import — if `confidence.py` can't be imported, returns a clear error.

### Impact
~15 lines in `_search`, ~20 lines for new `wiki_confidence` tool. Zero changes to `confidence.py`.

## What Is Explicitly NOT in Scope

- **Rejected-value tombstone** (Atlas pattern) — deferred. Needs frontmatter status field + write-path gate + search exclusion. ~30 lines, but design implications warrant separate review.
- **Conflict resolution gate** — deferred. Needs `wiki_list_conflicts` + `wiki_resolve_conflict` tools + write-path block. ~100 lines. The Atlas pattern ("Resolve, don't just detect") requires more design work.
- **KNOWLEDGE-DECAY.md implementation** — deferred. The draft design is sound but was marked "DRAFT" and dated April 2026. Needs Board decision on whether to build it.
- **Tests** — acknowledged as absent. Adding tests before the next phase is the right call, but is a separate task from closing the enforcement gaps.
- **License contradiction** — separate concern (README MIT vs source All Rights Reserved). Board decision on license before touching files.

## Verification Plan

After each section:
1. **Section 1:** `git ls-files L1/` returns empty. `.example` files exist. `SCHEMA.md` documents setup step.
2. **Section 2:** Write a page without `[Source:]` → rejected. Write a page with `[Source:]` → log entry appears. Force git commit failure → ⚠️ message, not ✅.
3. **Section 3:** Without `sentence-transformers` → substring path (unchanged behavior). With `sentence-transformers` → ranked results with scores.
4. **Section 4:** `wiki_search min_confidence=high` → only high-confidence pages. `wiki_confidence` tool returns distribution and stale pages.
