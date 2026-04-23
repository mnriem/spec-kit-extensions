# Extensify

A Spec Kit extension for creating and validating extensions and extension catalogs.

## Overview

Extensify provides tooling for extension authors — scaffolding new extensions, validating them before publishing, and managing self-hosted extension catalogs.

## Installation

```bash
specify extension add extensify
```

## Commands

| Command | Purpose |
|---------|---------|
| `/speckit.extensify.create-extension` | Scaffold a new extension from scratch |
| `/speckit.extensify.validate-extension` | Validate an extension directory for correctness |
| `/speckit.extensify.create-catalog` | Create a `catalog.json` for a self-hosted extension catalog |
| `/speckit.extensify.validate-catalog` | Validate an extension `catalog.json` for schema correctness |
| `/speckit.extensify.create-extension-from-skill` | Create a Spec Kit extension from a skill (`SKILL.md`) |

## Usage

### Creating a New Extension

```
/speckit.extensify.create-extension my-tool
```

The command will:
1. Ask for extension metadata (name, description, author, etc.)
2. Ask what commands the extension should provide
3. Generate the full extension scaffold with `extension.yml`, command stubs, README, CHANGELOG, and LICENSE

### Validating an Extension

Before publishing, validate the extension directory:

```
/speckit.extensify.validate-extension ./my-tool
```

Checks `extension.yml` schema, command name patterns, referenced files exist, unreferenced files, hooks, and recommended supporting files.

### Creating a Self-Hosted Catalog

If you maintain multiple extensions and want to make them discoverable via `specify extension search`:

```
/speckit.extensify.create-catalog
```

The command will:
1. Ask for the URL where you'll host the catalog
2. Optionally scan extension directories to auto-populate entries from their `extension.yml` manifests
3. Generate a valid `catalog.json`
4. Show how to register the catalog with `specify extension catalog add`

### Validating a Catalog

```
/speckit.extensify.validate-catalog ./catalog.json
```

Checks JSON syntax, schema conformance, semver format, alphabetical ordering, ID consistency, and required fields.

### Creating an Extension from a Skill

Skills (`SKILL.md`) are great for packaging procedural knowledge, but they live inside a single project or user profile. Converting a skill into a Spec Kit extension makes it:

- **Shareable** — publish to a catalog so others can install it with `specify extension add`
- **Versioned** — track changes with semver and a changelog
- **Discoverable** — listed in `specify extension search` across teams and organizations
- **Portable** — works in any project without copying files manually
- **Composable** — presets can customize the extension's templates and commands using composition strategies (replace, prepend, append, wrap)

If you have an existing agent skill (a directory with a `SKILL.md`), convert it into a Spec Kit extension:

```
/speckit.extensify.create-extension-from-skill ./path/to/skill-dir
```

The command will:
1. Read the `SKILL.md` frontmatter and body
2. Ask for additional metadata (author, repository, etc.)
3. Generate a full extension scaffold with the skill's procedure as the main command
4. Copy any bundled resources (scripts, references, assets) into a `resources/` directory
