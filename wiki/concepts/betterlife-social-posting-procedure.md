---
title: BetterLife Social Media Posting Procedure
type: concept
tags: []
created: 2026-06-29
author: marvin
---

# BetterLife Social Media Posting Procedure

**Owner:** Marketing Department | **Runtime:** Local MacBook | **Last verified:** 2026-06-29

## ⛔ HARD RULE
- **Post from local MacBook only.** Every API call — Meta Graph, X OAuth — goes direct from here.
- **Never touch Vane.** Never touch 207.180.227.214. Never touch betterlife.care FTP.
- **Credentials:** All in `~/workspace/TOOLS.md` — never hardcode in scripts.

---

## Quick Reference: Single Image → All Platforms

```
1. FB: POST /{page_id}/photos (multipart file upload)
2. Get FB CDN URL from photo response
3. IG: Use FB CDN URL → POST /{ig_id}/media → POST /{ig_id}/media_publish
4. X: OAuth 1.0a → media/upload → create tweet
```

No infra needed. No hosting. No SCP.

---

## Step 1: Fetch Fresh Page Token

The page token in TOOLS.md may be stale. Always fetch fresh via me/accounts.

## Step 2: Facebook Post

FB supports direct file upload via multipart form to `/{page_id}/photos`.

## Step 3: Get FB CDN URL

Use the photo ID to get CDN image URL from `fbcdn.net` — publicly accessible, no auth needed.

## Step 4: Instagram Post

IG Content Publishing API requires public HTTPS image URL. Use FB CDN URL:
- Create media container: `POST /{ig_id}/media`
- Publish: `POST /{ig_id}/media_publish`

## Step 5: X/Twitter Post

OAuth 1.0a required. Upload media to `upload.twitter.com/1.1/media/upload.json`, then create tweet at `api.twitter.com/2/tweets`.

Reference implementation: `scripts/x-post.py`

## Platform Accounts

| Platform | ID | Username |
|----------|-----|----------|
| FB Page | 1124600237410474 | Better Life AI Coaching |
| Instagram | 17841420275969728 | @better_life_ai_coaching |
| X/Twitter | — | @BetterLifeatjl |

## Posting Schedule

| Day | Theme | Platforms |
|-----|-------|-----------|
| Mon | Motivation Monday | IG, FB |
| Tue | Tip Tuesday | X, IG |
| Wed | Wellness Wednesday | IG, FB, X |
| Thu | Transformation Thursday | IG, FB |
| Fri | Feel-Good Friday | IG |
| Sat | Weekend Challenge | IG |
| Sun | Sunday Reflection | IG |
