# Research: awesome-claude (HeyClaude) Registry — Community Resource Directory

**Date:** 2026-05-19
**Status:** ✅ Complete
**Relevance:** Skill library patterns, agent best practices, tool taxonomy, industry benchmarks

---

## Executive Summary

HeyClaude (awesome-claude) is an unofficial, community-built directory of 385+ Claude-related resources organized into 10 categories. It functions as a searchable registry for AI agents, MCP servers, tools, skills, rules, commands, hooks, guides, collections, and statusline scripts. The repository is file-backed (assets stored as individual files), searchable via website and API, and distributed through multiple channels (web, RSS, API, Raycast extension).

**Key Value:** Benchmarking against industry standards—what agents/skills/tools already exist in the Claude ecosystem that AgentForge should learn from or integrate with.

---

## Registry Structure (385+ Entries)

### Category 1: AI Agents (39 entries)

**Types:**
- **Code agents:** Code review, DevOps, database management
- **Research agents:** Market research, trend analysis
- **Content agents:** Article writing, SEO optimization
- **Orchestration:** Multi-agent coordination, workflow automation

**Examples:**
- `codebuff` — Multi-agent code generation
- `cline` — Claude IDE integration
- `aider` — Pair programmer
- `crewai` — Multi-agent orchestration framework

**Insights for AgentForge:**
- Agent specialization is proven (14 agents is reasonable scope)
- Each agent should have a clear capability statement
- Consider integrating with Cline (IDE integration) for developer workflows

### Category 2: MCP Servers (49 entries)

**Purpose:** Model Context Protocol servers that extend Claude's capabilities

**Common Integrations:**
- **Data sources:** Airtable, Notion, Slack, GitHub, Stripe
- **Cloud services:** AWS, GCP, Azure
- **Productivity:** Linear, Asana, Jira
- **Communication:** Gmail, Slack, Discord

**Insights for AgentForge:**
- Hive Mind should surface available MCP context to agents
- Research agent could query Notion + GitHub MCP servers before starting
- Content agent could pull from Slack discussions via MCP before writing

**Schema Recommendation:**
```javascript
// In agent.yaml
mcp_servers: [
  { name: 'github', capabilities: ['read_repos', 'search_issues', 'list_prs'] },
  { name: 'notion', capabilities: ['read_databases', 'search_pages'] },
  { name: 'slack', capabilities: ['read_messages', 'search_channel'] }
]
```

### Category 3: Tools (52 entries)

**Categories:**
- **IDE Integration:** Cursor, VSCode extensions
- **Automation:** LangGraph, AutoGen, n8n
- **Monitoring:** Sentry, DataDog, New Relic
- **Testing:** Playwright, Selenium, Cypress

**Insights for AgentForge:**
- Integration with Cursor/VSCode extends developer workflow
- LangGraph patterns inform multi-agent orchestration
- Monitoring/testing tools should be available to Ops agent

### Category 4: Skills (68 entries)

**Taxonomy:**
- **Audio/Video:** Transcription, video understanding
- **Browser:** Automation, scraping, filling forms
- **Code:** Testing, linting, deployment
- **Smart Contracts:** Solidity, Web3
- **Document:** PDF processing, extraction

**Examples of Skill Naming:**
- `transcribe-audio` — Speech to text
- `analyze-video` — Video understanding
- `automate-browser` — Puppeteer/Playwright
- `extract-pdf` — Document processing

**Insights for AgentForge:**
- Skills follow `verb-noun` pattern (noun = domain)
- Each skill should be one focused capability
- Skills are reusable across agents

**Comparison: Skills vs. Agent Tools**
| Aspect | Skill | Agent Tool |
|--------|-------|-----------|
| **Scope** | Single focused capability | Agent-specific utility |
| **Reusability** | Global (all agents) | Agent-specific |
| **Invocation** | Via skill CLI or API | Via agent.tools object |
| **Examples** | transcribe-audio, extract-pdf | research.findArticles(), ops.deployDocker() |

**For AgentForge:**
- Implement global skills for cross-agent use (transcribe, pdf-extract, web-scrape)
- Keep agent-specific tools in agent.tools{}
- Skills go in `~/.claude/skills/`; agent tools in `agents/{id}/tools.js`

### Category 5: Rules (29 entries)

**Purpose:** Prompt guardrails and operating constraints

**Examples:**
- No code execution without approval
- Escalate security decisions
- Maintain audit trail
- Human approval for high-impact changes

**Insights for AgentForge:**
- Should be codified in agent.js as guardrails
- CEO agent needs strict rules (escalation, audit trail)
- Ops agent needs security rules (no destructive commands without approval)

