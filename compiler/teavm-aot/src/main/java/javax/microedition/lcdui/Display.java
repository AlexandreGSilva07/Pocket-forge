package javax.microedition.lcdui;
import javax.microedition.midlet.MIDlet;
import org.teavm.jso.JSBody;
public final class Display {
 private static final Display INSTANCE=new Display();
 private Displayable current;
 public static Display getDisplay(MIDlet m){return INSTANCE;}
 @JSBody(params={"canvas"},script="var game=document.getElementById('game');var screen=document.getElementById('pf-screen');if(screen)screen.style.display=canvas?'block':'none';var form=document.getElementById('pf-form');if(form)form.style.display=canvas?'none':'block';")
 private static native void chooseScreen(boolean canvas);
 public void setCurrent(Displayable item){
   current=item;
   chooseScreen(item instanceof Canvas);
   if(item instanceof Canvas){Canvas.__pfActivate((Canvas)item);((Canvas)item).repaint();}
   else if(item instanceof Form)((Form)item).show();
 }
 public Displayable getCurrent(){return current;}
 public boolean isColor(){return true;}
 public int numColors(){return 16777216;}
}