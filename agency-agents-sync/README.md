# Agency Agents — Sync

Mirror the [Agency Agents](https://github.com/msitarzewski/agency-agents)
collection into this repository as Spec Kit extensions — one extension per
division (agency), prefixed `agency-agents-` — and keep them up to date.

## Installation

```bash
specify extension add agency-agents-sync
```

## Commands

| Command | Purpose |
|---------|---------|
| `/speckit.agency-agents-sync.sync` | Regenerate the `agency-agents-<division>` extensions, `catalog.json`, and README from upstream |

## Usage

```
/speckit.agency-agents-sync.sync
```

The command drives the committed generator `scripts/sync-agency-agents.py`,
which clones the upstream repository, regenerates one extension per division,
and refreshes `catalog.json` and the top-level `README.md`. See the command for
the full workflow and a manual fallback.

## How it works

- Source of truth for the division set is upstream `divisions.json`.
- Each agent personality file becomes a command
  `speckit.agency-agents-<division>.<slug>`.
- Non-division extensions (`aide`, `extensify`, `presetify`, `agency-agents-sync`)
  are preserved across syncs.
