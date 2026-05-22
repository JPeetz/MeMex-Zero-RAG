# Research: Codebuff Multi-Agent Architecture & Agent Handoff Patterns

**Date:** 2026-05-19
**Status:** ✅ Complete
**Relevance:** Agent coordination patterns, specialized agent workflows, multi-step task decomposition

---

## Executive Summary

Codebuff is an open-source, terminal-based AI coding assistant that uses a **multi-agent architecture** to coordinate specialized agents (File Picker, Planner, Editor, Reviewer) rather than relying on a monolithic single-agent prompt loop. This design enables better project understanding, more accurate edits, and fewer errors when generating or modifying code.

**Key Innovation:** Agent handoff protocol where each agent passes structured context to the next agent in the pipeline, enabling task decomposition without losing project understanding.

---

## Multi-Agent Architecture

### Agent Roles & Responsibilities

```
User Request
    ↓
File Picker Agent → Planner Agent → Editor Agent → Reviewer Agent → Output
    ↓                 ↓               ↓                ↓
Identify relevant  Plan changes    Apply edits     Verify quality
files in codebase  in sequence     to files        & consistency
```

#### 1. **File Picker Agent**
**Responsibility:** Understand project structure and identify affected files

**Process:**
- Scans project architecture (package dependencies, file organization)
- Reads directory structure and file types
- Analyzes current codebase patterns
- Outputs: List of files to modify, in priority order

**Context Passed to Next Agent:**
```json
{
  "relevant_files": ["src/auth.ts", "src/api/login.ts", "tests/auth.test.ts"],
  "project_architecture": {
    "structure": "monorepo with src/, tests/, docs/",
    "patterns": "TypeScript, Jest for testing",
    "dependencies": ["express", "jsonwebtoken", "bcrypt"]
  }
}
```

**Key Insight for AgentForge:**
- Research agent should have a "context-gathering" phase before starting research
- File picker pattern = identify relevant knowledge sources before synthesizing

#### 2. **Planner Agent**
**Responsibility:** Determine the sequence and scope of changes

**Process:**
- Reviews file picker output
- Plans which files change first (dependencies matter)
- Defines change scope for each file
- Identifies potential conflicts or interdependencies
- Outputs: Detailed change plan with sequence

**Context Passed to Next Agent:**
```json
{
  "changes": [
    {
      "file": "src/auth.ts",
      "changes": ["Add JWT validation function", "Export new validateToken()"],
      "sequence": 1,
      "dependencies": []
    },
    {
      "file": "src/api/login.ts",
      "changes": ["Add token verification", "Update error handling"],
      "sequence": 2,
      "dependencies": ["auth.ts"]
    }
  ]
}
```

**Key Insight for AgentForge:**
- Mission decomposition: Complex missions should have a "planner" step
- Content agent: Draft outline before writing full article
- Operations agent: Plan rollout sequence before executing

#### 3. **Editor Agent**
**Responsibility:** Apply the planned changes to files

**Process:**
- Receives planner output with specific changes
- Generates code for each change
- Respects existing code style and patterns
- Applies changes in sequence (respects dependencies)
- Outputs: Modified files

**Context Needed:**
- The file itself (not just the request)
- Existing code style/patterns
- Change plan from planner
- Dependencies from previous changes

**Key Insight for AgentForge:**
- Agents should receive full context of dependencies before executing
- Style consistency matters (use existing patterns from hive_mind)
- Sequential execution respects interdependencies

#### 4. **Reviewer Agent**
**Responsibility:** Verify quality, consistency, and correctness

**Process:**
- Reviews all changes against original request
- Checks for style consistency
- Verifies dependencies are satisfied
- Tests modifications (if possible)
- Identifies issues for human review

**Outputs:**
```json
{
  "status": "approved" | "needs_fixes" | "human_review",
  "issues": [
    {
      "file": "src/api/login.ts",
      "line": 45,
      "issue": "Missing error handling for jwt.verify()",
      "severity": "high"
    }
  ],
  "confidence": 0.92
}
```

**Key Insight for AgentForge:**
- Every agent output should have a confidence score
- Escalate to human when confidence < threshold
- Reviewer acts as quality gate before results are persisted

---

## Agent Handoff Protocol

