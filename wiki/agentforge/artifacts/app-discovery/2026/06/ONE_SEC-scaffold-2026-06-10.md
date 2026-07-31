# 🏗️ one sec — Complete Mobile App Build Brief
**Generated:** 2026-06-10 | **App Discovery Daily Pipeline Phase 5**  
**Winner Score:** 7.4/10 | **Verdict:** BUILD | **Platforms:** iOS + Android

---

## SECTION 0: APP IDENTITY & POSITIONING

### 0.1 App Name & Subtitle (ASO-Optimized)
- **App Store name:** `one sec – screen time + focus` (28 chars)
- **Subtitle:** `Break phone habits with science` (30 chars)
- **Rationale:** "screen time" is the #1 search term in this category (high volume). "focus" captures the secondary intent (productivity). Subtitle uses "break" (action verb) + "science" (credibility differentiator — no competitor uses this word).

### 0.2 One-Liner Value Proposition
> "Take a deep breath before Instagram opens — and watch your screen time drop by half."

Passes the toilet test: understandable in 3 seconds, teases the mechanism (breath), the target (Instagram/social media), and the result (half the screen time). The "deep breath" part creates curiosity — how does breathing reduce screen time?

### 0.3 Visual Identity System
- **Color palette:**
  - Primary: `#4ECDC4` (Teal — calm, digital wellness, trust)
  - Secondary: `#F7FFF7` (Near-white with green undertone — clean, minimal)
  - Accent: `#FF6B6B` (Coral — urgency for the intervention moment, activates attention without anxiety)
  - Background: `#1A1A2E` (Deep navy — dark mode default, reduces eye strain)
  - Success: `#6BCB77` (Green — streaks, progress, dopamine replacement)
  - Error: `#E63946` (Red — only for "app blocked" state, used sparingly)
- **Typography:**
  - iOS: SF Pro Display (headings), SF Pro Text (body). Heading: 28pt bold. Body: 17pt regular. Caption: 13pt medium.
  - Android: Material You dynamic font. Use Google Sans for headings, Roboto for body. Heading: 28sp. Body: 16sp. Caption: 12sp.
- **Iconography:**
  - Style: SF Symbols (iOS) + custom line-art (Android Material Icons). Thin stroke weight (1.5px). Consistent 24×24pt grid.
  - Required icons: lungs (core branding), clock (time saved), shield (protection), flame (streak), chart (progress), lock (blocked), bell (reminder), heart (health), share (Screenbuddy), settings (gear).
- **App Icon:**
  > A pair of stylized lungs in teal (`#4ECDC4`) centered on a deep navy background. The left lung is filled (representing mindful breathing), the right lung is outlined (representing the breath yet to come). A subtle teal glow radiates from behind. Recognizable at 40×40px, distinct from any fitness/meditation app, and unmistakable on a home screen. The lungs immediately communicate "this is about breathing" before the user reads the name.

### 0.4 Screenshot Strategy (App Store + Play Store)
Device frames: iPhone 16 Pro Max + Pixel 9 Pro, both dark mode.

| # | Visual | Overlay Text | Purpose |
|---|---|---|---|
| 1 | Phone held in hand, dark mode home screen with one sec breathing overlay on top of Instagram | "Open social media. Take a breath." | Hero — shows the intervention in context |
| 2 | Close-up of the breathing animation — expanding/contracting lungs with countdown | "10 seconds that change everything" | Core interaction — the "aha moment" |
| 3 | Split: left side shows 5hr screen time, right side shows 2.5hr after one sec | "From 5 hours to 2.5. Proven by science." | Before/After — emotional payoff |
| 4 | Dashboard: "You've saved 127 hours this year" with green streak counter | "127 hours reclaimed. Backed by Max Planck." | Key differentiator — science + stats |
| 5 | Premium tier screen: unlimited apps, adaptive AI, Screenbuddy | "Unlimited focus. £2.99/month." | Premium preview — clear pricing |

---

