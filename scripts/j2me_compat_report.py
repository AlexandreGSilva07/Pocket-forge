#!/usr/bin/env python3
"""Deterministic J2ME constant-pool API dependency report. Does not decompile or execute.
Missing JS class files are evidence of *likely* gaps, not proof of a runtime failure.
Likewise a present stub is not proof it is implemented correctly.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import json
from pathlib import Path
import struct
import zipfile

EXTERNAL_ROOTS=("java/","javax/","com/nokia/","com/mascotcapsule/","com/siemens/","com/samsung/","com/sony_ericsson/")
def parse_class(b):
    if len(b)<10 or b[:4]!=b"\xca\xfe\xba\xbe": raise ValueError("invalid classfile")
    pos=4
    def u1():
        nonlocal pos
        if pos+1>len(b):raise ValueError("classfile truncated")
        n=b[pos];pos+=1;return n
    def u2():
        nonlocal pos
        if pos+2>len(b):raise ValueError("classfile truncated")
        n=struct.unpack_from(">H",b,pos)[0];pos+=2;return n
    def u4():
        nonlocal pos
        if pos+4>len(b):raise ValueError("classfile truncated")
        n=struct.unpack_from(">I",b,pos)[0];pos+=4;return n
    minor=u2(); major=u2()
    num=u2(); cp=[None]*num; i=1
    while i<num:
        tag=u1()
        if tag==1:
            length=u2()
            if pos+length>len(b):raise ValueError("truncated UTF8 pool")
            cp[i]=(tag,b[pos:pos+length].decode("utf-8","replace"));pos+=length
        elif tag in (3,4):pos+=4;cp[i]=(tag,None)
        elif tag in (5,6):pos+=8;cp[i]=(tag,None);i+=1
        elif tag in (7,8,16,19,20):cp[i]=(tag,u2())
        elif tag in (9,10,11,12,17,18):cp[i]=(tag,u2(),u2())
        elif tag==15:cp[i]=(tag,u1(),u2())
        else:raise ValueError("unsupported pool tag: "+str(tag))
        if pos>len(b):raise ValueError("truncated constant pool")
        i+=1
    def utf(j):
        return cp[j][1] if isinstance(j,int) and 0<j<num and cp[j] and cp[j][0]==1 else None
    def cls(j):
        return utf(cp[j][1]) if isinstance(j,int) and 0<j<num and cp[j] and cp[j][0]==7 else None
    names={cls(j) for j,v in enumerate(cp) if v and v[0]==7}
    refs=[]
    for v in cp:
        if not v or v[0] not in (9,10,11):continue
        owner=cls(v[1]);nt=cp[v[2]] if 0<v[2]<num else None
        if owner and nt and nt[0]==12:
            refs.append({"owner":owner,"member":utf(nt[1]),"descriptor":utf(nt[2]),
                         "kind":{9:"field",10:"method",11:"interface"}[v[0]]})
    return {"major":major,"classes":sorted(x for x in names if x),"members":refs}
def manifest_text(data):
    result={};last=None
    for row in data.decode("utf-8","replace").replace("\r\n","\n").split("\n"):
        if row.startswith(" ") and last:result[last]+=row[1:]
        elif ": " in row:last,value=row.split(": ",1);result[last]=value
    return result
def report(path,api_root=None):
    raw=path.read_bytes()
    if not zipfile.is_zipfile(path):raise ValueError("input not a valid JAR/ZIP")
    report={"file":path.name,"sha256":hashlib.sha256(raw).hexdigest(),
            "bytes":len(raw),"mode":"constant_pool_static_only","claims":{"original_executed":False,"coverage_proven":False}}
    declared=set(); classes=set(); calls=[];versions=collections.Counter();errors=[]
    with zipfile.ZipFile(path) as z:
        entries=z.namelist()
        report["jar_entry_count"]=len(entries)
        report["manifest"]=manifest_text(z.read("META-INF/MANIFEST.MF")) if "META-INF/MANIFEST.MF" in entries else {}
        for filename in entries:
            if not filename.endswith(".class"):continue
            if ".." in Path(filename).parts:continue
            declared.add(filename[:-6])
        for filename in entries:
            if not filename.endswith(".class"):continue
            try:
                info=parse_class(z.read(filename))
                classes.update(info["classes"]);calls+=info["members"];versions[info["major"]]+=1
            except Exception as exc:
                errors.append({"class":filename,"error":str(exc)[:130]})
    external=sorted(c for c in classes|{m["owner"] for m in calls}
                    if c.startswith(EXTERNAL_ROOTS) and c not in declared)
    groups=collections.defaultdict(list)
    for c in external:
        category=next((x.rstrip("/") for x in EXTERNAL_ROOTS if c.startswith(x)),"other")
        groups[category].append(c)
    report["classes_inside_jar"]=len(declared)
    report["java_classfile_major_versions"]=dict(versions)
    report["external_api_classes"]=external
    report["external_api_groups"]={k:{"count":len(v),"classes":v} for k,v in sorted(groups.items())}
    report["constant_pool_member_refs"]=len(calls)
    report["external_method_and_field_references"]=sorted(
      [x for x in calls if x["owner"] in external],
      key=lambda x:(x["owner"],x["member"] or "",x["descriptor"] or ""))
    report["parse_errors"]=errors
    if api_root:
        base=Path(api_root)
        available=sorted(c for c in external if (base/(c+".js")).is_file())
        missing=sorted(set(external)-set(available))
        report["js2me_static_api_presence"]={
            "api_root":str(base),"present_classes":available,"missing_classes":missing,
            "present":len(available),"missing":len(missing),
            "warning":"Filesystem presence ≠ runtime compatibility; no invocation verified"}
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("jar",type=Path)
    p.add_argument("--api-root",type=Path,help="built dist/j2me-web/js/me path")
    p.add_argument("--out",type=Path)
    a=p.parse_args();result=report(a.jar,a.api_root)
    data=json.dumps(result,ensure_ascii=False,indent=2)+"\n"
    if a.out:
        a.out.parent.mkdir(parents=True,exist_ok=True)
        a.out.write_text(data,encoding="utf-8")
    print(json.dumps({k:result[k] for k in ("file","sha256","classes_inside_jar",
            "java_classfile_major_versions","constant_pool_member_refs","parse_errors")},indent=2))
    if "js2me_static_api_presence" in result:
        status=result["js2me_static_api_presence"]
        print("API classes with JS2ME source:",status["present"],"Missing JS class files:",status["missing"])
        print("Missing examples:",status["missing_classes"][:30])
if __name__=="__main__":
    main()
