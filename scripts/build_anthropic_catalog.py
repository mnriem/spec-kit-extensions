#!/usr/bin/env python3
"""Rebuild catalog.json entries for the anthropic-skills-* extensions.

Scans the repo root for `anthropic-skills-*/extension.yml` manifests and merges
their entries into catalog.json, preserving any non-anthropic entries (aide,
extensify, presetify, ...) and keeping the `extensions` map alphabetically
sorted. Run after scripts/sync_anthropic_skills.py.

Usage:
    python3 scripts/build_anthropic_catalog.py [--repo-root DIR] [--catalog FILE]
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is required: pip install pyyaml")

PREFIX = "anthropic-skills-"
RELEASE_BASE = "https://github.com/mnriem/spec-kit-extensions/releases/download"
BLOB_BASE = "https://github.com/mnriem/spec-kit-extensions/blob/main"
REPO = "https://github.com/mnriem/spec-kit-extensions"
HOMEPAGE = REPO


def entry_from_manifest(path: str, ext_id: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    ext = data.get("extension", {})
    requires = data.get("requires", {})
    provides = data.get("provides", {})
    version = ext.get("version", "1.0.0")
    commands = provides.get("commands", []) or []
    hooks = provides.get("hooks", []) or []
    return {
        "name": ext.get("name", ext_id),
        "id": ext_id,
        "version": version,
        "description": ext.get("description", ""),
        "author": ext.get("author", "spec-kit-community"),
        "repository": REPO,
        "download_url": f"{RELEASE_BASE}/{ext_id}-v{version}/{ext_id}.zip",
        "homepage": HOMEPAGE,
        "documentation": f"{BLOB_BASE}/{ext_id}/README.md",
        "changelog": f"{BLOB_BASE}/{ext_id}/CHANGELOG.md",
        "license": ext.get("license", "MIT"),
        "requires": {"speckit_version": requires.get("speckit_version", ">=0.2.0")},
        "provides": {"commands": len(commands), "hooks": len(hooks)},
        "tags": data.get("tags", []),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", default=os.getcwd())
    ap.add_argument("--catalog", default=None)
    args = ap.parse_args()

    repo_root = os.path.abspath(args.repo_root)
    catalog_path = args.catalog or os.path.join(repo_root, "catalog.json")

    with open(catalog_path, encoding="utf-8") as fh:
        catalog = json.load(fh)
    extensions = catalog.get("extensions", {})

    # drop existing anthropic entries so removed skills disappear
    extensions = {k: v for k, v in extensions.items() if not k.startswith(PREFIX)}

    added = 0
    for d in sorted(os.listdir(repo_root)):
        if not d.startswith(PREFIX):
            continue
        manifest = os.path.join(repo_root, d, "extension.yml")
        if os.path.isfile(manifest):
            extensions[d] = entry_from_manifest(manifest, d)
            added += 1

    catalog["extensions"] = {k: extensions[k] for k in sorted(extensions)}
    catalog["updated_at"] = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    with open(catalog_path, "w", encoding="utf-8") as fh:
        json.dump(catalog, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    print(f"catalog.json updated: {added} anthropic-skills entries, "
          f"{len(catalog['extensions'])} total")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
