---
description: "Validate an extension catalog.json file for correctness."
---

# Validate Extension Catalog

Validate an extension `catalog.json` file for schema correctness and completeness.

## Purpose

After creating or manually editing an extension `catalog.json`, this command checks that the file is well-formed and conforms to the extension catalog schema. Useful before publishing a self-hosted catalog or in CI pipelines.

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
| `extensions` | object | Yes |

Report any missing or incorrectly typed fields.

### 4. Validate Each Extension Entry

For each entry in the `"extensions"` object, check:

**Required fields:**

| Field | Type |
|-------|------|
| `name` | string |
| `id` | string |
| `description` | string |
| `author` | string |
| `version` | string (semver) |
| `download_url` | string (URL) |
| `repository` | string (URL) |
| `license` | string |
| `requires` | object with `speckit_version` string |
| `provides` | object with `commands` (number) and `hooks` (number) |
| `tags` | array of strings |
| `created_at` | string (ISO 8601) |
| `updated_at` | string (ISO 8601) |

**Optional fields:**

| Field | Type |
|-------|------|
| `homepage` | string (URL) |
| `documentation` | string (URL) |
| `changelog` | string (URL) |
| `verified` | boolean |
| `downloads` | number |
| `stars` | number |

For each extension entry, report:
- **Errors** — missing required fields, wrong types, `id` in the entry doesn't match the object key
- **Warnings** — empty `download_url` (valid but not installable), empty `description`, `tags` array is empty

### 5. Validate Extension ID Format

Each key in the `"extensions"` object is an extension ID. Verify each:
- Contains only lowercase letters, numbers, and hyphens
- Does not start or end with a hyphen
- Is not empty
- Matches the `id` field inside the entry

### 6. Validate Alphabetical Ordering

Check that the extension IDs in the `"extensions"` object are sorted alphabetically. If not, list which entries are out of order.

### 7. Validate Version Format

For each extension's `version` field, check that it follows semantic versioning (`X.Y.Z` where X, Y, Z are non-negative integers).

### 8. Report Results

Present a summary:

```
Catalog: ./catalog.json
Extensions: 5 entries

✅ JSON syntax: valid
✅ Top-level schema: valid
✅ Alphabetical ordering: correct
✅ my-extension: all fields valid
✅ another-ext: all fields valid
⚠️  draft-ext: download_url is empty (extension won't be installable)
❌ broken-ext: missing required field "author"
❌ broken-ext: id "broken_ext" doesn't match key "broken-ext"

Result: 1 warning, 2 errors
```

- If there are **no errors**, confirm the catalog is valid and ready to publish.
- If there are **errors**, list each one clearly and suggest fixes.
- If there are only **warnings**, confirm the catalog is technically valid but recommend addressing the warnings.
