# BetterLife Marketing Department — Operations Manual

> **Last Updated:** 2026-07-29
> **Department Head:** Marvin (CEO, AgentForge)
> **Reports To:** Board (Joerg Peetz)
> **Purpose:** Daily AI-generated social media content for BetterLife.care across Instagram, Facebook, X/Twitter, and LinkedIn.

---

## 1. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    CRON (08:00 daily)                        │
│  OpenClaw isolated session — Gemini 2.5 Flash                │
├─────────────────────────────────────────────────────────────┤
│  1. betterlife-social-daily.py --generate-only               │
│     → kie.ai API → 3 image variants with Mira character      │
│  2. AI composes per-variant per-platform captions            │
│     → writes captions.md to tool-image-generation/           │
│  3. Presents images (MEDIA:) + captions in ONE message       │
│     → Board reviews & approves one variant                   │
├─────────────────────────────────────────────────────────────┤
│  Board: "V2"                                                 │
│                                                              │
│  bl-post-everywhere.py --captions-md PATH --variant 2       │
│     → Reads V2 image + captions from .md file                │
│     → Posts to FB, IG, X, LI with per-platform captions     │
│     → No caption text ever touches CLI args                  │
└─────────────────────────────────────────────────────────────┘
```

**Key principle:** The captions `.md` file is the single source of truth. Captions are written once to a file and read back for posting. No caption text ever passes through `sys.argv` — this structurally prevents the `--ig`/`--platform` class of bug where CLI arguments leak into captions.

---

## 2. Daily Workflow (End-to-End)

### 2.1 Cron Trigger (08:00 Europe/Dublin)

The cron job `BetterLife Daily Social Posting` fires at 08:00 daily. It spawns an **isolated OpenClaw session** running Gemini 2.5 Flash (with DeepSeek V4 Pro and GPT-4.1 as fallbacks). The session:

1. **Generates Images:** Runs `betterlife-social-daily.py --generate-only` which creates 3 distinct image variants using kie.ai's `flux-2/flex-image-to-image` model with Mira reference photos.

2. **Composes Captions:** For each variant, the AI composes per-platform captions tailored to that specific scene:
   - Instagram: 150-250 chars, emoji-heavy, 3-5 hashtags, engagement CTA
   - Facebook: 800-1000 chars, personal story narrative, 1-2 hashtags, CTA
   - X/Twitter: ≤280 chars, punchy/concise, 1 hashtag

3. **Writes captions.md:** All 3 variants × 3 platforms = 9 captions written to:
   ```
   /Users/joergpeetz/.openclaw/workspace/tool-image-generation/betterlife-captions-YYYY-MM-DD.md
   ```

4. **Presents to Board:** One Telegram message containing:
   - All 3 image variants (via `MEDIA:/path/to/variant.jpg`)
   - Per-platform captions for each variant
   - A recommendation
   - Waits for Board approval

### 2.2 Board Approval

The Board replies with `V1`, `V2`, or `V3` to approve one variant.

### 2.3 Posting

From the main session, run:
```bash
python3 ~/.openclaw/workspace/scripts/bl-post-everywhere.py \
  --captions-md /Users/joergpeetz/.openclaw/workspace/tool-image-generation/betterlife-captions-YYYY-MM-DD.md \
  --variant N
```

The script:
1. Parses the `.md` file for variant N
2. Extracts the image path and per-platform captions
3. Posts to Facebook → Instagram (via FB CDN URL) → X/Twitter → LinkedIn
4. Reports results

### 2.4 Fallback / Manual Posting

The script also supports legacy CLI mode for ad-hoc posts:
```bash
python3 bl-post-everywhere.py image.jpg \
  --ig "Instagram caption" \
  --fb "Facebook caption" \
  --x "X caption" \
  --li "LinkedIn caption"
```

When platform-specific `--ig`/`--fb`/`--x`/`--li` flags are used, only those platforms post.

---

## 3. Cron Jobs

| ID | Name | Schedule | Target | Model | Purpose |
|---|---|---|---|---|---|
| `dc253ad9-13d5-4e84-b9ce-d17bbbaeb690` | BetterLife Daily Social Posting | `0 8 * * *` (Europe/Dublin) | isolated → announce to Telegram | Gemini 2.5 Flash | Generate images + captions, present for Board review |
| `392d78ce-6390-400b-9c7a-62d8e7a156c9` | Memory Dreaming Promotion | cron (daily) | isolated | — | Memory consolidation (not marketing) |
| `678d1b10-74df-4896-9b5b-e31c24168b9d` | n8n-cert-renewal-check | cron (daily) | isolated | — | SSL cert monitoring (not marketing) |

**To manage the marketing cron job:**
```bash
# View details
openclaw task get dc253ad9-13d5-4e84-b9ce-d17bbbaeb690

