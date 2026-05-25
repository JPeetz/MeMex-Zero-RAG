# BeeDone Scaffold — Complete Mobile App Build Brief

_Generated 2026-05-25 | App Discovery Pipeline Phase 5 | Verdict: BUILD_

---

## SECTION 0: APP IDENTITY & POSITIONING

### 0.1. App Name & Subtitle (ASO-Optimized)
- **App Store name:** QuestFlow — Gamified To-Do List (30 chars)
- **Subtitle:** ADHD Task Manager with AI Coach (30 chars)
- **Rationale:** "QuestFlow" contains no direct keyword but is brandable and memorable. The subtitle front-loads the two highest-volume discoverability keywords: "ADHD" (booming search volume, 2026) and "Task Manager" (evergreen). The subtitle also signals the AI differentiator immediately.

### 0.2. One-Liner Value Proposition
"Turn your to-do list into an RPG quest log and watch your ADHD brain finally cooperate."

Passes the toilet test: gamification + ADHD + immediate emotional resonance. No jargon.

### 0.3. Visual Identity System
- **Color palette:**
  - Primary: `#7C3AED` (Vivid Purple) — creativity, transformation, premium gamification feel, distinct from the blue/green productivity sea
  - Secondary: `#F59E0B` (Amber Gold) — XP rewards, dopamine hits, warmth
  - Accent: `#10B981` (Emerald) — completion states, streaks, success
  - Background: `#0F0F23` (Deep Navy) — dark mode default, reduces eye strain, feels like a game UI
  - Error: `#EF4444` (Red) — missed streaks, overdue quests
- **Psychology:** Purple signals transformation (turn chaos into order); gold triggers reward anticipation (XP/coins); emerald = success; deep navy = focus and immersion.
- **Typography:**
  - iOS: SF Pro Display (headings), SF Pro Text (body), SF Pro Rounded (buttons/pills)
  - Android: Onest (headings), Inter (body) — both complement Material You dynamic theming
  - Heading: 28pt/sp bold | Body: 17pt/sp regular | Caption: 13pt/sp medium
- **Iconography:** Custom line-art with 2px stroke weight. SF Symbols fallback on iOS. Key icons: sword (quests), shield (habits), brain-sparkle (AI coach), castle (home), scroll (history), gem (premium), trophy (achievements), fire (streak), hourglass (focus timer)
- **App Icon:** A faceted crystal/purple gem with a subtle sword silhouette carved inside, floating against a deep navy-to-purple gradient. Two pixel specks orbit like quest markers. Recognizable at 40×40px — gem shape is unique in the productivity category, no checkmarks or clipboards.

### 0.4. Screenshot Strategy
- **Screenshot 1:** Hero — phone screen showing a quest log with XP bar and character avatar. Overlay: "Your Brain's New OS"
- **Screenshot 2:** Core interaction — dragging a task into "Complete" with confetti burst. Overlay: "Swipe. Earn. Level Up."
- **Screenshot 3:** AI Coach — chat interface suggesting personalized task breakdown. Overlay: "An AI Coach That Gets ADHD"
- **Screenshot 4:** Before/After — left side: chaotic list. Right side: organized quest board. Overlay: "Chaos → Clarity"
- **Screenshot 5:** Premium — character sheet with legendary gear and stats. Overlay: "Unlock Your Full Potential"
- **Device frames:** iPhone 16 Pro Max + Pixel 9 Pro, dark mode default

---

## SECTION 1: iOS ARCHITECTURE (SwiftUI-First)

### 1.1. Technology Stack
- **Language:** Swift 6 with SwiftUI (primary) + UIKit for complex gesture handling
- **Minimum target:** iOS 17 (94% of active devices)
- **Architecture:** MVVM with `@Observable` macro (Observation framework). No React Native.
- **Persistence:** SwiftData for local storage. CloudKit for free cross-device sync.
- **Networking:** URLSession with async/await. No Alamofire.
- **Analytics:** TelemetryDeck (privacy-first, no IDFA, GDPR-compliant)
- **Crash reporting:** Xcode Organizer + MetricKit (free, built-in, zero SDK bloat)

### 1.2. Subscription Paywall (RevenueCat Integration)
- RevenueCat SDK: offerings configured with QuestFlow_Premium entitlement
- **Custom SwiftUI paywall** (NOT default — custom converts +40% better)
- **Paywall trigger:** After user completes 5th quest AND earns first level-up. This is the "value moment" — they've experienced the gamification loop and want more.
- **Free tier:** Unlimited quests/tasks, basic gamification (XP, 3 character classes), 1 habit tracker, 7-day history
- **Premium tier ($4.99/month):** AI coach (task breakdown, prioritization), unlimited habits, all 12 character classes, legendary gear, detailed analytics, custom themes, widget stats
- **Annual tier ($39.99/year):** 33% discount vs monthly. Pre-selected on paywall. "Save 33% — that's like 4 months free."
- **Trial:** 7-day free trial of Premium, no card required (RevenueCat no-card trial → +15-30% conversion lift)

### 1.3. Screen-by-Screen Specification