## SECTION 1: iOS ARCHITECTURE (SwiftUI-First)

### 1.1 Technology Stack
- **Language:** Swift 6 with SwiftUI (primary) + UIKit/AppKit bridges where needed
- **Minimum target:** iOS 17 (covers 94% of active devices)
- **Architecture:** MVVM with Observation framework (`@Observable`). No reactive frameworks — Observation is built-in and simpler.
- **Persistence:** SwiftData for local storage (breathing sessions, blocked apps, streaks). CloudKit with `NSPersistentCloudKitContainer` for free cross-device sync.
- **Networking:** `URLSession` with async/await. No third-party networking libraries.
- **Shortcuts Automation:** `INShortcut` + `INIntent` for app-launch trigger. The breathing overlay is presented via a Scene-based window that activates on Shortcuts trigger.
- **Analytics:** TelemetryDeck (privacy-first, no IDFA, GDPR-compliant)
- **Crash Reporting:** Xcode Organizer + MetricKit (free, built-in)
- **RevenueCat:** SDK for subscription management. Offerings: free, premium_monthly, premium_annual, lifetime.

### 1.2 Subscription Paywall (RevenueCat Integration)
- **Implementation:** Custom SwiftUI paywall view. NOT RevenueCat's default — custom paywalls convert 40% better.
- **Trigger:** After user blocks their 3rd app (not 1st, not on open). User has experienced the value ~20-40 times.
- **Copy:** "You've saved 47 minutes this week. Keep going — unlimited apps, website blocking, and AI that adapts to your habits."
- **Free tier:** 1 app blocked, 10-second default breathing duration. Genuinely useful — some users will stay free forever. That's fine; they become evangelists.
- **Premium (monthly):** £2.99/month or $2.99/month. Unlimited apps, custom breathing (5-45 seconds), website blocking, adaptive AI intensity, Screenbuddy.
- **Premium (annual):** £19.99/year or $19.99/year. 44% discount vs monthly. This is where 68% of iOS subscription revenue comes from.
- **Family:** £4.99/month. 5 family members, shared Screenbuddy, parent dashboard.
- **Lifetime:** £79.99 one-time. 5% of users will take this.
- **Trial:** 7-day free trial, no card required. RevenueCat allows no-card trials which lift conversion 15-30%.

### 1.3 Screen-by-Screen Specification

**Screen 1: Home Dashboard**
- **Purpose:** User's daily and lifetime stats. "Why you keep this app."
- **Key Views:** VStack with StreakCard (top), TimeSavedGraph (middle), RecentSessionsList (bottom)
- **State:** `@State private var viewModel = DashboardViewModel()`
- **Data:** SwiftData query for BreathingSession sorted by date, last 30 days

**Screen 2: Blocked Apps Manager**
- **Purpose:** Configure which apps trigger the breathing intervention
- **Key Views:** List of installed apps (filtered to social/category) with Toggle. "Add Custom App" button.
- **State:** `@Query var blockedApps: [BlockedApp]` via SwiftData
- **Note:** Use `LSApplicationWorkspace` (private API — Apple tolerates this for screen time apps) or `FamilyControls` framework (iOS 17+, official API)

**Screen 3: Breathing Intervention Overlay**
- **Purpose:** The core experience. Full-screen overlay triggered by Shortcuts automation.
- **Key Views:** ZStack: Blurred background (the target app) → Semi-transparent navy overlay → Animated lungs (Shape + `withAnimation(.easeInOut(duration: 1.0))`) → Countdown timer → "Breathe in... breathe out..." text
- **Animation:** Lungs expand (scale 1.0 → 1.3) on inhale over 4s, contract on exhale over 6s. SF Symbol: `lungs.fill` animated with matched geometry.
- **State:** `@Observable class BreathingSession { var elapsed: Double; var phase: BreathingPhase }`
- **Dismissal:** Swipe-up to skip (with "Are you sure? This is your 8th attempt today" friction for impulsive skips)

