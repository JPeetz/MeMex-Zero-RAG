# Helix Stripe Full-Circle Fix + Supabase Migration — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the SQLite backend with Supabase PostgreSQL, fix all billing bugs (hardcoded credentials, NULL customer crash, missing webhook events, wrong quotas, price labels), add billing portal, and wire usage tracking end-to-end.

**Architecture:** `console.py` (Flask :5001) and `tier-proxy.py` (Flask :5002) both use a shared Supabase project via `supabase-py`. Secrets move from source to `/etc/agentforge-console.env` loaded via systemd `EnvironmentFile`. The tier-proxy caches account resolution for 5 minutes via `cachetools.TTLCache`; cache is invalidated by console.py webhook handlers via an internal HTTP call to the proxy.

**Tech Stack:** Python 3, Flask, Gunicorn, `supabase-py` v2, `cachetools`, Stripe Python SDK, Supabase PostgreSQL, systemd on Ubuntu VPS (`207.180.227.214`).

---

## File Map

| File | Action |
|------|--------|
| `/etc/agentforge-console.env` | Create — all secrets |
| `/etc/systemd/system/agentforge-console.service` | Modify — add EnvironmentFile |
| `/etc/systemd/system/agentforge-tier-proxy.service` | Modify — remove inline key, add EnvironmentFile |
| `/var/lib/agentforge-console/console.py` | Full rewrite |
| `/var/lib/agentforge-console/tier-proxy.py` | Full rewrite |
| `/var/www/html/pages/pricing.html` | Modify — 2 JS strings |
| `/var/www/html/pages/dashboard.html` | Modify — portal button + correct limits |

---

### Task 1: Run Supabase SQL Migration

Create all five tables in the Supabase project. No code changes — SQL only.

**Files:** None (run in Supabase dashboard)

- [ ] **Step 1: Open the Supabase SQL Editor**

Navigate to: `https://supabase.com/dashboard/project/psxtldxiqacrmvxdhrem/sql/new`

- [ ] **Step 2: Paste and run this SQL**

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
  tier                   TEXT NOT NULL,
  status                 TEXT DEFAULT 'active',
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

-- 5. Credit balance per account
CREATE TABLE IF NOT EXISTS credits (
  account_id  UUID PRIMARY KEY REFERENCES accounts(id),
  balance     INT DEFAULT 0,
  quota       INT DEFAULT 0,
  reset_at    TIMESTAMPTZ
);
```

Click **Run**. Expected: "Success. No rows returned."

- [ ] **Step 3: Verify all 5 tables exist**

In the Supabase Table Editor, confirm these tables appear: `accounts`, `api_keys`, `subscriptions`, `usage_log`, `credits`.

---

### Task 2: Create Environment File and Update Systemd

Move all secrets out of source files into a protected env file, then update both systemd units to load it.

**Files:**
- Create: `/etc/agentforge-console.env`
- Modify: `/etc/systemd/system/agentforge-console.service`
- Modify: `/etc/systemd/system/agentforge-tier-proxy.service`

- [ ] **Step 1: SSH into the server**

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214
```

- [ ] **Step 2: Create the env file as root**

```bash
sudo tee /etc/agentforge-console.env > /dev/null << 'EOF'
STRIPE_SECRET_KEY=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
STRIPE_WEBHOOK_SECRET=whsec_qCFGsNzQKZM5D8hqnezFBw3wZ4zS4I2e
SUPABASE_URL=https://psxtldxiqacrmvxdhrem.supabase.co
SUPABASE_SERVICE_KEY=sb_secret_qX3TIuotgyKiQSCivokDCg__UHO4Lc-
OPENROUTER_API_KEY=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
EOF
```

- [ ] **Step 3: Lock down permissions**

```bash
sudo chmod 600 /etc/agentforge-console.env
sudo chown root:root /etc/agentforge-console.env
```

Verify:
```bash
sudo ls -la /etc/agentforge-console.env
```
Expected: `-rw------- 1 root root ...`

- [ ] **Step 4: Update agentforge-console.service**

```bash
sudo tee /etc/systemd/system/agentforge-console.service > /dev/null << 'EOF'
[Unit]
Description=AgentForge Research Console Backend
After=network.target

[Service]
User=jpeetz
WorkingDirectory=/var/lib/agentforge-console
EnvironmentFile=/etc/agentforge-console.env
ExecStart=/usr/local/bin/gunicorn --workers 2 --bind 127.0.0.1:5001 console:app
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF
```

- [ ] **Step 5: Update agentforge-tier-proxy.service (remove inline key, add EnvironmentFile)**

```bash
sudo tee /etc/systemd/system/agentforge-tier-proxy.service > /dev/null << 'EOF'
[Unit]
Description=AgentForge Tier Proxy (OpenRouter)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=jpeetz
WorkingDirectory=/var/lib/agentforge-console
EnvironmentFile=/etc/agentforge-console.env
ExecStart=/usr/local/bin/gunicorn --workers 2 --bind 172.22.0.1:5002 --access-logfile - --error-logfile - --timeout 300 --capture-output tier-proxy:app
Restart=always
RestartSec=3
StandardOutput=journal
StandardError=journal
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF
```

- [ ] **Step 6: Reload systemd daemon**

```bash
sudo systemctl daemon-reload
```

Expected: no output (silent success).

---

### Task 3: Install Python Dependencies

- [ ] **Step 1: Install supabase-py and cachetools**

