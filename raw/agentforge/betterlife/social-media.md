# BetterLife Social Media — Posting History & Strategy

> Complete history of BetterLife social media posts, platform IDs, and strategies.
> **Related:** [[BetterLife-Brand]], [[Board-Directives]], [[Operations]]

---

## Platform Overview

| Platform | Handle | Status |
|----------|--------|--------|
| Instagram | @better_life_ai_coaching | ✅ Active |
| Facebook | Better Life AI Coaching (Page ID: 1124600237410474) | ✅ Active |
| X/Twitter | @BetterLifeatjl | ✅ Active |
| LinkedIn | Company Page 135134648 | ⚠️ Text-only (image upload scope issue) |

## Posting Procedure

### Pipeline: FB → CDN → IG (Primary method)
1. Upload image to FB Page via Graph API (`/page_id/photos`)
2. Get FB photo CDN URL via `GET /photo_id?fields=images`
3. Create IG media container: `POST /ig_id/media` with `image_url=CDN_URL`
4. Publish: `POST /ig_id/media_publish` with `creation_id`
5. X/Twitter: OAuth 1.0a media upload → v2 tweet

**Scripts:**
- `~/workspace/scripts/bl-post-everywhere.py` — all platforms
- `~/workspace/scripts/x-post.py` — X/Twitter only
- `~/workspace/scripts/linkedin_post.py` — LinkedIn only

### Daily Schedule
- **Mon-Thu:** 08:00-08:30 cron job → generate → audit → present → post
- **Fri:** Feel-Good Friday
- **Sat:** Saturday Stillness
- **Sun:** Sunday Reflection

## Posting History

### 2026-07-17 — Feel-Good Friday ✅
- **Image:** Beach Yoga (variant 3) — kie.ai nano-banana-2
- **Caption:** "Good vibes only. You made it through the week..."
- **FB:** ✅ Photo ID: 122108642889365340 | **IG:** ✅ 18158514325467588
- **X:** ✅ https://x.com/BetterLifeatjl/status/2078042286122778723

