#!/usr/bin/env python3
"""Generate a single ``gstack`` Spec Kit extension from garrytan/gstack.

gstack is a monolithic skill suite: every skill calls a shared ``bin/``/
``scripts/``/``lib/`` runtime and sibling skills through absolute
``~/.claude/skills/gstack/...`` paths, and its binaries are built by ``bun`` at
setup time. Splitting it into independent extensions therefore breaks those
references.

Instead this builds ONE extension, ``gstack``, that:

* exposes every gstack skill as a ``/speckit.gstack.<slug>`` command (the skill
  body verbatim, so its absolute paths keep working), and
* ships a ``/speckit.gstack.setup`` command that provisions the pinned gstack
  runtime at ``~/.claude/skills/gstack`` (the path the skills expect).

Re-running refreshes the extension and its ``catalog.json`` entry, and pins the
setup command to the exact gstack commit the bodies were generated from.

Usage:
    python3 scripts/sync_gstack_skills.py --gstack /path/to/gstack [--repo .] [--clean]

If ``--gstack`` is omitted the script clones the repo into a temp dir.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

EXT_ID = "gstack"
COMMAND_NS = "speckit.gstack."
OLD_PREFIX = "gstack-"  # first-pass per-skill extension dirs to clean up
REPO_URL = "https://github.com/mnriem/spec-kit-extensions"
RAW_CATALOG = "https://raw.githubusercontent.com/mnriem/spec-kit-extensions/main/catalog.json"
AUTHOR = "spec-kit-community"
LICENSE = "MIT"
SPECKIT_REQ = ">=0.2.0"
UPSTREAM = "https://github.com/garrytan/gstack"

# Integration-agnostic runtime home. gstack bakes the Claude-specific path
# ``~/.claude/skills/gstack`` into its skill bodies, but the runtime itself is
# relocatable (its bin scripts self-locate via ``dirname "$0"`` / honor
# ``GSTACK_DIR``). We install to a neutral home that works under any Spec Kit
# integration (Copilot, Codex, Cursor, Claude, ...) and rewrite the baked path.
INSTALL_PATH = "~/.gstack/runtime"          # display form (tilde)
RUNTIME_HOME = "$HOME/.gstack/runtime"      # shell-expandable form used in bodies
CLAUDE_PATHS = (
    "~/.claude/skills/gstack",
    "${HOME}/.claude/skills/gstack",
    "$HOME/.claude/skills/gstack",
)

EXCLUDE_PARTS = {"test", "node_modules", ".git"}


def rewrite_runtime_paths(body: str) -> str:
    """Rewrite gstack's baked Claude-specific install path to the neutral home.

    The runtime is relocatable, so pointing the skill bodies at ``$HOME/.gstack/
    runtime`` (and exporting ``GSTACK_DIR`` to match in setup) makes every gstack
    skill work regardless of which agent Spec Kit is wired to.
    """
    for pat in CLAUDE_PATHS:
        body = body.replace(pat, RUNTIME_HOME)
    # Project-local relative form ".claude/skills/gstack" not already handled.
    body = re.sub(r"(?<![\w/.])\.claude/skills/gstack", RUNTIME_HOME, body)
    return body


# --------------------------------------------------------------------------- #
# Frontmatter parsing
# --------------------------------------------------------------------------- #
def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw = text[3:end].strip("\n")
    body = text[end + 4:].lstrip("\n")

    data: dict = {}
    key = None
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if re.match(r"^\s*-\s+", line):
            if key is not None:
                data.setdefault(key, [])
                if isinstance(data[key], list):
                    data[key].append(_unquote(line.lstrip()[1:].strip()))
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            data[key] = [] if val == "" else _unquote(val)
    return data, body


def _unquote(v: str) -> str:
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def slug_for(name: str) -> str:
    slug = name.strip()
    if slug.startswith("gstack-"):
        slug = slug[len("gstack-"):]
    return slug


def title_for(slug: str) -> str:
    return " ".join(w.capitalize() for w in re.split(r"[-_]", slug) if w)


def clean_description(desc: str) -> str:
    desc = re.sub(r"\s*\(gstack\)\s*$", "", (desc or "").strip())
    return desc or "A gstack skill."


def discover_skills(gstack: Path) -> list[Path]:
    skills = []
    for skill_md in gstack.rglob("SKILL.md"):
        rel = skill_md.relative_to(gstack)
        if set(rel.parts) & EXCLUDE_PARTS:
            continue
        if rel.parent == Path("."):  # repo-root router skill
            continue
        skills.append(skill_md.parent)
    return sorted(skills)


def git_sha(gstack: Path) -> str:
    try:
        return subprocess.run(
            ["git", "-C", str(gstack), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except Exception:
        return ""


def read_version(gstack: Path) -> str:
    vf = gstack / "VERSION"
    if vf.exists():
        return vf.read_text(encoding="utf-8").strip() or "1.0.0"
    return "1.0.0"


# --------------------------------------------------------------------------- #
# Content generators
# --------------------------------------------------------------------------- #
def mit_license(author: str, year: int) -> str:
    return f"""MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


