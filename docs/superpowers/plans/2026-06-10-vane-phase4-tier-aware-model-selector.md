# Vane Phase 4 — Tier-Aware Model Selector Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the broken ChatModelSelector (shows wrong models, throws "Invalid Model Selected" for all tier-proxy models) with a tier-grouped UI that fetches live models from tier-proxy, locks Pro+Scale tiers, and shows friendly display names.

**Architecture:** A new Next.js server-side route `/api/tier-models` proxies the tier-proxy's `/api/v1/models` endpoint so the browser can fetch tier data without direct access to the Docker internal network. The OpenAI provider's `getDefaultModels()` is fixed to fetch from tier-proxy for non-OpenAI baseURLs, unblocking model validation. `ChatModelSelector` is fully rewritten with tier groups, a pill trigger, and lock UI.

**Tech Stack:** Next.js 15 App Router (TypeScript), React, Headless UI Popover, Framer Motion, Lucide icons, Tailwind CSS, SSH deploy to `jpeetz@207.180.227.214`, Docker image `vane-local:latest` on `searxng_default` network.

---

## Context (read before touching any file)

- **Source tree on server:** `/home/jpeetz/vane-src/`
- **Running container:** `vane` on network `searxng_default` (172.22.0.0/16)
- **Tier-proxy:** `http://172.22.0.1:5002` — accessible from inside the Vane container and from the server host. NOT accessible from the browser.
- **Vane container env:** `OPENAI_BASE_URL=http://172.22.0.1:5002/api/v1` — so the OpenAI provider points at tier-proxy, not real OpenAI.
- **Vane has starter tier** — free + starter models accessible; pro + scale locked.
- **`EmptyChatMessageInput.tsx` already renders `<ModelSelector />`** — no changes needed to that file.
- **After every Docker rebuild**, re-apply the 641.js scraper patch (see Task 4).
- **All SSH commands** use `sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214`.

## File Map

| File | Action | Responsibility |
|---|---|---|
| `src/app/api/tier-models/route.ts` | **Create** | Server-side proxy → tier-proxy `/api/v1/models` |
| `src/lib/models/providers/openai/index.ts` | **Modify** `getDefaultModels()` | Return tier-proxy model list for non-OpenAI baseURL |
| `src/components/MessageInputActions/ChatModelSelector.tsx` | **Rewrite** | Tier-grouped pill selector with lock UI |
| `src/components/EmptyChatMessageInput.tsx` | **No change** | Already imports + renders `<ModelSelector />` |

---

## Task 1: Create `/api/tier-models` route

**Files:**
- Create: `src/app/api/tier-models/route.ts`

This is a Next.js App Router route handler. It runs server-side inside the Vane container, so it can reach `http://172.22.0.1:5002`. The browser cannot reach that address directly.

- [ ] **Step 1: SSH into the server and create the directory**

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  "mkdir -p /home/jpeetz/vane-src/src/app/api/tier-models"
```

Expected: no output (directory created).

- [ ] **Step 2: Create the route file**

Write this exact content to `/home/jpeetz/vane-src/src/app/api/tier-models/route.ts`:

```typescript
export const dynamic = 'force-dynamic';

export async function GET() {
  try {
    const res = await fetch('http://172.22.0.1:5002/api/v1/models');
    if (!res.ok) {
      return Response.json(
        { error: 'Failed to fetch tier models' },
        { status: 502 },
      );
    }
    const data = await res.json();
    return Response.json(data);
  } catch {
    return Response.json({ error: 'Tier proxy unreachable' }, { status: 502 });
  }
}
```

`export const dynamic = 'force-dynamic'` prevents Next.js from trying to statically pre-render this route at build time (it would fail since `172.22.0.1` isn't reachable during build).

- [ ] **Step 3: Verify TypeScript compiles**

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  "cd /home/jpeetz/vane-src && npx tsc --noEmit 2>&1 | tail -20"
```

Expected: no errors. If errors appear, they are pre-existing — note them but don't fix unrelated issues.

