#!/usr/bin/env python3
"""Run SHA-verified javap inventory of the 88 remaining selected Java ME games."""
import hashlib,json,os,pathlib,subprocess,sys,tempfile,time,urllib.request,zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
D=ROOT/"docs/research/deep"
URL="https://archive.org/download/1000_J2ME_Games_Pack/1000JavaGames.zip"
EXPECTED="f8e3fb19f0cb451a1eebecccc16c4cb941c68293db2990a4e82df68bfa2c10dd"
def main():
 sel=json.loads((D/"selection-100.json").read_text(encoding="utf8"))["principal"]
 first=(D/"START_HERE.md").read_text(encoding="utf8")
 rest=[x for x in sel if x["jar_sha256"] not in first]
 assert len(rest)==88
 archive=pathlib.Path(os.environ.get("RUNNER_TEMP",tempfile.gettempdir()))/"pocketforge-j2me-source.zip"
 for attempt in range(3):
  try:
   req=urllib.request.Request(URL,headers={"User-Agent":"PocketForge-research/1.0"})
   with urllib.request.urlopen(req,timeout=60) as inp,archive.open("wb") as out:
    while True:
     chunk=inp.read(1024*1024)
     if not chunk:break
     out.write(chunk)
   with archive.open("rb") as f:sha=hashlib.file_digest(f,"sha256").hexdigest()
   if sha!=EXPECTED:raise ValueError("Archive hash mismatch: "+sha)
   with zipfile.ZipFile(archive) as z:print("ZIP_FILES",len(z.namelist()),flush=True)
   break
  except Exception as e:
   print("ATTEMPT",attempt+1,str(e)[:200],flush=True)
   if attempt==2:raise
   time.sleep((attempt+1)*4)
 try:
  for part in range(4):
   print("BEGIN",part,flush=True)
   subprocess.run([sys.executable,str(ROOT/"scripts/deep_bytecode_100.py"),str(archive),"--part",str(part),"--parts","4"],check=True,cwd=ROOT)
  folder=D/"bytecode-100";files=sorted(folder.glob("[0-9][0-9][0-9]-*.json"))
  assert len(files)==88,len(files)
  entries=[json.loads(f.read_text(encoding="utf8")) for f in files]
  assert {x["jar_sha256"] for x in entries}=={x["jar_sha256"] for x in rest}
  summary={"archive_sha256":EXPECTED,"scope":"Real javap disassembly and method inventory; no emulation or full semantic understanding.",
    "newly_indexed":88,"total_selected_indexed":100,
    "classes":sum(e["classes"] for e in entries),"classes_decoded":sum(e["classes_decoded"] for e in entries),
    "methods":sum(e["methods"] for e in entries),"instructions":sum(e["instructions"] for e in entries),
    "warnings":sum(len(e["errors"]) for e in entries),
    "items":[{"rank":e["rank"],"name":e["title"],"sha256":e["jar_sha256"],"methods":e["methods"],"warnings":len(e["errors"])} for e in sorted(entries,key=lambda e:e["rank"])]}
  (folder/"summary.json").write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
  lines=["# Bytecode inventories of all 100 selected JARs","",
    "12 were indexed earlier in wave01. The other 88 were SHA-verified, opened and disassembled with OpenJDK javap.",
    "This does NOT mean all 100 games are semantically understood or were executed in an emulator.",
    "",
    "Methods: "+str(summary["methods"])+"; instructions: "+str(summary["instructions"])+"; classes: "+str(summary["classes"])+"; warnings: "+str(summary["warnings"]),
    "",
    "| Rank | Game | SHA prefix | Classes and methods | Warnings |","|---:|---|---|---:|---:|"]
  for e in sorted(entries,key=lambda e:e["rank"]):
   lines.append("| "+str(e["rank"])+" | "+e["title"].replace("|","/")+" | "+e["jar_sha256"][:12]+" | "+str(e["classes"])+"/"+str(e["methods"])+" | "+str(len(e["errors"]))+" |")
  lines+=["","The 88 individual JSON reports include signatures, calls, branches and opcode counts. Resource data and proprietary classfiles are not published.","","Next: human control-flow analysis, original-game runtime verification, original engine reconstruction and benchmark comparisons."]
  (folder/"README.md").write_text("\n".join(lines)+"\n",encoding="utf8")
  registry_file=D/"registry.json"
  registry=json.loads(registry_file.read_text(encoding="utf8"))
  registry["status"]="bytecode_indexed_100_3_partial_method_reviews"
  registry["bytecode_indexed_count"]=100
  registry["bytecode_index_files"]=["docs/research/deep/wave01/overview.md","docs/research/deep/bytecode-100/README.md"]
  registry["completed_studies"]=[]
  registry_file.write_text(json.dumps(registry,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
  print("SUCCESS",json.dumps({k:v for k,v in summary.items() if k!="items"}),flush=True)
 finally:
  archive.unlink(missing_ok=True)
if __name__=="__main__":main()