```bash
sudo /usr/bin/pip3 install supabase cachetools || pip3 install supabase cachetools
```

- [ ] **Step 2: Verify imports**

```bash
python3 -c "from supabase import create_client; from cachetools import TTLCache; print('OK')"
```

Expected: `OK`

---

### Task 4: Rewrite console.py

Full replacement. Fixes: Supabase, hardcoded keys removed, NULL customer crash, missing webhooks, quota=2000, billing portal.

**Files:**
- Modify: `/var/lib/agentforge-console/console.py`

- [ ] **Step 1: Back up the existing file**

```bash
cp /var/lib/agentforge-console/console.py /var/lib/agentforge-console/console.py.bak2
```

- [ ] **Step 2: Write the new console.py**

```bash
cat > /var/lib/agentforge-console/console.py << 'PYEOF'
#!/usr/bin/env python3
"""
AgentForge Research — Developer Console Backend v2
Flask API for Stripe Checkout, webhooks, billing portal, API key management, and usage.
Deploy: systemd service on VPS, port 5001, NGINX proxy_pass /api/v1/*
Secrets: /etc/agentforge-console.env loaded via systemd EnvironmentFile
"""
import hashlib, json, os, secrets, uuid
from datetime import datetime, timezone
from functools import wraps
from flask import Flask, request, jsonify
import stripe
from supabase import create_client

# === CONFIG (crash at startup if any required var is missing) ===
STRIPE_SECRET_KEY     = os.environ["STRIPE_SECRET_KEY"]
STRIPE_WEBHOOK_SECRET = os.environ["STRIPE_WEBHOOK_SECRET"]
SUPABASE_URL          = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_KEY  = os.environ["SUPABASE_SERVICE_KEY"]

stripe.api_key = STRIPE_SECRET_KEY
app = Flask(__name__)
db = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

PRICES = {
    "starter": "price_1TfcWIIWMCL4q0q2J8Jq9IzY",
    "pro":     "price_1TfcWJIWMCL4q0q2ahdGGjOJ",
    "scale":   "price_1TfcWKIWMCL4q0q20iQVl75X",
}
QUOTA = {"starter": 2000, "pro": 5000, "scale": 25000}
TIER_PROXY_URL = "http://172.22.0.1:5002"

# === AUTH MIDDLEWARE ===
def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get("Authorization", "").replace("Bearer ", "").strip()
        if not key:
            return jsonify({"error": "Missing API key"}), 401
        h = hashlib.sha256(key.encode()).hexdigest()
        result = db.table("api_keys").select("id, account_id, key_prefix, created_at").eq("key_hash", h).eq("revoked", False).maybe_single().execute()
        if not result.data:
            return jsonify({"error": "Invalid or revoked API key"}), 401
        request.api_key = result.data
        return f(*args, **kwargs)
    return decorated

# === CHECKOUT ===
@app.route("/api/v1/checkout", methods=["POST"])
def create_checkout():
    data = request.json or {}
    email = (data.get("email") or "").strip().lower()
    tier = data.get("tier", "starter")
    if not email or "@" not in email:
        return jsonify({"error": "A valid email address is required."}), 400
    price_id = PRICES.get(tier)
    if not price_id:
        return jsonify({"error": f"Invalid tier: {tier}. Choose starter, pro, or scale."}), 400

    # Look up existing account
    acct_res = db.table("accounts").select("id, stripe_customer_id").eq("email", email).maybe_single().execute()
    account = acct_res.data

    if not account:
        # New account: create Stripe customer and store
        customer = stripe.Customer.create(email=email)
        account_id = str(uuid.uuid4())
        db.table("accounts").insert({
            "id": account_id,
            "email": email,
            "stripe_customer_id": customer.id,
        }).execute()
        customer_id = customer.id
    else:
        account_id = account["id"]
        if account["stripe_customer_id"]:
            customer_id = account["stripe_customer_id"]
        else:
            # Account exists but Stripe customer was never created (edge case)
            customer = stripe.Customer.create(email=email)
            db.table("accounts").update({"stripe_customer_id": customer.id}).eq("id", account_id).execute()
            customer_id = customer.id

    session = stripe.checkout.Session.create(
        customer=customer_id,
        mode="subscription",
        line_items=[{"price": price_id, "quantity": 1}],
        success_url="https://vane.sytes.net/dashboard?session={CHECKOUT_SESSION_ID}",
        cancel_url="https://vane.sytes.net/pricing",
        metadata={"account_id": account_id, "tier": tier},
        allow_promotion_codes=True,
    )
    return jsonify({"url": session.url})

# === STRIPE WEBHOOK ===
@app.route("/api/v1/webhook", methods=["POST"])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig = request.headers.get("Stripe-Signature")
    try:
        event = stripe.Webhook.construct_event(payload, sig, STRIPE_WEBHOOK_SECRET)
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        return jsonify({"error": str(e)}), 400

    etype = event["type"]

    if etype == "checkout.session.completed":
        session = event["data"]["object"]
        account_id = (session.get("metadata") or {}).get("account_id")
        tier = (session.get("metadata") or {}).get("tier", "starter")
        sub_id = session.get("subscription")
        if account_id and sub_id:
            sub = stripe.Subscription.retrieve(sub_id)
            key = "afr_" + secrets.token_urlsafe(32)
            key_hash = hashlib.sha256(key.encode()).hexdigest()
            db.table("api_keys").insert({
                "id": str(uuid.uuid4()),
                "account_id": account_id,
                "key_hash": key_hash,
                "key_prefix": key[:12],
                "name": "Default",
            }).execute()
            db.table("subscriptions").upsert({
                "id": str(uuid.uuid4()),
                "account_id": account_id,
                "stripe_subscription_id": sub_id,
                "tier": tier,
                "status": "active",
                "current_period_start": _ts(sub["current_period_start"]),
                "current_period_end":   _ts(sub["current_period_end"]),
                "cancel_at_period_end": sub.get("cancel_at_period_end", False),
            }, on_conflict="stripe_subscription_id").execute()
            db.table("credits").upsert({
                "account_id": account_id,
                "balance": QUOTA.get(tier, 2000),
                "quota":   QUOTA.get(tier, 2000),
            }).execute()

    elif etype == "customer.subscription.updated":
        sub = event["data"]["object"]
        sub_id = sub["id"]
        items = (sub.get("items") or {}).get("data") or []
        price_id = items[0]["price"]["id"] if items else None
        tier = next((t for t, p in PRICES.items() if p == price_id), None)
        update = {
            "status": sub.get("status", "active"),
            "current_period_start": _ts(sub["current_period_start"]),
            "current_period_end":   _ts(sub["current_period_end"]),
            "cancel_at_period_end": sub.get("cancel_at_period_end", False),
        }
        if tier:
            update["tier"] = tier
        db.table("subscriptions").update(update).eq("stripe_subscription_id", sub_id).execute()
        if tier:
            acct_res = db.table("subscriptions").select("account_id").eq("stripe_subscription_id", sub_id).maybe_single().execute()
            if acct_res.data:
                db.table("credits").update({"quota": QUOTA.get(tier, 2000)}).eq("account_id", acct_res.data["account_id"]).execute()
        _invalidate_proxy_cache(sub_id)

    elif etype == "customer.subscription.deleted":
        sub = event["data"]["object"]
        db.table("subscriptions").update({"status": "cancelled"}).eq("stripe_subscription_id", sub["id"]).execute()
        _invalidate_proxy_cache(sub["id"])

    elif etype == "invoice.payment_failed":
        invoice = event["data"]["object"]
        sub_id = invoice.get("subscription")
        if sub_id:
            db.table("subscriptions").update({"status": "past_due"}).eq("stripe_subscription_id", sub_id).execute()

    return jsonify({"status": "ok"})

def _ts(unix_ts):
    return datetime.fromtimestamp(unix_ts, tz=timezone.utc).isoformat()

def _invalidate_proxy_cache(stripe_sub_id):
    try:
        res = db.table("subscriptions").select("account_id").eq("stripe_subscription_id", stripe_sub_id).maybe_single().execute()
        if res.data:
            import requests as req
            req.post(
                f"{TIER_PROXY_URL}/internal/invalidate-cache",
                json={"account_id": res.data["account_id"]},
                timeout=2,
            )
    except Exception:
        pass  # Cache expires naturally in 5 min

# === BILLING PORTAL ===
@app.route("/api/v1/portal", methods=["POST"])
@require_api_key
def billing_portal():
    account_id = request.api_key["account_id"]
    res = db.table("accounts").select("stripe_customer_id").eq("id", account_id).maybe_single().execute()
    if not res.data or not res.data.get("stripe_customer_id"):
        return jsonify({"error": "No Stripe customer found for this account."}), 404
    portal = stripe.billing_portal.Session.create(
        customer=res.data["stripe_customer_id"],
        return_url="https://vane.sytes.net/dashboard",
    )
    return jsonify({"url": portal.url})

# === DASHBOARD ===
@app.route("/api/v1/dashboard", methods=["GET"])
@require_api_key
def dashboard():
    key = request.api_key
    account_id = key["account_id"]

    acct_res = db.table("accounts").select("email, created_at").eq("id", account_id).maybe_single().execute()
    account = acct_res.data or {}

    sub_res = db.table("subscriptions").select("tier, status, current_period_end, cancel_at_period_end").eq("account_id", account_id).in_("status", ["active", "past_due"]).order("created_at", desc=True).limit(1).execute()
    sub = sub_res.data[0] if sub_res.data else None

    creds_res = db.table("credits").select("balance, quota").eq("account_id", account_id).maybe_single().execute()
    creds = creds_res.data or {}

    month_start = datetime.now(timezone.utc).replace(day=1, hour=0, minute=0, second=0, microsecond=0).isoformat()
    usage_res = db.table("usage_log").select("queries, tokens_in, tokens_out, cost_eur").eq("account_id", account_id).gte("created_at", month_start).execute()
    rows = usage_res.data or []
    total_queries    = sum(r.get("queries", 0) for r in rows)
    total_tokens_in  = sum(r.get("tokens_in", 0) for r in rows)
    total_tokens_out = sum(r.get("tokens_out", 0) for r in rows)
    total_cost       = sum(float(r.get("cost_eur", 0)) for r in rows)

    return jsonify({
        "account": {"email": account.get("email"), "created": account.get("created_at")},
        "subscription": sub,
        "credits_remaining": creds.get("balance", 0),
        "credits_quota": creds.get("quota", 0),
        "api_key": {"prefix": key["key_prefix"], "created": key["created_at"]},
        "usage_this_month": {
            "total_queries": total_queries,
            "total_tokens_in": total_tokens_in,
            "total_tokens_out": total_tokens_out,
            "total_cost_eur": round(total_cost, 4),
        },
    })

# === HEALTH ===
@app.route("/api/v1/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "version": "2.0.0"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)
PYEOF
```

