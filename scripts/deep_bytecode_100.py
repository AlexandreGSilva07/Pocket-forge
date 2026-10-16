#!/usr/bin/env python3
"""Bytecode-level inventory for the remaining 88 selected games.

For every selected JAR: verify original SHA-256, javap disassemble classes,
store each named method signature, instruction/branch counts, main call
targets, resources and errors. NO execution. NO third-party decompiled code.
The first 12 were already analyzed with richer inventories in wave01/.
"""
import argparse, collections, hashlib, json, pathlib, tempfile, zipfile
from deep_bytecode_wave import inspect

ROOT=pathlib.Path(__file__).resolve().parents[1]
DEEP=ROOT/"docs/research/deep"
SEL=json.loads((DEEP/"selection-100.json").read_text(encoding="utf8"))["principal"]
WAVE=(DEEP/"START_HERE.md").read_text(encoding="utf8")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("archive")
    ap.add_argument("--part",type=int,required=True)
    ap.add_argument("--parts",type=int,default=4)
    args=ap.parse_args()
    if args.part<0 or args.part>=args.parts or args.parts!=4:
        raise ValueError("must be one of four deterministic shards")
    selection=[s for s in SEL if s["jar_sha256"] not in WAVE]
    assert len(selection)==88,len(selection)
    scope=[x for i,x in enumerate(selection) if i%args.parts==args.part]
    output=DEEP/"bytecode-100";output.mkdir(parents=True,exist_ok=True)
    count=0
    with zipfile.ZipFile(args.archive) as archive, tempfile.TemporaryDirectory() as temp:
        for game in scope:
            path=game["jar_path"]
            payload=archive.read(path)
            if hashlib.sha256(payload).hexdigest()!=game["jar_sha256"]:
                raise ValueError("source JAR SHA mismatch: "+path)
            existing_file=output/f"{game['rank']:03d}-{game['jar_sha256'][:12]}.json"
            if existing_file.exists():
                existing=json.loads(existing_file.read_text(encoding="utf8"))
                if (existing.get("jar_sha256")==game["jar_sha256"] and
                    existing.get("methods",0)>0 and not existing.get("errors")):
                    count+=1
                    print("REUSE_CLEAN_REPORT",game["rank"],flush=True)
                    continue
            raw=inspect(path,payload,game,pathlib.Path(temp))
            classes=[]
            for cl in raw["class_details"]:
                classes.append({
                    "class":cl["class_name"],"source_mode":cl.get("source_mode","unknown"),"method_count":cl["methods_count"],
                    "instructions":cl["instructions_count"],"branches":cl["branch_count"],
                    "methods":[{"signature":m["signature"],"instructions":m["instructions"],
                         "branches":m["branches"],"calls":dict(list(m["calls"].items())[:8])}
                      for m in cl["methods"]]
                })
            record={
                "rank":game["rank"],"jar_path":game["jar_path"],"jar_sha256":game["jar_sha256"],
                "title":game["game_title"],"track":game["track"],
                "status":"BYTECODE_DISASSEMBLED_INDEXED_NOT_FULLY_REVIEWED",
                "tool":"OpenJDK javap -p -c; JAR never executed",
                "classes":raw["class_count"],"classes_decoded":len(raw["class_details"]),
                "methods":raw["methods_count"],"instructions":raw["instructions_count"],
                "branches":raw["branch_count"],"errors":raw["errors"],
                "hot_methods_by_static_instruction_count":raw["method_examples"][:12],
                "call_targets":raw["call_edges"][:35],
                "opcode_histogram":raw["opcode_histogram"],
                "resource_file_count":len(raw["resource_files"]),
                "resources_by_suffix":dict(collections.Counter(
                  pathlib.PurePosixPath(r["path"]).suffix.lower() or "[none]"
                  for r in raw["resource_files"])),
                "class_methods":classes,
                "limitation":"Static method inspection, no game execution, no proof of hot paths or semantic equivalence."
            }
            file=output/f"{game['rank']:03d}-{game['jar_sha256'][:12]}.json"
            file.write_text(json.dumps(record,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
            count+=1
            print("DONE",count,"of",len(scope),"rank",game["rank"],
                  "methods",raw["methods_count"],"classes",raw["class_count"],
                  "errors",len(raw["errors"]),flush=True)
    assert count==22
    print("SHARD_COMPLETE",args.part,count,flush=True)

if __name__=="__main__":main()