**Implementation:**
```javascript
// In agent.js
const RULES = {
  financial: {
    max_spend_per_mission: 1000,
    escalate_above: 10000,
    require_approval: true
  },
  security: {
    allow_destructive: false,
    allow_aws_delete: false,
    require_audit_log: true
  },
  content: {
    require_citations: true,
    min_sources: 3,
    plagiarism_check: true
  }
};

async executeMission(missionId, prompt) {
  // Check rules before execution
  this.validateRules(missionId, RULES);
  // ... execute mission
}
```

### Category 6: Commands (27 entries)

**Purpose:** Slash commands and reusable prompts

**Examples:**
- `/summarize` — TLDR of document
- `/analyze-code` — Code review + suggestions
- `/research` — Deep dive on topic
- `/brainstorm` — Creative ideation
- `/debug` — Systematic problem solving

**Insights for AgentForge:**
- Commands should map to agent capabilities
- Research agent could have `/research` command
- Content agent could have `/draft-article` command
- CLI should expose these via mission CLI

**Implementation in AgentForge:**
```bash
# Mission CLI could support shortcuts
./mission-cli.js /research "AI agent architecture"
# → Creates research mission automatically

./mission-cli.js /draft-article "Best practices for LLMs"
# → Creates content mission automatically

./mission-cli.js /analyze-code "src/agent-framework.js"
# → Creates code review mission automatically
```

### Category 7: Hooks (66 entries)

**Purpose:** Claude Code automation configurations

**Triggers:**
- On file save
- On commit
- On PR creation
- On test failure
- On deployment

**Examples:**
- `auto-format-on-save` — Prettier/Black
- `run-tests-before-commit` — Pre-commit hook
- `auto-review-on-pr` — Code review automation
- `notify-on-deploy` — Slack notification

**Insights for AgentForge:**
- Hooks could trigger missions (PR created → code review mission)
- Executor could auto-escalate on test failure
- Hive Mind could log hook triggers

**Schema for Hooks:**
```yaml
# agents/ops/hooks.yaml
hooks:
  - trigger: "on_pr_created"
    action: "create_mission"
    agent: "code_review"
    priority: 8

  - trigger: "on_test_failure"
    action: "escalate_to_human"
    severity: "high"

  - trigger: "on_deployment"
    action: "notify_slack"
    channel: "#deployments"
```

### Category 8: Guides (19 entries)

**Topics:**
- Agent architecture patterns
- Prompt engineering best practices
- Multi-agent orchestration
- Error handling and recovery
- Performance optimization

**Insights for AgentForge:**
- Should document architecture in similar style
- Create guides for each agent's workflow
- Document common failure modes and recovery

### Category 9: Collections (10 entries)

**Purpose:** Curated bundles of related assets

**Examples:**
- "AI Agent Starter Pack" (5 agents + tools)
- "Content Creation Suite" (3 content agents + skills)
- "DevOps Automation" (ops agent + docker/k8s tools)

**Insights for AgentForge:**
- Could package agents by department (Content Collection, Ops Collection)
- Collections make it easy to onboard new users
- Each collection has README, setup guide, examples

### Category 10: Statuslines (26 entries)

**Purpose:** Workflow telemetry scripts

**Examples:**
- Token usage monitoring
- Context window status
- Mission queue depth
- Agent utilization %
- Cost tracking (USD/session)

**Insights for AgentForge:**
- Should implement statusline for executor health
- Show token usage per agent
- Track mission success rate by agent
- Monitor executor uptime

**Example Statusline Implementation:**
```bash
#!/bin/bash
# ~/.claude/statuslines/agentforge-executor.sh

db="/path/to/store/claudeclaw.db"

# Mission queue status
queued=$(sqlite3 "$db" "SELECT COUNT(*) FROM mission_tasks WHERE status='queued';")
running=$(sqlite3 "$db" "SELECT COUNT(*) FROM mission_tasks WHERE status='running';")
completed=$(sqlite3 "$db" "SELECT COUNT(*) FROM mission_tasks WHERE status='completed';")

# Executor health
executor_pid=$(pgrep -f "native-agent-executor.js")
uptime=$(ps -p $executor_pid -o etime= | tr -d ' ')

# Token usage (last 24h)
tokens=$(sqlite3 "$db" "SELECT SUM(output_tokens) FROM token_usage WHERE created_at > (SELECT MAX(created_at) - 86400 FROM token_usage);")

echo "Executor: $executor_pid | Queue: $queued | Running: $running | Done: $completed | Uptime: $uptime | Tokens (24h): $tokens"
```

---

## Distribution Channels

1. **Website:** heyclau.de (searchable directory)
2. **GitHub:** JSONbored/awesome-claude (file-backed)
3. **API:** `https://api.heyclau.de/` (query resources programmatically)
4. **RSS/Atom:** Subscribe to new entries by category
5. **Raycast Extension:** Quick access from command palette

