package javax.microedition.lcdui;

import org.teavm.jso.JSBody;
import org.teavm.jso.JSByRef;

/** Browser-backed J2ME image surface. Resource PNG/JPEG decoding is not yet implemented. */
public final class Image {
 private static int nextSurface=1;
 private final int id,width,height;
 private final boolean mutable;
 private Image(int w,int h,boolean mutable){
  if(w<1||h<1)throw new IllegalArgumentException("Image dimensions must be positive");
  id=nextSurface++;width=w;height=h;this.mutable=mutable;allocate(id,w,h);
 }
 @JSBody(params={"id","w","h"},script=
  "var c=document.createElement('canvas');c.width=w;c.height=h;"+
  "if(!window.PocketForgeSurfaces)window.PocketForgeSurfaces=new Map();window.PocketForgeSurfaces.set(id,c);")
 private static native void allocate(int id,int w,int h);
 @JSBody(params={"id"},script="var c=window.PocketForgeSurfaces.get(id);return c?c.width:window.PocketForgeConfig.screenWidth;")
 public static native int __pfWidth(int id);
 @JSBody(params={"id"},script="var c=window.PocketForgeSurfaces.get(id);return c?c.height:window.PocketForgeConfig.screenHeight;")
 public static native int __pfHeight(int id);
 public static Image createImage(int width,int height){return new Image(width,height,true);}
 public static Image createRGBImage(int[] rgb,int w,int h,boolean processAlpha){
  if(rgb==null)throw new NullPointerException();
  if(w<1||h<1||((long)w*h)>rgb.length)throw new IllegalArgumentException();
  Image img=new Image(w,h,false);
  img.getGraphicsInternal().drawRGB(rgb,0,w,0,0,w,h,processAlpha);
  return img;
 }
 @JSBody(params={"name"},script="var a=window.PocketForgeBitmapAssets&&window.PocketForgeBitmapAssets[name];return a?a.width:0;")
 private static native int resourceWidth(String name);
 @JSBody(params={"name"},script="var a=window.PocketForgeBitmapAssets&&window.PocketForgeBitmapAssets[name];return a?a.height:0;")
 private static native int resourceHeight(String name);
 @JSBody(params={"id","name"},script=
  "var a=window.PocketForgeBitmapAssets[name];var canvas=window.PocketForgeSurfaces.get(id);"+
  "var text=atob(a.rgba),ctx=canvas.getContext('2d'),pixels=ctx.createImageData(a.width,a.height);"+
  "for(var i=0;i<text.length;i++)pixels.data[i]=text.charCodeAt(i);ctx.putImageData(pixels,0,0);")
 private static native void fillFromResource(int id,String name);
 public static Image createImage(String path) throws java.io.IOException {
  if(path==null)throw new NullPointerException();
  String name=path.startsWith("/")?path.substring(1):path;
  int w=resourceWidth(name),h=resourceHeight(name);
  if(w<1||h<1)throw new java.io.IOException("Image asset not embedded or unsupported format: "+name);
  Image image=new Image(w,h,false);fillFromResource(image.id,name);return image;
 }
 public static Image createImage(byte[] bytes,int offset,int length){throw new UnsupportedOperationException("Binary image decoder not installed");}
 public int getWidth(){return width;}
 public int getHeight(){return height;}
 public boolean isMutable(){return mutable;}
 private Graphics getGraphicsInternal(){return new Graphics(id);}
 public Graphics getGraphics(){if(!mutable)throw new IllegalStateException("Immutable image");return getGraphicsInternal();}
 public int __pfSurfaceId(){return id;}
 @JSBody(params={"id","x","y","w","h"},script=
  "var c=window.PocketForgeSurfaces.get(id);var d=c.getContext('2d',{willReadFrequently:true}).getImageData(x,y,w,h).data;"+
  "var out=new Int32Array(w*h);for(var i=0;i<out.length;i++){var k=i*4;out[i]=((d[k+3]<<24)|(d[k]<<16)|(d[k+1]<<8)|d[k+2])|0;}return out;")
 @JSByRef private static native int[] getPixels(int id,int x,int y,int w,int h);
 public void getRGB(int[] out,int offset,int scanlength,int x,int y,int w,int h){
  if(out==null)throw new NullPointerException();
  if(w<0||h<0||x<0||y<0||x+w>width||y+h>height)throw new IllegalArgumentException();
  if(w==0||h==0)return;
  long last=offset+(long)(h-1)*scanlength;
  if(Math.min(offset,last)<0||Math.max(offset,last)+w>out.length)throw new ArrayIndexOutOfBoundsException();
  int[] pixels=getPixels(id,x,y,w,h);
  for(int row=0;row<h;row++)
   for(int col=0;col<w;col++)
    out[offset+row*scanlength+col]=pixels[row*w+col];
 }
}