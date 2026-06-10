# Vane Phase 4 — Tier-Aware Model Selector Design

**Date:** 2026-06-10  
**Status:** Approved  
**Project:** Vane (custom Perplexica build on `vmi1593174.contaboserver.net`)  
**Source tree:** `/home/jpeetz/vane-src/`  
**Running container:** `vane-local:latest`

---

## Goal

Replace the broken `ChatModelSelector` (currently shows hardcoded GPT stubs, throws "Invalid Model Selected" for all tier-proxy models) with a tier-aware model selector that:
- Fetches the live model list from tier-proxy at runtime
- Groups models by tier: Free, Starter (both accessible), Pro and Scale (locked)
- Shows friendly display names instead of raw OpenRouter model IDs
- Locks Pro + Scale with an "Upgrade to unlock" chip
- Persists the selected model across the session via localStorage
- Lives only in the home screen input (`EmptyChatMessageInput`) — model is sticky once chosen

**Internal enum values and API contracts are unchanged.** The `chatModelProvider` state, `useChat` hook, and all backend routes are unaffected.

---

## Problem Being Solved

The current stack has two bugs:

1. **Wrong model list**: `openai/index.ts` returns `chat: []` when `baseURL !== 'https://api.openai.com/v1'`. Perplexica then shows an empty list or hardcoded GPT stubs that don't exist in tier-proxy.

2. **Validation failure**: `loadChatModel(key)` throws `"Error Loading OpenAI Chat Model. Invalid Model Selected"` for any tier-proxy model ID, because the model isn't in the empty/stub list.

---

## Decisions

| Question | Decision | Reason |
|---|---|---|
| Model list source | Live from tier-proxy `/api/v1/models` | Single source of truth; auto-syncs when tier-proxy changes |
| Locked tier layout | Collapsed Pro+Scale block with "Upgrade to unlock" chip | Cleaner than four separate sections; upgrade path is clear |
| Where to show selector | Home screen input only | Model is sticky once selected; no need in follow-up bar |
| Display names | Static map in `ChatModelSelector.tsx` | Tier-proxy keys are stable; map is co-located with component |
| Auto-fallback toast | No — Phase 2 error toasts are sufficient | Silent rotation is good UX; toast per rotation would be noisy |

---

## Visual Design

### Pill trigger (home screen input)

```
[ 🔲 Gemini 2.5 Flash ▾ ]
```

- `Cpu` icon in `text-sky-500` (matches existing icon colour)
- Label: display name of active model, truncated at `max-w-[120px]`
- Chevron in muted colour
- Border: `border border-light-200 dark:border-dark-200`
- Background: `bg-light-secondary dark:bg-dark-secondary`
- Padding: `px-3 py-1.5`, border-radius: `rounded-full`
- Matches Phase 3 Optimization pill dimensions and style

### Popover layout

```
[ Search models… ]
── FREE ─────────────────────────────
  Llama 3.3 70B
  Kimi K2
  GPT OSS 120B
  … (all free models)
── STARTER ──────────────────────────
  ● Gemini 2.5 Flash   ✓ (active)
  DeepSeek V4 Flash
  DeepSeek V4 Pro
  Gemini 2.5 Flash Lite
  Llama 4 Maverick
── PRO + SCALE  [Upgrade to unlock] ─
  🔒 Claude Sonnet 4.6
  🔒 GPT-4.1
  🔒 Gemini 2.5 Pro
  🔒 Claude Opus 4.7
  🔒 GPT-4.5 Preview
```

- Width: `w-[260px]`
- Max height: `max-h-[380px] overflow-y-auto`
- Tier section headers: `text-[10px] uppercase tracking-wider text-black/40 dark:text-white/40`
- Active model row: `bg-green-500/10 border border-green-500/20`, label in `text-green-600 dark:text-green-400 font-medium`, checkmark icon
- Unlocked hover: `hover:bg-light-secondary dark:hover:bg-dark-secondary`
- Locked rows: `text-black/25 dark:text-white/25 cursor-not-allowed`, lock icon trailing
- "Upgrade to unlock" chip: `text-[10px] px-2 py-0.5 rounded-full bg-light-secondary dark:bg-dark-secondary text-black/40 dark:text-white/40 border border-light-200 dark:border-dark-200`
- Popover opens bottom-left (same as Optimization popover in Phase 3)
- `AnimatePresence` + `motion.div` with `opacity/scale` entrance (matches existing pattern)

---

## Display Name Map

Stored as a `const` at module scope in `ChatModelSelector.tsx`:

```typescript
const MODEL_DISPLAY_NAMES: Record<string, string> = {
  'deepseek/deepseek-v4-flash': 'DeepSeek V4 Flash',
  'deepseek/deepseek-v4-pro': 'DeepSeek V4 Pro',
  'google/gemini-2.5-flash': 'Gemini 2.5 Flash',
  'google/gemini-2.5-flash-lite': 'Gemini 2.5 Flash Lite',
  'meta-llama/llama-4-maverick': 'Llama 4 Maverick',
  'meta-llama/llama-3.3-70b-instruct:free': 'Llama 3.3 70B',
  'moonshotai/kimi-k2.6:free': 'Kimi K2',
  'openai/gpt-oss-120b:free': 'GPT OSS 120B',
  'openai/gpt-oss-20b:free': 'GPT OSS 20B',
  'nvidia/nemotron-3-ultra-550b-a55b:free': 'Nemotron Ultra 550B',
  'nvidia/nemotron-3-super-120b-a12b:free': 'Nemotron Super 120B',
  'nousresearch/hermes-3-llama-3.1-405b:free': 'Hermes 3 405B',
  'google/gemma-4-31b-it:free': 'Gemma 4 31B',
  'qwen/qwen3-coder:free': 'Qwen3 Coder',
  'qwen/qwen3-next-80b-a3b-instruct:free': 'Qwen3 80B',
  'openrouter/free': 'OpenRouter Free',
  'openrouter/owl-alpha': 'OpenRouter Owl Alpha',
  'anthropic/claude-sonnet-4.6': 'Claude Sonnet 4.6',
  'openai/gpt-4.1': 'GPT-4.1',
  'google/gemini-2.5-pro': 'Gemini 2.5 Pro',
  'anthropic/claude-opus-4.7': 'Claude Opus 4.7',
  'openai/gpt-4.5-preview': 'GPT-4.5 Preview',
};
```

