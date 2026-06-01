# Hearthly — App Scaffold

**Date:** 2026-05-28  
**Pipeline:** App Discovery Daily  
**Niche:** Family AI Organizer (NARROW gap)  
**Winner score:** 7.4/10  
**Scaffold version:** v1.0  

---

## SECTION 0: APP IDENTITY & POSITIONING

### 0.1. App Name & Subtitle (ASO-Optimized)
- **App Store name:** Hearthly – Family AI Organizer (30 chars)
- **Subtitle:** Calendar, Chores & Meal Plans (30 chars)
- **Rationale:** "Family AI Organizer" = primary keyword. "Calendar, Chores & Meal Plans" = three highest-volume secondary keywords in one subtitle. Every word earns its place.

### 0.2. One-Liner Value Proposition
"Your family's brain, without the mental load."

### 0.3. Visual Identity System
- **Color palette:**
  - Primary: `#FF6B35` (warm hearth orange — approachability, energy, family warmth)
  - Secondary: `#2D3142` (deep slate — trust, stability, contrast surface)
  - Accent: `#4ECDC4` (teal — calm, clarity, AI-assistant personality)
  - Background: `#F7F5F0` (warm cream — soft, paper-like, reduces eye strain)
  - Error: `#E15554` (muted red — clear but not alarming)
- **Typography:** SF Pro (iOS) / Roboto (Android). H1: 28pt bold, H2: 22pt semibold, Body: 16pt regular, Caption: 13pt
- **Iconography:** Custom line-art family silhouettes + hearth/fire motif. 10 icons: calendar, grocery cart, pot/meal, checkmark, bell, family group, photo, voice mic, timer/clock, settings gear.
- **App Icon:** A warm orange hearth/fireplace shape with a subtle family silhouette inside. White 2px border. Recognizable at 40×40px — reads as "home/family" instantly.

### 0.4. Screenshot Strategy
1. **Hero:** "Your family's brain." — Home dashboard showing today's view with calendar + task + meal all visible
2. **Core Action:** Voice capture — "Just say it: 'Soccer practice Tuesday 5pm'" — microphone UI
3. **Key Differentiator:** AI meal planning from fridge photo — before/after of mess → organized grocery list
4. **Before/After:** "Sunday chaos → Sunday calm" — cluttered sticky notes vs clean Hearthly dashboard
5. **Premium:** "Premium: Unlimited AI, shared voice journals, family insights"

---

## SECTION 1: iOS ARCHITECTURE

### 1.1. Technology Stack
- **Language:** Swift 6, SwiftUI primary, UIKit where Apple hasn't caught up
- **Minimum target:** iOS 17 (94% coverage)
- **Architecture:** MVVM with Observation framework. Actor-based concurrency for AI pipeline.
- **Persistence:** SwiftData (local) + CloudKit (free family sync, no server costs at launch)
- **Networking:** URLSession async/await. On-device AI via Core ML.
- **Analytics:** TelemetryDeck (privacy-first, no IDFA)
- **Crash reporting:** Xcode Organizer + MetricKit

### 1.2. Subscription Paywall (RevenueCat)
- **Paywall trigger:** After first fully successful "say it → it's organized" loop (value moment)
- **Free tier:** 1 family group (up to 4 members), shared calendar, 10 AI events/month, 3 AI meal plans/month, basic chore tracking
- **Premium tier ($4.99/month):** Unlimited families, unlimited AI events & meals, photo-to-calendar, voice journals, family insights dashboard, custom chore rewards, priority widget updates
- **Annual ($39.99/year):** 33% discount vs monthly
- **Trial:** 7-day free trial, no card required (RevenueCat no-card trial)
- **Paywall design:** Custom SwiftUI view — warm family photo background, feature grid, annual pre-selected

### 1.3. Screen-by-Screen Specification

**Onboarding (3 cards):**
1. "The mental load is real." — emotional hook: remembering everyone's everything is exhausting
2. "1,281 parents told us: 'I need one place for everything.'" — social proof
3. "You're 30 seconds from a calmer home." — value promise

