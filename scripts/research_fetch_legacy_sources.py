#!/usr/bin/env python3
"""Download and inspect research archives, never execute imported programs."""
import collections, hashlib, json, os, pathlib, sys, time, urllib.request, zipfile
SOURCES = {
"emulators":[("freej2me","https://api.github.com/repos/hex007/freej2me/zipball"),("freej2me-pro","https://api.github.com/repos/digitalgust/freej2mePro/zipball"),("j2me-loader","https://api.github.com/repos/nikita36078/J2ME-Loader/zipball"),("eka2l1","https://api.github.com/repos/EKA2L1/EKA2L1/zipball"),("squirreljme","https://api.github.com/repos/SquirrelJME/SquirrelJME/zipball")],
"runtimes":[("phoneme-source","https://api.github.com/repos/magicus/phoneME/zipball"),("phoneme-mr2-source","https://phonej2me.github.io/downloads-10-06-2007/phoneme_feature-mr2-rel-src-b23-08_may_2007.zip"),("phoneme-mr2-linux-x86","https://phonej2me.github.io/downloads-10-06-2007/phoneme_feature-mr2-rel-bin-b23-linuxx86-08_may_2007.zip"),("phoneme-mr2-linux-arm","https://phonej2me.github.io/downloads-10-06-2007/phoneme_feature-mr2-rel-bin-b23-linuxarm-08_may_2007.zip"),("phoneme-mr2-win-x86","https://phonej2me.github.io/downloads-10-06-2007/phoneme_feature-mr2-rel-bin-b23-win-08_may_2007.zip")],
"documents":[("symbian-archive","https://api.github.com/repos/mrRosset/Symbian-Archive/zipball"),("blackberry-jde-samples","https://api.github.com/repos/blackberry/JDE-Samples/zipball"),("palm-dev-docs","https://api.github.com/repos/pmastrosimone/palm-dev-docs/zipball"),("j2me-polish","https://api.github.com/repos/Enough-Software/j2mepolish/zipball"),("docomo-doja5-guide","https://www.docomo.ne.jp/english/binary/pdf/service/developer/make/content/iappli/technical_data/doja/jguidefordoja5_x_en_080527.pdf")]
}
MAX_FILE=85*1024*1024
MAX_GROUP=190*1024*1024
SIGNALS=["MIDlet","GameCanvas","drawRGB","drawRegion","DirectGraphics","Graphics3D","javax.microedition.m3g","RecordStore","OpenGL","MIDP","CLDC"]
def analyze(path):
    if path.suffix==".pdf": return {"type":"pdf","header_valid":True}
    with zipfile.ZipFile(path) as z:
        entries=z.infolist()
        ext=collections.Counter(pathlib.Path(x.filename).suffix.lower() for x in entries if not x.is_dir())
        found=collections.Counter(); scanned=0
        for x in entries:
            if scanned>=120:break
            if x.is_dir() or x.file_size>160000 or pathlib.Path(x.filename).suffix.lower() not in (".java",".c",".h",".cpp",".md",".txt"):continue
            try: sample=z.read(x)[:160000].decode("utf8","ignore").lower()
            except Exception:continue
            scanned+=1
            for key in SIGNALS:
                if key.lower() in sample:found[key]+=1
        return {"type":"zip","entries":len(entries),"top_extensions":ext.most_common(12),"source_samples":scanned,"signals_in_sample":dict(found)}
def fetch(url,dest,max_bytes):
    req=urllib.request.Request(url,headers={"User-Agent":"PocketForge-research/1.0","Accept":"application/octet-stream"})
    with urllib.request.urlopen(req,timeout=70) as response:
        size=response.headers.get("Content-Length")
        if size and int(size)>max_bytes:raise ValueError("content length exceeded limit: "+size)
        sha=hashlib.sha256();n=0
        with dest.open("wb") as output:
            while True:
                buf=response.read(262144)
                if not buf:break
                n+=len(buf)
                if n>max_bytes:raise ValueError("response exceeded byte cap")
                sha.update(buf);output.write(buf)
        return {"bytes":n,"sha256":sha.hexdigest(),"final_url":response.geturl()}
def main(group):
    folder=pathlib.Path("legacy-research-output")/group;folder.mkdir(parents=True,exist_ok=True)
    items=[];total=0
    for name,url in SOURCES[group]:
        kind="documentation" if url.endswith(".pdf") else ("runtimes" if "bin-b23" in url else "sources")
        destfolder=folder/kind;destfolder.mkdir(exist_ok=True)
        dest=destfolder/(name+(".pdf" if kind=="documentation" else ".zip"))
        entry={"name":name,"source_url":url,"category":kind}
        available=min(MAX_FILE,MAX_GROUP-total)
        if available<=0:entry["status"]="skipped_size_limit"
        else:
            for attempt in (1,2):
                try:
                    result=fetch(url,dest,available)
                    if dest.suffix==".zip" and not zipfile.is_zipfile(dest):raise ValueError("not a ZIP")
                    if dest.suffix==".pdf" and dest.open("rb").read(5)!=b"%PDF-":raise ValueError("not a PDF")
                    entry.update(result)
                    entry["inspection"]=analyze(dest)
                    entry["path"]=str(dest.relative_to(folder))
                    entry["status"]="downloaded"
                    total+=result["bytes"]
                    break
                except Exception as exc:
                    dest.unlink(missing_ok=True)
                    entry["status"]="failed"
                    entry["error"]=f"{type(exc).__name__}: {str(exc)[:250]}"
                    if attempt==1:time.sleep(1)
        items.append(entry)
        print(f"{name}: {entry['status']} {entry.get('bytes',0)} bytes",flush=True)
    report={"group":group,"date_utc":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),"total_downloaded_bytes":total,"notes":"No binary was executed; proprietary archives are not included; source/license still requires review","items":items}
    (folder/"MANIFEST.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
    lines=[f"# Research run: {group}","","| Resource | Status | Bytes | SHA256 |","|---|---|---:|---|"]
    for i in items:
        lines.append(f"| {i['name']} | {i['status']} | {i.get('bytes',0)} | {i.get('sha256','—')} |")
        if i.get("error"): lines.append(f"\n- **{i['name']} failure:** {i['error']}\n")
        if i.get("inspection",{}).get("signals_in_sample"):lines.append(f"\n- **{i['name']} sampled API signals:** {i['inspection']['signals_in_sample']}\n")
    lines+=["","**Sampling of source files only; no binaries executed, compatibility or performance measured.**"]
    report_md="\n".join(lines)+"\n";(folder/"REPORT.md").write_text(report_md)
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"],"a") as f:f.write(report_md)
if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 and sys.argv[1] in SOURCES else "emulators")
