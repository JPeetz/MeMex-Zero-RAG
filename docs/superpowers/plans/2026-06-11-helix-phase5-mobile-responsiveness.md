# Helix Phase 5 — Mobile Responsiveness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Helix usable on 375px–430px phone screens by collapsing the sources block to an inline pill and hiding label text in both input bar pill buttons on mobile.

**Architecture:** Three targeted Tailwind breakpoint changes — no new libraries, no layout rewrites. `MessageSources.tsx` gets a mobile rendering path (collapsible pill + 2-column grid) alongside the unchanged desktop grid. `ChatModelSelector.tsx` and `Optimization.tsx` each get a single `hidden sm:inline` class added to their label `<span>`.

**Tech Stack:** Next.js 15 App Router, Tailwind CSS, React, Headless UI, Lucide icons. All changes are in `.tsx` files compiled into the Docker image. No test suite — verify by visual inspection in the running container.

---

## Environment

- **SSH:** `jpeetz@207.180.227.214` password `Buddy-2019`
- **Source tree:** `/home/jpeetz/vane-src/`
- **Container:** `vane` running `vane-local:latest` on `searxng_default` network, port 3000
- **Container env:** `OPENAI_BASE_URL=http://172.22.0.1:5002/api/v1`, `OPENAI_API_KEY=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`
- **After every rebuild:** re-apply 641.js scraper depth patch (see Task 3)

---

## File Map

| File | Change |
|---|---|
| `src/components/MessageSources.tsx` | Add mobile collapsible pill path; wrap desktop grid in `hidden sm:block` |
| `src/components/MessageInputActions/ChatModelSelector.tsx` | Add `hidden sm:inline` to label `<span>` in pill trigger |
| `src/components/MessageInputActions/Optimization.tsx` | Add `hidden sm:inline` to label `<span>` in pill trigger |

---

## Task 1: Sources mobile collapsible pill

**Files:**
- Modify: `src/components/MessageSources.tsx`

- [ ] **Step 1: Read the current file**

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  'cat /home/jpeetz/vane-src/src/components/MessageSources.tsx'
```

Confirm the imports and the `MessageSources` component structure before editing.

- [ ] **Step 2: Write the updated file**

Replace the entire file with the following. The only structural changes are: (a) `isMobileExpanded` state added, (b) `ChevronDown` and `cn` added to imports, (c) the `MessageSources` return wraps existing desktop grid in `hidden sm:block` and adds a new `sm:hidden` mobile section above it. The `SourceCard` component and the Dialog are untouched.

```tsx
/* eslint-disable @next/next/no-img-element */
import {
  Dialog,
  DialogPanel,
  DialogTitle,
  Transition,
  TransitionChild,
} from '@headlessui/react';
import { ChevronDown, File } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Fragment, useState } from 'react';
import { Chunk } from '@/lib/types';

const MAX_VISIBLE = 6;

const SourceCard = ({
  source,
  index,
  compact = false,
}: {
  source: Chunk;
  index: number;
  compact?: boolean;
}) => {
  const isFile = source.metadata.url?.includes('file_id://');
  const domain = isFile
    ? 'Uploaded File'
    : (source.metadata.url?.replace(/.+\/\/|www\.|\/.*$/g, '') ?? '');
  const snippet = (source.content ?? '').trim().slice(0, 130);

  return (
    <a
      href={source.metadata.url}
      target="_blank"
      rel="noreferrer"
      className={`bg-light-100 hover:bg-light-200 dark:bg-dark-100 dark:hover:bg-dark-200 transition duration-200 rounded-lg p-3 flex flex-col space-y-2 font-medium ${compact ? '' : 'min-h-[88px]'}`}
    >
      <div className="flex flex-row items-center justify-between">
        <div className="flex flex-row items-center space-x-1 min-w-0">
          {isFile ? (
            <div className="bg-dark-200 flex items-center justify-center w-5 h-5 rounded-full shrink-0">
              <File size={10} className="text-white/70" />
            </div>
          ) : (
            <img
              src={`https://s2.googleusercontent.com/s2/favicons?domain_url=${source.metadata.url}`}
              width={14}
              height={14}
              alt=""
              className="rounded h-4 w-4 shrink-0"
            />
          )}
          <p className="text-xs text-black/50 dark:text-white/50 truncate">
            {domain}
          </p>
        </div>
        <span className="text-[10px] text-black/35 dark:text-white/35 shrink-0 ml-1 tabular-nums">
          [{index + 1}]
        </span>
      </div>

      <p className="dark:text-white text-xs leading-snug line-clamp-1 font-medium">
        {source.metadata.title}
      </p>

      {snippet && !compact && (
        <p className="text-[11px] text-black/50 dark:text-white/50 leading-snug line-clamp-2">
          {snippet}
        </p>
      )}
    </a>
  );
};

