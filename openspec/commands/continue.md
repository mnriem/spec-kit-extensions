---
description: "Create the next ready planning artifact for a change proposal."
argument-hint: "[change name]"
scripts:
  py: scripts/python/change.py
---

## User Input

```text
$ARGUMENTS
```

Create exactly one next artifact category for an active change.

## Select and Inspect

1. Select the change from the input, conversation, or `{SCRIPT} list --json`.
   Ask if ambiguous.
2. Run `{SCRIPT} next --change "<name>" --json`.
3. Read every existing artifact and inspect relevant repository context.
4. If `nextArtifact` is null, report that planning is complete and point to
   `__SPECKIT_COMMAND_OPENSPEC_APPLY__`.

## Create One Artifact

Use the matching bundled template:

| Next artifact | Template | Destination |
|---------------|----------|-------------|
| `proposal` | `templates/proposal.md` | `openspec/changes/<name>/proposal.md` |
| `specs` | `templates/spec.md` | `openspec/changes/<name>/specs/<capability-path>/spec.md` |
| `design` | `templates/design.md` | `openspec/changes/<name>/design.md` |
| `tasks` | `templates/tasks.md` | `openspec/changes/<name>/tasks.md` |

Rules:

- Create only the selected category in this run.
- The specs category may contain multiple capability files when the proposal
  clearly affects multiple capabilities.
- Re-read dependency artifacts before drafting.
- Ground content in relevant source, tests, and documentation.
- Ask about material ambiguity before writing.
- Never implement code.

After writing, run `{SCRIPT} status --change "<name>" --json`.

## Completion

Report the artifact paths created, progress out of four categories, and which
artifact is next. Stop after this one category even if another is ready.
