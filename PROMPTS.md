# Memex Prompts

Copy-paste prompts for every Memex operation. Customize as needed.

---

## Setup

### Initialize Wiki

```
Read SCHEMA.md to understand how this wiki works.

Then:
1. Confirm you understand the L1/L2 architecture
2. Check that wiki/index.md exists (create if missing)
3. Check that wiki/log.md exists (create if missing)
4. Report what focus areas I should customize in SCHEMA.md
```

---

## Ingest

### Ingest Single Source

```
Read SCHEMA.md. Then ingest raw/[FILENAME] following the ingest workflow:

1. Read the full source
2. Discuss key takeaways with me before writing anything
3. Create summary in wiki/sources/
4. Update wiki/index.md
5. Create or update relevant entity and concept pages
6. Add backlinks from existing pages
7. Check for contradictions with existing wiki content
8. Log the operation in wiki/log.md

Show me which pages you'll create/update before making changes.
```

### Ingest Multiple Sources (Supervised)

```
Read SCHEMA.md. I want to ingest all files in raw/ that aren't already in wiki/sources/.

For EACH source:
1. Tell me the filename
2. Give me a 2-sentence summary
3. Wait for my approval before processing

Process them one at a time. Do not batch without my explicit OK.
```

### Ingest Multiple Sources (Batch)

```
Read SCHEMA.md. Process all unprocessed files in raw/ sequentially.

For each: create summary, update index, update relevant pages, log the ingest.

Give me a final report with:
- Sources processed
- Pages created
- Pages updated
- Any contradictions found (DO NOT auto-resolve, add to wiki/contradictions.md)
```

---

## Query

### Ask a Question

```
Read wiki/index.md. Based on the knowledge base, answer:

[YOUR QUESTION HERE]

Requirements:
- Cite which wiki pages informed your answer: [Source: wiki/page.md]
- If you can't find the answer, say so honestly
- If the answer would be valuable to keep, offer to file it as a new wiki page
```

### Deep Research Query

```
Read wiki/index.md, then read ALL pages that might be relevant to:

[YOUR QUESTION HERE]

After reading everything relevant:
1. Synthesize a comprehensive answer
2. Note any gaps in the wiki's coverage
3. Suggest sources I could add to fill those gaps
4. Offer to create a wiki/synthesis/ page with your findings
```

### Exploratory Query

```
Read wiki/index.md and identify the 5 most interesting unexplored connections between existing topics.

For each:
1. What's the potential insight?
2. What wiki pages are involved?
3. What source would help confirm it?
```

---

## Lint

### Full Health Check

```
Run a full lint check on wiki/ per the lint workflow in SCHEMA.md.

Check for:
- Unsourced claims (🔴 ERROR)
- Broken [[wikilinks]] (🔴 ERROR)
- Orphan pages with no inbound links (🟡 WARNING)
- Stale pages not updated in 90 days (🟡 WARNING)
- Pages missing from index (🔴 ERROR)
- Credential patterns in content (🔴 CRITICAL)

Output to wiki/lint-report-[today's date].md with severity levels.

Also suggest 3 sources I could add to fill knowledge gaps.
```

### Quick Lint (Just Errors)

```
Quick lint: scan wiki/ for only 🔴 ERROR and 🔴 CRITICAL issues.
Report inline, don't create a file.
```

### Fix Lint Issues

```
Read wiki/lint-report-[LATEST].md.

For each issue:
1. Show me the problem
2. Propose a fix
3. Wait for my approval before applying

Do NOT auto-fix anything without my confirmation.
```

---

## Conflict Resolution

### List Pending Conflicts

```
Read wiki/contradictions.md and summarize all pending conflicts.

For each:
- The two claims
- Their sources
- Your recommendation (but DO NOT apply it)
```

### Resolve a Conflict

```
Read wiki/contradictions.md. I want to resolve:

[CONFLICT DESCRIPTION OR ID]

Present:
1. Claim A with source
2. Claim B with source
3. Your analysis of which is more likely correct and why

Then wait for my decision. Options:
- A supersedes B
- B supersedes A
- Both are valid (explain coexistence)
- Need more information (what would help?)
```

---

## Synthesis & Reports

### Generate Brief

```
Based on everything in wiki/, write a 500-word executive briefing on:

[TOPIC]

Structure:
1. Current state (what we know)
2. Key tensions (where things conflict or are uncertain)
3. Open questions (what we don't know)
4. Recommended next steps

Cite every claim with [Source: wiki/page.md].
Save to outputs/reports/[topic]-brief-[date].md
```

### Generate Comparison

```
Compare these topics across the wiki:

[TOPIC A] vs [TOPIC B]

Create a comparison table covering:
- Definition
- Key characteristics
- When to use each
- Sources that discuss each

Save to wiki/synthesis/[topic-a]-vs-[topic-b].md
```

### Generate Timeline

```
Based on wiki/, create a timeline of:

[SUBJECT]

Include:
- Dates (exact or approximate)
- Events
- Sources for each date

Format as a markdown table. Save to wiki/synthesis/[subject]-timeline.md
```

---

## Maintenance

### Update Index

```
Scan all files in wiki/sources/, wiki/entities/, wiki/concepts/, wiki/synthesis/.
Compare against wiki/index.md.

Report any discrepancies:
- Pages in folders but not in index
- Entries in index pointing to missing pages

Offer to fix the index.
```

### Archive Stale Content

```
Find all pages in wiki/ with:
- status: stale, OR
- updated date > 90 days ago, OR
- no inbound links

For each, ask me:
- Keep and mark for review?
- Archive (move to wiki/_archive/)?
- Delete?
```

### Consolidate Pages

```
Read wiki/index.md. Identify pages that could be merged:
- Near-duplicate content
- Overlapping scope
- One is subset of another

For each candidate merge, show me both pages and ask for approval.
```

---

## Session Start/End

### Session Start

```
Read L1/ (identity.md, rules.md).
Read wiki/log.md (last 10 entries).
Briefly tell me:
- Last 3 operations on this wiki
- Any pending contradictions
- Any lint issues from last check
```

### Session End

```
Before I go, summarize:
- What we added to the wiki today
- Any pending items (contradictions, lint issues, unanswered questions)
- Suggested next steps for next session

Log this session summary to wiki/log.md.
```

---

## Emergency

### Quarantine Page

```
Page wiki/[PATH] has too many unsourced claims.

1. Add `status: quarantine` to its frontmatter
2. Add a warning banner at the top:
   > ⚠️ QUARANTINED: This page has unsourced claims. Do not cite until reviewed.
3. Create an entry in wiki/log.md
```

### Remove Credentials

```
URGENT: Check all wiki/ files for credential patterns:
- API keys
- Tokens
- Passwords
- Private URLs

Report any findings. For each:
1. What file
2. What line
3. What it looks like (redact the actual value)

Then I'll tell you how to redact.
```

---

*Prompts version: 1.0 | See SCHEMA.md for full operation details*
