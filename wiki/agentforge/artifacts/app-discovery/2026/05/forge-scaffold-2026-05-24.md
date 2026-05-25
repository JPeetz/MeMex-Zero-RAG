# Forge — Superhuman App Scaffold

**Generated:** 2026-05-24 | **Pipeline:** App Discovery Daily | **Verdict:** BUILD
**Winner:** Forge — open-source reliability layer for self-hosted LLM tool-calling
**Founder:** Antoine Zambelli, AI Director at Texas Instruments
**Score:** 92/100

---

## PHASE 3 — SCORING MATRIX

| # | App | Source | Category | Market Signal (25%) | Comp Gap (20%) | SEO/ASO Opp (20%) | Monetization (20%) | Urgency (15%) | TOTAL | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **Forge** | HN (676▲, 250💬) | DevTools / AI Reliability | 25 | 18 | 18 | 16 | 15 | **92** | 🏆 BUILD |
| 2 | **Files.md** | HN (720▲, 355💬) | Note-taking / OSS | 22 | 12 | 14 | 13 | 13 | 74 | 👀 Watch |
| 3 | **Agent.email** (AgentMail YCS25) | HN (92▲, 105💬) | AI Infra / Email API | 20 | 15 | 15 | 14 | 12 | 76 | 👀 Watch |
| 4 | **Pablo (usepablo.dev)** | HN (27▲), Reddit | Chrome Ext / UI Copy | 14 | 9 | 16 | 12 | 11 | 62 | ❌ Kill |
| 5 | **ShadowCat** | HN (157▲, 60💬) | File Transfer / QR | 10 | 14 | 8 | 6 | 9 | 47 | ❌ Kill |
| 6 | **YapSnap** | HN (97▲, 45💬) | Transcription / CPU | 13 | 8 | 10 | 10 | 9 | 50 | ❌ Kill |
| 7 | **AgentLens** | HN (3▲) | AI Obs / Monitoring | 8 | 6 | 12 | 11 | 10 | 47 | ❌ Kill |
| 8 | **docx-editor (OSS)** | HN (104▲, 16💬) | DevTools / Documents | 12 | 7 | 11 | 8 | 8 | 46 | ❌ Kill |
| 9 | **Tinywind** | Reddit (258▲) | Gaming / Roguelike | 9 | 11 | 6 | 7 | 8 | 41 | ❌ Kill |
| 10 | **Superlog (YC P26)** | HN (72▲, 49💬) | Observability / DevOps | 15 | 6 | 10 | 12 | 11 | 54 | ❌ Kill |
| 11 | **Freenet** | HN (371▲, 267💬) | P2P / Decentralized | 16 | 13 | 7 | 5 | 8 | 49 | ❌ Kill |
| 12 | **SpecterSync** | HN (4▲) | Mac / GhostCMS | 5 | 10 | 9 | 9 | 7 | 40 | ❌ Kill |

### Kill Floor Analysis

- **Pablo:** Competition Gap 9/20. Pluck already dominates with structured AI prompts + Figma export. Pablo copies raw HTML/CSS only. No moat.
- **ShadowCat:** Monetization 6/20. Cute utility, zero revenue path. No one pays for QR file transfer in 2026.
- **YapSnap:** Competition Gap 8/20. Transcription market is a bloodbath (Otter, Rev, Descript, Wispr Flow, TurboScribe). CPU-only is a feature, not a business.
- **AgentLens:** Market Signal 8/25. 3 HN points. AI observability is real ($13.5B market by 2032) but this demo is too thin.
- **docx-editor (OSS):** Monetization 8/20. OSS doc editor is a commodity. Tiny addressable market of devs embedding doc editors.
- **Tinywind, Freenet, SpecterSync, Superlog:** Killed on one or more dimensions at 4/10 threshold.

---

## PHASE 4 — SCRUTINY: FORGE

### Section 1: Demand & Saturation

**Market Signal:** 676 HN points, 250 comments, cross-posted to r/LocalLLaMA, Mastodon, Reddit, covered by andrew.ooo (independent detailed review), and roipad.com. The r/LocalLLaMA community (one of the most technically demanding AI subreddits) gave it traction within 4 hours.

**Underlying Market:** The AI Agent Guardrails / Security market is projected to reach **$13.52 billion by 2032** (MarketsandMarkets), growing at 42% CAGR from $1.65B in 2026. The broader AI agent market hit $7.84B in 2025 and is projected at $52.62B by 2030. In 2026 through April alone, agentic AI companies raised $2.66B across 44 rounds.

**Saturation assessment: LOW.** Competitors like Galileo, NVIDIA NeMo Guardrails, Guardrails AI, Lakera, and Patronus AI focus on enterprise cloud deployments with content safety guardrails. Forge occupies a unique niche: **on-device, model-agnostic reliability for local/small models.** No competitor does what Forge does at the local-model level with an eval harness and interactive dashboard.

**92% of security pros are concerned about AI agents** (Darktrace 2026 survey). Only 20% of organizations have mature AI governance models (Deloitte 2026). The pain is real and under-addressed.

### Section 2: Overtake Strategy