### Context Passing Mechanism

Each agent passes **structured context** to the next:

1. **Original Request:** The user's ask (unchanged)
2. **Accumulated Context:** Results from previous agents
3. **Work Product:** The specific output of the current agent
4. **Metadata:** Timestamps, confidence scores, dependencies

**Example Handoff (File Picker → Planner):**

```
HANDOFF DATA
├── original_request: "Add authentication to the API"
├── file_picker_output:
│   ├── relevant_files: ["src/auth.ts", "src/api/login.ts", ...]
│   └── project_architecture: {...}
├── metadata:
│   ├── timestamp: 2026-05-19T18:30:00Z
│   ├── agent: "file_picker"
│   └── confidence: 0.95
└── next_agent: "planner"
```

### Conditional Handoff

Agents can conditionally skip or trigger next steps:

**File Picker Decision:**
- "Too many files to modify" → Escalate to human
- "No relevant files found" → Return error
- "Clear scope" → Pass to Planner

**Planner Decision:**
- "Changes are risky" → Add reviewer notes
- "Simple change" → Can skip to Editor directly
- "Complex dependencies" → Add warnings to Editor

**Editor Decision:**
- "Can't apply changes cleanly" → Escalate to human
- "Generated code has syntax errors" → Fix and retry
- "Success" → Pass to Reviewer

---

## Custom Workflows (TypeScript-Based)

Codebuff allows custom agent workflows using TypeScript generators:

```typescript
// Custom workflow for "add API endpoint" task

async function addApiEndpointWorkflow(request: string) {
  // Step 1: File Picker
  const files = await filePickerAgent(request);

  // Step 2: Conditional routing
  if (files.length > 5) {
    return escalateToHuman("Too many files");
  }

  // Step 3: Planner with custom logic
  const plan = await plannerAgent({
    request,
    files,
    customRules: ["endpoints must be in src/routes/", "add tests"]
  });

  // Step 4: Parallel execution (optimization)
  const changes = await Promise.all(
    plan.changes.map(change => editorAgent(change))
  );

  // Step 5: Reviewer with scoring
  const review = await reviewerAgent({ changes });

  if (review.confidence < 0.85) {
    return escalateToHuman("Low confidence", review.issues);
  }

  return {
    changes,
    review,
    status: "approved"
  };
}
```

**Key Features:**
- **Conditional Routing:** Branch based on complexity
- **Subagent Spawning:** Multiple agents working in parallel
- **Confidence Thresholds:** Escalate when uncertain
- **Custom Rules:** Domain-specific constraints
- **Retry Logic:** Fix and resubmit on failure

---

## Comparison: AgentForge vs. Codebuff Architecture

| Aspect | Codebuff | AgentForge |
|--------|----------|-----------|
| **Agent Count** | 4 (File Picker, Planner, Editor, Reviewer) | 14 (14 departments) |
| **Specialization** | Task-specific (writing code) | Domain-specific (research, ops, content, etc.) |
| **Handoff Protocol** | Structured JSON + metadata | Hive Mind signals + mission context |
| **Confidence Scoring** | Per-agent + per-decision | Per-signal (planned) |
| **Escalation** | Auto-escalate on low confidence | Escalation on blocker (planned) |
| **Custom Workflows** | TypeScript generators | Agent.js executeMission() overrides |
| **Error Recovery** | Retry with feedback | Mission status = 'failed' + logging |

---

## Agent Handoff Protocol for AgentForge

### Current State
Agents receive mission context via:
```javascript
async executeMission(missionId, prompt) {
  // Agent gets: missionId + prompt
  // No prior context about related missions or decisions
}
```

### Recommended Enhancement

**Handoff Structure:**
```javascript
async executeMission(missionId, prompt, context) {
  // context includes:
  const context = {
    original_request: "...",
    related_missions: [...],      // Similar prior missions
    hive_mind_signals: [...],      // Relevant learned patterns
    dependencies: [...],            // Which agents finished first
    escalation_rules: {...},       // When to escalate
    confidence_threshold: 0.85
  };
}
```

### Example: Content Agent Using Handoff