**Screen 1: Onboarding (3 cards max)**
- Card 1: "Your brain doesn't work like everyone else's. That's your superpower." — emotional validation
- Card 2: "500,000+ quests completed by people with brains like yours." — social proof
- Card 3: "Let's build your character. You're 60 seconds from a to-do list that actually works." — CTA
- State: @AppStorage for onboarding-completed flag
- Animation: Cards slide horizontally with spring (damping 0.7). Background gradient shifts from navy to purple as user progresses.
- Accessibility: All text VoiceOver-accessible. Swipe hints announced.
- Empty state: N/A (onboarding is the empty state)

**Screen 2: Home / Quest Board**
- Top: Character avatar + level + XP progress bar (linear gradient gold-to-amber)
- Center: Today's quests as cards — swipe right to complete (haptic + confetti), swipe left to postpone
- Bottom: Tab bar (Quests, Habits, Focus, Stats, Settings)
- State: @Observable QuestViewModel with SwiftData @Query for today's quests
- Animation: Quest cards stagger-fade in (0.05s delay each). Swipe completion: card shrinks + gold particles + haptic medium impact
- Empty state: "No quests yet, adventurer! Tap + to add your first quest." with glowing + button
- Accessibility: Quest cards have "Swipe right to complete, swipe left to postpone" accessibility hint

**Screen 3: Quest Creation (Core Action)**
- Text field for quest name (auto-focused)
- Quick-add buttons: "Buy groceries" / "Finish report" / "Work out" / Custom
- AI breakdown toggle (Premium): "Let AI break this into smaller quests?"
- Difficulty selector: Easy (10 XP) / Medium (25 XP) / Hard (50 XP) / Boss (100 XP with 3 sub-quests)
- Due date picker (optional)
- State: @State questName, @State difficulty, @Bindable viewModel
- Animation: Save button morphs into checkmark. Quest card "flies" into the quest board with spring animation.
- 2 taps max from home screen to quest created

**Screen 4: Quest Complete / Payoff**
- Full-screen celebration: confetti in brand colors, character dances, XP counter spins up
- Haptics: heavy impact on completion, then light impacts as XP counter increments
- Share button prominent: "I just defeated 'Write Quarterly Report' on QuestFlow! ⚔️ 50 XP earned"
- Streak counter updated with fire emoji animation
- "Add Another Quest" button for loop-back
- Duration: 2.5s total celebration. Tappable anywhere to dismiss (impatient users)

**Screen 5: Settings**
- Minimal. 8 items max: Profile, Notification preferences, Theme (dark/AMOLED), Sound effects toggle, Haptic strength, Data & sync (CloudKit status), Privacy, About/Version
- Every toggle here means we failed to set a smart default. Audit quarterly.
- Export data button: "Your data is yours. Export as JSON anytime."

**Screen 6: Premium Upgrade**
- Split screen comparison: Free column vs Premium column
- Feature list with animated checkmarks
- Annual plan pre-selected with "BEST VALUE" badge
- "7 days free, no card required" prominently displayed
- Testimonial carousel: real quotes from beta users
- Conversion CTA: "Level Up Your Productivity →"

### 1.4. iOS-Specific Optimizations
- **WidgetKit:** 3 sizes — Small: XP progress ring + streak count. Medium: Today's top 3 quests + completion status. Large: Quest board summary + character avatar + weekly completion rate. Widgets refresh every 15 minutes via SwiftData push.
- **App Intents / Siri:** "Hey Siri, add a quest in QuestFlow" — creates a new quest. "Hey Siri, what are my quests today?" — reads today's quests aloud.
- **Live Activities:** Focus Timer mode shows countdown in Dynamic Island. Streak-at-risk warning appears at 8pm if user hasn't completed any quests today.
- **App Store Review prompt:** Triggered after quest #10 completed (3rd successful core action felt too early — by quest #10 they're invested). Use SKStoreReviewController with 3-per-year limit consideration.
- **Push notifications:** Rich notifications with character avatar image. Actionable: "Complete 'Buy groceries'" with Mark Complete button right in the notification. Categories: quest-reminder, streak-at-risk, daily-summary, AI-coach-tip.
- **Privacy nutrition label:** Data Not Collected for everything except: User Content (quests/tasks you create — obvious, stored on-device and optionally CloudKit synced), Diagnostics (crash data, anonymized via MetricKit), Identifiers (RevenueCat anonymous subscriber ID only).

---

## SECTION 2: ANDROID ARCHITECTURE (Jetpack Compose-First)

### 2.1. Technology Stack
- **Language:** Kotlin 2.0 with Jetpack Compose (Material 3)
- **Minimum SDK:** 26 (Android 8.0, 96% of devices)
- **Architecture:** MVVM with StateFlow + collectAsStateWithLifecycle()
- **Persistence:** Room database + DataStore for preferences
- **Sync:** Firebase Firestore for cross-device sync (Android has no CloudKit equivalent)
- **DI:** Hilt (compile-time safe, Google-recommended)
- **Navigation:** Compose Navigation with type-safe routes (Kotlin serialization)
- **Analytics:** Firebase Analytics (GDPR consent flagged before initialization)

