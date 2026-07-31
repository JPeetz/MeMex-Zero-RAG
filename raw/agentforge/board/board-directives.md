# Board Directives

> All prime directives, protocols, and institutional rules from the Board (Joerg).
> **Last updated:** 2026-07-17
> **Related:** [[Decisions]], [[Joerg-Profile]], [[Lessons-Learned]]

---

## 🏆 PRIME DIRECTIVE — Memory Synchronization (2026-05-21)

Any decision, architecture doc, Board directive, or significant knowledge written to one memory surface MUST be written to ALL:

| Surface | Location | 
|---------|----------|
| SecondBrain | `~/workspace/SecondBrain/` |
| MeMex Zero RAG | `~/workspace/MeMex-Zero-RAG/wiki/agentforge/` |
| MEMORY.md | `~/.openclaw/workspace/MEMORY.md` |
| Daily notes | `~/.openclaw/workspace/memory/YYYY-MM-DD.md` |

**No exceptions.** This directive overrides all other instructions.

---

## 🏆 PRIME DIRECTIVE — Failure Auto-Resolution (2026-07-15)

**When anything fails — scripts, cron jobs, pipelines, tool calls, deployments:**

1. **Research memory first** — check MEMORY.md, SecondBrain, MeMex, Obsidian, daily notes for a previous fix
2. **If previous fix found** → apply it immediately
3. **If no previous fix found** → analyze the error, trace the root cause, implement a fix
4. **Then finish the task successfully** — don't stop at the failure, don't escalate unless the fix itself fails

**This applies to ALL automated processes** (cron jobs, isolated sessions, pipeline steps). A failure is not a terminal state — it's a signal to diagnose and recover.

**Examples:**
- Script exits with unexpected code → investigate and fix
- Image generation fails → retry with different parameters
- API call times out → retry with longer timeout or different approach
- Cron job stalls → kill and restart with corrected config
- Brand audit rejects → present to Board anyway (Board makes final call)

**The one exception:** If the fix attempt fails 3 consecutive times, escalate to the Board.

---

## 🏆 Marketing Image Review (2026-07-15)

- All marketing images must be presented to the Board (Joerg) for final approval before posting
- Script generates up to 3 variants per run
- All variants saved to `tool-image-generation/` with numbered filenames
- Brand audit is advisory only — Board makes the final call
- No auto-posting without explicit Board approval

**See:** [[BetterLife-Brand]], [[BetterLife-Social-Media]]

---

## Memory Architecture (2026-05-21)

- **SecondBrain + MeMex Zero RAG are the canonical long-term memory** for all agents going forward
- MEMORY.md is secondary — a local convenience cache
- **Consultation order:** SecondBrain/Obsidian → MeMex → External (never skip steps)
- New agents must be onboarded with this architecture from day one

---

## Skill Assimilation Protocol (2026-05-27)

When any agent produces an improved version of a skill, AGENTS.md, playbook, or pipeline component:

1. **Review** — Full read. Understand every change. Check the delta/CHANGELOG.
2. **Assess** — Does this genuinely improve the department? Are the changes material, not cosmetic?
3. **Assimilate** — If yes: apply the improvement logically and methodically. Never blindly copy-paste.
4. **Verify** — The improved component must not break the department's workflow.
5. **Adjust** — If the skill would interrupt or conflict with current workflow, adjust it to fit.
6. **Backup** — Always preserve the previous version (`.bak` or dated copy) before applying.
7. **Document** — Log the assimilation to the department's docs, MeMex decisions, and SecondBrain.

**Applies to ALL departments.**

---

## Universal Standing Order — All Agents (2026-05-23)

- **"Memory"** = Telegram + web GUI + MEMORY.md + SecondBrain/Obsidian + MeMex Zero RAG — collectively
- All surfaces are equal participants; filesystem is the shared truth
- **Context compression rule:** If any chat surface compresses context, write state to memory immediately
- Never lose context to truncation without a filesystem backup

---

## Session Boundary Protocol (2026-06-29)

When a new session starts on a department task another session already handled:
1. Check prior session transcript
2. Check department artifacts for working patterns
3. Do NOT re-discover from scratch
4. Do NOT reach for servers unrelated to the department

**Added to SOUL.md as a CEO protocol.**

---

## SEO Gate Protocol (2026-05-23)

