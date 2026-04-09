# Memex Schema

> This file is the brain of your Memex. It tells your LLM how the knowledge base works, what conventions to follow, and how to handle every operation.

## Identity

This is a personal knowledge base about **[YOUR DOMAIN HERE]**.

Maintained by an LLM agent. The human curates sources and asks questions. The LLM does everything else—except decide truth when sources conflict.

## Architecture

```
L1/          → Auto-loaded every session. Private. Git-ignored.
raw/         → Immutable source documents. LLM reads, never modifies.
wiki/        → LLM-maintained wiki. LLM writes, human reads.
outputs/     → Generated artifacts (reports, slides, exports).
```

### L1: Session Context (Private)

Files in `L1/` are loaded automatically at session start. They contain:
- `identity.md` — Who you are, preferences, communication style
- `rules.md` — Hard constraints, gotchas, things to always remember
- `credentials.md` — API keys, tokens (NEVER reference in wiki)

**L1 is git-ignored. Never commit it. Never reference credentials in wiki pages.**

### raw/: Source Documents (Immutable)

- Drop sources here: articles, papers, notes, transcripts
- The LLM reads from `raw/` but NEVER modifies files there
- Images go in `raw/assets/`
- This is your source of truth

### wiki/: Knowledge Base (LLM-Maintained)

The LLM owns this directory. It creates, updates, and maintains all pages.

```
wiki/
├── index.md          # Master catalog of all pages
├── log.md            # Chronological operation record
├── contradictions.md # Pending conflict resolutions
├── sources/          # One summary per ingested source
├── entities/         # People, orgs, tools, projects
├── concepts/         # Ideas, frameworks, patterns
└── synthesis/        # Analyses, comparisons, insights
```

---

## Page Conventions

### Frontmatter (Required)

Every wiki page starts with YAML frontmatter:

```yaml
---
title: Page Title
type: source | entity | concept | synthesis
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: draft | active | stale | quarantine
source_count: N  # Number of raw sources informing this page
tags: [tag1, tag2]
---
```

### Content Structure

After frontmatter:
1. **One-paragraph summary** — What this page is about
2. **Sections** — Organized content with headers
3. **Cross-references** — Use `[[page-name]]` for internal links
4. **Citations** — Every factual claim cites its source

### Citation Format

```markdown
Redis is used for session caching. [Source: raw/architecture-notes.md]

Multiple sources confirm the migration happened in Q1. [Source: raw/meeting-2026-03.md, raw/changelog.md]
```

If synthesizing across wiki pages:
```markdown
This pattern appears across multiple projects. [Source: wiki/entities/project-a.md, wiki/entities/project-b.md]
```

### Wikilinks

Use `[[page-name]]` to link between wiki pages:
```markdown
The [[redis]] caching layer connects to [[project-alpha]].
```

Page names should be lowercase-kebab-case: `my-concept-name.md`

---

## Index and Log

### wiki/index.md

The master catalog. Updated on every ingest. Format:

```markdown
# Wiki Index

Last updated: YYYY-MM-DD
Total pages: N

## Sources (N)
- [[source-name]] — One-line description

## Entities (N)
- [[entity-name]] — One-line description

## Concepts (N)
- [[concept-name]] — One-line description

## Synthesis (N)
- [[synthesis-name]] — One-line description
```

### wiki/log.md

Append-only chronological record. Format:

```markdown
## [YYYY-MM-DD HH:MM] action | Description

Actions: ingest, query, lint, resolve, update, brief
```

Example:
```markdown
## [2026-04-09 10:30] ingest | Processed architecture-notes.md
- Created: wiki/sources/architecture-notes.md
- Updated: wiki/entities/redis.md, wiki/concepts/caching.md
- New cross-references: 3

## [2026-04-09 11:00] query | "What caching strategy do we use?"
- Answer filed: wiki/synthesis/caching-strategy.md
```

---

## Operations

### Ingest Workflow

When processing a new source from `raw/`:

1. **Read** the full source document
2. **Discuss** key takeaways with the user
3. **Create summary** in `wiki/sources/[source-name].md`
4. **Update index** — Add entry to `wiki/index.md`
5. **Update entities** — Create or update pages in `wiki/entities/`
6. **Update concepts** — Create or update pages in `wiki/concepts/`
7. **Add backlinks** — Link existing pages to new content
8. **Check contradictions** — If new info conflicts with existing:
   - Add entry to `wiki/contradictions.md`
   - STOP and prompt user for resolution
   - Do NOT auto-resolve
9. **Log operation** — Append to `wiki/log.md`

**Target: A single source should touch 5-15 wiki pages.**

### Query Workflow

When answering a question:

