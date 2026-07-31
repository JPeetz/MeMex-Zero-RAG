# Project: GallopGenius — Competition Research

> Full deconstruction of gallopgenius.com — competitor analysis and replication blueprint.
> **Status:** 📝 Research complete
> **Related:** [[Project-RaceIntel]], [[Research]]

---

## Owner Profile

| Field | Value |
|-------|-------|
| Name | Charles Edward Miller (DOB Jan 1994) |
| Company | Miller & Steel Limited (SC739568), Kinross, Scotland |
| Day job | IT Service Manager / InfoSec at Cinos (Perth, Scotland) |
| Background | British Army veteran |
| Stack | Lovable.dev → React/Vite → Cloudflare, Supabase, Stripe + RevenueCat |
| Only active venture | GallopGenius (launched Feb 2026) |

## Stack Analysis

| Component | Tech |
|-----------|------|
| Frontend | React/Vite via Lovable.dev |
| Hosting | Cloudflare |
| Database | Supabase (mmeseuzuvnbffgqcpcdk) |
| Payments | Stripe + RevenueCat |
| Mobile | Capacitor native apps |
| Domain | gallopgenius.com (registered Feb 2026) |

## Key Findings

- GallopGenius has **zero SEO** — no SSR pages, no sitemap
- Racing Post is ad-bloated and slow
- Gap: no SEO-native competitor exists
- Opportunity: "Cheltenham race card" keywords wide open for SSR pages

## Replication Blueprint

- Full document: 1,409 lines, ~52KB
- Location: `~/workspace/projects/gallopgenius-replication-blueprint.md`
- Covers: SQL schema (30+ tables), The Racing API ingestion pipeline, GG Score Edge Function, Stripe checkout, SEO/GEO strategy, iOS app plan, 30-day build timeline, cost estimate ($100-115/mo)