- [ ] **Step 4: Commit**

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  "cd /home/jpeetz/vane-src && git add src/app/api/tier-models/route.ts && git commit -m 'feat(api): add tier-models route proxying tier-proxy model list'"
```

---

## Task 2: Fix OpenAI provider `getDefaultModels()`

**Files:**
- Modify: `src/lib/models/providers/openai/index.ts`

The current `getDefaultModels()` returns `{ embedding: [], chat: [] }` when `baseURL !== 'https://api.openai.com/v1'`. This causes `loadChatModel()` to throw "Invalid Model Selected" for every tier-proxy model. The fix: fetch the full model list from tier-proxy and return it as the chat list.

- [ ] **Step 1: Read the current `getDefaultModels` implementation**

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  "grep -n 'getDefaultModels\|getModelList\|chat:\|embedding:' /home/jpeetz/vane-src/src/lib/models/providers/openai/index.ts"
```

Confirm line numbers for the `getDefaultModels` method. The current body looks like:

```typescript
async getDefaultModels(): Promise<ModelList> {
  if (this.config.baseURL === 'https://api.openai.com/v1') {
    return {
      embedding: defaultEmbeddingModels,
      chat: defaultChatModels,
    };
  }

  return {
    embedding: [],
    chat: [],
  };
}
```

- [ ] **Step 2: Replace `getDefaultModels` with tier-proxy-aware version**

Replace the entire `getDefaultModels` method body with:

```typescript
async getDefaultModels(): Promise<ModelList> {
  if (this.config.baseURL === 'https://api.openai.com/v1') {
    return {
      embedding: defaultEmbeddingModels,
      chat: defaultChatModels,
    };
  }

  try {
    const tierRes = await fetch('http://172.22.0.1:5002/api/v1/models');
    const tierData: {
      tiers: Record<string, { models: string[] }>;
    } = await tierRes.json();
    const allModels = Object.values(tierData.tiers)
      .flatMap((t) => t.models)
      .map((key) => ({ key, name: key }));
    return {
      embedding: [],
      chat: allModels,
    };
  } catch {
    return {
      embedding: [],
      chat: [],
    };
  }
}
```

Use the Edit tool (or sed) to replace the old method. The catch block preserves graceful degradation if tier-proxy is down.

- [ ] **Step 3: Verify TypeScript compiles**

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  "cd /home/jpeetz/vane-src && npx tsc --noEmit 2>&1 | tail -20"
```

Expected: no new errors beyond any pre-existing ones.

- [ ] **Step 4: Commit**

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  "cd /home/jpeetz/vane-src && git add src/lib/models/providers/openai/index.ts && git commit -m 'fix(providers): fetch tier-proxy model list for non-OpenAI baseURL'"
```

---

## Task 3: Rewrite `ChatModelSelector.tsx`

**Files:**
- Rewrite: `src/components/MessageInputActions/ChatModelSelector.tsx`

Full replacement. The new component:
- Fetches `/api/tier-models` on mount
- Shows a pill trigger (Cpu icon + model display name + chevron)
- Opens a popover with Free section, Starter section, Pro+Scale locked section
- Locked section has "Upgrade to unlock" chip, grayed rows, lock icon
- Search filters Free + Starter models only (locked models always shown)
- Active model highlighted in green with checkmark
- Uses `setChatModelProvider` + `localStorage` on selection (same keys as before: `chatModelKey`)

- [ ] **Step 1: Write the new component**

Replace the entire contents of `/home/jpeetz/vane-src/src/components/MessageInputActions/ChatModelSelector.tsx` with:

```typescript
'use client';

import { Check, ChevronDown, Cpu, Lock, Loader2, Search } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Popover, PopoverButton, PopoverPanel } from '@headlessui/react';
import { useEffect, useState } from 'react';
import { useChat } from '@/lib/hooks/useChat';
import { AnimatePresence, motion } from 'motion/react';

type TierData = {
  tiers: {
    free: { models: string[]; quota: number };
    starter: { models: string[]; quota: number };
    pro: { models: string[]; quota: number };
    scale: { models: string[]; quota: number };
  };
};

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

function displayName(key: string): string {
  if (MODEL_DISPLAY_NAMES[key]) return MODEL_DISPLAY_NAMES[key];
  const slug = key.split('/').pop() ?? key;
  return slug
    .replace(/:.*$/, '')
    .replace(/-/g, ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

const ModelSelector = () => {
  const [tierData, setTierData] = useState<TierData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const { setChatModelProvider, chatModelProvider } = useChat();

  useEffect(() => {
    const load = async () => {
      try {
        const res = await fetch('/api/tier-models');
        if (!res.ok) throw new Error('Failed to fetch tier models');
        const data: TierData = await res.json();
        setTierData(data);
      } catch (e) {
        console.error('Error loading tier models:', e);
      } finally {
        setIsLoading(false);
      }
    };
    load();
  }, []);

  const handleModelSelect = (modelKey: string) => {
    setChatModelProvider({ providerId: chatModelProvider.providerId, key: modelKey });
    localStorage.setItem('chatModelKey', modelKey);
  };

  const activeKey = chatModelProvider?.key ?? '';

  const filterModels = (models: string[]) =>
    searchQuery
      ? models.filter((k) =>
          displayName(k).toLowerCase().includes(searchQuery.toLowerCase()),
        )
      : models;

  const freeModels = filterModels(tierData?.tiers.free.models ?? []);
  const starterModels = filterModels(tierData?.tiers.starter.models ?? []);
  const lockedModels = [
    ...(tierData?.tiers.pro.models ?? []),
    ...(tierData?.tiers.scale.models ?? []),
  ];

  return (
    <Popover className="relative">
      {({ open }) => (
        <>
          <PopoverButton
            type="button"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-full border border-light-200 dark:border-dark-200 bg-light-secondary dark:bg-dark-secondary text-black dark:text-white hover:bg-light-200 dark:hover:bg-dark-200 transition duration-200 focus:outline-none active:scale-95"
          >
            <Cpu size={13} className="text-sky-500 shrink-0" />
            <span className="text-xs max-w-[120px] truncate">
              {activeKey ? displayName(activeKey) : 'Select Model'}
            </span>
            <ChevronDown
              size={11}
              className="text-black/40 dark:text-white/40 shrink-0"
            />
          </PopoverButton>

          <AnimatePresence>
            {open && (
              <PopoverPanel
                className="absolute z-10 bottom-full mb-2 right-0 w-[260px]"
                static
              >
                <motion.div
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  transition={{ duration: 0.1, ease: 'easeOut' }}
                  className="origin-bottom-right bg-light-primary dark:bg-dark-primary border border-light-200 dark:border-dark-200 rounded-lg shadow-lg overflow-hidden"
                >
                  {/* Search */}
                  <div className="p-2 border-b border-light-200 dark:border-dark-200">
                    <div className="relative">
                      <Search
                        size={13}
                        className="absolute left-2.5 top-1/2 -translate-y-1/2 text-black/40 dark:text-white/40"
                      />
                      <input
                        type="text"
                        placeholder="Search models…"
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="w-full pl-7 pr-3 py-1.5 bg-light-secondary dark:bg-dark-secondary rounded-md text-xs text-black dark:text-white placeholder:text-black/40 dark:placeholder:text-white/40 focus:outline-none border border-transparent"
                      />
                    </div>
                  </div>

                  <div className="max-h-[320px] overflow-y-auto">
                    {isLoading ? (
                      <div className="flex items-center justify-center py-10">
                        <Loader2
                          className="animate-spin text-black/40 dark:text-white/40"
                          size={20}
                        />
                      </div>
                    ) : (
                      <div>
                        {/* FREE section */}
                        {freeModels.length > 0 && (
                          <>
                            <div className="px-3 pt-2 pb-1 text-[10px] uppercase tracking-wider font-semibold text-black/40 dark:text-white/40">
                              Free
                            </div>
                            <div className="px-2 pb-1">
                              {freeModels.map((key) => (
                                <button
                                  key={key}
                                  type="button"
                                  onClick={() => handleModelSelect(key)}
                                  className={cn(
                                    'w-full flex items-center gap-2 px-2 py-1.5 rounded-md text-xs text-start transition duration-150',
                                    activeKey === key
                                      ? 'bg-green-500/10'
                                      : 'hover:bg-light-secondary dark:hover:bg-dark-secondary',
                                  )}
                                >
                                  <Cpu
                                    size={12}
                                    className={cn(
                                      'shrink-0',
                                      activeKey === key
                                        ? 'text-green-500'
                                        : 'text-black/40 dark:text-white/40',
                                    )}
                                  />
                                  <span
                                    className={cn(
                                      'flex-1 truncate',
                                      activeKey === key
                                        ? 'text-green-600 dark:text-green-400 font-medium'
                                        : 'text-black/70 dark:text-white/70',
                                    )}
                                  >
                                    {displayName(key)}
                                  </span>
                                  {activeKey === key && (
                                    <Check size={11} className="text-green-500 shrink-0" />
                                  )}
                                </button>
                              ))}
                            </div>
                          </>
                        )}

                        {/* STARTER section */}
                        {starterModels.length > 0 && (
                          <>
                            {freeModels.length > 0 && (
                              <div className="mx-3 h-px bg-light-200 dark:bg-dark-200" />
                            )}
                            <div className="px-3 pt-2 pb-1 text-[10px] uppercase tracking-wider font-semibold text-black/40 dark:text-white/40">
                              Starter
                            </div>
                            <div className="px-2 pb-1">
                              {starterModels.map((key) => (
                                <button
                                  key={key}
                                  type="button"
                                  onClick={() => handleModelSelect(key)}
                                  className={cn(
                                    'w-full flex items-center gap-2 px-2 py-1.5 rounded-md text-xs text-start transition duration-150',
                                    activeKey === key
                                      ? 'bg-green-500/10'
                                      : 'hover:bg-light-secondary dark:hover:bg-dark-secondary',
                                  )}
                                >
                                  <Cpu
                                    size={12}
                                    className={cn(
                                      'shrink-0',
                                      activeKey === key
                                        ? 'text-green-500'
                                        : 'text-black/40 dark:text-white/40',
                                    )}
                                  />
                                  <span
                                    className={cn(
                                      'flex-1 truncate',
                                      activeKey === key
                                        ? 'text-green-600 dark:text-green-400 font-medium'
                                        : 'text-black/70 dark:text-white/70',
                                    )}
                                  >
                                    {displayName(key)}
                                  </span>
                                  {activeKey === key && (
                                    <Check size={11} className="text-green-500 shrink-0" />
                                  )}
                                </button>
                              ))}
                            </div>
                          </>
                        )}

                        {/* PRO + SCALE locked section */}
                        {lockedModels.length > 0 && (
                          <>
                            <div className="mx-3 h-px bg-light-200 dark:bg-dark-200" />
                            <div className="px-3 pt-2 pb-1 flex items-center justify-between">
                              <span className="text-[10px] uppercase tracking-wider font-semibold text-black/25 dark:text-white/25">
                                Pro + Scale
                              </span>
                              <span className="text-[10px] px-2 py-0.5 rounded-full bg-light-secondary dark:bg-dark-secondary text-black/40 dark:text-white/40 border border-light-200 dark:border-dark-200">
                                Upgrade to unlock
                              </span>
                            </div>
                            <div className="px-2 pb-2">
                              {lockedModels.map((key) => (
                                <div
                                  key={key}
                                  className="flex items-center gap-2 px-2 py-1.5 rounded-md text-xs cursor-not-allowed"
                                >
                                  <Cpu
                                    size={12}
                                    className="text-black/20 dark:text-white/20 shrink-0"
                                  />
                                  <span className="flex-1 truncate text-black/25 dark:text-white/25">
                                    {displayName(key)}
                                  </span>
                                  <Lock
                                    size={11}
                                    className="text-black/20 dark:text-white/20 shrink-0"
                                  />
                                </div>
                              ))}
                            </div>
                          </>
                        )}
                      </div>
                    )}
                  </div>
                </motion.div>
              </PopoverPanel>
            )}
          </AnimatePresence>
        </>
      )}
    </Popover>
  );
};

export default ModelSelector;
```