- [ ] **Step 3: Syntax-check the new file**

```bash
python3 -m py_compile /var/lib/agentforge-console/console.py && echo "Syntax OK"
```

Expected: `Syntax OK`

- [ ] **Step 4: Commit the change on the server**

```bash
cd /home/jpeetz/vane-src && git add /var/lib/agentforge-console/console.py 2>/dev/null || true
# console.py lives outside vane-src — commit in its own dir if tracked
cd /var/lib/agentforge-console && git init 2>/dev/null || true && git add console.py && git diff --cached --stat
```

> Note: If `/var/lib/agentforge-console` is not a git repo, skip the commit step — the backup (`console.py.bak2`) is the rollback.

---

### Task 5: Rewrite tier-proxy.py

Full replacement. Fixes: Supabase + TTL cache for `resolve_account`, `account_id` added to `log_usage`, `OPENROUTER_API_KEY` from env (hard crash if missing), `/internal/invalidate-cache` endpoint.

**Files:**
- Modify: `/var/lib/agentforge-console/tier-proxy.py`

- [ ] **Step 1: Back up the existing file**

```bash
cp /var/lib/agentforge-console/tier-proxy.py /var/lib/agentforge-console/tier-proxy.py.bak5
```

- [ ] **Step 2: Write the new tier-proxy.py**