const MessageSources = ({ sources }: { sources: Chunk[] }) => {
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [isMobileExpanded, setIsMobileExpanded] = useState(false);

  const closeModal = () => {
    setIsDialogOpen(false);
    document.body.classList.remove('overflow-hidden-scrollable');
  };

  const openModal = () => {
    setIsDialogOpen(true);
    document.body.classList.add('overflow-hidden-scrollable');
  };

  const visible = sources.slice(0, MAX_VISIBLE);
  const overflow = sources.length - MAX_VISIBLE;

  return (
    <>
      {/* Mobile: collapsible pill (hidden on sm+) */}
      <div className="sm:hidden">
        <button
          type="button"
          onClick={() => setIsMobileExpanded(!isMobileExpanded)}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-full border border-light-200 dark:border-dark-200 bg-light-secondary dark:bg-dark-secondary text-black dark:text-white hover:bg-light-200 dark:hover:bg-dark-200 transition duration-200 text-xs font-medium"
        >
          <File size={12} className="text-black/40 dark:text-white/40 shrink-0" />
          {sources.length} source{sources.length !== 1 ? 's' : ''}
          <ChevronDown
            size={11}
            className={cn(
              isMobileExpanded ? 'rotate-180' : 'rotate-0',
              'transition duration-200 text-black/40 dark:text-white/40 shrink-0',
            )}
          />
        </button>
        {isMobileExpanded && (
          <div className="grid grid-cols-2 gap-2 mt-2">
            {visible.map((source, i) => (
              <SourceCard key={i} source={source} index={i} compact />
            ))}
            {overflow > 0 && (
              <button
                onClick={openModal}
                className="bg-light-100 hover:bg-light-200 dark:bg-dark-100 dark:hover:bg-dark-200 transition duration-200 rounded-lg p-3 flex items-center justify-center text-xs text-black/50 dark:text-white/50 font-medium"
              >
                +{overflow} more
              </button>
            )}
          </div>
        )}
      </div>

      {/* Desktop: existing grid layout (hidden below sm) */}
      <div className="hidden sm:block">
        <div className="grid grid-cols-2 lg:grid-cols-3 gap-2">
          {visible.map((source, i) => (
            <SourceCard key={i} source={source} index={i} />
          ))}

          {overflow > 0 && (
            <button
              onClick={openModal}
              className="bg-light-100 hover:bg-light-200 dark:bg-dark-100 dark:hover:bg-dark-200 transition duration-200 rounded-lg p-3 flex flex-col justify-center items-start space-y-2 font-medium min-h-[88px]"
            >
              <div className="flex flex-row items-center space-x-1">
                {sources.slice(MAX_VISIBLE, MAX_VISIBLE + 3).map((source, i) =>
                  source.metadata.url?.includes('file_id://') ? (
                    <div
                      key={i}
                      className="bg-dark-200 flex items-center justify-center w-5 h-5 rounded-full"
                    >
                      <File size={10} className="text-white/70" />
                    </div>
                  ) : (
                    <img
                      key={i}
                      src={`https://s2.googleusercontent.com/s2/favicons?domain_url=${source.metadata.url}`}
                      width={14}
                      height={14}
                      alt=""
                      className="rounded h-4 w-4"
                    />
                  ),
                )}
              </div>
              <p className="text-xs text-black/50 dark:text-white/50">
                View {overflow} more
              </p>
            </button>
          )}
        </div>
      </div>

      <Transition appear show={isDialogOpen} as={Fragment}>
        <Dialog as="div" className="relative z-50" onClose={closeModal}>
          <div className="fixed inset-0 overflow-y-auto">
            <div className="flex min-h-full items-center justify-center p-4 text-center">
              <TransitionChild
                as={Fragment}
                enter="ease-out duration-200"
                enterFrom="opacity-0 scale-95"
                enterTo="opacity-100 scale-100"
                leave="ease-in duration-100"
                leaveFrom="opacity-100 scale-200"
                leaveTo="opacity-0 scale-95"
              >
                <DialogPanel className="w-full max-w-lg transform rounded-2xl bg-light-secondary dark:bg-dark-secondary border border-light-200 dark:border-dark-200 p-6 text-left align-middle shadow-xl transition-all">
                  <DialogTitle className="text-lg font-medium leading-6 dark:text-white mb-3">
                    All Sources
                    <span className="ml-2 text-sm font-normal text-black/40 dark:text-white/40">
                      {sources.length}
                    </span>
                  </DialogTitle>
                  <div className="grid grid-cols-2 gap-2 overflow-auto max-h-[360px] pr-1">
                    {sources.map((source, i) => (
                      <SourceCard key={i} source={source} index={i} compact />
                    ))}
                  </div>
                </DialogPanel>
              </TransitionChild>
            </div>
          </div>
        </Dialog>
      </Transition>
    </>
  );
};

