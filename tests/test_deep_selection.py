"""Ensure the deep-research selection is evidence-based and bound to 1649 JAR records."""
import collections
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
BATCHES = ROOT / "docs" / "research" / "batches"
DEEP = ROOT / "docs" / "research" / "deep"

class DeepSelectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.obj = json.loads((DEEP / "selection-100.json").read_text(encoding="utf-8"))
        cls.primary = cls.obj["principal"]
        cls.reserve = cls.obj["reserva"]
        cls.all = cls.primary + cls.reserve
        cls.pool = {}
        for i in range(1, 18):
            content = json.loads((BATCHES / f"{i:03d}.json").read_text(encoding="utf-8"))
            for row in content["records"]:
                cls.pool[row["jar_sha256"]] = row

    def test_selection_counts_and_track_quotas(self):
        self.assertEqual(len(self.primary), 100)
        self.assertEqual(len(self.reserve), 25)
        self.assertEqual(
            dict(collections.Counter(r["track"] for r in self.primary)),
            {"render3d":20, "worlds":20, "strategy":17,
             "assets":16, "physics":15, "compact":12})
        self.assertEqual([r["rank"] for r in self.primary], list(range(1,101)))
        self.assertEqual([r["rank"] for r in self.reserve], list(range(1,26)))

    def test_every_id_exists_in_complete_original_ledger(self):
        self.assertEqual(len(self.pool), 1649)
        ids = [r["jar_sha256"] for r in self.all]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(ids), 125)
        for r in self.all:
            with self.subTest(r=r["jar_path"]):
                self.assertIn(r["jar_sha256"], self.pool)
                src = self.pool[r["jar_sha256"]]
                self.assertEqual(r["jar_path"], src["jar_path"])
                self.assertEqual(r["jad_path"], src["jad_path"])
                self.assertEqual(r["classes"], src["classes"])
                self.assertEqual(r["images"], src["images"])
                self.assertEqual(r["audio"], src["audio"])
                self.assertEqual(r["id"], r["jar_sha256"][:16])
                self.assertFalse(src.get("entry_errors"))
                self.assertTrue(r["investigation_targets"])
                self.assertTrue(r["study_question"])

    def test_only_games_are_primary_not_benchmark_programs(self):
        self.assertNotIn("JBenchmark3D", [r["game_title"] for r in self.primary])
        controls = self.obj.get("technical_controls_not_games", [])
        self.assertEqual(len(controls), 1)
        self.assertEqual(controls[0]["jar_path"].split("/")[-1], "JBenchmark3D.jar")
        self.assertNotIn(controls[0]["jar_sha256"], [r["jar_sha256"] for r in self.all])

    def test_every_lot_represented_and_no_decompilation_claims(self):
        self.assertEqual(set(r["batch"] for r in self.primary), set(range(1,18)))
        self.assertTrue(all(r["status"] == "selected_not_decompiled" for r in self.all))
        self.assertEqual(self.obj["status"], "seleção_sem_descompilação")
        full_report = (DEEP / "selection-100.md").read_text(encoding="utf-8")
        for row in self.all:
            self.assertIn(row["id"], full_report)

if __name__ == "__main__":
    unittest.main()
