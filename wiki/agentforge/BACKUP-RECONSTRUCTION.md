# AgentForge — Complete Backup & Reconstruction Guide

_Last updated: 2026-05-26 22:45 Dublin | OpenClaw 2026.5.22 | Node v26 | Python 3.14_

**Purpose:** Rebuild the entire AgentForge multi-agent operation from a blank machine. Every department, every pipeline, every tool — in order, with exact paths, commands, and verification steps.

---

## 0. System State Snapshot

| Component | Version/Status | Notes |
|---|---|---|
| macOS | 24.6.0 (Darwin, x64) | Joerg's MacBook Pro |
| Node.js | v26.0.0 | `/usr/local/bin/node` |
| Python | 3.14.5 | `/usr/local/bin/python3` |
| Homebrew | 5.1.13 | Package manager |
| Git | 2.50.1 (Apple Git-155) | |
| Docker | 29.4.3 | Docker Desktop |
| uv | installed | `/Users/joergpeetz/.local/bin/uv` |
| Ollama | `gemma3:27b` | `http://127.0.0.1:11434` |
| OpenClaw | 2026.5.22 (a374c3a) | `/usr/local/lib/node_modules/openclaw` |

---

## 1. Install Order — Prerequisites

```bash
# 1. Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Node.js v26
brew install node@26
# Verify: node --version → v26.0.0

# 3. Python 3.14
brew install python@3.14
# Verify: python3 --version → Python 3.14.5

# 4. Git
brew install git
# Verify: git --version → 2.50+

# 5. Docker Desktop
brew install --cask docker
# Start Docker Desktop app, verify: docker --version → 29.4+

# 6. uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh
# Verify: ~/.local/bin/uv --version

# 7. Ollama (local LLM fallback)
brew install ollama
ollama pull gemma3:27b
# Verify: curl http://127.0.0.1:11434 → "Ollama is running"

# 8. OpenClaw (the agent runtime — DO THIS LAST among core tools)
npm install -g openclaw@2026.5.22
# Verify: openclaw --version → OpenClaw 2026.5.22
```

---

## 2. GitHub Repos — Clone & Restore

### 2.1 MeMex Zero RAG (INSTITUTIONAL MEMORY — CLONE FIRST)

```bash
cd ~/workspace
git clone https://github.com/JPeetz/MeMex-Zero-RAG.git
cd MeMex-Zero-RAG
# This is the canonical knowledge base. All agent configs, artifacts, and
# protocols live here. Everything else depends on it.
```

**What's inside:**
```
wiki/agentforge/
├── agents/           # Agent registry + playbooks
│   ├── *.md          # Registry docs per agent
│   ├── *-playbook.md # 7 department playbooks (learning loop)
│   └── skill-foundry/, advertisement/  # Agent subdirectories
├── articles/         # Pipeline article output
│   ├── *.md          # Published articles
│   └── images/       # Featured images
├── artifacts/        # All department outputs
│   ├── content/      # content.keyword + content.article JSON
│   ├── seo/          # SEO audit results
│   ├── social/       # Social distribution records
│   ├── pdf/          # PDF export records
│   ├── app-discovery/ # App scrutiny & scaffolding
│   ├── skill-foundry/  # Skill run reports
│   ├── prompts-foundry/  # Prompt run reports + seed tracker
│   └── advertisement/   # Ad campaign artifacts
├── decisions.md      # All CEO decisions (append-only log)
├── seo-patterns.md   # Accumulated SEO patterns
├── social-patterns.md    # Social distribution patterns
├── pipeline-log.md       # Pipeline run history
├── closed-learning-loop.md   # Learning loop design (checkboxes marked 2026-05-26)
├── standby-agents.md      # Agents awaiting activation
└── infrastructure-credentials.md  # Shared credential registry
```

### 2.2 Agent Skills Repository

```bash
cd ~/workspace
git clone https://github.com/JPeetz/agent-skills.git
# This is the published skills repo. The Skill Foundry pushes here.
```

### 2.3 SEO/GEO API

```bash
cd ~/workspace
git clone https://github.com/JPeetz/SEO-API.git seo-api
cd seo-api
npm install
# This is the Next.js SEO/GEO analysis tool running at seo-api-nu.vercel.app
# Local dev: npm run dev → http://localhost:3000
```