**Home Dashboard:**
- Today's agenda (chronological, color-coded by family member)
- Pending chores with assignee avatars
- Tonight's meal preview + one-tap "Get Groceries"
- Voice capture FAB (floating action button) bottom center
- Pull-down: week view

**Voice Capture Screen:**
- Large mic button, waveform animation
- "Try: 'Add dentist for Emma next Thursday at 3'" — suggestion chips
- AI processes intent → creates calendar event + assigns to correct family member
- Confetti animation on success (0.8s spring)

**Meal Planning Screen:**
- This week's plan (7 cards, swipeable)
- "Snap your fridge" button → AI suggests recipes from what you have
- Auto-generated grocery list, checkable, shareable
- Dietary preferences per family member (allergies, dislikes)

**Chore Board:**
- Kanban-ish: To Do / Doing / Done
- Kid-friendly view: emoji rewards, star streaks
- Parent view: assign, rotate, set recurring

**Settings (max 8 items):**
- Family members management
- Notification preferences
- Calendar sync (Apple, Google)
- Dietary preferences
- Premium management
- App icon (4 variants)
- Privacy
- About

### 1.4. iOS-Specific Optimizations
- **WidgetKit:** Small (today's next event), Medium (3 upcoming + tonight's meal), Large (full day + chore status). Updated every 15 min via background refresh.
- **Siri Intents:** "Hey Siri, add to Hearthly" → opens voice capture. "Hey Siri, what's for dinner?" → reads tonight's meal.
- **Live Activities:** Grocery shopping mode — active list in Dynamic Island
- **App Store Review prompt:** After 3rd successful voice-capture event
- **Push notifications:** Rich notifications with family member photo. Category: "Chore Done" with "Mark Complete" action button.

---

## SECTION 2: ANDROID ARCHITECTURE

### 2.1. Technology Stack
- **Language:** Kotlin 2.0, Jetpack Compose (Material 3)
- **Minimum SDK:** 26 (96% coverage)
- **Architecture:** MVVM with StateFlow + collectAsStateWithLifecycle()
- **Persistence:** Room + DataStore. Firebase Realtime Database for cross-platform sync (free tier: 100 simultaneous, 1GB stored)
- **DI:** Hilt (compile-time safe)
- **Navigation:** Compose Navigation with type-safe routes
- **Analytics:** Firebase Analytics (GDPR consent before init)

### 2.2. Google Play Billing
- BillingClient 7.0+
- Same pricing tiers as iOS
- Grace period: 7 days payment failure
- Account hold: 30 days
- Introductory: 50% off first 3 months annual

### 2.3. Android-Specific Optimizations
- **Material You:** Dynamic theming from user wallpaper — home feels personal
- **Predictive back gesture:** All screens
- **App Shortcuts:** "Add Event" (voice), "Tonight's Meal", "Chore Board", "Grocery List"
- **Notification channels:** Events (HIGH), Chores (DEFAULT), Meal Plans (DEFAULT), Family Updates (LOW)
- **Background work:** WorkManager for meal plan generation, calendar sync
- **Play Store:** Feature graphic shows family laughing around kitchen table with Hearthly overlay

---

## SECTION 3: SEO & GEO OPTIMIZATION

### 3.1. App Store Optimization (iOS)
- **Keyword Field (100 chars):** family organizer,shared calendar,meal planner,chore tracker,grocery list,ai family,household manager,family calendar,voice planner,grocery
- **Title keywords (2× weight):** "family", "organizer", "AI"
- **Subtitle keywords (1.5× weight):** "calendar", "chores", "meal"
- **Promotional Text:** "Snap your fridge, plan your meals. Say it, it's scheduled. The family organizer that actually reduces mental load."
- **Ratings prompt:** After 3rd voice capture with "It worked!" confetti. "You seem to love Hearthly! Help other families find calm?"

### 3.2. Google Play Store
- **Title:** "Hearthly – Family AI Organizer" (30 chars)
- **Short Description:** "Family organizer: shared calendar, AI meal plans, chores & grocery lists in one app."
- **Category:** Productivity (primary), Lifestyle (secondary)
- **Tags:** family, organizer, calendar, meal-planning, chores

