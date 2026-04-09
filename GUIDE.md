# Memex: Complete Guide

A deep dive into building and maintaining your zero-RAG personal knowledge base.

---

## Table of Contents

1. [Philosophy](#philosophy)
2. [Setup Walkthrough](#setup-walkthrough)
3. [Your First Ingest](#your-first-ingest)
4. [Building the Wiki](#building-the-wiki)
5. [Querying Effectively](#querying-effectively)
6. [Maintenance](#maintenance)
7. [Scaling Up](#scaling-up)
8. [Troubleshooting](#troubleshooting)

---

## Philosophy

### Why Not RAG?

Traditional RAG (Retrieval Augmented Generation) works like this:
1. Upload documents
2. Chunk them into pieces
3. When you ask a question, find relevant chunks
4. Generate answer from chunks

The problem: **every question starts from zero**. The LLM rediscovers knowledge each time. Ask a subtle question that requires synthesizing five documents, and it has to find and piece together fragments every time. Nothing compounds.

### The Wiki Approach

Instead:
1. You add a source
2. The LLM **reads it once** and extracts key information
3. It **integrates** that knowledge into a structured wiki
4. Cross-references are created, contradictions flagged, synthesis built
5. Next time you ask a question, the knowledge is **already compiled**

The wiki is a persistent, compounding artifact. Every source makes it richer. Every question you ask can be filed back in.

### The Human-LLM Division

| Human | LLM |
|-------|-----|
| Curate sources | Read and extract |
| Ask good questions | Write and organize |
| Decide truth when sources conflict | Flag contradictions |
| Think about what it means | Do the bookkeeping |

You do the thinking. The LLM does everything else.

---

## Setup Walkthrough

### Step 1: Clone

```bash
git clone https://github.com/JPeetz/memex.git my-wiki
cd my-wiki
```

### Step 2: Customize SCHEMA.md

Open `SCHEMA.md` and update:

1. **Identity section**: What is this wiki about?
   ```markdown
   This is a personal knowledge base about **machine learning research**.
   ```

2. **Focus Areas**: What topics will you cover?
   ```markdown
   ## Primary Topics
   - Transformer architectures
   - Training optimization
   - Inference efficiency
   
   ## Entity Types
   - Researchers
   - Papers
   - Models
   - Datasets
   ```

### Step 3: Set Up L1 (Private Context)

Edit `L1/identity.md`:
```markdown
## About Me
- **Name**: Jane
- **Role**: ML Research Engineer
- **Timezone**: US/Pacific

## Communication Preferences
- **Tone**: Technical but accessible
- **Detail level**: Thorough for research, brief for admin
```

Edit `L1/rules.md` with any domain-specific gotchas:
```markdown
## Domain-Specific Rules

### Papers
- Always note: title, authors, venue, year
- Flag if preprint vs peer-reviewed
- Note key contributions in bullet points
```

### Step 4: Initialize Git

```bash
git add .
git commit -m "Initialize wiki with schema and structure"
```

Note: L1/ is gitignored — it won't be committed.

### Step 5: Connect to Obsidian (Optional but Recommended)

1. Open Obsidian
2. "Open folder as vault" → select your wiki directory
3. Enable "Detect all file extensions" in Settings → Files & Links
4. The graph view will show your wiki's structure as it grows

---

## Your First Ingest

### Step 1: Add a Source

Drop a document into `raw/`:
```bash
cp ~/Downloads/attention-is-all-you-need.pdf raw/
```

Or create a markdown file with notes:
```bash
cat > raw/transformer-notes.md << 'EOF'
# Notes on Transformer Architecture

The Transformer was introduced in "Attention Is All You Need" (Vaswani et al., 2017).

Key innovations:
- Self-attention mechanism replacing recurrence
- Multi-head attention for parallel processing
- Positional encoding for sequence order

The model achieves SOTA on WMT translation benchmarks.
EOF
```

### Step 2: Tell Your LLM to Ingest

Open your AI agent and paste:

```
Read SCHEMA.md. Then ingest raw/transformer-notes.md following the ingest workflow.

Before writing anything, discuss the key takeaways with me.
```

### Step 3: Review and Approve

The LLM will:
1. Summarize what it found
2. Propose which pages to create/update
3. Wait for your approval

Example response:
> "This source covers the Transformer architecture. I'll create:
> - wiki/sources/transformer-notes.md (summary)
> - wiki/entities/transformer.md (model page)
> - wiki/entities/vaswani.md (researcher)
> - wiki/concepts/self-attention.md (concept)
> - wiki/concepts/multi-head-attention.md (concept)
> 
> Should I proceed?"

### Step 4: Watch It Work

After approval, the LLM creates pages with:
- YAML frontmatter (title, type, dates, status)
- One-paragraph summary
- Structured content with citations
- Cross-references via `[[wikilinks]]`

It updates `wiki/index.md` and `wiki/log.md`.

### Step 5: Browse in Obsidian

Open Obsidian. You'll see:
- New pages in the file tree
- Links between pages (click to navigate)
- Graph view showing connections

---

## Building the Wiki

### Good Ingestion Rhythm

**Start slow**: Ingest 1-3 sources per session. Review the output. Guide the LLM on what to emphasize.

**Batch later**: Once the wiki has structure (20+ pages), you can batch-ingest with less supervision.

**Quality over quantity**: A wiki with 50 well-integrated pages beats 200 poorly-linked ones.

### Source Types That Work Well

| Type | Tips |
|------|------|
| Research papers | Extract: title, authors, venue, key contributions, limitations |
| Articles | Extract: main argument, supporting evidence, counterpoints |
| Meeting notes | Extract: decisions, action items, attendees, context |
| Documentation | Extract: concepts, APIs, examples, gotchas |
| Books (chapters) | One source per chapter, link to book entity |

### Creating Good Cross-References

The LLM should link liberally:
- Every entity mentioned → link to its page
- Every concept used → link to its page
- Every source referenced → link to its summary

If a page has no inbound links after 30 days, lint will flag it.

### Filing Answers Back

When you query the wiki and get a valuable answer:

```
That answer is valuable. File it as wiki/synthesis/transformer-efficiency-comparison.md
```

Your explorations become part of the wiki. Knowledge compounds.

---

## Querying Effectively

### Basic Query

```
Read wiki/index.md. Based on the wiki, answer:
What are the main approaches to efficient Transformers?
```

### Deep Research Query

```
Read wiki/index.md, then read ALL pages related to attention mechanisms.
Synthesize a comprehensive overview, noting:
- Where sources agree
- Where sources conflict
- What gaps exist
```

### Exploratory Query

```
Read wiki/index.md. What are the 5 most interesting unexplored connections?
What sources would help investigate them?
```

### Gap Analysis

```
Read wiki/index.md. What topics are mentioned but have no dedicated page?
What entities are referenced but not defined?
```

---

## Maintenance

### Weekly: Quick Lint

```
Quick lint: scan wiki/ for 🔴 ERROR issues only.
```

### Monthly: Full Health Check

```
Run a full lint check on wiki/ per SCHEMA.md.
Output to wiki/lint-report-[today].md.
```

### As Needed: Resolve Contradictions

Check `wiki/contradictions.md`. For each pending:

```
Read wiki/contradictions.md. I want to resolve the [X] contradiction.
Present both claims with sources. I'll decide.
```

### Quarterly: Consolidation

```
Read wiki/index.md. Identify:
- Pages that could be merged
- Stale pages that should be archived
- Sections that have grown large enough to split
```

---

## Scaling Up

### 0-50 Pages: Index Is Enough

The LLM reads `wiki/index.md` to find relevant pages. This works fine.

### 50-200 Pages: Add Search

Install [qmd](https://github.com/tobi/qmd):
```bash
npm install -g @tobilu/qmd
```

Query with:
```
Use qmd to search for "attention optimization" across wiki/.
Then read the top 5 results and synthesize an answer.
```

### 200+ Pages: Consider Splitting

If topics are truly distinct, create separate wikis:
```
ml-research-wiki/     # Your main research wiki
project-alpha-wiki/   # Project-specific knowledge
reading-notes-wiki/   # Book notes and articles
```

Each has its own SCHEMA.md customized for its domain.

---

## Troubleshooting

### "The LLM isn't citing sources"

Reinforce in your prompt:
```
Remember: every factual claim MUST have [Source: path]. No exceptions.
```

Check that SCHEMA.md is clear about citation requirements.

### "Pages aren't being cross-referenced"

Ask explicitly:
```
After creating the page, add [[wikilinks]] to all related entities and concepts.
Then add backlinks from those pages to this one.
```

### "The index is out of sync"

```
Scan all files in wiki/. Compare to wiki/index.md.
Report discrepancies and offer to fix.
```

### "I found a hallucination"

Log it:
```
Add to wiki/hallucinations.md:
- Date: [today]
- Page: [which page]
- Claim: [the false claim]
- How detected: [how you found out]

Then fix the page and add proper citation or remove the claim.
```

### "Contradictions aren't being flagged"

The LLM might not catch all conflicts. Run periodically:
```
Read all pages in wiki/entities/ and wiki/concepts/.
Check for any claims that conflict with each other.
Report findings.
```

### "L1 was accidentally committed"

```bash
# Remove from git history (careful!)
git filter-branch --force --index-filter \
  'git rm -rf --cached --ignore-unmatch L1/' \
  --prune-empty --tag-name-filter cat -- --all

# Force push (coordinate with collaborators)
git push origin --force --all
```

Then rotate any credentials that were in L1/.

---

## Tips from Experience

1. **Start with one domain**. A wiki about "everything" becomes nothing.

2. **Ingest slowly at first**. Guide the LLM on your preferences before batching.

3. **Review the first 10 pages carefully**. Patterns set early persist.

4. **Use the graph view**. Orphan clusters reveal missing connections.

5. **File good answers back**. Your queries are valuable sources.

6. **Don't skip lint**. Small issues compound into big messes.

7. **Trust but verify**. Spot-check citations, especially on important topics.

8. **Let the schema evolve**. Update SCHEMA.md as you learn what works.

---

*Guide version: 1.0 | See SCHEMA.md and PROMPTS.md for reference*
