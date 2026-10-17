package javax.microedition.lcdui;
import org.teavm.jso.JSBody;
public final class Image {
 private static int nextSurface=1;
 private final int id,width,height;
 private Image(int w,int h){if(w<1||h<1)throw new IllegalArgumentException();
   id=nextSurface++;width=w;height=h;allocate(id,w,h);}
 @JSBody(params={"id","w","h"},script="var c=document.createElement('canvas');c.width=w;c.height=h;if(!window.PocketForgeSurfaces)window.PocketForgeSurfaces=new Map();window.PocketForgeSurfaces.set(id,c);")
 private static native void allocate(int id,int w,int h);
 public static Image createImage(int width,int height){return new Image(width,height);}
 public static Image createImage(String path){throw new UnsupportedOperationException("Image resources not yet linked: "+path);}
 public static Image createImage(byte[] data,int offset,int length){throw new UnsupportedOperationException("Image byte decoder unavailable");}
 public int getWidth(){return width;}
 public int getHeight(){return height;}
 public Graphics getGraphics(){return new Graphics(id);}
 public int __pfSurfaceId(){return id;}
}