# spec-kit-extensions

> **⚠️ Experimental** — This is the `mnriem` persona Spec Kit extensions
> repository. The extensions here are experimental and may change or break
> without notice.

This repository contains experimental
[Spec Kit](https://github.com/mnriem/spec-kit) extensions developed by
`mnriem`. These are personal experiments and are not official or
community-contributed extensions.

## Extensions

| Extension | Description |
|-----------|-------------|
| **[aide](aide/)** | AI-Driven Engineering — a structured 7-step workflow for building new projects from scratch with AI assistants. |
| **[extensify](extensify/)** | Create and validate extensions and extension catalogs. |
| **[presetify](presetify/)** | Create and validate presets and preset catalogs. |
| **[gstack](gstack/)** | The [garrytan/gstack](https://github.com/garrytan/gstack) skill suite (~58 skills) as `/speckit.gstack.*` commands, with a one-time `setup` command for the shared runtime. |

### gstack

[`gstack/`](gstack/) packages the entire [garrytan/gstack](https://github.com/garrytan/gstack)
skill suite as a **single** extension. Each skill becomes a
`/speckit.gstack.<slug>` command; a `/speckit.gstack.setup` command installs the
shared gstack runtime once.

It's packaged as one extension (rather than one per skill) because gstack skills
share a `bin/`/`scripts/`/`lib/` runtime and call each other — so they can't run
in isolation. The runtime installs to the neutral, **integration-agnostic** home
`~/.gstack/runtime` (not Claude-specific `~/.claude/...`), so it works under any
Spec Kit integration.

This extension is **generated, not hand-authored**. To (re)generate it and keep
it in sync with upstream, run the reusable prompt
[`.github/prompts/sync-gstack-skills.prompt.md`](.github/prompts/sync-gstack-skills.prompt.md)
or its generator directly:

```bash
python3 scripts/sync_gstack_skills.py --clean
```

## Forking

If you like a specific extension or all the extensions in this repository, it
is recommended to **fork** this repository. This gives you a stable copy that
won't be affected by experimental changes made here.

## Usage

Add this catalog URL to your Spec Kit configuration:

```
https://raw.githubusercontent.com/mnriem/spec-kit-extensions/main/catalog.json
```

Then install an extension with the Spec Kit CLI:

```
specify extension install <extension-id>
```

You can also browse individual extensions by navigating to their directory
(e.g., [aide/](aide/)) and reading the README for more details.

## More Information

See the [Spec Kit README](https://github.com/github/spec-kit/blob/main/README.md)
for more information about Spec Kit and its extension system.

## License

MIT
