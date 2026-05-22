
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

## 2026-05-22 — Board Decisions (Model Policy & Pipeline Handoff)

### Model Policy
- **owl-alpha**: low-hit-rate/low-impact tasks only
- **DeepSeek V4 Pro**: all high-quality work (CEO + all department agents)
- **Expiry**: 2026-05-31 — review then
- **Reminder set**: cron job e7021d89 fires 09:00 IE 2026-05-31

### Pipeline Handoff
- Adopt structured JSON artifact approach from agent-handoff-schema.md v1.0
- Canonical handoff path: MeMex Zero RAG + Obsidian vault
- File-based gating (daily-pipeline/) is deprecated in favor of typed artifacts

### Preserved from Hermes
- Self-improving skill loop concept → implement via OpenClaw skills + skill-creator
- FTS5 session search → OpenClaw memory_search / QMD backend
- Honcho user modeling → OpenClaw memory engines
- Cron-native scheduling → OpenClaw cron (already in use)
- Multi-platform gateway → OpenClaw channels (already in use)
