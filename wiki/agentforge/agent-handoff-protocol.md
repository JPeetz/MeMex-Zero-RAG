# Agent Handoff Protocol — Real-World Examples

**Date:** 2026-05-19
**Status:** ✅ Complete
**Purpose:** Document how agents coordinate via context passing and Hive Mind signals

---

## Overview

The Agent Handoff Protocol enables sequential and parallel agent execution within a single mission or across related missions. Agents pass **structured context** (prior results, related signals, dependencies) rather than starting from scratch.

**Key Principles:**
1. Each agent builds on previous work (cumulative context)
2. Confidence scores determine escalation (> 0.85 = continue, < 0.75 = escalate)
3. Hive Mind signals enable cross-agent learning
4. Missions are atomic but can spawn subagents

---

## Handoff Context Structure

Every mission carries a `handoff_context` through the agent pipeline:

```javascript
{
  // Original mission metadata
  mission_id: "abc123",
  original_request: "Enter the AI market in Southeast Asia",
  request_type: "strategic_decision",
  created_at: "2026-05-19T10:00:00Z",

  // Prior agent results
  prior_results: [
    {
      agent: "research",
      mission_id: "research-001",
      output_preview: "Market size estimated at $2.5B by 2028...",
      confidence: 0.87,
      completed_at: "2026-05-19T11:30:00Z"
    },
    {
      agent: "analytics",
      mission_id: "analytics-001",
      output_preview: "Profitability timeline: 18-24 months...",
      confidence: 0.82,
      completed_at: "2026-05-19T12:15:00Z"
    }
  ],

  // Hive Mind signals (cross-agent learning)
  related_signals: [
    {
      signal_type: "MARKET_TREND",
      content: "SE Asia AI adoption accelerating",
      confidence: 0.90,
      source_agent: "niche_scout",
      created_at: "2026-05-19T08:00:00Z"
    },
    {
      signal_type: "COMPETITIVE_THREAT",
      content: "Competitor entering Vietnam Q3 2026",
      confidence: 0.85,
      source_agent: "research",
      created_at: "2026-05-19T09:45:00Z"
    }
  ],

  // Dependencies
  dependencies: {
    research: "completed",
    analytics: "completed",
    ops: "pending"  // waiting for ops feasibility check
  },

  // Quality criteria
  confidence_threshold: 0.80,
  escalation_triggers: {
    low_confidence: true,
    conflicting_data: true,
    high_financial_impact: true
  }
}
```

---

## Real-World Example 1: Market Entry Decision

### Scenario
User: "Should we enter the Southeast Asia market?"

This triggers a **multi-agent workflow** where CEO/Marvin coordinates research, analytics, ops, and competitive analysis.

### Agent Sequence

```
User Request
    ↓
[1] Research Agent (Market Analysis)
    ├─ Input: "SE Asia AI market opportunity"
    ├─ Output: Market size, growth, customer profiles
    ├─ Confidence: 0.87
    ├─ Duration: 45 minutes
    └─ Hive Mind Signal: "MARKET_SIZE: $2.5B by 2028"
    ↓
[2] Analytics Agent (Financial Modeling)
    ├─ Input: Research output + company financials
    ├─ Output: Profitability timeline, ROI, payback period
    ├─ Confidence: 0.82
    ├─ Duration: 30 minutes
    └─ Hive Mind Signal: "FINANCIAL_FEASIBILITY: 18-24mo breakeven"
    ↓
[3] Ops Agent (Operational Feasibility)
    ├─ Input: Research output + current ops capacity
    ├─ Output: Infrastructure requirements, team needs
    ├─ Confidence: 0.90
    ├─ Duration: 25 minutes
    └─ Hive Mind Signal: "OPS_READY: Can support launch in Q3 2026"
    ↓
[4] Niche Scout Agent (Competitive Threat Assessment)
    ├─ Input: Market research + competitor tracking
    ├─ Output: Threat level, competitive moat
    ├─ Confidence: 0.85
    ├─ Duration: 35 minutes
    └─ Hive Mind Signal: "THREAT_LEVEL: Medium (one competitor moving in)"
    ↓
[5] CEO/Marvin Agent (Strategic Decision)
    ├─ Input: All prior agent outputs + Hive Mind signals
    ├─ Processing:
    │   ✅ Market size: $2.5B (confidence 0.87)
    │   ✅ Profitability: 18-24 months (confidence 0.82)
    │   ✅ Ops ready: Q3 2026 (confidence 0.90)
    │   ⚠️ Threat level: Medium (one competitor moving in)
    │
    │   Overall analysis confidence: 0.86
    │   (Above 0.80 threshold → proceed without escalation)
    │
    ├─ Decision: "YES - Market entry approved"
    ├─ Rationale: "Market opportunity (TAM $2.5B) outweighs competitive threat"
    ├─ Conditions: ["Launch before competitor (target Q2 2026)", "Maintain <$500K burn rate"]
    ├─ Confidence: 0.86
    └─ Output: Strategic decision memo with implementation roadmap
```

