---
title: Local-First Software
type: concept
created: 2026-04-09
updated: 2026-04-09
status: active
source_count: 1
tags: [architecture, data-ownership, offline]
---

# Local-First Software

A software architecture pattern where data lives primarily on the user's device, with cloud synchronization as an optional enhancement rather than a core requirement.

## Core Idea

Traditional cloud-first apps treat user devices as thin clients—data lives on servers, and devices just display it. Local-first inverts this: **the device is the source of truth**, and the cloud is a convenience for sync and backup.

[Source: wiki/sources/sample-article.md]

## Key Properties

1. **Works offline**: No degraded mode. Full functionality without network.
2. **Fast**: Operations happen instantly—no round-trip latency.
3. **User owns data**: Files/databases are on your machine, in readable formats.
4. **Privacy-preserving**: Data doesn't need to leave your device.

[Source: wiki/sources/sample-article.md]

## Enabling Technologies

- [[crdt]]: Conflict-free data structures for multi-device sync
- [[sqlite]]: Local database with full SQL power
- [[yjs]], [[automerge]]: CRDT libraries for JavaScript

[Source: wiki/sources/sample-article.md]

## Examples

- [[obsidian]]: Local markdown files, optional sync
- [[linear]]: Optimistic local-first UI
- [[figma]]: Local rendering with real-time collaboration

[Source: wiki/sources/sample-article.md]

## Trade-offs

| Benefit | Challenge |
|---------|-----------|
| Offline works | Initial sync can be slow |
| User owns data | Storage limits on mobile |
| Fast operations | Merge conflicts still possible |
| Privacy | Local encryption needed |

## Related Concepts

- [[offline-first]]: Subset focusing on offline capability
- [[edge-computing]]: Processing at the network edge
- [[data-ownership]]: User control over their data

---

*See also: [[crdt]], [[sqlite]], [[obsidian]]*
