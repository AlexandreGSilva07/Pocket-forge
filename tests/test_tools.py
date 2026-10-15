"""Testes determinísticos das ferramentas PocketForge (stdlib)."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable


class PocketForgeTests(unittest.TestCase):
    def test_scaffold_creates_standalone_game(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "aurora"
            result = subprocess.run(
                [PY, str(ROOT / "scripts/new_game.py"), str(dest), "--title", "Aurora Runner"],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Aurora Runner", (dest / "index.html").read_text())
            self.assertIn("Aurora Runner", (dest / "game.js").read_text())
            self.assertTrue((dest / "style.css").is_file())

    def test_scaffold_refuses_to_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "existing"
            dest.mkdir()
            result = subprocess.run([PY, str(ROOT / "scripts/new_game.py"), str(dest)], capture_output=True)
            self.assertNotEqual(result.returncode, 0)

    def test_audit_reports_bytes(self):
        proc = subprocess.run(
            [PY, str(ROOT / "scripts/audit.py"), str(ROOT / "demo"), "--json"],
            capture_output=True, text=True, check=True
        )
        data = json.loads(proc.stdout)
        self.assertGreaterEqual(data["file_count"], 3)
        self.assertGreater(data["total_bytes"], 100)
        self.assertIn(".js", data["by_extension"])

    def test_audit_enforces_budget(self):
        proc = subprocess.run(
            [PY, str(ROOT / "scripts/audit.py"), str(ROOT / "demo"), "--max-bytes", "1"],
            capture_output=True,
        )
        self.assertEqual(proc.returncode, 2)

    def test_asset_generator_is_reproducible(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp) / "a", Path(tmp) / "b"
            for dest in (a, b):
                p = subprocess.run([PY, str(ROOT / "scripts/make_assets.py"), str(dest), "--seed", "57"],
                                   capture_output=True, text=True)
                self.assertEqual(p.returncode, 0, p.stderr)
            for path in sorted(a.iterdir()):
                self.assertEqual(hashlib.sha256(path.read_bytes()).digest(),
                                 hashlib.sha256((b / path.name).read_bytes()).digest())
            manifest = json.loads((a / "manifest.json").read_text())
            self.assertEqual(len(manifest["assets"]), 4)


if __name__ == "__main__":
    unittest.main()
