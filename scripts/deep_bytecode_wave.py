#!/usr/bin/env python3
"""Disassemble real Java ME classfiles for a verified 12-JAR research wave.

Stores ORIGINAL analysis metadata (method inventories, opcode/call summaries).
Does not execute MIDlets or publish decompiled third-party code/resources.
Disassembly is performed with javap -c -p in a temporary directory.
"""
import collections
import hashlib
import io
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import zipfile

ROOT=pathlib.Path(__file__).resolve().parents[1]
SELECTION=json.loads((ROOT/"docs/research/deep/selection-100.json").read_text(encoding="utf8"))
SAMPLE=(ROOT/"docs/research/deep/START_HERE.md").read_text(encoding="utf8")
DEST=ROOT/"docs/research/deep/wave01"
FOCUS=("drawPixels","drawRegion","drawImage","paint","render","update","run",
       "minimax","undoMove","getResourceAsStream","read","step","tick","level","drawRGB")
SIGNATURE=re.compile(r"^\s{2}(?:public |private |protected |static |final |synchronized |abstract |native )*[\w.$<>\[\]/ ,]+\(.*\)[;]?\s*(?:throws [\w., ]+)?$")
INSTR=re.compile(r"^\s+\d+:\s+([a-z][a-z0-9_]*)\b")
CALL=re.compile(r"// (?:InterfaceMethod|Method) ([\w/$<>.]+)\.([\w$<>]+):")
STRINGS=re.compile(r"// String ([^;]+)")

def parse_disassembly(text):
    methods=[];cur=None;call_edges=collections.Counter();opcodes=collections.Counter()
    for line in text.splitlines():
        if SIGNATURE.match(line):
            cur={"signature":line.strip(),"instructions":0,"calls":collections.Counter(),
                 "opcodes":collections.Counter(),"strings":[],"branches":0}
            methods.append(cur)
        m=INSTR.match(line)
        if cur is None or not m:continue
        op=m.group(1);cur["instructions"]+=1;cur["opcodes"][op]+=1;opcodes[op]+=1
        if op.startswith(("if","goto","tableswitch","lookupswitch")):cur["branches"]+=1
        f=CALL.search(line)
        if f:
            called=(f.group(1).replace("/",".")+"."+f.group(2))
            cur["calls"][called]+=1;call_edges[called]+=1
        s=STRINGS.search(line)
        if s and len(cur["strings"])<25:cur["strings"].append(s.group(1)[:80])
    for v in methods:
        v["calls"]=dict(v["calls"].most_common(20))
        v["opcodes"]=dict(v["opcodes"].most_common(15))
    return methods,opcodes,call_edges

def inspect(path,raw,selected,temp_root):
    if hashlib.sha256(raw).hexdigest()!=selected["jar_sha256"]:
        raise ValueError("SHA mismatch for "+path)
    out={"jar_path":path,"jar_sha256":selected["jar_sha256"],
         "game_title":selected["game_title"],"jar_bytes":len(raw),
         "research_status":"BYTECODE_DISASSEMBLED_INDEXED_NOT_FULLY_REVIEWED",
         "class_count":0,"methods_count":0,"instructions_count":0,
         "branch_count":0,"method_examples":[],"class_details":[],"errors":[],
         "call_edges":[],"opcode_histogram":{},"resource_files":[]}
    jarpath=temp_root/"subject.jar";jarpath.write_bytes(raw)
    all_calls=collections.Counter();all_ops=collections.Counter()
    with zipfile.ZipFile(io.BytesIO(raw)) as jar:
        class_files=sorted(n for n in jar.namelist() if n.endswith(".class"))
        out["class_count"]=len(class_files)
        out["resource_files"]=[{"path":i.filename,"size":i.file_size}
              for i in jar.infolist() if not i.is_dir() and not i.filename.endswith(".class")][:180]
        for name in class_files:
            class_id=name[:-6].replace("/",".")
            try:
                cp=subprocess.run(["javap","-classpath",str(jarpath),"-p","-c",class_id],
                                  capture_output=True,text=True,timeout=25)
                if cp.returncode:raise RuntimeError(cp.stderr[:250])
                methods,ops,calls=parse_disassembly(cp.stdout)
                if not methods:
                    raise RuntimeError("no method signatures detected (obfuscated/invalid class?)")
                all_ops.update(ops);all_calls.update(calls)
                out["methods_count"]+=len(methods)
                class_report={"class_file":name,"class_name":class_id,
                    "methods_count":len(methods),
                    "instructions_count":sum(m["instructions"] for m in methods),
                    "branch_count":sum(m["branches"] for m in methods),
                    "methods":[{"signature":m["signature"],"instructions":m["instructions"],
                                "branches":m["branches"],"calls":m["calls"],
                                "opcodes":m["opcodes"]} for m in methods]}
                out["class_details"].append(class_report)
                for m in methods:
                    imp=sum(m["instructions"] for k in m["calls"] if any(tag in k for tag in FOCUS))
                    priority=m["instructions"]+m["branches"]*3+imp
                    if priority>10:
                        out["method_examples"].append({"class":class_id,"signature":m["signature"],
                           "instructions":m["instructions"],"branches":m["branches"],
                           "priority_score":priority,"calls":m["calls"]})
            except Exception as exc:
                out["errors"].append({"class_file":name,"reason":str(exc)[:250]})
    out["instructions_count"]=sum(x["instructions_count"] for x in out["class_details"])
    out["branch_count"]=sum(x["branch_count"] for x in out["class_details"])
    out["call_edges"]=[{"target":k,"count":n} for k,n in all_calls.most_common(70)]
    out["opcode_histogram"]=dict(all_ops.most_common(35))
    out["method_examples"].sort(key=lambda x:-x["priority_score"])
    out["method_examples"]=out["method_examples"][:20]
    return out