```bash
cat > /var/lib/agentforge-console/tier-proxy.py << 'PYEOF'
#!/usr/bin/env python3
"""
AgentForge Research — Tiered Model Proxy v5
Progressive model access + quota enforcement + usage logging via Supabase.
Secrets: /etc/agentforge-console.env loaded via systemd EnvironmentFile
"""
import json, hashlib, os, threading
from datetime import datetime
from flask import Flask, request, Response, jsonify
from supabase import create_client
from cachetools import TTLCache
import requests as req_lib

app = Flask(__name__)
OPENROUTER_BASE = "https://openrouter.ai/api/v1"

# === CONFIG (crash at startup if missing) ===
OPENROUTER_API_KEY = os.environ["OPENROUTER_API_KEY"]
SUPABASE_URL       = os.environ["SUPABASE_URL"]
SUPABASE_SERVICE_KEY = os.environ["SUPABASE_SERVICE_KEY"]

db = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# ── Tier Configuration ──────────────────────────────────────────────
TIER_MODELS = {
    "free": [
        "openrouter/owl-alpha",
        "openrouter/free",
        "nvidia/nemotron-3-super-120b-a12b:free",
        "nvidia/nemotron-3-ultra-550b-a55b:free",
        "openai/gpt-oss-120b:free",
        "openai/gpt-oss-20b:free",
        "nousresearch/hermes-3-llama-3.1-405b:free",
        "meta-llama/llama-3.3-70b-instruct:free",
        "moonshotai/kimi-k2.6:free",
        "google/gemma-4-31b-it:free",
        "qwen/qwen3-coder:free",
        "qwen/qwen3-next-80b-a3b-instruct:free",
    ],
    "starter": [
        "deepseek/deepseek-v4-flash",
        "deepseek/deepseek-v4-pro",
        "google/gemini-2.5-flash",
        "google/gemini-2.5-flash-lite",
        "meta-llama/llama-4-maverick",
    ],
    "pro": [
        "anthropic/claude-sonnet-4.6",
        "openai/gpt-4.1",
        "google/gemini-2.5-pro",
    ],
    "scale": [
        "anthropic/claude-opus-4.7",
        "openai/gpt-4.5-preview",
    ],
}

TIER_QUOTA = {"free": 100, "starter": 2000, "pro": 5000, "scale": 25000}
TIER_RANK  = {"free": 0, "starter": 1, "pro": 2, "scale": 3}

MODEL_TIER = {}
for _tier, _models in TIER_MODELS.items():
    for _m in _models:
        MODEL_TIER[_m] = _tier

DEFAULT_FREE_MODEL = TIER_MODELS["free"][0]

# ── Account resolution cache (TTL = 300s) ───────────────────────────
_account_cache = TTLCache(maxsize=1000, ttl=300)
_cache_lock = threading.Lock()

# ── Free-model fallback rotation ────────────────────────────────────
_fallback_lock = threading.Lock()
_fallback_index = 0

def _next_fallback_model(tried):
    global _fallback_index
    free_models = TIER_MODELS["free"]
    with _fallback_lock:
        for _ in range(len(free_models)):
            idx = _fallback_index % len(free_models)
            _fallback_index = idx + 1
            candidate = free_models[idx]
            if candidate not in tried:
                return candidate
    return None

MODEL_COSTS = {
    "anthropic/claude-opus":    (0.015, 0.075),
    "anthropic/claude-sonnet":  (0.003, 0.015),
    "openai/gpt-4.5":           (0.01, 0.03),
    "openai/gpt-4.1":           (0.002, 0.008),
    "google/gemini-2.5-pro":    (0.00125, 0.005),
    "google/gemini-2.5-flash":  (0.000075, 0.0003),
    "deepseek/deepseek-v4-pro": (0.00027, 0.0011),
    "deepseek/deepseek-v4-flash":(0.00015, 0.0006),
}

def estimate_cost(model, tokens_in, tokens_out):
    for prefix, (in_rate, out_rate) in MODEL_COSTS.items():
        if model.startswith(prefix):
            return (tokens_in * in_rate + tokens_out * out_rate) / 1000
    if model.endswith(":free"):
        return 0.0
    return (tokens_in * 0.0005 + tokens_out * 0.0015) / 1000

def get_allowed_models(tier):
    allowed = set()
    for t in ["free", "starter", "pro", "scale"]:
        allowed.update(TIER_MODELS[t])
        if t == tier:
            break
    return allowed

def _anon_ip_key(r):
    xff = r.headers.get('X-Forwarded-For', '')
    ip = xff.split(',')[0].strip() if xff else (r.remote_addr or '0.0.0.0')
    return 'anon_' + hashlib.sha256(f"{ip}:vane-v1".encode()).hexdigest()[:20]

def resolve_account(auth_header):
    key = auth_header.replace("Bearer ", "") if auth_header else ""
    if not key or not key.startswith("afr_"):
        return None
    h = hashlib.sha256(key.encode()).hexdigest()
    with _cache_lock:
        if h in _account_cache:
            return _account_cache[h]
    try:
        k_res = db.table("api_keys").select("id, account_id").eq("key_hash", h).eq("revoked", False).maybe_single().execute()
        if not k_res.data:
            return None
        s_res = db.table("subscriptions").select("tier").eq("account_id", k_res.data["account_id"]).in_("status", ["active", "past_due"]).order("created_at", desc=True).limit(1).execute()
        tier = s_res.data[0]["tier"] if s_res.data else "free"
        result = {
            "account_id":  k_res.data["account_id"],
            "api_key_id":  k_res.data["id"],
            "tier":        tier,
        }
        with _cache_lock:
            _account_cache[h] = result
        return result
    except Exception:
        return None

def check_quota(account_id, api_key_id, tier):
    limit = TIER_QUOTA.get(tier, 100)
    try:
        month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0).isoformat()
        res = db.table("usage_log").select("queries").eq("api_key_id", api_key_id).gte("created_at", month_start).execute()
        used = sum(r.get("queries", 0) for r in (res.data or []))
        return used < limit, int(used), limit
    except Exception:
        return True, 0, limit

def log_usage(api_key_id, account_id, tier, model, tokens_in, tokens_out):
    cost = estimate_cost(model, tokens_in, tokens_out)
    try:
        db.table("usage_log").insert({
            "api_key_id": api_key_id,
            "account_id": account_id,
            "model":      model,
            "tokens_in":  tokens_in,
            "tokens_out": tokens_out,
            "queries":    1,
            "cost_eur":   float(cost),
        }).execute()
    except Exception:
        pass

def _patch_tool_args(line_bytes):
    if not line_bytes.startswith(b"data: ") or line_bytes.rstrip() == b"data: [DONE]":
        return line_bytes
    try:
        payload = line_bytes[6:].rstrip()
        if not payload:
            return line_bytes
        data = json.loads(payload)
        changed = False
        for choice in data.get("choices", []):
            for tc in (choice.get("delta") or {}).get("tool_calls") or []:
                func = tc.get("function") or {}
                if func.get("arguments") == "":
                    del func["arguments"]
                    changed = True
        if changed:
            return b"data: " + json.dumps(data, separators=(",", ":")).encode()
    except Exception:
        pass
    return line_bytes

def make_counting_stream(resp, api_key_id, account_id, tier, model):
    tokens_in = 0
    tokens_out = 0
    buf = b""
    try:
        for chunk in resp.iter_content(chunk_size=8192):
            if not chunk:
                continue
            buf += chunk
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                line = line.rstrip(b"\r")
                line = _patch_tool_args(line)
                if line.startswith(b"data: ") and line.rstrip() != b"data: [DONE]":
                    try:
                        data = json.loads(line[6:])
                        usage = data.get("usage") or {}
                        if usage.get("prompt_tokens"):
                            tokens_in = usage["prompt_tokens"]
                        if usage.get("completion_tokens"):
                            tokens_out = usage["completion_tokens"]
                    except Exception:
                        pass
                yield line + b"\n"
        if buf:
            buf = buf.rstrip(b"\r")
            if buf:
                yield _patch_tool_args(buf) + b"\n"
    finally:
        log_usage(api_key_id, account_id, tier, model, tokens_in, tokens_out)

# ── Routes ──────────────────────────────────────────────────────────

@app.route("/health")
def health():
    return jsonify({
        "service": "tier-proxy-v5",
        "status": "healthy",
        "tiers": {t: {"models": len(m), "quota": TIER_QUOTA[t]} for t, m in TIER_MODELS.items()},
    })

@app.route("/api/v1/models", methods=["GET"])
def list_models():
    return jsonify({
        "tiers": {
            tier: {"models": sorted(models), "quota": TIER_QUOTA[tier]}
            for tier, models in TIER_MODELS.items()
        },
    })

@app.route("/internal/invalidate-cache", methods=["POST"])
def invalidate_cache():
    data = request.json or {}
    account_id = data.get("account_id")
    if not account_id:
        return jsonify({"error": "account_id required"}), 400
    with _cache_lock:
        keys_to_drop = [h for h, v in list(_account_cache.items()) if isinstance(v, dict) and v.get("account_id") == account_id]
        for h in keys_to_drop:
            _account_cache.pop(h, None)
    return jsonify({"cleared": len(keys_to_drop)})

@app.route("/api/v1/<path:subpath>", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
def proxy(subpath):
    auth = request.headers.get("Authorization", "")
    body = request.get_data() or b"{}"
    try:
        body_json = json.loads(body) if body else {}
    except Exception:
        body_json = {}

    model = body_json.get("model", "") or ""
    account = resolve_account(auth)
    tier = account["tier"] if account else "free"
    api_key_id = account["api_key_id"] if account else _anon_ip_key(request)
    account_id = account["account_id"] if account else None

    # Starter tier for internal Vane Docker requests
    if account is None:
        xff = request.headers.get("X-Forwarded-For", "")
        client_ip = xff.split(",")[0].strip() if xff else (request.remote_addr or "")
        if client_ip.startswith("172.22."):
            tier = "starter"

    if not model:
        model = DEFAULT_FREE_MODEL
        body_json["model"] = model
        body = json.dumps(body_json).encode()

    allowed = get_allowed_models(tier)
    if model not in allowed:
        required = MODEL_TIER.get(model, "unknown")
        return jsonify({"error": {
            "message": f"Model '{model}' requires '{required}' tier or higher. You are on '{tier}'. Upgrade at https://vane.sytes.net/pricing",
            "type": "tier_restriction",
            "code": "tier_upgrade_required",
            "current_tier": tier,
            "required_tier": required,
        }}), 402

    quota_ok, used, limit = check_quota(account_id, api_key_id, tier)
    if not quota_ok:
        return jsonify({"error": {
            "message": f"Monthly quota exceeded ({used}/{limit} queries). Upgrade at https://vane.sytes.net/pricing",
            "type": "quota_exceeded",
            "code": "quota_exceeded",
            "tier": tier,
            "quota_used": used,
            "quota_limit": limit,
        }}), 429

    url = f"{OPENROUTER_BASE}/{subpath}"
    if request.query_string:
        url += f"?{request.query_string.decode()}"

    fwd_headers = {k: v for k, v in request.headers if k.lower() not in ("host", "content-length")}
    fwd_headers["Authorization"] = f"Bearer {OPENROUTER_API_KEY}"

    tried_models = {model}
    current_model = model
    current_body = body
    MAX_FALLBACKS = 3
    fallbacks_used = 0

    while True:
        try:
            resp = req_lib.request(
                method=request.method, url=url, headers=fwd_headers,
                data=current_body or None, stream=True, timeout=295,
            )
        except req_lib.exceptions.RequestException as e:
            return jsonify({"error": {"message": f"Upstream error: {str(e)}", "code": "upstream_error"}}), 502

        if resp.status_code == 200:
            excluded = ("transfer-encoding", "content-encoding", "connection")
            rh = [(k, v) for k, v in resp.raw.headers.items() if k.lower() not in excluded]
            return Response(
                make_counting_stream(resp, api_key_id, account_id, tier, current_model),
                200, rh
            )

        if resp.status_code in (402, 429) and fallbacks_used < MAX_FALLBACKS:
            try:
                err_body = resp.content
                err = json.loads(err_body)
                err_msg = str((err.get("error") or {}).get("message", ""))
                upstream_blocked = (
                    "Insufficient credits" in err_msg
                    or "rate" in err_msg.lower()
                    or "temporarily" in err_msg.lower()
                    or "upstream" in err_msg.lower()
                )
                if upstream_blocked:
                    next_model = _next_fallback_model(tried_models)
                    if next_model:
                        tried_models.add(next_model)
                        current_model = next_model
                        body_json["model"] = current_model
                        current_body = json.dumps(body_json).encode()
                        fallbacks_used += 1
                        continue
            except Exception:
                pass

        if resp.status_code in (402, 429) and fallbacks_used >= MAX_FALLBACKS:
            return jsonify({"error": {"message": "All available models are temporarily rate-limited or out of credits. Please try again in a minute.", "code": "all_models_exhausted"}}), resp.status_code

        try:
            err_body = resp.content
        except Exception:
            err_body = b'{"error":{"message":"Upstream error","code":"upstream_error"}}'
        excluded = ("transfer-encoding", "content-encoding", "connection")
        rh = [(k, v) for k, v in resp.raw.headers.items() if k.lower() not in excluded]
        return Response(err_body, resp.status_code, rh)

if __name__ == "__main__":
    app.run(host="172.22.0.1", port=5002, debug=False)
PYEOF
```