### 2.4 Obsidian Mind Vault

```bash
cd ~/workspace
git clone https://github.com/breferrari/obsidian-mind.git obsidian-mind-vault
# Reference only — not an active runtime dependency
```

### 2.5 AgentForge Research Swarm

```bash
cd ~/workspace
git clone https://github.com/VRSEN/OpenSwarm.git agentforge-research-swarm
# Reference only — Python research swarm framework
```

---

## 3. OpenClaw Agent Configs — Restore

All agent configs live at `~/.openclaw/agents/`. These must match the MeMex registry.

### 3.1 Active Agents (with cron jobs)

```bash
mkdir -p ~/.openclaw/agents
```

**Skill Foundry** (`~/.openclaw/agents/skill-foundry/AGENTS.md`):
```
# See full content at:
# https://github.com/JPeetz/MeMex-Zero-RAG/blob/main/wiki/agentforge/agents/skill-foundry.md
# Core: 8-phase pipeline (DISCOVER→EVALUATE→SELECT→IMPROVE→PACKAGE→VALIDATE→PUBLISH→MAINTAIN)
# 10-dimension scoring, nightly 02:00 Dublin, Flash model
# Outputs to ~/workspace/skills/[name]/SKILL.md
```

**Prompts Foundry** (`~/.openclaw/agents/prompts-foundry/AGENTS.md`):
```
# See: MeMex-Zero-RAG/wiki/agentforge/agents/prompts-foundry.md
# Core: Mirrors skill foundry, seed-first (52 existing prompts refactored first)
# 10-dimension scoring, nightly 01:00 Dublin, Flash model
# Outputs PROMPT.md format (text templates, NOT agent workflows)
# Clash prevention: never produce SKILL.md — that's skill foundry's territory
```

**App Discovery** (`~/.openclaw/agents/app-discovery/AGENTS.md`):
```
# Core: 6-phase mobile app discovery → scaffolding pipeline
# Daily 06:00-08:00 Dublin, agent: Alex, VP App Strategy
# HARD GATE: mobile-only apps, never web/SaaS
```

**Astra Ad Department** (`~/.openclaw/agents/advertisement/AGENTS.md`):
```
# Core: DIAGNOSE→RESEARCH→STRATEGIZE→CREATE→OPTIMIZE→QC→EXPORT
# On-demand, agent: Astra, Creative Director
```

**Content, SEO, Social, PDF, Analytics** — these are cron-driven pipelines without standalone AGENTS.md files. Their pipeline logic lives in the cron job payloads (see Section 5).

### 3.2 Workspace Files (RESTORE THESE)

These files define the CEO agent identity. They MUST be at `~/.openclaw/workspace/`:

| File | Purpose |
|---|---|
| `AGENTS.md` | CEO operating procedures, decision framework, memory architecture |
| `SOUL.md` | CEO identity — Marvin, CEO of AgentForge |
| `USER.md` | Joerg's preferences, communication style |
| `TOOLS.md` | Local infrastructure: SSH, Docker WP, n8n, fal.ai, SkillsMP, Ollama, SEO API, Superpowers |
| `MEMORY.md` | Curated long-term memory — decisions, patterns, directives |
| `HEARTBEAT.md` | CEO periodic check-ins: cross-dept pattern extraction, pipeline health, memory maintenance |
| `IDENTITY.md` | Agent identity fast-reference (name, role, departments) |

**These files are backed up in this GitHub repo. Restore them from:**
```
https://github.com/JPeetz/MeMex-Zero-RAG (or the original machine at ~/.openclaw/workspace/)
```

---

## 4. Memory Architecture — How It All Connects

### The Three-Layer System

```
┌─────────────────────────────────────────────┐
│  LAYER 1: MeMex Zero RAG (Primary)          │
│  ~/workspace/MeMex-Zero-RAG/wiki/agentforge/ │
│  Structured wiki, searchable, Git-backed    │
│  GitHub: JPeetz/MeMex-Zero-RAG              │
│  → ALL agents consult this first            │
├─────────────────────────────────────────────┤
│  LAYER 2: Obsidian Vault (Narrative)        │
│  ~/obsidian-vault/AgentForge/               │
│  Linked second brain, prompts inventory     │
│  → Consulted after MeMex                    │
├─────────────────────────────────────────────┤
│  LAYER 3: External (Web / AI)               │
│  web_search, web_fetch, SkillsMP API        │
│  → Only if 1 and 2 yield nothing            │
└─────────────────────────────────────────────┘

SHARED TRUTH: Filesystem + Git
- MeMex git is the canonical long-term memory
- Pushed to GitHub → disaster recovery source
- MEMORY.md is a local convenience cache (secondary)
```

