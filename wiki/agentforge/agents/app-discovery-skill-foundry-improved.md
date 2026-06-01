# AGENTS.md — App Discovery Department

_OpenClaw native. Built 2026-05-23. Refactored 2026-05-27 (5-stage pain-first pipeline). Skill-Foundry improved 2026-05-27._

## Core Principle: Discover Pain, Not Apps

**This department finds MARKET GAPS — underserved problems people are actively complaining about.** The goal is to identify niches where AgentForge can build a better mobile product. Existing apps are competitors, not build targets.

This pipeline is a **funnel, not a daily quota.** "No winner today" is a perfectly valid result — and better than a forced bad pick.

---

## Run Startup (MANDATORY — First 2 Minutes)

Before entering any stage, execute these startup tasks:

```
1. Read the playbook: web_fetch or read ~/workspace/MeMex-Zero-RAG/wiki/agentforge/agents/app-discovery-playbook.md
2. Check watchlist for stale signals: read ~/workspace/MeMex-Zero-RAG/wiki/agentforge/artifacts/app-discovery/watchlist.md
3. Verify today's date: extract YYYY-MM-DD and YYYY/MM for artifact paths
4. Check artifact directory exists: if ~/workspace/MeMex-Zero-RAG/wiki/agentforge/artifacts/app-discovery/YYYY/MM/ doesn't exist, create it
5. Check obsidian path exists: if ~/obsidian-vault/AgentForge/app-discovery/YYYY/MM/ doesn't exist, create it
```

**Rationale:** The May 27 failure happened because the agent didn't consult the playbook before scoring. Startup is non-negotiable.

---

## Daily Pipeline (06:00-08:00 Dublin)

```
06:00  STARTUP: Read playbook + watchlist. Verify paths.            2 min
06:02  STAGE 1 — PAIN HARVEST: Scan for complaints. 10-15 pain points.  18 min
06:20  STAGE 2 — SIGNAL CHECK: Validate with 3-signal test. 5-8 survivors. 15 min
06:35  STAGE 3 — COMPETITIVE GAP MAP: Who's solving this? 3-5 viable niches. 15 min
06:50  STAGE 4 — NICHE SCORING: Score niche. 1 winner or "no winner."     16 min
07:06  STAGE 5 — SCAFFOLD + SCRUTINIZE: Build blueprint + competitor reports. 48 min
07:54  STAGE 6 — REPORT: Deliver to Board via Telegram.              6 min
08:00  Pipeline complete.
```

**Timing note:** Stage times include 1-2 min buffer for transitions. If a stage runs long, trim Stage 5 scrutiny depth — never skip it.

---

## HARD GATE: Niche vs Competitor

**This gate is checked at THREE points in the pipeline:**
- **Entry to Stage 3:** When listing who's solving a pain point, classify each result immediately.
- **Entry to Stage 4:** Before any niche scoring, the scoring candidate itself must pass this check.
- **Entry to Stage 5:** Before scaffolding, confirm the winner is not a live app.

**Check procedure (non-bypassable):**
1. Is this an app downloadable from the App Store or Google Play Store **RIGHT NOW**?
2. Search: `web_search: "[name] app store iOS"` and `web_search: "[name] google play Android"`
3. If either returns a live store listing → **COMPETITOR.** Do not score. Do not declare BUILD.
4. If no store listing found → **NICHE.** Proceed to scoring.

**Definitions:**
- **Niche** = a market gap / underserved problem. Score it. Build for it.
- **Competitor** = an existing live app in that niche. Scrutinize it against our scaffold. Never declare BUILD for it.

**May 27 failure reference:** Preplo was on WhistleOut as a live iOS app. The agent did not run the App Store check. Result: live app scored 7.7/10 and declared BUILD. This gate prevents that recurrence.

---

## STAGE 1: PAIN HARVEST (18 min)

**Goal:** Collect 10-15 raw pain points from people complaining about real problems.

**Do NOT look for apps.** Look for COMPLAINTS. The signal is in the frustration, not in the product.

### Source Scanning Matrix

| Source | Method | Fallback if blocked | What to Extract |
|--------|--------|---------------------|-----------------|
| **Reddit** | `web_fetch` r/AppIdeas, r/SideProject, r/Entrepreneur, r/SaaS, r/microsaas, r/indiehackers sorted by hot | `web_search: "app idea site:reddit.com/r/AppIdeas 2026"` | Posts asking "is there an app that…" or "I wish there was…" |
| **Reddit pain search** | `web_search: "I wish there was an app" OR "frustrated with" OR "why doesn't" site:reddit.com` | Try without site: filter, filter manually | Direct quotes of frustration with current solutions |
| **App Store reviews** | `web_search: "[category] app review terrible worst complaints 2026"` | `web_fetch` specific app review pages from App Store | 1-2 star reviews on competitor apps — these ARE pain points |
| **Product Hunt** | `web_fetch: producthunt.com/topics/mobile-app` | `web_search: "Product Hunt top mobile app launches may 2026"` | What categories are getting built? What gaps remain? |
| **Hacker News** | `web_fetch: news.ycombinator.com/show` | `web_search: "Show HN mobile app 2026"` | Posts where people describe problems (filter: mobile-relevant only) |
| **Google Trends** | `web_search: "trending app category growing 2026"` | `web_search: "app category growth 2026 market research"` | Rising categories = growing demand, check if supply is lagging |
| **Niche app repos** | Reference `github.com/zeck00/niche-app-ideas` INDEX.md for pattern-matching | N/A (reference only) | Learning validated gap structure — not copying, pattern-matching |

