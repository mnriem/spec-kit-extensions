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
| **[mattpocock-engineering](mattpocock-engineering/)** | Matt Pocock's engineering skills — TDD, code review, diagnosing bugs, domain modeling, prototyping, research, and issue/PRD workflows. |
| **[mattpocock-misc](mattpocock-misc/)** | Matt Pocock's occasional-use skills — git guardrails, pre-commit setup, exercise scaffolding, and shoehorn migration. |
| **[mattpocock-personal](mattpocock-personal/)** | Matt Pocock's personal-setup skills — editing articles and managing an Obsidian vault. |
| **[mattpocock-productivity](mattpocock-productivity/)** | Matt Pocock's general workflow skills — grilling plans, conversation handoffs, teaching, and writing great skills. |
| **[presetify](presetify/)** | Create and validate presets and preset catalogs. |

The `mattpocock-*` extensions are converted from
[`mattpocock/skills`](https://github.com/mattpocock/skills) and can be
regenerated with the
[`sync-mattpocock-skills`](prompts/sync-mattpocock-skills.md) prompt to keep
them up to date.

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
