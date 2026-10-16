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
            page.wait_for_function("document.querySelector(\'#dash\').classList.contains(\'cooling\')", timeout=3000)
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
            touch_page.wait_for_function("document.querySelector(\'#dash\').classList.contains(\'cooling\')", timeout=3000)
            touch_page.screenshot(path=str(SHOT_DIR / "mobile.png"))
            mobile.close()
            # Original test game for deep-research AI module.
            ai_page = browser.new_context(
                viewport={"width": 800, "height": 700}
            ).new_page()
            ai_page.on("pageerror", lambda error: errors.append(str(error)))
            ai_response = ai_page.goto(url + "ai-lab.html", wait_until="load")
            assert ai_response is not None and ai_response.status == 200
            assert ai_page.locator("#piles span").count() == 15
            assert "Sua vez" in ai_page.locator("#turn").inner_text()
            ai_page.locator("[data-take='1']").click()
            remaining = ai_page.locator("#piles span").count()
            assert 11 <= remaining <= 13, f"CPU did not play: {remaining}"
            assert "nós" in ai_page.locator("#stats").inner_text()
            ai_page.locator("#reset").click()
            assert ai_page.locator("#piles span").count() == 15
            ai_page.screenshot(path=str(SHOT_DIR / "ai-lab.png"))
            ai_page.context.close()
            pixel_context = browser.new_context(viewport={"width": 820, "height": 760})
            pixel_page = pixel_context.new_page()
            pixel_page.on("pageerror", lambda error: errors.append(str(error)))
            pixel_response = pixel_page.goto(url + "pixel-lab.html", wait_until="load")
            assert pixel_response is not None and pixel_response.status == 200
            pixel_page.wait_for_function(
                "document.querySelector('#info').textContent.includes('Framebuffer')",
                timeout=8000
            )
            assert pixel_page.locator("#lab").evaluate("(c) => c.width === 160 && c.height === 120")
            pixel_page.screenshot(path=str(SHOT_DIR / "pixel-lab.png"))
            pixel_context.close()
            tactics_ctx = browser.new_context(viewport={"width": 820, "height": 820})
            tactics_page = tactics_ctx.new_page()
            tactics_page.on("pageerror", lambda error: errors.append(str(error)))
            response = tactics_page.goto(url + "tactics-lab.html", wait_until="load")
            assert response is not None and response.status == 200
            assert tactics_page.locator(".cell").count() == 121
            tactics_page.locator(".cell[data-x='5'][data-y='5']").click()
            tactics_page.wait_for_function(
                "document.querySelectorAll('.cell.cpu').length === 1",timeout=10000
            )
            assert tactics_page.locator(".cell.you").count() == 1
            tactics_page.locator("#reset").click()
            assert tactics_page.locator(".cell.cpu").count() == 0
            assert tactics_page.locator(".cell.you").count() == 0
            tactics_page.screenshot(path=str(SHOT_DIR / "tactics-lab.png"))
            tactics_ctx.close()
            asset_ctx = browser.new_context(viewport={"width": 850, "height": 700})
            asset_page = asset_ctx.new_page()
            asset_page.on("pageerror", lambda error: errors.append(str(error)))
            asset_response = asset_page.goto(url + "assets-lab.html", wait_until="load")
            assert asset_response is not None and asset_response.status == 200
            asset_page.wait_for_function(
                "document.querySelector('#stats').textContent.includes('3 PNGs originais')",
                timeout=12000
            )
            asset_page.screenshot(path=str(SHOT_DIR / "assets-lab.png"))
            asset_ctx.close()
            browser.close()
    finally:
        server.shutdown()
        server.server_close()
    assert not errors, f"Erros JavaScript em runtime: {errors}"
    print("PASS: browser smoke desktop + touch; screenshots:", SHOT_DIR)


if __name__ == "__main__":
    run()