# Run now (force)
openclaw task run dc253ad9-13d5-4e84-b9ce-d17bbbaeb690 --run-mode force

# Disable
openclaw task update dc253ad9-13d5-4e84-b9ce-d17bbbaeb690 --enabled false
```

---

## 4. Python Scripts

### 4.1 Primary Scripts

| Script | Lines | Purpose |
|---|---|---|
| `betterlife-social-daily.py` | 724 | **Core engine.** Generates 3 image variants via kie.ai, injects Mira character, outfits, and saves to workspace. Called with `--generate-only`. |
| `bl-post-everywhere.py` | 459 | **Posting engine.** Posts to FB/IG/X/LI using either `--captions-md` mode (recommended) or `--ig/--fb/--x/--li` CLI mode (legacy). |
| `joerg-founder-content.py` | 431 | **Pipeline B.** Founder-led thought leadership content for LinkedIn/X. Manually triggered, not automated. |
| `betterlife-mira-daily.py` | 328 | Previous Mira-specific image generator (mostly superseded by `betterlife-social-daily.py`). |
| `kie_image.py` | 268 | Standalone kie.ai image generation CLI tool. `python3 kie_image.py "prompt" --out path.jpg` |
| `x-post.py` | 116 | Standalone X/Twitter posting. `python3 x-post.py "text" [image_path]` |
| `linkedin_post.py` | 131 | Standalone LinkedIn posting with OAuth token management. |

### 4.2 Utility Scripts

| Script | Purpose |
|---|---|
| `bl-delete-all.py` | Delete all BetterLife test posts from a platform |
| `bl-delete-retry.py` | Retry failed deletions |
| `bl-video-captions.py` | Generate video caption overlays |
| `betterlife_first_tweets.py` | Initial Twitter seeding (one-time use) |
| `betterlife_x_engage.py` → symlink | X/Twitter engagement automation |
| `betterlife_x_post.py` → symlink | Alternative X posting |
| `betterlife_x_replies.py` → symlink | X reply automation |
| `betterlife_x_search.py` → symlink | X search utilities |
| `betterlife-composite.py` → symlink | Image compositing |
| `kie_flux_test.py` | kie.ai flux model testing |
| `kie_mira_test.py` | Mira character generation testing |

---

## 5. Image Generation Pipeline

### 5.1 Provider: kie.ai

| Setting | Value |
|---|---|
| API Base | `https://api.kie.ai/api/v1` |
| Model | `flux-2/flex-image-to-image` |
| Auth | Bearer token (stored in `betterlife-social-daily.py`) |
| Cost | ~8-16 credits per image (varies by model) |
| Image Size | 1:1 square, 1K resolution |
| Format | JPG |

**Dashboard:** https://kie.ai/billing (credits), https://kie.ai/logs (task history)

### 5.2 Mira Character (Image-to-Image Reference)

The model uses **img2img** with 8 reference photos of the Mira character from Google Drive. These anchor the character's appearance:

| File | Drive ID | Angle |
|---|---|---|
| Mira_front.png | `1PSdi34X7On-4qTLlbtnJ4JZ_eQSwqa2t` | Front |
| Mira_casual-front.jpg | `1Tti0nBrDaK0dpU6y-Kn0i88Is69ej2Uf` | Casual front |
| Mira_3-4.png | `1qesehRbOZ1tMD2P5B-06V2g12oQbSDo7` | 3/4 view |
| Mira_left_3-4.png | `1XcMzsGf69MJjuNc6OxzTl41ytuxC8GWY` | Left 3/4 |
| Mira_left.jpg | `1BXkJTpyeVBrUURoOpIir403uz5MgWZC7` | Left |
| Mira_right.png | `1ZuVszgEkp4_Jsf_ZOop47NL8Y2bvKnpG` | Right |
| Mira_looking-down.png | `1Ob-tUeRbcfHgVHBcrGSFNAVA6wpqOzGv` | Looking down |
| Mira_looking-up.png | `1FP2a-ePkGS143c0NfFbfxVKnvnmQRiwa` | Looking up |

