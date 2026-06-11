# Helix Phase 5 — Mobile Responsiveness Design

**Date:** 2026-06-11
**Status:** Approved
**Project:** Helix (custom Perplexica build on `vmi1593174.contaboserver.net`)
**Source tree:** `/home/jpeetz/vane-src/`
**Running container:** `vane-local:latest`

---

## Goal

Make Helix usable on regular mobile phones (375px–430px screens) with three targeted changes:

1. Sources block collapses to an inline collapsible pill on mobile
2. Home screen input bar collapses Model and Optimization pills to icon-only on mobile
3. Follow-up input bar is left unchanged (already correct)

No new libraries. No layout rewrites. All changes are additive Tailwind breakpoint classes and small component logic additions.

---

## Decisions

| Question | Decision | Reason |
|---|---|---|
| Source panel pattern | Inline collapsible pill (B) | No overlay, no drawer — stays in scroll flow, familiar expand/collapse |
| Input bar on mobile | Icon-only pills below 640px (B) | 4 items crowd on 375px; collapsing labels frees ~140px while popovers still show full names |
| Follow-up input bar | No changes | Only 3 items — no crowding; model is sticky by Phase 4 design |
| Breakpoint | `< 640px` (`sm:` in Tailwind) | Standard Tailwind small breakpoint; covers all common phones up to tablet |

---

## Visual Behavior

### Sources — inline collapsible pill

**Mobile (`< 640px`):**
```
[ 6 sources ▾ ]          ← collapsed (default)

[ 6 sources ▴ ]          ← after tap
┌─────────────┬─────────────┐
│ [1] wiki…   │ [2] tech…   │
│ [3] reut…   │ [4] bbc…    │
│ [5] guar…   │ [6] cnn…    │
└─────────────┴─────────────┘
```

- Pill: `text-sm font-medium` with chevron that rotates 180° when expanded
- Expanded: 2-column compact grid, same `SourceCard` component reused with `compact={true}` prop
- `compact` prop already exists on `SourceCard` — removes `min-h-[88px]`
- Collapsed by default; state local to the component

**Desktop (`≥ 640px`):** existing sticky sidebar panel, unchanged.

### Home screen input bar — icon-only pills

**Mobile (`< 640px`):**
```
[ 📎 ] [ ⬡ ▾ ] [ ⚡ ▾ ]          [ ↑ ]
```

**Desktop (`≥ 640px`):**
```
[ 📎 ] [ ⬡ Gemini 2.5 Flash ▾ ] [ ⚡ Speed ▾ ]   [ ↑ ]
```

- Model selector label: `<span className="hidden sm:inline truncate max-w-[120px]">{displayName}</span>`
- Optimization label: `<span className="hidden sm:inline">{modeLabel}</span>`
- Icons stay visible at all sizes; only the text label is hidden on mobile
- Both popovers continue to show full names and labels when open — no information loss

### Follow-up input bar

No changes. `MessageInput.tsx` has `[📎] [⚡ Speed ▾] [↑]` — 3 items, fits comfortably on all phones.

---

## Component Changes

### 1. `src/components/MessageSources.tsx`

**What changes:**
- Add `isExpanded` state (default `false`)
- On mobile (`className` conditional driven by Tailwind breakpoint), render:
  - A pill button: `N sources ▾/▴` that toggles `isExpanded`
  - When expanded: 2-column grid of `SourceCard compact={true}`
- On desktop (`sm:` prefix): render existing layout unchanged

**What stays the same:** `SourceCard` component, `MAX_VISIBLE` logic, dialog for full source view.

**Implementation note:** Use a wrapper `<div>` that switches between mobile and desktop rendering using `sm:hidden` / `hidden sm:block` classes — no JS breakpoint detection needed.

```tsx
{/* Mobile: collapsible pill */}
<div className="sm:hidden">
  <button onClick={() => setIsExpanded(!isExpanded)} ...>
    {sources.length} sources {isExpanded ? '▴' : '▾'}
  </button>
  {isExpanded && (
    <div className="grid grid-cols-2 gap-2 mt-2">
      {sources.slice(0, MAX_VISIBLE).map((s, i) => (
        <SourceCard key={i} source={s} index={i} compact />
      ))}
    </div>
  )}
</div>

{/* Desktop: existing layout */}
<div className="hidden sm:block">
  {/* existing source panel JSX */}
</div>
```

### 2. `src/components/MessageInputActions/ChatModelSelector.tsx`

**What changes:** The display name `<span>` inside the pill trigger gets `hidden sm:inline`:

```tsx
{/* Before */}
<span className="truncate max-w-[120px] text-xs">{displayName(chatModelProvider.key)}</span>

{/* After */}
<span className="hidden sm:inline truncate max-w-[120px] text-xs">{displayName(chatModelProvider.key)}</span>
```

The `Cpu` icon and chevron remain visible at all sizes.

**What stays the same:** Popover content, model selection logic, localStorage persistence, all existing behavior.

### 3. `src/components/MessageInputActions/Optimization.tsx`

**What changes:** The mode label text inside the pill trigger gets `hidden sm:inline`:

```tsx
{/* Before */}
<span className="text-xs capitalize">{optimizationMode}</span>

{/* After */}
<span className="hidden sm:inline text-xs capitalize">{optimizationMode}</span>
```

The mode icon remains visible at all sizes.

**What stays the same:** Popover, mode switching logic, all existing behavior.

---

## Files Changed Summary

| File | Type of change |
|---|---|
| `src/components/MessageSources.tsx` | Add mobile collapsible pill, keep desktop layout |
| `src/components/MessageInputActions/ChatModelSelector.tsx` | Hide label text below 640px |
| `src/components/MessageInputActions/Optimization.tsx` | Hide label text below 640px |

**Requires Docker image rebuild** — all three files are compiled into the Next.js bundle.
**641.js scraper patch** must be re-applied after container recreation.

---

## Out of Scope

- Follow-up input bar (`MessageInput.tsx`) — no changes
- Sidebar / bottom nav — already mobile-responsive, no changes
- Settings, Library, Discover pages — out of scope for this phase
- Font size scaling — no changes
- Touch gesture swipe for sources — out of scope

---

## Success Criteria

- On a 375px screen, the sources block shows as a collapsed pill by default
- Tapping the pill expands a 2-column source grid; tapping again collapses it
- On a 375px screen, the home screen input bar shows `[📎] [⬡ ▾] [⚡ ▾] [↑]` with no text overflow
- On a desktop/tablet (≥ 640px), all labels are visible and layout is unchanged
- Model selector and Optimization popovers still show full names and labels when opened on mobile
- No regressions on desktop layout