### Consultation Order (HARD RULE — ALL AGENTS)

```
1. MeMex Zero RAG — structured wiki search
2. Obsidian vault — narrative linked notes
3. External — web search / AI query
```

### Playbook Learning System (Activated 2026-05-26)

```
Department Agent runs
  │
  ├─→ READS [dept]-playbook.md BEFORE starting
  │     (accumulated lessons from prior runs)
  │
  ├─→ EXECUTES pipeline
  │
  └─→ WRITES 1-3 lessons to [dept]-playbook.md AFTER completing
        │
        ↓ (weekly)
  Analytics Agent reads ALL playbooks
        │   detects cross-department patterns
        │   identifies failure clusters
        ↓
  CEO Heartbeat reads ALL playbooks every 4-6hrs
        │   escalates contradictions
        │   turns patterns into standing rules
        ↓
  AGENTS.md / cron payloads updated if needed
```

**Playbook files** (at `MeMex/agents/`):
- `content-playbook.md`
- `seo-playbook.md`
- `skill-foundry-playbook.md`
- `prompts-foundry-playbook.md`
- `analytics-playbook.md`
- `app-discovery-playbook.md`
- `advertisement-playbook.md`

---

## 5. Cron Jobs — Exact Schedule & Payloads

### 5.1 Content Pipeline (Mon-Fri 08:30 Dublin)

```
Job ID: e11f88c3-e588-40f9-a858-805ec76b0fd3
Name: content_pipeline_daily
Schedule: 30 8 * * 1-5 (Europe/Dublin)
Model: openrouter/deepseek/deepseek-v4-pro (thinking: medium)
Timeout: 1500s
Delivery: telegram → Joerg

Pipeline:
  1. READ content-playbook.md (accumulated lessons)
  2. Research keyword via SEO API
  3. Write content.keyword artifact → MeMex artifacts/content/
  4. Write SEO-optimized article with GEO requirements
  5. Craft image prompt → generate via image_generate
  6. Insert image into article
  7. Copy .md to ~/workspace/agentforge/pipeline/
  8. Copy image to ~/workspace/agentforge/pipeline/images/
  9. Generate PDF via reportlab script → ~/Documents/AgentForge/
  10. WRITE content-playbook.md (1-3 lessons)
  11. Commit to MeMex git
```

### 5.2 Skill Foundry (Nightly 02:00 Dublin)

```
Job ID: aac3a368-4307-4565-b6bf-5ef68a88009e
Name: skill_foundry_nightly
Schedule: 0 2 * * * (Europe/Dublin)
Model: openrouter/deepseek/deepseek-v4-flash
Timeout: 900s
Delivery: none (writes to MeMex)

Pipeline:
  1. READ skill-foundry-playbook.md
  2. Read prior run reports
  3. DISCOVER 10-15 candidates (web_search + SkillsMP API)
  4. EVALUATE 10-dimension scoring (kill floor 5/10)
  5. SELECT top 3-5
  6. IMPROVE each (7-step workflow)
  7. PACKAGE to ~/workspace/skills/[name]/SKILL.md
  8. WRITE run report to MeMex
  9. WRITE skill-foundry-playbook.md (1-3 lessons)
```

### 5.3 Prompts Foundry (Nightly 01:00 Dublin)

```
Job ID: f895ddc4-55a8-4167-b998-d6e3304ba22b
Name: prompts_foundry_nightly
Schedule: 0 1 * * * (Europe/Dublin)
Model: openrouter/deepseek/deepseek-v4-flash
Timeout: 900s
Delivery: none

Pipeline (SEED PHASE — until 52 prompts refactored):
  1. READ prompts-foundry-playbook.md
  2. Read seed-progress.json
  3. Read 3-5 prompts from ~/obsidian-vault/AgentForge/prompts/[category]/
  4. Apply 7-step improvement
  5. Package to PROMPT.md format
  6. Update seed-progress.json
  7. WRITE prompts-foundry-playbook.md (1-3 lessons)
  8. Write run report
```

