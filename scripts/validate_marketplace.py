#!/usr/bin/env python3
"""Validate the local Codex marketplace catalog without external dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / ".agents/plugins/marketplace.json"
CATEGORIES = ROOT / "categories.json"
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
INSTALLATION = {"AVAILABLE", "INSTALLED_BY_DEFAULT", "NOT_AVAILABLE"}
AUTHENTICATION = {"ON_INSTALL", "ON_USE"}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(f"missing file: {path.relative_to(ROOT)}")
    except json.JSONDecodeError as error:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {error}")
    if not isinstance(value, dict):
        fail(f"{path.relative_to(ROOT)} must contain a JSON object")
    return value


def require_string(value: Any, field: str, context: str) -> str:
    if not isinstance(value, str) or not value:
        fail(f"{context}.{field} must be a non-empty string")
    return value


def main() -> None:
    catalog = load_json(CATALOG)
    categories = load_json(CATEGORIES)
    catalog_name = require_string(catalog.get("name"), "name", "marketplace")
    if not NAME.fullmatch(catalog_name):
        fail("marketplace.name must use kebab-case")

    interface = catalog.get("interface")
    if not isinstance(interface, dict):
        fail("marketplace.interface must be an object")
    require_string(interface.get("displayName"), "displayName", "marketplace.interface")

    plugins = catalog.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        fail("marketplace.plugins must be a non-empty array")

    seen: set[str] = set()
    local_plugin_directories: set[str] = set()
    for index, entry in enumerate(plugins):
        context = f"marketplace.plugins[{index}]"
        if not isinstance(entry, dict):
            fail(f"{context} must be an object")
        name = require_string(entry.get("name"), "name", context)
        if not NAME.fullmatch(name):
            fail(f"{context}.name must use kebab-case")
        if name in seen:
            fail(f"duplicate marketplace plugin name: {name}")
        seen.add(name)

        source = entry.get("source")
        if not isinstance(source, dict):
            fail(f"{context}.source must be an object")
        source_type = require_string(source.get("source"), "source", f"{context}.source")
        policy = entry.get("policy")
        if not isinstance(policy, dict):
            fail(f"{context}.policy must be an object")
        installation = require_string(policy.get("installation"), "installation", f"{context}.policy")
        authentication = require_string(policy.get("authentication"), "authentication", f"{context}.policy")
        if installation not in INSTALLATION:
            fail(f"{context}.policy.installation must be one of {sorted(INSTALLATION)}")
        if authentication not in AUTHENTICATION:
            fail(f"{context}.policy.authentication must be one of {sorted(AUTHENTICATION)}")
        category = require_string(entry.get("category"), "category", context)
        if category not in categories:
            fail(f"{context}.category is not registered in categories.json")

        if source_type == "local":
            source_path = require_string(source.get("path"), "path", f"{context}.source")
            if not source_path.startswith("./"):
                fail(f"{context}.source.path must start with ./")
            plugin_root = (ROOT / source_path).resolve()
            try:
                plugin_root.relative_to(ROOT.resolve())
            except ValueError:
                fail(f"{context}.source.path must remain inside the repository")
            manifest_path = plugin_root / ".codex-plugin/plugin.json"
            manifest = load_json(manifest_path)
            local_plugin_directories.add(plugin_root.name)
            manifest_name = require_string(manifest.get("name"), "name", str(manifest_path.relative_to(ROOT)))
            if manifest_name != name:
                fail(f"{context}.name ({name}) does not match manifest name ({manifest_name})")
            require_string(manifest.get("version"), "version", str(manifest_path.relative_to(ROOT)))
            require_string(manifest.get("description"), "description", str(manifest_path.relative_to(ROOT)))
            interface = manifest.get("interface")
            if not isinstance(interface, dict):
                fail(f"{manifest_path.relative_to(ROOT)}.interface must be an object")
            for field in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
                require_string(interface.get(field), field, f"{manifest_path.relative_to(ROOT)}.interface")
            for field in ("composerIcon", "logo", "logoDark"):
                asset = interface.get(field)
                if asset is None:
                    continue
                asset_path = require_string(asset, field, f"{manifest_path.relative_to(ROOT)}.interface")
                if not asset_path.startswith("./") or not (plugin_root / asset_path).is_file():
                    fail(f"{manifest_path.relative_to(ROOT)}.interface.{field} must reference an existing plugin file")
        elif source_type in {"url", "git-subdir", "npm"}:
            # Remote entries are intentionally validated only structurally here.
            print(f"INFO: remote source validation is deferred for {name} ({source_type})")
        else:
            fail(f"{context}.source.source is unsupported by this validator: {source_type}")

    on_disk = {
        path.name
        for path in (ROOT / "plugins").iterdir()
        if path.is_dir() and (path / ".codex-plugin" / "plugin.json").is_file()
    }
    if on_disk != local_plugin_directories:
        fail(
            "local marketplace entries and plugin directories differ: "
            f"catalog={sorted(local_plugin_directories)}, disk={sorted(on_disk)}"
        )

    print(f"OK: {catalog_name} — validated {len(plugins)} plugin(s)")


if __name__ == "__main__":
    main()
