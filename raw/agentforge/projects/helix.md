# Helix — AI Research Engine

[[Home]] > [[Projects Overview]] > **Helix**

- **Status:** Active | **Type:** Project | **Created:** 2026-06-12
- **URL:** [vane.sytes.net](https://vane.sytes.net)
- **Tech:** Next.js 15 + SearXNG + OpenRouter + Supabase + Stripe
- **License:** AGPL-3.0

## One-Liner

SearXNG (meta-search privacy proxy) + OpenRouter LLMs + Next.js streaming UI → cited AI answers.

## Architecture

```
User browser
  → Nginx :443 (TLS, vane.sytes.net)
    → Next.js :3000 (vane-local Docker)    ← main UI + API
    → Flask :5001 (agentforge-console)     ← Stripe webhooks, admin
    → /var/www/html/pages/                 ← pricing, docs, about (static HTML)

Next.js
  → tier-proxy :5002 (172.22.0.1)          ← model gating, quota tracking
  → Supabase PostgreSQL                    ← accounts, credits, subscriptions

tier-proxy → OpenRouter API                ← 400+ LLMs
```

## Auth Flow

NextAuth v5 — Google + GitHub OAuth. Hard-gate middleware redirects all unauthenticated traffic. JWT callback provisions Supabase account on first sign-in (find-by-provider → find-by-email → create-new + 3 free credits). Chat API gate: `auth()` → `decrement_credits_balance` RPC → 402 if balance = 0.

Billing portal bridge: `GET /api/billing/portal` — NextAuth session → Supabase lookup of `stripe_customer_id` → Stripe REST → redirect.

## Business Model

| Tier | Price | Models | Queries/mo | Margin |
|------|-------|--------|------------|--------|
| Free | €0 | Open-source free | 3 lifetime | n/a |
| Starter | €9 | DeepSeek, Gemini Flash, Llama 4 | 1,000 | 87% |
| Pro | €39 | GPT-4.1, Gemini 2.5 Pro | 2,500 | 19% |
| Scale | €149 | Claude Sonnet 4.6 | 6,000 | 31% |

## Key Design Choices

- **Sonnet moved to Scale** — was too expensive for lower tiers (~$0.027/query)
- **Opus/GPT-4.5 removed** — would cost ~$3,375/user/month at old quotas
- **Stripe webhooks** update credits on checkout, plan change, monthly renewal (`invoice.payment_succeeded`), cancellation (zeroes credits)
- **Privacy-first:** SearXNG proxy means user queries don't reach Google/Bing directly

## Related

- [[Infrastructure-Vane]] — Vane server infrastructure
- [[Research]] — Research platform analysis
- [[Board-Directives]] — Pricing decisions
- [Architecture detail](raw: `~/workspace/MeMex-Zero-RAG/raw/helix/architecture-2026-06-12.md`)