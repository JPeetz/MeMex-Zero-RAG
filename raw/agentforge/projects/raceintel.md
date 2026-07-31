# Project: RaceIntel

> Horse racing prediction app — AI-powered race analysis and tips.
> **Status:** 🟡 Stalled (needs Stripe key + Vercel redeploy)
> **Related:** [[Project-GallopGenius]], [[Infrastructure]]

---

## Current State

| Component | Status |
|-----------|--------|
| GitHub repo | ✅ JPeetz/raceintel — 17 routes, zero TS errors |
| Supabase DB | ✅ 19 tables, ~514K rows |
| Historical data | ✅ 493,936 horses, 21,258 trainers, 20,658 jockeys, 730 racecourses |
| Recent racecards | ✅ 137 races, 1,277 runners (2026-05-26 to 2026-05-28) |
| GDPR pages | ✅ Privacy, Terms, Responsible Gambling |
| Sitemap + robots.txt | ✅ Done |
| GG Score engine | ✅ gg_score.py ready |
| Ingestion pipeline | ✅ ingest.py ready |
| Validation tracker | ✅ validate.py ready |
| Stripe secret key | 🔴 MISSING — needs sk_live_ from dashboard |
| Vercel deploy | 🔴 STUCK — stale build, needs manual redeploy |
| The Racing API | 🔴 BROKEN — 404 on all endpoints |

## Data Status

- **Historical:** Kaggle dataset (38 years) imported
- **Live/upcoming races:** NOT available — The Racing API returns 404 on all endpoints
- **Pivot:** Using Kaggle dataset for GG Score training instead of live API

## Blockers

1. **Stripe:** `sk_live_51SJiGOIWMCL4q0q2...` secret key not found on disk. Need from Stripe dashboard.
2. **Vercel:** Dashboard shows stale build `a9cc813` despite latest code at `36bf48e`. Git state is correct.
3. **Racing API:** All endpoints 404. May need paid tier or alternative data source.

## Next Steps

1. 🔐 Joerg retrieves Stripe `sk_live_` key from dashboard
2. 🚀 Manual redeploy in Vercel dashboard
3. 🏇 Fix Racing API or find alternative
4. After blocks resolved: `python3 scripts/gg_score.py` → 30-day validation phase