Fallback for unknown keys: strip provider prefix and title-case the remainder.

---

## Component Changes

### 1. `src/app/api/tier-models/route.ts` *(new file)*

Server-side Next.js route. Fetches `http://172.22.0.1:5002/api/v1/models` and returns the tier structure. Running server-side ensures the internal Docker network address is reachable.

```typescript
export async function GET() {
  const res = await fetch('http://172.22.0.1:5002/api/v1/models');
  const data = await res.json();
  return Response.json(data);
}
```

Response shape (pass-through from tier-proxy):
```json
{
  "tiers": {
    "free":    { "models": [...], "quota": 100 },
    "starter": { "models": [...], "quota": 2000 },
    "pro":     { "models": [...], "quota": 5000 },
    "scale":   { "models": [...], "quota": 25000 }
  }
}
```

### 2. `src/lib/models/providers/openai/index.ts`

**What changes:** In `getModelList()`, when `baseURL !== 'https://api.openai.com/v1'`, fetch from `http://172.22.0.1:5002/api/v1/models`, flatten all tiers into a single chat model list, and return it. This fixes the "Invalid Model Selected" validation error.

```typescript
// Replace the current `else { chat: [] }` branch:
const tierRes = await fetch('http://172.22.0.1:5002/api/v1/models');
const tierData = await tierRes.json();
const allModels: Model[] = Object.values(tierData.tiers)
  .flatMap((t: any) => t.models)
  .map((key: string) => ({ key, name: key }));
return {
  ...defaultModels,
  chat: [...allModels, ...configProvider.chatModels],
};
```

**What stays the same:** All other provider logic, `loadChatModel`, `loadEmbeddingModel`, config validation.

### 3. `src/components/MessageInputActions/ChatModelSelector.tsx`

**What changes:** Full rewrite.
- `MODEL_DISPLAY_NAMES` map at module scope
- `useEffect` fetches `/api/tier-models` on mount
- Renders: search input, Free section, Starter section, Pro+Scale locked section
- Pill trigger showing current model display name + `Cpu` icon + chevron
- `handleModelSelect(key)` calls `setChatModelProvider({ providerId: currentProviderId, key })` and updates localStorage
- `currentProviderId` read from `chatModelProvider.providerId` (already in `useChat`)
- Active model detected by `chatModelProvider.key === modelKey`

**What stays the same:** `setChatModelProvider` call signature, localStorage keys (`chatModelKey`, `chatModelProviderId`), Popover/AnimatePresence structure.

### 4. `src/components/EmptyChatMessageInput.tsx`

**What changes:** Import `ChatModelSelector` (renamed export from `ModelSelector` to `ChatModelSelector` for clarity — or keep existing export name). Add `<ModelSelector />` to the input bar alongside `<Optimization />`.

**Placement:** In the bottom action row of the home screen input, to the right of the attach button and to the left of `<Optimization />`. Order from left to right: `[Attach] [ModelSelector] [Optimization] ... [Submit]`.

**What stays the same:** All existing layout, textarea, submit handler, placeholder logic from Phase 3.

---

## Files Changed Summary

| File | Type of change |
|---|---|
| `src/app/api/tier-models/route.ts` | New — tier-proxy model list API |
| `src/lib/models/providers/openai/index.ts` | Fix — dynamic model list for non-OpenAI baseURL |
| `src/components/MessageInputActions/ChatModelSelector.tsx` | Rewrite — tier groups, pill trigger, lock UI |
| `src/components/EmptyChatMessageInput.tsx` | Add `<ModelSelector />` to home screen input bar |

**Requires Docker image rebuild** — all four files are compiled into the Next.js bundle.  
**641.js scraper patch** must be re-applied after container recreation (`slice(0,3)` → `slice(0,6)`, path: `/home/vane/.next/server/chunks/641.js`).

---

## Out of Scope

- Follow-up input model selector — model is sticky once chosen on home screen
- Auto-fallback toast for silent model rotation — Phase 2 error toasts are sufficient
- Subscription/payment UI — locked tiers show "Upgrade to unlock" chip only; no payment flow
- Tier quota display in UI — out of scope for this phase
- Sidebar, navbar, settings — not touched

---

## Success Criteria

- Model selector pill appears in home screen input showing current model name
- Selecting a model persists across page refresh (localStorage)
- Free and Starter models are selectable and successfully route through tier-proxy
- Pro + Scale models are visible, grayed out, non-clickable, with "Upgrade to unlock" chip
- Search filters the visible (unlocked) models
- No "Invalid Model Selected" errors when using tier-proxy model keys
- 641.js scraper depth patch persists after redeploy
