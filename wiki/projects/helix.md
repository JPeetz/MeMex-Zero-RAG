---
title: Helix
type: project
status: active
created: 2026-06-12
updated: 2026-06-12
tags: [project, saas, nextjs, auth, stripe, supabase]
description: AI research engine at vane.sytes.net. Next.js 15 + SearXNG + OpenRouter. Subscription SaaS with NextAuth, Stripe billing, and 3-free-query teaser.
sources:
  - raw/helix/architecture-2026-06-12.md
---

# Helix

AI-powered research engine. European, privacy-first, subscription-funded. Live at [vane.sytes.net](https://vane.sytes.net).

**One-liner:** SearXNG (meta-search privacy proxy) + OpenRouter LLMs + Next.js streaming UI → cited AI answers.

## Architecture

```
User browser
  → Nginx :443 (TLS, vane.sytes.net)
    → Next.js :3000 (vane-local Docker)  ← main UI + API
    → Flask :5001 (agentforge-console)   ← Stripe webhooks, admin
    → /var/www/html/pages/               ← pricing, docs, about (static HTML)

Next.js
  → tier-proxy :5002 (172.22.0.1)        ← model gating, quota tracking
  → Supabase PostgreSQL                  ← accounts, credits, subscriptions

tier-proxy → OpenRouter API              ← 400+ LLMs
```

**Source:** [raw/helix/architecture-2026-06-12.md]

## Auth Flow

NextAuth v5 — Google + GitHub OAuth. Hard-gate middleware redirects all unauthenticated traffic to `/login`. JWT callback provisions Supabase account on first sign-in (find-by-provider → find-by-email → create-new + 3 free credits).

Chat API gate: `auth()` → `decrement_credits_balance(account_id)` RPC → 402 if balance=0.

Billing portal bridge: `GET /api/billing/portal` — NextAuth session → Supabase lookup of `stripe_customer_id` → Stripe REST API → redirect to portal. No API key needed for OAuth users.

## Business Model (2026-06-12 revised — economically viable)

**Reasoning:** At ~3k input + 1.2k output tokens/query:
- Claude Sonnet 4.6 costs ~$0.027/query, Opus ~$0.135/query.
- Opus + GPT-4.5 at old Scale quota (25,000) would cost ~$3,375/user/month — catastrophic.

**Tier redesign — Sonnet moved to Scale, Opus/GPT-4.5 removed:**

| Tier | Price | Models | Queries | Avg cost | Margin |
|------|-------|--------|---------|----------|--------|
| Free | €0 | Open-source free models | 3 lifetime | ~$0 | n/a |
| Starter | €9 | + DeepSeek, Gemini Flash, Llama 4 | 1,000/mo | ~$0.0013 | 87% |
| Pro | €39 | + GPT-4.1, Gemini 2.5 Pro | 2,500/mo | ~$0.014 | 19% |
| Scale | €149 | + Claude Sonnet 4.6 | 6,000/mo | ~$0.019 | 31% |

Stripe webhooks update credits on: checkout completion, plan change, monthly renewal (`invoice.payment_succeeded`), and cancellation (zeroes credits).

## Credits System

Two-layer system:
- **Web users (NextAuth):** Supabase `credits.balance` decremented by `decrement_credits_balance()` RPC per query. Monthly reset on `invoice.payment_succeeded` Stripe webhook.
- **API key users:** tier-proxy counts usage from `usage_log` table. Quota: starter=1000, pro=2500, scale=6000/month.
- **Internal web requests (172.22.x.x):** tier-proxy bypasses quota check entirely — credits system handles per-user limiting.

## Brand

PP Editorial serif (weight 300) · indigo `#6366f1` · double-helix SVG mark with CSS pulse · "Think deeper."

## Status (2026-06-12)

✅ Deployed and running  
✅ Stripe billing complete  
✅ NextAuth v5 wired  
✅ Credits gate on chat route  
✅ Full Helix rebrand (UI + all static pages including legal)  
✅ Monthly credit renewal webhook (invoice.payment_succeeded)  
✅ Subscription cancellation zeros credits  
✅ Plan upgrades update balance immediately  
✅ Billing portal bridge (`/api/billing/portal`) for OAuth users  
✅ Tier-proxy redesigned (Sonnet → Scale, Opus/GPT-4.5 removed)  
✅ Economically viable quotas: 1000 / 2500 / 6000  
⏳ OAuth credentials — user must create Google/GitHub apps  

## Key Patterns Learned

- **Lazy Supabase init in Next.js:** `createClient()` at module top-level fails during `next build`. Use a lazy getter. [[concepts/nextjs-build-env-vars]]
- **yarn.lock frozen builds:** Add new packages by running `yarn add` inside a Docker container of the same Node version. `--ignore-scripts` skips native compilation.
- **Atomic credit decrement:** PostgreSQL function `UPDATE WHERE balance > 0 RETURNING balance` — returns 0 rows when exhausted. No app-level race condition possible.
- **NextAuth v5 App Router:** `auth()` is a server-side function. `SessionProvider` only needed for client-side `useSession()`. Middleware uses `export default auth(handler)` pattern.
- **Next.js on Contabo VPS:** Hostname in `/etc/hosts` maps to 127.0.1.1, so standalone `node server.js` binds to 127.0.1.1 not 0.0.0.0. Fix: set `HOSTNAME=0.0.0.0` in Docker env file.
- **Billing portal without API key:** Add server-side Next.js route that queries Supabase for `stripe_customer_id`, then calls Stripe REST API directly. No Stripe SDK needed — plain fetch() POST to `api.stripe.com/v1/billing_portal/sessions`.
- **Supabase RPC typing without generated types:** Cast entire client as `any` — `(getSupabase() as any).rpc(...)`. Casting only args collapses return type to `never`.

## Related

- [raw/helix/architecture-2026-06-12.md](../raw/helix/architecture-2026-06-12.md) — full technical reference
- [[agentforge/projects/counter-project-blueprint]] — related product context
