---
description: "Create a catalog.json for a self-hosted extension catalog."
---

# Create Extension Catalog

Generate a valid `catalog.json` file for hosting your own extension catalog.

## Purpose

Organizations and teams may want to maintain a private or internal catalog of extensions. This command creates a correctly structured `catalog.json` that can be hosted on a web server, GitHub repository, or any URL-accessible location and registered with `specify extension catalog add`.

## User Input

$ARGUMENTS

The user may provide:
- A URL where the catalog will be hosted (e.g. `https://raw.githubusercontent.com/my-org/extensions/main/catalog.json`). If omitted, ask for one or use a placeholder.
- An output path for the file. Defaults to `./catalog.json` in the current directory.
- One or more extension directories to include in the catalog. If omitted, the catalog starts empty.

## Instructions

### 1. Gather Catalog Metadata

Collect from the user (use arguments if already provided, otherwise ask):

| Field | Required | Default |
|-------|----------|---------|
| `catalog_url` | Yes | — |
| Output file path | No | `./catalog.json` |

### 2. Discover Extensions to Include

If the user points to one or more directories containing `extension.yml` files, read each manifest and extract the catalog entry fields. Supported inputs:

- A single directory path containing an `extension.yml`
- Multiple directory paths
- A parent directory where each subdirectory contains an `extension.yml`
- No directories — create an empty catalog the user can populate later

For each discovered `extension.yml`, extract:

| Catalog field | Source |
|---------------|--------|
| `name` | `extension.name` |
| `id` | `extension.id` |
| `description` | `extension.description` |
| `author` | `extension.author` |
| `version` | `extension.version` |
| `repository` | `extension.repository` |
| `homepage` | `extension.homepage` |
| `license` | `extension.license` |
| `requires.speckit_version` | `requires.speckit_version` |
| `requires.tools` | `requires.tools` (if present) |
| `tags` | `tags` |
| `provides.commands` | Count of entries in `provides.commands` |
| `provides.hooks` | Count of entries in `hooks` (0 if absent) |

The following fields must be provided by the user or prompted per extension:

| Field | Description |
|-------|-------------|
| `download_url` | URL to a `.zip` archive of the extension (e.g. a GitHub release archive) |
| `documentation` | URL to documentation (optional, defaults to empty) |
| `changelog` | URL to changelog (optional, defaults to empty) |

Set `verified` to `false`, `downloads` and `stars` to `0`, and `created_at`/`updated_at` to the current UTC timestamp in ISO 8601 format.

### 3. Generate `catalog.json`

Generate the file with this exact schema:

```json
{
  "schema_version": "1.0",
  "updated_at": "2026-03-18T00:00:00Z",
  "catalog_url": "https://example.com/catalog.json",
  "extensions": {
    "my-extension": {
      "name": "My Extension",
      "id": "my-extension",
      "description": "Brief description",
      "author": "Author Name",
      "version": "1.0.0",
      "download_url": "https://example.com/my-extension/v1.0.0.zip",
      "repository": "https://github.com/org/spec-kit-my-extension",
      "homepage": "https://github.com/org/spec-kit-my-extension",
      "documentation": "",
      "changelog": "",
      "license": "MIT",
      "requires": {
        "speckit_version": ">=0.2.0"
      },
      "provides": {
        "commands": 2,
        "hooks": 0
      },
      "tags": ["example"],
      "verified": false,
      "downloads": 0,
      "stars": 0,
      "created_at": "2026-03-18T00:00:00Z",
      "updated_at": "2026-03-18T00:00:00Z"
    }
  }
}
```

Entries in the `"extensions"` object **must be sorted alphabetically by extension ID**.

### 4. Validate

After generating:
- Verify the JSON is valid.
- Confirm all required fields are present for each extension entry.
- Warn if any extension is missing a `download_url` (the catalog will be valid but the extension won't be installable).

### 5. Show Next Steps

Tell the user:

1. Host the `catalog.json` at the URL specified in `catalog_url`.
2. Register the catalog in any project:
   ```bash
   specify extension catalog add <catalog_url> --name my-org --install-allowed
   ```
3. Verify it works:
   ```bash
   specify extension search
   ```
4. To add more extensions later, run this command again pointing to additional extension directories, or manually add entries to the `"extensions"` object (keeping alphabetical order).
