# AgentForge Handoff Schema — Unified Context Passing Across All Pipelines

**Date:** 2026-05-22
**Status:** Draft v1
**Purpose:** Typed JSON artifact schema for passing context between agents in all AgentForge pipelines — current and future

---

## Why a Schema

When one agent hands off to the next in a pipeline, the receiving agent needs:
1. **What happened before** (prior results, not just a summary)
2. **What to do next** (next step instructions, not a wall of text)
3. **Quality bar** (what "done" looks like)
4. **Escalation trigger** (when to stop and flag)

Codebuff's `outputSchema` + `set_output` pattern addresses this. AgentForge already has an `agent-handoff-protocol.md` with the concept but no enforced typing. This schema makes it machine-readable and agent-native.

---

## Core Principle

**Every pipeline agent outputs one `handoff-artifact.json`** at the end of its run. The next agent reads it as its first input. No free-text summaries as primary context carriers — those are secondary human-facing outputs.

---

## Universal Fields (all agents)

Every handoff artifact contains:

```json
{
  "schema_version": "1.0",
  "artifact_id": "uuid-v4",
  "agent": "content | seo | social | pdf | wp-design | prompts | analytics | hiring | ... ",
  "mission_id": "uuid-v4",
  "pipeline": "content | wp-design | prompts | ... ",
  "stage": "stage name",
  "status": "complete | escalated | failed",
  "timestamp": "ISO-8601",

  "input_received": {
    "mission_id": "...",
    "prior_artifact_id": "uuid or null if first",
    "original_request": "..."
  },

  "output": { /* agent-type-specific, see below */ },

  "quality": {
    "confidence": 0.0-1.0,
    "score": null | number,
    "checks_passed": ["..."],
    "checks_failed": ["..."]
  },

  "escalation": {
    "triggered": false,
    "reason": null | "low_confidence" | "conflicting_data" | "resource_blocked" | "human_required",
    "detail": null | "..."
  },

  "next_steps": [
    {
      "agent": "target-agent-id",
      "action": "what to do",
      "input_artifact_id": "this artifact's id",
      "priority": 1-5
    }
  ],

  "hive_mind_signal": {
    "type": "CONTENT_PUBLISHED" | "SEO_APPROVED" | "...",
    "content": "human-readable summary",
    "confidence": 0.0-1.0
  }
}
```

---

## Pipeline-Specific Output Schemas

### `content` Pipeline
**Stages:** keyword → research → seo-check → write → review → publish
**Departments:** content, seo, social, pdf

```json
{
  "output": {
    "keyword": "...",
    "cluster": "...",
    "article": {
      "slug": "...",
      "title": "...",
      "word_count": 0,
      "sections": [
        {
          "heading": "...",
          "word_count": 0,
          "keywords_used": ["..."],
          "citations": ["..."]
        }
      ],
      "seo_score": 0.0,
      "plagiarism_score": 0.0,
      "readability_score": 0.0,
      "tone_consistency": 0.0
    },
    "media": {
      "images": [{ "alt": "...", "caption": "...", "generated": true|false, "asset_id": "..." }],
      "featured_image_url": "..."
    },
    "publish": {
      "target_url": "https://agent-forge.co/{slug}/",
      "wordpress_status": "draft | publish | future",
      "categories": ["..."],
      "tags": ["..."]
    }
  }
}
```

### `prompts` Pipeline
**Stages:** bundle → optimise → test → review → publish
**Departments:** prompts, hiring (skill sourcing)

```json
{
  "output": {
    "bundle": {
      "name": "...",
      "category": "...",
      "prompt_count": 0,
      "description": "...",
      "tags": ["..."],
      "license": "MIT | proprietary",
      "marketplace": "skillsmp | internal"
    },
    "prompts": [
      {
        "prompt_id": "uuid",
        "name": "...",
        "description": "...",
        "prompt_text": "...",
        "model": "...",
        "variables": ["..."],
        "test_result": {
          "passed": true|false,
          "score": 0.0,
          "notes": "..."
        }
      }
    ],
    "bundle_stats": {
      "avg_length_chars": 0,
      "diversity_score": 0.0,
      "test_coverage": "0%"
    }
  }
}
```

### `wp-design` Pipeline
**Stages:** spec → build → review → deliver
**Departments:** design (wp-design)

