# Social Distribution Patterns — AgentForge

_Learned patterns and outcomes from post-publication social distribution. Updated after each distribution cycle._

---

## Pattern Log

### 2026-05-23 — "AI Agent Orchestration in 2026: The Enterprise Guide"

**Article:** `ai-agent-orchestration-2026` | **Keyword:** AI Agent Orchestration | **SEO Score:** 79/100
**Artifact:** `sd-f3a9b4c2-d6f7-4a8e-b10c-4e7f3d5a6103`

**Platform Adaptations:**

| Platform | Format | Key Insight |
|----------|--------|-------------|
| Reddit | r/LocalLLaMA — self-post, value-first, personal production experience | Emphasized self-hosted angle (n8n) to fit community ethos. Led with the 1.7% vs 100% actionable-rate stat for hook. Honest about NOT needing multi-agent. Backed by personal pipeline anecdote. |
| Hacker News | Show HN — pipeline as the "thing built" | Led with production credibility. Avoided all marketing language. Emphasized architecture, real trade-offs, and the contrarian "start with one agent" take. |
| X/Twitter | 5-tweet thread — hook → patterns → decisions → frameworks → close | Opener uses shock stat (1.7% vs 100%). Middle tweets deliver substance compressed to ~270 chars each. Final tweet is contrarian take + link. Hashtags only on last tweet. |
| LinkedIn | 174-word professional post — data-forward, bold claim opener | Professional tone. Starts with "single-agent era is ending" claim, immediately backs with data. Delivers framework names and decision count for credibility. Closes with actionable contrarian take. |
| Dev.to | Cross-post with canonical URL | Full article content, canonical URL preserved. Tags: ai, agents, orchestration, enterprise, architecture. Dev.to renders existing Markdown (tables, code blocks) natively. |

**Patterns Learned:**

1. **Statistic-led hooks work across platforms** — the 1.7% vs 100% actionable-rate stat was the anchor for Reddit, HN, and Twitter. Powerful single-number comparisons are portable.
2. **Contrarian take as memorable close** — "most teams don't need multiple agents" is counterintuitive and memorable. Used as close on Twitter and LinkedIn, worked as discussion starter on Reddit.
3. **Platform-specific angle matters** — Reddit got the self-hosted angle (n8n), HN got the architecture depth, LinkedIn got the enterprise implications. Same article, different framing.
4. **Reddit value-first rule** — never lead with a link. Self-post format with personal experience draws engagement. Bare links get removed or ignored.
5. **HN doesn't tolerate marketing** — Show HN format works only because we're showing the production pipeline, not selling. Emphasized technical depth and honest trade-offs.
6. **Twitter thread density** — each tweet needed to deliver one complete idea while fitting in ~270 chars. The structure (hook → substance ×3 → close) compresses well.
7. **LinkedIn wants data + implications** — enterprise audience responds to "Gartner says 40%..." more than "here's a cool framework." Frame as industry shift, not tool tutorial.
8. **Dev.to canonical URLs are critical** — always include `canonical_url` in front matter to preserve SEO credit for the original post on agent-forge.co.

**Posting Order Rationale:** Reddit + HN first (generate discussion, set the narrative), then Twitter + LinkedIn (broadcast), Dev.to last (long-tail SEO cross-post).

**Approval Gate:** SEO 79 → CEO review required. Below ≥80 full-auto threshold.

---

## Template: Distribution Checklist (per article)

```
□ Read article + content artifact + SEO audit
□ Adapt for Reddit (target subreddit by topic)
□ Adapt for Hacker News (Show HN if applicable)
□ Adapt for X/Twitter (3-5 tweet thread)
□ Adapt for LinkedIn (150-200 words, professional)
□ Adapt for Dev.to (canonical URL in front matter)
□ Verify: no bare links on Reddit
□ Verify: no marketing on HN
□ Verify: canonical URL on Dev.to
□ Produce social.distribution artifact to MeMex
□ Log patterns to this file
□ Handoff → PDF Agent (via next_steps)
```
