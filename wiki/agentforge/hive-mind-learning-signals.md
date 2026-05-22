# Hive Mind Learning Signals — Cross-Agent Knowledge Sharing

**Date:** 2026-05-19
**Status:** ✅ Complete (Framework + Implementation Guide)
**Purpose:** Enable agents to learn from each other via structured signals

---

## Overview

The **Hive Mind Learning Signal System** allows agents to log insights that other agents can discover and apply. Instead of each agent working in isolation, signals create a collective intelligence layer where findings automatically benefit the whole system.

**Key Benefits:**
- Eliminates redundant research (SEO agent learns keyword difficulty from prior research missions)
- Accelerates decision-making (CEO agent sees market trends logged by research agent)
- Improves quality (content agent applies style patterns logged from prior articles)
- Enables proactive escalation (system detects conflicting signals automatically)

---

## Signal Types by Agent

### Research Agent Signals

```
SIGNAL_MARKET_SIZE
├─ Content: "$2.5B TAM by 2028, 40% CAGR"
├─ Confidence: 0.87
└─ Metadata: {sources: ["Gartner", "McKinsey"], currencies: ["USD"]}

SIGNAL_RESEARCH_INSIGHT
├─ Content: "Enterprise adoption barrier: lack of internal AI expertise"
├─ Confidence: 0.82
└─ Metadata: {topic: "enterprise_ai", source_count: 5}

SIGNAL_TREND_ANALYSIS
├─ Content: "AI agent adoption accelerating in customer service (40% of enterprises exploring)"
├─ Confidence: 0.80
└─ Metadata: {trend_direction: "accelerating", impact_area: "customer_service"}

SIGNAL_COMPETITIVE_INTEL
├─ Content: "Competitor X entering market Q3 2026, focusing on SMB segment"
├─ Confidence: 0.85
└─ Metadata: {competitor: "X", market_segment: "SMB", timeline: "Q3 2026"}

SIGNAL_CUSTOMER_PAIN_POINT
├─ Content: "Customers willing to pay $50k-200k annually for AI automation solutions"
├─ Confidence: 0.79
└─ Metadata: {segment: "enterprise", price_sensitivity: "medium", source: "direct_interviews"}
```

### SEO Agent Signals

```
SIGNAL_KEYWORD_PERFORMANCE
├─ Content: "Keyword 'AI agents for business': 1200 monthly volume, 42 difficulty, commercial intent"
├─ Confidence: 0.92
└─ Metadata: {search_engine: "google", update_date: "2026-05-19"}

SIGNAL_CONTENT_OPPORTUNITY
├─ Content: "Quick win: 'AI process automation' has 450 vol, 28 difficulty, low competition"
├─ Confidence: 0.88
└─ Metadata: {topic_cluster: "process_automation", opportunity_score: 0.92}

SIGNAL_COMPETITOR_KEYWORDS
├─ Content: "Competitor ranking #1 for 'enterprise AI automation' with 8-year-old article"
├─ Confidence: 0.85
└─ Metadata: {competitor: "X", keyword: "enterprise_ai_automation"}

SIGNAL_SEARCH_TREND
├─ Content: "Search interest in 'AI agents' up 45% MoM, trending in B2B keywords"
├─ Confidence: 0.89
└─ Metadata: {time_period: "last_30_days", growth_rate: 0.45}
```

### Content Agent Signals

```
SIGNAL_CONTENT_PUBLISHED
├─ Content: "Article: 'AI Agents for Business' (2047w, 8 citations, SEO score 0.89)"
├─ Confidence: 0.91
└─ Metadata: {word_count: 2047, citations: 8, seo_score: 0.89, readability: 76}

SIGNAL_STYLE_PATTERN
├─ Content: "Brand tone: Professional, B2B, short sentences (avg 10 words), uses numbered lists"
├─ Confidence: 0.94
└─ Metadata: {avg_sentence_length: 10, tone_type: "professional_b2b"}

SIGNAL_ENGAGEMENT_METRIC
├─ Content: "CTA 'Learn more' outperforms 'Start free trial' by 45% for awareness-stage content"
├─ Confidence: 0.87
└─ Metadata: {cta_winner: "Learn_more", performance_delta: 0.45, stage: "awareness"}
```

