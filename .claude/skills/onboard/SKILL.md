---
name: onboard
description: Read this project before making changes and report project understanding, commands, and risks without editing files.
disable-model-invocation: true
---

# Onboard

Use this skill when first taking over this repository or when the user asks for a project orientation.

Do not modify files.

Read, while respecting `.claude/settings.json`:

1. `CLAUDE.md`
2. `content_inbox/CLAUDE.md`
3. Relevant README and docs files
4. The target module's `app/`, `scripts/`, `tests/`, and config files
5. `git status --short`

Do not read `.env`, `.env.*`, secrets, tokens, credentials, keys, `content_inbox/data/**`, or `content_inbox/outputs/runs/**`.

Output:

1. Project goal
2. Current mainline
3. Core processing chain
4. Core modules and responsibilities
5. Common commands
6. Safety boundaries
7. Risks or inconsistencies noticed
8. Suggested next steps

End by stating that no files were modified.
