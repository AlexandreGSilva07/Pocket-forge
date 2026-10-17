package demo;
import javax.microedition.midlet.MIDlet;
import javax.microedition.lcdui.Display;
import javax.microedition.lcdui.Canvas;
import javax.microedition.lcdui.Graphics;
public final class InteractiveMIDlet extends MIDlet {
 protected void startApp(){Display.getDisplay(this).setCurrent(new Game());}
 protected void pauseApp(){} protected void destroyApp(boolean unconditional){}
 static final class Game extends Canvas {
  int moves;
  protected void paint(Graphics g){
    g.setColor(10,24,43);g.fillRect(0,0,240,320);
    g.setColor(moves>0?0x41dd87:0xcddd41);g.fillRect(30,90,180,80);
    g.setColor(0xffffff);g.drawString("MOVES="+moves,50,120,Graphics.TOP|Graphics.LEFT);
  }
  protected void keyPressed(int code){moves++;repaint();}
 }
}