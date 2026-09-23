---
description: "Implement the remaining tasks from a change proposal."
argument-hint: "[change name]"
scripts:
  py: scripts/python/change.py
---

## User Input

```text
$ARGUMENTS
```

Implement a planned change task by task.

## Select the Change

1. If the input names a change, use it.
2. Otherwise run `{SCRIPT} list --json`.
3. Auto-select only when exactly one active change exists or the conversation
   unambiguously identifies one. If several remain possible, ask the user.
4. Run `{SCRIPT} status --change "<name>" --json`.
5. Announce the selected change and how to override it.

## Preconditions

- `proposal.md`, at least one delta spec, `design.md`, and `tasks.md` must exist.
- If planning is incomplete, stop and point to
  `__SPECKIT_COMMAND_OPENSPEC_CONTINUE__` or
  `__SPECKIT_COMMAND_OPENSPEC_FF__`.
- Read every planning artifact before editing code.
- Inspect nearby implementation and tests to confirm current conventions.

## Implementation Loop

For each unchecked task in `tasks.md`, in order:

1. State the task being implemented.
2. Make the smallest complete code and documentation changes required by the
   task and its associated requirements.
3. Run the narrowest relevant validation.
4. Mark the task `- [x]` only after its specified behavior is complete and
   validation succeeds.
5. Continue until all tasks are complete or a blocker requires user input.

Pause and ask before proceeding when:

- A task is materially ambiguous.
- Implementation conflicts with a requirement or design decision.
- Required work exceeds the planned scope.
- A compatibility, migration, security, or data-loss decision is unresolved.
- Validation fails and the cause cannot be corrected within the task.

Never silently narrow, defer, or reinterpret specified behavior merely to mark
a task complete.

## Completion

Run `{SCRIPT} status --change "<name>" --json` and report:

- Tasks completed in this session
- Overall completed/total task count
- Validation performed
- Remaining blockers

When every task is complete, point to
`__SPECKIT_COMMAND_OPENSPEC_VERIFY__` before archival.
