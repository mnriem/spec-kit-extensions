# Changelog

All notable changes to the Presetify extension will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-18

### Added

- Initial release of the Presetify extension
- `speckit.presetify.create-preset` command to package project-local overrides into a preset
- `speckit.presetify.create-catalog` command to generate a `catalog.json` for self-hosted preset catalogs
- `speckit.presetify.validate-catalog` command to validate a `catalog.json` for schema correctness
- `speckit.presetify.validate-preset` command to validate a preset directory before publishing
- Discovers template overrides from `.specify/templates/overrides/`
- Discovers command overrides from `.specify/commands/overrides/`
- Generates `preset.yml` manifest and `README.md`
- Optional cleanup of original override files after packaging