### 5.4 Analytics (Monday 09:00 Dublin)

```
Job ID: 2430ef65-a0e6-4718-aa87-6e96fbe6975f
Name: analytics_weekly_report
Schedule: 0 9 * * 1 (Europe/Dublin)
Model: openrouter/deepseek/deepseek-v4-pro (thinking: high)
Timeout: 1800s
Delivery: telegram → Joerg

Pipeline:
  1. READ analytics-playbook.md
  2. Pull performance data from pipeline artifacts
  3. Top 5 / bottom 5 articles
  4. Niche refresh (external research)
  5. Update cluster map
  6. READ ALL 7 DEPARTMENT PLAYBOOKS — cross-dept pattern detection
  7. Synthesize recommendations
  8. Autonomous learning loop — drift detection, failure patterns
  9. WRITE analytics-playbook.md (1-3 lessons)
  10. Write weekly report artifact
```

### 5.5 Model Policy Review (May 31, 2026 08:00 UTC)

```
Job ID: e7021d89-2611-4358-a039-828b4af1cffa
Name: Model policy review
Schedule: at 2026-05-31T08:00:00.000Z
Model: openrouter/deepseek/deepseek-v4-pro
Delete after run: true
Delivery: telegram → Joerg
```

### How to Recreate Cron Jobs (OpenClaw CLI)

```bash
# Restore content pipeline
openclaw cron add --name "content_pipeline_daily" \
  --schedule "30 8 * * 1-5" --tz "Europe/Dublin" \
  --model "openrouter/deepseek/deepseek-v4-pro" \
  --thinking "medium" --timeout 1500 \
  --deliver "telegram:1948246956"

# Restore skill foundry
openclaw cron add --name "skill_foundry_nightly" \
  --schedule "0 2 * * *" --tz "Europe/Dublin" \
  --model "openrouter/deepseek/deepseek-v4-flash" \
  --timeout 900

# Restore prompts foundry
openclaw cron add --name "prompts_foundry_nightly" \
  --schedule "0 1 * * *" --tz "Europe/Dublin" \
  --model "openrouter/deepseek/deepseek-v4-flash" \
  --timeout 900

# Restore analytics
openclaw cron add --name "analytics_weekly_report" \
  --schedule "0 9 * * 1" --tz "Europe/Dublin" \
  --model "openrouter/deepseek/deepseek-v4-pro" \
  --thinking "high" --timeout 1800 \
  --deliver "telegram:1948246956"
```

> **Note:** Exact payload messages are stored in MeMex git history. After restoring cron structure, copy payloads from the MeMex backup or reconstruct from this document's descriptions above.

---

## 6. Skills Inventory — 32 Shipped

All skills at `~/.openclaw/workspace/skills/`:

### AgentForge Native (18 skills)
| Skill | Category |
|---|---|
| agent-orchestration | AI Engineering |
| api-design | Development |
| app-discovery-scrutiny | Mobile |
| app-scaffolding | Mobile |
| astra-campaign | Advertising |
| cli-anything-hub | Infrastructure |
| code-review | Development |
| content-strategy-multi-platform | Content |
| data-pipeline | Data Engineering |
| deployment-automation | DevOps |
| documentation-generation | Documentation |
| git-workflow | Development |
| knowledge-management-vault | Knowledge |
| n8n-workflow-automation | Automation |
| prompt-engineering | AI |
| security-auditing | Security |
| seo-geo-optimization | SEO |
| systematic-debugging | Development (duplicate) |
| testing-methodology | Testing |

### Superpowers Framework (13 skills from obra/superpowers)
| Skill | Category |
|---|---|
| brainstorming | Methodology |
| dispatching-parallel-agents | Agent Orchestration |
| executing-plans | Methodology |
| finishing-a-development-branch | Git |
| receiving-code-review | Methodology |
| requesting-code-review | Methodology |
| subagent-driven-development | Methodology |
| systematic-debugging | Methodology |
| test-driven-development | Methodology |
| using-git-worktrees | Git |
| verification-before-completion | Methodology |
| writing-plans | Methodology |
| writing-skills | Methodology |