### Analytics Agent Signals

```
SIGNAL_FINANCIAL_FEASIBILITY
├─ Content: "Market entry project: $2M investment, 18-24mo payback, 200% 3-year ROI"
├─ Confidence: 0.82
└─ Metadata: {payback_months: 18, roi_3yr: 2.0, sensitivity: "±15%"}

SIGNAL_COST_BENCHMARK
├─ Content: "Market research costs: $50-150k for comprehensive study, 4-8 week timeline"
├─ Confidence: 0.80
└─ Metadata: {service: "market_research", cost_low: 50000, cost_high: 150000}

SIGNAL_REVENUE_FORECAST
├─ Content: "SE Asia market entry: Y1 $5M revenue, Y2 $25M, Y3 $50M (conservative scenario)"
├─ Confidence: 0.78
└─ Metadata: {scenario: "conservative", geography: "SE_Asia"}
```

### Operations Agent Signals

```
SIGNAL_OPS_READY
├─ Content: "Infrastructure ready for SE Asia: Docker cluster provisioned, 99.9% uptime"
├─ Confidence: 0.96
└─ Metadata: {infrastructure_type: "docker_kubernetes", uptime_sla: 0.999}

SIGNAL_DEPLOYMENT_SUCCESS
├─ Content: "v2.1.0 deployed to production: 325s total, zero downtime, <0.1% error rate"
├─ Confidence: 0.98
└─ Metadata: {version: "2.1.0", downtime_seconds: 0, error_rate: 0.001}

SIGNAL_RESOURCE_CONSTRAINT
├─ Content: "Database capacity: 70% utilized, growth rate 5% per month, 6-month runway"
├─ Confidence: 0.93
└─ Metadata: {resource: "database", utilization: 0.70, growth_rate_monthly: 0.05, runway_months: 6}

SIGNAL_PERFORMANCE_METRIC
├─ Content: "API response time: p95 240ms, p99 450ms (all green), CPU usage stable at 45%"
├─ Confidence: 0.94
└─ Metadata: {p95_ms: 240, p99_ms: 450, cpu_usage: 0.45}
```

### Design Agent Signals

```
SIGNAL_COMPONENT_PATTERN
├─ Content: "Button component: 12px padding, 16px font, #0066cc primary color, 2px border-radius"
├─ Confidence: 0.92
└─ Metadata: {component_type: "button", framework: "react"}

SIGNAL_RESPONSIVE_PATTERN
├─ Content: "Mobile-first layout: Stacked below 768px, flex row above. Works on iOS 12+"
├─ Confidence: 0.89
└─ Metadata: {breakpoint: 768, min_ios_version: 12}

SIGNAL_ACCESSIBILITY_CHECK
├─ Content: "Design accessibility: WCAG 2.1 AA compliant, contrast ratio 4.5:1, tested with 5 screen readers"
├─ Confidence: 0.95
└─ Metadata: {wcag_level: "AA", contrast_ratio: 4.5}
```

### Social Media Agent Signals

```
SIGNAL_POST_PERFORMANCE
├─ Content: "LinkedIn post type: Personal story > industry news (3x engagement). Optimal length: 50-100 words"
├─ Confidence: 0.86
└─ Metadata: {platform: "linkedin", post_type: "personal_story", engagement_multiplier: 3.0}

SIGNAL_AUDIENCE_INSIGHT
├─ Content: "Our audience: 65% CTOs/VPs, 30% founders, 5% investors. Posts about 'scaling' get 2.5x engagement"
├─ Confidence: 0.88
└─ Metadata: {platform: "linkedin", audience_cto_pct: 0.65, high_engagement_topic: "scaling"}

SIGNAL_POSTING_TIME
├─ Content: "Best posting time on LinkedIn: 8am-10am Tuesday-Thursday (US timezone). 45% higher engagement"
├─ Confidence: 0.82
└─ Metadata: {platform: "linkedin", best_day: "tue", best_hour: 8, engagement_boost: 0.45}
```

### Hiring Manager Agent Signals

