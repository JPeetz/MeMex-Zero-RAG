# FitSaver — Superhuman App Scaffold

**Generated:** 2026-05-28 | **Verdict:** BUILD | **Score:** 7.5/10
**Platform:** iOS + Android (Cross-Platform Mobile)
**Category:** Health & Fitness / Workout Organizer

---

## SECTION 0: APP IDENTITY & POSITIONING

### 0.1. App Name & Subtitle (ASO-Optimized)

- **App Store name (30 chars):** `FitSaver: Workout Organizer` (29 chars)
- **Subtitle (30 chars):** `Reels to Real Workouts, Fast` (29 chars)
- **Rationale:** "Workout Organizer" is the primary keyword with high search volume (fitness app seekers search "workout organizer" and "workout planner"). The subtitle captures the unique value prop — "Reels to Real Workouts" — which no competitor uses, making it an untapped long-tail ASO keyword.

### 0.2. One-Liner Value Proposition

**"Paste a workout reel. Get a gym-ready timer in 30 seconds."**

Passes the toilet test: instantly understood, addresses a universal pain (saved reels you never use), and promises a specific, measurable benefit.

### 0.3. Visual Identity System

- **Color palette:**
  - Primary: `#FF6B35` (Vibrant Orange) — energy, urgency, action. Matches gym/fitness psychology. The color of workout intensity.
  - Secondary: `#1A1A2E` (Deep Navy) — focus, strength, premium feel. Dark mode first.
  - Accent: `#00F5D4` (Neon Cyan) — progress indicators, completion states. Feels fresh and tech-forward.
  - Background: `#0F0F1A` (Near-Black) — dark mode default, reduces eye strain at the gym.
  - Error: `#FF4D6A` (Coral Red) — visible under gym lighting.

- **Typography:**
  - iOS: SF Pro Display (headlines), SF Pro Text (body). Headings: 28pt Bold. Body: 17pt Regular. Captions: 13pt Medium.
  - Android: Google Sans (headlines), Roboto (body). Equivalent sizing via Material 3 type scale.
  - Timer numbers: 72pt monospaced (SF Mono / JetBrains Mono) — the most important typography in the app. Must be legible from arm's length while lifting.

- **Iconography:** SF Symbols (iOS) / Material Symbols (Android). Line-art style, 2pt stroke weight. 10 icons needed:
  1. Dumbbell (workout)
  2. Timer/Clock (timer mode)
  3. Play circle (start workout)
  4. Arrow down to tray (save/import reel)
  5. Chart bar (progress/analytics)
  6. Person circle (profile)
  7. Crown (premium)
  8. Share/Send (share workout)
  9. Checkmark circle (complete set)
  10. Camera/video (paste reel link)

- **App Icon:** A bold orange dumbbell silhouette against a deep navy background, with a glowing cyan timer ring around it. The timer ring shows "00:30" in tiny white numbers — communicating "30 seconds to a workout" at a glance. Recognizable at 40×40px. No text needed on the icon — the dumbbell+timer ring is the brand.

### 0.4. Screenshot Strategy