PREREQ_NOTE = (
    "> **Prerequisite:** run `/speckit.gstack.setup` once. This skill invokes\n"
    f"> shared gstack tooling and sibling skills under `{INSTALL_PATH}/`.\n"
)


def skill_command(slug: str, title: str, description: str, body: str) -> str:
    body = rewrite_runtime_paths(body).rstrip() + "\n"
    return (
        f"---\ndescription: {json.dumps(description)}\n---\n\n"
        f"# {title}\n\n{PREREQ_NOTE}\n{body}"
    )


def setup_command(sha: str, version: str) -> str:
    ref = sha or "main"
    return f'''---
description: "One-time setup: install the pinned gstack runtime so /speckit.gstack.* commands work (integration-agnostic)."
---

# gstack setup

Installs the [gstack]({UPSTREAM}) runtime (shared `bin/`, `scripts/`, `lib/`
and every skill directory) at `{INSTALL_PATH}` — a neutral, **integration-agnostic**
home that works whether Spec Kit is wired to Copilot, Codex, Cursor, Claude, or
anything else. (gstack normally bakes the Claude-specific `~/.claude/skills/gstack`
path into its skills; this extension rewrites those references to
`{INSTALL_PATH}` and exports `GSTACK_DIR` so the relocatable runtime resolves
correctly.)

Run this **once** before using any other `/speckit.gstack.*` command, and again
after updating the extension.

Pinned to gstack `v{version}` (commit `{ref}`).

## Steps

1. Provision the runtime at the neutral home, pinned to the matching commit:

   ```bash
   GSTACK_SHA="{ref}"
   DEST="{RUNTIME_HOME}"
   mkdir -p "$(dirname "$DEST")"
   if [ -d "$DEST/.git" ]; then
     git -C "$DEST" fetch --depth 1 origin "$GSTACK_SHA"
   else
     rm -rf "$DEST"
     git init -q "$DEST"
     git -C "$DEST" remote add origin {UPSTREAM}.git
     git -C "$DEST" fetch --depth 1 origin "$GSTACK_SHA"
   fi
   git -C "$DEST" checkout -q --force FETCH_HEAD
   chmod +x "$DEST"/bin/* 2>/dev/null || true
   ```

2. Export `GSTACK_DIR` and add the runtime to `PATH`, for this and future shells:

   ```bash
   printf 'export GSTACK_DIR="%s"\\n' "{RUNTIME_HOME}" >> "$HOME/.profile"
   printf 'export PATH="%s/bin:$PATH"\\n' "{RUNTIME_HOME}" >> "$HOME/.profile"
   export GSTACK_DIR="{RUNTIME_HOME}"
   export PATH="{RUNTIME_HOME}/bin:$PATH"
   ```

3. **Optional (recommended for browser/design skills):** run gstack's own
   installer, which builds the `browse`/`design` binaries. Requires
   [`bun`](https://bun.sh):

   ```bash
   if command -v bun >/dev/null 2>&1; then
     (cd "{RUNTIME_HOME}" && ./setup)
   else
     echo "bun not installed — core (bash) skills work; browse/design/scrape need bun."
   fi
   ```

4. Verify:

   ```bash
   ls "{RUNTIME_HOME}/bin/gstack-config" && echo "gstack runtime ready"
   ```

If anything fails, confirm `git` (and optionally `bun`) are installed and that
`$HOME/.gstack/` is writable.
'''