### Restore Superpowers

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/obra/superpowers.git superpowers
# Skills are at superpowers/skills/[name]/SKILL.md
```

---

## 7. Pipeline Scripts

All at `~/workspace/agentforge/pipeline/scripts/`:

| Script | Purpose |
|---|---|
| `article-to-pdf.py` | reportlab-based styled PDF generator. A4, proper typography, embedded images, tables, code blocks. Uses venv at `~/workspace/agentforge/.venv` |
| `seo-check.py` | SEO quality gate |
| `citation-check.py` | Citation verification |
| `gen-hero-img.py` | Hero image generation (legacy) |
| `generate-image.py` | Image generation |
| `geo-audit-draft.py` | GEO structural audit |
| `geo-eval-check.py` | GEO evaluation |
| `geo-quick-check.py` | Quick GEO check |
| `seo_api_client.py` | SEO API client library |
| `wordcount.py` | Article word count |

### Restore PDF venv

```bash
cd ~/workspace/agentforge
uv venv
source .venv/bin/activate
uv pip install reportlab pillow
# Verify: python3 pipeline/scripts/article-to-pdf.py --help
```

---

## 8. External APIs & Credentials

All credentials live in three synchronized files:
- `~/workspace/TOOLS.md` (workspace convenience)
- `~/obsidian-vault/AgentForge/infrastructure/credentials.md` (narrative vault)
- `~/workspace/MeMex-Zero-RAG/wiki/agentforge/infrastructure-credentials.md` (structured wiki)

### API Inventory

| Service | URL | Auth | Notes |
|---|---|---|---|
| **OpenRouter** | api.openrouter.ai | API key (in .env) | DeepSeek V4 Pro + Flash models |
| **SkillsMP** | skillsmp.com/api/v1 | Bearer token (TOOLS.md) | 500 req/day, 30/min |
| **SEO/GEO API** | seo-api-nu.vercel.app | None (open) | Keyword density, readability, meta tags, SERP, GEO, E-E-A-T |
| **fal.ai Flux** | queue.fal.run/fal-ai/flux/schnell | Key pair (TOOLS.md) | Image generation, ~0.3s inference |
| **n8n** | jpeetzn8n.xyz | JWT (TOOLS.md) | 101 workflows, 26 MCP tools |
| **WordPress** | localhost:80 (Docker) | jpeetz / Buddy-2019 | Local dev |
| **Ollama** | 127.0.0.1:11434 | None | gemma3:27b local fallback |
| **Notion** | api.notion.com | Token (TOOLS.md) | |
| **GitHub** | github.com/JPeetz | git credential | MeMex, agent-skills, seo-api repos |

### Services to Verify

```bash
# After restore, verify each service is reachable:
curl -s https://seo-api-nu.vercel.app/ | grep "SEO"            # SEO API
curl -s https://skillsmp.com/api/v1/skills/search?q=test \
  -H "Authorization: Bearer $SKILLSMP_KEY" | head -1          # SkillsMP
curl -s http://localhost:80 | grep -i wordpress                # WordPress
curl -s https://jpeetzn8n.xyz | head -1                        # n8n
curl -s http://127.0.0.1:11434                                 # Ollama
docker ps                                                       # Docker containers
```

---

## 9. Obsidian Vault — Restore

```bash
# The Obsidian vault should exist at ~/obsidian-vault/AgentForge/
# This is a local directory (not yet Git-backed)
# Restore from backup or mirror from MeMex

