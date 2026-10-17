package javax.microedition.media;
import java.io.IOException;
import java.io.InputStream;
import pocketforge.media.BrowserPlayer;
/** MMAPI core. Throws explicit errors for formats the browser cannot decode. */
public final class Manager {
 private Manager(){}
 public static Player createPlayer(InputStream stream,String mime) throws IOException,MediaException {
  if(stream==null||mime==null)throw new IllegalArgumentException("Null media source");
  return new BrowserPlayer(stream,mime);
 }
 public static Player createPlayer(String locator) throws IOException,MediaException {
  if(locator==null)throw new IllegalArgumentException("Null locator");
  throw new IOException("Media locators require an explicit supported source: "+locator);
 }
 public static String[] getSupportedContentTypes(String protocol) {
  return new String[]{"audio/wav","audio/mpeg","audio/ogg","audio/mp4","audio/midi","audio/x-midi","audio/sp-midi"};
 }
 public static String[] getSupportedProtocols(String type){return new String[]{"stream"};}
}