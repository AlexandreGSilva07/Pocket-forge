#!/usr/bin/env python3
"""Build an offline browser package from a PINNED MIT-licensed JS2ME source revision.

No network calls occur when the resulting browser package runs.
Source is downloaded at BUILD time only (unless --source is provided).
Never include copyrighted sample JARs in the distributable.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import shutil
import tempfile
import urllib.request
import zipfile
from pathlib import Path

UPSTREAM_REPO = "szatkus/js2me"
REVISION = "828b81b468953c34bb754b59e67c1021754e8bdb"
ARCHIVE = f"https://codeload.github.com/{UPSTREAM_REPO}/zip/{REVISION}"
MAX_ARCHIVE_BYTES = 20 * 1024 * 1024
MAX_EXTRACTED_BYTES = 60 * 1024 * 1024
ROOT = Path(__file__).resolve().parents[1]


def download_archive(destination: Path) -> str:
    request = urllib.request.Request(ARCHIVE, headers={
        "User-Agent": "PocketForge-J2ME/0.1 (pinned open-source research)",
        "Accept": "application/zip",
    })
    digest = hashlib.sha256()
    received = 0
    with urllib.request.urlopen(request, timeout=65) as src, destination.open("wb") as out:
        while True:
            chunk = src.read(262144)
            if not chunk:
                break
            received += len(chunk)
            if received > MAX_ARCHIVE_BYTES:
                raise ValueError("upstream archive exceeds safety cap")
            digest.update(chunk)
            out.write(chunk)
    return digest.hexdigest()


def safely_extract(archive: Path, dest: Path) -> Path:
    total = 0
    with zipfile.ZipFile(archive) as z:
        members = z.infolist()
        for entry in members:
            if entry.is_dir():
                continue
            name = Path(entry.filename)
            if name.is_absolute() or ".." in name.parts:
                raise ValueError("unsafe ZIP member path")
            total += entry.file_size
            if total > MAX_EXTRACTED_BYTES:
                raise ValueError("upstream extracted content exceeds cap")
        z.extractall(dest)
    roots = [p for p in dest.iterdir() if p.is_dir()]
    if len(roots) != 1:
        raise ValueError("unexpected upstream root directory")
    return roots[0]


def assemble(source: Path, output: Path, archive_sha256: str | None) -> dict:
    if not (source / "LICENSE").is_file() or "MIT License" not in (source / "LICENSE").read_text(errors="replace"):
        raise ValueError("upstream MIT license missing or changed: abort build")
    for key in ["index.html", "js/js2me.js", "js/loader.js", "js/program_zazu.js",
                "js/zip/zip.js", "js/zip/inflate.js", "js/zip/zip-ext.js", "css/emulator.css"]:
        if not (source / key).is_file():
            raise FileNotFoundError(f"upstream layout changed: {key}")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    for folder in ("js", "css", "img"):
        shutil.copytree(source / folder, output / folder)
    # Two standard Java ME API gaps observed by runtime probes (not game hacks):
    # StringBuffer.append(char[], offset, length) and Player.getMediaTime().
    standard_api_patches = {
        "js/me/java/lang/StringBuffer.js": """\t$append$_CII$Ljava_lang_StringBuffer_: function(chars, offset, count) {
        if(chars == null) throw new javaRoot.$java.$lang.$NullPointerException();
        if(offset < 0 || count < 0 || offset > chars.length - count)
            throw new javaRoot.$java.$lang.$IndexOutOfBoundsException();
        for(var k=0;k<count;k++) this.string += String.fromCharCode(chars[offset+k] & 65535);
        return this;
    },
    """,
        "js/me/javax/microedition/media/PlayerImpl.js": """\t$getMediaTime$J: function() {
        var sec=this.element && Number(this.element.currentTime);
        var micro=Number.isFinite(sec) && sec>0 ? Math.floor(sec*1000000) : 0;
        return {hi:Math.floor(micro/4294967296)|0,lo:(micro%4294967296)>>>0};
    },
    """,
    }
    for rel, patch in standard_api_patches.items():
        file=output / rel
        raw=file.read_text(encoding="utf-8")
        if not raw.startswith("js2me.createClass({"):
            raise ValueError("JS2ME API definition changed: "+rel)
        file.write_text(raw.replace("js2me.createClass({", "js2me.createClass({"+chr(10)+patch,1),encoding="utf-8")
    # Fix a generic JVM-wide-bytecode defect in old upstream Zazu interpreter.
    # The original function lacked the context argument, used context.push/pop
    # instead of context.stack and threw unconditionally after every supported op.
    # This is a runtime-wide fix, not a patch to any commercial game.
    zazu_path = output / "js" / "program_zazu.js"
    zazu = zazu_path.read_text(encoding="utf-8")
    start = zazu.index("executors[0xc4] = function () {")
    end = zazu.index("js2me.generateProgram = function (data) {", start)
    patch = """executors[0xc4] = function (context) {
        var p = context.parameters[context.position - 1];
        var op = p.op, i = p.pointer;
        if (op >= 0x15 && op <= 0x19) {
            context.stack.push(context.locals[i]);
            return;
        }
        if (op >= 0x36 && op <= 0x3a) {
            context.locals[i] = context.stack.pop();
            return;
        }
        if (op === 0x84) {
            context.locals[i] = (context.locals[i] + p.value) | 0;
            return;
        }
        throw new Error("unsupported wide opcode: " + op);
    };
    """
    zazu_path.write_text(zazu[:start] + patch + chr(10) + chr(9) + zazu[end:], encoding="utf-8")
    # Replace generic TypeError on unresolved call sites with an exact class
    # and method signature. This fixes diagnostics without inventing behavior.
    replacements = {
        "obj[methodInfo.name].apply(obj, args)": "js2me.safeInvoke(obj[methodInfo.name], obj, args, methodInfo)",
        "classObj.prototype[methodInfo.name].apply(classObj.prototype, args)": "js2me.safeInvoke(classObj.prototype[methodInfo.name], classObj.prototype, args, methodInfo)",
        "classObj.prototype[methodInfo.name].apply(obj, args)": "js2me.safeInvoke(classObj.prototype[methodInfo.name], obj, args, methodInfo)",
    }
    for name in ("program_zazu.js", "program_pumba.js"):
        file = output / "js" / name
        code = file.read_text(encoding="utf-8")
        for before, after in replacements.items():
            if before not in code:
                raise ValueError(name + " upstream call layout changed: " + before)
            code = code.replace(before, after)
        file.write_text(code, encoding="utf-8")
    original = (source / "index.html").read_text(encoding="utf-8")
    original = original.replace('<script type="text/javascript" src="js/emulator.js"></script>',
        '<script type="text/javascript" src="js/emulator.js"></script>\n'
        '<script>js2me.config.selector=true;js2me.config.workers=false;</script>')
    original = original.replace("</head>",
        '<script defer src="pocketforge-bridge.js"></script>\n'
        '<link rel="stylesheet" href="pocketforge-style.css">\n</head>', 1)
    if "pocketforge-bridge.js" not in original or "config.selector=true" not in original:
        raise ValueError("could not adapt upstream HTML entry")
    (output / "index.html").write_text(original, encoding="utf-8")
    shutil.copy2(ROOT / "runtime" / "j2me-bridge.js", output / "pocketforge-bridge.js")
    shutil.copy2(ROOT / "runtime" / "j2me-style.css", output / "pocketforge-style.css")
    shutil.copy2(source / "LICENSE", output / "LICENSE-js2me-MIT.txt")
    (output / "LICENSE-PocketForge.txt").write_text(
        "PocketForge adapter: MIT, see https://github.com/AlexandreGSilva07/Pocket-forge/blob/main/LICENSE\n")
    manifest = {
        "name": "PocketForge J2ME Offline Runtime — experimental",
        "upstream": "https://github.com/" + UPSTREAM_REPO,
        "upstream_commit": REVISION,
        "upstream_archive_sha256": archive_sha256,
        "license": "JS2ME MIT; bundled zip.js sources carry BSD-style notices retained within js/zip/",
        "built_from": "MIT upstream, locally packaged; no runtime dependency on a CDN or JVM",
        "status": "partial MIDP/CLDC compatibility — individual games not guaranteed",
        "installed_games": 0,
        "usage": "Serve this folder with python3 -m http.server 8000, then select a JAR",
    }
    (output / "build-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (output / "README.txt").write_text(
        "PocketForge J2ME Offline Runtime (experimental)\n"
        "Run: python3 -m http.server 8000 --directory dist/j2me-web\n"
        "Open: http://localhost:8000\n"
        "Drop/select a legally obtained JAR; it stays on your machine.\n"
        "Offline means no external network or installed Java required AFTER packaging.\n"
        "Coverage is partial: unsupported MIDP/CLDC/JSRs are expected.\n"
        "For historical/proprietary games use your own legitimate copies.\n", encoding="utf-8")
    return manifest


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--source", type=Path, help="Existing checkout of pinned JS2ME revision (no network)")
    p.add_argument("--output", type=Path, default=ROOT / "dist" / "j2me-web")
    p.add_argument("--ci-fixture", action="store_true", help="Copy upstream demo test.jar for ephemeral smoke (remove before distribution)")
    args = p.parse_args()
    if args.source:
        manifest = assemble(args.source.resolve(), args.output, None)
        if args.ci_fixture:
            (args.output / "ci").mkdir(exist_ok=True)
            shutil.copy2(args.source.resolve() / "jars" / "test.jar", args.output / "ci" / "test.jar")
    else:
        with tempfile.TemporaryDirectory() as td:
            temp = Path(td)
            sha = download_archive(temp / "js2me.zip")
            source = safely_extract(temp / "js2me.zip", temp / "source")
            manifest = assemble(source, args.output, sha)
            if args.ci_fixture:
                (args.output / "ci").mkdir(exist_ok=True)
                shutil.copy2(source / "jars" / "test.jar", args.output / "ci" / "test.jar")
    print(json.dumps({"output": str(args.output), **manifest}, indent=2))


if __name__ == "__main__":
    main()
