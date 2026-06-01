
## 2026-05-21 — Memory Architecture Decision (CEO)

**Decision:** Obsidian vault (`~/obsidian-vault/AgentForge/`) and MeMex Zero RAG (`~/workspace/MeMex-Zero-RAG/wiki/agentforge/`) are designated as the **canonical long-term memory** for all agents going forward.

**Rationale:** 
- Local knowledge systems reduce token usage over time
- Agents should never re-query external sources for information already captured locally
- MEMORY.md remains as a secondary convenience cache, not the primary memory store

**Consultation order for all agents:**
1. MeMex Zero RAG (structured wiki)
2. Obsidian vault (narrative, linked)
3. External (web search / AI query) — only as last resort

**Scope:** Applies to Marvin (CEO) and all new agents created going forward.

**Logged by:** CEO (Marvin)

## 2026-05-22 — Board Decisions (Model Policy & Pipeline Handoff)

### Model Policy
- **owl-alpha**: low-hit-rate/low-impact tasks only
- **DeepSeek V4 Pro**: all high-quality work (CEO + all department agents)
- **Expiry**: 2026-05-31 — review then
- **Reminder set**: cron job e7021d89 fires 09:00 IE 2026-05-31

### Pipeline Handoff
- Adopt structured JSON artifact approach from agent-handoff-schema.md v1.0
- Canonical handoff path: MeMex Zero RAG + Obsidian vault
- File-based gating (daily-pipeline/) is deprecated in favor of typed artifacts

### Preserved from Hermes
- Self-improving skill loop concept → implement via OpenClaw skills + skill-creator
- FTS5 session search → OpenClaw memory_search / QMD backend
- Honcho user modeling → OpenClaw memory engines
- Cron-native scheduling → OpenClaw cron (already in use)
- Multi-platform gateway → OpenClaw channels (already in use)

## 2026-05-22 — Tier 1 Deployment Complete

### Deployed
- **6 agents total:** CEO (main) + 5 department agents (content, seo, social, pdf, analytics)
- **Model policy:** OpenRouter only — all Claude models stripped
- **3 cron jobs:** content_pipeline_daily (Mon-Fri 08:30 IE), analytics_weekly_report (Mon 09:00 IE), model_policy_review (2026-05-31)
- **Agent registries:** 5 active agents registered in MeMex + Obsidian
- **Standby registry:** 8 agents (prompts, wp-design, hiring, research, comms, niche-scout, ops, design) — on-demand activation
- **Artifact structure:** MeMex/Obsidian mirror at artifacts/YYYY/MM/<pipeline>/
- **Handoff mechanism:** JSON artifacts v1.0 (poll-based downstream, cron-initiated upstream)

### Next: Tier 2 — Skill Packs
- 8 AgentForge skill packs to create in ~/.openclaw/skills/agentforge/
- Wire downstream agents to poll MeMex for artifacts
- End-to-end pipeline test: Content fires → produces artifacts → SEO polls → scores

- [2026-05-23] [DECISION]: App Discovery Department created. VP of App Strategy (Alex) as C-level orchestrator, OpenClaw native. Daily pipeline: Scout (8-15 candidates) → GEO (competitive matrix via seo-api-nu.vercel.app) → Score (5-dimension kill-floor) → Scrutiny (full 5-section Zero-Day Dominance Report) → Report (Telegram). Cron: Mon-Fri 06:00 Dublin. Replaces old ClaudeClaw niche-scout.

- [2026-05-24] [DECISION]: App Discovery fixes applied. SearXNG enabled in plugin config. Web search provider switched to Tavily. Scoring framework updated: "SEO/ASO Opportunity" dimension — mobile apps scored on ASO (App Store rankings, reviews, category competitiveness) not web SEO. Cron payload modularized into 5 distinct phases. Runner-up watchlist created at MeMex/artifacts/app-discovery/watchlist.md. Cron confirmed operational (previous run: 4min, delivered to Telegram).

