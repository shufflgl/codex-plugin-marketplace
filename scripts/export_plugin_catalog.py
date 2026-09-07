#!/usr/bin/env python3
"""Export a public, repository-backed plugin catalog for the website."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def run(args: list[str], root: Path) -> str:
    result = subprocess.run(args, cwd=root, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain an object")
    return value


def repository_url(root: Path) -> str:
    url = run(["git", "remote", "get-url", "origin"], root)
    if url.startswith("git@github.com:"):
        url = "https://github.com/" + url.removeprefix("git@github.com:")
    return url.removesuffix(".git")


def latest_change(root: Path, path: str) -> dict[str, str] | None:
    output = run(["git", "log", "-1", "--format=%h%x1f%cI%x1f%s", "--", path], root)
    if not output:
        return None
    commit, date, subject = output.split("\x1f", 2)
    return {"commit": commit, "date": date, "subject": subject}


def build_catalog(root: Path, assets_dir: Path | None = None) -> dict[str, Any]:
    marketplace = load_json(root / ".agents" / "plugins" / "marketplace.json")
    base_url = repository_url(root)
    plugins: list[dict[str, Any]] = []

    if assets_dir:
        shutil.rmtree(assets_dir, ignore_errors=True)
        assets_dir.mkdir(parents=True, exist_ok=True)

    for entry in marketplace["plugins"]:
        if entry["source"]["source"] != "local":
            continue
        plugin_root = root / entry["source"]["path"]
        manifest = load_json(plugin_root / ".codex-plugin" / "plugin.json")
        interface = manifest.get("interface", {})
        logo = interface.get("logo") or interface.get("composerIcon")
        logo_url = None
        if logo:
            logo_path = plugin_root / logo.removeprefix("./")
            if assets_dir and logo_path.is_file():
                extension = logo_path.suffix.lower()
                output_name = f"{entry['name']}{extension}"
                shutil.copy2(logo_path, assets_dir / output_name)
                logo_url = f"/plugin-logos/{output_name}"

        plugin_path = plugin_root.relative_to(root).as_posix()
        plugins.append(
            {
                "name": entry["name"],
                "displayName": interface.get("displayName", entry["name"]),
                "summary": manifest["description"],
                "longDescription": interface.get("longDescription", manifest["description"]),
                "version": manifest["version"],
                "developerName": interface.get("developerName")
                or manifest.get("author", {}).get("name", "Unknown developer"),
                "category": entry["category"],
                "capabilities": interface.get("capabilities", []),
                "logoUrl": logo_url,
                "sourceUrl": f"{base_url}/tree/main/{plugin_path}",
                "latestChange": latest_change(root, plugin_path),
            }
        )

    return {
        "schemaVersion": 1,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "marketplace": {
            "name": marketplace["name"],
            "displayName": marketplace.get("interface", {}).get("displayName", marketplace["name"]),
        },
        "repository": {
            "name": "shufflgl/codex-plugin-marketplace",
            "url": base_url,
            "branch": run(["git", "branch", "--show-current"], root) or "main",
            "commit": run(["git", "rev-parse", "--short=7", "HEAD"], root),
        },
        "plugins": plugins,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--assets-dir", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    catalog = build_catalog(root, args.assets_dir.resolve() if args.assets_dir else None)
    output.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
    print(f"Exported {len(catalog['plugins'])} plugins to {output}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