**Primary Keyword:** "AI agent guardrails" — 42% CAGR market, keyword rapidly growing.

**Top 3 Competitors & Gaps:**

| Competitor | Strength | Gap / Forge's Advantage |
|---|---|---|
| **Galileo** | Enterprise eval-driven guardrails, full observability | Cloud-only, expensive, enterprise sales cycle. Forge: free, local, open-source, runs on $600 GPU |
| **NVIDIA NeMo Guardrails** | Deep NVIDIA ecosystem, enterprise trust | Requires NVIDIA stack, heavy, not for indie devs. Forge: model-agnostic, lightweight Python |
| **Guardrails AI / Lakera / Patronus AI** | Content safety, prompt injection detection | Focus on security/content filtering, NOT on agentic task reliability. Forge solves a different problem: making agents actually WORK correctly |

**Forge's killer gap:** Everyone else protects against bad outputs. Forge makes outputs CORRECT. Different category entirely — "agentic task reliability" vs "content safety guardrails."

### Section 3: Revenue & Success Probability

**Revenue Model (open-core + cloud):**
1. **Open-source core:** Forever free, Apache 2.0 license, GitHub stars as marketing flywheel
2. **Forge Cloud:** Managed eval dashboards, team collaboration, CI/CD integration — $29/seat/month
3. **Forge Enterprise:** On-prem deployment, SSO, audit logs, SLA — $999+/month
4. **Forge GPU:** Managed GPU instances with pre-loaded optimized 8B models + Forge — usage-based pricing

**Comparable success:** Langfuse (open-source LLM observability) raised Series A at $200M+ valuation. Braintrust (eval platform) raised at similar valuations. The open-core → cloud model is proven in this exact space.

**Why now:** AI agents are going mainstream in 2026. 52% of enterprise execs report active AI agent use. But "half of agentic AI projects are stuck at pilot" because they're unreliable. Forge solves THE bottleneck.

**Bottom line:** 5/5 stars for market timing, technical moat, monetization path, and founder credibility (TI AI Director).

### Section 4: Scaffolding Prompt (200-word PRD)

Forge needs a hosted cloud platform to monetize the open-source GitHub traction. The PRD:

> **Forge Cloud** is a managed evaluation and reliability platform for AI agent teams. It wraps the open-source Forge guardrails library with a collaborative web dashboard, CI/CD integration, team workspaces, and managed GPU inference. Developers upload their eval datasets, run Forge's guardrail harness in the cloud, and get pass/fail reports with detailed trace visualization showing exactly where and why their agents fail. Teams can set quality gates in CI/CD (e.g., "deploy fails if agentic task accuracy drops below 95%"). The platform supports any model — local 8B, frontier API, or custom fine-tune. Pricing: Free for individual OSS users (up to 100 eval runs/month), Pro at $29/seat (unlimited evals, team dashboards), Enterprise at $999+/month (SSO, on-prem, SLA). Target: capture 2% of the $1.65B AI agent security market by 2028 = $33M ARR.

### Section 5: X-Factors

1. **Founder credibility:** Antoine Zambelli is AI Director at Texas Instruments. This isn't a weekend project — it's a director-level engineer solving his own problem.
2. **Hardware tailwind:** Apple M4/M5, NVIDIA RTX 5090, AMD AI chips — local inference is getting faster and cheaper every quarter. The "run agents locally" market is growing, and Forge makes local agents reliable.
3. **Enterprise fear:** 92% of security pros are concerned about AI agents. Forge's value prop ("make agents reliable") directly addresses the fear keeping enterprises from deploying agents.
4. **YC Spring 2026 RFS alignment:** YC explicitly called for AI agent infrastructure. Forge is a perfect fit.
5. **Gap vs frontier APIs shrinking to <1%:** The tagline "local 8B + Forge = frontier API" is a marketing nuclear weapon.

### Verdict: **BUILD** 🏆

Forge is the strongest app discovery hit since the pipeline began. It has everything: massive HN validation, billion-dollar market tailwind, unique technical moat, proven founder, clear monetization path, and perfect market timing.

---

## PHASE 5 — COMPLETE SCAFFOLD

---

# SUPERHUMAN APP SCAFFOLD: FORGE

## SYSTEM PROMPT: ACT AS A SUPERHUMAN APP ARCHITECT

You are a **Superhuman App Architect** — a hybrid of Senior Platform Engineer, Developer Tools Product Manager, Open-Source Growth Strategist, and AI Infrastructure Designer. You have built 10+ successful developer-tools companies and understand exactly what separates a dusty GitHub repo from a $30M ARR platform.

**Your mandate:** Produce a complete scaffold for `Forge` — an AI agent reliability platform targeting the `AI agent guardrails and evaluation` niche. Every decision must optimize for: **developer love**, **enterprise adoption**, and **open-source → cloud conversion funnel**.

