# BetterLife Image Quality Reference — Board-Approved Standard

**Established:** 2026-07-07 by Board (Joerg)

## ✅ APPROVED — The Standard

These four Instagram posts are the quality baseline. Every generated image must match this level:

| Shortcode | Theme | Key Qualities |
|-----------|-------|---------------|
| `DaHtmlJjrE0` | Sunday Reflection | Clean, minimal abstract, calm aesthetic |
| `DadKmEUiKfK` | Abstract Geometric | Premium feel, balanced composition |
| `DaSBCo8Cp29` | Growth Thursday | Professional, on-brand |
| `DaLZYe7jgh0` | Monday Motivation | Strong visual, no clutter |

**Common qualities across all approved images:**
- No text burned into the image
- No watermarks or logo boxes
- No social handles on the image
- Clean, minimal composition
- Dark navy/indigo backgrounds
- Premium wellness app aesthetic (Calm/Headspace level)
- Eight-point compass star logo when present

## ❌ REJECTED — What NOT to Produce

| Shortcode | Issue |
|-----------|-------|
| `DaPc5qoDcU6` | PIL text overlay with Arial font, opaque watermark box with clashing star colors, amateur PowerPoint feel |

**Failure modes to avoid:**
- PIL text overlays with generic fonts (Arial)
- Opaque watermark boxes that clip into image elements
- Mismatched color schemes between watermark and main image
- Any post-processing that degrades the clean FLUX output
- Social handles burned into images (they go in captions)

## Pipeline Rules (effective 2026-07-07)

1. **FLUX output = final image.** No PIL overlays. No text. No watermark boxes.
2. **Social handles live in captions only.**
3. **Adversarial audit:** Vision model acts as critic, finds defects, rejects below-standard.
4. **Max 3 regeneration attempts.** If all fail, do NOT post — report failure.
5. **Calm/Headspace is the quality bar.** If the image wouldn't fit their feed, reject.