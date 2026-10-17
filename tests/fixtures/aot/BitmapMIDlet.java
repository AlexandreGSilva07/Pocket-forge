package demo;
import javax.microedition.midlet.MIDlet;
import javax.microedition.lcdui.Canvas;
import javax.microedition.lcdui.Display;
import javax.microedition.lcdui.Graphics;
import javax.microedition.lcdui.Image;
public class BitmapMIDlet extends MIDlet {
 protected void startApp(){Display.getDisplay(this).setCurrent(new Bitmap());}
 protected void pauseApp(){}
 protected void destroyApp(boolean b){}
 static class Bitmap extends Canvas {
  protected void paint(Graphics g){
   g.setColor(0);g.fillRect(0,0,240,320);
   try{Image image=Image.createImage("/demo/bitmap.png");g.drawImage(image,20,20,Graphics.TOP|Graphics.LEFT);
    if(image.getWidth()!=2||image.getHeight()!=2)throw new AssertionError("size");
    int[] rgb=new int[4];image.getRGB(rgb,0,2,0,0,2,2);
    if(rgb[0]!=0xffff0000||rgb[3]!=0xff0000ff)throw new AssertionError("pixels");
    System.out.println("PHONE_ME_BITMAP_RESOURCE_PASS");
   }catch(java.io.IOException ex){throw new RuntimeException(ex);}
  }
 }
}