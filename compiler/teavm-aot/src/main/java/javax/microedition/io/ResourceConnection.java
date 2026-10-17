package javax.microedition.io;
import java.io.IOException;
import java.io.InputStream;
import java.io.DataInputStream;
/** Read-only connection to embedded classpath resources, never the host filesystem. */
public final class ResourceConnection implements InputConnection {
 private final String name; private boolean closed;
 public ResourceConnection(String name){this.name=name;}
 public InputStream openInputStream() throws IOException {
  if(closed)throw new IOException("Connection closed");
  InputStream in=ResourceConnection.class.getClassLoader().getResourceAsStream(name);
  if(in==null)throw new IOException("Resource not found: "+name);
  return in;
 }
 public DataInputStream openDataInputStream() throws IOException {
  return new DataInputStream(openInputStream());
 }
 public void close(){closed=true;}
}