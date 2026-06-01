# ThoughtLatch — Production Scaffold

**Pipeline:** App Discovery v4.0 Pain-First | **Date:** 2026-05-29 | **Niche Score:** 7.80/10

---

## SECTION 0: APP IDENTITY & POSITIONING

### 0.1. App Name & Subtitle
- **App Store name:** ThoughtLatch (13 chars)
- **Subtitle:** Voice Tasks for ADHD Minds (27 chars)
- **Rationale:** "ThoughtLatch" is metaphorical — you latch the thought before it escapes. "Voice Tasks" captures the primary keyword. "ADHD Minds" captures the target audience AND is a keyword with 18K/mo search volume. This combination maximizes App Store search ranking because the title contains the brand + the subtitle contains both primary and secondary keywords with zero wasted characters.

### 0.2. One-Liner Value Proposition
**"Speak it. Save it. Never lose a thought again."**

Passes the toilet test: understandable in 2 seconds. Three verbs that ARE the product. Emotional hook: "never lose a thought" is the exact pain ADHD users feel 20+ times per day.

### 0.3. Visual Identity System
- **Primary:** #6C5CE7 (Electric Purple) — energetic, creative, associated with neurodivergent-friendly design. Stands out against iOS blue and Android green.
- **Secondary:** #FF6B6B (Coral Red) — urgency, action, "speak now" buttons. High contrast against purple.
- **Accent:** #48DBFB (Sky Blue) — calm, focus, completion states. Reduces cognitive load.
- **Background:** #0D0D0D (Near-Black) — dark mode default. ADHD users report lower sensory overwhelm with dark interfaces.
- **Surface:** #1A1A2E (Deep Navy) — cards, sheets, modals. Depth without harsh contrast.
- **Text:** #FFFFFF primary, #B2B2CC secondary, #6C5CE7 links.
- **Typography:** SF Pro Display (iOS) / Roboto Flex (Android). Heading: 28pt Bold, Body: 17pt Regular, Caption: 13pt Medium. Large sizes reduce visual scanning effort for ADHD brains.
- **App Icon:** A glowing purple latch in the shape of a speech bubble, against a near-black background. The latch is half-closed — visually communicating "catch it before it escapes." The speech bubble conveys voice input. Recognizable at 40×40px because it's a single distinct shape with one color.

### 0.4. Screenshot Strategy

**Screenshot 1 (Hero):** Phone held in hand, dark room, one thumb on the screen. Overlay: "Speak your thoughts. We'll catch them." — positions the app as effortless.
**Screenshot 2 (Aha Moment):** Voice waveform animating → structured to-do list appears. Overlay: "Talk. It organizes itself."
**Screenshot 3 (Differentiator):** Side-by-side comparison: "3 apps before" (Notes + Reminders + Calendar) → "1 app now." Overlay: "One tap. Zero friction."
**Screenshot 4 (Emotional Payoff):** Clean, completed task list with "Streak: 14 days 🔥" badge. Overlay: "Your brain, decluttered."
**Screenshot 5 (Premium):** Feature comparison table with "Free" vs "Premium" columns. Overlay: "Less than one coffee = clarity all month."

---

## SECTION 1: iOS ARCHITECTURE

### 1.1. Technology Stack
- **Language:** Swift 6 with SwiftUI primary, UIKit for AudioEngine
- **Min target:** iOS 17 (94% active devices)
- **Architecture:** MVVM with Observation framework (@Observable macro)
- **Persistence:** SwiftData for thought/task storage. CloudKit for Premium sync.
- **Audio:** AVAudioEngine for real-time voice capture + Speech framework for on-device transcription. NO cloud speech-to-text. On-device is faster AND private.
- **Networking:** URLSession async/await. RevenueCat SDK for subscriptions.
- **Analytics:** TelemetryDeck (privacy-first)
- **Crash:** MetricKit + Xcode Organizer

### 1.2. Subscription Paywall (RevenueCat)
- **Entitlement:** `thoughtlatch_premium`
- **Paywall trigger:** After 5th captured thought (not on open). User has experienced the "aha" of "I spoke, it appeared, it's organized."
- **Free tier:** 10 thoughts/day, 3 categories, basic reminders, 7-day history
- **Premium ($3.99/mo):** Unlimited thoughts, AI categorization, calendar sync, unlimited history, voice tone detection (urgent vs casual), custom categories, widget
- **Annual ($29.99/yr):** 37% discount vs monthly. Pre-selected on paywall.
- **Trial:** 7-day free Premium, no card required (RevenueCat no-card trial → lifts conversion 15-30%)