def extension_yml(version: str, commands: list[dict]) -> str:
    lines = [
        'schema_version: "1.0"',
        "",
        "extension:",
        f"  id: {EXT_ID}",
        '  name: "gstack"',
        f"  version: {json.dumps(version)}",
        '  description: "The gstack skill suite as Spec Kit commands — install once, then use every gstack skill via /speckit.gstack.*."',
        f"  author: {AUTHOR}",
        f'  repository: "{REPO_URL}"',
        f"  license: {LICENSE}",
        f'  homepage: "{UPSTREAM}"',
        "",
        "requires:",
        f'  speckit_version: "{SPECKIT_REQ}"',
        "",
        "provides:",
        "  commands:",
    ]
    for c in commands:
        lines += [
            f"    - name: {c['name']}",
            f"      file: {c['file']}",
            f"      description: {json.dumps(c['description'])}",
        ]
    lines += ["", "tags:", "  - gstack", "  - skills", "  - workflow", "  - experimental", ""]
    return "\n".join(lines)


def readme(version: str, sha: str, commands: list[dict]) -> str:
    lines = [
        "# gstack",
        "",
        "The [gstack](" + UPSTREAM + ") skill suite, packaged as a single Spec Kit "
        "extension. Every gstack skill is exposed as a `/speckit.gstack.<slug>` command.",
        "",
        f"Pinned to gstack `v{version}`" + (f" (commit `{sha}`)." if sha else "."),
        "",
        "## Why one extension?",
        "",
        "gstack skills are not independent: they share a `bin/`/`scripts/`/`lib/` "
        "runtime and call each other through absolute paths, and the browser/design "
        "tools are compiled by `bun` at setup. Packaging the suite as one extension "
        "keeps those references intact.",
        "",
        "## Integration-agnostic",
        "",
        "Upstream gstack bakes the Claude-specific path `~/.claude/skills/gstack` into "
        "its skills. Because the runtime is relocatable (its `bin/` scripts self-locate "
        "and honor `GSTACK_DIR`), this extension rewrites that path to a neutral home, "
        f"`{INSTALL_PATH}`, and `/speckit.gstack.setup` exports `GSTACK_DIR` to match — "
        "so the commands work under any Spec Kit integration (Copilot, Codex, Cursor, "
        "Claude, …), not just Claude Code.",
        "",
        "## Installation",
        "",
        "```bash",
        f"specify extension add {EXT_ID}",
        "```",
        "",
        "Then run the one-time setup to install the gstack runtime:",
        "",
        "```",
        "/speckit.gstack.setup",
        "```",
        "",
        "## Commands",
        "",
        "| Command | Purpose |",
        "|---------|---------|",
    ]
    for c in commands:
        lines.append(f"| `/{c['name']}` | {c['description']} |")
    lines += [
        "",
        "## Keeping up to date",
        "",
        "Regenerated from upstream by "
        "[`.github/prompts/sync-gstack-skills.prompt.md`](../.github/prompts/sync-gstack-skills.prompt.md) "
        "/ `scripts/sync_gstack_skills.py`. Re-running re-pins the setup command to the "
        "matching gstack commit.",
        "",
    ]
    return "\n".join(lines)


def changelog(version: str, today: str, n_skills: int) -> str:
    return (
        "# Changelog\n\n"
        f"## [{version}] - {today}\n\n"
        "### Added\n\n"
        f"- Packaged the gstack skill suite as a single extension: {n_skills} skill "
        "commands plus `/speckit.gstack.setup`.\n"
    )


