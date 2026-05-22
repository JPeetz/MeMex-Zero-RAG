# Standby Agents — Activation Protocol

Agents not yet deployed. Activate on-demand via CEO directive when their pipeline function is needed.

## Activation Process
1. CEO directive triggers activation
2. Read ClaudeClaw source: CLAUDE.md + config.json from `/Users/joergpeetz/Documents/claudeclaw-agent-backup/agents/<dept>/`
3. Adapt role → AGENTS.md with Standing Orders
4. Register as: `openclaw agents add <dept>`
5. Wire into handoff schema v1.0 as artifact consumer/producer
6. Add cron job if periodic
7. Update MeMex + Obsidian agent registry (this file)

## Standby Agents

| Agent | Trigger | Pipeline Position | Source |
|-------|---------|-------------------|--------|
| prompts | 50+ prompts ready for bundle | Producer: prompt-bundle artifacts | ClaudeClaw prompts/CLAUDE.md |
| wp-design | Docker WP theme needed | Consumer: design-spec → Producer: theme-deployed | ClaudeClaw wp-design/CLAUDE.md |
| hiring | New department/agent proposal | Adversarial review pipeline | ClaudeClaw hiring/CLAUDE.md |
| research | CEO requests external analysis | Isolated producer | ClaudeClaw research/CLAUDE.md |
| comms | Email/social response volume spikes | Consumer: message artifacts | ClaudeClaw comms/CLAUDE.md |
| niche-scout | Analytics weekly report flags new niche | Isolated producer → analytics consumer | ClaudeClaw niche-scout/CLAUDE.md |
| ops | Gateway/node health alerts fire | System monitoring | ClaudeClaw ops/CLAUDE.md |
| design | Frontend component work needed | Consumer: design-spec artifacts | ClaudeClaw design/CLAUDE.md |