**Source diversity requirement:** Must use at least 3 different source types. No more than 60% of pain points from a single source.

### Pain Harvest Search Terms

Run ALL of these searches (minimum 5, maximum 8):
- `"I wish there was an app" site:reddit.com`
- `"frustrated with" app OR tool site:reddit.com`
- `"why doesn't anyone build" site:reddit.com`
- `"I'd pay for" app OR tool site:reddit.com`
- `"[category] alternative" OR "[category] too expensive" site:reddit.com`
- `"is there an app that" site:reddit.com`
- `"I hate [app_name]" OR "[app_name] is terrible" site:reddit.com`
- `"I need an app for" OR "looking for an app" site:reddit.com`

**For categories, rotate through:** productivity, health, finance, social, education, travel, food, creative tools, dating, mental health, parenting, home automation.

### Deduplication Rule

Before concluding Stage 1, scan your entire output for duplicates:
- If two pain points describe the same problem in different words → **merge** them. Keep the strongest quote, reference both sources.
- If a pain point is a sub-problem of another → **merge** into the broader pain point as an evidence bullet.

### Output Format (per pain point)

```
Pain Point #N:
- Quote: "[exact quote from source]"
- Source: [URL]
- Category: [e.g., Productivity, Health, Finance]
- What they want: [one sentence]
- Current workaround: [what they're doing now instead]
- Estimated audience: [small <10K / medium 10K-100K / large >100K based on thread engagement]
```

### Auto-Reject Filters

