# Presetify Extension

A Spec Kit extension that converts project-local template and command overrides into a shareable preset.

## Overview

When developing a preset you often start by experimenting with project-local overrides — files in `.specify/templates/overrides/` that sit at the top of the template resolution stack. Once you're happy with the result, Presetify packages those overrides into a proper preset with a `preset.yml` manifest, ready to be shared, version-controlled, and installed in other projects.

## Installation

```bash
specify extension add presetify
```

## Commands

| Command | Purpose |
|---------|---------|
| `/speckit.presetify.create-preset` | Package project-local overrides into a preset |
| `/speckit.presetify.create-catalog` | Create a `catalog.json` for a self-hosted preset catalog |
| `/speckit.presetify.validate-catalog` | Validate a `catalog.json` for schema correctness |
| `/speckit.presetify.validate-preset` | Validate a preset directory before publishing |

## Usage

### 1. Experiment with Overrides

Place your customized templates in `.specify/templates/overrides/`:

```
.specify/
└── templates/
    └── overrides/
        ├── spec-template.md
        └── plan-template.md
```

### 2. Create a Preset

Once the overrides are working as expected:

```
/speckit.presetify.create-preset my-team-preset
```

The command will:
1. Discover all override files
2. Ask for preset metadata (name, description, author, etc.)
3. Generate a preset directory with `preset.yml`, `README.md`, and the template/command files
4. Optionally remove the original overrides to avoid shadowing

### 3. Test the Preset

```bash
specify preset add --dev ./my-team-preset
specify preset resolve spec-template
```

### 4. Share

Version-control the generated preset directory and publish it to the preset catalog if desired.

## Creating a Self-Hosted Catalog

If you maintain multiple presets and want to make them discoverable via `specify preset search`:

```
/speckit.presetify.create-catalog
```

The command will:
1. Ask for the URL where you'll host the catalog
2. Optionally scan preset directories to auto-populate entries from their `preset.yml` manifests
3. Generate a valid `catalog.json`
4. Show how to register the catalog with `specify preset catalog add`

To validate an existing or edited catalog:

```
/speckit.presetify.validate-catalog ./catalog.json
```

Checks JSON syntax, schema conformance, semver format, alphabetical ordering, and required fields.

### Validating a Preset

Before publishing, validate the preset directory:

```
/speckit.presetify.validate-preset ./my-preset
```

Checks `preset.yml` schema, referenced files exist, unreferenced files, ID format, semver, and recommended supporting files.

## What Gets Packaged

| Source | Destination |
|--------|-------------|
| `.specify/templates/overrides/*.md` | `<preset>/templates/` |
| `.specify/commands/overrides/*.md` | `<preset>/commands/` |