def main():
    if len(sys.argv)!=2:raise SystemExit("Usage: deep_bytecode_wave.py /tmp/1000JavaGames.zip")
    archive=pathlib.Path(sys.argv[1])
    with zipfile.ZipFile(archive) as z:
        selection=[a for a in SELECTION["principal"]
                   if a["jar_sha256"] in SAMPLE]
        if len(selection)!=12:raise ValueError(f"Expected 12 SHA IDs in START_HERE.md, got {len(selection)}")
        order={sha:i for i,sha in enumerate(
            re.findall(r"\b[a-f0-9]{64}\b",SAMPLE))}
        selection.sort(key=lambda x:order[x["jar_sha256"]])
        DEST.mkdir(parents=True,exist_ok=True)
        summary=[]
        with tempfile.TemporaryDirectory() as td:
            for index,record in enumerate(selection,1):
                path=record["jar_path"]
                raw=z.read(path)
                a=inspect(path,raw,record,pathlib.Path(td))
                summary.append(a)
                (DEST/f"{index:02d}-{record['jar_sha256'][:12]}.json").write_text(
                    json.dumps(a,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
                print(f"METHOD_AUDIT {index}/12 {record['game_title']} "
                      f"classes={a['class_count']} methods={a['methods_count']} "
                      f"instructions={a['instructions_count']} errors={len(a['errors'])}",flush=True)
    lines=["# Wave 01 — bytecode method inventory for 12 J2ME games","",
      "> These 12 JARs were verified by their complete SHA-256 and passed to javap for actual bytecode disassembly. "
      "**These mechanically obtained method inventories are not 12 fully understood/reconstructed engines.**",
      "",
      "| # | JAR | Classes | Methods | Instructions | Branch instructions | Errors |",
      "|---:|---|---:|---:|---:|---:|---:|"]
    for i,rec in enumerate(summary,1):
        lines.append(f"| {i} | \`{rec['game_title']}\` (\`{rec['jar_sha256'][:12]}\`) | "
            f"{rec['class_count']} | {rec['methods_count']} | {rec['instructions_count']} | "
            f"{rec['branch_count']} | {len(rec['errors'])} |")
    lines.extend(["","## Evidence records","","Each numbered JSON stores EVERY readable class and method signature, "
            "instruction count, branch count, top method-local call targets/opcodes, important methods, "
            "aggregated call references, and non-code resource names/sizes. No full source or bytecode text is published.",
            "Game executability and visual behavior have NOT been verified here. "
            "Static methods may be dead code; calls don't imply hot paths.","",
            "## Next required work","","Manual reconstruction of selected methods, original-game runtime tests, "
            "functional PocketForge implementations and measured benchmarks are separate stages.",
            "",
            "## Validation","",
            "Source corpus SHA-256 is pinned in ../batches/registry.json; each record checks exact JAR SHA-256. "
            "Run via scripts/deep_bytecode_wave.py with the source ZIP on GitHub Actions."])
    (DEST/"overview.md").write_text("\n".join(lines)+"\n",encoding="utf8")
    print("WAVE_COMPLETE",len(summary),"class_count",sum(x["class_count"] for x in summary),
        "method_count",sum(x["methods_count"] for x in summary),flush=True)

if __name__=="__main__":main()
