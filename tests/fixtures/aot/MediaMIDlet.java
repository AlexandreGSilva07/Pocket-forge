package demo;
import javax.microedition.midlet.MIDlet;
import javax.microedition.lcdui.Canvas;
import javax.microedition.lcdui.Display;
import javax.microedition.lcdui.Graphics;
import javax.microedition.media.*;
import javax.microedition.media.control.*;
import java.io.InputStream;
public final class MediaMIDlet extends MIDlet {
 protected void startApp(){
  try{
   InputStream stream=getClass().getResourceAsStream("/demo/beep.wav");
   if(stream==null)throw new IllegalStateException("Missing WAV in original JAR");
   Player player=Manager.createPlayer(stream,"audio/wav");
   if(player.getState()!=Player.UNREALIZED)throw new AssertionError("state unrealized");
   player.realize();
   if(player.getState()!=Player.REALIZED)throw new AssertionError("state realized");
   player.prefetch();
   if(player.getState()!=Player.PREFETCHED)throw new AssertionError("state prefetched");
   VolumeControl volume=(VolumeControl)player.getControl("VolumeControl");
   RateControl rate=(RateControl)player.getControl("RateControl");
   TempoControl tempo=(TempoControl)player.getControl("TempoControl");
   if(volume==null||rate==null||tempo==null)throw new AssertionError("controls");
   if(volume.setLevel(35)!=35)throw new AssertionError("volume");
   volume.setMute(false);
   if(rate.setRate(150000)!=150000)throw new AssertionError("rate");
   if(tempo.setTempo(144000)!=144000)throw new AssertionError("tempo");
   player.setLoopCount(2);
   System.out.println("MMAPI_STATES_CONTROLS_PASS");
   Display.getDisplay(this).setCurrent(new AudioCanvas(player));
  }catch(Exception e){throw new RuntimeException(e);}
 }
 protected void pauseApp(){} protected void destroyApp(boolean unconditional){}
 static final class AudioCanvas extends Canvas {
  private final Player player;
  AudioCanvas(Player p){player=p;}
  protected void paint(Graphics g){g.setColor(0x112234);g.fillRect(0,0,240,320);}
  protected void keyPressed(int key){
   try{
    player.start();
    if(player.getState()!=Player.STARTED)throw new AssertionError("started");
    player.stop();
    if(player.getState()!=Player.PREFETCHED)throw new AssertionError("stopped");
    player.close();
    if(player.getState()!=Player.CLOSED)throw new AssertionError("closed");
    System.out.println("MMAPI_START_STOP_CLOSE_PASS");
   }catch(Exception ex){throw new RuntimeException(ex);}
  }
 }
}