---
description: "Generate a prioritized queue of the next batch of work items."
---

# Create Queue

Generate the next batch of prioritized work items.

## Purpose

This is Step 4 of the AI-Driven Engineering workflow. The queue contains the next ~10 actionable work items prioritized from the roadmap and progress documents. This step is repeated whenever the current queue is exhausted.

## Prerequisites

- `docs/aide/vision.md` must exist
- `docs/aide/roadmap.md` must exist
- `docs/aide/progress.md` must exist

## Instructions

Read `docs/aide/vision.md`, `docs/aide/roadmap.md`, and `docs/aide/progress.md`, then create a prioritized queue of work items.

### Requirements

1. **Next logical items** — select the next ~10 items based on roadmap priority and current progress
2. **No duplicates** — check existing queues in `docs/aide/queue/queue-*.md` to avoid re-queuing completed or already-queued items
3. **Sequential numbering** — work item numbers must be sequential across all queues. Check existing queues to find the highest item number used, then start from the next number. For example, if `queue-001.md` ends at item 10, `queue-002.md` starts at item 11.
4. **Testable items** — each item must be testable locally
5. **Week-sized batch** — the total work in the queue should be deliverable in about a week
6. **Consistent format** — each item must follow this format so other commands can parse it:
   ```
   ### Item NNN: Short Title
   Brief description of the scope and deliverables for this item.
   ```
   Where NNN is the sequential item number (e.g., 001, 012, 023).

### Queue Naming

Name the queue file sequentially: `queue-001.md`, `queue-002.md`, etc.

### Output

Save the queue to `docs/aide/queue/queue-NNN.md` (where NNN is the next sequential number).

## Next Step

Select an item from the queue and start a **new chat session**. Run `/speckit.aide.create-item` with the item description to create a detailed work item specification.