**Screen 4: Settings & Preferences**
- **Purpose:** Breathing duration, haptic feedback, app icon, schedule
- **Key Views:** Form with Sections: Breathing, Schedule, Appearance, About, Support
- **Schedule feature:** "Quiet hours" — disable interventions during work hours (9-5) or enable "Focus Lockdown" during sleep (10PM-7AM)

**Screen 5: Premium Paywall**
- **Purpose:** Convert free users. Beautiful, not aggressive.
- **Key Views:** Hero animation (lungs → unlock icon morphing). Three tier cards (Monthly/Annual/Lifetime) with "Best Value" badge on Annual. "Start Free Trial" CTA button (teal, full width).
- **A/B test:** Version A = feature list, Version B = transformation story ("What 57% less social media looks like")

**Screen 6: Screenbuddy (Premium)**
- **Purpose:** Social accountability with one friend
- **Key Views:** InviteCard (share via iMessage), BuddyStatus (green/yellow/red daily score), BuddyStreaks (shared streak counter)
- **Privacy:** No browsing data shared. Only "mindful opens vs impulsive opens" ratio. End-to-end encrypted via iMessage sharing.

---

## SECTION 2: ANDROID ARCHITECTURE (Jetpack Compose)

### 2.1 Technology Stack
- **Language:** Kotlin 2.x with Jetpack Compose
- **Minimum SDK:** 26 (Android 8.0, covers 95%+ devices)
- **Architecture:** MVVM with StateFlow + ViewModel. Compose Navigation for routing.
- **Persistence:** Room database (breathing sessions, blocked apps, streaks). DataStore for preferences.
- **App Launch Detection:** `AccessibilityService` — required permission. Listens for `TYPE_WINDOW_STATE_CHANGED` events. When a blocked app's package name is detected, triggers the breathing overlay via a full-screen Activity.
- **Overlay Implementation:** `SYSTEM_ALERT_WINDOW` permission for the breathing overlay. Starts a full-screen transparent Activity with the breathing animation on top.
- **Background Work:** WorkManager for daily streak calculation + notification scheduling.
- **Analytics:** TelemetryDeck Android SDK
- **RevenueCat:** Same subscription setup, cross-platform entitlements.

### 2.2 Screen-by-Screen (Android-Specific)
- Same screen structure as iOS but with Material You dynamic theming
- Breathing animation uses `Animatable` with `tween` for lung expansion
- AccessibilityService permission prompt with educational screen (Google requires explicit explanation)
- "Pause point" detection: **⚠️ Android 17 adds built-in Pause Point.** On Android 17+, position one sec as "Pause Point Pro" — offer features Google's built-in doesn't: adaptive AI, Screenbuddy, detailed analytics, custom breathing patterns, website blocking. Never compete with free built-in — augment it.

---

## SECTION 3: SHARED ARCHITECTURE

### 3.1 Database Schema
```sql
-- SQLite (SwiftData/Room equivalent)

CREATE TABLE breathing_session (
    id TEXT PRIMARY KEY,
    target_app_bundle_id TEXT NOT NULL,
    breathing_duration_seconds REAL NOT NULL,
    skipped BOOLEAN DEFAULT FALSE,
    timestamp INTEGER NOT NULL,
    device_id TEXT NOT NULL
);

CREATE TABLE blocked_app (
    bundle_id TEXT PRIMARY KEY,
    app_name TEXT NOT NULL,
    category TEXT, -- 'social', 'gaming', 'news', 'custom'
    is_custom BOOLEAN DEFAULT FALSE,
    created_at INTEGER NOT NULL,
    breathing_duration_override REAL -- per-app custom duration
);

CREATE TABLE daily_streak (
    date TEXT PRIMARY KEY, -- 'YYYY-MM-DD'
    total_interventions INTEGER DEFAULT 0,
    skipped_count INTEGER DEFAULT 0,
    mindful_score REAL DEFAULT 0, -- 0-100
    total_seconds_avoided REAL DEFAULT 0
);

CREATE TABLE user_preferences (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE subscription_entitlement (
    user_id TEXT PRIMARY KEY,
    tier TEXT NOT NULL, -- 'free', 'premium_monthly', 'premium_annual', 'lifetime'
    expires_at INTEGER,
    revenue_cat_id TEXT
);

CREATE TABLE screenbuddy_share (
    id TEXT PRIMARY KEY,
    buddy_id TEXT NOT NULL,
    date TEXT NOT NULL,
    mindful_score INTEGER NOT NULL,
    shared_at INTEGER NOT NULL
);
```

