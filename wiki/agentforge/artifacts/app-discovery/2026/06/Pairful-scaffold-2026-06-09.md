# Pairful — Scaffold

**Date:** 2026-06-09  
**Pipeline run:** App Discovery Daily  
**App name:** Pairful  
**Niche:** Couples Shared Planner (childless couples falling through the gap between dating apps and family organizers)

---

## 0. App Identity & Positioning

**Tagline:** The shared home for two. Plan together, not around each other.

**One-liner:** Pairful is the first all-in-one shared planner purpose-built for couples without kids — calendar, finances, grocery lists, date ideas, and a private memory feed — replacing 4+ fragmented apps with one beautiful space.

**Target user:** Committed couples (dating, engaged, married) who don't have children and don't want a "family" app with school calendars, chore charts, and kid photo albums. Ages 22-40.

**Problem (validated):** "Cozi and FamCal serve families well, but couples without kids fall through the cracks. They want a clean shared space for date plans, gift ideas, joint goals, and a private memory feed." — CatDoes blog, June 2026. Current workaround: WhatsApp + Google Calendar + Splitwise + Notes = 4+ apps.

---

## 1. iOS Architecture

- **Swift 6 + SwiftUI** target iOS 17+
- MVVM-C (MVVM + Coordinator) for navigation
- **Core Data + CloudKit** for sync (on-device + private cloud, not third-party servers)
- RevenueCat for subscriptions
- StoreKit 2 for in-app purchases
- Local push notifications (UNUserNotificationCenter)
- WidgetKit for shared calendar widget, countdown widget

**Key iOS-native capabilities:**
- Live Activity for shared countdowns and reminders
- App Intents for Siri shortcuts ("Hey Siri, add milk to Pairful")
- Focus Filters (work mode hides relationship feed)

---

## 2. Android Architecture

