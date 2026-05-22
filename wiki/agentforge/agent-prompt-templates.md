# Agent-Specific Prompt Templates

**Date:** 2026-05-19
**Status:** ✅ Complete
**Purpose:** Reusable, high-quality prompts optimized for each agent's domain

---

## Template Structure

Each template includes:
1. **Context Loading** — Pull relevant data from Hive Mind / MCP
2. **Task Definition** — Clear instructions
3. **Output Format** — Expected structure
4. **Quality Criteria** — Success metrics
5. **Escalation Triggers** — When to escalate

---

## 1. Research Agent Templates

### Template 1.1: Market Research

```
# Market Research Mission

## Context
- Previous research on [topic]: [last_research_summary]
- Related trends (past 30 days): [hive_mind_signals]
- Competing analyses: [similar_previous_missions]

## Task
Research: {{RESEARCH_TOPIC}}

Time frame: {{TIME_FRAME}}
Geographic scope: {{GEOGRAPHY}}
Target audience: {{AUDIENCE}}

## Instructions
1. Identify 5+ unique data sources (not just summaries)
2. Analyze market size, growth rate, TAM/SAM/SOM
3. Map competitive landscape (4-5 key competitors)
4. Surface customer pain points (direct quotes preferred)
5. Identify trends and inflection points
6. Provide data confidence scores per claim

## Output Format
```yaml
research:
  topic: {{RESEARCH_TOPIC}}
  conducted_at: ISO_TIMESTAMP
  market_size:
    tam: "$X billion"
    sam: "$Y billion"
    som: "$Z billion"
    confidence: 0.85
  competitors:
    - name: "Company X"
      market_share: "XX%"
      strengths: ["...", "..."]
      weaknesses: ["...", "..."]
      threat_level: "high/medium/low"
  customer_insights:
    pain_points: ["...", "..."]
    willingness_to_pay: "$X-$Y"
    adoption_barriers: ["...", "..."]
  trends:
    - trend: "..."
      trajectory: "accelerating/stable/declining"
      impact_on_market: "high/medium/low"
  sources:
    - title: "..."
      url: "..."
      type: "research_report/news/customer_feedback"
      reliability: "high/medium"
  confidence_score: 0.87
  confidence_explanation: "Based on X primary sources and Y secondary sources"
```

## Quality Criteria
- ✅ Minimum 5 unique sources (no recycled summaries)
- ✅ Market size estimates with confidence ranges
- ✅ Competitive analysis with primary data
- ✅ Customer voice (direct quotes, not synthesis)
- ✅ Confidence scores ≥ 0.80 to avoid escalation

## Escalation Triggers
- Confidence score < 0.75 → Request human review
- Data conflicts between sources → Flag and research further
- Market too new/nascent → Escalate with "insufficient_data" reason
- Topic requires proprietary data → Escalate with available_alternative suggestions
```

### Template 1.2: Competitive Analysis

```
# Competitive Analysis Mission

## Context
- Company: {{OUR_COMPANY}}
- Competitors identified: [hive_mind_competitors]
- Previous analyses: [similar_missions]

## Task
Analyze competitor: {{COMPETITOR_NAME}}

Dimensions: {{ANALYSIS_DIMENSIONS}} (pricing, technology, market position, etc.)

## Instructions
1. Gather 5+ data points on each dimension
2. Compare to our company (provide deltas)
3. Identify strategic advantages/disadvantages
4. Score threat level (1-10)
5. Recommend defensive/offensive actions

## Output Format
```yaml
competitor_analysis:
  competitor: "{{COMPETITOR_NAME}}"
  analysis_date: ISO_TIMESTAMP

  dimensions:
    pricing:
      competitor_model: "..."
      competitor_price_point: "$X"
      our_price_point: "$Y"
      delta: "{{our_price_point - competitor_price_point}}"
      market_perception: "..."
      confidence: 0.90

    technology:
      competitor_stack: ["...", "..."]
      our_stack: ["...", "..."]
      competitive_advantage_them: "..."
      competitive_advantage_us: "..."
      confidence: 0.85

    market_position:
      competitor_market_share: "XX%"
      our_market_share: "YY%"
      growth_rate_them: "XX% YoY"
      growth_rate_us: "YY% YoY"
      confidence: 0.80

  threat_assessment:
    threat_level: 1-10
    rationale: "..."

    defensive_moves: ["...", "..."]
    offensive_moves: ["...", "..."]

  data_sources:
    - url: "..."
      type: "public_filing/press_release/news"
      reliability: "high/medium"

  overall_confidence: 0.85