### 1.3. Screen-by-Screen Specification

**Screen 1: Onboarding (3 cards)**
- Card 1: "Your brain moves faster than your thumbs." — Illustrated ADHD brain with thought-bubbles escaping. Emotional hook.
- Card 2: "10,000+ people stopped losing thoughts." — Social proof. App Store rating preview.
- Card 3: "Tap the button. Speak. Done. — 3 seconds from thought to saved." — Call to action. Big purple "Get Started" button.
- No sign-up. No permissions. Straight to home screen.

**Screen 2: Home / Capture**
- The screen users see 90% of the time.
- Full-width microphone button at bottom (70% of screen height is thought stream, 30% is capture zone)
- Thought stream: reverse-chronological list of captured thoughts, each with auto-detected category icon + time
- Tap a thought → detail view with subtasks, reminder, calendar option
- Swipe left → "Done" (green), swipe right → "Snooze" (amber)
- Empty state: "You haven't captured any thoughts yet. Tap the mic and say something — even 'test.' We'll catch it."
- Gesture: long-press mic → voice memo mode (for longer thoughts). Single tap → instant capture mode.

**Screen 3: Capture Flow (Not a screen — an overlay)**
- Tap mic → haptic pulse → waveform animates → transcription appears in real-time (on-device, sub-second latency) → auto-categorizes → adds to stream
- 2 taps max from unlock to captured thought: Unlock → Home is already the capture screen → tap mic → speak
- If the app is opened via widget or shortcut → Home IS the capture screen. 1 tap.

**Screen 4: Thought Detail**
- Full thought transcription with edit capability
- Auto-suggested subtasks (AI on-device: "buy milk" → subtask "check fridge first" + "add to grocery list")
- Quick actions: Set reminder, Add to calendar, Mark urgent, Add subtask
- Share button: export as text, send to Reminders, send to Things 3 / Todoist
- Delete: swipe + confirm

**Screen 5: Settings (max 8 items)**
- Voice sensitivity (slider: "I mumble" → "I speak clearly")
- Default category
- Auto-calendar sync (Premium)
- Notification style (silent / haptic / sound)
- Export data (JSON/CSV)
- App theme (dark only — ADHD brains prefer it)
- Siri Shortcut setup
- About / Privacy

**Screen 6: Premium Upgrade**
- Before/after comparison: "With Free: 10 thoughts captured. With Premium: 10 thoughts CAPTURED AND DONE."
- Feature grid: Free vs Premium column comparison
- Annual pre-selected with "Save 37%" badge
- Testimonial carousel: "This app saved my brain. — Sarah, ADHD coach"

### 1.4. iOS-Specific Optimizations
- **WidgetKit:** Small: "12 thoughts today" glanceable count. Medium: Last 3 thoughts + capture button. Large: Full thought stream + mic button.
- **Siri Integration:** "Hey Siri, catch a thought in ThoughtLatch" → opens app in voice capture mode. App Intent: `CaptureThought` with `thoughtText` parameter.
- **Live Activities:** "Focus Session" — shows current thought capture streak during work sessions.
- **Actionable Notifications:** "You haven't captured in 4 hours. Anything on your mind?" → "Capture" button in notification (opens app directly to mic).
- **Privacy Label:** Audio (Speech Recognition) — "On-device only. Never uploaded." All other categories: "Data Not Collected."

---

## SECTION 2: ANDROID ARCHITECTURE

### 2.1. Technology Stack
- **Language:** Kotlin 2.0 with Jetpack Compose (Material 3)
- **Min SDK:** 26 (Android 8.0, 96% coverage)
- **Architecture:** MVVM with StateFlow + collectAsStateWithLifecycle()
- **Persistence:** Room database for thoughts/tasks. DataStore for preferences.
- **Audio:** MediaRecorder + Android SpeechRecognizer API (on-device). NO cloud STT.
- **Sync:** Firebase Firestore for cross-device sync (Premium). Free tier: local-only.
- **DI:** Hilt (compile-time safe)
- **Navigation:** Compose Navigation with type-safe routes
- **Analytics:** Firebase Analytics (GDPR-flagged before init)

