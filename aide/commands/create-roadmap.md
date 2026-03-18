---
description: "Generate a staged development roadmap from the vision document."
---

# Create Roadmap

Generate a staged development roadmap based on the project vision.

## Purpose

This is Step 2 of the AI-Driven Engineering workflow. The roadmap breaks the vision into deliverable stages, each producing a demonstrable version of the project.

## Prerequisites

- `docs/aide/vision.md` must exist (created by `/speckit.aide.create-vision`)

## Instructions

Read `docs/aide/vision.md`. If `docs/aide/roadmap.md` already exists, **update it incrementally** — do not regenerate from scratch. If it does not exist, create it.

### Updating an Existing Roadmap

When updating an existing roadmap:

1. **Read `docs/aide/progress.md` first** to determine which stages are completed or in progress.
2. **Completed and in-progress stages are immutable** — never modify their goals, deliverables, dependencies, or acceptance criteria.
3. **Add new stages** at the end of the roadmap to cover new or changed vision features.
4. **Only planned/not-started stages may be edited** — adjust goals, deliverables, or acceptance criteria as needed.

### Requirements

1. **Staged delivery** — break the vision into incremental stages that build on each other
2. **Each stage is demonstrable** — every stage must deliver a version that can be shown and tested
3. **Each stage is testable** — include clear acceptance criteria per stage
4. **Logical progression** — features should flow naturally from foundational to advanced
5. **Prescriptive detail** — assume most work will be done by AI, so be as specific as possible
6. **Realistic scope** — each stage should be deployable locally and deliverable in about a week

### Output Format

Generate the document with:
- Description of each stage and its goals
- Bulleted list of specific deliverables per stage
- Dependencies between stages (if any)
- Testing/validation criteria per stage

### Output

Save the completed roadmap to `docs/aide/roadmap.md`.

## Next Step

After reviewing the roadmap, start a **new chat session** and run `/speckit.aide.create-progress` to create the progress tracking file.
