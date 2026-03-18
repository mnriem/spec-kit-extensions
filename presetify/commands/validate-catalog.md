---
description: "Validate a catalog.json file for correctness."
---

# Validate Preset Catalog

Validate a `catalog.json` preset catalog file for schema correctness and completeness.

## Purpose

After creating or manually editing a `catalog.json`, this command checks that the file is well-formed and conforms to the preset catalog schema. Useful before publishing a self-hosted catalog or in CI pipelines that maintain one.

## User Input

$ARGUMENTS

The user should provide:
- A path to the `catalog.json` file to validate. Defaults to `./catalog.json` in the current directory.

## Instructions

### 1. Read the Catalog File

Read the file at the specified path. If the file does not exist, report the error and stop.

### 2. Validate JSON Syntax

Parse the file as JSON. If it is not valid JSON, report the parse error with line/column if possible and stop.

### 3. Validate Top-Level Schema

Check for required top-level fields:

| Field | Type | Required |
|-------|------|----------|
| `schema_version` | string | Yes |
| `updated_at` | string (ISO 8601) | Yes |
| `catalog_url` | string (URL) | Yes |
| `presets` | object | Yes |

Report any missing or incorrectly typed fields.

### 4. Validate Each Preset Entry

For each entry in the `"presets"` object, check:

**Required fields:**

| Field | Type |
|-------|------|
| `name` | string |
| `description` | string |
| `author` | string |
| `version` | string (semver) |
| `download_url` | string (URL) |
| `repository` | string (URL) |
| `license` | string |
| `requires` | object with `speckit_version` string |
| `provides` | object with `templates` (number) and `commands` (number) |
| `tags` | array of strings |
| `created_at` | string (ISO 8601) |
| `updated_at` | string (ISO 8601) |

For each preset entry, report:
- **Errors** — missing required fields, wrong types
- **Warnings** — empty `download_url` (valid but not installable), empty `description`, `tags` array is empty

### 5. Validate Preset ID Format

Each key in the `"presets"` object is a preset ID. Verify each:
- Contains only lowercase letters, numbers, and hyphens
- Does not start or end with a hyphen
- Is not empty

### 6. Validate Alphabetical Ordering

Check that the preset IDs in the `"presets"` object are sorted alphabetically. If not, list which entries are out of order.

### 7. Validate Version Format

For each preset's `version` field, check that it follows semantic versioning (`X.Y.Z` where X, Y, Z are non-negative integers).

### 8. Report Results

Present a summary:

```
Catalog: ./catalog.json
Presets:  3 entries

✅ JSON syntax: valid
✅ Top-level schema: valid
✅ Alphabetical ordering: correct
✅ preset-a: all fields valid
⚠️  preset-b: download_url is empty (preset won't be installable)
❌ preset-c: missing required field "author"
❌ preset-c: version "1.0" is not valid semver (expected X.Y.Z)

Result: 1 warning, 2 errors
```

- If there are **no errors**, confirm the catalog is valid and ready to publish.
- If there are **errors**, list each one clearly and suggest fixes.
- If there are only **warnings**, confirm the catalog is technically valid but recommend addressing the warnings.