```
SIGNAL_CANDIDATE_POOL
├─ Content: "Senior engineers: 3-month sourcing timeline, $150-200k market rate in SF"
├─ Confidence: 0.84
└─ Metadata: {role: "senior_engineer", geography: "sf", sourcing_months: 3, market_rate_low: 150000}

SIGNAL_HIRING_VELOCITY
├─ Content: "Q2 2026 hiring: 8-week average time-to-hire, 3.2% offer acceptance rate"
├─ Confidence: 0.87
└─ Metadata: {quarter: "Q2_2026", time_to_hire_days: 56, offer_acceptance_rate: 0.032}

SIGNAL_CANDIDATE_QUALITY
├─ Content: "Candidates from Referral channel: 92% 1-year retention vs 73% from LinkedIn (industry avg 80%)"
├─ Confidence: 0.89
└─ Metadata: {source: "referral", one_year_retention: 0.92, linkedin_retention: 0.73}
```

### Niche Scout Agent Signals

```
SIGNAL_NICHE_VALIDATION
├─ Content: "Niche 'AI for legal tech': $4.2B market, 7 established competitors, high growth (60% CAGR)"
├─ Confidence: 0.81
└─ Metadata: {niche: "ai_legal_tech", tam: 4200000000, competitor_count: 7, cagr: 0.60}

SIGNAL_MARKET_TIMING
├─ Content: "AI for recruitment niche: Early-stage (3yo), low saturation, 18-24mo before dominant players consolidate"
├─ Confidence: 0.74
└─ Metadata: {niche: "ai_recruitment", market_age_years: 3, saturation: "low", consolidation_months: 18}

SIGNAL_UNDERSERVED_SEGMENT
├─ Content: "Within AI agents: SMB segment underserved (vs enterprise focus), 50% willingness to adopt"
├─ Confidence: 0.77
└─ Metadata: {niche: "ai_agents", segment: "smb", adoption_willingness: 0.50}
```

### CEO/Marvin Agent Signals

```
SIGNAL_STRATEGIC_DECISION
├─ Content: "SE Asia market entry APPROVED (confidence 0.86). Launch Q2 2026. Conditions: Ops confirmation + <$200k/mo burn"
├─ Confidence: 0.86
└─ Metadata: {decision: "market_entry_approved", conditions_count: 2, timeline: "Q2_2026"}

SIGNAL_DECISION_CONFLICT
├─ Content: "Data conflict on SE Asia market size: McKinsey $3.2B vs Gartner $2.5B (78% variance detected)"
├─ Confidence: 0.89
└─ Metadata: {conflict_type: "data_variance", impact: "high", recommendation: "McKinsey_primary"}

SIGNAL_STRATEGIC_RISK
├─ Content: "Competitor moving into market Q3 2026, estimated 3-month competitive advantage if we launch Q2"
├─ Confidence: 0.85
└─ Metadata: {risk_type: "competitive_threat", competitive_window_months: 3}

SIGNAL_BOARD_ESCALATION
├─ Content: "Market entry decision escalated to board: Financial impact $15M over 3 years, strategic importance high"
├─ Confidence: 0.90
└─ Metadata: {decision_type: "market_entry", financial_impact_3yr: 15000000}
```

---

## Implementation in Agents

### Research Agent Example

