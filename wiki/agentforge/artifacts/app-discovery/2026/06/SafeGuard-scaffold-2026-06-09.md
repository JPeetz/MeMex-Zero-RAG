# SafeGuard — Scaffold

**Date:** 2026-06-09  
**Pipeline run:** App Discovery Daily  
**App name:** SafeGuard  
**Niche:** Elderly Scam Protection — AI-powered active interception for aging parents

---

## 0. App Identity & Positioning

**Tagline:** Protect the people who raised you. Before the scammer calls.

**One-liner:** SafeGuard is the first mobile app that actively intercepts scams targeting elderly parents — scanning messages, emails, and calls with on-device AI, alerting caregivers in real time BEFORE money is lost.

**Target user (payer):** Adult children (35-55) caring for aging parents (65+).  
**Target user (protected):** Seniors with smartphones who are vulnerable to phone/text/email scams.

**Problem (validated):** "I've been trying to find something that helps protect older family members from scams — especially as AI and fake websites get more convincing. My dad sometimes gets caught out by online 'lotteries' or suspicious emails. He paid £70 for a mystery gift." — r/eldercare, Oct 2025. $3B+/year in US elder fraud, growing with AI-powered scams.

---

## 1. iOS Architecture

- Swift 6 + SwiftUI, target iOS 17+
- **On-device Core ML** for scam text/email classification (no cloud — privacy-critical for message scanning)
- CallKit integration for incoming call screening and scam flagging
- Message Filter Extension (SMS filtering without reading full content)
- RevenueCat for subscriptions
- CloudKit for caregiver dashboard sync (encrypted)
- WidgetKit for caregiver dashboard widget
- Critical Alerts entitlement for scam emergency notifications

---

## 2. Android Architecture

- Kotlin + Jetpack Compose
- **On-device ML Kit** / TensorFlow Lite for scam classification
- CallScreeningService for real-time call screening (Android 10+)
- NotificationListenerService for scam alert overlay
- Firebase Firestore for caregiver sync
- WorkManager for background scam database updates
- Accessibility Service (optional) for web browsing scam detection

---

## 3. SEO & GEO Optimization

**Primary keyword:** "scam protection for elderly parents" (~1K-5K searches/mo, growing)  
**Secondary keywords:** "protect parents from scams", "senior scam blocker", "elder fraud protection app", "anti-scam app for seniors", "AI scam detector"

**ASO strategy:**
- App Store subtitle: "AI Scam Blocker for Seniors"
- Long-tail play: "is this a scam checker", "fake website detector for parents"
- GEO: US (elder fraud capital), UK, Canada, Australia — English-first, localized scam database per country
- SEO content: "How to protect elderly parents from [scam type]" blog series

---

## 4. Behavioral Architecture

**Onboarding (Senior Side — designed by caregiver):**
- Caregiver installs app, creates account, enters parent's phone number
- Parent receives SMS: "[Name] set up SafeGuard to help protect you from scams. Tap to activate."
- Senior onboarding: ONE screen. "SafeGuard watches for scams so you don't have to worry. Ready?" → Tap "Protect Me"
- No account creation for senior. No password. No settings. Zero friction.

**Hook: First Scam Blocked (Day 1-7)**
- Senior receives scam text: "Your Social Security number has been suspended. Click here."
- SafeGuard intercepts, flags: ⚠️ "This may be a scam. We blocked the link."
- Caregiver gets push: "SafeGuard blocked a phishing attempt on [Mom's] phone. No action needed."

**Retention Loop (Caregiver Dashboard):**
- Weekly: "SafeGuard blocked 3 scams targeting your mom this week. Here's what they tried."
- Monthly: "Scam trends in your parent's area. Romance scams are up 40%."
- Peace-of-mind metric: "98 days since last scam reached [Dad]"

**Retention Loop (Senior Side):**
- Silent. SafeGuard works in the background.
- Occasional positive reinforcement: "You're protected. SafeGuard is watching for scams."

---

## 5. Visual Design System