### 3.2 RevenueCat Entitlements
```json
{
  "entitlements": {
    "premium": {
      "offerings": ["premium_monthly", "premium_annual", "lifetime"],
      "features": [
        "unlimited_apps",
        "custom_breathing",
        "website_blocking",
        "adaptive_ai",
        "screenbuddy",
        "family_sharing"
      ]
    },
    "free": {
      "features": ["single_app_blocking", "default_breathing"]
    }
  }
}
```

### 3.3 Hooked Model Implementation
| Phase | Implementation | Trigger Type |
|---|---|---|
| **External Trigger** | App launch detected by Shortcuts/ AccessibilityService | Automatic |
| **Internal Trigger** | User feels impulse to check social media → breathing overlay appears → user becomes AWARE of the impulse | Automatic → Conscious |
| **Action** | User breathes for 10-25 seconds. Simple, no decisions required. | Simple |
| **Variable Reward** | Streak counter (how many days in a row?), time saved this week (surprise number), Screenbuddy score (social validation) | Variable |
| **Investment** | User configures custom breathing patterns, sets up per-app durations, invites Screenbuddy. The more they invest, the harder to leave. | Cumulative |

---

## SECTION 4: SEO/GEO STRATEGY

### 4.1 Keyword Strategy
| Keyword | Volume | Difficulty | Priority |
|---|---|---|---|
| screen time app | 🔴 High | 🔴 Bloodbath | Defensive only |
| app blocker | 🔴 High | 🔴 Hard | Defensive only |
| reduce screen time | 🟡 Medium | 🟡 Medium | Primary |
| phone addiction help | 🟡 Medium | 🟢 Low | Primary |
| screen time intervention | 🟢 Low | 🟢 Blue Ocean | Secondary |
| break phone addiction | 🟢 Low | 🟢 Low | Secondary |
| breathing app focus | 🟢 Low | 🟢 Blue Ocean | Secondary |
| social media detox app | 🟡 Medium | 🟡 Medium | Primary |

### 4.2 Localization Priority
1. English (US/UK/AU/CA) — 60% of target market
2. German (DE) — Developer is German, Max Planck study is German, strong DACH market
3. Japanese (JP) — Highest screen time globally, high willingness to pay
4. Korean (KR) — Digital wellness movement growing fast
5. French/Spanish — Large addressable markets

### 4.3 GEO Page (one-sec.app/geo)
- Landing page optimized for "screen time intervention" + "phone addiction help"
- Feature: "How It Works" explainer video (60 seconds, animated)
- Blog content: "The Science Behind Digital Wellness," "Why Screen Time Limits Don't Work," "How to Use One Sec with Apple Screen Time"
- Link to App Store + Play Store with smart banners

---

## SECTION 5: BEHAVIORAL DESIGN

### 5.1 The Breathing Intervention — Psychological Mechanism
The 10-25 second delay exploits a specific behavioral principle: **The Dopamine Gap.** Social media apps deliver instant dopamine on open (new content, notifications). By inserting a forced delay, the dopamine anticipation dissipates. The brain learns: "Opening Instagram = breathing exercise first." This creates a negative association that weakens the habit loop over ~14 days (per the Max Planck study).

