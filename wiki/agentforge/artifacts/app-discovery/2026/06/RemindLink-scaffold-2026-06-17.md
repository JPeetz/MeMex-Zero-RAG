# RemindLink — Superhuman App Scaffold
**Generated:** 2026-06-17 | **Pipeline:** App Discovery Daily | **Verdict:** BUILD | **Score:** 83/100

## App Identity

- **App name (ASO):** RemindLink — Bookmark Reminder (29 chars)
- **Subtitle:** Save links. Set reminders. Done. (28 chars)
- **One-liner:** Save any link from any app, set a reminder, and RemindLink brings it back when it actually matters.
- **Category:** Productivity
- **Platform launch order:** Android-first (Play Store), iOS +2 weeks

## Problem & Solution

Pocket shut down July 2025, displacing 20M+ registered users. Every existing alternative (Raindrop, Readwise, Instapaper) focuses on *reading experience* — none solves the core problem: **saved links never get revisited.** RemindLink adds a reminder layer: save a link, set when you want to be reminded, get a push notification at exactly the right time.

## Killer Differentiator

No bookmark/read-later app on the market has a time-based re-surfacing mechanic as the *core* feature. Raindrop shows your bookmarks. RemindLink *nags you to read them* — and that's exactly what users need.

## Revenue Model & Unit Economics

| Tier | Monthly | Annual | What you get |
|---|---|---|---|
| Free | $0 | $0 | 10 active reminders, basic categories, manual tagging |
| Premium | $3.99 | $29.99 ($2.49/mo) | Unlimited reminders, AI auto-tagging, recurring patterns, bulk import, export, priority support |

- **CAC target:** $0 (organic-first, no paid UA at launch)
- **LTV at 6mo:** ~$15 (annual sub avg 7.5mo retention)
- **Payback:** Immediate (zero CAC)
- **Target churn:** <8% monthly

## iOS Tech Stack
- Swift 6 + SwiftUI, iOS 17 minimum
- MVVM + SwiftData + CloudKit sync
- RevenueCat (paywall, custom SwiftUI view)
- WidgetKit (small + medium widgets)
- App Intents: "Hey Siri, remind me about [link]"
- TelemetryDeck analytics (privacy-first)
- Local-first AI via MLX Swift + Phi-4-mini (3.8B Q4) for auto-tagging

## Android Tech Stack
- Kotlin 2.0 + Jetpack Compose (Material 3), min SDK 26
- MVVM + StateFlow + Room + DataStore
- Firebase Realtime Database for sync
- Hilt DI, Compose Navigation
- BillingClient 7.0, notification channels
- App Shortcuts: 4 static (New Reminder, Upcoming, Expired, Settings)
- WorkManager for background reminder scheduling
- MediaPipe LLM for on-device auto-tagging (Gemma-3-1B)

## Screens (6 screens, 30-day MVP)

1. **Onboarding (3 slides)** — "Stop bookmarking forever. Start revisiting."
2. **Home Dashboard** — Upcoming reminders timeline. Search bar. Category pills.
3. **Save Link Sheet** — Share sheet capture → URL preview → pick reminder time (Later Today, Tomorrow, This Weekend, Pick Date, Recurring)
4. **Reminder Notification** — Rich notification with link preview + Open + Snooze + Mark Done actions
5. **Library** — All saved links, filterable by status (pending/done/expired) and category
6. **Premium Upgrade** — Comparison table, "7-day free trial, no card needed"

## Viral Mechanics
- Shareable: "Just cleared my bookmark backlog! 15 links revisited today on RemindLink 🔥"
- Referral: Both parties get 1 free Premium month
- Streaks: Days with at least one completed reminder backlink

## Launch Plan
- **Pre-launch (T-14):** App Store + Play Store metadata, Privacy Policy, TestFlight
- **Launch day:** Product Hunt, r/androidapps, r/iosapps, indie hacker communities
- **Post-launch week 1:** Observe metrics (D1/D7/D30 retention, conversion). Fix crashes only.
- **Week 2-4:** Ship top 3 user requests. A/B test paywall if conversion <20%.

## Anti-Patterns — Don't
1. Don't ask for notification permission on first open (ask after first save)
2. Don't require account creation (try before you sign up)
3. Don't show ads (subscription-only monetization preserves premium feel)
4. Don't use default system paywall (custom SwiftUI/Compose = 40% better conversion)
5. Don't ship static splash screen (animate into content immediately)
6. Don't skip 1-star review replies (respond within 24h, it boosts ranking)
7. Don't build features nobody asked for (ship at least one user request per sprint)

## 30-Day Sprint

**Week 1:** Project setup, models, onboarding, home screen, core action flow
**Week 2:** Notifications, share sheet, library screen, settings, empty states
**Week 3:** Haptics, animations, accessibility, widgets, app shortcuts, ASO assets
**Week 4:** Bug fixes, TestFlight, Play Store beta, submission

## DB Schema (Core Tables)

- `Bookmark`: id, url, title, domain, notes, categoryId, createdAt
- `Reminder`: id, bookmarkId, remindAt, repeatInterval, repeatUntil, status, snoozedUntil
- `Category`: id, name, icon, color, sortOrder
- `Tag`: id, name
- `BookmarkTag`: bookmarkId, tagId

## API Endpoints (Minimal — mostly on-device)

- `POST /api/v1/sync` — batch sync bookmarks from device
- `GET /api/v1/sync` — pull changes since last sync
- Firebase Auth for Apple/Google sign-in

## Risk Register

| Risk | Likelihood | Mitigation |
|---|---|---|
| Raindrop adds reminders | Medium | First-mover advantage, UX depth |
| Low free→paid conversion | Medium | Generous free tier, value-first paywall timing |
| Notification fatigue | Low | User controls all timing, opt-in recurring patterns |
| Android-only limits reach | Low (by design) | iOS within 2 weeks |

---

*Scaffold generated 2026-06-17. Engineer-ready — no additional clarification questions needed.*