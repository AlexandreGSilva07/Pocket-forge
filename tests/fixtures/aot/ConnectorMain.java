package demo;
import java.io.*;
import javax.microedition.io.*;
public final class ConnectorMain {
 public static void main(String[] args) throws Exception {
  Connection c=Connector.open("resource:/demo/hello.txt",Connector.READ);
  InputStream in=((InputConnection)c).openInputStream();
  byte[] buf=new byte[32];int n=in.read(buf);String t=new String(buf,0,n,"UTF-8");
  if(!"PHONE_ME_RESOURCE_OK".equals(t))throw new AssertionError("resource contents "+t);
  in.close();c.close();
  boolean refused=false;
  try{Connector.open("file:///private/device/c:/system",Connector.READ);}catch(IOException ex){refused=true;}
  if(!refused)throw new AssertionError("file:// must not get fake filesystem access");
  System.out.println("CONNECTOR_RESOURCE_AND_DENIAL_PASS");
 }
}