```

## Quality Criteria
- ✅ Minimum 5 data points per dimension
- ✅ Direct comparison to our company
- ✅ Specific, actionable recommendations
- ✅ Threat scores justified by data
- ✅ Confidence > 0.80

## Escalation Triggers
- Competitor changed strategy since last analysis → Flag for urgent update
- Threat level increased by 2+ points → Escalate to CEO agent
- Missing key financial data → Escalate with available_alternatives
```

---

## 2. Content Agent Templates

### Template 2.1: Article Writing

```
# Article Writing Mission

## Context
- Topic: {{TOPIC}}
- Target audience: {{AUDIENCE}}
- Similar articles published: [hive_mind_content]
- SEO keywords (if available): [related_seo_mission]
- Tone/style guide: [extracted_from_past_articles]

## Task
Write article: {{ARTICLE_TITLE}}

Word count: {{WORD_COUNT}}
Format: {{FORMAT}} (blog post, white paper, case study)
Publishing platform: {{PLATFORM}}

## Instructions
1. Research {{TOPIC}} using 5+ credible sources
2. Structure with:
   - Hook (curiosity + value promise)
   - 3-5 main sections (logical flow)
   - Actionable takeaways (not just theory)
   - Conclusion with next steps
3. Include citations for all claims
4. Optimize for SEO (use provided keywords naturally)
5. Match existing tone (analyze recent articles)

## Output Format
```yaml
article:
  title: "{{ARTICLE_TITLE}}"
  word_count: {{ACTUAL_COUNT}}
  published_at: ISO_TIMESTAMP

  metadata:
    target_audience: "{{AUDIENCE}}"
    main_keyword: "{{PRIMARY_KEYWORD}}"
    related_keywords: ["...", "...", "..."]
    seo_score: 0.88

  structure:
    hook: "..."
    sections:
      - title: "..."
        content: "..."
        citations: [url1, url2]

    takeaways:
      - "..."
      - "..."

    cta: "Next step: ..."

  quality_metrics:
    readability_score: 85  # Flesch-Kincaid
    original_research: true  # Not just summary
    citations_count: 7
    citations_reliability: "high"
    tone_consistency: 0.92
    keyword_density: "optimal"
    plagiarism_risk: "< 2%"

  confidence_score: 0.89
```

## Quality Criteria
- ✅ Minimum 5 citations (credible sources)
- ✅ Original analysis (not just aggregation)
- ✅ Tone matches brand (if brand guidelines exist)
- ✅ Word count ±5% of target
- ✅ All claims supported by citations
- ✅ SEO score ≥ 0.80
- ✅ Plagiarism risk < 5%

## Escalation Triggers
- Insufficient sources (< 3) → Research agent for deeper dive
- Tone deviation > 10% → Request human review
- Plagiarism risk > 5% → Rewrite with original analysis
- Too technical for audience → Simplify or escalate
```

### Template 2.2: Email Campaign

```
# Email Campaign Mission

## Context
- Target segment: {{SEGMENT}}
- Campaign goal: {{GOAL}} (awareness/conversion/retention)
- Historical performance: [similar_campaigns]
- Brand voice: [extracted_from_templates]

## Task
Create {{EMAIL_COUNT}}-email campaign: {{CAMPAIGN_NAME}}

## Instructions
1. Email 1 (Subject line): {{OBJECTIVE_1}}
   - Hook: {{EMAIL_1_HOOK}}
   - Body: {{EMAIL_1_BODY_OUTLINE}}
   - CTA: {{EMAIL_1_CTA}}

2. Email 2 (Subject line): {{OBJECTIVE_2}}
   - Build on Email 1
   - Add social proof / urgency
   - CTA must be congruent with Email 1

3. Email 3 (Subject line): {{OBJECTIVE_3}}
   - Final ask / close
   - Address objections
   - Strong CTA

## Output Format
```yaml
email_campaign:
  name: "{{CAMPAIGN_NAME}}"
  created_at: ISO_TIMESTAMP
  segment: "{{SEGMENT}}"
  goal: "{{GOAL}}"

  emails:
    - sequence: 1
      subject: "..."
      preview_text: "..."
      body: "..."
      cta_text: "..."
      cta_url: "..."
      estimated_click_rate: 0.12

    - sequence: 2
      subject: "..."
      # ... repeat format ...

  campaign_metrics:
    expected_open_rate: 0.28
    expected_click_rate: 0.08
    expected_conversion_rate: 0.03
    conversion_value: "$X"

  quality_checks:
    mobile_friendly: true
    accessibility_score: 92
    readability_score: 78
    tone_consistency: 0.95
    personalization_tokens: ["first_name", "company"]
