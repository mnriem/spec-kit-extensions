---
description: "Create a Spec Kit extension from a skill (SKILL.md and its enclosing directory)."
---

# Create Extension from Skill

Convert an agent skill into a Spec Kit extension, mapping the skill's metadata, instructions, and bundled resources into the extension directory structure.

## Purpose

Skills defined by a `SKILL.md` file (with optional scripts, references, and assets in the same directory) contain valuable procedural knowledge. This command packages that knowledge as a Spec Kit extension so it can be versioned, shared via catalogs, and installed with `specify extension add`.

## User Input

$ARGUMENTS

The user may provide:
- A path to a `SKILL.md` file **or** the directory containing it. If omitted, ask for one.
- An output directory for the generated extension. Defaults to `./<skill-name>` in the current working directory.
- Override values for extension metadata (author, repository, license, tags). Prompted if not provided.

## Instructions

### 1. Locate and Read the Skill

1. If the user provides a directory path, look for `SKILL.md` inside it. If they provide a file path, use it directly.
2. Parse the YAML frontmatter of `SKILL.md` to extract:
   - `name` — becomes the extension `id`
   - `description`
   - `argument-hint` (if present)
   - `user-invocable` (if present)
3. Read the full markdown body of `SKILL.md` (everything after the frontmatter).
4. Inventory every other file and subdirectory in the skill's enclosing directory (e.g. `scripts/`, `references/`, `assets/`, templates, etc.).

### 2. Gather Additional Metadata

Collect from the user (use arguments if already provided, otherwise ask):

| Field | Required | Default |
|-------|----------|---------|
| `author` | Yes | — |
| `version` | No | `1.0.0` |
| `repository` | No | empty |
| `license` | No | `MIT` |
| `homepage` | No | same as `repository` |
| `speckit_version` | No | `>=0.2.0` |
| `tags` | No | derived from skill name |

The extension `id` and `description` come from the skill's frontmatter. The extension `name` is derived from the `id` (title-cased, hyphens to spaces).

### 3. Map Skill Content to Extension Structure

Create the following directory layout:

```
<output-dir>/
├── extension.yml
├── README.md
├── CHANGELOG.md
├── LICENSE
├── commands/
│   └── <skill-name>.md          # main command — the skill's procedure
└── resources/                    # only if the skill has bundled files
    ├── scripts/                  # copied from skill
    ├── references/               # copied from skill
    └── <other-dirs-or-files>/    # any other skill content
```

#### Mapping rules

| Skill source | Extension destination |
|--------------|----------------------|
| `SKILL.md` frontmatter `name` | `extension.id` and command suffix |
| `SKILL.md` frontmatter `description` | `extension.description` and command description |
| `SKILL.md` markdown body | `commands/<skill-name>.md` body (the procedure) |
| `scripts/`, `references/`, `assets/`, other files | `resources/` subtree (preserving directory structure) |

### 4. Generate `extension.yml`

```yaml
schema_version: "1.0"

extension:
  id: "<skill-name>"
  name: "<Skill Name>"
  version: "1.0.0"
  description: "<description from SKILL.md>"
  author: "<author>"
  repository: "<repository>"
  license: "MIT"
  homepage: "<homepage>"

requires:
  speckit_version: ">=0.2.0"

provides:
  commands:
    - name: speckit.<skill-name>.<skill-name>
      file: commands/<skill-name>.md
      description: "<description from SKILL.md>"

tags:
  - "<skill-name>"
  - "skill-conversion"
```

### 5. Generate `commands/<skill-name>.md`

Create the main command file from the skill's body content:

```markdown
---
description: "<description from SKILL.md>"
---

# <Skill Name>

<body content from SKILL.md>
```

When converting the body:
- Rewrite relative file references (e.g. `[script](./scripts/test.js)`) to point into the `resources/` directory (e.g. `[script](../resources/scripts/test.js)`).
- Preserve all headings, procedures, code blocks, and formatting from the original skill.

### 6. Copy Bundled Resources

Copy every file and subdirectory from the skill's enclosing directory (excluding `SKILL.md` itself) into `<output-dir>/resources/`, preserving the original directory structure.

If there are no additional files beyond `SKILL.md`, skip creating the `resources/` directory entirely.

### 7. Generate `README.md`

```markdown
# <Skill Name>

<description from SKILL.md>

> Converted from an agent skill (`SKILL.md`).

## Installation

\```bash
specify extension add <skill-name>
\```

## Commands

| Command | Purpose |
|---------|---------|
| `/speckit.<skill-name>.<skill-name>` | <description> |

## Resources

<list bundled resources if any, otherwise omit this section>
```

### 8. Generate `CHANGELOG.md`

```markdown
# Changelog

## [1.0.0] - <current date>

### Added

- Initial release — converted from agent skill
- `speckit.<skill-name>.<skill-name>` command
```

### 9. Generate `LICENSE`

Generate an MIT license file (or the license specified by the user) with the author name and current year.

### 10. Show Next Steps

Tell the user:

1. Review and refine the generated command in `commands/<skill-name>.md` — the skill body was copied as-is and may need adjustments for the Spec Kit command format.
2. Check that resource references in the command file correctly point to `../resources/`.
3. Test locally:
   ```bash
   specify extension add --dev <output-dir>
   specify extension list
   ```
4. Validate:
   ```
   /speckit.extensify.validate-extension <output-dir>
   ```
5. See the [Extension Publishing Guide](https://github.com/github/spec-kit/blob/main/extensions/EXTENSION-PUBLISHING-GUIDE.md) when ready to share.
