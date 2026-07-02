# Sync `anthropic-skills-*` extensions from anthropics/skills

A reusable prompt for (re)generating and updating the `anthropic-skills-*` Spec Kit
extensions in this repository from the upstream
[anthropics/skills](https://github.com/anthropics/skills) repo.

Run this whenever upstream changes (new skills, updated `SKILL.md` bodies, changed
bundled resources, or removed skills) to keep this repository in sync. The mapping
is **strictly 1:1** — one `anthropic-skills-<skill>` extension per upstream skill —
which is what makes syncing a mechanical diff.

---

## Copy-paste prompt

> Update the `anthropic-skills-*` extensions in this repository so they match the
> current state of the upstream `anthropics/skills` repo.
>
> 1. Run the generator, letting it clone upstream and prune skills that were removed:
>    ```bash
>    python3 scripts/sync_anthropic_skills.py --repo-root . --prune
>    ```
>    (Add `--ref <tag-or-branch>` to pin a specific upstream revision, or
>    `--source <path>` to use an existing local checkout instead of cloning.)
> 2. Rebuild the catalog entries:
>    ```bash
>    python3 scripts/build_anthropic_catalog.py --repo-root .
>    ```
> 3. Review the diff:
>    - Confirm each new/changed `anthropic-skills-<skill>/` has `extension.yml`,
>      `README.md`, `CHANGELOG.md`, `commands/<skill>.md`, and (when the skill
>      bundles files) a `resources/` tree.
>    - Confirm `catalog.json` lists every generated extension, alphabetically, with
>      descriptions under 200 characters.
>    - Confirm skills marked **Proprietary** upstream (`docx`, `pdf`, `pptx`,
>      `xlsx`, and any newly-proprietary skill) are **excluded** — the generator
>      skips them automatically; there should be no dirs/catalog entries for them.
>    - Confirm each `license` field reflects the upstream skill's terms (NOT MIT).
>    - For extensions whose upstream `SKILL.md` body changed, bump the `version`
>      in `extension.yml` and add a `CHANGELOG.md` entry (the generator writes
>      `1.0.0` on first creation; version bumps are a manual editorial decision).
> 4. Update the extensions table in the root `README.md` if the set of skills
>    changed (added or removed rows).
> 5. Validate a couple of representative extensions:
>    ```
>    /speckit.extensify.validate-extension ./anthropic-skills-pdf
>    /speckit.extensify.validate-extension ./anthropic-skills-canvas-design
>    ```
> 6. Report a summary: which extensions were added, updated, or pruned.

---

## What the generator does (for reference / manual runs)

`scripts/sync_anthropic_skills.py` performs a deterministic 1:1 conversion:

| Upstream skill source | Generated extension destination |
|-----------------------|---------------------------------|
| `skills/<name>/` directory | `anthropic-skills-<name>/` extension |
| `SKILL.md` frontmatter `name` | `extension.id` (`anthropic-skills-<name>`) and command suffix |
| `SKILL.md` frontmatter `description` | `extension.description` — summarized to the first sentence, always `< 200` chars |
| `SKILL.md` markdown body | `commands/<name>.md` body (the procedure) |
| every other file/dir in the skill | `resources/` subtree, copied verbatim |

Conventions applied to every extension:

- `extension.id`: `anthropic-skills-<skill>` (lowercase, hyphens only).
- command name: `speckit.anthropic-skills-<skill>.<skill>`.
- **Proprietary skills are excluded.** Any skill whose upstream `SKILL.md`
  `license` frontmatter contains "Proprietary" (currently `docx`, `pdf`, `pptx`,
  `xlsx`) is skipped by the generator and never written to this repo or catalog.
- `version`: `1.0.0`, `author`: `spec-kit-community`, `license`: `MIT`,
  `speckit_version`: `>=0.2.0`.
- `tags`: `anthropic-skills`, `<skill>`, `skill-conversion`.
- The command body keeps the original skill procedure verbatim. When the skill
  bundles resources, a note maps the skill root to `../resources/`, and relative
  markdown links are rewritten to point into `../resources/`. External URLs and
  `#anchors` are left untouched.

`scripts/build_anthropic_catalog.py` regenerates the `anthropic-skills-*` entries
in `catalog.json` from each extension's `extension.yml`, preserves the other
entries (aide, extensify, presetify, …), keeps the map alphabetically sorted, and
refreshes `updated_at`.

## Why 1:1 instead of grouping

Grouping related skills (e.g. an "office" bundle of docx/pdf/pptx/xlsx) would mean
fewer catalog entries, but it breaks the clean mapping to upstream: an upstream
change to one skill would bump a bundle that also ships unrelated skills, and
adding/removing an upstream skill would require restructuring a bundle. The 1:1
mapping keeps sync a mechanical, low-risk operation — which is the whole point of
this prompt.
