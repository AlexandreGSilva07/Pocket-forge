#!/usr/bin/env python3
"""Bundle the already-built JS2ME offline runtime into ONE standalone file:// HTML.

All JavaScript engines, native Java ME classes, CSS and image resources are embedded.
No server, CDN or Java installation is required to open the output; JAR import is local.
Upstream JS2ME MIT and zip.js BSD licenses are retained in HTML comments.
"""
from __future__ import annotations
import argparse
import base64
import json
import mimetypes
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUNTIME = ROOT / "dist" / "j2me-web"
DEFAULT_OUTPUT = ROOT / "dist" / "PocketForge-J2ME-Offline.html"
JS_TAG = re.compile(r'<script\b[^>]*\bsrc=["\']([^"\']+)["\'][^>]*>\s*</script>', re.I)
CSS_TAG = re.compile(r'<link\b[^>]*\brel=["\']stylesheet["\'][^>]*\bhref=["\']([^"\']+)["\'][^>]*>', re.I)
ASSET_URL = re.compile(r'url\(\s*(["\']?)([^"\')]+)\1\s*\)', re.I)
TAG_END = re.compile(r'</script', re.I)


def safe_inline_js(source: str) -> str:
    return TAG_END.sub(r'<\\/script', source)


def relative_path(root: Path, rel: str) -> Path:
    if "://" in rel or rel.startswith(("/", "\\")):
        raise ValueError(f"External/absolute resource is forbidden: {rel}")
    base = root.resolve()
    resolved = (root / rel).resolve()
    if resolved != base and base not in resolved.parents:
        raise ValueError(f"Resource escaped bundle: {rel}")
    if not resolved.is_file():
        raise FileNotFoundError(resolved)
    return resolved


def css_inline_assets(css_path: Path, css: str) -> str:
    def replace(match: re.Match) -> str:
        raw = match.group(2)
        if raw.startswith(("data:", "#")):
            return match.group(0)
        path = relative_path(css_path.parent, raw.split("?")[0])
        mime = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        payload = base64.b64encode(path.read_bytes()).decode("ascii")
        return 'url("data:' + mime + ';base64,' + payload + '")'
    return ASSET_URL.sub(replace, css)


