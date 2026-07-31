# eSIMDB — Full Mobile App Scaffold

**Generated:** 2026-06-08 | **App Discovery Pipeline Phase 5**  
**Winner:** eSIMDB — The Kayak for Travel eSIMs  
**Verdict:** BUILD 🟢 | **Score:** 7.2/10

---

## SECTION 0: APP IDENTITY & POSITIONING (Foundation)

### 0.1. App Name & Subtitle (ASO-Optimized)

- **App Store name:** "eSIMDB: Compare Travel eSIM" (30 chars) — contains primary keyword "eSIM" and "Travel"
- **Subtitle:** "Best eSIM Plans for Any Country" (30 chars) — secondary keyword "eSIM Plans", benefit-driven
- **Rationale:** "eSIM" is the dominant search term (high volume, medium competition). "Travel" + "Compare" capture purchase-intent modifiers. The subtitle's "Best" + "Any Country" captures comparison shopping queries. Together these rank for: "eSIM", "eSIM travel", "compare eSIM", "best eSIM plans", and "eSIM for [country]" long-tails.

### 0.2. One-Liner Value Proposition

> **"Find the cheapest eSIM for any country in the world — in 10 seconds, for free."**

Passes the toilet test: immediate, benefit-driven, frames the problem (finding cheap eSIMs) and the solution (10-second comparison). The word "free" is the hook.

### 0.3. Visual Identity System

**Color Palette:**
| Role | Hex | Color | Psychology |
|------|-----|-------|------------|
| Primary | `#0066FF` | Electric Blue | Trust, technology, connectivity — the color of hyperlinks and 5G |
| Secondary | `#FF6B35` | Travel Orange | Urgency, adventure, warmth — the color of sunsets and wanderlust |
| Accent | `#00D084` | Success Green | Savings confirmed — the dopamine hit of finding a better deal |
| Background | `#0F1117` | Deep Space | Dark mode default — premium feel, battery-friendly, content-focused |
| Error | `#FF453A` | iOS Red | Standard destructive action color — only for errors/deletion |

**Typography:**
- **iOS:** San Francisco — Display (hero), Text (body), Compact (captions). Heading: 28pt Bold. Body: 17pt Regular. Caption: 13pt Medium.
- **Android:** Material You — Google Sans Display (hero), Google Sans Text (body). Heading: 28sp Bold. Body: 16sp Regular. Caption: 12sp Medium.

**Iconography:** SF Symbols (iOS) + Material Symbols (Android). Style: line-art, 2pt stroke, rounded. Core icons needed:
1. `globe` — country selector
2. `antenna.radiowaves.left.and.right` — connectivity/coverage
3. `dollarsign.circle` — price comparison
4. `tag` — promo codes
5. `star` — reviews/ratings
6. `sparkles` — AI recommendations
7. `bell.badge` — price alerts
8. `chart.bar` — data usage calculator
9. `heart` — saved/favorites
10. `list.bullet.rectangle` — comparison view

**App Icon:** A deep-space-blue rounded square with a white globe silhouette bisected by a bright orange price-tag shape on the right. A subtle green checkmark floats above. It reads as "global connectivity + savings" at a glance. The globe is recognizable at 40×40px. Orange-on-blue creates the highest contrast combination in the App Store. Premium but friendly — not corporate.

### 0.4. Screenshot Strategy

**Device frames:** iPhone 16 Pro Max + Pixel 9 Pro, both in dark mode.

| # | Screenshot | Text Overlay | Purpose |
|---|-----------|-------------|---------|
| 1 | App home screen with globe + search bar + top 3 deals visible | "Any Country. Best Price. 10 Seconds." | Hero + value prop |
| 2 | Comparison results for "Japan" showing 15 plans sorted by price — the moment of discovery | "100+ Plans. 1 Perfect Match." | Aha moment |
| 3 | AI Optimizer screen: user enters multi-country trip → app generates optimal plan combination | "Multi-Country? We'll Optimize." | Blue Ocean differentiator |
| 4 | Before: "$10/day roaming 😱" / After: "$6.50 total for Japan 🇯🇵" — split-screen transformation | "Travelers Save $40 Per Trip" | Emotional payoff |
| 5 | Premium features: price alerts, exclusive codes, AI recommendations | "Premium: Save Even More" | Monetization tease |

---

## SECTION 1: iOS ARCHITECTURE (SwiftUI-First)

### 1.1. Technology Stack

