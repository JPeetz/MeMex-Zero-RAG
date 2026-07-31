# Project: BiteSaver

> AI Recipe Vault & Social Cooking Companion.
> **Status:** 📝 Planning (PRD complete)
> **Related:** [[Department-App-Discovery]]

---

## Core Vision

Capture → organize → auto meal plan → grocery lists → gamified social cooking (CookStreak)

## Problem

- Recipe graveyards in every phone
- Fragmented market ($2.5B by 2028)
- Nobody owns the full pipeline: capture → organize → plan → cook → share

## Solution

- AI extraction from TikTok/IG
- Auto meal plans from saved library
- Grocery lists
- CookStreak (Strava for cooking)
- Social challenges

## Competitors

| App | Weakness | BiteSaver Advantage |
|-----|----------|---------------------|
| ReciMe | $9.99/mo | Pricing at $4.99/mo (50% under) |
| Paprika | No AI extraction | AI extraction from social |
| AnyList | No meal planning | Auto meal plans |
| Mealime | Limited recipe library | Any recipe from social |
| Whisk | No social/gamification | CookStreak challenges |

## Pricing

| Tier | Price | Feature |
|------|-------|---------|
| Free | $0 | 25 recipes |
| Pro | $4.99/mo | Unlimited recipes |
| Family | $7.99/mo | Shared with family |

## Technical Foundation

- **Local-First AI:** Phi-4-mini on-device inference (from ai-agents-from-scratch repo)
- **Zero cloud inference costs** at scale — competitive moat
- **Full PRD:** MeMex `synthesis/bitesaver-prd-prompt.md`
