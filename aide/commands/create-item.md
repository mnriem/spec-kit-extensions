---
description: "Create a detailed work item specification from a queue item."
---

# Create Work Item

Create a comprehensive work item specification.

## Purpose

This is Step 5 of the AI-Driven Engineering workflow. Work items are detailed specifications that contain everything needed to implement a feature, including acceptance criteria, testing prerequisites, and validation checklists.

## User Input

$ARGUMENTS

## Instructions

### Item Selection

If `$ARGUMENTS` is provided, treat it as an item number. Look up that item in the queue files under `docs/aide/queue/` and use its description to create the work item.

If `$ARGUMENTS` is empty, automatically pick the next item:
1. Read the most recent queue file in `docs/aide/queue/` (highest numbered `queue-NNN.md`)
2. Cross-reference with existing work items in `docs/aide/items/` and status in `docs/aide/progress.md`
3. Select the first item from the queue that does **not** already have a corresponding work item file in `docs/aide/items/`. A ✅ or 🚧 mark in progress.md alone is NOT sufficient to skip an item — the work item file must also exist. If progress.md shows ✅ but no work item file exists, flag this to the user as a potential inconsistency before proceeding.
4. Tell the user which item was auto-selected before proceeding

### Work Item Creation

Create a comprehensive work item specification for the selected item and save it to `docs/aide/items/NNN-descriptive-name.md`.

### Required Sections

The work item MUST include:

#### 1. Standard Sections
- Description
- Acceptance criteria
- Implementation steps
- Testing strategy
- Dependencies

#### 2. Decision Log
Add a "Decisions & Trade-offs" section where implementation decisions will be documented as work progresses. Initialize with "To be updated during implementation."

#### 3. Completion Reminder
Note that `docs/aide/progress.md` MUST be updated (📋 → 🚧 → ✅) when the item is completed.

#### 4. Project-Specific Adaptations
If this project has unique needs (e.g., specific test strategy, deployment process), adapt the template accordingly. Document any template changes in the work item.

#### 5. Testing Prerequisites (CRITICAL)

Document exactly what's needed to test the feature:

**Required Services**
- List all external services needed (databases, APIs, message queues, etc.)
- For each service: name, version, Docker image/command to start, port
- Example: PostgreSQL 15+ (Docker: `docker compose up -d postgres`, Port: 5432)

**Environment Configuration**
- Environment variables required
- User secrets to set (with example commands)
- Configuration files to create
- Ports that must be available

**Manual Validation Checklist**
- [ ] Build succeeds
- [ ] Tests pass (if applicable)
- [ ] **Services started**: List commands to start required services
- [ ] **Application runs**: List command to start application
- [ ] **Feature verified**: Specific steps to verify the feature works
- [ ] **Data verified**: Database queries, API calls, or file checks to verify data
- [ ] **Health checks pass**: URL and expected response

**Expected Outcomes**
Provide concrete, verifiable results:
- For database work: "7 tables created (list names)", "4 seed users with hashed passwords"
- For API work: "Endpoint responds 200 OK", "Response contains expected fields"
- For UI work: "Page loads without errors", "Form submission succeeds"

**Validation Documentation Template**

```markdown
## Validation Results
- [ ] Service started: [service name]
- [ ] Application started successfully
- [ ] Database tables verified: [list tables or N/A]
- [ ] Seed data verified: [describe or N/A]
- [ ] API endpoints verified: [list endpoints or N/A]
- [ ] Screenshots captured: [if UI changes]
```

#### 6. Project-Specific Sections (Add as needed)

### Output

Save the work item to `docs/aide/items/NNN-descriptive-name.md`.

## Next Step

Start a **new chat session** and run `/speckit.aide.execute-item` with the item number to implement it.
