# App Discovery — Playbook

_Read before every run. Update after._

## Skill Assimilation Advisory

This department's AGENTS.md may be improved by the Skill Foundry at any time. When an improvement is applied:
- Date, what changed, and any adjustments made during assimilation are logged here
- Latest assimilation: 2026-05-27 — 24 improvements applied (34 gaps → algorithmic pipeline). See AGENTS.md changelog.

---

## CRITICAL: Pain-First Pipeline (Refactor 2026-05-27)

The pipeline was completely refactored after May 27's failure (declared live app Preplo as BUILD winner).

**Old pipeline (broken):** Scout apps → score apps → clone winner → sometimes scrutinize.
**New pipeline (current):** Harvest pain points → validate signals → map competitive gaps → score niche → scaffold OUR app → scrutinize competitors.

### The 5-Stage Flow
1. **PAIN HARVEST** — Scan Reddit, App Store reviews, HN for COMPLAINTS (not apps). Use pain keywords: "I wish there was", "frustrated with", "I'd pay for". Output: 10-15 pain points with quotes.
2. **SIGNAL CHECK** — Validate with 3-signal test: Persistence (≥3 threads, ≥1 month apart), Payment intent (explicit/implicit), Workaround pain (3+ tools or manual process). Kill if <2/3. Output: 5-8 validated.
3. **COMPETITIVE GAP MAP** — For each niche: who's solving it? How well? Gap width: WIDE (no solution), NARROW (overpriced/missing features), CLOSED (kill immediately). Output: 3-5 viable.
4. **NICHE SCORING** — Score the NICHE: Demand 25%, Gap Width 25%, ASO 20%, Monetization 20%, Urgency 10%. 1 winner or "no winner today".
5. **SCAFFOLD + SCRUTINIZE** — Build OUR app. Then scrutinize top 3 competitors against it. Every competitor gets a report.

### What Changed
- **Pain-first, not app-first** — never start by looking at apps
- **3-signal validation** — persistence + payment + workaround complexity before scoring
- **Gap mapping** — WIDE/NARROW/CLOSED replaces blind scoring
- **"No winner today"** is explicit and valid
- **Competitor scrutiny is MANDATORY** for every scaffold winner's top 3
- **Scoring weights adjusted** — Demand and Gap Width now 25% each (were 20% Market Signal + 20% Competition Gap)

## CRITICAL: Niche vs App Distinction (Hotfix 2026-05-27)

**The pipeline broke on May 27 because it confused existing live apps with market niches.**

- **Niche** = a market gap. "People can't save TikTok recipes to cook later." Score this. Build our app for it.
- **Competitor** = an existing app in that niche. "Preplo" or "ReciMe." Scrutinize this against our scaffold. Do NOT score it or declare BUILD.

**Rule: Before scoring anything, check if it's already live on App Store / Play Store. If yes → competitor, not build target.**

On May 27, the pipeline found Preplo on WhistleOut, scored it 7.7/10, declared BUILD, and announced it as the daily winner. Preplo is a live App Store app since March 2026. It should have been scrutinized as BiteSaver's #1 competitor, not declared a build winner. The niche was already won by BiteSaver on May 24.

**Pipeline fix:** AGENTS.md rewritten to separate Phase 1 (niche scouting) from Phase 5 (competitor scrutiny). Hard gate added: "Is this an existing app?" check before scoring.

## May 28 Lessons

### 1. Family Organizer = Reddit Goldmine
Domistiq's 1,281-thread Reddit analysis proved what we suspected: family organization is one of the most pain-rich, under-served niches on mobile. Parents are literally screaming into the void about context-switching between 5 apps. This category should be monitored weekly, not just during discovery runs. The AI+family intersection is where the next billion-dollar consumer app will come from.

### 2. "Free to Paid" Transitions Are Predictable Vulnerabilities
AppClose (co-parenting) faced a Reddit revolt when they added subscriptions in Jan 2026. Nori will face the same. When a competitor announces a free→paid transition, be ready with migration tools within 48 hours. This is a repeatable competitive attack pattern: monitor competitor pricing pages, detect the transition, market to their angry users immediately.

