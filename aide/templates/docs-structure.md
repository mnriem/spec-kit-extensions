# AIDE Document Structure Reference

This document describes the file structure created and maintained by the AIDE workflow.

## Directory Layout

```
your-project/
├── docs/
│   └── aide/
│       ├── vision.md              # Step 1: Product vision and scope
│       ├── roadmap.md             # Step 2: Staged development plan
│       ├── progress.md            # Step 3: Feature tracking
│       ├── queue/
│       │   ├── queue-001.md       # Step 4: First batch of work items
│       │   ├── queue-002.md       # Step 4: Second batch
│       │   └── ...
│       └── items/
│           ├── 001-feature.md     # Step 5: Detailed work item spec
│           ├── 002-setup.md       # Step 5: Another work item
│           └── ...
```

## Document Descriptions

### vision.md

The foundation document. Contains the complete project vision including goals, features, technology choices, constraints, and scope boundaries. Created once, updated via the feedback loop when scope changes.

### roadmap.md

A staged delivery plan derived from the vision. Each stage produces a demonstrable, testable version. Stages build incrementally and are sized to be deliverable in about a week. Updated via the feedback loop when priorities shift.

### progress.md

A checklist tracking every feature and deliverable from the vision and roadmap. Uses status icons:

| Icon | Status |
|------|--------|
| 📋 | Planned |
| 🚧 | In Progress |
| ✅ | Complete |
| ⏸️ | Deferred |
| ❌ | Excluded |

Updated during work item execution (Step 6).

### queue/queue-NNN.md

Batches of ~10 prioritized work items. Each queue is numbered sequentially. Work item numbers are sequential across all queues (queue-002 starts where queue-001 left off). Generated from the roadmap, progress, and vision documents.

### items/NNN-descriptive-name.md

Detailed work item specifications including:
- Description and acceptance criteria
- Implementation steps
- Testing prerequisites (services, configuration, validation checklist)
- Expected outcomes
- Decisions & trade-offs log (updated during implementation)

## Workflow Summary

```
Steps 1-3: Done once at project start
Step 4: Generate queue of ~10 work items
Steps 5-6: Repeat for each item (create spec → implement → update progress)
Step 4 again: When queue is empty, generate next batch
Step 7: Feedback loop — use at any point when issues arise
```
