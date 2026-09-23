#!/usr/bin/env python3
"""Manage file-based change proposal state for the extension."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path


NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TASK_PATTERN = re.compile(r"^\s*-\s*\[\s*([xX]?)\s*\]")
ARTIFACT_ORDER = ("proposal", "specs", "design", "tasks")


def project_root() -> Path:
    current = Path.cwd().resolve()
    candidates = (current, *current.parents)
    for candidate in candidates:
        if (candidate / ".specify").is_dir():
            return candidate
    for candidate in candidates:
        if (candidate / ".git").exists():
            return candidate
    return current


def project_paths() -> tuple[Path, Path, Path]:
    root = project_root() / "openspec"
    return root, root / "changes", root / "specs"


def ensure_root() -> tuple[Path, Path, Path]:
    root, changes, specs = project_paths()
    (changes / "archive").mkdir(parents=True, exist_ok=True)
    specs.mkdir(parents=True, exist_ok=True)
    return root, changes, specs


def validate_name(name: str) -> str:
    if not NAME_PATTERN.fullmatch(name):
        raise ValueError(
            "change name must be kebab-case using lowercase letters, digits, and hyphens"
        )
    return name


def change_path(name: str, *, require: bool = True) -> Path:
    _, changes, _ = project_paths()
    path = changes / validate_name(name)
    if path.is_symlink():
        raise ValueError(f"change path must not be a symbolic link: {name}")
    if require and not path.is_dir():
        raise FileNotFoundError(f"active change not found: {name}")
    return path


def task_progress(path: Path) -> dict[str, int]:
    total = 0
    complete = 0
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            match = TASK_PATTERN.match(line)
            if match:
                total += 1
                complete += bool(match.group(1))
    return {"total": total, "complete": complete, "remaining": total - complete}


def artifact_status(path: Path) -> dict[str, object]:
    specs = sorted(
        str(spec.relative_to(path))
        for spec in (path / "specs").glob("**/spec.md")
        if spec.is_file()
    )
    tasks = task_progress(path / "tasks.md")
    artifacts = {
        "proposal": (path / "proposal.md").is_file(),
        "specs": bool(specs),
        "design": (path / "design.md").is_file(),
        "tasks": (path / "tasks.md").is_file(),
    }
    next_artifact = next(
        (artifact for artifact in ARTIFACT_ORDER if not artifacts[artifact]),
        None,
    )
    return {
        "name": path.name,
        "path": str(path),
        "artifacts": artifacts,
        "specFiles": specs,
        "tasks": tasks,
        "planningComplete": all(artifacts.values()),
        "implementationComplete": tasks["total"] > 0 and tasks["remaining"] == 0,
        "nextArtifact": next_artifact,
        "modified": path.stat().st_mtime,
    }


def active_changes() -> list[dict[str, object]]:
    _, changes, _ = project_paths()
    if not changes.is_dir():
        return []
    entries = [
        artifact_status(path)
        for path in changes.iterdir()
        if path.is_dir() and not path.is_symlink() and path.name != "archive"
    ]
    return sorted(entries, key=lambda entry: entry["modified"], reverse=True)


def emit(payload: object, as_json: bool) -> None:
    if as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif isinstance(payload, str):
        print(payload)
    else:
        print(json.dumps(payload, indent=2, sort_keys=True))


def command_init(args: argparse.Namespace) -> None:
    root, changes, specs = ensure_root()
    emit(
        {
            "root": str(root),
            "changes": str(changes),
            "specs": str(specs),
        },
        args.json,
    )


def command_new(args: argparse.Namespace) -> None:
    ensure_root()
    path = change_path(args.change, require=False)
    if path.exists():
        raise FileExistsError(f"change already exists: {args.change}")
    path.mkdir(parents=True)
    emit(artifact_status(path), args.json)


def command_list(args: argparse.Namespace) -> None:
    emit({"changes": active_changes()}, args.json)


def command_status(args: argparse.Namespace) -> None:
    emit(artifact_status(change_path(args.change)), args.json)


def command_next(args: argparse.Namespace) -> None:
    status = artifact_status(change_path(args.change))
    emit(
        {
            "change": status["name"],
            "path": status["path"],
            "nextArtifact": status["nextArtifact"],
            "artifacts": status["artifacts"],
        },
        args.json,
    )


def command_archive(args: argparse.Namespace) -> None:
    _, changes, _ = ensure_root()
    source = change_path(args.change)
    prefix = args.date or date.today().isoformat()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", prefix):
        raise ValueError("archive date must use YYYY-MM-DD format")
    try:
        date.fromisoformat(prefix)
    except ValueError as error:
        raise ValueError("archive date must use YYYY-MM-DD format") from error
    target_name = (
        source.name
        if re.match(r"^\d{4}-\d{2}-\d{2}-", source.name)
        else f"{prefix}-{source.name}"
    )
    target = changes / "archive" / target_name
    if target.exists():
        raise FileExistsError(f"archive target already exists: {target}")
    shutil.move(str(source), str(target))
    emit(
        {
            "change": args.change,
            "archivePath": str(target),
        },
        args.json,
    )


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser()
    subcommands = root.add_subparsers(dest="command", required=True)

    init = subcommands.add_parser("init")
    init.add_argument("--json", action="store_true")
    init.set_defaults(handler=command_init)

    new = subcommands.add_parser("new")
    new.add_argument("--change", required=True)
    new.add_argument("--json", action="store_true")
    new.set_defaults(handler=command_new)

    listing = subcommands.add_parser("list")
    listing.add_argument("--json", action="store_true")
    listing.set_defaults(handler=command_list)

    status = subcommands.add_parser("status")
    status.add_argument("--change", required=True)
    status.add_argument("--json", action="store_true")
    status.set_defaults(handler=command_status)

    next_artifact = subcommands.add_parser("next")
    next_artifact.add_argument("--change", required=True)
    next_artifact.add_argument("--json", action="store_true")
    next_artifact.set_defaults(handler=command_next)

    archive = subcommands.add_parser("archive")
    archive.add_argument("--change", required=True)
    archive.add_argument("--date")
    archive.add_argument("--json", action="store_true")
    archive.set_defaults(handler=command_archive)

    return root


def main() -> int:
    args = parser().parse_args()
    try:
        args.handler(args)
    except (FileExistsError, FileNotFoundError, OSError, ValueError) as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