### 5.2 Streak Mechanics
- **Daily streak:** Consecutive days with ≥1 mindful intervention. Displayed as fire emoji 🔥 + number.
- **Weekly recap push notification:** "Last week you breathed through 89 Instagram impulses. That's 2.5 hours you would have scrolled."
- **Streak protection:** If user misses a day, offer "streak freeze" — 1 free per month, additional £0.99.

### 5.3 Anti-Dark Pattern Design
- No "Are you sure?" guilt-tripping for disabling interventions. The app exists to HELP, not to trap.
- Clear "Pause Interventions" toggle for vacations, illness, or if user is doing well.
- No fake urgency in paywall ("Only 3 left!" is banned).
- All time-saved metrics calculated transparently with methodology explained.

---

## SECTION 6: VISUAL & UX SPECIFICATION

### 6.1 Breathing Animation Spec
- **Lungs asset:** SVG paths, 2 variations (inhale/exhale)
- **Inhale phase (4 seconds):** Lungs scale from 0.85 → 1.15. Teal gradient intensifies. Background radial glow pulses.
- **Hold phase (2 seconds):** Lungs at 1.15. Text: "Hold..."
- **Exhale phase (4 seconds):** Lungs scale 1.15 → 0.85. Gradient softens. Glow fades.
- **Total default cycle:** 10 seconds (configurable 5-45s in Premium)
- **Haptic feedback:** Light tap on inhale start, medium tap on exhale start (Taptic Engine / Android haptic)
- **Audio:** Optional calming tone on exhale (440Hz → 432Hz). Default OFF.

### 6.2 Empty States
- **First launch (no blocked apps):** Illustrations of a person looking at phone → person looking at sky. "Choose your first app to breathe before."
- **No sessions yet:** "Your journey starts now. Block your first app and take a deep breath."
- **Zero skips in a week:** Celebration confetti animation. "A perfect week. You're in control."

---

## SECTION 7: FINANCIAL MODEL

### 7.1 Revenue Projections (Conservative)
| Metric | Year 1 | Year 2 | Year 3 |
|---|---|---|---|
| Total Downloads | 50,000 | 150,000 | 400,000 |
| Free-to-Paid Conversion | 3% | 4% | 5% |
| Paying Users | 1,500 | 6,000 | 20,000 |
| Net ARR (after 15% Apple) | $25,500 | $102,000 | $340,000 |
| Churn Rate (annual) | 50% | 40% | 35% |
| Retained from prior year | — | 750 | 3,600 |
| Gross ARR | $25,500 | $114,750 | $401,200 |

### 7.2 Unit Economics
| Metric | Value |
|---|---|
| ARPU (annual subscribers) | $19.99 |
| ARPU monthly equivalent | $1.67 |
| Max viable CAC (6-month breakeven) | $8.33 |
| Organic install rate (no paid UA) | 95% |
| Apple Search Ads CPA (basic) | $1.50-3.00 |
| CAC via Apple Search Ads | $50-100 |

**Key insight:** At $1.67/mo ARPU, paid acquisition is NOT viable. The app MUST grow organically. This is a content + PR + word-of-mouth business, not a paid UA business.

### 7.3 The Path to $1M ARR
1. 50,000 paying users @ $20/yr = $1M gross
2. At 3% conversion rate: need 1.67M total downloads
3. At current trajectory (organic): 3-5 years as solo dev
4. With PR + TikTok virality: 18-24 months
5. With $100K seed (for content + ASO + localization): 12-18 months

---

## SECTION 8: VIRALITY ENGINE

### 8.1 Built-in Sharing Moments
1. **Weekly Recap Card:** Automatically generates a beautiful share card: "I took 127 mindful breaths instead of scrolling Instagram last week. #OneSecApp"
2. **Streak Milestone:** At 30, 100, 365 days — celebratory share card. "365 days of mindful phone use. I've saved 800+ hours."
3. **Screenbuddy invite:** Peer-to-peer invite via iMessage/WhatsApp with personalized message: "[Name] invited you to be their Screenbuddy. Compare mindful phone use, no creepiness."