### Handoff Example: Research → Analytics

**Research Agent Output:**
```json
{
  "mission_id": "research-001",
  "agent": "research",
  "output": {
    "market_size": {
      "tam": "$2.5 billion",
      "sam": "$800 million",
      "som": "$50 million",
      "confidence": 0.87
    },
    "customer_profiles": {
      "early_adopters": "Tech startups in Singapore, Bangkok",
      "pain_point": "Lack of AI expertise internally",
      "willingness_to_pay": "$50k-200k annually"
    },
    "competitive_landscape": {
      "players": ["OpenAI (via API)", "Local players (limited)"],
      "market_share_leader": "None (fragmented)"
    }
  },
  "hive_mind_signal": {
    "type": "MARKET_SIZE",
    "content": "SE Asia AI market: $2.5B TAM, growing 40% YoY",
    "confidence": 0.87,
    "created_at": "2026-05-19T11:30:00Z"
  }
}
```

**Handoff to Analytics Agent:**
```json
{
  "handoff_context": {
    "original_request": "Should we enter the Southeast Asia market?",
    "prior_results": [
      {
        "agent": "research",
        "market_data": {
          "tam": "$2.5 billion",
          "sam": "$800 million",
          "growth_rate": "40% YoY",
          "confidence": 0.87
        },
        "customer_willingness_to_pay": "$50k-200k annually",
        "competitive_intensity": "low (fragmented)"
      }
    ],
    "dependencies": {
      "research": "completed",
      "ops": "pending"
    }
  },

  "mission_prompt": "Analyze financial feasibility of SE Asia market entry. Input: TAM $2.5B, SAM $800M, initial target: $50M revenue (SOM). Assume: 2-year runway to profitability, $2M YE setup costs. Output: ROI, payback period, cash burn scenario.",

  "quality_criteria": {
    "confidence_threshold": 0.80,
    "required_outputs": ["roi", "payback_period", "cash_burn_forecast"],
    "escalation_if": "confidence < 0.75 or roi < 0% by year 3"
  }
}
```

**Analytics Agent Response:**
```json
{
  "mission_id": "analytics-001",
  "agent": "analytics",
  "output": {
    "financial_analysis": {
      "year_1": {
        "revenue": "$5M",
        "costs": "$8M",
        "net": "-$3M"
      },
      "year_2": {
        "revenue": "$25M",
        "costs": "$18M",
        "net": "$7M"
      },
      "year_3": {
        "revenue": "$50M",
        "costs": "$28M",
        "net": "$22M"
      },
      "payback_period": "18-24 months",
      "roi_3yr": "200%"
    },
    "confidence": 0.82,
    "confidence_rationale": "Based on comparable market entries; adjusted for SE Asia specifics"
  },
  "hive_mind_signal": {
    "type": "FINANCIAL_FEASIBILITY",
    "content": "SE Asia market entry: $2M initial investment, $7M net profit by Year 2, 200% 3-year ROI",
    "confidence": 0.82
  }
}
```

### CEO/Marvin Synthesis

**Input to CEO Agent:**
```
Mission: Make strategic decision on SE Asia market entry

Handoff Context:
- Research: TAM $2.5B, SAM $800M, confidence 0.87
  Hive Mind Signal: Market growing 40% YoY

- Analytics: Payback 18-24 months, ROI 200%, confidence 0.82
  Hive Mind Signal: Financial feasibility confirmed

- Ops: (still pending) Awaiting infrastructure assessment

- Niche Scout: (still pending) Competitive threat analysis

Overall Readiness: 2/4 major agents complete, confidence 0.82+
Decision Timeline: User marked URGENT
```

