#!/usr/bin/env python3
"""Sync the anthropics/skills repository into `anthropic-skills-*` Spec Kit extensions.

For every skill under `skills/<name>/SKILL.md` in the upstream repo this script
generates (or refreshes) a self-contained Spec Kit extension named
`anthropic-skills-<name>` in this repository, using a strict 1:1 mapping so the
set of extensions can be kept in sync with upstream just by re-running it.

Skills whose upstream `SKILL.md` license frontmatter is marked "Proprietary"
(currently docx, pdf, pptx, xlsx) are skipped and never generated.

Each generated extension contains:
  extension.yml           - manifest (id, single command, tags)
  README.md               - short docs
  CHANGELOG.md            - initial changelog
  commands/<name>.md      - the skill's SKILL.md body (the procedure)
  resources/...           - every other file from the skill dir (scripts, refs, assets)

Usage:
    python3 scripts/sync_anthropic_skills.py [--source DIR] [--repo-root DIR]
                                             [--ref GITREF] [--prune] [--dry-run]

If --source is omitted the upstream repo is shallow-cloned into a temp dir.
Run scripts/build_anthropic_catalog.py afterwards (or the sync prompt) to refresh
catalog.json.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is required: pip install pyyaml")

PREFIX = "anthropic-skills-"
UPSTREAM = "https://github.com/anthropics/skills.git"
UPSTREAM_HTML = "https://github.com/anthropics/skills"
AUTHOR = "spec-kit-community"
REPOSITORY = "https://github.com/mnriem/spec-kit-extensions"
SPECKIT_VERSION = ">=0.2.0"
VERSION = "1.0.0"
MAX_DESC = 199  # extension.yml description must be < 200 chars

# Words to force-uppercase when building a human-readable name.
ACRONYMS = {"pdf", "docx", "pptx", "xlsx", "api", "mcp", "gif", "ui", "ux"}


def log(msg: str) -> None:
    print(msg, flush=True)


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split a SKILL.md into (frontmatter dict, body markdown)."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("\n")
    end = None
    for i in range(1, len(parts)):
        if parts[i].strip() == "---":
            end = i
            break
    if end is None:
        return {}, text
    fm_text = "\n".join(parts[1:end])
    body = "\n".join(parts[end + 1:]).lstrip("\n")
    data = yaml.safe_load(fm_text) or {}
    if not isinstance(data, dict):
        data = {}
    return data, body


def normalize_license(raw: str, has_license_file: bool) -> str:
    """Reflect the upstream skill's license instead of assuming MIT.

    Upstream skills are not MIT: some declare "Proprietary" and the rest ship a
    LICENSE.txt. We surface an accurate, honest value and point at the bundled
    file / upstream repo rather than mislabeling third-party content.
    """
    raw = re.sub(r"\s+", " ", (raw or "").strip())
    low = raw.lower()
    if "proprietary" in low:
        loc = "resources/LICENSE.txt" if has_license_file else UPSTREAM_HTML
        return f"Proprietary (Anthropic) — see {loc}"
    if has_license_file:
        return "See resources/LICENSE.txt (from anthropics/skills)"
    if raw:
        return raw
    return f"See {UPSTREAM_HTML}"


def human_name(skill: str) -> str:
    words = []
    for w in skill.split("-"):
        words.append(w.upper() if w.lower() in ACRONYMS else w.capitalize())
    return " ".join(words)


def short_description(desc: str) -> str:
    """Collapse whitespace and return a first-sentence summary under MAX_DESC chars."""
    desc = re.sub(r"\s+", " ", (desc or "").strip())
    if not desc:
        return ""
    m = re.search(r"[.!?]\s", desc)
    if m and (m.start() + 1) <= MAX_DESC:
        candidate = desc[: m.start() + 1].strip()
    else:
        candidate = desc
    if len(candidate) > MAX_DESC:
        candidate = candidate[: MAX_DESC - 1].rstrip() + "\u2026"
    return candidate


LINK_RE = re.compile(r"(\]\()([^)]+)(\))")


def rewrite_links(body: str) -> str:
    """Rewrite relative markdown link targets to point into ../resources/."""
    def repl(m: re.Match) -> str:
        target = m.group(2).strip()
        low = target.lower()
        if (
            low.startswith(("http://", "https://", "mailto:", "#", "/"))
            or target.startswith("../resources/")
        ):
            return m.group(0)
        anchor = ""
        if "#" in target:
            target, anchor = target.split("#", 1)
            anchor = "#" + anchor
        if not target:
            return m.group(0)
        target = target[2:] if target.startswith("./") else target
        return f"{m.group(1)}../resources/{target}{anchor}{m.group(3)}"

    return LINK_RE.sub(repl, body)


def render_extension_yml(ext_id: str, name: str, desc: str, skill: str,
                         tags: list[str], license_str: str) -> str:
    lines = [
        'schema_version: "1.0"',
        "",
        "extension:",
        f"  id: {ext_id}",
        f'  name: "{name}"',
        f'  version: "{VERSION}"',
        f"  description: {json.dumps(desc)}",
        f"  author: {AUTHOR}",
        f'  repository: "{REPOSITORY}"',
        f"  license: {json.dumps(license_str)}",
        f'  homepage: "{REPOSITORY}"',
        "",
        "requires:",
        f'  speckit_version: "{SPECKIT_VERSION}"',
        "",
        "provides:",
        "  commands:",
        f"    - name: speckit.{ext_id}.{skill}",
        f"      file: commands/{skill}.md",
        f"      description: {json.dumps(desc)}",
        "",
        "tags:",
    ]
    for t in tags:
        lines.append(f"  - {t}")
    return "\n".join(lines) + "\n"


def render_command(name: str, desc: str, body: str, has_resources: bool) -> str:
    note = ""
    if has_resources:
        note = (
            "> **Bundled resources.** This skill ships supporting files (scripts, "
            "references, assets) in this extension's `resources/` directory. Any "
            "relative path referenced below is rooted there — from this command "
            "file the resources live at `../resources/`.\n\n"
        )
        body = rewrite_links(body)
    return (
        "---\n"
        f"description: {json.dumps(desc)}\n"
        "---\n\n"
        f"# {name}\n\n"
        f"{note}"
        f"{body.rstrip()}\n"
    )


def render_readme(ext_id: str, name: str, skill: str, desc: str,
                  resources: list[str]) -> str:
    out = [
        f"# {name}",
        "",
        desc,
        "",
        f"> Converted from the [`{skill}`]({UPSTREAM_HTML}/tree/main/skills/{skill}) "
        "agent skill (`SKILL.md`) in the [anthropics/skills]"
        f"({UPSTREAM_HTML}) repository.",
        "",
        "## Installation",
        "",
        "```bash",
        f"specify extension add {ext_id}",
        "```",
        "",
        "## Commands",
        "",
        "| Command | Purpose |",
        "|---------|---------|",
        f"| `/speckit.{ext_id}.{skill}` | {desc} |",
        "",
    ]
    if resources:
        out += ["## Resources", "",
                "Bundled under `resources/` (copied verbatim from the upstream skill):",
                ""]
        for r in resources:
            out.append(f"- `{r}`")
        out.append("")
    return "\n".join(out)


def render_changelog(ext_id: str, skill: str, date: str) -> str:
    return (
        "# Changelog\n\n"
        f"All notable changes to the {ext_id} extension will be documented in this file.\n\n"
        "The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),\n"
        "and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).\n\n"
        f"## [{VERSION}] - {date}\n\n"
        "### Added\n\n"
        f"- Initial release \u2014 converted from the upstream `{skill}` agent skill\n"
        f"- `speckit.{ext_id}.{skill}` command\n"
    )


def build_tags(skill: str) -> list[str]:
    tags = ["anthropic-skills", "skill-conversion"]
    if skill not in tags:
        tags.insert(1, skill)
    return tags[:5]


def generate(skill_dir: str, repo_root: str, date: str, dry_run: bool) -> str | None:
    skill = os.path.basename(skill_dir.rstrip("/"))
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return None
    with open(skill_md, encoding="utf-8") as fh:
        fm, body = parse_frontmatter(fh.read())
    if "proprietary" in re.sub(r"\s+", " ", str(fm.get("license", ""))).lower():
        log(f"  skipping {PREFIX}{fm.get('name', skill)} (upstream license is proprietary)")
        return None
    name_field = fm.get("name", skill)
    desc = short_description(fm.get("description", ""))
    ext_id = PREFIX + name_field
    display = f"Anthropic Skills: {human_name(name_field)}"

    extras = []
    for root, _dirs, files in os.walk(skill_dir):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), skill_dir)
            if rel == "SKILL.md":
                continue
            extras.append(rel)
    extras.sort()
    has_resources = bool(extras)
    has_license_file = any(os.path.basename(r).lower().startswith("license") for r in extras)
    license_str = normalize_license(fm.get("license", ""), has_license_file)

    out_dir = os.path.join(repo_root, ext_id)
    if dry_run:
        log(f"  would write {ext_id}  (command + {len(extras)} resource files)")
        return ext_id

    if os.path.isdir(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(os.path.join(out_dir, "commands"), exist_ok=True)

    with open(os.path.join(out_dir, "extension.yml"), "w", encoding="utf-8") as fh:
        fh.write(render_extension_yml(ext_id, display, desc, name_field, build_tags(name_field), license_str))
    with open(os.path.join(out_dir, "commands", f"{name_field}.md"), "w", encoding="utf-8") as fh:
        fh.write(render_command(display, desc, body, has_resources))
    with open(os.path.join(out_dir, "README.md"), "w", encoding="utf-8") as fh:
        fh.write(render_readme(ext_id, display, name_field, desc, extras))
    with open(os.path.join(out_dir, "CHANGELOG.md"), "w", encoding="utf-8") as fh:
        fh.write(render_changelog(ext_id, name_field, date))

    for rel in extras:
        src = os.path.join(skill_dir, rel)
        dst = os.path.join(out_dir, "resources", rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)

    log(f"  wrote {ext_id}  (1 command, {len(extras)} resource files)")
    return ext_id


def clone_upstream(ref: str | None) -> str:
    tmp = tempfile.mkdtemp(prefix="anthropic-skills-")
    cmd = ["git", "clone", "--depth", "1"]
    if ref:
        cmd += ["--branch", ref]
    cmd += [UPSTREAM, tmp]
    log(f"Cloning {UPSTREAM} -> {tmp}")
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return tmp


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source", help="path to a checkout of anthropics/skills")
    ap.add_argument("--repo-root", default=os.getcwd(), help="target repo root (default: cwd)")
    ap.add_argument("--ref", help="git ref/branch to clone when --source is not given")
    ap.add_argument("--prune", action="store_true",
                    help="remove anthropic-skills-* dirs that no longer exist upstream")
    ap.add_argument("--dry-run", action="store_true", help="report actions without writing")
    args = ap.parse_args()

    cleanup = None
    source = args.source
    if not source:
        source = clone_upstream(args.ref)
        cleanup = source

    skills_root = os.path.join(source, "skills")
    if not os.path.isdir(skills_root):
        sys.exit(f"no skills/ directory in {source}")

    date = _dt.date.today().isoformat()
    repo_root = os.path.abspath(args.repo_root)
    generated: list[str] = []
    log(f"Generating extensions into {repo_root}")
    for skill in sorted(os.listdir(skills_root)):
        sd = os.path.join(skills_root, skill)
        if os.path.isdir(sd):
            ext = generate(sd, repo_root, date, args.dry_run)
            if ext:
                generated.append(ext)

    if args.prune:
        existing = {d for d in os.listdir(repo_root)
                    if d.startswith(PREFIX) and os.path.isdir(os.path.join(repo_root, d))}
        stale = sorted(existing - set(generated))
        for d in stale:
            log(f"  pruning stale {d}")
            if not args.dry_run:
                shutil.rmtree(os.path.join(repo_root, d))

    if cleanup:
        shutil.rmtree(cleanup, ignore_errors=True)

    log(f"\nDone. {len(generated)} extensions:")
    for e in generated:
        log(f"  - {e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