# Key structure:
# ~/obsidian-vault/AgentForge/
# ├── prompts/           # 52 prompt files across 18 categories
# │   ├── openclaw/      # 14 prompts
# │   ├── coding/        # 10 prompts
# │   ├── hermes/        # 7 prompts
# │   ├── agent-swarms/  # 5 prompts
# │   ├── research/      # 3 prompts
# │   ├── email-calendar/# 3 prompts
# │   ├── content-creation/# 3 prompts
# │   ├── claude-code/   # Claude-specific prompts
# │   ├── codex-cli/     # Codex-specific prompts
# │   ├── image-generation/
# │   ├── video-gen/
# │   ├── voice-tts/
# │   ├── trading/
# │   └── ... (18 total categories)
# ├── agents/            # Agent registry mirrors
# ├── articles/          # Published article mirrors
# ├── artifacts/         # Department artifacts
# ├── infrastructure/    # Credentials
# ├── protocols/         # Agent handoff, decision protocols
# ├── departments/       # Department guides
# ├── decisions/         # Decision log mirrors
# ├── research/          # External research
# └── weekly-reports/    # Analytics weekly reports
```

> **Note:** Prompts Foundry reads the 52 prompts from Obsidian during seed phase. Ensure this path exists and is populated.

---

## 10. Docker WordPress (Local Dev)

```bash
# WordPress runs locally on port 80
# Admin: http://localhost/wp-admin
# User: jpeetz | Pass: Buddy-2019 | Email: j.peetz69@gmail.com

# If Docker container is missing, restore:
docker run -d \
  --name wordpress \
  -p 80:80 \
  -e WORDPRESS_DB_HOST=db \
  -e WORDPRESS_DB_USER=wordpress \
  -e WORDPRESS_DB_PASSWORD=wordpress \
  -e WORDPRESS_DB_NAME=wordpress \
  wordpress:latest

# Also needs MySQL container:
docker run -d \
  --name db \
  -e MYSQL_ROOT_PASSWORD=somewordpress \
  -e MYSQL_DATABASE=wordpress \
  -e MYSQL_USER=wordpress \
  -e MYSQL_PASSWORD=wordpress \
  mysql:5.7
```

---

## 11. n8n Automation

```bash
# n8n runs at https://jpeetzn8n.xyz
# 101 workflows, 26 MCP tools
# JWT auth (stored in TOOLS.md)
# MCP server at https://jpeetzn8n.xyz/mcp-server/http

# If self-hosted n8n is needed:
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  -e N8N_SECURE_COOKIE=false \
  n8nio/n8n:latest
```

---

## 12. Model Policy

| Use Case | Model | Why |
|---|---|---|
| Content Pipeline (article writing) | deepseek-v4-pro | Quality-critical, SEO + GEO generation |
| Skill Foundry | deepseek-v4-flash | Cost-efficient, throughput work |
| Prompts Foundry | deepseek-v4-flash | Cost-efficient, prompt text refactoring |
| Analytics | deepseek-v4-pro | Complex cross-dept analysis |
| CEO / Board communication | deepseek-v4-pro | Strategic decisions |
| Image generation | Gemini Flash / fal.ai Flux | Images only |
| Local fallback | gemma3:27b (Ollama) | When APIs unavailable |

**Board policy:** Review May 31, 2026. Current split preserved until then.

---

## 13. Department Map — Who Does What

| Department | Agent Config | Cron Job | Model | Output |
|---|---|---|---|---|
| **CEO** | main (Marvin) | Heartbeat | deepseek-v4-pro | Decisions, orchestration |
| **Content** | cron-based | Mon-Fri 08:30 | deepseek-v4-pro | Articles + PDFs → ~/Documents/AgentForge/ |
| **SEO** | cron-based (via content) | With content pipeline | — | SEO audit artifacts |
| **Skill Foundry** | ~/.openclaw/agents/skill-foundry/ | Nightly 02:00 | deepseek-v4-flash | SKILL.md to ~/workspace/skills/ |
| **Prompts Foundry** | ~/.openclaw/agents/prompts-foundry/ | Nightly 01:00 | deepseek-v4-flash | PROMPT.md to MeMex |
| **Analytics** | cron-based | Monday 09:00 | deepseek-v4-pro | Weekly report + playbook analysis |
| **Social** | cron-based (on-demand) | Post-publication | — | Social distribution |
| **PDF** | cron-based (via content) | With content pipeline | — | PDF generation |
| **App Discovery** | ~/.openclaw/agents/app-discovery/ | On-demand | deepseek-v4-pro | App scrutiny + scaffolding |
| **Astra Ad Dept** | ~/.openclaw/agents/advertisement/ | On-demand | deepseek-v4-pro | Campaign creation |
| **Hiring** | Standby | — | — | Agent design + adversarial review |
| **WP Design** | Standby | — | — | WordPress theme design |
| **Research** | Standby | — | — | External analysis |
| **Prompts** | → Prompts Foundry | Activated 2026-05-26 | — | Prompt bundling |

---

## 14. GitHub Repo Creation Policy

| Milestone | Action |
|---|---|
| 50 skills shipped | Create AgentForge/skills GitHub repo |
| 100 skills + site | WP Design builds wp website (Flux images, competitor-inspired design) |
| 50 prompts shipped | Create AgentForge/prompts GitHub repo |
| 100 prompts + site | Same website treatment |

**All repos MUST have (created first, then updated every run):**
- `README.md` — keyword-rich, comparison tables, install one-liner, platform matrix, FAQ
- `CHANGELOG.md` — semantic versioning, per-run entries
- `DEVLOG.md` — narrative development history

---

## 15. CEO Decision Log

All CEO-level decisions are logged to two places:
1. `~/workspace/MeMex-Zero-RAG/wiki/agentforge/decisions.md` (primary)
2. `~/workspace/MEMORY.md` (convenience cache)

**How to log a decision:**
```bash
echo "- [$(date '+%Y-%m-%d')] [DECISION]: [what was decided and why]" \
  >> ~/workspace/MeMex-Zero-RAG/wiki/agentforge/decisions.md
