# Marketing Image Review Protocol

**Board Directive** | 2026-07-15 | Status: Active

## The Directive

"From now on the marketing presents all created images for review and for me to decide which picture is going to be published."

## Implementation

- Script generates up to 3 variants per run
- All variants saved to `tool-image-generation/` with numbered filenames (v1, v2, v3)
- All variants presented to Board (Joerg) for review in the chat
- Brand audit is advisory only — Board makes the final call
- No auto-posting without explicit Board approval
- Script exits with code 42 to signal "images ready, awaiting Board review"

## Related

- [[prime-directive-failure-autoresolution]]
- [[betterlife-social-posting-procedure]]