### 3.3. Off-Store SEO
- **Domain:** hearthly.app
- **H1:** "Hearthly – Family AI Organizer That Reduces Your Mental Load"
- **Meta:** "Stop juggling 5 apps. Hearthly combines shared calendar, AI meal planning, chore tracking, and grocery lists into one beautiful family organizer. Free for families of 4."
- **Blog cluster:** "Family Organizer Apps 2026 (Honest Comparison)", "How AI Meal Planning Saves Families $1,365/Year in Food Waste", "Cozi vs Hearthly: Which Family App Actually Works?", "The Mental Load Problem: Why Moms Need AI Family Tools"
- **GEO:** FAQ blocks: "What's the best family organizer app?" "How do I reduce mental load as a parent?" "Can AI plan my family's meals?"

---

## SECTION 4: BEHAVIORAL ARCHITECTURE

### 4.1. Trigger Design
- **Push #1 (Daily Brief):** "Good morning! 📋 Today: soccer 5pm, pasta for dinner, 2 chores due." — 7:00 AM, warm tone
- **Push #2 (Social):** "Emma completed her chore! 🌟 +1 star" — FOMO for other kids
- **Push #3 (Loss Aversion):** "Your meal plan streak: 3 weeks! Don't break it — plan this week in 2 taps."
- **Widget:** Passive trigger — glanceable dashboard on home screen
- **Email re-engagement (Day 3):** "Your family's week is waiting. 3 things you're missing in Hearthly."

### 4.2. Action Design
- **Core action:** Voice-capture an event. 1 tap to open mic → speak → done. Fogg BMAT: Motivation HIGH (reducing mental load), Ability TRIVIAL (voice), Trigger PRESENT (widget, push)
- **Onboarding:** Skip account creation → "Try it: say 'Dinner with parents Friday 7pm'" → immediate value

### 4.3. Variable Reward
- **Tribe:** "Sarah commented on your meal plan" — social within family
- **Hunt:** Weekly "Family Insight" — "You saved 2.3 hours this week by planning ahead"
- **Self:** "Perfect Week" badge, chore completion streaks, meal planning streaks

### 4.4. Investment
- **Data:** All family events, preferences, meal history — switching costs are real
- **Social:** Whole family must be on it for it to work
- **Financial:** $4.99/mo subscription = sunk cost
- **Reputation:** Kid star streaks, family "calm score" visible dashboard

---

## SECTION 5: VISUAL DESIGN SYSTEM

### 5.1. Design Principles
1. "Warmth over utility. This is a home, not a factory."
2. "Voice is primary. Taps are secondary. Typing is last resort."
3. "Every family member sees their world — color-coded, personalized."
4. "Data is invisible until you need it. The dashboard feels light."

### 5.2. Key Animations
- **App open:** Hearth logo (warm glow) → fades into today's dashboard (0.6s crossfade)
- **Voice capture success:** Orange confetti burst → event card slides in from top (0.8s spring)
- **Meal plan generated:** Cards stagger-fade in, each 0.05s delay
- **Chore complete:** Checkmark bounces + star particle effect (0.5s)
- **Empty state:** Gentle pulsing "Add your first..." prompt

### 5.3. Haptic Feedback
- Light: Row selection, toggle
- Medium: Voice capture success, chore complete
- Heavy: Weekly insight milestone
- Selection: Date/time pickers

### 5.4. Accessibility
- VoiceOver labels on every interactive element
- Dynamic Type support to largest accessibility size
- Reduce Motion: skip decorative animations
- No color-only information — all status has icons + text
- Tested: protanopia, deuteranopia, tritanopia

---

## SECTION 6: FINANCIAL ARCHITECTURE

### 6.1. Pricing Tiers

| Tier | Monthly | Annual | What's Included |
|---|---|---|---|
| Free | $0 | $0 | 1 family (4 members), shared calendar, 10 AI events/mo, 3 AI meals/mo, basic chores |
| Premium | $4.99 | $39.99 | Unlimited families, unlimited AI, photo-to-calendar, voice journals, insights, custom rewards |
| Family+ | $7.99 | $63.99 | Premium for up to 8 members + shared grocery sync + priority support |

