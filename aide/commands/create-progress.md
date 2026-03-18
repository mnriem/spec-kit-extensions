---
description: "Create a progress tracking file from the vision and roadmap."
---

# Create Progress File

Create a progress tracking file to monitor project completion.

## Purpose

This is Step 3 of the AI-Driven Engineering workflow. The progress file provides visibility into which features and capabilities have been completed, are in progress, or are still planned.

## Prerequisites

- `docs/aide/vision.md` must exist (created by `/speckit.aide.create-vision`)
- `docs/aide/roadmap.md` must exist (created by `/speckit.aide.create-roadmap`)

## Instructions

Read both `docs/aide/vision.md` and `docs/aide/roadmap.md`. If `docs/aide/progress.md` already exists, **update it incrementally** — do not regenerate from scratch. If it does not exist, create it.

### Updating an Existing Progress File

When updating an existing progress file:

1. **Preserve all existing statuses** — never change a ✅, 🚧, ⏸️, or ❌ status back to 📋.
2. **Add new items** for any stages, deliverables, or features that appear in the roadmap but are not yet tracked in the progress file.
3. **Do not remove items** — even if they no longer appear in the roadmap, keep them and mark as ⏸️ Deferred (with a note) rather than deleting.
4. **Preserve acceptance criteria checkboxes** — do not uncheck any already-checked criteria.

### Requirements

1. **Comprehensive coverage** — every feature, capability, and deliverable from the vision and roadmap should be tracked
2. **Status tracking** — use status icons to indicate state:
   - 📋 Planned
   - 🚧 In Progress
   - ✅ Complete
   - ⏸️ Deferred
   - ❌ Excluded
3. **Organized by stage** — group items according to the roadmap stages
4. **Actionable** — each item should be specific enough to verify completion

### Output

Save the completed progress file to `docs/aide/progress.md`.

## Next Step

After reviewing the progress file, start a **new chat session** and run `/speckit.aide.create-queue` to generate the first batch of prioritized work items.
