---
title: "Claude Code"
type: entity
created: 2026-04-09
updated: 2026-04-09
status: active
source_count: 1
tags: [tool, ai-agent, anthropic, coding]
---

# Claude Code

Anthropic's coding-focused AI agent, designed for software development tasks with built-in tool use and file system access.

## Overview

Claude Code is an AI coding agent that can:
- Read and write files
- Execute shell commands
- Navigate codebases
- Maintain context across sessions

[Source: wiki/sources/ai-agents-overview.md]

## Key Features

| Feature | Description |
|---------|-------------|
| Tool use | File I/O, shell, web search |
| CLAUDE.md | Project-specific instructions |
| Memory | Session and cross-session context |
| Safety | [[human-in-the-loop]] for risky operations |

## Use with Memex

Claude Code is one of several agents that can maintain a Memex wiki. The SCHEMA.md file serves as its instructions (similar to CLAUDE.md). [Source: wiki/sources/karpathy-llm-wiki-gist.md]

## Comparison to Other Agents

Part of a broader landscape including:
- Cursor (IDE-integrated)
- GitHub Copilot (code completion focus)
- OpenAI Codex (API-based)

[Source: wiki/sources/ai-agents-overview.md]

## Related

- [[human-in-the-loop]] — Safety pattern it implements
- [[andrej-karpathy]] — References it for LLM Wiki

---

*Last updated: 2026-04-09*
