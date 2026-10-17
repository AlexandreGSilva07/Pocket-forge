package javax.microedition.lcdui;
import java.util.ArrayList;
public class Displayable {
 private String title;
 private CommandListener listener;
 private final ArrayList<Command> commands=new ArrayList<Command>();
 public boolean isShown(){return true;}
 public int getWidth(){return Canvas.__pfScreenWidth();}
 public int getHeight(){return Canvas.__pfScreenHeight();}
 public void setTitle(String title){this.title=title;}
 public String getTitle(){return title;}
 public void setCommandListener(CommandListener listener){this.listener=listener;}
 public void addCommand(Command command){if(command!=null&&!commands.contains(command))commands.add(command);}
 public void removeCommand(Command command){commands.remove(command);}
 public void __pfCommand(int index){if(listener!=null&&index>=0&&index<commands.size())listener.commandAction(commands.get(index),this);}
 public int __pfCommandCount(){return commands.size();}
 public String __pfCommandLabel(int index){return commands.get(index).getLabel();}
}