**CEO Agent Output:**
```json
{
  "mission_id": "ceo-001",
  "agent": "ceo",
  "decision": {
    "action": "APPROVED",
    "confidence": 0.86,
    "rationale": "Market opportunity ($2.5B TAM, 40% growth) with favorable financial metrics (200% ROI) outweighs wait for pending Ops assessment"
  },
  "decision_reasoning": {
    "pros": [
      "Large TAM ($2.5B) with strong growth (40% YoY)",
      "Healthy margins (Year 2: $7M net from $25M revenue)",
      "Fast payback (18-24 months)"
    ],
    "cons": [
      "Competitive threat assessment pending (Niche Scout)",
      "Ops feasibility not yet confirmed",
      "Initial $3M Year 1 loss"
    ],
    "risks": [
      {
        "risk": "Competitor moves faster",
        "probability": 0.40,
        "mitigation": "Accelerate launch to Q2 2026 (vs Q3 plan)"
      }
    ]
  },
  "conditions": [
    "Ops feasibility must be confirmed before contract signatures",
    "Launch window: Q2 2026 (before expected competitor entry)",
    "Monthly burn rate cap: $200k to protect runway"
  ],
  "next_steps": [
    {
      "action": "Ops agent: Confirm infrastructure readiness (URGENT)",
      "owner": "ops",
      "deadline": "2026-05-19 EOD"
    },
    {
      "action": "Legal: Begin market entry documentation",
      "owner": "comms",
      "deadline": "2026-05-20"
    }
  ],
  "hive_mind_signal": {
    "type": "STRATEGIC_DECISION",
    "content": "SE Asia market entry APPROVED (confidence 0.86). Launch Q2 2026. Conditions: Ops confirmation + <$200k/mo burn",
    "confidence": 0.86
  }
}
```

---

## Real-World Example 2: Content Production Pipeline

### Scenario
User: "Write an article on AI agents for enterprise"

This triggers a **sequential handoff** between Research → SEO → Content agents.

### Agent Sequence

```
User Request: "Write article: AI agents for enterprise"
    ↓
[1] Research Agent
    ├─ Task: Deep research on enterprise AI agents
    ├─ Outputs: Key trends, use cases, vendor analysis
    ├─ Hive Mind Signal: "ENTERPRISE_AI_TRENDS: Agents for process automation, cost reduction"
    └─ Handoff Context: {research_findings: {...}}
    ↓
[2] SEO Agent
    ├─ Input: Research findings + article topic
    ├─ Task: Keyword research, content optimization
    ├─ Outputs: Primary keyword, related keywords, structure
    ├─ Hive Mind Signal: "KEYWORDS: 'AI agents for business', 'enterprise automation', 'LLM use cases'"
    └─ Handoff Context: {keywords: [...], content_outline: {...}}
    ↓
[3] Content Agent
    ├─ Input: Research + SEO keywords + style guide
    ├─ Task: Write article (2000 words)
    ├─ Process:
    │   ✓ Hook (engagement + value promise)
    │   ✓ 4 main sections (with keywords naturally incorporated)
    │   ✓ Actionable takeaways
    │   ✓ Citations from research sources
    │   ✓ CTA aligned with business goal
    │
    ├─ Output: Fully written article
    ├─ Quality Checks:
    │   ✓ SEO score: 0.89 (keywords naturally integrated)
    │   ✓ Citations: 8 sources
    │   ✓ Plagiarism risk: < 2%
    │   ✓ Tone match: 0.94 (vs company voice)
    │   ✓ Readability: 78 (Flesch-Kincaid)
    │
    └─ Hive Mind Signal: "CONTENT_PUBLISHED: AI agents for enterprise, 2000w, 8 citations"
```

### Handoff Example: Research → SEO

