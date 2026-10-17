#!/usr/bin/env python3
"""PocketForge AOT: compile an original JAR's Java bytecode to standalone HTML.

The compiler uses a pinned major-version TeaVM AOT backend and *generic* CLDC/MIDP
adapters. It NEVER executes the JAR's Java code during compilation or bundles
the original JAR into the resulting HTML. Unsupported APIs are explicit errors.
Requires Java 21+, Maven 3.9+ and network for first Maven dependency resolution.
The generated HTML needs only a browser; no local server, JRE, or external URL.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import shutil
from html import escape as html_escape
import subprocess
import tempfile
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "compiler" / "teavm-aot"
DEFAULT_MAVEN = Path(shutil.which("mvn") or (Path.home() / ".cache/pocketforge-toolchains/apache-maven-3.9.11/bin/mvn"))
JAVA_NAME = re.compile(r"^[a-zA-Z_$][\w$]*(\.[a-zA-Z_$][\w$]*)*$")
MAX_JAR = 32 * 1024 * 1024
MAX_JS = 12 * 1024 * 1024

def parse_manifest(raw: bytes) -> dict:
    # Continuation lines start with one literal space.
    result = {}
    last = None
    for line in raw.decode("utf8", errors="replace").replace("\r\n", "\n").split("\n"):
        if line.startswith(" ") and last:
            result[last] += line[1:]
        elif ": " in line:
            k, v = line.split(": ", 1)
            last = k.strip()
            result[k.strip()] = v.strip()
    return result

def entrypoint(manifest: dict) -> tuple[str, str]:
    if "MIDlet-1" in manifest:
        cls = manifest["MIDlet-1"].rsplit(",", 1)[-1].strip().replace("/", ".")
        kind = "midlet"
    elif "Main-Class" in manifest:
        cls = manifest["Main-Class"].strip().replace("/", ".")
        kind = "main"
    else:
        raise ValueError("JAR needs MIDlet-1 or Main-Class in MANIFEST.MF")
    if not JAVA_NAME.fullmatch(cls):
        raise ValueError("Unsupported entrypoint class name: " + repr(cls))
    return cls, kind

def compile_game(jar: Path, output: Path, maven: Path) -> dict:
    if not jar.is_file() or not zipfile.is_zipfile(jar):
        raise ValueError("Input must be an existing valid Java .jar")
    if jar.stat().st_size > MAX_JAR:
        raise ValueError("JAR exceeds 32 MiB")
    if not maven.is_file():
        raise FileNotFoundError("Maven missing at "+str(maven))
    with zipfile.ZipFile(jar) as z:
        names = z.namelist()
        if len(names)>12000 or sum(e.file_size for e in z.infolist())>160*1024*1024:
            raise ValueError("JAR expanded size or entry count exceeds compiler safety limits")
        manifest_name = next((x for x in names if x.upper()=="META-INF/MANIFEST.MF"), None)
        if not manifest_name:
            raise ValueError("Missing Java manifest")
        manifest = parse_manifest(z.read(manifest_name))
        cls, kind = entrypoint(manifest)
        class_names = [x for x in names if x.endswith(".class")]
        resources = [x for x in names if not x.endswith(".class") and not x.endswith("/") and not x.startswith("META-INF/")]
        if cls.replace(".","/")+".class" not in names:
            raise ValueError("Entrypoint class missing in JAR: "+cls)
    invoke = ("new "+cls+"().__pocketforgeStart();" if kind=="midlet"
              else cls+".main(new String[0]);")
    default_package = "." not in cls
    launcher_class = "Launcher" if default_package else "pocketforge.generated.Launcher"
    launcher = (("" if default_package else "package pocketforge.generated;\n")
                + "public final class Launcher {"
                + "public static void main(String[] args) {" + invoke + "}"
                + "}\n")
    report = {
        "input":str(jar), "sha256":hashlib.sha256(jar.read_bytes()).hexdigest(),
        "entrypoint":cls,"kind":kind,"launcher_package":"default" if "." not in cls else "generated","classes":len(class_names),
        "resource_files":len(resources),"resources_embedded":False,
        "translation":"TeaVM AOT, original game bytecode is not distributed",
        "known_limitations":["Incomplete MIDP/CLDC adapter coverage",
                             "Game resources are not yet linked",
                             "Threads and optional manufacturer JSRs not yet verified"]
    }
    with tempfile.TemporaryDirectory(prefix="pf_aot_") as td:
        work = Path(td)
        shutil.copytree(PROJECT / "src", work / "src")
        shutil.copy2(PROJECT / "pom.xml", work / "pom.xml")
        shutil.copy2(jar, work / "input.jar")
        source = work / "src/main/java" / ("Launcher.java" if default_package
                                    else "pocketforge/generated/Launcher.java")
        source.parent.mkdir(parents=True,exist_ok=True)
        if default_package:
            original=work / "src/main/java/pocketforge/generated/Launcher.java"
            original.unlink(missing_ok=True)
            pom=work / "pom.xml"
            pom.write_text(pom.read_text().replace(
                "<mainClass>pocketforge.generated.Launcher</mainClass>",
                "<mainClass>Launcher</mainClass>"),encoding="utf8")
        source.write_text(launcher,encoding="utf8")
        proc = subprocess.run([str(maven),"-B","-q","package"],
                              cwd=work, stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                              text=True, timeout=180)
        if proc.returncode:
            report["status"]="compile_error"
            report["compiler_error"]=proc.stdout[-7500:]
            report["missing_symbols"]=sorted(set(re.findall(
                r"(?m)^\[ERROR\] ((?:Class|Method|Field) [^\r\n]*? (?:not found|was not found))",
                proc.stdout)))
            output.parent.mkdir(parents=True,exist_ok=True)
            output.with_suffix(".compile.json").write_text(
                json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
            raise RuntimeError("Java ME compilation failed:\n"+proc.stdout[-7500:])
        compiled = work / "target/compiled-web/compiled.js"
        if not compiled.is_file():
            raise RuntimeError("TeaVM returned success but did not produce compiled JavaScript")
        code = compiled.read_text("utf8")
        if len(code.encode())>MAX_JS:
            raise ValueError("Generated script exceeds safety budget")
    # The HTML is intentionally a SINGLE FILE and has no reference to the JAR.
    code = code.replace("</script", "<\\/script")
    title = manifest.get("MIDlet-Name") or cls
    html = """<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>PocketForge AOT — """+html_escape(title)+"""</title>
