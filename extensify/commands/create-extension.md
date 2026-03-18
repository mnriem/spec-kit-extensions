---
description: "Scaffold a new extension from scratch."
---

# Create Extension

Scaffold a new Spec Kit extension with the correct directory structure, manifest, and starter command files.

## Purpose

Instead of copying the extension template and manually editing boilerplate, this command gathers the extension metadata interactively and generates a ready-to-develop extension scaffold.

## User Input

$ARGUMENTS

The user may provide:
- An extension ID (e.g. `my-tool`). If omitted, ask for one.
- An output directory. Defaults to `./<id>` in the current directory.
- Additional metadata (name, description, author). Prompted if not provided.

## Instructions

### 1. Gather Extension Metadata

Collect from the user (use arguments if already provided, otherwise ask):

| Field | Required | Default |
|-------|----------|---------|
| `id` | Yes | — |
| `name` | Yes | Derived from `id` (title-cased, hyphens to spaces) |
| `version` | No | `1.0.0` |
| `description` | Yes | — |
| `author` | Yes | — |
| `repository` | No | empty |
| `license` | No | `MIT` |
| `homepage` | No | same as `repository` |
| `speckit_version` | No | `>=0.2.0` |
| `tags` | No | `[]` |
| `output directory` | No | `./<id>` in the current working directory |

The `id` must be lowercase, alphanumeric, and hyphen-separated only.

### 2. Gather Commands

Ask the user what commands the extension should provide. For each command, collect:

| Field | Required | Default |
|-------|----------|---------|
| Command name suffix | Yes | — |
| Description | Yes | — |

The full command name will be `speckit.<id>.<suffix>`.

If the user doesn't specify any commands, create one example command named `speckit.<id>.example`.

### 3. Create Extension Directory Structure

```
<output-dir>/
├── extension.yml
├── README.md
├── CHANGELOG.md
├── LICENSE
└── commands/
    └── <command-name>.md    # one per command
```

### 4. Generate `extension.yml`

Generate a valid manifest:

```yaml
schema_version: "1.0"

extension:
  id: "my-tool"
  name: "My Tool"
  version: "1.0.0"
  description: "Brief description"
  author: "Author Name"
  repository: "https://github.com/org/spec-kit-my-tool"
  license: "MIT"
  homepage: "https://github.com/org/spec-kit-my-tool"

requires:
  speckit_version: ">=0.2.0"

provides:
  commands:
    - name: speckit.my-tool.example
      file: commands/example.md
      description: "Example command"

tags:
  - "example"
```

### 5. Generate Command Files

For each command, create a starter `.md` file in `commands/` with:

```markdown
---
description: "Command description here"
---

# Command Name

Brief description of what this command does.

## User Input

$ARGUMENTS

## Instructions

1. Step one
2. Step two
3. Step three
```

### 6. Generate `README.md`

Generate a README with:
- Extension name and description
- Installation instructions (`specify extension add <id>`)
- Command table with names and descriptions
- Basic usage examples

### 7. Generate `CHANGELOG.md`

Generate a changelog with an initial `[1.0.0]` entry listing all commands as added.

### 8. Generate `LICENSE`

Generate an MIT license file (or the license specified by the user) with the author name and current year.

### 9. Show Next Steps

Tell the user:

1. Develop the command files in `commands/`.
2. Test locally:
   ```bash
   specify extension add --dev <output-dir>
   specify extension list
   ```
3. Validate before publishing:
   ```
   /speckit.extensify.validate-extension <output-dir>
   ```
4. See the [Extension Publishing Guide](https://github.com/github/spec-kit/blob/main/extensions/EXTENSION-PUBLISHING-GUIDE.md) when ready to share.