**Drive API Key:** `AIzaSy…U4rM`

**Image2Image strength:** `0.85` (maintains character likeness while allowing scene variation)

### 5.3 Outfit System

Each variant has a content-driven outfit direction defined in `OUTFIT_DIRECTION[day_num][variant_idx]`. Outfits are composed fresh every run from pools of pieces, bottoms, colors, and fabrics matched to the scene's vibe. Key parameters:
- `no_outfit: True` — for scenes where clothing isn't appropriate (e.g., bathtub)
- `vibe`, `style`, `colors`, `fabrics`, `silhouette`, `accessory`, `appeal`
- Two-outfit composition mode (alternates between options for variety)

### 5.4 Image Generation Process

```
POST /jobs/createTask
{
  "model": "flux-2/flex-image-to-image",
  "input": {
    "prompt": "...",
    "input_urls": [list of Mira ref URLs],
    "strength": 0.85,
    "aspect_ratio": "1:1",
    "resolution": "1K",
    "output_format": "jpg"
  }
}
→ Poll GET /jobs/recordInfo?taskId=TASK_ID
→ Download resultUrls[0]
→ Save to /tmp/bl-daily-post-vN.jpg
→ Copy to ~/.openclaw/workspace/tool-image-generation/
```

---

## 6. Social Media Posting

### 6.1 Posting Order & Method

| # | Platform | Method | Auth |
|---|---|---|---|
| 1 | Facebook | Graph API v22.0 — `/{page-id}/photos` | Page Access Token (fetched fresh via `me/accounts`) |
| 2 | Instagram | FB CDN URL approach — upload to FB → extract CDN URL → IG media container → publish | Page Access Token + IG Business Account ID |
| 3 | X/Twitter | OAuth 1.0a — v1.1 media upload + v2 tweet creation | Consumer Key/Secret + Access Token/Secret |
| 4 | LinkedIn | REST API — image upload → post creation | OAuth 2.0 with refresh token flow |

### 6.2 Instagram CDN Approach

```
1. Upload image to FB as published post → get CDN URL from images[0].source
2. Create IG media container: POST /{ig-account-id}/media?image_url=CDN_URL&caption=...
3. Wait 20s for processing
4. Publish: POST /{ig-account-id}/media_publish?creation_id=CONTAINER_ID
5. Delete temporary FB post
```

**Common IG failure:** "Media ID is not available" — this happens when the container isn't fully processed. Fix: wait longer (20-30s) before publishing. If the FB CDN URL is rejected ("Media download failed"), the photo must be uploaded as PUBLISHED (not unpublished) to get a stable CDN URL.

### 6.3 LinkedIn Token Management

- **Token:** Stored in `~/workspace/linkedin_access_token.txt`
- **Refresh Token:** Stored in `~/workspace/linkedin_refresh_token.txt`
- **Auto-refresh:** Script attempts refresh when access token is expired
- **App:** Client ID `775zrppl9vp2nh`, Company URN `urn:li:organization:135134648`
- **Re-auth needed:** When both tokens are expired, requires OAuth flow at LinkedIn Developer portal

---

## 7. Platform Connections & Credentials

### 7.1 Credential Location

All secrets are stored in:
- **TOOLS.md** — primary local reference at `~/.openclaw/workspace/TOOLS.md`
- **Script internals** — some API keys are hardcoded in the scripts (KIE_API_KEY, GDRIVE_API_KEY, FB tokens)
- **LinkedIn tokens** — file-based at `~/workspace/linkedin_*_token.txt`

### 7.2 Facebook / Meta

| Setting | Value |
|---|---|
| App ID | `998362096164262` |
| App Secret | `f99b8e544506eaaa56f7c66dde7177a3` |
| Page | Better Life AI Coaching (ID: `1124600237410474`) |
| Page URL | https://facebook.com/1124600237410474 |
| Instagram Business | @better_life_ai_coaching (ID: `17841420275969728`) |
| User Token (long-lived) | 60-day expiry, stored in TOOLS.md |
| Page Token | Fetched fresh via `me/accounts` on each run |
| Graph API Version | v22.0 |
| Ad Account | `act_1621691669958432` (BetterLife AI Coaching) |
| Business ID | `990093167247033` |