- **Kotlin + Jetpack Compose**
- MVVM + Navigation Compose
- Room database + Firebase Firestore for sync
- RevenueCat Android SDK
- WorkManager for background sync
- Glance for widgets
- Material 3 design language (adapted to Pairful's design system)

**Cross-platform sync:** CloudKit ↔ Firestore bridge via Cloud Functions. Real-time sync for calendar changes.

---

## 3. SEO & GEO Optimization

**Primary keyword:** "couples shared planner" (~5K-10K searches/mo)  
**Secondary keywords:** "shared calendar for couples", "couples app without kids", "relationship planner app", "couples to-do list", "date night planner"

**ASO strategy:**
- App Store subtitle: "Shared Calendar & Life Planner"
- Keyword field (100 chars): couples planner, shared calendar, to-do list, grocery list, date ideas, relationship app
- Screenshot A/B test variants: Calendar-first vs. Memory-feed-first
- **GEO play:** Localized metadata for US, UK, Canada, Australia, Germany. "Couples planner" searches vary by region.

---

## 4. Behavioral Architecture

**Hook 1: The "Invite Your Partner" Moment (Day 1)**
- After onboarding, user sees an empty shared calendar
- One-tap invite link (SMS/WhatsApp/iMessage)
- Partner receives "Build our life together 💫" with deep link

**Hook 2: First Shared Event (Day 1-3)**
- AI suggests default events based on onboarding: "Movie night Saturday?", "Grocery run Sunday?"
- Push notification: "Your partner added 'Sushi date Friday 🍣'"

**Hook 3: Memory Feed (Week 2+)**
- Weekly recap: "This week in your relationship"
- Auto-generated from calendar events, shared photos, grocery runs
- Streak mechanic: "You've planned 8 dates this month 🔥"

**Retention loops:**
- Morning briefing notification: "Today: gym 6 PM, groceries due, 42 days until anniversary"
- Partner activity triggers: "Sarah just added 'Beach trip' to the wishlist"
- Weekly digest with date suggestions from AI

**No shame UX:** Unlike habit trackers, Pairful never shows "you missed X days." It's always aspirational. "Here's what you could do this weekend" not "you haven't planned anything."

---

## 5. Visual Design System

- **Color palette:** Deep plum (#2D1B4E) + warm peach (#FFB5A7) + cream (#FFF8F0)
- NOT blue/teal productivity colors — this feels warm, intimate, relationship-focused
- **Typography:** Satoshi (headings), Inter (body) — clean, modern, warm
- **Illustrations:** Custom couple illustrations by Leni Kauffman style — diverse, inclusive, warm
- **Iconography:** Rounded, 2px stroke, couple-themed (two icons together for shared features)

**Design principle:** Every screen should feel like you're building something together. Empty states show two figures, not one. Button labels use "we" not "you."

---

## 6. Financial Architecture

**Pricing (undercut strategy):**
- **Free tier:** Shared calendar (2-person), 3 shared lists, 1 wishlist, 10 memory feed items
- **Pairful Plus: $4.99/mo or $39.99/yr** — unlimited lists, AI date suggestions, shared finances (expense tracking), grocery autofill, custom categories, widgets, export

**Why $4.99/mo:** Undercuts Cupla ($6.99/mo), avoids the $9.99+ "family app" price point, hits the lifestyle sweet spot ($3-10/mo category benchmark). Annual at $3.33/mo makes it a no-brainer.

**Revenue model:**
- 80% subscriptions (target 5-8% conversion from free)
- 15% one-time purchases (theme packs, premium stickers)
- 5% partnerships (date-night venue referrals, meal kit integrations)

**Unit economics target:**
- CAC: $3-5 (organic + ASO)
- LTV: $40-60 (avg 10-12 month retention)
- LTV:CAC ratio: 10:1+

---

## 7. Virality Engine

**Built-in sharing loops:**
- "Share your list" — grocery list one-tap share to partner (organic install)
- "Plan a date" — AI suggests a date, creates a shareable invite card
- "Memory of the day" — auto-generated relationship memory with partner's photo, shareable
- Anniversary countdown widget — visible on home screen, prompts questions from friends
- Couple "Year in Review" — December viral moment, auto-generated video from shared memories

**K-factor target:** 0.4 (every user brings 0.4 new users organically) through shared invite cards and countdown widgets.

---

## 8. Technical Specification

**Backend:**
- Firebase (auth, Firestore, Cloud Functions, FCM)
- RevenueCat (subscriptions)
- CloudKit (iOS sync — privacy differentiator)

**AI features:**
- **Date suggestion engine:** GPT-5 mini — analyzes past dates, preferences, local venues
- **Grocery list autocomplete:** OCR from photos + NLP — "add these 5 things I saw at the store"
- **Memory auto-tagger:** On-device ML (Create ML / ML Kit) — tags photos, detects faces
- **Expense scanning:** Receipt OCR for shared finance tab

**Privacy (differentiator):**
- On-device AI where possible
- Encrypted shared data at rest
- No third-party data sharing
- GDPR-compliant by default
- "Private mode" — hide certain entries from partner (gift ideas, surprise plans)

---

## 9. 30-Day MVP Sprint Plan

| Week | Focus | Deliverable |
|------|-------|-------------|
| **1** | Auth + invite flow + shared calendar | Working shared calendar, partner invite |
| **2** | Lists + grocery + to-dos | Shared lists with real-time sync |
| **3** | Memory feed + date planner | Photo upload, date suggestions, countdown |
| **4** | Finances + AI features + polish | Expense tracking, grocery OCR, date AI |
| **Day 30** | App Store submission | Beta via TestFlight first, then launch |

---

## 10. Launch Checklist

- [ ] App Store Connect: metadata, screenshots (5 variants A/B test)
- [ ] Google Play Console: listing, feature graphic
- [ ] RevenueCat products configured (monthly + annual)
- [ ] Firebase production project set up
- [ ] Landing page: pairful.app with email capture
- [ ] Social: @pairfulapp on Instagram, TikTok, X
- [ ] Launch content: 3 TikTok videos, 2 Reddit posts (r/relationships, r/relationship_advice), 1 Product Hunt launch
- [ ] Press kit: App Store icon, screenshots, founder story

---

## 11. Post-Launch Iteration Plan

**30 days:** Widget, dark mode, push notification fine-tuning  
**60 days:** Android launch, location-aware date suggestions  
**90 days:** AI couples coaching (pattern analysis from shared data — e.g., "You two plan 37% fewer dates in winter")  
**180 days:** Wedding planning module (tier 2 monetization)

---

## 12. Anti-Patterns

- ❌ Don't add kids/family features (destroys the core positioning)
- ❌ Don't gamify the relationship (no "relationship score")
- ❌ Don't be a messaging app — this is a planner, not a chat replacement
- ❌ Don't add social features (no public feeds, no "compare with other couples")
- ❌ Don't be a dating app — Pairful is for established couples, not matchmaking

---

**Scaffold by:** Alex, VP of App Strategy  
**Pipeline:** App Discovery Daily — June 9, 2026
