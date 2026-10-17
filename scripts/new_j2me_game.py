#!/usr/bin/env python3
"""Create J2ME CLDC 1.1 / MIDP 2.0 source scaffold for the Sun/Nokia SDK.

Does NOT generate verified JARs without an authentic J2ME toolchain + preverifier.
"""
import argparse
from pathlib import Path
import re
from textwrap import dedent

def new_game(target: Path, name: str, title: str):
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9]{0,47}",name):
        raise ValueError("name must be a Java identifier: letters followed by letters/digits (max 48)")
    if any(c in title for c in "\r\n") or not title.strip():
        raise ValueError("title must contain one nonempty line")
    if target.exists() and any(target.iterdir()):
        raise FileExistsError("target exists and is not empty; will not overwrite")
    src=target/"src"/"pocketforge"
    src.mkdir(parents=True,exist_ok=True)
    midlet=name+"MIDlet";canvas=name+"Canvas"
    (src/(midlet+".java")).write_text(dedent(f"""\
        package pocketforge;

        import javax.microedition.midlet.MIDlet;
        import javax.microedition.lcdui.Display;

        public final class {midlet} extends MIDlet {{
            private {canvas} game;
            protected void startApp() {{
                if (game == null) game = new {canvas}();
                Display.getDisplay(this).setCurrent(game);
                game.startGame();
            }}
            protected void pauseApp() {{ if (game != null) game.pauseGame(); }}
            protected void destroyApp(boolean unconditional) {{
                if (game != null) game.pauseGame();
            }}
        }}
    """),encoding="utf-8")
    (src/(canvas+".java")).write_text(dedent(f"""\
        package pocketforge;

        import javax.microedition.lcdui.game.GameCanvas;
        import javax.microedition.lcdui.Graphics;

        public final class {canvas} extends GameCanvas implements Runnable {{
            private volatile boolean running;
            private int x=110, y=150, score=0;
            private Thread worker;

            public {canvas}() {{ super(true); }}
            public synchronized void startGame() {{
                if (running) return;
                running=true;
                worker=new Thread(this);
                worker.start();
            }}
            public void pauseGame() {{ running=false; }}
            public void run() {{
                while (running) {{
                    long before=System.currentTimeMillis();
                    int keys=getKeyStates();
                    if ((keys & LEFT_PRESSED) != 0) x-=3;
                    if ((keys & RIGHT_PRESSED) != 0) x+=3;
                    if ((keys & UP_PRESSED) != 0) y-=3;
                    if ((keys & DOWN_PRESSED) != 0) y+=3;
                    if ((keys & FIRE_PRESSED) != 0) score++;
                    if (x < 0) x=0;
                    if (x > getWidth()-20) x=getWidth()-20;
                    if (y < 0) y=0;
                    if (y > getHeight()-20) y=getHeight()-20;
                    Graphics g=getGraphics();
                    g.setColor(8,16,30);g.fillRect(0,0,getWidth(),getHeight());
                    g.setColor(80,220,170);g.fillRect(x,y,20,20);
                    g.setColor(255,255,255);g.drawString("Score: "+score,4,4,Graphics.TOP|Graphics.LEFT);
                    flushGraphics();
                    long elapsed=System.currentTimeMillis()-before;
                    try {{ Thread.sleep(elapsed < 33 ? 33-elapsed : 1); }}
                    catch (InterruptedException ex) {{ running=false; }}
                }}
            }}
        }}
    """),encoding="utf-8")
    (target/"MANIFEST.MF").write_text("\n".join([
        "Manifest-Version: 1.0",
        "MIDlet-Name: "+title,
        "MIDlet-Version: 1.0",
        "MIDlet-Vendor: PocketForge",
        "MIDlet-1: "+title+", , pocketforge."+midlet,
        "MicroEdition-Configuration: CLDC-1.1",
        "MicroEdition-Profile: MIDP-2.0",
        "",
    ]),encoding="utf-8")
    (target/"README.md").write_text(dedent(f"""\
        # {title}

        **Fonte Java ME, ainda não testada em aparelho real.** Um microgame de
        movimento em 2D com controles GameCanvas; inteiramente autoral.

        Para gerar um JAR para celulares J2ME autênticos, use uma toolchain
        CLDC 1.1/MIDP 2.0 (ex.: Sun Wireless Toolkit 2.5.2) para compilar
        com as bibliotecas da plataforma, pré-verificar bytecode e criar
        JAR/JAD com MANIFEST.MF. Um JDK moderno sozinho **não garante**
        compatibilidade de versão de classfile, APIs ou verificação CLDC.

        Arquivos: src/pocketforge/{midlet}.java e {canvas}.java.
        Teste o JAR resultante no PocketForge J2ME Offline Runtime,
        em um emulador de referência e no dispositivo-alvo, quando possível.

        O runtime web baseado em JS2ME tem APIs incompletas; um teste bem-sucedido
        no navegador não substitui os testes com Sun/Nokia SDK.
    """),encoding="utf-8")
    print(target)
    return target
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("name")
    p.add_argument("--title")
    p.add_argument("--out",type=Path)
    a=p.parse_args()
    target=a.out or Path("generated")/a.name
    new_game(target,a.name,a.title or a.name)
if __name__=="__main__":main()