**Context from Discovery Pipeline:**
- **Scout data:** Forge hit #1 on Hacker News with 676 points and 250 comments. Built by Antoine Zambelli, AI Director at Texas Instruments. Takes an 8B local model from 53% to 99% on agentic tasks. Open source Python framework with eval harness and interactive dashboard.
- **GEO/ASO data:** Primary keyword "AI agent guardrails" — market growing 42% CAGR to $13.52B by 2032. Competitors: Galileo, NVIDIA NeMo Guardrails, Guardrails AI, Lakera, Patronus AI. Gap: No competitor combines on-device local model reliability + eval harness + open-source.
- **Scrutiny winner reasoning:** Perfect market timing (agents going mainstream in 2026, 52% enterprise adoption, 92% of security pros concerned). Unique technical moat (makes local models outperform cloud APIs). Clear monetization path (open-core → cloud). Founder is AI Director at Fortune 500 company.
- **Killer differentiator:** "A $0 local 8B model on a $600 GPU, wrapped in Forge, beats a frontier API." Competitors focus on content safety; Forge focuses on task CORRECTNESS.
- **Revenue model:** Open-core (Apache 2.0) → Forge Cloud ($29/seat/month) → Forge Enterprise ($999+/month) → Forge GPU (usage-based).

---

### SECTION 0: PRODUCT IDENTITY & POSITIONING

**0.1. Product Name & Tagline**
- **Name:** Forge
- **Tagline:** "Make your AI agents reliable. From 53% to 99% — without changing your model."
- **GitHub tagline:** "Guardrails that take an 8B model from 53% to 99% on agentic tasks."
- **Rationale:** The name "Forge" implies strength, reliability, craftsmanship. The tagline is the single most powerful sentence in the entire discovery pipeline — it is the reason Forge hit 676 HN points. Every marketing asset must lead with this statistic.

**0.2. One-Liner Value Proposition**
"Run reliable AI agents on your own hardware for $0 — with accuracy that beats frontier APIs."

**0.3. Visual Identity System**
- **Color palette:**
  - Primary: `#FF6B35` (Forged Orange) — warmth, energy, the color of hot metal. Communicates transformation (raw model → reliable agent).
  - Secondary: `#2D3436` (Anvil Dark) — stability, seriousness, enterprise trust.
  - Accent: `#00B894` (Pass Green) — success, test passing, eval scores. Used for pass/fail badges.
  - Background: `#0F1117` (Forge Black) — developer dark mode default. All dashboards and docs use dark theme.
  - Error: `#FF4757` (Failure Red) — test failures, agent errors. High contrast for accessibility.
- **Typography:** JetBrains Mono for code, Inter for UI/documentation. Heading: 24px/20px, Body: 16px, Caption: 13px.
- **Iconography:** Custom SVG icons mixing anvil/hammer motifs with modern dev tool aesthetics (gears, checkmarks, shields). Style: filled, 2px stroke, rounded corners.
- **Logo:** A stylized anvil with a checkmark embedded in its face. Orange gradient with dark background. Recognizable at 32×32px (favicon size).

**0.4. Developer Experience (Replaces Screenshot Strategy)**

Since Forge is a developer tool (not a mobile app), the equivalent of screenshots is the **README and documentation experience:**

- **README Hero:** Terminal recording (asciinema) showing: `pip install forge-guardrails` → run eval → dashboard opens → 99.3% pass rate. Duration: 15 seconds. Overlay text: "From 53% to 99%. One command."
- **Quickstart:** 3 code blocks. Copy-paste-runnable in 60 seconds.
- **Dashboard preview:** Animated GIF of the interactive eval dashboard showing pass/fail traces with visual diffs.
- **Comparison table:** "Forge vs Bare Model vs Frontier API" — side-by-side accuracy numbers.
- **GitHub social proof:** Star count badge, contributor faces, "Used by" company logos (to be added).

---

### SECTION 1: PYTHON ARCHITECTURE (Core Library)

**1.1. Technology Stack**
- **Language:** Python 3.11+ (primary)
- **Package manager:** uv (fast, modern, Rust-based)
- **Core dependencies:** pydantic v2 (validation), rich (terminal UI), fastapi (dashboard server), plotly (eval charts), httpx (async HTTP)
- **Optional deps:** torch (local model inference), transformers (HuggingFace), llama-cpp-python (GGUF models)
- **Testing:** pytest + pytest-asyncio + pytest-cov
- **CI/CD:** GitHub Actions, pre-commit hooks (ruff, mypy, black)
- **Documentation:** MkDocs Material + mkdocstrings (auto-generated API docs from docstrings)
- **License:** Apache 2.0

**1.2. Package Structure**
```
forge/
├── __init__.py
├── guardrails/
│   ├── __init__.py
│   ├── retry.py          # Retry nudges with exponential backoff
│   ├── step_enforcer.py  # Multi-step enforcement engine
│   ├── error_recovery.py # Automatic error recovery strategies
│   ├── context.py        # VRAM-aware context management
│   └── pipeline.py       # Guardrail pipeline orchestrator
├── eval/
│   ├── __init__.py
│   ├── harness.py        # Eval harness (run test suites)
│   ├── metrics.py        # Accuracy, latency, cost metrics
│   ├── dataset.py        # Eval dataset loader (JSONL, CSV, HuggingFace)
│   └── reporter.py       # Pass/fail report generation
├── dashboard/
│   ├── __init__.py
│   ├── server.py         # FastAPI dashboard server
│   ├── templates/        # Jinja2 HTML templates
│   └── static/           # CSS, JS (HTMX + Alpine.js for interactivity)
├── cli/
│   ├── __init__.py
│   └── main.py           # Typer CLI: forge init, forge eval, forge dashboard
└── types.py              # Shared Pydantic models
```