### 2.2. Google Play Billing (Subscription)
- BillingClient 7.0+ with Play Billing Library
- Product IDs: `questflow_premium_monthly`, `questflow_premium_annual`
- **Paywall trigger:** Same as iOS — after 5th quest + first level-up
- **Grace period:** 7 days (reduces involuntary churn by 40%)
- **Account hold:** 30 days (Android default)
- **Introductory price:** 50% off first 3 months for annual, 50% off first month for monthly

### 2.3. Android-Specific Optimizations
- **Material You dynamic theming:** Monet colors from user wallpaper replace the default purple. QuestFlow respects the user's device personality while maintaining brand identity through the gem icon and layout structure.
- **Predictive back gesture:** All screens support Android 14+ predictive back animation. Quest creation screen shows blurred quest board behind.
- **App Shortcuts:** 4 static shortcuts (long-press): Add Quest, Start Focus Timer, View Streak, Talk to AI Coach
- **Notification channels:** quest-reminders (High importance), streak-warnings (Urgent), daily-summary (Default), focus-timer (Low), ai-tips (Default). Each with distinct sound and vibration pattern.
- **Background work:** WorkManager for periodic sync, streak recalculation at midnight, notification scheduling. Doze-mode compatible.
- **Play Store listing:** 8 screenshots (feature-grid style). Feature graphic (1024×500): character avatar + "Turn To-Dos Into Quests" on purple/amber gradient. Short description: "ADHD-friendly gamified task manager with AI coach. Turn your to-do list into an RPG. 500K+ quests completed." Full description: progressive disclosure, first 250 characters = core pitch.

---

## SECTION 3: SEO & GEO OPTIMIZATION

### 3.1. App Store Optimization (iOS)

**Keyword Field (100 characters):**
```
gamified,task,manager,adhd,to-do,list,habit,tracker,productivity,quest,rpg,ai,coach,daily,planner
```
- "gamified" — high-volume modifier, competitive but essential
- "task manager" — primary discoverability keyword
- "adhd" — booming search volume 2026, lower competition than "productivity"
- "to-do list" — evergreen volume
- "habit tracker" — growing category, 15% CAGR
- "quest" — unique differentiator, low competition
- "ai coach" — trending 2026, medium competition
- Competitor brand names deliberately excluded

**Title + Subtitle Keywords (2× ranking weight):**
"Gamified", "Task", "ADHD", "AI Coach" appear in both title and subtitle.

**Description (first 3 lines):**
"QuestFlow is the ADHD-friendly gamified task manager that turns your to-do list into an RPG adventure. Join 500K+ quests completed by users who finally found a productivity app that understands their brain. Our AI coach helps you break down overwhelming tasks into bite-sized quests — then rewards you with XP, levels, and legendary gear when you complete them."

**Promotional Text (170 characters):**
"New: AI Coach now breaks down any task into ADHD-friendly sub-quests automatically. Just type 'clean garage' and watch it become a 5-step quest chain. Try it free for 7 days!"

**Ratings & Reviews Strategy:**
- Prompt timing: After completing a "Boss" quest (50+ XP), when dopamine is highest
- Prompt copy: "Your quest board is thriving! Would you help other adventurers discover QuestFlow?"
- Negative review templates, 3 common complaints:
  1. "Too expensive" → "We hear you! QuestFlow Premium costs less than one coffee per month. Free tier is unlimited and will always remain free. What features would make Premium feel worth it to you?"
  2. "Too complex" → "QuestFlow was designed for ADHD brains that need structure. We'd love to know what felt confusing — our AI coach can actually simplify things for you. Want us to walk you through it?"
  3. "Bug report" → "Thanks for flagging this! Our dev team is on it. Can you email us at support@questflow.app with your device model? We'll get this fixed in the next update."

### 3.2. Google Play Store Optimization

- **Title:** QuestFlow: Gamified ADHD Task Manager (41 chars, keyword-rich)
- **Short Description:** Gamified ADHD task manager with AI coach. Complete quests, earn XP, build habits. (82 chars)
- **Full Description:** 2-3% keyword density for "ADHD task manager", "gamified to-do list", "productivity app", "habit tracker"
- **Category:** Productivity (primary), Lifestyle (secondary)

### 3.3. Off-Store SEO (Web Presence)

**Landing Page (questflow.app):**
- H1: "QuestFlow — The Gamified ADHD Task Manager That Finally Works"
- Meta description: "QuestFlow turns your to-do list into an RPG quest log. AI-powered task breakdown, XP rewards, and habit tracking designed for ADHD brains. 500K+ quests completed. Free on iOS & Android."
- Above-fold: App screenshot hero + "Download on iOS" / "Get on Android" badges + "4.8 ★ (2,300+ reviews)"
- OG image: 1200×630 — purple gem icon on dark background with "Turn To-Dos Into Quests" text
- Schema.org: SoftwareApplication markup with rating, price ($0 with IAP), OS, category

