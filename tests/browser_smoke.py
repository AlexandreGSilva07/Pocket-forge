#!/usr/bin/env python3
"""Smoke de navegador real; requer playwright + chromium instalados (dev/CI)."""
import functools
import http.server
import os
from pathlib import Path
import threading

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
GAME_DIR = ROOT / "demo"
SHOT_DIR = Path(os.environ.get("POCKETFORGE_SCREENSHOT_DIR", "/tmp/pocketforge-browser"))


def run():
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(GAME_DIR))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    url = f"http://127.0.0.1:{server.server_port}/"
    SHOT_DIR.mkdir(parents=True, exist_ok=True)
    errors = []
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            desktop = browser.new_context(viewport={"width": 1366, "height": 768}, device_scale_factor=1)
            page = desktop.new_page()
            page.on("pageerror", lambda error: errors.append(str(error)))
            response = page.goto(url, wait_until="load")
            assert response is not None and response.status == 200, "HTTP 200 esperado"
            assert page.locator("#centerOverlay").is_visible(), "Menu inicial não visível"
            assert page.locator("#game").evaluate("(c) => c.width > 0 && c.height > 0"), "Canvas sem tamanho"
            page.locator("#primaryButton").click()
            assert not page.locator("#centerOverlay").is_visible(), "Jogo não entrou em playing"
            page.keyboard.down("ArrowRight")
            page.wait_for_timeout(450)
            page.keyboard.up("ArrowRight")
            page.wait_for_function("Number(document.querySelector('#score').textContent) > 5", timeout=8000)
            page.keyboard.press("p")
            assert page.locator("#centerOverlay").is_visible(), "Pausa não abriu overlay"
            assert "pausa" in page.locator("#overlayTitle").inner_text().lower()
            page.locator("#primaryButton").click()
            assert not page.locator("#centerOverlay").is_visible(), "Retomar não voltou ao jogo"
            page.locator("#dash").click()
            assert "cooling" in (page.locator("#dash").get_attribute("class") or ""), "Dash não iniciou recarga"
            page.screenshot(path=str(SHOT_DIR / "desktop.png"))
            desktop.close()

            mobile = browser.new_context(
                viewport={"width": 390, "height": 844},
                device_scale_factor=2, is_mobile=True, has_touch=True
            )
            touch_page = mobile.new_page()
            touch_page.on("pageerror", lambda error: errors.append(str(error)))
            touch_page.goto(url, wait_until="load")
            touch_page.locator("#primaryButton").tap()
            assert not touch_page.locator("#centerOverlay").is_visible(), "Touch não iniciou jogo"
            touch_page.locator("#dash").tap()
            assert "cooling" in (touch_page.locator("#dash").get_attribute("class") or ""), "Dash touch não funcionou"
            touch_page.screenshot(path=str(SHOT_DIR / "mobile.png"))
            mobile.close()
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    assert not errors, f"Erros JavaScript em runtime: {errors}"
    print("PASS: browser smoke desktop + touch; screenshots:", SHOT_DIR)


if __name__ == "__main__":
    run()