**1.3. API Design (The Developer Interface)**

```python
# The core API must be so simple it fits in a tweet:
from forge import GuardrailPipeline, EvalHarness

# 1. Wrap your agent with guardrails
pipeline = GuardrailPipeline(
    model="meta-llama/Llama-3.1-8B-Instruct",
    guardrails=["retry", "step_enforce", "error_recover", "context_manage"]
)

# 2. Run with guardrails
result = await pipeline.run(agent_function, input_data)

# 3. Evaluate accuracy
harness = EvalHarness(dataset="my_eval_dataset.jsonl")
report = await harness.evaluate(pipeline)
print(f"Accuracy: {report.accuracy:.1%}")  # → 99.3%

# 4. Open dashboard
harness.dashboard()  # → http://localhost:8555
```

**1.4. CLI Design**
```
$ forge init                    # Create forge.yaml config
$ forge eval --dataset my_evals.jsonl  # Run eval suite
$ forge dashboard               # Open interactive dashboard
$ forge serve --port 8555       # Start dashboard server
$ forge export --format html    # Export report
```

---

### SECTION 2: CLOUD PLATFORM ARCHITECTURE (Forge Cloud)

**2.1. Technology Stack**
- **Backend:** Python FastAPI + PostgreSQL + Redis
- **Frontend:** Next.js 15 + Tailwind CSS + shadcn/ui (developer tools benefit from web UI, not mobile)
- **Auth:** Clerk (social login: GitHub, Google, SSO for enterprise)
- **Payments:** Stripe (subscriptions, usage-based billing)
- **Infrastructure:** AWS (ECS Fargate for API, S3 for eval artifacts, CloudFront CDN)
- **GPU Instances:** RunPod / Modal (serverless GPU for eval runs)
- **Queue:** Redis + BullMQ for async eval jobs
- **Monitoring:** Sentry + Grafana + PostHog (product analytics)
- **Email:** Resend (transactional emails, drip sequences)

**2.2. Pricing Tiers**

| Tier | Price | What's Included | Target User |
|---|---|---|---|
| **Free** | $0/month | 100 eval runs/month, 3 datasets, public dashboard, community support | Indie devs, hobbyists |
| **Pro** | $29/seat/month | Unlimited evals, 50 datasets, team dashboards, CI/CD webhooks, priority support | Startup teams (2-20 devs) |
| **Team** | $79/seat/month | Pro + SSO, audit logs, role-based access, custom evaluators, 99.5% SLA | Mid-market (20-200 devs) |
| **Enterprise** | $999+/month | Team + on-prem deployment, dedicated support, custom integrations, volume discounts | Fortune 500 |
| **Forge GPU** | Usage-based | Managed GPU inference with pre-loaded optimized 8B/70B models + Forge | Anyone who doesn't own a GPU |

**2.3. Monetization Funnel**
1. Developer discovers Forge on GitHub → stars, clones
2. `pip install forge-guardrails` → runs first eval locally → sees 99% accuracy
3. Hits free tier limit (100 evals) → upgrade prompt: "Run unlimited evals in the cloud"
4. Invites teammates → team needs shared dashboard → Pro plan
5. Team grows → needs SSO/SLA → Enterprise plan
6. Total conversion: 2% of OSS users → 1% Pro → 0.1% Enterprise (standard OSS funnel)

**2.4. Unit Economics**
- **CAC (organic):** $0 (GitHub stars, HN, word of mouth)
- **CAC (paid):** $150 (targeted dev content + conference sponsorships)
- **ARPU (Pro):** $29 × 12 = $348/year
- **ARPU (Enterprise):** $12,000/year minimum
- **LTV at 12 months:** $348 (Pro), $12,000+ (Enterprise)
- **Payback period:** 0 months (organic), 5.1 months (paid)
- **Monthly churn target:** <5% (dev tools average 3-7%)
- **Target at Year 3:** 2,000 Pro seats + 50 Enterprise = $58K MRR + $50K = $108K MRR = $1.3M ARR

---

### SECTION 3: SEO & GEO OPTIMIZATION

**3.1. GitHub SEO (Primary Discovery Channel)**
- **Repo name:** `antoinezambelli/forge` → eventually `getforge/forge`
- **Description:** "Guardrails that take an 8B model from 53% to 99% on agentic tasks. Open-source reliability layer for self-hosted LLM tool-calling."
- **Topics:** `ai-agents`, `guardrails`, `llm-evaluation`, `agentic-ai`, `local-llm`, `reliability-engineering`, `tool-calling`, `model-evaluation`, `opensource`
- **README:** Keyword-rich first paragraph with "AI agent guardrails", "LLM reliability", "agentic task evaluation"
- **GitHub Pages:** `getforge.dev` with full documentation (MkDocs Material)