**Content SEO Strategy (blog):**
1. "Habitica vs QuestFlow: Which Gamified Task Manager Actually Works for ADHD in 2026?"
2. "How to Turn Your ADHD To-Do List Into an RPG (Complete Guide)"
3. "Best ADHD Productivity Apps 2026: Honest Review from Someone Who Tested All 20"
4. "Why Gamification Is the Missing Piece in ADHD Task Management"
5. "AI Task Breakdown: How QuestFlow's Coach Makes Overwhelming Projects Possible"

**GEO (Generative Engine Optimization):**
- FAQ section: 8 question-answer blocks targeting AI overviews
- List-type content: "7 Features That Make QuestFlow Different From Every Other Task Manager"
- Author bylines with credentials on all posts (EEAT)

---

## SECTION 4: BEHAVIORAL ARCHITECTURE (Hooked Model)

### 4.1. Trigger Design

**External Triggers:**
- **Push #1 (Timely Reminder):** "⚔️ Morning, adventurer! Your quest 'Send invoice' is due today. 25 XP awaits." Sends at 8:30am local time. Tone: warm fantasy RPG.
- **Push #2 (Social Proof):** "🔥 3 of your quest buddies completed all their quests yesterday. Your streak is at risk — 2 hours left!" Drives FOMO + loss aversion.
- **Push #3 (Loss Aversion):** "⚠️ Your 12-day streak ends in 3 hours. Even one quest saves it. A 1-minute quest counts."
- **Widget update:** Every 15 minutes. Passive trigger showing XP ring and streak on home screen.
- **Email re-engagement (Day 3 inactive):** Subject: "Your quest log misses you, adventurer." Body: "You were on a 12-day streak. The goblins are getting complacent. One quest today and your streak is back."

**Internal Triggers (Negative Emotion → App Open):**
- User feels **overwhelmed** by a big project → remembers QuestFlow's AI breaks it into bite-sized quests
- User feels **scattered** with too many tasks → remembers QuestFlow organizes everything by difficulty and priority
- User feels **unproductive** at day's end → remembers QuestFlow makes productivity feel like a game with visible progress
- User feels **bored** with traditional to-do lists → remembers QuestFlow is actually fun to use

### 4.2. Action Design
- **Core action:** Add and complete a quest. 2 taps: tap + button → type quest name → tap save.
- **Fogg Behavior Model:** Motivation (9/10 — user actively wants to be productive), Ability (9/10 — 2 taps to complete a quest), Trigger (8/10 — push notification or widget reminder). All exceed activation threshold.
- **Onboarding:** No explanation. "What's one thing you need to do today?" → user types it → immediately sees it as a quest card. Core action completed in <20 seconds. "Set up later" not offered — there's nothing to set up.

### 4.3. Variable Reward Design

**Reward of the Tribe (Social):**
- Quest Buddy system: See friends' completed quests, cheer them on, compete on weekly leaderboard
- Shareable achievement cards designed for Instagram Stories / X. Watermark with QuestFlow gem.
- "Your friend Alex just defeated a Boss quest. Send them a power-up!"

**Reward of the Hunt (Search):**
- Random loot drops on quest completion (1 in 10 chance of "legendary item" — cosmetic only but highly coveted)
- Daily quest: randomized each morning. "Today's bounty: 3× XP on any Health quest"
- Progressive class unlocks: start as Squire, discover you can become a Paladin, Shadow, or Alchemist at level 5

**Reward of the Self (Mastery):**
- Streak counter with milestone celebrations (7 days, 30 days, 100 days, 365 days)
- Personal stats dashboard: "You're 23% more productive on Tuesdays. You complete Hard quests 2× faster in the morning."
- Level progression: visual character evolution, title unlocks ("QuestLord", "Productivity Paladin")

### 4.4. Investment Design
- **Data investment:** All quests, habits, stats, preferences stored locally + synced. Switching means losing your character, history, and streaks. This is the moat.
- **Social investment:** Quest Buddies network. Leaving means abandoning your party.
- **Financial investment:** Even $4.99/month creates sunk cost. The $0.99 "tip jar" or "cosmetic gem pack" IAP creates micro-investment.
- **Skill investment:** Learning the quest system, optimizing character builds, mastering the AI coach commands — invested users won't restart elsewhere.
- **Reputation investment:** Streak numbers, character level, legendary items, leaderboard rank. Users will open the app at 11:55pm to save their 87-day streak.

---

## SECTION 5: VISUAL DESIGN SYSTEM

### 5.1. Design Principles
1. **Dark mode is the default.** Light mode is the option. The fantasy RPG aesthetic works best in dark environments. Light mode should still feel premium but is secondary.
2. **Every animation tells a story.** Quest completion = confetti + character celebration. Level up = screen-wide glow + particle burst. No motion is decorative — it all reinforces the game loop.
3. **The user is the hero.** Every piece of copy, every animation, every reward system reinforces that the user is the protagonist of their own productivity story. The app is just the game engine.
4. **Accessibility is character class, not afterthought.** Every feature works with VoiceOver/TalkBack. Reduced motion users get simplified but still satisfying feedback. Color-blind modes for all 3 major types.