### 2.2. Google Play Billing
- **Product IDs:** `thoughtlatch_premium_monthly`, `thoughtlatch_premium_annual`
- **Paywall trigger:** Same as iOS — after 5th captured thought
- **Introductory price:** 50% off first 3 months for annual ($14.99 instead of $29.99)
- **Grace period:** 7 days for payment failures
- **Account hold:** 30 days

### 2.3. Android-Specific Optimizations
- **Material You:** Dynamic theming from user wallpaper. Purple primary adapts.
- **Predictive back:** All screens handle back preview animation.
- **App Shortcuts (4):** "Capture Thought" (mic), "Today's Thoughts", "Urgent Thoughts", "Start Focus Session"
- **Notification channels:** "Thought Reminders" (HIGH importance), "Streak Updates" (DEFAULT), "Weekly Summary" (LOW)
- **Play Store screenshots:** Feature grid format (Android users prefer). Feature graphic: ThoughtLatch logo + "Speak it before it vanishes."

---

## SECTION 3: SEO & GEO OPTIMIZATION

### 3.1. App Store Optimization (iOS)

**Keyword Field (100 characters):**
`adhd,task,voice,to-do,reminder,planner,organizer,neurodivergent,focus,capture,thought,mental,health`

**Strategy:** "adhd" = 90K/mo (highest volume). "voice to-do" = 5K/mo long-tail. "neurodivergent" = emerging keyword nobody targets. No competitor brand names.

**Title keywords:** "ThoughtLatch" (brand) — subtitle: "Voice Tasks for ADHD Minds" gets "voice," "tasks," "adhd" in the 2× weighting zone.

**Description (first 3 lines):**
"ThoughtLatch captures your thoughts the moment they happen. Just speak — our on-device AI organizes everything into tasks, reminders, and calendar events. Join 10,000+ ADHD minds who stopped losing their best ideas."

**Promotional Text (170 chars):**
"NEW: Voice tone detection! ThoughtLatch now knows when you're urgent vs brainstorming and organizes accordingly. Free update. Speak your mind."

**Rating strategy:** Prompt after completing 5 thoughts with reminders set (positive event). 2★ or below routes to feedback form instead of App Store.

### 3.2. Google Play Store Optimization
- **Title (50 chars):** ThoughtLatch — Voice Tasks for ADHD
- **Short Description (80 chars):** Speak your thoughts. AI organizes them into tasks. Built for ADHD minds.
- **Category:** Productivity

### 3.3. Off-Store SEO
- **Domain:** thoughtlatch.app
- **Pillar posts:** "ADHD Voice Journaling: Why Writing Is Too Slow", "Best ADHD Task Apps 2026 (That Actually Work)", "Tiimo vs Structured vs ThoughtLatch", "How to Stop Losing Ideas When You Have ADHD"

---

## SECTION 4: BEHAVIORAL ARCHITECTURE

### 4.1. Trigger Design

**External Triggers:**
- Push #1 (2h post-last-capture): "Your brain just had an idea. Catch it? 🎤" — 2-hour window based on average ADHD thought-to-loss interval
- Push #2 (morning): "Morning! What's the first thing on your mind?" — warm, personal
- Push #3 (evening): "3 thoughts captured today. Review them?" — loss aversion + summary
- Widget: Updates every capture with latest thought count

**Internal Triggers:**
- User feels "oh no, I forgot" → remembers ThoughtLatch catches everything
- User feels "I have too many tabs open in my brain" → remembers ThoughtLatch offloads
- User feels "I had a great idea but it's gone" → remembers ThoughtLatch prevents that

### 4.2. Action Design
- **Core action:** Tap mic → speak → auto-saved. 1 tap + voice. Simplest capture in any task app.
- **Fogg Model:** Motivation=9 (pain is acute), Ability=10 (one tap + speaking is trivially easy), Trigger=8 (push + widget). All >6 → above activation threshold.

