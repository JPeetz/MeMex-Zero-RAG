# EchoJournal — App Scaffold

**Scaffolded:** 2026-06-02  
**Niche:** AI Voice-First Journaling  
**Pipeline Winner Score:** 6.25/10  
**Pipeline:** Pain Harvest → Signal Check → Gap Map → Niche Scoring → Scaffold  

---

## 0. App Identity & Positioning

**Name:** EchoJournal  
**Tagline:** Talk. Reflect. Grow.  
**Category:** Health & Fitness / Mental Wellness  
**Platforms:** iOS + Android (simultaneous launch)  
**Price:** $6.99/mo or $49.99/yr (30% below category median of $9.99/mo)  
**Freemium:** 3 free voice entries/week + AI weekly summary. Premium: unlimited entries, AI deep analysis, export, custom prompts.

**One-liner:** The first journaling app that's *built* for your voice — not a keyboard app with a mic button tacked on.

**The Problem:** "Typing feels slow, but voice journaling feels impractical" — r/digitaljournaling. Millions want to journal but hate typing on a phone. Existing apps (Day One, Rosebud, Stoic) are typing-first with voice as an afterthought.

**Key Differentiator:** Voice-FIRST architecture. Every feature designed around speaking, not typing. Open → tap mic → talk → AI extracts themes, mood patterns, and recurring stressors across weeks. On-device AI for privacy (no cloud processing of journal entries).

**Target Users:** Commuters, parents with no time to type, founders with racing thoughts, anyone who "would journal if it was easier."

---

## 1. iOS Architecture

- **SwiftUI + SwiftData** for local persistence
- **Apple Speech Framework** for on-device transcription (iOS 17+)
- **Core ML + Apple Intelligence** for on-device theme extraction, mood analysis
- **CloudKit** for sync (E2E encrypted)
- **RevenueCat** for subscriptions
- **WidgetKit** for home screen streak/streak widgets
- **Siri Intents** — "Hey Siri, journal in EchoJournal"
- **Live Activities** — recording indicator

**Minimum iOS:** 17.0 (for on-device AI capabilities)

---

## 2. Android Architecture

- **Kotlin + Jetpack Compose**
- **ML Kit** for on-device transcription
- **TensorFlow Lite** for on-device mood/themes
- **Room DB** for local storage
- **Firebase** for optional encrypted cloud sync
- **Google Play Billing** for subscriptions

**Minimum Android:** 14 (for on-device ML capabilities)

---

## 3. SEO & GEO Optimization

**Primary Keyword:** "voice journaling app"  
**Secondary:** "AI journal", "talk diary", "voice diary", "journal app voice", "audio journal"  
**ASO Strategy:** 
- App name: "EchoJournal: Voice AI Diary"
- Subtitle: "Talk. Reflect. Grow."
- Keyword field: voice,journal,diary,ai,mood,tracker,self,care,reflect,growth
- Long-tail targets: "journal app you can talk to", "voice diary with AI insights", "talk instead of type journal"

**Estimated Search Volume:** "voice journaling" growing niche — ~3-5K/mo. "AI journaling" ~8-12K/mo but more competitive.

---

## 4. Behavioral Architecture

**Core Loop:**
1. **Trigger:** Daily push notification at user's chosen time ("What's on your mind?")
2. **Action:** Tap mic → speak 30-120 seconds → done. No typing required.
3. **Reward:** Instant AI summary ("Here's what you talked about..."), mood detection, theme extraction
4. **Investment:** Weekly summaries, streak counter, monthly "Year in Review"-style recap

**Habit Formation:**
- Streak counter with gentle reminders (no shame language)
- "3-day trend" summaries to drive return
- Widget showing current streak
- Apple Watch companion for quick voice entries

**Anti-Churn Mechanics:**
- Content lock-in: "Your journal history is irreplaceable"
- Export-as-book feature (PDF/print) for annual subscribers
- "Your year in words" annual recap video

---

## 5. Visual Design System

**Mood:** Warm, calm, minimal. Not clinical — cozy.
**Palette:** Warm cream background, deep navy accents, amber highlights
**Typography:** Serif for journal text (feels personal), sans-serif for UI
**Key Screens:**
- Home: Single large mic button (80% of screen). Below: today's streak, last entry preview
- Journal feed: Cards with mood emoji, AI-generated title, time since recorded
- Insights tab: Mood graph, recurring themes word cloud, "patterns" carousel
- Settings: Reminder time, theme, export, privacy controls

