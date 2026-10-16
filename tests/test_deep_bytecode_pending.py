"""Verify 88 pending bytecode subjects are the exact selected candidates, without claims of execution."""
import json
import pathlib
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
DEEP=ROOT/"docs/research/deep"

class PendingBytecodeSubjectsTests(unittest.TestCase):
    def test_shards_have_exact_disjoint_subjects(self):
        data=json.loads((DEEP/"selection-100.json").read_text(encoding="utf8"))
        text=(DEEP/"START_HERE.md").read_text(encoding="utf8")
        selected=data["principal"]
        already=[r for r in selected if r["jar_sha256"] in text]
        remaining=[r for r in selected if r["jar_sha256"] not in text]
        self.assertEqual(len(already),12)
        self.assertEqual(len(remaining),88)
        batches=[[r for i,r in enumerate(remaining) if i%4==part] for part in range(4)]
        self.assertEqual([len(b) for b in batches],[22]*4)
        hashes=[r["jar_sha256"] for batch in batches for r in batch]
        self.assertEqual(len(set(hashes)),88)
        self.assertEqual(len(set(hashes)|{r["jar_sha256"] for r in already}),100)

if __name__=="__main__":unittest.main()