- [ ] **Step 3: Syntax-check the new file**

```bash
python3 -m py_compile /var/lib/agentforge-console/tier-proxy.py && echo "Syntax OK"
```

Expected: `Syntax OK`

---

### Task 6: Fix pricing.html and dashboard.html

- [ ] **Step 1: Fix the price label mismatch in pricing.html**

The JS `_planLabels` object shows `pro: '€29/mo'` and `scale: '€99/mo'` — both wrong. Fix:

```bash
sed -i "s/pro:'Pro — €29\/mo'/pro:'Pro — €39\/mo'/" /var/www/html/pages/pricing.html
sed -i "s/scale:'Scale — €99\/mo'/scale:'Scale — €149\/mo'/" /var/www/html/pages/pricing.html
```

- [ ] **Step 2: Verify the fix**

```bash
grep '_planLabels' /var/www/html/pages/pricing.html
```

Expected:
```
var _planLabels = {starter:'Starter — €9/mo', pro:'Pro — €39/mo', scale:'Scale — €149/mo'};
```

- [ ] **Step 3: Update dashboard.html — replace "Manage Subscription →" link with portal button and add subscription status**

The current account card renders a static link `<a href="/pricing" ...>Manage Subscription →</a>`. Replace the entire `renderDashboard` function's `accountContent` block and add a `manageSubscription()` function. The change is in the `<script>` tag.

