---
description: "Create a comprehensive vision document for a new project."
---

# Create Vision

Create a comprehensive vision document for the project described below.

## Purpose

This is Step 1 of the AI-Driven Engineering workflow. The vision document is the foundation for all subsequent steps — roadmap, progress tracking, work items, and implementation all flow from this document.

## User Input

$ARGUMENTS

## Instructions

### Existing Vision Check

Before creating, check if `docs/aide/vision.md` already exists.
- If it exists, **warn the user** and show a brief summary of the existing vision.
- Ask for confirmation before overwriting.
- If the user wants to update rather than replace, incorporate their input as amendments to the existing document.

### Creating the Vision

Create (or update) the vision document and store it in `docs/aide/vision.md`.

### Requirements

1. **Be exhaustive** — cover all aspects of the project scope
2. **Explain reasoning** — justify what is included and why
3. **Document exclusions** — explicitly state what is out of scope and why
4. **Be specific** — include technology choices, constraints, and assumptions
5. **Structure clearly** — use headings, lists, and sections for readability

### Suggested Structure

The vision document should cover (adapt to the specific project):

- **Project Overview** — what is being built and why
- **Goals & Objectives** — measurable outcomes
- **Target Users** — who will use this and how
- **Core Features** — detailed feature descriptions
- **Technical Architecture** — technology stack, infrastructure, deployment
- **Non-Functional Requirements** — performance, security, scalability, accessibility
- **Constraints & Assumptions** — technical, business, and timeline constraints
- **Out of Scope** — what is explicitly excluded from this project
- **Success Criteria** — how to measure project success

### Output

Save the completed vision document to `docs/aide/vision.md`.

## Next Step

After reviewing the vision document, start a **new chat session** and run `/speckit.aide.create-roadmap` to generate a staged development roadmap.
