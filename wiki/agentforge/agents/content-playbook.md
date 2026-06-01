# Content Pipeline — Playbook

_Lessons that carry forward across pipeline runs. Read before each run, update after._

## Architecture (as of 2026-05-29)
- **Part A (08:30):** keyword → article → image prompt only. Article .md + artifacts written to MeMex.
- **Part B (09:15):** image generation → pipeline copy → PDF → SEO audit → git commit. Tool-heavy, must complete all steps.
- Split because single cron failed at image generation — the model writes the full article then considers task "done."
- Never put image_generate + article writing in the same cron — tool generation commands need their own isolated run.
- After completing a series arc (all 5 parts), pivot to a new cluster — do not force continuation.
- **SEO API fallback:** seo-api-nu.vercel.app has been unreliable (404s on all endpoints as of May 29). If it returns 404, fall back to Tavily web search for keyword research + deep source fetching via web_fetch.
- **Part A (08:30):** keyword → article → image prompt only. Article .md + artifacts written to MeMex.
- **Part B (09:15):** image generation → pipeline copy → PDF → SEO audit → git commit. Tool-heavy, must complete all steps.
- Split because single cron failed at image generation — the model writes the full article then considers task "done."
- Never put image_generate + article writing in the same cron — tool generation commands need their own isolated run.

## What Works
- Keyword research with SEO API produces strong clusters
- Series format (Orchestration → Governance → Evaluation → Deployment) builds editorial momentum and internal link equity
- GEO blocks (definition, FAQ, quotable summary, featured image) consistently met
- Article quality: 2,800-3,000 words, 10-11 H2s, 15+ hyperlinks, 2+ tables

## What Failed
- Run #4 (May 27): image generation, SEO audit, PDF all skipped — cron completed after writing article draft
- Root cause: single cron asking for 6 tool-heavy stages in one prompt. Model writes 3,000 words then returns.
- Fix: split into Part A (text) + Part B (tools). Effective immediately.

## Image Prompts That Scored Well
- Run #4: "Enterprise AI agent deployment infrastructure visualization. Dark blue technological dashboard, glowing nodes, Kubernetes-style cluster, central holographic globe, blue and teal gradients." — Generated well on gemini-3.1-flash-image-preview.
- Run #5: "Six connected AI agent framework nodes as glowing geometric icons in radial cluster arrangement on dark blue/teal gradient with hexagonal grid background. HUD-style overlay panels. Cinematic volumetric lighting." — Designed for 16:9 landscape; the radial six-node design directly maps to the six frameworks compared.

## New Patterns That Worked
- **draft_pending_image status:** Explicit artifact status for Part A→B handoff. Part B reads artifacts with this status to find its work queue.
- **Five-part lifecycle series structure:** Orchestration (why) → Governance (how to control) → Evaluation (how to measure) → Deployment (how to ship) → Frameworks (what tools). The framework piece converts readers into action-takers.

## SEO Patterns
- FLAG (50-69): auto-revision typically 1 cycle to PASS. Common fixes: add meta description, hyperlinks, improve Flesch score.
- Title <60 chars for SERP. Meta description 150-160 chars with keyword + CTA.
- B2B enterprise articles naturally score Flesch 24-35 — this is acceptable for technical/CTO audience

## Keyword Clusters That Performed
- "AI agent production deployment scaling enterprise" — Run #4, high commercial intent, 4,800-7,200/mo combined
- Series cross-linking boosts cluster authority across runs
- When a series arc completes (5 parts), the final article should include a full series recap with links to all prior pieces — this creates a navigable hub page effect
- Framework comparison format (6+ products in a decision matrix) generates high commercial intent and outsized backlink potential
- Tagging articles with 'draft_pending_image' status makes the Part A→Part B handoff explicit — Part B knows exactly which article to process
- MCP (Model Context Protocol) adoption by multiple frameworks in H1 2026 is the angle that differentiates a frameworks article from older comparison pieces — lead with it

## Pipeline Timings
- Part A: ~6-8 minutes (keyword research + article writing)
- Part B: ~8-12 minutes (image gen + PDF + SEO + git)
- Total pipeline: ~15-20 minutes fully automated

## Lesson Log
### Run #5 (May 28) — Multi-Agent AI Frameworks
1. **Series arc completion strategy:** When a planned lifecycle series ends, the final article should explicitly recap all prior entries with links. This creates a self-contained resource cluster that search engines treat as authoritative on the topic.
2. **Framework comparison articles are their own format:** Unlike explanatory articles (Runs #1–4), comparison articles need a decision matrix table, per-framework deep dives, and an explicit "pick X if Y" framework. The CTA is procurement, not education — structure accordingly.
3. **MCP as differentiator:** Articles about multi-agent frameworks published before mid-2026 missed the MCP interoperability story. Writing after MCP adoption by CrewAI, MS Agent Framework, and Vercel AI SDK makes the article current and referenceable.

### Run #6 (May 29) — AI Agent Security (New Cluster Start)
1. **Pivot strategy after series completion:** When a 5-part lifecycle series ends, the next article should address the #1 blocker for the prior content's audience. After Orchestration → Governance → Evaluation → Deployment → Frameworks, the natural question is "how do I secure all of this?" Security is the gatekeeper topic — the article CISOs read before approving any of the architecture in Runs #1–5. Pivot to the blocker, not a random adjacent topic.
2. **OWASP ASI Top 10 as article backbone:** Having an industry-standard framework (OWASP ASI01–ASI10) to structure the article around makes writing dramatically faster and the output more authoritative. Search for relevant standards/frameworks before committing to a cluster — they become the skeleton the article hangs on.
3. **SEO API degraded — web search fallback works:** The seo-api-nu.vercel.app returned 404s on all endpoints during this run. Web search (Tavily) provided sufficient keyword research and source material. Fallback should be automatic: try SEO API, if 404 → web search for keyword research + deep source fetching.

### Run #7 (June 1) — Prompt Injection Defense (Security Cluster Part 2)
1. **Series deep-dives need the Progressive Breach Model as framing:** A Part 2 tactical deep-dive ("how do I actually defend against X") is more compelling when structured around a breach progression model rather than a flat taxonomy. Lakera's 4-phase model (Compromise Mind → Convert Autonomy → Propagate → Lose Containment) gave the article narrative momentum that a simple "7 layers" list wouldn't have. Every defense layer then answers a specific phase of the breach chain.
2. **Tavily multi-query research pattern:** When SEO API is down, run 3 parallel Tavily searches at different angles (general topic, specific vulnerability, vendor comparison) then deep-fetch the top 3-4 sources. This produces richer source material than a single broad search. The Penligent, Lakera, and Alex Ewerlöf sources each contributed distinct and non-overlapping insights.