**Research Agent Output:**
```json
{
  "mission_id": "research-content-001",
  "agent": "research",
  "output": {
    "research_topic": "AI agents for enterprise",
    "findings": {
      "use_cases": [
        "Customer service automation (40% of enterprises exploring)",
        "Process automation (RPA replacement, 35% exploring)",
        "Data analysis and insights (30% exploring)"
      ],
      "benefits": [
        "Cost reduction (20-40% on automated processes)",
        "Speed (3-5x faster than manual)",
        "Quality (consistency, fewer errors)"
      ],
      "vendor_landscape": [
        "OpenAI Assistants API (mature)",
        "Anthropic Claude (enterprise-focused)",
        "Google Vertex (enterprise suite)"
      ]
    },
    "sources": [
      "https://...gartner-report-2026",
      "https://...mckinsey-ai-adoption",
      "https://...fortune-enterprise-ai"
    ]
  },
  "hive_mind_signal": {
    "type": "RESEARCH_INSIGHT",
    "content": "Enterprise AI agents: 3 main use cases (customer service, process automation, data analysis). Market drivers: cost reduction, speed, quality. Leaders: OpenAI, Anthropic, Google.",
    "confidence": 0.88
  }
}
```

**Handoff to SEO Agent:**
```json
{
  "handoff_context": {
    "article_topic": "AI agents for enterprise",
    "research_findings": {
      "use_cases": ["Customer service automation", "Process automation", "Data analysis"],
      "key_themes": ["Cost reduction", "Speed", "Quality", "Enterprise adoption"],
      "vendor_landscape": ["OpenAI", "Anthropic", "Google"]
    },
    "target_audience": "Enterprise decision-makers, CTOs",
    "article_goal": "Awareness + consideration (not conversion)"
  },
  "quality_criteria": {
    "confidence_threshold": 0.80,
    "required_outputs": ["primary_keyword", "related_keywords", "content_outline"]
  }
}
```

**SEO Agent Response:**
```json
{
  "mission_id": "seo-content-001",
  "agent": "seo",
  "output": {
    "primary_keyword": "AI agents for business",
    "keyword_cluster": [
      {
        "keyword": "AI agents for business",
        "volume": 1200,
        "difficulty": 42,
        "intent": "commercial",
        "placement": "H1, meta description"
      },
      {
        "keyword": "enterprise AI automation",
        "volume": 890,
        "difficulty": 38,
        "intent": "commercial",
        "placement": "Section H2"
      },
      {
        "keyword": "AI process automation",
        "volume": 2100,
        "difficulty": 45,
        "intent": "commercial",
        "placement": "Throughout body"
      }
    ],
    "content_structure": [
      {
        "section": "Hook",
        "keyword_target": "AI agents for business",
        "angle": "Cost savings + speed benefits"
      },
      {
        "section": "What are AI agents?",
        "keyword_target": "AI agents for business, AI automation",
        "content_points": ["Definition", "How they work", "Why now?"]
      },
      {
        "section": "Use cases for enterprises",
        "keyword_target": "enterprise AI automation, process automation",
        "content_points": ["Customer service", "Process automation", "Data analysis"]
      },
      {
        "section": "Vendor comparison",
        "keyword_target": "enterprise AI tools",
        "content_points": ["OpenAI Assistants", "Anthropic Claude", "Google Vertex"]
      },
      {
        "section": "Takeaways & next steps",
        "keyword_target": "AI agents for business",
        "content_points": ["ROI calculation", "Implementation roadmap"]
      }
    ]
  },
  "hive_mind_signal": {
    "type": "SEO_STRATEGY",
    "content": "Article: AI agents for business. Primary: 'AI agents for business' (1200 vol, 42 diff). Structure: 5 sections, 2000 words, 3-4 keywords per section.",
    "confidence": 0.85
  }
}
```

### Content Agent Synthesis

**Input to Content Agent:**
```
Mission: Write article "AI Agents for Enterprise" (2000 words)

Handoff Context:
- Research: 3 main use cases, key benefits (cost, speed, quality)
  Sources: Gartner, McKinsey, Fortune

- SEO: Primary keyword "AI agents for business" (1200 vol, 42 difficulty)
  Structure: 5 sections with integrated keywords

- Style Guide: Professional, B2B tone, 1-2 sentence paragraphs, include case studies
```

