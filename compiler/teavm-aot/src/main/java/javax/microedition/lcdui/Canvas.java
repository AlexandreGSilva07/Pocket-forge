package javax.microedition.lcdui;
import org.teavm.jso.JSBody;
/** Generic MIDP key mapping for the TeaVM browser compiler. */
public abstract class Canvas extends Displayable {
 public static final int UP=1,DOWN=6,LEFT=2,RIGHT=5,FIRE=8;
 private final Graphics graphics=new Graphics();
 private static Canvas current;
 private static int pressed;
 private static boolean keyboardInstalled;
 @JSBody(script="if(!document.getElementById('pf-screen')){var c=document.createElement('canvas');c.id='pf-screen';c.width=240;c.height=320;c.style='border:1px solid #888;image-rendering:pixelated;max-width:100%;background:white';document.getElementById('game').appendChild(c);}")
 protected static native void ensureCanvas();
 @JSBody(script="if(window.__PF_MIDP_KEYS)return;window.__PF_MIDP_KEYS=true;var mapping={ArrowUp:-1,ArrowDown:-2,ArrowLeft:-3,ArrowRight:-4,Enter:-5,Space:-5,Digit2:50,Digit4:52,Digit5:53,Digit6:54,Digit8:56,Numpad2:50,Numpad4:52,Numpad5:53,Numpad6:54,Numpad8:56,Digit0:48,Digit1:49,Digit3:51,Digit7:55,Digit9:57,Digit6:54,Digit4:52,Digit8:56,Digit5:53,Digit2:50,F1:-6,F2:-7,Escape:-7,Backspace:-7,Home:-6,End:-7};document.addEventListener('keydown',e=>{var key=mapping[e.code];if(key===undefined)return;e.preventDefault();javaMethods.get('javax.microedition.lcdui.Canvas.__pfKeyDown(I)V').invoke(key);});document.addEventListener('keyup',e=>{var key=mapping[e.code];if(key===undefined)return;e.preventDefault();javaMethods.get('javax.microedition.lcdui.Canvas.__pfKeyUp(I)V').invoke(key);});")
 private static native void installKeyEvents();
 @JSBody(script="var c=document.getElementById('pf-screen');if(!c||c.__pfPointerInstalled)return;c.__pfPointerInstalled=true;"+
 "function pos(e){var r=c.getBoundingClientRect();return [Math.floor((e.clientX-r.left)*c.width/r.width),Math.floor((e.clientY-r.top)*c.height/r.height)]}"+
 "c.addEventListener('pointerdown',function(e){e.preventDefault();var p=pos(e);if(c.setPointerCapture)c.setPointerCapture(e.pointerId);javaMethods.get('javax.microedition.lcdui.Canvas.__pfPointerDown(II)V').invoke(p[0],p[1])});"+
 "c.addEventListener('pointerup',function(e){e.preventDefault();var p=pos(e);javaMethods.get('javax.microedition.lcdui.Canvas.__pfPointerUp(II)V').invoke(p[0],p[1])});"+
 "c.addEventListener('pointermove',function(e){if(e.buttons){var p=pos(e);javaMethods.get('javax.microedition.lcdui.Canvas.__pfPointerMove(II)V').invoke(p[0],p[1])}});")
 private static native void installPointerEvents();
 protected Canvas(){ensureCanvas();}
 public static void __pfActivate(Canvas canvas){current=canvas;installPointerEvents();if(!keyboardInstalled){keyboardInstalled=true;installKeyEvents();}}
 public static void __pfKeyDown(int keyCode){int action=actionFor(keyCode);pressed|=bitFor(action);if(current!=null)current.keyPressed(keyCode);}
 public static void __pfKeyUp(int keyCode){int action=actionFor(keyCode);pressed&=~bitFor(action);if(current!=null)current.keyReleased(keyCode);}
 public static int __pfKeyStates(){return pressed;}
 private static int bitFor(int action){switch(action){case UP:return 1;case DOWN:return 64;case LEFT:return 4;case RIGHT:return 32;case FIRE:return 256;default:return 0;}}
 private static int actionFor(int code){switch(code){
  case -1:case 50:return UP;case -2:case 56:return DOWN;
  case -3:case 52:return LEFT;case -4:case 54:return RIGHT;
  case -5:case 53:return FIRE;default:return code;}}
 public static void __pfPointerDown(int x,int y){if(current!=null)current.pointerPressed(x,y);}
 public static void __pfPointerUp(int x,int y){if(current!=null)current.pointerReleased(x,y);}
 public static void __pfPointerMove(int x,int y){if(current!=null)current.pointerDragged(x,y);}
 protected void pointerPressed(int x,int y){}
 protected void pointerReleased(int x,int y){}
 protected void pointerDragged(int x,int y){}
 public Graphics getGraphics(){return graphics;}
 protected abstract void paint(Graphics graphics);
 public void repaint(){paint(graphics);}
 public void serviceRepaints(){}
 public boolean isDoubleBuffered(){return true;}
 protected void keyPressed(int keyCode){}
 protected void keyReleased(int keyCode){}
 public int getGameAction(int keyCode){return actionFor(keyCode);}
 public int getKeyCode(int action){switch(action){case UP:return -1;case DOWN:return -2;case LEFT:return -3;case RIGHT:return -4;case FIRE:return -5;default:return action;}}
 public void setFullScreenMode(boolean full){}
}