**Token refresh:** The `me/accounts` endpoint is called on every posting run to get a fresh page token. If the user token expires, a new one must be generated at the Facebook Developer portal.

### 7.3 X/Twitter

| Setting | Value |
|---|---|
| Handle | @BetterLifeatjl |
| User ID | `2069423281115910144` |
| App | BetterLife (OAuth 1.0a + OAuth 2.0) |
| Auth | Consumer Key/Secret + Access Token/Secret |
| API Level | Free tier — limited v1.1 (media upload, OAuth) + v2 |

### 7.4 LinkedIn

| Setting | Value |
|---|---|
| Company Page | BetterLife (ID: `135134648`) |
| URL | https://www.linkedin.com/company/135134648 |
| App ID | `775zrppl9vp2nh` |
| Auth | OAuth 2.0, 2-month token TTL |
| Scope | `w_organization_social` |

---

## 8. Content Calendar — 7-Day Theme Rotation

| Day | Theme | Platforms | Vibe |
|---|---|---|---|
| Monday | Motivation Monday — start the week strong | IG, FB | Intention, fresh start, discipline |
| Tuesday | Tip Tuesday — practical coaching advice | X, IG | Habits, 1% rule, practical wisdom |
| Wednesday | Wellness Wednesday — mental health focus | IG, FB, X | Mindfulness, check-in, self-compassion |
| Thursday | Transformation Thursday — growth stories | IG, FB | Progress, quiet wins, becoming |
| Friday | Feel-Good Friday — positive vibes | IG | Gratitude, celebration, connection |
| Saturday | Weekend Challenge — community engagement | IG | Comfort zone, adventure, expansion |
| Sunday | Sunday Reflection — weekly roundup | IG | Rest, gratitude, slow living |

---

## 9. Captions Format

### 9.1 Platform-Specific Rules

| Platform | Length | Style | Hashtags | CTA |
|---|---|---|---|---|
| Instagram | 150-250 chars | Emoji-heavy, visual-first, aspirational | 3-5 | Yes (👇) |
| Facebook | 800-1000 chars | Personal story, first-person narrative | 1-2 | Yes (👇) |
| X/Twitter | ≤280 chars | Punchy, concise, bold | 1 | Optional |
| LinkedIn | 1000-1600 chars | Thought leadership, research-backed, professional | 0 | Optional |

### 9.2 captions.md File Format

```markdown
# BetterLife Daily — YYYY-MM-DD (DayName)
## Theme: [theme name]

### V1 — [one-line scene description]
image: /absolute/path/to/v1.jpg

#### Instagram
[caption text]

#### Facebook
[caption text]

#### X
[caption text]

---
### V2 — [one-line scene description]
image: /absolute/path/to/v2.jpg
...
```

**This file is the single source of truth.** The posting script reads from it; no caption text ever touches `sys.argv`.

---

## 10. Image Output Directory

```
~/.openclaw/workspace/tool-image-generation/
```

All generated images are saved here with the naming convention:
```
betterlife-{theme-slug}-{YYYY-MM-DD}-v{N}.jpg
```

Example: `betterlife-wellness-wednesday--mental-health-focus-2026-07-29-v1.jpg`

---

## 11. Known Issues & Guardrails

### 11.1 Critical: MEDIA Directive Syntax

