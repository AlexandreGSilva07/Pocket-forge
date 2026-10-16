"""Verify that bytecode investigations refer to real selected JARs."""
import json
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
DEEP=ROOT/"docs/research/deep"

class Wave01Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        s=json.loads((DEEP/"selection-100.json").read_text(encoding="utf8"))
        cls.known={x["jar_sha256"]:x for x in s["principal"]}
        cls.files=sorted((DEEP/"wave01").glob("[0-9][0-9]-*.json"))
    def test_12_identity_and_disassembly(self):
        self.assertEqual(len(self.files),12)
        ids=set()
        for f in self.files:
            r=json.loads(f.read_text(encoding="utf8"))
            key=r["jar_sha256"]
            self.assertIn(key,self.known)
            self.assertNotIn(key,ids)
            ids.add(key)
            self.assertEqual(r["jar_path"],self.known[key]["jar_path"])
            self.assertGreater(r["class_count"],0)
            self.assertGreater(r["methods_count"],0)
            self.assertGreater(r["instructions_count"],0)
            self.assertTrue(r["class_details"])
            self.assertEqual(r["research_status"],"BYTECODE_DISASSEMBLED_INDEXED_NOT_FULLY_REVIEWED")
            for klass in r["class_details"]:
                self.assertTrue(klass["class_file"].endswith(".class"))
                for method in klass["methods"]:
                    self.assertIn("signature",method)
                    self.assertIn("instructions",method)
        self.assertEqual(len(ids),12)
    def test_real_reviews_marked_as_partial_not_completed(self):
        registry=json.loads((DEEP/"registry.json").read_text(encoding="utf8"))
        self.assertGreaterEqual(len(registry["studies_in_progress"]),3)
        baseline={
            "f2667dd8ee20f37d323d16a705ef9e26ed4e61f704af185e1dbb187cf7cf5761",
            "8db1413d8135bfc300525375ae0ff398548707d0d8f824cb610d797130e67c9d",
            "6df7ffc301a3524aa0935ac23311d9e132ce4c1dbf81129e5485052afc0828f2"
        }
        self.assertTrue(baseline.issubset({
            item["jar_sha256"] for item in registry["studies_in_progress"]
        }))
        self.assertEqual(registry["completed_studies"],[])
        for item in registry["studies_in_progress"]:
            self.assertEqual(item["stage"],"METHOD_REVIEW_PARTIAL")
            self.assertFalse(item["original_executed"])
            self.assertTrue((ROOT/item["report"]).is_file())
            self.assertTrue(item["reviewed_methods"])

if __name__=="__main__":
    unittest.main()
