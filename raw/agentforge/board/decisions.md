# Decisions

> Chronological log of all major decisions made by the Board (Joerg) and CEO (Marvin).
> **Related:** [[Board-Directives]], [[Lessons-Learned]]

---

## 2026-07-17
- **SecondBrain vault created** — unified Obsidian memory for all AgentForge departments
- **Absolute path lesson** — all script file arguments must use absolute paths going forward
- **Image 3 (Beach Yoga)** approved for Feel-Good Friday, posted to all platforms

## 2026-07-15
- **Prime Directive: Failure Auto-Resolution** — research memory → fix → finish. Escalate after 3 failures.
- **Marketing Image Review** — all images presented to Board for final approval, no auto-posting

## 2026-07-14
- **SkillClaw + Skill Foundry** — integrate, don't replace. SkillClaw drafts → Skill Foundry reviews/approves
- **Memory search fix** — switched from Ollama to OpenRouter for embeddings

## 2026-07-13
- **Cron timeout** → 900s (15 min), idempotency guard added (Phase 0.5)
- **Duplicate posts** — cleanup executed, guard prevents recurrence

## 2026-07-07
- **Image quality standard** — no PIL overlays, handles in captions only, 7-question visual audit
- **BetterLife image pipeline** — FLUX/kie.ai output = final image

## 2026-07-06
- **Pipeline gap identified** — cron generates + reviews but no auto-posting trigger. Phase 3 needed.

## 2026-07-05
- **Sunday Reflection** posted — brand audit clean, #BetterLife over #BetterLifeCare

## 2026-06-29
- **"Post Everywhere"** — Board instruction for Monday motivation image
- **Session Boundary Protocol** added to SOUL.md
- **Marketing playbook** deployed as live skill
- **Memory index** — switched from OpenAI to Ollama embeddings

## 2026-06-25
- **X API Free tier** — confirmed post-only. Upgrade needed for read/search.

## 2026-06-22
- **BetterLife.care domain** created, emails configured, social accounts created

## 2026-06-19
- **BetterLife approved** on App Store (v1.0.5, iOS 26.2+, Health & Fitness)

## 2026-07-14
- **SkillClaw + Skill Foundry integration approved** — SkillClaw drafts, Skill Foundry reviews/approves (3-layer integration)
- **Memory search provider switched** — Ollama → OpenRouter-compatible (text-embedding-3-small), index rebuilt
- **SkillForge concept created** — Combine SkillClaw + Skill Foundry into single OSS platform

## 2026-07-05
- **T3MP3ST Dashboard** — Production-ready code-audit vertical
- **Sunday Reflection posted** — brand audit passed, all platforms live

## 2026-07-03
- **Unified watermark mandate** — ALL social images use `betterlife-watermark-unified.jpg` — never substitute
- **Agent Marketplace Solana** — Land first + waitlist first recommendation (Phase 0)
- **CashClaw archived** — agent config created but not deployed (dormant)

## 2026-06-30
- **LinkedIn OAuth integration completed** — 3-legged auth without PKCE, 2-month token TTL
- **Skill Foundry Run #5** — 20 candidates → 5 skills shipped (Agentic Security Scanner, API Contract Testing, SRE Runbooks, LLM Security Red Teaming, Database Schema Designer)

## 2026-06-28
- **GitHub Department (OctoForge) created** — Agent ID `github-dept`, 4-tier repo monitoring
- **Awesome Generative AI Apps analyzed** — 45 apps across 10 categories, 4 high-potential identified
- **Pre-Mortem Skill adopted** — from Board's Google Drive, translated from Spanish

## 2026-06-25
- **Marketing Cost Analysis** — $0-First Rule: shell/Python for execution, cheap models for formatting, expensive models for reasoning only
- **X API Free tier** — confirmed post-only. Reply engagement blocked. Upgrade needed for read/search
- **Skill Foundry Run #4** — 5 skills shipped (Design-to-Code, GraphQL API, Privacy Compliance, Production Engineering, Documentation)
- **BetterLife social launch** — First tweet and FB/IG posts live