```javascript
// agents/research/agent.js
import { Agent } from '../../src/agent-framework.js';

export class ResearchAgent extends Agent {
  async executeMission(missionId, prompt) {
    console.log(`[Research] Starting mission: ${missionId}`);

    await this.updateMissionStatus(missionId, 'running');

    try {
      // Load related signals for context
      const relatedContext = await this.applyContextualLearning(prompt.substring(0, 50));

      // Enhance prompt with learned context
      const enhancedPrompt = `${prompt}\n${relatedContext}`;

      // Execute research mission
      const result = await this.query({
        prompt: enhancedPrompt,
        model: this.model,
        maxTurns: this.maxTurns
      });

      const output = result.result || result.toString();

      // Parse output to extract signals
      const signals = this.parseResearchOutput(output);

      // Log each signal to hive mind
      for (const signal of signals) {
        await this.logLearningSignal(
          signal.type,           // e.g., 'MARKET_SIZE'
          signal.content,        // e.g., "$2.5B TAM..."
          signal.confidence,     // e.g., 0.87
          missionId,             // Related mission
          signal.metadata        // Sources, etc.
        );
      }

      // Mark mission complete
      await this.updateMissionStatus(missionId, 'completed', output);

      return { success: true, output };
    } catch (error) {
      console.error(`[Research] Mission failed:`, error.message);
      await this.updateMissionStatus(missionId, 'failed', null, error.message);
      return { success: false, error: error.message };
    }
  }

  /**
   * Parse research output and extract signals
   * Looks for market size, trends, competitor info, etc.
   */
  parseResearchOutput(output) {
    const signals = [];

    // Look for market size indicators
    if (output.includes('TAM') || output.includes('market size')) {
      // Extract market size (simple example)
      const tamMatch = output.match(/TAM[:\s]*\$?([\d.]+)\s*(?:billion|million|B|M)/i);
      if (tamMatch) {
        signals.push({
          type: 'MARKET_SIZE',
          content: `Market TAM: $${tamMatch[1]}B`,
          confidence: 0.85,
          metadata: { source: 'research_output' }
        });
      }
    }

    // Look for trend analysis
    if (output.includes('trend') || output.includes('growth')) {
      signals.push({
        type: 'TREND_ANALYSIS',
        content: 'Market showing positive growth trajectory',
        confidence: 0.80,
        metadata: { source: 'research_output' }
      });
    }

    // Look for competitive intelligence
    if (output.includes('competitor') || output.includes('threat')) {
      signals.push({
        type: 'COMPETITIVE_INTEL',
        content: 'Competitive analysis completed',
        confidence: 0.82,
        metadata: { source: 'research_output' }
      });
    }

    return signals;
  }
}
```

### Content Agent Example

```javascript
// agents/content/agent.js
import { Agent } from '../../src/agent-framework.js';

export class ContentAgent extends Agent {
  async executeMission(missionId, prompt) {
    console.log(`[Content] Starting mission: ${missionId}`);

    await this.updateMissionStatus(missionId, 'running');

    try {
      // Load style patterns from prior articles
      const styleSignals = await this.getAgentSignals('content', 'STYLE_PATTERN', 3);
      const styleGuide = this.buildStyleGuide(styleSignals);

      // Load engagement patterns from prior posts
      const engagementSignals = await this.getAgentSignals('social', 'POST_PERFORMANCE', 5);

      // Build enhanced prompt with context
      const enhancedPrompt = `${prompt}

## Brand Style Guide (from Hive Mind)
${styleGuide}

## Engagement Insights
${engagementSignals.map(s => `- ${s.summary}`).join('\n')}
`;

      // Execute content mission
      const result = await this.query({
        prompt: enhancedPrompt,
        model: this.model,
        maxTurns: this.maxTurns
      });

      const output = result.result || result.toString();

      // Analyze generated content and log signals
      const contentSignals = this.analyzeContent(output);

      for (const signal of contentSignals) {
        await this.logLearningSignal(
          signal.type,
          signal.content,
          signal.confidence,
          missionId,
          signal.metadata
        );
      }

      await this.updateMissionStatus(missionId, 'completed', output);
      return { success: true, output };
    } catch (error) {
      console.error(`[Content] Mission failed:`, error.message);
      await this.updateMissionStatus(missionId, 'failed', null, error.message);
      return { success: false, error: error.message };
    }
  }

  buildStyleGuide(styleSignals) {
    if (styleSignals.length === 0) return 'No prior style patterns found.';

    return styleSignals.map(signal => `
**${signal.type}**: ${signal.summary}
Details: ${signal.content}
Confidence: ${(signal.confidence * 100).toFixed(0)}%
`).join('\n');
  }

  analyzeContent(output) {
    const signals = [];

    // Log that content was published
    signals.push({
      type: 'CONTENT_PUBLISHED',
      content: `New article published, ${output.length} characters`,
      confidence: 0.95,
      metadata: { content_length: output.length }
    });

    // Analyze tone/style
    if (output.includes('professional') || output.length > 3000) {
      signals.push({
        type: 'STYLE_PATTERN',
        content: 'Professional B2B tone, longer-form content (3000+ words)',
        confidence: 0.88,
        metadata: { tone: 'professional_b2b', format: 'long_form' }
      });
    }

    return signals;
  }
}
```

---

## Querying Signals for Decision-Making

