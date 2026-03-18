---
description: "Create a catalog.json for a self-hosted preset catalog."
---

# Create Preset Catalog

Generate a valid `catalog.json` file for hosting your own preset catalog.

## Purpose

Organizations and teams often want to maintain a private or internal catalog of presets. This command creates a correctly structured `catalog.json` that can be hosted on a web server, GitHub repository, or any URL-accessible location and registered with `specify preset catalog add`.

## User Input

$ARGUMENTS

The user may provide:
- A URL where the catalog will be hosted (e.g. `https://raw.githubusercontent.com/my-org/presets/main/catalog.json`). If omitted, ask for one or use a placeholder.
- An output path for the file. Defaults to `./catalog.json` in the current directory.
- One or more preset directories to include in the catalog. If omitted, the catalog starts empty.

## Instructions

### 1. Gather Catalog Metadata

Collect from the user (use arguments if already provided, otherwise ask):

| Field | Required | Default |
|-------|----------|---------|
| `catalog_url` | Yes | — |
| Output file path | No | `./catalog.json` |

### 2. Discover Presets to Include

If the user points to one or more directories containing `preset.yml` files, read each manifest and extract the catalog entry fields. Supported inputs:

- A single directory path containing a `preset.yml`
- Multiple directory paths
- A parent directory where each subdirectory contains a `preset.yml`
- No directories — create an empty catalog the user can populate later

For each discovered `preset.yml`, extract:

| Catalog field | Source |
|---------------|--------|
| `name` | `preset.name` |
| `description` | `preset.description` |
| `author` | `preset.author` |
| `version` | `preset.version` |
| `repository` | `preset.repository` |
| `license` | `preset.license` |
| `requires.speckit_version` | `requires.speckit_version` |
| `tags` | `tags` |
| `provides.templates` | Count of entries with `type: "template"` |
| `provides.commands` | Count of entries with `type: "command"` |

The `download_url` must be provided by the user or prompted per preset. This is typically a URL to a `.zip` archive of the preset (e.g. a GitHub release archive).

Set `created_at` and `updated_at` to the current UTC timestamp in ISO 8601 format.

### 3. Generate `catalog.json`

Generate the file with this exact schema:

```json
{
  "schema_version": "1.0",
  "updated_at": "2026-03-18T00:00:00Z",
  "catalog_url": "https://example.com/catalog.json",
  "presets": {
    "preset-id": {
      "name": "Preset Name",
      "description": "Brief description",
      "author": "Author Name",
      "version": "1.0.0",
      "download_url": "https://example.com/preset-id/v1.0.0.zip",
      "repository": "https://github.com/org/preset-repo",
      "license": "MIT",
      "requires": {
        "speckit_version": ">=0.2.0"
      },
      "provides": {
        "templates": 2,
        "commands": 1
      },
      "tags": ["custom", "workflow"],
      "created_at": "2026-03-18T00:00:00Z",
      "updated_at": "2026-03-18T00:00:00Z"
    }
  }
}
```

Entries in the `"presets"` object **must be sorted alphabetically by preset ID**.

### 4. Validate

After generating:
- Verify the JSON is valid.
- Confirm all required fields are present for each preset entry.
- Warn if any preset is missing a `download_url` (the catalog will be valid but the preset won't be installable).

### 5. Show Next Steps

Tell the user:

1. Host the `catalog.json` at the URL specified in `catalog_url`.
2. Register the catalog in any project:
   ```bash
   specify preset catalog add <catalog_url> --name my-org --install-allowed
   ```
3. Or set it globally:
   ```bash
   # In ~/.specify/preset-catalogs.yml
   ```
4. Verify it works:
   ```bash
   specify preset search
   ```
5. To add more presets later, run this command again pointing to additional preset directories, or manually add entries to the `"presets"` object (keeping alphabetical order).