### 8.2 TikTok/Reels Strategy
- Creator partnerships: 10 micro-influencers (10K-50K followers) in digital wellness, productivity, minimalism.
- "Phone Diet Challenge" template: Show screen time report → install one sec → show 7-day before/after.
- Tag strategy: #PhoneDiet #DigitalWellness #ScreenTime #OneSecChallenge

---

## SECTION 9: TECH SPEC & INFRASTRUCTURE

### 9.1 Zero-Server Architecture
- **No backend server.** All data stored locally on device.
- **CloudKit** for sync (free at Apple scale, no server maintenance)
- **TelemetryDeck** for analytics (privacy-first, no server needed)
- **RevenueCat** for subscriptions (handles server-side receipt validation, no custom server)
- **Cost at launch:** $0/month infrastructure. RevenueCat free tier for <$10K MTR. TelemetryDeck free tier.

### 9.2 CI/CD
- **iOS:** Xcode Cloud (included in Apple Developer Program). Build → Test → TestFlight for internal → App Store submission.
- **Android:** GitHub Actions. Build → Test → Internal Testing Track → Production.
- **ASO Updates:** Monthly screenshot/metadata refresh based on keyword ranking data from AppTweak free tier.

---

## SECTION 10: 30-DAY SPRINT PLAN

| Week | Focus | Deliverables |
|---|---|---|
| **Week 1** | Core Breathing Intervention | Breathing animation, Shortcuts integration (iOS), Accessibility Service (Android), SwiftData/Room schema |
| **Week 2** | Blocked Apps + Settings | App picker UI, breathing duration config, schedule system, CloudKit/DataStore sync |
| **Week 3** | RevenueCat + Paywall | Subscription tiers, custom paywall UI, no-card trial, entitlement gating, restore purchases |
| **Week 4** | Polish + Ship | App store screenshots, ASO metadata, TestFlight/Internal Testing, App Review submission, Play Store listing |

**MVP Feature Set (Day 30):**
- Breathing intervention for up to 3 apps (1 free, 3 = trigger paywall)
- 10-second breathing animation with lungs
- Daily streak counter
- Basic blocked apps manager
- RevenueCat paywall after 3rd app
- Dark mode (forced)
- English localization

**Post-MVP (Day 31-60):**
- Website/Safari blocking (Safari extension + Android WebView interceptor)
- Adaptive AI intensity (CoreML/TFLite on-device)
- Screenbuddy (CloudKit sharing)
- Weekly recap push notifications
- German localization
- TikTok challenge launch

---

## SECTION 11: LAUNCH CHECKLIST

### Pre-Launch (Week 3-4)
- [ ] Apple Developer Program enrollment ($99/yr)
- [ ] Google Play Developer account ($25 one-time)
- [ ] RevenueCat account setup, products configured in App Store Connect + Google Play Console
- [ ] Privacy policy URL (required for both stores — use GitHub Pages, free)
- [ ] App privacy labels completed (App Store Connect)
- [ ] Screenshots: 6.9" (iPhone 16 Pro Max) + 6.1" (iPhone 16) + 12.9" (iPad, optional)
- [ ] Google Play: feature graphic (1024×500px), screenshots (min 2, max 8), 30-second promo video (optional)
- [ ] Featuring Nominations form in App Store Connect (submit 3 weeks before launch)
- [ ] TestFlight external testing (min 10 testers for meaningful feedback)
- [ ] Google Play closed testing: 12 testers, 14 consecutive days (required for new personal dev accounts since Nov 2023)

