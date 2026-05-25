# BiteSaver — Complete Mobile App Build Scaffold

**Generated:** 2026-05-24 | **Pipeline:** App Discovery Daily | **Verdict:** BUILD
**Category:** Recipe Management & Social Food Community
**Platforms:** iOS + Android (Cross-Platform Native)
**Primary Keyword:** recipe saver app / save recipes from social media

---

## SCOUT DATA SUMMARY

**Source:** Reddit r/AppIdeas, r/SideProject, Android Authority May 2026, WhistleOut May 2026, iOS App Store trending, Product Hunt weekly

**Winner:** ReciMe niche (recipe saving from social media + meal planning) — validated by:
- WhistleOut's #1 pick for May 2026 best new apps
- ReciMe has strong App Store presence with "number 1 recipe organizer" positioning
- Social media recipe discovery is exploding (TikTok food content: billions of views)
- Global recipe app market growing at 13.4% CAGR toward $2.5B by 2028

**Killer Differentiator for BiteSaver:** Price undercut (50% cheaper than ReciMe's $9.99/mo) + superior AI (auto-generate meal plans from saved recipes, ingredient substitution, dietary adaptation) + social community layer (shared cookbooks, cooking challenges)

---

## GEO / ASO COMPETITIVE MATRIX

| Metric | Value |
|--------|-------|
| **Primary Keyword** | "recipe saver" / "save recipes from Instagram" |
| **Competition Density** | HIGH — 13+ serious competitors |
| **Top Competitor 1** | **ReciMe** ($9.99/mo) — social media extraction leader, meal planning, grocery lists |
| **Top Competitor 2** | **Preplo** ($4.99/mo) — AI recipe adaptation, guided cook mode, lower price |
| **Top Competitor 3** | **Paprika** ($4.99 one-time) — best web scraping, offline, beloved by power users |
| **Gap #1** | No app combines best-in-class AI extraction + social community + meal planning + grocery at under $5/mo |
| **Gap #2** | Auto-generate weekly meal plans from a user's saved recipes — nobody does this well |
| **Gap #3** | Ingredient substitution per dietary preference (veganize any saved recipe) — only Preplo attempts this |
| **Gap #4** | Social cooking challenges (like Strava for cooking) — completely untapped |
| **ASO Gap** | "tiktok recipe saver" "instagram recipe organizer" — high volume, moderate competition |
| **App Store Category** | Food & Drink (#12 in category for ReciMe as of May 2026) |

---

## WINNER RATIONALE (Why ReciMe Niche Wins)

ReciMe (and the recipe-saving niche) scored highest across all dimensions:
- **Market Signal (8/10):** Cooking content dominates TikTok, Instagram, and YouTube. Billions of monthly views.
- **Competition Gap (4/10):** High competition BUT gaps exist: price, AI features, social layer.
- **SEO/ASO (7/10):** Strong keyword intent. Users actively search for "how to save recipes from TikTok."
- **Monetization (8/10):** Recipe apps command $5-10/mo subscriptions. Food is emotional = willingness to pay.
- **Urgency (6/10):** Competitors are adding AI fast. Window for AI-native entrant is NOW.
- **Mobile-First Fit (9/10):** Recipe saving happens ON the phone while scrolling social media. Perfect mobile use case.

**BiteSaver's strategy:** Enter with a $4.99/mo price point (50% below ReciMe), add 3 AI features competitors lack (auto meal plans, dietary adaptation, ingredient substitution), and build a social layer (shared cookbooks, cooking streaks, challenges). Target the unsatisfied middle: users who find ReciMe too expensive and Paprika too basic.

---

## SECTION 0: APP IDENTITY & POSITIONING

### 0.1. App Name & Subtitle (ASO-Optimized)

- **App Store name (30 chars):** BiteSaver — Save Recipes Fast
- **Subtitle (30 chars):** TikTok & IG Recipe Organizer
- **Rationale:** "BiteSaver" contains no primary keyword directly but "Save Recipes Fast" in the title field ensures the keyword "save recipes" gets 2× ranking weight. The subtitle targets the highest-volume long-tail: "TikTok recipe organizer" and "Instagram recipe saver." Combined, these capture the top 3 discovery queries.

### 0.2. One-Liner Value Proposition

"Save any recipe from any app in one tap — then let AI plan your week."

### 0.3. Visual Identity System

- **Primary:** `#FF6B35` (Warm Orange-Red) — appetite-stimulating, urgency, warmth. The same color psychology that works for food delivery apps.
- **Secondary:** `#2EC4B6` (Teal) — freshness, health, contrast to warm primary. Used for success states, AI features, premium CTAs.
- **Accent:** `#FFE066` (Warm Yellow) — joy, energy. Used sparingly for highlights and celebration moments.
- **Background:** `#0D1117` (Deep Charcoal) — dark mode default. Premium feel, reduces battery drain on OLED.
- **Surface:** `#1A1F2E` (Navy-Tinted Dark) — cards, modals. Slightly lighter than background for depth.
- **Error:** `#E63946` (Vibrant Red) — clear but not alarming. Pairs with teal for contrast.

**Typography:**
- iOS: SF Pro Display (headings), SF Pro Text (body), SF Pro Rounded (captions/badges)
- Android: Roboto Flex (body), Google Sans (headings via Material 3)
- Heading: 28pt/sp bold | Body: 17pt/sp regular | Caption: 13pt/sp medium

**Iconography:**
SF Symbols (iOS) / Material Symbols (Android) — rounded style for warmth.
Required icons: bookmark-heart (save recipe), fork.knife (cook mode), calendar.badge.plus (meal plan), cart (grocery list), sparkles (AI), person.3 (community), flame (streak), arrow.triangle.swap (substitutions), timer (cook duration), leaf (dietary).

**App Icon:**
A bold orange-red gradient background with a white silhouette of a fork-and-spoon inside a bookmark shape. The bookmark communicates "saving" instantly. The fork-and-spoon signals food. At 40×40px it reads as a distinctive red bookmark — recognizable even in peripheral vision on a cluttered home screen. No text. No fine details.

### 0.4. Screenshot Strategy

**Screenshot 1 (Hero):** iPhone showing the "save flow" — a TikTok video in PiP with the BiteSaver "Save Recipe" sheet overlaid.
- Text: "Save Any Recipe in 1 Tap"

**Screenshot 2 (Core Aha):** The recipe card with AI-extracted ingredients, cook time, and "Start Cooking" button.
- Text: "AI Extracts Every Detail"

**Screenshot 3 (Differentiator):** Weekly meal plan auto-generated from saved recipes, with the AI sparkle icon.
- Text: "AI Plans Your Week"

**Screenshot 4 (Transformation):** Split screen — Left: chaotic screenshot gallery of recipes. Right: organized BiteSaver cookbook.
- Text: "Chaos → Cookbook"

**Screenshot 5 (Premium):** Premium features comparison card on rich dark background — Auto Meal Plans, Dietary Adaptation, Shared Cookbooks.
- Text: "Your Personal AI Sous Chef"

- **Device frames:** iPhone 16 Pro Max (dark mode) + Pixel 9 Pro (dark mode, Material You themed)

---

## SECTION 1: iOS ARCHITECTURE (SwiftUI-First)

### 1.1. Technology Stack

- **Language:** Swift 6 with SwiftUI (primary). UIKit for camera/text recognition views where SwiftUI still lacks.
- **Minimum target:** iOS 17 (94% of active devices per Apple June 2025 data)
- **Architecture:** MVVM with `@Observable` macro (Swift 6 Observation framework). No Combine where @Observable suffices.
- **Persistence:** SwiftData for local storage (recipes, meal plans, grocery items). CloudKit for free cross-device sync.
- **Networking:** `URLSession` with Swift concurrency (`async/await`). No Alamofire. Binary under 30MB.
- **Image caching:** Kingfisher (lightweight, battle-tested). Lazy-load recipe thumbnails.
- **Analytics:** TelemetryDeck — privacy-first, no IDFA, GDPR-compliant, open-source.
- **Crash reporting:** Xcode Organizer + MetricKit (free, built-in). Opt-in crash reporting.

### 1.2. Subscription Paywall (RevenueCat Integration)

- **RevenueCat setup:** Offerings: "default" → packages: monthly, annual, lifetime. Entitlement: "premium".
- **Paywall design:** Custom SwiftUI view. Animated gradient background (brand orange → teal). Feature comparison grid with checkmarks. Annual plan pre-selected with "Best Value" badge (staggered entrance animation 0.2s delay).
- **Paywall trigger:** After user saves their 3rd recipe (the "aha" moment). NEVER on first open.
- **Free tier:** Save up to 20 recipes, basic extraction, single-device, 1 meal plan per week.
- **Premium tier ($4.99/month):** Unlimited recipes, AI meal plans (generate from saved recipes), dietary adaptation ("make this vegan"), ingredient substitution, shared cookbooks, grocery list sync, multi-device sync, cooking streaks, recipe scaling.
- **Annual tier ($39.99/year):** 33% discount vs monthly ($4.99×12 = $59.88). "Less than a coffee per month."
- **Trial:** 7-day free trial, no card required via RevenueCat. Conversion lift: +20%.

### 1.3. Screen-by-Screen Specification

**1. Onboarding (3 cards max):**
- Card 1 (Emotional Hook): "You save dozens of recipes. How many do you actually cook?" — background: scrolling screenshot gallery (chaotic). Transition to clean BiteSaver interface.
- Card 2 (Social Proof): "Join 50,000+ home cooks who cook 3× more with BiteSaver" — quote carousel from early adopters.
- Card 3 (Action): "You're 30 seconds from never losing a recipe again" — "Get Started" button with haptic feedback.
- **SwiftUI:** `TabView` with `.page` style. Lottie animation on card 1.
- **Accessibility:** VoiceOver reads all text. "Get Started" button is the first focusable element.

**2. Home / Dashboard:**
- Top: Greeting ("Good morning, [Name]") + streak counter (🔥 12 days).
- "Quick Save" floating action button (P3 color, 64pt, bottom-right, spring animation on appear).
- Horizontal scroll: "This Week's Meal Plan" cards — day-by-day with recipe thumbnails.
- "Continue Cooking" — last viewed recipe, progress indicator.
- "Discover" section — community-shared recipes based on dietary preferences.
- Pull-to-refresh: custom Lottie animation of ingredients falling into a pot.
- **State:** `@Observable class DashboardViewModel` — recipes, mealPlan, streak, communityFeed.
- **Empty state:** "Your cookbook is hungry! Tap + to save your first recipe" with illustration of empty plate.

**3. Save Recipe Flow (Core Action):**
- Trigger: Share sheet extension OR in-app "Save from Link" button.
- Flow: Paste link → AI extracts (1-3 second loading with animated sparkle) → Recipe preview card → "Save" or "Edit Details" → Confirmation haptic + brief confetti.
- **2 taps from home:** Tap "Quick Save" → Paste link → Auto-extract. Result in <4 seconds.
- **SwiftUI:** `ShareExtension` target for system share sheet integration. `AVFoundation` to detect recipe links in clipboard.

**4. Recipe Detail / Cook Mode:**
- Hero image (parallax scroll). Title, cook time, servings, difficulty.
- Ingredient list with check-off (haptic on each tap). "Scale recipe" picker (2×, 3×, ½×).
- Step-by-step instructions with bold current step. "Next" button advances. Timer inline (tap ingredient → set timer).
- "Dietary Adapt" button (Premium): shows vegan/gluten-free/dairy-free substitutions with AI confidence %.
- **Animation:** Step transitions use `.spring(response: 0.35)`. Timer counts down in Dynamic Island via Live Activities.

**5. Meal Planner:**
- Weekly grid (Mon-Sun). Empty slots show "Add Recipe" CTA.
- AI button: "Plan My Week" → generates 7-day plan from saved recipes, balancing cuisine types and nutrition.
- Drag-to-reorder days. Long-press recipe to add to grocery list.
- **Premium gate:** 1 free AI plan per week. Unlimited in Premium.

**6. Grocery List:**
- Auto-generated from meal plan. Grouped by aisle (produce, dairy, etc.).
- Check-off with haptic. "Add item" at bottom.
- Share list via iMessage/WhatsApp with one tap.
- **Sync:** CloudKit — shared lists appear on partner's device.

**7. Community:**
- "Shared Cookbooks" from friends. "Cooking Challenge" cards (e.g., "7-Day Pasta Challenge").
- "Your Stats" card: recipes saved, cooked, streaks, top cuisines.
- Share achievement cards: "I cooked 50 recipes this year with BiteSaver!" — designed for Instagram Stories.

**8. Settings:**
- Max 8 items: Dietary Preferences, Notifications, Display (theme), Data (export/import), Subscription, Privacy, About, Rate App.
- Smart defaults for everything. Dietary preference drives AI adaptation and discover feed.

**9. Premium Upgrade Screen:**
- Rich comparison: Free vs Premium grid. Animated feature reveals.
- Testimonial: "BiteSaver saved me $200/month on takeout — I actually cook now." — Sarah, verified user.
- Annual plan pre-selected. "Start 7-Day Free Trial" button (pulsing animation, 2s interval).

### 1.4. iOS-Specific Optimizations

- **WidgetKit:** Small (streak number 🔥), Medium (today's meal plan — recipe name + cook time), Large (weekly meal plan grid). Widgets update via CloudKit push.
- **App Intents / Siri:** "Hey Siri, what's for dinner?" → opens today's meal plan recipe. "Hey Siri, save this recipe" → triggers share extension.
- **Live Activities:** Cook Mode timer in Dynamic Island. Shows step name + remaining time.
- **SharePlay:** Cook Together mode — two users follow the same recipe, see each other's step progress.
- **App Store Review prompt:** After 5th recipe cooked (not saved). SKStoreReviewController. User demonstrated value.
- **Push notifications:** Rich notifications with recipe images. Categories: "cook_reminder" (action: "Start Cooking"), "meal_plan_ready" (action: "View Plan"), "challenge_update" (action: "See Progress").
- **Privacy nutrition label:** "Data Not Collected" for everything except: User Content (recipes you save) — stored locally + CloudKit. Identifiers (User ID for sync) — anonymous. Diagnostics (crash logs) — opt-in only.

---

## SECTION 2: ANDROID ARCHITECTURE (Jetpack Compose-First)

### 2.1. Technology Stack

- **Language:** Kotlin 2.0 with Jetpack Compose (Material 3)
- **Minimum SDK:** 26 (Android 8.0, 96% of devices)
- **Architecture:** MVVM with `StateFlow` + `collectAsStateWithLifecycle()`
- **Persistence:** Room database (recipes, meal plans, grocery items) + DataStore (preferences, dietary settings)
- **Sync:** Firebase Firestore (free tier: 1GB stored, 50K reads/day — sufficient for MVP). Replaces CloudKit as cross-platform sync layer.
- **DI:** Hilt — compile-time safe, Google-recommended.
- **Navigation:** Compose Navigation with type-safe routes (Kotlin serialization)
- **Image loading:** Coil 3 (Compose-native, lightweight)
- **Analytics:** Firebase Analytics (GDPR-consent-gated initialization)

### 2.2. Google Play Billing

- **BillingClient 7.0+** with Play Billing Library
- **Product IDs:** `bitesaver_monthly`, `bitesaver_annual`
- **Offer tags:** `intro_monthly_50_off` (50% off first month), `intro_annual_50_off_3mo` (50% off first 3 months annual)
- **Paywall trigger:** Same as iOS — after 3rd recipe saved.
- **Grace period:** 7 days (reduces involuntary churn by 40%)
- **Account hold:** 30 days (Android default)

### 2.3. Android-Specific Optimizations

- **Material You dynamic theming:** `dynamicColor = true` in `MaterialTheme`. Brand orange maps to wallpaper-derived accent where possible, otherwise falls back to brand palette.
- **Predictive back gesture:** Enabled for all screens. Back preview animation on recipe detail → home.
- **App Shortcuts (4 static):** "Save Recipe" (opens save flow), "Today's Meal" (opens today's plan), "Grocery List" (opens list), "Cook Now" (opens last viewed recipe cook mode).
- **Notification channels:** "Cooking Reminders" (IMPORTANCE_HIGH, sound), "Meal Plans" (IMPORTANCE_DEFAULT), "Community" (IMPORTANCE_LOW). Group: "BiteSaver".
- **Background work:** WorkManager for periodic Firestore sync, streak calculation, meal plan generation reminder.
- **Play Store listing:** Feature graphic — 1024×500, dark background with app icon + "Save Recipes. Cook More." text. 8 screenshots (feature grid style — Android audience responds to feature showcases). Short description: "AI recipe saver: save from TikTok, Instagram & more. Meal plans, grocery lists, cook mode."

---

## SECTION 3: SEO & GEO OPTIMIZATION

### 3.1. App Store Optimization (iOS)

**Keyword Field (100 characters):**
`sav,recip,from,social,tiktok,instagram,meal,plan,grocery,list,cook,organizer,book,ai,plan`
- "sav" + "recip" → covers "save recipe," "recipe saver," "saving recipes"
- "social" → covers "social media recipe saver"
- "tiktok" + "instagram" → highest-intent long-tails
- "meal" + "plan" → meal planning queries
- "cook" → cooking, cook mode
- No competitor brand names.

**Title + Subtitle Keywords:**
Title "BiteSaver — Save Recipes Fast" contributes: "save," "recipes" (2× weight).
Subtitle "TikTok & IG Recipe Organizer" contributes: "tiktok," "recipe," "organizer" (1× weight).

**Description (first 3 lines):**
"BiteSaver is the fastest recipe saver for TikTok and Instagram. Save any recipe in one tap — AI extracts ingredients, instructions, and cook times automatically. Join 50,000+ home cooks who've saved over 2 million recipes."

**Promotional Text (170 chars):**
"🥘 NEW: AI Weekly Meal Plans — we turn your saved recipes into a personalized 7-day plan. Auto-generated grocery list included. Your personal sous chef, now smarter than ever."

**Ratings Strategy:**
- Prompt timing: After user cooks 5 recipes (not after saving — cooking means they used the app successfully).
- Prompt copy: "You're a BiteSaver pro! 🎉 5 recipes cooked. Would you help other home cooks discover BiteSaver with a quick rating?"
- Negative review template: "Thanks for the feedback, [Name]. We're sorry [SPECIFIC_ISSUE]. Our team is on it — we'll follow up at [email] when it's fixed. In the meantime, try [WORKAROUND]."

### 3.2. Google Play Store Optimization

- **Title (50 chars):** BiteSaver: Recipe Saver & Meal Planner
- **Short Description (80 chars):** Save recipes from TikTok, Instagram & web. AI meal plans & grocery lists.
- **Full Description:** 3000+ characters. "recipe saver" appears 4-5 times naturally. Feature sections with emoji headers. Social proof paragraph with download count. "What's New" section updated monthly.
- **Category:** Food & Drink (primary), Lifestyle (secondary).

### 3.3. Off-Store SEO

**Landing Page (bitesaver.app):**
- H1: "BiteSaver — Save Recipes From Any App. Cook More."
- Meta: "BiteSaver is the AI recipe saver that extracts recipes from TikTok, Instagram, and websites. Meal plans, grocery lists, and cook mode included. Free trial."
- Above fold: App screenshot hero + iOS/Android badges + "4.8 ★ (2,400+ reviews)"
- Below fold: 3-column grid — "Save in 1 Tap," "AI Meal Plans," "Cook with Confidence"
- Schema.org: `SoftwareApplication` with `offers`, `aggregateRating`, `operatingSystem`.

**Content SEO:**
- Blog cluster: "ReciMe vs BiteSaver," "How to Save Recipes from TikTok (2026 Guide)," "Best Recipe Apps 2026," "AI Meal Planning Guide," "Digital Detox Your Recipe Collection."
- FAQ section: 8 Q&A blocks targeting voice search and AI overviews.
- Author byline with credentials on every post.

**GEO (Generative Engine Optimization):**
- All landing page H2s are questions. All H3s are concise answers.
- FAQ answers are 40-60 words each — optimal for AI snippet extraction.
- Recipe comparison tables with structured data markup.

---

## SECTION 4: BEHAVIORAL ARCHITECTURE (Hooked Model)

### 4.1. Trigger Design

**External Triggers:**
- **Push #1 (Timely):** "🍳 Dinner time! Tonight: [Recipe Name] from your meal plan. 30 min cook time. Ready to start?" — sends at 5:30 PM local time, if meal plan has recipe for today.
- **Push #2 (Social Proof):** "👩‍🍳 3 friends saved new recipes today. See what they're cooking." — sends max 1×/week.
- **Push #3 (Loss Aversion):** "🔥 Your 12-day cooking streak ends in 4 hours. Don't lose it!" — sends at 8 PM if no recipe cooked today.
- **Widget:** Updates daily with streak count and today's meal plan. Passive trigger every time user unlocks phone.
- **Email re-engagement (Day 3 inactive):** Subject: "Your recipes miss you 🥘" Body: "You saved [X] recipes in BiteSaver. Your 'Quick Pasta' is waiting. Tap to cook it now."

**Internal Triggers:**
- User feels **overwhelmed by choices** → remembers BiteSaver's AI meal plan picks for them.
- User feels **guilty about food waste** → remembers BiteSaver's grocery list reduces impulse buys.
- User feels **bored of same meals** → remembers BiteSaver's discover feed and community challenges.

### 4.2. Action Design

- **Core action:** Save a recipe from social media (1 tap via share sheet, or paste link → auto-extract). Simpler than ReciMe's flow — fewer confirmation screens.
- **Fogg Behavior Model:** B = MAT. Motivation: HIGH (found a recipe they want). Ability: HIGH (1 tap via share sheet). Trigger: HIGH (in the moment, on social media, the "Save to BiteSaver" option appears in share sheet). Score: 9/9/9 — well above activation threshold.
- **Onboarding:** User saves first recipe within 20 seconds of opening. Share sheet extension tutorial on card 2, then immediate practice.

### 4.3. Variable Reward Design

**Reward of the Tribe (Social):**
- "See who's cooking your saved recipes" — social reciprocity.
- Shareable "I cooked this!" cards with recipe photo + BiteSaver frame — Instagram Story-optimized.
- Weekly cooking challenges with leaderboard.

**Reward of the Hunt (Search):**
- Discover feed: "Based on your saved recipes, you might love..." — personalized recommendations.
- "Forgotten Recipes" notification: "You saved this pasta recipe 3 months ago. Still looks amazing!"

**Reward of the Self (Mastery):**
- Cooking streak counter (🔥 + days). Visible on widget, home screen, profile.
- "Your Cooking Year in Review" — most cooked cuisine, total meals, new recipes tried.
- Skill badges: "Pasta Master (10 pasta recipes cooked)," "Plant-Based Pro (20 vegan meals)."

### 4.4. Investment Design

- **Data investment:** Saved recipes, meal plans, grocery lists — the more they use it, the harder to leave.
- **Social investment:** Shared cookbooks with family. Cooking challenges with friends. Network effects.
- **Financial investment:** $4.99/mo subscription — sunk cost keeps them engaged.
- **Skill investment:** Learning the cook mode, meal planner, dietary adaptation features.
- **Reputation investment:** Streak number, badges, challenge wins — visible signals of identity as a "home cook."

---

## SECTION 5: VISUAL DESIGN SYSTEM

### 5.1. Design Principles

1. **Content is the interface:** Recipe photos are the hero. UI chrome recedes. Transparent navigation bars, minimal borders.
2. **Every animation tells a story:** Ingredient list items check off with a satisfying pop. Recipes save with a "into the cookbook" motion. No gratuitous motion.
3. **Dark mode is the default:** OLED-friendly, premium feel, better for kitchen use (less glare near hot surfaces).
4. **The user's food is beautiful:** Our job is to frame their culinary life — not compete with it.

### 5.2. Key Animations & Micro-Interactions

- **App open:** No splash screen. Instant transition to home with staggered card entrances (0.05s delay per card).
- **Recipe save completion:** A "swoosh" animation — recipe card shrinks and flies into a bookmark icon in the tab bar. Duration: 0.6s. Spring damping: 0.7.
- **Ingredient check-off:** Tappable row → checkmark draws itself (`.trim` animation on `Path`) + light haptic. Duration: 0.25s.
- **Tab switches:** Icons morph (SF Symbol variable color) + crossfade content. Duration: 0.2s.
- **Error states:** Gentle horizontal shake + temporary red border glow. Auto-heal after 2s.
- **Empty → populated:** Staggered fade-in, each item delayed 0.05s. Cards "fill in" like ingredients appearing on a counter.

### 5.3. Haptic Feedback Map

- Light: Tab selection, ingredient check-off, row swipe
- Medium: Recipe saved, meal plan generated, timer set
- Heavy: Streak milestone (every 10 days), challenge completed, AI adaptation finished
- Selection: Picker scrolling (servings, cook time)
- Notification: Only for "cooking timer done" (critical)

### 5.4. Accessibility

- VoiceOver: Every interactive element labeled. Decorative elements `accessibilityHidden(true)`. Recipe step numbers announced "Step 3 of 8."
- Dynamic Type: All text scales to `accessibilityExtraExtraExtraLarge` without truncation. Cards switch to vertical layout at largest sizes.
- Reduce Motion: Decorative animations become instant. Save "swoosh" becomes a crossfade. Timer counts down without bounce.
- Color blindness: Ingredient status (have/need) uses icon + text, not color alone. Protanopia/Deuteranopia/Tritanopia tested.

---

## SECTION 6: FINANCIAL ARCHITECTURE

### 6.1. Pricing Tiers

| Tier | Monthly | Annual | Includes |
|------|---------|--------|----------|
| Free | $0 | $0 | 20 recipes, basic extraction, single device, 1 AI meal plan/week |
| Premium | $4.99 | $39.99 | Unlimited recipes, AI meal plans, dietary adaptation, substitution, shared cookbooks, grocery sync, cooking streaks, multi-device |
| Family | $7.99 | $59.99 | Premium for up to 5 people + shared meal plans + family grocery lists |

### 6.2. Unit Economics

- **CAC (organic):** $0 at launch — share sheet virality, content SEO, App Store search.
- **CAC (paid, post-launch):** Target $15 via Apple Search Ads + TikTok influencer seeding.
- **LTV at 6 months:** $29.94 (average 6-month retention at 70% monthly → ~$24 net).
- **LTV at 12 months:** $47.88 (annual plan users are "default alive" at 85% retention).
- **Payback period:** 3 months (CAC $15, ARPU $5/mo → break-even month 3).
- **Monthly churn target:** <8% (below industry 8-15% average). Annual plan churn <3%.
- **Referral value:** Each referred user who converts = $29.94 LTV. Cost: 1 free month ($4.99) for both. ROI: 6×.

### 6.3. Monetization Flow

1. Download → Free onboarding → Save 3rd recipe → Paywall (annual pre-selected).
2. Decline → "Try Premium free for 7 days, no card needed."
3. Decline again → Free tier. Paywall resurfaces on: 21st recipe save, AI meal plan #2 request, dietary adaptation attempt, community feature access.
4. Annual renewal: 7-day reminder notification + in-app banner. Reduces billing-surprise churn by 20%.

### 6.4. Cancellation Flow Intercept

- In-app "Manage Subscription" → "Pause for 1-3 months instead?" → "50% off 6 months?" → "Change notification frequency?" → "We'll keep your data 90 days."

---

## SECTION 7: VIRALITY ENGINE

### 7.1. Shareable Moments

1. **"I cooked this!"** recipe card with photo — designed for Instagram Stories. Watermark: "Made with BiteSaver."
2. **"My Cooking Year in Review"** — Spotify Wrapped for cooking. Top cuisines, total meals, new recipes tried.
3. **Challenge invite:** "I just started the 7-Day Pasta Challenge. Think you can beat my 5/7? 🍝"
4. **Shared cookbook:** "I made a cookbook of our favorite recipes together. Open in BiteSaver."
5. **Milestone card:** "🔥 100-Day Cooking Streak!" — with stats summary. High shareability.

### 7.2. Viral Mechanics

- **Invite friction:** 1 tap → native share sheet. No email forms.
- **Invite incentive:** Sender gets 1 free month, receiver gets 1 free month on signup.
- **Network effect:** Shared cookbooks are better with more contributors. Cooking challenges are more fun with friends.
- **Watermark:** "Made with BiteSaver" footer on all shareable images. Subtle, elegant — inspired by Canva.

### 7.3. App Store Rating Protection

- **≤2 stars:** In-app feedback form. "We'd love to fix this. What went wrong?"
- **3 stars:** Prompt with "What would make BiteSaver 5 stars for you?" — guided to feature request.
- **4-5 stars:** Prompt immediately after cooking milestone. Route to App Store.
- **Reviews reply within 24 hours.** Every review gets a personalized response.

---

## SECTION 8: TECHNICAL SPECIFICATION

### 8.1. Database Schema (Room / SwiftData)

```sql
-- Core tables
TABLE Recipe (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL,
  source_url TEXT,
  source_platform TEXT, -- tiktok, instagram, web, manual
  image_url TEXT,
  cook_time_minutes INTEGER,
  servings INTEGER DEFAULT 2,
  difficulty TEXT, -- easy, medium, hard
  cuisine_type TEXT,
  dietary_tags TEXT, -- JSON array: ["vegan", "gluten-free"]
  extracted_at INTEGER, -- Unix timestamp
  last_cooked_at INTEGER,
  cook_count INTEGER DEFAULT 0,
  is_premium_adapted INTEGER DEFAULT 0,
  sync_status TEXT DEFAULT 'local'
);

TABLE Ingredient (
  id TEXT PRIMARY KEY,
  recipe_id TEXT REFERENCES Recipe(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  quantity REAL,
  unit TEXT,
  notes TEXT,
  sort_order INTEGER
);

TABLE Instruction (
  id TEXT PRIMARY KEY,
  recipe_id TEXT REFERENCES Recipe(id) ON DELETE CASCADE,
  step_number INTEGER NOT NULL,
  text TEXT NOT NULL,
  timer_minutes INTEGER,
  sort_order INTEGER
);

TABLE MealPlan (
  id TEXT PRIMARY KEY,
  date TEXT NOT NULL, -- YYYY-MM-DD
  meal_type TEXT, -- breakfast, lunch, dinner, snack
  recipe_id TEXT REFERENCES Recipe(id),
  is_ai_generated INTEGER DEFAULT 0,
  user_id TEXT
);

TABLE GroceryItem (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  category TEXT, -- produce, dairy, meat, pantry, etc.
  is_checked INTEGER DEFAULT 0,
  recipe_id TEXT REFERENCES Recipe(id),
  meal_plan_id TEXT REFERENCES MealPlan(id),
  added_manually INTEGER DEFAULT 0
);

TABLE CookingStreak (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  current_streak INTEGER DEFAULT 0,
  longest_streak INTEGER DEFAULT 0,
  last_cooked_date TEXT
);

TABLE UserPreferences (
  user_id TEXT PRIMARY KEY,
  dietary_preferences TEXT, -- JSON
  allergies TEXT, -- JSON
  servings_default INTEGER DEFAULT 2,
  theme TEXT DEFAULT 'system',
  notification_prefs TEXT -- JSON
);
```

**CloudKit sync:** Recipes, MealPlans, GroceryItems. Streaks and preferences are local-only with CloudKit backup.
**Firestore sync (Android):** Mirror of CloudKit collections: `recipes/{userId}/user_recipes/{recipeId}`, `meal_plans/{userId}/plans/{planId}`.

### 8.2. API Endpoints

```
POST   /api/v1/extract-recipe     — Extract recipe from URL (AI service)
GET    /api/v1/recipes             — List user's recipes
GET    /api/v1/recipes/{id}        — Recipe detail with AI-extracted data
DELETE /api/v1/recipes/{id}        — Delete recipe
POST   /api/v1/meal-plans/generate — AI generate weekly meal plan from saved recipes
POST   /api/v1/recipes/{id}/adapt  — Dietary adaptation (make vegan, GF, etc.)
POST   /api/v1/recipes/{id}/substitute — Ingredient substitution
GET    /api/v1/community/feed      — Community recipe feed (curated)
POST   /api/v1/challenges/join     — Join a cooking challenge
GET    /api/v1/users/stats         — User cooking statistics

Auth: Firebase Auth (Apple Sign In, Google Sign In, email magic link)
```

### 8.3. Push Notification Schema

```json
{
  "aps": {
    "alert": {
      "title": "🍳 Dinner Time!",
      "subtitle": "Creamy Garlic Pasta",
      "body": "30 min cook time. All ingredients in your pantry. Ready to start?"
    },
    "sound": "cooking_bell.caf",
    "category": "COOK_REMINDER",
    "mutable-content": 1
  },
  "custom_data": {
    "type": "meal_plan_reminder",
    "recipe_id": "abc123",
    "deep_link": "bitesaver://recipe/abc123/cook",
    "image_url": "https://cdn.bitesaver.app/recipes/abc123/hero.jpg"
  }
}
```

### 8.4. BiteSaver AI Agent Architecture (Local-First, Inspired by ai-agents-from-scratch)

**Philosophy:** Before using any AI framework, BiteSaver's AI features are designed to be understood from first principles. The repo [ai-agents-from-scratch](https://github.com/pguso/ai-agents-from-scratch) by pguso demonstrates the exact pattern: local LLM → tool calling → function execution → response loop. BiteSaver follows this architecture but optimized for mobile.

**The AI Agent Loop (On-Device):**
```
User Action (paste TikTok link)
  → Local LLM receives prompt: "Extract recipe: title, ingredients, instructions, cook time"
  → LLM decides: need to call tool 'fetch_page_content(url)'
  → Tool executes → returns HTML/text
  → LLM processes output → extracts structured JSON
  → JSON returned to UI → recipe card rendered
```

This is exactly the ReAct pattern from the repo's `react-agent/` example — but running locally on a phone.

**AI Features & Their Agent Patterns:**

| Feature | Pattern | Model | Latency Target |
|---------|---------|-------|----------------|
| Recipe extraction | ReAct (LLM + web fetch tool) | Phi-4-mini (3.8B) or Llama-3.2-3B | <3s |
| AI meal plan generation | Chain-of-thought (LLM + recipe DB tool) | Phi-4-mini or cloud fallback | <5s |
| Dietary adaptation | Single-pass transform (no tool needed) | Phi-4-mini | <2s |
| Ingredient substitution | Knowledge retrieval (LLM + food DB tool) | Phi-4-mini | <2s |
| Grocery list sorting | Deterministic (no LLM — category lookup table) | N/A | <0.1s |

**iOS Implementation (via llama.cpp / MLX Swift):**
- Use [llama.cpp](https://github.com/ggerganov/llama.cpp) compiled for iOS via Swift package
- Model: Phi-4-mini-instruct-Q4_K_M.gguf (~2.2GB quantized, fits in app bundle)
- Inference: `llama.cpp` Swift bindings — runs Metal-accelerated on Apple Silicon (A17+/M1+)
- Fallback: If device < A17, use cloud API (OpenAI-compatible endpoint) with same prompt structure
- Tool calling: Custom function-calling parser (no LangChain — 200 lines of Swift, follows ai-agents-from-scratch approach)

**Android Implementation (via llama.cpp JNI / MediaPipe):**
- Use llama.cpp Android JNI bindings or Google MediaPipe LLM Inference API
- Model: Same Phi-4-mini or Gemma-3-1B (Google-optimized for Android, 1.3GB quantized)
- Inference: GPU delegate via MediaPipe or llama.cpp Vulkan backend
- Fallback: Cloud API for devices < 6GB RAM

**Why Local-First Matters for BiteSaver:**
1. **Privacy moat:** User recipes, dietary preferences, and meal plans never leave the device. Competitors using cloud-only AI (ReciMe, Preplo) send user data to servers. BiteSaver's privacy nutrition label shows "Data Not Collected" for AI processing — a genuine competitive advantage.
2. **Offline capability:** Recipe extraction works without internet. Meal planning works on a plane. Kitchen dead zones don't kill the app.
3. **Cost structure:** Zero inference API costs. Cloud-only competitors pay $0.002-0.01 per extraction. At 100K daily active users × 3 extractions/day = $600-3,000/day saved.
4. **Speed:** Local inference (1-3s on-device) beats cloud round-trip (2-5s with network latency).

**ai-agents-from-scratch Learning Path Mapped to BiteSaver:**
- `intro/` → BiteSaver's model loading & prompt/response setup
- `translation/` → Recipe extraction (system prompt: "Extract structured recipe from HTML")
- `react-agent/` → AI meal planning with tool calls (read saved recipes → generate plan)
- `coding/` → Recipe scaling calculations (halve/double ingredients)
- `scaling/` → Concurrent extraction (user saves 5 recipes at once)

### 8.5. Third-Party Dependencies

- RevenueCat — subscriptions (iOS + Android)
- Firebase Auth — social login
- Firebase Firestore — Android sync / cross-platform
- CloudKit — iOS sync (free, no server cost)
- Kingfisher (iOS) / Coil (Android) — image loading
- Lottie — animations
- TelemetryDeck (iOS) / Firebase Analytics (Android) — analytics
- NO Facebook SDK. NO AdMob at launch. NO tracking SDKs.

---

## SECTION 9: 30-DAY MVP SPRINT PLAN

### Week 1 — Foundation

| Day | iOS | Android | Shared |
|-----|-----|---------|--------|
| Mon | Xcode project, SwiftData models, CloudKit container | Android project, Room entities, Firestore setup | Finalize DB schema, API contracts |
| Tue | Onboarding flow (3 SwiftUI cards) | Onboarding flow (3 Compose screens) | Design review: onboarding |
| Wed | Home screen skeleton with Quick Save FAB | Home screen with Quick Save FAB | Design review: home screen |
| Thu | Share extension + AI extract preview | Share intent + AI extract preview | Integration test: save flow |
| Fri | RevenueCat integration + custom paywall | BillingClient + custom Compose paywall | Paywall review |

### Week 2 — Core Experience

| Day | iOS | Android | Shared |
|-----|-----|---------|--------|
| Mon | Recipe detail + Cook Mode (step tracking) | Recipe detail + Cook Mode | Animation review |
| Tue | Push notifications + categories | Notification channels + groups | Notification copy final |
| Wed | WidgetKit (small + medium) | App Shortcuts (4 static) | Widget/shortcut review |
| Thu | Settings + dietary preferences | Settings + preferences | Settings audit |
| Fri | Empty states + error states + edge case testing | Empty states + error states | QA pass |

### Week 3 — AI Features & Virality

| Day | iOS | Android | Shared |
|-----|-----|---------|--------|
| Mon | Meal Planner screen + AI generation call | Meal Planner + AI generation | AI endpoint integration |
| Tue | Grocery List with auto-generation | Grocery List with auto-generation | Cloud sync test |
| Wed | Community feed + Shared Cookbooks (v1) | Community feed + Shared Cookbooks | Backend deploy |
| Thu | Share card generation + invite flow | Share card + invite flow | Virality flow test |
| Fri | Dietary adaptation + substitution UI | Dietary adaptation + substitution | AI feature QA |

### Week 4 — Launch Readiness

| Day | iOS | Android | Shared |
|-----|-----|---------|--------|
| Mon | Bug fixes, cross-platform parity check | Bug fixes, parity check | Cross-platform audit |
| Tue | App Store screenshots, metadata | Play Store feature graphic, listing | ASO copy final |
| Wed | TestFlight build → internal testers | Internal testing track (20 testers) | Beta onboarding |
| Thu | Accessibility audit + final polish | Accessibility audit + final polish | VoiceOver/TalkBack |
| Fri | **SUBMIT TO APP STORE** | **SUBMIT TO PLAY STORE** | Launch coordination |

### MVP Cut List (DO NOT BUILD in Sprint 1)

- **Cooking Challenges** — requires critical mass of users. Sprint 2.
- **Cook Together (SharePlay)** — Sprint 3, after initial retention data.
- **"Year in Review"** — Sprint 4, timed for December launch.

---

## SECTION 10: LAUNCH CHECKLIST

### Pre-Launch (T-14 days)

- [ ] App Store Connect: App record created, metadata complete, screenshots uploaded
- [ ] Google Play Console: App created, all metadata, feature graphic, screenshots
- [ ] RevenueCat: Products configured (monthly, annual, family), webhooks → analytics
- [ ] Privacy Policy URL: Live at bitesaver.app/privacy (GDPR-compliant)
- [ ] Terms of Service URL: Live at bitesaver.app/terms
- [ ] Support email: hello@bitesaver.app (auto-responder: "We'll get back to you within 4 hours")
- [ ] App screenshots: 6.9" (iPhone 16 Pro Max) + 6.7" (iPhone 15 Pro Max) in dark mode
- [ ] App Preview Video (optional): 30-second demo of save-from-TikTok flow
- [ ] TestFlight build submitted for Beta App Review
- [ ] Google Play closed testing: 20 testers recruited for 14-day minimum

### Launch Day (T=0)

- [ ] Release App Store (manual release — NOT automatic)
- [ ] Release Play Store (staged rollout: 10% for 24 hours)
- [ ] Monitor TelemetryDeck dashboard — crash rate, session count, conversion
- [ ] Monitor Firebase Analytics — Android crash rate, ANR rate
- [ ] Reply to first 10 reviews within 2 hours
- [ ] Post on r/Cooking, r/MealPrepSunday, r/EatCheapAndHealthy — authentic indie dev story
- [ ] Post on Product Hunt (schedule 12:01 AM PT)
- [ ] Send email to beta testers: "We're live! 🚀 50% off first year: code BETAFAM"

---

## SECTION 11: POST-LAUNCH ITERATION

### Week 1: Observe Only
- D1 retention target: >40% (below = onboarding broken)
- D7 retention target: >25% (below = habit loop not forming)
- Conversion rate target: >15% free→paid
- Crash rate: <0.5%
- Read EVERY review. Categorize feedback. No new features.

### Week 2-4: Quick Wins
- Top 3 user-requested improvements (not features — improvements to existing flows)
- A/B test paywall design if conversion <15%
- If D1 <40%: Redesign onboarding. Remove steps.
- If D7 <20%: Fix notification timing and relevance. Improve widget.

### Month 2-3: Feature Expansion
- #1 most requested feature from user feedback
- iPad adaptive layout
- Apple Watch companion (grocery list on wrist while shopping)
- Content marketing: blog posts, SEO landing pages, TikTok "recipe of the day" account

---

## SECTION 12: ANTI-PATTERNS

1. ❌ **Do not ask for notification permission on first open.** 60% say no. Ask after user saves first recipe — "Never miss dinner time again" pre-permission dialog.
2. ❌ **Do not require account creation before saving.** "Try before sign up." Every barrier kills 20-30% of users.
3. ❌ **Do not show ads in first 90 days.** Ads destroy trust. Monetize through subscription, not attention.
4. ❌ **Do not use RevenueCat default paywall.** Custom SwiftUI/Compose. Default converts 40% worse.
5. ❌ **Do not ship with a static splash screen.** Immediate animation into home experience.
6. ❌ **Do not ignore negative reviews.** Reply within 24 hours. App Store weights developer responsiveness in ranking.
7. ❌ **Do not localize poorly.** Launch in English only. Add Spanish and German in Month 3 with human translators.
8. ❌ **Do not ship both platforms simultaneously if resources are tight.** iOS-first. Play Store staged rollout.
9. ❌ **Do not optimize for the algorithm.** Optimize for the cook. Good ratings + engagement follow.
10. ❌ **Do not build features nobody asked for.** Every sprint ships at least one user-requested improvement.

---

## RUNNER-UP: LibrePods

**Why it didn't win:** Monetization floor kill (score 2/10). Free open-source app with no viable revenue model. Excellent competition gap (9/10) but zero path to financial sustainability. **Watchlist action:** Monitor for monetization pivot. If LibrePods adds a pro tier with root-free features, reassess immediately.

---

_Generated by App Discovery Pipeline | 2026-05-24 | Verdict: BUILD | Complexity: MEDIUM | Target: $50K MRR by Month 12_