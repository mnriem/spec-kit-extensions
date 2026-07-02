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

### Anthropic Skills

The `anthropic-skills-*` extensions are 1:1 conversions of the skills in the
[anthropics/skills](https://github.com/anthropics/skills) repository — one
extension per upstream skill. Each exposes the skill's procedure as a
`/speckit.anthropic-skills-<skill>.<skill>` command and bundles the skill's
scripts, references, and assets under `resources/`.

Skills whose upstream license is marked **Proprietary** (`docx`, `pdf`, `pptx`,
`xlsx`) are intentionally **excluded**.

| Extension | Description |
|-----------|-------------|
| **[anthropic-skills-algorithmic-art](anthropic-skills-algorithmic-art/)** | Creating algorithmic art using p5.js with seeded randomness and interactive parameter exploration. |
| **[anthropic-skills-brand-guidelines](anthropic-skills-brand-guidelines/)** | Applies Anthropic's official brand colors and typography to artifacts. |
| **[anthropic-skills-canvas-design](anthropic-skills-canvas-design/)** | Design polished visual canvases and layouts. |
| **[anthropic-skills-claude-api](anthropic-skills-claude-api/)** | Reference for the Claude API / Anthropic SDK — models, pricing, params, streaming, tool use, MCP, agents, caching. |
| **[anthropic-skills-doc-coauthoring](anthropic-skills-doc-coauthoring/)** | Collaboratively co-author documents. |
| **[anthropic-skills-frontend-design](anthropic-skills-frontend-design/)** | Frontend design guidance for polished UIs. |
| **[anthropic-skills-internal-comms](anthropic-skills-internal-comms/)** | Draft internal communications. |
| **[anthropic-skills-mcp-builder](anthropic-skills-mcp-builder/)** | Build MCP servers (Node and Python) following best practices. |
| **[anthropic-skills-skill-creator](anthropic-skills-skill-creator/)** | Author new agent skills. |
| **[anthropic-skills-slack-gif-creator](anthropic-skills-slack-gif-creator/)** | Create animated GIFs optimized for Slack. |
| **[anthropic-skills-theme-factory](anthropic-skills-theme-factory/)** | Generate and apply visual themes. |
| **[anthropic-skills-web-artifacts-builder](anthropic-skills-web-artifacts-builder/)** | Build self-contained web artifacts. |
| **[anthropic-skills-webapp-testing](anthropic-skills-webapp-testing/)** | Interact with and test local web apps using Playwright. |

These are generated from upstream and kept up to date with a reusable prompt —
see [prompts/sync-anthropic-skills.md](prompts/sync-anthropic-skills.md). To
refresh them:

```bash
python3 scripts/sync_anthropic_skills.py --repo-root . --prune
python3 scripts/build_anthropic_catalog.py --repo-root .
```

> **Licensing note.** The included skills are **not** MIT-licensed — each bundles
> its own `LICENSE.txt` under `resources/`, and the extension's `license` field
> reflects the upstream terms. Skills marked **Proprietary** upstream (`docx`,
> `pdf`, `pptx`, `xlsx`) are excluded by the generator and are not shipped here.
> Review the upstream [anthropics/skills](https://github.com/anthropics/skills)
> license terms before redistributing.

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