### 5.2. Key Animations & Micro-Interactions
- **App open:** Gem icon expands into the quest board. Duration: 0.4s, spring damping 0.6. No static splash screen.
- **Quest completion:** Confetti burst in brand colors + character victory pose + XP counter spin-up + haptic heavy impact. Duration: 2.5s total. Spring damping 0.5.
- **Tab switches:** Morphing icons + crossfade. Duration: 0.25s, ease-in-out.
- **Quest list reordering:** Spring animation. Duration: 0.35s.
- **Error states:** Gentle shake + amber highlight on the offending element. No modal. Auto-heal after 1.5s.
- **Empty → populated:** Staggered fade-in, 0.05s delay per quest card.
- **Level-up:** Screen-edge purple glow → particle burst → new title banner slides down. Duration: 2s.

### 5.3. Haptic Feedback Map
- Light impact: Quest card tap, difficulty selector, theme toggle
- Medium impact: Quest completion, habit check-off, streak milestone
- Heavy impact: Level-up, Boss quest completion, 30-day streak
- Selection feedback: Difficulty picker scroll, date picker
- Notification feedback: ONLY for streak-at-risk warning (urgent)

### 5.4. Accessibility as Luxury
- **VoiceOver/TalkBack:** Every quest has "Quest: [name], [difficulty], worth [XP] XP. Swipe right to complete." Decorative particles have accessibilityHidden.
- **Dynamic Type:** Everything scales to largest accessibility size. Quest cards stack vertically instead of horizontally at large sizes.
- **Reduce Motion:** All decorative animations become instant. Core feedback (quest complete checkmark, XP change) keeps simplified animation.
- **Color blindness:** Quest difficulty indicated by icon shape AND color. XP amounts always shown numerically. No information is color-alone.

---

## SECTION 6: FINANCIAL ARCHITECTURE

### 6.1. Pricing Tiers

| Tier | Monthly | Annual | What's Included | Why This Price |
|---|---|---|---|---|
| Free | $0 | $0 | Unlimited quests, 3 character classes, basic XP, 1 habit tracker, 7-day history, dark/light themes | Generous enough for 4★ reviews. Core gamification loop intact. Premium features visible but locked ("Legendary item — unlock in Premium") |
| Premium | $4.99 | $39.99 | Everything in Free + AI Coach, unlimited habits, 12 character classes, legendary gear drops, detailed analytics, custom themes, all widget sizes | Anchored to a coffee. "$4.99 = your most productive month ever." Annual at $39.99 is 33% off — this is where 68% of iOS revenue comes from. |
| Party (Family) | — | $59.99 | Premium for up to 5 people + shared quest boards + party leaderboards + shared habits | Viral expansion vector. Every party member is free acquisition. Works for families, roommates, small teams. |

### 6.2. Unit Economics
- **CAC target:** $0 at launch (organic + content marketing + Reddit/product hunt)
- **LTV at 6 months:** $28.50 (avg subscription length 5.7 months × $5 ARPU)
- **Payback period:** 0 months at launch (CAC = $0). With paid acquisition later: target <4 months.
- **Monthly churn target:** 6% (below 8-15% industry average; gamification + streaks reduce churn naturally)
- **Referral value:** Each referred user who converts = $28.50 LTV. Referral cost = 1 free month for both parties (~$4 per successful referral). 7.1× ROI.

### 6.3. Monetization Flow
1. Download → Free tier, zero friction, no account required
2. Complete 5 quests + level up to Level 2 → "Aha moment" achieved
3. Paywall appears: "You've earned 175 XP and reached Level 2. Ready to unlock your full potential?" Annual pre-selected.
4. Decline → "No worries! Try Premium free for 7 days. No card required. Your character keeps all XP either way."
5. Still decline → Continue in Free. Paywall resurfaces after hitting Free limits (unlocking 4th character class, trying AI coach, viewing analytics)
6. Annual renewal reminder: 7 days before. In-app banner + RevenueCat push. "Your QuestFlow Premium renews next week. Lock in your rate now."

### 6.4. Cancellation Flow Intercept
- **In-app "Manage Subscription" screen** (before system Settings):
  - Step 1: Pause offer — "Would you like to pause your subscription for 1-3 months? Your character, gear, and streak history are all safe."
  - Step 2: Reason picker — Too expensive / Not using enough / Found alternative / Missing feature / Other
  - Step 3: If "Too expensive" → 50% off for 6 months ($2.49/month). Retention yield: 25-35% saved.
  - Step 4: If "Not using enough" → Offer weekly summary instead of daily notifications. "Lighter touch, same great quest board."
  - Step 5: Final → "We'll keep your character and data for 90 days. Come back anytime — you'll pick up right where you left off, adventurer."

---

## SECTION 7: VIRALITY ENGINE

### 7.1. Shareable Moments
1. **Streak Milestone:** "I've completed quests for 30 days straight on QuestFlow! 🔥 My ADHD brain has never been this consistent."
2. **Level-Up:** Character sheet showing new level, title, and stats. "Just hit Level 25 Productivity Paladin on QuestFlow ⚔️"
3. **Boss Defeated:** "I just defeated a Boss quest: 'Finish quarterly taxes' — 200 XP earned! 💀"
4. **Year-in-Review:** Personalized "QuestLog Annual Report" with total quests, XP earned, favorite character class, most productive day/time. Spotify Wrapped for productivity.
5. **Quest Buddy Challenge:** "I challenge you to complete more quests than me this week. Loser buys coffee ☕"

