package javax.microedition.lcdui;

import org.teavm.jso.JSBody;
import org.teavm.jso.JSByRef;

/** General MIDP 2 Graphics adapter; independent of particular games. */
public class Graphics {
 public static final int TOP=16,BOTTOM=32,LEFT=4,RIGHT=8,HCENTER=1,VCENTER=2,BASELINE=64;
 private int color=0, surface=0, tx=0,ty=0;
 private int clipX=0,clipY=0,clipW=240,clipH=320;
 private Font font=Font.getDefaultFont();
 public Graphics(){}
 Graphics(int id){surface=id;clipW=Image.__pfWidth(id);clipH=Image.__pfHeight(id);}
 public void setColor(int r,int g,int b){if((r|g|b)<0||r>255||g>255||b>255)throw new IllegalArgumentException();color=(r<<16)|(g<<8)|b;}
 public void setColor(int rgb){color=rgb&0xFFFFFF;}
 public int getColor(){return color;}
 public void setFont(Font f){if(f==null)throw new NullPointerException();font=f;}
 public Font getFont(){return font;}
 public void translate(int x,int y){tx+=x;ty+=y;}
 public int getTranslateX(){return tx;}
 public int getTranslateY(){return ty;}
 public int getClipX(){return clipX-tx;}
 public int getClipY(){return clipY-ty;}
 public int getClipWidth(){return clipW;}
 public int getClipHeight(){return clipH;}
 public void setClip(int x,int y,int w,int h){clipX=x+tx;clipY=y+ty;clipW=Math.max(0,w);clipH=Math.max(0,h);}
 public void clipRect(int x,int y,int w,int h){
  int x1=Math.max(clipX,x+tx),y1=Math.max(clipY,y+ty);
  int x2=Math.min(clipX+clipW,x+tx+Math.max(0,w));
  int y2=Math.min(clipY+clipH,y+ty+Math.max(0,h));
  clipX=x1;clipY=y1;clipW=Math.max(0,x2-x1);clipH=Math.max(0,y2-y1);
 }
 @JSBody(params={"id","x","y","w","h","rgb","cx","cy","cw","ch"},script=
  "var c=id===0?document.getElementById('pf-screen'):window.PocketForgeSurfaces.get(id);if(!c)return;"+
  "var g=c.getContext('2d');g.save();g.beginPath();g.rect(cx,cy,cw,ch);g.clip();"+
  "g.fillStyle='#'+(rgb>>>0).toString(16).padStart(6,'0');g.fillRect(x,y,w,h);g.restore();")
 private static native void rectangle(int id,int x,int y,int w,int h,int rgb,int cx,int cy,int cw,int ch);
 public void fillRect(int x,int y,int w,int h){if(w>0&&h>0)rectangle(surface,x+tx,y+ty,w,h,color,clipX,clipY,clipW,clipH);}
 public void drawRect(int x,int y,int w,int h){
  if(w<0||h<0)return;
  fillRect(x,y,w+1,1);fillRect(x,y+h,w+1,1);
  fillRect(x,y,1,h+1);fillRect(x+w,y,1,h+1);
 }
 @JSBody(params={"id","s","x","y","rgb","height","cx","cy","cw","ch"},script=
  "var c=id===0?document.getElementById('pf-screen'):window.PocketForgeSurfaces.get(id);if(!c)return;"+
  "var g=c.getContext('2d');g.save();g.beginPath();g.rect(cx,cy,cw,ch);g.clip();"+
  "g.fillStyle='#'+(rgb>>>0).toString(16).padStart(6,'0');g.font=height+'px monospace';g.fillText(s,x,y);g.restore();")
 private static native void print(int id,String s,int x,int y,int rgb,int height,int cx,int cy,int cw,int ch);
 public void drawString(String s,int x,int y,int anchor){
  if(s==null)throw new NullPointerException();
  print(surface,s,x+tx,y+ty+((anchor&TOP)!=0?font.getHeight():0),color,font.getHeight(),clipX,clipY,clipW,clipH);
 }
 public void drawChar(char c,int x,int y,int anchor){drawString(String.valueOf(c),x,y,anchor);}
 public void drawChars(char[] chars,int offset,int len,int x,int y,int anchor){drawString(new String(chars,offset,len),x,y,anchor);}
 @JSBody(params={"id","x1","y1","x2","y2","rgb","cx","cy","cw","ch"},script=
  "var c=id===0?document.getElementById('pf-screen'):window.PocketForgeSurfaces.get(id);if(!c)return;"+
  "var g=c.getContext('2d');g.save();g.beginPath();g.rect(cx,cy,cw,ch);g.clip();"+
  "g.strokeStyle='#'+(rgb>>>0).toString(16).padStart(6,'0');g.beginPath();g.moveTo(x1+.5,y1+.5);g.lineTo(x2+.5,y2+.5);g.stroke();g.restore();")
 private static native void line(int id,int x1,int y1,int x2,int y2,int rgb,int cx,int cy,int cw,int ch);
 public void drawLine(int x1,int y1,int x2,int y2){line(surface,x1+tx,y1+ty,x2+tx,y2+ty,color,clipX,clipY,clipW,clipH);}
 public void fillTriangle(int x1,int y1,int x2,int y2,int x3,int y3){
  triangle(surface,x1+tx,y1+ty,x2+tx,y2+ty,x3+tx,y3+ty,color,clipX,clipY,clipW,clipH);
 }
 @JSBody(params={"id","x1","y1","x2","y2","x3","y3","rgb","cx","cy","cw","ch"},script=
  "var c=id===0?document.getElementById('pf-screen'):window.PocketForgeSurfaces.get(id);if(!c)return;"+
  "var g=c.getContext('2d');g.save();g.beginPath();g.rect(cx,cy,cw,ch);g.clip();"+
  "g.fillStyle='#'+(rgb>>>0).toString(16).padStart(6,'0');g.beginPath();"+
  "g.moveTo(x1,y1);g.lineTo(x2,y2);g.lineTo(x3,y3);g.closePath();g.fill();g.restore();")
 private static native void triangle(int id,int x1,int y1,int x2,int y2,int x3,int y3,int rgb,int cx,int cy,int cw,int ch);
 public void drawArc(int x,int y,int w,int h,int start,int angle){drawRect(x,y,w,h);}
 public void fillArc(int x,int y,int w,int h,int start,int angle){fillRect(x,y,w,h);}
 @JSBody(params={"dst","src","x","y","anchor","cx","cy","cw","ch"},script=
  "var d=dst===0?document.getElementById('pf-screen'):window.PocketForgeSurfaces.get(dst);"+
  "var s=window.PocketForgeSurfaces.get(src);if(!d||!s)return;"+
  "var px=x,py=y;if(anchor&1)px-=s.width/2;else if(anchor&8)px-=s.width;"+
  "if(anchor&2)py-=s.height/2;else if(anchor&32)py-=s.height;"+
  "var g=d.getContext('2d');g.save();g.beginPath();g.rect(cx,cy,cw,ch);g.clip();g.drawImage(s,px,py);g.restore();")
 private static native void copyImage(int dst,int src,int x,int y,int anchor,int cx,int cy,int cw,int ch);
 public void drawImage(Image img,int x,int y,int anchor){
  if(img==null)throw new NullPointerException();
  copyImage(surface,img.__pfSurfaceId(),x+tx,y+ty,anchor,clipX,clipY,clipW,clipH);
 }
 @JSBody(params={"dst","src","sx","sy","w","h","transform","dx","dy","anchor","cx","cy","cw","ch"},script=
  "var d=dst===0?document.getElementById('pf-screen'):window.PocketForgeSurfaces.get(dst);"+
  "var s=window.PocketForgeSurfaces.get(src);if(!d||!s)return;"+
  "var g=d.getContext('2d');g.save();g.beginPath();g.rect(cx,cy,cw,ch);g.clip();"+
  "var pw=((transform&4)!==0)?h:w,ph=((transform&4)!==0)?w:h;"+
  "if(anchor&1)dx-=pw/2;else if(anchor&8)dx-=pw;"+
  "if(anchor&2)dy-=ph/2;else if(anchor&32)dy-=ph;"+
  "g.translate(dx,dy);"+
  "switch(transform){case 1:g.translate(0,h);g.scale(1,-1);break;"+
  "case 2:g.translate(w,0);g.scale(-1,1);break;"+
  "case 3:g.translate(w,h);g.rotate(Math.PI);break;"+
  "case 4:g.translate(h,0);g.rotate(Math.PI/2);break;"+
  "case 5:g.translate(0,w);g.rotate(-Math.PI/2);break;"+
  "case 6:g.translate(h,w);g.rotate(Math.PI/2);g.scale(-1,1);break;"+
  "case 7:g.rotate(-Math.PI/2);g.scale(-1,1);break;}"+
  "g.drawImage(s,sx,sy,w,h,0,0,w,h);g.restore();")
 private static native void region(int dst,int src,int sx,int sy,int w,int h,int transform,int dx,int dy,int anchor,int cx,int cy,int cw,int ch);
 public void drawRegion(Image img,int sx,int sy,int w,int h,int transform,int dx,int dy,int anchor){
  if(img==null)throw new NullPointerException();
  if(w<1||h<1||sx<0||sy<0||sx+w>img.getWidth()||sy+h>img.getHeight())throw new IllegalArgumentException();
  if(transform<0||transform>7)throw new IllegalArgumentException();
  region(surface,img.__pfSurfaceId(),sx,sy,w,h,transform,dx+tx,dy+ty,anchor,clipX,clipY,clipW,clipH);
 }
 @JSBody(params={"id","argb","offset","stride","x","y","w","h","alpha","cx","cy","cw","ch"},script=
  "var c=id===0?document.getElementById('pf-screen'):window.PocketForgeSurfaces.get(id);if(!c)return;"+
  "var tmp=document.createElement('canvas');tmp.width=w;tmp.height=h;"+
  "var tg=tmp.getContext('2d');var img=tg.createImageData(w,h),out=img.data;"+
  "for(var j=0;j<h;j++)for(var i=0;i<w;i++){var q=argb[offset+j*stride+i]>>>0;var k=(j*w+i)*4;"+
  "out[k]=(q>>>16)&255;out[k+1]=(q>>>8)&255;out[k+2]=q&255;out[k+3]=alpha?((q>>>24)&255):255;}"+
  "tg.putImageData(img,0,0);var g=c.getContext('2d');g.save();g.beginPath();g.rect(cx,cy,cw,ch);g.clip();g.drawImage(tmp,x,y);g.restore();")
 private static native void pixelArea(int id,@JSByRef int[] argb,int offset,int stride,int x,int y,int w,int h,boolean alpha,int cx,int cy,int cw,int ch);
 public void drawRGB(int[] rgb,int offset,int scanlength,int x,int y,int w,int h,boolean processAlpha){
  if(rgb==null)throw new NullPointerException();
  if(w<0||h<0)throw new IllegalArgumentException();
  if(w==0||h==0)return;
  long first=offset,last=offset+(long)(h-1)*scanlength;
  long min=Math.min(first,last),max=Math.max(first,last)+w-1;
  if(min<0||max>=rgb.length)throw new ArrayIndexOutOfBoundsException();
  pixelArea(surface,rgb,offset,scanlength,x+tx,y+ty,w,h,processAlpha,clipX,clipY,clipW,clipH);
 }
}