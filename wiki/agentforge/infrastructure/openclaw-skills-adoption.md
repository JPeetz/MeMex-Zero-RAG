---
title: OpenClaw Skills Adoption
type: directive
tags: [meta, skills, openclaw, hermes]
created: 2026-07-31
updated: 2026-07-31
---

# OpenClaw Skills Adoption

Board directive: adopt all locally installed OpenClaw skills into Hermes.

## Result

- Raw OpenClaw `SKILL.md` files discovered: **265**
- Unique exact skill contents imported into Hermes: **254**
- Exact duplicate skill files deduplicated: **11**
- Validation errors: **0**
- Hermes destination: `/Users/joergpeetz/.hermes/skills/openclaw-imports/`
- Import manifest: `/Users/joergpeetz/.hermes/skills/openclaw-imports/IMPORT_MANIFEST.md`

## Runtime rule

OpenClaw-imported skills use the `openclaw-` prefix to avoid colliding with native Hermes skills. When a user asks for a capability that might exist in OpenClaw, search/load these imported skills before reinventing the workflow.

Because Hermes skill discovery is session-initialized, new OpenClaw-imported skills are visible to new Hermes sessions and the CLI (`hermes skills list`) immediately, but this already-running chat may need direct file reads or a fresh session to load them by name.

## Verification

`hermes skills list | grep -c 'openclaw-'` returned **254**.

## Full manifest

# OpenClaw Skills Import Manifest

Imported: 2026-07-31T17:59:45
Source root: `/Users/joergpeetz/.openclaw`
Destination root: `/Users/joergpeetz/.hermes/skills/openclaw-imports`
Raw `SKILL.md` files discovered: **265**
Unique exact `SKILL.md` contents imported: **254**
Duplicate exact-content source groups skipped as redundant: **11**
Validation errors: **0**

## Imported Skills