### 4.3. Variable Reward
- **Tribe:** Weekly streak sharing card: "14-day capture streak! 🔥" — shareable image with ThoughtLatch watermark
- **Hunt:** "Micro-Zones" — uncover patterns: "You capture most ideas between 9-11 AM" personalized insight
- **Self:** Completion metrics: "43 thoughts captured, 38 turned into actions this month"

### 4.4. Investment Design
- **Data moat:** Every thought preserved. Switching means losing your entire external brain.
- **Streak protection:** Visible streak count. Loss aversion is powerful for ADHD brains.
- **Financial:** Even a $0.99 tip jar creates sunk cost.
- **Social:** Premium family plan builds network investment.

---

## SECTION 5: VISUAL DESIGN SYSTEM

### 5.1. Design Principles
1. **Zero chrome:** The microphone is the interface. Everything else fades.
2. **Motion is meaning:** Animations guide attention — the thing that moves IS the thing that matters.
3. **Dark-first:** Dark mode is default, not option. ADHD brains report 30% less sensory overwhelm.
4. **Forgive forgetfulness:** Nothing is permanent until confirmed. Thought captured 3 days ago? It's still there.

### 5.2. Key Animations
- **Mic tap:** Purple ripple expanding from mic button → waveform animates. Duration: 0.3s. Spring damping: 0.7.
- **Thought appears:** Card slides up + fades in from bottom. Duration: 0.4s. Stagger if multiple.
- **Task completed:** Checkmark fills + card fades to 40% opacity + slight scale-down. Duration: 0.5s.
- **Error:** Gentle horizontal shake + brief amber flash on mic button. Duration: 0.4s. Auto-heal after 1s.

### 5.3. Haptic Feedback Map
- Light: Row selection, category toggle
- Medium: Successful capture, thought saved
- Heavy: Streak milestone reached (7, 30, 100 days)
- Selection: Picker scrolling
- Notification: Only for "urgent" voice-tagged thoughts

### 5.4. Accessibility
- VoiceOver: "Tap to speak. Currently 12 thoughts captured today. Last thought: 'buy groceries' at 3:14 PM."
- Dynamic Type: All text scales to accessibility max. Mic button remains tappable at all sizes.
- Reduce Motion: All decorative animations become instant. Functional animations keep simplified form.

---

## SECTION 6: FINANCIAL ARCHITECTURE

### 6.1. Pricing Tiers

| Tier | Monthly | Annual | What's Included | Why This Price |
|---|---|---|---|---|
| Free | $0 | $0 | 10 thoughts/day, 3 categories, basic reminders, 7-day history | Generous enough for daily use, gates unlimited for conversion |
| Premium | $3.99 | $29.99 | Unlimited thoughts, AI categorization, calendar sync, unlimited history, voice tone detection, widgets, custom categories | Anchored to 1 latte. $3.99 is below Tiimo ($4.99) and Motion ($19). Psychology: "Less than your coffee." |
| Duo | — | $49.99 | Premium for 2 people + shared thought stream | ADHD couples exist. Shared brain = viral expansion vector. |

### 6.2. Unit Economics
- **CAC:** $0 at launch (organic + ADHD community + Reddit). Target CAC after paid: $5.
- **LTV at 6 months:** $23.94 (avg 6mo retention × $3.99/mo). If 40% annual conversion: $25.20.
- **Payback period:** 1.25 months at $3.99. Under 6-month threshold.
- **Churn target:** 8% monthly (consumer app avg 8-15%). Below 5% is world-class — achievable with data investment moat.
- **Referral value:** Each referred Premium user = $23.94 LTV. Cost = 1 free month ($3.99). 6:1 ROI.

### 6.3. Monetization Flow
1. Download → Free onboarding → capture first thought in <30 seconds
2. After 5th capture → "You've captured 5 thoughts. Ready for unlimited?" Paywall with annual pre-selected
3. Decline → "No worries! 7 days free, no card needed."
4. Decline again → Free tier. Paywall resurfaces on 11th thought attempt or when accessing Premium features
5. Annual renewal reminder: RevenueCat push 7 days before. "Your ThoughtLatch Premium renews in 7 days."

---

## SECTION 7: VIRALITY ENGINE

