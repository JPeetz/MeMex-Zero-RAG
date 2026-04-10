# Security Policy

Copyright (c) 2026 Joerg Peetz. All rights reserved.

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in Memex, please report it responsibly:

1. **Do NOT open a public issue**
2. Email: [security contact via GitHub profile]
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

You can expect:
- Acknowledgment within 48 hours
- Status update within 7 days
- Credit in the fix (if desired)

## Security Considerations

### Credentials Protection

**NEVER commit your `L1/` directory.** It contains:
- `credentials.md` — API keys, tokens
- Personal rules and identity files

The `.gitignore` excludes `L1/` by default. If you accidentally commit credentials:

1. Rotate all exposed keys immediately
2. Use `git filter-branch` or BFG Repo-Cleaner to purge history
3. Force push (coordinate with collaborators)

### API Keys at Runtime

The batch API (`mcp/batch.py`) accepts API keys via:
- Constructor parameter
- Environment variables (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`)

Keys are held in memory only — never logged or persisted.

### Input Validation

- PDF ingestion validates file headers
- Web clipper sanitizes URLs
- SQL queries use parameterized statements (no injection risk)

### MCP Server

The MCP server uses stdio transport by default (local only). If exposing over network:
- Use authentication
- Enable rate limiting
- Run behind a reverse proxy with TLS

## Dependency Security

Run periodic audits:

```bash
pip-audit
# or
safety check
```

Pin dependencies in production deployments.