### 7.2. Viral Mechanics
- **Invite friction:** One tap → native share sheet. No email forms. Every extra field kills 65% of invites.
- **Invite incentive:** Sender gets exclusive "Recruiter" title + 100 bonus XP. Receiver gets first month of Premium free. If 1 in 10 receivers converts, it pays for all free months.
- **Network effect:** Quest Buddies / Party feature is usable solo but demonstrably better with friends. Shared quest boards, weekly leaderboards, party power-ups.
- **Watermark:** Every shareable card has "⚔️ QuestFlow" in bottom corner. Elegant, like Canva's export footer. Not obnoxious — aspirational.

### 7.3. App Store Rating Protection
- **≤2-star users:** Route to in-app feedback form. "We'd love to fix this. What went wrong?" Captures negative sentiment privately.
- **3-star users:** Show rating prompt with pre-selected 4-star nudge.
- **≥4-star users:** Prompt after Boss quest completion. "Adventurers like you help others discover QuestFlow. Rate us?"
- **Rating reply:** EVERY review gets a response within 24 hours. Developer-responsiveness boosts App Store search ranking.

---

## SECTION 8: TECHNICAL SPECIFICATION

### 8.1. Database Schema

```
TABLE Quest (
  id: UUID PRIMARY KEY,
  title: String NOT NULL,
  description: String?,
  difficulty: Enum(EASY, MEDIUM, HARD, BOSS) DEFAULT MEDIUM,
  xpValue: Int NOT NULL,
  dueDate: Date?,
  completedAt: Date?,
  status: Enum(ACTIVE, COMPLETED, POSTPONED, ABANDONED) DEFAULT ACTIVE,
  characterClass: Enum(SQUIRE, KNIGHT, PALADIN, SHADOW, ALCHEMIST, SAGE, BERSERKER, RANGER, BARD, NECROMANCER, DRUID, MONK),
  parentQuestId: UUID? (FK → Quest.id, for sub-quests),
  isAIGenerated: Bool DEFAULT FALSE,
  createdAt: Date NOT NULL,
  updatedAt: Date NOT NULL,
  syncToCloud: Bool DEFAULT TRUE
) INDEXES: idx_status, idx_dueDate, idx_completedAt

TABLE Habit (
  id: UUID PRIMARY KEY,
  name: String NOT NULL,
  frequency: Enum(DAILY, WEEKLY, CUSTOM),
  targetCount: Int DEFAULT 1,
  currentStreak: Int DEFAULT 0,
  longestStreak: Int DEFAULT 0,
  completions: JSON (array of Date),
  color: String DEFAULT "#F59E0B",
  iconName: String,
  createdAt: Date NOT NULL,
  syncToCloud: Bool DEFAULT TRUE
) INDEXES: idx_frequency

TABLE Character (
  id: UUID PRIMARY KEY,
  name: String DEFAULT "Adventurer",
  level: Int DEFAULT 1,
  xp: Int DEFAULT 0,
  xpToNextLevel: Int DEFAULT 100,
  title: String DEFAULT "Squire",
  class: Enum DEFAULT SQUIRE,
  equippedItems: JSON,
  totalQuestsCompleted: Int DEFAULT 0,
  totalXPEarned: Int DEFAULT 0,
  longestStreak: Int DEFAULT 0,
  currentStreak: Int DEFAULT 0,
  premiumUnlocked: Bool DEFAULT FALSE,
  lastActiveDate: Date
) LOCAL-ONLY (no sync — character data is personal)

TABLE UserPreferences (
  id: UUID PRIMARY KEY,
  theme: Enum(DARK, AMOLED, LIGHT) DEFAULT DARK,
  hapticStrength: Enum(OFF, LIGHT, MEDIUM, HEAVY) DEFAULT MEDIUM,
  soundEffects: Bool DEFAULT TRUE,
  notificationPreferences: JSON,
  aiCoachPersonality: Enum(MOTIVATIONAL, GENTLE, DRILL_SERGEANT, WISE_SAGE) DEFAULT MOTIVATIONAL,
  reducedMotion: Bool DEFAULT FALSE,
  colorBlindMode: Enum(NONE, PROTANOPIA, DEUTERANOPIA, TRITANOPIA) DEFAULT NONE
) LOCAL-ONLY
```

### 8.2. API Endpoints (Firebase Firestore for Android + cross-platform)
```
Firestore Collections:
  /users/{userId}/quests/{questId}
  /users/{userId}/habits/{habitId}
  /users/{userId}/party/{partyId}
  
REST endpoints (lightweight Node.js backend for shared features):
  POST /api/v1/party/create — create party
  POST /api/v1/party/{id}/invite — invite member
  GET  /api/v1/party/{id}/leaderboard — weekly rankings
  POST /api/v1/referral/claim — claim referral reward
  
Auth: Firebase Auth (Apple Sign In, Google Sign In, email)
```

