# Rules

> Hard constraints for the MeMex wiki. The LLM must follow these without exception.

## Citation Rules

1. Every factual claim MUST have a `[Source: path]` citation
2. If you cannot cite, say so explicitly — "I believe X but cannot find the source"
3. Never present inference as fact — mark with `[Inference]` or `[Unverified]`
4. Two-hop maximum: Answer → wiki page → raw source

## Conflict Rules

1. When sources contradict, STOP and flag — never auto-resolve truth
2. Add to `wiki/contradictions.md` before proceeding
3. Wait for human decision

## Content Rules

1. Never modify files in `raw/` — they are immutable sources
2. Never commit files from `L1/` — they are git-ignored
3. Never reference credentials from `L1/credentials.md` in wiki content
4. Every wiki page must have complete YAML frontmatter
5. Every wiki page must have at least one `[[wikilink]]`
6. Update `wiki/index.md` on every ingest
7. Append to `wiki/log.md` on every operation

## Quality Rules

1. Pages with >20% unsourced claims get `status: quarantine`
2. Orphan pages (no inbound links for 30+ days) get flagged in lint
3. Stale pages (not updated in 90 days) get `status: stale`

## Domain Rules

1. This wiki is for Marvin's self-learning and self-improvement
2. Ingest sources that help Marvin do its job better
3. Focus on: software engineering, AI systems, agent design, monetisation, research
4. When ingesting, target 5-15 wiki pages per source
5. Cross-reference with obsidian-mind vault when relevant

---

*Rules version: 1.0 | Created: 2026-05-09*
