package demo;
import javax.microedition.midlet.MIDlet;
import javax.microedition.lcdui.*;
/** Screen dimensions and default Graphics clip must follow compile configuration. */
public final class WideScreenMIDlet extends MIDlet {
 protected void startApp(){Display.getDisplay(this).setCurrent(new Wide());}
 protected void pauseApp(){}
 protected void destroyApp(boolean b){}
 static final class Wide extends Canvas {
  protected void paint(Graphics g){
   if(getWidth()!=320||getHeight()!=240)throw new AssertionError("Canvas resolution");
   if(g.getClipWidth()!=320||g.getClipHeight()!=240)throw new AssertionError("Graphics clip");
   g.setColor(0x27384c);g.fillRect(0,0,getWidth(),getHeight());
   g.setColor(0xffd966);g.fillRect(290,210,25,25);
   System.out.println("SCREEN_320x240_PASS");
  }
 }
}