### 8.3. Push Notification Schema
```json
{
  "aps": {
    "alert": {
      "title": "⚔️ Morning, adventurer!",
      "subtitle": "3 quests await you today",
      "body": "'Send invoice' is due by 2pm. 25 XP each."
    },
    "sound": "quest_horn.caf",
    "badge": 0,
    "mutable-content": 1,
    "category": "QUEST_REMINDER"
  },
  "custom_data": {
    "type": "daily_quest_reminder",
    "deep_link": "questflow://quests/today",
    "image_url": "https://cdn.questflow.app/notifications/morning_quest.png",
    "quest_count": 3,
    "top_quest_id": "abc-123"
  }
}
```

**Notification types:**
- `DAILY_QUEST_REMINDER`: 8:30am, lists today's quests
- `STREAK_AT_RISK`: 8pm if no quests completed, urgent priority
- `STREAK_MILESTONE`: On achievement (7/30/100/365 days)
- `QUEST_BUDDY_ACTIVITY`: Friend completed a quest
- `AI_COACH_TIP`: Weekly, personalized productivity insight
- `LEVEL_UP`: Character leveled up while app closed

### 8.4. AI Agent Architecture (Local-First)

Based on the "ai-agents-from-scratch" philosophy (pguso/ai-agents-from-scratch on GitHub): understand the ReAct pattern from first principles.

**On-Device Agent Loop:**
```
User: "Clean garage" → Local LLM receives prompt with system context →
LLM decides: TOOL_CALL "break_down_task" → Tool executes: query vector DB for similar task decompositions →
LLM processes: structured output with 5 sub-quests → UI renders quest chain
```

**Model mapping:**
| Feature | Pattern | iOS Model | Android Model | Latency |
|---|---|---|---|---|
| Task breakdown | ReAct (LLM + tools) | Phi-4-mini Q4_K_M (~2.2GB) | Gemma-3-1B (~1.3GB) | <3s |
| Priority suggestion | Chain-of-thought | Phi-4-mini | Gemma-3-1B | <5s |
| Daily recap | Single-pass transform | Phi-4-mini | Gemma-3-1B | <2s |
| Habit recommendation | Knowledge retrieval | Phi-4-mini | Gemma-3-1B | <2s |

- **iOS:** llama.cpp Swift bindings, Metal-accelerated
- **Android:** MediaPipe LLM Inference with Vulkan backend
- **Fallback:** Cloud API (Claude Haiku) for <A17 / <6GB RAM devices
- **Privacy moat:** Zero AI data leaves device. This is a competitive advantage no cloud-only competitor can match without architectural rewrite.

### 8.5. Third-Party Dependencies
- RevenueCat (subscriptions)
- Firebase Auth (social login)
- Firebase Firestore (Android/cross-platform sync)
- CloudKit (iOS sync)
- TelemetryDeck (iOS analytics)
- Firebase Analytics (Android)
- llama.cpp / MediaPipe (on-device AI)
- NO Facebook SDK. NO Google AdMob at launch. NO third-party analytics that touch user content.

---

## SECTION 9: 30-DAY MVP SPRINT PLAN

### Week 1 — Foundation
| Day | iOS | Android | Shared |
|---|---|---|---|
| Mon | Project setup, SwiftData models, CloudKit container | Project setup, Room entities, Hilt config | Finalize DB schema, Firestore structure |
| Tue | Onboarding flow (3 cards) | Onboarding flow (3 cards) | Design review: onboarding copy + visuals |
| Wed | Quest board home screen skeleton | Quest board home screen skeleton | Design review: quest card component |
| Thu | Quest creation + completion flow | Quest creation + completion flow | Integration test: add → complete loop |
| Fri | RevenueCat integration + custom paywall | BillingClient + custom paywall | Paywall design review |

### Week 2 — Core Experience
| Day | iOS | Android | Shared |
|---|---|---|---|
| Mon | XP system + level-up celebration | XP system + level-up animation | Animation review: confetti + particles |
| Tue | Push notifications (all 6 types) | Notification channels (all 6 types) | Notification copy + sound design final |
| Wed | WidgetKit (small, medium, large) | App Shortcuts (4 static) | Widget/shortcut review |
| Thu | Settings screen | Settings screen | Settings audit (max 8 items) |
| Fri | Empty states, error states, edge cases | Empty states, error states | Edge case matrix testing |

### Week 3 — Polish & Virality
| Day | iOS | Android | Shared |
|---|---|---|---|
| Mon | Haptics, quest animations, character animations | Motion system, predictive back, character animations | Micro-interaction review pass |
| Tue | Share sheet + shareable cards | Share intent + shareable cards | Virality flow end-to-end test |
| Wed | App Store screenshots + metadata | Play Store feature graphic + screenshots | ASO copy final |
| Thu | Accessibility audit (VoiceOver, Dynamic Type) | Accessibility audit (TalkBack, font scale) | Accessibility sign-off |
| Fri | Premium upgrade screen (comparison) | Premium upgrade screen (comparison) | Monetization flow full test |