```

---

## 16. Key Decisions (2026-05)

| Date | Decision |
|---|---|
| 2026-05-21 | CEO role activated. MeMex + Obsidian = canonical long-term memory for all agents. |
| 2026-05-21 | SkillsMP API available for all agents. Superpowers framework available for all agents. |
| 2026-05-22 | Infrastructure credentials centralized in TOOLS.md, Obsidian, and MeMex. |
| 2026-05-23 | SEO FLAG (50-69) triggers auto-revision cycle. Content agent revises → SEO re-audits. Loop until PASS. Escalate only after 3 consecutive FLAGs. |
| 2026-05-23 | Universal Standing Order: If any chat surface compresses context, write state to memory immediately. Never lose context to truncation. |
| 2026-05-24 | Astra Ad Department created (7-phase campaign pipeline). |
| 2026-05-24 | Closed Learning Loop designed. |
| 2026-05-25 | Skill Foundry activated. Nightly 02:00, Flash model. Omni-Skills-Forge competitive analysis complete. |
| 2026-05-26 | Pipeline fixed: image generation (Flux fal.ai) + PDF via reportlab + copy to ~/Documents/AgentForge/. |
| 2026-05-26 | MeMex duplication fixed: ~/.openclaw/workspace/MeMex-Zero-RAG → symlink to ~/workspace/MeMex-Zero-RAG. |
| 2026-05-26 | Prompts Foundry activated. Seed-first (52 existing prompts), nightly 01:00, Flash model. Clash prevention boundary with Skill Foundry. |
| 2026-05-26 | Playbook learning system activated. 7 department playbooks. All cron jobs read playbook first, write lessons after. CEO heartbeat cross-dept extraction. |

---

## 17. Disaster Recovery — Step-by-Step

### What to do if the machine dies:

1. **Install base tools** (Section 1 above): Homebrew → Node → Python → Git → Docker → uv → Ollama → OpenClaw
2. **Clone MeMex:** `git clone https://github.com/JPeetz/MeMex-Zero-RAG.git ~/workspace/MeMex-Zero-RAG`
3. **Clone agent-skills:** `git clone https://github.com/JPeetz/agent-skills.git ~/workspace/agent-skills`
4. **Clone seo-api:** `git clone https://github.com/JPeetz/SEO-API.git ~/workspace/seo-api`
5. **Restore workspace files:** Copy AGENTS.md, SOUL.md, USER.md, TOOLS.md, MEMORY.md, HEARTBEAT.md, IDENTITY.md from MeMex backup to `~/.openclaw/workspace/`
6. **Restore agent configs:** Copy agent directories from MeMex backup to `~/.openclaw/agents/`
7. **Restore Obsidian vault:** Copy from backup to `~/obsidian-vault/AgentForge/`
8. **Recreate cron jobs** (Section 5)
9. **Restore PDF venv** (Section 7)
10. **Verify all services** (Section 8)
11. **Run a test content pipeline** to verify end-to-end
12. **Restore Docker WordPress** (Section 10)

### What to do if OpenClaw goes down:

