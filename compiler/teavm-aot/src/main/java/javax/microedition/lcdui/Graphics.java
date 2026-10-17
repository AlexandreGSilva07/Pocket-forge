package javax.microedition.lcdui;
import org.teavm.jso.JSBody;
public class Graphics {
 public static final int TOP=16,BOTTOM=32,LEFT=4,RIGHT=8,HCENTER=1,VCENTER=2,BASELINE=64;
 private int color=0, surface=0;
 private Font font=Font.getDefaultFont();
 public Graphics(){}
 Graphics(int id){surface=id;}
 public void setColor(int r,int g,int b){color=((r&255)<<16)|((g&255)<<8)|(b&255);}
 public void setColor(int rgb){color=rgb&0xFFFFFF;}
 public int getColor(){return color;}
 public void setFont(Font font){this.font=font;}
 public Font getFont(){return font;}
 @JSBody(params={"id","x","y","w","h","color"},script="var c=id===0?document.getElementById('pf-screen'):window.PocketForgeSurfaces.get(id);if(!c)return;var g=c.getContext('2d');g.fillStyle='#'+(color>>>0).toString(16).padStart(6,'0');g.fillRect(x,y,w,h);")
 private static native void rectangle(int id,int x,int y,int w,int h,int color);
 public void fillRect(int x,int y,int w,int h){rectangle(surface,x,y,w,h,color);}
 @JSBody(params={"id","text","x","y","color","height"},script="var c=id===0?document.getElementById('pf-screen'):window.PocketForgeSurfaces.get(id);if(!c)return;var g=c.getContext('2d');g.fillStyle='#'+(color>>>0).toString(16).padStart(6,'0');g.font=height+'px monospace';g.fillText(text,x,y);")
 private static native void print(int id,String text,int x,int y,int color,int height);
 public void drawString(String text,int x,int y,int anchor){print(surface,text,x,y+((anchor&TOP)!=0?font.getHeight():0),color,font.getHeight());}
 public void drawChar(char ch,int x,int y,int anchor){drawString(String.valueOf(ch),x,y,anchor);}
 public void drawChars(char[] chars,int offset,int length,int x,int y,int anchor){drawString(new String(chars,offset,length),x,y,anchor);}
 public void drawRect(int x,int y,int w,int h){rectangle(surface,x,y,w+1,1,color);rectangle(surface,x,y+h,w+1,1,color);rectangle(surface,x,y,1,h+1,color);rectangle(surface,x+w,y,1,h+1,color);}
 @JSBody(params={"id","x1","y1","x2","y2","color"},script="var c=id===0?document.getElementById('pf-screen'):window.PocketForgeSurfaces.get(id);if(!c)return;var g=c.getContext('2d');g.strokeStyle='#'+(color>>>0).toString(16).padStart(6,'0');g.beginPath();g.moveTo(x1+.5,y1+.5);g.lineTo(x2+.5,y2+.5);g.stroke();")
 private static native void line(int id,int x1,int y1,int x2,int y2,int color);
 public void drawLine(int x1,int y1,int x2,int y2){line(surface,x1,y1,x2,y2,color);}
 @JSBody(params={"id","x","y","w","h","start","angle","color"},script="var c=id===0?document.getElementById('pf-screen'):window.PocketForgeSurfaces.get(id);if(!c)return;var g=c.getContext('2d');g.strokeStyle='#'+(color>>>0).toString(16).padStart(6,'0');g.beginPath();g.ellipse(x+w/2,y+h/2,Math.max(1,w/2),Math.max(1,h/2),0,(start*Math.PI)/180,((start+angle)*Math.PI)/180);g.stroke();")
 private static native void arc(int id,int x,int y,int w,int h,int start,int angle,int color);
 public void drawArc(int x,int y,int w,int h,int start,int angle){arc(surface,x,y,w,h,start,angle,color);}
 public void fillArc(int x,int y,int w,int h,int start,int angle){fillRect(x,y,w,h);}
 @JSBody(params={"dstId","srcId","x","y","anchor"},script="var dst=dstId===0?document.getElementById('pf-screen'):window.PocketForgeSurfaces.get(dstId);var src=window.PocketForgeSurfaces.get(srcId);if(!dst||!src)return;var px=x,py=y;if((anchor&1)!==0)px-=src.width/2;else if((anchor&8)!==0)px-=src.width;if((anchor&2)!==0)py-=src.height/2;else if((anchor&32)!==0)py-=src.height;dst.getContext('2d').drawImage(src,px,py);")
 private static native void copyImage(int dstId,int srcId,int x,int y,int anchor);
 public void drawImage(Image image,int x,int y,int anchor){if(image!=null)copyImage(surface,image.__pfSurfaceId(),x,y,anchor);}
}