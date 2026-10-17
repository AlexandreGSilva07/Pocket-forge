package demo;
import java.io.InputStream;
import javax.microedition.lcdui.Canvas;
import javax.microedition.lcdui.Display;
import javax.microedition.lcdui.Graphics;
import javax.microedition.media.Manager;
import javax.microedition.media.Player;
import javax.microedition.midlet.MIDlet;

/** A standalone MIDI fixture; no game-specific audio logic. */
public final class MidiMIDlet extends MIDlet {
 protected void startApp() {
  try {
   InputStream in=getClass().getResourceAsStream("/demo/song.mid");
   if(in==null)throw new IllegalStateException("MIDI fixture resource missing");
   Player player=Manager.createPlayer(in,"audio/midi");
   player.prefetch();
   if(player.getState()!=Player.PREFETCHED)throw new AssertionError("MIDI prefetch");
   System.out.println("MIDI_SYNTH_ASSET_PASS");
   Display.getDisplay(this).setCurrent(new View(player));
  }catch(Exception ex){throw new RuntimeException(ex);}
 }
 protected void pauseApp(){}
 protected void destroyApp(boolean unconditional){}
 private static final class View extends Canvas {
  private final Player player;
  View(Player p){player=p;}
  protected void paint(Graphics g){g.setColor(0x283950);g.fillRect(0,0,240,320);
   g.setColor(0xffffff);g.drawString("MIDI rendered offline",12,12,Graphics.TOP|Graphics.LEFT);}
  protected void keyPressed(int key){
   try{player.start();System.out.println("MIDI_START_PASS");}
   catch(Exception ex){throw new RuntimeException(ex);}
  }
 }
}