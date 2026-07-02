# gstack

The [gstack](https://github.com/garrytan/gstack) skill suite, packaged as a single Spec Kit extension. Every gstack skill is exposed as a `/speckit.gstack.<slug>` command.

Pinned to gstack `v1.58.5.0` (commit `11de390be1be6849eb9a15f91ff4922dd16c589a`).

## Why one extension?

gstack skills are not independent: they share a `bin/`/`scripts/`/`lib/` runtime and call each other through absolute paths, and the browser/design tools are compiled by `bun` at setup. Packaging the suite as one extension keeps those references intact.

## Integration-agnostic

Upstream gstack bakes the Claude-specific path `~/.claude/skills/gstack` into its skills. Because the runtime is relocatable (its `bin/` scripts self-locate and honor `GSTACK_DIR`), this extension rewrites that path to a neutral home, `~/.gstack/runtime`, and `/speckit.gstack.setup` exports `GSTACK_DIR` to match — so the commands work under any Spec Kit integration (Copilot, Codex, Cursor, Claude, …), not just Claude Code.

## Installation

```bash
specify extension add gstack
```

Then run the one-time setup to install the gstack runtime:

```
/speckit.gstack.setup
```

## Commands

| Command | Purpose |
|---------|---------|
| `/speckit.gstack.setup` | One-time setup: install the pinned gstack runtime so /speckit.gstack.* commands work. |
| `/speckit.gstack.autoplan` | Auto-review pipeline — reads the full CEO, design, eng, and DX review skills from disk and runs them sequentially with auto-decisions using 6 decision principles. |
| `/speckit.gstack.benchmark` | Performance regression detection using the browse daemon. |
| `/speckit.gstack.benchmark-models` | Cross-model benchmark for gstack skills. |
| `/speckit.gstack.browse` | Fast headless browser for QA testing and site dogfooding. |
| `/speckit.gstack.hackernews-frontpage` | Scrape the Hacker News front page (titles, points, comment counts). |
| `/speckit.gstack.canary` | Post-deploy canary monitoring. |
| `/speckit.gstack.careful` | Safety guardrails for destructive commands. |
| `/speckit.gstack.codex` | OpenAI Codex CLI wrapper — three modes. |
| `/speckit.gstack.context-restore` | Restore working context saved earlier by /context-save. |
| `/speckit.gstack.context-save` | Save working context. |
| `/speckit.gstack.cso` | Chief Security Officer mode. |
| `/speckit.gstack.design-consultation` | Design consultation: understands your product, researches the landscape, proposes a complete design system (aesthetic, typography, color, layout, spacing, motion), and generates font+color preview... |
| `/speckit.gstack.design-html` | Design finalization: generates production-quality Pretext-native HTML/CSS. |
| `/speckit.gstack.design-review` | Designer's eye QA: finds visual inconsistency, spacing issues, hierarchy problems, AI slop patterns, and slow interactions — then fixes them. |
| `/speckit.gstack.design-shotgun` | Design shotgun: generate multiple AI design variants, open a comparison board, collect structured feedback, and iterate. |
| `/speckit.gstack.devex-review` | Live developer experience audit. |
| `/speckit.gstack.diagram` | Turn an English description (or mermaid source) into a diagram triplet: the source, an editable .excalidraw file you can open |
| `/speckit.gstack.document-generate` | Generate missing documentation from scratch for a feature, module, or entire project. |
| `/speckit.gstack.document-release` | Post-ship documentation update. |
| `/speckit.gstack.freeze` | Restrict file edits to a specific directory for the session. |
| `/speckit.gstack.upgrade` | Upgrade gstack to the latest version. |
| `/speckit.gstack.guard` | Full safety mode: destructive command warnings + directory-scoped edits. |
| `/speckit.gstack.health` | Code quality dashboard. |
| `/speckit.gstack.investigate` | Systematic debugging with root cause investigation. |
| `/speckit.gstack.ios-clean` | Remove the DebugBridge SPM package and all #if DEBUG wiring from an iOS app. |
| `/speckit.gstack.ios-design-review` | Visual design audit for iOS apps on real hardware. |
| `/speckit.gstack.ios-fix` | Autonomous iOS bug fixer. |
| `/speckit.gstack.ios-qa` | Live-device iOS QA for SwiftUI apps. |
| `/speckit.gstack.ios-sync` | Regenerate the iOS debug bridge against the latest upstream gstack templates. |
| `/speckit.gstack.land-and-deploy` | Land and deploy workflow. |
| `/speckit.gstack.landing-report` | Read-only queue dashboard for workspace-aware ship. |
| `/speckit.gstack.learn` | Manage project learnings. |
| `/speckit.gstack.make-pdf` | Turn any markdown file into a publication-quality PDF. |
| `/speckit.gstack.office-hours` | YC Office Hours — two modes. |
| `/speckit.gstack.open-gstack-browser` | Launch GStack Browser — AI-controlled Chromium with the sidebar extension baked in. |
| `/speckit.gstack.openclaw-ceo-review` | Use when asked to review a plan, challenge a proposal, run a CEO review, poke holes in an approach, think bigger about scope, or decide whether to expand or reduce the plan. |
| `/speckit.gstack.openclaw-investigate` | Use when asked to debug, fix a bug, investigate an error, or do root cause analysis, and when users report errors, stack traces, unexpected behavior, or say something stopped working. |
| `/speckit.gstack.openclaw-office-hours` | Use when asked to brainstorm, evaluate whether an idea is worth building, run office hours, or think through a new product idea or design direction before any code is written. |
| `/speckit.gstack.openclaw-retro` | Weekly engineering retrospective. Analyzes commit history, work patterns, and code quality metrics with persistent history and trend tracking. Team-aware with per-person contributions, praise, and growth areas. Use when asked for weekly retro, what shipped this week, or engineering retrospective. |
| `/speckit.gstack.pair-agent` | Pair a remote AI agent with your browser. |
| `/speckit.gstack.plan-ceo-review` | CEO/founder-mode plan review. |
| `/speckit.gstack.plan-design-review` | Designer's eye plan review — interactive, like CEO and Eng review. |
| `/speckit.gstack.plan-devex-review` | Interactive developer experience plan review. |
| `/speckit.gstack.plan-eng-review` | Eng manager-mode plan review. |
| `/speckit.gstack.plan-tune` | Self-tuning question sensitivity + developer psychographic for gstack (v1: observational). |
| `/speckit.gstack.qa` | Systematically QA test a web application and fix bugs found. |
| `/speckit.gstack.qa-only` | Report-only QA testing. |
| `/speckit.gstack.retro` | Weekly engineering retrospective. |
| `/speckit.gstack.review` | Pre-landing PR review. |
| `/speckit.gstack.scrape` | Pull data from a web page. |
| `/speckit.gstack.setup-browser-cookies` | Import cookies from your real Chromium browser into the headless browse session. |
| `/speckit.gstack.setup-deploy` | Configure deployment settings for /land-and-deploy. |
| `/speckit.gstack.setup-gbrain` | Set up gbrain for this coding agent: install the CLI, initialize a local PGLite or Supabase brain, register MCP, capture per-remote trust policy. |
| `/speckit.gstack.ship` | Ship workflow: detect + merge base branch, run tests, review diff, bump VERSION, update CHANGELOG, commit, push, create PR. |
| `/speckit.gstack.skillify` | Codify the most recent successful /scrape flow into a permanent browser-skill on disk. |
| `/speckit.gstack.spec` | Turn vague intent into a precise, executable spec in five phases. |
| `/speckit.gstack.sync-gbrain` | Keep gbrain current with this repo's code and refresh agent search guidance in CLAUDE.md. Wraps the gstack-gbrain-sync orchestrator with state |
| `/speckit.gstack.unfreeze` | Clear the freeze boundary set by /freeze, allowing edits to all directories again. |

## Keeping up to date

Regenerated from upstream by [`.github/prompts/sync-gstack-skills.prompt.md`](../.github/prompts/sync-gstack-skills.prompt.md) / `scripts/sync_gstack_skills.py`. Re-running re-pins the setup command to the matching gstack commit.