- [2026-05-24] [DECISION]: App Discovery extended with Phase 6 — Superhuman Scaffolding Prompt. New phase triggers after Build verdict. Produces complete 12-section app architecture blueprint: App Identity (ASO-optimized name/subtitle/visuals), iOS Architecture (SwiftUI, RevenueCat, WidgetKit, SwiftData, screen-by-screen spec), Android Architecture (Jetpack Compose, Play Billing, Material You, WorkManager), SEO/GEO Optimization (keyword field, description copy, landing page, GEO FAQ structure, schema markup), Behavioral Architecture (Hook Model — triggers, actions, variable rewards, investments), Visual Design System (animations, haptics, accessibility as luxury, color psychology), Financial Architecture (pricing tiers, unit economics, cancellation intercept flow), Virality Engine (shareable moments, invite mechanics, rating protection), Technical Spec (DB schema, API endpoints, push notification schema), 30-Day MVP Sprint (daily tasks iOS/Android/shared, feature cut list), Launch Checklist (T-14 through T+0), Post-Launch Iteration (observe/review/ship cadence), Anti-Patterns (10 things to never do). Template: ~/.openclaw/agents/app-discovery/scaffolding-prompt.md. Cron updated from 5-phase to 6-phase. Pipeline: Scout → GEO → Score → Scrutiny → Build(Scaffold) → Report.

- [2026-05-24] [DECISION]: ai-agents-from-scratch (pguso/pguso) integrated into AgentForge. Applied in two places: (1) BiteSaver scaffold Section 8.4 — AI Agent Architecture — local-first ReAct pattern for recipe extraction, meal planning, dietary adaptation using llama.cpp/MediaPipe/MLX Swift with Phi-4-mini, following the repo's intro→translation→react-agent→coding→scaling learning path. (2) Hiring department standards — new quality benchmarks doc at MeMex/agents/hiring-standards.md defining 5-level checklist (Fundamentals→Tool Architecture→Agent Loop→Memory→Production Readiness→Local-First Capability) plus adversarial review process. All future agents must pass before deployment. Scaffolding prompt template permanently updated with Section 8.4 (local-first AI architecture). Obsidian mirrors updated.

- [2026-05-24] [DECISION]: Astra Ad Department created. Agent ID: advertisement. Registered in openclaw.json. SOUL.md + AGENTS.md deployed. Pipeline: 8-phase end-to-end advertising: Research → Strategy → Concept → Production → SEO/GEO → A/B Matrix → Claims Check → Export. Covers X, TikTok, Instagram. Quality gates: 10+ headlines, 15+ hooks, platform-native concepts, video storyboards + shot lists + scripts, keyword architecture, schema markup, brand safety review. Adversarial review passed — see hiring department for full assessment. Activation: on-demand, brief-driven. Output to MeMex artifacts + Obsidian.

- [2026-05-24] [DECISION v2]: Astra Ad Department fully upgraded. AGENTS.md now 414 lines covering: 7-stage campaign method (Diagnose→Research→Strategize→Create→Optimize→QC→Export), 9-category research framework, 14-item creative standard minimums, platform-native rules for X/TikTok/Instagram, image generation tool logic (FLUX photorealism/stylized/fast-iteration/brand-consistency workflows via fal.ai), video generation tool logic (short-form social/cinematic/avatar/motion-graphics), per-asset tool stack rationales with engine-aware prompts, full production stack integration (fal-ai/flux, video_generate, music_generate, image_generate). Uses AgentForge's already-available tools — no external tool dependency. Decision framework for tool selection: output objective, realism, style, speed, platform, format, budget, scale, fidelity, animation, brand consistency.

- [2026-05-24] [DECISION v3]: Astra Ad Dept tool stack upgraded to explicit model routing. Image: fal.ai FLUX (schnell/dev/pro-ultra tiers) as primary, image_generate as fallback. Video: Runway Gen-4.5 primary for premium ads, Luma Dream Machine secondary for rapid iteration, video_generate for motion graphics/avatars. Audio: music_generate. Routing rule: still → FLUX, premium video → Runway, rapid tests → Luma, motion graphics → video_generate. Every asset now specifies: primary tool, secondary fallback, why chosen, expected quality, export settings, engine-aware prompt variant, seed values.

