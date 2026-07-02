---
description: "Regenerate the agency-agents-<division> extensions and catalog from the upstream Agency Agents repository."
---

# Sync Agency Agents

Mirror the [Agency Agents](https://github.com/msitarzewski/agency-agents)
collection into this repository as Spec Kit extensions — **one extension per
division (agency)**, each prefixed `agency-agents-` — and refresh
`catalog.json` and the top-level `README.md`.

## User Input

$ARGUMENTS

The user may optionally provide:

- An upstream git ref (branch or tag) to sync from. Defaults to `main`.
- A path to a local `agency-agents` checkout to use instead of cloning.

## Preferred path: run the committed script

This repository ships a deterministic generator. Prefer running it — it is the
source of truth for how the extensions are produced.

```bash
# Sync from upstream main
python3 scripts/sync-agency-agents.py

# Sync from a specific upstream tag/branch
python3 scripts/sync-agency-agents.py --ref <ref>

# Sync from an existing local checkout (no network)
python3 scripts/sync-agency-agents.py --src /path/to/agency-agents
```

The script:

1. Clones (or reads) upstream and loads `divisions.json` (the source of truth
   for the division set).
2. For every division `X`, regenerates `agency-agents-X/` with:
   - `extension.yml` — id `agency-agents-X`, one command per agent.
   - `commands/<slug>.md` — each agent's personality/body, where `<slug>` is the
     agent filename with a leading `X-` stripped.
   - `README.md` and `CHANGELOG.md`.
   Commands are named `speckit.agency-agents-X.<slug>`.
3. Rebuilds `catalog.json`, preserving non-division extensions (`aide`,
   `extensify`, `presetify`, `agency-agents-sync`) and sorting alphabetically.
4. Refreshes the managed Agency Agents table in the top-level `README.md`.

After running, review the diff and commit:

```bash
git add -A && git status
```

## Fallback: do it by hand

If the script cannot be run, reproduce its behavior exactly:

1. **Fetch upstream.** Clone `https://github.com/msitarzewski/agency-agents` at
   the requested ref. Read `divisions.json` → the map of division → `{label}`.
2. **Per division**, collect every `*.md` under that division directory
   (recursively, excluding `README.md`) that has YAML frontmatter with a `name`.
   These are the agents.
3. **Per agent**, create `commands/<slug>.md` where `<slug>` is the filename
   without `.md`, with a leading `<division>-` removed. The file is:

   ```markdown
   ---
   description: "<agent frontmatter description>"
   ---

   > Agency Agents specialist: **<agent name>**. Activate this agent for the task below.

   <agent markdown body, verbatim>
   ```

4. **Write `agency-agents-<division>/extension.yml`** with id
   `agency-agents-<division>`, name `Agency Agents — <label>`, version `1.0.0`,
   author `spec-kit-community`, license MIT, `speckit_version: ">=0.2.0"`, and a
   `provides.commands` entry per agent named
   `speckit.agency-agents-<division>.<slug>`. Tags:
   `agency-agents`, `agents`, `<division>`, `experimental`.
5. **Write `README.md` and `CHANGELOG.md`** for the extension, crediting the
   upstream Agency Agents collection (MIT).
6. **Update `catalog.json`**: add/replace an entry per generated extension,
   preserve `aide`, `extensify`, `presetify`, `agency-agents-sync`, keep keys
   sorted alphabetically, and bump `updated_at`.
7. **Update the top-level `README.md`** managed block delimited by the
   `<!-- BEGIN agency-agents ... -->` / `<!-- END agency-agents ... -->`
   comments with a table of the generated extensions.

## Notes

- Removing an agent upstream removes its command on the next sync (the script
  rebuilds each `commands/` directory from scratch).
- Adding a new division upstream automatically produces a new
  `agency-agents-<division>` extension — no code changes required.
- Bump extension versions in `scripts/sync-agency-agents.py` (`VERSION`) if you
  want the regenerated catalog to advertise a new release.