### 6.2. Unit Economics
- **CAC target:** $0 (organic at launch)
- **LTV at 6 months (Premium):** ~$25 (avg 5-month retention × $4.99)
- **Payback period:** Immediate (organic CAC = $0)
- **Monthly churn target:** 8% (consumer subscription average)
- **Referral value:** Each referred Premium = $25 LTV. Cost: 1 free month for both ($0 marginal cost)

### 6.3. Monetization Flow
1. Download → Onboarding → Voice-capture value moment
2. 3rd voice capture → Paywall (annual pre-selected)
3. Decline → "7-day free trial, no card needed"
4. Decline → Free tier. Re-prompt on AI limit hit or photo-to-calendar attempt
5. Annual renewal reminder: 7 days before

### 6.4. Cancellation Flow
- Step 1: Pause 1-3 months option
- Step 2: Reason picker (too expensive / not using / found alternative / missing feature)
- Step 3: If "too expensive" → 50% off 6 months
- Step 4: If "not using" → weekly digest instead of daily
- Step 5: "Data kept 90 days. Come back anytime."

---

## SECTION 7: VIRALITY ENGINE

### 7.1. Shareable Moments
1. "Our family's calm score this week: 92% 🌿" — shareable card
2. "I planned all our meals this week and saved $47 🎉" — receipt-style card
3. "Join our Hearthly family" — invite link with 1 free month
4. "Emma's chore streak: 14 days! ⭐" — kid achievement card
5. "Year in Review: The [Family Name] 2026" — Spotify Wrapped style

### 7.2. Viral Mechanics
- **Invite:** 1 tap → native share sheet. Sender gets 1 month free, receiver gets 1 month free.
- **Network effect:** App is useless solo — designed for families. Each new user = family group value increases.
- **Watermark:** "Made with Hearthly" on every shareable card

### 7.3. Rating Protection
- 2-star or below: Route to feedback form
- 3-star: Pre-selected 4-star prompt
- 4-5 star: Route to App Store rating
- Reply to every review within 24 hours

---

## SECTION 8: TECHNICAL SPECIFICATION

### 8.1. Database Schema (SwiftData)

```
Family:
  id: UUID (PK)
  name: String
  createdAt: Date
  premiumUntil: Date?
  calmScore: Int

Member:
  id: UUID (PK)
  familyId: UUID (FK → Family)
  name: String
  color: String (hex)
  role: Enum(parent, child, caregiver)
  avatar: Data?
  dietaryPreferences: [String]

Event:
  id: UUID (PK)
  familyId: UUID (FK → Family)
  creatorId: UUID (FK → Member)
  title: String
  startDate: Date
  endDate: Date?
  location: String?
  assignedMembers: [UUID]
  source: Enum(voice, manual, photo, email)

Meal:
  id: UUID (PK)
  familyId: UUID (FK → Family)
  date: Date
  mealType: Enum(breakfast, lunch, dinner, snack)
  recipeName: String
  ingredients: [String]
  dietaryTags: [String]
  generatedBy: Enum(ai, manual, fridgePhoto)

Chore:
  id: UUID (PK)
  familyId: UUID (FK → Family)
  assigneeId: UUID (FK → Member)
  title: String
  recurring: Enum(none, daily, weekly, monthly)
  dueDate: Date?
  completedAt: Date?
  rewardPoints: Int

GroceryItem:
  id: UUID (PK)
  familyId: UUID (FK → Family)
  name: String
  category: Enum(produce, dairy, meat, pantry, frozen, other)
  checked: Bool
  addedBy: Enum(mealPlan, manual, voice)
```

### 8.2. API Endpoints (CloudKit/Firebase)
- CK sync: Events, Members, Chores (CloudKit free tier)
- Firebase RTDB: Meal plans, Grocery lists (cross-platform sync)
- Auth: Apple Sign In (iOS), Google Sign In (Android), email fallback

### 8.3. AI Architecture (On-Device)
- **Model:** Phi-4-mini (3.8B Q4) via llama.cpp for iOS Metal / Android Vulkan
- **Fallback:** On-device Core ML model for voice intent classification
- **Meal planning:** Local LLM + ingredient DB → generates weekly plan from preferences + pantry
- **Voice→Event:** Intent classifier extracts: who, what, when, where → structured event
- **Zero cloud inference costs.** Privacy moat.

