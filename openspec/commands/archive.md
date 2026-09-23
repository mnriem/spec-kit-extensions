---
description: "Synchronize and archive a completed change proposal."
argument-hint: "[change name]"
scripts:
  py: scripts/python/change.py
---

## User Input

```text
$ARGUMENTS
```

Move a finished change into the dated archive, optionally synchronizing its
delta specifications first.

## Workflow

1. Select the change from the input, conversation, or `{SCRIPT} list --json`.
   Ask if ambiguous.
2. Run `{SCRIPT} status --change "<name>" --json`.
3. Review artifact completeness.
   - If any planning artifact is missing, list it and ask for explicit
     confirmation before continuing.
4. Review `tasks.md`.
   - If any task is unchecked, show the remaining count and ask for explicit
     confirmation before continuing.
5. Inspect every delta spec and compare it with the corresponding main spec
   under `openspec/specs/`.
6. If unsynchronized changes exist, ask whether to:
   - Synchronize them now using the merge rules from
     `__SPECKIT_COMMAND_OPENSPEC_SYNC__`
   - Archive without synchronizing
   - Cancel
7. If synchronization is selected, complete and validate it before archiving.
8. Run:

   ```text
   {SCRIPT} archive --change "<name>" --json
   ```

   The script moves the directory to
   `openspec/changes/archive/YYYY-MM-DD-<name>/`. A name that already starts
   with an ISO date keeps its existing prefix.

## Safety Rules

- Never overwrite an existing archive directory.
- Never hide incomplete artifacts, incomplete tasks, or sync conflicts.
- Do not delete change contents.
- Do not modify implementation code.

## Completion

Report the archived change name, final path, specification sync status,
artifact/task warnings, and any user-approved exceptions.
