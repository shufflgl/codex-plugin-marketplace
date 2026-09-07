from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "export_plugin_catalog", ROOT / "scripts" / "export_plugin_catalog.py"
)
exporter = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(exporter)


class PluginCatalogExportTests(unittest.TestCase):
    def test_catalog_is_generated_from_every_local_marketplace_entry(self) -> None:
        catalog = exporter.build_catalog(ROOT)
        marketplace = exporter.load_json(
            ROOT / ".agents" / "plugins" / "marketplace.json"
        )
        expected = {
            entry["name"]
            for entry in marketplace["plugins"]
            if entry["source"]["source"] == "local"
        }
        self.assertEqual({plugin["name"] for plugin in catalog["plugins"]}, expected)
        self.assertTrue(all(plugin["sourceUrl"].startswith("https://") for plugin in catalog["plugins"]))

    def test_public_catalog_contains_no_local_absolute_paths(self) -> None:
        catalog = exporter.build_catalog(ROOT)
        self.assertNotIn("/Users/", str(catalog))
        self.assertNotIn("/home/", str(catalog))


if __name__ == "__main__":
    unittest.main()
