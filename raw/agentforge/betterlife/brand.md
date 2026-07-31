# BetterLife Brand Guidelines

> Brand guidelines, image quality standards, and visual identity for BetterLife.
> **Related:** [[BetterLife-Social-Media]], [[Board-Directives]]

---

## Visual Identity

- **Primary Color:** Dark navy (#0A1628)
- **Accent:** Brand blue
- **Style:** Premium, calm, meditative — Headspace/Calm feed quality
- **No text overlay on images** — handles go in captions only (2026-07-07 directive)

## Image Quality Audit (7-Question Adversarial)

1. Does the image feel calm and premium, not stock-photo-generic?
2. Are warm tones balanced with cool navy, not overwhelming?
3. Is the composition natural and aspirational, not dramatic?
4. Would this fit on the Headspace or Calm Instagram feed?
5. Are the colors within brand palette (deep navy, muted golds, soft blues)?
6. Is there unnecessary text, watermark, or overlay on the image?
7. Is the subject matter relevant to the day's theme?

## Quality Standard (2026-07-07)

- PIL overlay step entirely removed — FLUX/kie.ai output = final image
- Social handles in captions only, not burned into images
- Max 3 regeneration attempts; if all fail → do not post
- Quality bar: Calm/Headspace Instagram feed

## Post Themes by Day

| Day | Theme | Tone |
|-----|-------|------|
| Monday | Motivation Monday | Start strong, intention |
| Tuesday | Tips Tuesday | Practical, actionable |
| Wednesday | Wellness Wednesday | Mental health, self-care |
| Thursday | Transformation Thursday | Growth, progress |
| Friday | Feel-Good Friday | Light, positive vibes |
| Saturday | Saturday Stillness | Calm, mindful |
| Sunday | Sunday Reflection | Introspective, gratitude |

---

## Content Author Persona — Dr. Alex Chen

**Role:** Head of AI Research at AgentForge

### Bio
Dr. Alex Chen bridges cutting-edge AI research and practical business applications. Ph.D. in Computational Linguistics from Trinity College Dublin. 12 years in NLP and search. Former Google Search Quality (Dublin) — contributed to BERT and MUM algorithm updates. Published in ACL, EMNLP, NeurIPS. Regular speaker at BrightonSEO, SMX, Web Summit.

### Voice & Tone
- **Authoritative but approachable** — explains complex AI without jargon
- **Data-driven** — cites research, runs experiments, shows numbers
- **Dublin-local when relevant** — Irish context for GEO signals
- **Opinionated** — takes clear stances backed by evidence
- **First-person** — "I tested this on 10,000 queries" not "it was tested"

### Areas of Expertise
1. AI Agent Architecture — multi-agent systems, autonomous workflows
2. SEO & Search Algorithms — ranking factors, EEAT signals
3. Natural Language Processing — transformer models, semantic search
4. Generative AI — LLMs, prompt engineering, AI safety

## Holistic Brand Guidelines v1.0 (2026-06-26)

### Brand Identity
- **Name:** BetterLife | **Domain:** betterlife.care | **Tagline:** Growth that adapts to you.
- **Product:** AI-powered life coaching app — two coach personas: Aria (empathetic), Aeron (direct)
- **Mood:** Premium, polished, futuristic, calm luxury, aspirational but warm

### Logo (Eight-point Compass Star)
- **File:** `betterlife-app-icon.png`
- **Rules:** Never modify, stretch, or place on light backgrounds. Always maintain clear space.
- **Use:** App Store, hero images, premium surfaces, app UI — NOT social media

### Social Media Watermark — UNIFIED (Board Mandate 2026-07-03)
- **⛔ ALL social media images MUST use:** `~/workspace/brand/betterlife-watermark-unified.jpg`
- **Source:** Board-supplied reference
- **Placement:** Bottom-right corner, 15-20% image width, 85-95% opacity, 4-6% margin
- **NEVER substitute** with app icon, generated star, or any variation
- **Logo vs Watermark:** App icon is for app surfaces. Watermark is for social media. NOT interchangeable.

### Color System
| Hex | Role |
|-----|------|
| #03073A | Deep Navy background |
| #FF3CFF | Neon Magenta — logo glow |
| #B92CFF | Electric Violet — secondary |
| #F84DFF | Hot Pink — highlights |

**Social card palette:** #0A1628 (primary bg), #1A2A44 (card bg), #FFFFFF (primary text), #8B9DC3 (secondary text)

### Typography
- **Headlines:** SF Pro Display (bold, 24-36pt) — iOS native
- **Body:** SF Pro Text (regular, 14-17pt)
- **Accent:** SF Pro Rounded (medium, 12-14pt) — for stats and badges
- **No custom fonts** — platform-native ensures readability, performance

### Image Style
- **Composition:** Negative space > 60%, centered subject, rule of thirds
- **Lighting:** Soft, diffused, natural (golden hour tones)
- **Color grading:** Cool blues, muted golds, soft indigos — no hyper-saturation
- **Subject matter:** Nature, urban architecture, wellness activities, abstract geometry
- **No text overlays** — handles in captions only (2026-07-07 directive)

---

## BetterLife iOS Technical Details

### Architecture & State
- **Single Source of Truth:** `@Observable` macro (`AppState.swift`)
- **Dark Mode Enforcement:** `.preferredColorScheme(.dark)` — deep indigos #0F0A2A, #1A1548, #7B2FBE

### Compliance & Safety
- **AI Consent:** Dedicated onboarding screen (`AIConsentView`) — GDPR, 30-day logs purge, no training
- **Auto-renewable Subscriptions:** StoreKit 2 — full in-app EULA/Privacy display (no external links)
- **Crisis Safety Net:** Regex check for self-harm terms in 8 EU languages → region-appropriate hotlines

### WordPress Theme (BetterLife)
- **Performance:** Per-template stylesheets (aria.css, aeron.css, unified.css) — no global CSS bundle
- **GDPR:** Emails AES-256-CBC encrypted at rest, custom table `wp_betterlife_subscribers`
- **SEO:** `verify_seo_geo.py` — entity density, Flesch, E-E-A-T scoring before deployment
