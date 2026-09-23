---
description: "Think through an idea, investigate a problem, or clarify requirements without implementing."
argument-hint: "[topic or change]"
scripts:
  py: scripts/python/change.py
---

## User Input

```text
$ARGUMENTS
```

Enter a read-only thinking mode. Investigate the repository, existing
specifications, and active changes, but do not implement code.

## Context Discovery

1. Run `{SCRIPT} list --json` to discover active changes.
2. If the input names an active change, run:

   ```text
   {SCRIPT} status --change "<name>" --json
   ```

   Read every existing artifact under `openspec/changes/<name>/`.
3. Inspect relevant source, tests, configuration, and documentation before
   asking factual questions the repository can answer.
4. Distinguish observed behavior, confirmed decisions, assumptions, and open
   questions.

## Exploration Stance

- Follow the user's thread rather than imposing a fixed questionnaire.
- Ask one focused question at a time when a decision materially affects scope,
  behavior, compatibility, or acceptance criteria.
- Compare viable options with concrete trade-offs.
- Use diagrams or tables when they make relationships clearer.
- Challenge hidden assumptions and identify edge cases.
- Do not write implementation code, modify configuration, or start applying a
  change.

## Optional Capture

Do not write files unless the user explicitly asks to capture the exploration.
Before writing, state exactly which artifacts will change.

For a new change:

1. Derive a unique kebab-case name.
2. Run `{SCRIPT} new --change "<name>" --json`.
3. Read the relevant templates under `templates/`.
4. Create only the artifacts the user requested under
   `openspec/changes/<name>/`.

For an existing change, update only the explicitly requested planning
artifacts. Never mark tasks complete or modify project code.

## Completion

Summarize:

- Problem or opportunity
- Relevant evidence
- Decisions made
- Assumptions
- Open questions
- Recommended next step

When the idea is ready to become a complete plan, point to
`__SPECKIT_COMMAND_OPENSPEC_PROPOSE__`. Implementation starts only through
`__SPECKIT_COMMAND_OPENSPEC_APPLY__`.
