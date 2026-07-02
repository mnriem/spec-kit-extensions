#!/usr/bin/env python3
"""Generate Matt Pocock category extensions from a clone of mattpocock/skills."""
import os, re, shutil, datetime, json

SRC = os.environ.get("MP_SKILLS_SRC", "/tmp/mp-skills/skills")
DEST = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "https://github.com/mnriem/spec-kit-extensions"
AUTHOR = "mattpocock"
UPSTREAM = "https://github.com/mattpocock/skills"
TODAY = datetime.date.today().isoformat()

CATEGORIES = {
    "engineering": {
        "name": "Matt Pocock Engineering",
        "description": "Matt Pocock's engineering skills for daily code work \u2014 TDD, code review, diagnosing bugs, domain modeling, prototyping, research, and issue/PRD workflows.",
        "tags": ["engineering", "workflow", "tdd", "code-review", "skills"],
    },
    "productivity": {
        "name": "Matt Pocock Productivity",
        "description": "Matt Pocock's general workflow skills \u2014 grilling plans, conversation handoffs, teaching, and writing great skills.",
        "tags": ["productivity", "workflow", "planning", "skills"],
    },
    "misc": {
        "name": "Matt Pocock Misc",
        "description": "Matt Pocock's occasional-use skills \u2014 git guardrails, pre-commit setup, exercise scaffolding, and shoehorn migration.",
        "tags": ["misc", "tooling", "setup", "skills"],
    },
    "personal": {
        "name": "Matt Pocock Personal",
        "description": "Matt Pocock's personal-setup skills \u2014 editing articles and managing an Obsidian vault.",
        "tags": ["personal", "writing", "notes", "skills"],
    },
}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.DOTALL)


def parse_frontmatter(text):
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    raw, body = m.group(1), m.group(2)
    meta = {}
    key = None
    for line in raw.splitlines():
        mk = re.match(r"^([a-zA-Z0-9_-]+):\s*(.*)$", line)
        if mk:
            key = mk.group(1)
            val = mk.group(2).strip()
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            meta[key] = val
    return meta, body


def title_case(slug):
    return " ".join(w.capitalize() for w in slug.replace("-", " ").split())


def yq(s):
    """Escape a string for use inside a YAML double-quoted scalar."""
    return s.replace("\\", "\\\\").replace('"', '\\"')


def rewrite_links(body, skill, resource_names):
    """Rewrite relative markdown links pointing at bundled resources into ../resources/<skill>/..."""
    def repl(m):
        text, target = m.group(1), m.group(2)
        t = target.strip()
        if t.startswith(("http://", "https://", "#", "/", "mailto:")):
            return m.group(0)
        clean = t.lstrip("./")
        first = clean.split("/")[0]
        if first in resource_names:
            return f"[{text}](../resources/{skill}/{clean})"
        return m.group(0)
    return re.sub(r"\[([^\]]*)\]\(([^)]+)\)", repl, body)