1. **Read** `wiki/index.md` to find relevant pages
2. **Read** all relevant wiki pages
3. **Synthesize** answer with `[Source: wiki/page.md]` citations
4. **Two-hop max**: Answer cites wiki, wiki cites raw
5. **Offer to file**: If answer reveals new insight, offer to save as `wiki/synthesis/[topic].md`
6. **Log** the query in `wiki/log.md`

### Lint Workflow

Health check for the wiki. Run monthly or after every 10 ingests.

**Check for:**

| Issue | Severity | Action |
|-------|----------|--------|
| Unsourced claims | 🔴 ERROR | Mark for citation or quarantine page |
| Broken `[[wikilinks]]` | 🔴 ERROR | Fix or remove |
| Orphan pages (no inbound links) | 🟡 WARNING | Add links or flag for review |
| Stale pages (not updated in 90 days) | 🟡 WARNING | Mark `status: stale` |
| Missing from index | 🔴 ERROR | Add to index |
| Credentials in content | 🔴 CRITICAL | Remove immediately |

**Output**: `wiki/lint-report-YYYY-MM-DD.md`

### Resolve Workflow

When resolving a conflict from `wiki/contradictions.md`:

1. **Present** both claims to user with sources
2. **Get decision**: Which is authoritative? Both valid? Need more info?
3. **Update wiki** — Modify relevant pages
4. **Log resolution** with rationale
5. **Mark resolved** in contradictions file

### Brief Workflow

Generate an executive summary on a topic:

1. **Read** all relevant wiki pages
2. **Structure** as: Current state → Key tensions → Open questions → Next steps
3. **Cite** every claim
4. **Save** to `outputs/reports/[topic]-brief-YYYY-MM-DD.md`

---

## Anti-Hallucination Protocol

### Hard Rules

1. **Every factual claim MUST have a citation** — `[Source: path]`
2. **If you cannot cite, say so** — "I believe X but cannot find the source"
3. **Never present inference as fact** — Mark speculation: `[Inference]` or `[Unverified]`
4. **Two-hop maximum** — Answer → wiki page → raw source

### Enforcement

- **Ingest**: Only write claims you can cite
- **Lint**: Flag unsourced claims as 🔴 ERROR
- **Quarantine**: Pages with >20% unsourced claims get `status: quarantine`
- **Shame log**: Track failures in `wiki/hallucinations.md` for pattern analysis

### What to do when uncertain

```markdown
❓ [Unverified] The migration may have happened in Q2.

🔍 [Needs source] Redis cluster size is reportedly 8 nodes.

💭 [Inference] Based on the architecture, this likely uses Redis Cluster.
```

---

## Conflict Handling

### Detection

When new information contradicts existing wiki content:

```markdown
> ⚠️ CONTRADICTION DETECTED
> - Existing: [claim] from [source]
> - New: [claim] from [source]
> - See: wiki/contradictions.md
```

### Resolution Process

1. **Do NOT silently overwrite or pick a side**
2. **Add to `wiki/contradictions.md`**:
   ```markdown
   ### [YYYY-MM-DD] Brief description
   - **Page**: wiki/path/to/page.md
   - **Existing claim**: "X" [Source: raw/old.md]
   - **New claim**: "Y" [Source: raw/new.md]
   - **Status**: ⏳ PENDING
   - **Resolution**: 
   ```
3. **Prompt user** — "Found contradiction. Which is authoritative?"
4. **Wait for decision** — Do not proceed until resolved
5. **Log resolution** with rationale and timestamp

---

## Focus Areas

Customize this section for your domain:

```markdown
## Primary Topics
- [Topic 1]
- [Topic 2]
- [Topic 3]

## Entity Types
- People
- Projects
- Tools/Technologies
- Organizations

## Key Questions to Answer
- [Question 1]
- [Question 2]
```

---

## Quality Standards

### Good Wiki Page

✅ Has complete frontmatter  
✅ Starts with one-paragraph summary  
✅ Every claim has `[Source: ]` citation  
✅ Has at least one `[[wikilink]]` to another page  
✅ Is listed in `wiki/index.md`  
✅ Status is `active`

### Quarantine Triggers

❌ >20% unsourced claims  
❌ No inbound links for 30+ days  
❌ Contains credential patterns  
❌ Contradicts multiple other pages without resolution

---

## Evolution

This schema evolves. After a few dozen ingests and lint passes:

1. **Add domain-specific entity types** to Focus Areas
2. **Refine contradiction handling** based on what conflicts arise
3. **Adjust lint thresholds** based on your tolerance
4. **Document patterns** that work for your knowledge domain

The first version will be rough. That's fine. Let it grow with your wiki.

---

*Schema version: 1.0 | Based on Karpathy's LLM Wiki pattern*