**Content Agent Output:**
```json
{
  "mission_id": "content-001",
  "agent": "content",
  "output": {
    "title": "AI Agents for Business: How Enterprises Are Automating Work",
    "word_count": 2047,
    "article": "{{full_article_text}}",
    "sections": [
      {
        "heading": "The Rise of AI Agents in Enterprise",
        "word_count": 420,
        "keywords_used": ["AI agents for business", "enterprise automation"],
        "has_research_citations": true,
        "citations": [1, 2, 3]
      },
      // ... more sections
    ]
  },
  "quality_metrics": {
    "seo_score": 0.89,
    "keywords_integrated": 12,
    "citations_count": 8,
    "plagiarism_risk": "1.2%",
    "readability_score": 76,
    "tone_consistency": 0.94,
    "word_count_variance": "+2.3% (target: 2000)",
    "sections_complete": 5,
    "confidence": 0.91
  },
  "hive_mind_signal": {
    "type": "CONTENT_PUBLISHED",
    "content": "Article: 'AI Agents for Business' (2047w, 8 citations, SEO 0.89, 94% tone match)",
    "confidence": 0.91
  }
}
```

---

## Failure & Escalation Example

### Scenario
Research Agent encounters conflicting data on market size.

**Research Agent Processing:**
```
Task: Estimate SE Asia AI market size

Sources found:
- Gartner: $2.5B TAM by 2028 (report from March 2026)
- IDC: $1.8B TAM by 2028 (report from January 2026)
- McKinsey: $3.2B TAM by 2028 (report from May 2026)

Data conflict detected!
- Delta between sources: $1.4B (78% variance)
- Confidence in Gartner: 0.87
- Confidence in IDC: 0.75
- Confidence in McKinsey: 0.90

ESCALATION TRIGGER: Conflicting data (variance > 30%)
```

**Handoff to CEO Agent (Escalated):**
```json
{
  "mission_id": "research-001",
  "agent": "research",
  "status": "escalated",
  "escalation_reason": "conflicting_data",

  "output": {
    "finding": "SE Asia AI market size estimates vary significantly",
    "data_sources": [
      {
        "source": "McKinsey (May 2026)",
        "tam": "$3.2B",
        "confidence": 0.90,
        "rationale": "Most recent, enterprise-focused"
      },
      {
        "source": "Gartner (March 2026)",
        "tam": "$2.5B",
        "confidence": 0.87,
        "rationale": "Established analyst, may be conservative"
      },
      {
        "source": "IDC (January 2026)",
        "tam": "$1.8B",
        "confidence": 0.75,
        "rationale": "Older data, likely underestimating growth"
      }
    ],
    "recommendation": "Use McKinsey estimate ($3.2B) as primary, with range $2.5B-$3.2B for sensitivity analysis",
    "escalation_note": "Request human judgment on which source is most credible for this decision"
  },

  "escalation_context": {
    "conflict_type": "data_variance",
    "variance_percentage": 78,
    "impact_on_decision": "high",  // Large TAM delta affects ROI calculations
    "confidence_overall": 0.84     // Below escalation threshold due to conflict
  }
}
```

**CEO Agent Receives Escalation:**
```javascript
// In CEO agent's executeMission()
if (context.prior_results.find(r => r.escalation_reason)) {
  // Research escalated due to conflicting data
  const escalation = context.prior_results.find(r => r.escalation_reason);

  // Decision: Which TAM estimate to use?
  const decision = {
    action: "CONDITIONAL_APPROVAL",
    condition: "Use McKinsey $3.2B estimate for primary scenario",
    sensitivity_analysis: "Model also with Gartner $2.5B (downside scenario)",
    rationale: "McKinsey most recent, but hedge with Gartner as conservative case"
  };

  // Requires escalation to human for final sign-off
  await this.escalate(missionId, {
    reason: "conflicting_market_data",
    context: escalation,
    recommendation: decision
  });
}
```

---

## Database Schema for Handoff Tracking

