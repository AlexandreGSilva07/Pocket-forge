package pocketforge.media;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import javax.microedition.media.*;
import javax.microedition.media.control.*;
import org.teavm.jso.JSBody;
/** General MMAPI audio player backed by an in-document HTMLAudioElement.
 * Never fetches network data. Unsupported codecs fail at creation time.
 */
public final class BrowserPlayer implements Player,VolumeControl,RateControl,TempoControl {
 private static int nextId=1;
 private final int id;
 private final String type;
 private int state=UNREALIZED,loopCount=1,level=100,rate=100000,tempo=120000;
 private boolean muted;
 public BrowserPlayer(InputStream stream,String mime) throws IOException {
  if(stream==null||mime==null)throw new IllegalArgumentException("Source and MIME required");
  type=mime.toLowerCase().split(";")[0].trim();
  boolean supported=type.equals("audio/wav")||type.equals("audio/x-wav")||
       type.equals("audio/mpeg")||type.equals("audio/mp3")||
       type.equals("audio/ogg")||type.equals("audio/mp4")||
       type.equals("audio/midi")||type.equals("audio/x-midi")||
       type.equals("audio/sp-midi")||type.equals("audio/mid");
  if(!supported)throw new IOException("Unsupported MMAPI codec: "+mime);
  ByteArrayOutputStream out=new ByteArrayOutputStream();
  byte[] buf=new byte[4096];int total=0,n;
  while((n=stream.read(buf))!=-1){total+=n;
   if(total>8*1024*1024)throw new IOException("Audio exceeds 8 MiB");
   out.write(buf,0,n);
  }
  byte[] bytes=out.toByteArray();
  if(bytes.length==0)throw new IOException("Empty media stream");
  // Java ME games often store IMA ADPCM inside RIFF/WAVE (format 0x0011).
  // Browsers accept WAV as a container but commonly reject that codec.
  // Decode the standard codec to PCM while preserving the Player interface.
  boolean converted=ImaAdpcmWav.isImaAdpcm(bytes);
  if(converted){
    bytes=ImaAdpcmWav.toPcm16Wav(bytes);
  }
  boolean isMidi=bytes.length>=14&&bytes[0]=='M'&&bytes[1]=='T'&&
                 bytes[2]=='h'&&bytes[3]=='d';
  id=nextId++;
  if(!create(id,converted?"audio/wav":isMidi?"audio/midi":type,encode(bytes)))
   throw new IOException("No offline-synthesized MIDI asset for this resource");
 }
 private static String encode(byte[] data){
  final char[] chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".toCharArray();
  StringBuilder sb=new StringBuilder((data.length+2)/3*4);
  for(int i=0;i<data.length;i+=3){
   int a=data[i]&255,b=i+1<data.length?data[i+1]&255:0,c=i+2<data.length?data[i+2]&255:0;
   sb.append(chars[a>>>2]).append(chars[((a&3)<<4)|(b>>>4)]);
   sb.append(i+1<data.length?chars[((b&15)<<2)|(c>>>6)]:'=');
   sb.append(i+2<data.length?chars[c&63]:'=');
  }
  return sb.toString();
 }
 @JSBody(params={"id","mime","base64"},script=
 "if(!window.PocketForgeAudio)window.PocketForgeAudio=new Map();"+
 "if(!window.__pfAudioUnlock){window.__pfAudioUnlock=true;"+
 "var unlock=function(){window.PocketForgeAudio.forEach(function(audio){"+
 "if(audio.__pfNeedsGesture&&audio.__pfDesired){audio.__pfNeedsGesture=false;"+
 "var attempt=audio.play();if(attempt&&attempt.catch)attempt.catch(function(){audio.__pfNeedsGesture=true;});}});};"+
 "document.addEventListener('pointerdown',unlock,true);document.addEventListener('keydown',unlock,true);}"+
 "if(mime==='audio/midi'||mime==='audio/x-midi'||mime==='audio/sp-midi'||mime==='audio/mid'){"+
 "var converted=window.PocketForgeMidiAssets&&window.PocketForgeMidiAssets[base64];"+
 "if(!converted)return false;"+
 "base64=converted;mime='audio/ogg';}"+
 "var a=document.createElement('audio');a.preload='auto';"+
 "a.__pfDesired=false;a.__pfNeedsGesture=false;"+
 "a.src='data:'+mime+';base64,'+base64;window.PocketForgeAudio.set(id,a);return true;")
 private static native boolean create(int id,String mime,String base64);
 @JSBody(params={"id"},script="var a=window.PocketForgeAudio.get(id);a.load();")
 private static native void load(int id);
 @JSBody(params={"id","loops"},script=
 "var a=window.PocketForgeAudio.get(id);a.__pfDesired=true;a.loop=loops===-1;"+
 "if(loops>1){var remain=loops-1;a.onended=function(){if(remain-->0){a.currentTime=0;a.play().catch(function(e){console.warn('MMAPI playback failed: '+e.message)})}}}"+
 "var p=a.play();if(p&&p.then)p.then(function(){a.__pfNeedsGesture=false;},function(e){"+
 "if(a.__pfDesired)a.__pfNeedsGesture=true;window.PocketForgeAudioError=String(e);"+
 "if(e.name!=='NotAllowedError')console.warn('MMAPI playback failed: '+e.message);});")
 private static native void play(int id,int loops);
 @JSBody(params={"id"},script="var a=window.PocketForgeAudio.get(id);a.__pfDesired=false;a.__pfNeedsGesture=false;a.pause();")
 private static native void pause(int id);
 @JSBody(params={"id","seconds"},script="var a=window.PocketForgeAudio.get(id);try{a.currentTime=Math.max(0,seconds)}catch(e){}")
 private static native void seek(int id,double seconds);
 @JSBody(params={"id"},script="return window.PocketForgeAudio.get(id).currentTime||0;")
 private static native double position(int id);
 @JSBody(params={"id"},script="var d=window.PocketForgeAudio.get(id).duration;return Number.isFinite(d)?d:-1;")
 private static native double duration(int id);
 @JSBody(params={"id"},script="var a=window.PocketForgeAudio.get(id);a.__pfDesired=false;a.__pfNeedsGesture=false;a.pause();a.removeAttribute('src');a.load();window.PocketForgeAudio.delete(id);")
 private static native void destroy(int id);
 @JSBody(params={"id","level","muted"},script="var a=window.PocketForgeAudio.get(id);a.volume=level/100;a.muted=muted;")
 private static native void volume(int id,int level,boolean muted);
 @JSBody(params={"id","rate"},script="window.PocketForgeAudio.get(id).playbackRate=rate/100000;")
 private static native void speed(int id,int rate);
 private void ensureOpen(){if(state==CLOSED)throw new IllegalStateException("Player is closed");}
 public int getState(){return state;}
 public void realize() throws MediaException{ensureOpen();if(state==UNREALIZED)state=REALIZED;}
 public void prefetch() throws MediaException{ensureOpen();realize();if(state==REALIZED){load(id);state=PREFETCHED;}}
 public void start() throws MediaException{ensureOpen();prefetch();if(state!=STARTED){play(id,loopCount);state=STARTED;}}
 public void stop() throws MediaException{ensureOpen();if(state==STARTED){pause(id);state=PREFETCHED;}}
 public void deallocate(){ensureOpen();if(state==STARTED)pause(id);if(state>=PREFETCHED)state=REALIZED;}
 public void close(){if(state==CLOSED)return;destroy(id);state=CLOSED;}
 public long getMediaTime(){ensureOpen();return (long)(position(id)*1000000.0);}
 public long setMediaTime(long time) throws MediaException{ensureOpen();if(time<0)time=0;seek(id,time/1000000.0);return getMediaTime();}
 public long getDuration(){ensureOpen();double d=duration(id);return d<0?TIME_UNKNOWN:(long)(d*1000000.0);}
 public void setLoopCount(int count){ensureOpen();if(count==0||count< -1)throw new IllegalArgumentException();if(state==STARTED)throw new IllegalStateException();loopCount=count;}
 public String getContentType(){ensureOpen();return type;}
 public Control getControl(String name){
  ensureOpen();if(name==null)return null;
  if(name.equals("VolumeControl")||name.equals("javax.microedition.media.control.VolumeControl"))return this;
  if(name.equals("RateControl")||name.equals("javax.microedition.media.control.RateControl"))return this;
  if(name.equals("TempoControl")||name.equals("javax.microedition.media.control.TempoControl"))return this;
  return null;
 }
 public Control[] getControls(){ensureOpen();return new Control[]{this};}
 public int getLevel(){ensureOpen();return level;}
 public int setLevel(int value){ensureOpen();level=Math.max(0,Math.min(100,value));volume(id,level,muted);return level;}
 public boolean isMuted(){ensureOpen();return muted;}
 public void setMute(boolean value){ensureOpen();muted=value;volume(id,level,muted);}
 public int getRate(){ensureOpen();return rate;}
 public int getMinRate(){return 50000;}
 public int getMaxRate(){return 200000;}
 public int setRate(int value){ensureOpen();rate=Math.max(getMinRate(),Math.min(getMaxRate(),value));speed(id,rate);return rate;}
 public int getTempo(){ensureOpen();return tempo;}
 public int setTempo(int value){ensureOpen();tempo=Math.max(10000,Math.min(300000,value));speed(id,(int)(((long)tempo*100000L)/120000L));return tempo;}
}