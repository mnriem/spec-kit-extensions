---
description: "Analyze issues and suggest improvements to the process and documents."
---

# Feedback Loop

Analyze what went wrong and identify improvements needed.

## Purpose

This is Step 7 of the AI-Driven Engineering workflow. Use this whenever work didn't go smoothly — when you needed help, found unclear requirements, or the process broke down. This step is available at any point in the workflow.

## Instructions

Analyze the current state of the project documents and recent work to identify improvements.

### 1. Document Gaps

- What should have been in `docs/aide/vision.md` but wasn't?
- What should have been in `docs/aide/roadmap.md` (dependencies, prerequisites)?
- What should have been in `docs/aide/progress.md` for tracking?
- Was the work item specification missing critical information?

### 2. Process Issues

- Did the human need to intervene? Why?
- Were requirements unclear or ambiguous?
- Were dependencies not identified upfront?
- Did scope expand unexpectedly?

### 3. Command Adaptations Needed

The AIDE commands may need project-specific adjustments. Because Spec Kit installs extension commands into agent-specific directories, the installed copies must be located and updated:

**Finding installed commands:**
- Look for AIDE command files in agent-specific directories such as:
  - `.claude/commands/` (Claude Code)
  - `.github/prompts/` (GitHub Copilot commands)
  - `.github/agents/` (GitHub Copilot agents)
  - `.gemini/commands/` (Gemini CLI)
  - `.cursor/commands/` (Cursor)
  - Or any other agent directory present in the project
- Also check for installed skills (e.g., in `.github/skills/` or similar)
- Search for files containing `speckit.aide` to locate all installed copies

**What to adapt:**
- Should the create-item command be adapted for this project's needs?
  - Example: Add "API Contract" section for API-heavy projects
  - Example: Add "Database Migration" section for data-intensive projects
  - Example: Add "Security Review" section for sensitive systems
- Should we create project-specific commands? (e.g., testing strategy, deployment checklist)
- What worked well that we should keep?

**When modifying commands**, update the installed copies in the agent-specific directories — these are the files that actually get executed.

### 4. Recommendations

Provide specific, actionable suggestions:
- Updates to vision/roadmap/progress
- Changes to command templates
- New commands to create
- Process improvements

### Important Notes

- **Routine decisions** during smooth implementation belong in the work item's "Decisions" section, not here.
- This feedback loop is for **systemic issues** that need process, document, or command improvements.
- **Be minimal** — suggest the smallest set of changes that will prevent the problem from recurring.

## Next Step

After applying the recommended changes, resume the workflow from where you left off. Start a **new chat session** for the next step.
