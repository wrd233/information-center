---
name: safe-change
description: Plan a safe code or config change before editing; supports $ARGUMENTS as the requested change.
disable-model-invocation: true
---

# Safe Change

Requested change:

```text
$ARGUMENTS
```

Use this skill before any code or config modification.

Before editing files, read the relevant project guides and target files, then output a plan. Do not modify files until the user confirms.

The plan must include:

1. Requirement understanding
2. Files likely to be changed
3. Files and paths that will not be touched
4. Main risks
5. Verification commands
6. Step-by-step plan

Respect these boundaries:

- Do not read `.env`, `.env.*`, secrets, tokens, credentials, keys, `content_inbox/data/**`, or `content_inbox/outputs/runs/**`.
- Do not run Docker, network calls, real batch processing, or data-mutating commands without explicit user confirmation.
- Do not perform whole-repository refactors unless the user explicitly asks.
- Keep the change narrow and consistent with existing code.
