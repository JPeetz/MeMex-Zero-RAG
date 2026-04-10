# Research: Existing LLM Wiki Implementations

> Research conducted for building Memex — a zero-RAG personal knowledge base.

## Sources Analyzed

### 1. Karpathy's Original Gist
- URL: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- **Approach**: Abstract "idea file" — describes pattern, not implementation
- **Layers**: raw/ (immutable sources) → wiki/ (LLM-maintained) → schema (CLAUDE.md)
- **Operations**: Ingest, Query, Lint
- **Strengths**: Clean conceptual model, tool-agnostic
- **Gaps**: No schema template, no prompts, no conflict resolution, no lifecycle

### 2. NicholasSpisak/second-brain
- URL: https://github.com/NicholasSpisak/second-brain
- **Approach**: AgentSkills-based (npx skills add)
- **Structure**: wiki/{sources, entities, concepts, synthesis}/
- **Strengths**: Wizard setup, Obsidian-native, skill-based commands
- **Gaps**: Requires Node.js + AgentSkills ecosystem, Obsidian-specific

### 3. MehmetGoekce/llm-wiki
- URL: https://github.com/MehmetGoekce/llm-wiki
- **Approach**: L1/L2 cache architecture (key insight!)
- **L1 (auto-loaded)**: Rules, gotchas, identity, credentials (~10-20 files)
- **L2 (on-demand)**: Deep wiki knowledge (~50-200 pages)
- **Strengths**: Cache hierarchy concept, Claude Code native
- **Gaps**: Claude Code specific, setup.sh approach

### 4. lucasastorian/llmwiki
- URL: https://github.com/lucasastorian/llmwiki
- **Approach**: Full SaaS stack (Next.js + FastAPI + Supabase + MCP)
- **Strengths**: Hosted option, PDF viewer, MCP server
- **Gaps**: Heavy infrastructure, not portable

### 5. xoai/sage-wiki
- URL: https://github.com/xoai/sage-wiki
- **Approach**: Single Go binary with embedded web UI
- **Strengths**: Cross-platform, MCP server, TUI, hybrid search, cost estimation
- **Gaps**: Requires Go compilation, heavy feature set

### 6. LLM Wiki v2 (rohitg00)
- URL: https://gist.github.com/rohitg00/2067ab416f7bbe447c1977edaaa681e2
- **Approach**: Extended pattern with agentmemory lessons
- **Key additions**:
  - Confidence scoring (sources, recency, contradiction count)
  - Supersession (explicit version control for claims)
  - Forgetting (retention decay, Ebbinghaus curve)
  - Consolidation tiers (working → episodic → semantic → procedural)
  - Typed knowledge graph (not just wikilinks)
  - Automation hooks (on-ingest, on-session-start, on-schedule)
  - Quality scoring + self-healing lint
  - Multi-agent mesh sync

---

## Gap Analysis: What's Missing from ALL Implementations

| Gap | Description | Our Solution |
|-----|-------------|--------------|
| **Zero hallucination enforcement** | All mention "cite sources" but none enforce it | Mandatory citations, quarantine unsourced pages, shame log |
| **User-resolved conflicts** | Most auto-resolve or just flag | STOP and prompt user, never auto-resolve |
| **LLM-agnostic** | Most tied to Claude/specific providers | Works with any LLM that can read/write files |
| **Git-first versioning** | Mentioned but no actual workflow | Branch strategy, commit hooks, rollback procedures |
| **Multi-wiki isolation** | Single wiki assumed | Project wikis + main wiki, clear boundaries |
| **Credential safety** | L1/L2 approach (MehmetGoekce) is best | Adopt L1 (auto-load, git-ignored) + L2 (wiki) pattern |
| **Offline-first** | Most need APIs always | Pure markdown, works offline, sync when online |

---

## Design Decisions for Our Repo

### 1. Target Audience
- **Primary**: Developers using AI coding agents (Claude Code, Cursor, Codex, OpenClaw, etc.)
- **Secondary**: Researchers, knowledge workers wanting structured personal wikis
- **NOT**: End-users wanting a GUI app (use llmwiki.app or sage-wiki for that)

### 2. Core Principles
1. **LLM-agnostic**: Works with ANY agent that can read/write markdown
2. **Zero infrastructure**: No databases, no embeddings, no servers required
3. **Git-native**: Version control built-in, not bolted on
4. **Human-in-the-loop**: Conflicts prompt user, never auto-resolved
5. **Zero hallucination tolerance**: Unsourced claims are errors, not warnings

### 3. Architecture (Inspired by L1/L2 pattern)