**3.2. Content SEO Strategy**

**Pillar Pages (getforge.dev/blog):**
1. "AI Agent Guardrails: The Complete 2026 Guide" (5,000 words, targets primary keyword)
2. "Local LLM vs Frontier API: The Real Numbers (2026)" (comparison post, high shareability)
3. "How We Made an 8B Model Beat GPT-4o on Agentic Tasks" (technical deep-dive, HN-bait)
4. "AI Agent Evaluation: From 53% to 99% Reliability" (tutorial, product-led)
5. "The State of AI Agent Security in 2026" (thought leadership, EEAT)

**Blog topics (12-month content calendar):**
- "Forge vs Galileo vs NeMo Guardrails: Which AI Guardrail Tool Should You Choose?"
- "5 Common AI Agent Failures and How Forge Fixes Them"
- "Running Reliable AI Agents on a Raspberry Pi (Yes, Really)"
- "CI/CD for AI Agents: Adding Guardrails to Your Deploy Pipeline"
- "Why 92% of Security Teams Are Worried About AI Agents (and What to Do)"

**3.3. GEO (Generative Engine Optimization)**
- FAQ section with 10 Q&A blocks targeting LLM-generated search queries
- H2 = "What are AI agent guardrails?" H2 = "How do I make my local LLM reliable?" etc.
- Author bylines with Antoine Zambelli's TI credentials on every post (EEAT signal)
- Schema.org: SoftwareSourceCode schema on docs site

**3.4. Platform-Specific SEO**

**PyPI:** Package description exactly matches GitHub description. Keywords: "ai", "llm", "guardrails", "agent", "reliability", "evaluation", "tool-calling", "local-model"

**Docker Hub:** `getforge/forge` — description, tags matching PyPI

**npm (if CLI ships as npm):** Not applicable — Python-only tool

---

### SECTION 4: BEHAVIORAL ARCHITECTURE (Developer Adoption Loop)

**4.1. Trigger Design**

**External Triggers:**
- **HN launch post:** The initial spike (676 points = 50,000+ impressions)
- **r/LocalLLaMA cross-posts:** Ongoing community engagement, every major release gets a post
- **GitHub star notifications:** "X starred your repo" — social proof loop
- **Weekly Release Notes email:** "Forge v0.3: VRAM-aware context now supports 70B models"
- **Conference talks:** Antoine presenting at AI Engineer Summit, PyCon, Local AI meetups

**Internal Triggers:**
- Developer is frustrated their AI agent keeps failing → remembers Forge made their last agent reliable
- Developer sees cloud API bill → remembers Forge makes local models work as well as cloud
- Developer is about to ship an agent to production → remembers Forge's CI/CD quality gates

**4.2. Action Design (Developer Onboarding)**
1. `pip install forge-guardrails` — 5 seconds
2. `forge init` — creates config, downloads sample dataset — 10 seconds
3. `forge eval` — runs first evaluation, prints 99% accuracy — 30 seconds
4. `forge dashboard` — opens interactive trace visualizer — instant dopamine
5. **Total time to "aha moment":** <60 seconds. This is the key metric.

**4.3. Variable Reward Design**

**Reward of the Tribe:** GitHub stars, Twitter mentions, conference invitations. Being the person who "made agents reliable" is social currency.

**Reward of the Hunt:** Each new model release is a hunt — "Can Forge make Llama-4-8B hit 99%?" The community races to post benchmark results.

**Reward of the Self:** Watching your eval dashboard go from red (53%) to green (99%) after adding Forge guardrails. Deeply satisfying. Screenshot-worthy.

**4.4. Investment Design (Open-Source Moat)**
- **Code investment:** Users contribute guardrail strategies, evaluators, model configs. They're invested in the ecosystem.
- **Data investment:** Eval datasets built over months of agent development. Switching means losing all that calibration.
- **Workflow investment:** Forge integrated into CI/CD pipelines. Ripping it out breaks the deploy process.
- **Reputation investment:** GitHub contributors get their face on the README. Top contributors get invited to the Forge advisor program.

---

### SECTION 5: VISUAL DESIGN SYSTEM

**5.1. Design Principles**
1. **Terminal-first, dashboard-second:** The CLI must be beautiful before the web UI. Rich formatting, progress bars, color-coded pass/fail.
2. **Data density with clarity:** Eval dashboards show a LOT of data. Every pixel must earn its place. No decorative elements.
3. **Green means go:** The entire product is built around the transition from red (failing) to green (passing). Color is the primary UX.
4. **Copy-paste is the primary interaction:** Every code block, every command, every config is one click to copy.

**5.2. Key Visual Moments**
- **First eval completion:** Animation of the accuracy counter ticking up from 53% → 99.3%. Confetti when it crosses 95%. Sound: subtle success chime.
- **Trace waterfall:** Interactive trace visualization showing each guardrail step — retry nudges, step enforcement, error recovery — as a horizontal waterfall chart. Failed steps are red, recovered steps are orange, passed steps are green.
- **CI/CD status badge:** A simple badge that says "Forge: 99.3% ✓" in the GitHub README. This badge IS the growth engine. Every repo that adds it is a free ad.

