"""Guarantee all 100 SHA-pinned J2ME candidates have real bytecode method inventories."""
import json
import pathlib
import unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
DEEP=ROOT/"docs/research/deep"
class Deep100InventoryTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  sel=json.loads((DEEP/"selection-100.json").read_text(encoding="utf8"))["principal"]
  cls.targets={r["jar_sha256"]:r for r in sel}
  cls.first=set()
  for f in (DEEP/"wave01").glob("[0-9][0-9]-*.json"):
   j=json.loads(f.read_text(encoding="utf8"));cls.first.add(j["jar_sha256"])
  cls.reports=sorted((DEEP/"bytecode-100").glob("[0-9][0-9][0-9]-*.json"))
 def test_all_100_present_nonoverlapping_and_decoded(self):
  self.assertEqual(len(self.targets),100)
  self.assertEqual(len(self.first),12)
  self.assertEqual(len(self.reports),88)
  seen=set()
  for f in self.reports:
   j=json.loads(f.read_text(encoding="utf8"))
   key=j["jar_sha256"]
   self.assertIn(key,self.targets)
   self.assertNotIn(key,seen)
   seen.add(key)
   self.assertEqual(j["jar_path"],self.targets[key]["jar_path"])
   self.assertGreater(j["methods"],0)
   self.assertGreater(j["classes_decoded"],0)
   self.assertLessEqual(j["classes_decoded"],j["classes"])
   self.assertEqual(j["status"],"BYTECODE_DISASSEMBLED_INDEXED_NOT_FULLY_REVIEWED")
   self.assertTrue(j["class_methods"])
  self.assertFalse(seen.intersection(self.first))
  self.assertEqual(seen.union(self.first),set(self.targets))
 def test_partial_review_status_stays_explicit(self):
  registry=json.loads((DEEP/"registry.json").read_text(encoding="utf8"))
  self.assertEqual(registry["bytecode_indexed_count"],100)
  self.assertEqual(len(registry["studies_in_progress"]),4)
  self.assertEqual(registry["completed_studies"],[])
  self.assertTrue(all(not j["original_executed"] for j in registry["studies_in_progress"]))
 def test_aggregate_matches_individual_records(self):
  summary=json.loads((DEEP/"bytecode-100"/"summary.json").read_text(encoding="utf8"))
  rows=[json.loads(f.read_text(encoding="utf8")) for f in self.reports]
  self.assertEqual(summary["newly_indexed"],88)
  self.assertEqual(summary["methods"],sum(r["methods"] for r in rows))
  self.assertEqual(summary["classes"],sum(r["classes"] for r in rows))
  self.assertEqual(summary["instructions"],sum(r["instructions"] for r in rows))
  self.assertEqual(summary["warnings"],sum(len(r["errors"]) for r in rows))
if __name__=="__main__":unittest.main()