```
your-wiki/
├── .git/                    # Version control
├── .gitignore               # Excludes L1 (sensitive), raw/assets/
│
├── L1/                      # Auto-loaded every session (GIT-IGNORED)
│   ├── identity.md          # Who am I, preferences
│   ├── rules.md             # Hard rules, gotchas, constraints
│   └── credentials.md       # API keys, tokens (NEVER committed)
│
├── raw/                     # Immutable source documents
│   ├── assets/              # Images, diagrams (git-lfs or ignored)
│   └── [sources...]         # PDFs, articles, notes
│
├── wiki/                    # LLM-maintained knowledge base
│   ├── index.md             # Master catalog
│   ├── log.md               # Append-only operation log
│   ├── contradictions.md    # Pending user resolution
│   │
│   ├── sources/             # One summary per raw source
│   ├── entities/            # People, orgs, tools, projects
│   ├── concepts/            # Ideas, frameworks, patterns
│   └── synthesis/           # Analyses, comparisons, insights
│
├── outputs/                 # Generated artifacts
│   ├── reports/             # Briefings, analyses
│   ├── presentations/       # Marp slides
│   └── exports/             # JSON, CSV extracts
│
├── SCHEMA.md                # The brain — how wiki works
├── PROMPTS.md               # Copy-paste prompts for operations
└── README.md                # Getting started guide
```

### 4. Operations

| Operation | Command | What Happens |
|-----------|---------|--------------|
| **Setup** | `init` | Create structure, customize SCHEMA.md |
| **Ingest** | `ingest <source>` | Read → Extract → Update 5-15 pages → Log |
| **Query** | `query <question>` | Search index → Read pages → Synthesize → Offer to file |
| **Lint** | `lint` | Find orphans, broken refs, unsourced claims, stale content |
| **Brief** | `brief <topic>` | Generate executive summary with citations |
| **Resolve** | `resolve <conflict>` | User decides truth, update wiki |

### 5. Anti-Hallucination Protocol

Every claim must have `[Source: filename.md]` or `[Source: wiki/page.md]`.

**Enforcement layers:**
1. **Ingest**: Schema instructs LLM to cite everything
2. **Lint**: Flags unsourced claims as 🔴 ERROR
3. **Quarantine**: Pages with >20% unsourced claims get `status: quarantine`
4. **Shame log**: `wiki/hallucinations.md` tracks failures for pattern analysis

### 6. Conflict Resolution

```markdown
## wiki/contradictions.md

### [2026-04-09] Redis caching claim
- **Existing**: "Project X uses Memcached" [Source: architecture-notes.md]
- **New**: "Project X migrated to Redis in Q1" [Source: meeting-2026-03.md]
- **Status**: ⏳ PENDING USER RESOLUTION
- **Options**:
  1. New supersedes old (meeting notes more recent)
  2. Both true (Memcached for legacy, Redis for new)
  3. Investigate further
```

LLM NEVER resolves. Prompts user. Logs decision.

### 7. Git Workflow

```
main                    # Production state
├── ingest/YYYY-MM-DD   # Major ingest sessions
├── lint/YYYY-MM-DD     # Lint fix batches
└── archive/pre-X       # Snapshots before restructures
```

**Hooks:**
- Pre-commit: Validate YAML frontmatter, check for credential patterns
- Post-ingest: Auto-commit with descriptive message

---

## Differentiation from Existing Implementations

| Feature | Ours | second-brain | llm-wiki | llmwiki | sage-wiki |
|---------|------|--------------|----------|---------|-----------|
| LLM-agnostic | ✅ | ❌ (AgentSkills) | ❌ (Claude Code) | ❌ (Claude MCP) | ✅ |
| Zero infrastructure | ✅ | ✅ | ✅ | ❌ (Supabase) | ❌ (Go binary) |
| Git-native | ✅ | Partial | Partial | ❌ | ✅ |
| Zero hallucination | ✅ | ❌ | ❌ | ❌ | ❌ |
| User-resolved conflicts | ✅ | ❌ | ❌ | ❌ | ❌ |
| L1/L2 architecture | ✅ | ❌ | ✅ | ❌ | ❌ |
| Prompt library | ✅ | Partial | Partial | ❌ | ✅ |

---

## Next Steps

1. Create folder structure
2. Write SCHEMA.md (the brain)
3. Write PROMPTS.md (copy-paste operations)
4. Write README.md (getting started)
5. Write GUIDE.md (deep dive)
6. Add example content
7. Initialize git with proper .gitignore
8. Test with actual ingest


---

Copyright (c) 2026 Joerg Peetz. All rights reserved.
