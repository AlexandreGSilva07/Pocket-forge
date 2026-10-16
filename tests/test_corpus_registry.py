"""Verifica o ledger persistente das 17 auditorias sintéticas J2ME.

Não acessa o ZIP de terceiros; verifica identidade, integridade e rastreabilidade
de todos os relatórios versionados que serão usados nas próximas conversas.
"""
import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
BATCHES = ROOT / "docs" / "research" / "batches"


class CorpusRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads((BATCHES / "registry.json").read_text(encoding="utf-8"))

    def test_complete_corpus_and_unique_hashes(self):
        batches = self.registry["batches"]
        self.assertEqual(self.registry["total_recorded"], 1649)
        self.assertEqual([b["batch"] for b in batches], list(range(1, 18)))
        self.assertEqual([b["count"] for b in batches], [100] * 16 + [49])
        hashes = [h for b in batches for h in b["file_ids_sha256"]]
        self.assertEqual(len(hashes), 1649)
        self.assertEqual(len(set(hashes)), 1649)
        for h in hashes:
            self.assertRegex(h, r"^[a-f0-9]{64}$")

    def test_each_report_matches_registry(self):
        cursor = 0
        for batch in self.registry["batches"]:
            tag = f"{batch['batch']:03d}"
            with self.subTest(batch=tag):
                catalog = json.loads((BATCHES / f"{tag}.json").read_text(encoding="utf-8"))
                markdown = (BATCHES / f"{tag}.md").read_text(encoding="utf-8")
                csv_file = BATCHES / f"{tag}.csv"
                self.assertTrue(csv_file.exists())
                records = catalog["records"]
                self.assertEqual(len(records), batch["count"])
                self.assertEqual(len(records), catalog["count"])
                self.assertEqual(
                    [r["jar_sha256"] for r in records],
                    batch["file_ids_sha256"])
                for i, record in enumerate(records):
                    self.assertEqual(record["sequence"], cursor + i + 1)
                    self.assertEqual(record["id"], record["jar_sha256"][:16])
                    self.assertTrue(record["jar_path"].lower().endswith(".jar"))
                    self.assertTrue(record["game_title"])
                    self.assertIn(record["jar_path"], markdown)
                    self.assertIn(record["id"], markdown)
                    self.assertEqual(bool(record["jad_path"]), record["jad_available"])
                    if record["jad_path"]:
                        self.assertTrue(record["jad_path"].lower().endswith(".jad"))
                cursor += len(records)
        self.assertEqual(cursor, 1649)

    def test_fixed_archive_provenance(self):
        expected = "f8e3fb19f0cb451a1eebecccc16c4cb941c68293db2990a4e82df68bfa2c10dd"
        self.assertEqual(self.registry["archive_sha256"], expected)
        self.assertEqual(
            self.registry["source"],
            "https://archive.org/download/1000_J2ME_Games_Pack/1000JavaGames.zip")


if __name__ == "__main__":
    unittest.main()
