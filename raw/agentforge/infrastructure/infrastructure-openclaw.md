# Infrastructure: OpenClaw Configuration

> OpenClaw setup, memory configuration, model policies, and gateway config.
> **Related:** [[Infrastructure]], [[Board-Directives]]

---

## Runtime

| Setting | Value |
|---------|-------|
| Host | macOS 15.7.5 (x64), Node v26.0.0 |
| Workspace | ~/.openclaw/workspace |
| Model | DeepSeek V4 Pro (production) / V4 Flash (nightly) |
| Fallback | minimax/m2.7 → kimi/k2.6 → flash |

## Memory Configuration

| Setting | Value |
|---------|-------|
| Provider | openai-compatible (OpenRouter) |
| Model | openai/text-embedding-3-small |
| Base URL | https://openrouter.ai/api/v1/ |
| Status | ✅ Working (~1.2s) |

**Fix history:** Originally Ollama/nomic-embed-text (hung silently), switched to OpenRouter 2026-07-14.

## Model Policy (2026-05-31)

| Model | Use | Status |
|-------|-----|--------|
| DeepSeek V4 Pro | All production work | ✅ Active |
| DeepSeek V4 Flash | Nightly/background cron jobs | ✅ Active |
| owl-alpha | Previously low-impact only | ❌ Sunset 2026-05-31 |

## Gateway

- Telegram integration: ✅ Configured 2026-05-22
- Discord: 🟡 Bot created, not invited to server (OAuth2 Code Grant toggle)
- Dashboard: Architecture designed (FastAPI + SQLite + SSE), not built

## Agents

| Agent | ID | Status |
|-------|-----|--------|
| CEO | ceo | ✅ Active |
| App Discovery | app-discovery | ✅ Active |
| Advertisement | advertisement | ✅ Active |
| CashClaw | cashclaw | 💤 Dormant |

## Plugin Status

- `@openclaw/discord` — installed, bot connected, no server invite
- `AlexChen31337/openclaw-plugin-claude-code` — 📝 Pending (CLI syntax issue)