```javascript
async executeMission(missionId, prompt, context) {
  // 1. Load context from related missions
  const relatedArticles = context.hive_mind_signals
    .filter(s => s.type === 'article_published')
    .slice(0, 3);

  // 2. Get keyword research from SEO agent (if completed)
  const keywords = context.related_missions
    .find(m => m.agent_id === 'seo')
    ?.result?.keywords;

  // 3. Check for style guide from prior articles
  const stylePattern = extractStyle(relatedArticles);

  // 4. Write article with all context
  const article = await query({
    prompt: `${prompt}\n\nContext:\n${JSON.stringify({
      keywords,
      stylePattern,
      relatedArticles: relatedArticles.map(s => s.content)
    })}`
  });

  // 5. Score confidence
  const confidence = article.citations.length / keywords.length;

  // 6. Escalate if low confidence
  if (confidence < context.confidence_threshold) {
    await this.escalate(missionId, {
      reason: 'low_citation_coverage',
      missing_keywords: keywords.filter(k => !article.text.includes(k))
    });
  }

  return article;
}
```

---

## Documentation Structure in Codebuff

Codebuff maintains clear docs for:
- `architecture.md` — Package structure, dependencies, patterns
- `docs/agents-and-tools.md` — Agent system, shell shims, tool definitions
- `docs/custom-workflows.md` — TypeScript generators, subagent spawning
- `AGENTS.md` — Agent capabilities and specifications

**For AgentForge:**
- Each agent needs clear documentation of:
  - What it does (capability)
  - What context it needs (inputs)
  - What it produces (outputs)
  - When to escalate (thresholds)
  - How it integrates (related agents)

---

## Key Takeaways for AgentForge Implementation

### 1. **Structured Handoff Over Loose Context**
- ✅ Pass explicit context object between agents
- ✅ Include related mission results, not just raw request
- ✅ Metadata (confidence, dependencies) travels with payload

### 2. **Confidence Scoring is Essential**
- Each agent output: confidence 0.0-1.0
- Escalate if confidence < threshold (default 0.85)
- Track confidence over time for learning

### 3. **Conditional Execution Patterns**
- Simple requests → Fewer steps, faster execution
- Complex requests → More agents, higher quality
- Risky operations → Automatic escalation

### 4. **Subagent Spawning**
- Content agent should spawn SEO agent for keyword research
- Design agent should spawn PDF agent for asset generation
- CEO agent should spawn all other agents for strategic decisions

### 5. **Reviewer Role is Separate**
- Quality gate before results persist
- Catches style inconsistencies
- Identifies missing context or errors
- Confidence scoring for aggregated output

### 6. **Retry with Feedback**
- On failure, pass failure reason back to agent
- Agent learns from previous attempt
- Exponential backoff before escalation

---

## Database Schema for Handoff Protocol

```sql
-- Current: mission_tasks
-- Proposal: Add handoff context

ALTER TABLE mission_tasks ADD COLUMN (
  handoff_context JSON,     -- structured context from previous agents
  confidence_score REAL,    -- per-agent confidence (0.0-1.0)
  escalation_reason TEXT,   -- why escalated (if applicable)
  related_mission_ids TEXT  -- JSON array of related missions
);

-- New table: agent_capabilities
CREATE TABLE agent_capabilities (
  agent_id TEXT PRIMARY KEY,
  capability_name TEXT,
  input_schema JSON,        -- what context this agent needs
  output_schema JSON,       -- what this agent produces
  confidence_threshold REAL,
  escalation_rules JSON,
  created_at INTEGER
);

-- New table: agent_handoffs
CREATE TABLE agent_handoffs (
  id TEXT PRIMARY KEY,
  from_agent TEXT,
  to_agent TEXT,
  mission_id TEXT,
  context_passed JSON,
  confidence_score REAL,
  created_at INTEGER
);
```

---

## References

- **GitHub:** [CodebuffAI/codebuff](https://github.com/CodebuffAI/codebuff)
- **Documentation:** `AGENTS.md`, `docs/agents-and-tools.md`
- **Blog:** [Codebuff: Multi-Agent AI Coding That Actually Works](https://yuv.ai/blog/codebuff)
- **Official Website:** https://www.codebuff.com/

---

**Completed:** 2026-05-19 18:45 UTC
**Next Action:** Implement handoff context in mission_tasks + add confidence scoring to all agent outputs

