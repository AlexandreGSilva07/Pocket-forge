#!/usr/bin/env python3
"""Compile SIX independently authored Java JARs to standalone JS and test file:// in Chromium.

No game-specific compiler modifications and no JAR/runtime bytecode in the HTML.
This test proves the AOT pipeline for the exercised APIs; it does not imply
that unsupported MIDP, 3D, sound, networking and manufacturer JSRs will work.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/compile_j2me_aot.py"
SOURCES = ROOT / "tests/fixtures/aot"
SDK = ROOT / "compiler/teavm-aot/src/main/java"
TEAVM_JAR = Path.home()/".m2/repository/org/teavm/teavm-jso/0.16.0/teavm-jso-0.16.0.jar"
OUT=Path(os.environ.get("POCKETFORGE_AOT_EVIDENCE",str(ROOT/"artifacts/aot")))

def run(*args):
    proc=subprocess.run([str(a) for a in args],capture_output=True,text=True,timeout=180)
    if proc.returncode!=0:
        raise RuntimeError("FAILED "+str(args)+"\n"+proc.stdout[-2000:]+"\n"+proc.stderr[-4500:])
    return proc.stdout

def jar_with_manifest(location:Path, classes:Path, main: str, midlet: bool):
    from io import BytesIO
    mani=("Manifest-Version: 1.0\nMIDlet-Name: PocketForge AOT Test\n"
          + ("MIDlet-1: Test, , "+main+"\nMicroEdition-Configuration: CLDC-1.1\nMicroEdition-Profile: MIDP-2.0\n"
             if midlet else "Main-Class: "+main+"\n")+"\n")
    with zipfile.ZipFile(location,"w",zipfile.ZIP_DEFLATED) as z:
        z.writestr("META-INF/MANIFEST.MF",mani)
        for f in sorted((classes/"demo").rglob("*.class")):
            z.write(f,f.relative_to(classes).as_posix())

def build_fixture(root:Path,name:str):
    classes=root/name/"classes"
    classes.mkdir(parents=True)
    if name in ("Calculator","ResourceMain","ConnectorMain","RmsMain"):
        if name in ("ConnectorMain","RmsMain"):
            shimfiles=sorted((SDK/"javax").rglob("*.java"))+sorted((SDK/"pocketforge/media").rglob("*.java"))
            run("javac","--release","8","-cp",TEAVM_JAR,"-d",classes,*shimfiles,SOURCES/(name+".java"))
        else:
            run("javac","--release","8","-d",classes,SOURCES/(name+".java"))
        jar=root/name/(name+".jar")
        main="demo."+name
        jar_with_manifest(jar,classes,main,False)
        if name in ("ResourceMain","ConnectorMain"):
            with zipfile.ZipFile(jar,"a") as z:
                z.writestr("demo/hello.txt", (SOURCES/"hello.txt").read_bytes())
    else:
        if not TEAVM_JAR.is_file():
            raise RuntimeError("Run an AOT compilation first to download TeaVM dependencies")
        shims=sorted((SDK/"javax").rglob("*.java"))+sorted((SDK/"pocketforge/media").rglob("*.java"))
        class_name=(name+"MIDlet" if name in ("Interactive","ReferenceGraphics","Bitmap","Media","Adpcm","Midi","WideScreen") else "PocketDemoMIDlet")
        run("javac","--release","8","-cp",TEAVM_JAR,
            "-d",classes,*shims,SOURCES/(class_name+".java"))
        jar=root/name/(name+".jar")
        jar_with_manifest(jar,classes,"demo."+class_name,True)
        if name=="Midi":
            import struct
            # MIDI format 0: one note AOT rendered with a local SoundFont.
            events=bytes.fromhex("00 c0 00 00 90 3c 64 60 80 3c 00 00 ff 2f 00")
            song=b"MThd"+struct.pack(">IHHH",6,0,1,96)+b"MTrk"+struct.pack(">I",len(events))+events
            with zipfile.ZipFile(jar,"a") as z:z.writestr("demo/song.mid",song)
        if name=="Adpcm":
            import struct
            # WAV format 0x0011 (IMA DVI ADPCM), 8kHz mono, one block;
            # generated in the test, independent of proprietary game audio.
            block=bytes([0,0,0,0])+bytes([0x11]*8)
            fmt=struct.pack("<HHIIHHHH",17,1,8000,8000*len(block)//17,len(block),4,2,17)
            chunk=lambda tag,data:tag+struct.pack("<I",len(data))+data+(b"\0" if len(data)%2 else b"")
            body=b"WAVE"+chunk(b"fmt ",fmt)+chunk(b"fact",struct.pack("<I",17))+chunk(b"data",block)
            wav=b"RIFF"+struct.pack("<I",len(body))+body
            with zipfile.ZipFile(jar,"a") as z:z.writestr("demo/adpcm.wav",wav)
        if name=="Media":
            import wave,math,struct
            from io import BytesIO
            blob=BytesIO()
            with wave.open(blob,"wb") as wav:
                wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(8000)
                wav.writeframes(b"".join(struct.pack("<h",int(3500*math.sin(i*2*math.pi*440/8000))) for i in range(1600)))
            with zipfile.ZipFile(jar,"a") as z:z.writestr("demo/beep.wav",blob.getvalue())
        if name=="Bitmap":
            from PIL import Image as PILImage
            from io import BytesIO
            im=PILImage.new("RGBA",(2,2))
            im.putdata([(255,0,0,255),(0,255,0,255),(255,255,0,255),(0,0,255,255)])
            blob=BytesIO();im.save(blob,format="PNG")
            with zipfile.ZipFile(jar,"a") as z:
                z.writestr("demo/bitmap.png",blob.getvalue())
    return jar

def main():
    from playwright.sync_api import sync_playwright
    evidence={}
    OUT.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="pocketforge_aot_browser_") as td:
        t=Path(td)
        fixtures={}
        for name in ("Calculator","ResourceMain","PocketDemo","Interactive","ReferenceGraphics","Bitmap","ConnectorMain","RmsMain","Media","Adpcm","Midi","WideScreen"):
            if name=="PocketDemo" and not TEAVM_JAR.exists():
                raise RuntimeError("TeaVM 0.16.0 JSO jar is required (resolved by Maven)")
            jar=build_fixture(t,name)
            html=t/(name+".html")
            stdout=run(sys.executable,SCRIPT,jar,"--out",html,*( ["--screen","320x240"] if name=="WideScreen" else []))
            report=json.loads(stdout)
            assert report["status"]=="compiled"
            assert report["jar_embedded"] is False
            assert report["requires_java_at_runtime"] is False
            assert report["requires_http_server"] is False
            assert "<script src=" not in html.read_text()
            print("AOT_FIXTURE",name,html.stat().st_size,flush=True)
            assert html.stat().st_size<1000000,"AOT output unexpectedly large for fixtures"
            fixtures[name]=(jar,html,report)
        with sync_playwright() as p:
            executable="/usr/bin/google-chrome" if Path("/usr/bin/google-chrome").is_file() else None
            browser=p.chromium.launch(headless=True,executable_path=executable)
            for name,(jar,html,report) in fixtures.items():
                page=browser.new_page(viewport={"width":900,"height":800})
                errors=[];network=[]
                page.on("pageerror",lambda e:errors.append(str(e)))
                page.on("request",lambda r:network.append(r.url) if r.url.startswith(("http:","https:")) else None)
                page.goto(html.resolve().as_uri(),wait_until="load",timeout=30000)
                page.wait_for_timeout(350)
                output=page.locator("#log").inner_text()
                canvas=page.evaluate("""() => {
                  const c=document.getElementById('pf-screen');
                  if(!c)return null;
                  const pixels=c.getContext('2d').getImageData(0,0,c.width,c.height).data;
                  let nonblack=0,colors=new Set();
                  for(let i=0;i<pixels.length;i+=4){
                    const rgb=pixels[i]*65536+pixels[i+1]*256+pixels[i+2];
                    if(rgb)nonblack++;colors.add(rgb);
                  }
                  return {width:c.width,height:c.height,nonblack,colors:colors.size};
                }""")
                pixels_check=None
                if name=="RmsMain":
                    assert "RMS_BEFORE=0 RMS_AFTER=1" in output,output
                    for _ in range(2):
                        page.reload();page.wait_for_timeout(250)
                        output=page.locator('#log').inner_text()
                        assert "RMS_BEFORE=1 RMS_AFTER=1" in output,output
                    page.evaluate("console.log('X'.repeat(60000))")
                    assert page.evaluate("document.querySelector('#log').textContent.length")<=40000
                    output=page.locator('#log').inner_text()
                if name=="WideScreen":
                    assert "SCREEN_320x240_PASS" in output,output
                    assert canvas and canvas['width']==320 and canvas['height']==240,canvas
                    edge=page.evaluate("Array.from(document.querySelector('#pf-screen').getContext('2d').getImageData(300,220,1,1).data)")
                    assert edge==[255,217,102,255],edge
                if name=="ReferenceGraphics":
                    assert "PHONE_ME_GRAPHICS_CONTRACT_PASS" in output,output
                    pixels_check=page.evaluate("""() => {const g=document.getElementById('pf-screen').getContext('2d');const pixel=(x,y)=>Array.from(g.getImageData(x,y,1,1).data);return {green:pixel(21,23),clipped:pixel(18,18),red:pixel(30,30),cyan:pixel(40,40)};}""")
                    assert pixels_check["green"]==[0,255,0,255],pixels_check
                    assert pixels_check["clipped"]==[0,0,0,255],pixels_check
                    assert pixels_check["red"]==[255,0,0,255],pixels_check
                    assert pixels_check["cyan"]==[0,255,255,255],pixels_check
                if name=="Bitmap":
                    assert "PHONE_ME_BITMAP_RESOURCE_PASS" in output,output
                    bitmap_pixel=page.evaluate("Array.from(document.getElementById('pf-screen').getContext('2d').getImageData(20,20,1,1).data)")
                    assert bitmap_pixel==[255,0,0,255],bitmap_pixel
                input_changed=None
                touch_changed=None
                if name=="Midi":
                    assert "MIDI_SYNTH_ASSET_PASS" in output,output
                    assert report['midi_tracks_rendered']==1,report
                    midi=page.evaluate("""() => {
                       const a=[...window.PocketForgeAudio.values()][0];
                       const source=a.getAttribute('src');
                       return {mime:source.slice(5,source.indexOf(';base64,')),ready:a.readyState,
                               decoded:atob(source.split(';base64,')[1].slice(0,8)),error:a.error?.code||0};
                    }""")
                    assert midi['mime']=='audio/ogg' and midi['decoded'].startswith('OggS'),midi
                    assert midi['ready']>=2 and not midi['error'],midi
                    page.locator('#pf-controls button[data-key="Digit5"]').click()
                    page.wait_for_timeout(200)
                    output=page.locator('#log').inner_text()
                    assert "MIDI_START_PASS" in output,output
                    page.wait_for_timeout(200)
                    assert page.evaluate("[...window.PocketForgeAudio.values()][0].currentTime")>0.1
                if name=="Adpcm":
                    assert "IMA_ADPCM_PLAYER_PASS" in output,output
                    audio=page.evaluate("""() => {
                       const a=[...window.PocketForgeAudio.values()][0];
                       const s=a.getAttribute('src');const b=atob(s.slice(s.indexOf(';base64,')+8));
                       return {mime:s.slice(5,s.indexOf(';base64,')),
                         format:b.charCodeAt(20)+b.charCodeAt(21)*256,
                         samples:(b.length-44)/2,ready:a.readyState,error:a.error?.code||null};
                    }""")
                    assert audio['format']==1,audio
                    assert audio['samples']==17,audio
                    assert audio['ready']>=2 and not audio['error'],audio
                    # Verify browser can start real playback after a trusted user gesture.
                    page.evaluate("""() => {
                      const btn=document.querySelector('#pf-controls button[data-key=Digit5]');
                      btn.addEventListener('pointerdown',function(){
                        const a=[...window.PocketForgeAudio.values()][0];
                        a.play().then(()=>window.PFAdpcmPlay='resolved')
                                .catch(e=>window.PFAdpcmPlay=String(e));
                      },{once:true,capture:true});
                    }""")
                    page.locator('#pf-controls button[data-key=Digit5]').click()
                    page.wait_for_function("window.PFAdpcmPlay!==undefined",timeout=2500)
                    assert page.evaluate("window.PFAdpcmPlay")=='resolved'
                if name=="Media":
                    assert "MMAPI_STATES_CONTROLS_PASS" in output,output
                    assert page.evaluate("window.PocketForgeAudio?.size") == 1
                    rate=page.evaluate("[...window.PocketForgeAudio.values()][0].playbackRate")
                    assert abs(rate-1.2)<0.001,rate
                    page.keyboard.press("ArrowUp")
                    page.wait_for_timeout(250)
                    output=page.locator("#log").inner_text()
                    assert "MMAPI_START_STOP_CLOSE_PASS" in output,output
                    assert page.evaluate("window.PocketForgeAudio.size") == 0
                if name=="Interactive":
                    previous=page.evaluate("document.getElementById('pf-screen').toDataURL()")
                    page.keyboard.press("ArrowUp")
                    page.wait_for_timeout(200)
                    after=page.evaluate("document.getElementById('pf-screen').toDataURL()")
                    input_changed=previous!=after
                    assert input_changed,"MIDP keyPressed was not triggered by ArrowUp"
                    before_touch=page.evaluate("document.getElementById('pf-screen').toDataURL()")
                    page.locator('#pf-screen').click(position={"x":120,"y":100})
                    page.wait_for_timeout(200)
                    touch_changed=before_touch!=page.evaluate("document.getElementById('pf-screen').toDataURL()")
                    assert touch_changed,"MIDP Canvas.pointerPressed was not triggered"
                    before_button=page.evaluate("document.getElementById('pf-screen').toDataURL()")
                    page.locator('#pf-controls button[data-key="Digit5"]').click()
                    page.wait_for_timeout(150)
                    assert before_button!=page.evaluate("document.getElementById('pf-screen').toDataURL()"),"Virtual keypad failed to send MIDP key"
                    # A focused button must dispatch one logical key, not both
                    # the native Enter/Space and a synthetic Digit5.
                    button=page.locator('#pf-controls button[data-key="Digit5"]')
                    button.focus()
                    for key in ('Enter','Space'):
                        count=page.locator('#log').inner_text().count('KEY_CODE=')
                        page.keyboard.press(key)
                        page.wait_for_timeout(100)
                        after_log=page.locator('#log').inner_text()
                        assert after_log.count('KEY_CODE=')==count+1,after_log
                        assert 'KEY_CODE=53' in after_log

                image=OUT/(name+".png")
                page.screenshot(path=str(image),full_page=True)
                assert not errors,errors
                assert not network,network
                if name in ("Calculator","ResourceMain","ConnectorMain","RmsMain"):
                    marker={"Calculator":"CALCULATOR=57","ResourceMain":"PHONE_ME_RESOURCE_OK","ConnectorMain":"CONNECTOR_RESOURCE_AND_DENIAL_PASS","RmsMain":"RMS_BEFORE=1 RMS_AFTER=1"}[name]
                    assert marker in output,output
                    assert canvas is None
                else:
                    assert canvas and canvas["width"]==(320 if name=="WideScreen" else 240) and canvas["height"]==(240 if name=="WideScreen" else 320)
                    assert (canvas["colors"]>=3 and canvas["nonblack"]>1000) or (name in ("ReferenceGraphics","Bitmap") and canvas["colors"]>=5) or (name in ("Media","Adpcm","Midi","WideScreen") and canvas["nonblack"]>1000),canvas
                evidence[name]={
                    "jar_sha256":hashlib.sha256(jar.read_bytes()).hexdigest(),
                    "html_sha256":hashlib.sha256(html.read_bytes()).hexdigest(),
                    "generated_bytes":html.stat().st_size,
                    "output":output,"canvas":canvas,
                    "network_requests":network,"page_errors":errors,
                    "original_jar_embedded":False,"jsvm_embedded":False,
                    "input_changed":input_changed,"touch_changed":touch_changed,"pixels_check":pixels_check,
                    "screenshot":str(image)
                }
                page.close()
            browser.close()
    receipt=OUT/"aot-validation.json"
    receipt.write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(evidence,ensure_ascii=False,indent=2))
    print("PASS: twelve independent JARs compiled AOT to standalone HTML; no JVM/JAR/runtime network")
if __name__=="__main__":
    main()
