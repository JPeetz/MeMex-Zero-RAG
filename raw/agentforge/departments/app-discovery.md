# Department: App Discovery

> **Lead:** Alex, VP App Strategy
> **Pipeline:** Scout → GEO → Score → Scrutiny → Build → Report
> **Related:** [[Project-BiteSaver]], [[Departments]]

---

## Pipeline (6 Phases)

| Phase | Description |
|-------|-------------|
| 1. Scout | 30 apps daily from Product Hunt, HN, App Store |
| 2. GEO | Geographic optimization check |
| 3. Score | 10-dimension scoring with mobile-first filter |
| 4. Scrutiny | Deep dive into top app |
| 5. Build (Scaffold) | Superhuman scaffolding prompt — 12-section blueprint |
| 6. Report | Full report with mobile-first analysis |

## Mobile-First Filter (2026-05-24 fix)

Added after a dev tool (Forge) was incorrectly scored:
- **Mobile-First Fit dimension** (10%) with 6/10 kill floor
- Auto-reject: CLI, SDK, desktop-only, Chrome extensions without mobile companion
- HN scanning now filters for mobile-only

## Scoring Dimensions

| Dimension | Weight |
|-----------|--------|
| Mobile-First Fit | 10% |
| Market Size | — |
| Problem Validation | — |
| Competitive Gap | — |
| SEO/ASO Potential | — |
| Revenue Model | — |
| Technical Feasibility | — |
| Viral Potential | — |
| Team Fit | — |
| Personal Interest | — |

## Scaffolding Prompt (Phase 6)

Built 2026-05-24: 505-line superhuman initial prompt for iOS + Android development:
12 sections covering: identity, iOS architecture, Android architecture, SEO/GEO, behavioral hooks, visual design, financial model, virality, technical spec, 30-day sprint, launch checklist, anti-patterns.

**Location:** `~/.openclaw/agents/app-discovery/scaffolding-prompt.md`

## Key Tests

| Date | App Scored | Result | Note |
|------|-----------|--------|------|
| 2026-05-24 | Forge (CLI dev tool) | ❌ Killed | Not mobile — added Mobile-First filter |
| 2026-05-24 | BiteSaver | ✅ 7.30/10 | Valid mobile app, full scaffold produced |
| 2026-05-29 | RaceIntel | ✅ 7.25/10 | Horse racing, full scrutiny report |