# --------------------------------------------------------------------------- #
# Build
# --------------------------------------------------------------------------- #
def build_extension(gstack: Path, repo: Path) -> int:
    today = _dt.date.today().isoformat()
    year = _dt.date.today().year
    sha = git_sha(gstack)
    version = read_version(gstack)

    out = repo / EXT_ID
    if out.exists():
        shutil.rmtree(out)
    (out / "commands").mkdir(parents=True)

    commands: list[dict] = [{
        "name": f"{COMMAND_NS}setup",
        "file": "commands/setup.md",
        "description": "One-time setup: install the pinned gstack runtime so /speckit.gstack.* commands work.",
    }]
    (out / "commands" / "setup.md").write_text(setup_command(sha, version), encoding="utf-8")

    skills = discover_skills(gstack)
    seen: set[str] = {"setup"}
    for skill_dir in skills:
        text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        name = fm.get("name")
        if not isinstance(name, str) or not name:
            name = skill_dir.name
        slug = slug_for(name)
        if slug in seen:
            slug = slug_for(skill_dir.name) or slug
        if slug in seen:
            continue
        seen.add(slug)
        title = title_for(slug)
        description = clean_description(fm.get("description", ""))
        (out / "commands" / f"{slug}.md").write_text(
            skill_command(slug, title, description, body), encoding="utf-8"
        )
        commands.append({
            "name": f"{COMMAND_NS}{slug}",
            "file": f"commands/{slug}.md",
            "description": description,
        })

    n_skills = len(commands) - 1
    (out / "extension.yml").write_text(extension_yml(version, commands), encoding="utf-8")
    (out / "README.md").write_text(readme(version, sha, commands), encoding="utf-8")
    (out / "CHANGELOG.md").write_text(changelog(version, today, n_skills), encoding="utf-8")
    (out / "LICENSE").write_text(mit_license(AUTHOR, year), encoding="utf-8")

    update_catalog(repo, version, len(commands))
    print(f"Built '{EXT_ID}' extension: {n_skills} skills + setup "
          f"({len(commands)} commands), pinned to {sha[:10] or 'main'} (v{version})")
    return n_skills


def update_catalog(repo: Path, version: str, command_count: int) -> None:
    catalog_path = repo / "catalog.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    exts = catalog.setdefault("extensions", {})

    # Drop first-pass per-skill entries and any prior gstack entry.
    for key in list(exts):
        if key == EXT_ID or key.startswith(OLD_PREFIX):
            del exts[key]

    exts[EXT_ID] = {
        "name": "gstack",
        "id": EXT_ID,
        "version": version,
        "description": "The gstack skill suite as Spec Kit commands — install once, then use every gstack skill via /speckit.gstack.*.",
        "author": AUTHOR,
        "repository": REPO_URL,
        "download_url": f"{REPO_URL}/releases/download/{EXT_ID}-v{version}/{EXT_ID}.zip",
        "homepage": UPSTREAM,
        "documentation": f"{REPO_URL}/blob/main/{EXT_ID}/README.md",
        "changelog": f"{REPO_URL}/blob/main/{EXT_ID}/CHANGELOG.md",
        "license": LICENSE,
        "requires": {"speckit_version": SPECKIT_REQ},
        "provides": {"commands": command_count, "hooks": 0},
        "tags": ["gstack", "skills", "workflow", "experimental"],
    }
    catalog["updated_at"] = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT00:00:00Z")
    catalog["catalog_url"] = RAW_CATALOG
    catalog_path.write_text(
        json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def clean_stale(repo: Path) -> list[str]:
    removed = []
    for entry in repo.iterdir():
        if entry.is_dir() and entry.name.startswith(OLD_PREFIX) and entry.name != EXT_ID:
            shutil.rmtree(entry)
            removed.append(entry.name)
    return removed


# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--gstack", help="Path to a gstack checkout. Cloned if omitted.")
    ap.add_argument("--repo", default=".", help="Path to this extensions repo root.")
    ap.add_argument("--clean", action="store_true",
                    help="Remove leftover first-pass gstack-<slug> extension dirs.")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    if not (repo / "catalog.json").exists():
        print(f"error: {repo}/catalog.json not found (wrong --repo?)", file=sys.stderr)
        return 1

    tmp = None
    if args.gstack:
        gstack = Path(args.gstack).resolve()
    else:
        tmp = tempfile.mkdtemp(prefix="gstack-")
        gstack = Path(tmp) / "gstack"
        print(f"Cloning {UPSTREAM} ...")
        subprocess.run(["git", "clone", "--depth", "1", f"{UPSTREAM}.git", str(gstack)],
                       check=True)

    if args.clean:
        for r in clean_stale(repo):
            print(f"  - removed stale {r}")

    build_extension(gstack, repo)

    if tmp:
        shutil.rmtree(tmp, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
