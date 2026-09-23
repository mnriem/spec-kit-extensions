---
description: "Start a change proposal as an empty scaffold."
argument-hint: "<change name or description>"
scripts:
  py: scripts/python/change.py
---

## User Input

```text
$ARGUMENTS
```

Create an empty change directory without drafting planning artifacts or
implementation code.

## Workflow

1. If the input is empty, ask what the user wants to build or fix.
2. Derive or validate a concise kebab-case name.
3. Run `{SCRIPT} list --json` and verify the name is unique.
4. Run:

   ```text
   {SCRIPT} new --change "<name>" --json
   ```

5. Do not create `proposal.md`, spec deltas, `design.md`, or `tasks.md`.
6. Read `templates/proposal.md` and show its structure as the next artifact
   without copying it into the change directory.

## Completion

Report:

- Change name and path
- Artifact sequence: proposal, specs, design, tasks
- Progress: 0/4 artifact categories complete
- The proposal template structure

Point to `__SPECKIT_COMMAND_OPENSPEC_CONTINUE__` to create the first artifact
or `__SPECKIT_COMMAND_OPENSPEC_FF__` to create the complete planning package.
