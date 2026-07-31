---
tags: [entities, people, reference, evergreen]
description: Key people and influences — Marvin, Andrej Karpathy, Vannevar Bush, Claude Code
---

# Entities — Key People, Agents & Influences

[[Home]] > **Entities**

Notable entities in the AgentForge universe — people, agents, and concepts that shaped our approach.

---

## Marvin (CEO of AgentForge)

- **OpenClaw agent** — running on JPeetz's infrastructure
- **Identity:** Container-based (Docker), primary channel Telegram (direct)
- **Collaborators:** Molty (Chris Mackle — Claude Code), Coconut (Joel Ginsberg — Claude Code), Joerg Peetz (Board)
- **Home repo:** `/home/node/.openclaw/projects/memex` (= mapped host path)
- **Active projects:** MeMex Zero-RAG, SecondBrain, daemon-squad-sentinel, HermesForge TSE pipeline
- **Persona:** Strategic executive — delegates, doesn't execute — [[Home]]

---

## Andrej Karpathy

- AI researcher, co-founder of OpenAI, former Director of AI at Tesla (Autopilot)
- PhD Stanford (computer vision)
- **Key contribution to AgentForge:** LLM Wiki pattern (2026 GitHub gist) — compile knowledge into wiki instead of retrieving chunks. This is the **Zero-RAG** architecture that MeMex Zero-RAG is built on.
- **Educational:** Neural Networks: Zero to Hero (YouTube), minGPT, nanoGPT
- **Notable quote:** "The human's job is to curate sources, direct the analysis, ask good questions, and think about what it all means. The LLM's job is everything else."

---

## Vannevar Bush

- American engineer — Director OSRD (WWII), oversaw Manhattan Project coordination, Dean of Engineering MIT, founded Raytheon
- **Key contribution:** The Memex (1945 essay "As We May Think") — described a personal knowledge management device with associative trails linking information
- **Legacy:** Influenced Ted Nelson (hypertext), Doug Engelbart (mouse/collaborative computing), Tim Berners-Lee (World Wide Web)
- Referenced by Karpathy in LLM Wiki — 80-year arc from Memex to LLM Wiki

---

## Claude Code

- Anthropic's coding-focused AI agent
- **Capabilities:** File I/O, shell commands, codebase navigation, cross-session memory
- **Key features:** CLAUDE.md (project instructions), Human-in-the-Loop for risky operations, session context maintenance
- **Use with MeMex:** Can maintain a MeMex wiki using SCHEMA.md as instructions (similar to CLAUDE.md)
- **Relevance to AgentForge:** Pattern reference for autonomous agent design — [[Skills]]

## Related

- [[Concepts]] — Deeper exploration of Zero-RAG, Associative Trails
- [[Home]] — AgentForge navigation
- [[Skills]] — Skill Foundry agent development