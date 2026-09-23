---
description: "Verify that an implementation matches its change proposal artifacts."
argument-hint: "[change name]"
scripts:
  py: scripts/python/change.py
---

## User Input

```text
$ARGUMENTS
```

Perform a read-only verification of planning completeness and implementation
alignment.

## Select and Load

1. Select the change from the input, conversation, or `{SCRIPT} list --json`.
   Ask if ambiguous.
2. Run `{SCRIPT} status --change "<name>" --json`.
3. Read every planning artifact.
4. Inspect all implementation and test files referenced by the tasks, plus
   nearby code needed to verify behavior.
5. Run relevant non-destructive tests, builds, linters, or checks when
   available.

## Verification Dimensions

### Completeness

- Every planned artifact exists.
- Every requirement has implementation evidence.
- Every scenario has test or direct validation evidence.
- Every task is checked only when its work is present.

### Correctness

- Implemented behavior satisfies requirement language and scenarios.
- Edge cases and failure paths match the plan.
- Tests exercise the specified behavior rather than a weaker proxy.
- Compatibility and migration requirements are satisfied.

### Coherence

- Implementation follows recorded design decisions.
- Naming and behavior remain consistent across artifacts and code.
- No task introduces unplanned behavior or leaves stale documentation.
- Main specs and delta specs do not contradict each other.

## Findings

Classify findings:

- **CRITICAL**: Missing required behavior, unsafe mismatch, or falsely
  completed task
- **WARNING**: Partial coverage, design drift, weak validation, or unresolved
  inconsistency
- **SUGGESTION**: Non-blocking clarity or maintainability improvement

For each finding include evidence, affected requirement/task, and a concrete
recommendation. Do not edit files.

## Output

Provide:

| Dimension | Result | Evidence |
|-----------|--------|----------|
| Completeness | PASS/PARTIAL/FAIL | Summary |
| Correctness | PASS/PARTIAL/FAIL | Summary |
| Coherence | PASS/PARTIAL/FAIL | Summary |

Then list findings by severity and conclude whether the change is ready for
`__SPECKIT_COMMAND_OPENSPEC_ARCHIVE__`.
