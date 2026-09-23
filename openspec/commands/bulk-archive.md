---
description: "Synchronize and archive multiple completed change proposals."
scripts:
  py: scripts/python/change.py
---

Archive several active changes as one reviewed batch.

## Selection

1. Run `{SCRIPT} list --json`.
2. If no active changes exist, report that and stop.
3. Present each change with planning status and completed/total tasks.
4. Ask the user to select any number of changes or all changes.
5. Load every selected change and identify capabilities touched by more than
   one selected delta.

## Preflight

For each selected change:

- List missing artifacts.
- List incomplete tasks.
- Determine whether each delta is already represented in the main spec.
- Flag archive-path collisions.

For shared capabilities:

1. Inspect implementation evidence to determine which deltas shipped.
2. Order applicable deltas from oldest to newest using the change directory
   modification time and artifact history.
3. Detect contradictory modifications, removals, or renames.
4. Stop and ask the user if ordering or intended final behavior is unclear.

Show one batch table and request a single confirmation:

| Change | Artifacts | Tasks | Spec sync | Warnings |
|--------|-----------|-------|-----------|----------|

## Execute

After confirmation, process changes in the established order:

1. Synchronize outstanding deltas using the merge rules from
   `__SPECKIT_COMMAND_OPENSPEC_SYNC__`.
2. Validate affected main specs.
3. Run `{SCRIPT} archive --change "<name>" --json`.
4. If one change fails, record the failure and continue only when later changes
   do not depend on its spec updates. Otherwise stop the dependent chain.

## Completion

Report:

| Change | Sync result | Archive result | Final path or error |
|--------|-------------|----------------|---------------------|

Summarize archived, skipped, and failed counts. Never claim an archive or sync
succeeded unless the filesystem change completed.
