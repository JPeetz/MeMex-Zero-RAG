# SkillsMP Skills Installation — 2026-05-18

## Summary
Installed 6 skills from SkillsMP marketplace to expand Claude Code capabilities for WP design department and DevOps pipeline automation.

## Installed Skills

| Skill | Purpose | Author | Status |
|-------|---------|--------|--------|
| `security-auditor` | Code & system security vulnerability analysis | - | ✅ Installed |
| `static` | Binary reverse engineering (PE/ELF analysis with Ghidra) | - | ✅ Installed |
| `frontend-design` | Advanced frontend UI/UX design (React, Tailwind) | - | ✅ Installed |
| `web-artifacts-builder` | Complex React/Tailwind web component generation | - | ✅ Installed |
| `ci-cd-pipeline-builder` | Reliable CI/CD pipeline automation | - | ✅ Installed |
| `github-automation` | GitHub operations via gh CLI (repos, PRs, issues, workflows) | - | ✅ Installed |

## Not Found on SkillsMP

| Skill | Reason |
|-------|--------|
| `webapp-testing` (Playwright E2E) | No matching search results |
| `skill-creator` | No matching search results |

## Installation Method

1. Queried SkillsMP API: `GET https://skillsmp.com/api/v1/skills/ai-search?q={query}`
2. Extracted GitHub URLs from results
3. Converted tree URLs to git clone URLs
4. Cloned repos and extracted SKILL.md files
5. Installed to `~/.claude/skills/{skill-name}/`

## Next Steps

- Consider creating custom `webapp-testing` skill if needed for WP design QA
- Monitor skill performance and update as versions are released
- Evaluate whether `skill-creator` needs to be built in-house
- Integrate security-auditor into pre-deployment pipeline checks

## Related

- Skills location: `~/.claude/skills/`
- Total available skills now: 42
- Dependencies: curl, git, Python 3

## Infrastructure (2026-05-21)

| Service | URL | Notes |
|---------|-----|-------|
| Local sudo | — | password: Buddy-2019 |
| SSH | jpeetz@207.180.227.214 | password: Buddy-2019 |
| SearNXG | http://207.180.227.214:8080 | Search server |
| N8n | https://jpeetzn8n.xyz | Automation — j.peetz69@gmail.com / Buddy-2019 |
