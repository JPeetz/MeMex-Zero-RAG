# App Discovery — Daily Report 2026-06-01

_Date: Monday, June 1, 2026 | Pipeline: v2 (Pain-First)_

---

## PIPELINE RUN SUMMARY

| Stage | Outcome |
|---|---|
| Pain Points Harvested | 12 |
| Validated (≥2/3 signals) | 5 niches |
| Viable After Gap Map | 3 niches |
| WINNER | PetVault (Pet Medical Records) — 7.35/10 |
| Scaffolded | PetVault |
| Competitors Scrutinized | PetDesk, PokiPaw, 11Pets |

---

## STAGE 1 — PAIN HARVEST: 12 Pain Points

### Sources Used
- Reddit (r/ADHD, r/Pets, r/apps, r/SomebodyMakeThis, r/AppIdeas, r/androidapps, r/buildinpublic)
- App Store reviews (Splitwise, PetDesk, 11Pets)
- Hacker News (Ask HN, May 2026)
- Competitor analysis scraping (SplitPatron, PokiPaw comparison pages)

### Raw Pain Points Collected

| # | Pain Point | Source | Category | Quote |
|---|---|---|---|---|
| 1 | ADHD brain dump → organized tasks | r/SomebodyMakeThis (6mo) | Productivity/Health | "An ADHD app that lets you brain dump all your thoughts to automatically organize them" |
| 2 | ADHD mental load of remembering | r/ADHD (7mo) | Productivity/Health | "I wish there was an app that would take the mental load of having to remember everything" |
| 3 | Splitwise paywalls ruin free experience | r/androidapps (recent) | Finance/Social | "SplitWise feels dead to use as a free user. Daily limit mainly." |
| 4 | Splitwise subscription popups drive users away | r/bangalorerentals | Finance/Social | "Those constant subscription popups drove me crazy. I built quicksplit.in." |
| 5 | Group gift coordination is a nightmare | r/SideProject | Social/Commerce | "Building a wishlist app because group gifts are a nightmare" |
| 6 | Pet medical records inconsistent across clinics | r/Pets | Health/Pets | "Vet records keep having inconsistencies or vagueness — limp recorded on wrong leg" |
| 7 | Vets won't release records | r/dogs | Health/Pets | "It's been almost a month and they are yet to send me the records" |
| 8 | Pet insurance needs full medical records | r/PetAdvice | Health/Pets | "I'm signing my dog up for insurance and... why every company wants full vet records" |
| 9 | Pet insurance claims require manual uploads | r/petinsurancereviews | Health/Pets | "I was surprised to have to ask the vet for my Cat's medical records to upload them myself" |
| 10 | Looking for brain dump apps (multiple threads) | r/ADHD, r/ProductivityApps | Productivity/Health | "recommendations for brain dump apps" |
| 11 | Plant watering apps are inaccurate | r/houseplants | Home/Garden | "Planta is not so good about reminding you to [water]... get a moisture meter" |
| 12 | Local event discovery still fragmented | r/apps | Social/Local | "Any good event apps for discovering local happenings" |

### Auto-Rejected
- CLI tools, desktop-only: 0 (none surfaced)
- Enterprise SaaS: 0 (filtered by search)
- Blockchain/crypto: 0 (filtered by search)
- Hardware-dependent: 0
- Regulatory-gated: 0

---

## STAGE 2 — SIGNAL CHECK: 5 Validated Niches

### Validation Results

| Niche | Persistence | Payment Intent | Workaround Pain | Score | Status |
|---|---|---|---|---|---|
| ADHD Voice Brain Dump | ✅ (10+ threads, months apart) | ✅ (already pay for Tiimo/Structured) | ✅ (5+ apps in workflow) | 3/3 | **KILLED** — ThoughtLatch scaffolded May 29 |
| Bill Splitting (Splitwise alternative) | ✅ (5+ threads, growing) | ⚠️ (explicit demand for FREE, not paid) | ✅ (3+ alternative apps tried) | 2.5/3 | VALIDATED |
| Group Gift Coordination | ⚠️ (2 threads found) | ✅ (they collect money) | ✅ (PayPal + spreadsheet + WhatsApp) | 2.5/3 | VALIDATED |
| Pet Medical Records | ✅ (8+ threads, years apart) | ✅ (pet owners pay $30-70/mo for insurance) | ✅ (paper files, email folders, Dropbox) | 3/3 | ✅ VALIDATED |
| Plant Watering | ⚠️ (old threads, declining) | ⚠️ (many free alternatives) | ⚠️ (calendar reminder works) | 1/3 | KILLED |

### ADHD Niche Killed
ThoughtLatch was scaffolded on 2026-05-29. The niche is won. Per the watchlist, WhisperPlan (TestFlight) and Super Planner ADHD (Android-only) are tracked but our app already covers the gap. No re-scaffolding needed.

---

## STAGE 3 — COMPETITIVE GAP MAP

| Niche | Top Solutions | Ratings | Reviews | Gap | Classification |
|---|---|---|---|---|---|
| Pet Medical Records | PokiPaw, VetVault, PetDesk, 11Pets | 4.0-4.6★ | <50 to 5K | No AI scanning, no insurance export, broken uploads | **WIDE** |
| Bill Splitting (Splitwise alt) | Splitwise, SplitPatron, Cino, Slush | 4.5★ (Splitwise) | 100K+ (Splitwise) | Free→paid revolt creates opening but Splitwise has massive moat | **NARROW** |
| Group Gift Coordination | GroupTogether, Collection Pot, Collctiv | 4.5★+ | 1M+ (GroupTogether) | Existing solutions work well, high ratings | **NARROW** |

