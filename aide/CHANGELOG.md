# Changelog

All notable changes to the AIDE extension will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-17

### Added

- Initial release of the AI-Driven Engineering (AIDE) extension
- 7-step workflow for building new projects from scratch:
  - `speckit.aide.create-vision` — Create comprehensive vision document
  - `speckit.aide.create-roadmap` — Generate staged development roadmap
  - `speckit.aide.create-progress` — Create progress tracking file
  - `speckit.aide.create-queue` — Generate prioritized work item queue
  - `speckit.aide.create-item` — Create detailed work item specification
  - `speckit.aide.execute-item` — Implement work item and update progress
  - `speckit.aide.feedback-loop` — Analyze issues and improve the process
- Work item template with mandatory testing prerequisites and validation checklists
- Sequential queue numbering across batches
- Progress tracking with status icons (📋 🚧 ✅ ⏸️ ❌)
- Decision logging in work items during implementation
