# Sync Matt Pocock Skills → Spec Kit Extensions

A reusable prompt for (re)generating the `mattpocock-*` category extensions in
this repository from the upstream [`mattpocock/skills`](https://github.com/mattpocock/skills)
repository. Run it whenever upstream changes to keep the extensions up to date.

## How to use

Paste the **Task** section below into Copilot CLI (or `/speckit` chat) from the
root of this repository. It is idempotent — it fully rebuilds the four
`mattpocock-*` extension directories each time, so re-running it picks up any
upstream additions, edits, renames, or deletions.

---

## Task

You are updating the `mattpocock-*` Spec Kit extensions in this repository so
they mirror the current state of the upstream skills repo.

### 1. Fetch the source

Clone the latest upstream skills repo to a temporary location and record the
commit SHA so it can be cited in changelogs:

```bash
rm -rf /tmp/mp-skills && git clone --depth 1 https://github.com/mattpocock/skills.git /tmp/mp-skills
git -C /tmp/mp-skills rev-parse HEAD
```

The skills live under `/tmp/mp-skills/skills/<category>/<skill>/SKILL.md`.

### 2. Scope: which skills to include

- **Include** these categories, one extension per category:
  | Category | Extension id | Extension name |
  |----------|--------------|----------------|
  | `engineering` | `mattpocock-engineering` | `Matt Pocock Engineering` |
  | `productivity` | `mattpocock-productivity` | `Matt Pocock Productivity` |
  | `misc` | `mattpocock-misc` | `Matt Pocock Misc` |
  | `personal` | `mattpocock-personal` | `Matt Pocock Personal` |
- **Exclude** the `deprecated/` and `in-progress/` categories entirely.
- A directory counts as a skill only if it contains a `SKILL.md`. Ignore
  category-level `README.md` files.

> **Grouping rationale:** skills are combined by upstream category rather than
> shipped as one extension per skill. This mirrors how upstream organizes and
> ships them, keeps `catalog.json` small, preserves the cross-references
> between skills in the same category, and makes this sync a 4-folder refresh
> instead of ~27.

### 3. For each category, rebuild the extension directory

Delete and recreate `./<extension-id>/` so removed upstream skills disappear.
Produce this layout:

```
<extension-id>/
├── extension.yml
├── README.md
├── CHANGELOG.md
├── commands/
│   └── <skill-name>.md          # one per skill
└── resources/                    # only if any skill has bundled files
    └── <skill-name>/             # everything from the skill dir except SKILL.md
```

For every skill directory:

1. **Parse `SKILL.md` frontmatter** — read `name`, `description`, and
   `argument-hint` (if present).
2. **Command file** → `commands/<name>.md`:
   - Frontmatter: `description: "<description>"`, and `argument-hint: "..."`
     if the skill had one. Escape any embedded `"` as `\"` so the YAML stays
     valid.
   - Body: the full `SKILL.md` markdown body. If the body does **not** already
     start with an `# ` H1 heading, inject `# <Title Cased name>` as the first
     heading; if it already has one, leave it (avoid duplicate H1s).
   - **Rewrite relative resource links.** Any markdown link
     `[text](target)` whose `target` is relative (not `http(s)://`, `#`, `/`,
     or `mailto:`) and whose first path segment names a bundled file/dir in the
     skill must be rewritten to `[text](../resources/<skill-name>/<target>)`.
3. **Copy bundled resources** — copy every file/subdirectory in the skill dir
   *except* `SKILL.md` into `resources/<skill-name>/`, preserving structure.
   If a skill has no extra files, don't create a `resources/` entry for it.

### 4. Generate `extension.yml`

```yaml
schema_version: "1.0"

extension:
  id: <extension-id>
  name: "<Extension Name>"
  version: "1.0.0"          # bump per Semantic Versioning when re-syncing
  description: "<category description — see table below>"
  author: mattpocock
  repository: "https://github.com/mnriem/spec-kit-extensions"
  license: MIT
  homepage: "https://github.com/mnriem/spec-kit-extensions"

requires:
  speckit_version: ">=0.2.0"

provides:
  commands:
    - name: speckit.<extension-id>.<skill-name>
      file: commands/<skill-name>.md
      description: "<skill description>"
    # ...one entry per skill, in alphabetical order by skill name

tags:
  - <category tags>
```

Author is **`mattpocock`** for all four extensions. Category descriptions and
tags:

| Extension | Description | Tags |
|-----------|-------------|------|
| `mattpocock-engineering` | Matt Pocock's engineering skills for daily code work — TDD, code review, diagnosing bugs, domain modeling, prototyping, research, and issue/PRD workflows. | engineering, workflow, tdd, code-review, skills |
| `mattpocock-productivity` | Matt Pocock's general workflow skills — grilling plans, conversation handoffs, teaching, and writing great skills. | productivity, workflow, planning, skills |
| `mattpocock-misc` | Matt Pocock's occasional-use skills — git guardrails, pre-commit setup, exercise scaffolding, and shoehorn migration. | misc, tooling, setup, skills |
| `mattpocock-personal` | Matt Pocock's personal-setup skills — editing articles and managing an Obsidian vault. | personal, writing, notes, skills |

### 5. Generate `README.md` and `CHANGELOG.md`

- `README.md`: title, description, an installation snippet
  (`specify extension add <extension-id>`), a Commands table
  (`/speckit.<extension-id>.<skill-name>` → skill description), and a Source
  note pointing at `mattpocock/skills` (`skills/<category>/`) and this prompt.
- `CHANGELOG.md`: Keep a Changelog / SemVer format. On first creation use
  `1.0.0`; on re-sync add a new dated entry describing added/changed/removed
  commands (cite the upstream commit SHA from step 1).

### 6. Update `catalog.json`

For each extension add/update an entry with `name`, `id`, `version`,
`description`, `author` (`mattpocock`), `repository`,
`download_url` (`.../releases/download/<id>-v<version>/<id>.zip`), `homepage`,
`documentation`, `changelog`, `license`, `requires.speckit_version`,
`provides.commands` (count) + `hooks: 0`, and `tags`. Keep the `extensions`
object sorted alphabetically by key and refresh the top-level `updated_at`.

### 7. Update the root `README.md`

Ensure the Extensions table lists all four `mattpocock-*` extensions (keep the
table alphabetical) with the note that they are converted from
`mattpocock/skills` and regenerated via this prompt.

### 8. Validate

Run the repo's own validators and confirm a clean result:

```
/speckit.extensify.validate-extension ./mattpocock-engineering
/speckit.extensify.validate-extension ./mattpocock-productivity
/speckit.extensify.validate-extension ./mattpocock-misc
/speckit.extensify.validate-extension ./mattpocock-personal
/speckit.extensify.validate-catalog ./catalog.json
```

Also confirm: every `../resources/...` link in a command resolves to a file
that exists, and every `extension.yml` / command frontmatter parses as valid
YAML.

### 9. Report

Summarize what changed since the previous sync: skills added, removed, or
whose descriptions changed, and the upstream commit SHA the extensions now
reflect.

---

## Notes

- The mechanical parts of steps 1–6 are implemented by
  [`scripts/sync-mattpocock-skills.py`](../scripts/sync-mattpocock-skills.py);
  running that script performs the same regeneration deterministically. This
  prompt is the source of truth for the intended behavior.
- Some skills reference sibling skills by their slash-command name (e.g.
  `code-review` mentions `/setup-matt-pocock-skills`). Those are runtime
  references to other commands in the same extension and are intentionally left
  as-is.
