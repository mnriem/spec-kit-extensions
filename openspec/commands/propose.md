---
description: "Create a change proposal and all planning artifacts required for implementation."
argument-hint: "<change name or description>"
scripts:
  py: scripts/python/change.py
---

## User Input

```text
$ARGUMENTS
```

Create a complete planning package. This command writes planning artifacts
only; it must not edit implementation code.

## Workflow

1. Understand the requested change. If the input is empty or materially
   ambiguous, ask one focused question and wait.
2. Derive a concise kebab-case change name. If the user supplied a name, keep
   it after validation.
3. Run `{SCRIPT} list --json`. If the name already exists, stop and ask whether
   to use `__SPECKIT_COMMAND_OPENSPEC_FF__` to complete it or choose a new name.
4. Run:

   ```text
   {SCRIPT} new --change "<name>" --json
   ```

5. Read these bundled templates:
   - `templates/proposal.md`
   - `templates/spec.md`
   - `templates/design.md`
   - `templates/tasks.md`
6. Inspect relevant source, tests, configuration, and documentation. Ground the
   proposal in existing behavior and conventions.
7. Create `openspec/changes/<name>/proposal.md`.
8. Identify every affected capability. For each capability, create
   `openspec/changes/<name>/specs/<capability-path>/spec.md`.
   - Preserve existing nested capability paths.
   - Use ADDED, MODIFIED, REMOVED, and RENAMED sections.
   - Write complete replacement text for modified requirements.
   - Give every requirement at least one observable scenario.
9. Create `openspec/changes/<name>/design.md`.
   - Record meaningful technical decisions and alternatives.
   - For a simple change, state why no complex design is required rather than
     omitting the file.
10. Create `openspec/changes/<name>/tasks.md`.
    - Order tasks by dependency.
    - Include exact file paths and validation commands where known.
    - Ensure every requirement is covered by one or more tasks.
    - Keep all tasks unchecked.
11. Run `{SCRIPT} status --change "<name>" --json` and verify all four artifact
    categories are complete.

## Quality Rules

- Proposal explains why and what, not implementation detail.
- Specifications define testable behavior.
- Design explains how and why.
- Tasks are executable and trace back to the specifications.
- Record minor assumptions; ask about decisions that materially alter behavior.
- Do not implement any task in this command.

## Completion

Report the change path, capabilities, artifacts created, assumptions, and any
open questions. End by pointing to `__SPECKIT_COMMAND_OPENSPEC_APPLY__`.
