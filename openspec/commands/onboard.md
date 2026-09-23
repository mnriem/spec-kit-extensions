---
description: "Learn the workflow by completing a narrated cycle on a real starter change."
scripts:
  py: scripts/python/change.py
---

Guide the user through one small, real change while explaining each stage.
Pause for user input at every decision or write boundary.

## 1. Find a Starter Change

Inspect the repository for small, bounded opportunities such as:

- A clear TODO or FIXME
- Missing validation or error handling
- A small untested behavior
- Stale documentation
- A narrowly scoped developer-experience improvement

Present two or three candidates with expected scope and recommend the safest
one. Let the user choose or provide another idea.

## 2. Explore

Demonstrate the stance from `__SPECKIT_COMMAND_OPENSPEC_EXPLORE__`:

- Inspect relevant code and tests.
- Clarify the desired observable behavior.
- Identify scope, non-goals, and important edge cases.
- Do not write yet.

Summarize the proposed change and ask permission to create its planning
artifacts.

## 3. Create the Change

After approval:

1. Derive a kebab-case name.
2. Run `{SCRIPT} new --change "<name>" --json`.
3. Explain the artifact sequence: proposal, specs, design, tasks.

## 4. Build Artifacts One at a Time

For each category:

1. Read the matching template under `templates/`.
2. Explain what the artifact answers.
3. Draft it from repository evidence and confirmed decisions.
4. Show a concise summary before writing.
5. Write only after user confirmation.
6. Run `{SCRIPT} status --change "<name>" --json` and show progress.

Create all four categories before implementation.

## 5. Implement

Explain that `tasks.md` is the progress record. Ask whether to begin
implementation.

If approved, follow `__SPECKIT_COMMAND_OPENSPEC_APPLY__`:

- Implement one task at a time.
- Validate each task.
- Mark it complete only after success.
- Pause on ambiguity or scope expansion.

## 6. Verify

Run the read-only checks from `__SPECKIT_COMMAND_OPENSPEC_VERIFY__`. Explain
the completeness, correctness, and coherence results. Resolve blocking
findings before continuing.

## 7. Synchronize and Archive

Explain how delta specs update the main specs without losing change history.
Ask whether to synchronize and archive.

If approved:

1. Apply `__SPECKIT_COMMAND_OPENSPEC_SYNC__`.
2. Run `{SCRIPT} archive --change "<name>" --json`.

## Completion

Recap:

- The five-stage loop: explore, plan, implement, verify, archive
- Artifact paths created
- Code and tests changed
- Main specs updated
- Archive path

Point to `__SPECKIT_COMMAND_OPENSPEC_PROPOSE__` for the next independent
change.