**Correct:** `MEDIA:/absolute/path/file.jpg` (colon after MEDIA, no space)
**Wrong:** `MEDIA /absolute/path/file.jpg` (space — images won't attach)

### 11.2 Critical: CLI Argument Caption Leak (FIXED 2026-07-29)

**Bug:** Old `bl-post-everywhere.py` used a single `CAPTION = sys.argv[2]` variable for all platforms. Passing `--ig "text"` set CAPTION to `--ig`, posting that literal string everywhere.

**Fix:** Script now supports `--captions-md FILE --variant N` mode where captions are read from a `.md` file, never from CLI arguments. The legacy `--ig/--fb/--x/--li` mode is preserved for backward compatibility but should be avoided for daily posting.

**Damage from this bug (2026-07-29):** All 4 platforms posted with `--ig` as caption. Required full cleanup: delete + repost on FB, IG, X, LI. Recent X tweets from 2026-07-27 also had `--platform` as caption — same root cause.

### 11.3 Critical: Page Post Auto-Boost

The Facebook page had ~50 posts with `promotion_status=inactive` — indicating automated post boosting was enabled. This caused unexpected charges.

**Protection in place:**
- Ad account spend cap set to **€0** (Graph API, confirmed `{"success": true}`)
- Revolut vendor payment blocked
- The auto-boost toggle itself is a **UI-only setting** in Facebook Page Settings — not accessible via Graph API. Must be manually verified at `facebook.com/1124600237410474/settings`

### 11.4 Instagram "Media ID is not available"

Common failure during IG publishing. Root cause: container not fully processed when publish is called. Fix: increase wait time to 20-30s. If FB CDN URL is rejected, use published (not unpublished) FB upload for CDN.

### 11.5 Token Expiry

- **FB User Token:** 60-day expiry. When expired, `me/accounts` calls fail. Regenerate at FB Developer portal.
- **LinkedIn Token:** 2-month TTL with refresh. When both expire, re-auth required.
- **X OAuth 1.0a:** No expiry (user context tokens don't expire).

### 11.6 X API Limitations

The X API key has **Free tier** access. v1.1 endpoints are limited to media upload and OAuth only — timeline reads, user search, and other v1.1 endpoints return 453 errors. Use v2 endpoints where possible.

---

## 12. Recovery Procedures

### 12.1 Cron Job Didn't Fire

```bash
# Check if cron is healthy
openclaw task list

# Force run the marketing cron
openclaw task run dc253ad9-13d5-4e84-b9ce-d17bbbaeb690 --run-mode force
```

### 12.2 Image Generation Failed

Check kie.ai dashboard for credits and error logs: https://kie.ai/logs
If credits depleted, add more at https://kie.ai/billing

### 12.3 Posting Failed

Check each platform individually:
- **FB:** Verify token via `curl -s "https://graph.facebook.com/v22.0/me/accounts?access_token=***"`
- **IG:** Check IG Business Account is connected to the FB page
- **X:** Verify OAuth credentials still work
- **LI:** Check if token needs refresh (delete `linkedin_access_token.txt` and re-auth)

### 12.4 Caption Bug (Wrong Text Posted)

```bash
# Delete bad posts
python3 ~/.openclaw/workspace/scripts/bl-delete-retry.py

# Repost with correct captions
python3 ~/.openclaw/workspace/scripts/bl-post-everywhere.py \
  --captions-md PATH --variant N
```

### 12.5 Instagram CDN Failure

If the FB CDN URL is rejected by Instagram:
1. Upload image to FB as a PUBLISHED post (not unpublished)
2. Extract the CDN URL from the post's images field
3. Use for IG media container
4. Delete the temporary FB post after IG publishes

---

## 13. Cost Summary

| Item | Cost | Status |
|---|---|---|
| kie.ai image generation | ~8-16 credits/variant (~€0.02-0.04 each) | Active |
| Facebook posting | Free (organic) | — |
| Instagram posting | Free (organic) | — |
| X/Twitter posting | Free (organic) | — |
| LinkedIn posting | Free (organic) | — |
| Instagram ad campaign | ~€8.99 (one-time, Board-approved) | Complete |
| Page post boosts | Previously draining ~€10-15/month | **Blocked** (€0 spend cap + Revolut block) |

---

## 14. Handoff Checklist

For a new person taking over this department, they need:

- [ ] Access to this MacBook (or equivalent OpenClaw runtime)
- [ ] Telegram access to receive the daily review messages
- [ ] kie.ai API key (dashboard: https://kie.ai)
- [ ] Facebook Developer app access (App ID `998362096164262`)
- [ ] X/Twitter Developer app access
- [ ] LinkedIn Developer app access (App ID `775zrppl9vp2nh`)
- [ ] Google Drive API access for Mira reference photos
- [ ] Workspace path: `~/.openclaw/workspace/`
- [ ] Scripts path: `~/.openclaw/workspace/scripts/`
- [ ] Image output: `~/.openclaw/workspace/tool-image-generation/`
- [ ] Verify Facebook auto-boost is OFF in Page Settings
- [ ] Verify ad account spend cap is €0
- [ ] Revolut vendor block for Facebook/Meta (optional, belt-and-suspenders)
