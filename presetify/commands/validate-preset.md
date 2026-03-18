---
description: "Validate a preset directory for correctness before publishing."
---

# Validate Preset

Validate a preset directory and its `preset.yml` manifest for schema correctness and completeness.

## Purpose

Before publishing or sharing a preset, this command checks that the directory structure, manifest, and referenced files are all correct. Catches common mistakes like missing files, invalid IDs, or malformed YAML before they become problems.

## User Input

$ARGUMENTS

The user should provide:
- A path to the preset directory (the directory containing `preset.yml`). Defaults to the current directory.

## Instructions

### 1. Locate the Manifest

Look for `preset.yml` in the specified directory. If it does not exist, report the error and stop.

### 2. Validate YAML Syntax

Parse `preset.yml`. If it is not valid YAML, report the parse error and stop.

### 3. Validate Top-Level Schema

Check for required top-level fields:

| Field | Type | Required |
|-------|------|----------|
| `schema_version` | string | Yes |
| `preset` | object | Yes |
| `requires` | object | Yes |
| `provides` | object | Yes |

### 4. Validate Preset Metadata

Check `preset` sub-fields:

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `id` | string | Yes | Lowercase, alphanumeric, hyphens only; no leading/trailing hyphens |
| `name` | string | Yes | Non-empty |
| `version` | string | Yes | Semver format (`X.Y.Z`) |
| `description` | string | Yes | Non-empty, under 200 characters |
| `author` | string | Yes | Non-empty |
| `repository` | string | No | URL format if present |
| `license` | string | No | Non-empty if present |

### 5. Validate Requirements

Check `requires` sub-fields:

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `speckit_version` | string | Yes | Valid version specifier (e.g. `>=0.1.0`) |

### 6. Validate Provides Entries

For each entry in `provides.templates`:

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `type` | string | Yes | Must be `"template"` or `"command"` |
| `name` | string | Yes | Templates: lowercase with hyphens. Commands: dot notation (e.g. `speckit.specify`) |
| `file` | string | Yes | Relative path from preset root |
| `description` | string | No | — |
| `replaces` | string | No | — |

### 7. Validate Referenced Files Exist

For each entry in `provides.templates`, check that the file referenced in `file` actually exists in the preset directory. Report missing files as errors.

### 8. Check for Unreferenced Files

Scan the `templates/` and `commands/` subdirectories (if they exist) for `.md` files that are **not** referenced by any entry in `provides.templates`. Report these as warnings — they exist but won't be used.

### 9. Validate Tags

If `tags` is present:
- Must be an array of strings
- Each tag should be lowercase
- Recommend 2–5 tags

### 10. Check Supporting Files

Report as warnings (not errors) if the following are missing:
- `README.md` — recommended for documentation
- `LICENSE` — recommended for open-source presets

### 11. Report Results

Present a summary:

```
Preset: ./my-preset
ID:     my-preset (v1.0.0)

✅ YAML syntax: valid
✅ Preset metadata: valid
✅ Requirements: valid
✅ templates/spec-template.md: exists
✅ templates/plan-template.md: exists
✅ commands/speckit.specify.md: exists
⚠️  templates/draft-template.md: not referenced in preset.yml
⚠️  README.md: missing (recommended)
❌ commands/speckit.review.md: referenced in preset.yml but file not found

Result: 2 warnings, 1 error
```

- If there are **no errors**, confirm the preset is valid and ready to publish.
- If there are **errors**, list each one clearly and suggest fixes.
- If there are only **warnings**, confirm the preset is valid but recommend addressing the warnings.
