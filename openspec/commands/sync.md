---
description: "Merge delta specs from an active change into the main specs without archiving."
argument-hint: "[change name] [capability ...]"
scripts:
  py: scripts/python/change.py
---

## User Input

```text
$ARGUMENTS
```

Merge selected capability deltas into `openspec/specs/` while leaving the
change active.

## Select and Load

1. Select the change from the input, conversation, or `{SCRIPT} list --json`.
   Ask if ambiguous.
2. Run `{SCRIPT} status --change "<name>" --json`.
3. Read every listed delta spec, or only the capabilities explicitly named by
   the user.
4. For each delta at
   `openspec/changes/<name>/specs/<capability-path>/spec.md`, load the main spec
   at `openspec/specs/<capability-path>/spec.md` when it exists.

## Merge Rules

Apply operations in this order:

1. **RENAMED**
   - Find the exact existing requirement heading.
   - Rename it without changing its body unless a MODIFIED entry also exists.
2. **MODIFIED**
   - Replace the complete existing requirement block, including scenarios.
   - Stop if the target requirement cannot be identified exactly.
3. **REMOVED**
   - Remove the complete requirement block.
   - Stop if the target is absent; do not report a successful removal.
4. **ADDED**
   - Append the complete new requirement block.
   - Stop on a duplicate requirement name unless the user resolves the conflict.

For a capability without a main spec, create it from the applicable ADDED
requirements. A new main spec must describe the current capability state, not
retain delta-operation headings.

## Validation

Before saving each capability:

- Ensure every requirement name is unique.
- Ensure every requirement is testable and has at least one scenario.
- Ensure no delta markers remain in the main spec.
- Preserve unaffected requirements and their order.
- Show the planned added, modified, removed, and renamed counts.

Write only after the merge is internally consistent. If a conflict cannot be
resolved from the artifacts and repository, pause and ask the user.

## Completion

Report a per-capability summary and confirm that
`openspec/changes/<name>/` remains active. Do not edit code, tasks, or archive
the change.