**5.3. Dashboard UI (Next.js)**

**Pages:**
1. **Projects:** Card grid of eval projects. Each card: name, model, last accuracy, pass/fail status, last run time.
2. **Eval Run Detail:** Trace waterfall, accuracy over time chart, failure breakdown by guardrail type, export button.
3. **Dataset Manager:** Upload/edit eval datasets. Preview with syntax highlighting.
4. **Team Settings:** Members, API keys, billing, webhooks.
5. **Docs:** Embedded MkDocs documentation with "Run this example" buttons that open in Forge Sandbox.

**5.4. Accessibility**
- All charts have text alternatives
- Color-blind safe palette (green is not the only indicator — icons + text always accompany)
- Keyboard-navigable dashboard
- Screen reader support for trace waterfall

---

### SECTION 6: FINANCIAL ARCHITECTURE

**6.1. Pricing Strategy**

| Tier | Monthly | Annual | Key Features |
|---|---|---|---|
| Free | $0 | $0 | 100 evals/month, 3 datasets, public dashboard |
| Pro | $29/seat | $290/seat (17% off) | Unlimited evals, 50 datasets, team dashboard, CI/CD webhooks |
| Team | $79/seat | $790/seat (17% off) | SSO, audit logs, RBAC, custom evaluators, 99.5% SLA |
| Enterprise | Custom | Custom | On-prem, dedicated support, volume, custom integrations |
| GPU | $0.50/eval-run | — | Managed GPU inference with Forge pre-loaded |

**6.2. Revenue Model Detail**
- **Primary:** SaaS subscriptions (Pro + Team + Enterprise)
- **Secondary:** GPU compute (Forge GPU)
- **Tertiary (Year 2+):** Forge Certified Evaluators Marketplace (third-party eval suites), Forge Academy (paid courses)
- **Not now, maybe never:** Ads, data selling (never, violates trust), open-core bait-and-switch (community would revolt)

**6.3. Cancellation Flow**
- In-app cancellation: "Pause subscription" option first, then downgrade to Free
- Exit survey: "What's changing?" → if cost: offer annual discount → if not using: offer email tips
- Data retention: 90 days. "Come back anytime. Your evals will be waiting."

---

### SECTION 7: GROWTH ENGINE

**7.1. Open-Source Flywheel**
```
GitHub Stars → Social Proof → More Stars
      ↓
Blog/Conference Talks → Website Traffic → PyPI Downloads
      ↓
Free Users → 2% Convert to Pro → Revenue
      ↓
Revenue → Hire DevRel → More Content → More Stars
```

**7.2. Viral Mechanics**
- **CI/CD Badge:** Every repo that adds the "Forge Verified" badge is a distribution channel. Target: 10,000 repos in Year 1.
- **Shareable Reports:** "My agent just hit 99.3% with Forge 🔥" — one-click share to Twitter/LinkedIn with a chart image.
- **Model Leaderboard:** Public leaderboard showing which models score highest with Forge guardrails. HuggingFace SEO gold.
- **Guest Evaluators:** Let the community build and share evaluator plugins. Marketplace in Year 2.

**7.3. Community Building**
- **Discord server:** Real-time support, showcase channel, contributor discussions
- **GitHub Discussions:** Feature requests, troubleshooting, model config sharing
- **Weekly Office Hours:** Antoine + team on Discord/YouTube live, answering questions
- **Contributor Program:** Top contributors get swag, conference tickets, advisory board invites

---

### SECTION 8: TECHNICAL SPECIFICATION

**8.1. Core Architecture Diagram**

```
┌──────────────────────────────────────────────────────┐
│                    User's AI Agent                     │
│  (LangChain, LlamaIndex, custom Python, etc.)         │
└────────────────────┬─────────────────────────────────┘
                     │ agent_function(input) → output
                     ▼
┌──────────────────────────────────────────────────────┐
│              Forge Guardrail Pipeline                  │
│                                                       │
│  ┌──────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  Retry   │→│ Step Enforcer │→│ Error Recovery │  │
│  │  Nudges  │  │              │  │               │  │
│  └──────────┘  └──────────────┘  └───────────────┘  │
│                         │                             │
│              ┌──────────▼──────────┐                  │
│              │  VRAM-Aware Context │                  │
│              │     Manager         │                  │
│              └─────────────────────┘                  │
└────────────────────┬─────────────────────────────────┘
                     │ guarded_output
                     ▼
┌──────────────────────────────────────────────────────┐
│                Eval Harness                            │
│  ┌──────────┐  ┌──────────┐  ┌───────────────────┐  │
│  │ Dataset  │→│  Scoring │→│  Report Generation │  │
│  │  Loader  │  │  Engine  │  │  (Pass/Fail/Stats) │  │
│  └──────────┘  └──────────┘  └───────────────────┘  │
└────────────────────┬─────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────┐
│           Interactive Dashboard (localhost:8555)       │
│  Trace Waterfall │ Accuracy Charts │ Export │ Config  │
└──────────────────────────────────────────────────────┘
```

**8.2. Database Schema (Forge Cloud)**