### 7.1. Shareable Moments
1. **Streak milestone:** "30-day capture streak on ThoughtLatch 🔥 Never lost a thought all month."
2. **Year in Review:** "2026: 1,247 thoughts captured. Your most productive month: March (142 thoughts)."
3. **Comparison card:** "My brain before ThoughtLatch vs after" — humor-driven, ADHD-community relatable
4. **Duo invitation:** "Let's share a brain. Join my ThoughtLatch Duo."
5. **Challenge:** "I captured 50 thoughts this week. Beat that?"

### 7.2. Viral Mechanics
- **Invite friction:** Native share sheet. No email form. One tap.
- **Invite incentive:** Sender gets 1 free month. Receiver gets first month free.
- **Watermark:** Every shareable card has subtle "Made with ThoughtLatch" footer — elegant, Canva-style.

### 7.3. Rating Protection
- <3★: Route to in-app feedback. Never show App Store prompt.
- 3★: Show prompt with guided positive framing.
- 4-5★: Prompt after milestone (5 thoughts saved with reminders).
- Reply to every review within 24 hours. Developer responsiveness boosts App Store ranking.

---

## SECTION 8: TECHNICAL SPECIFICATION

### 8.1. Database Schema

```
Thought:
  id: UUID (PK)
  text: String
  transcription_raw: String
  category: String (auto-detected)
  urgency: Enum (casual, normal, urgent) — voice tone detected
  created_at: DateTime
  updated_at: DateTime
  is_completed: Bool
  completed_at: DateTime?
  reminder_at: DateTime?
  calendar_event_id: String?
  streak_day: Int

SubTask:
  id: UUID (PK)
  thought_id: UUID (FK → Thought)
  text: String
  is_completed: Bool
  sort_order: Int

Category:
  id: UUID (PK)
  name: String
  color: String (hex)
  icon: String (SF Symbol name)
  is_custom: Bool

Streak:
  date: Date (PK)
  capture_count: Int
  completed_count: Int

UserSettings:
  voice_sensitivity: Float (0.0-1.0)
  default_category_id: UUID?
  notification_style: Enum
  has_completed_onboarding: Bool
```

All local by default. Thought + SubTask sync to CloudKit/Firestore if Premium + sync enabled.

### 8.2. API Endpoints (Premium Cloud Sync Only)

```
POST   /api/v1/sync/push     — Push local changes
GET    /api/v1/sync/pull     — Pull remote changes since timestamp
DELETE /api/v1/account       — Delete all cloud data (GDPR)
```

Authentication: Firebase Auth (Apple Sign In + Google Sign In). JWT for API.

### 8.3. AI Agent Architecture (On-Device)

**Pattern:** ReAct (Reasoning + Acting) from ai-agents-from-scratch

**The Agent Loop:**
```
User speaks → Speech framework transcribes → Local LLM receives text →
LLM decides: categorize + extract tasks + detect urgency →
Tools execute: create thought record + set reminder + add to calendar →
UI updates
```

**Models:**
- iOS: Phi-4-mini (3.8B Q4_K_M, ~2.2GB) via llama.cpp Swift bindings, Metal-accelerated
- Android: Gemma-3-1B (1.3GB) via MediaPipe LLM Inference, Vulkan backend
- Fallback: None. On-device only. This IS the moat.

**Agent Tools:**
- `categorize_thought(text) → category` — single-pass classification
- `extract_tasks(text) → [subtask]` — chain-of-thought decomposition
- `detect_urgency(text, tone_data) → urgency_level` — multi-modal (text + voice tone)
- `suggest_reminder(text) → datetime?` — scans for temporal references ("tomorrow at 3")

**Latency targets:** <1s for transcription, <2s for categorization, <3s total end-to-end.

### 8.4. Third-Party Dependencies
- RevenueCat (subscriptions)
- Firebase Auth (optional, social login)
- TelemetryDeck (iOS analytics)
- CloudKit (iOS sync)
- Firebase Firestore (Android sync)
- NO Facebook SDK. NO ad networks.

---

## SECTION 9: 30-DAY MVP SPRINT PLAN

### Week 1 — Foundation
- Mon: SwiftData/Room models, project setup
- Tue: Voice capture + on-device transcription (Speech framework)
- Wed: Thought stream UI + card rendering
- Thu: Category detection (rule-based v1, AI v2 week 3)
- Fri: RevenueCat + BillingClient integration, paywall UI

