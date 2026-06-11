# Helix Stripe Full-Circle Fix + Supabase Migration — Design Spec

## Goal

Replace the SQLite backend in the Helix payment system with Supabase PostgreSQL, fix all identified billing bugs, add a Stripe billing portal, and ensure quota enforcement is correctly wired from Stripe through to the tier-proxy model router.

## Architecture

```
pricing.html / dashboard.html
        │
        ▼ POST /api/v1/checkout  •  POST /api/v1/portal
console.py  ─────────────────────────────────────► Stripe API
(Flask :5001)                                          │
        │                              webhook ◄─────── │
        ▼ supabase-py (service role)
  Supabase PostgreSQL (psxtldxiqacrmvxdhrem.supabase.co)
        ▲ supabase-py (service role)
        │  + TTLCache(maxsize=1000, ttl=300s) on resolve_account()
tier-proxy.py
(Flask :5002)
        │
        ▼ Bearer OPENROUTER_API_KEY (from env)
    OpenRouter API
```

Both services run as systemd units on the VPS (`207.180.227.214`). Both load secrets from a single env file: `/etc/agentforge-console.env` (chmod 600, owned by root).

## Environment File

**`/etc/agentforge-console.env`** (new file, never committed to git):
```
STRIPE_SECRET_KEY=sk_live_<from_console.py>
STRIPE_WEBHOOK_SECRET=whsec_<from_console.py>
SUPABASE_URL=https://psxtldxiqacrmvxdhrem.supabase.co
SUPABASE_SERVICE_KEY=<service_role_key>
OPENROUTER_API_KEY=<from_tier-proxy.py>
```

Both `agentforge-console.service` and `agentforge-tier-proxy.service` get:
```ini
EnvironmentFile=/etc/agentforge-console.env
```

## Supabase Schema

Run in Supabase SQL Editor before deploying the updated code.

```sql
-- 1. One row per registered user
CREATE TABLE IF NOT EXISTS accounts (
  id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email              TEXT UNIQUE NOT NULL,
  stripe_customer_id TEXT,
  created_at         TIMESTAMPTZ DEFAULT now()
);

-- 2. API keys issued on successful checkout
CREATE TABLE IF NOT EXISTS api_keys (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  account_id  UUID NOT NULL REFERENCES accounts(id),
  key_hash    TEXT UNIQUE NOT NULL,
  key_prefix  TEXT NOT NULL,
  name        TEXT,
  created_at  TIMESTAMPTZ DEFAULT now(),
  revoked     BOOLEAN DEFAULT false
);
CREATE INDEX IF NOT EXISTS idx_api_keys_hash ON api_keys(key_hash) WHERE revoked = false;

-- 3. Subscription state — updated by every Stripe lifecycle event
CREATE TABLE IF NOT EXISTS subscriptions (
  id                     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  account_id             UUID NOT NULL REFERENCES accounts(id),
  stripe_subscription_id TEXT UNIQUE,
  tier                   TEXT NOT NULL,   -- free | starter | pro | scale
  status                 TEXT DEFAULT 'active',  -- active | past_due | cancelled | paused
  current_period_start   TIMESTAMPTZ,
  current_period_end     TIMESTAMPTZ,
  cancel_at_period_end   BOOLEAN DEFAULT false,
  created_at             TIMESTAMPTZ DEFAULT now()
);

-- 4. Append-only usage ledger (one row per model request)
CREATE TABLE IF NOT EXISTS usage_log (
  id          BIGSERIAL PRIMARY KEY,
  api_key_id  UUID NOT NULL,
  account_id  UUID NOT NULL,
  model       TEXT,
  tokens_in   INT DEFAULT 0,
  tokens_out  INT DEFAULT 0,
  queries     INT DEFAULT 1,
  cost_eur    NUMERIC(10,6) DEFAULT 0,
  created_at  TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_usage_key_time     ON usage_log(api_key_id, created_at);
CREATE INDEX IF NOT EXISTS idx_usage_account_time ON usage_log(account_id, created_at);

-- 5. Credit balance per account (balance + quota + reset date)
CREATE TABLE IF NOT EXISTS credits (
  account_id  UUID PRIMARY KEY REFERENCES accounts(id),
  balance     INT DEFAULT 0,
  quota       INT DEFAULT 0,
  reset_at    TIMESTAMPTZ
);
```

**Row-Level Security:** Disable RLS on all five tables — both services use the service role key, which bypasses RLS regardless.

## Bug Fix Inventory

