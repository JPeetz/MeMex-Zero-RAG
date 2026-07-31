# Helix — Architecture Reference (2026-06-12)

> Source: direct session notes. Immutable snapshot. See wiki/projects/helix.md for living wiki page.

## Identity

- **Product name:** Helix
- **Live URL:** https://vane.sytes.net
- **Origin:** Perplexica fork, fully rebased as commercial SaaS
- **Tagline:** "Think deeper." / "Search gives you links. Helix gives you insight."
- **Owner:** Joerg Peetz, Dublin, Ireland

## System Components

### 1. Nginx (reverse proxy, VPS 207.180.227.214)
- Port 443 TLS, cert via Let's Encrypt
- Config: `/etc/nginx/sites-enabled/vane`
- Routes: `/api/v1/` → :5001 (console), streaming paths → :3000 (no buffering), static pages from `/var/www/html/pages/`, all other → :3000

### 2. Next.js App (`vane-local:latest` Docker, :3000)
- Next.js 15 App Router, TypeScript
- Source: `/home/jpeetz/vane-src/`
- Runtime env: `/etc/helix.env` (chmod 600)
- Key files:
  - `src/auth.ts` — NextAuth v5 config (Google, GitHub, Supabase provisioning)
  - `src/middleware.ts` — hard gate: all routes redirect to /login if no session
  - `src/app/login/page.tsx` — Helix-branded login (Google + GitHub buttons)
  - `src/app/api/auth/[...nextauth]/route.ts` — NextAuth handler
  - `src/app/api/chat/route.ts` — auth check + credits gate + SearchAgent
  - `src/components/EmptyChat.tsx` — home screen (Helix mark, PP Editorial, mode chips)
  - `src/lib/config/index.ts` — isSetupComplete() bypassed when OPENAI_BASE_URL set

### 3. tier-proxy.py (Flask :5002, internal `172.22.0.1`)
- OpenRouter-compatible API proxy
- Location: `/var/lib/agentforge-console/tier-proxy.py`
- Resolves API key → account → tier → enforces model access by tier
- Internal Docker requests (172.22.x.x) get "starter" tier automatically
- Quota tracking via `usage_log` table (monthly rolling window)
- Circuit: Next.js → `OPENAI_BASE_URL=http://172.22.0.1:5002/api/v1`

### 4. agentforge-console (Flask :5001)
- Stripe webhooks, checkout sessions, billing portal
- Supabase writes for account/subscription management
- Admin dashboard: `/admin/`, `/dashboard.html`
- Env: `/etc/agentforge-console.env` (chmod 600, Stripe + Supabase keys)

### 5. SearXNG (Docker :8080)
- Privacy-respecting meta-search (Google/Bing/DDG/Brave)
- Next.js connects via `SEARXNG_API_URL=http://localhost:8080`

### 6. Supabase PostgreSQL
- Project ID: `psxtldxiqacrmvxdhrem`
- Tables: `accounts`, `api_keys`, `subscriptions`, `usage_log`, `credits`
- Key function: `decrement_credits_balance(p_account_id UUID)` — atomic, returns 0 rows when balance=0

## Auth Flow (NextAuth v5)

```
Browser → GET /any-route
  → middleware.ts: no session? → 302 /login
  → /login: Google/GitHub OAuth buttons
  → NextAuth /api/auth/callback/[provider]
  → jwt() callback:
      1. Find account by (auth_provider, auth_provider_id)
      2. Fallback: find by email (links OAuth to Stripe-created account)
      3. Not found: INSERT accounts + INSERT credits(balance=3, quota=3)
      token.accountId = account.id
  → Session contains: user.accountId
  → Subsequent requests: middleware sees session → passes through
```

## Credits Gate (chat/route.ts)

