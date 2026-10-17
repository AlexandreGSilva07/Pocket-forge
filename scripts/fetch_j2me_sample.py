#!/usr/bin/env python3
"""Download a named J2ME research specimen into ignored external-corpus/, never into Git."""
import argparse,hashlib,json,zipfile
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request,urlopen
ALLOWED={"M5-Dev/j2me-vault","M5-Dev/j2me-full-romset"}
CAP=64*1024*1024
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument("--dataset",choices=sorted(ALLOWED),default="M5-Dev/j2me-vault")
 p.add_argument("--filename",required=True,help="e.g. Games/AsphaltNitro.jar")
 p.add_argument("--revision",default="main")
 a=p.parse_args();name=Path(a.filename)
 if name.is_absolute() or ".." in name.parts or name.suffix.lower() not in {".jar",".jad"}:p.error("unsafe or unsupported filename")
 url="https://huggingface.co/datasets/"+a.dataset+"/resolve/"+quote(a.revision,safe="")+"/"+quote(name.as_posix(),safe="/")+"?download=true"
 dest=Path("external-corpus")/a.dataset.replace("/","_")/name
 dest.parent.mkdir(parents=True,exist_ok=True);tmp=dest.with_suffix(dest.suffix+".partial")
 h=hashlib.sha256();n=0
 try:
  with urlopen(Request(url,headers={"User-Agent":"PocketForge-research/1.0"}),timeout=75) as resp, tmp.open("wb") as f:
   while True:
    chunk=resp.read(262144)
    if not chunk:break
    n+=len(chunk)
    if n>CAP:raise ValueError("download exceeded 64 MiB cap")
    h.update(chunk);f.write(chunk)
  if dest.suffix.lower()==".jar" and not zipfile.is_zipfile(tmp):raise ValueError("download not a valid JAR/ZIP")
  tmp.replace(dest)
 finally:tmp.unlink(missing_ok=True)
 receipt={"dataset":a.dataset,"filename":a.filename,"sha256":h.hexdigest(),"bytes":n,"path":str(dest),"url":url}
 dest.with_suffix(dest.suffix+".receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
 print(json.dumps(receipt,indent=2))
if __name__=="__main__":main()