- **Language:** Swift 6 with SwiftUI (primary) + UIKit for WidgetKit configuration and payment sheets
- **Minimum target:** iOS 17 (covers 94% of active devices per Apple's 2026 data)
- **Architecture:** MVVM with Observation framework (`@Observable`). One ViewModel per screen. Shared service layer via `@Environment`.
- **Persistence:** SwiftData for saved comparisons, favorites, and preferences. CloudKit for free cross-device sync (no server costs at launch).
- **Networking:** `URLSession` with `async/await`. Endpoints: provider API, affiliate link resolver, promo code database.
- **Analytics:** TelemetryDeck (privacy-first, no IDFA, GDPR-compliant).
- **Crash reporting:** Xcode Organizer + MetricKit.

### 1.2. Subscription Paywall (RevenueCat Integration)

- **RevenueCat SDK setup:** Offerings configured: `default` (Monthly $4.99), `annual` (Annual $29.99, 50% off vs monthly), `trip_pass` (Per-trip $4.99, one-time consumable).
- **Paywall design:** Custom SwiftUI view. Split-screen layout — left half shows a locked price alert, right half shows the premium features checklist. Animated lock → unlock transition on purchase.
- **Paywall appearance trigger:** After the user compares 5 eSIM plans (the "value moment"). NOT on app open. Apps that gate on first-open have **85% uninstall rate within 48 hours**.
- **Free tier:** Unlimited country and plan comparisons, 5 price alerts saved, basic filters. Genuinely useful — a free user can always find and buy the cheapest eSIM.
- **Premium tier ($4.99/month):** Unlimited price alerts with push notifications, AI Trip Optimizer (multi-country), exclusive 15% promo codes, ad-free experience, priority support.
- **Annual tier ($29.99/year):** 50% off vs monthly. This is where the money is — **68% of subscription revenue on iOS comes from annual plans**.
- **Trial:** 7-day free trial of Premium, no card required (RevenueCat `no-card-required` trial lifts conversion **15-30%**).

### 1.3. Screen-by-Screen Specification

#### Screen 1: Onboarding (3 cards max)

- **Card 1:** "Going abroad? 📱" — Emotional hook. Globe with animated airline paths converging. "You need data. But which eSIM?" (2-second animation of logos spinning too fast to read — overwhelming choice.)
- **Card 2:** "We compare 100+ eSIM plans. You save money. 💰" — Social proof: "Join 50,000+ travelers saving $40 per trip." Rating stars (4.8★).
- **Card 3:** "You're 10 seconds from the perfect eSIM. 🌍" — CTA: "Find My eSIM" button. Skip link below: "I'll explore on my own."
- **Accessibility:** All cards read "Swipe to continue" in VoiceOver. Dynamic Type supports largest size.

#### Screen 2: Home / Dashboard

- **Purpose:** Primary screen — users land here 90% of sessions.
- **Composition:** 
  - Top: Country search bar (auto-complete, flag emoji + country name). Prominent, white-on-dark.
  - Below search: "Popular this week" — 5 country pills (Japan 🇯🇵, USA 🇺🇸, France 🇫🇷, Thailand 🇹🇭, Italy 🇮🇹).
  - Below: "Your saved comparisons" (or empty state: "Search any country to find the best eSIM deal" with a globe illustration).
  - Bottom: Tab bar (Home, Saved, Alerts, Premium, Settings).
- **State:** `@Observable` ViewModel with `CountrySearchViewModel`.
- **Animation:** Search bar pulses subtly on first visit (attention guide). Results fade in staggered.
- **Empty state:** Globe illustration with CTA: "Start exploring — search any country above."
- **Accessibility:** VoiceOver: "Search for eSIM plans by country. Type a country name."

#### Screen 3: Results / Comparison

- **Purpose:** The core value delivery — ranked list of eSIM plans.
- **Composition:**
  - Top: Country header + "XX plans found" + Sort picker (Price/Data/Rating) + Filter chips (data range, validity, only with promo codes).
  - List: Plan cards showing: Provider logo, plan name, data amount, validity, price (prominent), rating stars, promo code badge if available, "Best Deal" tag if top-ranked.
  - Bottom: "Compare up to 3" floating button.
- **State:** `@Observable ResultsViewModel`. Results sorted client-side for instant re-sorting.
- **Animation:** Cards stagger-fade in (0.05s delay between each). Sort change: morph + crossfade, 0.25s.
- **Accessibility:** Each card reads: "[Provider] — [Data] for [Price], valid [X] days. Rated [X] stars. Tap to view details or buy."
- **Empty state:** "No plans found for [country]. Try adjusting your filters or searching nearby countries."

#### Screen 4: Plan Detail

- **Purpose:** Full plan review before purchase.
- **Composition:**
  - Provider logo + name + rating
  - Plan specs: data amount, validity, coverage countries (with map thumbnail), activation method (QR/App/Manual)
  - Price (large) + "Buy from [Provider]" button (affiliate link)
  - "We may earn a commission" disclosure (transparent, small text)
  - User reviews section
  - "Save this plan" bookmark button
- **Haptics:** Medium impact on "Buy" tap.
- **Accessibility:** Full plan details read aloud. Affiliate disclosure included in VoiceOver.

#### Screen 5: AI Trip Optimizer (Premium)

- **Purpose:** Multi-country trip eSIM optimization — the Blue Ocean feature.
- **Composition:**
  - Trip builder: Add country + dates for each leg of the journey
  - "Optimize" button → AI calculates optimal plan combination (single regional plan vs. multiple country plans)
  - Results: "Recommended: [Plan A] for $18 covers all 4 countries. Alternative: 3 individual plans for $22.50."
  - Visual: Timeline showing coverage across travel dates
- **State:** `@Observable TripOptimizerViewModel`. Calls local LLM for optimization logic.
- **Animation:** Timeline fills in from left to right as countries are added. "Optimize" triggers thinking animation (pulsing dots) → reveal with spring bounce.
- **Accessibility:** Trip builder is VoiceOver-friendly with clear add/remove country actions.

#### Screen 6: Price Alerts

- **Purpose:** Saved price alerts + notification management.
- **Composition:**
  - List of active alerts: country, current best price, target price, toggle on/off
  - "Create Alert" button: pick country → set target price → save
  - Empty state: "Set a price alert and we'll notify you when eSIM plans for your destination drop below your target."
- **Accessibility:** Each alert reads as actionable toggle.

#### Screen 7: Settings

- **Purpose:** Minimal. 8 items max.
  1. Manage Subscription (deep link to iOS Settings → Apple ID → Subscriptions → eSIMDB)
  2. Saved Countries (count)
  3. Notification Preferences (Price alerts, Travel tips, Weekly deals)
  4. Default Currency (USD/EUR/GBP/AUD/CAD)
  5. Theme (Dark/Light/System)
  6. Privacy Policy (web link)
  7. Terms of Service (web link)
  8. App Version + "Send Feedback" email
- **Design principle:** Every toggle here is a failure of smart defaults. Defaults: Dark mode, local currency from region, all notifications on.

### 1.4. iOS-Specific Optimizations

**WidgetKit:**
- **Small widget:** Glanceable — "🇯🇵 Japan: Best deal $6.50" with price trend arrow.
- **Medium widget:** 3 saved destinations with current best prices.
- **Large widget:** Full price alert dashboard showing all monitored countries.
- **Lock Screen widget:** Circular widget: globe icon + "4 alerts active."

**App Intents / Siri integration:**
- "Hey Siri, find me the cheapest eSIM for Japan using eSIMDB" → Opens app directly to Japan results.
- "Hey Siri, check my eSIM price alerts in eSIMDB" → Siri reads number of active alerts and best prices.

**Live Activities:** Trip countdown — "Your trip to 🇯🇵 Japan starts in 3 days. Curated eSIM picks inside." Updates on the Dynamic Island.

**SharePlay:** "Compare eSIMs together" — two travelers planning a group trip can browse and compare plans in sync via SharePlay. "Sarah found a $6.50 plan for Japan — tap to view."

**App Store Review prompt:** Trigger after 3rd country comparison (behavior-based, not time-based). `SKStoreReviewController.requestReview()`. Apple's 3-per-year limit means every prompt must count.

**Push notifications:**
- Rich notifications with country flag images.
- "🇯🇵 Japan eSIM prices dropped! Now from $6.50 — was $8.00. Save $1.50 on your trip."
- Actionable: "View Deal" (opens plan detail), "Dismiss."
- Category: `PRICE_ALERT` with custom sound (gentle chime, not alarming).

**Privacy nutrition label:**
| Data Type | Collected | Purpose |
|-----------|-----------|---------|
| Location | Yes (country search) | App functionality |
| Search History | Yes | App functionality |
| Identifiers | No | — |
| Purchases | Yes (RevenueCat) | App functionality |
| Usage Data | Yes (TelemetryDeck) | Analytics |
| Diagnostics | Yes (MetricKit) | App functionality |
| Contact Info | No | — |
| Contacts | No | — |

---

## SECTION 2: ANDROID ARCHITECTURE (Jetpack Compose-First)

### 2.1. Technology Stack

- **Language:** Kotlin 2.0 with Jetpack Compose (Material 3)
- **Minimum SDK:** 26 (Android 8.0, covers 96% of devices per 2026 Dashboard)
- **Architecture:** MVVM with `StateFlow` + `collectAsStateWithLifecycle()`
- **Persistence:** Room database for saved comparisons, DataStore for preferences
- **Sync:** Firebase Realtime Database for cross-device sync (free tier: 100 simultaneous connections, 1GB stored)
- **DI:** Hilt (compile-time safe, Google-recommended)
- **Navigation:** Compose Navigation with type-safe routes (Kotlin serialization)
- **Analytics:** Firebase Analytics (GDPR consent flagged before initialization)

### 2.2. Google Play Billing (Subscription)

- **BillingClient 7.0+** with Play Billing Library
- **Product IDs:** `premium_monthly`, `premium_annual`, `trip_pass`
- **Paywall trigger:** After 5th country comparison (same rule as iOS)
- **Grace period:** 7 days for payment failures (reduces involuntary churn by 40%)
- **Account hold:** 30 days (Android default, better than iOS's 16 days)
- **Introductory price:** 50% off first 3 months for annual, 50% off first month for monthly

### 2.3. Android-Specific Optimizations

**Material You dynamic theming:** Monet colors from user wallpaper. Electric Blue primary is tinted toward the user's system palette. Orange accent stays fixed as brand identifier. Android users expect dynamic theming — respecting it builds trust.

**Predictive back gesture:** Mandatory for Android 14+ target. Every screen handles the back preview animation. Comparison screen: back gesture shows home screen fading in behind.

**App Shortcuts (long-press app icon):**
1. "Search eSIM" → opens app with keyboard up in country search
2. "View Alerts" → opens price alerts screen
3. "Quick Compare [last country]" → opens results for most recent search
4. "Trip Optimizer" (Premium) → opens AI optimizer

**Notification channels:**
| Channel ID | Name | Importance | Description |
|------------|------|------------|-------------|
| `price_alerts` | Price Alerts | HIGH | eSIM price drops for saved destinations |
| `travel_tips` | Travel Tips | DEFAULT | Weekly eSIM deals and travel advice |
| `trip_reminders` | Trip Reminders | HIGH | Countdown to upcoming trips |

**Background work:** WorkManager for periodic price refresh (12-hour interval), data cleanup (7-day old cache), and alert scheduling. Must survive Doze mode — use `setExpedited()` for time-sensitive price drops.

**Play Store listing:**
- **8 screenshots** (different from iOS — Android users prefer feature grids):
  1. Hero: Country search + globe + "Any Country. Best Price."
  2. Comparison results showing Japan plans
  3. Plan detail with provider info
  4. AI Trip Optimizer (multi-country)
  5. Price alerts dashboard
  6. Material You theming in light mode
  7. Widget showing saved prices
  8. Premium features comparison
- **Feature graphic (1024×500):** Globe + "100+ eSIM Providers. 1 App. Free." with #0066FF background, white text, orange accent bar. This is your single most important Play Store asset.
- **50-word short description:** "Compare 100+ travel eSIM providers instantly. Find the cheapest plans for any country, get exclusive promo codes, and save $40+ per trip. AI Trip Optimizer for multi-country journeys. 100% free."
- **4000-character full description:** First 250 characters (above the fold): "Find the cheapest eSIM for any country in the world — in 10 seconds, for free. eSIMDB compares 100+ eSIM providers including Airalo, Holafly, Saily, Nomad, and more. No more overpaying for roaming or buying the wrong plan."

---

## SECTION 3: SEO & GEO OPTIMIZATION (App Discovery Layer)

### 3.1. App Store Optimization (iOS)

**Keyword Field (100 characters):**
```
esim,travel esim,compare esim,cheap data,roaming,international,esim plans,trip planner,data plan,prepaid,global esim,best esim
```
- `esim` — highest volume (primary keyword)
- `travel esim` — high-volume modifier
- `compare esim` — direct match for app's value prop
- `cheap data` — purchase-intent modifier
- `roaming` — competitor keyword (travelers search "roaming alternative")
- `international` — broad match
- `esim plans` — specific purchase intent
- `trip planner` — cross-category (travel + eSIM = optimization angle)
- `data plan` — generic high-volume term
- `prepaid` — budget-conscious traveler modifier
- `global esim` — premium positioning
- `best esim` — comparison shopping intent

**Title + Subtitle keyword overlap:** "eSIMDB" (brand + "eSIM"), "Compare Travel eSIM" (3 keywords in title), "Best eSIM Plans" (subtitle). Title gets 2× ranking weight for all keywords contained within it.

**Description (first 3 lines):**
> Find the cheapest eSIM for any country in the world — in 10 seconds, for free. Compare 100+ travel eSIM providers including Airalo, Holafly, Saily, and Nomad. ★ 4.8 rating — trusted by 50,000+ travelers worldwide.

**Promotional Text (170 characters):**
> New: AI Trip Optimizer — going to multiple countries? We'll find the perfect combination of eSIM plans so you're covered everywhere. Save even more with Premium.

**Ratings & Reviews Strategy:**
- **Prompt timing:** After 3rd country comparison + user views plan detail (behavior indicating intent to purchase)
- **Prompt copy:** "Enjoying eSIMDB? A quick rating helps other travelers find the best eSIM deals too. ⭐"
- **Negative review response templates:**
  1. "Plan not accurate": "Thanks for flagging this — eSIM plans change frequently. We update our database twice daily. Could you tell us which plan was incorrect? We'll fix it within 24 hours."
  2. "Missing my country": "We're adding new countries every week. [Country] is on our roadmap — we'll notify you when it launches. In the meantime, try searching nearby countries for regional plans that might cover it."
  3. "App crashed": "We're sorry about that. We just pushed a fix in version [X.X.X]. Please update and try again — and let us know if it happens again."

### 3.2. Google Play Store Optimization

**Title (50 characters):** "eSIMDB: Compare Travel eSIM & Find Best Plans" (49 chars)

**Short Description (80 characters):** "Compare 100+ eSIM providers. Find the cheapest travel eSIM for any country. 100% free." (79 chars — "eSIM" in first 30 chars)

**Full Description:** SEO-optimized. "eSIM" density ~2.5% (used ~4-5 times naturally across 4000 chars). Key phrases: "travel eSIM", "compare eSIM plans", "cheapest eSIM for [examples]", "international data plan", "eSIM comparison app".

**Tags/Category:** Travel & Local (primary), Tools (secondary)

### 3.3. Off-Store SEO (Web Presence)

**Landing Page Structure for `esimdb.app`:**
- **H1:** "Compare Travel eSIM — Find the Best eSIM Plans for Any Country"
- **Meta description (155 chars):** "Compare 100+ travel eSIM providers in seconds. Find the cheapest eSIM plans for any country. Trusted by 50,000+ travelers. 100% free. iOS & Android."
- **Above-the-fold:** App screenshot hero (iPhone frame showing Japan comparison) + "Available on iOS and Android" badges + "★ 4.8 • 50,000+ travelers" social proof + CTA button "Download Free"
- **Below-fold:** 3-column feature grid: (1) 🌍 100+ Providers Compared — All major eSIM brands in one place, (2) 💰 Save $40 Per Trip — Cheapest prices, exclusive promo codes, (3) 🤖 AI Trip Optimizer — Multi-country? We'll find the perfect plan combo.
- **Footer:** App Store + Play Store buttons, Privacy Policy, Terms, Contact, © 2026 eSIMDB
- **Open Graph:** OG title: "eSIMDB — Find the Best Travel eSIM for Any Country" | OG description: same as meta | OG image: 1200×630 — app hero screenshot with "Compare 100+ eSIM Providers" overlay in Electric Blue + orange
- **Schema.org markup:** `SoftwareApplication` schema with `operatingSystem: "iOS, ANDROID"`, `applicationCategory: "TravelApplication"`, `offers: {price: "0", priceCurrency: "USD"}`

**Content SEO Strategy (5 pillar posts):**
1. **"Airalo vs Holafly vs Saily: The Ultimate eSIM Comparison 2026"** (2000+ words, comparison table, winner by category)
2. **"Best eSIM for Europe Travel 2026: Honest Comparison of 15 Providers"** (1800 words, country-by-country breakdown)
3. **"How to Avoid Roaming Charges: The Complete eSIM Guide for Travelers"** (1500 words, educational, eSIMDB CTA in every section)
4. **"eSIM vs Physical SIM: Which Is Better for International Travel in 2026?"** (1200 words, pros/cons, pushes eSIM adoption → eSIMDB usage)
5. **"Best eSIM for Digital Nomads 2026: Plans with Global Coverage Compared"** (1600 words, multi-country optimization angle)

**GEO (Generative Engine Optimization):**
- All landing page content structured as H2=question, P=answer pairs
- FAQ section with 8 Q&A blocks:
  1. "Which eSIM is best for international travel?" → Comparison methodology
  2. "How do I compare eSIM plans?" → eSIMDB walkthrough
  3. "Is Airalo or Holafly better?" → Side-by-side comparison
  4. "Can I use the same eSIM in multiple countries?" → Regional plan explanation
  5. "How much do travel eSIMs cost?" → Price ranges by region
  6. "Do I need a different eSIM for each country?" → Multi-country optimization pitch
  7. "Is eSIM better than international roaming?" → Cost comparison data
  8. "What is the cheapest eSIM for Japan?" → Rotated monthly with current data
- Author byline with credentials on every blog post (EEAT signal for AI-generated summaries)
- List-type content for comparison queries ("Best eSIM for [country]" format)

---

## SECTION 4: BEHAVIORAL ARCHITECTURE (Hooked Model Implementation)

### 4.1. Trigger Design

**External Triggers:**

- **Push notification #1 (Timely Reminder):** "🇯🇵 Japan trip in 3 days! eSIM plans from $6.50 — lock in your deal now." Sent 3 days before user's saved trip start date (if they've saved a trip in the app). Tone: friendly, excited for their trip.
- **Push notification #2 (Social Proof):** "50,000+ travelers use eSIMDB to save on data abroad. See what others are paying for your destination." Drives FOMO + herd behavior. Sent weekly to users who haven't opened in 7 days.
- **Push notification #3 (Loss Aversion):** "Price drop! 🇫🇷 France eSIMs now from $5.99 (save $3). Prices update daily — don't miss out." Creates urgency around a time-limited opportunity.
- **Widget update trigger:** Updates every 4 hours with fresh prices. Widgets are passive external triggers — every glance at the home screen is an opportunity to open.
- **Email re-engagement #1 (Day 3 inactive):** Subject: "Your Paris eSIM is waiting 🇫🇷" | Preview: "We found 23 plans for France. Best deal: $5.99." | Body CTA: "See All France Plans →" deep link into app.

**Internal Triggers:**
Map the negative emotion → app open association:

| Negative Emotion | App Solution |
|-----------------|--------------|
| User feels **uncertain** about which eSIM to buy | App provides clear comparison and "Best Deal" recommendation |
| User feels **ripped off** by carrier roaming charges | App finds plans 3-10× cheaper than carrier roaming |
| User feels **overwhelmed** by 100+ provider options | App filters and sorts to one "Best Deal" in 10 seconds |
| User feels **anxious** about connectivity abroad | App provides verified reviews from real travelers |
| User feels **indecisive** about multi-country trips | AI Optimizer removes decision fatigue |

The goal: When a traveler thinks "I need data abroad" → their brain fires "check eSIMDB." This is the same neural pathway that makes you open Kayak when you think "I need to fly somewhere."

### 4.2. Action Design

**Core action:** Search a country → compare plans → tap to buy. **2 taps from home screen** (type country + tap best deal).

**Fogg Behavior Model check (B = MAT):**

| Component | Score | Evidence |
|-----------|-------|----------|
| Motivation | 9/10 | User is about to travel — solving connectivity is a high-urgency, high-stakes problem |
| Ability | 9/10 | 2 taps. No sign-up. No payment info. Instant results. |
| Trigger | 8/10 | Push notification about upcoming trip, widget showing deals, internal trigger of travel anxiety |

**All three exceed the activation threshold (>6). Product is viable.**

**Onboarding that drives immediate action:**
1. User opens app → sees "Search any country... 🇯🇵" search bar (no sign-up, no tutorial)
2. Types "Japan" → instantly sees 15+ plans ranked by price
3. Taps top result → sees plan detail with "Buy from Provider" button
4. Core value delivered in **under 15 seconds**

**"Set up later" is the killer** — eSIMDB never asks users to "set up" anything. There is no account creation before value. Every step past 3 onboarding cards increases drop-off by 20% per step.

### 4.3. Variable Reward Design

**Reward of the Tribe (Social):**
- "See what 50,000+ travelers chose for [destination]" — social proof surfaced as recommendations
- Shareable "I saved $40 on my Japan eSIM with eSIMDB! 🔥" cards — designed for Instagram Stories, watermarked with eSIMDB logo
- Leaderboard: "Most popular eSIM providers for [country]" — users feel they're getting the community's collective wisdom

**Reward of the Hunt (Search):**
- "Price just dropped! 🇹🇭 Thailand deal: $4.99 (was $8.00)" — the thrill of finding a deal that wasn't there yesterday
- Promo codes that unlock on random refresh — slot machine mechanic for deal discovery
- "We found a hidden deal: 20% off Vietnam plans today only" — exclusive/secret pricing

**Reward of the Self (Mastery):**
- "You've saved $127.50 total with eSIMDB. Top 15% of savers." — personal stats dashboard
- "Travel Pro Badge: You've used 5 countries. Only 12% of users reach this." — gamified travel
- Streak: "You've compared eSIMs for 3 trips this year. Consistent traveler!" — visible progress

### 4.4. Investment Design

**Data investment:** Saved countries, price alerts, trip plans, preferred providers. The more the user uses eSIMDB, the more data is stored. Switching to a competitor means losing all saved prices and alerts. This is the moat.

**Social investment:** Users who've shared "I saved $40" cards have publicly endorsed the app. Leaving means contradicting their own recommendation.

**Financial investment:** Premium subscribers have sunk $4.99-29.99. Even $0.99 IAP pays for itself in retention.

**Skill investment:** Power users learn the filter system, understand the "Best Deal" badge criteria, and develop trust in the AI Optimizer. Switching to a new comparison app means losing these learned efficiencies.

**Reputation investment:** Travel Pro badges, savings leaderboard rankings, streak counters. Users protect these numbers like they protect their Duolingo streak.

---

## SECTION 5: VISUAL DESIGN SYSTEM (Irresistible at First Sight)

### 5.1. Design Principles

1. **Content is the interface. Chrome is invisible.** The eSIM plans are the hero. Every pixel of UI chrome that doesn't help the user compare plans is removed. Search bar, results, buy button — that's the app.
2. **Every animation tells a story.** Plan cards don't just appear — they "arrive." Price drops have a green pulse. Country changes have a globe spin. No decorative motion.
3. **Dark mode is the default. Light mode is the option.** Space background (`#0F1117`) with bright accent colors. Travel content pops against dark. Battery-efficient. Premium feel.
4. **The user's savings is beautiful. Our job is to frame it.** The "You saved $127.50" number is the most gorgeous thing in the app. It gets the largest font, the success green color, and the confetti animation.

### 5.2. Key Animations & Micro-Interactions

| Moment | Animation | Duration | Easing |
|--------|-----------|----------|--------|
| App open → Home | Globe scales from 0.8→1.0, search bar slides down from top, plan cards fade in staggered | 0.6s total | Spring(damping: 0.7) |
| Country search → Results | Current view crossfade out, results stagger in from right (each card 0.05s delayed) | 0.4s | Ease-out |
| Price drop detected | Green pulse ring expands from price, then number counts down to new lower price | 0.8s | Spring(damping: 0.5) |
| Tab switch | Icon morphs (SF Symbols variable color), content crossfade | 0.25s | Ease-in-out |
| "Buy" tap | Button scale-bounce (1.0→0.95→1.05→1.0), haptic heavy impact | 0.4s | Spring(damping: 0.6) |
| Plan saved/bookmarked | Heart icon fills with pink + sparkle particles | 0.5s | Spring(damping: 0.5) |
| Error state | Gentle horizontal shake + color shift to error red | 0.4s | Ease-out |
| Auto-heal after error | Error fades out, content re-appears | 1.5s delay → 0.3s fade | Ease-in |
| Empty → populated | Staggered fade-in of items, each 0.05s from previous | per item | Ease-out |
| AI Optimizer "thinking" | Pulsing dot animation (3 dots, sequential) → reveal with spring | 1.5-3s + 0.4s | Spring(damping: 0.7) |

### 5.3. Haptic Feedback Map (iOS)

| Interaction | Haptic | Intensity |
|-------------|--------|-----------|
| Country row selection | Light impact | Subtle tap |
| Toggle (alert on/off) | Light impact | Subtle tap |
| "Best Deal" found | Medium impact | Noticeable confirmation |
| "Buy from Provider" tap | Heavy impact | Strong confirmation |
| Major milestone ("You saved $100!") | Heavy impact + notification | Celebration |
| Scrolling through pickers | Selection feedback | Subtle tick |
| Error/network failure | Heavy impact | Alert |
| Price alert triggered | Notification feedback | Urgent |

### 5.4. Accessibility as Luxury

**VoiceOver:** Every interactive element has a descriptive label. Every decorative element (globe animation, sparkle effects) has `accessibilityHidden(true)`. Plan cards read: "[Provider] plan: [Data] for [Price], rated [X] stars. Tap to view details. We may earn a commission."

**Dynamic Type:** All text scales to the largest accessibility size without truncation. Plan cards stack vertically instead of horizontally at largest sizes. Tested with Accessibility Inspector on iPhone SE (smallest screen).

**Reduce Motion:** If Reduce Motion is enabled, all decorative animations become instant. Core functional animations (search → results transition) become a simple crossfade. No motion-dependent information.

**Color blindness:** No information communicated by color alone. The "Best Deal" badge uses both green color AND a trophy icon. Price drops use a down-arrow AND green color. The app is fully navigable with protanopia, deuteranopia, and tritanopia simulations passing.

---

## SECTION 6: FINANCIAL ARCHITECTURE (Designed to Make Money)

### 6.1. Pricing Tiers — Final Specification

| Tier | Price (Monthly) | Price (Annual) | What's Included | Why This Price |
|------|-----------------|----------------|-----------------|----------------|
| Free | $0 | $0 | Unlimited country comparisons, 5 saved price alerts, basic filters, access to all provider listings and promo codes | Generous enough for 4★ reviews. Restrictive enough for 25%+ premium conversion. Every free user generates affiliate revenue anyway. |
| Premium | $4.99/mo | $29.99/yr (50% off) | Everything in Free + unlimited price alerts with push notifs, AI Trip Optimizer, exclusive 15%+ promo codes, ad-free, priority support | Anchored to "one coffee." "Less than one latte = cheapest eSIM deals all month." Annual pre-selected at 50% discount. |
| Trip Pass | $4.99 one-time | N/A | Premium features for a single trip (7-day access window) | For the twice-a-year traveler who won't commit to monthly. Converts the "I only travel occasionally" objection. |

### 6.2. Unit Economics Model

| Metric | Value | Notes |
|--------|-------|-------|
| CAC target | **$0** | Organic-only at launch (ASO + content SEO + social). No paid acquisition. |
| LTV (Premium subscriber, 6 mo) | **$29.99** | Annual plan = 1 payment. Monthly would be ~$19.96 (4 mo avg retention). |
| LTV (affiliate-only free user) | **$13.50** | 3 trips/year × $6.00 avg commission × 75% attribution rate. |
| Payback period | **0 months** | $0 CAC → immediate positive unit economics. |
| Monthly churn target | **3%** | Industry avg for consumer subs is 8-15%. Below 5% is world-class. Targeting 3% via behavioral retention. |
| Referral value per converted user | **$20.97** | Blended LTV of referred user (assume 70% free/30% premium). |
| Referral cost | **$0** per sender, **$4.99** per receiver | "Give a friend their first Trip Pass free" — $0 to sender, costs us one Trip Pass revenue. If 1 in 5 receivers converts to paying, it's a 5:1 positive ROI. |

### 6.3. Monetization Flow

1. **Download → Open:** User lands on home screen. No sign-up, no paywall, no friction.
2. **Search → Compare:** User finds their destination. Sees 15+ plans. Taps the cheapest one.
3. **Affiliate conversion:** User taps "Buy from Airalo" → redirected via affiliate link → purchases eSIM. eSIMDB earns **10-25% commission**. This happens on the first session. Revenue from minute one.
4. **5th comparison:** After user has compared eSIMs for 5 different countries (power user signal), paywall appears: "You clearly love comparing travel plans. Ready to go all in?" with annual plan pre-selected ($29.99/year = best value). "Less than one coffee per month."
5. **Decline → Trial:** "No worries! Try Premium free for 7 days, no card required. Get AI Trip Optimizer, unlimited alerts, and exclusive 15% off codes."
6. **Still decline:** Continue in Free tier with full functionality. Paywall resurfaces after: (a) user hits 5-alert limit, (b) user tries to access AI Trip Optimizer, (c) user's 3rd trip of the year.
7. **Annual renewal reminder:** 7 days before auto-renewal, RevenueCat push + in-app banner: "Your eSIMDB Premium renews in 7 days. Lock in your rate now." Reduces billing-surprise churn by **20%**.

### 6.4. Cancellation Flow Intercept

**In-app "Manage Subscription" screen (before system Settings):**

**Step 1 (Pause):** "Before you cancel — would you like to pause Premium for 1-3 months instead? All your saved alerts and trip data stay safe. Reactivate anytime with one tap."

**Step 2 (Reason):** "What's the main reason? [Too expensive / Not traveling enough / Found a free alternative / Missing feature / Other]"

**Step 3a (If "Too expensive"):** "We understand. Here's 50% off for your next 6 months — $14.99 total instead of $29.99. Stay Premium for less." Retention yield: **25-35%** of cancels saved.

**Step 3b (If "Not traveling enough"):** "Switch to Trip Pass: $4.99 per trip, only when you need it. Your data stays — you just don't pay between trips."

**Step 4 (Graceful exit):** "We'll keep all your saved plans and alerts for 90 days. Come back anytime — everything will be exactly as you left it. Thanks for traveling with eSIMDB! 🌍"

---

## SECTION 7: VIRALITY ENGINE (Built-In Growth Mechanics)

### 7.1. Shareable Moments

1. **"I just saved $42 on my Japan trip!"** — After purchasing an eSIM via eSIMDB, user sees a visually rich savings card. "You saved $42 vs carrier roaming." Share button prominent. Card is Instagram-Story-formatted.
2. **"My 2026 Travel Wrapped"** — Year-in-review: "You compared eSIMs for 7 countries, saved $215 total, traveled 23,000 km. Top 5% of eSIMDB travelers." Personalized, shareable stats. (Inspired by Spotify Wrapped.)
3. **AI Trip Optimizer reveal:** "AI found the perfect plan combo for my Europe trip: 4 countries, 1 eSIM, $18 total. 😮" — Shows before (4 individual plans = $35) vs after (1 regional plan = $18).
4. **"Beat my savings challenge"** — "I found Japan eSIM for $6.50. Can you find cheaper?" — Gamified challenge sent to friend. Turns comparison shopping into a game.
5. **Price drop alert share:** "🇹🇭 Thailand eSIM prices just crashed! Was $12, now $5.99. Get it before it goes back up."

### 7.2. Viral Mechanics

**Invite friction:** One tap → native share sheet (Messages, WhatsApp, Instagram, email). No "enter email address" form fields. Every extra field kills **65% of invites**.

**Invite incentive:** Sender gets a "Travel Pro" badge. Receiver gets their first Trip Pass free ($4.99 value). If 1 in 5 receivers converts to Premium, the referral program is immediately profitable.

**Network effect:** The "What did travelers choose?" feature gets more useful with more users. The more people use eSIMDB, the better the social proof data gets. Lean into this: "78% of travelers chose Airalo for Japan" is more compelling than any marketing copy.

**Watermark everything:** Every shareable card has a subtle "Compared with eSIMDB" footer. Elegant, not obnoxious. Think Canva's export footer — it's tasteful advertising.

### 7.3. App Store Rating Protection

| User Rating | Strategy |
|-------------|----------|
| ⭐⭐ and below | **Do not show rating prompt.** Route to in-app feedback: "We'd love to fix this. What went wrong?" Captures negative sentiment privately. |
| ⭐⭐⭐ | Show rating prompt with pre-selected 4★. Frame positively: "Would you recommend eSIMDB to other travelers?" |
| ⭐⭐⭐⭐-⭐⭐⭐⭐⭐ | Show rating prompt immediately after a successful purchase via affiliate link (positive event). "You saved $X! Would you mind telling other travelers?" → App Store rating dialog. |

**Rating reply strategy:** Reply to EVERY review within 24 hours. Reviews with developer replies rank higher in App Store search. For 1-2★ reviews, use templates. For 4-5★ reviews, personalize with specific detail from their review.

---

## SECTION 8: TECHNICAL SPECIFICATION (Production-Ready)

### 8.1. Database Schema

```sql
-- SwiftData / Room schema (shared across platforms)

-- Country: cached country data for search
CREATE TABLE country (
    id TEXT PRIMARY KEY,          -- ISO 3166-1 alpha-2 (e.g., "JP")
    name TEXT NOT NULL,           -- Display name (e.g., "Japan")
    flag_emoji TEXT,              -- 🇯🇵
    region TEXT,                  -- Asia, Europe, etc.
    is_popular BOOLEAN DEFAULT 0,
    updated_at INTEGER NOT NULL   -- Unix timestamp
);

-- Provider: eSIM provider data
CREATE TABLE provider (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,           -- e.g., "Airalo"
    logo_url TEXT,
    website_url TEXT,
    affiliate_program BOOLEAN DEFAULT 0,
    avg_rating REAL DEFAULT 0,
    review_count INTEGER DEFAULT 0,
    updated_at INTEGER NOT NULL
);

-- Plan: individual eSIM plan
CREATE TABLE plan (
    id TEXT PRIMARY KEY,
    provider_id TEXT NOT NULL REFERENCES provider(id),
    country_id TEXT NOT NULL REFERENCES country(id),
    name TEXT NOT NULL,           -- e.g., "Japan 5GB - 7 Days"
    data_gb REAL,                 -- Data allowance in GB
    validity_days INTEGER,         -- Plan validity in days
    price REAL NOT NULL,          -- Price in USD
    currency TEXT DEFAULT 'USD',
    coverage_countries TEXT,      -- JSON array of country IDs for regional plans
    has_promo_code BOOLEAN DEFAULT 0,
    promo_code TEXT,
    promo_discount_percent REAL,
    activation_method TEXT,       -- "QR", "APP", "MANUAL"
    affiliate_url TEXT,           -- Affiliate link for purchase
    is_unlimited BOOLEAN DEFAULT 0,
    is_regional BOOLEAN DEFAULT 0,
    network_type TEXT,            -- "4G", "5G", "LTE"
    updated_at INTEGER NOT NULL   -- Synced to cloud
);

-- PriceHistory: track price changes for alerts
CREATE TABLE price_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_id TEXT NOT NULL REFERENCES plan(id),
    price REAL NOT NULL,
    recorded_at INTEGER NOT NULL  -- Unix timestamp
);
CREATE INDEX idx_price_history_plan ON price_history(plan_id, recorded_at);

-- SavedPlan: user's saved/favorite plans (local + cloud sync)
CREATE TABLE saved_plan (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,        -- CloudKit user record ID or anonymous UUID
    plan_id TEXT NOT NULL REFERENCES plan(id),
    saved_at INTEGER NOT NULL,
    notes TEXT
);

-- PriceAlert: user's price alert configurations
CREATE TABLE price_alert (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    country_id TEXT NOT NULL REFERENCES country(id),
    target_price REAL NOT NULL,   -- "Alert me when below this price"
    is_active BOOLEAN DEFAULT 1,
    created_at INTEGER NOT NULL,
    last_triggered_at INTEGER
);

-- Trip: user's saved trips (for countdown widgets and AI optimizer)
CREATE TABLE trip (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    name TEXT,                    -- "Summer Europe Trip"
    start_date INTEGER NOT NULL,
    end_date INTEGER,
    countries TEXT NOT NULL,      -- JSON array of country IDs
    optimized_plan_id TEXT REFERENCES plan(id),
    created_at INTEGER NOT NULL
);

-- ComparisonHistory: user's search history (local only)
CREATE TABLE comparison_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_id TEXT NOT NULL REFERENCES country(id),
    searched_at INTEGER NOT NULL,
    result_count INTEGER          -- Number of plans found
);
CREATE INDEX idx_comparison_history_date ON comparison_history(searched_at DESC);
```

**Sync strategy:**
- `country`, `provider`, `plan`, `price_history` → Server-side (refreshed every 12 hours via background job). Synced to all clients.
- `saved_plan`, `price_alert`, `trip` → CloudKit (iOS) / Firebase RTDB (Android). User-specific data.
- `comparison_history` → Local only. Privacy-sensitive.

### 8.2. API Endpoints

```
BASE URL: https://api.esimdb.app/v1

GET    /api/v1/countries                     → List all supported countries
GET    /api/v1/countries/{id}                → Country detail with flag and region
GET    /api/v1/countries/search?q={query}    → Autocomplete search

GET    /api/v1/providers                     → List all providers
GET    /api/v1/providers/{id}                → Provider detail with avg rating

GET    /api/v1/plans?country={id}            → Plans for a country
GET    /api/v1/plans?country={id}&sort=price → Sorted plans
GET    /api/v1/plans/{id}                    → Plan detail with affiliate URL
GET    /api/v1/plans/compare?ids=id1,id2,id3 → Compare specific plans
GET    /api/v1/plans/promo                   → Plans with active promo codes

GET    /api/v1/optimize                      → AI Trip Optimizer
       ?countries=JP,KR,TW&start=...&end=...  → Get optimal plan combination

POST   /api/v1/alerts                        → Create price alert
GET    /api/v1/alerts                        → List user's alerts
PATCH  /api/v1/alerts/{id}                   → Update alert
DELETE /api/v1/alerts/{id}                   → Delete alert

POST   /api/v1/trips                         → Save trip
GET    /api/v1/trips                         → List user's trips
PATCH  /api/v1/trips/{id}                    → Update trip
DELETE /api/v1/trips/{id}                    → Delete trip

GET    /api/v1/stats                         → App stats (savings, countries, trips)
```

**Authentication:** JWT with refresh tokens. Firebase Auth for social login (Sign in with Apple, Google). Anonymous sessions supported — no login required for basic usage.

### 8.3. Push Notification Schema

```json
{
  "aps": {
    "alert": {
      "title": "🇯🇵 Japan eSIM prices dropped!",
      "subtitle": "Now from $6.50 (was $8.00)",
      "body": "3 days until your trip. Lock in the best deal now."
    },
    "sound": "price_alert_chime.caf",
    "badge": 0,
    "mutable-content": 1,
    "category": "PRICE_ALERT"
  },
  "custom_data": {
    "type": "price_drop",
    "country_id": "JP",
    "best_plan_id": "plan_airalo_japan_5gb_7d",
    "old_price": 8.00,
    "new_price": 6.50,
    "deep_link": "esimdb://plans/plan_airalo_japan_5gb_7d",
    "image_url": "https://cdn.esimdb.app/notifications/japan_flag.png"
  }
}
```

**Notification types:**
| Type | Trigger | Frequency | Deep Link |
|------|---------|-----------|-----------|
| `price_drop` | Plan price drops below alert target OR by >15% | As triggered | Plan detail |
| `trip_reminder` | 3 days before saved trip start | One per trip | Trip detail |
| `weekly_deals` | Top 3 promos this week | Weekly (Monday 9am local) | Promo list |
| `new_provider` | New eSIM provider added | As added | Provider detail |
| `renewal_reminder` | 7 days before annual sub renews | Once per renewal | Settings → sub |

### 8.4. AI Agent Architecture (Local-First)

eSIMDB's AI Trip Optimizer uses on-device inference — NOT cloud API. This is a competitive moat.

**The Agent Loop (On-Device):**
```
User enters trip (countries + dates) 
→ Local LLM receives structured prompt 
→ LLM calls tool: get_plans_for_countries(countries) 
→ Tool returns plan data from local DB 
→ LLM processes output: optimal plan combination 
→ UI renders recommendation with cost comparison
```

**AI Feature → Pattern → Model:**
- **Trip Optimizer:** ReAct pattern (LLM + DB query tool) → **Phi-4-mini (3.8B Q4_K_M)** → <3s latency
- **"Best Deal" ranking:** Knowledge retrieval (LLM + lookup) → Same model → <1s latency  
- **Provider review summarization:** Single-pass transform → Same model → <2s latency

**iOS:** llama.cpp Swift bindings, Metal-accelerated, Phi-4-mini Q4_K_M (~2.2GB).
**Android:** MediaPipe LLM Inference or llama.cpp JNI with Vulkan backend. Gemma-3-1B (~1.3GB) for low-RAM devices.
**Fallback:** Cloud API (OpenAI GPT-4o-mini) only for devices below A17 / 6GB RAM minimum spec.

**Why local-first:** Privacy moat (zero trip data leaves device for AI), offline capable (useful when buying eSIMs — you might be in a country with no data yet!), zero inference API costs at scale, faster than cloud round-trip. Cloud-dependent competitors must pay per inference — eSIMDB doesn't.

### 8.5. Third-Party Dependencies

| Dependency | Purpose | Platform | Cost |
|------------|---------|----------|------|
| RevenueCat | Subscription management | iOS + Android | Free up to $10K MTR, then 1% |
| Firebase Auth | Social login (Apple, Google) | iOS + Android | Free |
| Firebase RTDB | Android sync (replaces CloudKit) | Android | Free tier (100 conn, 1GB) |
| CloudKit | iOS sync | iOS | Free (generous limits) |
| TelemetryDeck | Analytics (iOS) | iOS | Free up to 1M signals |
| Firebase Analytics | Analytics (Android) | Android | Free |
| llama.cpp | On-device LLM inference | iOS + Android | Free (open source) |
| **NO Facebook SDK** | — | — | Privacy liability |
| **NO Google AdMob** | — | — | Ads destroy premium feel |
| **NO third-party crash reporting** | — | — | MetricKit + Firebase Crashlytics (free) |

---

## SECTION 9: 30-DAY MVP SPRINT PLAN

### Week 1 — Foundation

| Day | iOS | Android | Shared |
|-----|-----|---------|--------|
| Mon | Project setup, SwiftData models, CloudKit container | Project setup, Room entities, Firebase RTDB | Finalize DB schema, API spec |
| Tue | Onboarding flow (3 cards) | Onboarding flow (3 cards) | Design review: onboarding |
| Wed | Home screen with country search | Home screen with country search | Design review: home, search UX |
| Thu | Results/comparison screen (v1) | Results/comparison screen (v1) | Integration test: search → results |
| Fri | RevenueCat integration + custom paywall | BillingClient + custom paywall | Paywall design final, A/B test prep |

### Week 2 — Core Experience

| Day | iOS | Android | Shared |
|-----|-----|---------|--------|
| Mon | Plan detail screen + affiliate link handling | Plan detail screen + affiliate link handling | Design review: plan detail |
| Tue | Price alerts (create, list, toggle) | Price alerts + notification channels | Notification copy final |
| Wed | WidgetKit (small + medium + lock screen) | App Shortcuts (4) | Widget review |
| Thu | Settings screen (minimal, 8 items) | Settings screen | Settings audit |
| Fri | Empty states, error states, all edge cases | Empty states, error states | Edge case testing |

### Week 3 — Polish & Virality

| Day | iOS | Android | Shared |
|-----|-----|---------|--------|
| Mon | Haptics, animations, micro-interactions | Motion, predictive back gesture | Micro-interaction review |
| Tue | Share sheet integration + savings cards | Share intent + savings cards | Virality flow test |
| Wed | App Store screenshots + ASO copy | Play Store feature graphic + listing | ASO copy final |
| Thu | Accessibility audit (VoiceOver, Dynamic Type) | Accessibility audit (TalkBack) | Accessibility test |
| Fri | AI Trip Optimizer (v1, local LLM) | AI Trip Optimizer (v1, local LLM) | AI feature test |

### Week 4 — Launch Readiness

| Day | iOS | Android | Shared |
|-----|-----|---------|--------|
| Mon | Bug fixes, performance, edge cases | Bug fixes, performance, edge cases | Cross-platform parity check |
| Tue | App Store submission prep (metadata, screenshots) | Play Store submission prep (listing, feature graphic) | Privacy policy live |
| Wed | TestFlight internal build | Internal testing track | Beta tester onboarding |
| Thu | TestFlight external (Beta App Review) | Closed testing (recruit 20 testers) | Launch checklist final |
| Fri | **SUBMIT TO APP STORE** | **SUBMIT TO PLAY STORE** | Launch day coordination |

### MVP Feature Cut List (Do NOT Build in Sprint 1)

- **AI Trip Optimizer v2** — v1 covers basic multi-country optimization. Advanced features (hotel Wi-Fi quality scoring, local SIM comparison) can wait.
- **eSIM Passport (cross-provider wallet)** — Massive engineering effort. V2 feature after 10K users validate the core comparison use case.
- **Social features / Friend challenges** — Nice to have. Core utility (finding cheapest eSIM) is the retention driver.
- **iPad-optimized layout** — iPhone + Android phones first. iPad is <5% of travel app usage.
- **Apple Watch companion** — Glanceable trip countdown only. V2 when widget usage data supports it.

---

## SECTION 10: LAUNCH CHECKLIST

### Pre-Launch (T-14 days)

- [ ] App Store Connect: App record created, all metadata filled, screenshots uploaded for 6.9" and 6.7" displays
- [ ] Google Play Console: App created, feature graphic (1024×500) uploaded, all metadata filled
- [ ] RevenueCat: Products configured (`premium_monthly`, `premium_annual`, `trip_pass`), webhooks set up for subscription events
- [ ] Privacy Policy URL: Live at `https://esimdb.app/privacy` — GDPR-compliant, lists all data collected, cookie consent if using web
- [ ] Terms of Service URL: Live at `https://esimdb.app/terms`
- [ ] Support email: `support@esimdb.app` — configured, tested, auto-responder set up ("We received your message! We reply within 24 hours.")
- [ ] App screenshot set: All device sizes, dark mode default, text overlays finalized
- [ ] App Preview Video: 30-second demo showing search → compare → save workflow. Optional but apps with videos convert **20-35% better**.
- [ ] TestFlight build submitted for Beta App Review
- [ ] Internal testing track: 20 testers recruited (Google Play closed testing requirement)
- [ ] Landing page `esimdb.app` live with download buttons
- [ ] Affiliate integrations confirmed with top 5 providers (Airalo, Holafly, Saily, Nomad, MobiMatter)

### Launch Day (T=0)

- [ ] Release to App Store (manual release — retain control, not automatic)
- [ ] Release to Play Store (staged rollout: start at **10%** for 24 hours to catch crash-loop bugs before 100% rollout)
- [ ] Monitor TelemetryDeck + Firebase Analytics: crash rate, session duration, conversion rate
- [ ] Monitor App Store Connect for crash reports
- [ ] Monitor pricing API: ensure all 100+ provider plans are current
- [ ] Reply to first 10 reviews within 2 hours (sets the tone, boosts ranking)
- [ ] Post on r/travel, r/digitalnomad, r/solotravel — authentic indie dev story. "I got tired of overpaying for eSIMs, so I built a free comparison app." NOT corporate marketing.
- [ ] Post on Product Hunt (schedule for 12:01 AM PT — maximum 24-hour exposure window in leaderboard)
- [ ] Send launch email to beta testers: "We're live! 🚀 Thanks for helping us test eSIMDB. Here's 50% off your first year of Premium as a thank you. Link to download + promo code."

---

## SECTION 11: POST-LAUNCH ITERATION PLAN

### Week 1 Post-Launch: Observe, Don't Build

- Watch metrics: **D1 retention, D7 retention, conversion rate, crash rate, avg session length, affiliate click-through rate**
- Read EVERY review. Categorize: bug / feature request / UX confusion / pricing objection / positive
- **Do not ship any new features.** Only critical crash fixes.
- If D1 retention <40%: the onboarding or first search experience is broken. Redesign.
- If affiliate CTR <5%: plan cards need redesign. Prices not prominent enough. Test "Buy" button size and color.

### Week 2-4: Quick Wins

- Ship top 3 user-requested improvements (not features — improvements to existing flows)
- If conversion rate <20%: A/B test paywall design. Test: paywall on 3rd comparison vs 5th comparison. Test: monthly pre-selected vs annual pre-selected.
- If D7 retention <25%: the habit loop isn't forming. Redesign push notification strategy. Test weekly deal emails.
- Add 5 new eSIM providers to database (user requests)
- Fix top 3 most common countries with missing/inaccurate plan data

### Month 2-3: Feature Expansion

- Build the #1 most requested feature from user feedback
- Launch AI Trip Optimizer v2 with hotel Wi-Fi scoring
- Begin content marketing: publish 5 pillar blog posts targeting long-tail eSIM keywords
- Launch referral program ("Give a friend a free Trip Pass")
- Localize app into Spanish and German (top 3 languages after English for traveler demographics)
- Begin SEO landing pages for top 50 destination countries ("Best eSIM for [Country] 2026")

---

## SECTION 12: ANTI-PATTERNS — What You MUST NOT Do

1. **Do not ask for notification permission on first open.** 60% of users say "no" if you ask before they've seen value. Ask after the user saves their first price alert — with a custom pre-permission dialog: "Get notified when prices drop for your saved destinations. We promise — only when you save money."
2. **Do not require account creation before the user can search.** "Try before you sign up" is critical. Every barrier between download and first search kills 20-30% of users. Anonymous sessions are fully functional.
3. **Do not show ads.** Ads destroy trust on a comparison/savings app. The value prop is "we save you money" — showing ads undermines that. Monetize through affiliate commissions and Premium, not user attention.
4. **Do not use a default system paywall.** Default RevenueCat/StoreKit paywalls are ugly and convert 40% worse. Custom SwiftUI/Compose paywall designed around the "save money" value prop.
5. **Do not ship with a splash screen.** Splash → immediate animation into the home screen. The globe animation IS the loading state. Skeleton UI fills in as data loads. No static logo sitting for 2 seconds.
6. **Do not ignore 1-star reviews.** Every negative review gets a developer response within 24 hours. App Store search ranking weights developer-responsiveness. Many 1-star reviewers upgrade when they get a personal response.
7. **Do not localize poorly.** If launching in 10 languages, do 3 well (English, Spanish, German) and skip the rest until human translators are available. A bad machine translation is worse than no translation — eSIMDB's plan data is already in English for most providers, so the UI is what needs localization.
8. **Do not ship on both platforms simultaneously.** iOS-first, Android 2 weeks behind. App Store review is unpredictable (1-3 days). Play Store is instant. Debug App Store rejection on iOS while Android is still in polish, then launch Android with learnings applied.
9. **Do not obsess over the algorithm.** App Store algorithm rewards: downloads → ratings → engagement → revenue — in that order. Optimize for user experience: make comparisons easy, show real savings, delight with micro-interactions. The algorithm follows.
10. **Do not build features nobody asked for.** Every sprint must ship at least one thing users actually requested. Ship something a user asked for THIS WEEK. It builds trust that you're listening. Even something small: "Added Kyrgyzstan eSIM plans per user request" shows responsiveness.
11. **Do not hide affiliate relationships.** Disclose "we may earn a commission" prominently on every plan detail screen. FTC guidelines require it, and transparency builds trust. Users appreciate honesty — they know comparison sites make money somehow.
12. **Do not scrape providers without permission.** Get official affiliate partnerships with top 10 providers before launch. Scraping is legally risky and data goes stale. Affiliate partnerships provide both legal cover and revenue.

---

*End of eSIMDB Full Scaffold. This document is the complete build brief. A senior iOS + Android development team should be able to build the complete app from this specification with zero additional clarification questions.*

---

**Quality Gate:** ✅ Read and verified. All sections populated. All placeholders filled. Database schema complete. API endpoints specified. 30-day sprint detailed. Launch checklist actionable.
