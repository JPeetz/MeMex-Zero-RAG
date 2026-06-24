---
title: BiteSaver PRD — Full Prompt (Board Directive 2026-06-24)
type: synthesis
tags: ["bitesaver", "prd", "product", "board-directive", "recipe-app"]
created: 2026-06-24
author: marvin
---

# BiteSaver PRD — Full Prompt

## Board Directive — 2026-06-24

### Role
You are a world-class Senior Product Manager, Full-Stack Architect, Behavioral Designer, and Award-Winning UI/UX Expert (ex-Notion, ex-Figma, ex-Head of Product at a top recipe app).

### Mission
Create the definitive, production-ready Technical Specification and Product Requirements Document (PRD) for **BiteSaver** — the ultimate AI Recipe Vault & Social Cooking Companion.

---

## Core Vision

BiteSaver solves "recipe graveyards" and nightly "what's for dinner?" panic by owning the full pipeline:

1. Seamless social media capture
2. Intelligent organization
3. One-tap auto meal planning from the user's own library
4. Smart grocery lists
5. Gamified social cooking via CookStreak

---

## Market Context (Brutal Realism)

### Top Competitors
ReciMe, Paprika, AnyList, Mealime, Whisk

### What They Excel At
Basic import, lists, and scaling

### What They Fail At
True auto-planning from personal saves and compelling social accountability

### Table Stakes (Must Match or Exceed for Retention)
- Flawless TikTok/Instagram/YouTube link paste → auto-extract (ingredients, steps, time, video thumbnails)
- Aisle-organized grocery lists
- Recipe scaling
- Basic nutritional tagging

### Blue Ocean Differentiators (Defend Aggressively)
1. **One-tap Auto Weekly Meal Plan** — Generated exclusively from user's saved library with nutritional balance scoring and smart substitutions
2. **CookStreak** — Strava-like social challenges where friends compete on "recipes cooked" with photo proof, shared streaks, leaderboards, FOMO notifications

### Pricing
| Tier | Price |
|------|-------|
| Free | 25 recipes, basic features |
| Pro | $4.99/mo or $39.99/yr |
| Family | $7.99/mo or $69.99/yr |

- 7-day no-card Pro trial
- Target: 8-15% free-to-paid conversion

### Goal
Beat ReciMe on price/value while creating network effects that Paprika/AnyList cannot match quickly.

---

## Full App Features & Requirements (Implement All)

### Capture & Extraction
- Paste any TikTok/IG/YouTube/Reel link → AI-powered extraction of title, ingredients (with quantities), step-by-step instructions, cook time, servings, difficulty, cuisine tags, thumbnail
- Support manual add/edit with photo upload or voice dictation
- Offline-first saving

### Vault/Organization
- Beautiful personal library with folders, tags (e.g., "Weeknight", "High-Protein", "Family Favorites")
- Smart search/filter (by time, ingredients on hand, dietary)
- AI-suggested tagging

### Auto Meal Planner
- One-tap "Generate My Week" button — creates balanced 7-day plan (breakfast/lunch/dinner + snacks) using only user's saved recipes
- Nutritional scoring (calories, macros, balance)
- Substitutions for dietary restrictions (vegan, keto, allergies)
- "Use What I Have" pantry integration

### Smart Grocery Lists
- Auto-generated from meal plan or selected recipes
- Organized by supermarket aisle (produce, dairy, pantry, etc.)
- Sync to Instacart/Walmart (affiliate tracking)
- Shared Family lists with real-time updates

### CookStreak Social Layer
- Invite friends/families to challenges
- Monthly "Most Recipes Cooked" leaderboards
- Post "I Made This" photos with before/after, ratings, notes
- Shared streaks, comments, likes
- Viral invite system

### Cooking Mode
- Hands-free view with large text
- Built-in timers per step
- Progress checklist
- Voice-guided instructions
- Adjustable font/size for kitchen use

### Pro Features (Additional)
- Unlimited saves
- Advanced analytics (recipes tried vs. saved, cost tracking)
- Recipe scaling for parties
- Export/share
- Nutritional deep insights
- Priority AI extraction

### Family Plan Extras
- Shared vault
- Synced lists ("Mom added milk")
- Family challenges
- Profile-based dietary filters

### Monetization & Paywall
- RevenueCat integration
- Free tier generous for reviews
- Paywall after 25 saves or first full auto meal plan attempt
- Pause mode on cancellation

### Tech Stack & Architecture
- **Cross-platform:** React Native (iOS/Android) + responsive Web PWA
- **Database:** Local SQLite (offline-first priority) + Firebase (auth, social sync, real-time challenges) + Postgres (analytics)
- **AI:** On-device/edge for basic extraction + cloud (Groq/Claude/Gemini) for advanced planning. Stub advanced AI in MVP
- **Subscriptions:** RevenueCat with Small Business Program (15% Apple / 10-15% Google fees)
- **Other:** HealthKit/Apple Health optional for calorie tracking, deep links, push notifications, widgets (quick grocery view, daily dinner idea)

### Hooked Model Integration
- **External Triggers:** Friend challenge notifications, daily "What's for Dinner?" push, widget reminders
- **Internal Triggers:** Meal-time panic relief, streak dopamine, social FOMO
- **Variable Rewards:** Beautiful meal plan reveals, challenge wins, new recipe discoveries
- **Investment:** Building personal vault, friend connections, photo history, streaks

### First 30-Day MVP Scope
**Build:** Link import/extraction (parser + stub AI), vault organization, basic grocery list, rule-based meal planner, simple streaks, onboarding
**Fake:** Full social (local stubs), advanced AI
**Prioritize:** Offline functionality, kitchen-friendly cooking view, import accuracy
