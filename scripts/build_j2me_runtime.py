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
    args = p.parse_args()
    if args.source:
        manifest = assemble(args.source.resolve(), args.output, None)
    else:
        with tempfile.TemporaryDirectory() as td:
            temp = Path(td)
            sha = download_archive(temp / "js2me.zip")
            source = safely_extract(temp / "js2me.zip", temp / "source")
            manifest = assemble(source, args.output, sha)
    print(json.dumps({"output": str(args.output), **manifest}, indent=2))


if __name__ == "__main__":
    main()