### 8.4. Third-Party Dependencies
- RevenueCat (subscriptions)
- TelemetryDeck (iOS analytics)
- Firebase Analytics + RTDB (Android + cross-platform)
- CloudKit (iOS sync)
- NO Facebook SDK, NO AdMob

---

## SECTION 9: 30-DAY MVP SPRINT PLAN

**Week 1 — Foundation**
| Day | iOS | Android | Shared |
|---|---|---|---|
| Mon | Project setup, SwiftData models | Project setup, Room entities | DB schema final |
| Tue | Onboarding (3 cards) | Onboarding (3 cards) | Design review |
| Wed | Home dashboard skeleton | Home dashboard skeleton | UI parity check |
| Thu | Voice capture (AVFoundation) | Voice capture (MediaRecorder) | AI intent classifier integration |
| Fri | RevenueCat + paywall | BillingClient + paywall | Pricing final |

**Week 2 — Core Experience**
| Day | iOS | Android | Shared |
|---|---|---|---|
| Mon | Calendar views | Calendar views | CloudKit/Firebase sync |
| Tue | Chore board | Chore board | Family invite flow |
| Wed | Meal planning UI | Meal planning UI | Fridge photo → recipe AI pipeline |
| Thu | Push notifications | Notification channels | Notification copy |
| Fri | WidgetKit (small, medium) | App Widgets | Widget review |

**Week 3 — Polish**
| Day | iOS | Android | Shared |
|---|---|---|---|
| Mon | Haptics, animations | Motion, predictive back | Micro-interaction review |
| Tue | Grocery list with check-off | Grocery list with check-off | Cross-platform sync test |
| Wed | App Store screenshots | Play Store feature graphic | ASO copy |
| Thu | Accessibility audit | Accessibility audit | VoiceOver/TalkBack |
| Fri | Premium upgrade screen | Premium upgrade screen | Monetization flow test |

**Week 4 — Launch**
| Mon-Wed: Bug fixes, edge cases | Thu: TestFlight + Internal Testing | Fri: SUBMIT |

**Cut List:**
- Family insights dashboard (Month 2)
- Voice journals (Month 2)
- Photo-to-calendar (Month 2)
- Custom chore rewards (Month 3)

---

## SECTION 10: LAUNCH CHECKLIST

- [ ] App Store Connect: record created, all metadata
- [ ] Google Play Console: app created, metadata
- [ ] RevenueCat: products, webhooks
- [ ] Privacy Policy URL live
- [ ] Terms of Service URL live
- [ ] Support email with auto-responder
- [ ] Screenshots: 6.9" and 6.7" displays
- [ ] TestFlight submitted for Beta Review
- [ ] 20 testers for Play Store closed testing
- [ ] Launch day: manual release both stores
- [ ] Stage rollout: 10% Android for 24h
- [ ] Reply to first 10 reviews within 2 hours
- [ ] Post on r/parenting, r/workingmoms, r/daddit
- [ ] Product Hunt launch (12:01 AM PT)

---

## SECTION 11: POST-LAUNCH ITERATION

**Week 1:** Observe D1/D7/D30 retention, conversion rate. Only crash fixes.
**Week 2-4:** Top 3 user-requested improvements. A/B test paywall if conversion <20%.
**Month 2-3:** Family insights, voice journals, photo-to-calendar. Content marketing (blog cluster).

---

## SECTION 12: ANTI-PATTERNS

1. Do not ask for notification permission on first open (60% rejection rate)
2. Do not require account creation before value (20-30% drop per barrier)
3. Do not show ads in first 30 days (destroys trust before habit forms)
4. Do not use default RevenueCat paywall (40% worse conversion)
5. Do not ship static splash screen → instant animation into dashboard
6. Do not ignore 1-star reviews → reply within 24 hours
7. Do not localize poorly → English + Spanish only at launch
8. Do not ship both platforms simultaneously if resources tight → iOS first, Android +2 weeks
9. Do not force typing → voice-first design is the core differentiator
10. Do not skip family invite flow testing → it's the entire growth engine

---

_End of Hearthly Scaffold v1.0. Pipeline date: 2026-05-28._