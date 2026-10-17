#!/usr/bin/env python3
"""Chromium test of packaged JS2ME with an actual MIDlet JAR (upstream test fixture).
Test fixture is temporary and removed before upload of offline package.
"""
import functools
import http.server
import json
import os
from pathlib import Path
import threading
from playwright.sync_api import sync_playwright

BASE = Path(__file__).resolve().parents[1] / "dist" / "j2me-web"
SHOT = Path(os.environ.get("POCKETFORGE_SCREENSHOT_DIR", "/tmp/pocketforge-browser"))
def main():
    assert (BASE / "index.html").is_file(), "run build_j2me_runtime.py first"
    assert (BASE / "ci" / "test.jar").is_file(), "build using --ci-fixture"
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(BASE))
    server = http.server.ThreadingHTTPServer(("127.0.0.1",0), handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    errors = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width":1180,"height":800})
            page.on("pageerror", lambda e: errors.append(str(e)))
            r = page.goto(f"http://127.0.0.1:{server.server_port}/?selector=1",wait_until="load")
            assert r and r.status == 200
            page.wait_for_function("!!window.PocketForgeJ2ME && !!document.querySelector('#pf-jar-file')",timeout=10000)
            assert page.evaluate("PocketForgeJ2ME.offline") is True
            page.locator("#pf-jar-file").set_input_files(str(BASE / "ci" / "test.jar"))
            page.wait_for_function("!!window.js2me.manifest && !!window.js2me.manifest['midlet-1']",timeout=30000)
            page.wait_for_timeout(6000)
            data = page.evaluate("""() => ({
              manifest: window.js2me.manifest,
              runtime: window.PocketForgeJ2ME.diagnostics(),
              resourceCount: window.js2me.resources ? Object.keys(window.js2me.resources).length : 0,
              usedMethods: window.js2me.usedMethods ? Object.keys(window.js2me.usedMethods).length : 0,
              bytecodeExecutions:window.PocketForgeJ2ME.executionCount(),
              threadCount: window.js2me.threads ? window.js2me.threads.length : 0,
              currentScreen: document.querySelector('#screen').textContent.slice(0,500),
              canvasCount: document.querySelectorAll('canvas').length
            })""")
            SHOT.mkdir(parents=True,exist_ok=True)
            (SHOT/"j2me-test-diagnostic.json").write_text(json.dumps({
                "browserErrors": errors, "observations":data
            },indent=2))
            page.screenshot(path=str(SHOT/"j2me-test.png"),full_page=True)
            assert data["manifest"].get("midlet-1"), "MIDlet entrypoint not recognized"
            assert data["resourceCount"] > 0, "JAR resources not loaded"
            assert data["bytecodeExecutions"] > 0, "No actual Java bytecode was interpreted"
            print("PASS: real JAR loaded, manifest read, Java bytecode entered (not full compatibility)")
            print(json.dumps({"resourceCount":data["resourceCount"],"usedMethods":data["usedMethods"],
                              "bytecodeExecutions":data["bytecodeExecutions"],"threadCount":data["threadCount"],"canvasCount":data["canvasCount"],
                              "browserErrors":errors,"events":data["runtime"][-8:]},ensure_ascii=False))
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
if __name__=="__main__":
    main()