- [ ] **Step 2: Verify TypeScript compiles**

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  "cd /home/jpeetz/vane-src && npx tsc --noEmit 2>&1 | tail -30"
```

Expected: no new errors. If you see `Cannot find module 'motion/react'` — check the existing import in `Optimization.tsx` to confirm the exact package name used in this project.

- [ ] **Step 3: Commit**

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  "cd /home/jpeetz/vane-src && git add src/components/MessageInputActions/ChatModelSelector.tsx && git commit -m 'feat(ui): tier-aware model selector with pill trigger and lock UI'"
```

---

## Task 4: Build, deploy, patch, and verify

**Files:** None — Docker build + patch only.

- [ ] **Step 1: Build the Docker image**

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  "cd /home/jpeetz/vane-src && docker build -t vane-local:latest . 2>&1 | tail -20"
```

Expected: `Successfully built <sha>` and `Successfully tagged vane-local:latest`. Build takes 3–5 minutes.

If build fails with a TypeScript error, read the full error output:
```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  "cd /home/jpeetz/vane-src && docker build -t vane-local:latest . 2>&1 | grep -A5 'error TS\|Error:'"
```

- [ ] **Step 2: Stop and remove the old container**

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  "docker stop vane && docker rm vane"
```

Expected: `vane` printed twice.