Find the line (around line 1031):
```js
            <a href="/pricing" class="btn btn-sm btn-secondary" style="width:auto;">Manage Subscription →</a>
```

Replace the entire `document.getElementById('accountContent').innerHTML` assignment (lines 1011–1033) with:

```bash
python3 << 'EOF'
import re

path = "/var/www/html/pages/dashboard.html"
with open(path, "r") as f:
    content = f.read()

old_block = """        document.getElementById('accountContent').innerHTML = `
          <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:16px;">
            <div>
              <div style="font-size:12px;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.04em;margin-bottom:4px;">Plan</div>
              <div style="font-size:20px;font-weight:700;">${tierDisplay}</div>
            </div>
            <div>
              <div style="font-size:12px;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.04em;margin-bottom:4px;">Status</div>
              <div style="font-size:16px;font-weight:600;color:var(--success);">Active</div>
            </div>
            <div>
              <div style="font-size:12px;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.04em;margin-bottom:4px;">Email</div>
              <div style="font-size:14px;color:var(--text-primary);word-break:break-all;">${escapeHtml(account.email || '—')}</div>
            </div>
            <div>
              <div style="font-size:12px;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.04em;margin-bottom:4px;">Credits Remaining</div>
              <div style="font-size:20px;font-weight:700;color:var(--accent);">${formatNumber(usage.credits_remaining ?? account.credits_remaining ?? 0)}</div>
            </div>
          </div>
          <div style="margin-top:20px;">
            <a href="/pricing" class="btn btn-sm btn-secondary" style="width:auto;">Manage Subscription →</a>
          </div>
        `;"""

new_block = """        const subStatus = (data.subscription && data.subscription.status) || 'active';
        const subStatusColor = subStatus === 'active' ? 'var(--success)' : subStatus === 'past_due' ? 'var(--warning)' : 'var(--danger)';
        const subStatusLabel = subStatus === 'active' ? 'Active' : subStatus === 'past_due' ? 'Past Due' : subStatus.charAt(0).toUpperCase() + subStatus.slice(1);
        const periodEnd = data.subscription && data.subscription.current_period_end ? new Date(data.subscription.current_period_end).toLocaleDateString('en-IE', {year:'numeric',month:'short',day:'numeric'}) : '—';
        document.getElementById('accountContent').innerHTML = `
          <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:16px;">
            <div>
              <div style="font-size:12px;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.04em;margin-bottom:4px;">Plan</div>
              <div style="font-size:20px;font-weight:700;">${tierDisplay}</div>
            </div>
            <div>
              <div style="font-size:12px;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.04em;margin-bottom:4px;">Status</div>
              <div style="font-size:16px;font-weight:600;color:${subStatusColor};">${subStatusLabel}</div>
            </div>
            <div>
              <div style="font-size:12px;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.04em;margin-bottom:4px;">Email</div>
              <div style="font-size:14px;color:var(--text-primary);word-break:break-all;">${escapeHtml(account.email || '—')}</div>
            </div>
            <div>
              <div style="font-size:12px;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.04em;margin-bottom:4px;">Credits Remaining</div>
              <div style="font-size:20px;font-weight:700;color:var(--accent);">${formatNumber(data.credits_remaining ?? 0)}</div>
            </div>
            <div>
              <div style="font-size:12px;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.04em;margin-bottom:4px;">Period Ends</div>
              <div style="font-size:14px;color:var(--text-primary);">${periodEnd}</div>
            </div>
          </div>
          <div style="margin-top:20px;display:flex;gap:12px;flex-wrap:wrap;">
            <button class="btn btn-sm btn-secondary" style="width:auto;" onclick="manageSubscription()">Manage Subscription →</button>
          </div>
        `;"""

if old_block in content:
    content = content.replace(old_block, new_block)
    print("accountContent block replaced")
else:
    print("ERROR: old_block not found — check manually")
    import sys; sys.exit(1)

with open(path, "w") as f:
    f.write(content)
print("Done")
EOF
```