def main():
    ensure_source()
    summary = {}
    for cat, cfg in CATEGORIES.items():
        cat_src = os.path.join(SRC, cat)
        ext_id = f"{AUTHOR}-{cat}"
        ext_dir = os.path.join(DEST, ext_id)
        cmds_dir = os.path.join(ext_dir, "commands")
        # clean rebuild
        if os.path.isdir(ext_dir):
            shutil.rmtree(ext_dir)
        os.makedirs(cmds_dir, exist_ok=True)

        commands = []
        for skill in sorted(os.listdir(cat_src)):
            sdir = os.path.join(cat_src, skill)
            skill_md = os.path.join(sdir, "SKILL.md")
            if not os.path.isdir(sdir) or not os.path.isfile(skill_md):
                continue
            with open(skill_md, encoding="utf-8") as f:
                meta, body = parse_frontmatter(f.read())
            name = meta.get("name", skill)
            desc = " ".join(meta.get("description", "").split())
            arg_hint = meta.get("argument-hint")

            # bundled resources = everything except SKILL.md
            extras = [e for e in os.listdir(sdir) if e != "SKILL.md"]
            if extras:
                rdir = os.path.join(ext_dir, "resources", skill)
                os.makedirs(rdir, exist_ok=True)
                for e in extras:
                    s = os.path.join(sdir, e)
                    d = os.path.join(rdir, e)
                    if os.path.isdir(s):
                        shutil.copytree(s, d)
                    else:
                        shutil.copy2(s, d)

            new_body = rewrite_links(body.rstrip(), skill, set(extras))
            fm_lines = ["---", f'description: "{yq(desc)}"']
            if arg_hint:
                fm_lines.append(f'argument-hint: "{yq(arg_hint)}"')
            fm_lines.append("---")
            heading = title_case(name)
            body_stripped = new_body.lstrip()
            if body_stripped.startswith("# "):
                content = "\n".join(fm_lines) + f"\n\n{new_body}\n"
            else:
                content = "\n".join(fm_lines) + f"\n\n# {heading}\n\n{new_body}\n"
            with open(os.path.join(cmds_dir, f"{name}.md"), "w", encoding="utf-8") as f:
                f.write(content)
            commands.append({"name": name, "desc": desc, "heading": heading})

        # extension.yml
        yml = ['schema_version: "1.0"', "", "extension:",
               f"  id: {ext_id}",
               f'  name: "{cfg["name"]}"',
               '  version: "1.0.0"',
               f'  description: "{yq(cfg["description"])}"',
               f"  author: {AUTHOR}",
               f'  repository: "{REPO}"',
               "  license: MIT",
               f'  homepage: "{REPO}"', "",
               "requires:", '  speckit_version: ">=0.2.0"', "",
               "provides:", "  commands:"]
        for c in commands:
            yml.append(f"    - name: speckit.{ext_id}.{c['name']}")
            yml.append(f"      file: commands/{c['name']}.md")
            yml.append(f'      description: "{yq(c["desc"])}"')
            yml.append("")
        yml.append("tags:")
        for t in cfg["tags"]:
            yml.append(f"  - {t}")
        with open(os.path.join(ext_dir, "extension.yml"), "w", encoding="utf-8") as f:
            f.write("\n".join(yml) + "\n")

        # README.md
        rd = [f"# {cfg['name']}", "", cfg["description"], "",
              f"> Converted from the [`mattpocock/skills`]({UPSTREAM}) `{cat}` skills. "
              "Each skill is exposed as a Spec Kit command; bundled reference files live in `resources/`.", "",
              "## Installation", "", "```bash", f"specify extension add {ext_id}", "```", "",
              "## Commands", "", "| Command | Purpose |", "|---------|---------|"]
        for c in commands:
            rd.append(f"| `/speckit.{ext_id}.{c['name']}` | {c['desc']} |")
        rd += ["", "## Source", "",
               f"Skills sourced from [{UPSTREAM}]({UPSTREAM}) (`skills/{cat}/`). "
               "Regenerate with the `sync-mattpocock-skills` prompt to keep them up to date.", ""]
        with open(os.path.join(ext_dir, "README.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(rd))

        # CHANGELOG.md
        cl = ["# Changelog", "",
              f"All notable changes to the {cfg['name']} extension will be documented in this file.", "",
              "The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),",
              "and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).", "",
              f"## [1.0.0] - {TODAY}", "", "### Added", "",
              f"- Initial release \u2014 converted from the `mattpocock/skills` `{cat}` skills"]
        for c in commands:
            cl.append(f"- `speckit.{ext_id}.{c['name']}` command")
        with open(os.path.join(ext_dir, "CHANGELOG.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(cl) + "\n")

        summary[ext_id] = {"name": cfg["name"], "description": cfg["description"],
                           "requires": ">=0.2.0", "tags": cfg["tags"],
                           "version": "1.0.0", "commands": len(commands),
                           "cmd_names": [c["name"] for c in commands]}

    update_catalog(summary)
    print(json.dumps(summary, indent=2))


def ensure_source():
    """Clone the upstream skills repo if the source tree is not already present."""
    if os.path.isdir(SRC):
        return
    import subprocess
    root = os.path.dirname(SRC.rstrip("/")) if SRC.endswith("/skills") else "/tmp/mp-skills"
    target = SRC[:-len("/skills")] if SRC.endswith("/skills") else "/tmp/mp-skills"
    subprocess.run(["git", "clone", "--depth", "1",
                    "https://github.com/mattpocock/skills.git", target], check=True)


def update_catalog(summary):
    """Add/update the mattpocock-* entries in catalog.json (sorted, refreshed timestamp)."""
    path = os.path.join(DEST, "catalog.json")
    if not os.path.isfile(path):
        return
    with open(path, encoding="utf-8") as f:
        cat = json.load(f)
    cat["updated_at"] = TODAY + "T00:00:00Z"
    for eid, s in summary.items():
        ver = s["version"]
        cat["extensions"][eid] = {
            "name": s["name"], "id": eid, "version": ver,
            "description": s["description"], "author": AUTHOR, "repository": REPO,
            "download_url": f"{REPO}/releases/download/{eid}-v{ver}/{eid}.zip",
            "homepage": REPO,
            "documentation": f"{REPO}/blob/main/{eid}/README.md",
            "changelog": f"{REPO}/blob/main/{eid}/CHANGELOG.md",
            "license": "MIT",
            "requires": {"speckit_version": s["requires"]},
            "provides": {"commands": s["commands"], "hooks": 0},
            "tags": s["tags"],
        }
    cat["extensions"] = dict(sorted(cat["extensions"].items()))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cat, f, indent=2, ensure_ascii=False)
        f.write("\n")


if __name__ == "__main__":
    main()