## 2026-06-22
- **BetterLife.care domain** created, emails configured, social accounts created
- **Instagram Business connected** to Facebook Page — FB CDN workaround for IG posting

## 2026-06-29
- **FinanceFlow decoupled from Racing** — Remove racing integration from FinanceFlow. Migrate from Gemini CLI to OpenRouter API. Prepare for market launch.
- **JP Technologies portfolio page** — https://jp-technologies.vercel.app — unified landing page for all 7 ventures

## 2026-06-27
- **Gemini CLI** — Registered as CLI tool for FinanceFlow (racing research, invoice analysis, structured extraction). Source: Claude CLI independent brain note.

## 2026-06-19
- **BetterLife approved** on App Store (v1.0.5, iOS 26.2+, Health & Fitness)
- **AdForge System Prompt v2.0** — full ad creative workflow (Foreplay.co replica) archived for prompts dept
- **Competitive analysis completed** — BetterLife uniquely in top-right quadrant: AI-Powered × Cross-Domain

## 2026-06-16
- **Skill Foundry unbounded growth** — NO skill count cap. Board clarified: GitHub topics ≠ skill count. Target trajectory: 12 → 50 → 100 → 500 → 1000+
- **Skill Foundry Run #3** — 5 skills shipped (Playwright E2E Testing, Browser Automation, Document Processing, Auth+Auth, Data Viz)

## 2026-06-12
- **Helix business model revised** — Sonnet moved to Scale tier, Opus/GPT-4.5 removed. Economically viable tiers designed.
- **Tier pricing finalized:** Starter €9 (1K/mo, 87% margin), Pro €39 (2.5K/mo, 19% margin), Scale €149 (6K/mo, 31% margin)

## 2026-06-09
- **Hermes Agent Transition Architecture** — blueprint for migrating from OpenClaw
- **Prompt Development Department** — 7-agent spec, weekly cycle, 5-dimension scoring

## 2026-06-07
- **Vane research engine** deployed at vane.sytes.net (Perplexica + SearXNG)
- **Stripe** — restricted key received, may need full sk_live_

## 2026-06-02
- **Week 1 complete** — Auth, cost tracking, MCP client, SSE streaming, Slack+Signal adapters

## 2026-06-01
- **SEO API single-point-of-failure** identified — 6 articles un-audited since May 29

## 2026-05-31
- **SUNSET owl-alpha** — removed from fallback chain. Two-tier DeepSeek formalized.

## 2026-05-30
- **RaceIntel data imported** — 493K horses, 21K trainers, 20K jockeys
- **The Racing API broken** — 404 on all endpoints. Pivoted to Kaggle dataset.
- **Vercel deployment stuck** — stale build, git mismatch. Needs manual redeploy.

## 2026-05-29
- **GallopGenius replication blueprint** — 1,409 lines, 52KB full spec
- **RaceIntel scrutiny** — 7.25/10 BUILD decision

## 2026-05-24
- **App Discovery mobile-only** — killed dev tool scoring, added Mobile-First Fit dimension
- **Astra Ad Department created** — 7-step campaign method, tool-verified
- **Closed Learning Loop designed** — Act → Reflect → Extract → Carry Forward
- **Tool honesty policy** — never claim tools without verification

## 2026-05-23
- **n8n MCP connected** — 26 tools, 101 workflows
- **FLAG auto-iteration protocol** proven working (1 cycle: 65→79)
- **Notion token** received and stored

## 2026-05-22
- **Superpowers skills ported** — 13 SKILL.md files written
- **Telegram integration** configured and gateway restarted

## 2026-05-21
- **CEO role activated** — Marvin, CEO of AgentForge
- **Memory architecture** — Obsidian + MeMex as canonical long-term memory
- **SkillsMP API** — available for all agents
- **Superpowers Framework** — available for all agents