---
title: OpenClaw HEARTBEAT.md Template - Scheduled Tasks
use_case: Agent scheduling and automation
status: raw
source_url: https://blink.new/blog/openclaw-heartbeat-soul-memory-configuration-guide-2026
source_author: Blink Team
source_type: blog
license: unclear
discovered: 2026-05-14
last_updated: 2026-05-14
agentforge_optimized: false
tags: [openclaw, heartbeat, scheduling, automation, cron, template]
---

# OpenClaw HEARTBEAT.md Template - Scheduled Tasks

## Prompt Text

```
# Heartbeat Schedule

## Daily Tasks

### 6:45 AM — Morning Briefing
- Check Google Calendar: list all events for today with times
- Check yesterday's metrics: [describe your dashboard URL or data source]
- Scan email inbox for: urgent flags, emails from [key client names],
  anything with "deadline" or "urgent"
- Search web for: "[your company name]" mentions, "[competitor name]" news
- Compile a structured Telegram message with sections:

   📅 TODAY'S SCHEDULE
   📊 YESTERDAY'S METRICS
   ⚡ NEEDS YOUR ATTENTION (urgent items only)
   📰 ONE THING TO KNOW (1 key insight from news/email)

### 5:00 PM Friday — Weekly Report
- Pull this week's key metrics vs. last week
- Write a narrative summary: what drove results, concerns, wins
- Post the full report to #growth Slack channel

## Continuous Monitoring

### Every 60 Minutes — Lead Alert
- Check CRM for new trial signups in the last 60 minutes
- For each new signup:
  * Look up their LinkedIn profile and company
  * Draft a personalized welcome email (save as draft, do not send)
  * Send me Telegram: "New trial: [name] from [company]. Email draft ready."

### Every 4 Hours — Uptime Check
- Check uptime of https://app.acmecorp.com
- If down or returning non-200: immediately alert on Telegram

### Every Monday 9:00 AM — Weekly Pipeline Review
- Query HubSpot for all open deals
- Identify deals not updated in 7+ days
- Send to Telegram and post to #sales Slack
```

## Context

HEARTBEAT.md is the agent's scheduling brain. OpenClaw reads it every 30 minutes and executes any scheduled tasks whose time has come. This template covers: daily morning briefings, weekly reports, continuous monitoring (lead alerts, uptime checks), and weekly pipeline reviews.

## Quality Notes

- Uses natural language scheduling (not cron syntax)
- Each task has clear steps and output format
- Mix of scheduled and continuous monitoring tasks
- Estimated token cost: ~500 tokens
