---
description: "Implement a work item and update progress tracking."
---

# Execute Work Item

Implement a work item as specified in the docs/aide/items/ directory.

## Purpose

This is Step 6 of the AI-Driven Engineering workflow. This step takes a detailed work item specification and implements it — writing code, tests, configuration, and documentation as specified.

## User Input

$ARGUMENTS

## Instructions

### Item Selection

If `$ARGUMENTS` is provided, treat it as an item number. Find the matching file in `docs/aide/items/` (e.g., item 5 maps to `docs/aide/items/005-*.md`).

If `$ARGUMENTS` is empty, automatically pick the next item:
1. Read `docs/aide/progress.md` and scan `docs/aide/items/` for existing work item files
2. Select the first work item whose status in `docs/aide/progress.md` is 📋 (Planned) — i.e., it has a spec but hasn't been started yet
3. Tell the user which item was auto-selected before proceeding

### During Implementation

1. **Follow the specification** — implement exactly what the work item describes
2. **Document decisions** — as you make implementation choices, UPDATE the work item's "Decisions & Trade-offs" section with:
   - What was decided
   - Why this approach over alternatives
   - Any trade-offs or future considerations
3. **Update progress** — update `docs/aide/progress.md` status:
   - 📋 → 🚧 when starting implementation
   - 🚧 → ✅ when implementation is complete
4. **Scope your updates** — only update progress rows that correspond to YOUR item number. Do NOT mark other items as complete, even if their criteria happen to be satisfied as a side effect of your work. Each item must go through its own create-item → execute-item cycle.

### On Smooth Completion

- No feedback loop needed
- Ensure work item decisions are documented
- Mark progress as complete

### On Issues

If you encounter problems (unclear requirements, blocked, need help):
- Document the issue in the work item
- Tell the user to run `/speckit.aide.feedback-loop` to adjust the process

## Next Step

- **More items in queue?** Start a **new chat session** and run `/speckit.aide.create-item` for the next queue item, then `/speckit.aide.execute-item` to implement it.
- **Queue exhausted?** Start a **new chat session** and run `/speckit.aide.create-queue` to generate the next batch.
- **All stages complete?** The project is done!
