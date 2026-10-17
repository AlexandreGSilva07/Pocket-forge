package demo;
import javax.microedition.midlet.MIDlet;
import javax.microedition.lcdui.Display;
import javax.microedition.lcdui.Canvas;
import javax.microedition.lcdui.Graphics;
public class PocketDemoMIDlet extends MIDlet {
 protected void startApp(){Display.getDisplay(this).setCurrent(new Game());}
 protected void pauseApp(){} protected void destroyApp(boolean unconditional){}
 static final class Game extends Canvas {
  private int total;
  Game(){int[] vals={2,4,6,8}; for(int i=0;i<vals.length;i++)total+=vals[i]*(i+1);}
  protected void paint(Graphics g){g.setColor(8,16,30);g.fillRect(0,0,getWidth(),getHeight());
    g.setColor(44,220,145);g.fillRect(20,35,190,55);
    g.setColor(255,255,255);g.drawString("POCKETFORGE AOT",30,53,Graphics.TOP|Graphics.LEFT);
    g.drawString("Java ME compiled: "+total,22,120,Graphics.TOP|Graphics.LEFT);
  }
 }
}