**For AgentForge:**
- Should be discoverable in HeyClaude (submit as agent entry)
- Could provide API for agents to query skill/tool catalog
- Could provide Raycast extension for quick mission creation

---

## Benchmarking AgentForge Against Industry

### Agent Specialization
- **Codebuff:** 4 agents (focused on code)
- **CrewAI:** Unlimited (framework)
- **AgentForge:** 14 agents (department-based) ✅ Optimal

### Capability Documentation
- **Industry Standard:** Each agent has README with:
  - What it does
  - What it needs (inputs)
  - What it produces (outputs)
  - Integration examples

**AgentForge Status:**
- ✅ agent.yaml has metadata
- ✅ agent.js has implementation
- ⚠️ Missing: Detailed README per agent
- ⚠️ Missing: Integration examples

**Recommendation:**
```
agents/
├── research/
│   ├── README.md          # ← Add this
│   ├── CLAUDE.md
│   ├── agent.yaml
│   ├── agent.js
│   └── tools.js
```

### MCP Server Integration
- **Industry:** Agents query external MCP servers
- **AgentForge:** Currently isolated
- **Recommendation:** Extend agents to query:
  - GitHub MCP (for repo info)
  - Notion MCP (for documentation)
  - Slack MCP (for team context)

### Skill Library
- **Industry:** 50+ community skills
- **AgentForge:** Zero global skills (all embedded in agents)
- **Recommendation:** Extract reusable skills:
  - `web-scrape` — used by research, seo, niche-scout
  - `extract-pdf` — used by pdf, content
  - `analyze-sentiment` — used by social, hiring

---

## Industry Benchmarks (as of May 2026)

| Metric | Codebuff | CrewAI | AgentForge |
|--------|----------|--------|-----------|
| **Specialized Agents** | 4 | Unlimited | 14 |
| **Agent Types** | Code-focused | Multi-domain | Department-based |
| **Handoff Protocol** | Structured JSON | Task-based | Hive Mind (planned) |
| **Confidence Scoring** | Per-agent | Per-task | Per-signal (planned) |
| **MCP Integration** | No | Yes | No (planned) |
| **Global Skills** | No | No | No (planned) |
| **Community Registry** | No | Yes | No (planned) |
| **Open Source** | Yes | Yes | Yes |
| **Self-Hostable** | Yes | Yes | Yes |

---

## Recommendations for AgentForge Community & Discoverability

### 1. **Submit to HeyClaude**
```yaml
# Entry for awesome-claude
name: AgentForge
category: AI Agents / Multi-Agent Orchestration
description: Self-hosted department-based agent system with native Claude SDK
github: https://github.com/joergpeetz/claudeclaw
docs: /wiki/agentforge/
features:
  - 14 specialized agents (research, ops, design, content, etc.)
  - Native Claude Agent SDK (no external frameworks)
  - Hive Mind cross-agent learning
  - Mission queue with SQ Lite persistence
  - Telegram bot interface
license: MIT
stars: ⭐
```

### 2. **Create README per Agent**
```markdown
# Research Agent

**Capability:** Deep-dive research, market analysis, trend synthesis

**Inputs:**
- Research topic/prompt
- Context from related missions
- Available MCP servers (GitHub, Notion)

**Outputs:**
- Synthesized research document
- Confidence score (0-1)
- Sources and citations
- Related findings

**Example Mission:**
```bash
./mission-cli.js create --agent research "Market trends in AI agents"
```

**Integration:**
- CEO agent spawns research for strategic decisions
- Content agent uses research for article background
- Niche Scout agent bases market analysis on research
```

### 3. **Create Skill Library**
Extract common tools into global skills:
```bash
~/.claude/skills/
├── web-scrape/
├── pdf-extract/
├── sentiment-analysis/
├── keyword-research/
└── video-analysis/
```

### 4. **Hooks for Mission Automation**
```yaml
# .claude/hooks/agentforge.yaml
hooks:
  - event: "github.pull_request.opened"
    mission: "code_review"
    agent: "research"
    priority: 8

  - event: "slack.message_mention"
    mission: "quick_research"
    agent: "research"
    priority: 6

  - event: "notion.page_update"
    mission: "content_sync"
    agent: "content"
    priority: 5
```

---

## References

- **GitHub:** [JSONbored/awesome-claude](https://github.com/JSONbored/awesome-claude)
- **Website:** https://heyclau.de
- **API:** https://api.heyclau.de/
- **Raycast Extension:** heyclau.de (Raycast marketplace)

---

**Completed:** 2026-05-19 18:55 UTC
**Next Action:** Update agent READMEs, extract global skills, submit AgentForge to HeyClaude registry

