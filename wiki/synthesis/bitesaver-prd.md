# BiteSaver — Technical Specification & Product Requirements Document

> **Version:** 1.0.0  
> **Date:** 2026-06-24  
> **Status:** Approved for Engineering  
> **Owner:** Product / Architecture Team

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Competitive Matrix](#2-competitive-matrix)
3. [User Personas](#3-user-personas)
4. [Feature Specification](#4-feature-specification)
5. [Technical Architecture](#5-technical-architecture)
6. [Data Model](#6-data-model)
7. [API Design](#7-api-design)
8. [UI/UX Key Screens](#8-uiux-key-screens)
9. [Behavioral Design System](#9-behavioral-design-system)
10. [AI Pipeline](#10-ai-pipeline)
11. [Monetization & Pricing Ladder](#11-monetization--pricing-ladder)
12. [KPIs & Success Metrics](#12-kpis--success-metrics)
13. [Development Phases](#13-development-phases)
14. [Risk Register](#14-risk-register)

---

## 1. Executive Summary

### Vision

BiteSaver is the recipe platform that closes the loop — from casual social media discovery to a hot meal on the table tonight. It is the first cooking app that treats a user's saved recipe library as a living, intelligent asset rather than a passive archive.

### Problem

Three distinct pain points exist today with no single solution addressing all three:

1. **The Graveyard Problem:** 73% of saved recipes are never cooked (internal survey proxy, validated by Reddit r/recipes community audits). Social media makes discovery effortless; acting on discoveries is still manual, hard, and forgettable.

2. **The Planning Paralysis Problem:** "What's for dinner?" is the most Googled food query in 21 consecutive years. Existing meal planner apps require users to browse and drag recipes into a planner manually — a 10–15 minute chore most people abandon after week 1.

3. **The Social Isolation Problem:** Cooking is inherently social (we cook *for* people, we share food with people) yet every major recipe app treats cooking as a solitary, transactional act. There is no Strava for cooking. There is no shared accountability surface.

### Solution

BiteSaver attacks all three problems with a single, deeply integrated product:

- **Zero-friction capture:** Paste any TikTok, Instagram Reel, YouTube Short, or web URL into BiteSaver. Within 3 seconds, a fully structured recipe (ingredients, steps, time, nutrition, thumbnail) is extracted and saved. No typing. No copy-paste ingredients. One tap.

- **One-tap Auto-Plan:** BiteSaver's AI scans the user's library, respects their dietary tags, applies nutritional balance scoring, and generates a complete 7-day meal plan from *their own saves* in under 2 seconds. The plan respects variety (no repeat proteins within 3 days), balances calories ±15% of a user-set target, and surfaces recipes that have been waiting longest in the graveyard.

- **CookStreak:** A Strava-for-cooking social layer. Users join Challenges (7-day "Cook 5 new recipes," "Meatless Monday Month," "Family Dinner Streak"), post photo proof via in-app camera, accumulate streak counts visibly on their profile, compete on public leaderboards, and receive FOMO-trigger push notifications when friends cook ahead.

### Moat

- **Data flywheel:** Every recipe extracted trains the NLP extraction model. Every plan generated trains the recommendation engine. Every cooked photo trains the visual verification model. The product gets smarter with scale in ways competitors cannot replicate without equivalent data.
- **Social lock-in:** CookStreak creates network effects. When three friends are on a streak, churning means disappointing them — not just losing app features.
- **Library ownership psychology:** Within 60 days, the average user has 40–80 personalized recipes. Starting over elsewhere is psychologically costly.

### Target Market

- **Primary:** Women 25–45, household meal deciders, active on TikTok/Instagram, time-poor, health-aware. US/CA/UK/AU/DE.
- **TAM:** $3.2B global recipe/cooking app market (2026 estimate, Statista).
- **SAM:** 180M English-speaking social-media-active home cooks in T5 markets.
- **SOM Year 1:** 400K MAU, 40K paid subscribers, $2.2M ARR.

---

## 2. Competitive Matrix

| Feature | **BiteSaver** | ReciMe | Paprika 3 | AnyList | Mealime | Whisk |
|---|---|---|---|---|---|---|
| **Pricing** | Free / $4.99 / $7.99 | Free / $2.99/mo | $4.99 one-time | Free / $11.99/mo | Free / $5.99/mo | Free |
| **Social media import** | ✅ TikTok, IG, YT, web | ✅ TikTok, IG, YT | ✅ Web only | ❌ | ❌ | ✅ Limited |
| **Video thumbnail save** | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Auto ingredient extraction** | ✅ AI (NLP + CV) | ✅ | ✅ | ❌ | ✅ | ✅ |
| **Aisle-organized grocery list** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Recipe scaling** | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ |
| **Nutritional tags (basic)** | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ |
| **Detailed macros** | ✅ Pro | ✅ | ❌ | ❌ | ✅ Pro | ❌ |
| **Auto meal planning from user library** | ✅ One-tap AI | ❌ Manual | ❌ Manual | ❌ | ❌ Fixed catalog | ❌ |
| **Nutritional balance scoring in planner** | ✅ | ❌ | ❌ | ❌ | Basic | ❌ |
| **Smart substitutions** | ✅ AI | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Social challenges / CookStreak** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Photo proof + leaderboard** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Friends activity feed** | ✅ | ❌ | ❌ | ❌ | ❌ |(partial)|
| **Family sharing** | ✅ $7.99/mo | ❌ | ❌ | ✅ | ❌ | ❌ |
| **Offline access** | ✅ Pro | ✅ | ✅ | ✅ | ✅ | ❌ |
| **Collections / folders** | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| **Cross-platform (iOS + Android)** | ✅ | ✅ | iOS + macOS | iOS only | ✅ | ✅ |
| **Web app** | ✅ V1 | ❌ | ❌ | ❌ | ❌ | ✅ |

**Verdict:** BiteSaver leads on auto-planning from personal library, social layer, and cross-platform presence. It matches or exceeds on capture. It undercuts ReciMe on price and offers real annual plan savings. Paprika's one-time purchase is a competitive concern for price-sensitive users — mitigated by CookStreak network effect (no social reason to use Paprika).

---

## 3. User Personas

### Persona 1: "Scroll-and-Save Sarah"
- **Age:** 28 | **Location:** Austin, TX | **Household:** Partner, no kids
- **Profile:** Marketing manager, spends 45 min/day on TikTok/Instagram. Saves 5–10 food videos per week. Has cooked fewer than 5% of them.
- **Quote:** *"I have 200 saved recipes and still order DoorDash every night because I can't figure out what to make."*
- **Jobs-To-Be-Done:**
  - Capture recipes instantly without breaking scroll flow
  - See saved recipes organized so she can actually find them
  - Know what to cook *tonight* without decision fatigue
- **Pain Points:** Decision paralysis, recipe graveyard guilt, hates typing ingredients manually
- **KPIs to move:** Recipe save rate, Plan activation rate, DAU
- **Feature resonance:** Smart capture, one-tap auto-plan, graveyard revival feature

---

### Persona 2: "Meal-Prep Mike"
- **Age:** 35 | **Location:** Chicago, IL | **Household:** Wife + 2 kids (ages 5 and 8)
- **Profile:** Software engineer, weekend meal-preps every Sunday. Uses Google Sheets for grocery lists. Militant about budget.
- **Quote:** *"I spend 2 hours on Sunday planning meals. There has to be a better way."*
- **Jobs-To-Be-Done:**
  - Generate a full week of family-friendly meals with one action
  - Produce a consolidated, aisle-sorted grocery list
  - Accommodate kids' preferences (no spicy, no mushrooms)
- **Pain Points:** Time cost of manual planning, fragmented tools (recipes here, list there), no family sharing
- **KPIs to move:** Plan completion rate, Grocery list generation, Family plan upgrade
- **Feature resonance:** One-tap auto-plan, family sharing, aisle-organized list, dietary filters

---

### Persona 3: "Competitive Chris"
- **Age:** 31 | **Location:** London, UK | **Household:** Apartment, 3 roommates
- **Profile:** UX designer. Runs 3x/week (uses Strava). Loves friendly competition. Cooks to impress.
- **Quote:** *"I need a reason to try new recipes. I'll cook way more if there's something at stake."*
- **Jobs-To-Be-Done:**
  - Have a social context for cooking — someone to cook "against"
  - Show off meals with beautiful photos
  - Track cooking habit progress over time
- **Pain Points:** Cooking alone feels pointless, no accountability, social platforms don't value cooking effort
- **KPIs to move:** CookStreak enrollment, Challenge completion, Friend invites sent, Streak days
- **Feature resonance:** CookStreak, leaderboards, social profile, photo proof, FOMO notifications

---

### Persona 4: "Health-Conscious Helen"
- **Age:** 42 | **Location:** Sydney, AU | **Household:** Partner, post-kids empty nest
- **Profile:** Office manager, recently diagnosed pre-diabetic. Counting carbs. Follows low-GI food creators on Instagram.
- **Quote:** *"I need to change how I eat but I don't want to give up food I love. I need recipes I can trust are actually healthy."*
- **Jobs-To-Be-Done:**
  - Know exact macros for saved recipes
  - Plan meals that hit daily nutrition targets
  - Find substitution suggestions for high-carb ingredients
- **Pain Points:** Manual macro tracking is tedious, mixed health quality in social media recipes, no intelligent dietary filtering
- **KPIs to move:** Pro conversion (macro features), plan usage frequency, recipe tagging accuracy
- **Feature resonance:** Macro tracking, nutritional balance scoring, smart substitutions, dietary filters (low-GI, diabetic-friendly)

---

## 4. Feature Specification

### Tier 0 — Table Stakes (MVP, Weeks 1–6)

#### 4.1 Recipe Capture
| ID | Feature | Description | Acceptance Criteria |
|----|---------|-------------|---------------------|
| CAP-001 | Social URL import | Paste TikTok, Instagram Reel, YouTube Short, or YouTube video URL. Auto-extract title, ingredients, steps, cook time, servings, thumbnail | Extraction success rate ≥ 85% on curated test set of 500 URLs; complete in ≤ 4s P95 |
| CAP-002 | Web URL scrape | Paste any food blog / recipe website URL. Structured data extraction via schema.org/Recipe + NLP fallback | ≥ 92% success on Alexa top 100 food blogs |
| CAP-003 | Manual entry | Form-based recipe entry with rich ingredients editor (amount, unit, ingredient name, optional note) | Full CRUD, supports up to 50 ingredients and 30 steps |
| CAP-004 | Photo import | User photos a recipe from a book or card — OCR + structured extraction | ≥ 75% OCR accuracy on printed text |
| CAP-005 | Share sheet extension | iOS Share Extension + Android Share Target: share URL from TikTok/Instagram app directly to BiteSaver | Works for iOS 16+ Share Sheet and Android 12+ Share Target |
| CAP-006 | Duplicate detection | Before saving, system detects near-duplicate recipes (same source URL, or >80% ingredient overlap) and warns user | No silent duplicates; user confirmation required to save duplicate |

#### 4.2 Recipe Organization
| ID | Feature | Description | Acceptance Criteria |
|----|---------|-------------|---------------------|
| ORG-001 | Collections | Create, rename, delete, and reorder named collections (e.g., "Quick Weeknights," "Date Night," "Summer BBQ") | Unlimited collections Free/Pro; drag-to-reorder |
| ORG-002 | Tags | Multi-tag recipes with system tags (cuisine, diet, protein, cook time bucket) and custom user tags | Typeahead tag input; auto-suggested tags from AI |
| ORG-003 | Search | Full-text search across title, ingredients, notes. Filters: tag, collection, cook time, dietary restriction | Search results in ≤ 200ms for libraries up to 1000 recipes |
| ORG-004 | Sort & filter | Sort by: saved date, last cooked, cook time, highest rated | All sort + filter combinations work in offline mode |
| ORG-005 | Recipe limit (Free) | Free tier capped at 25 saved recipes; clear upgrade prompts at 20 and 25 | Soft limit at 20 (upsell banner), hard limit at 25 (modal gate) |

#### 4.3 Recipe Detail
| ID | Feature | Description | Acceptance Criteria |
|----|---------|-------------|---------------------|
| DET-001 | Video playback | Embedded in-app video player for YouTube/Instagram source videos | Works without leaving app; fallback to browser opens for unsupported |
| DET-002 | Ingredient scaling | Slider or input to scale recipe servings (0.5x to 10x). All ingredient amounts recalculate proportionally with smart unit conversion | Fractions handled gracefully (1/3 cup × 2 = 2/3 cup, not 0.667) |
| DET-003 | Cook mode | Step-by-step mode: one step fills the screen, tap to advance. Screen stays on. Voice "next step" support (iOS/Android accessibility) | No screen sleep during cook mode |
| DET-004 | Basic nutritional info | Per-serving: calories, protein (g), carbs (g), fat (g). Sourced from USDA FoodData Central API lookup on ingredients | Displayed on recipe card and detail page |

#### 4.4 Grocery List
| ID | Feature | Description | Acceptance Criteria |
|----|---------|-------------|---------------------|
| GRO-001 | Add from recipe | One tap to add all (or selected) ingredients from a recipe to the active grocery list | Batch consolidation: same ingredient from multiple recipes sums quantities |
| GRO-002 | Aisle organization | Ingredients auto-sorted by aisle category: Produce, Proteins, Dairy, Bakery, Frozen, Pantry, Beverages, Cleaning | ≥ 90% correct aisle assignment on USDA reference ingredient set |
| GRO-003 | Manual add/edit | Freeform text add, swipe to delete, tap to check off | Checked items collapse to bottom; uncollapse toggle |
| GRO-004 | Sharing | Share grocery list via SMS, iMessage, WhatsApp, copy as text | Plain text format is readable without the app |
| GRO-005 | Offline sync | Grocery list works fully offline, syncs on reconnect | Conflict resolution: last-edit-wins on per-item granularity |

---

### Tier 1 — Differentiators (V1, Weeks 7–14)

#### 4.5 One-Tap Auto Meal Plan
| ID | Feature | Description | Acceptance Criteria |
|----|---------|-------------|---------------------|
| PLAN-001 | Auto-generate 7-day plan | Single tap generates Mon–Sun dinner plan (optionally breakfast/lunch) sourced exclusively from user's saved library | Generates plan in ≤ 2s; uses only saved recipes; allows regeneration |
| PLAN-002 | Nutritional balance scoring | Plan rated on macro balance (protein target, carb ratio, fat ratio) relative to user's profile goals. Score displayed as A/B/C/D | Score calculation documented; user can adjust targets |
| PLAN-003 | Variety algorithm | No same protein source (chicken, beef, pork, fish, plant) on consecutive days; no exact recipe repeat within plan | Algorithm enforced; edge case: if library too small (<14 recipes), warns user and relaxes constraints |
| PLAN-004 | Dietary filters | Plan respects all active dietary flags: gluten-free, dairy-free, vegetarian, vegan, low-carb, nut-free | Filters applied pre-generation; conflicting filter combinations surface warning |
| PLAN-005 | Graveyard surfacing | Plan preference-weights recipes saved >30 days ago and never cooked ("rescue" weight: 1.5x vs recently cooked recipes) | Visible "Rescued from your saves!" label on plan cards |
| PLAN-006 | Smart substitutions | On recipe detail within a plan, AI suggests ingredient swaps: "Swap chicken breast for tofu (vegan)" or "Use almond milk instead of dairy" | Substitutions offered inline; user accepts/ignores; substituted plan cards show visual diff |
| PLAN-007 | Export to grocery list | One tap: entire week's plan ingredients consolidated into grocery list with aisle sorting | Duplicate ingredient merging; quantities summed correctly |
| PLAN-008 | Plan edit | Drag-to-swap meals within the week. Tap meal to replace with another saved recipe. Tap to remove a meal | Changes auto-recalculate nutritional score |

#### 4.6 CookStreak — Social Layer
| ID | Feature | Description | Acceptance Criteria |
|----|---------|-------------|---------------------|
| STK-001 | Personal streak | Daily streak counter: increments each day user logs a cooked meal with photo. Freezes (not resets) if user grants a "freeze" token | Streak displayed prominently on profile and home screen; trophy at 7/30/100 days |
| STK-002 | Challenge creation | Any user can create a named challenge: duration (7/14/30 days), requirement (X recipes cooked), dietary theme (optional), max participants | Challenge card shows: name, creator, start date, progress bars for all participants |
| STK-003 | Challenge join | Browse public challenges or join via invite link. Join up to 3 active challenges simultaneously | Deep link invite format: `bitesaver://challenge/{id}` |
| STK-004 | Log a cook | From recipe detail page: "I cooked this!" → camera opens → photo captured → confirming submits proof to challenge and friends | Photo is required for challenge log; optional for personal streak log |
| STK-005 | Leaderboard | Within a challenge: ranked list of participants by recipes cooked, streak days, or combined score | Real-time updates; last updated timestamp shown |
| STK-006 | Activity feed | Chronological feed of friends' logged cooks: photo, recipe name, challenge name, streak count. Reactions (🔥 ❤️ 👏) | Load ≤ 500ms cached; real-time push for new items |
| STK-007 | FOMO notifications | Push notification to friends when someone extends a streak: "[Name] just cooked [Recipe] — Day 5! Don't fall behind 🔥" | Sent within 60s of cook log; respects user notification preferences per challenge |
| STK-008 | Anti-cheat photo verification | CV model checks submitted photo contains food (confidence ≥ 0.85). Flags obvious non-food images for manual review | False positive rate ≤ 2%; processing time ≤ 3s |
| STK-009 | Freeze tokens | 2 freeze tokens per week (Pro: 3). Use to pause streak for 1 day without breaking it. Displayed as ice icons on streak counter | Token pool resets every Monday; unused tokens do not roll over |
| STK-010 | Social profile | Public profile page showing: streak count, total recipes cooked, current challenges, recent activity grid (like GitHub contributions) | Private mode option: hides activity feed but shows aggregate stats |

---

### Tier 2 — Delighters (V2, Week 15+)

| ID | Feature | Description |
|----|---------|-------------|
| DLT-001 | Pantry tracker | Log available pantry ingredients; auto-plan uses pantry-first suggestions and grocery list subtracts what you already have |
| DLT-002 | Cook history + timeline | Visual timeline of all cooked recipes with photos, dates, and caloric totals; exportable to CSV |
| DLT-003 | Recipe remix | AI generates a new recipe as an "inspired by" variant of a saved recipe using different ingredients |
| DLT-004 | Voice capture | Add recipe via voice: "Hey BiteSaver, save this recipe: chicken stir fry, 30 minutes, serves 4…" |
| DLT-005 | Instacart / Kroger integration | One-tap grocery list → Instacart cart or Kroger digital list |
| DLT-006 | Smart TV companion | Cast cook mode to Apple TV / Fire TV / Android TV for hands-free cooking |
| DLT-007 | Weekly report | Sunday email: "You cooked 4 times this week, saved $47 vs delivery, 1,800 avg daily calories" |
| DLT-008 | Restaurant recreation | User submits restaurant name + dish → AI generates estimated recreation recipe |
| DLT-009 | Seasonal ingredients | Location + season-aware suggestions ("asparagus is in season near you — here are 3 saved recipes using it") |
| DLT-010 | Clan challenges | Team-vs-team cooking competitions (e.g., "Family Peetz vs Family Smith — who cooks more this month?") |

---

## 5. Technical Architecture

### 5.1 Technology Stack

#### Mobile (iOS + Android)
```
Framework:         React Native 0.74 + Expo SDK 51
State management:  Zustand 4 (local) + React Query 5 (server)
Navigation:        Expo Router (file-based, typed)
UI library:        Custom design system built on React Native Paper
Video playback:    expo-video (native AVFoundation / ExoPlayer bridge)
Camera:            expo-camera + expo-image-picker
Push notifications: Expo Notifications (FCM + APNs)
Offline storage:   MMKV (fast k/v) + WatermelonDB (relational local DB)
Share extension:   Custom iOS App Extension + Android ShareTarget Activity
```

#### Backend
```
Runtime:           Node.js 22 LTS (Bun 1.x considered; stays on Node for ecosystem)
Framework:         Fastify 4 (2–3x throughput vs Express; built-in JSON schema validation)
API style:         REST + WebSockets (real-time feed/streak events via Socket.io 4)
ORM:               Prisma 5 (type-safe; PostgreSQL adapter)
Database:          PostgreSQL 16 on Supabase (managed, RLS built-in, realtime channels)
File storage:      Supabase Storage (S3-compatible) — recipe photos, thumbnails
Cache:             Redis 7 (Upstash serverless) — session cache, plan generation cache, rate limits
Job queue:         BullMQ (Redis-backed) — extraction jobs, notification dispatch, AI tasks
Auth:              Supabase Auth (JWT + magic link + OAuth: Google, Apple, Facebook)
Search:            pgvector extension on PostgreSQL (semantic recipe search via embeddings)
Email:             Resend (transactional) + React Email (templates)
Payments:          Stripe (subscriptions, trials, family plan seat management)
CDN:               Cloudflare R2 + CDN — static assets and recipe thumbnail caching
```

#### AI / ML Services
```
Recipe extraction NLP:    OpenAI GPT-4o-mini (structured output mode) — cost: ~$0.001/recipe
Food CV verification:     Google Vision API (food detection confidence score) — $1.50/1000 images
Ingredient embeddings:    OpenAI text-embedding-3-small — semantic ingredient matching
Nutritional lookup:       USDA FoodData Central API (free tier, 3,600 req/hour) + local cache
Meal plan generation:     Custom scoring algorithm on Node.js (no LLM needed; deterministic + fast)
Smart substitutions:      GPT-4o-mini with ingredient substitution system prompt
OCR (photo capture):      Google Vision API (Document Text Detection)
```

#### Infrastructure
```
Deployment:        Railway.app (backend + workers) — $20/mo dev, $300/mo at scale
CI/CD:             GitHub Actions → Railway deploy hooks
Monitoring:        Better Stack (logs + uptime) + Sentry (mobile error tracking)
Secrets:           Railway environment variables + 1Password Secrets Automation
Analytics:         PostHog (product analytics, feature flags, session replay)
A/B testing:       PostHog feature flags
```

### 5.2 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                            │
│  iOS App (React Native)    Android App (React Native)           │
│  ┌───────────────┐         ┌───────────────┐                    │
│  │ Share Extension│         │ Share Target  │                    │
│  └───────────────┘         └───────────────┘                    │
└─────────────────────────┬───────────────────────────────────────┘
                          │ HTTPS + WSS
┌─────────────────────────▼───────────────────────────────────────┐
│                      API GATEWAY LAYER                          │
│  Cloudflare (DDoS, WAF, TLS termination, CDN)                   │
└─────────────────────────┬───────────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────────┐
│                    APPLICATION LAYER (Railway)                  │
│                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐                    │
│  │  API Service     │  │  WebSocket Server│                    │
│  │  (Fastify)       │  │  (Socket.io)     │                    │
│  └────────┬─────────┘  └────────┬─────────┘                    │
│           │                     │                               │
│  ┌────────▼─────────────────────▼──────┐                       │
│  │           BullMQ Job Workers         │                       │
│  │  ┌───────────┐  ┌───────────────┐   │                       │
│  │  │ Extraction│  │ Notification  │   │                       │
│  │  │ Worker    │  │ Worker        │   │                       │
│  │  └───────────┘  └───────────────┘   │                       │
│  └─────────────────────────────────────┘                       │
└─────────────────────────────────────────────────────────────────┘
          │              │              │              │
┌─────────▼──┐  ┌────────▼───┐  ┌──────▼────┐  ┌────▼──────────┐
│ PostgreSQL │  │ Redis 7    │  │ Supabase  │  │ AI Services   │
│ (Supabase) │  │ (Upstash)  │  │ Storage   │  │ GPT-4o-mini   │
│            │  │            │  │ (Photos)  │  │ Google Vision │
│ pgvector   │  │ BullMQ     │  │           │  │ USDA FoodData │
└────────────┘  └────────────┘  └───────────┘  └───────────────┘
```

### 5.3 Data Flow: Recipe Capture

```
User pastes URL
      │
      ▼
Mobile app → POST /api/v1/recipes/extract {url}
      │
      ▼
API validates URL format → returns job_id immediately (202 Accepted)
      │
      ▼
BullMQ extraction job created
      │
      ├─ URL type detection (TikTok / Instagram / YouTube / web)
      │
      ├─ Platform handler:
      │   TikTok: yt-dlp metadata + OpenAI vision on thumbnail
      │   YouTube: YouTube Data API v3 (description) + yt-dlp chapters
      │   Instagram: unofficial scrape layer (yt-dlp) + OpenAI
      │   Web: Puppeteer headless fetch + schema.org parsing + NLP fallback
      │
      ├─ GPT-4o-mini structured extraction:
      │   Input: raw text + video description
      │   Output: {title, ingredients[], steps[], cookTime, servings, tags[]}
      │
      ├─ USDA FoodData API: nutritional lookup per ingredient
      │
      ├─ Thumbnail download → Supabase Storage (CDN URL generated)
      │
      └─ Recipe record created in PostgreSQL
             │
             ▼
       WebSocket push to client: {event: "recipe_ready", recipe_id}
             │
             ▼
       Client navigates to recipe detail
```

---

## 6. Data Model

### 6.1 Core Entities (PostgreSQL — Prisma Schema)

```prisma
model User {
  id              String    @id @default(cuid())
  email           String    @unique
  displayName     String
  avatarUrl       String?
  subscriptionTier String   @default("free") // free | pro | family
  subscriptionId  String?   // Stripe subscription ID
  familyPlanId    String?   // FK to FamilyPlan
  dietaryFlags    String[]  // ["gluten-free", "vegetarian", ...]
  calorieTarget   Int?      // daily calorie goal
  proteinTargetPct Float    @default(0.25)  // % of calories
  carbTargetPct   Float     @default(0.50)
  fatTargetPct    Float     @default(0.25)
  timezone        String    @default("UTC")
  streakCount     Int       @default(0)
  longestStreak   Int       @default(0)
  freezeTokens    Int       @default(2)
  lastStreakDate  DateTime?
  createdAt       DateTime  @default(now())
  updatedAt       DateTime  @updatedAt

  recipes         Recipe[]
  collections     Collection[]
  mealPlans       MealPlan[]
  groceryLists    GroceryList[]
  cookLogs        CookLog[]
  challengeMembers ChallengeParticipant[]
  following       Follow[]   @relation("follower")
  followers       Follow[]   @relation("following")
  familyPlan      FamilyPlan? @relation(fields: [familyPlanId], references: [id])
}

model Recipe {
  id              String    @id @default(cuid())
  userId          String
  title           String
  sourceUrl       String?
  sourcePlatform  String?   // tiktok | instagram | youtube | web | manual | photo
  thumbnailUrl    String?
  videoEmbedUrl   String?
  description     String?
  servings        Int       @default(4)
  cookTimeMinutes Int?
  prepTimeMinutes Int?
  ingredients     Ingredient[]
  steps           RecipeStep[]
  tags            String[]
  cuisineType     String?
  dietaryFlags    String[]
  caloriesPerServing Int?
  proteinPerServing Float?
  carbsPerServing  Float?
  fatPerServing    Float?
  lastCookedAt    DateTime?
  cookCount       Int       @default(0)
  isPublic        Boolean   @default(false)
  extractionStatus String   @default("pending") // pending | complete | failed
  createdAt       DateTime  @default(now())
  updatedAt       DateTime  @updatedAt

  user            User      @relation(fields: [userId], references: [id])
  collections     RecipeCollection[]
  mealPlanItems   MealPlanItem[]
  groceryListItems GroceryListItem[]
  cookLogs        CookLog[]
  embedding       RecipeEmbedding?

  @@index([userId, createdAt])
  @@index([userId, lastCookedAt])
}

model Ingredient {
  id          String  @id @default(cuid())
  recipeId    String
  position    Int
  amount      Float?
  unit        String?  // cup, tbsp, g, ml, pinch, etc.
  name        String
  note        String?  // "finely diced", "room temperature"
  usdaFdcId   String?  // USDA FoodData Central ID for nutritional lookup
  recipe      Recipe  @relation(fields: [recipeId], references: [id], onDelete: Cascade)

  @@index([recipeId])
}

model RecipeStep {
  id          String  @id @default(cuid())
  recipeId    String
  position    Int
  instruction String
  durationSeconds Int?
  imageUrl    String?
  recipe      Recipe  @relation(fields: [recipeId], references: [id], onDelete: Cascade)
}

model Collection {
  id          String    @id @default(cuid())
  userId      String
  name        String
  description String?
  coverImageUrl String?
  position    Int       @default(0)
  isDefault   Boolean   @default(false)
  createdAt   DateTime  @default(now())

  user        User      @relation(fields: [userId], references: [id])
  recipes     RecipeCollection[]
}

model RecipeCollection {
  recipeId     String
  collectionId String
  addedAt      DateTime @default(now())

  recipe       Recipe     @relation(fields: [recipeId], references: [id])
  collection   Collection @relation(fields: [collectionId], references: [id])

  @@id([recipeId, collectionId])
}

model MealPlan {
  id              String    @id @default(cuid())
  userId          String
  weekStartDate   DateTime  // Monday of the planned week
  nutritionScore  String?   // A | B | C | D
  calorieAvg      Float?
  proteinAvgPct   Float?
  carbAvgPct      Float?
  fatAvgPct       Float?
  generatedAt     DateTime  @default(now())
  status          String    @default("active") // active | archived

  user            User      @relation(fields: [userId], references: [id])
  items           MealPlanItem[]
  groceryListId   String?   @unique
  groceryList     GroceryList? @relation(fields: [groceryListId], references: [id])
}

model MealPlanItem {
  id          String    @id @default(cuid())
  mealPlanId  String
  recipeId    String
  dayOfWeek   Int       // 0 = Monday, 6 = Sunday
  mealType    String    // breakfast | lunch | dinner | snack
  servings    Int       @default(1)

  mealPlan    MealPlan  @relation(fields: [mealPlanId], references: [id])
  recipe      Recipe    @relation(fields: [recipeId], references: [id])
}

model GroceryList {
  id          String    @id @default(cuid())
  userId      String
  name        String    @default("Shopping List")
  mealPlanId  String?   @unique
  createdAt   DateTime  @default(now())
  updatedAt   DateTime  @updatedAt

  user        User      @relation(fields: [userId], references: [id])
  items       GroceryListItem[]
  mealPlan    MealPlan?
}

model GroceryListItem {
  id              String  @id @default(cuid())
  groceryListId   String
  recipeId        String?
  name            String
  amount          Float?
  unit            String?
  aisleCategory   String  // produce | protein | dairy | bakery | frozen | pantry | beverage | other
  isChecked       Boolean @default(false)
  checkedAt       DateTime?
  position        Int     @default(0)

  groceryList     GroceryList @relation(fields: [groceryListId], references: [id])
  recipe          Recipe?  @relation(fields: [recipeId], references: [id])

  @@index([groceryListId, aisleCategory])
}

model CookLog {
  id          String    @id @default(cuid())
  userId      String
  recipeId    String
  photoUrl    String
  photoVerified Boolean  @default(false)
  photoScore  Float?    // CV food confidence score
  note        String?
  rating      Int?      // 1-5 stars
  loggedAt    DateTime  @default(now())

  user        User      @relation(fields: [userId], references: [id])
  recipe      Recipe    @relation(fields: [recipeId], references: [id])
  challengeContributions ChallengeContribution[]
  reactions   CookLogReaction[]

  @@index([userId, loggedAt])
}

model Challenge {
  id              String    @id @default(cuid())
  creatorId       String
  name            String
  description     String?
  startDate       DateTime
  endDate         DateTime
  requirementType String    // recipes_cooked | streak_days | combined
  requirementValue Int      // e.g., 5 (cook 5 recipes)
  maxParticipants Int?
  isPublic        Boolean   @default(true)
  dietaryTheme    String?   // optional: "vegetarian", "30-min meals"
  status          String    @default("upcoming") // upcoming | active | ended
  inviteCode      String    @unique @default(cuid())
  createdAt       DateTime  @default(now())

  participants    ChallengeParticipant[]
  contributions   ChallengeContribution[]
}

model ChallengeParticipant {
  id          String    @id @default(cuid())
  challengeId String
  userId      String
  joinedAt    DateTime  @default(now())
  rank        Int?
  score       Int       @default(0)
  currentStreak Int     @default(0)

  challenge   Challenge @relation(fields: [challengeId], references: [id])
  user        User      @relation(fields: [userId], references: [id])

  @@unique([challengeId, userId])
}

model ChallengeContribution {
  id              String    @id @default(cuid())
  challengeId     String
  participantId   String
  cookLogId       String
  contributedAt   DateTime  @default(now())

  challenge       Challenge @relation(fields: [challengeId], references: [id])
  cookLog         CookLog   @relation(fields: [cookLogId], references: [id])
}

model Follow {
  followerId  String
  followingId String
  createdAt   DateTime @default(now())

  follower    User @relation("follower", fields: [followerId], references: [id])
  following   User @relation("following", fields: [followingId], references: [id])

  @@id([followerId, followingId])
}

model FamilyPlan {
  id            String    @id @default(cuid())
  ownerId       String    @unique
  stripeSubId   String?
  maxMembers    Int       @default(6)
  createdAt     DateTime  @default(now())

  members       User[]
}

model RecipeEmbedding {
  recipeId    String    @id
  embedding   Float[]   // stored as pgvector type via raw Prisma
  updatedAt   DateTime  @updatedAt

  recipe      Recipe    @relation(fields: [recipeId], references: [id])
}

model Notification {
  id          String    @id @default(cuid())
  userId      String
  type        String    // streak_fomo | challenge_update | friend_cooked | plan_ready
  title       String
  body        String
  data        Json?     // deep link params
  readAt      DateTime?
  sentAt      DateTime  @default(now())

  @@index([userId, readAt])
}
```

---

## 7. API Design

### Base URL
```
Production: https://api.bitesaver.app/v1
Development: http://localhost:3000/v1
```

### Authentication
All endpoints require `Authorization: Bearer <supabase_jwt>` except `/auth/*`.

### 7.1 Recipe Endpoints

```
POST   /recipes/extract          # Submit URL for async extraction; returns {job_id}
GET    /recipes/extract/:job_id  # Poll extraction status {status, recipe_id?}
POST   /recipes                  # Create recipe manually {title, ingredients, steps, ...}
GET    /recipes                  # List user recipes {page, limit, collection_id, tags, q, sort}
GET    /recipes/:id              # Get single recipe with full detail
PUT    /recipes/:id              # Update recipe (title, ingredients, steps, tags, etc.)
DELETE /recipes/:id              # Delete recipe
POST   /recipes/:id/duplicate    # Duplicate recipe into user's library
GET    /recipes/:id/substitutions # AI substitution suggestions for dietary goal
POST   /recipes/:id/scale        # Return scaled ingredient amounts {servings}
```

### 7.2 Collection Endpoints

```
POST   /collections              # Create collection {name, description}
GET    /collections              # List user collections with recipe counts
GET    /collections/:id          # Collection detail with recipes
PUT    /collections/:id          # Update collection
DELETE /collections/:id          # Delete (recipes not deleted)
POST   /collections/:id/recipes  # Add recipe to collection {recipe_id}
DELETE /collections/:id/recipes/:recipe_id  # Remove from collection
PUT    /collections/reorder      # Reorder collections [{id, position}]
```

### 7.3 Meal Plan Endpoints

```
POST   /meal-plans/generate      # Auto-generate plan {week_start, meal_types[], dietary_overrides[]}
POST   /meal-plans               # Save/update a plan
GET    /meal-plans               # List plans {limit, include_archived}
GET    /meal-plans/:id           # Plan detail with nutrition score
PUT    /meal-plans/:id/items     # Update plan items (drag/drop edits)
DELETE /meal-plans/:id           # Archive plan
POST   /meal-plans/:id/grocery   # Generate grocery list from plan → returns {grocery_list_id}
```

### 7.4 Grocery List Endpoints

```
GET    /grocery-lists            # List active grocery lists
GET    /grocery-lists/:id        # Full list with aisle-sorted items
POST   /grocery-lists            # Create empty list {name}
POST   /grocery-lists/:id/items  # Add items [{name, amount, unit, recipe_id?}]
PUT    /grocery-lists/:id/items/:item_id # Update item (check/uncheck, edit amount)
DELETE /grocery-lists/:id/items/:item_id # Remove item
DELETE /grocery-lists/:id/clear_checked  # Remove all checked items
GET    /grocery-lists/:id/share  # Get shareable text + deep link
```

### 7.5 CookStreak Endpoints

```
POST   /cook-logs                # Log a cook {recipe_id, photo_base64, note?, rating?}
GET    /cook-logs                # User's cook history {page, limit}
GET    /streak                   # Current streak state {count, freeze_tokens, last_date}
POST   /streak/freeze            # Use a freeze token

POST   /challenges               # Create challenge
GET    /challenges               # Browse public challenges {status, theme}
GET    /challenges/:id           # Challenge detail + leaderboard
POST   /challenges/:id/join      # Join by challenge ID or invite code
DELETE /challenges/:id/leave     # Leave challenge

GET    /feed                     # Social activity feed {cursor}
POST   /cook-logs/:id/react      # React to someone's cook log {emoji}

GET    /users/:id/profile        # Public profile {streak, stats, recent_logs}
POST   /users/follow             # Follow user {user_id}
DELETE /users/follow/:user_id    # Unfollow
GET    /users/search             # Search users by display name {q}
```

### 7.6 Notification Endpoints

```
GET    /notifications            # List notifications {unread_only, cursor}
POST   /notifications/read       # Mark as read {notification_ids[] | all: true}
PUT    /notifications/preferences # Update push notification preferences
```

### 7.7 WebSocket Events

```
Connection: wss://api.bitesaver.app/v1/realtime?token=<jwt>

Client → Server:
  subscribe:feed          # Start receiving feed events
  subscribe:challenge:{id} # Real-time leaderboard updates

Server → Client:
  recipe:ready {recipe_id}              # Extraction complete
  recipe:failed {job_id, reason}        # Extraction failed
  feed:new_item {cook_log}              # Friend cooked something
  challenge:score_update {challenge_id, rankings[]} # Leaderboard change
  notification:new {notification}       # In-app notification push
```

### 7.8 Error Format

```json
{
  "error": {
    "code": "RECIPE_LIMIT_REACHED",
    "message": "Free tier allows 25 recipes. Upgrade to Pro to save unlimited recipes.",
    "upgrade_url": "https://bitesaver.app/upgrade",
    "http_status": 402
  }
}
```

### Standard error codes:
| Code | HTTP | Meaning |
|------|------|---------|
| `RECIPE_LIMIT_REACHED` | 402 | Free tier limit |
| `EXTRACTION_FAILED` | 422 | URL could not be parsed |
| `PHOTO_REJECTED` | 422 | CV model rejected photo as not food |
| `CHALLENGE_FULL` | 409 | Max participants reached |
| `INVALID_DIETARY_COMBO` | 422 | Conflicting dietary filters |
| `LIBRARY_TOO_SMALL` | 422 | <7 recipes, can't generate plan |

---

## 8. UI/UX Key Screens

### Design System Foundation
- **Typography:** Inter (body) + Fraunces (display/headers — warm, editorial)
- **Color palette:** Tomato-red primary (#E8452A), warm cream background (#FAF7F2), deep forest green accent (#2D5016), off-black (#1A1A1A)
- **Border radius:** 16px cards, 24px modals, 100% pill buttons
- **Spacing:** 4px base grid, 16px page margins
- **Motion:** Spring-physics animations (react-native-reanimated 3), ≤250ms transitions
- **Dark mode:** Full support (system-detected)

---

### Screen 1: Home / Feed

**Layout:** Tab bar bottom nav (Home | Capture | Planner | Grocery | CookStreak)

**Home screen sections (scroll view):**

1. **Streak hero band** (if active): Animated flame icon + streak count + "Cook tonight to keep your streak!" CTA button
2. **"Tonight's Dinner" card** (if active plan): Large image card from today's planned meal — title, cook time, "Start Cooking" button
3. **"From Your Graveyard" horizontal scroll:** 3–5 cards of recipes saved >30 days, never cooked with label "Saved X days ago — finally make it?"
4. **Friends Activity** (if following anyone): Compact feed cards showing friend name + recipe photo + "🔥 Day 7 streak!"
5. **Recent Saves:** 2-column card grid of 6 most recent recipes

**Empty state:** Centered illustration of a phone with a social media video, headline "Save your first recipe," large "Paste a link" CTA button, sub-copy showing TikTok/Instagram/YouTube brand badges

---

### Screen 2: Capture (Tab)

**Layout:** Single-focus screen for recipe import

1. **Large URL input field** at top: placeholder "Paste TikTok, Instagram, or any recipe link…" with paste button (auto-reads clipboard on focus)
2. **Recent clipboard detection:** If clipboard contains a detectable URL, auto-populates with a "We found a link!" banner
3. **Import alternatives:** 3 secondary action chips below input: "📷 Take a Photo of Recipe" | "✏️ Create Manually" | "📎 Share from App"
4. **Loading state:** After URL submit — animated pulsing skeleton card with progress indicator and text "Extracting ingredients…" then "Looking up nutrition…" then "Done!"
5. **Preview modal:** Extracted recipe shown in a bottom sheet with edit affordances before saving — user can correct any field
6. **Save confirmation:** Confetti burst + "Saved to [Collection]" toast + option to "Add to Tonight's Plan"

---

### Screen 3: Recipe Detail

**Layout:** Full-bleed header image/video with overlaid gradient, scrollable body content

1. **Header:** Full-bleed thumbnail with play button overlay (opens video player)
2. **Quick info bar:** Cook time | Prep time | Servings (tap to scale) | Calorie badge
3. **Macro pills:** Protein / Carbs / Fat colored dots with gram values (Pro subscribers see full breakdown)
4. **Collections & Tags:** Horizontal chip row, tappable
5. **Ingredients tab:** Checkboxes next to each ingredient (for cook mode tracking) + scaling control at top + "Add all to Grocery List" button
6. **Steps tab:** Numbered steps, each tappable to mark complete, timer integration on steps with time mentions
7. **Cook Mode button (FAB):** Sticky FAB at bottom — enters Cook Mode (steps take over full screen, phone stays awake)
8. **"I Cooked This!" button:** Persistent at bottom — opens camera for CookStreak log
9. **AI Substitutions chip:** "🔄 Show substitutions for [your diet filter]" — inline expansion

---

### Screen 4: Meal Planner

**Layout:** Week view calendar at top, recipe cards in body

1. **Week navigation:** Horizontal week pills (Mon–Sun), today highlighted, previous/next chevrons
2. **Auto-Generate banner (first time or empty week):** Large CTA: "✨ Generate My Week" with sub-copy "BiteSaver picks from your saves — 2 seconds" — single tap, full week fills
3. **Day rows:** For each day, up to 3 meal slots (Breakfast/Lunch/Dinner). Each slot shows: recipe thumbnail (40×40 stack), title, cook time, calorie count
4. **Nutrition score card:** Sticky below week header — letter grade (A–D) with colored ring + tooltip breakdown
5. **Drag-to-swap:** Long press a meal card → drag to another day slot to swap; haptic feedback on valid drop zone
6. **Replace tap:** Tap any meal → bottom sheet "Replace Meal" shows library search + AI suggestion chips (e.g., "Show high-protein options")
7. **Grocery list button:** Sticky at bottom: "🛒 Generate Grocery List for This Week" — single tap, navigates to Grocery List tab

---

### Screen 5: Grocery List

**Layout:** Aisle-section headers with items, FAB for manual add

1. **Aisle sections:** Expandable/collapsible sections: Produce, Proteins, Dairy, Bakery, Frozen, Pantry, Beverages, Other
2. **Item rows:** Checkbox + ingredient name + amount/unit + recipe attribution tag (small chip: "for Chicken Stir Fry")
3. **Checked items:** Strike-through + grey out; collapse to "X checked items (show)" fold at bottom of each section
4. **Manual add:** FAB (+) opens modal with typeahead ingredient name search
5. **Share button (top right):** Share sheet with options: "Text Message," "Copy List," "WhatsApp"
6. **Store mode header:** Optional "Store Mode" toggle — removes nav and recipe attribution for clean shopping experience, font bumped to 18px for aisle readability
7. **Consolidation markers:** When same ingredient appears from 2+ recipes, merged row shows combined amount with recipe count badge

---

### Screen 6: CookStreak Hub

**Layout:** Hero streak stat card + challenge cards + activity feed

1. **Streak hero card:** Animated flame + big number + "Your longest: X days" + 7-day dot tracker, 2 freeze token ice icons (tap to use)
2. **Active Challenges section:** Horizontal scroll of challenge cards showing: challenge name, your rank (#2 of 8), days remaining, progress bar (e.g., "3/5 recipes cooked")
3. **Join / Create buttons:** "Browse Challenges" and "+ Create Challenge" side by side
4. **Leaderboard sheet (per challenge tap):** Full-screen modal, ranked list with avatars, streak flames, cook counts. Gold/Silver/Bronze treatment for top 3. User's own row highlighted and pinned at bottom if not in top view.
5. **Activity feed:** Card feed of friends' cook logs — photo, recipe name, streak day count, challenge name, reaction bar (🔥❤️👏), comment count

**Challenge creation flow:**
- Name field + description
- Duration picker (7 / 14 / 30 / custom days)
- Requirement toggle: "Cook X recipes total" vs "Maintain a daily streak"
- Optional dietary theme pill selector
- Max participants slider (5–100)
- Visibility: Public / Friends only / Invite link only
- Preview → Create → Share sheet with invite link

---

### Screen 7: Profile

**Layout:** Header with avatar/cover, stats grid, contribution heatmap, recent cooks

1. **Header:** Avatar (circular), display name, follower/following counts (tappable)
2. **Stats row:** Total recipes saved | Total cooked | Current streak | Longest streak
3. **Contribution heatmap:** GitHub-style 52-week grid of cook activity (green = cooked, shade intensity = meals cooked that day)
4. **Achievement badges:** Unlocked trophies (7-day streak, 30-day streak, 5 challenges completed, 100 recipes saved, etc.) in horizontal scroll
5. **Recent Cook Log grid:** 3-column photo grid of cooking photos — Instagram profile feel
6. **Active Challenges section:** Challenge progress cards
7. **Settings access:** Top-right gear icon → Settings (account, notifications, dietary profile, subscription management)

---

## 9. Behavioral Design System

### 9.1 Streak Psychology

BiteSaver's streak system is modeled on Duolingo's research but adapted for the less-daily nature of cooking (vs. language practice).

**Core Mechanics:**
- **Streak increment trigger:** Logging a cook with photo within the calendar day (midnight–midnight in user's timezone)
- **Streak display:** Animated fire emoji with count on profile, home screen hero card, and inside challenges
- **Grace period:** None — this is intentional. The urgency of "cook tonight or lose it" is a key driver.
- **Freeze tokens:** 2/week (Pro: 3). Named "Chef's Night Off" tokens — humanizes the feature. Applied proactively from settings OR retroactively within 24h of a missed day.
- **Streak milestones:** At 7, 30, 60, 100, 365 days — animated trophy reveal, shareable image generated, push notification congratulation

**Psychology:** The streak counter creates an "investment" (Nir Eyal's Hooked model) that becomes increasingly costly to lose. The visibility of the streak on the social profile amplifies commitment through identity signaling.

### 9.2 Challenge Design

**Challenge types:**
1. **Recipe Count:** Cook N recipes in X days (e.g., "Cook 5 new recipes in 7 days")
2. **Streak:** Maintain a daily cooking streak for X consecutive days
3. **Theme:** Cook N recipes matching a theme (vegetarian, 30-minute meals)
4. **Combined:** Score = recipes cooked × streak multiplier

**Leaderboard scoring:**
```
Score = (recipes_cooked × 10) + (current_streak_days × 5) + (bonus: used_freeze_0 × 20)
```
The freeze bonus encourages natural cooking rather than token use.

**Anti-cheat photo verification:**
1. **CV food confidence check:** Google Vision API SafeSearch + food label detection. Rejects images confidence < 0.85 food label.
2. **Metadata check:** EXIF timestamp must be within ±2 hours of submission. Alerts flag photos with stripped EXIF (common in screenshots).
3. **Duplicate hash check:** SHA-256 of image file — same photo cannot be submitted twice. Prevents reusing one photo across multiple challenge log entries.
4. **Human review queue:** Flagged submissions enter a 24-hour review queue. Until reviewed, submission counts as provisional (labeled with ⏳). False positives refunded within 24h.
5. **Community report:** Users can "flag" a suspicious contribution. 3+ flags triggers automatic hold and manual review.

**FOMO notification system:**
```
Trigger: Friend logs a cook that extends their streak ≥ 3 days
Condition: Recipient has NOT cooked today
Delay: 0–60 minutes randomized (prevents coordinated notification floods)
Message examples:
  "Alex just cooked Lemon Herb Salmon 🐟 — Day 7! You're 3 days behind."
  "Sarah and Mike both cooked tonight 🔥 Don't let them pull ahead!"
  "[Name]'s Week 1 Challenge score just jumped to 28. Yours: 20. 👀"

Opt-out: Per-challenge and per-friend FOMO notification preferences
Throttle: Max 2 FOMO notifications per user per day (avoids fatigue)
```

### 9.3 Variable Reward Structure

**Notification cadence design (Behavioral Design Framework):**
- **Immediate reward:** Cook log accepted → confetti animation + streak counter increments with satisfying haptic + score update sound
- **Social reward:** Friends react to cook log → notification delivered within 5 minutes
- **Surprise rewards:** "Recipe Streak Bonus" — on day 10 of a streak, unlock a hidden "Chef" badge. On day 30, unlock "Master Chef" profile frame
- **Loss aversion triggers (3× day):**
  - Morning (8 AM): "You haven't cooked yet today. Your 5-day streak is at risk 🔥"
  - Afternoon (5 PM): If no cook log yet + streak active + friends cooked: "2 friends already cooked today. Don't break your streak!"
  - Evening (8 PM): "Last chance to protect your [X]-day streak tonight 🍳"

### 9.4 Onboarding Behavioral Hook

**Day 0 (First install):**
1. "What's your cooking goal?" → options: "Save money on delivery" | "Eat healthier" | "Learn new recipes" | "Cook more with family"
2. Dietary flags setup
3. "Invite 1 friend to join a challenge and you both get 2 weeks Pro free" (viral loop)
4. First recipe import tutorial — guided URL paste with sample URL pre-filled
5. Auto-generate first 3-day mini plan immediately after saving 3+ recipes

**Day 3:** Push notification: "You saved [X] recipes! Generate your first meal plan?"
**Day 7:** If no cook log: "You haven't cooked yet. Challenge a friend — it makes it 3× more likely you'll follow through (science!)."

---

## 10. AI Pipeline

### 10.1 Recipe Extraction Pipeline

**Stage 1: URL Classification**
```javascript
// Deterministic; no LLM needed
function classifyUrl(url: string): Platform {
  if (url.includes('tiktok.com')) return 'tiktok';
  if (url.includes('instagram.com/reel') || url.includes('instagram.com/p/')) return 'instagram';
  if (url.includes('youtube.com') || url.includes('youtu.be')) return 'youtube';
  return 'web';
}
```

**Stage 2: Content Fetch (platform-specific)**

| Platform | Method | Fallback |
|----------|--------|----------|
| TikTok | yt-dlp (metadata: description, auto-captions) | OpenAI vision on thumbnail |
| Instagram | yt-dlp (caption, auto-captions) | Vision API on thumbnail |
| YouTube | YouTube Data API v3 (description + chapters) + yt-dlp | Vision on thumbnail |
| Web | Puppeteer render + schema.org/Recipe extraction | Mozilla Readability → Cheerio NLP |

**Stage 3: Structured Extraction (GPT-4o-mini)**
```
System prompt:
"You are a recipe extraction AI. Given the following text content from a food video or recipe webpage, extract a structured recipe. Return ONLY valid JSON matching this schema:
{
  title: string (recipe name, max 80 chars),
  servings: number (integer, default 4 if not stated),
  cookTimeMinutes: number | null,
  prepTimeMinutes: number | null,
  description: string | null (max 200 chars, from creator description),
  ingredients: [{amount: number|null, unit: string|null, name: string, note: string|null}],
  steps: [{instruction: string, durationSeconds: number|null}],
  cuisineType: string | null (Italian/Mexican/Asian/etc),
  dietaryFlags: string[] (from: gluten-free, dairy-free, vegan, vegetarian, low-carb, nut-free, keto, paleo)
}

If information is not available, use null. Do not invent information. Extract only what is stated."

Temperature: 0.1 (low creativity, high accuracy)
Max tokens: 2000
```

**Stage 4: Nutritional Enrichment**
```
For each ingredient:
1. Query USDA FoodData Central API: GET /v1/foods/search?query={name}&limit=1
2. Cache result in Redis for 30 days (ingredient name → usda_fdc_id + per100g macros)
3. Calculate per-serving macros: (amount_in_grams / 100) × per100g_value × (1 / servings)
4. Sum all ingredients → recipe totals
5. Handle unit conversion: 1 cup = 240ml, 1 tbsp = 15ml, 1 tsp = 5ml (via conversion table)

Edge cases:
- "a pinch of salt" → 0.5g, minimal caloric contribution
- "to taste" → 0g (ignored in calc)
- Compound ingredients ("2 cans crushed tomatoes") → match to "crushed tomatoes, canned" FDC entry
```

**Stage 5: Semantic Embedding**
```
After recipe saved:
1. Concatenate: title + cuisine + dietary flags + top 5 ingredients
2. OpenAI text-embedding-3-small (1536 dimensions, $0.00002/1K tokens)
3. Store in recipe_embeddings table (pgvector column)
4. Used for: semantic search, similarity matching in meal plan generation
```

### 10.2 Meal Plan Generation Algorithm

```
FUNCTION generate_meal_plan(user_id, week_start, meal_types, dietary_overrides):

  // Step 1: Load candidate pool
  candidates = SELECT recipes WHERE userId = user_id
               AND dietaryFlags CONTAINS ALL user.dietaryFlags (+ overrides)
               ORDER BY score_weight DESC

  // Step 2: Score each recipe
  FOR recipe IN candidates:
    age_days = (now - recipe.createdAt).days
    last_cooked_days = recipe.lastCookedAt ? (now - recipe.lastCookedAt).days : 999

    recipe.score = 0
    recipe.score += min(age_days, 90) × 0.3          // older saves get higher score
    recipe.score += min(last_cooked_days, 180) × 0.4  // not-recently-cooked bonus
    recipe.score += (recipe.cookCount === 0 ? 50 : 0) // graveyard bonus
    recipe.score += random() × 10                     // mild randomization for variety

  // Step 3: Generate slots
  FOR day IN [Mon, Tue, Wed, Thu, Fri, Sat, Sun]:
    FOR meal_type IN meal_types:
      
      // Variety constraint: no same protein within 3 days
      recent_proteins = proteins used in last 3 days
      eligible = candidates WHERE protein NOT IN recent_proteins
      
      // If eligible pool empty, relax constraint to 2 days
      IF eligible.length < 3: eligible = candidates WHERE protein NOT IN last_2_days_proteins
      
      selected = eligible.sort(by: score).slice(0, 5)  // top 5 candidates
      winner = weighted_random(selected)               // random pick weighted by score
      
      plan_slot = {day, meal_type, recipe_id: winner.id}
      mark winner as used in this plan

  // Step 4: Score nutritional balance
  daily_totals = aggregate calories/protein/carbs/fat per day
  week_avg = average across 7 days
  score = grade_nutritional_balance(week_avg, user.targets)
  // Grade A: all macros within 10% of targets; B: within 20%; C: within 30%; D: beyond 30%

  RETURN {plan_slots, nutritional_score, daily_breakdown}
```

**Edge case handling:**
- **Library < 7 recipes:** Return warning, suggest saving more recipes before planning. Allow generation with repeats if user confirms.
- **All library recipes match same protein:** Relax protein variety constraint, note this in UI.
- **Breakfast/lunch requested but no breakfast/lunch recipes tagged:** Create a separate "Quick Breakfast" collection prompt.

### 10.3 Smart Substitutions (GPT-4o-mini)

```
System prompt:
"You are a culinary ingredient substitution expert. Given a recipe ingredient and a dietary constraint, suggest 1-3 practical substitutions. For each substitution provide:
- substitute ingredient name
- amount adjustment ratio (e.g., 0.8 = use 80% of original amount)  
- brief explanation (max 15 words)
- impact on dish (e.g., 'slightly less rich', 'texture change')

Only suggest substitutions that genuinely work. Return JSON array."

Examples cached in Redis (common substitutions served without LLM call):
- dairy milk → oat milk (1:1, vegan)
- butter → coconut oil (0.8:1, dairy-free, slightly different flavor)
- chicken → tofu (1:1, vegan, press first)
- wheat flour → almond flour (1:1.2, gluten-free, denser texture)
- heavy cream → coconut cream (1:1, vegan)
```

### 10.4 Photo Verification Pipeline

```
POST /cook-logs submits base64 image

Step 1: SHA-256 dedup check (Redis set lookup) → 409 if already used

Step 2: Google Vision API annotateImage:
{
  features: [
    {type: "LABEL_DETECTION", maxResults: 10},
    {type: "SAFE_SEARCH_DETECTION"}
  ]
}

Step 3: Score evaluation
food_labels = ['Food', 'Dish', 'Meal', 'Cuisine', 'Recipe', 'Cooking', 'Ingredient']
food_score = max confidence of any food_label in response

IF food_score >= 0.85:
  accept, photoVerified = true
ELSE IF food_score >= 0.60:
  provisional acceptance, enter human review queue
ELSE:
  reject with PHOTO_REJECTED error

Step 4: EXIF timestamp check  
IF EXIF data present:
  IF abs(exif_time - submission_time) > 7200 seconds:
    flag for review, photoVerified = false (provisional)
IF no EXIF:
  flag as "screenshot likely" (lower trust, not rejected)

Step 5: Store image → Supabase Storage
Path: cook-logs/{user_id}/{cook_log_id}.jpg
CDN URL stored in cookLog.photoUrl
```

---

## 11. Monetization & Pricing Ladder

### 11.1 Tier Structure

| Feature | Free | Pro ($4.99/mo or $39.99/yr) | Family ($7.99/mo or $69.99/yr) |
|---------|------|----|------|
| Saved recipes | **25** | **Unlimited** | Unlimited per member |
| Social media import | ✅ | ✅ | ✅ |
| Basic nutritional info (cal only) | ✅ | ✅ | ✅ |
| Full macros (P/C/F) | ❌ | ✅ | ✅ |
| Collections | 3 max | Unlimited | Unlimited |
| Auto meal planning | **1 plan/month** | Unlimited | Unlimited |
| Nutritional balance scoring | ❌ | ✅ | ✅ |
| Smart substitutions | ❌ | ✅ | ✅ |
| Graveyard surfacing | Basic | Advanced (more rescue types) | Advanced |
| CookStreak challenges | Join only | Join + Create | Join + Create |
| Freeze tokens/week | 2 | 3 | 3 |
| Offline access | ❌ | ✅ | ✅ |
| Cook history (full) | 30 days | Unlimited | Unlimited |
| Family sharing | ❌ | ❌ | Up to 6 members |
| Shared grocery list (family) | ❌ | ❌ | ✅ |
| Shared meal planning (family) | ❌ | ❌ | ✅ |
| Export recipes (PDF) | ❌ | ✅ | ✅ |
| AI recipe remix (V2) | ❌ | ✅ | ✅ |

### 11.2 Conversion Architecture

**Free-to-Pro triggers (in order of effectiveness, based on Behavioral Design):**

1. **Recipe limit gate:** At recipe 20 → inline upsell banner on save. At recipe 25 → hard modal block with "Upgrade to save unlimited recipes" — cannot be dismissed without choice.
2. **Macro data lock:** Macros shown as "--- g" with lock icon + "Pro feature" chip. Taps reveal a 2-screen pitch.
3. **Meal plan exhaustion:** "You've used your free plan this month. Next plan in 23 days — or upgrade."
4. **Challenge create gate:** Attempting to create challenge → "Create unlimited challenges with Pro. Your friends are waiting."
5. **Offline mode:** Network unavailable → "Upgrade to Pro for offline access" vs generic error.
6. **Cook history truncation:** Tapping a cook log older than 30 days shows blurred photo with upgrade prompt.

**Trial:** 7-day full Pro trial, **no credit card required**, single tap from any paywall. After trial expiry: graceful downgrade with "Your data is safe. Upgrade again anytime."

**Annual conversion:** Monthly plan → Annual upsell after 45 days of active use. "Switch to annual — save $20/year (33% off)."

### 11.3 Family Plan Mechanics

- Owner subscribes, pays $7.99/mo or $69.99/yr
- Owner generates an invite link (max 5 additional members; 6 total)
- Each member's recipe library remains private; grocery list and meal plan can be shared optionally
- If owner cancels: 30-day grace period for members to subscribe individually at Pro rate (prorated discount)

### 11.4 Revenue Projections (Year 1)

```
Month 6 targets:
  MAU: 150,000
  Free users: 130,000 (87%)
  Pro subscribers: 15,000 (10%)
  Family subscribers: 5,000 (3.3%, ~20,000 members)

  Monthly recurring:
    Pro: 15,000 × $4.99 = $74,850
    Family: 5,000 × $7.99 = $39,950
    MRR: ~$115K
    
Month 12 targets:
  MAU: 400,000
  Pro: 35,000
  Family: 8,000
  MRR: $237K → ARR: ~$2.8M
```

### 11.5 Retention Hooks

- **Weekly recap push notification:** "You cooked 4 times last week. Your friends averaged 2.1. 📊"
- **Monthly cooking certificate:** Auto-generated shareable "I cooked 18 meals in May" graphic
- **Streak preservation anxiety:** The longer the streak, the higher the switching cost. 30-day streak = major retention anchor
- **Library lock-in:** At 50+ recipes, switching means losing a curated personal cookbook. Emphasize "Your recipes, your library" in messaging

---

## 12. KPIs & Success Metrics

### 12.1 North Star Metric

**"Weekly Meal Plans Generated"** — this metric captures the most value-creating core loop: save recipes → generate plan → cook → streak. When this metric is high, everything else follows (retention, conversion, engagement).

### 12.2 Acquisition Metrics

| Metric | Definition | Target M6 | Target M12 |
|--------|-----------|-----------|-----------|
| App Downloads | Total installs | 250K | 700K |
| Organic install rate | % from App Store search / referral | ≥ 60% | ≥ 65% |
| Day-1 activation rate | Saves ≥ 1 recipe on day of install | ≥ 45% | ≥ 55% |
| Invite-driven installs | Installs from CookStreak challenge invite links | ≥ 12% of total | ≥ 20% |
| CAC (blended) | Total marketing spend / new subscribers | < $8 | < $6 |

### 12.3 Engagement Metrics

| Metric | Definition | Target |
|--------|-----------|--------|
| DAU/MAU ratio | Daily actives / monthly actives | ≥ 0.28 (industry benchmark: 0.20 for utility apps) |
| Recipes saved per user per week | Mean across active users | ≥ 3.5 |
| Plan generation rate | % of eligible users (≥7 saves) who generate ≥1 plan | ≥ 35% |
| Weekly plan completion rate | Plans where ≥5/7 meals logged as cooked | ≥ 22% |
| Grocery list generation rate | % of plan users who generate grocery list | ≥ 70% |
| Capture success rate | Successful extractions / total URL submissions | ≥ 87% |

### 12.4 Social / Streak Metrics

| Metric | Target |
|--------|--------|
| CookStreak activation rate (% of users who log ≥1 cook) | ≥ 30% by Day 30 |
| Average streak length (actives) | ≥ 5.5 days |
| Challenge participation rate | ≥ 18% of MAU in ≥1 active challenge |
| Viral coefficient (K-factor from challenge invites) | ≥ 0.30 (each 10 users generate 3 new users via invites) |
| Friend connections per user (median) | ≥ 3 by Day 60 |

### 12.5 Retention Cohorts

| Cohort | Day 1 | Day 7 | Day 30 | Day 90 |
|--------|-------|-------|--------|--------|
| All users | 70% | 40% | 22% | 14% |
| Streak active users | 95% | 80% | 58% | 38% |
| Challenge-enrolled users | 92% | 75% | 52% | 34% |
| Pro subscribers | 98% | 92% | 78% | 62% |

*(Retention = returned to app and performed any action)*

### 12.6 Monetization Metrics

| Metric | Target M3 | Target M12 |
|--------|-----------|-----------|
| Free-to-paid conversion | ≥ 8% | ≥ 12% |
| Paywall click-through | ≥ 25% on recipe limit gate | ≥ 30% |
| Trial start rate | ≥ 40% of paywall CTAs | ≥ 45% |
| Trial-to-paid conversion | ≥ 55% | ≥ 65% |
| Monthly churn (Pro) | ≤ 8% | ≤ 5% |
| Annual plan uptake rate | ≥ 35% of Pro subscribers choose annual | ≥ 45% |
| LTV (Pro, 12-month) | ≥ $38 | ≥ $48 |
| LTV (Family, 12-month) | ≥ $75 | ≥ $95 |

### 12.7 AI Pipeline Quality Metrics

| Metric | Target |
|--------|--------|
| Extraction accuracy (ingredients complete) | ≥ 85% (auto-graded on test set) |
| Ingredient nutritional match rate | ≥ 92% (USDA lookup success) |
| Photo verification false positive rate | ≤ 2% (legitimate food rejected) |
| Photo verification false negative rate | ≤ 5% (non-food accepted) |
| Extraction latency P95 | ≤ 4 seconds |
| Plan generation latency | ≤ 2 seconds |

---

## 13. Development Phases

### Phase 0: Foundation (Weeks 1–2)
**Engineering setup**
- Monorepo setup: Turborepo (apps/mobile, apps/api, packages/shared)
- Supabase project provisioned; Prisma schema + migrations
- Railway deployment pipeline (dev + prod environments)
- GitHub Actions CI: lint + type-check + test on PR
- Expo development build configured (EAS Build)
- PostHog installed (product analytics)
- Sentry installed (error tracking, both mobile and API)
- Design system: Figma component library + React Native component library bootstrapped

**Deliverable:** Deployed skeleton with auth (sign up, login, magic link), empty home screen, CI green.

---

### Phase 1: MVP (Weeks 3–8)
**Goal:** Core recipe loop working — save, organize, cook, list.

```
Week 3-4: Recipe Capture
  - URL extraction pipeline (web + YouTube first; TikTok/Instagram week 4)
  - Manual entry form
  - Photo OCR
  - Share extension (iOS + Android)

Week 5: Recipe Detail + Organization
  - Full recipe detail screen (ingredients, steps, scaling)
  - Cook mode
  - Collections + tagging
  - Search + filter

Week 6: Grocery List
  - Add from recipe
  - Aisle sorting
  - Manual add/edit/check
  - Share list
  - Offline sync (WatermelonDB)

Week 7-8: Polish + Paywall
  - Free tier limits (25 recipes, 1 plan/month)
  - Stripe subscription setup
  - 7-day trial flow
  - App Store submission (TestFlight external beta)
  - Fix top crash/issue bucket from beta
```

**MVP exit criteria:**
- Capture success rate ≥ 80% on 100-URL manual test
- <5 P1 bugs in beta
- Day-1 activation rate ≥ 35% in beta cohort

---

### Phase 2: V1 Differentiators (Weeks 9–16)
**Goal:** Launch the two moat features: Auto Meal Plan + CookStreak.

```
Week 9-10: Meal Plan Foundation
  - Plan generation algorithm (deterministic, no ML)
  - 7-day plan UI (week view, drag-to-swap)
  - Nutritional balance scorer + grade display
  - Dietary filters integration
  - Graveyard rescue weighting

Week 11: Meal Plan Advanced
  - Smart substitutions (GPT-4o-mini integration)
  - Plan → Grocery list export (one tap)
  - Plan editing (replace, remove meals)

Week 12-13: CookStreak Core
  - Personal streak (log cook + photo, increment counter)
  - Photo verification pipeline (Google Vision)
  - Challenge create/join/leave
  - Basic leaderboard

Week 14-15: CookStreak Social
  - Activity feed (following system)
  - Reactions on cook logs
  - FOMO notification system
  - Social profile + contribution heatmap

Week 16: V1 Launch Prep
  - Performance audit (profile + optimize render cycles)
  - Push notification copy review + timing audit
  - A/B test: trial CTA placement (paywall variants tested via PostHog)
  - App Store + Google Play launch submission
  - Press kit + launch blog post
```

**V1 exit criteria:**
- Auto-plan generates in ≤ 2s for libraries up to 500 recipes
- CookStreak photo verification false positive ≤ 3% in staging test set
- Public launch production deploy with 99.5% uptime SLA

---

### Phase 3: V2 Growth (Weeks 17+, rolling)

**Sprint-based, prioritized by KPI impact:**

| Priority | Feature | Target KPI |
|----------|---------|-----------|
| 1 | Pantry tracker (reduces grocery friction) | Plan completion rate +5% |
| 2 | Instacart integration | Grocery list generation rate +15% |
| 3 | Clan challenges | K-factor +0.1 |
| 4 | Recipe remix (AI) | Pro conversion +1% |
| 5 | Smart TV companion | DAU/MAU +0.02 |
| 6 | Weekly email digest | D30 retention +3% |
| 7 | Seasonal suggestions | Recipe save rate +0.5/week |
| 8 | Voice capture | Capture attempts +20% |

---

## 14. Risk Register

### 14.1 Technical Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| **TikTok/Instagram scraping breaks** (platform API changes / bot detection) | High | High | yt-dlp maintained by open source community; monitor weekly; fallback to OpenAI vision on screenshot; legal API partnerships (TikTok for Developers program v2) as medium-term fix |
| **USDA API rate limits at scale** | Medium | Medium | Aggressively cache ingredient lookups in Redis (30-day TTL). Build local ingredient nutritional database seeded from USDA bulk download (2MB JSON) for fallback |
| **GPT-4o-mini extraction accuracy degrades** | Low | High | Maintain 500-recipe golden test set; automated regression testing weekly; fallback to Claude Haiku if OpenAI has outage (same prompt format) |
| **PostgreSQL pgvector performance at scale** | Medium | Low | Semantic search used only for similarity features (non-critical path); separate read replica for vector queries; migrate to Pinecone if query P95 > 300ms with >1M embeddings |
| **Photo verification false negatives (cheat via food image from Google)** | Medium | Medium | Add: metadata timestamp stricter check, device-sourced EXIF camera make required for challenge submissions, rate-limit re-submissions after rejection |
| **WatermelonDB offline sync conflicts** | Low | Medium | Per-item conflict resolution (last-write-wins at item granularity); full audit log stored server-side; allow user to "reset from server" |

### 14.2 Market Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| **ReciMe launches CookStreak equivalent** | Medium | High | 6-month head start window. Focus on quality of social experience (FOMO mechanics, challenge variety) vs. feature parity. Patent provisional filing on auto-plan algorithm (legal budget: $3K). |
| **Meta/TikTok launch native recipe save feature** | Medium | High | BiteSaver's moat is cross-platform (saves TikTok *and* YouTube *and* Instagram *and* web; they won't cooperate). Lean into multi-platform value + social layer they cannot build across competing apps. |
| **$4.99 price point resistance in emerging markets** | Low | Low | Phase 1 markets are US/CA/UK/AU. Localized pricing for DE/FR in Phase 2 via Stripe + purchasing power parity. |
| **Low CookStreak virality (K < 0.20)** | Medium | Medium | A/B test invite copy, challenge type, and reward mechanics in first 60 days. If K < 0.15 at Day 60, pivot CookStreak to "solo accountability" mode with recurring AI coach persona. |

### 14.3 Legal / Compliance Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| **Copyright claim from recipe content owners** | Medium | High | BiteSaver saves structure (ingredients + steps) not verbatim recipe text. Recipe content is factual/functional, not protected expression under US copyright law (see *Lapine v. Seinfeld*). Always preserve source URL attribution. ToS explicitly states user is responsible for personal library content. Legal review budget: $5K before launch. |
| **GDPR compliance (EU users)** | Low | High | Supabase EU region option for EU users (data residency). Privacy policy with explicit GDPR user rights. Consent management for push notifications. Cookie consent for web app. DPA signed with Supabase, OpenAI, Google. |
| **COPPA (users under 13)** | Low | Medium | Age gate in onboarding (birthdate required). If under 13: app blocked. COPPA notice in ToS. |
| **Apple App Store 30% in-app purchase fee** | Certain | Medium | iOS uses StoreKit 2 (required by Apple for in-app subscriptions). Android uses Google Play Billing (15% for first $1M). Web app allows direct Stripe checkout (0% platform fee, just Stripe 2.9% + 30¢). Convert power users to web billing via email campaigns. |
| **TikTok/Instagram Terms of Service violation** | Medium | Medium | yt-dlp usage for personal recipe saving is analogous to bookmarking. Monitor platform ToS changes. Shift to official APIs where available (YouTube Data API v3 already official). Instagram Basic Display API is deprecated — maintain yt-dlp pipeline with fallback. |

### 14.4 Financial Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|-----------|
| **AI costs outpace revenue** | Medium | High | GPT-4o-mini at $0.001/recipe extraction. At 1M recipes/month = $1,000. Well within margins. Monitor with cost per extraction KPI. Hard rate limit: 10 imports/day free, 50/day Pro. |
| **User acquisition cost exceeds LTV** | Medium | High | Focus on organic + word-of-mouth (CookStreak viral loops) before paid UA. Target CAC < $6 blended. Performance marketing only after Month 6 with proven LTV data. |

---

## Appendix A: Tech Stack Summary Table

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Mobile | React Native + Expo | Single codebase for iOS + Android; Expo ecosystem for camera, notifications, share extension; large talent pool |
| Backend | Fastify (Node.js) | 2-3x Express throughput; schema validation built-in; excellent TypeScript support |
| Database | PostgreSQL (Supabase) | ACID, relations, pgvector for semantic search, RLS for security, realtime channels |
| Cache | Redis (Upstash) | Serverless, no maintenance; BullMQ job queues; session + rate limit store |
| Auth | Supabase Auth | OAuth + magic link out of the box; integrates with RLS; social logins |
| Storage | Supabase Storage | S3-compatible; auto CDN; integrates with Supabase Auth policies |
| AI Extraction | GPT-4o-mini | Fast structured output; $0.001/recipe = sustainable unit economics |
| AI Vision | Google Vision API | Food detection + OCR; $1.50/1000 requests; reliable food label scores |
| Nutritional Data | USDA FoodData Central | Free; comprehensive; standard reference |
| Payments | Stripe | Best-in-class subscription management; in-app webhooks |
| Deployment | Railway.app | Low ops overhead; auto-deploys from GitHub; reasonable cost up to 500K MAU |
| Monitoring | Better Stack + Sentry | Full observability stack; Sentry for mobile crash reporting |
| Analytics | PostHog | Open source, privacy-friendly; feature flags + funnels + session replay |

---

## Appendix B: Definition of Done Checklist (per feature)

Before any feature ships to production:

- [ ] Unit tests cover core business logic (≥ 80% coverage on service layer)
- [ ] Integration test covers the API endpoint (happy path + top 3 error cases)
- [ ] Mobile component has snapshot test
- [ ] PostHog event fired on all key user actions within the feature
- [ ] Paywall gate implemented if feature is Pro-exclusive
- [ ] Error states implemented (empty state, loading state, failure state)
- [ ] Accessibility: all interactive elements have accessible labels (React Native accessibility props)
- [ ] Dark mode verified in Storybook
- [ ] Offline behavior documented and tested
- [ ] Performance check: component renders < 16ms on mid-range Android device (Pixel 4a class)
- [ ] Security: no PII logged, no sensitive data in AsyncStorage unencrypted
- [ ] Sentry error boundaries wrapping the feature component
- [ ] Tested on iOS 16 + iOS 17, Android 12 + Android 14

---

## Appendix C: Expanded UI/UX Design System — Cooking-Optimized, 2026 Mobile-First

> **Board Addition — 2026-06-24**
> This section supersedes the design system summary in §8 and provides complete wireframe specifications, design token definitions, and mockup generation prompts for the full screen inventory.

### C.1 Design Philosophy & Visual Language

**Core Aesthetic:** Warm, appetite-stimulating food photography combined with clean, editorial minimalism. The visual language signals *home-cooked abundance* — not sterile diet-app efficiency, not fast-food red-and-yellow urgency. Think: a beautiful Italian grandmother's kitchen, but on your phone.

**Mood board keywords:** Rustic warmth, sun-drenched produce, linen textures, terracotta pots, sage-dusted wooden boards, candlelit dinner scenes.

**Design Pillars:**
1. **Appetite-first:** Every color, typographic choice, and image treatment is tested against "does this make me want to cook?"
2. **Kitchen-safe:** Everything operable with one clean or wet hand. Minimum 44px touch targets everywhere; critical actions (Next Step, I Cooked This) use 64px+ thumb-zone buttons.
3. **Low-friction at every moment of use:** Capture = 1 gesture. Plan generation = 1 tap. Grocery check-off = 1 tap. No navigation mazes.
4. **Beautiful at rest:** Empty states, loading states, and error states all use warm illustration — never raw spinner + grey box.

---

### C.2 Design Token Reference

#### Color Palette

```
// Primary Brand Colors
--color-terracotta-500:    #C85A3A  // Primary CTAs, streak flame, active states
--color-terracotta-400:    #E07055  // Hover states, secondary CTAs
--color-terracotta-200:    #F2BCA8  // Tints, progress fills, tag chips
--color-terracotta-100:    #FAE8E2  // Light backgrounds, selected card tints

// Nature / Vegetable Greens
--color-sage-600:          #4A6741  // Header text, active nav icons
--color-sage-500:          #627B57  // Secondary text, collection labels
--color-sage-300:          #96AD8B  // Dividers, inactive tints
--color-sage-100:          #EAF0E8  // Green tint backgrounds, dietary tag chips

// Warm Neutrals (Linen / Beige)
--color-linen-50:          #FAF7F2  // Primary page background (light mode)
--color-linen-100:         #F2EDE4  // Card backgrounds (light mode)
--color-linen-200:         #E8DFD0  // Elevated card / modal backgrounds
--color-linen-300:         #D8CCBA  // Input borders, dividers

// Typography / Dark
--color-charcoal-900:      #1C1A17  // Primary body text (light mode)
--color-charcoal-700:      #3D3830  // Secondary body text
--color-charcoal-400:      #7A7368  // Muted / caption text
--color-charcoal-200:      #C4BFBA  // Placeholder text, disabled state

// Dark Mode Background Stack
--color-dark-900:          #141210  // Root background (dark mode)
--color-dark-800:          #1E1C19  // Card background (dark mode)
--color-dark-700:          #272420  // Elevated surface (dark mode)
--color-dark-600:          #32302C  // Input background, dividers (dark mode)

// Semantic
--color-success:           #3A7D44  // Streak confirmed, cook logged
--color-warning:           #D4880A  // Streak at risk, low library warning
--color-error:             #C0392B  // Photo rejected, extraction failed
--color-info:              #2B6CB0  // Plan nutrition info, tooltips

// Glassmorphism
--glass-bg-light:          rgba(255, 252, 248, 0.72)  // Card on photo background
--glass-bg-dark:           rgba(20, 18, 16, 0.68)     // Dark mode glass card
--glass-border-light:      rgba(255, 252, 248, 0.40)  // Glass card border
--glass-border-dark:       rgba(255, 255, 255, 0.10)
--glass-blur:              16px                       // backdrop-filter blur
```

#### Typography Scale

```
// Typefaces
--font-display:      'Fraunces', serif         // Hero headlines, recipe titles
--font-body:         'Inter', sans-serif       // Body text, UI labels
--font-mono:         'JetBrains Mono', mono    // Quantities, macros, timers

// Scale (Mobile)
--text-xs:     11px / 1.4  // Captions, aisle labels, metadata
--text-sm:     13px / 1.5  // Secondary body, ingredient notes, tags
--text-base:   15px / 1.6  // Primary body text, recipe step text
--text-lg:     17px / 1.5  // Card titles, list item primaries
--text-xl:     20px / 1.4  // Section headers, modal titles
--text-2xl:    24px / 1.3  // Screen titles in Fraunces
--text-3xl:    30px / 1.2  // Hero numbers (streak count, days)
--text-4xl:    38px / 1.1  // Splash stats, empty state callouts

// Cook Mode Override (visibility at arm's length)
--cook-step-text:    22px / 1.6 / Inter SemiBold
--cook-timer-text:   48px / 1.0 / JetBrains Mono Bold
--cook-ingredient:   18px / 1.6 / Inter Regular
```

#### Spacing & Layout

```
--space-1:   4px
--space-2:   8px
--space-3:   12px
--space-4:   16px    // Page horizontal margin
--space-5:   20px
--space-6:   24px    // Card internal padding
--space-8:   32px    // Section vertical gap
--space-10:  40px    // Large section padding
--space-12:  48px    // Hero padding

--radius-sm:    8px   // Tags, chips, badges
--radius-md:    12px  // Input fields, small cards
--radius-lg:    16px  // Standard recipe cards
--radius-xl:    20px  // Large feature cards
--radius-2xl:   24px  // Bottom sheets, modals
--radius-pill:  100px // Buttons, filter pills

// Safe areas
--safe-top:     env(safe-area-inset-top)     // iOS dynamic island
--safe-bottom:  env(safe-area-inset-bottom)  // iOS home indicator

// Touch targets
--touch-min:    44px   // Minimum (WCAG 2.5.5 compliance)
--touch-comfortable: 52px  // Standard interactive elements
--touch-primary:     64px  // Primary CTAs in cook mode
```

#### Motion & Animation

```
// Spring presets (react-native-reanimated withSpring)
--spring-snappy:   { damping: 18, stiffness: 280 }  // Tab switches, card appear
--spring-bouncy:   { damping: 14, stiffness: 200 }  // Streak counter, badge unlock
--spring-gentle:   { damping: 22, stiffness: 180 }  // Photo transitions, modals

// Duration presets (for non-spring animations)
--duration-instant:  80ms   // Checkbox check, button press
--duration-fast:    150ms   // Toast appear, chip select
--duration-normal:  250ms   // Screen transitions, card expand
--duration-slow:    400ms   // Bottom sheet open, plan generation reveal
--duration-story:   600ms   // Confetti, trophy unlock, streak reveal

// Haptics (expo-haptics)
Card tap:           ImpactFeedbackStyle.Light
Big CTA confirm:    ImpactFeedbackStyle.Medium
Streak milestone:   NotificationFeedbackType.Success
Swipe archive:      ImpactFeedbackStyle.Heavy
Error / reject:     NotificationFeedbackType.Error
```

---

### C.3 Wireframe Specifications — 7 Key Screens

---

#### Screen C.3.1 — Home / Dashboard

**Purpose:** Personalized daily entry point. Delivers one clear action (cook tonight) without overwhelming.

**Layout: Single scroll view, no tabs visible until scroll begins**

```
┌─────────────────────────────── 390px ───────────────────────────────┐
│ STATUS BAR (system)                                                  │
├─────────────────────────────────────────────────────────────────────┤
│ ╔═══════════════════════════════════════════════════════════════╗   │
│ ║  HEADER NAV (height: 56px)                                   ║   │
│ ║  [Avatar 32px]   BiteSaver        [🔔 notif]  [⚙ settings]  ║   │
│ ║  linen-100 bg / sage-600 logo text / charcoal-700 icons      ║   │
│ ╚═══════════════════════════════════════════════════════════════╝   │
│                                                                      │
│ ╔═══════════════════════════════════════════════════════════════╗   │
│ ║  STREAK HERO BAND  (height: 72px, terracotta-500 gradient)   ║   │
│ ║  [🔥 animated flame 32px]  "12-Day Streak!"  [Freeze ❄️ ❄️]  ║   │
│ ║  Sub: "Cook tonight to keep your fire going →"               ║   │
│ ║  Glassmorphism: semi-transparent on linen bg below           ║   │
│ ╚═══════════════════════════════════════════════════════════════╝   │
│                                                                      │
│  TONIGHT'S DINNER CARD  (height: 200px, full-bleed hero image)      │
│ ┌───────────────────────────────────────────────────────────────┐   │
│ │ [Full-bleed recipe photo as bg — warm lit food photography]  │   │
│ │ ┌── GLASS CARD (position: bottom 16px, mx: 16px) ──────────┐ │   │
│ │ │ Lemon Herb Salmon              🕐 25 min  🍽 4 servings   │ │   │
│ │ │ From your Meal Plan — Monday                              │ │   │
│ │ │         [START COOKING →]  64px height, terracotta pill   │ │   │
│ │ └───────────────────────────────────────────────────────────┘ │   │
│ └───────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  QUICK CAPTURE BAR  (height: 56px, shadow-elevated)                 │
│ ┌───────────────────────────────────────────────────────────────┐   │
│ │ 🔗  "Paste a recipe link..."              [SAVE]  terracotta │   │
│ │ linen-200 bg / charcoal-400 placeholder / radius-pill border  │   │
│ └───────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  SECTION HEADER: "Saved Too Long Ago" (sage-600, Fraunces 20px)     │
│  Sub: "Your graveyard — time to rescue these" (charcoal-400, 13px)  │
│                                                                      │
│  GRAVEYARD HORIZONTAL SCROLL  (height: 180px, gap: 12px)           │
│ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐         │
│ │ [Photo]    │ │ [Photo]    │ │ [Photo]    │ │ [Photo]    │         │
│ │ Pasta      │ │ Thai Curry │ │ Apple Tart │ │ Shakshuka  │         │
│ │ Carbonara  │ │            │ │            │ │            │         │
│ │ 📅 43 days │ │ 📅 61 days │ │ 📅 89 days │ │ 📅 112 days│         │
│ │ [+Add Plan]│ │ [+Add Plan]│ │ [+Add Plan]│ │ [+Add Plan]│         │
│ └────────────┘ └────────────┘ └────────────┘ └────────────┘         │
│  Cards: 140×180px, radius-lg, linen-100 bg, terracotta-200 date tag │
│                                                                      │
│  SECTION HEADER: "Friends Cooking Now" (sage-600, Fraunces 20px)    │
│                                                                      │
│  ACTIVITY CARDS  (full width, stacked, height: 80px each)           │
│ ┌───────────────────────────────────────────────────────────────┐   │
│ │ [Avatar 40px]  Sarah cooked Mushroom Risotto  🔥 Day 7       │   │
│ │                "7-Day Streak — Challenge: Meatless Month"     │   │
│ │ [Recipe thumb 52px]             [🔥 React] [❤️] [👏]         │   │
│ └───────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  SECTION HEADER: "Recently Saved" (sage-600, Fraunces 20px)         │
│                                                                      │
│  2-COLUMN GRID  (gap: 12px, card: 174px wide)                       │
│ ┌──────────────┐  ┌──────────────┐                                   │
│ │ [Photo 16:9] │  │ [Photo 16:9] │                                   │
│ │ Title        │  │ Title        │                                   │
│ │ 🕐 20min  kcal│  │ 🕐 35min  kcal│                                   │
│ └──────────────┘  └──────────────┘                                   │
│                                                                      │
│ ╔═══════════════════════════════════════════════════════════════╗   │
│ ║  BOTTOM TAB BAR  (height: 49px + safe-bottom)                ║   │
│ ║  🏠Home  🔍Vault  ✚Capture  📅Plan  🛒List   🔥Streak       ║   │
│ ║  Active: terracotta-500 icon + label. Inactive: charcoal-400 ║   │
│ ╚═══════════════════════════════════════════════════════════════╝   │
└─────────────────────────────────────────────────────────────────────┘
```

**Interaction Notes:**
- Streak band uses `react-native-reanimated` loop animation: flame scale 1.0→1.15→1.0 over 1.5s ease-in-out
- Tonight's Dinner card background parallax scrolls at 0.6× scroll speed
- Graveyard horizontal scroll has momentum physics; rubber-band at boundary
- Each activity card image loads with a terracotta-tinted shimmer skeleton
- Quick Capture Bar auto-reads clipboard on focus (shows "📋 Link detected!" if URL present)
- Dark mode: linen-50 → dark-900, linen-100 → dark-800, terracotta values unchanged

---

#### Screen C.3.2 — Recipe Vault

**Purpose:** Browse, search, and organize the full personal recipe library. Powerful but instantly scannable.

```
┌─────────────────────────────── 390px ───────────────────────────────┐
│ ╔═══════════════════════════════════════════════════════════════╗   │
│ ║  SEARCH HEADER  (height: 96px, linen-50 floating)            ║   │
│ ║  "Your Vault"  (Fraunces 24px, charcoal-900)                 ║   │
│ ║  🔍 [ Search recipes, ingredients...     ]  [Filter ≡]      ║   │
│ ║      linen-200 bg input, radius-pill, 48px height            ║   │
│ ╚═══════════════════════════════════════════════════════════════╝   │
│                                                                      │
│  FILTER PILL SCROLL (height: 44px, horizontal scroll, no fade)      │
│  [All ✓]  [Quick <30m]  [Vegetarian 🌿]  [Chicken]  [Graveyard ⚰️] │
│  Active pill: terracotta-500 bg, white text                         │
│  Inactive: linen-200 bg, charcoal-700 text, radius-pill             │
│                                                                      │
│  SORT BAR  (height: 36px)                                           │
│  "47 recipes"  (charcoal-400 13px)    Sort: [Recently Saved ▾]     │
│                                                                      │
│  VIEW TOGGLE  (top right): [▦ Grid] [≡ List]                        │
│                                                                      │
│  ─────────── GRID VIEW (default) ─────────────────────────────────  │
│                                                                      │
│  2-column staggered grid (gap: 10px, mx: 16px)                      │
│  Card height: variable (image + info), min 200px, max 280px         │
│                                                                      │
│ ┌──────────────┐  ┌──────────────┐                                   │
│ │ [Food Photo  │  │ [Food Photo  │                                   │
│ │  full-bleed  │  │  tall crop]  │                                   │
│ │  16:9 crop]  │  │              │                                   │
│ │              │  │ Spicy Miso   │                                   │
│ │ Chicken      │  │ Ramen        │                                   │
│ │ Tikka Masala │  │              │                                   │
│ │ 🕐 45m  🔥 GF │  │ 🕐 30m  🌿 V  │                                   │
│ │ [⋯ more]     │  │ [⋯ more]     │                                   │
│ └──────────────┘  └──────────────┘                                   │
│                                                                      │
│  Card anatomy (linen-100 bg, radius-lg, shadow-sm):                 │
│  - Full-bleed top photo (radius-lg top corners only)                │
│  - Platform badge (TikTok/YT/IG): 20px icon top-left on photo      │
│  - Graveyard badge: "⚰️ 43 days" terracotta-200 chip top-right      │
│  - Title: Inter SemiBold 15px, charcoal-900, 2-line max             │
│  - Tags row: cook time + dietary chips, compact 11px text           │
│  - Long-press: context menu (Add to Plan / Add to List / Move /     │
│    Delete) — blur overlay behind options sheet                      │
│                                                                      │
│  SWIPE ACTIONS (right→left swipe on card in list view):             │
│  [Add to Grocery 🛒]  [Archive ⊘]                                   │
│  Sage-600 and terracotta-500 revealed action backgrounds            │
│                                                                      │
│  EMPTY STATE (0 recipes):                                           │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  [Illustration: terracotta bowl with sage herbs, 180px]      │  │
│  │  "Your vault is empty"  (Fraunces 28px, charcoal-700)        │  │
│  │  "Paste a TikTok or Instagram link to save your first        │  │
│  │   recipe in seconds"  (Inter 15px, charcoal-400, centered)   │  │
│  │  [✚  Save My First Recipe]  terracotta pill button 56px      │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

**Interaction Notes:**
- Pull-to-refresh: custom illustration — wooden spoon stirs as you pull
- Switching Grid↔List animates cards with shared-element spring
- Filter pills filter in-place without full reload (client-side filter on cached data)
- "Graveyard" filter shows only recipes saved >30 days + never cooked; cards tinted with subtle sepia overlay
- Long-press card previews full recipe in peek modal (80% screen height bottom sheet)

---

#### Screen C.3.3 — Meal Planner

**Purpose:** Generate, view, and adjust the week's meal plan. Speed is the entire value proposition here.

```
┌─────────────────────────────── 390px ───────────────────────────────┐
│ ╔═══════════════════════════════════════════════════════════════╗   │
│ ║  HEADER: "Meal Plan"  (Fraunces 24px)                        ║   │
│ ║  [< Jun 22]    Week of Jun 23    [Jun 30 >]                  ║   │
│ ║  Subtitle: "3 of 7 meals planned" (charcoal-400 13px)        ║   │
│ ╚═══════════════════════════════════════════════════════════════╝   │
│                                                                      │
│  ╔═══════════════════════════════════════════════════════════╗      │
│  ║  NUTRITION SCORE CARD  (linen-200 bg, radius-xl, mx:16px)║      │
│  ║  ┌──────────────────────────────────────────────────────┐║      │
│  ║  │ [●Grade A ring  ]  Nutritional Balance        ⓘ    │║      │
│  ║  │   filled 80%      Protein  ████████░░  78%          │║      │
│  ║  │   terracotta-500  Carbs    █████████░  85%          │║      │
│  ║  │   animated draw   Fat      ███████░░░  71%          │║      │
│  ║  │                   Avg 1,820 kcal/day               │║      │
│  ║  └──────────────────────────────────────────────────────┘║      │
│  ╚═══════════════════════════════════════════════════════════╝      │
│                                                                      │
│  ╔═══════════════════════════════════════════════════════════╗      │
│  ║  GENERATE BANNER (shown when <5 meals planned)           ║      │
│  ║  ✨ "Fill My Week Automatically"                          ║      │
│  ║  "BiteSaver picks from your saves — nutritionally        ║      │
│  ║   balanced in 2 seconds"                                 ║      │
│  ║  [✨  Generate Full Week]  terracotta-500 pill, 56px     ║      │
│  ╚═══════════════════════════════════════════════════════════╝      │
│                                                                      │
│  DAY ROWS (one per day, stacked, mx: 16px)                          │
│                                                                      │
│ ┌────────────────────────────────────────────────────────────┐      │
│ │ MON 23        📅 Today                                     │      │
│ │ ┌──────────────────────────────────────────────────────┐  │      │
│ │ │ [Photo 52px] Lemon Herb Salmon    🕐 25m   420 kcal  │  │      │
│ │ │               Dinner              [swap ↻] [✗ remove]│  │      │
│ │ └──────────────────────────────────────────────────────┘  │      │
│ │ [+ Add Breakfast]  [+ Add Lunch]  (sage-300 dashed cards) │      │
│ └────────────────────────────────────────────────────────────┘      │
│                                                                      │
│ ┌────────────────────────────────────────────────────────────┐      │
│ │ TUE 24                                                     │      │
│ │ ┌──────────────────────────────────────────────────────┐  │      │
│ │ │ [Photo 52px] Chicken Stir-Fry     🕐 20m   380 kcal  │  │      │
│ │ │               Dinner              [swap ↻] [✗ remove]│  │      │
│ │ └──────────────────────────────────────────────────────┘  │      │
│ └────────────────────────────────────────────────────────────┘      │
│                                                                      │
│  [Additional days scroll below...]                                  │
│                                                                      │
│  DRAG-TO-SWAP:                                                      │
│  Long press meal row → floating card lifts (shadow-xl, scale 1.04) │
│  Target day slots highlight in sage-100 with dashed terracotta ring │
│  Drop → spring-physics settle + haptic ImpactFeedbackStyle.Medium   │
│                                                                      │
│  REPLACE MEAL BOTTOM SHEET (on [swap ↻] tap, 70% screen):          │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │ "Replace Monday Dinner"  (Fraunces 20px)                     │   │
│  │ [🔍 Search your recipes...]                                  │   │
│  │ ── AI Suggestions ─────────────────────────────────────────   │   │
│  │ [High-protein tonight?]  [Something quick?]  [Vegetarian?]   │   │
│  │ ── All Recipes ─────────────────────────────────────────────   │   │
│  │ [scrollable recipe list, sorted by score]                    │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  STICKY BOTTOM BAR:                                                 │
│ ╔═══════════════════════════════════════════════════════════════╗   │
│ ║  [🛒  Generate Grocery List for This Week]  sage-600 pill    ║   │
│ ╚═══════════════════════════════════════════════════════════════╝   │
└─────────────────────────────────────────────────────────────────────┘
```

**Interaction Notes:**
- "Generate Full Week" taps shows a 1.8s animated loading state: recipe card thumbnails fly in from the library sequentially, slots fill left-to-right, nutrition ring animates to final grade
- Day rows are collapsible (tap day header to collapse to single line for quick weekly overview)
- Swapping meals also re-runs nutrition score with animated grade transition
- Empty meal slots use sage-100 dashed-border cards with `+` icon and label — visually inviting, not clinical

---

#### Screen C.3.4 — Grocery List

**Purpose:** Clean, aisle-organized shopping list that works at arm's length in a grocery store.

```
┌─────────────────────────────── 390px ───────────────────────────────┐
│ ╔═══════════════════════════════════════════════════════════════╗   │
│ ║  HEADER: "Grocery List"  (Fraunces 24px)                     ║   │
│ ║  Sub: "For week of Jun 23 · 24 items"  (charcoal-400 13px)   ║   │
│ ║  Right: [📤 Share]  [⋯ More]                                 ║   │
│ ╚═══════════════════════════════════════════════════════════════╝   │
│                                                                      │
│  STORE MODE TOGGLE (linen-200 chip row):                            │
│  [🏪 Store Mode OFF]  ──  toggle → hides recipe attribution,        │
│                             bumps font to 18px, removes nav bar     │
│                                                                      │
│  PROGRESS BAR: "8 of 24 items checked"  ████░░░░░░░  33%           │
│  terracotta-500 fill, linen-300 track, 6px height, radius-pill      │
│                                                                      │
│  ──── AISLE SECTIONS (collapsible, default expanded) ──────────────  │
│                                                                      │
│  🥬  PRODUCE  (sage-600 header, Fraunces 17px)  [collapse ▾]        │
│ ┌────────────────────────────────────────────────────────────┐      │
│ │ ☑  Cherry tomatoes        2 cups     for: Pasta Salad ──  │      │
│ │       strikethrough + charcoal-200 color when checked      │      │
│ │ □  Baby spinach           3 oz       for: Salmon + Frittata│      │
│ │ □  Garlic                 4 cloves   from 3 recipes        │      │
│ │ □  Lemons                 3          for: Salmon, Dressing │      │
│ └────────────────────────────────────────────────────────────┘      │
│                                                                      │
│  🥩  PROTEINS  (sage-600)  [collapse ▾]                             │
│ ┌────────────────────────────────────────────────────────────┐      │
│ │ □  Salmon fillet          600g       for: Lemon Herb Salmon│      │
│ │ □  Chicken breast         800g       from 2 recipes        │      │
│ └────────────────────────────────────────────────────────────┘      │
│                                                                      │
│  🥛  DAIRY  (sage-600)  [collapse ▾]                                │
│  🍞  BAKERY  (sage-600)  [collapse ▾]                               │
│  🧊  FROZEN  (sage-600)  [collapse ▾]                               │
│  🫙  PANTRY  (sage-600)  [collapse ▾]                               │
│                                                                      │
│  Item row anatomy (height: 52px, comfortable touch):                │
│  [Checkbox 24px] [Name Inter 15px SemiBold] [Amount Inter 13px]    │
│  [Recipe attribution chip: sage-100 bg, 11px, truncated]           │
│                                                                      │
│  Multi-recipe item badge:                                           │
│  When same item from 3 recipes: shows "from 3 recipes" chip         │
│  Tap chip → expands inline to show which recipes + amounts          │
│                                                                      │
│  SWIPE LEFT on item:  [✗ Delete]  terracotta-500 reveal             │
│  SWIPE RIGHT on item: [+ Duplicate]  sage-600 reveal                │
│                                                                      │
│  CHECKED ITEMS FOOTER (per section, always collapsed):              │
│  "2 checked items  [Show ▾]"  (charcoal-400 13px italic)           │
│                                                                      │
│  MANUAL ADD FAB:  [+]  terracotta-500 circle, 56px, pos: BR        │
│  Tap → bottom sheet with ingredient typeahead + aisle auto-assign   │
│                                                                      │
│  SHARE BOTTOM SHEET (on [📤 Share]):                                │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  Share Grocery List                                           │  │
│  │  [iMessage 📱]  [WhatsApp 💬]  [Copy Text 📋]  [More... ⋯]  │  │
│  │                                                               │  │
│  │  Preview — plain text format:                                 │  │
│  │  PRODUCE: Cherry tomatoes (2 cups), Baby spinach (3oz)...    │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

**Interaction Notes:**
- Tapping checkbox triggers: checkmark draw animation (80ms) + light haptic + item fades/strikes through (150ms spring)
- Progress bar updates with each check: terracotta fill grows, subtle bounce
- Store Mode: nav bar slides down and hides, font bumps to 18px, attribution chips hidden, progress bar stays prominent
- "Clear all checked" action accessible from [⋯ More] menu with confirmation alert
- Aisle section headers are sticky within scroll so aisle label stays visible while scrolling through long sections (>6 items)

---

#### Screen C.3.5 — CookStreak Social Hub

**Purpose:** Social accountability, challenge competition, and cooking identity.

```
┌─────────────────────────────── 390px ───────────────────────────────┐
│ ╔═══════════════════════════════════════════════════════════════╗   │
│ ║  HEADER: "CookStreak"  (Fraunces 24px, terracotta-500)       ║   │
│ ║                              [+ Create Challenge]            ║   │
│ ╚═══════════════════════════════════════════════════════════════╝   │
│                                                                      │
│  PERSONAL STREAK HERO CARD  (full width, mx:16px, radius-xl)       │
│ ┌───────────────────────────────────────────────────────────────┐   │
│ │  [Warm kitchen photo bg — blurred, dark overlay]             │   │
│ │  ┌── GLASS CARD ────────────────────────────────────────┐   │   │
│ │  │                                                      │   │   │
│ │  │  🔥                    12                   🔥       │   │   │
│ │  │  [flame anim]   "Day Streak"         [flame anim]   │   │   │
│ │  │               Fraunces 48px bold                    │   │   │
│ │  │                                                      │   │   │
│ │  │  7-day tracker: ● ● ● ● ● ● ○                       │   │   │
│ │  │  Mon Tue Wed Thu Fri  Sa  Sun                        │   │   │
│ │  │  filled terracotta, empty linen-300                  │   │   │
│ │  │                                                      │   │   │
│ │  │  Longest: 24 days        ❄️❄️ 2 freezes left        │   │   │
│ │  │  [Cook Tonight to Keep It →]  terracotta pill 52px  │   │   │
│ │  └──────────────────────────────────────────────────────┘   │   │
│ └───────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ACTIVE CHALLENGES  (Fraunces 20px, sage-600)                      │
│                                                                      │
│  CHALLENGE CARDS  horizontal scroll (width: 280px each, height:160) │
│ ┌───────────────────────────────────────────────────┐               │
│ │  🌿 Meatless Month                     Day 12/30  │               │
│ │  You: #2 of 6 participants  🏆                    │               │
│ │  ████████░░░░░░  8 of 15 recipes cooked           │               │
│ │  [Sarah: 9] [You: 8] [Mike: 7] +3 more            │               │
│ │  [View Leaderboard →]  (sage-600 text link)       │               │
│ └───────────────────────────────────────────────────┘               │
│                                                                      │
│  [Browse More Challenges →]  (charcoal-400 full-width text link)    │
│                                                                      │
│  ─── ACTIVITY FEED  (Fraunces 20px, sage-600) ─────────────────    │
│                                                                      │
│  FEED ITEM CARD  (full width, mx:16px, radius-lg, linen-100 bg):    │
│ ┌───────────────────────────────────────────────────────────────┐   │
│ │ [Avatar 40px] Sarah Chen  · 23 mins ago                      │   │
│ │              🔥 Day 7 Streak  in Meatless Month              │   │
│ │                                                               │   │
│ │ [Cook photo 100% width, 200px height, radius-md]             │   │
│ │ [Photo — Mushroom Risotto, warm candlelit plating]           │   │
│ │                                                               │   │
│ │ "Mushroom & Truffle Risotto"  (Inter SemiBold 15px)          │   │
│ │  From: The Flavour Bible (Web import)                        │   │
│ │                                                               │   │
│ │ [🔥 14]  [❤️ 8]  [👏 3]    [Comment 💬]  [Share ↗]          │   │
│ └───────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  LEADERBOARD BOTTOM SHEET (from [View Leaderboard]):                │
│  Full-screen modal (radius-2xl top corners)                         │
│ ┌───────────────────────────────────────────────────────────────┐   │
│ │  🌿 Meatless Month Leaderboard            Day 12 of 30       │   │
│ │  ─────────────────────────────────────────────────────────── │   │
│ │  🥇  Sarah Chen          9 recipes  🔥 12 days  Score: 105   │   │
│ │  🥈  You (highlighted)   8 recipes  🔥 12 days  Score: 95    │   │
│ │  🥉  Mike Torres         7 recipes  🔥 9 days   Score: 79    │   │
│ │      James O'Brien       5 recipes  🔥 7 days   Score: 57    │   │
│ │      Priya Sharma        4 recipes  🔥 5 days   Score: 43    │   │
│ │      Tom Wilson          2 recipes  🔥 2 days   Score: 22    │   │
│ │  ─────────────────────────────────────────────────────────── │   │
│ │  Top 3 rows: subtle gold/silver/bronze left border accent    │   │
│ │  Your row: terracotta-100 highlight background, sticky       │   │
│ └───────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

**Interaction Notes:**
- Flame animations in streak hero are Lottie JSON animations; two instances synced to beat slightly off-phase for organic feel
- "Cook Tonight" CTA opens recipe detail screen with cook mode pre-primed
- Challenge progress bar uses terracotta fill with a leading glow dot (running lights effect)
- Leaderboard polls via WebSocket — scores update in real-time with a smooth height/value transition
- FOMO notification deeplinks directly to relevant challenge leaderboard

---

#### Screen C.3.6 — Cooking View (Full-Screen Cook Mode)

**Purpose:** Hands-free, kitchen-safe, full-screen step viewer. Must be readable at arm's length with messy hands.

```
┌─────────────────────────────── 390px ───────────────────────────────┐
│  STATUS BAR: minimal — clock + battery only (all other icons hidden) │
│                                                                      │
│ ╔═══════════════════════════════════════════════════════════════╗   │
│ ║  TOP BAR (height: 52px, dark-900/80% semi-transparent)       ║   │
│ ║  [✕ Exit Cook Mode]    "Lemon Herb Salmon"    Step 2 of 7   ║   │
│ ╚═══════════════════════════════════════════════════════════════╝   │
│                                                                      │
│  STEP PROGRESS BAR:                                                 │
│  ●──●──○──○──○──○──○  (filled terracotta dots + line)              │
│  Horizontal dot tracker full screen width (mx: 24px)                │
│                                                                      │
│  ─────────────────────────────────────────────────────────────────  │
│                                                                      │
│  STEP CONTENT (flex: 1, centered, mx: 24px):                        │
│                                                                      │
│  Step number badge:                                                 │
│  [  2  ]  (terracotta-500, 36px circle, Fraunces 18px)             │
│                                                                      │
│  Step instruction:  (Inter SemiBold, 22px, charcoal-100 on dark)   │
│  ┌───────────────────────────────────────────────────────────┐     │
│  │                                                           │     │
│  │  "Heat olive oil in a large pan over medium-high heat.   │     │
│  │   Add garlic and cook until fragrant, about 1 minute."  │     │
│  │                                                           │     │
│  └───────────────────────────────────────────────────────────┘     │
│                                                                      │
│  TIMER BLOCK (shown when step has time mention):                    │
│ ┌───────────────────────────────────────────────────────────┐      │
│ │                                                           │      │
│ │   01:00  (JetBrains Mono Bold, 52px, terracotta-400)     │      │
│ │   [▶ Start Timer]  sage-600 pill button, 52px height     │      │
│ │                                                           │      │
│ └───────────────────────────────────────────────────────────┘      │
│                                                                      │
│  INGREDIENT REFERENCE (expandable drawer from bottom, collapsed):   │
│  [🧾 Show ingredients for this step ▾]                             │
│  Tap → drawer reveals: garlic (2 cloves), olive oil (2 tbsp)       │
│  Items pre-checked if already on ingredient checklist               │
│                                                                      │
│  ─────────────────────────────────────────────────────────────────  │
│                                                                      │
│  NAVIGATION ZONE (height: 80px + safe-bottom):                      │
│ ╔═══════════════════════════════════════════════════════════════╗   │
│ ║  [← Prev Step]      [NEXT STEP →]                            ║   │
│ ║   40% width           64px height, terracotta-500            ║   │
│ ║   charcoal-400 bg     full-bleed right side button           ║   │
│ ║   Inter 15px          Inter Bold 17px, white letter-spaced   ║   │
│ ╚═══════════════════════════════════════════════════════════════╝   │
│                                                                      │
│  LAST STEP VARIATION:                                               │
│  [NEXT STEP →] becomes [🎉 I Cooked This!]  terracotta-500          │
│  Tap → confetti burst + camera opens for CookStreak photo           │
│                                                                      │
│  GESTURE NAVIGATION:                                                │
│  Swipe left = next step (with spring-physics page turn)             │
│  Swipe right = previous step                                        │
│  Swipe up = show all steps overview (mini step list bottom sheet)   │
│  Screen never sleeps during cook mode (keepAwake: true)             │
│                                                                      │
│  DARK MODE: forced dark regardless of system setting (default dark) │
│  Rationale: dark screens are less blinding in a dimly-lit kitchen  │
│  Background: dark-900, text: linen-50, accent: terracotta-400       │
└─────────────────────────────────────────────────────────────────────┘
```

**Interaction Notes:**
- Timer: runs in background; sends local notification when done if user navigates away
- Text size control: pinch-to-zoom on step text adjusts font size for that session (persists if user preference)
- Voice "Next" command: microphone always listening in cook mode for "next step" / "previous" / "start timer" / "repeat" — powered by on-device speech recognition (no network call for privacy + speed)
- All taps in navigation zone register with `ImpactFeedbackStyle.Light` haptic

---

#### Screen C.3.7 — Onboarding

**Purpose:** First-impression hook. Get user to their first saved recipe in under 60 seconds. Demonstrate the product's core magic before asking for anything.

```
┌─────────────────────────────── 390px ───────────────────────────────┐
│                                                                      │
│  ──── SLIDE 1: Hook ("What BiteSaver does") ────────────────────   │
│                                                                      │
│ ┌───────────────────────────────────────────────────────────────┐   │
│ │ [Full bleed 16:10 animation / photo collage]                 │   │
│ │ TikTok phone → paste URL → structured recipe card pops in   │   │
│ │ Recipe card → calendar week fills → grocery list appears     │   │
│ │ Two friends' cook photos side by side — streak flames        │   │
│ │ Animation: lottie, 4 seconds, auto-plays                     │   │
│ └───────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌── GLASS CONTENT CARD (bottom 40%, terracotta bg) ─────────┐     │
│  │  "Save. Plan. Cook."  (Fraunces 34px, white)              │     │
│  │  "The app that actually gets you cooking the               │     │
│  │   recipes you save."  (Inter 16px, white/80%)             │     │
│  │                                                            │     │
│  │  [Get Started — It's Free]  white pill, charcoal-900 text │     │
│  │  56px height, full width, radius-pill                     │     │
│  │                                                            │     │
│  │  Already have an account? [Sign in]  (white 14px link)    │     │
│  └────────────────────────────────────────────────────────────┘     │
│                                                                      │
│  ──── SLIDE 2: Goal ("What's your cooking goal?") ─────────────   │
│                                                                      │
│  "What brings you to BiteSaver?"  (Fraunces 26px, charcoal-900)    │
│  "We'll personalize your experience"  (Inter 14px, charcoal-400)   │
│                                                                      │
│  Goal selection GRID (2×2, each card: radius-xl, 160px height):     │
│ ┌──────────────────┐  ┌──────────────────┐                          │
│ │  [Bowl emoji     │  │  [Heart emoji    │                          │
│ │   illustration]  │  │   illustration]  │                          │
│ │  "Stop ordering  │  │  "Eat healthier" │                          │
│ │   delivery"      │  │                  │                          │
│ └──────────────────┘  └──────────────────┘                          │
│ ┌──────────────────┐  ┌──────────────────┐                          │
│ │  [Friends emoji  │  │  [Family emoji   │                          │
│ │   illustration]  │  │   illustration]  │                          │
│ │  "Cook with      │  │  "Plan family    │                          │
│ │   friends"       │  │   meals"         │                          │
│ └──────────────────┘  └──────────────────┘                          │
│                                                                      │
│  Selected card: terracotta-500 border (2px) + terracotta-100 bg     │
│  Multi-select allowed (up to 2)                                     │
│  [Continue →]  terracotta pill                                      │
│                                                                      │
│  ──── SLIDE 3: Dietary flags ────────────────────────────────────  │
│                                                                      │
│  "Any dietary needs?"  (Fraunces 26px)                             │
│  "Your plans and grocery lists will respect these"                 │
│                                                                      │
│  TAG CLOUD (centered, wrap, tap to select):                         │
│  [Vegetarian 🌿]  [Vegan 🌱]  [Gluten-Free 🌾]  [Dairy-Free 🥛]    │
│  [Low-Carb 🥩]  [Nut-Free 🥜]  [Keto ⚡]  [Halal ✡]  [None ✓]   │
│                                                                      │
│  ──── SLIDE 4: Try it — paste your first link ──────────────────   │
│                                                                      │
│  "Try it right now"  (Fraunces 26px)                               │
│  "Paste a TikTok, Instagram, or YouTube recipe link"               │
│  "We'll extract it in seconds"                                     │
│                                                                      │
│  DEMO INPUT (full width, 64px height, prominent):                  │
│  🔗 [ https://www.tiktok.com/@...           ] [SAVE]               │
│                                                                      │
│  Below input (subtle):                                              │
│  "Or try our sample: [Pasta Carbonara demo link]"                  │
│  (Sample pre-fills input + auto-runs extraction)                   │
│                                                                      │
│  EXTRACTION ANIMATION (on submit):                                  │
│  Input field fills with terracotta progress bar (left to right)    │
│  Text cycling: "Reading link..." → "Extracting ingredients..."     │
│  → "Looking up nutrition..." → "Done! ✓"                          │
│  Then: recipe card slides up from bottom with spring physics        │
│                                                                      │
│  ──── SLIDE 5: Invite (social hook before main app) ────────────  │
│                                                                      │
│  "Invite 1 friend = 2 weeks Pro free"  (Fraunces 26px)            │
│  "For both of you. Start cooking together."                        │
│                                                                      │
│  [📤 Invite a Friend]  terracotta pill                             │
│  [Skip for now →]  charcoal-400 text link                          │
│                                                                      │
│  Trust signals below button:                                        │
│  "🔒 No credit card needed · Cancel anytime"                      │
│                                                                      │
│  ──── SLIDE 6: Auth (last step before app) ──────────────────────  │
│                                                                      │
│  "Create your account"  (Fraunces 26px)                           │
│  "Save your recipes across all devices"                           │
│                                                                      │
│  [  Continue with Apple  ]  black pill, 100% width, 52px           │
│  [  Continue with Google ]  white pill, border, 100% width, 52px  │
│  ───────  or  ───────                                               │
│  [  Email address field  ]  linen-200 bg input, 48px               │
│  [  Continue with Email  ]  terracotta pill, 100% width, 52px      │
└─────────────────────────────────────────────────────────────────────┘
```

**Interaction Notes:**
- Slide 4 (paste link) can be skipped but if user completes it, they see their actual first recipe and the app hook is 10× stronger than abstract description
- "Sample" link is a real extraction of a popular TikTok recipe (pre-cached result served <200ms to avoid extraction wait on first impression)
- Slide 5 invite is optional; if user skips, onboarding still completes cleanly
- Page indicator: minimal dot row at top (not bottom, stays out of thumb zone)
- Progress auto-saves: if app is closed mid-onboarding and reopened within 48h, resumes from same slide

---

### C.4 Component Library Specification

#### Recipe Card (Standard)

```
RecipeCard Component
Props: recipe, variant (grid|list|horizontal), onPress, onLongPress, showSource

Grid variant (174px wide, variable height):
  - Image: full-bleed top, 16:9 ratio, radius-lg (top corners only)
  - Platform badge: 20×20px icon absolute top-left on image (8px padding)
  - Graveyard badge: conditional, top-right on image, terracotta-200 chip
  - Body padding: 10px
  - Title: Inter SemiBold 14px, charcoal-900, 2-line clamp with ellipsis
  - Meta row: cook time icon + text (charcoal-400 12px) + dietary chips
  - Dietary chips: sage-100 bg, sage-600 text, 10px font, 4px padding
  - Shadow: 0 2px 8px rgba(28,26,23,0.10)

List variant (full width, 80px height):
  - Thumbnail: 64×64px, radius-md, left-aligned
  - Content: flex-1, pl:12px
  - Title: Inter SemiBold 15px, 1-line clamp
  - Meta: cook time + last-cooked (charcoal-400 12px)
  - Arrow: charcoal-200 chevron right, 16px

Horizontal scroll variant (140px wide, 160px tall):
  Used in: Home graveyard scroll, plan replace sheet
  - Square 1:1 image top half
  - Title 2-line
  - CTA button full width bottom
```

#### Streak Flame Badge

```
StreakBadge Component
Props: count, size (sm|md|lg), animated

Sizes:
  sm: 28px flame + 14px count — for feed items
  md: 40px flame + 22px count — for challenge cards
  lg: 64px flame + 48px count — for profile/hero streak card

Animation (when animated=true):
  Lottie animation: flame flickers with scale 1.0→1.2→1.0, 1.5s loop
  Count increments: spring bounce up + brief orange glow on number
  Milestone hit (7/30/100): full screen confetti overlay + sound
```

#### Bottom Sheet

```
BiteSaverSheet Component (wraps @gorhom/bottom-sheet)
Props: title, children, snapPoints, onDismiss

Styling:
  Background: linen-50 (light) / dark-800 (dark)
  Border radius: 24px top corners only
  Handle: 4×32px rounded linen-300 pill, centered, mt:8px
  Title: Fraunces 20px, charcoal-900, px:20px, pt:16px, pb:12px
  Separator: 1px linen-300 below title
  Content scroll: BouncyScrollView with overscroll glow in linen-200

Dismiss: drag handle down OR tap scrim (semi-transparent dark-900/40%)
Animation: spring-gentle preset (250ms feel)
```

---

### C.5 Dark Mode Adaptation

**Philosophy:** Dark mode is the *default and recommended* mode for BiteSaver. 67% of evening cooking (the primary use case) happens in dim kitchens. Dark UI reduces eye strain and makes food photography pop more vividly.

**Design decisions by surface:**

| Surface | Light mode | Dark mode | Rationale |
|---------|-----------|-----------|----------|
| Page background | linen-50 `#FAF7F2` | dark-900 `#141210` | Near-black with warmth (not pure black) |
| Card background | linen-100 `#F2EDE4` | dark-800 `#1E1C19` | Distinguish from page bg |
| Elevated card / modal | linen-200 `#E8DFD0` | dark-700 `#272420` | 3-layer depth stack |
| Input fields | linen-200 | dark-600 `#32302C` | Slightly lighter than card |
| Primary text | charcoal-900 `#1C1A17` | linen-50 `#FAF7F2` | Full contrast |
| Secondary text | charcoal-700 `#3D3830` | linen-200 `#E8DFD0` | Reduced but readable |
| Muted text | charcoal-400 `#7A7368` | charcoal-200 `#C4BFBA` | Captions, meta |
| Terracotta (CTAs) | terracotta-500 | terracotta-400 | Slightly brighter for dark bg contrast |
| Sage (headers) | sage-600 | sage-300 `#96AD8B` | Brighter sage for dark bg |
| Borders / dividers | linen-300 | dark-600 | Subtle separation |
| Recipe photo bg | — | dark-700 behind image | Prevent harsh crop edges |
| Glassmorphism | glass-bg-light | glass-bg-dark | Different alpha for each mode |

**System toggle:** Respects `useColorScheme()` from React Native. Toggle available in Profile > Settings > Appearance (System / Light / Dark).

---

## Appendix D: FLUX Image Generation Prompts for Mockup Creation

> Use these with `fal-ai/flux/dev` (high quality) for marketing mockups or `fal-ai/flux/schnell` for rapid iteration.
> All prompts assume **1:2 aspect ratio (1024×2048)** for mobile screenshot format.
> CLI: `python ~/workspace/scripts/fal_image.py "<PROMPT>" --size portrait_3x4 --out ~/workspace/projects/bitesaver/mockups/`

---

### D.1 App Store Screenshots

**Screenshot 1 — Home Screen Mockup**
```
A photorealistic iPhone 15 Pro mockup in natural titanium showing a cooking app home screen. 
The app has a warm earthy aesthetic: terracotta orange and sage green color scheme on a soft 
linen cream background. The screen shows: a glowing orange flame streak counter "Day 12" at 
the top, a gorgeous full-bleed photo of plated lemon herb salmon with a glassmorphism card 
overlaid showing recipe title and a terracotta Call-to-Action button "Start Cooking", a 
horizontal recipe card scroll below labeled "Saved Too Long Ago" with beautiful food photography 
cards, and a clean bottom navigation bar. Warm studio lighting, food photography magazine 
aesthetic. 4K sharp, no watermarks, professional app store screenshot quality.
```

**Screenshot 2 — Meal Planner Mockup**
```
A photorealistic iPhone 15 Pro mockup showing a meal planning app screen with warm earthy 
design. The screen displays a weekly calendar (Mon-Sun) with recipe thumbnail cards in each 
day slot — showing beautiful food photos. At top: a nutritional balance score card with an 
"A" grade in an animated terracotta ring, and protein/carb/fat progress bars in sage green 
and terracotta. A prominent glowing button reads "Generate My Week" in terracotta orange. 
Font is elegant serif for headings (Fraunces-style) with clean sans-serif for body text. 
Earthy color palette: warm linen backgrounds, sage green section headers, terracotta CTAs. 
Professional app screenshot, 4K quality, warm natural lighting atmosphere.
```

**Screenshot 3 — CookStreak Social Mockup**
```
A photorealistic iPhone 15 Pro mockup showing a social cooking app screen. At top: a hero 
card with a blurred kitchen background photo and a glassmorphism overlay showing a large 
flaming streak counter "12" in Fraunces serif font with two flame animations. Below: challenge 
progress cards showing friends' names and cooking scores on a leaderboard with gold/silver/
bronze treatment. Below that: a social activity feed showing beautiful food photos posted by 
friends — warm candlelit plated dishes — with reaction buttons (fire emoji, heart, clapping 
hands). Color scheme: terracotta orange, sage green, dark charcoal accents, linen cream cards. 
Vibes: Strava meets Instagram meets gourmet cooking magazine. Sharp 4K, no watermarks.
```

**Screenshot 4 — Cook Mode Mockup**
```
A photorealistic iPhone 15 Pro mockup displaying a full-screen step-by-step cooking guide. 
Dark background (warm near-black #141210). A large step number badge in terracotta orange. 
Large 22px text instruction for the current cooking step in warm white on dark. A prominent 
timer block showing "01:00" in monospace font — terracotta colored. At bottom: two navigation 
buttons — "← Prev Step" in a dark button left, and a wide terracotta "NEXT STEP →" button 
right. Clean minimal UI designed for kitchen use — high contrast, large type, thumb-friendly. 
Top bar shows step progress dots. Warm dark background, orange accent, readable at arm's 
length. Professional mockup, 4K quality.
```

**Screenshot 5 — Grocery List Mockup**
```
A photorealistic iPhone 15 Pro mockup showing an aisle-organized grocery list app screen. 
Warm linen cream background. Section headers in sage green with vegetable-category emoji 
(🥬 Produce, 🥩 Proteins, 🥛 Dairy). Each section contains checklist items with checkboxes — 
some items have a strikethrough indicating they're checked (crossed items are in light grey). 
Small terracotta recipe attribution chips next to each ingredient ("for: Salmon Recipe"). 
A progress bar at top showing "8 of 24 items" in terracotta. Bottom right: a terracotta plus 
button FAB. The typography is large (18px) for easy in-store reading. Clean, minimal, warm. 
Professional app store screenshot, 4K, natural warm lighting.
```

---

### D.2 Feature Illustration Prompts

**Hero illustration — "The Graveyard" feature**
```
A warm, slightly whimsical editorial illustration in earthy terracotta, sage green, and cream 
tones. Shows a smartphone screen as a small cemetery with cute little recipe tombstones — each 
tombstone has a food emoji on it (pasta, pizza, salad, salmon). A friendly illustrated chef's 
hand reaches in from the side holding a spatula, "rescuing" one of the tombstones from the 
graveyard. Style: modern digital illustration, editorial cookbook art direction, slightly 
playful but sophisticated. Flat perspective with subtle depth. Warm background.
```

**Hero illustration — CookStreak onboarding**
```
A warm editorial illustration showing three diverse people cooking in their own kitchen 
with small flame streak badges floating above them (Day 7, Day 12, Day 5). They are 
connected by glowing thread lines showing their social challenge connection. Each kitchen 
has a warm, inviting vibe — steam rising from pots, beautiful fresh ingredients. Style: 
modern editorial digital illustration, diverse characters, warm terracotta and sage color 
palette, Instagram-worthy food styling vibes. Clean white background.
```

**Empty state illustration — Empty recipe vault**
```
A charming editorial illustration of a beautiful empty wooden salad bowl with a few sage 
leaves and a terracotta sprig of rosemary resting in it. Below the bowl: a small URL link 
icon trailing off to the side, hinting at how to fill the bowl. Warm cream background. 
Style: modern cookbook editorial illustration, minimal, warm. Earthy terracotta and sage 
green colors. Inviting, not discouraging. 1:1 ratio, 512px.
```

**Achievement badge series — CookStreak milestones**
```
A series of four achievement badge designs for a cooking app, rendered in a flat jewelry/medal 
style. Badge 1 (7-day streak): terracotta flame medal with "7" in Fraunces font. Badge 2 
(30-day streak): deep sage laurel wreath award with "30" in gold. Badge 3 (100-day streak): 
ornate dark charcoal and terracotta Grand Chef trophy. Badge 4 (First challenge win): 
glowing golden spatula trophy on a terracotta podium. Rich, appetizing colors, jewel-like 
finish, medal/trophy aesthetic. Flat with subtle metallic sheen. Transparent background, 
512×512px each.
```

---

### D.3 Marketing Asset Prompts

**App icon**
```
A clean, modern iOS/Android app icon for a recipe saving app called BiteSaver. The design 
shows a stylized bookmark shape in terracotta orange, overlaid with a small fork-and-spoon 
icon in warm cream/white. The background is deep linen cream (not white, not dark — warm 
earthy mid-tone). The bookmark has a tiny heart notch cut into the bottom. Minimal, warm, 
recognizable at 29px. No text. Flat design with subtle inner glow. Rounded square format.
```

**Social media banner — 1200×630**
```
A vibrant social media ad banner for a recipe app. Left half: a gorgeous candlelit photo 
of plated pasta carbonara. Right half: warm terracotta background with bold Fraunces serif 
headline text "Stop losing recipes. Start cooking them." in white, sub-text "Save any recipe 
from TikTok, Instagram, or YouTube — in seconds" in ivory, and a prominent terracotta-to-coral 
gradient pill button "Try BiteSaver Free". Small TikTok, Instagram, YouTube logos shown at 
bottom. Professional food photography quality, warm editorial magazine layout. 1200×630px.
```

**TikTok video thumbnail (9:16)**
```
A compelling TikTok/Instagram Reel thumbnail for a recipe app video. Shows a split screen: 
top half — a person scrolling TikTok on their phone seeing a food video; bottom half — the 
exact same recipe magically appearing as a structured card in the BiteSaver app with 
ingredients neatly listed. Large white text overlay at top: "Wait... you can do THIS?" 
and at bottom: "Save any recipe in 3 seconds 🔥". Warm earthy color grading, authentic 
UGC-style video thumbnail feel, viral hook visual. 1080×1920px.
```

---

*Appendix C and D added per Board directive — 2026-06-24*
*Document version 1.1.0 — BiteSaver Product & Engineering Team — 2026-06-24*
*Next review: Sprint 2 retrospective (Week 4)*

