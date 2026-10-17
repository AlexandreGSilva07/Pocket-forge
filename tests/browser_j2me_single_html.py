#!/usr/bin/env python3
"""End-to-end file:// and offline test on a REAL installed Google Chrome.
No local server, no external requests, no JVM. Uses upstream's tiny test.jar.
"""
import argparse, hashlib, json, os
from pathlib import Path
from playwright.sync_api import sync_playwright

DEFAULT_HTML = Path(__file__).resolve().parents[1] / "dist" / "PocketForge-J2ME-Offline.html"
def test(html:Path,jar:Path | None,screenshot:Path):
    observed={"html":str(html),"jar":str(jar) if jar else "(embedded)","browser":"Google Chrome / Chromium",
              "protocol":"file://","external_network_requests":[],"page_errors":[],"console_errors":[]}
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True,executable_path="/usr/bin/google-chrome" if Path("/usr/bin/google-chrome").exists() else None)
        page=browser.new_page(viewport={"width":1280,"height":980})
        def on_request(request):
            if not request.url.startswith(("file:","data:","blob:")):
                observed["external_network_requests"].append(request.url)
        page.on("request",on_request)
        page.on("pageerror",lambda exc: observed["page_errors"].append(str(exc)))
        page.on("console",lambda msg:observed["console_errors"].append(msg.text[:300]) if msg.type=="error" else None)
        response=page.goto(html.as_uri(),wait_until="load",timeout=30000)
        page.wait_for_function("!!window.PocketForgeJ2ME && !!window.PocketForgeBundleInfo",timeout=16000)
        observed["embedded_modules"]=page.evaluate("window.PocketForgeBundleInfo.modules")
        observed["status_initial"]=page.locator("#pf-status").inner_text()
        if jar: page.locator("#pf-jar-file").set_input_files(str(jar))
        page.wait_for_timeout(9000)
        observed.update(page.evaluate("""() => ({
          manifest: window.js2me.manifest || null,
          bytecodeExecutions: window.PocketForgeJ2ME.executionCount(),
          canvas: [...document.querySelectorAll('canvas')].map(c=>({width:c.width,height:c.height})),
          resources:window.js2me.resources?Object.keys(window.js2me.resources).length:0,
          runtimeEvents:window.PocketForgeJ2ME.diagnostics().slice(-15),
          status:document.querySelector('#pf-status').textContent
        })"""))
        screenshot.parent.mkdir(parents=True,exist_ok=True)
        page.screenshot(path=str(screenshot),full_page=True)
        observed["screenshot_sha256"]=hashlib.sha256(screenshot.read_bytes()).hexdigest()
        browser.close()
    return observed

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--html",type=Path,default=DEFAULT_HTML)
    p.add_argument("--jar",type=Path,help="JAR to import; omit for self-running HTML with JAR embedded")
    p.add_argument("--screenshot",type=Path,default=Path("/home/alexandre/.cache/pocketforge-tests/offline-test.png"))
    p.add_argument("--report",type=Path,default=Path("/home/alexandre/.cache/pocketforge-tests/offline-test.json"))
    a=p.parse_args()
    result=test(a.html.resolve(),a.jar.resolve() if a.jar else None,a.screenshot.resolve())
    a.report.parent.mkdir(parents=True,exist_ok=True)
    a.report.write_text(json.dumps(result,indent=2,ensure_ascii=False))
    print(json.dumps(result,indent=2,ensure_ascii=False)[:6500])
    assert not result["external_network_requests"],"External network was requested"
    assert result["manifest"] and result["manifest"].get("midlet-1"),"JAR manifest wasn't loaded"
    assert result["bytecodeExecutions"]>0,"No Java bytecode was executed"
    print("PASS: file:// single HTML executed real JAR bytecode with no local server")
if __name__=="__main__":main()
