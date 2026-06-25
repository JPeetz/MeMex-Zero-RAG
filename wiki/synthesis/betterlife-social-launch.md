---
title: BetterLife Social Media Launch — X/Twitter
type: synthesis
tags: ["betterlife", "social-media", "twitter", "launch", "x-api"]
created: 2026-06-25
author: marvin
---

# BetterLife Social Media Launch — X/Twitter

## Account
- **Handle:** @BetterLifeatjl
- **URL:** https://x.com/BetterLifeatjl
- **App:** BetterLife AI Coach (iOS)
- **App Store:** https://apps.apple.com/us/app/betterlife-ai-coach/id6773072166

## Launch Status: 🟡 Partial

### First Tweet — Posted ✅
- **Date:** 2026-06-25 09:00 IST
- **Tweet ID:** `2070054633888710760`
- **URL:** https://x.com/BetterLifeatjl/status/2070054633888710760

**Content:**
> AI coaching that adapts to YOUR culture, goals, and personality.
>
> Meet Aria (empathetic) and Aeron (assertive) — your personal AI coaches, 24/7.
>
> BetterLife on the App Store:
> https://apps.apple.com/us/app/betterlife-ai-coach/id6773072166
>
> #AICoaching #BetterLifeCare

### Reply Engagement — Blocked ❌
- **Planned targets:** @Theholisticpsyc, @NedraTawwab, @drmikeisraetel
- **Blocker:** X API Free tier does not support read endpoints (user lookup, timeline, search). Only post + media upload available.
- **Error:** `403 Forbidden — 453: You currently have access to a subset of X API V2 endpoints and limited v1.1 endpoints`

### Resolution Path
1. Apply for **Elevated** access at https://developer.x.com/en/portal/products/elevated (free, requires a short application describing the use case)
2. Once approved, re-run the reply engagement batch using `get_users_tweets` + `create_tweet` with `in_reply_to_tweet_id`
3. Elevated access provides: 2 app IDs, 500k posts/month (read), 100 posts/24h (write per app), 50 requests/15min (user auth)

## Strategy Notes
- **Tone:** Authentic, warm, professional — NOT salesy
- **Reply rule:** Add genuine value (insight, question, support). Never "check out our app."
- **Hashtags:** Max 1-2 per tweet per X best practice
- **Coaches:** Aria (empathetic tone), Aeron (assertive tone)
- **Content pillars:** AI coaching, mental wellness, personal growth, fitness/health
