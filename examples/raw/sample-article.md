# The Rise of Local-First Software

*A sample source document for testing wiki ingestion.*

---

## Overview

Local-first software is an approach where data lives primarily on the user's device, with cloud sync as an optional enhancement rather than a requirement. This contrasts with cloud-first software where data lives on servers and devices are thin clients.

## Key Principles

1. **Offline capability**: The app works fully without internet
2. **Data ownership**: Users control their data
3. **Speed**: No network latency for basic operations
4. **Privacy**: Data doesn't have to leave your device

## Notable Implementations

- **Obsidian**: Markdown notes stored locally, optional sync
- **Linear**: Optimistic UI with local-first architecture
- **Figma**: Real-time collaboration with local rendering

## Technologies Enabling Local-First

### CRDTs (Conflict-free Replicated Data Types)

CRDTs allow multiple users to edit the same document simultaneously without conflicts. Each edit is automatically mergeable. Libraries like Yjs and Automerge implement CRDTs for JavaScript.

### SQLite + Sync

SQLite databases on device, synced via protocols like Electric SQL or CR-SQLite. Gives you full SQL power locally.

## Challenges

- **Merge conflicts**: CRDTs help but don't solve everything
- **Storage limits**: Mobile devices have constraints
- **Initial sync**: Large datasets take time to download
- **Security**: Local data needs encryption

## Conclusion

Local-first represents a philosophical shift: trusting the edge, empowering users, treating the network as an enhancement rather than a requirement. It trades some complexity for better UX and genuine data ownership.

---

*Source: Compiled from various articles on local-first software, 2026*