```
POST /api/chat
  → auth(): no session → 401
  → supabase.rpc('decrement_credits_balance', { p_account_id })
    → returns [] if balance=0 → 402 {message:"credits_exhausted"}
    → returns [{remaining: N}] if balance>0 → continue
  → SearchAgent.searchAsync() → tier-proxy → OpenRouter → stream response
```

## Subscription Tiers

| Tier | EUR/mo | Queries/mo | Key Models |
|------|--------|-----------|------------|
| Free | 0 | 3 lifetime | Owl Alpha, Kimi K2, Gemma 4 31B |
| Starter | 9 | 2,000 | + DeepSeek V4, Gemini 2.5 Flash, Llama 4 |
| Pro | 39 | 5,000 | + Claude Sonnet 4.6, GPT-4.1, Gemini 2.5 Pro |
| Scale | 149 | 25,000 | + Claude Opus 4.7, GPT-4.5 |

## Brand Identity

- **Font:** PP Editorial (otf) at weight 300, `/public/fonts/pp-ed-ul.otf`
- **Accent:** `#6366f1` (indigo-500)
- **Mark:** SVG double helix — two crossing bezier curves + center dot, `helix-pulse` CSS animation (5s ease-in-out)
- **Mode chips:** Speed / Balanced / Research (was: speed/balanced/quality)

## Supabase Schema (2026-06-12 state)

```sql
-- accounts
id UUID PRIMARY KEY
email TEXT UNIQUE NOT NULL
name TEXT
avatar_url TEXT
auth_provider TEXT        -- 'google' | 'github'
auth_provider_id TEXT     -- provider's user ID
created_at TIMESTAMPTZ

-- credits
account_id UUID REFERENCES accounts(id)
balance INT DEFAULT 3     -- remaining queries
quota INT DEFAULT 3       -- original allocation

-- subscriptions
account_id UUID
tier TEXT                 -- 'free'|'starter'|'pro'|'scale'
status TEXT               -- 'active'|'past_due'|'canceled'
stripe_subscription_id TEXT

-- usage_log
api_key_id UUID NULLABLE  -- NULL for session-based web users
account_id UUID
model TEXT
tokens_in INT
tokens_out INT
queries INT DEFAULT 1
cost_eur NUMERIC(10,6)
created_at TIMESTAMPTZ
```

## Key Gotchas

1. **Lazy Supabase init** — `createClient()` at module top-level throws during `next build`. Use getter function.
2. **yarn.lock freeze** — `--frozen-lockfile` Dockerfile. Update lockfile via `docker run node:24-slim yarn add <pkg> --ignore-scripts`.
3. **scraper depth patch** — `docker exec vane grep -rl '.slice(0,' /home/vane/.next/server/chunks/` re-patch after every rebuild (sets slice(0,3) → slice(0,6)).
4. **tier-proxy internal tier** — requests from 172.22.x.x get "starter" tier. API key auth overrides this.

## Docker Commands

```bash
# Build
cd /home/jpeetz/vane-src && docker build -t vane-local:latest .

# Run
docker stop vane && docker rm vane
docker run -d --name vane --restart unless-stopped \
  --network host --env-file /etc/helix.env \
  vane-local:latest

# Logs
docker logs -f vane

# Patch scraper depth after rebuild
docker exec vane bash -c "
  f=\$(grep -rl '.slice(0,' /home/vane/.next/server/chunks/ | head -1)
  sed -i 's/slice(0,3)/slice(0,6)/g' \"\$f\" && echo patched \"\$f\"
"
```

## Pending Work (as of 2026-06-12)

1. **OAuth credentials** — AUTH_GOOGLE_ID/SECRET, AUTH_GITHUB_ID/SECRET into /etc/helix.env
2. **Subscribed users credits** — on Stripe webhook `customer.subscription.created`: set credits.balance high (e.g. 999999) or skip decrement for accounts with active subscription
3. **Legal pages** — terms.html, privacy.html, gdpr.html still say AgentForge
4. **Billing portal wiring** — dashboard.html portal button needs authenticated session account_id
