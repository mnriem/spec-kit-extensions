---
description: "Validate an extension directory for correctness."
---

# Validate Extension

Validate an extension directory and its `extension.yml` manifest for schema correctness and completeness.

## Purpose

Before publishing or sharing an extension, this command checks that the directory structure, manifest, and referenced command files are all correct. Catches common mistakes like missing files, invalid IDs, or malformed YAML.

## User Input

$ARGUMENTS

The user should provide:
- A path to the extension directory (the directory containing `extension.yml`). Defaults to the current directory.

## Instructions

### 1. Locate the Manifest

Look for `extension.yml` in the specified directory. If it does not exist, report the error and stop.

### 2. Validate YAML Syntax

Parse `extension.yml`. If it is not valid YAML, report the parse error and stop.

### 3. Validate Top-Level Schema

Check for required top-level fields:

| Field | Type | Required |
|-------|------|----------|
| `schema_version` | string | Yes |
| `extension` | object | Yes |
| `requires` | object | Yes |
| `provides` | object | Yes |

### 4. Validate Extension Metadata

Check `extension` sub-fields:

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `id` | string | Yes | Lowercase, alphanumeric, hyphens only; no leading/trailing hyphens |
| `name` | string | Yes | Non-empty |
| `version` | string | Yes | Semver format (`X.Y.Z`) |
| `description` | string | Yes | Non-empty, under 200 characters |
| `author` | string | Yes | Non-empty |
| `repository` | string | No | URL format if present |
| `license` | string | No | Non-empty if present |
| `homepage` | string | No | URL format if present |

### 5. Validate Requirements

Check `requires` sub-fields:

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `speckit_version` | string | Yes | Valid version specifier (e.g. `>=0.1.0`) |
| `tools` | array | No | Each tool has `name` (string), `version` (string), `required` (boolean) |
| `commands` | array | No | Each entry is a string |

### 6. Validate Commands

`provides.commands` must be present and contain at least one entry. For each command:

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `name` | string | Yes | Must match pattern `speckit.<ext-id>.<command>` |
| `file` | string | Yes | Relative path from extension root |
| `description` | string | No | — |
| `aliases` | array | No | Array of strings |

Validate that:
- The `name` contains the extension `id` as the second segment (e.g. `speckit.my-ext.cmd` for extension `my-ext`)
- The `file` path points to an existing file in the extension directory

### 7. Validate Hooks (if present)

If `hooks` is defined, check each hook entry:

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `command` | string | Yes | Must reference a command declared in `provides.commands` or a core command |
| `optional` | boolean | No | — |
| `prompt` | string | No | Non-empty if present |

### 8. Check for Unreferenced Command Files

Scan the `commands/` directory for `.md` files that are **not** referenced by any entry in `provides.commands`. Report these as warnings — they exist but won't be registered.

### 9. Validate Tags

If `tags` is present:
- Must be an array of strings
- Each tag should be lowercase
- Recommend 2–5 tags

### 10. Check Supporting Files

Report as warnings (not errors) if the following are missing:
- `README.md` — recommended for documentation
- `LICENSE` — recommended for open-source extensions
- `CHANGELOG.md` — recommended for version history

### 11. Report Results

Present a summary:

```
Extension: ./my-extension
ID:        my-extension (v1.0.0)
Commands:  3

✅ YAML syntax: valid
✅ Extension metadata: valid
✅ Requirements: valid
✅ Command name pattern: speckit.my-extension.* (3/3 correct)
✅ commands/analyze.md: exists
✅ commands/report.md: exists
⚠️  commands/draft.md: not referenced in extension.yml
⚠️  CHANGELOG.md: missing (recommended)
❌ commands/export.md: referenced in extension.yml but file not found

Result: 2 warnings, 1 error
```

- If there are **no errors**, confirm the extension is valid and ready to publish.
- If there are **errors**, list each one clearly and suggest fixes.
- If there are only **warnings**, confirm the extension is valid but recommend addressing the warnings.