Expected: `accountContent block replaced` then `Done`

- [ ] **Step 4: Add `manageSubscription()` function before the closing `})();` of the IIFE**

```bash
python3 << 'EOF'
path = "/var/www/html/pages/dashboard.html"
with open(path, "r") as f:
    content = f.read()

old_closing = """      // ===== Enter key support =====
      signupEmail.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') handleSubscribe();
      });
      loginKey.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') handleLogin();
      });

    })();"""

new_closing = """      // ===== Manage Subscription (Stripe billing portal) =====
      window.manageSubscription = function() {
        if (!currentApiKey) return;
        fetch('/api/v1/portal', {
          method: 'POST',
          headers: { 'Authorization': 'Bearer ' + currentApiKey, 'Content-Type': 'application/json' }
        })
        .then(function(r) { return r.json(); })
        .then(function(data) {
          if (data.url) { window.location.href = data.url; }
          else { alert('Could not open billing portal: ' + (data.error || 'Unknown error')); }
        })
        .catch(function() { alert('Network error. Please try again.'); });
      };

      // ===== Enter key support =====
      signupEmail.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') handleSubscribe();
      });
      loginKey.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') handleLogin();
      });

    })();"""

if old_closing in content:
    content = content.replace(old_closing, new_closing)
    print("manageSubscription added")
else:
    print("ERROR: closing IIFE not found — check manually")
    import sys; sys.exit(1)

with open(path, "w") as f:
    f.write(content)
print("Done")
EOF
```