```json
{
  "output": {
    "spec": {
      "project_name": "...",
      "target_audience": "...",
      "feature_list": ["..."],
      "design_tokens": {
        "colors": { "primary": "...", "secondary": "...", "dark": "...", "light": "..." },
        "typography": { "font_family": "...", "sizes": {} },
        "spacing": { "base": "...", "scale": "..." }
      },
      "performance_targets": {
        "lcp_ms": 0,
        "fid_ms": 0,
        "cls": 0.0
      },
      "accessibility": ["WCAG-A" | "WCAG-AA"]
    },
    "build": {
      "theme_dir": "/var/www/html/wp-content/themes/...",
      "files_created": ["..."],
      "docker_image": "...",
      "core_web_vitals": {
        "lcp_ms": 0,
        "fid_ms": 0,
        "cls": 0.0
      },
      "dark_mode": true|false,
      "responsive": true|false
    },
    "review": {
      "validation_checklist": ["..."],
      "passed": true|false,
      "issues": ["..."],
      "reviewer_notes": "..."
    }
  }
}
```

### `hiring` Pipeline
**Stages:** agent-design → adversarial-review → deploy
**Departments:** hiring

```json
{
  "output": {
    "agent_design": {
      "agent_id": "...",
      "name": "...",
      "department": "...",
      "capabilities": ["..."],
      "tools": ["..."],
      "skills": ["..."],
      "claude_md": "...",
      "superpowers_skills": ["..."]
    },
    "adversarial_review": {
      "passed": true|false,
      "risk_flags": ["..."],
      "bypass_count": 0,
      "reviewer_feedback": "..."
    },
    "deployment": {
      "status": "staged | active",
      "agent_config_path": "...",
      "tested_with": ["..."]
    }
  }
}
```

### `analytics` Pipeline
**Stages:** performance-report → niche-refresh → cluster-update → recommendations
**Departments:** analytics

```json
{
  "output": {
    "performance": {
      "period": "YYYY-WW",
      "articles_published": 0,
      "top_performers": [{ "slug": "...", "traffic": 0, "ctr": 0.0, "seo_score": 0.0 }],
      "underperformers": [{ "slug": "...", "issue": "...", "fix": "..." }]
    },
    "niche_refresh": {
      "trending_tools": ["..."],
      "new_keywords": [{ "keyword": "...", "volume": 0, "difficulty": 0.0, "cluster": "..." }],
      "competitor_gaps": ["..."]
    },
    "cluster_map": {
      "updated_clusters": ["..."],
      "new_opportunities": ["..."]
    },
    "recommendations": [
      { "action": "...", "priority": 1-5, "rationale": "...", "owner": "..." }
    ]
  }
}
```

### `research` Pipeline
**Stages:** gather → analyse → synthesise → deliver
**Departments:** research, niche-scout

```json
{
  "output": {
    "research_question": "...",
    "sources": [{ "url": "...", "title": "...", "confidence": 0.0, "recency": "..." }],
    "findings": {
      "key_insights": ["..."],
      "data_points": { "...": "..." },
      "conflicting_data": [{ "source_a": "...", "source_b": "...", "delta": "..." }]
    },
    "synthesis": {
      "summary": "...",
      "confidence": 0.0,
      "recommendation": "..."
    }
  }
}
```

---

## Artifact Lifecycle

```
Agent Run Starts
    ↓
Read prior artifact (if any) from known path
    ↓
Execute task
    ↓
Write handoff-artifact.json to:
  ~/workspace/agentforge/artifacts/{pipeline}/{mission_id}/{stage}-{agent}-{timestamp}.json
    ↓
Write Hive Mind signal to log
    ↓
If escalation.triggered === true:
    → Write escalation artifact
    → Alert CEO via mission task
    → Halt pipeline until resolved
Else:
    → Next agent reads artifact and continues
```

---

## Known Artifact Paths

| Pipeline | Artifact directory |
|----------|-------------------|
| content | `~/workspace/agentforge/artifacts/content/` |
| prompts | `~/workspace/agentforge/artifacts/prompts/` |
| wp-design | `~/workspace/agentforge/artifacts/wp-design/` |
| hiring | `~/workspace/agentforge/artifacts/hiring/` |
| analytics | `~/workspace/agentforge/artifacts/analytics/` |
| research | `~/workspace/agentforge/artifacts/research/` |

---

## Schema Versioning

- `schema_version` is mandatory in every artifact
- Breaking changes bump to `2.0` with a migration note
- Agents validate incoming artifacts against their pipeline's schema
- Unknown fields are ignored (forward compatibility)

---

## Relation to Existing docs

- Supersedes: `agent-handoff-protocol.md` (2026-05-19) — same concept, typed and extended
- Extends: `wp-design-agent-handoff.md` — adds universal artifact structure to WP Design stages
- Complements: `memory-architecture.md` — handoff artifacts are runtime context; MeMex/Obsidian are long-term memory

---

**Status:** Draft v1 — Board review required before adoption
**Next:** CEO to present to Board for approval, then onboard each department agent