```

## Quality Criteria
- ✅ Mobile-friendly layouts
- ✅ Clear hierarchy (one main CTA per email)
- ✅ Tone consistent with brand
- ✅ No spam trigger words
- ✅ Personalization tokens included
- ✅ Sequence flows logically (Email 2 builds on Email 1)

## Escalation Triggers
- Expected conversion rate < 2% → Request human review of positioning
- Accessibility score < 85 → Fix for ADA compliance
- Tone deviation > 10% → Rewrite
- Unclear CTAs → Clarify and resubmit
```

---

## 3. SEO Agent Template

### Template 3.1: Keyword Research

```
# Keyword Research Mission

## Context
- Seed keyword: {{SEED_KEYWORD}}
- Industry: {{INDUSTRY}}
- Target market: {{TARGET_MARKET}}
- Current rankings: [if_existing_site]

## Task
Research keywords for: {{BUSINESS_OBJECTIVE}}

Focus areas: {{FOCUS_AREAS}} (e.g., awareness, consideration, conversion)

## Instructions
1. Generate 50+ keyword variations (seed + modifiers)
2. Gather volume, difficulty, intent for each
3. Cluster by search intent (informational/commercial/transactional)
4. Identify quick wins (volume > 100, difficulty < 40)
5. Map to content stages (awareness/consideration/decision)

## Output Format
```yaml
keyword_research:
  seed: "{{SEED_KEYWORD}}"
  conducted_at: ISO_TIMESTAMP

  keywords:
    - keyword: "..."
      monthly_volume: 1200
      competition_score: 32
      intent: "informational/commercial/transactional"
      commercial_value: "high/medium/low"
      opportunity_score: 0.82  # volume / difficulty
      content_stage: "awareness/consideration/decision"

  clusters:
    cluster_1:
      theme: "..."
      keywords: ["...", "...", "..."]
      recommended_content: "..."

  quick_wins:  # volume > 100, difficulty < 40
    - keyword: "..."
      volume: 450
      difficulty: 28
      recommended_content: "blog_post"

  content_strategy:
    awareness: ["...", "..."]  # High volume, informational
    consideration: ["...", "..."]  # Medium volume, commercial
    decision: ["...", "..."]  # Low volume, transactional

  confidence_score: 0.91
```

## Quality Criteria
- ✅ Volume + difficulty data from primary source
- ✅ 50+ keywords minimum
- ✅ Intent classification accuracy
- ✅ Opportunity scoring clear
- ✅ Content mapping actionable

## Escalation Triggers
- No quick wins found (< 5 keywords) → Escalate for niche validation
- Market too competitive (all keywords > 60 difficulty) → Request strategy adjustment
- Seed keyword too broad → Refine and resubmit
```

---

## 4. Operations Agent Template

### Template 4.1: System Deployment

```
# System Deployment Mission

## Context
- System: {{SYSTEM_NAME}}
- Current version: {{CURRENT_VERSION}}
- Target environment: {{ENVIRONMENT}} (staging/production)
- Deployment history: [last_3_deployments]

## Task
Deploy {{SYSTEM_NAME}} to {{ENVIRONMENT}}

Changes: {{CHANGE_SUMMARY}}
Rollback plan: {{ROLLBACK_PLAN}}

## Instructions
1. Pre-deployment checks
   - ✅ All tests passing
   - ✅ No breaking changes
   - ✅ Configuration in place

2. Deployment steps (in sequence)
   - Load new version
   - Run migrations
   - Health check
   - Monitor error rates (5 min)

3. Rollback procedure (if errors detected)
   - Revert to {{PREVIOUS_VERSION}}
   - Restore database
   - Verify system health

4. Post-deployment verification
   - Check error rates (1 hour)
   - Monitor resource usage
   - Verify all endpoints responding

## Output Format
```yaml
deployment:
  system: "{{SYSTEM_NAME}}"
  timestamp: ISO_TIMESTAMP
  environment: "{{ENVIRONMENT}}"

  pre_checks:
    tests_passing: true
    configuration_valid: true
    dependencies_available: true

  deployment_steps:
    - step: 1
      action: "Load new version"
      duration_seconds: 45
      status: "success"

    - step: 2
      action: "Run migrations"
      duration_seconds: 120
      status: "success"

  health_check:
    endpoint: "/health"
    response_time_ms: 145
    status_code: 200

  monitoring:
    error_rate_5min: "< 0.1%"
    cpu_usage: "45%"
    memory_usage: "62%"
    response_time_p95: "240ms"

  rollback_executed: false

  status: "success"
  duration_seconds: 325

  confidence_score: 0.98
```

## Quality Criteria
- ✅ Zero-downtime deployment
- ✅ Rollback executed if errors detected
- ✅ Health checks pass
- ✅ Error rate stays < 0.5%
- ✅ Performance metrics stable

## Escalation Triggers
- Health check fails → Immediately rollback
- Error rate > 1% → Investigate and rollback if needed
- Any manual intervention needed → Escalate to human ops
- Performance degradation > 20% → Rollback
```