| Hermes skill name | OpenClaw original | Source | Duplicate sources deduped |
|---|---|---|---|
| `openclaw-advanced-testing-toolkit` | `advanced-testing-toolkit` | `/Users/joergpeetz/.openclaw/workspace/skills/advanced-testing-toolkit` |  |
| `openclaw-agent-orchestration` | `agent-orchestration` | `/Users/joergpeetz/.openclaw/workspace/skills/agent-orchestration` |  |
| `openclaw-agent-skill-foundry-workspace-skills-in-progre-094f51c0` | `event-driven-architecture` | `/Users/joergpeetz/.openclaw/agents/skill-foundry/workspace/skills-in-progress/event-driven-architecture` |  |
| `openclaw-agent-skill-foundry-workspace-skills-in-progre-1a1c58cd` | `database-schema-designer` | `/Users/joergpeetz/.openclaw/agents/skill-foundry/workspace/skills-in-progress/database-schema-designer` |  |
| `openclaw-agent-skill-foundry-workspace-skills-in-progre-4a512831` | `internationalization-i18n` | `/Users/joergpeetz/.openclaw/agents/skill-foundry/workspace/skills-in-progress/internationalization-i18n` |  |
| `openclaw-agent-skill-foundry-workspace-skills-in-progre-568d6b1e` | `api-contract-testing` | `/Users/joergpeetz/.openclaw/agents/skill-foundry/workspace/skills-in-progress/api-contract-testing` |  |
| `openclaw-agent-skill-foundry-workspace-skills-in-progre-aa439b36` | `rag-implementation` | `/Users/joergpeetz/.openclaw/agents/skill-foundry/workspace/skills-in-progress/rag-implementation` |  |
| `openclaw-agent-skill-foundry-workspace-skills-in-progre-acaa2d16` | `kubernetes-operations` | `/Users/joergpeetz/.openclaw/agents/skill-foundry/workspace/skills-in-progress/kubernetes-operations` |  |
| `openclaw-agent-skill-foundry-workspace-skills-in-progre-c98ad00d` | `performance-optimization` | `/Users/joergpeetz/.openclaw/agents/skill-foundry/workspace/skills-in-progress/performance-optimization` |  |
| `openclaw-agent-skill-foundry-workspace-skills-in-progre-d25c1331` | `sre-runbooks` | `/Users/joergpeetz/.openclaw/agents/skill-foundry/workspace/skills-in-progress/sre-runbooks` |  |
| `openclaw-agent-skill-foundry-workspace-skills-in-progre-e9ad4a55` | `llm-security-redteaming` | `/Users/joergpeetz/.openclaw/agents/skill-foundry/workspace/skills-in-progress/llm-security-redteaming` |  |
| `openclaw-agent-skill-foundry-workspace-skills-in-progress` | `agentic-security-scanner` | `/Users/joergpeetz/.openclaw/agents/skill-foundry/workspace/skills-in-progress/agentic-security-scanner` |  |
| `openclaw-agentforge-code-review` | `code-review` | `/Users/joergpeetz/.openclaw/workspace/agentforge/skills/code-review` |  |
| `openclaw-agentforge-memory-manager` | `memory-manager` | `/Users/joergpeetz/.openclaw/workspace/agentforge/skills/memory-manager` |  |
| `openclaw-agentforge-security-audit` | `security-audit` | `/Users/joergpeetz/.openclaw/workspace/agentforge/skills/security-audit` |  |
| `openclaw-api-design` | `api-design` | `/Users/joergpeetz/.openclaw/workspace/skills/api-design` |  |
| `openclaw-app-discovery-scrutiny` | `app-discovery-scrutiny` | `/Users/joergpeetz/.openclaw/workspace/skills/app-discovery-scrutiny` |  |
| `openclaw-app-scaffolding` | `app-scaffolding` | `/Users/joergpeetz/.openclaw/workspace/skills/app-scaffolding` |  |
| `openclaw-astra-campaign` | `astra-campaign` | `/Users/joergpeetz/.openclaw/workspace/skills/astra-campaign` |  |
| `openclaw-betterlife-social-posting` | `betterlife-social-posting` | `/Users/joergpeetz/.openclaw/workspace/skills/betterlife-social-posting` |  |
| `openclaw-blueprint` | `blueprint` | `/Users/joergpeetz/.openclaw/tmp/skills-oVQAAh/skills/blueprint` |  |
| `openclaw-cli-anything-hub` | `cli-hub-meta-skill` | `/Users/joergpeetz/.openclaw/workspace/skills/cli-anything-hub` |  |
| `openclaw-code-review` | `code-review` | `/Users/joergpeetz/.openclaw/workspace/skills/code-review` |  |
| `openclaw-content-strategy-multi-platform` | `content-strategy-multi-platform` | `/Users/joergpeetz/.openclaw/workspace/skills/content-strategy-multi-platform` |  |
| `openclaw-data-pipeline` | `data-pipeline` | `/Users/joergpeetz/.openclaw/workspace/skills/data-pipeline` |  |
| `openclaw-data-visualization` | `data-visualization` | `/Users/joergpeetz/.openclaw/workspace/skills/data-visualization` |  |
| `openclaw-deployment-automation` | `deployment-automation` | `/Users/joergpeetz/.openclaw/workspace/skills/deployment-automation` |  |
| `openclaw-devops-cloud-infrastructure` | `devops-cloud-infrastructure` | `/Users/joergpeetz/.openclaw/workspace/skills/devops-cloud-infrastructure` |  |
| `openclaw-discord` | `discord` | `/Users/joergpeetz/.openclaw/npm/projects/openclaw-discord-c0892df945__openclaw-generation__g-3a4aecad18bbe2c4/node_modules/@openclaw/discord/skills/discord` |  |
| `openclaw-dmp-ab-test-plan` | `ab-test-plan` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/ab-test-plan` |  |
| `openclaw-dmp-ad-creative` | `ad-creative` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/ad-creative` |  |
| `openclaw-dmp-add-integration` | `add-integration` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/add-integration` |  |
| `openclaw-dmp-aeo-audit` | `aeo-audit` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/aeo-audit` |  |
| `openclaw-dmp-aeo-geo` | `aeo-geo` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/aeo-geo` |  |
| `openclaw-dmp-agency-dashboard` | `agency-dashboard` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/agency-dashboard` |  |
| `openclaw-dmp-analytics-insights` | `analytics-insights` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/analytics-insights` |  |
| `openclaw-dmp-anomaly-scan` | `anomaly-scan` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/anomaly-scan` |  |
| `openclaw-dmp-attribution-model` | `attribution-model` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/attribution-model` |  |
| `openclaw-dmp-attribution-report` | `attribution-report` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/attribution-report` |  |
| `openclaw-dmp-audience-intelligence` | `audience-intelligence` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/audience-intelligence` |  |
| `openclaw-dmp-audience-profile` | `audience-profile` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/audience-profile` |  |
| `openclaw-dmp-autopilot-status` | `autopilot-status` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/autopilot-status` |  |
| `openclaw-dmp-backlink-gap` | `backlink-gap` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/backlink-gap` |  |
| `openclaw-dmp-brand-setup` | `brand-setup` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/brand-setup` |  |
| `openclaw-dmp-budget-optimizer` | `budget-optimizer` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/budget-optimizer` |  |
| `openclaw-dmp-budget-tracker` | `budget-tracker` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/budget-tracker` |  |
| `openclaw-dmp-c2pa-metadata` | `c2pa-metadata` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/c2pa-metadata` |  |
| `openclaw-dmp-campaign-audit` | `campaign-audit` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/campaign-audit` |  |
| `openclaw-dmp-campaign-orchestrator` | `campaign-orchestrator` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/campaign-orchestrator` |  |
| `openclaw-dmp-campaign-plan` | `campaign-plan` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/campaign-plan` |  |
| `openclaw-dmp-campaign-status` | `campaign-status` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/campaign-status` |  |
| `openclaw-dmp-case-study-plan` | `case-study-plan` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/case-study-plan` |  |
| `openclaw-dmp-check` | `check` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/check` |  |
| `openclaw-dmp-churn-risk` | `churn-risk` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/churn-risk` |  |
| `openclaw-dmp-client-onboarding` | `client-onboarding` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/client-onboarding` |  |
| `openclaw-dmp-client-proposal` | `client-proposal` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/client-proposal` |  |
| `openclaw-dmp-client-report` | `client-report` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/client-report` |  |
| `openclaw-dmp-client-validation-document` | `client-validation-document` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/client-validation-document` |  |
| `openclaw-dmp-cohort-analysis` | `cohort-analysis` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/cohort-analysis` |  |
| `openclaw-dmp-competitor-alerts` | `competitor-alerts` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/competitor-alerts` |  |
| `openclaw-dmp-competitor-analysis` | `competitor-analysis` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/competitor-analysis` |  |
| `openclaw-dmp-competitor-monitor` | `competitor-monitor` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/competitor-monitor` |  |
| `openclaw-dmp-competitor-pages` | `competitor-pages` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/competitor-pages` |  |
| `openclaw-dmp-connect` | `connect` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/connect` |  |
| `openclaw-dmp-content-brief` | `content-brief` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/content-brief` |  |
| `openclaw-dmp-content-calendar` | `content-calendar` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/content-calendar` |  |
| `openclaw-dmp-content-decay-scan` | `content-decay-scan` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/content-decay-scan` |  |
| `openclaw-dmp-content-engine` | `content-engine` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/content-engine` |  |
| `openclaw-dmp-content-repurpose` | `content-repurpose` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/content-repurpose` |  |
| `openclaw-dmp-context-engine` | `context-engine` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/context-engine` |  |
| `openclaw-dmp-continuous-improvement-loop` | `continuous-improvement-loop` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/continuous-improvement-loop` |  |
| `openclaw-dmp-counter-narrative` | `counter-narrative` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/counter-narrative` |  |
| `openclaw-dmp-cowork-setup` | `cowork-setup` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/cowork-setup` |  |
| `openclaw-dmp-creative-health` | `creative-health` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/creative-health` |  |
| `openclaw-dmp-creative-testing-framework` | `creative-testing-framework` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/creative-testing-framework` |  |
| `openclaw-dmp-credential-switch` | `credential-switch` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/credential-switch` |  |
| `openclaw-dmp-crisis-response` | `crisis-response` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/crisis-response` |  |
| `openclaw-dmp-crm-sync` | `crm-sync` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/crm-sync` |  |
| `openclaw-dmp-cro` | `cro` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/cro` |  |
| `openclaw-dmp-dark-funnel` | `dark-funnel` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/dark-funnel` |  |
| `openclaw-dmp-data-export` | `data-export` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/data-export` |  |
| `openclaw-dmp-data-import` | `data-import` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/data-import` |  |
| `openclaw-dmp-digital-pr` | `digital-pr` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/digital-pr` |  |
| `openclaw-dmp-email-sequence` | `email-sequence` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/email-sequence` |  |
| `openclaw-dmp-emerging-channels` | `emerging-channels` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/emerging-channels` |  |
| `openclaw-dmp-engagement-workflow` | `engagement-workflow` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/engagement-workflow` |  |
| `openclaw-dmp-entity-audit` | `entity-audit` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/entity-audit` |  |
| `openclaw-dmp-eval-config` | `eval-config` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/eval-config` |  |
| `openclaw-dmp-eval-content` | `eval-content` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/eval-content` |  |
| `openclaw-dmp-eval-suite` | `eval-suite` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/eval-suite` |  |
| `openclaw-dmp-exec-summary` | `exec-summary` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/exec-summary` |  |
| `openclaw-dmp-executive-dashboard` | `executive-dashboard` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/executive-dashboard` |  |
| `openclaw-dmp-focus-group` | `focus-group` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/focus-group` |  |
| `openclaw-dmp-four-core-documents` | `four-core-documents` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/four-core-documents` |  |
| `openclaw-dmp-funnel-architect` | `funnel-architect` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/funnel-architect` |  |
| `openclaw-dmp-funnel-audit` | `funnel-audit` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/funnel-audit` |  |
| `openclaw-dmp-geo-monitor` | `geo-monitor` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/geo-monitor` |  |
| `openclaw-dmp-growth-engineering` | `growth-engineering` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/growth-engineering` |  |
| `openclaw-dmp-growth-plan` | `growth-plan` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/growth-plan` |  |
| `openclaw-dmp-gsc-ai-performance` | `gsc-ai-performance` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/gsc-ai-performance` |  |
| `openclaw-dmp-help` | `help` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/help` |  |
| `openclaw-dmp-hreflang-check` | `hreflang-check` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/hreflang-check` |  |
| `openclaw-dmp-image-seo-audit` | `image-seo-audit` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/image-seo-audit` |  |
| `openclaw-dmp-import-guidelines` | `import-guidelines` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/import-guidelines` |  |
| `openclaw-dmp-import-sop` | `import-sop` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/import-sop` |  |
| `openclaw-dmp-import-template` | `import-template` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/import-template` |  |
| `openclaw-dmp-influencer-brief` | `influencer-brief` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/influencer-brief` |  |
| `openclaw-dmp-influencer-creator` | `influencer-creator` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/influencer-creator` |  |
| `openclaw-dmp-integrations` | `integrations` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/integrations` |  |
| `openclaw-dmp-intelligence-report` | `intelligence-report` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/intelligence-report` |  |
| `openclaw-dmp-journey-design` | `journey-design` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/journey-design` |  |
| `openclaw-dmp-keyword-cluster` | `keyword-cluster` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/keyword-cluster` |  |
| `openclaw-dmp-keyword-research` | `keyword-research` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/keyword-research` |  |
| `openclaw-dmp-landing-page-audit` | `landing-page-audit` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/landing-page-audit` |  |
| `openclaw-dmp-language-audit` | `language-audit` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/language-audit` |  |
| `openclaw-dmp-language-config` | `language-config` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/language-config` |  |
| `openclaw-dmp-launch-ad-campaign` | `launch-ad-campaign` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/launch-ad-campaign` |  |
| `openclaw-dmp-launch-campaign` | `launch-campaign` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/launch-campaign` |  |
| `openclaw-dmp-launch-plan` | `launch-plan` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/launch-plan` |  |
| `openclaw-dmp-lead-import` | `lead-import` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/lead-import` |  |
| `openclaw-dmp-learn` | `learn` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/learn` |  |
| `openclaw-dmp-live-dashboard` | `live-dashboard` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/live-dashboard` |  |
| `openclaw-dmp-local-seo` | `local-seo` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/local-seo` |  |
| `openclaw-dmp-local-seo-audit` | `local-seo-audit` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/local-seo-audit` |  |
| `openclaw-dmp-localize-campaign` | `localize-campaign` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/localize-campaign` |  |
| `openclaw-dmp-loop-detect` | `loop-detect` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/loop-detect` |  |
| `openclaw-dmp-market-weather` | `market-weather` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/market-weather` |  |
| `openclaw-dmp-marketing-automation` | `marketing-automation` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/marketing-automation` |  |
| `openclaw-dmp-martech-audit` | `martech-audit` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/martech-audit` |  |
| `openclaw-dmp-media-plan` | `media-plan` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/media-plan` |  |
| `openclaw-dmp-message-test` | `message-test` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/message-test` |  |
| `openclaw-dmp-multilingual-score` | `multilingual-score` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/multilingual-score` |  |
| `openclaw-dmp-narrative-landscape` | `narrative-landscape` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/narrative-landscape` |  |
| `openclaw-dmp-narrative-tracker` | `narrative-tracker` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/narrative-tracker` |  |
| `openclaw-dmp-page-seo-analysis` | `page-seo-analysis` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/page-seo-analysis` |  |
| `openclaw-dmp-paid-advertising` | `paid-advertising` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/paid-advertising` |  |
| `openclaw-dmp-pdf-report` | `pdf-report` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/pdf-report` |  |
| `openclaw-dmp-performance-check` | `performance-check` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/performance-check` |  |
| `openclaw-dmp-performance-report` | `performance-report` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/performance-report` |  |
| `openclaw-dmp-pipeline-update` | `pipeline-update` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/pipeline-update` |  |
| `openclaw-dmp-pr-pitch` | `pr-pitch` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/pr-pitch` |  |
| `openclaw-dmp-pricing-test` | `pricing-test` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/pricing-test` |  |
| `openclaw-dmp-programmatic-seo` | `programmatic-seo` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/programmatic-seo` |  |
| `openclaw-dmp-prompt-test` | `prompt-test` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/prompt-test` |  |
| `openclaw-dmp-publish-blog` | `publish-blog` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/publish-blog` |  |
| `openclaw-dmp-qbr-plan` | `qbr-plan` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/qbr-plan` |  |
| `openclaw-dmp-quality-report` | `quality-report` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/quality-report` |  |
| `openclaw-dmp-rank-monitor` | `rank-monitor` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/rank-monitor` |  |
| `openclaw-dmp-recall` | `recall` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/recall` |  |
| `openclaw-dmp-redirect-manager` | `redirect-manager` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/redirect-manager` |  |
| `openclaw-dmp-region-config` | `region-config` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/region-config` |  |
| `openclaw-dmp-reputation-management` | `reputation-management` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/reputation-management` |  |
| `openclaw-dmp-retargeting-strategy` | `retargeting-strategy` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/retargeting-strategy` |  |
| `openclaw-dmp-review-response` | `review-response` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/review-response` |  |
| `openclaw-dmp-roi-calculator` | `roi-calculator` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/roi-calculator` |  |
| `openclaw-dmp-save-knowledge` | `save-knowledge` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/save-knowledge` |  |
| `openclaw-dmp-schedule-social` | `schedule-social` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/schedule-social` |  |
| `openclaw-dmp-search-knowledge` | `search-knowledge` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/search-knowledge` |  |
| `openclaw-dmp-segment-audience` | `segment-audience` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/segment-audience` |  |
| `openclaw-dmp-send-email-campaign` | `send-email-campaign` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/send-email-campaign` |  |
| `openclaw-dmp-send-notification` | `send-notification` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/send-notification` |  |
| `openclaw-dmp-send-report` | `send-report` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/send-report` |  |
| `openclaw-dmp-send-sms` | `send-sms` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/send-sms` |  |
| `openclaw-dmp-seo-audit` | `seo-audit` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/seo-audit` |  |
| `openclaw-dmp-seo-drift` | `seo-drift` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/seo-drift` |  |
| `openclaw-dmp-seo-implement` | `seo-implement` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/seo-implement` |  |
| `openclaw-dmp-seo-plan` | `seo-plan` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/seo-plan` |  |
| `openclaw-dmp-serp-tracker` | `serp-tracker` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/serp-tracker` |  |
| `openclaw-dmp-share-of-voice` | `share-of-voice` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/share-of-voice` |  |
| `openclaw-dmp-simulate` | `simulate` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/simulate` |  |
| `openclaw-dmp-sitemap-manager` | `sitemap-manager` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/sitemap-manager` |  |
| `openclaw-dmp-social-strategy` | `social-strategy` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/social-strategy` |  |
| `openclaw-dmp-sop-library` | `sop-library` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/sop-library` |  |
| `openclaw-dmp-status` | `status` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/status` |  |
| `openclaw-dmp-switch-brand` | `switch-brand` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/switch-brand` |  |
| `openclaw-dmp-sync-memory` | `sync-memory` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/sync-memory` |  |
| `openclaw-dmp-team-assign` | `team-assign` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/team-assign` |  |
| `openclaw-dmp-tech-seo-audit` | `tech-seo-audit` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/tech-seo-audit` |  |
| `openclaw-dmp-technical-seo` | `technical-seo` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/technical-seo` |  |
| `openclaw-dmp-translate-content` | `translate-content` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/translate-content` |  |
| `openclaw-dmp-validate-output` | `validate-output` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/validate-output` |  |
| `openclaw-dmp-validate-profile` | `validate-profile` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/validate-profile` |  |
| `openclaw-dmp-verify-claims` | `verify-claims` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/verify-claims` |  |
| `openclaw-dmp-video-script` | `video-script` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/video-script` |  |
| `openclaw-dmp-webinar-plan` | `webinar-plan` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/webinar-plan` |  |
| `openclaw-dmp-what-if` | `what-if` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/what-if` |  |
| `openclaw-dmp-yearly-planner` | `yearly-planner` | `/Users/joergpeetz/.openclaw/workspace/skills/dmp/yearly-planner` |  |
| `openclaw-docker-compose-patterns` | `docker-compose-patterns` | `/Users/joergpeetz/.openclaw/workspace/skills/docker-compose-patterns` |  |
| `openclaw-documentation-generation` | `documentation-generation` | `/Users/joergpeetz/.openclaw/workspace/skills/documentation-generation` |  |
| `openclaw-dotenv` | `dotenv` | `/Users/joergpeetz/.openclaw/tools/node/npm/lib/node_modules/@steipete/oracle/node_modules/dotenv/skills/dotenv` |  |
| `openclaw-dotenvx` | `dotenvx` | `/Users/joergpeetz/.openclaw/tools/node/npm/lib/node_modules/@steipete/oracle/node_modules/dotenv/skills/dotenvx` |  |
| `openclaw-fastapi` | `fastapi` | `/Users/joergpeetz/.openclaw/headroom-venv/lib/python3.14/site-packages/fastapi/.agents/skills/fastapi` |  |
| `openclaw-git-workflow` | `git-workflow` | `/Users/joergpeetz/.openclaw/workspace/skills/git-workflow` |  |
| `openclaw-knowledge-management-vault` | `knowledge-management-vault` | `/Users/joergpeetz/.openclaw/workspace/skills/knowledge-management-vault` |  |
| `openclaw-llm-guardrails-security` | `llm-guardrails-security` | `/Users/joergpeetz/.openclaw/workspace/skills/llm-guardrails-security` |  |
| `openclaw-memex-search` | `memex-search` | `/Users/joergpeetz/.openclaw/tmp/clawhub-github-publish-2mALTO/skills/memex-search` | `/Users/joergpeetz/.openclaw/tmp/clawhub-github-publish-yC51Bw/skills/memex-search` |
| `openclaw-ml-pipeline` | `ml-pipeline` | `/Users/joergpeetz/.openclaw/workspace/skills/ml-pipeline` |  |
| `openclaw-mobile-accessibility-native` | `mobile-accessibility-native` | `/Users/joergpeetz/.openclaw/workspace/skills/mobile-accessibility-native` |  |
| `openclaw-mobile-development` | `mobile-development` | `/Users/joergpeetz/.openclaw/workspace/skills/mobile-development` |  |
| `openclaw-n8n-operations` | `n8n-operations` | `/Users/joergpeetz/.openclaw/workspace/skills/n8n-operations` |  |
| `openclaw-n8n-workflow-automation` | `n8n-workflow-automation` | `/Users/joergpeetz/.openclaw/workspace/skills/n8n-workflow-automation` |  |
| `openclaw-nlp-engineering` | `nlp-engineering` | `/Users/joergpeetz/.openclaw/workspace/skills/nlp-engineering` |  |
| `openclaw-observability-monitoring` | `observability-monitoring` | `/Users/joergpeetz/.openclaw/workspace/skills/observability-monitoring` |  |
| `openclaw-openapi-spec-generator` | `openapi-spec-generator` | `/Users/joergpeetz/.openclaw/workspace/skills/openapi-spec-generator` |  |
| `openclaw-playwright-e2e-testing` | `playwright-e2e-testing` | `/Users/joergpeetz/.openclaw/workspace/skills/playwright-e2e-testing` |  |
| `openclaw-postgresql-advanced-sql` | `postgresql-advanced-sql` | `/Users/joergpeetz/.openclaw/workspace/skills/postgresql-advanced-sql` |  |
| `openclaw-prompt-engineering` | `prompt-engineering` | `/Users/joergpeetz/.openclaw/workspace/skills/prompt-engineering` |  |
| `openclaw-rag-system-architecture` | `rag-system-architecture` | `/Users/joergpeetz/.openclaw/workspace/skills/rag-system-architecture` |  |
| `openclaw-secondbrain-vault-consolidation` | `secondbrain-vault-consolidation` | `/Users/joergpeetz/.openclaw/workspace/skills/secondbrain-vault-consolidation` |  |
| `openclaw-security-auditing` | `security-auditing` | `/Users/joergpeetz/.openclaw/workspace/skills/security-auditing` |  |
| `openclaw-seo-geo-optimization` | `seo-geo-optimization` | `/Users/joergpeetz/.openclaw/workspace/skills/seo-geo-optimization` |  |
| `openclaw-supabase` | `supabase` | `/Users/joergpeetz/.openclaw/workspace/.agents/skills/supabase` | `/Users/joergpeetz/.openclaw/workspace/.claude/skills/supabase`<br>`/Users/joergpeetz/.openclaw/workspace/.hermes/skills/supabase`<br>`/Users/joergpeetz/.openclaw/workspace/skills/supabase` |
| `openclaw-supabase-postgres-best-practices` | `supabase-postgres-best-practices` | `/Users/joergpeetz/.openclaw/workspace/.agents/skills/supabase-postgres-best-practices` | `/Users/joergpeetz/.openclaw/workspace/.claude/skills/supabase-postgres-best-practices`<br>`/Users/joergpeetz/.openclaw/workspace/.hermes/skills/supabase-postgres-best-practices`<br>`/Users/joergpeetz/.openclaw/workspace/skills/supabase-postgres-best-practices` |
| `openclaw-supabase-server` | `supabase-server` | `/Users/joergpeetz/.openclaw/tmp/skills-mPxEtK/skills/supabase-server` | `/Users/joergpeetz/.openclaw/workspace/.agents/skills/supabase-server`<br>`/Users/joergpeetz/.openclaw/workspace/.claude/skills/supabase-server`<br>`/Users/joergpeetz/.openclaw/workspace/.hermes/skills/supabase-server`<br>`/Users/joergpeetz/.openclaw/workspace/skills/supabase-server` |
| `openclaw-superpowers-brainstorming` | `brainstorming` | `/Users/joergpeetz/.openclaw/workspace/skills/superpowers/brainstorming` |  |
| `openclaw-superpowers-dispatching-parallel-agents` | `dispatching-parallel-agents` | `/Users/joergpeetz/.openclaw/workspace/skills/superpowers/dispatching-parallel-agents` |  |
| `openclaw-superpowers-executing-plans` | `executing-plans` | `/Users/joergpeetz/.openclaw/workspace/skills/superpowers/executing-plans` |  |
| `openclaw-superpowers-finishing-a-development-branch` | `finishing-a-development-branch` | `/Users/joergpeetz/.openclaw/workspace/skills/superpowers/finishing-a-development-branch` |  |
| `openclaw-superpowers-receiving-code-review` | `receiving-code-review` | `/Users/joergpeetz/.openclaw/workspace/skills/superpowers/receiving-code-review` |  |
| `openclaw-superpowers-requesting-code-review` | `requesting-code-review` | `/Users/joergpeetz/.openclaw/workspace/skills/superpowers/requesting-code-review` |  |
| `openclaw-superpowers-subagent-driven-development` | `subagent-driven-development` | `/Users/joergpeetz/.openclaw/workspace/skills/superpowers/subagent-driven-development` |  |
| `openclaw-superpowers-systematic-debugging` | `systematic-debugging` | `/Users/joergpeetz/.openclaw/workspace/skills/superpowers/systematic-debugging` |  |
| `openclaw-superpowers-test-driven-development` | `test-driven-development` | `/Users/joergpeetz/.openclaw/workspace/skills/superpowers/test-driven-development` |  |
| `openclaw-superpowers-using-git-worktrees` | `using-git-worktrees` | `/Users/joergpeetz/.openclaw/workspace/skills/superpowers/using-git-worktrees` |  |
| `openclaw-superpowers-verification-before-completion` | `verification-before-completion` | `/Users/joergpeetz/.openclaw/workspace/skills/superpowers/verification-before-completion` |  |
| `openclaw-superpowers-writing-plans` | `writing-plans` | `/Users/joergpeetz/.openclaw/workspace/skills/superpowers/writing-plans` |  |
| `openclaw-superpowers-writing-skills` | `writing-skills` | `/Users/joergpeetz/.openclaw/workspace/skills/superpowers/writing-skills` |  |
| `openclaw-systematic-debugging` | `systematic-debugging` | `/Users/joergpeetz/.openclaw/workspace/skills/systematic-debugging` |  |
| `openclaw-tavily` | `tavily` | `/Users/joergpeetz/.openclaw/npm/projects/openclaw-tavily-plugin-8ad843922d__openclaw-generation__g-259a9119e3e24c7e/node_modules/@openclaw/tavily-plugin/skills/tavily` |  |
| `openclaw-testing-methodology` | `testing-methodology` | `/Users/joergpeetz/.openclaw/workspace/skills/testing-methodology` |  |
| `openclaw-typer` | `typer` | `/Users/joergpeetz/.openclaw/headroom-venv/lib/python3.14/site-packages/typer/.agents/skills/typer` |  |
| `openclaw-ui-ux-pro-max` | `ui-ux-pro-max` | `/Users/joergpeetz/.openclaw/workspace/skills/ui-ux-pro-max` |  |
| `openclaw-video-production-pipeline` | `video-production-pipeline` | `/Users/joergpeetz/.openclaw/workspace/skills/video-production-pipeline` |  |
| `openclaw-web-accessibility-auditor` | `web-accessibility-auditor` | `/Users/joergpeetz/.openclaw/workspace/skills/web-accessibility-auditor` |  |
| `openclaw-web-performance-optimization` | `web-performance-optimization` | `/Users/joergpeetz/.openclaw/workspace/skills/web-performance-optimization` |  |
| `openclaw-wordpress-fullstack-development` | `wordpress-fullstack-development` | `/Users/joergpeetz/.openclaw/workspace/skills/wordpress-fullstack-development` |  |
| `openclaw-wordpress-router` | `wordpress-router` | `/Users/joergpeetz/.openclaw/tmp/skills-oVQAAh/skills/wordpress-router` |  |
| `openclaw-workspace-projects-forgenet` | `docs` | `/Users/joergpeetz/.openclaw/workspace/projects/forgenet/docs` |  |
| `openclaw-wp-abilities-api` | `wp-abilities-api` | `/Users/joergpeetz/.openclaw/tmp/skills-oVQAAh/skills/wp-abilities-api` |  |
| `openclaw-wp-abilities-audit` | `wp-abilities-audit` | `/Users/joergpeetz/.openclaw/tmp/skills-oVQAAh/skills/wp-abilities-audit` |  |
| `openclaw-wp-abilities-verify` | `wp-abilities-verify` | `/Users/joergpeetz/.openclaw/tmp/skills-oVQAAh/skills/wp-abilities-verify` |  |
| `openclaw-wp-block-development` | `wp-block-development` | `/Users/joergpeetz/.openclaw/tmp/skills-oVQAAh/skills/wp-block-development` |  |
| `openclaw-wp-block-themes` | `wp-block-themes` | `/Users/joergpeetz/.openclaw/tmp/skills-oVQAAh/skills/wp-block-themes` |  |
| `openclaw-wp-interactivity-api` | `wp-interactivity-api` | `/Users/joergpeetz/.openclaw/tmp/skills-oVQAAh/skills/wp-interactivity-api` |  |
| `openclaw-wp-patterns` | `wp-patterns` | `/Users/joergpeetz/.openclaw/tmp/skills-oVQAAh/skills/wp-patterns` |  |
| `openclaw-wp-performance` | `wp-performance` | `/Users/joergpeetz/.openclaw/tmp/skills-oVQAAh/skills/wp-performance` |  |
| `openclaw-wp-phpstan` | `wp-phpstan` | `/Users/joergpeetz/.openclaw/tmp/skills-oVQAAh/skills/wp-phpstan` |  |
| `openclaw-wp-playground` | `wp-playground` | `/Users/joergpeetz/.openclaw/tmp/skills-oVQAAh/skills/wp-playground` |  |
| `openclaw-wp-plugin-development` | `wp-plugin-development` | `/Users/joergpeetz/.openclaw/tmp/skills-oVQAAh/skills/wp-plugin-development` |  |
| `openclaw-wp-plugin-directory-guidelines` | `wp-plugin-directory-guidelines` | `/Users/joergpeetz/.openclaw/tmp/skills-oVQAAh/skills/wp-plugin-directory-guidelines` |  |
| `openclaw-wp-project-triage` | `wp-project-triage` | `/Users/joergpeetz/.openclaw/tmp/skills-oVQAAh/skills/wp-project-triage` |  |
| `openclaw-wp-rest-api` | `wp-rest-api` | `/Users/joergpeetz/.openclaw/tmp/skills-oVQAAh/skills/wp-rest-api` |  |
| `openclaw-wp-wpcli-and-ops` | `wp-wpcli-and-ops` | `/Users/joergpeetz/.openclaw/tmp/skills-oVQAAh/skills/wp-wpcli-and-ops` |  |
| `openclaw-wpds` | `wpds` | `/Users/joergpeetz/.openclaw/tmp/skills-oVQAAh/skills/wpds` |  |
