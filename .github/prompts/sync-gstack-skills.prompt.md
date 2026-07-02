---
description: "Sync the garrytan/gstack skill suite into the single, integration-agnostic `gstack` Spec Kit extension and refresh catalog.json."
---

# Sync gstack → the `gstack` Spec Kit extension

Reusable prompt to (re)generate **one** `gstack` extension that exposes every
skill in [garrytan/gstack](https://github.com/garrytan/gstack) as a
`/speckit.gstack.<slug>` command, plus a `/speckit.gstack.setup` command that
installs the shared gstack runtime. Run it whenever gstack changes.

## Why one extension (not 58)

gstack is a **monolithic suite**, not independent skills:

- Every skill calls a shared `bin/`/`scripts/`/`lib/` runtime (~2,400 references)
  and sibling skills, via absolute paths.
- The `browse`/`design` tools are compiled by [`bun`](https://bun.sh) at setup.

Splitting it into per-skill extensions breaks those references. Packaging the
whole suite as one extension keeps them intact: the skill *commands* live in the
extension, and the shared *runtime* is installed once by `/speckit.gstack.setup`.

## Integration-agnostic runtime

Upstream gstack bakes the Claude-specific path `~/.claude/skills/gstack` into its
skill bodies. The runtime itself is **relocatable** — its `bin/` scripts
self-locate via `dirname "$0"` and honor `GSTACK_DIR`. So the generator:

- rewrites `~/.claude/skills/gstack` → the neutral home **`~/.gstack/runtime`** in
  every command body (project-local `$_ROOT/.claude/...` override probes are left
  intact — they already fall back to the neutral home), and
- emits a `setup` command that installs the runtime there and exports
  `GSTACK_DIR` + `PATH`.

Result: the commands work under any Spec Kit integration (Copilot, Codex, Cursor,
Claude, …), not just Claude Code.

## What counts as a skill

Any directory in the gstack repo containing a `SKILL.md`, **except** the
repo-root router `SKILL.md`, anything under `test/`, and `*.tmpl`. Includes
nested skills (`openclaw/skills/*`, `browser-skills/*`).

## Naming

| Thing | Rule | Example |
|-------|------|---------|
| slug | frontmatter `name`, leading `gstack-` stripped | `gstack-openclaw-retro` → `openclaw-retro` |
| command | `speckit.gstack.<slug>` | `speckit.gstack.review` |
| setup | `speckit.gstack.setup` | (installs the runtime) |

## Generated layout

```
gstack/
├── extension.yml          # id: gstack, one command per skill + setup
├── README.md
├── CHANGELOG.md
├── LICENSE
└── commands/
    ├── setup.md           # installs pinned runtime to ~/.gstack/runtime
    ├── review.md          # skill body, paths rewritten to ~/.gstack/runtime
    └── … (one per skill)
```

The extension `version` tracks gstack's `VERSION`, and `setup.md` is **pinned to
the exact gstack commit** the bodies were generated from, so the runtime always
matches the commands.

## How to run

```bash
# Clones gstack, rebuilds the gstack extension + catalog.json, and removes any
# leftover first-pass gstack-<slug> dirs from earlier attempts:
python3 scripts/sync_gstack_skills.py --clean

# Or point at an existing checkout:
python3 scripts/sync_gstack_skills.py --gstack /path/to/gstack --clean
```

## After running

1. `git status` — review the `gstack/` extension and `catalog.json`.
2. Confirm `extension.yml` command count == number of files in `gstack/commands/`.
3. Confirm command bodies contain no `~/.claude/skills/gstack` (only the neutral
   `~/.gstack/runtime`, aside from the project-local override probes).
4. Confirm `setup.md` is pinned to the current gstack commit.
5. Commit.

## Known limitations

- `browse`, `design`, `scrape`, and other binary-backed skills need `bun`;
  `/speckit.gstack.setup` runs gstack's own installer when `bun` is present.
- Command bodies are copied faithfully. A few skills reference Claude-Code-only
  host features (e.g. plan-mode reminders) that degrade gracefully on other
  agents.