---

## 5. CEO/Marvin Agent Template

### Template 5.1: Strategic Decision

```
# Strategic Decision Mission

## Context
- Decision type: {{DECISION_TYPE}} (market entry, product pivot, acquisition, etc.)
- Stakeholders: [involved_departments]
- Market data: [related_research_missions]
- Financial impact: {{FINANCIAL_IMPACT}} (high/medium/low)
- Timeline: {{DEADLINE}}

## Task
Make strategic decision: {{DECISION_STATEMENT}}

## Instructions
1. Gather data from all relevant agents
   - Market research (research agent)
   - Financial analysis (analytics agent)
   - Operational feasibility (ops agent)
   - Competitive positioning (research agent)

2. Synthesize findings
   - Pro arguments (with confidence scores)
   - Con arguments (with confidence scores)
   - Risk assessment
   - Opportunity assessment

3. Generate recommendations
   - Recommendation (yes/no/maybe with conditions)
   - Conditions (if applicable)
   - Timeline for decision
   - Implementation roadmap

4. Escalation criteria
   - If confidence < 0.80 → Escalate to board
   - If financial impact > $500K → Escalate to board
   - If timeline < 2 weeks and impact is high → Escalate

## Output Format
```yaml
strategic_decision:
  decision: "{{DECISION_STATEMENT}}"
  decision_date: ISO_TIMESTAMP

  research_synthesis:
    market:
      summary: "..."
      confidence: 0.85
      source_mission: "..."

    financial:
      net_present_value: "$X million"
      payback_period: "X months"
      confidence: 0.80
      source_mission: "..."

    operational:
      feasibility: "high/medium/low"
      resource_requirement: "..."
      timeline: "X months"
      confidence: 0.75
      source_mission: "..."

  analysis:
    pros:
      - argument: "..."
        confidence: 0.85
        impact: "high/medium"

    cons:
      - argument: "..."
        confidence: 0.80
        impact: "high/medium"

    risks:
      - risk: "..."
        probability: 0.40
        impact: "$X million"
        mitigation: "..."

    opportunities:
      - opportunity: "..."
        probability: 0.60
        upside: "$X million"

  recommendation:
    action: "YES / NO / YES_WITH_CONDITIONS"
    rationale: "..."
    conditions: ["...", "..."]  # if YES_WITH_CONDITIONS

  confidence_score: 0.82

  escalation:
    escalated: false  # or true with reason
    reason: "..."  # if escalated
    board_recommendation: "..."

  next_steps:
    - step: "..."
      owner: "agent_id"
      deadline: "date"
```

## Quality Criteria
- ✅ All major agents consulted
- ✅ Confidence scores > 0.75
- ✅ Clear pro/con analysis
- ✅ Risk assessment complete
- ✅ Implementation roadmap defined
- ✅ Escalation criteria applied

## Escalation Triggers
- Overall confidence < 0.75 → Escalate to board
- Major disagreement between agents (conflicting analyses) → Escalate
- Financial impact > $500K AND confidence < 0.80 → Escalate
- Timeline < 2 weeks AND impact is strategic → Escalate to human decision-makers
```

---

## Using Templates in Agents

### In agent.js:

```javascript
import templates from './templates.js';

async executeMission(missionId, prompt) {
  // 1. Load template based on mission type
  const template = templates[this.missionType];

  // 2. Extract variables from mission prompt
  const variables = extractVariables(prompt);

  // 3. Render template with variables
  const enhancedPrompt = template.render(variables);

  // 4. Load context from Hive Mind
  const context = await this.loadContext(variables.topic);

  // 5. Combine template + context
  const finalPrompt = `${enhancedPrompt}\n\n## Related Context:\n${JSON.stringify(context)}`;

  // 6. Execute with enhanced prompt
  const result = await this.query({ prompt: finalPrompt, maxTokens: 8000 });

  // 7. Validate output format
  this.validateOutput(result, template.schema);

  return result;
}
```

---

## Template Versioning

Templates should be versioned in `agents/{id}/templates/`:

```
agents/research/templates/
├── market-research-v1.yaml
├── market-research-v2.yaml  # Latest
├── competitive-analysis-v1.yaml
└── README.md

agents/content/templates/
├── article-v1.yaml
├── article-v2.yaml
├── email-campaign-v1.yaml
└── email-campaign-v2.yaml
```

When template improves, increment version. Missions reference version explicitly:
```
./mission-cli.js create --agent research --template market-research-v2 "AI market sizing"
```

---

**Completed:** 2026-05-19 19:15 UTC
**Next:** Agent handoff protocol documentation with real examples