### console.py

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 1 | CRITICAL | `STRIPE_KEY` hardcoded in source | Read `STRIPE_SECRET_KEY` from env; crash at startup if missing |
| 2 | CRITICAL | `STRIPE_WEBHOOK_SECRET` hardcoded | Read `STRIPE_WEBHOOK_SECRET` from env; crash at startup if missing |
| 3 | HIGH | `stripe.Customer.retrieve(account["stripe_customer_id"])` crashes when `stripe_customer_id` is NULL | Check: if NULL → create new customer; if set → retrieve existing |
| 4 | HIGH | Missing `customer.subscription.updated` webhook | Add handler: upsert tier, status, current_period_start/end, cancel_at_period_end |
| 5 | HIGH | Missing `invoice.payment_failed` webhook | Add handler: set subscription status to `past_due` |
| 6 | HIGH | `QUOTA["starter"] = 500` (plan card says 2,000) | Fix to `2000` |
| 7 | HIGH | No billing portal | Add `POST /api/v1/portal`: creates Stripe billing portal session, returns `{ url }` |
| 8 | HIGH | SQLite throughout | Replace all `sqlite3` calls with `supabase-py` service-role client |
| 9 | MINOR | `balance - 1` race condition in usage decrement | Credits table updated by tier-proxy log_usage, not console.py; remove from console |

### tier-proxy.py

| # | Severity | Issue | Fix |
|---|----------|-------|-----|
| 1 | CRITICAL | `OPENROUTER_API_KEY` reads from env with `"sk-or-v1-placeholder"` default (silently broken) | Read from env, raise `RuntimeError` at startup if missing |
| 2 | HIGH | SQLite throughout | Replace with Supabase service-role client |
| 3 | MEDIUM | No cache on `resolve_account()` — 2 SQLite calls per request | Add `cachetools.TTLCache(maxsize=1000, ttl=300)` keyed on key_hash |
| 4 | MEDIUM | `TIER_QUOTA["starter"] = 2000` already correct but `check_quota` uses usage_log not credits table | Keep usage_log approach (more accurate); ensure counts match |

### pricing.html

| # | Issue | Fix |
|---|-------|-----|
| 1 | JS `_planLabels` shows `pro:'€29/mo'` (should be €39) and `scale:'€99/mo'` (should be €149) | Update both values |

### dashboard.html

| # | Addition | Detail |
|---|----------|--------|
| 1 | No billing portal link | Add "Manage Subscription" button → `POST /api/v1/portal` (with current API key) → `window.location.href = data.url` |
| 2 | No subscription status shown | Show tier badge, status (active/past_due), period end date in account panel |

## Webhook Events

| Event | Handler | Action |
|-------|---------|--------|
| `checkout.session.completed` | Existing (fix) | Create api_key row, subscription row, credits row in Supabase |
| `customer.subscription.updated` | **New** | Upsert subscription: tier, status, period dates, cancel_at_period_end |
| `customer.subscription.deleted` | Existing (fix) | Set subscription status to `cancelled` |
| `invoice.payment_failed` | **New** | Set subscription status to `past_due` |

## TTL Cache Behaviour

`resolve_account()` in tier-proxy caches by `sha256(api_key)` for 300 seconds.

**Cache invalidation:** The `customer.subscription.updated` and `customer.subscription.deleted` webhook handlers in console.py call a shared `invalidate_tier_cache(account_id)` function that clears the cache entry. Since both processes run on the same host, this is done via a lightweight HTTP call from console.py to tier-proxy's `POST /internal/invalidate-cache` endpoint (bound to `127.0.0.1` only, no external exposure).

**Fallback:** If cache invalidation call fails, the stale cache expires naturally within 5 minutes.

## File Map

| File | Action |
|------|--------|
| `/etc/agentforge-console.env` | Create |
| `/etc/systemd/system/agentforge-console.service` | Modify: add `EnvironmentFile=` |
| `/etc/systemd/system/agentforge-tier-proxy.service` | Modify: add `EnvironmentFile=` |
| `/var/lib/agentforge-console/console.py` | Rewrite |
| `/var/lib/agentforge-console/tier-proxy.py` | Modify |
| `/var/www/html/pages/pricing.html` | Modify: 2 JS string values |
| `/var/www/html/pages/dashboard.html` | Modify: add portal button + subscription status |

## Security Notes

- `/etc/agentforge-console.env` must be `chmod 600` and owned by the user running the systemd services
- The `sb_secret_...` service role key bypasses all RLS — never expose it in frontend code or logs
- Live Stripe key (`sk_live_...`) must never appear in source files — the migration removes it from `console.py`
- `POST /internal/invalidate-cache` binds only to `127.0.0.1` and has no authentication (internal only)

## Quota Constants (post-fix)

| Tier | Queries/month | Monthly price |
|------|--------------|---------------|
| free | 100 | €0 |
| starter | 2,000 | €9 |
| pro | 5,000 | €39 |
| scale | 25,000 | €149 |

These values must be consistent between `console.py` `QUOTA` dict, `tier-proxy.py` `TIER_QUOTA` dict, pricing.html plan cards, and the `credits.quota` column written at checkout.
