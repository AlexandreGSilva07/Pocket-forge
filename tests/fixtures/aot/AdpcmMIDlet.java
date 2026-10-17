package demo;
import java.io.InputStream;
import javax.microedition.midlet.MIDlet;
import javax.microedition.lcdui.Canvas;
import javax.microedition.lcdui.Display;
import javax.microedition.lcdui.Graphics;
import javax.microedition.media.Manager;
import javax.microedition.media.Player;

/** One portable IMA ADPCM WAV resource, decoded by shared MMAPI to PCM16. */
public final class AdpcmMIDlet extends MIDlet {
 protected void startApp() {
  try {
   InputStream in=getClass().getResourceAsStream("/demo/adpcm.wav");
   if(in==null)throw new IllegalStateException("Missing ADPCM WAV");
   Player p=Manager.createPlayer(in,"audio/x-wav");
   p.prefetch();
   if(p.getState()!=Player.PREFETCHED)throw new AssertionError("Player prefetch");
   if(!p.getContentType().equals("audio/x-wav"))throw new AssertionError("Original content type");
   System.out.println("IMA_ADPCM_PLAYER_PASS");
   Display.getDisplay(this).setCurrent(new AudioCanvas(p));
  }catch(Exception e){throw new RuntimeException(e);}
 }
 protected void pauseApp(){}
 protected void destroyApp(boolean unconditional){}
 static final class AudioCanvas extends Canvas {
  private final Player player;
  AudioCanvas(Player player){this.player=player;}
  protected void paint(Graphics g){
   g.setColor(0x111c31);g.fillRect(0,0,240,320);
   g.setColor(0xc8eaff);g.drawString("IMA ADPCM -> PCM",14,14,Graphics.TOP|Graphics.LEFT);
  }
  protected void keyPressed(int code) {
   try {player.start();System.out.println("IMA_ADPCM_START_PASS");}
   catch(Exception ex){throw new RuntimeException(ex);}
  }
 }
}