# CLAUDE.md — MeMex Zero-RAG Personal Knowledge Base

## System Purpose
MeMex builds a **structured, interlinked wiki from sources**. It's the long-term knowledge compilation layer that lives alongside Second Brain.

### Relationship to Second Brain
```
Second Brain (~/Documents/)
├─ inbox/      → Capture → raw/sources → MeMex processing
├─ daily/      → Work    → Discover patterns → wiki/
├─ research/   → Gather → Feed into L2 layer
└─ projects/   → Build  → Reference compiled knowledge

MeMex (~/workspace/MeMex-Zero-RAG)
├─ raw/        ← Feed research from Second Brain here
├─ wiki/       → Query via MCP server during work
├─ L1/         → Personal context (git-ignored)
└─ graph/      → Relationships and structure
```

## Core Workflow

### 1. Ingest Sources
```bash
# Add files to raw/ folder (markdown, txt, docs)
# Run MCP server or use /memex slash command from Second Brain
# LLM extracts, creates summaries, links entities
```

### 2. Build Knowledge
- L2 wiki/ contains structured pages
- Every claim must cite sources (enforced by linter)
- Entity pages auto-created for recurring concepts
- Relationships tracked in graph/

### 3. Query Knowledge
- Via MCP server: Claude Code can ask the wiki directly
- From Second Brain: Use `/memex-query` slash command
- From anywhere: "Read ~/workspace/MeMex-Zero-RAG/wiki/[topic].md"

## File Structure

```
raw/          ← Drop sources here (feeds wiki)
wiki/         ← The compiled knowledge base
  L2-index.md   ← Auto-updated, all entities and relationships
  /entities/    ← People, concepts, topics
  /topics/      ← Domain knowledge pages
L1/           ← Personal context (git-ignored, never shared)
  /memory/      ← Your own notes, drafts, thinking
mcp/          ← MCP server for Claude Code integration
graph/        ← Knowledge graph analysis
```

## Key Rules

1. **Zero Hallucination** — Every claim in wiki/ must have a source citation
2. **Human Truth** — Conflicts are flagged; you decide authoritative sources
3. **Compound Knowledge** — Each new source makes the whole wiki richer
4. **Git-Native** — Full history, multi-agent via worktrees, rollback on errors

## Slash Commands (from Claude Code)

- `/memex-query [topic]` — Search the wiki
- `/memex-ingest [folder]` — Process files from Second Brain/research into raw/
- `/memex-check` — Verify all claims have sources
- `/memex-report` — Generate a knowledge report on a topic

## Integration with Claude Code / Hermes

The MCP server is already configured:
```yaml
mcp_servers:
  memex:
    command: /Users/joergpeetz/workspace/MeMex-Zero-RAG/.venv/bin/python
    args: [mcp/server.py]
    cwd: /Users/joergpeetz/workspace/MeMex-Zero-RAG
```

Use it directly in any Claude Code session to query compiled knowledge without hallucination.

## How to Maintain

- **Daily**: Review wiki changes via `git log`
- **Weekly**: Archive processed sources from raw/ to outputs/
- **Monthly**: Generate knowledge report, identify gaps
- **Quarterly**: Review L1 context, update ground truth sources

## Knowledge Decay Prevention

See [KNOWLEDGE-DECAY.md](KNOWLEDGE-DECAY.md) for strategies to keep the wiki current and relevant as new information arrives.