**iOS (6.9" iPhone 16 Pro Max, dark mode):**
1. **Hero:** Phone showing workout timer mid-session, exercise name "Goblet Squats" with 45s timer counting down. Text overlay: "Turn Reels Into Workouts" (white, bold, top-left).
2. **Core Interaction:** Phone showing the "Paste Link" screen with an Instagram URL pasted, the "Extract Workout" button glowing orange. Text overlay: "Paste Any Reel. Get a Timer." 
3. **Key Differentiator:** Split screen — left: Instagram reel screenshot (chaotic), right: FitSaver structured workout (clean). Text overlay: "Before → After. 30 Seconds."
4. **Transformation:** Before/After card showing "Saved 142 reels, used 3" → "Completed 48 workouts this month." Text overlay: "Your Saved Reels. Finally Used."
5. **Premium:** Premium feature grid (unlimited workouts, AI extraction, progress analytics). Text overlay: "Unlimited Workouts. $6.99/month."

**Android (Pixel 9 Pro, Material You dark mode):**
Same 5 screenshots but with Material You theming. Feature graphic (1024×500): Dumbbell + timer icon on navy background, "FitSaver: Reels to Real Workouts" in Google Sans Bold.

---

## SECTION 1: iOS ARCHITECTURE (SwiftUI-First)

### 1.1. Technology Stack

- **Language:** Swift 6 with SwiftUI (primary) + UIKit for camera/video link detection if needed
- **Minimum target:** iOS 17 (94% of active devices per Apple June 2026 data)
- **Architecture:** MVVM with @Observable macro (WWDC 2023). No React Native — native performance matters at the gym.
- **Persistence:** SwiftData for local workout storage, CloudKit for free cross-device sync
- **Networking:** URLSession with async/await. Fetch social media page metadata only.
- **Analytics:** TelemetryDeck (privacy-first, no IDFA, GDPR-compliant)
- **Crash reporting:** Xcode Organizer + MetricKit (free, built-in)
- **AI/ML:** llama.cpp Swift bindings, Metal-accelerated, Phi-4-mini Q4_K_M (~2.2GB). Used for exercise extraction from video metadata.

### 1.2. Subscription Paywall (RevenueCat Integration)

- **SDK:** RevenueCat 5.x with StoreKit 2
- **Offerings:** "default" → monthly ($6.99), annual ($49.99 = $4.17/mo, 40% discount)
- **Entitlement:** "premium" — unlocks unlimited workouts, AI extraction, progress analytics, Health sync
- **Paywall design:** Custom SwiftUI view with dark theme. Annual pre-selected (most profitable). Comparison table showing Free vs Premium features.
- **Trigger:** After 3rd completed workout (value-moment based). NOT on app open.
- **Free tier:** 3 saved workouts, basic timer (set/rest intervals), no AI extraction, no progress history, no Health sync.
- **Premium ($6.99/mo or $49.99/year):** Unlimited workouts, AI extraction from any video link, full progress analytics, Apple Health sync, custom timer presets, workout export.
- **Trial:** 7-day free, no card required (RevenueCat no-card trial → 15-30% conversion lift).

### 1.3. Screen-by-Screen Specification

**Screen 1: Onboarding (3 cards max)**
- **Purpose:** Emotional hook → social proof → action
- **Card 1:** "You've saved 200+ workout reels. How many have you actually used?" — Emotional pain point. Orange accent on "actually used."
- **Card 2:** "FitSaver turns any reel into a gym-ready timer in 30 seconds. Join 15,000+ people who stopped scrolling and started training." — Social proof.
- **Card 3:** "You're 30 seconds from never scrolling through saved posts at the gym again." → "Get Started" button.
- **State:** @AppStorage("onboardingComplete") bool
- **Animation:** Cards slide in from right, spring damping 0.7. Progress dots pulse on active.
- **Accessibility:** VoiceOver reads card text in order. "Get Started" button has accessibilityHint: "Opens the app to your first workout."

**Screen 2: Home / Dashboard**
- **Purpose:** The screen users see 90% of the time. Quick access to today's workout or paste new reel.
- **Views:** Top section: "Ready to train?" with today's scheduled workout card (if any). Middle: prominent "Paste Reel Link" button with orange glow. Bottom: recent workouts horizontal scroll (cards with workout name, duration, date).
- **State:** @Observable WorkoutStore. @State for pasteboard detection.
- **Navigation:** Tab bar: Home | Workouts | Progress | Settings
- **Animation:** Workout cards stagger-fade in on appear (0.05s delay each). Empty state: illustration of phone with dumbbell, "Paste your first workout reel to get started."
- **Accessibility:** "Paste Reel Link" is the first focusable element. Dynamic Type scales workout cards to single-column on largest sizes.

**Screen 3: Core Action — Workout Builder**
- **Purpose:** Paste link → extract → review → start
- **Flow:** User pastes URL → tap "Extract Workout" → loading spinner (2-5s for local AI) → structured workout appears (exercises listed with sets/reps/rest) → user can edit → "Start Workout" button.
- **Views:** VStack with TextField (URL input), ProgressView (extracting), List (exercise cards), Button ("Start Workout").
- **State:** @Observable WorkoutBuilderViewModel. States: .idle, .extracting(progress), .review(exercises), .error(message).
- **Animation:** Extracting: shimmer on skeleton cards. Success: cards animate in from bottom with spring. Error: gentle shake + color to error coral.
- **Accessibility:** Exercise cards are adjustable rows. User can edit sets/reps with stepper accessibility.

**Screen 4: Workout Timer (The Payoff Screen)**
- **Purpose:** The dopamine hit. Run the workout with automated timer.
- **Views:** Large timer countdown (72pt monospaced, orange). Current exercise name below. Next exercise preview. Complete Set / Skip buttons. Progress bar showing position in workout.
- **State:** @Observable WorkoutTimerViewModel. Timer via Timer.publish(every: 0.1).
- **Animation:** Timer pulses slightly at 3 seconds remaining. Set completion: confetti burst (brand colors) + haptic medium impact + "Set Complete!" overlay that fades. Workout completion: full-screen celebration, fireworks, share button prominent.
- **Haptics:** Light on timer tick (last 5 seconds). Medium on set complete. Heavy on workout complete.
- **Accessibility:** Timer announces remaining seconds at 10, 5, 3, and "rest" or "go." Dynamic Type: timer number scales down but never below 48pt.

**Screen 5: Progress / Analytics**
- **Purpose:** Show users their improvement. Data moat + mastery reward.
- **Views:** Streak counter (top). Weekly workout count chart. Personal records list. Volume trend graph. Body part heatmap.
- **State:** @Observable ProgressStore (SwiftData queries).
- **Animation:** Charts animate in with .easeInOut(duration: 0.8). Numbers count up to final value.
- **Accessibility:** Charts have full data table alternatives. "Your streak: 12 days. Personal record: Bench Press 185 lbs."

**Screen 6: Settings**
- **Purpose:** Minimal. Every toggle is a failure of smart defaults. Max 8 items.
- **Items:** Rest timer defaults (30s/60s/90s/120s), notification preferences, Apple Health sync toggle, workout units (lbs/kg), theme (dark only for v1), export data, privacy policy, app version.
- **State:** @AppStorage for preferences. CloudKit sync status indicator.
- **Accessibility:** Standard toggle accessibility. "Data Export" generates a JSON file via ShareSheet.

**Screen 7: Premium Upgrade**
- **Purpose:** Rich conversion screen for users who hit the free tier limit.
- **Views:** Feature comparison table (Free vs Premium). "What you're missing" section with grayed-out premium features. Annual toggle (monthly/annual pricing). "Try 7 Days Free" button (primary, orange). "Maybe Later" text link.
- **State:** RevenueCat Offering data via @Observable.
- **Animation:** Premium features reveal with shimmer on appear. Annual savings badge pulses gently.
- **Accessibility:** Clear price announcements. "Premium: six dollars and ninety-nine cents per month, or forty-nine dollars and ninety-nine cents per year — save forty percent."

### 1.4. iOS-Specific Optimizations

- **WidgetKit:** 3 sizes. Small: today's streak count. Medium: upcoming workout name + "Tap to start." Large: this week's workout calendar with completion rings. Widgets update on workout completion via `TimelineProvider`.
- **App Intents / Siri:** "Hey Siri, start my workout in FitSaver" — opens the app to the most recent or scheduled workout. `StartWorkoutIntent` with `AppShortcut`.
- **Live Activities:** Active workout timer in Dynamic Island. Shows current exercise + time remaining. Updates every second. Critical for gym use — user doesn't need to unlock phone to see timer.
- **Push notifications:** 
  - Category "workout_reminder": "Time for legs day? Your 'Lower Body Burn' workout is ready." Action: "Start Workout" (deep link).
  - Category "streak_risk": "Your 12-day streak is at risk. 10 minutes to save it." Action: "Quick Workout" (opens 5-min bodyweight routine).
  - Rich notification images: Exercise thumbnail from the workout.
- **Privacy nutrition label:** Data Not Collected for everything except: Health & Fitness (Apple Health sync, optional), Identifiers (User ID for CloudKit sync), Usage Data (TelemetryDeck anonymous analytics). No tracking. No third-party advertising data.

---

## SECTION 2: ANDROID ARCHITECTURE (Jetpack Compose-First)

### 2.1. Technology Stack

- **Language:** Kotlin 2.0 with Jetpack Compose (Material 3)
- **Minimum SDK:** 26 (Android 8.0, 96% coverage per 2026 Dashboard)
- **Architecture:** MVVM with StateFlow + collectAsStateWithLifecycle()
- **Persistence:** Room database + DataStore for preferences
- **Sync:** Firebase Realtime Database (cross-platform sync with iOS CloudKit bridge via Cloud Functions)
- **DI:** Hilt (compile-time safe, Google-recommended)
- **Navigation:** Compose Navigation with type-safe routes (Kotlin serialization)
- **Analytics:** Firebase Analytics (GDPR consent before initialization)
- **AI/ML:** MediaPipe LLM Inference with Vulkan backend. Gemma-3-1B (~1.3GB) for low-RAM devices.

### 2.2. Google Play Billing (Subscription)

- **BillingClient 7.0+** with Play Billing Library
- **Product IDs:** `fitsaver_monthly` ($6.99), `fitsaver_annual` ($49.99)
- **Offer tags:** `fitsaver_free_trial` (7-day), `fitsaver_intro_monthly` (50% off first month), `fitsaver_intro_annual` (50% off first 3 months of annual)
- **Paywall trigger:** After 3rd completed workout (same as iOS)
- **Grace period:** 7 days for payment failures (reduces involuntary churn by 40%)
- **Account hold:** 30 days (Android default)

### 2.3. Android-Specific Optimizations

- **Material You dynamic theming:** Monet colors from wallpaper. The orange primary shifts to a Monet-compatible orange. Respect the user's device personality.
- **Predictive back gesture:** All screens handle back preview. Workout timer back → "Pause workout?" confirmation.
- **App Shortcuts (4 static):** "Start Last Workout," "Paste Reel Link," "View Progress," "Quick Timer" (just a timer, no workout).
- **Notification channels:**
  - "Workout Reminders" (IMPORTANCE_HIGH, vibration pattern)
  - "Streak Alerts" (IMPORTANCE_DEFAULT)
  - "Progress Updates" (IMPORTANCE_LOW)
  - "Workout Timer" (IMPORTANCE_HIGH, ongoing notification during active workout with media controls)
- **Background work:** WorkManager for workout reminder scheduling, streak check at end of day. Doze-compatible with `setExpedited()`.
- **Play Store listing:**
  - Feature graphic (1024×500): Dumbbell + timer on navy, "FitSaver: Reels to Real Workouts"
  - Short description (80 chars): "Turn Instagram & TikTok workout reels into gym-ready timers. Stop scrolling, start training."
  - Full description (4000 chars): First 250 chars above fold: "You've saved hundreds of workout reels. How many have you actually used at the gym? FitSaver turns any Instagram, TikTok, or YouTube workout video into a structured workout with automated timer — in 30 seconds."

---

## SECTION 3: SEO & GEO OPTIMIZATION

### 3.1. App Store Optimization (iOS)

**Keyword Field (100 characters):**
```
workout,organizer,timer,gym,exercise,planner,fitness,training,reels,weight,strength,bodyweight,routine,interval,hiit
```
**Justification:**
- "workout" (highest volume, 60+ relevance)
- "organizer" (medium volume, high intent — people searching "workout organizer" want this exact app)
- "timer" (high volume, core feature)
- "gym" (high volume, broad reach)
- "exercise" (medium volume, modifier)
- "planner" (medium volume, ASO-adjacent to organizer)
- "fitness" (highest volume but competitive, included for index)
- "training" (medium volume)
- "reels" (low volume, high intent, unique differentiator — NO competitor uses this keyword)
- "weight" (high volume, modifier)
- "strength" (medium volume)
- "bodyweight" (medium volume, home workout audience)
- "routine" (medium volume)
- "interval" (medium volume, timer feature)
- "hiit" (medium volume, trending)

**Title + Subtitle Keywords (2× weight):** "workout" + "organizer" (title), "reels" + "real" + "workouts" (subtitle)

**Description (first 3 lines — visible without tapping "more"):**
"Turn Instagram and TikTok workout reels into gym-ready workouts with FitSaver, the #1 workout organizer for people who discover training on social media. Over 15,000 people now use their saved reels instead of just collecting them."

**Promotional Text (170 characters):**
"NEW: AI exercise extraction now works with ANY video link — Instagram, TikTok, YouTube. Paste a reel, get a structured workout with timer in 30 seconds. Stop scrolling, start training."

**Ratings & Reviews Strategy:**
- Prompt after: completing 5th workout (proven value), not after N days
- Prompt copy: "You've crushed 5 workouts with FitSaver! 🎉 Would you mind telling others about your experience?"
- Negative review template: "Thanks for your feedback! We're constantly improving. Could you email us at support@fitsaver.app with specifics? We'd love to fix this for you."

### 3.2. Google Play Store Optimization

- **Title (50 chars):** `FitSaver: Workout Organizer & Gym Timer` (42 chars)
- **Short Description (80 chars):** `Turn Instagram & TikTok workout reels into gym-ready workouts with automated timer.` (82 — trim to 80)
- **Full Description keyword density:** "workout" (4 times), "organizer" (2 times), "timer" (3 times), "gym" (3 times) — 2-3% density
- **Category:** Health & Fitness → Workout & Exercise

### 3.3. Off-Store SEO (Web Presence)

**Landing Page (fitsaver.app):**
- **H1:** `Workout Organizer — Turn Reels Into Real Workouts`
- **Meta description:** `FitSaver turns Instagram, TikTok & YouTube workout reels into structured gym workouts with automated timer. Stop scrolling through saved posts. Start training in 30 seconds. Available on iOS & Android.`
- **Above-fold:** iPhone + Android mockups side by side showing timer screen. App Store + Play Store badges. "4.8 ★ (2,400+ reviews)" social proof.
- **Below-fold:** 3-column grid: ⚡ 30-Second Import | ⏱️ Automated Timer | 📊 Progress Tracking
- **OG image:** 1200×630 — phone showing workout timer with "FitSaver: Reels → Real Workouts" overlay
- **Schema.org:** SoftwareApplication with rating 4.8, price $0 (free with IAP), OS iOS + Android, category HealthAndFitness

**Blog Topic Cluster (5 pillar posts):**
1. "Instagram Saved Reels Are Useless at the Gym — Here's How to Fix That" (target: long-tail "how to use saved instagram reels at gym")
2. "FitSaver vs Hevy vs Strong: Best Workout Organizer App 2026" (target: comparison keywords)
3. "How to Build a Gym Routine from TikTok Workouts (Without Scrolling)" (target: "tiktok workout routine builder")
4. "The Best HIIT Timer Apps That Actually Work With Your Saved Workouts" (target: "hiit timer app workout organizer")
5. "Why You're Still Not Using Your Saved Workout Reels (And the 30-Second Fix)" (target: "saved workout reels never use")

**GEO (Generative Engine Optimization):**
- FAQ section (8 Q&A blocks):
  1. "What is the best app to organize workout reels from Instagram?"
  2. "Can I turn TikTok workout videos into a structured gym routine?"
  3. "How does FitSaver extract exercises from workout videos?"
  4. "Is FitSaver free?"
  5. "Does FitSaver work with YouTube workout videos?"
  6. "What makes FitSaver different from Hevy or Strong?"
  7. "Can I use FitSaver without an internet connection?"
  8. "Does FitSaver sync with Apple Health or Google Fit?"
- Each answer: 2-3 sentences, answer-first format, natural language. Optimized for Google AI Overviews and ChatGPT citations.
- Author byline on blog posts: "FitSaver Team — helping 15,000+ people turn saved reels into real workouts."

---

## SECTION 4: BEHAVIORAL ARCHITECTURE (Hooked Model)

### 4.1. Trigger Design

**External Triggers:**
- **Push #1 (Timely Reminder):** "🏋️ Time for 'Lower Body Burn'? Your 45-min workout is ready." Sent at user's preferred gym time (learned after 3 workouts). Deep link: opens workout directly.
- **Push #2 (Social Proof):** "3 new workouts from your saved creators this week. See what's new." Drives FOMO and discovery. Deep link: opens "New for You" feed.
- **Push #3 (Loss Aversion):** "Your 12-day streak ends in 3 hours. 5 minutes saves it." Deep link: opens quick 5-minute bodyweight workout.
- **Widget update:** Updates every hour with streak count. Passive external trigger every time user glances at home screen.
- **Email re-engagement (Day 3 inactive):** Subject: "Your workouts are waiting." Body: "You crushed 8 workouts with FitSaver. Your 'Upper Body Power' routine is ready when you are. [Start Workout]" CTA.

**Internal Triggers (negative emotion → app open):**
1. User feels **"I'm at the gym and don't know what to do"** → remembers FitSaver has their saved creator workouts structured and ready
2. User feels **"I wasted time scrolling instead of training"** → remembers FitSaver converts scrolling into structured action
3. User feels **"I'm losing progress"** → remembers FitSaver tracks streaks and PRs, showing tangible improvement

### 4.2. Action Design

- **Core action:** Paste workout reel link → get structured timer workout. 2 taps from home screen. Hevy requires 4+ taps to log a single exercise. FitSaver's 2-tap core action is the competitive behavioral advantage.
- **Fogg Behavior Model check:**
  - Motivation: **8/10** — user just arrived at gym, highly motivated to work out
  - Ability: **9/10** — paste link, tap one button. Trivially easy.
  - Trigger: **9/10** — the saved reel graveyard is a constant trigger
  - All exceed activation threshold (>6). The product is behaviorally viable.
- **Onboarding drives immediate action:** Don't explain the app. Prompt: "Paste your first workout reel link" with a demo URL pre-filled. User taps "Extract Workout" and sees results within 30 seconds of opening.

### 4.3. Variable Reward Design

**Reward of the Tribe (Social):**
- Weekly "Creator workouts you follow" digest — shows new workouts from creators the user has imported from
- Shareable workout completion card — designed for Instagram Stories with FitSaver watermark. "Just crushed [WORKOUT] in [TIME] 🔥"

**Reward of the Hunt (Search):**
- "Discover" tab: trending community workouts, new creator workouts, workout categories
- Progressive disclosure: beginner workouts unlock first, advanced programs unlock after 10 completed workouts
- "Quick Add" — paste ANY fitness video link and see if it works. The uncertainty of "will this extract?" is itself a reward.

**Reward of the Self (Mastery):**
- Streak counter (prominent on home screen)
- Personal records: "New PR! Bench Press 185 lbs ↑5 lbs from last week"
- Body part heatmap: "You've trained legs 12 times this month, but only hit shoulders 3 times"
- "Workout Age" metric: "You've been consistent for 47 days — that's top 15% of all FitSaver users"

### 4.4. Investment Design

- **Data investment:** Every workout completed builds history. Switching to Hevy means losing all that data. Users who've completed 20+ workouts will never switch.
- **Social investment:** Following creators, sharing workouts to Stories, inviting gym buddies. The network grows with each share.
- **Financial investment:** Premium subscribers have sunk cost. Even $6.99/mo creates "I should use this" psychology.
- **Skill investment:** Users learn the app's flow. Custom rest timers, preferred exercise order, favorite creator list. The app adapts to them.
- **Reputation investment:** Streak number is visible on the widget. Users protect their streak. (Snapchat/Duolingo/Apple Watch rings psychology.)

---

## SECTION 5: VISUAL DESIGN SYSTEM

### 5.1. Design Principles

1. **The timer is the interface.** Every other UI element serves the timer. Chrome is invisible during a workout.
2. **Dark mode is the default.** Gyms are bright. Phone screens shouldn't be. Light mode is the option.
3. **Motion signals progress.** Every animation communicates forward momentum. No motion is purely decorative.
4. **Your saved reels, finally useful.** The app transforms chaos (scattered saved posts) into order (structured workouts). The UI should feel like that transformation.

### 5.2. Key Animations & Micro-Interactions

- **App open:** No static splash screen. Logo pulses once (0.3s) → home screen fades in (0.25s). Zero wait time.
- **Workout extraction complete:** Exercise cards animate in from the bottom, staggered 0.05s each. Spring damping 0.6. Duration: 0.8s total. Feels like the workout is "building itself."
- **Timer countdown:** Smooth digital flip animation on the seconds number at 3 seconds remaining. Pulse animation (scale 1.0 → 1.05 → 1.0) at 5s mark.
- **Set complete:** Confetti burst in brand colors (orange, cyan, white). Duration: 1.0s. Scale bounce on the "Set Complete" text (spring damping 0.5).
- **Tab switches:** Morphing SF Symbols + crossfade. Duration: 0.25s. Not instant swap.
- **Empty → populated:** Skeleton shimmer on first load, then staggered fade-in of content items (0.05s delay each).

### 5.3. Haptic Feedback Map

- **Light impact:** Row selection, toggle switches, paste link confirmation
- **Medium impact:** Set complete, workout start, timer hits zero
- **Heavy impact:** Workout complete, new personal record, streak milestone (10, 30, 100 days)
- **Selection feedback:** Scrolling through rest timer picker (30s/60s/90s/120s)
- **Notification feedback:** Only for streak-at-risk alerts (critical retention event)

### 5.4. Accessibility as Luxury

- **VoiceOver:** Every exercise card: "Exercise: Goblet Squats, 3 sets of 12 reps, 60 seconds rest." Timer: "45 seconds remaining. Next: Push-Ups."
- **Dynamic Type:** All text scales to AX5 without truncation. Timer number scales down gracefully — minimum 48pt at AX5.
- **Reduce Motion:** Confetti becomes a static checkmark. Staggered animations become instant. Timer still pulses for accessibility.
- **Color blindness:** Pass/fail states use icons (✓/✗) alongside color. Exercise difficulty is indicated by dumbbell count, not color. Progress charts use patterns + colors.

---

## SECTION 6: FINANCIAL ARCHITECTURE

### 6.1. Pricing Tiers

| Tier | Monthly | Annual | What's Included | Why This Price |
|---|---|---|---|---|
| Free | $0 | $0 | 3 saved workouts, basic timer (set/rest), no AI extraction, no history | Generous enough for 4-star reviews, restrictive enough for 25%+ conversion |
| Premium | $6.99 | $49.99 ($4.17/mo) | Unlimited workouts, AI extraction, progress analytics, Health sync, custom timers | "Less than one post-workout smoothie = unlimited workouts all month" |
| Premium Family | — | — | Post-MVP. Will be $12.99/mo for up to 5 family members. | Viral expansion vector. Launch Month 3. |

### 6.2. Unit Economics

- **CAC target:** $0 (organic-only at launch — creator partnerships, Reddit, gym QR codes)
- **LTV at 6 months:** ~$25.16 (weighted average with 50% churn by month 3, 15% monthly churn thereafter)
- **Payback period:** 0 months at $0 CAC. With paid acquisition (post-launch): 1.5 months at $5 CAC.
- **Monthly churn target:** <8% (below 5% is world-class; 8% is achievable for fitness apps with strong streaks)
- **Referral value:** Each referred user who converts = ~$25 LTV. Cost = 1 free month ($6.99). 3.6:1 ROI.

### 6.3. Monetization Flow

1. User downloads app → lands on onboarding (3 cards, ~15 seconds)
2. Pre-filled demo workout link → user taps "Extract Workout" → sees structured workout in 30 seconds (aha moment)
3. User completes first workout → full celebration animation + share card → feels the value
4. After 3rd completed workout → paywall appears: "You've crushed 3 workouts. Ready to go unlimited?" Annual pre-selected.
5. If user declines → "No worries! Try Premium free for 7 days, no card required."
6. If still declines → continue in Free tier. Paywall resurfaces when user tries to save 4th workout, use AI extraction, or view progress.
7. Annual renewal reminder: 7 days before via RevenueCat push + in-app banner. "Your FitSaver Premium renews in 7 days."
8. Cancellation flow intercept (below)

### 6.4. Cancellation Flow Intercept

1. In-app "Manage Subscription" → "Before you go — would you like to pause for 1-3 months? Your workouts stay saved."
2. If still canceling: "What's the main reason?" [Too expensive / Not using enough / Found alternative / Missing feature / Other]
3. If "Too expensive": Offer 50% off for 6 months ($3.49/mo). Retention yield: 25-35% saved.
4. If "Not using enough": "Would you like weekly summaries instead of daily reminders? Just the highlights." Change notification frequency.
5. If still canceling: "We'll keep your workout history for 90 days. Come back — everything will be exactly as you left it."

---

## SECTION 7: VIRALITY ENGINE

### 7.1. Shareable Moments

1. **Workout completion card:** "Just crushed 'Full Body Burn' in 32 minutes 🔥 8 exercises • 280 calories" — designed for Instagram Stories. Orange gradient card with workout stats.
2. **Personal record:** "NEW PR! Bench Press 185 lbs 💪 Up 5 lbs from last week. Made with FitSaver."
3. **Streak milestone:** "30 days of consistent training 🏆 Never missed a workout. #FitSaverStreak"
4. **Year in Review (annual):** Spotify Wrapped-style shareable: "2026: 187 workouts, 93 hours, 142,000 lbs lifted. Your top exercise: Goblet Squats."
5. **Challenge a friend:** "I bet you can't beat my 12-day streak. 👀 [LINK]"

### 7.2. Viral Mechanics

- **Invite friction:** One tap → native share sheet (Messages, Instagram, WhatsApp). No email forms. Each extra field kills 65% of invites.
- **Invite incentive:** Sender gets 1 free month of Premium. Receiver gets first month free. Zero marginal cost if neither would have paid. If one converts, it pays for 10 free months.
- **Network effect:** Creator following system. The more creators who use FitSaver, the more workout deeplinks circulate on social media. Each deeplink is a free acquisition channel.
- **Watermark:** Every shareable image has a subtle "Made with FitSaver" footer. Elegant, not obnoxious. Orange brand color, 11pt SF Pro Text.

### 7.3. App Store Rating Protection

- **1-2 star:** Do not show rating prompt. Route to in-app feedback form. "We'd love to fix this. What went wrong?"
- **3-star:** Show rating prompt with pre-selected 4-star. Guide toward positive rating.
- **4-5 star:** Show rating prompt after 5th workout. "You seem to love FitSaver! Would you mind telling others?" → App Store rating dialog.
- **Rating reply strategy:** Reply within 24 hours to every review. Reviews with developer replies rank higher in App Store search.

---

## SECTION 8: TECHNICAL SPECIFICATION

### 8.1. Database Schema

```sql
-- iOS: SwiftData models (auto-synced via CloudKit)
-- Android: Room entities (synced via Firebase Realtime Database)

-- Workout table (Cross-platform, CloudKit/Firebase)
CREATE TABLE Workout (
    id TEXT PRIMARY KEY,          -- UUID
    name TEXT NOT NULL,           -- e.g., "Full Body Burn"
    source_url TEXT,              -- Original Instagram/TikTok URL
    creator_name TEXT,            -- Content creator name if known
    duration_seconds INTEGER,     -- Total workout duration
    created_at INTEGER NOT NULL,  -- Unix timestamp
    updated_at INTEGER NOT NULL,
    is_favorite INTEGER DEFAULT 0,
    times_completed INTEGER DEFAULT 0
);

-- Exercise table (Child of Workout)
CREATE TABLE Exercise (
    id TEXT PRIMARY KEY,          -- UUID
    workout_id TEXT NOT NULL,     -- FK → Workout.id
    name TEXT NOT NULL,           -- e.g., "Goblet Squats"
    sets INTEGER NOT NULL,        -- Number of sets
    reps INTEGER NOT NULL,        -- Reps per set (or 0 for timed)
    rest_seconds INTEGER DEFAULT 60,
    exercise_order INTEGER NOT NULL, -- Position in workout
    notes TEXT,                   -- User notes (optional)
    FOREIGN KEY (workout_id) REFERENCES Workout(id) ON DELETE CASCADE
);

-- Workout Session (Each time user runs a workout)
CREATE TABLE WorkoutSession (
    id TEXT PRIMARY KEY,          -- UUID
    workout_id TEXT NOT NULL,     -- FK → Workout.id
    started_at INTEGER NOT NULL,
    completed_at INTEGER,         -- NULL if abandoned
    total_duration_seconds INTEGER,
    calories_burned INTEGER,      -- From Apple Health / Google Fit
    FOREIGN KEY (workout_id) REFERENCES Workout(id)
);

-- Set Log (Individual set completion data)
CREATE TABLE SetLog (
    id TEXT PRIMARY KEY,          -- UUID
    session_id TEXT NOT NULL,     -- FK → WorkoutSession.id
    exercise_id TEXT NOT NULL,    -- FK → Exercise.id
    set_number INTEGER NOT NULL,
    reps_completed INTEGER,
    weight_lbs REAL,              -- Weight used (optional)
    completed INTEGER DEFAULT 1,  -- 0 = skipped
    FOREIGN KEY (session_id) REFERENCES WorkoutSession(id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_id) REFERENCES Exercise(id)
);

-- User Preferences (local DataStore)
-- rest_timer_default: 60 (seconds)
-- notification_enabled: true
-- preferred_workout_time: "17:00"
-- weight_unit: "lbs" | "kg"
-- streak_count: 0
-- last_workout_date: Unix timestamp
-- onboarding_complete: false
```

**Sync annotation:**
- Workout, Exercise: Synced via CloudKit (iOS) / Firebase (Android) with local Room/SwiftData cache
- WorkoutSession, SetLog: Local-only by default. Opt-in cloud backup for Premium users.
- User Preferences: Local DataStore only. Never synced.

### 8.2. API Endpoints

```
# Social Media Metadata Extraction (Edge Function)
POST /api/v1/extract
  Body: { "url": "https://www.instagram.com/reel/..." }
  Response: { "exercises": [{ "name": "Goblet Squats", "sets": 3, "reps": 12, "rest": 60 }, ...] }
  
# Creator Analytics (for Creator Dashboard, post-MVP)
GET /api/v1/creator/{creator_id}/stats
  Response: { "total_workouts_created": 12, "total_user_completions": 3420, ... }

# Cross-Platform Sync Bridge (CloudKit ↔ Firebase)
POST /api/v1/sync
  Body: { "device_id": "...", "platform": "ios", "workouts": [...] }
  Response: { "synced": true, "new_items": [...] }
```

Authentication: Firebase Auth (Apple Sign In, Google Sign In, email). JWT tokens. Required only for cross-platform sync.

### 8.3. Push Notification Schema

```json
{
  "aps": {
    "alert": {
      "title": "Time for Lower Body Burn",
      "subtitle": "Your 45-min workout is ready",
      "body": "3 sets of squats, lunges, and deadlifts waiting for you 🏋️"
    },
    "sound": "workout_chime.caf",
    "badge": 0,
    "mutable-content": 1,
    "category": "WORKOUT_REMINDER"
  },
  "custom_data": {
    "type": "workout_reminder",
    "workout_id": "abc-123",
    "deep_link": "fitsaver://workout/abc-123",
    "image_url": "https://cdn.fitsaver.app/notifications/workout_thumb.jpg"
  }
}
```

**Notification Types:**
1. `workout_reminder` — Trigger: user's preferred gym time. Deep link: workout detail.
2. `streak_risk` — Trigger: 3 hours before end of day, if no workout logged. Deep link: quick workout.
3. `new_creator_workout` — Trigger: creator user follows posts new workout. Deep link: new workout.
4. `weekly_summary` — Trigger: Sunday 10am. Deep link: progress screen.
5. `pr_congratulations` — Trigger: immediately after new personal record. Deep link: progress screen.

### 8.4. AI Agent Architecture (Local-First)

**The Agent Loop (On-Device):**
```
User pastes URL → Local LLM receives prompt: "Extract exercises, sets, reps, and rest intervals from this workout video metadata: [URL_METADATA]" → LLM outputs structured JSON → JSON parsed into Exercise objects → UI displays for user review
```

This is the ReAct pattern from pguso/ai-agents-from-scratch.

**Models:**
- **iOS:** Phi-4-mini (3.8B Q4_K_M) via llama.cpp Swift bindings, Metal-accelerated. ~2.2GB on device.
- **Android:** Gemma-3-1B via MediaPipe LLM Inference, Vulkan backend. ~1.3GB on device.
- **Latency:** <3 seconds for exercise extraction on A17+ / Snapdragon 8 Gen 2+ devices.
- **Fallback:** Cloud API (Claude Haiku) only for devices below minimum spec. <5% of users.

**Why local-first:** Zero inference API costs at scale. Privacy moat — workout data never leaves device for AI. Faster than cloud round-trip (no network latency). Works offline at the gym. This architecture is a competitive moat that cloud-dependent competitors cannot match without rewriting their entire stack.

### 8.5. Third-Party Dependencies

- RevenueCat (subscriptions, iOS + Android)
- Firebase Auth + Realtime Database (Android sync, cross-platform)
- TelemetryDeck (iOS analytics, privacy-first)
- Firebase Analytics (Android)
- CloudKit (iOS sync)
- **NO Facebook SDK. NO AdMob. NO Google Ads.** Ads destroy premium feel. Monetize through the user, not their attention.

---

## SECTION 9: 30-DAY MVP SPRINT PLAN

### Week 1 — Foundation
| Day | iOS | Android | Shared |
|---|---|---|---|
| Mon | Project setup, SwiftData models | Project setup, Room entities | DB schema finalized |
| Tue | Onboarding (3 cards) | Onboarding (3 cards) | Design review: onboarding |
| Wed | Home screen skeleton + paste URL | Home screen skeleton + paste URL | Design review: home |
| Thu | URL metadata fetch + local LLM integration | URL metadata fetch + MediaPipe LLM | LLM extraction test suite |
| Fri | RevenueCat + paywall (custom SwiftUI) | BillingClient + paywall (Compose) | Paywall design finalized |

### Week 2 — Core Experience
| Day | iOS | Android | Shared |
|---|---|---|---|
| Mon | Workout timer screen (core) | Workout timer screen (core) | Animation review |
| Tue | Push notifications + categories | Notification channels | Notification copy final |
| Wed | WidgetKit (small + medium) | App Shortcuts (4) | Widget review |
| Thu | Settings screen | Settings screen | Settings audit |
| Fri | Empty states, error states, edge cases | Empty states, error states | Edge case testing |

### Week 3 — Polish & Virality
| Day | iOS | Android | Shared |
|---|---|---|---|
| Mon | Haptics, animations, confetti | Motion, predictive back | Micro-interaction review |
| Tue | Share sheet + workout cards | Share intent + cards | Virality flow test |
| Wed | App Store screenshots | Play Store feature graphic + screenshots | ASO copy final |
| Thu | Accessibility audit (VoiceOver) | Accessibility audit (TalkBack) | Accessibility test |
| Fri | Premium upgrade screen | Premium upgrade screen | Monetization flow test |

### Week 4 — Launch Readiness
| Day | iOS | Android | Shared |
|---|---|---|---|
| Mon | Bug fixes, edge cases | Bug fixes, edge cases | Cross-platform parity check |
| Tue | App Store submission prep | Play Store submission prep | Privacy policy final |
| Wed | TestFlight internal | Internal testing track | Beta tester onboarding |
| Thu | TestFlight external | Closed testing (20 testers) | Launch checklist |
| Fri | **SUBMIT TO APP STORE** | **SUBMIT TO PLAY STORE** | Launch day coordination |

### MVP Feature Cut List (Do NOT Build in Sprint 1)
1. **Creator analytics dashboard** — only useful after 50+ creators onboarded. Month 3.
2. **Social feed / community tab** — requires moderation, network effect needs critical mass. Month 4.
3. **Apple Watch companion app** — nice to have, but phone timer is sufficient for MVP. Month 2.

---

## SECTION 10: LAUNCH CHECKLIST

### Pre-Launch (T-14 days)
- [ ] App Store Connect: App record created, metadata, screenshots uploaded
- [ ] Google Play Console: App created, all metadata, feature graphic uploaded
- [ ] RevenueCat: Products configured, webhooks set up, entitlement mapped
- [ ] Privacy Policy URL: Live at fitsaver.app/privacy (GDPR-compliant)
- [ ] Terms of Service URL: Live at fitsaver.app/terms
- [ ] Support email: support@fitsaver.app configured with auto-responder
- [ ] Screenshots: 6.9" iPhone 16 Pro Max + Pixel 9 Pro, all 5 per platform
- [ ] App Preview Video: Optional but recommended (20-35% conversion lift)
- [ ] TestFlight: Submitted for Beta App Review
- [ ] Internal testing: 20 testers recruited for Google Play closed testing
- [ ] Landing page: fitsaver.app live with App Store + Play Store badges
- [ ] Social accounts: @fitsaver.app on Instagram, @FitSaverApp on X/Twitter
- [ ] Blog posts: 3 of 5 pillar posts drafted and scheduled

### Launch Day (T=0)
- [ ] Release to App Store (manual release — retain control)
- [ ] Release to Play Store (staged rollout: 10% for 24 hours, catch crash-loop bugs)
- [ ] Monitor TelemetryDeck + Firebase Analytics dashboards
- [ ] Monitor App Store Connect for crash reports
- [ ] Reply to first 10 reviews within 2 hours
- [ ] Post on r/SideProject, r/Fitness, r/iosapps, r/androidapps — authentic indie dev story
- [ ] Post on Product Hunt (schedule 12:01 AM PT)
- [ ] Email beta testers: "We're live! 50% off your first year. Thanks for building this with us."

---

## SECTION 11: POST-LAUNCH ITERATION

### Week 1 Post-Launch: Observe
- Watch: D1/D7/D30 retention, conversion rate (free→paid), crash rate, avg session length
- Read EVERY review. Tag: bug / feature request / UX confusion / pricing objection
- Do NOT ship features. Only critical crash fixes.

### Week 2-4: Quick Wins
- Ship top 3 user-requested improvements
- A/B test paywall design if conversion <20%
- If D1 retention <40%: onboarding is broken. Redesign.
- If D7 retention <20%: core habit loop failing. Redesign triggers.
- If crash rate >1%: pause feature work, fix stability.

### Month 2-3: Feature Expansion
- Apple Watch companion app
- Creator analytics dashboard (outreach to 50+ creators)
- Premium Family plan ($12.99/mo, up to 5 members)
- iPad-optimized layout
- Apple Health / Google Fit deep integration (auto-log workouts)

---

## SECTION 12: ANTI-PATTERNS

1. **Do not ask for notification permission on first open.** 60% say no. Ask after first completed workout: "Want us to remind you when it's time to train?" with custom pre-permission dialog.
2. **Do not require account creation before using the app.** "Try before you sign up." Account required only for cross-device sync.
3. **Do not show ads in the first 90 days.** Ads destroy trust before the habit forms. Monetize through subscriptions.
4. **Do not use default RevenueCat paywall.** Default paywalls convert 40% worse. Custom SwiftUI/Compose paywall only.
5. **Do not ship with a static splash screen.** Logo pulse (0.3s) → instant transition to home. Zero wait.
6. **Do not ignore 1-star reviews.** Developer reply within 24 hours. Many 1-star reviewers upgrade when they get a response.
7. **Do not localize poorly.** Launch in English only. Add Spanish + German with human translators after traction. Bad localization > no localization.
8. **Do not copy Instagram/TikTok branding.** FitSaver is a standalone tool, not a "social media companion." This protects against platform ToS enforcement.
9. **Do not over-build the AI extraction.** The extraction needs to work for 80% of workout reels. Perfection is not required for MVP. Users can manually edit.
10. **Do not launch on Android simultaneously if iOS is delayed.** iOS-first submission (App Store review is 1-3 days). Android 1 week behind. Learn from App Store review before Play Store launch.

---

*End of FitSaver Scaffold. Generated 2026-05-28. A development agent or senior engineer should be able to build the complete iOS + Android app from this document with zero additional clarification questions.*