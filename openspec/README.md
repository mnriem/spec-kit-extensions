# OpenSpec

Manage structured change proposals from early exploration through planning,
implementation, verification, specification synchronization, and archival.

The workflow design is based on OpenSpec v1.13.1.

## Installation

```bash
specify extension add openspec
```

## Development Installation

From a Spec Kit project, install the extension directly from this repository:

```bash
specify extension add --dev /path/to/spec-kit-extensions/openspec
specify extension list
```

After changing the manifest, commands, templates, or helper script, refresh the
development installation:

```bash
specify extension add --dev /path/to/spec-kit-extensions/openspec --force
```

No additional CLI or project initialization is required. Commands create and
manage artifacts directly under:

```text
openspec/
├── specs/
└── changes/
    └── archive/
```

The extension includes reusable artifact templates and a native helper script
for deterministic change discovery, status reporting, scaffolding, and
archival.

## Commands

| Command | Purpose |
|---------|---------|
| `/speckit.openspec.explore` | Think through an idea without implementing it |
| `/speckit.openspec.propose` | Create a change and all planning artifacts |
| `/speckit.openspec.apply` | Implement a change's remaining tasks |
| `/speckit.openspec.update` | Revise existing planning artifacts coherently |
| `/speckit.openspec.sync` | Merge delta specs into the main specs |
| `/speckit.openspec.archive` | Synchronize and archive a completed change |
| `/speckit.openspec.new` | Start an empty change scaffold |
| `/speckit.openspec.continue` | Create the next ready artifact |
| `/speckit.openspec.ff` | Create all implementation prerequisites |
| `/speckit.openspec.verify` | Compare implementation with change artifacts |
| `/speckit.openspec.bulk-archive` | Archive several completed changes |
| `/speckit.openspec.onboard` | Walk through a narrated end-to-end workflow |

When the active Spec Kit integration uses skills, each command is also
registered as a skill such as `speckit-openspec-propose`.