- [2026-05-24] [DECISION]: AgentForge capabilities packaged as Agent Skills (agentskills.io open standard). Three skills created: (1) app-discovery-scrutiny — "Zero-Day Dominance Report" framework, 5-section VC/PM/behavioral analysis ending in Build/Pivot/Kill. (2) app-scaffolding — 12-section mobile app build blueprint covering iOS/Android/ASO/Hooked Model/financial/virality/30-day sprint. (3) astra-campaign — full-service ad campaign generator, 7-phase Diagnose→Research→Strategize→Create→Optimize→QC→Export. All three use progressive disclosure (name+description loaded at startup, full instructions only when task matches). Cross-platform: works on OpenClaw, Claude Code, Codex, Cursor, Hermes Agent, any skills-compatible agent. Stored at ~/.openclaw/workspace/skills/. This closes the loop with Hermes Agent's self-improving skills architecture.

## 2026-05-25 — Social Distribution Approval

- **[DECISION]:** Social distribution for "AI Agent Orchestration in 2026" (Run #1, sd-f3a9b4c2) APPROVED for posting.
  - SEO: 79/100 (below ≥80 full-auto threshold — CEO review required per standing orders)
  - Platforms: Reddit (r/LocalLLaMA), Hacker News (Show HN), X/Twitter (5-tweet thread), LinkedIn, Dev.to
  - Rationale: Social content quality is high — platform-specific adaptations, value-first framing, contrarian hook. Risk of posting sub-80 SEO score article is low because the article itself is 3,091 words of original technical content with 7 real-world patterns. The SEO score was docked for metadata/schema issues (which don't affect social), not content quality.
  - CEO: Marvin | Signed: 2026-05-25 16:40 IST
- [2026-05-26] [DECISION]: Prompts Foundry activated. Mirrors skill-foundry architecture. Nightly 01:00 Dublin via Flash model. 17-domain rotation. Output: 3-5 improved cross-platform prompts per run to MeMex artifacts/prompts-foundry/. GitHub repo at 50 prompts (per standing policy).

- [2026-05-31] [DECISION — Model Policy Review]: The owl-alpha restriction expired today. 9-day performance review complete.

  **Data reviewed:**
  - All 20+ sessions across 4 agents (CEO, app-discovery, skill-foundry, main)
  - 6 content pipeline runs (May 23-29), 3 SEO audits, 2 social distributions
  - CodexBar cost data (no Codex usage — all OpenRouter)

  **Findings:**
  - owl-alpha: ZERO sessions in 9 days. Never selected by any agent or pipeline.
  - DeepSeek V4 Pro: 100% of high-quality work (CEO, pipelines, subagents). SEO scores improving: 65 → 78 → 90%.
  - DeepSeek V4 Flash: All nightly cron jobs (skill foundry, prompts foundry, backups)
  - Fallback chain (minimax → kimi → flash → owl-alpha): owl-alpha is last resort, never triggered.

  **Decision: SUNSET owl-alpha.** Remove from fallback chain entirely. The two-tier DeepSeek split (V4 Pro for quality, Flash for background) is performing well and needs no policy intervention — it's organically self-enforcing.

  **New model policy (no expiry):**
  - DeepSeek V4 Pro: CEO, all department agents, content pipeline, SEO, app discovery, social, PDF — all high-quality/production work
  - DeepSeek V4 Flash: Nightly/low-priority background jobs (skill foundry, prompts foundry, backups, healthchecks)
  - owl-alpha: REMOVED. Not in fallback chain.

  **Fallback chain (revised):** minimax/m2.7 → kimi/k2.6 → deepseek-v4-flash

  **Rationale:** owl-alpha had 402 credit issues on May 22 and was never organically selected. The policy wasn't needed — agents naturally chose the right model. Removing it simplifies the config and eliminates a known-unreliable provider.