export default MessageSources;
```

- [ ] **Step 3: Verify the file was written correctly**

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  'grep -n "sm:hidden\|isMobileExpanded\|ChevronDown\|hidden sm:block" /home/jpeetz/vane-src/src/components/MessageSources.tsx'
```

Expected output — all four strings found:
```
6:import { ChevronDown, File } from 'lucide-react';
...
  <div className="sm:hidden">
  const [isMobileExpanded, setIsMobileExpanded] = useState(false);
  <div className="hidden sm:block">
```

- [ ] **Step 4: Commit**

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  'cd /home/jpeetz/vane-src && git add src/components/MessageSources.tsx && git commit -m "feat(mobile): collapsible source pill on small screens"'
```

Expected: commit SHA printed.

---

## Task 2: Icon-only pills on mobile

**Files:**
- Modify: `src/components/MessageInputActions/ChatModelSelector.tsx`
- Modify: `src/components/MessageInputActions/Optimization.tsx`

- [ ] **Step 1: Patch the label span in ChatModelSelector.tsx**

Find the `<span>` inside the `PopoverButton` that shows the model display name. It currently reads:

```tsx
<span className="text-xs max-w-[120px] truncate">
  {activeKey ? displayName(activeKey) : 'Select Model'}
</span>
```

Change it to:

```tsx
<span className="hidden sm:inline text-xs max-w-[120px] truncate">
  {activeKey ? displayName(activeKey) : 'Select Model'}
</span>
```

Apply via SSH:

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  'sed -i "s/className=\"text-xs max-w-\[120px\] truncate\"/className=\"hidden sm:inline text-xs max-w-[120px] truncate\"/" /home/jpeetz/vane-src/src/components/MessageInputActions/ChatModelSelector.tsx'
```

- [ ] **Step 2: Verify ChatModelSelector.tsx patch**

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  'grep -n "hidden sm:inline" /home/jpeetz/vane-src/src/components/MessageInputActions/ChatModelSelector.tsx'
```

Expected: one line found containing `hidden sm:inline text-xs max-w-[120px] truncate`.

- [ ] **Step 3: Patch the label span in Optimization.tsx**

Find the `<span>` inside the `PopoverButton` that shows the mode title. It currently reads:

```tsx
<span className="text-xs font-semibold text-black dark:text-white">{activeMode.title}</span>
```

Change it to:

```tsx
<span className="hidden sm:inline text-xs font-semibold text-black dark:text-white">{activeMode.title}</span>
```

Apply via SSH:

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  'sed -i "s/className=\"text-xs font-semibold text-black dark:text-white\">{activeMode.title}/className=\"hidden sm:inline text-xs font-semibold text-black dark:text-white\">{activeMode.title}/" /home/jpeetz/vane-src/src/components/MessageInputActions/Optimization.tsx'
```