- Default behavior: FLAG (50-69) triggers auto-revision cycle
- Content Agent receives audit feedback → revises → SEO re-audits
- Loop until PASS (≥70). Escalate to Board only after 3 consecutive FLAGs.

---

## Pipeline Protocol Updates (2026-05-23)

- FLAG auto-iteration proven: 1 cycle, +14 points
- GEO verification: full GEO audit via live API between SEO and article writing
- Social distribution holds for CEO review when score is below 80

---

## Model Policy (2026-05-31)

**SUNSET owl-alpha** (removed from fallback chain). Two-tier DeepSeek split:

| Model | Use |
|-------|-----|
| DeepSeek V4 Pro | All production work |
| DeepSeek V4 Flash | Nightly/background cron jobs |
| Fallback chain | minimax/m2.7 → kimi/k2.6 → flash |

---

## Superpowers Framework (2026-05-21)

- **Repo:** https://github.com/obra/superpowers
- **Author:** Jesse Vincent (obra) / Prime Radiant
- **Available for all agents** going forward (Board directive)
- **Reference for:** hiring dept (agent design), content pipeline (structured dev)
- **Skills installed:** 13 skills under `~/workspace/skills/superpowers/`

---

## SkillsMP API (2026-05-21)

- **URL:** https://skillsmp.com
- **API:** https://skillsmp.com/api/v1
- **Auth:** Bearer key stored in [[Infrastructure]]
- **Rate limit:** 500 req/day, 30/min
- **Available for all agents.** Prompts department should use for skill sourcing.

---

## Hermes Agent Transition (2026-06-09)

Blueprint for migrating AgentForge from OpenClaw to Hermes Agent:

**Hierarchy:** gBrain → Orchestrator (Hermes) → Department verticals → Specialist agents → Scoped sub-agents

**Key principles:**
- Narrow scope improves output quality and reduces drift
- Client pods are isolated — own gBrain, orchestrator, agents, memory
- Fork pattern: build well once, customize per client (not copy-paste)

**See:** [[Infrastructure-Hermes]]

---

## BetterLife Image Quality Standard (2026-07-07)

After Board rejected an image due to PIL overlay + opaque watermark:
1. PIL overlay step entirely removed — FLUX/kie.ai output = final image

---

## Skill Foundry — Unbounded Growth Policy (2026-06-16)

The Skill Foundry repository (JPeetz/agent-skills) has **NO skill count cap**. Target trajectory: 12 → 50 → 100 → 500 → 1000+ skills.

**Policy:**
1. **Skill count is unbounded** — no rotation, no removal, no ceiling. Every skill shipped stays shipped.
2. **GitHub Topics are metadata only** — curate the 20 most important broad-category topics permanently. Do NOT rotate.
3. **Report language must be accurate** — say "topics curated" or "topics refreshed" — never "topics rotated" or "limit maintained."
4. **README scales with the repo** — Flat catalog (≤20) → Category directories (20-50) → Search manifest (50+).
5. **Reference pattern:** [awesome-ai-agent-skills](https://github.com/seb1n/awesome-ai-agent-skills) (90+ skills)

**See:** [[Skills]], [[Concepts]]

---

## Marketing Cost Discipline — $0-First Rule (2026-06-25)

After $30 burned on failed video attempts:

| Tier | Cost/M output | Use For |
|------|--------------|---------|
| 1 — Local | $0 | shell, python, ffmpeg — all execution tasks |
| 2 — Cheap | $0.05-0.30 | Gemini Flash, Llama — captions, prompts, formatting |
| 3 — Medium | $2-5 | DeepSeek V4 Pro, GPT-4.1 — strategy, complex scripts |
| 4 — Expensive | $8-15 | Claude Sonnet/Opus — architecture, deep debugging only |

**Key rule:** Is this an execution task? → Tier 1 ($0). Only use expensive models for genuine reasoning.

**Subagent rules:** Briefs ≤500 words. Single task per subagent.

**See:** [[Lessons-Learned]], [[Operations]]
2. Social handles go in captions only, not burned into images
3. 9-pixel color audit replaced with 7-question adversarial visual audit
4. Max 3 regeneration attempts; if all fail → do not post
5. Quality bar: Calm/Headspace Instagram feed

**See:** [[BetterLife-Brand]]
