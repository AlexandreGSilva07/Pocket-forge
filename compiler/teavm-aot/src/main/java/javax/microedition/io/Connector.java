package javax.microedition.io;
import java.io.IOException;
/** Generic GCF dispatch for offline AOT. Unavailable protocols fail explicitly. */
public final class Connector {
 public static final int READ=1,WRITE=2,READ_WRITE=3;
 private Connector(){}
 public static Connection open(String locator) throws IOException {return open(locator,READ_WRITE);}
 public static Connection open(String locator,int mode) throws IOException {
  if(locator==null)throw new IllegalArgumentException("Null locator");
  if(mode!=READ&&mode!=WRITE&&mode!=READ_WRITE)throw new IllegalArgumentException("Invalid mode");
  if(locator.startsWith("resource:")){
   if(mode!=READ)throw new IOException("Embedded resources are read-only");
   String name=locator.substring("resource:".length());
   if(name.startsWith("//"))name=name.substring(2);
   if(name.startsWith("/"))name=name.substring(1);
   return new ResourceConnection(name);
  }
  throw new IOException("Unsupported offline GCF protocol: "+locator);
 }
 public static Connection open(String locator,int mode,boolean timeouts) throws IOException {
  return open(locator,mode);
 }
}