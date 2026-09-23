---
description: "Revise a change proposal's existing planning artifacts and keep them coherent."
argument-hint: "[change name] [revision]"
scripts:
  py: scripts/python/change.py
---

## User Input

```text
$ARGUMENTS
```

Revise existing planning artifacts without creating missing artifacts or
editing implementation code.

## Workflow

1. Select the change from the input, conversation, or `{SCRIPT} list --json`.
   Ask if the selection is ambiguous.
2. Run `{SCRIPT} status --change "<name>" --json`.
3. Read every existing artifact under `openspec/changes/<name>/`.
4. Inspect relevant source and tests when needed to check whether the plan still
   matches reality.
5. Determine the requested revision. If none was provided, perform a coherence
   review covering:
   - Proposal scope versus specification requirements
   - Design decisions versus requirements
   - Task coverage versus every requirement and scenario
   - Contradictions, duplication, terminology drift, and stale assumptions
6. Present proposed changes one artifact at a time. Explain why each revision
   is needed and wait for confirmation before writing it.
7. After each approved edit, re-read the affected artifacts and preserve
   consistency across the complete planning package.

## Boundaries

- Edit only artifact files that already exist.
- Do not create a missing proposal, spec, design, or tasks file; point to
  `__SPECKIT_COMMAND_OPENSPEC_CONTINUE__`.
- Do not edit project code or mark tasks complete.
- If implementation already exists, warn that plan revisions may require
  another `__SPECKIT_COMMAND_OPENSPEC_APPLY__` pass.
- If the requested revision changes the original intent rather than refining
  it, recommend a new change via `__SPECKIT_COMMAND_OPENSPEC_NEW__`.

## Completion

Report each artifact revised, the consistency checks performed, and any
follow-up implementation or missing-artifact work.
