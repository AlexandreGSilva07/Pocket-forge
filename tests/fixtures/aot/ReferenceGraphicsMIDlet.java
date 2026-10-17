package demo;
import javax.microedition.midlet.MIDlet;
import javax.microedition.lcdui.Display;
import javax.microedition.lcdui.Canvas;
import javax.microedition.lcdui.Graphics;
import javax.microedition.lcdui.Image;
/** Original fixture for MIDP 2 display/clip/pixel contract verification. */
public final class ReferenceGraphicsMIDlet extends MIDlet {
 protected void startApp(){Display.getDisplay(this).setCurrent(new TestCanvas());}
 protected void pauseApp(){}
 protected void destroyApp(boolean unconditional){}
 static final class TestCanvas extends Canvas {
  protected void paint(Graphics g) {
   g.setColor(0);g.fillRect(0,0,240,320);
   g.translate(5,7);
   if(g.getTranslateX()!=5||g.getTranslateY()!=7)throw new AssertionError("translate");
   g.setClip(10,10,12,12);
   g.clipRect(15,15,10,10);
   if(g.getClipX()!=15||g.getClipY()!=15||g.getClipWidth()!=7||g.getClipHeight()!=7)
    throw new AssertionError("clip intersection");
   g.setColor(0x00ff00);g.fillRect(0,0,240,320); // Should draw only in device coords 20..26.
   g.translate(-5,-7);g.setClip(0,0,240,320);
   int[] pixels={0xffff0000,0x8000ff00,0xff0000ff,0xffffff00};
   Image img=Image.createRGBImage(pixels,2,2,true);
   int[] out=new int[4];img.getRGB(out,0,2,0,0,2,2);
   for(int k=0;k<4;k++)if(out[k]!=pixels[k])throw new AssertionError("ARGB image readback at "+k);
   g.drawImage(img,30,30,Graphics.TOP|Graphics.LEFT);
   g.drawRGB(new int[]{0xff00ffff,0xffff00ff},0,2,40,40,2,1,true);
   g.drawRegion(img,0,0,2,2,0,50,50,Graphics.TOP|Graphics.LEFT);
   g.setColor(0xffffff);g.fillTriangle(80,50,90,50,85,60);
   System.out.println("PHONE_ME_GRAPHICS_CONTRACT_PASS");
  }
 }
}