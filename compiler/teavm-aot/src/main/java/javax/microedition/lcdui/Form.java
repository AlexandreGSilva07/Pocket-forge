package javax.microedition.lcdui;
import java.util.ArrayList;
import org.teavm.jso.JSBody;
public final class Form extends Displayable {
 private final ArrayList<String> fields=new ArrayList<String>();
 public Form(String title){setTitle(title);}
 public int append(String text){fields.add(text);return fields.size()-1;}
 public int append(Item item){fields.add((item.getLabel()==null?"":item.getLabel())+": "+
   (item instanceof TextField?((TextField)item).getString():""));return fields.size()-1;}
 @JSBody(params={"text"},script="var node=document.getElementById('pf-form');if(!node){node=document.createElement('section');node.id='pf-form';document.getElementById('game').appendChild(node)}node.textContent=text;")
 private static native void render(String text);
 public void show(){StringBuilder builder=new StringBuilder(getTitle()==null?"":getTitle());
   for(int i=0;i<fields.size();i++)builder.append("\n").append(fields.get(i));
   render(builder.toString());}
}