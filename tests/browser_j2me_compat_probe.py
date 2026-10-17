#!/usr/bin/env python3
"""Compatibility probe for user-selected commercial JAR, never a distribution step.

Observes deterministic startup, missing APIs and errors. Failure to run the game
is a reported compatibility gap; never mark a game as supported from manifest only.
"""
import argparse,functools,http.server,json,threading
from pathlib import Path
from playwright.sync_api import sync_playwright
BASE=Path(__file__).resolve().parents[1]/"dist"/"j2me-web"
def main():
    p=argparse.ArgumentParser()
    p.add_argument("jar",type=Path)
    p.add_argument("--out",type=Path,default=Path("artifacts/j2me-asphalt-probe.json"))
    p.add_argument("--engine",choices=("zazu","pumba","timon"),default="zazu")
    a=p.parse_args()
    if not a.jar.is_file():raise FileNotFoundError(a.jar)
    handler=functools.partial(http.server.SimpleHTTPRequestHandler,directory=str(BASE))
    server=http.server.ThreadingHTTPServer(("127.0.0.1",0),handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    report={"jar":a.jar.name,"bytes":a.jar.stat().st_size,"engine":a.engine,
            "stage":"not_started","bytecode_executions":0,
            "original_full_gameplay_verified":False,"limitations":[]}
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(headless=True)
            page=browser.new_page(viewport={"width":1180,"height":800})
            errors=[];console_errors=[]
            page.on("pageerror",lambda e:errors.append({"message":str(e),"stack":getattr(e,"stack",None)}))
            page.on("console",lambda msg:console_errors.append(msg.text[:300]) if msg.type=="error" else None)
            base=f"http://127.0.0.1:{server.server_port}"
            def intercept(route):
                if route.request.url.startswith(base+"/") or route.request.url.startswith("data:"):
                    route.continue_()
                else:
                    route.abort()
            page.route("**/*",intercept)
            response=page.goto(base+"/?selector=1&engine="+a.engine)
            assert response and response.status==200
            page.wait_for_function("!!window.PocketForgeJ2ME")
            page.locator("#pf-jar-file").set_input_files(str(a.jar))
            page.wait_for_timeout(12000)
            data=page.evaluate("""() => ({
             manifest: window.js2me.manifest || null,
             executions: window.PocketForgeJ2ME.executionCount(),
             events: window.PocketForgeJ2ME.diagnostics().slice(-80),
             resourceCount:window.js2me.resources ? Object.keys(window.js2me.resources).length : 0,
             canvasCount:document.querySelectorAll('canvas').length,
             currentScreen:document.querySelector('#screen').textContent.slice(0,300)
            })""")
            report.update({"manifest":data["manifest"],"bytecode_executions":data["executions"],
                "resource_count":data["resourceCount"],"canvas_count":data["canvasCount"],
                "error_count":len(errors),"javascript_errors":errors[:25],"console_errors":console_errors[:25],
                "event_log":data["events"],"screen_text":data["currentScreen"]})
            if not data["manifest"]:
                report["stage"]="jar_not_initialized"
            elif not data["executions"]:
                report["stage"]="manifest_only_no_bytecode"
            elif errors:
                report["stage"]="entered_bytecode_then_runtime_error"
            else:
                report["stage"]="entered_bytecode_no_page_error"
            report["limitations"]=["No original-to-browser pixel comparison",
                                   "No verified full game loop/race",
                                   "Manifest, canvas and methods do not prove gameplay"]
            browser.close()
    finally:
        server.shutdown();server.server_close()
        a.out.parent.mkdir(parents=True,exist_ok=True)
        a.out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print(json.dumps({k:report.get(k) for k in ("jar","stage","bytecode_executions","resource_count","canvas_count","error_count","javascript_errors")},ensure_ascii=False,indent=2))
if __name__=="__main__":main()