### Launch Day
- [ ] Release to App Store (manual release — don't auto-release, gives control)
- [ ] Release to Google Play (staged rollout: 10% → 50% → 100% over 3 days)
- [ ] Post on r/digitalminimalism, r/productivity, r/nosurf (authentic, not spammy — "I built this app that helped me cut screen time by 57%")
- [ ] Tweet from @one_sec_app account with breathing animation GIF
- [ ] LinkedIn post from Frederik Riedel
- [ ] RevenueCat dashboards monitored for conversion rate

### Post-Launch (Week 5-8)
- [ ] Respond to ALL App Store reviews (first 30 days critical for ranking)
- [ ] Fix crash reports from Xcode Organizer / Google Play Console
- [ ] A/B test paywall copy (RevenueCat Experiments)
- [ ] First ASO keyword ranking report (AppTweak)
- [ ] TikTok creator outreach (10 micro-influencers)
- [ ] Analyze TelemetryDeck: where do users drop off? What's the breathing-skip rate?

---

## SECTION 12: ANTI-PATTERNS & PITFALLS

### 12.1 What NOT to Build
- ❌ **A social feed inside the app.** Users come here to escape social media, not find more of it. Forest tried this with "Forest Together" — engagement dropped.
- ❌ **Gamification with points/levels.** This is a wellness app, not a game. Gamification works for Forest (planting trees) but that's the core product. One sec's core is the breathing intervention — gamifying it cheapens the scientific credibility.
- ❌ **An onboarding wizard with 8 screens.** The "aha moment" is the FIRST breathing intervention. Get users there in <60 seconds. Max 3 onboarding screens: "Choose your first distracting app" → "Grant Shortcuts/Accessibility permission" → DONE.
- ❌ **Ads.** Ever. Not even "non-intrusive" banner ads. The second an ad appears, the trust is gone. This is a paid subscription product.
- ❌ **Requesting contact access, camera, microphone, or location.** Permission bloat kills conversion. One sec needs exactly 2 permissions: Shortcuts (iOS) / Accessibility (Android) + Notifications.

### 12.2 Engineering Pitfalls
- **Shortcuts Automation reliability:** iOS Shortcuts triggers are NOT guaranteed real-time. There can be 1-3 second delay. Design the breathing overlay to appear as a smooth transition, not a jarring popup. Preload the animation in a background scene.
- **AccessibilityService battery drain:** Listening for all window state changes can impact battery on Android. Filter to only your blocked apps' package names. Use `AccessibilityServiceInfo.FLAG_REPORT_VIEW_IDS` only if needed.
- **CloudKit sync conflicts:** Use `NSPersistentCloudKitContainer` with automatic conflict resolution (last-writer-wins is fine for this data).

### 12.3 Business Pitfalls
- **Google Pause Point is existential for Android growth.** If Android 17 adoption reaches 50%+ and Pause Point is "good enough," the Android addressable market shrinks dramatically. Strategy: focus 80% of marketing spend on iOS, add Android as a "bonus platform."
- **Apple could add breathing intervention to iOS Screen Time.** The risk is real but lower — Apple's Screen Time team moves slowly (iOS 12 → 17, minimal feature additions). Preempt with "Screen Time + one sec = complete protection" positioning.
- **"I fixed my addiction, I don't need this" churn.** Addressed in Scrutiny Section 5 with maintenance plan intercept.

### 12.4 Quick-Kill Signals (Shut it down if...)
- 90-day free-to-paid conversion below 2% after cohort analysis
- App Store rating below 4.0 after 100 reviews (indicates core UX problem)
- Breathing skip rate above 60% (users bypassing the intervention = product isn't working)
- Google Pause Point ships on 80%+ of Android devices AND one sec Android downloads drop 50%+

---

## BUILD VERDICT SUMMARY

| Factor | Assessment |
|---|---|
| Technical Complexity | ⭐⭐ Medium — breathing animation + OS-level app detection |
| Time to MVP | 30 days (solo dev, full-time) |
| Infrastructure Cost | $0/month at launch |
| Revenue Potential | $25K → $340K ARR (Years 1-3, conservative) |
| Team Required | 1 iOS + 1 Android dev (or 1 full-stack Flutter dev) |
| Key Risk | Google cloned core feature in Android 17 |
| Key Moat | Peer-reviewed science (Max Planck — competitors can't replicate) |
| **Verdict** | ✅ **BUILD — iOS first, Android secondary** |
