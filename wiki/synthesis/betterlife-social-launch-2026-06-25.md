---
title: BetterLife Social Media Launch — 2026-06-25
type: synthesis
tags: ["betterlife", "social-media", "launch", "instagram", "facebook", "2026-06"]
created: 2026-06-25
author: marvin
---

# BetterLife Social Media Launch — 2026-06-25

## Status: LIVE

Instagram Business Account connected to Facebook Page. First posts published on both platforms. Daily automated posting engine deployed.

## Accounts Active

| Platform | Handle/Page | Status |
|---|---|---|
| Instagram | @better_life_ai_coaching (ID: 17841420275969728) | ✅ Live, posting enabled |
| Facebook | Better Life AI Coaching (ID: 1124600237410474) | ✅ Live, posting enabled |
| X/Twitter | @BetterLifeatjl | ✅ Live, post-only (Elevated access pending) |
| Threads | — | ⏸️ Deferred |

## First Posts

- **Instagram:** June 25 — Intro post with AI-generated image (1024×1024), wellness brand aesthetic
- **Facebook:** June 25 — Intro post with App Store link
- **X/Twitter:** June 25 — Intro tweet + batch (scheduled via cron)

## Daily Posting Engine

- **Cron job:** Daily at 8:00 AM Dublin (Europe/Dublin)
- **Schedule:** Mon IG+FB | Tue X+IG | Wed IG+FB+X | Thu IG+FB | Fri-Sun IG only
- **Content themes:** Motivation Mon, Tip Tue, Wellness Wed, Growth Thu, Feel-Good Fri, Challenge Sat, Reflection Sun
- **Hashtags:** #AICoaching #BetterLifeCare #MentalWellness (+ niche per platform)
- **Image generation:** Daily fresh AI images via Google Imagen

## Image Hosting

- **Server:** vane.sytes.net (207.180.227.214)
- **Path:** `/var/www/html/social/`
- **URL pattern:** `https://vane.sytes.net/social/betterlife-*-YYYYMMDD.jpg`
- **Nginx:** Location `/social/` block added to vane config

## Image Catalog

- **250+ assets** cataloged across ~workspace/artifacts/social/betterlife-image-catalog.md
- Sources: Website theme, App Store screenshots, iOS simulator, social media kit, Xcode archives
- No design source files (Figma/Sketch) found — all assets are rendered PNG/JPG

## Token Status

| Token | Type | Expiry |
|---|---|---|
| Facebook User Token | Long-lived (60-day) | ~Aug 24, 2026 |
| Facebook Page Token | Rotates per query | Refresh via me/accounts |

## Reference

- Social media research: `synthesis/betterlife-social-media-research`
- Image catalog: `~/workspace/artifacts/social/betterlife-image-catalog.md`
- Daily script: `~/workspace/scripts/betterlife-social-daily.py`
- Cron job: BetterLife Daily Social Posting (1b9e5b2e-b535-4bc4-882e-c66789b26f13)