def build(runtime: Path, output: Path, embed_jar: Path | None = None) -> dict:
    html = relative_path(runtime, "index.html").read_text("utf8")
    native = {}
    for path in sorted((runtime / "js" / "me").rglob("*.js")):
        native[path.relative_to(runtime).as_posix()] = path.read_text("utf8")
    for path in sorted((runtime / "js").glob("program_*.js")):
        native[path.relative_to(runtime).as_posix()] = path.read_text("utf8")

    bridge = relative_path(runtime, "pocketforge-bridge.js").read_text("utf8")
    # The legacy class-loader calls js2me.loadScript(path, success, failure)
    # for native classes and selects its interpreter/JIT dynamically.
    # Execute embedded code in the same global scope as the upstream scripts.
    shim = """(function () {
      'use strict';
      const modules = """ + json.dumps(native, ensure_ascii=True, separators=(",", ":")) + """;
      const compiled = Object.create(null);
      const originalLoadScript = js2me.loadScript;
      js2me.loadScript = function(path, success, failure) {
        try {
          if (!Object.prototype.hasOwnProperty.call(modules, path)) {
            const error = new Error('Module not embedded: '+path);
            if (typeof failure === 'function') {failure(error);return;}
            throw error;
          }
          // JS2ME native class modules populate js2me.classBucket on evaluation;
          // always re-evaluate, because classBucket belongs to the current VM.
          const source = modules[path];
          let run = compiled[path];
          if (!run) run = compiled[path] = new Function(source + '\\n//# sourceURL=pocketforge:///' + path);
          run.call(window);
          if (typeof success === 'function') success();
        } catch (e) {
          console.error('[PocketForge embedded module]', path, e);
          if (typeof failure === 'function') failure(e); else throw e;
        }
      };
      window.PocketForgeBundleInfo = Object.freeze({
        singleFile:true, modules:Object.keys(modules).length, offline:true
      });
    })();"""

    def script_replace(m: re.Match) -> str:
        name = m.group(1)
        if name == "pocketforge-bridge.js":
            return "<script>\n" + safe_inline_js(shim) + "\n</script>\n<script>\n" + safe_inline_js(bridge) + "\n</script>"
        source = relative_path(runtime, name).read_text("utf8")
        return "<script>\n" + safe_inline_js(source) + "\n</script>"
    html, script_count = JS_TAG.subn(script_replace, html)
    if script_count < 15 or 'pocketforge-bridge.js' in html or '<script src=' in html:
        raise ValueError(f"missing script dependency: {script_count} scripts replaced")

    def css_replace(m: re.Match) -> str:
        path = relative_path(runtime, m.group(1))
        css = css_inline_assets(path, path.read_text("utf8"))
        return '<style>\n' + css + '\n</style>'
    html, css_count = CSS_TAG.subn(css_replace, html)
    if css_count < 3:
        raise ValueError(f"Only {css_count} CSS files embedded")

    # Legacy homepage has an image arrow which is hidden after load; still embed it.
    def image_replace(m: re.Match) -> str:
        src = m.group(1)
        if src.startswith("data:"):
            return m.group(0)
        path = relative_path(runtime, src)
        mime = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        uri = "data:" + mime + ";base64," + base64.b64encode(path.read_bytes()).decode("ascii")
        return m.group(0).replace(src, uri)
    html = re.sub(r'<img\b[^>]*src=["\']([^"\']+)["\'][^>]*>', image_replace, html, flags=re.I)

    license_js2me = relative_path(runtime, "LICENSE-js2me-MIT.txt").read_text("utf8")
    zip_lic = (runtime / "js" / "zip" / "zip.js").read_text("utf8")[:1200]
    attribution = ('\n<!-- JS2ME original MIT LICENSE\n' + license_js2me
                    + '\n\nBundled zip.js file retains its original headers. Header excerpt:\n'
                    + zip_lic.replace("-->", "-- >") + '\n-->\n')
    html = '<!doctype html>\n' + attribution + html
    html = html.replace("<title>JS2ME</title>", "<title>PocketForge J2ME — arquivo único offline</title>", 1)
    single_style = (ROOT / "runtime" / "j2me-onefile-style.css").read_text("utf8")
    html = html.replace('</head>',
         '<meta name="pocketforge-single-file" content="offline, no server, MIT JS2ME">\n'
         '<style>\n' + single_style + '\n</style>\n</head>',1)
    if any(re.search(pattern, html, re.I) for pattern in (
        r'<script[^>]*\bsrc=', r'<link[^>]*\bhref=', r'<img[^>]*\bsrc=["\'](?!data:)')):
        raise ValueError("unbundled browser resources detected")
    if embed_jar is not None:
        if not embed_jar.is_file() or not zipfile.is_zipfile(embed_jar):
            raise ValueError("Embedded game must be a valid local JAR/ZIP")
        if embed_jar.stat().st_size > 64 * 1024 * 1024:
            raise ValueError("Embedded JAR must be <= 64 MiB")
        # This output is PRIVATE and intentionally carries game bytes.
        # NEVER publish copyrighted game JARs or generated HTML to a public Git repository.
        raw = base64.b64encode(embed_jar.read_bytes()).decode("ascii")
        javascript = """
window.addEventListener("load", function(){
  if (!window.PocketForgeJ2ME) { console.error("PocketForge bridge unavailable"); return; }
  var encoded = """ + json.dumps(raw) + """;
  var text = atob(encoded), data = new Uint8Array(text.length);
  for (var i=0;i<text.length;i++) data[i]=text.charCodeAt(i);
  var name = """ + json.dumps(embed_jar.name) + """;
  window.PocketForgeJ2ME.load(new File([data], name, {type:"application/java-archive"}));
});
"""
        if "</body>" not in html:raise ValueError("Missing closing HTML body")
        html=html.replace("</body>","<script>\n"+safe_inline_js(javascript)+"\n</script>\n</body>",1)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf8")
    return {"output":str(output),"bytes":output.stat().st_size,
            "embedded_jar":embed_jar.name if embed_jar else None,
            "javascript_scripts_inlined":script_count,"stylesheets_inlined":css_count,
            "java_me_native_modules_embedded":len(native),
            "browser_runtime_network_dependencies":0,
            "java_required_for_execution":False}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--runtime",type=Path,default=DEFAULT_RUNTIME)
    p.add_argument("--output",type=Path,default=DEFAULT_OUTPUT)
    p.add_argument("--jar",type=Path,help="PRIVATE game JAR to embed and auto-launch in the single HTML")
    args=p.parse_args()
    print(json.dumps(build(args.runtime.resolve(),args.output.resolve(),args.jar.resolve() if args.jar else None),indent=2))
if __name__=="__main__":
    main()