```sql
-- Table: agent_handoffs
-- Tracks all context passing between agents
CREATE TABLE agent_handoffs (
  id TEXT PRIMARY KEY,
  from_agent TEXT,           -- 'research', 'analytics', etc.
  to_agent TEXT,             -- Next agent in pipeline
  mission_id TEXT,           -- Related mission
  context_json JSON,         -- Full handoff context
  context_size_bytes INTEGER,-- For monitoring
  confidence_transferred REAL, -- Confidence from prior agent
  escalation BOOLEAN,        -- Was this escalated?
  escalation_reason TEXT,    -- If escalated: why
  created_at INTEGER,
  completed_at INTEGER,

  FOREIGN KEY (mission_id) REFERENCES mission_tasks(id)
);

-- Table: agent_capabilities
-- Defines what each agent can accept/produce
CREATE TABLE agent_capabilities (
  agent_id TEXT PRIMARY KEY,
  can_accept_from TEXT[],    -- Which agents can handoff to this one
  can_handoff_to TEXT[],     -- Which agents can this one handoff to
  input_schema JSON,         -- What context is required
  output_schema JSON,        -- What context is produced
  confidence_threshold REAL, -- Minimum confidence to proceed
  escalation_rules JSON,     -- When to escalate
  updated_at INTEGER
);

-- Example: Research agent
INSERT INTO agent_capabilities VALUES (
  'research',
  '["user_request"]',  -- Can accept direct requests
  '["analytics", "content", "ops", "ceo"]',  -- Can handoff to these
  '{
    "required_fields": ["topic", "time_frame", "scope"],
    "optional_fields": ["context", "related_missions"]
  }',
  '{
    "required_fields": ["findings", "sources", "confidence"],
    "hive_mind_signal": "RESEARCH_INSIGHT"
  }',
  0.80,  -- Must have 80%+ confidence to handoff
  '{
    "escalate_if_confidence_below": 0.75,
    "escalate_if_data_conflicts": true,
    "escalate_if_sources_insufficient": true
  }',
  UNIX_TIMESTAMP()
);

-- Index for efficient mission tracking
CREATE INDEX idx_handoffs_mission ON agent_handoffs(mission_id, created_at DESC);
CREATE INDEX idx_handoffs_flow ON agent_handoffs(from_agent, to_agent, created_at DESC);
```

---

## Monitoring Handoff Health

### Metrics to Track

```javascript
// In native executor or monitoring script

// 1. Handoff latency (time between agent completions)
SELECT
  from_agent, to_agent,
  AVG(completed_at - created_at) as avg_handoff_latency_seconds,
  COUNT(*) as handoff_count
FROM agent_handoffs
WHERE created_at > (SELECT MAX(created_at) - 86400 FROM agent_handoffs)
GROUP BY from_agent, to_agent;

// Result: Identifies slow handoff paths

// 2. Escalation rate by agent
SELECT
  from_agent,
  COUNT(*) as total_handoffs,
  SUM(CASE WHEN escalation = true THEN 1 ELSE 0 END) as escalations,
  (SUM(CASE WHEN escalation = true THEN 1 ELSE 0 END) / COUNT(*) * 100) as escalation_rate
FROM agent_handoffs
WHERE created_at > (SELECT MAX(created_at) - 86400 FROM agent_handoffs)
GROUP BY from_agent;

// Result: Identifies agents with reliability issues

// 3. Confidence decay across handoffs
SELECT
  mission_id,
  COUNT(*) as agent_count,
  MIN(confidence_transferred) as min_confidence,
  MAX(confidence_transferred) as max_confidence,
  (MIN(confidence_transferred) / MAX(confidence_transferred) * 100) as confidence_retention
FROM agent_handoffs
WHERE created_at > (SELECT MAX(created_at) - 86400 FROM agent_handoffs)
GROUP BY mission_id
HAVING confidence_retention < 0.90;

// Result: Identifies missions where confidence degraded (quality issue)
```

---

## Implementation Checklist

- [x] Handoff context structure defined
- [x] Real-world examples documented
- [x] Failure scenarios covered
- [ ] Database schema migrations
- [ ] Handoff tracking in native executor
- [ ] Escalation auto-detection logic
- [ ] Monitoring dashboard queries
- [ ] Agent capability registry setup

---

**Completed:** 2026-05-19 19:45 UTC
**Next:** Implement Hive Mind cross-agent learning + Monitor executor performance

