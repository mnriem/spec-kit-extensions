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