### 3. On-Device AI as Structural Competitive Advantage
Nori has the best AI features in the family organizer category, but all their processing is cloud-based. Family data (kids' schedules, dietary preferences, locations) in the cloud is a privacy vulnerability. On-device AI (our scaffold) creates a moat that cloud competitors can't match without a full architectural rewrite. This insight applies beyond family organizers — any app handling sensitive personal data should default to on-device AI.

## Scrutiny Patterns That Work
- **Competitor feature matrix** is the single most valuable section — enables direct comparison across price, features, platform, and moat
- **Web_fetch competitor's own comparison pages** (e.g., preplo.app/vs/recime) — they've already done the research. Use it to reverse-engineer their positioning.
- **Shipyard/Hackathon winners** are high-signal — they've passed judge evaluation AND have influencer partnerships built in. RevenueCat Shipyard winners are particularly strong signals (monetization baked in from day 1).
- **App Store review count** is the best traction proxy — fewer than 50 reviews = very early stage. 100+ reviews with 4+ stars = scaling.
- **Every scaffold winner's top 3 competitors MUST get scrutiny reports.** BiteSaver had Preplo and ReciMe in its matrix — ReciMe got scrutinized (May 26), Preplo was missed until CEO flagged it (May 27). This is now a standard rule.

## Scaffolding Improvements
- **Price anchoring matters** — BiteSaver's $4.99 vs Preplo/ReciMe's $9.99 is the strongest competitive lever. Always include a freemium comparison in scrutiny reports.
- **Platform gap analysis** — iOS-only apps have a capped TAM. Android-first competitors can exploit this. Flag platform gaps immediately.

## May 29 Lessons

### 1. Old Pipeline Artifacts = Broken Windows
Today's run replaced a May 29 artifact that was generated using the OLD app-first pipeline — even though the pipeline was refactored on May 27. The old run scouted ReciMe as a "winner" and scaffolded Plateful. This was wrong on arrival: the playbook explicitly mandates pain-first, not app-first. **Lesson:** Always check whether existing daily artifacts were generated with the CURRENT pipeline version before reading them as canonical. If they smell wrong (app names in the scout section instead of pain quotes), they ARE wrong. Replace them.

### 3. ADHD = The Most Underserved High-Value Mobile Niche
After family organizers (May 28), ADHD voice-first tools are the next pain goldmine. r/ADHD (1.9M members) has more explicit "I wish there was an app" content than any subreddit except r/Parenting. The key insight: ADHD users don't need another planner. They need a CATCHER — something that grabs thoughts before they vanish. The capture-first vs planner-first paradigm is the decisive product differentiator. ADHD users already pay for tools (Tiimo $4.99/mo, Motion $19/mo, Structured $2.99/mo), so monetization isn't theoretical.

### 2. HARD GATE Saved Us From KitchenPal
KitchenPal (pantry/food expiry) at 4.5★ with 7,000+ reviews and both platforms was correctly flagged as a CLOSED-approaching niche. The old pipeline would have scored and scaffolded it. The HARD GATE mechanism ("Is this already live on App Store? → Competitor, don't score") caught it. The pantry/food expiry niche isn't worth entering unless you can out-feature KitchenPal on AI-powered automatic expiry detection — and even then, their review moat is substantial.

## June 1 Lessons

### 1. Pet Medical Records = The Next Family Organizer
Like family organizers (May 28), pet health records is a pain-rich, under-served mobile niche with massive TAM. 90.5M US households own pets. 17% CAGR in pet insurance creates tailwind demand for organized records. Yet NO app in the space has AI scanning, insurance exports, or multi-vet merge. Three of the four top competitors have broken/basic features (11Pets file upload broken, PetDesk forced ads, PokiPaw manual-only). This is a WIDE gap with high demand and weak incumbents — the ideal pipeline target.

### 2. Monetization Must Match User Psychology
Splitwise exodus was flagged as a high-signal pain point (5+ Reddit threads, growing revolt). But signal check revealed users are angry about PAYING — they want free alternatives, not paid ones. At paid ones. A "Splitwise alternative" app with a subscription is self-defeating. Lesson: payment intent must be FOR the solution, not just against the incumbent. Verify that the pain includes willingness to pay, not just frustration with paying.\n\n### 3. Broken Core Features = Immediate Opportunity\n11Pets has "file upload does not work at all" in current App Store reviews — for a medical records app. This isn't a feature gap; it's a product failure. When an incumbent has a broken CORE feature (not a nice-to-have, but the app's fundamental promise), the window to capture their users is wide open. Scan for "doesn't work" or "broken" in competitor reviews specifically for core features — these are higher-signal than general dissatisfaction.\n\n## Competitor Moves Detected"}]
- **Preplo (May 2026):** RevenueCat Shipyard winner. iOS-only, $9.99/mo. Adding meal planning (roadmap). Missing Android, community, Pinterest import. Extraction quality is live and working (9K+/week). Lifetime option ($129.99) is rare in category.
- **ReciMe (May 2026):** 800K+ downloads, 201K+ reviews. Raised prices to $9.99/mo — churn risk. Missing AI adaptation, cost estimates, guided cook mode. Has Pinterest + Facebook import (advantage over Preplo). Meal planning is core.
- **Super Planner ADHD (May 2026):** Android-only voice-first ADHD task planner. AI-powered task breakdown, mood check-in, personality toggle. Low review count. Cloud AI (privacy gap). No iOS version — ThoughtLatch can capture iOS market uncontested.
- **WhisperPlan (2025-2026):** TestFlight-only ADHD voice-first task manager. Still in beta after 12+ months. First-mover positioning on ADHD + voice, but no launch momentum. iOS only.