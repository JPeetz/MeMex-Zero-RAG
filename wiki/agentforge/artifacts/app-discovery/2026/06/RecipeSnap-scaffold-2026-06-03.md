# RecipeSnap — Complete App Scaffold

**Generated:** June 3, 2026 | **Verdict:** BUILD | **App Discovery Winner**
**Clone Target Analysis:** ReciMe ($2M funded, $2M ARR, $59.99/yr) with key improvements

---

## SECTION 0: APP IDENTITY & POSITIONING

### 0.1 App Name & Subtitle (ASO-Optimized)
- **App Store Name:** RecipeSnap — Save & Cook (30 chars)
- **Subtitle:** Social Recipe Saver & Planner (30 chars)
- **Rationale:** "RecipeSnap" contains "recipe" (primary keyword, 70+ search volume score), suggests instant capture. Subtitle hits "social recipe saver" (rising search trend — 68% discover recipes on social media) and "planner" (meal planning is the #2 use case after saving).

### 0.2 One-Liner Value Proposition
**"Save any recipe you see on social media, and cook it tonight."**

Passes the toilet test: immediately clear who it's for (anyone who scrolls past food videos), what it does (save → cook), and the emotional payoff (tonight — immediacy).

### 0.3 Visual Identity System

**Color Palette:**
- **Primary:** #FF6B35 (Warm Orange) — Appetite-stimulating, urgency, energy. Orange is the most food-associated color in app design psychology.
- **Secondary:** #2EC4B6 (Teal Mint) — Freshness, health, contrast to orange. Used for CTAs and success states.
- **Accent:** #FFD166 (Golden Yellow) — Warmth, premium feel. Used for streaks, achievements, special features.
- **Background:** #0F0F0F (Near-Black) — Dark mode default. Makes food photos pop. Reduces eye strain during cooking.
- **Surface:** #1A1A2E (Deep Navy) — Cards, sheets, modals. Cool contrast to warm food imagery.
- **Error:** #E63946 (Crimson) — High contrast against dark backgrounds.

**Typography:**
- **iOS:** SF Pro Display (headings 28pt bold), SF Pro Text (body 16pt regular, caption 13pt)
- **Android:** Google Sans (headings 28sp medium), Roboto (body 16sp regular, caption 13sp)
- **Monospace for measurements:** SF Mono / JetBrains Mono (ingredient quantities, cooking times)

**Iconography:**
- Style: Custom line-art at 2px stroke, rounded caps, consistent 24×24pt grid
- Icons needed: save-recipe, cook-mode, meal-plan, grocery-list, profile, search, settings, premium-crown, streak-fire, share-arrow, dietary-leaf, timer-clock

**App Icon:**
A deep navy rounded square with a warm orange spatula silhouetted against a golden-yellow "snap" camera shutter burst. The spatula doubles as the center element of the shutter. Recognizable at 40×40px — the orange/gold pop on navy reads as "food app" instantly on any home screen.

### 0.4 Screenshot Strategy

| # | Content | Text Overlay |
|---|---|---|
| 1 | Hero: Phone showing TikTok recipe being snapped | "Your TikTok recipes, cooked tonight." |
| 2 | Core: Recipe extraction result — ingredients auto-populated | "Snap. Extract. Cook. That's it." |
| 3 | Differentiator: Guided cook mode with step timer | "Never burn garlic again." |
| 4 | Before/After: Messy screenshot gallery → organized recipe collection | "From chaos to cookbook." |
| 5 | Premium: Dietary adaptation + cost estimate overlay | "Make any recipe YOURS." |

**Device frames:** iPhone 16 Pro Max (6.9") + Pixel 9 Pro (6.3"), dark mode, no notch hiding.

---

## SECTION 1: iOS ARCHITECTURE (SwiftUI-First)

### 1.1 Technology Stack
- **Language:** Swift 6 with SwiftUI primary, UIKit for camera capture and video player
- **Minimum target:** iOS 17 (94% active device coverage, 2026)
- **Architecture:** MVVM with @Observable (Observation framework). No React Native.
- **Persistence:** SwiftData for local recipes, CloudKit for free cross-device sync
- **Networking:** URLSession async/await. Vision framework for on-device text recognition.
- **AI/ML:** Vision (OCR for screenshot recipe extraction), Core ML for Phi-4-mini (on-device recipe adaptation)
- **Analytics:** TelemetryDeck (privacy-first, no IDFA, GDPR-compliant)
- **Crash reporting:** Xcode Organizer + MetricKit (zero third-party SDK bloat)

### 1.2 Subscription Paywall (RevenueCat Integration)

**Tiers:**
- **Free:** Save 20 recipes, basic meal plan (3 days), standard grocery list, web recipe import
- **Premium ($4.99/mo):** Unlimited recipe saves, social media video extraction, AI dietary adaptation, guided cook mode, ingredient cost estimates, cooking streaks, family sharing
- **Annual ($39.99/yr):** All Premium, 33% discount vs monthly (effective $3.33/mo)
- **7-day free trial:** No card required (RevenueCat no-card trial → 15-30% conversion uplift)

**Paywall trigger:** After user saves their 3rd recipe and views it in cook mode — they've experienced the full value loop.

### 1.3 Screen-by-Screen Specification

**Screen 1: Onboarding (3 cards)**
- Card 1: "You save recipes on TikTok. Then forget them. We fix that." — Emotional hook, warm food illustration
- Card 2: "Join 50,000+ home cooks who never lose a recipe again." — Social proof
- Card 3: "Grant camera access to start snapping." — Single CTA, 30 seconds from download to first save
- State: @AppStorage("onboardingComplete")
- Animation: Cards slide horizontally with spring (damping 0.7). Background gradient shifts warm → cool.

**Screen 2: Home — My Recipes**
- Purpose: The 90% screen. Grid of recipe cards with hero image, title, cook time badge, dietary tags
- Gestures: Pull-to-refresh, long-press for quick actions (cook now, share, delete)
- Empty state: "Your recipe collection is waiting. Tap + to save your first recipe." — Illustrated empty plate with fork and knife
- Search bar: Filter by name, ingredient, cuisine, dietary tag
- Segmented control: All / Recent / Favorites / Meal Plan
- State: @Query<Recipe> with sort descriptors, @Environment for navigation

**Screen 3: Recipe Capture (Core Action)**
- Purpose: Import recipe from social media, photo, web link, or manual entry
- Import options: Snap from Camera / Import from Photos / Paste Link / Type Manually
- After capture: Vision-based OCR extracts title, ingredients, instructions. Progress bar with "Extracting recipe…"
- Review screen: Editable fields — confirm/correct AI extraction before saving
- Dietary auto-tagging: Detects "contains dairy", "vegetarian", "gluten" from ingredients
- Cook time estimate: AI-parsed from instructions ("simmer 20 min" → tagged)
- State: @State for capture session, Combine pipeline for Vision → text processing

**Screen 4: Recipe Detail / Cook Mode**
- Purpose: The payoff. Beautiful recipe view with step-by-step guided cooking
- Guided Cook Mode: One step at a time, large text, built-in timer for each step. Swipe right for next step.
- Timer overlay: Tap any time mention ("20 minutes") → timer starts. Live Activity in Dynamic Island.
- Ingredient checklist: Tap to check off as you go. Visual progress bar.
- Scale servings: +/- stepper adjusts all quantities proportionally (1× → 2× → 4×)
- Dietary adaptation toggle (Premium): "Make this vegan / gluten-free / low-carb" — AI substitutes ingredients
- Share: "I made this!" card with photo + RecipeSnap watermark for Instagram Stories
- Haptics: Medium impact on step completion, heavy impact on recipe finished
- Animation: Step transitions use spring animation. Completed recipe triggers confetti burst (brand colors).

**Screen 5: Meal Planner**
- Purpose: Weekly calendar drag-and-drop. Recipes scheduled to days.
- Grocery list auto-generated from week's meal plan
- Empty state: "Plan your week. Drag recipes onto any day."
- Premium gate: Unlimited weeks (free = 3 days), grocery cost estimates

**Screen 6: Settings**
- Max 8 items: Dietary Preferences, Measurement Units, Notification Settings, App Icon, Theme, Export Data, Privacy Policy, About
- Smart defaults: Dark mode on, metric for non-US, imperial for US, notifications off until user completes first recipe

**Screen 7: Premium Upgrade**
- Comparison table: Free vs Premium side-by-side
- "Before/After" visualization: Free user's 20-recipe limit → Premium's unlimited library
- Annual plan pre-selected (green border, "BEST VALUE" badge)
- "Less than one latte per month" anchor copy
- Trial CTA: "Start 7-Day Free Trial — No Card Required"

### 1.4 iOS-Specific Optimizations
- **WidgetKit:** Small (today's meal), Medium (next 3 meals + grocery count), Large (weekly meal plan). Updates on recipe schedule change.
- **Siri Intents:** "Hey Siri, what's for dinner tonight?" → opens today's meal plan. "Hey Siri, add avocados to my grocery list."
- **Live Activities:** Active cook mode timer in Dynamic Island. Shows current step + remaining time.
- **App Store Review prompt:** After 3rd completed recipe (SKStoreReviewController). Behavior-based, not time-based.
- **Push notifications:** Rich with meal photo. "Tonight's dinner: Creamy Tuscan Chicken. Tap to start cooking." Actionable: "I already ate" → reschedules.
- **Privacy label:** "Data Not Collected" for everything except email (for account sync) and recipes (user-generated content).

---

## SECTION 2: ANDROID ARCHITECTURE (Jetpack Compose-First)

### 2.1 Technology Stack
- **Language:** Kotlin 2.0, Jetpack Compose + Material 3
- **Minimum SDK:** 26 (Android 8.0, 96% coverage)
- **Architecture:** MVVM with StateFlow + collectAsStateWithLifecycle()
- **Persistence:** Room (recipes, meal plans) + DataStore (preferences)
- **Sync:** Firebase Firestore for cross-platform sync (iOS CloudKit ↔ Android Firebase bridge via shared backend at scale)
- **DI:** Hilt (compile-time safe)
- **Navigation:** Compose Navigation with type-safe Kotlin serialization routes
- **AI:** MediaPipe LLM Inference with Gemma-3-1B for on-device recipe adaptation
- **Analytics:** Firebase Analytics (GDPR consent flagged before init)

### 2.2 Google Play Billing
- BillingClient 7.0+, same tiers as iOS
- Introductory price: 50% off first 3 months annual, 50% off first month monthly
- Grace period: 7 days, account hold: 30 days
- Paywall trigger identical: after 3rd recipe save

### 2.3 Android-Specific Optimizations
- **Material You:** Dynamic theming from wallpaper. Orange primary adapts to user's system colors.
- **Predictive back:** Every screen. Back preview animation on recipe detail → home.
- **App Shortcuts:** (1) Snap Recipe, (2) Tonight's Dinner, (3) Grocery List, (4) New Meal Plan
- **Notification channels:** Cooking Reminders (HIGH), Weekly Plan (DEFAULT), Tips & Inspiration (LOW). Grouped under "RecipeSnap".
- **Background work:** WorkManager for weekly meal plan notification, grocery list sync
- **Play Store feature graphic:** Phone showing guided cook mode + "Save. Adapt. Cook." overlay. 1024×500.

---

## SECTION 3: SEO & GEO OPTIMIZATION

### 3.1 App Store Optimization (iOS)

**Keyword Field (100 characters):**
```
recipe,saver,social,media,tiktok,instagram,cook,meal,planner,grocery,list,organizer,book,video,ai,adapt
```
- "recipe saver" (medium volume, low competition) 
- "social media" + "tiktok" + "instagram" (capture the behavioral hook — where users ARE)
- "cook" + "meal planner" (high volume adjacent)
- "ai adapt" (differentiator — no competitor targets this)
- No competitor brand names

**Title keywords double-weighted:** recipe, saver, cook (all in title "RecipeSnap — Save & Cook")

**Description (first 3 lines):**
"RecipeSnap is the easiest recipe saver for social media. Found an amazing dish on TikTok or Instagram? Snap it, save it, and cook it tonight. Join 50,000+ home cooks who never lose a recipe again. AI adapts every recipe to YOUR dietary needs. Premium includes guided cook mode, grocery lists, and ingredient cost estimates."

**Promotional Text (170 chars):**
"New: AI Dietary Adaptation! Make ANY recipe vegan, gluten-free, or low-carb with one tap. Your TikTok recipes, YOUR way. Try Premium free for 7 days."

**Ratings Strategy:**
- Prompt after 3rd completed recipe with positive cook mode session (>2 min)
- Pre-prompt: "You're a natural! ⭐ Would you help other home cooks find RecipeSnap?"
- Negative review response: "Thanks for the feedback! We're shipping improvements weekly. What specific feature would make this 5 stars for you? Email us at support@recipesnap.app — our team reads every message."

### 3.2 Google Play Store Optimization

**Title:** RecipeSnap — Save Recipes from TikTok & IG (50 chars)
**Short Description:** Save recipes from TikTok, Instagram & more. AI adapts them to YOU. Cook tonight. (80 chars)
**Full Description:** 4000 chars, "recipe saver" at 2-3% density. Progressive disclosure with emoji section headers. Social proof above the fold.
**Category:** Food & Drink (primary), Lifestyle (secondary)

### 3.3 Off-Store SEO (Web Presence)

**Landing Page (recipesnap.app):**
- H1: "Save Any Recipe from TikTok & Instagram — RecipeSnap"
- Meta: "RecipeSnap is the #1 recipe saver for social media. Snap any recipe from TikTok, Instagram, or YouTube. AI adapts it to your diet. Cook tonight. Free download." (155 chars)
- Open Graph image: App screenshot hero with "Your TikTok recipes, cooked tonight" overlay
- Schema.org: SoftwareApplication with rating, price, OS

**Content SEO — 5 Pillar Posts:**
1. "Paprika vs RecipeSnap: Which Recipe App Actually Saves TikTok Recipes?"
2. "How to Save Recipes from TikTok and Instagram (2026 Guide)"
3. "Best Recipe Apps 2026: Honest Review from a Home Cook"
4. "AI Dietary Adaptation: Make Any Recipe Vegan, Gluten-Free, or Keto"
5. "Meal Planning for Social Media Cooks: From Saved Posts to Dinner Table"

**GEO (Generative Engine Optimization):**
- FAQ section with 8 Q&A blocks targeting AI Overview snippets
- "How do I save a recipe from TikTok?" → Answer structured for featured snippet
- Author byline with "Home Cook & RecipeSnap Co-Founder" on every blog post (EEAT signal)

---

## SECTION 4: BEHAVIORAL ARCHITECTURE

### 4.1 Trigger Design

**External Triggers:**
- **Push #1 (Timely):** "Tonight's dinner idea: [Recipe Name] from your saves. Tap to start cooking." — sends at 4:30 PM local, before dinner decision time.
- **Push #2 (Social Proof):** "🔥 'Creamy Tuscan Chicken' is trending! 200+ people cooked it this week. Try it tonight."
- **Push #3 (Loss Aversion):** "Your 7-day cooking streak ends today! Cook any recipe to keep it alive 🔥"
- **Widget:** Updates daily at 6 AM with today's meal plan. Passive external trigger on home screen.
- **Email re-engagement Day 3:** Subject: "Your saved recipes are waiting." Preview: "You saved 3 amazing dishes. Don't let them go to waste — pick one for tonight."

**Internal Triggers (Negative Emotion → App Open):**
- User feels **"what's for dinner?" panic at 5 PM** → opens RecipeSnap to check meal plan
- User feels **"I saw a great recipe but can't find it" frustration** → remembers RecipeSnap is where recipes go
- User feels **"I want to cook something new but don't know what" boredom** → opens RecipeSnap explore/discover

### 4.2 Action Design
- **Core action:** Snap/import recipe → auto-extract → save → cook. Maximum 3 taps from home screen.
- **Fogg B = MAT:** Motivation (8/10 — hungry, want to cook), Ability (9/10 — snap, review, save), Trigger (7/10 — widget, push, social media encounter). Well above activation threshold.

### 4.3 Variable Reward Design

**Tribe (Social):**
- "Recipe of the Week" community pick — social validation
- Shareable "I made this!" cards designed for Instagram Stories with RecipeSnap watermark
- See what recipes friends are saving (opt-in social feature)

**Hunt (Search/Delight):**
- Weekly "Forgotten Gem" notification: "You saved this 2 months ago. Perfect for tonight."
- AI-powered "You might also love" based on saved recipe patterns
- Seasonal discovery: "Cozy fall soups" when temperature drops locally

**Self (Mastery):**
- Cooking Streaks: "7-Day Cooking Streak 🔥" — visible counter, loss-aversion protected
- Recipe completion rate: "You've cooked 85% of saved recipes — top 10% of users!"
- Skill badges: "Sauce Master" (made 5+ sauces), "Baking Pro" (completed 10+ baked recipes), "Global Chef" (cooked 5+ cuisines)

### 4.4 Investment Design
- **Data moat:** User's entire recipe collection, meal plans, dietary preferences, cooking history. Irreplaceable.
- **Social moat:** Shared meal plans with family, collaborative grocery lists. Network effect.
- **Financial moat:** Annual subscriber has sunk cost. Even a one-time $0.99 tip jar creates psychological ownership.
- **Skill moat:** Learning guided cook mode, dietary adaptation workflow. Switching costs.
- **Reputation moat:** Streak counters and badges. Users will cook just to protect a 30-day streak.

---

## SECTION 5: VISUAL DESIGN SYSTEM

### 5.1 Design Principles
1. **Food is the hero.** Chrome disappears during cooking. Full-bleed recipe photos. Minimal UI chrome.
2. **Dark by default.** Warm food photography against dark backgrounds. Kitchens are often dimly lit — the app must be readable.
3. **Motion guides, never distracts.** Every animation serves a purpose: step transitions, timer urgency, completion celebration.
4. **One-thumb operability.** Every action reachable with one hand while the other stirs a pot.

### 5.2 Key Animations & Micro-Interactions
- **Recipe save:** Camera shutter animation (0.3s) → extraction progress bar (0.5-2s) → recipe card scales and slides into collection (0.4s, spring damping 0.6)
- **Step completion:** Swipe triggers page curl (0.35s) → new step fades in (0.25s) → haptic medium impact
- **Timer:** Radial progress with color shift (teal → yellow → orange → red as time decreases). Pulse animation at 1 min remaining.
- **Recipe finished:** Confetti burst in brand colors (0.8s) + "You did it!" scale-bounce card + heavy haptic
- **Error:** Gentle shake + crimson accent flash (0.4s), auto-resolves after 1.5s
- **Empty → populated:** Staggered fade-in of recipe cards, 0.05s delay per card

### 5.3 Haptic Feedback Map
- Light: Card tap, checkbox toggle, tab switch
- Medium: Step complete, timer start, recipe saved
- Heavy: Recipe finished, streak milestone, major achievement
- Selection: Picker scrolling (ingredients, servings)
- Notification: Only for timer completion

### 5.4 Accessibility as Luxury
- VoiceOver labels on every element: "Recipe card: Creamy Tuscan Chicken, 35 minutes, dairy-free option"
- Dynamic Type: Tested at largest accessibility size. Recipe steps reflow to single-column.
- Reduce Motion: All decorative animations become instant. Functional animations simplified.
- Color blindness: Icons + text ALWAYS accompany color-coded dietary tags. Timer uses shape (circle → filled) not just color.
- Minimum contrast: 4.5:1 for all text, 7:1 for cook mode text (larger, critical)

---

## SECTION 6: FINANCIAL ARCHITECTURE

### 6.1 Pricing Tiers

| Tier | Monthly | Annual | What's Included | Why This Price |
|---|---|---|---|---|
| Free | $0 | $0 | 20 recipe saves, 3-day meal plan, basic grocery list, web import | Generous enough to be genuinely useful. 20 recipes is 2-3 weeks of meals. |
| Premium | $4.99 | $39.99 ($3.33/mo) | Unlimited saves, social video extraction, AI dietary adaptation, guided cook mode, cost estimates, cooking streaks, family sharing (up to 5) | "Less than one latte = unlimited recipes all month." Below ReciMe's $9.99, competitive with Preplo's $4.99. |
| Family | — | $59.99 | Premium × 5, shared meal plans, collaborative grocery list | Viral expansion. Every family member is acquisition. |

### 6.2 Unit Economics
- **CAC target:** $0 at launch (organic-only: ASO, content marketing, social media)
- **LTV at 6 months:** $19.98 (avg 4 months retention × $4.99/mo) for monthly; $39.99 for annual
- **Payback period:** 0 months (organic CAC = $0)
- **Churn target:** <8% monthly (below 10% industry average for consumer subs)
- **Referral value:** Each converted referral = $39.99 LTV. Cost = 1 free month for both ($9.98 total cost). 4:1 ROI.

### 6.3 Monetization Flow
1. Download → Free onboarding → Snap first recipe (zero friction)
2. Snap 3rd recipe → "You clearly love RecipeSnap!" paywall, annual pre-selected
3. Decline → "Try Premium free for 7 days. No card required."
4. Still decline → Free tier. Paywall resurfaces when: hitting 20-recipe limit, tapping dietary adaptation, starting guided cook mode
5. Annual renewal: 7-day advance notification. "Your RecipeSnap Premium renews in 7 days."

### 6.4 Cancellation Intercept
1. "Before you go — pause your subscription for 1-3 months? All your recipes stay safe."
2. Reason picker: Too expensive / Not cooking enough / Found alternative / Missing feature
3. If "Too expensive" → 50% off 6 months ($2.49/mo). Yield: 25-35% save rate.
4. If "Not cooking enough" → "Switch to weekly inspiration? We'll send 3 recipes every Sunday."
5. Still cancels → "We'll keep your cookbook for 90 days. Come back anytime."

---

## SECTION 7: VIRALITY ENGINE

### 7.1 Shareable Moments
1. **"I made this!" card** — Finished recipe photo + RecipeSnap frame + streak count. Instagram-ready.
2. **Streak milestone** — "30-Day Cooking Streak 🔥 on RecipeSnap" shareable badge
3. **Recipe discovery** — "You'd love this: [Recipe]. I found it on RecipeSnap."
4. **Year in Food** — Spotify Wrapped-style annual: "You cooked 187 recipes, mastered 12 cuisines. Your top dish: Creamy Tuscan Chicken."
5. **Challenge a friend** — "I bet you can't match my 7-day streak. Join RecipeSnap."

### 7.2 Viral Mechanics
- **Invite:** One tap → native share sheet. No email forms. Reward: 1 free month for both.
- **Network effect:** Shared family meal plans. Solo usable, better with partner/roommates.
- **Watermark:** Every shareable image: subtle "Made with RecipeSnap" footer. Elegant, Canva-style.

### 7.3 Rating Protection
- ≤2 stars: Route to in-app feedback form. "We'd love to fix this. What went wrong?"
- 3 stars: Prompt with pre-selected 4 stars.
- 4-5 stars: Prompt after 3rd completed recipe → App Store rating.
- Reply within 24 hours to ALL reviews. Prioritize 1-2 star responses.

---

## SECTION 8: TECHNICAL SPECIFICATION

### 8.1 Database Schema

```sql
-- Core recipe table
CREATE TABLE Recipe (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    source_url TEXT,
    source_platform TEXT, -- 'tiktok', 'instagram', 'youtube', 'web', 'manual'
    source_thumbnail_url TEXT,
    image_url TEXT,
    prep_time_minutes INTEGER,
    cook_time_minutes INTEGER,
    total_time_minutes INTEGER,
    servings INTEGER DEFAULT 2,
    difficulty TEXT, -- 'easy', 'medium', 'hard'
    cuisine TEXT,
    dietary_tags TEXT, -- JSON array: ['vegetarian', 'gluten-free', 'dairy-free']
    created_at INTEGER, -- Unix timestamp
    updated_at INTEGER,
    is_favorite INTEGER DEFAULT 0,
    cook_count INTEGER DEFAULT 0,
    last_cooked_at INTEGER,
    sync_status TEXT DEFAULT 'local' -- 'local', 'synced', 'pending'
);

-- Ingredients
CREATE TABLE Ingredient (
    id TEXT PRIMARY KEY,
    recipe_id TEXT NOT NULL REFERENCES Recipe(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    quantity REAL,
    unit TEXT,
    notes TEXT,
    sort_order INTEGER,
    is_checked INTEGER DEFAULT 0, -- for cook mode checklist
    dietary_category TEXT -- 'dairy', 'gluten', 'meat', 'vegan', etc.
);

-- Instructions
CREATE TABLE Instruction (
    id TEXT PRIMARY KEY,
    recipe_id TEXT NOT NULL REFERENCES Recipe(id) ON DELETE CASCADE,
    step_number INTEGER NOT NULL,
    text TEXT NOT NULL,
    timer_minutes INTEGER, -- extracted time mention
    timer_label TEXT -- "simmer", "bake", "rest"
);

-- Meal plan
CREATE TABLE MealPlan (
    id TEXT PRIMARY KEY,
    date TEXT NOT NULL, -- ISO date
    meal_type TEXT NOT NULL, -- 'breakfast', 'lunch', 'dinner', 'snack'
    recipe_id TEXT REFERENCES Recipe(id) ON DELETE SET NULL,
    notes TEXT,
    UNIQUE(date, meal_type)
);

-- Grocery list
CREATE TABLE GroceryItem (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    quantity REAL,
    unit TEXT,
    category TEXT, -- 'produce', 'dairy', 'meat', 'pantry', etc.
    is_checked INTEGER DEFAULT 0,
    added_from_recipe_id TEXT,
    added_from_meal_plan_date TEXT,
    sort_order INTEGER
);

-- User preferences (DataStore, not Room)
-- dietary_preferences: [vegetarian, vegan, gluten_free, dairy_free, nut_free]
-- measurement_system: metric | imperial
-- theme_mode: dark | light | system
-- notification_prefs: { cooking_reminders: bool, weekly_plan: bool, inspiration: bool }
-- streak: { current: int, longest: int, last_cooked_date: ISO }

-- Indexes
CREATE INDEX idx_recipe_created ON Recipe(created_at DESC);
CREATE INDEX idx_recipe_favorite ON Recipe(is_favorite) WHERE is_favorite = 1;
CREATE INDEX idx_ingredient_recipe ON Ingredient(recipe_id);
CREATE INDEX idx_instruction_recipe ON Instruction(recipe_id);
CREATE INDEX idx_mealplan_date ON MealPlan(date);
CREATE INDEX idx_mealplan_recipe ON MealPlan(recipe_id);
```

### 8.2 API Endpoints (Backend — Firebase/FastAPI at scale)

```
POST   /api/v1/recipes/extract    — Extract recipe from social media URL or image
GET    /api/v1/recipes             — List user's recipes (paginated)
GET    /api/v1/recipes/{id}        — Single recipe detail
POST   /api/v1/recipes             — Create recipe (manual or corrected extraction)
PATCH  /api/v1/recipes/{id}        — Update recipe
DELETE /api/v1/recipes/{id}        — Delete recipe
POST   /api/v1/recipes/{id}/adapt  — AI dietary adaptation (returns adapted recipe)
POST   /api/v1/recipes/{id}/scale  — Scale servings (returns adjusted quantities)

GET    /api/v1/meal-plan?week={ISO} — Get week's meal plan
PUT    /api/v1/meal-plan           — Set meal plan for a date/meal

POST   /api/v1/grocery-list/generate — Generate from meal plan

Auth: Firebase Auth (Apple, Google, email). JWT Bearer token.
```

### 8.3 Push Notification Schema

```json
{
  "aps": {
    "alert": {
      "title": "Tonight's Dinner: Creamy Tuscan Chicken",
      "subtitle": "35 min · Easy · 4 servings",
      "body": "Tap to start cooking with guided cook mode."
    },
    "sound": "cooking_bell.caf",
    "badge": 0,
    "mutable-content": 1,
    "category": "COOKING_REMINDER"
  },
  "recipe_id": "abc123",
  "deep_link": "recipesnap://recipe/abc123/cook",
  "image_url": "https://cdn.recipesnap.app/recipes/abc123/hero.jpg"
}
```

### 8.4 AI Agent Architecture (On-Device First)

**Recipe Extraction (Cloud + On-Device Hybrid):**
- Cloud: Social media URL → scraped content → structured recipe
- On-Device: Screenshot → Vision OCR → ingredient/instruction parsing → Core ML Phi-4-mini formatting

**Dietary Adaptation (On-Device):**
- Input: Original recipe + target diet (vegan/GF/etc.)
- Model: Phi-4-mini Q4_K_M (~2.2GB) on iOS (Metal), Gemma-3-1B (~1.3GB) on Android (Vulkan)
- ReAct pattern: Analyze ingredients → identify substitutions → generate adapted instructions → validate
- All on-device. Zero cloud cost. Privacy moat.

**Recipe Discovery Recommendations (On-Device):**
- Chain-of-thought: Analyze saved recipes → identify patterns → suggest similar
- Model: Same local LLM. Embedding-based similarity + LLM reasoning.

**Fallback:** Cloud API (GPT-4o-mini via backend) for devices below A17/6GB RAM minimum.

### 8.5 Third-Party Dependencies
- RevenueCat (subscriptions — both platforms)
- Firebase Auth (social login — both platforms)
- Firebase Firestore (Android sync + cross-platform bridge)
- CloudKit (iOS sync)
- TelemetryDeck (iOS analytics)
- Firebase Analytics (Android analytics)
- NO Facebook SDK, NO AdMob, NO Google Ads at launch

---

## SECTION 9: 30-DAY MVP SPRINT PLAN

### Week 1 — Foundation
| Day | iOS | Android | Shared |
|---|---|---|---|
| Mon | Project setup, SwiftData models, CloudKit container | Project setup, Room entities, Firebase project | Finalize DB schema |
| Tue | Onboarding 3-card flow | Onboarding 3-card flow | Design review: onboarding |
| Wed | Home screen: Recipe grid, empty state | Home screen: Recipe grid, empty state | Design review: home |
| Thu | Recipe capture v1: camera + Vision OCR | Recipe capture v1: CameraX + ML Kit OCR | Test extraction pipeline |
| Fri | RevenueCat + custom paywall | BillingClient + custom paywall | Paywall A/B variants |

### Week 2 — Core Experience
| Day | iOS | Android | Shared |
|---|---|---|---|
| Mon | Recipe detail screen + ingredient checklist | Recipe detail screen + ingredient checklist | Design review |
| Tue | Guided cook mode v1 (step-by-step) | Guided cook mode v1 | Cook mode UX test |
| Wed | Timer + Live Activities (iOS) | Timer + foreground service (Android) | Timer integration |
| Thu | Meal planner (drag-and-drop or tap-to-add) | Meal planner | Meal plan UX |
| Fri | Grocery list auto-generation + checklist | Grocery list | Integration test |

### Week 3 — Polish & Virality
| Day | iOS | Android | Shared |
|---|---|---|---|
| Mon | Haptics, animations, transitions | Motion, predictive back, Material You | Micro-interaction review |
| Tue | Share sheet: "I made this!" card | Share intent: "I made this!" card | Virality flow test |
| Wed | WidgetKit (small, medium) | App Shortcuts, widget | Widget review |
| Thu | Accessibility audit (VoiceOver, Dynamic Type) | Accessibility audit (TalkBack) | A11y fixes |
| Fri | Premium upgrade screen + cancellation flow | Premium upgrade + cancellation | Monetization flow test |

### Week 4 — Launch Readiness
| Day | iOS | Android | Shared |
|---|---|---|---|
| Mon | Bug bash + edge cases | Bug bash + edge cases | Cross-platform parity |
| Tue | App Store screenshots + metadata | Play Store listing + feature graphic | ASO final review |
| Wed | TestFlight internal | Internal testing track | Beta tester onboarding |
| Thu | TestFlight external (if approved) | Closed testing (20 testers) | Launch checklist |
| Fri | **SUBMIT TO APP STORE** | **SUBMIT TO PLAY STORE** | 🚀 |

**MVP Cut List:**
- ❌ AI dietary adaptation (build v2, post-launch — needs model fine-tuning)
- ❌ Family/team sharing (v3 — needs account system)
- ❌ Social features (friend following, feeds — v4)
- ❌ "Year in Food" (build for December launch, not MVP)

---

## SECTION 10: LAUNCH CHECKLIST

**Pre-Launch (T-14):**
- [ ] App Store Connect: App record, metadata, screenshots, 6.9" + 6.7"
- [ ] Google Play Console: App, all metadata, feature graphic
- [ ] RevenueCat: Products, entitlements, webhooks configured
- [ ] Privacy Policy live at recipesnap.app/privacy
- [ ] Terms of Service live at recipesnap.app/terms
- [ ] Support email: support@recipesnap.app (auto-responder)
- [ ] TestFlight Beta App Review submitted
- [ ] Play Console closed testing: 20 testers recruited

**Launch Day (T=0):**
- [ ] Manual release App Store (not automatic)
- [ ] Play Store staged rollout 10% → 50% after 24h → 100% after 48h
- [ ] Monitor TelemetryDeck + Firebase crash-free rate
- [ ] Reply to first 10 reviews within 2 hours
- [ ] Reddit post in r/Cooking, r/MealPrepSunday, r/EatCheapAndHealthy
- [ ] Product Hunt launch (12:01 AM PT)
- [ ] Email beta testers: "We're live! 50% off first year — thank you."

---

## SECTION 11: POST-LAUNCH ITERATION PLAN

**Week 1: Observe Only**
- Track: D1 retention, D7 retention, conversion rate, crash rate, session length
- Read EVERY review. Categorize: bug / feature request / UX confusion / pricing objection
- Zero new features. Only critical crash fixes.

**Weeks 2-4: Quick Wins**
- Ship top 3 user-requested improvements
- A/B test paywall if conversion <15% (target: 20%+)
- D1 retention <40% → redesign onboarding
- D7 retention <20% → increase push notification relevance

**Month 2-3: Feature Expansion**
- Ship AI dietary adaptation (most requested Premium feature)
- Ship cost estimates
- Launch iPad-optimized layout
- Begin content marketing: 5 pillar blog posts

---

## SECTION 12: ANTI-PATTERNS

1. ❌ **Do not ask for notification permission on first open.** Ask after first recipe save: "Want us to remind you when it's time to cook?" — custom pre-permission dialog first.
2. ❌ **Do not require account creation before saving a recipe.** "Save locally first, sync later." Every barrier kills 20-30%.
3. ❌ **Do not show ads in first 90 days.** Monetize through Premium, not attention. Ads in a cooking app = greasy.
4. ❌ **Do not use default RevenueCat paywall.** Custom SwiftUI/Compose. Default converts 40% worse.
5. ❌ **Do not ship a static splash screen.** Animate immediately into home. Skeleton UI if loading.
6. ❌ **Do not ignore 1-star reviews.** Reply within 24 hours. Many upgrade.
7. ❌ **Do not machine-translate.** English only at launch. Add Spanish + German when you can afford human translators.
8. ❌ **Do not launch both platforms simultaneously if resources tight.** iOS-first. Android 2 weeks behind with App Store learnings.
9. ❌ **Do not build features nobody asked for.** Ship at least one user-requested improvement every sprint.
10. ❌ **Do not underestimate the cooking context.** Users have messy hands. Design for one-thumb, glanceable, voice-friendly interaction.

---

*Generated by App Discovery Pipeline | Phase 5 Scaffold | June 3, 2026*
*Target: RecipeSnap — Social Recipe Saver & Meal Planner | $4.99/mo | iOS + Android*