**Color palette:**
- Primary: Shield Blue (#1A5276) — trust, security, calm
- Accent: Safety Green (#27AE60) — "protected" status indicators
- Warning: Alert Amber (#F39C12) — scam detection alerts
- Background: Warm White (#FAFAF5)

**Typography:** Inter (all platforms) — accessible, large default text size (16pt min for seniors)

**Design principles:**
- **Senior side:** Maximum 3 buttons per screen. Large tap targets (48pt+). No jargon. Warm, reassuring tone.
- **Caregiver side:** Clean dashboard. Red/Amber/Green status. Actionable alerts. Data-rich but calm.

---

## 6. Financial Architecture

**Pricing:**
- **SafeGuard Basic:** $7.99/mo per senior — scam text/email scanning, call screening, caregiver dashboard
- **SafeGuard Family:** $14.99/mo — up to 3 seniors, priority alerts, quarterly scam report
- **Annual:** $59.99/yr ($5/mo) per senior

**Why $7.99/mo:**
- Below SeniorShield's $9.99/mo, above the "free app" zone
- Elder fraud costs families $3B+/year — $7.99/mo is 0.3% of a single $3,000 scam loss
- Category benchmark for health/safety: $5-15/mo

**Revenue model:**
- 90% subscriptions (caregivers pay, seniors protected)
- 10% partnerships (identity theft insurance upsell, elder law attorney referrals)

**Unit economics target:**
- CAC: $8-15 (Facebook ads targeting 35-55 age group with aging parents)
- LTV: $80-120 (10-15 month retention — peace-of-mind apps have high retention)
- LTV:CAC ratio: 8:1+

---

## 7. Virality Engine

**Built-in sharing loops:**
- "Protect another parent" — in-app upgrade to Family plan
- "Share your parent's safety status" — caregiver can share "Mom's been scam-free for 6 months" to family group chat
- "Recommend to a friend" — caregiver referral: "Your parents might need this too." $0 discount incentive.
- Holiday spike: "Before the holidays, make sure your parents are protected from gift card scams"
- Scam alert sharing: "A new Medicare scam is targeting seniors in [City]. Warn others →" with share button

**K-factor target:** 0.3 (word of mouth among siblings, friends with aging parents)

---

## 8. Technical Specification

**Scam Detection Pipeline (on-device):**
1. SMS/email received → on-device ML classifier → confidence score
2. URL detected → check against SafeGuard scam URL database (cached locally, updated daily)
3. Incoming call → caller ID check + spam score (Truecaller-like but privacy-first)
4. If confidence >70% → block + alert caregiver
5. If 50-70% → flag with warning + caregiver notification
6. All processing on-device. No message content leaves the phone.

**Backend:**
- Firebase Auth + Firestore (caregiver accounts, scam database sync)
- Cloud Functions (scam database aggregation, trending scam alerts)
- RevenueCat (subscriptions)

**Privacy (CORE DIFFERENTIATOR):**
- On-device AI for ALL message/content scanning
- Caregiver dashboard shows ALERTS (scam type, timestamp) — NEVER message content
- Senior's privacy is preserved. Caregiver knows about threats, not conversations.
- GDPR-compliant by architecture (no personal data leaves device)
- No third-party data sharing. Period.

---

## 9. 30-Day MVP Sprint Plan

| Week | Focus | Deliverable |
|------|-------|-------------|
| **1** | Auth + caregiver onboarding + senior invite flow | Working invite system, caregiver dashboard shell |
| **2** | SMS/email scam detection ML pipeline | Core ML model trained + running on-device |
| **3** | Call screening + alert system + caregiver notifications | Working scam alerts, push notifications |
| **4** | Polish, scam database, testing, App Store prep | Production build, scam DB v1, TestFlight |
| **Day 30** | App Store submission | iOS launch. Android in Week 6-8. |

---

## 10. Launch Checklist

- [ ] App Store Connect: metadata, screenshots (caregiver + senior views)
- [ ] Core ML model trained on 10K+ known scam patterns
- [ ] Scam URL database v1 populated (5K+ known phishing domains)
- [ ] RevenueCat products: $7.99/mo, $14.99/mo, $59.99/yr
- [ ] Landing page: safeguard-app.com with "Protect My Parents" CTA
- [ ] Facebook Ads setup: targeting adults 35-55, interests: "elderly care," "aging parents"
- [ ] Reddit launch: r/eldercare, r/agingparents, r/Scams
- [ ] Content: "How I Protected My Dad From Losing His Life Savings" founder story
- [ ] Press outreach: AARP, SeniorLiving, aging/eldercare publications

---

## 11. Post-Launch Iteration Plan

**30 days:** Android launch, scam database expansion to 50K+ URLs  
**60 days:** WhatsApp/Telegram scam scanning, web browsing protection (Safari/Chrome extension)  
**90 days:** AI voice scam detection (analyze scam call audio patterns)  
**180 days:** Identity theft monitoring integration, credit freeze one-tap  
**Annual:** Insurance partnership (elder fraud insurance add-on)

---

## 12. Anti-Patterns

- ❌ Don't read the senior's messages to the caregiver (privacy violation)
- ❌ Don't be surveillance — be protection. No location tracking, no social media monitoring.
- ❌ Don't block ALL unknown numbers (seniors need doctor calls, pharmacy calls)
- ❌ Don't require the senior to install/configure anything complex
- ❌ Don't be another "scam education" app — education without interception doesn't stop fraud
- ❌ Don't market as "spying on your parents" — market as "protecting your parents"

---

**Scaffold by:** Alex, VP of App Strategy  
**Pipeline:** App Discovery Daily — June 9, 2026  
**Note:** Pairful (couples planner, 7.05/10) was initially scaffolded in error due to Stage 4 calculation mistake. SafeGuard (7.15/10) is the correct winner. Pairful added to watchlist.