```
-- PostgreSQL
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    clerk_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    github_username VARCHAR(255),
    plan VARCHAR(50) DEFAULT 'free',  -- free, pro, team, enterprise
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    team_id UUID REFERENCES teams(id),
    name VARCHAR(255) NOT NULL,
    model_name VARCHAR(255),
    guardrail_config JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE eval_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id),
    status VARCHAR(50) DEFAULT 'pending',  -- pending, running, completed, failed
    accuracy DECIMAL(5,2),
    total_tests INT,
    passed_tests INT,
    failed_tests INT,
    duration_ms INT,
    trace_data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE datasets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id),
    name VARCHAR(255),
    format VARCHAR(50),  -- jsonl, csv
    size_bytes BIGINT,
    s3_key VARCHAR(1024),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE teams (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE team_members (
    team_id UUID REFERENCES teams(id),
    user_id UUID REFERENCES users(id),
    role VARCHAR(50) DEFAULT 'member',  -- admin, member
    PRIMARY KEY (team_id, user_id)
);

CREATE INDEX idx_eval_runs_project ON eval_runs(project_id, created_at DESC);
CREATE INDEX idx_users_plan ON users(plan);
```

**8.3. API Endpoints (Forge Cloud)**

```
POST   /api/v1/auth/login          — GitHub OAuth / Clerk
GET    /api/v1/projects            — List user/team projects
POST   /api/v1/projects            — Create project
GET    /api/v1/projects/{id}       — Project detail
DELETE /api/v1/projects/{id}       — Delete project

POST   /api/v1/projects/{id}/runs  — Trigger eval run (async)
GET    /api/v1/runs/{id}           — Eval run status + results
GET    /api/v1/runs/{id}/trace     — Trace waterfall data

POST   /api/v1/datasets/upload     — Upload eval dataset
GET    /api/v1/datasets/{id}       — Download dataset

GET    /api/v1/teams/{id}          — Team detail
POST   /api/v1/teams/{id}/members  — Invite member

POST   /api/v1/webhooks/github     — GitHub CI/CD integration
GET    /api/v1/billing/usage       — Current billing usage
POST   /api/v1/billing/checkout    — Stripe checkout session
```

**8.4. CI/CD Integration Spec**

```yaml
# .github/workflows/forge-eval.yml
name: Forge Agent Eval
on: [push, pull_request]
jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: getforge/forge-action@v1
        with:
          dataset: ./evals/agent_tasks.jsonl
          min-accuracy: 95
          api-key: ${{ secrets.FORGE_API_KEY }}
```

**8.5. Third-Party Dependencies**
- **Core:** pydantic, rich, fastapi, plotly, httpx, typer
- **Optional:** torch, transformers, llama-cpp-python
- **Cloud:** FastAPI, PostgreSQL, Redis, Clerk, Stripe, AWS SDK, Resend
- **Frontend:** Next.js 15, Tailwind CSS, shadcn/ui, Recharts, Monaco Editor
- **Monitoring:** Sentry, PostHog, Grafana

---

### SECTION 9: 30-DAY MVP SPRINT PLAN

**Week 1 — Foundation**
| Day | Core Library | Cloud Platform | Docs/Marketing |
|---|---|---|---|
| Mon | Package structure, pydantic models | FastAPI skeleton, DB schema | README refresh |
| Tue | Retry nudge implementation | User auth (Clerk) | Quickstart guide |
| Wed | Step enforcer implementation | Project CRUD API | API reference docs |
| Thu | Error recovery implementation | Eval run queue (Redis) | Landing page v1 |
| Fri | VRAM context manager | Dataset upload API | Blog: "Introducing Forge" |

**Week 2 — Core Experience**
| Day | Core Library | Cloud Platform | Docs/Marketing |
|---|---|---|---|
| Mon | Eval harness v1 | Eval run execution | Eval dataset format spec |
| Tue | Metrics engine | Trace waterfall endpoint | Tutorial video script |
| Wed | Report generator | Dashboard — project list | Blog: "53% to 99%" deep-dive |
| Thu | CLI (typer) | Dashboard — run detail | HN launch prep |
| Fri | Integration tests | CI/CD webhook receiver | Social media assets |

**Week 3 — Polish & Community**
| Day | Core Library | Cloud Platform | Docs/Marketing |
|---|---|---|---|
| Mon | Model config presets | Stripe integration | Discord server setup |
| Tue | Dashboard v1 (local) | Team management | Contributor guide |
| Wed | Dashboard polish | Usage billing | GitHub Discussions setup |
| Thu | Bug fixes | Error handling + monitoring | Conference talk proposal |
| Fri | Performance optimization | Load testing | Community launch plan |

**Week 4 — Launch**
| Day | Core Library | Cloud Platform | Docs/Marketing |
|---|---|---|---|
| Mon | PyPI release prep | Production deploy | Launch blog post final |
| Tue | **PUBLISH to PyPI** | Production monitoring | HN post draft |
| Wed | Bug fixes from initial users | Scale testing | r/LocalLLaMA post |
| Thu | v0.1.1 patch | Analytics dashboard | Twitter thread |
| Fri | Community issue triage | On-call rotation setup | Weekly roundup |