Reject immediately (no exception):
- CLI tools, libraries, SDKs, developer tools with no end-user mobile angle
- Desktop-only software
- Enterprise SaaS with no consumer mobile angle
- Infrastructure/hosting/DevOps tools
- Blockchain/crypto projects (unless consumer-facing utility with clear non-speculative use case)
- Hardware-dependent ideas (if hardware isn't widely available)
- Ideas requiring regulatory approval as a gating factor (FDA, FCC, etc.)

Mark for "low priority" (collect but don't prioritize):
- Single-use utility apps (e.g., "one-button flashlight")
- Ideas where the primary user benefit is "it's free"
- Ideas dependent on a platform API that could be deprecated

---

## STAGE 2: SIGNAL CHECK (15 min)

**Goal:** Validate pain points. Kill anything that's just noise. Keep only validated problems.

### 3-Signal Validation Test

| Signal | What to Check | Method | Pass Condition |
|--------|-------------|--------|----------------|
| **Persistence** | Multiple threads across time | Search: `"[pain point] site:reddit.com"` — count distinct threads + date range | ≥3 distinct threads, earliest ≥1 month apart from latest |
| **Payment intent** | Explicit or implicit willingness to pay | Scan for: "I'd pay", "worth $X/mo", "if it was cheaper than", "I pay [competitor] $X but..." | At least 1 explicit or 2 implicit payment signals across threads |
| **Workaround pain** | Complex current solution | Identify the current process: manual? 3+ tools? spreadsheets? WhatsApp? | Multi-step workaround described (≥2 tools/steps) OR "there's literally no way to do this" |

**Kill floor:** Must pass ≥2 of 3 signals to advance to Stage 3.

### Composite Signal Strength

For ranking survivors (needed when you have more than 8 and need to cut):

| Passed Signals | Signal Strength | Action |
|---------------|----------------|--------|
| 3/3 + strong payment ($10+/mo) | **STRONG** | Priority advance |
| 3/3 + weak payment | **GOOD** | Advance |
| 2/3 passing, payment is one of them | **ADECUATE** | Advance |
| 2/3 passing, payment is NOT one of them | **WEAK** | Advance only if gap is WIDE in Stage 3 |
| 1/3 or 0/3 | **DEAD** | ❌ Kill |

### Trend Direction Check

For each surviving pain point:
```bash
web_search: "[pain topic] trending 2025 2026 growth interest"
web_search: "[pain topic] market size 2026"
```

Classification:
- **Growing** → multiple sources cite rising interest, Google Trends shows upward slope → ✅ advance
- **Flat** → no growth signals, stable mentions → ⚠️ advance only with STRONG signal strength (3/3 signals + strong payment)
- **Declining** → mentions decreasing, platform shifts reducing relevance → ❌ kill

**No Google Trends API?** Use `web_search: "Google Trends [topic] 2026"` and scrape the result snippets. Acceptable proxy.

### Output: 5-8 validated pain points

```
VALIDATED PAIN POINT #N:
- Original pain: "[quote from Stage 1]"
- Signals passed: Persistence [✓/✗], Payment [✓/✗], Workaround [✓/✗] = N/3
- Signal strength: [STRONG/GOOD/ADECUATE/WEAK]
- Trend direction: [Growing/Flat/Declining]
- Evidence: [3 URLs/quotes from signal validation]
- Category: [same as Stage 1]
```

---

## STAGE 3: COMPETITIVE GAP MAP (15 min)

**Goal:** For each surviving pain point, map who's already solving it and how well.

### HARD GATE CHECK (Execute BEFORE gap mapping)

For EVERY name/term you encounter that sounds like a product:
```
web_search: "[name] app store iOS"
web_search: "[name] google play Android"
```
If live store listing exists → **COMPETITOR.** Map it, scrutinize it later — do NOT score it.

### For each surviving pain point, answer four questions:

**Q1: Who's solving this?**
List ALL live competitors found via:
```bash
web_search: "[niche keyword] app iOS Android 2026"
web_search: "best [niche keyword] apps 2026"
web_fetch: App Store search results for "[niche keyword]"
```
For each competitor: Name, Platforms (iOS/Android/Both), Price, App Store rating, Estimated downloads.

**Q2: How well are they solving it?**
```bash
web_search: "[competitor name] review complaints problems"
web_search: "[competitor name] alternative reddit"
web_fetch: App Store page for top competitor (check 1-2 star reviews)
```
For each competitor: Top 3 user complaints, missing features, pricing complaints.

**Q3: Gap Width Classification**

| Gap Width | Definition | What it Means |
|-----------|-----------|---------------|
| **WIDE** | No solution exists. People use manual workarounds (spreadsheets, WhatsApp, memory). OR all existing solutions have <3.0 stars. | Green field. Build. |
| **NARROW** | A solution exists but it's too expensive (>$10/mo without justification), missing key features (>2 major gaps), >30% of reviews are 1-2 star, or it's iOS/Android-only with clear demand on the missing platform. | Attack the weakness. Build with differentiation. |
| **CLOSED** | A free/cheap/great solution already dominates (4.5+ stars, >50K reviews). Switching cost is high. Competitor iterating fast. | ❌ Kill immediately. Do NOT score in Stage 4. |

### Gap Classification Rules (no judgment, these are formulaic)

```
CLOSED if ALL of:
  - At least 1 competitor with ≥4.5 stars AND ≥1K reviews
  - That competitor is priced ≤$5/mo OR has a generous free tier
  - No major feature gap (≥2 missing features users are begging for)
  - Updated within last 6 months

WIDE if ANY of:
  - Zero competitors found with >100 reviews
  - All competitors have <3.0 stars
  - No dedicated app exists (people using general-purpose tools)

NARROW if:
  - Neither CLOSED nor WIDE (default)
```

**Q4: Competitor Freshness**
For the top 3 competitors: when was their last update? First launched?
```bash
web_search: "[competitor name] launched date annoucement"
web_search: "[competitor name] update 2026"
```
Tag each: VETERAN (>3 years), ESTABLISHED (1-3 years), NEWCOMER (<1 year), UNKNOWN.

### Output: 3-5 viable niches

```
NICHE #N: [niche name]
- Pain point: [validated pain from Stage 2]
- Gap width: [WIDE / NARROW] (CLOSED killed)
- Competitors mapped: N
  - [Competitor 1] — [platforms], [price], [rating ★], [reviews count], [freshness]
  - [Competitor 2] — ...
  - [Competitor 3] — ...
- Top user complaints across competitors: [3 bullet points with quotes]
- Our attack surface: [what competitors are NOT doing that we can]
```

---

## STAGE 4: NICHE SCORING (16 min)

**Goal:** Score the NICHE itself (not any app). Pick 1 winner or declare "no winner today."

### HARD GATE CHECK (Execute BEFORE scoring each niche)

For each niche candidate:
1. Confirm it is NOT a live App Store / Play Store app
2. Confirm it was NOT previously scaffolded (check watchlist + artifact directory)
3. If previously scaffolded → skip, note "already covered" in report

**Niche freshness check:**
```bash
rg -l "[niche name]" ~/workspace/MeMex-Zero-RAG/wiki/agentforge/artifacts/app-discovery/
```
If found in any scaffold file → already explored. Skip unless significant market change detected.

### Scoring Framework

| Dimension | Weight | Kill Floor | Scoring Guide |
|-----------|--------|------------|---------------|
| **Demand Strength** | 25% | 4/10 | See conversion table below |
| **Gap Width** | 25% | 4/10 | WIDE=9-10, NARROW=5-8, no CLOSED passes kill floor |
| **ASO/SEO Opportunity** | 20% | 4/10 | See conversion table below |
| **Monetization Potential** | 20% | 4/10 | See conversion table below |
| **Urgency/Timing** | 10% | 4/10 | See conversion table below |

### Scoring Conversion Tables (Exact — No Subjective Judgment)

#### Demand Strength (0-10)
| Evidence | Score |
|---------|-------|
| ≥3 threads with "I'd pay $10+/mo" across ≥2 months + ≥5 threads total | **10** |
| ≥3 threads with payment intent ($5-$10/mo) + ≥5 threads total, ≥2 months span | **8-9** |
| ≥3 threads with payment intent + ≥5 threads total | **6-7** |
| ≥3 threads total, ≥1 month span, payment intent present | **4-5** |
| ≥3 threads total, ≥1 month span, NO payment intent | **2-3** |
| <3 threads OR all in same week | **0-1** |

#### ASO/SEO Opportunity (0-10)
Search: `web_search: "[niche keyword] app store keyword search volume"`
| Evidence | Score |
|---------|-------|
| Primary keyword >10K searches/month, <5 competing apps ranking for it | **9-10** |
| Primary keyword >5K searches/month, <10 competing apps, long-tail variants available | **7-8** |
| Primary keyword 1K-5K searches/month, some competition but gaps in long-tail | **5-6** |
| Primary keyword <1K searches/month OR >20 competing apps dominating | **3-4** |
| No identifiable keyword with search volume | **0-2** |

#### Monetization Potential (0-10)
| Evidence | Score |
|---------|-------|
| Category benchmarks at $15+/mo, competitors pricing $9.99+, "I'd pay $20" quotes found | **9-10** |
| Category benchmarks at $5-15/mo, competitors pricing $4.99+, payment intent confirmed | **7-8** |
| Subscription model viable but price-sensitive market, $2.99-4.99/mo ceiling | **5-6** |
| Unclear monetization path, freemium-only space, ads-dependent | **3-4** |
| No viable monetization model (pure utility, everyone expects free) | **0-2** |

**Category price benchmarks (2026):**
| Category | Typical Monthly Price Range |
|---------|---------------------------|
| Finance/Investing | $10-30/mo |
| Health & Fitness | $5-20/mo |
| Productivity | $3-15/mo |
| Education/Learning | $5-25/mo |
| Creative Tools | $3-20/mo |
| Dating/Social | $5-30/mo |
| Food/Recipes | $3-10/mo |
| Mental Wellness | $5-15/mo |
| Parenting | $3-10/mo |
| Travel | $3-10/mo |

#### Urgency/Timing (0-10)
| Evidence | Score |
|---------|-------|
| Competitor launched recently, growing fast, platform gap they'll fill in <3 months | **9-10** |
| Growing trend, multiple new entrants in last 6 months, first-mover advantage closing | **7-8** |
| Steady demand, niche growing, some new competitors but no dominant player | **5-6** |
| Stable demand, established players but gap still exists, window open but not urgent | **3-4** |
| Declining interest, no new competitors, market shrinking | **0-2** |

### Winner Selection

**Winner:** Highest weighted total score. Only 1 winner.

**Tiebreaker (if scores within 0.5 points):**
1. Prefer WIDE gap over NARROW gap
2. Prefer higher Demand Strength score
3. Prefer higher Monetization Potential score
4. If still tied, pick the one with fewer existing competitors

**"No winner today" threshold:** No niche passes ALL kill floors (score ≥4 on every dimension). In this case:
- Report "no winner today" honestly
- List the best runner-up (highest total score, even if below floor)
- Add to watchlist if any dimensions hit 6+ despite failing a kill floor
- Never force a pick. A blank day is better than a bad pick.

### Output: 1 winning niche (or zero)

```
WINNER: [Niche Name]
- Score: X.X/10
- Demand Strength: X/10 — [justify with evidence from conversion table]
- Gap Width: X/10 — [WIDE/NARROW with evidence]
- ASO/SEO: X/10 — [primary keyword + estimated volume]
- Monetization: X/10 — [price point + category benchmark]
- Urgency/Timing: X/10 — [window status + evidence]
- Key differentiator: [one sentence — what our app will do that no competitor does]
- Kill floor check: [ALL PASSED / FAILED: dimension names]

[OR]

NO WINNER TODAY: [Best runner-up niche name] scored X.X/10 but failed [dimension(s)] kill floor.
Watchlist addition: [Niche name] — revisit if [condition changes].
```

---

## STAGE 5: SCAFFOLD + SCRUTINIZE (48 min)

**Goal:** Build AgentForge's app blueprint, then scrutinize top 3 competitors against it.

### Pre-Stage 5 Checklist (MANDATORY)

Before scaffolding, verify:
- [ ] Winner is a NICHE (not a live app) — re-run HARD GATE check
- [ ] Winner was not previously scaffolded — check artifacts and watchlist
- [ ] Winner's niche name is not identical to any existing app name
- [ ] At least 1 WIDE or NARROW gap identified that we can fill

### 5A — Scaffold OUR App (25 min)

The scaffolding prompt template is at `~/.openclaw/agents/app-discovery/scaffolding-prompt.md`.

**Key rules:**
- **Original name** — never copy a competitor's name. Check before choosing: `web_search: "[proposed name] app store"` — if any result, pick a different name
- **Features fill gaps** — our app does what competitors don't (from Stage 3 gap map)
- **Price undercuts** — always below the most expensive competitor, preferably 30-50% below the median
- **Differentiation is real** — at least one feature no competitor has, confirmed by competitor map
- **Platform strategy:** Unless the data shows single-platform demand only, scaffold both iOS and Android. Our competitive advantage over iOS-only competitors is cross-platform launch.

**Scaffold sections (all 12 required, no abbreviation):**
0. App Identity & Positioning
1. iOS Architecture
2. Android Architecture
3. SEO & GEO Optimization
4. Behavioral Architecture
5. Visual Design System
6. Financial Architecture
7. Virality Engine
8. Technical Specification
9. 30-Day MVP Sprint Plan
10. Launch Checklist
11. Post-Launch Iteration Plan
12. Anti-Patterns

**Write scaffold to BOTH paths:**
```
~/workspace/MeMex-Zero-RAG/wiki/agentforge/artifacts/app-discovery/YYYY/MM/AppName-scaffold-YYYY-MM-DD.md
~/obsidian-vault/AgentForge/app-discovery/YYYY/MM/AppName-scaffold-YYYY-MM-DD.md
```

Where `YYYY/MM` is the current year/month (e.g., `2026/05`). Create directories if they don't exist.

### 5B — Scrutinize Top 3 Competitors (23 min)

**Every scaffold winner's top 3 competitors get a scrutiny report.** No exceptions.

**Before writing, check for existing reports:**
```bash
ls ~/workspace/MeMex-Zero-RAG/wiki/agentforge/artifacts/app-discovery/YYYY/MM/ | grep -i "[competitorname]"
ls ~/obsidian-vault/AgentForge/app-discovery/YYYY/MM/ | grep -i "[competitorname]"
```
If a report exists from a previous date: **reference it, do not rewrite.** Add a "Re-evaluation as of [date]" section with any new findings.

**Scrutiny report structure (6 sections):**

| Section | Content | Key Questions |
|---------|---------|---------------|
| **1. Demand & Saturation** | Latent demand score + market saturation index | Is this a Blue/Growing/Crowded/Bloodbath market? Aspirin or Vitamin? |
| **2. Overtake Strategy** | Feature matrix (them vs top 2 others vs us) + their weaknesses + their strengths | What can't they do that we can? What must we match? |
| **3. Revenue & Success** | Estimated MRR, user base, unit economics, monetization weaknesses | Can we undercut them? Is their pricing vulnerable? |
| **4. X-Factors** | Churn risk, regulatory/legal risks, growth channels | What could kill them without us doing anything? |
| **5. Head-to-Head** | Side-by-side vs our scaffold: features, price, platforms, AI, community, freemium | Where we win. Where they win. Acquisition potential. |
| **6. Verdict** | Threat level, timeline urgency, acquisition viability | LOW/MEDIUM/HIGH. What must we do? How many months until feature parity? |

**Scrutiny prompt template** (use the full template from `~/.openclaw/agents/app-discovery/scaffolding-prompt.md`, adapting it):

```
ACT AS A HYBRID: 40% Venture Capital Market Analyst, 40% Growth Product Manager, 20% Behavioral Architect.
...
```
Full template is embedded in this document's Appendix — copy and fill placeholders.

**Write scrutiny to BOTH paths:**
```
~/workspace/MeMex-Zero-RAG/wiki/agentforge/artifacts/app-discovery/YYYY/MM/CompetitorName-scrutiny-YYYY-MM-DD.md
~/obsidian-vault/AgentForge/app-discovery/YYYY/MM/CompetitorName-scrutiny-YYYY-MM-DD.md
```

### Error Handling During Stage 5

If web_fetch fails on a competitor's page:
1. Retry once with a different URL (their Twitter, LinkedIn, Product Hunt page)
2. If still failing: use web_search results instead, flag in report as "limited data"
3. Never fabricate data. Mark missing fields as "UNAVAILABLE."

If scaffold file write fails:
1. Verify directory exists, create if not
2. Retry write once
3. If still failing: write to workspace as fallback, flag in report

---

## STAGE 6: Daily Report (6 min)

### Report Delivery

Deliver to Board via Telegram. Use the exact format below.

### If Winner Found:

```markdown
📱 App Discovery Daily — [YYYY-MM-DD]

🔍 Pain Points Harvested: N
✅ Validated (passed signals): N
💀 Killed (failed signals): N
🗺️ Viable Niches (after gap map): N
❌ Killed (CLOSED gaps): N

🏆 Niche winner: [NICHE NAME] (X.X/10)
- Demand: X/10 — [key signal + conversion table justification]
- Gap width: X/10 — [WIDE/NARROW] — [why, with competitor evidence]
- ASO: X/10 — [keyword: "[primary keyword]" — est. XK/mo]
- Monetization: X/10 — [$X.XX/mo target — category benchmark $X-$X/mo]
- Urgency: X/10 — [window status]

🛠️ Scaffolded: [OUR APP NAME]
- Price: $X.XX/mo (annual: $XX.XX/yr)
- Key differentiator: [one sentence — feature no competitor has]
- Target platforms: [iOS / Android / Both]

🔬 Competitors scrutinized against our scaffold:
- [Competitor 1] — [freshness] — threat level [LOW/MED/HIGH] — [one line why]
- [Competitor 2] — [freshness] — threat level [LOW/MED/HIGH] — [one line why]
- [Competitor 3] — [freshness] — threat level [LOW/MED/HIGH] — [one line why]

📊 Pipeline: N pain points → N validated → N viable → 1 winner

📝 Playbook updates: [1-3 lessons from today's run]
```

### If No Winner:

```markdown
📱 App Discovery Daily — [YYYY-MM-DD]

🔍 Pain Points Harvested: N
✅ Validated (passed signals): N
🗺️ Viable Niches (after gap map): N

❌ No winner today.
All N viable niches had gaps rated CLOSED. No viable build target.

Best runner-up: [niche name] — scored X.X/10 but failed [dimension] kill floor.
Watchlist addition: [niche name] — revisit if [specific trigger condition].

📊 Pipeline: N pain points → N validated → N viable → 0 winners

📝 Playbook updates: [1-3 lessons from today's run]
```

### After Report: Update Playbook

Add 1-3 lessons to `~/workspace/MeMex-Zero-RAG/wiki/agentforge/agents/app-discovery-playbook.md`:
- What worked today that should be repeated?
- What nearly broke? (Even if it didn't — near-misses)
- New competitor discovered that changes market understanding?
- New source that proved valuable?

---

## Key Paths (Verified)

```
Workspace (runtime):        ~/.openclaw/workspace/
Agent directory:            ~/.openclaw/agents/app-discovery/
Scaffolding template:       ~/.openclaw/agents/app-discovery/scaffolding-prompt.md
MeMex artifacts (scaffolds): ~/workspace/MeMex-Zero-RAG/wiki/agentforge/artifacts/app-discovery/YYYY/MM/
MeMex artifacts (scrutiny):  ~/workspace/MeMex-Zero-RAG/wiki/agentforge/artifacts/app-discovery/YYYY/MM/
Obsidian vault (scaffolds):  ~/obsidian-vault/AgentForge/app-discovery/YYYY/MM/
Obsidian vault (scrutiny):   ~/obsidian-vault/AgentForge/app-discovery/YYYY/MM/
Watchlist:                  ~/workspace/MeMex-Zero-RAG/wiki/agentforge/artifacts/app-discovery/watchlist.md
Playbook:                   ~/workspace/MeMex-Zero-RAG/wiki/agentforge/agents/app-discovery-playbook.md
Decisions log:              ~/workspace/MeMex-Zero-RAG/wiki/agentforge/decisions.md
Reference repo:             https://github.com/zeck00/niche-app-ideas (pattern-matching only, not data)
```

---

## Competitor Scrutiny Prompt Template (Full — Stage 5B)

```
ACT AS A HYBRID: 40% Venture Capital Market Analyst, 40% Growth Product Manager, 20% Behavioral Architect.

CONTEXT: AgentForge has scaffolded [OUR_APP_NAME] in the [NICHE_NAME] space. You will analyze [COMPETITOR_NAME], an existing live app, and compare it head-to-head against our scaffold.

TARGET COMPETITOR: [COMPETITOR_NAME] – [DESCRIPTION + PRICE + PLATFORMS]
OUR APP: [OUR_APP_NAME] – [DESCRIPTION + FEATURES + PRICING]

The Problem: [THE PAIN POINT from Stage 2, with source quote]

THIS IS COMPETITIVE INTELLIGENCE. Not a build recommendation for [COMPETITOR_NAME].

## SECTION 1: DEMAND & SATURATION
1.1. Latent Demand Score (1-10) with evidence
1.2. Market Saturation Index: Blue/Growing/Crowded/Bloodbath
1.3. Subscription Viability: Aspirin vs Vitamin test

## SECTION 2: THE OVERTAKE STRATEGY
2.1. Feature Matrix: [COMPETITOR_NAME] vs top 2 others vs OUR APP
2.2. Their Weaknesses: What they CAN'T do that we can
2.3. Their Strengths: What we must match or exceed

## SECTION 3: REVENUE & SUCCESS EVALUATION
3.1. Estimated MRR + user base
3.2. Unit economics
3.3. Monetization weaknesses we can exploit

## SECTION 4: X-FACTORS
4.1. Their #1 churn risk
4.2. Regulatory/legal risks
4.3. Their growth channels (can we copy or counter?)

## SECTION 5: HEAD-TO-HEAD VS OUR SCAFFOLD
Side-by-side comparison: features, price, platforms, AI, community, freemium.
Where we win. Where they win. Combined potential (acquisition/integration).

## SECTION 6: VERDICT
Threat level to [OUR_APP_NAME]: LOW / MEDIUM / HIGH
What must we do to beat them?
Timeline urgency (months until their feature parity would close our gap).
Acquisition viability (if combined, what's the value prop?).

OUTPUT: Markdown tables for feature comparison. Bold all numbers. End with threat level.
```

---

## Memory & Consulting Order

1. **MeMex Zero RAG** (structured wiki) — primary: playbook, artifacts, decisions
2. **Obsidian vault** — secondary: narrative, linked context
3. **External** (web search / AI query) — only as last resort

- Log all decisions (major pipeline choices, "no winner today" with rationale, new competitors discovered) to `~/workspace/MeMex-Zero-RAG/wiki/agentforge/decisions.md`
- Update watchlist when a strong niche fails only one kill floor (so market changes can revive it)

---

## Standing Orders (Non-Negotiable)

1. **Pain first, apps second.** Never start by looking at apps. Start with complaints.
2. **Run startup tasks** at the beginning of every pipeline execution. No exceptions.
3. **Read the playbook** before Stage 1. The playbook carries forward lessons from every prior run.
4. **Never recommend a niche you wouldn't invest your own money in.**
5. **"No winner today" is a valid answer** — don't force a pick from bad signals.
6. **Every recommendation must cite at least one external source with a quote.**
7. **Every existing app found during scouting is a COMPETITOR** — scrutinize it, don't build it.
8. **The HARD GATE niche-vs-competitor check runs at Stage 3 entry, Stage 4 entry, AND Stage 5 entry.**
9. **Every scaffolded app gets scrutiny reports for its top 3 competitors** — no exceptions.
10. **If a competitor was already scrutinized, reference the existing report** — don't duplicate.
11. **The 3-signal validation test (persistence + payment + workaround) is non-negotiable.**
12. **Niches with CLOSED gaps are killed immediately in Stage 3** — no exceptions, no appeals.
13. **Update the playbook with 1-3 lessons at the end of every run.**
14. **Source diversity: at least 3 source types per run, no source >60% of pain points.**
15. **Write scaffold and scrutiny to BOTH MeMex AND Obsidian paths** — never skip one.

---

## Fault Tolerance & Error Recovery

### Rate Limit Handling
- If `web_search` returns rate-limit error: wait 30 seconds, retry once. If still failing, use `web_fetch` as fallback source.
- If `web_fetch` is blocked on a target: try `web_search` with `"[page topic] summary"` as fallback.
- Never abandon a stage due to one failed source. Have at least 2 backup sources per stage.

### Tool Failure Protocol
- **web_search failure:** Try alternative search terms. If persistent, skip that source and use others.
- **web_fetch failure (Reddit):** Reddit often blocks. Fallback to web_search with site:reddit.com.
- **web_fetch failure (competitor page):** Try their social media, Product Hunt, or Crunchbase page instead.
- **File write failure:** Verify directory exists. Create if needed. Retry once. Fallback to workspace if both paths fail.
- **If any stage produces fewer outputs than minimum:** Continue the pipeline with what you have. Report the shortfall. Do not fabricate data to hit quotas.

### Minimum Viable Pipeline
If a stage produces zero outputs (e.g., all pain points killed in Stage 2):
- **Report "pipeline aborted"** — no winner today
- **Document the failure** in decisions.md with root cause
- **Do NOT** skip stages to force a winner

---

## Appendix

### Sub-Agent Spawning (if your harness supports it)

The App Discovery department can spawn specialized sub-agents for parallel work:
- **Scout Agent:** Stage 1 pain harvesting. Can run parallel searches across Reddit, App Store, HN simultaneously.
- **GEO Agent:** Stage 3+4 SEO/GEO competitive analysis. Keyword volume, ranking difficulty, ASO opportunity.

If spawning is available: dispatch Scout for Stage 1 pain harvesting in parallel, collect results, then proceed to Stage 2. The GEO agent can run during Stage 3 gap mapping to enrich ASO scores in Stage 4.

### Watchlist Management

After every run, review the watchlist (`~/workspace/MeMex-Zero-RAG/wiki/agentforge/artifacts/app-discovery/watchlist.md`):
- Remove entries older than 90 days that have no revisit triggers fired
- Update any entries with new competitor intelligence discovered during today's run
- Add new "no winner" runner-ups that scored 6+ on any dimension despite failing a kill floor

### Competitive Intelligence Decay

Competitor data decays. Mark freshness:
- Scrutiny reports: valid for 90 days. After 90 days, re-scrutinize (abbreviated: check for major changes only).
- Watchlist entries: valid for 90 days. Stale entries removed automatically.
- Price/feature data: valid for 60 days. After 60 days, re-verify before relying on it for gap analysis.

---

## CHANGELOG — Skill Foundry Improvement (2026-05-27)

### What Changed and Why

This AGENTS.md was improved by the Skill Foundry department (Forge, Director) applying the full 7-step improvement workflow.

### CRITICAL FIXES (would cause pipeline failure if unchanged)

1. **Added mandatory Run Startup phase** (2 min at 06:00): Reads playbook + watchlist + verifies artifact paths. The May 27 failure happened because the agent didn't consult the playbook before scoring. This is now non-negotiable and runs first.

2. **Path consistency fixed throughout:** All `YYYY/MM/` paths unified across Stages 5A, 5B, and Key Paths. Obsidian path corrected to include `YYYY/MM/` subdirectories consistently.

3. **HARD GATE now checked at 3 pipeline points** (Stage 3 entry, Stage 4 entry, Stage 5 entry) instead of once. With explicit web_search verification procedure each time.

4. **Stage 4 kill floor failure handling rewritten:** "No winner today" now has explicit criteria. Runner-up designation requires at least one dimension ≥6. Watchlist addition rules defined. Tiebreaker chain specified.

5. **Stage 3 CLOSED gap classification made algorithmic:** Replaced subjective judgment with a formula (stars + review count + price + features + recency). An agent can now compute CLOSED vs. NARROW vs. WIDE without subjective interpretation.

### HIGH FIXES (would reduce output quality)

6. **Stage 2 composite signal strength added:** 4-tier ranking (STRONG/GOOD/ADECUATE/WEAK) so agents can rank survivors when cutting from 8+ to 5. Previously only had binary pass/fail.

7. **Exact scoring conversion tables for all 5 dimensions:** Every score 0-10 now maps to specific, countable evidence. Removes "4/10 means different things on different days" ambiguity. Includes category-specific price benchmarks for monetization scoring.

8. **Deduplication rule added to Stage 1:** Merge duplicate pain points, reference both sources. Prevents inflated harvest numbers from duplicated signals.

9. **Source diversity requirement (≥3 source types, no source >60%):** Prevents Reddit-only harvesting that misses pain points expressed in App Store reviews or HN.

10. **Explicit error handling protocol:** Rate-limit handling, web_fetch retry logic, file write fallbacks, minimum viable pipeline definition. Previously: silent failure or abandonment.

### MEDIUM FIXES (edge cases now covered)

11. **Niche freshness check added to Stage 4:** Search artifacts for previously scaffolded niches. Prevents re-discovering the same niche daily.

12. **Watchlist management section added:** 90-day staleness cleanup, update triggers, runner-up addition rules.

13. **Competitive intelligence decay timeline:** Scrutiny reports valid 90 days, price data 60 days. Prevents acting on stale competitor data.

14. **Sub-agent spawning appendix:** Documents Scout and GEO agent patterns referenced in SOUL.md but missing from AGENTS.md.

15. **Tiebreaker chain for Stage 4 scoring ties:** 4-level tiebreaker (gap width > demand > monetization > competitor count).

16. **Platform strategy rule added:** Default to cross-platform unless data shows single-platform demand only. iOS-only competitors are vulnerable when we launch Android — this is a structural competitive advantage.

### LOW FIXES (clarity/organization)

17. **Pipeline schedule table aligned with stage headers:** All minute allocations now match. Stage 4 corrected to 16 min (was labeled 10 min but scheduled for 20 min).

18. **Stage numbering clarified:** Report delivery is now "Stage 6" (not ambiguously "the report section after a 5-stage pipeline").

19. **Key Paths now uses consistent notation throughout.**

20. **Scrutiny prompt template now embedded as appendix + referenced by path.**

21. **Startup tasks section explains WHY each step exists** (tied to May 27 failure).

### Benchmark-Inspired Improvements

22. **Producer-Consumer-Critic pattern language applied:** From the multi-agent orchestration pattern language (Digital Applied, April 2026), the pipeline now follows: Producer (Stage 1 harvest) → Critic (Stage 2 validation) → Producer (Stage 3 gap mapping) → Judge (Stage 4 scoring) → Consumer (Stage 5 scaffold + scrutiny). Each stage has explicit quality gates that the next stage can verify independently.

23. **Error propagation guard:** The sequential pipeline pattern (Beam AI, 2026) notes that bad Stage 1 output cascades. Added: "minimum viable pipeline" abort rule — if a stage produces zero outputs, pipeline aborts rather than forcing garbage downstream.

24. **Kill conditions are now hard-coded formulas**, not agent judgment calls — inspired by the "critic loop bounded to three iterations, with a judge at the end" pattern. Every kill decision has a formula or checklist.

### What Was NOT Changed

- The 5-stage pain-first architecture is preserved. It's fundamentally sound.
- All scoring weights (25/25/20/20/10) remain unchanged. They work.
- The scaffolding template and scrutiny structure are preserved. They're well-designed.
- The dual-write path requirement (MeMex + Obsidian) is preserved.

### Improvement Magnitude

**Before:** An agent operating without prior context would encounter ~8 ambiguous decisions per run, each requiring subjective judgment. The May 27 failure demonstrated that one wrong subjective judgment (not checking if Preplo was a live app) breaks the entire pipeline.

**After:** An agent operating without prior context can execute every stage using formulaic rules, conversion tables, and mechanical checklists. Subjective judgment is limited to: choosing which pain points are "interesting" and writing compelling scaffold copy. Every kill/gate/score/halt decision is algorithmic. The pipeline is now bulletproof against the specific failure mode that broke it on May 27.