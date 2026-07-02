# Matt Pocock Engineering

Matt Pocock's engineering skills for daily code work — TDD, code review, diagnosing bugs, domain modeling, prototyping, research, and issue/PRD workflows.

> Converted from the [`mattpocock/skills`](https://github.com/mattpocock/skills) `engineering` skills. Each skill is exposed as a Spec Kit command; bundled reference files live in `resources/`.

## Installation

```bash
specify extension add mattpocock-engineering
```

## Commands

| Command | Purpose |
|---------|---------|
| `/speckit.mattpocock-engineering.ask-matt` | Ask which skill or flow fits your situation. A router over the skills in this repo. |
| `/speckit.mattpocock-engineering.code-review` | Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes — Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/PRD asked for?). Runs both reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to "review since X". |
| `/speckit.mattpocock-engineering.codebase-design` | Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more testable or AI-navigable, or when another skill needs the deep-module vocabulary. |
| `/speckit.mattpocock-engineering.diagnosing-bugs` | Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow. |
| `/speckit.mattpocock-engineering.domain-modeling` | Build and sharpen a project's domain model. Use when the user wants to pin down domain terminology or a ubiquitous language, record an architectural decision, or when another skill needs to maintain the domain model. |
| `/speckit.mattpocock-engineering.grill-with-docs` | A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go. |
| `/speckit.mattpocock-engineering.implement` | Implement a piece of work based on a PRD or set of issues. |
| `/speckit.mattpocock-engineering.improve-codebase-architecture` | Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick. |
| `/speckit.mattpocock-engineering.prototype` | Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should look like. |
| `/speckit.mattpocock-engineering.research` | Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent. |
| `/speckit.mattpocock-engineering.resolving-merge-conflicts` | Use when you need to resolve an in-progress git merge/rebase conflict. |
| `/speckit.mattpocock-engineering.setup-matt-pocock-skills` | Configure this repo for the engineering skills — set up its issue tracker, triage label vocabulary, and domain doc layout. Run once before first use of the other engineering skills. |
| `/speckit.mattpocock-engineering.tdd` | Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests. |
| `/speckit.mattpocock-engineering.to-issues` | Break a plan, spec, or PRD into independently-grabbable issues on the project issue tracker using tracer-bullet vertical slices. |
| `/speckit.mattpocock-engineering.to-prd` | Turn the current conversation into a PRD and publish it to the project issue tracker — no interview, just synthesis of what you've already discussed. |
| `/speckit.mattpocock-engineering.triage` | Move issues and external PRs through a state machine of triage roles — categorise, verify, grill if needed, and write agent-ready briefs. |

## Source

Skills sourced from [https://github.com/mattpocock/skills](https://github.com/mattpocock/skills) (`skills/engineering/`). Regenerate with the `sync-mattpocock-skills` prompt to keep them up to date.