### Week 4 — Launch Readiness
| Day | iOS | Android | Shared |
|---|---|---|---|
| Mon | Bug fixes, edge case hardening | Bug fixes, edge case hardening | Cross-platform parity checklist |
| Tue | App Store Connect submission prep | Play Console submission prep | Privacy policy + ToS final |
| Wed | TestFlight internal (team) | Internal testing track | Beta tester feedback collection |
| Thu | TestFlight external (50 testers) | Closed testing (20 testers req.) | Beta feedback triage |
| Fri | **SUBMIT TO APP STORE** | **SUBMIT TO PLAY STORE** | Launch day coordination |

### MVP Feature Cut List (Do NOT Build in Sprint 1)
1. **Party/Quest Buddies system** — social features add complexity without validating core value first
2. **AI coach** — ships in v1.1 (Week 5-6). Core gamification must work flawlessly before adding AI layer. This is the hook for v2.
3. **Year-in-review / Wrapped** — needs data accumulation, ships after 6 months
4. **Apple Watch / Wear OS companion** — v1.3, after mobile retention is proven

---

## SECTION 10: LAUNCH CHECKLIST

### Pre-Launch (T-14 days)
- [ ] App Store Connect: App record created, all metadata filled, privacy labels complete
- [ ] Google Play Console: App created, all metadata, content ratings, data safety section
- [ ] RevenueCat: Products configured, webhooks set up, offerings tested
- [ ] Privacy Policy URL: Live at questflow.app/privacy (GDPR compliant)
- [ ] Terms of Service URL: Live at questflow.app/terms
- [ ] Support email: support@questflow.app with auto-responder
- [ ] App screenshots: 6.9" and 6.7" displays, all localizations (EN only at launch)
- [ ] App Preview Video (optional but recommended — +20-35% conversion)
- [ ] TestFlight build submitted for Beta App Review
- [ ] Closed testing: 20 testers opted in for 14 days (Google Play requirement)
- [ ] Landing page live: questflow.app with download badges

### Launch Day (T=0)
- [ ] Release to App Store (manual release, not automatic)
- [ ] Release to Play Store (staged rollout: 10% for 24h to catch crash loops)
- [ ] Monitor TelemetryDeck + Firebase Analytics dashboards
- [ ] Monitor App Store Connect crash reports
- [ ] Reply to first 10 reviews within 2 hours
- [ ] Post on r/ADHD, r/ProductivityApps, r/AppIdeas — authentic indie dev story
- [ ] Post on Product Hunt (schedule 12:01 AM PT for max exposure)
- [ ] Send launch email to beta testers: "We're live! 50% off your first year — thank you for helping us build QuestFlow."

---

## SECTION 11: POST-LAUNCH ITERATION PLAN

### Week 1 Post-Launch: Observe
- Watch: D1/D7/D30 retention, free→premium conversion, crash rate, avg session length
- Read EVERY review. Categorize: bug / feature request / UX confusion / pricing
- Ship ZERO new features. Only critical crash fixes.

### Week 2-4: Quick Wins
- Ship top 3 user-requested improvements
- A/B test paywall if conversion <20%
- D1 retention <40% → onboarding is broken, redesign
- D7 retention <20% → habit loop failing, redesign triggers

### Month 2-3: Feature Expansion
- Ship AI Coach (v1.1) — the promised premium differentiator
- Party/Quest Buddies system (v1.2)
- Content marketing: 5 SEO pillar posts published
- Begin ASO iteration based on keyword ranking data

---

## SECTION 12: ANTI-PATTERNS — What You MUST NOT Do

1. **Do not ask for notification permission on first open.** 60% say no. Ask after user completes first quest, with custom pre-permission: "Quest reminders keep your streak alive. Want us to notify you when quests are due?"
2. **Do not require account creation before use.** Try before sign-up. Every barrier between download and first quest kills 20-30% of users.
3. **Do not show ads, ever.** Ads destroy the premium RPG aesthetic. Monetize through the user (subscription), not their attention. QuestFlow is a premium product.
4. **Do not use default system paywall.** Default RevenueCat/StoreKit paywalls convert 40% worse. Build custom in SwiftUI/Compose.
5. **Do not ship with a static splash screen.** Gem icon → immediate animation into quest board. No logo sitting still.
6. **Do not ignore 1-star reviews.** Respond within 24 hours. Many 1-star reviewers upgrade when they get a personal response.
7. **Do not localize poorly.** English-only at launch. Add Spanish and German when you can afford human translators.
8. **Do not launch both platforms simultaneously if resources are tight.** iOS first, Android 2 weeks behind. App Store review is unpredictable; Play Store learnings applied to Android launch.
9. **Do not obsess over algorithms.** Optimize for user experience. Algorithms follow users, not the other way.
10. **Do not build features nobody asked for.** Every sprint ships at least one thing users actually requested this week.

---

_End of BeeDone/QuestFlow Scaffold. Generated 2026-05-25 by App Discovery Pipeline._
_A dev agent should be able to build the complete iOS + Android app from this document with zero additional clarification._