**Accessibility:** VoiceOver support, high-contrast mode, adjustable text sizes

---

## 6. Financial Architecture

| Tier | Price | Features |
|------|-------|----------|
| Free | $0 | 3 voice entries/week, basic AI summary, 7-day history |
| Premium | $6.99/mo | Unlimited entries, deep AI analysis, export, custom prompts, 5-year history |
| Annual | $49.99/yr | All Premium + annual "Your Year in Words" book PDF |

**Unit Economics (mature):**
- CAC: $3-5 (organic ASO + Reddit/journaling community)
- LTV: $84 (@ $7/mo × 12 months avg retention)
- LTV:CAC ratio: 17-28x (healthy)
- Break-even: Month 3 per user

**Category Benchmark:** Mental Wellness $5-15/mo. EchoJournal at $6.99/mo is median — 30% below Rosebud's $12.99/mo.

---

## 7. Virality Engine

- **"Share a Thought"** — generate a beautiful card from an AI-insight (mood trend, theme). Shareable to Instagram/Twitter.
- **"Journal Together"** — couples/friends mode: shared prompt of the day, each records separately, optionally share insights
- **TikTok/Reels:** "What my journal app told me about my week" reveal videos (high viral potential)
- **Reddit communities:** r/journaling, r/digitaljournaling, r/mentalhealth — authentic participation + feature posts

---

## 8. Technical Specification

**Voice Processing Pipeline:**
1. On-device speech recognition (Apple Speech / Android ML Kit)
2. Local LLM extracts: mood (positive/negative/neutral), 3-5 key themes, named entities
3. Cross-entry analysis runs weekly on-device: pattern detection, mood trends, recurring topics
4. Everything stays on-device. Cloud sync is encrypted-at-rest.

**Privacy:** 
- All journal content processed ON-DEVICE. Never sent to cloud for AI.
- CloudKit/Firebase sync is E2E encrypted
- "Private Mode" with FaceID/TouchID lock
- No data used to train AI models
- GDPR/CCPA compliant by default

**Data Model:**
- Entry: id, audioFileURL, transcript, mood, themes[], date, duration, isPrivate
- User: preferences, streak, reminderTime, subscriptionTier
- Insights: weeklySummary, moodGraph, themeCloud, patterns

---

## 9. 30-Day MVP Sprint Plan

| Week | Focus | Deliverable |
|------|-------|------------|
| 1 | Core recording + transcription | Working iOS prototype: record → transcribe → save |
| 2 | AI mood/themes + UI | On-device mood detection, theme extraction, journal feed UI |
| 3 | Insights + reminders + streak | Weekly summaries, push notifications, streak counter |
| 4 | Subscription + sync + polish | RevenueCat, CloudKit sync, App Store screenshots, TestFlight |

**Launch:** Day 30 — App Store submission. Day 37 — launch if approved.

---

## 10. Launch Checklist

- [ ] App Store listing: screenshots, description, keywords
- [ ] Google Play listing
- [ ] Privacy policy + terms (GDPR CCPA compliant)
- [ ] TestFlight beta (50-100 testers)
- [ ] Reddit r/journaling, r/digitaljournaling launch post
- [ ] Product Hunt launch
- [ ] Press kit + outreach to mental health/wellness bloggers
- [ ] RevenueCat subscription ready
- [ ] Analytics: PostHog for retention tracking

---

## 11. Post-Launch Iteration Plan

**Month 1-2:** Watch retention. If D7 <40%, investigate onboarding friction. Add guided first-entry flow.  
**Month 3:** Add Apple Watch companion. Add "Journal Together" couples mode.  
**Month 6:** Android launch. Add "Year in Words" annual recap.  
**Month 9:** Therapist mode (share insights with therapist). Multi-language transcription.  
**Month 12:** Enterprise/wellness program: sell to companies as employee benefit ($5/user/mo).

---

## 12. Anti-Patterns

- ❌ **Don't build a typing app with a mic button.** The whole architecture must be voice-first.
- ❌ **Don't send journal data to cloud AI.** Privacy is the differentiator vs Rosebud/Stoic.
- ❌ **Don't shame streak breaks.** ADHD-friendly, shame-free design.
- ❌ **Don't compete on features with Day One.** Compete on voice-first simplicity.
- ❌ **Don't charge $12.99/mo.** Underprice Rosebud significantly.
