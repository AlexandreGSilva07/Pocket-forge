package javax.microedition.lcdui.game;
import javax.microedition.lcdui.Canvas;import javax.microedition.lcdui.Graphics;
public abstract class GameCanvas extends Canvas {
 public static final int UP_PRESSED=1,DOWN_PRESSED=64,LEFT_PRESSED=4,RIGHT_PRESSED=32,FIRE_PRESSED=256;
 protected GameCanvas(boolean suppressKeyEvents){super();}
 public Graphics getGraphics(){return super.getGraphics();}
 public void flushGraphics(){}
 public void flushGraphics(int x,int y,int w,int h){}
 public int getKeyStates(){return Canvas.__pfKeyStates();}
 public void paint(Graphics graphics){}
}