- [ ] **Step 4: Verify Optimization.tsx patch**

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  'grep -n "hidden sm:inline" /home/jpeetz/vane-src/src/components/MessageInputActions/Optimization.tsx'
```

Expected: one line found containing `hidden sm:inline text-xs font-semibold`.

- [ ] **Step 5: Commit both files**

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  'cd /home/jpeetz/vane-src && git add src/components/MessageInputActions/ChatModelSelector.tsx src/components/MessageInputActions/Optimization.tsx && git commit -m "feat(mobile): icon-only pills below 640px in home screen input bar"'
```

Expected: commit SHA printed.

---

## Task 3: Build, deploy, patch, verify

**Files:** None (build + deploy only)

- [ ] **Step 1: Build Docker image (no cache)**

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  'cd /home/jpeetz/vane-src && docker build --no-cache -t vane-local:latest . 2>&1 | tail -5'
```

Expected output ends with something like:
```
Successfully built <sha>
Successfully tagged vane-local:latest
```
This takes 3–5 minutes. Wait for it to complete before proceeding.

- [ ] **Step 2: Stop old container and start new one**

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  'docker stop vane && docker rm vane && docker run -d \
    --name vane \
    --network searxng_default \
    -p 3000:3000 \
    -e OPENAI_BASE_URL=http://172.22.0.1:5002/api/v1 \
    -e "OPENAI_API_KEY=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" \
    vane-local:latest'
```

Expected: new container ID printed.

- [ ] **Step 3: Wait for app to start, then apply 641.js scraper depth patch**

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  'sleep 25 && CHUNK_FILE=$(docker exec vane grep -rl "\.slice(0," /home/vane/.next/server/chunks/ | head -1) && docker exec vane sed -i "s/\.slice(0,3)/\.slice(0,6)/g" "$CHUNK_FILE" && echo "Patched $CHUNK_FILE: $(docker exec vane grep -c '\''slice(0,6)'\'' "$CHUNK_FILE") matches"'
```

Expected output: `Patched /home/vane/.next/server/chunks/NNN.js: N matches`

- [ ] **Step 4: Verify tier-models API is healthy**

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  'curl -s http://localhost:3000/api/tier-models | python3 -c "import json,sys; d=json.load(sys.stdin); print(list(d[\"tiers\"].keys()))"'
```

Expected: `['free', 'pro', 'scale', 'starter']`

- [ ] **Step 5: Verify mobile classes are present in the built assets**

```bash
sshpass -p 'Buddy-2019' ssh -o StrictHostKeyChecking=no jpeetz@207.180.227.214 \
  'docker exec vane grep -rl "sm:hidden\|hidden sm:block" /home/vane/.next/static/ 2>/dev/null | head -3'
```

Expected: at least one `.js` chunk file listed (confirms the mobile classes compiled into the bundle).

- [ ] **Step 6: Visual verification checklist**

Open `http://207.180.227.214:3000` in a browser. Use DevTools device emulation set to iPhone 14 (390×844):

- [ ] Home screen input bar shows `[📎] [⬡ ▾] [⚡ ▾] [↑]` — no label text visible
- [ ] Switching to desktop viewport (≥ 640px) shows `[📎] [⬡ Model Name ▾] [⚡ Search ▾] [↑]` with labels
- [ ] Run a search query — in the response, sources section shows `N sources ▾` pill (collapsed) on mobile
- [ ] Tapping the pill expands a 2-column compact grid of source cards
- [ ] Tapping again collapses the grid
- [ ] On desktop viewport, sources still render as the full 2/3-column grid (no pill)
- [ ] Model selector popover still opens and shows full model names on mobile
- [ ] Optimization popover still opens and shows mode names and descriptions on mobile