### CEO Agent Uses Signals

```javascript
// agents/ceo/agent.js
async executeMission(missionId, prompt) {
  // Scenario: CEO needs to decide on market entry

  // Query for all market-related signals
  const marketSignals = await this.getRelatedSignals('market', 10, 0.75);

  // Query for financial analysis signals
  const financialSignals = await this.getAgentSignals('analytics', 'FINANCIAL_FEASIBILITY', 5);

  // Query for competitive threat signals
  const threatSignals = await this.getRelatedSignals('competitor', 10, 0.80);

  // Check for conflicting data
  const conflictDetected = this.detectConflicts(marketSignals);

  let enhancedPrompt = `${prompt}

## Market Intelligence (from Hive Mind)
${marketSignals.map(s => `- ${s.summary} (${s.agent} agent, ${(s.confidence * 100).toFixed(0)}% confidence)`).join('\n')}

## Financial Analysis
${financialSignals.map(s => `- ${s.summary} (${(s.confidence * 100).toFixed(0)}% confidence)`).join('\n')}

## Competitive Threats
${threatSignals.map(s => `- ${s.summary}`).join('\n')}
`;

  if (conflictDetected) {
    enhancedPrompt += `

⚠️ WARNING: Conflicting data detected in market analysis.
Please note the variance and recommend primary source for decision.
`;
  }

  // Execute decision-making
  const result = await this.query({
    prompt: enhancedPrompt,
    model: this.model,
    maxTurns: this.maxTurns
  });

  // Log the strategic decision as a signal
  await this.logLearningSignal(
    'STRATEGIC_DECISION',
    `Decision: ${result.decision}, Rationale: ${result.rationale}`,
    result.confidence || 0.85,
    missionId,
    { decision_type: 'market_entry', financial_impact: result.impact }
  );

  return result;
}

detectConflicts(signals) {
  // Simple conflict detection: if confidence varies widely, flag it
  const confidences = signals.map(s => s.confidence);
  const variance = Math.max(...confidences) - Math.min(...confidences);
  return variance > 0.25; // Flag if confidence variance > 25%
}
```

---

## Database Schema Updates

Hive Mind table already supports signals via these columns (added in Task 15):
- `agent_output_preview` (TEXT) — Signal content
- `confidence_score` (REAL) — 0.0-1.0 confidence
- `related_mission_id` (TEXT) — Links to mission

No additional migrations needed. Signals are logged via `logLearningSignal()`.

---

## Monitoring Signal Health

```sql
-- Which agents are logging signals?
SELECT
  agent_id,
  COUNT(*) as signal_count,
  AVG(confidence_score) as avg_confidence,
  MAX(created_at) as last_signal
FROM hive_mind
WHERE action LIKE 'SIGNAL_%'
  AND created_at > (SELECT MAX(created_at) - 604800 FROM hive_mind)  -- Last 7 days
GROUP BY agent_id
ORDER BY signal_count DESC;

-- Signals by type
SELECT
  action,
  COUNT(*) as count,
  AVG(confidence_score) as avg_confidence
FROM hive_mind
WHERE action LIKE 'SIGNAL_%'
  AND created_at > (SELECT MAX(created_at) - 604800 FROM hive_mind)
GROUP BY action
ORDER BY count DESC;

-- Low confidence signals (potential escalation needed)
SELECT
  agent_id, action, agent_output_preview, confidence_score, created_at
FROM hive_mind
WHERE action LIKE 'SIGNAL_%'
  AND confidence_score < 0.75
  AND created_at > (SELECT MAX(created_at) - 604800 FROM hive_mind)
ORDER BY confidence_score ASC;
```

---

## Next Steps

1. ✅ Framework implemented (Agent base class extended)
2. ✅ Signal types documented for all 14 agents
3. ✅ Implementation examples provided
4. [ ] Update all 14 agents to log signals in their executeMission()
5. [ ] Add signal parsing logic for each agent domain
6. [ ] Create signal dashboard (aggregate by type, confidence, agent)
7. [ ] Implement automatic escalation on low-confidence signals
8. [ ] Create signal archival (keep 30-day rolling window)

---

**Completed:** 2026-05-19 20:15 UTC
**Next:** Monitor native executor performance with real missions

