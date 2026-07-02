# Matt Pocock Misc

Matt Pocock's occasional-use skills — git guardrails, pre-commit setup, exercise scaffolding, and shoehorn migration.

> Converted from the [`mattpocock/skills`](https://github.com/mattpocock/skills) `misc` skills. Each skill is exposed as a Spec Kit command; bundled reference files live in `resources/`.

## Installation

```bash
specify extension add mattpocock-misc
```

## Commands

| Command | Purpose |
|---------|---------|
| `/speckit.mattpocock-misc.git-guardrails-claude-code` | Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use when user wants to prevent destructive git operations, add git safety hooks, or block git push/reset in Claude Code. |
| `/speckit.mattpocock-misc.migrate-to-shoehorn` | Migrate test files from `as` type assertions to @total-typescript/shoehorn. Use when user mentions shoehorn, wants to replace `as` in tests, or needs partial test data. |
| `/speckit.mattpocock-misc.scaffold-exercises` | Create exercise directory structures with sections, problems, solutions, and explainers that pass linting. Use when user wants to scaffold exercises, create exercise stubs, or set up a new course section. |
| `/speckit.mattpocock-misc.setup-pre-commit` | Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current repo. Use when user wants to add pre-commit hooks, set up Husky, configure lint-staged, or add commit-time formatting/typechecking/testing. |

## Source

Skills sourced from [https://github.com/mattpocock/skills](https://github.com/mattpocock/skills) (`skills/misc/`). Regenerate with the `sync-mattpocock-skills` prompt to keep them up to date.