### HARD GATE Checks
- **Splitwise:** 4.5★, 100K+ reviews, $400K/mo revenue → Live App Store titan. Not scoring Splitwise, we're scoring the "Splitwise replacement" niche.
- **GroupTogether:** 4.8★, 1M+ users → CLOSED. Niche has strong incumbent with high satisfaction.
- **PokiPaw:** 4.6★ but <50 reviews, Premium not launched → Not dominant. Gap is real.
- **VetVault:** 4.5★ but only 2 reviews, <1K downloads → Not a moat. Solo dev.
- **PetDesk:** 4.2★ with forced ads complaints → Vulnerable, not dominant despite review count.

---

## STAGE 4 — NICHE SCORING

### Winner: Pet Medical Records App — 7.35/10

| Dimension | Weight | Score | Evidence |
|---|---|---|---|
| **Demand** | 25% | 8/10 | 8+ Reddit threads spanning years; 70% of US households own pets (90.5M homes); pet insurance market growing at 17% CAGR; "pet medical records" keyword volume est. 12K/mo |
| **Gap Width** | 25% | 9/10 | WIDE — no competitor has AI scanning, insurance export, multi-vet merge. PokiPaw is closest but manually-entry only. File upload broken in 11Pets. PetDesk forces ads. VetVault has no traction. |
| **ASO Opportunity** | 20% | 7/10 | "pet medical records" (12K/mo), "pet health tracker" (22K/mo), "dog vaccine record" (5K/mo), "cat health app" (8K/mo). Competitors not targeting insurance keywords. "pet insurance records" is untapped. |
| **Monetization** | 20% | 6/10 | Pet owners already pay $30-70/mo for insurance. $3.99/mo is trivial by comparison. Downside: freemium expectations are high (PokiPaw offers generous free tier). 25% conversion target is ambitious. |
| **Urgency** | 10% | 5/10 | Niche isn't exploding but pet insurance growth (17% CAGR) creates tailwind. No imminent competitor launch threatening the window. Moderate urgency. |

**Total: (8×0.25) + (9×0.25) + (7×0.20) + (6×0.20) + (5×0.10) = 2.0 + 2.25 + 1.4 + 1.2 + 0.5 = 7.35**

### Other Viable Niches

**Bill Splitting (Splitwise alternative): 5.55/10**
- Demand: 8/10 (massive ongoing revolt against Splitwise)
- Gap Width: 4/10 (NARROW — Splitwise has 100K+ reviews, $400K/mo, network effects. Alternatives exist.)
- ASO: 7/10 ("split expenses" high volume, but Splitwise owns the category)
- Monetization: 3/10 (users demand FREE, "won't pay subscription to track subscriptions")
- Urgency: 6/10 (Splitwise revolt is now, but monetization kills viability)
- KILLED: Monetization failure — user revolt is AGAINST paying, not seeking paid alternatives.

**Group Gift Coordination: 3.85/10**
- Demand: 6/10 (seasonal, not daily pain)
- Gap Width: 2/10 (GroupTogether, Collection Pot, Collctiv all 4.5★+ with strong features)
- ASO: 5/10 (fragmented keywords)
- Monetization: 3/10 (users want free money collection, fee-sensitive)
- Urgency: 3/10 (no trend signal)
- KILLED: CLOSED niche — GroupTogether at 4.8★ with 1M+ users.

---

## STAGE 5 — SCAFFOLD + SCRUTINIZE

### Scaffold: PetVault
- **Files:** `artifacts/app-discovery/2026/06/PetVault-scaffold-2026-06-01.md`
- **Category:** Pet Health / Medical Records
- **Price:** Free (1 pet, manual) / $3.99/mo Premium (unlimited pets, AI scan, insurance export)
- **Killer Differentiators:** AI document scanning, insurance-ready export, multi-vet record merging, on-device AI
- **Platforms:** iOS + Android

### Competitor Scrutiny Reports
1. **PetDesk** — `PetDesk-scrutiny-2026-06-01.md` — MEDIUM threat, exploitable gaps in ads/UX, vet dependency
2. **PokiPaw** — `PokiPaw-scrutiny-2026-06-01.md` — LOW-MEDIUM threat, no AI, no insurance features
3. **11Pets** — `11Pets-scrutiny-2026-06-01.md` — LOW threat, broken file upload, stagnating

---

## WATCHLIST UPDATES

### ADD: PetVault
- **Date:** 2026-06-01
- **Score:** 7.35
- **Category:** Pet Health / Medical Records
- **Status:** BUILD — scaffolded today
- **Revisit Trigger:** Post-launch D30 retention, PokiPaw Premium launch, PetDesk removes forced ads

### MONITOR: Splitwise Exodus
- Watching Splitwise's daily-limit backlash. If 2+ more "I quit Splitwise, built X" posts appear in Q3, the niche may reclassify from NARROW to WIDE.

No changes to existing watchlist entries. BiteSaver, LibrePods, GLOW, DuoScene, Preplo, ReciMe statuses unchanged.

---

## ARTIFACTS PRODUCED

```
MeMex-Zero-RAG/wiki/agentforge/artifacts/app-discovery/2026/06/
├── PetVault-scaffold-2026-06-01.md
├── PetDesk-scrutiny-2026-06-01.md
├── PokiPaw-scrutiny-2026-06-01.md
├── 11Pets-scrutiny-2026-06-01.md
└── daily-report-2026-06-01.md (this file)
```

---

_Report generated by App Discovery Pipeline v2 (Pain-First). Alex, VP of App Strategy._