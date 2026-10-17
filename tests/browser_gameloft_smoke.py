#!/usr/bin/env python3
"""Real Chromium smoke: local .jar -> native ZIP deflate -> Gameloft bank -> UI.
Uses only original synthetic test bytes, NEVER a commercial JAR.
"""
import functools
import http.server
import os
from pathlib import Path
import struct
import tempfile
import threading
import zipfile

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "demo"
OUT = Path(os.environ.get("POCKETFORGE_SCREENSHOT_DIR", "/tmp/pocketforge-browser"))

def run():
    # one valid resource tagged 2, DF05 magic; u16LE n=1, parts=1,
    # starts=[0], u32LE offsets=(14,18), payload=(2,DF,05,09)
    bank = struct.pack("<HBBHII", 1,1,0,0,14,18) + bytes([2,223,5,9])
    with tempfile.TemporaryDirectory() as td:
        jar=Path(td)/"minimal-game.jar"
        with zipfile.ZipFile(jar, "w", compression=zipfile.ZIP_DEFLATED) as z:
            z.writestr("6",bank)
        handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(DEMO))
        server=http.server.ThreadingHTTPServer(("127.0.0.1",0),handler)
        threading.Thread(target=server.serve_forever,daemon=True).start()
        errors=[]
        try:
            with sync_playwright() as p:
                browser=p.chromium.launch(headless=True)
                page=browser.new_page(viewport={"width":1100,"height":800})
                page.on("pageerror",lambda e: errors.append(str(e)))
                response=page.goto(f"http://127.0.0.1:{server.server_port}/gameloft-bank-lab.html")
                assert response is not None and response.status==200
                page.locator("#jar").set_input_files(str(jar))
                page.wait_for_function("document.querySelector('#status').textContent.includes('JAR carregado')")
                page.locator("#load").click()
                page.wait_for_function("document.querySelector('#status').textContent.includes('1 registros')")
                assert page.locator("#entries button").count()==1
                assert "gameloft_sprite" in page.locator("#entries button").first.inner_text()
                page.locator("#entries button").first.click()
                assert page.locator("#save").is_enabled()
                assert "df 05 09" in page.locator("#hex").inner_text().lower()
                OUT.mkdir(parents=True,exist_ok=True)
                page.screenshot(path=str(OUT/"gameloft-bank-lab.png"))
                browser.close()
        finally:
            server.shutdown();server.server_close()
        assert not errors, f"JS runtime errors: {errors}"
        print("PASS: Chromium imported deflated JAR in JavaScript, decoded bank and rendered inspector")

if __name__=="__main__": run()
