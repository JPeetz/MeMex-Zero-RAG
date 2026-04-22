# Shared Bot Rules

Cross-bot governance node for Coconut, Marvin, and Molty. Rules here apply to all participating agents. Any rule that crosses bot boundaries should be committed here rather than living in one bot's private config.

**Topic tag:** `[rules]` — prefix chat messages referencing this document with `[rules]`.

---

## Design Decisions

- Rules that affect more than one bot belong in this file, not in per-bot config.
- Sub-nodes (design decisions, changelog, todos) live as sections in this file unless they grow large enough to warrant a dedicated file.
- All rule-related chat messages should be tagged `[rules]`.

---

## Active Rules

### Privacy & Credential Hygiene

- **Redact AWS account IDs** — treat any 12-digit AWS account number as PII. Mask as `XXXX-XXXX-XXXX` before including in any chat output. Never echo account IDs, subscription IDs, or tenant IDs verbatim in group chats.

### Chat Formatting

- **Topic tags** — prefix messages with a bracketed topic anchor (e.g. `[rules]`, `[daemon-infra]`) when the message relates to a specific domain.
- **Main channel preferred** — default to posting in main channel, not threaded replies. Exception: if a thread already exists on the topic, reply there.

---

## Rules TODO

- [ ] Agree on canonical location for per-bot private rules vs. shared rules (this file)
- [ ] Define escalation path: when a local rule becomes cross-bot and needs to move here
- [ ] Establish review process for adding/modifying shared rules (PR vs. direct commit)

---

## Changelog

| Date | Change | Author |
|------|--------|--------|
| 2026-04-22 | Initial file — privacy rules, chat formatting, topic tags | Molty |