**MVP Feature Cut List (Do NOT Build in Sprint 1):**
- Model leaderboard (Week 6)
- Evaluator marketplace (Month 4)
- On-prem Enterprise deploy (Month 6, wait for first enterprise customer)
- Forge GPU managed instances (Month 3)
- Mobile dashboard (probably never — dev tools on mobile is a solved problem via responsive web)

---

### SECTION 10: LAUNCH CHECKLIST

**Pre-Launch (T-14 days)**
- [x] GitHub repo: Clean, documented, CI passing, 676 stars
- [ ] PyPI: Package registered, description polished, classifiers set
- [ ] getforge.dev: Landing page live, docs live, blog with 3 posts
- [ ] Discord: Server set up with welcome, showcase, help, contrib channels
- [ ] Twitter/X: @getforge account with 5 warmup posts
- [ ] r/LocalLLaMA: "Forge is launching next week" teaser post
- [ ] HN: "Launch HN" draft written, reviewed by 3 people
- [ ] Press kit: Logo, screenshots, founder bio, key stats

**Launch Day (Monday, 12:01 AM PT)**
- [ ] PyPI: `pip install forge-guardrails` live
- [ ] HN: "Launch HN: Forge — open-source guardrails for reliable AI agents" → post at 12:01 AM PT
- [ ] r/LocalLLaMA: Cross-post HN discussion
- [ ] r/MachineLearning: "Forge: 8B model hits 99% on agentic tasks [open source]"
- [ ] Twitter/X: Launch thread with GIF demo
- [ ] Discord: Welcome message, founder AMA scheduled
- [ ] Monitor: GitHub stars, PyPI downloads, website traffic

**Post-Launch (T+7 days)**
- [ ] Ship v0.1.1 with top 3 community bug reports
- [ ] Write "Forge Launch: The Numbers" blog post (transparency builds trust)
- [ ] Respond to ALL GitHub issues within 24 hours
- [ ] Begin weekly office hours on Discord

---

### SECTION 11: POST-LAUNCH ITERATION PLAN

**Week 1-2: Observe**
- Metrics: PyPI downloads, GitHub stars, Discord members, website traffic
- Top user request categories: track in GitHub issues with labels
- Do NOT ship features. Only critical bug fixes.

**Week 3-6: Quick Wins**
- Ship top 3 most-requested model configs
- Add support for Llama-4, Mistral-3, Phi-4
- Publish 2 comparison blog posts ("Forge vs Galileo", "Forge vs NeMo")
- Launch Forge Cloud free beta

**Month 2-4: Growth**
- Model leaderboard launch (SEO play)
- CI/CD GitHub Action marketplace listing
- First conference talk (AI Engineer Summit)
- Forge Cloud paid tiers go live

**Month 5-8: Enterprise**
- First enterprise customer (use existing network: TI, AI Director connections)
- SSO, audit logs, on-prem option
- Case study: "How [Company] saved $200K/year by running reliable local agents with Forge"

---

### SECTION 12: ANTI-PATTERNS

1. **Do not close-source the core.** Apache 2.0 forever. The open-source community IS the moat. HashiCorp's BSL switch is a cautionary tale, not a playbook.
2. **Do not position as "AI safety."** Forge is about reliability and correctness, not censorship. "Guardrails" in Forge means "making your agent work," not "blocking your agent from saying bad things." Conflating these destroys developer trust.
3. **Do not charge for local usage.** The local CLI and dashboard are free forever. Only the cloud platform (team dashboards, managed evals, GPU instances) is paid.
4. **Do not compete on model quality.** Forge doesn't fine-tune models. It wraps them. Don't get dragged into benchmark wars. Compete on reliability infrastructure, not model performance.
5. **Do not ignore the r/LocalLLaMA community.** They are the early adopters, the evangelists, and the most demanding users. Treat them like royalty. Their word-of-mouth built Forge's initial 676 HN points.
6. **Do not ship without an eval harness.** The eval harness and dashboard are what differentiate Forge from every other guardrails library. Ship them together or don't ship.
7. **Do not accept VC money too early.** Forge can reach $1M ARR on organic growth alone. Take funding only when the use of capital is obvious (hire DevRel team, build enterprise features, sponsor conferences).
8. **Do not let the dashboard get slow.** Trace waterfalls with 10,000+ steps must render in <500ms. Performance is a feature. A slow dashboard is a 1-star GitHub issue.

---

## BUILD VERDICT: ✅ PROCEED

Forge is the strongest app discovery hit in pipeline history. The combination of massive community validation (676 HN points), billion-dollar market tailwind ($13.52B by 2032), unique technical moat (local 8B beats frontier API), founder credibility (AI Director at TI), and clear monetization path (open-core → cloud) makes this a rare "full marks" opportunity.

**Top Action Item:** Publish Forge Cloud free beta within 30 days. The window of "Forge is the hot new thing on HN" lasts ~4-6 weeks. Convert that attention into signups before it fades.

---

_Generated by App Discovery Pipeline Phase 5. Scaffolding prompt template v2026-05-24._
_Next: Phase 6 — Report generation._