<style>
:root{color-scheme:dark;font:14px system-ui;background:#0b1220;color:#e7eef7}
body{margin:0 auto;max-width:760px;padding:28px;text-align:center}
h1{font-size:21px}#game{display:grid;place-items:center;min-height:330px;
background:#122238;border:1px solid #36526d;border-radius:16px;padding:14px}
#game canvas{max-width:100%;height:auto}#log{color:#a9f0b9;background:#070e19;
text-align:left;border-radius:10px;padding:14px;white-space:pre-wrap;max-height:220px;overflow:auto}
p{color:#a2b8c9}a{color:#8bd5ee}
</style></head><body>
<h1>PocketForge · Compilação antecipada</h1>
<p>Java ME original convertido para JavaScript. Sem JAR, interpretador Java ou servidor.</p>
<div id="game"></div><pre id="log" aria-label="Saída do programa">Iniciando JavaScript compilado…\n</pre>
<script>
(function(){
 const output=document.getElementById('log');output.textContent='';
 for(const k of ['log','info','warn','error']){
  const orig=console[k];console[k]=function(...args){orig.apply(console,args);
    output.textContent+=args.map(x=>String(x)).join(' ')+'\\n';};
 }
 window.addEventListener('error',e=>{output.textContent+='ERROR '+e.message+'\\n';});
})();
</script>
<script>"""+code+"""</script>
<script>
try { if(typeof main !== 'function') throw Error('AOT main not exported');main(); }
catch(e){ console.error(e&&e.stack?e.stack:e); }
</script></body></html>
"""
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(html,encoding="utf8")
    report.update({"status":"compiled","output":str(output),
                   "html_bytes":output.stat().st_size,
                   "js_bytes":len(code.encode()),"jar_embedded":False,
                   "requires_java_at_runtime":False,"requires_http_server":False})
    receipt=output.with_suffix(".compile.json")
    receipt.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("jar",type=Path)
    p.add_argument("--out",type=Path)
    p.add_argument("--maven",type=Path,default=DEFAULT_MAVEN)
    a=p.parse_args()
    target=a.out or ROOT/"dist"/"aot"/(a.jar.stem+".html")
    result=compile_game(a.jar.resolve(),target.resolve(),a.maven.resolve())
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=="__main__":
    main()