Expected: `manageSubscription added` then `Done`

- [ ] **Step 5: Fix the hardcoded tier limits in dashboard.html JS**

```bash
python3 << 'EOF'
path = "/var/www/html/pages/dashboard.html"
with open(path, "r") as f:
    content = f.read()

# Fix tierLimits (credits) to match actual quotas
old_tier_limits = "        const limits = { starter: 1000, pro: 10000, scale: 50000 };"
new_tier_limits = "        const limits = { starter: 2000, pro: 5000, scale: 25000 };"

# Fix tierCallLimits (queries) to match actual quotas
old_call_limits = "        const limits = { starter: 500, pro: 5000, scale: 25000 };"
new_call_limits = "        const limits = { starter: 2000, pro: 5000, scale: 25000 };"

count = 0
if old_tier_limits in content:
    content = content.replace(old_tier_limits, new_tier_limits)
    count += 1
if old_call_limits in content:
    content = content.replace(old_call_limits, new_call_limits)
    count += 1

with open(path, "w") as f:
    f.write(content)
print(f"Fixed {count} tier limit lines")
EOF
```

Expected: `Fixed 2 tier limit lines`

---

### Task 7: Deploy and Verify End-to-End

- [ ] **Step 1: Restart both services**

```bash
sudo systemctl restart agentforge-console agentforge-tier-proxy
```

Wait 3 seconds, then check status:

```bash
sleep 3 && sudo systemctl status agentforge-console agentforge-tier-proxy --no-pager -l
```

Expected: both show `Active: active (running)`. If either shows `failed`, check logs:
```bash
sudo journalctl -u agentforge-console -n 30
sudo journalctl -u agentforge-tier-proxy -n 30
```

Common failure: `KeyError: 'SUPABASE_URL'` → the `EnvironmentFile` was not loaded. Verify: `sudo systemctl cat agentforge-console | grep EnvironmentFile`

- [ ] **Step 2: Health check both services**

```bash
curl -s http://127.0.0.1:5001/api/v1/health | python3 -m json.tool
```

Expected:
```json
{
  "status": "healthy",
  "version": "2.0.0"
}
```

```bash
curl -s http://172.22.0.1:5002/health | python3 -m json.tool
```

Expected: `"service": "tier-proxy-v5"` and `"status": "healthy"`

- [ ] **Step 3: Smoke-test the checkout endpoint**

```bash
curl -s -X POST http://127.0.0.1:5001/api/v1/checkout \
  -H 'Content-Type: application/json' \
  -d '{"email":"test-smoke@example.com","tier":"starter"}' | python3 -m json.tool
```

Expected: response contains `"url": "https://checkout.stripe.com/..."` (a real Stripe checkout URL).

If you get `{"error": "..."}`, check the Stripe key is valid and the price IDs still exist.

- [ ] **Step 4: Smoke-test the pricing.html label fix**

```bash
curl -s http://vane.sytes.net/pricing.html | grep '_planLabels'
```

Expected:
```
var _planLabels = {starter:'Starter — €9/mo', pro:'Pro — €39/mo', scale:'Scale — €149/mo'};
```

- [ ] **Step 5: Smoke-test the tier-proxy Supabase connection**

```bash
curl -s http://172.22.0.1:5002/api/v1/models | python3 -m json.tool | head -20
```

Expected: JSON with `"tiers"` key containing model lists. If the proxy crashes (502), it means `supabase-py` can't reach the Supabase project — verify `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` in the env file.

- [ ] **Step 6: Verify cache invalidation endpoint is reachable from the console host**

```bash
curl -s -X POST http://172.22.0.1:5002/internal/invalidate-cache \
  -H 'Content-Type: application/json' \
  -d '{"account_id":"test-id"}' | python3 -m json.tool
```

Expected: `{"cleared": 0}` (no cache entries for "test-id", but the endpoint responded).

- [ ] **Step 7: Register the webhook in Stripe dashboard**

If not already registered, add the Helix webhook at:
`https://dashboard.stripe.com/webhooks/create`

- **Endpoint URL**: `https://vane.sytes.net/api/v1/webhook`
- **Events to send**: `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted`, `invoice.payment_failed`
- After creating, copy the **Signing secret** (starts `whsec_`). If it differs from the one in `/etc/agentforge-console.env`, update the file and restart: `sudo systemctl restart agentforge-console`

---

## Verification Summary

After Task 7, all of these must pass:

| Check | Command | Expected |
|-------|---------|----------|
| Console health | `curl -s http://127.0.0.1:5001/api/v1/health` | `"version":"2.0.0"` |
| Proxy health | `curl -s http://172.22.0.1:5002/health` | `"service":"tier-proxy-v5"` |
| Checkout URL | `curl -X POST ... /checkout` with valid email | Stripe URL returned |
| Price labels | `grep '_planLabels' /var/www/html/pages/pricing.html` | `€39` and `€149` |
| Cache invalidation | `curl -X POST .../internal/invalidate-cache` | `{"cleared":0}` |
| No hardcoded keys | `grep -r 'sk_live_' /var/lib/agentforge-console/` | no output |
