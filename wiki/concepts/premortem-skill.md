---
title: Pre-Mortem Skill — Strategic Decision Framework
type: concept
tags: ["skill", "decision-making", "strategy", "risk-management", "framework"]
created: 2026-06-28
author: marvin
---

# Pre-Mortem Skill

**Stored:** 2026-06-28
**Source:** Joerg (Board) via Google Drive
**Language:** Translated from Spanish original

## What It Is
A pre-mortem is the opposite of a post-mortem. Instead of figuring out what went wrong AFTER something fails, you imagine it already failed and figure out why BEFORE starting. Method from psychologist Gary Klein, published in Harvard Business Review. Daniel Kahneman called it his most valuable decision-making technique.

**Key insight:** When you ask "what could go wrong?" people give cautious, vague answers. When you say "this already failed, tell me why," the brain shifts to narrative mode and generates much more specific, creative, and honest reasons.

## Triggers

**Mandatory triggers** — run the pre-mortem when user says:
- "premortem this", "premortem my"
- "run a premortem"
- "what could kill this"
- "stress test this plan"
- "what am I missing here"
- "find the blind spots"

**Strong triggers:**
- "what could go wrong"
- "I'm missing something"
- "poke holes in this"
- "where will this break"
- "devil's advocate"

**Do NOT trigger on:** simple feedback requests, factual questions, LLM Council requests. DO trigger when someone has a plan or commitment where the cost of being wrong is high.

## When to Run
Good targets: product/feature about to build, launch with money/reputation at stake, pricing change, hiring decision, strategy pivot, partnership evaluation

Bad targets: vague ideas without a plan, questions with one right answer, creative feedback on drafts, already-made irreversible decisions

## Execution Protocol

### Phase 0: Context Gathering
1. Scan current conversation for plan details
2. Scan workspace for relevant files (CLAUDE.md, memory/, project files, briefs)
3. Assess sufficiency — need three things:
   - What is it? (one sentence)
   - Who is it for / affected?
   - What does success look like?
4. Fill gaps conversationally (one question at a time, only what's needed)

### Phase 1: Set the Frame
"Alright, I have enough context. Let's run the pre-mortem. The premise: it's been 6 months. [The plan] has failed. It's done. We're looking back trying to understand what went wrong."

### Phase 2: Raw Pre-Mortem
Generate every genuine reason why it could have failed. Be exhaustive, specific, grounded in real details. Each reason: 1-2 sentences, specific to this plan, a genuine threat (not minor inconvenience).

### Phase 3: Deep-Dive Agents (Parallel)
Spawn one sub-agent per failure reason, all in parallel. Each agent:
- Gets the full plan context
- Gets their assigned failure reason
- Produces: failure story (2-3 paragraphs), underlying assumption (one sentence), early warning signs (1-2 measurable signals)
- Max 300 words per agent

**Sub-agent prompt template:**
```
You are a researcher in a pre-mortem analysis. Assigned a specific failure reason.

THE PLAN:
[full context: what, who, success criteria, workspace context]

PRE-MORTEM FRAME: It's been 6 months. This plan has failed.

YOUR FAILURE REASON: [specific reason from Phase 2]

Your job: dig deep into this failure. Write the story of how it actually played out. Be specific. Use plan details. Make it feel real.

Output:
1. FAILURE STORY: 2-3 paragraph narrative of how this specific failure unfolded. Name specific moments where things went wrong and why.
2. UNDERLYING ASSUMPTION: The single thing the user took for granted that made this failure possible. One sentence.
3. EARLY WARNING SIGNS: 1-2 concrete, observable signals to watch for. Must be measurable, not vague feelings.

Under 300 words. Direct. No softening.
```

### Phase 4: Synthesis
After all agents complete:
1. **Most Likely Failure** — which is most probable and why
2. **Most Dangerous Failure** — which causes most damage even if less likely
3. **Hidden Assumption** — most critical unquestioned assumption across all analyses
4. **Revised Plan** — specific, concrete changes. Not "consider your pricing" but "test pricing at $X with 20 people before public commitment"
5. **Pre-Launch Checklist** — 3-5 specific items to verify/test before executing

### Phase 5: Generate HTML Report
File: `premortem-report-[timestamp].html`
- Dark background (#0a0e1a), clean typography
- Synthesis prominent at top (most people read only this)
- Visual cards per failure reason (heading, story, assumption, warning signs)
- Distinct accent colors per card
- Severity/probability indicator
- Agent grid showing all findings
- Footer with timestamp and what was pre-mortemed

### Phase 6: Save Transcript
File: `premortem-transcript-[timestamp].md`
- Context gathered (what, who, success criteria)
- Raw pre-mortem failure reasons
- All agent deep-dive analyses
- Complete synthesis

### Final Chat Output
Concise summary: most likely failure, hidden assumption, single most important plan revision. Max three sentences. Report has full details.

## Important Notes
- Always launch agents in parallel (sequential wastes time, allows bias)
- Always set the pre-mortem frame explicitly ("this already failed")
- Be exhaustive but don't pad — find every genuine failure reason
- The synthesis is the product — make it specific and actionable
- Don't soften — the point is to say things the user doesn't want to hear
- Revised plan must be concrete: doable this week
- Respect minimum context threshold — ask one more question rather than produce a bad pre-mortem
- Not the LLM Council — different mechanism, different result