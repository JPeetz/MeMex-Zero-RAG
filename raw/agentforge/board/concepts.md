---
tags: [concepts, architecture, knowledge, evergreen]
description: Core architecture concepts — Zero-RAG, Associative Trails, Human-in-the-Loop
---

# Core Concepts — AgentForge Architecture & Philosophy

[[Home]] > **Concepts**

A collection of foundational concepts that underpin AgentForge's memory architecture, agent design, and operational philosophy.

---

## Zero-RAG (Knowledge Compilation)

**An approach to LLM knowledge management where sources are compiled into structured knowledge rather than retrieved as chunks at query time.**

### The Problem with RAG
Traditional RAG chunks documents → embeds vectors → retrieves on query → generates. The LLM rediscovers knowledge from scratch every time. Nothing compounds.

### The Zero-RAG Alternative
1. LLM reads source **once**
2. Extracts entities, concepts, relationships
3. Writes structured wiki pages
4. Cross-references everything
5. Flags contradictions

On query, the LLM reads the **compiled wiki** — synthesis is already done.

| Aspect | RAG | Zero-RAG |
|--------|-----|----------|
| Setup cost | Low | Higher |
| Query speed | Fast | Fast |
| Knowledge accumulates | No | Yes |
| Cross-document reasoning | Fragmented | Holistic |
| Maintenance | Low | Medium |

**Origin:** [[andrej-karpathy]]'s LLM Wiki gist (2026). **Our implementation:** MeMex Zero-RAG + SecondBrain.

---

## Associative Trails

**User-defined links between related pieces of information, mirroring how human memory works by association rather than hierarchical indexing.**

**Origin:** Conceived by [[vannevar-bush]] in his 1945 essay "As We May Think":
> "The process of tying two items together is the important thing…"

### Modern Implementation
- **[[wikilinks]]** — Direct connections between pages
- **Cross-references** — "See also" sections
- **Backlinks** — Automatic reverse links

In SecondBrain, every file uses `[[wikilinks]]` to create an interconnected knowledge graph. This IS associative trails applied to agent memory.

---

## Human-in-the-Loop

**A design pattern where AI agents propose actions but require human approval before executing critical or irreversible operations.**

### The Pattern
```
Agent perceives → Agent plans → Agent proposes → HUMAN APPROVES → Agent executes
```

**Human stays in the loop for:**
- Destructive operations (delete, overwrite)
- External actions (send email, post publicly)
- Financial operations (purchases, transfers)
- Ambiguous decisions (multiple valid interpretations)

### AgentForge Examples
- **Marketing images:** Board reviews before posting ([[BetterLife-Social-Media]])
- **Bundle launches:** CEO checks bundle tracker before approving
- **Agent deployment:** Adversarial review required before any hire goes live

---

## Memex → LLM Wiki: 80 Years

A synthesis tracing the evolution from [[vannevar-bush]]'s 1945 Memex vision through to Karpathy's LLM Wiki pattern (2026).

**The Vision (1945):** Bush imagined a "memex" — a personal device storing all books, records, and communications with associative trails linking information the way human memory works.

**The Failed Intermediaries:** Hypertext (manual links), Personal wikis (maintenance burden), Roam/Obsidian (still manual), RAG systems (no accumulation). All required humans to do tedious work or gave up on structure.

**The Solution (2026):** Combine LLM intelligence (reads sources, extracts entities, writes structured wiki) with human curation (select sources, direct analysis, ask good questions). The LLM does the tedious work; the human provides direction.

> "The human's job is to curate sources, direct the analysis, ask good questions, and think about what it all means. The LLM's job is everything else." — Andrej Karpathy

**Our implementation:** MeMex Zero-RAG (LLM-maintained wiki) + SecondBrain (human-curated Obsidian vault) = complete knowledge management system.

---

## Skill Forge — Unbounded Growth Policy

**Board Directive — 2026-06-16:** The Skill Foundry repository has **NO skill count cap**. Target trajectory: 12 → 50 → 100 → 500 → 1000+ skills.

**Key points:**
- No rotation, no removal, no ceiling. Every skill shipped stays shipped.
- GitHub Topics (20 max) are metadata only — curate the 20 most important categories permanently
- Report language: "topics curated" not "topics rotated"
- README scales: flat (≤20) → category dirs (20-50) → search manifest (50+)
- Reference: [awesome-ai-agent-skills](https://github.com/seb1n/awesome-ai-agent-skills)

---

## Failure Auto-Resolution (Prime Directive)

**Board Directive — 2026-07-15:** When anything fails, automatically diagnose and fix before escalating.

**Protocol:** Research memory first → Previous fix? Apply it → No fix? Analyze + fix → Complete task. Escalate only after **3 consecutive failures**.

---

## SkillForge — Combined SkillClaw + Skill Foundry

**Design stage (Board review pending, 2026-07-14)**

Open-source skill lifecycle management platform combining SkillClaw (session capture + auto-evolution) with Skill Foundry (quality gate + GitHub publishing).

**Architecture:** Capture → Evolve → Quality Gate → Publish

**Three integration layers:** Light (archived sessions) → Medium (CEO proxy) → Full (all agents)

## Related

- [[Infrastructure]] — How concepts are implemented
- [[Learning-Loop]] — How concepts compound over time
- [[Skills]] — Skills repository reflecting unbounded growth policy