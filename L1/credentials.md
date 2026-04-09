# Credentials

> 🔒 CRITICAL: This file is git-ignored. NEVER commit credentials.

Store API keys and tokens here. The LLM can read them when needed but will never write them to wiki pages.

## API Keys

```
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_API_KEY=
```

## Service Tokens

```
GITHUB_TOKEN=
NOTION_TOKEN=
```

## Usage Notes

- Reference credentials by name, never by value
- If the LLM needs to use an API, it reads the key from here
- If you see a credential in a wiki page, that's a 🔴 CRITICAL lint error

---

*Keep this file minimal. Only add credentials the LLM actually needs.*