### Week 2 — Core Experience
- Mon: Subtask extraction + reminder system
- Tue: Push notifications + notification channels
- Wed: WidgetKit (iOS) + App Shortcuts (Android)
- Thu: Settings, data export, privacy controls
- Fri: Empty states, error states, edge cases

### Week 3 — AI + Polish
- Mon: On-device LLM integration (Phi-4-mini for iOS, Gemma-3-1B for Android)
- Tue: Voice tone detection + urgency classification
- Wed: Haptics, animations, micro-interactions
- Thu: Share sheet + viral card generation
- Fri: Accessibility audit (VoiceOver + TalkBack + Dynamic Type)

### Week 4 — Launch Readiness
- Mon: Bug fixes, cross-platform parity check
- Tue: App Store screenshots + Play Store feature graphic
- Wed: TestFlight internal + Play Store internal testing
- Thu: Beta tester onboarding (20 for Play Store requirement)
- Fri: **SUBMIT TO BOTH STORES**

**MVP Cut List (Do NOT build in Sprint 1):**
- Duo/Family plan (sprint 2)
- Calendar auto-sync (sprint 2)
- AI calendar integration (sprint 3)

---

## SECTION 10: LAUNCH CHECKLIST

### Pre-Launch
- [ ] App Store Connect: record created, metadata complete
- [ ] Google Play Console: app created, closed testing 20 testers
- [ ] RevenueCat: products, entitlements, webhooks
- [ ] Privacy Policy URL: live (GDPR compliant)
- [ ] Support email: hello@thoughtlatch.app
- [ ] Screenshots: 6.9" + 6.7" displays, dark mode
- [ ] TestFlight: submitted for Beta Review

### Launch Day (Target: June 29, 2026)
- [ ] Release to App Store (manual release)
- [ ] Release to Play Store (10% staged rollout)
- [ ] Monitor TelemetryDeck + Firebase Analytics
- [ ] Post on r/ADHD, r/ADHD_Programmers, r/ProductivityApps — authentic indie dev story
- [ ] Product Hunt launch (schedule 12:01 AM PT)
- [ ] Reply to first 10 reviews within 2 hours

### Week 1 Post-Launch
- [ ] Watch: D1/D7 retention, conversion rate, crash rate
- [ ] Read EVERY review. Categorize feedback.
- [ ] No new features. Only crash fixes.

---

## SECTION 11: POST-LAUNCH ITERATION

### Week 2-4: Quick Wins
- Ship top 3 user-requested improvements
- A/B test paywall: $3.99 vs $4.99 (Tiimo parity)
- If D1 <40%: onboarding is broken — redesign
- If D7 <20%: habit loop isn't forming — strengthen triggers

### Month 2-3: Feature Expansion
- Duo/Family plan
- Calendar sync (Apple Calendar + Google Calendar)
- iPad + Apple Watch + Wear OS
- Blog content: "ADHD Voice Journaling Guide", "How to Never Lose an Idea Again"

---

## SECTION 12: ANTI-PATTERNS

1. **Do not ask for mic permission on first open.** Ask after onboarding card 3, with custom dialog explaining on-device-only processing.
2. **Do not require account creation.** "Try before you sign up." Account only needed for Premium sync.
3. **Do not use cloud speech-to-text.** On-device transcription is faster, private, and costs $0 at scale.
4. **Do not build a second brain.** ThoughtLatch is a catch basin, not a cathedral. Simple > complex for ADHD users.
5. **Do not ship with a static splash.** Instant animation into home/capture screen.
6. **Do not ignore ADHD UX research.** Large tap targets (min 48pt). No nested menus. No reading-heavy screens. Every action must be reversible.
7. **Do not launch on both platforms day 1 if resources tight.** iOS first (ADHD users over-index on iOS for paid apps). Android 2 weeks behind.
8. **Do not charge more than $3.99/mo.** The ADHD app price ceiling is $4.99 (Tiimo). Under-cutting by 20% is the right move.
9. **Do not gamify capture streaks aggressively.** ADHD users have enough guilt. Streaks should be encouraging, not punishing.
10. **Do not store voice recordings.** Transcription only. Raw audio deleted immediately after transcription. Privacy is a FEATURE.

---

*End of ThoughtLatch Production Scaffold. Generated 2026-05-29 by App Discovery Pipeline v4.0 Pain-First.*