### 2026-07-16 — Transformation Thursday
- **Image:** growth-stories (Joerg's choice)
- All platforms posted

### 2026-07-15 — Wellness Wednesday
- Mental health focus

### 2026-07-13 — Motivation Monday ✅
- **Theme:** Start the week strong
- **Image:** Lake deck with mug, misty forest (cool palette, premium wellness)
- **FB:** ✅ | **IG:** ✅ | **X:** ✅ | **LI:** ⚠️ text-only
- ⚠️ **Duplicate posts** due to cron timeout loop (600s → 900s fix applied)

### 2026-07-11 — Saturday Stillness ✅
- **X:** ✅ 2075841303783375310 | **FB:** ✅ | **IG:** ✅
- **LI:** ❌ Token revoked (re-auth needed)

### 2026-07-07 — Tuesday Tips ✅
- **Theme:** Micro-Shifts > Massive Leaps
- **X:** ✅ 2074391325978345581 | **IG:** ✅ 17973502851115779
- **LI:** ✅ company page 135134648 | **FB:** ✅

### 2026-07-06 — Monday Motivation (posted late 16:00)
- **Root cause:** Pipeline gap — cron stopped after generating images, no auto-post trigger
- **FB:** ✅ | **IG:** ✅ | **X:** ✅

### 2026-07-05 — Sunday Reflection ✅
- **Image:** sunday-reflection-ig-final.jpg (110KB, 1024×1024)
- **FB:** ✅ | **IG:** ✅ 18002972804767962

### 2026-07-02 — Thursday Growth ✅
- **Image:** growth-thursday (Board-approved)
- **FB:** ✅ | **IG:** ✅ 18136834435497784

### 2026-06-29 — Monday Motivation ✅
- **Board instruction:** "post everywhere"
- **Image:** lotus sunrise
- **FB:** ✅ | **IG:** ✅ 18120316861802177 | **X:** ✅
- bl-post-everywhere.py created during this session

### 2026-06-25 — X/Twitter First Batch ✅
- **Intro Tweet:** ✅ 2070054633888710760
- **Reply tweets:** ❌ Blocked by Free tier (no read/search)

## Known Issues

| Issue | Status | Fix |
|-------|--------|-----|
| LinkedIn image upload 404 | 🔴 Open | Need OAuth re-auth with w_media_upload scope |
| FTP timeout (Hostinger) | 🔴 Open | FB CDN workaround is permanent |
| X API read/search | 🔴 Open | Upgrade to Elevated tier needed |
| Pipeline auto-post trigger | 🟡 Fixed | Manual approval → CEO posts |

---

## Campaign Briefs (from Claude CLI brain note, 2026-06-26)

### The Situation
BetterLife is live on App Store. Zero ratings. Zero awareness. AI coaching market $6.69B, growing 22.3% CAGR. Competitors are single-domain, forgetful, or enterprise-only. BetterLife is alone in top-right quadrant: AI-Powered × Cross-Domain.

### Campaign 1: "Your Coach Remembers"
- **Angle:** Deep Memory AI — no competitor has this
- **Format:** Instagram Reel / TikTok (9:16)
- **Visual:** Split screen — generic chatbot ("Hello! How can I help?") vs BetterLife ("Hey, last time we talked about your presentation anxiety. How did the meeting go?")
- **CTA:** Download BetterLife. The coach that remembers.
- **Targeting:** AI curiosity, self-improvement, mental wellness interest groups

### Campaign 2: "The App That Replaces 5"
- **Angle:** Unified dashboard — convenience moat
- **Format:** Carousel (IG) / Thread (X)
- **Visual:** 5 app icons fading into one BetterLife icon. Each slide = one domain.
- **Copy:** "Habit tracker. Mood journal. Goal planner. CBT coach. Finance tracker. Or… one app."

### Campaign 3: "4 Million People Lost Their Coach"
- **Angle:** Woebot orphan audience — search-targeted
- **Format:** Static image + search ads ($10-15/day Meta)
- **Keywords:** "Woebot alternative," "AI therapy app," "CBT coach app"
- **Copy:** "When Woebot shut down, 4 million people lost their AI coach. We built one that does more."

### Campaign 4: "Meet Aria & Aeron"
- **Angle:** Coach personality — character-driven brand building
- **Format:** Video series (IG Reels / TikTok)
- **Aria** (Gentle, Playful): "Some days you need a warm hug and someone who believes in you."
- **Aeron** (Direct, Focused): "Some days you need someone to stop you from making excuses."

### Campaign 5: "Real People, Real Words"
- **Angle:** Tester quote — organic validation
- **Format:** Quote card + testimonial
- **Visual:** Screenshot of BetterLife app, quote overlay
- **Copy:** "It does more than any other similar app provides." — an actual user, not our marketing team.

### 2-Week Content Calendar
| Day | Campaign | Format |
|-----|----------|--------|
| Mon | "Your Coach Remembers" | IG Reel + TikTok |
| Tue | "The App That Replaces 5" | IG Carousel + X Thread |
| Wed | "4 Million People" | IG + X + search ads |
| Thu | "Meet Aria" | IG Reel + TikTok |
| Fri | "Meet Aeron" | IG Reel + TikTok |
| Sat | "Real People, Real Words" | Quote card |
| Sun | Roundup / BTS | IG Stories |

### Hashtag Strategy
| Campaign | Primary Hashtags |
|----------|-----------------|
| Your Coach Remembers | #AICoaching #DeepMemory #BetterLifeCare |
| App That Replaces 5 | #ProductivityHack #OneApp #BetterLifeCare |
| 4 Million People | #WoebotAlternative #CBTcoach #BetterLifeCare |
| Meet Aria & Aeron | #AICoach #MeetTheCoach #BetterLifeCare |
| Real People | #RealReview #AICoaching #BetterLifeCare |

**Always-On Branded:** #BetterLifeCare #AICoaching #BetterLifeAI

---

## LinkedIn Integration

### OAuth Flow (Manual 3-Legged)
1. Generate authorization URL: `https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=775zrppl9vp2nh&redirect_uri=http://localhost:9999/callback&scope=openid%20profile%20w_organization_social`
2. Start local HTTP server on port 9999
3. User opens URL → Allow → redirects with code
4. Exchange code for token (POST to `/accessToken`)
5. **2-month token TTL** — re-auth when expired

**❌ CRITICAL:** PKCE breaks LinkedIn OAuth. Do NOT use code_verifier. Use 3-legged auth without PKCE.

**Client ID:** `775zrppl9vp2nh` | **Primary Secret:** `REDACTED_linkedin_secret`
**Company Page ID:** `135134648` | **Script:** `scripts/linkedin_post.py`

### Known Issue
Image upload 404: Need `w_media_upload` scope added on re-auth.

---

## Marketing Image Review Protocol (Board Directive 2026-07-15)

- Script generates **up to 3 variants** per run
- All variants saved to `tool-image-generation/` with numbered filenames (v1, v2, v3)
- **All variants presented** to Board (Joerg) for review in the chat
- Brand audit is advisory only — Board makes the final call
- **No auto-posting** without explicit Board approval
- Script exits with code 42 to signal "images ready, awaiting Board review"

**See:** [[Board-Directives]], [[BetterLife-Brand]]

---

## Image Quality Reference Standard (Board-Approved, 2026-07-07)

### ✅ APPROVED Reference Posts
| Shortcode | Theme | Key Qualities |
|-----------|-------|---------------|
| `DaHtmlJjrE0` | Sunday Reflection | Clean, minimal abstract, calm aesthetic |
| `DadKmEUiKfK` | Abstract Geometric | Premium feel, balanced composition |
| `DaSBCo8Cp29` | Growth Thursday | Professional, on-brand |
| `DaLZYe7jgh0` | Monday Motivation | Strong visual, no clutter |

### ✅ Common Qualities
- No text burned into image
- No watermarks or logo boxes
- No social handles on image
- Clean, minimal composition
- Dark navy/indigo backgrounds
- Premium wellness app aesthetic (Calm/Headspace level)
- Eight-point compass star logo when present

### ❌ REJECTED — What NOT to Produce
- PIL text overlays with Arial font
- Opaque watermark boxes with clashing colors
- Mismatched color schemes between watermark and main image
- Any post-processing that degrades clean FLUX/kie.ai output
- Social handles burned into images (captions only)

---

## X/Twitter Launch (2026-06-25)

- **Handle:** @BetterLifeatjl | https://x.com/BetterLifeatjl
- **First tweet:** ✅ 2070054633888710760 (AI coaching launch)
- **Reply engagement:** ❌ Blocked — X API Free tier has no read endpoints
- **Resolution:** Apply for Elevated access (free, short application)

---

## Posting Procedure — Detailed

### FB → CDN → IG Pipeline (Primary)
1. Upload image to FB Page via Graph API (`/page_id/photos`) — multipart file
2. Get FB photo CDN URL from photo response (`GET /photo_id?fields=images`)
3. Create IG media container: `POST /ig_id/media` with `image_url=CDN_URL`
4. Publish: `POST /ig_id/media_publish` with `creation_id`
5. X/Twitter: OAuth 1.0a media upload → v2 tweet

### ⛔ Core Rules
- **Post from local MacBook only** — no Vane, no remote server, no FTP
- **Credentials in TOOLS.md** — never hardcode in scripts
- **Watermark:** `~/workspace/brand/betterlife-watermark-unified.jpg` — bottom-right, 15-20% size, 85-95% opacity, never substitute

### Scripts
- `~/workspace/scripts/bl-post-everywhere.py` — all platforms
- `~/workspace/scripts/x-post.py` — X/Twitter only
- `~/workspace/scripts/linkedin_post.py` — LinkedIn only

---

## Social Media Research (Pre-launch, 2026-06-21)

### Optimal Posting Times (Local Times)

| Platform | Best Days | Best Times |
|----------|-----------|------------|
| Instagram | Wed, Thu, Tue | Thu 9AM, Wed 12PM, Wed 6PM |
| TikTok | Sat, Sun, Mon | Sun 9AM, Mon 1PM |
| X/Twitter | Wed, Tue, Thu | Tue 9AM, Wed 10AM |
| Facebook | Wed, Thu, Tue | Thu 9AM |
| LinkedIn | Wed, Thu, Tue | Tue/Wed 9-10AM |

Instagram wellness niche: 5-7AM, 12-2PM, 7PM

### Hashtag Strategy (Per Campaign)

| Campaign | Primary Hashtags |
|----------|-----------------|
| Your Coach Remembers | #AICoaching #DeepMemory #BetterLifeCare |
| App That Replaces 5 | #ProductivityHack #OneApp #BetterLifeCare |
| 4 Million People | #WoebotAlternative #CBTcoach #BetterLifeCare |
| Meet Aria & Aeron | #AICoach #MeetTheCoach #BetterLifeCare |
| Real People | #RealReview #AICoaching #BetterLifeCare |

### Ad Strategy
- Budget split: Meta 60% | TikTok 25-30% | X 5% | LinkedIn 0-10% | Reddit 5-10%
- CPI target: $1.50-5.00 | D30 Retention: >25%
- 3-Week kickstart: Audience Testing → Winner Consolidation → Conversion Focus

### Content Calendar: 4:3:2:1
Mon=Motivation, Tue=Education, Wed=Story, Thu=Interactive, Fri=BTS, Sat=Community, Sun=Roundup
