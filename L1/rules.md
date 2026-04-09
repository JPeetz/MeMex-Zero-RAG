# Rules & Gotchas

> ⚠️ This file is git-ignored. It stays private on your machine.

These are hard rules the LLM must follow every session. Add domain-specific constraints as you discover them.

## Universal Rules

1. **Never commit L1/** — This directory is private
2. **Never auto-resolve contradictions** — Always ask me
3. **Always cite sources** — No unsourced claims
4. **Never modify raw/** — Source documents are immutable

## My Gotchas

Add things you've learned the hard way:

```markdown
### Example: API Rate Limits
- Don't make more than 3 concurrent requests to [service]
- Always add exponential backoff

### Example: Naming Conventions  
- Use kebab-case for wiki page names
- Use ISO 8601 for all dates (YYYY-MM-DD)
```

## Domain-Specific Rules

Add rules specific to your knowledge domain:

```markdown
### Example: Research Papers
- Always note publication date and venue
- Flag if paper is preprint vs peer-reviewed

### Example: Project Documentation
- Link every decision to its ADR (Architecture Decision Record)
- Mark deprecated approaches clearly
```

---

*The LLM reads this at session start. Keep it concise but complete.*