OpenClaw is installed globally via npm. Reinstall:
```bash
npm install -g openclaw@2026.5.22
openclaw gateway start
```

### What to do if MeMex git is corrupted locally:

```bash
rm -rf ~/workspace/MeMex-Zero-RAG
git clone https://github.com/JPeetz/MeMex-Zero-RAG.git ~/workspace/MeMex-Zero-RAG
# Recreate the .openclaw symlink:
ln -s ~/workspace/MeMex-Zero-RAG ~/.openclaw/workspace/MeMex-Zero-RAG
```

### What to do if memory is lost (context compression):

All agents follow the Universal Standing Order (2026-05-23):
> If either chat surface compresses context, write state to memory immediately. Never lose context to truncation without a filesystem backup.

The filesystem is the shared truth. Re-read from MeMex + Obsidian + MEMORY.md.

---

## 18. Git Remotes — Quick Reference

```bash
# Push MeMex (institutional memory)
cd ~/workspace/MeMex-Zero-RAG && git push origin main

# Push agent-skills (published skills)
cd ~/workspace/agent-skills && git push origin main

# Push SEO API
cd ~/workspace/seo-api && git push origin main
```

---

## 19. Daily/Weekly Run Schedule (Dublin Time)

```
01:00 — Prompts Foundry (Flash, 15min timeout)
02:00 — Skill Foundry (Flash, 15min timeout)
06:00 — App Discovery (on-demand days)
08:30 — Content Pipeline (V4 Pro, 25min timeout) → Telegram delivery
09:00 — Analytics Monday (V4 Pro, 30min timeout) → Telegram delivery
HEARTBEAT — CEO every 4-6 hours (playbook scan + pipeline health)
```

---

## 20. Key Paths — Quick Reference

| What | Where |
|---|---|
| MeMex (canonical) | `~/workspace/MeMex-Zero-RAG/wiki/agentforge/` |
| MeMex (symlink) | `~/.openclaw/workspace/MeMex-Zero-RAG/` → above |
| Obsidian vault | `~/obsidian-vault/AgentForge/` |
| Agent configs | `~/.openclaw/agents/[name]/AGENTS.md` |
| Workspace files | `~/.openclaw/workspace/` |
| Skills (shipped) | `~/.openclaw/workspace/skills/[name]/SKILL.md` |
| Pipeline scripts | `~/workspace/agentforge/pipeline/scripts/` |
| Article output | `~/Documents/AgentForge/YYYY-MM-DD-[slug].{md,pdf}` |
| Memory (daily) | `~/workspace/memory/YYYY-MM-DD.md` |
| Memory (long-term) | `~/workspace/MEMORY.md` |
| Heartbeat | `~/workspace/HEARTBEAT.md` |
| User model | `~/workspace/memory/user-model.md` |
| Agent reflections | `~/workspace/memory/agent-reflections/` |
| Playbooks (7 dept) | `~/workspace/MeMex-Zero-RAG/wiki/agentforge/agents/*-playbook.md` |
| Articles (MeMex) | `~/workspace/MeMex-Zero-RAG/wiki/agentforge/articles/` |
| Article images | `~/workspace/MeMex-Zero-RAG/wiki/agentforge/articles/images/` |
| SEO API local | `~/workspace/seo-api/` |
| Docker WP | `localhost:80` |
| n8n | `https://jpeetzn8n.xyz` |
| Ollama | `http://127.0.0.1:11434` |
| Superpowers | `~/.openclaw/workspace/skills/superpowers/` |

---

## 21. This Document

This document is the single source of truth for rebuilding AgentForge. Update it when:
- New departments are added
- Cron jobs change
- Credentials rotate
- Infrastructure moves
- Major decisions are made

**Commit it to MeMex:**
```bash
cp ~/Desktop/AgentForge-BACKUP-RECONSTRUCTION.md \
  ~/workspace/MeMex-Zero-RAG/wiki/agentforge/BACKUP-RECONSTRUCTION.md
cd ~/workspace/MeMex-Zero-RAG
git add wiki/agentforge/BACKUP-RECONSTRUCTION.md
git commit -m "docs: full backup & reconstruction guide"
git push origin main
```

---

_AgentForge. OpenClaw native. No Hermes. No ClaudeClaw. Built fresh, documented thoroughly._