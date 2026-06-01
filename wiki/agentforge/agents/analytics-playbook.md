# Analytics — Playbook

_Cross-department pattern detection._

## Drift Patterns Detected
- **SEO audit single-point-of-failure (Jun 1):** Pipeline's only quality gate depends on one API (seo-api-nu.vercel.app). When it goes 404, ALL downstream stages block (social, PDF, WordPress). No fallback audit path exists. This is the #1 drift pattern — service dependency without redundancy.
- **Part B fragmentation (Jun 1):** Image generation + SEO + PDF + git stages consistently fail when bundled in a single cron. Splitting into Part A (text) and Part B (tools) is architecturally correct but Part B crons are NOT consistently created or executed. Result: articles exist in MeMex but are invisible (no images, no PDFs, no git).
- **Dual-write decay (recurring):** MeMex → Obsidian mirror degrades steadily between weekly reports. Each run that doesn't explicitly sync widens the gap. Standing orders need hard enforcement, not best-effort guidance.
- **Learning loop atrophy (recurring):** Architecture documented May 24. Phase 1 never executed. Proposed patches never applied. The loop exists on paper only — token cost of weekly execution is trivial but habit hasn't formed.

## Agent Failure Patterns
- **Content agent Part B skip (May 27):** Single occurrence — model exhausted resources after 3,000-word article when a single cron also demanded image gen + SEO + PDF + git. Fixed by splitting into Part A/B. Has not recurred.
- **Content agent self-improvement (positive):** From Run #2 onward, content agent self-applies pre-SEO checks (meta description, hyperlinks, readability interludes, GEO blocks) WITHOUT the external gate functioning. This is autonomous learning from a single FLAG event.
- **SEO agent structural block (not a failure):** Agent has never failed — it has never been invoked since May 23 because the API it depends on is down. This is infrastructure, not agent performance.

## Cluster Performance
- **Enterprise Agent Lifecycle (5 articles):** Complete. Strong editorial arc (Build → Control → Measure → Deploy → Choose Tools). Highest structural quality cluster. 0/5 externally audited.
- **AI Agent Security (2 articles):** Active. Well-timed (OWASP ASI Top 10 fresh, 340% attack surge). Well-researched (multi-source Tavily pattern). 0/2 externally audited.

## Recommendations That Stuck
- **Part A/B split (May 27):** Applied immediately after Run #4 failure. Content playbook updated. All subsequent runs use the split. This is the first operational fix that actually shipped and held.
- **Pre-SEO self-checks (May 25+):** Content agent internalized Run #1's FLAG lessons. All articles from Run #2 onward include meta descriptions, 15-30+ hyperlinks, readability interludes, and GEO blocks — without being told. The learning signal propagated correctly.
