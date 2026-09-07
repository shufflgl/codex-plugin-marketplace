from __future__ import annotations

import json
import struct
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "photo-art-studio"


class PhotoArtStudioTests(unittest.TestCase):
    def test_manifest_references_packaged_skill_and_logo(self) -> None:
        manifest = json.loads(
            (PLUGIN / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["name"], PLUGIN.name)
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertTrue(
            (PLUGIN / "skills" / "create-photo-art" / "SKILL.md").is_file()
        )
        for key in ("composerIcon", "logo"):
            asset = manifest["interface"][key].removeprefix("./")
            self.assertTrue((PLUGIN / asset).is_file(), asset)

    def test_logo_is_square_rgba_png(self) -> None:
        logo = (PLUGIN / "assets" / "logo.png").read_bytes()
        self.assertEqual(logo[:8], b"\x89PNG\r\n\x1a\n")
        width, height, _, color_type = struct.unpack(">IIBB", logo[16:26])
        self.assertEqual(width, height)
        self.assertEqual(color_type, 6)


if __name__ == "__main__":
    unittest.main()
