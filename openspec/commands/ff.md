---
description: "Fast-forward a change proposal through all artifacts required for implementation."
argument-hint: "<change name or description>"
scripts:
  py: scripts/python/change.py
---

## User Input

```text
$ARGUMENTS
```

Create every missing planning artifact in one pass. Do not implement code.

## Workflow

1. Understand the requested change. Ask about material ambiguity before
   writing.
2. Resolve a kebab-case name.
3. Run `{SCRIPT} list --json`.
4. If the change does not exist, run:

   ```text
   {SCRIPT} new --change "<name>" --json
   ```

   If it exists, treat this as completion of the existing scaffold and preserve
   all current artifacts.
5. Run `{SCRIPT} status --change "<name>" --json`.
6. Read all existing artifacts and these templates:
   - `templates/proposal.md`
   - `templates/spec.md`
   - `templates/design.md`
   - `templates/tasks.md`
7. Inspect relevant source, tests, configuration, and documentation once, then
   reuse that evidence across artifacts.
8. Create every missing category in dependency order:
   - Proposal
   - One or more capability spec deltas
   - Design
   - Tasks
9. Never overwrite an existing artifact silently. If existing content
   conflicts with the requested change, stop and explain the conflict.
10. Ensure tasks cover every requirement and remain unchecked.
11. Run `{SCRIPT} status --change "<name>" --json` and verify all categories
    are complete.

## Completion

Report existing artifacts preserved, artifacts created, capabilities covered,
assumptions, and open questions. End by pointing to
`__SPECKIT_COMMAND_OPENSPEC_APPLY__`.
