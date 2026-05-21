
## 2026-05-21 — Memory Architecture Decision (CEO)

**Decision:** Obsidian vault (`~/obsidian-vault/AgentForge/`) and MeMex Zero RAG (`~/workspace/MeMex-Zero-RAG/wiki/agentforge/`) are designated as the **canonical long-term memory** for all agents going forward.

**Rationale:** 
- Local knowledge systems reduce token usage over time
- Agents should never re-query external sources for information already captured locally
- MEMORY.md remains as a secondary convenience cache, not the primary memory store

**Consultation order for all agents:**
1. MeMex Zero RAG (structured wiki)
2. Obsidian vault (narrative, linked)
3. External (web search / AI query) — only as last resort

**Scope:** Applies to Marvin (CEO) and all new agents created going forward.

**Logged by:** CEO (Marvin)
