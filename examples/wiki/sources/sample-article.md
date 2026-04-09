---
title: "The Rise of Local-First Software"
type: source
created: 2026-04-09
updated: 2026-04-09
status: active
source_count: 1
tags: [software-architecture, local-first, data-ownership]
---

# The Rise of Local-First Software

Local-first software prioritizes storing data on the user's device, with cloud sync as optional enhancement rather than requirement. This represents a philosophical shift toward trusting edge devices and empowering users with genuine data ownership.

## Key Principles

- **Offline capability**: Full functionality without internet [Source: raw/sample-article.md]
- **Data ownership**: Users control their own data [Source: raw/sample-article.md]
- **Speed**: No network latency for operations [Source: raw/sample-article.md]
- **Privacy**: Data can stay on-device [Source: raw/sample-article.md]

## Notable Implementations

| Tool | Approach |
|------|----------|
| [[obsidian]] | Markdown files stored locally, optional sync |
| [[linear]] | Optimistic UI with local-first architecture |
| [[figma]] | Real-time collab with local rendering |

[Source: raw/sample-article.md]

## Enabling Technologies

### CRDTs

[[crdt|CRDTs]] (Conflict-free Replicated Data Types) enable simultaneous editing without conflicts. Key libraries: [[yjs]], [[automerge]]. [Source: raw/sample-article.md]

### Local Databases

[[sqlite]] on device with sync protocols like Electric SQL or CR-SQLite. [Source: raw/sample-article.md]

## Challenges

- Merge conflicts (CRDTs help but don't solve everything)
- Mobile storage limits
- Initial sync time for large datasets  
- Local data needs encryption

[Source: raw/sample-article.md]

## Related Concepts

- [[data-ownership]]
- [[offline-first]]
- [[edge-computing]]

---

*Ingested: 2026-04-09 | See also: [[crdt]], [[sqlite]]*