- [ ] **Step 3: Start the new container**

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  "docker run -d \
    --name vane \
    --network searxng_default \
    -p 3000:3000 \
    -v vane-data:/app/data \
    -e OPENAI_API_KEY=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 \
    -e OPENAI_BASE_URL=http://172.22.0.1:5002/api/v1 \
    vane-local:latest"
```

Expected: container ID printed (long hex string). Verify it started:

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  "docker ps --filter name=vane --format 'table {{.Names}}\t{{.Status}}'"
```

Expected: `vane   Up X seconds`

- [ ] **Step 4: Re-apply the 641.js scraper depth patch**

Find the chunk (path changes with each build):

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  "docker exec vane grep -rl '\.slice(0,' /home/vane/.next/server/chunks/ 2>/dev/null"
```

Expected output: something like `/home/vane/.next/server/chunks/641.js` (number may differ).

Apply the patch (replace `CHUNK_PATH` with the path from above):

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  "docker exec vane sed -i 's/\.slice(0,3)/\.slice(0,6)/g' CHUNK_PATH"
```

Verify the patch applied:

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  "docker exec vane grep -o '\.slice(0,[0-9])' CHUNK_PATH"
```

Expected: `.slice(0,6)`

- [ ] **Step 5: Verify the tier-models API endpoint**

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  "curl -s http://localhost:3000/api/tier-models | python3 -m json.tool | head -20"
```

Expected: JSON with `tiers.free.models`, `tiers.starter.models`, `tiers.pro.models`, `tiers.scale.models` arrays.

If you get `502` or empty response, check tier-proxy is running:
```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  "curl -s http://172.22.0.1:5002/api/v1/models | head -5"
```

- [ ] **Step 6: Smoke-test a query**

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  "curl -s -X POST http://localhost:3000/api/chat \
    -H 'Content-Type: application/json' \
    -d '{\"message\":\"What is 2+2?\",\"chatModel\":{\"provider\":\"openai\",\"model\":\"google/gemini-2.5-flash\"},\"optimizationMode\":\"speed\",\"files\":[],\"history\":[],\"focusMode\":\"webSearch\"}' \
    | head -5"
```

Expected: streaming response lines starting with `data:`. If you see `Invalid Model Selected`, the `getDefaultModels` fix in Task 2 didn't apply correctly — rebuild.

- [ ] **Step 7: Browser verification checklist**

Open `http://vmi1593174.contaboserver.net:3000` and confirm:

1. **Pill visible**: Model selector pill appears in the home screen input bar (between Sources and Attach), showing a model name or "Select Model"
2. **Popover opens**: Clicking the pill shows the tier-grouped list with Free, Starter, and Pro+Scale sections
3. **Lock UI**: Pro + Scale entries are grayed out with lock icons and "Upgrade to unlock" chip
4. **Selection works**: Clicking a Free or Starter model updates the pill label and closes the popover
5. **Persistence**: Refresh the page — the selected model is remembered
6. **Search**: Typing in the search box filters Free and Starter models by display name
7. **Query succeeds**: Submit a query — no "Invalid Model Selected" error in the browser console

---

## Self-Review Notes

- **Spec coverage confirmed**: tier-models API route ✓, openai provider fix ✓, ChatModelSelector rewrite ✓, EmptyChatMessageInput already done ✓
- **No placeholders**: all steps contain complete code
- **Type consistency**: `TierData` type defined once in `ChatModelSelector.tsx` and used consistently throughout
- **`export default ModelSelector`**: preserved — `EmptyChatMessageInput.tsx` imports as `import ModelSelector from './MessageInputActions/ChatModelSelector'`
- **`setChatModelProvider` call signature**: unchanged — `{providerId, key}` matches `useChat` hook type
- **localStorage key**: `chatModelKey` — same key used by original component and `useChat.tsx` line 87
