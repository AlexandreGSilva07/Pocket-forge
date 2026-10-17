package demo;
import java.io.InputStream;
import java.io.ByteArrayOutputStream;
public final class ResourceMain {
 public static void main(String[] args) throws Exception {
  InputStream in=ResourceMain.class.getClassLoader().getResourceAsStream("demo/hello.txt");
  if(in==null)throw new IllegalStateException("Classpath resource missing");
  ByteArrayOutputStream out=new ByteArrayOutputStream();
  byte[] buf=new byte[128];int n;
  while((n=in.read(buf))!=-1)out.write(buf,0,n);
  in.close();
  String text=new String(out.toByteArray(),"UTF-8");
  if(!"PHONE_ME_RESOURCE_OK".equals(text))throw new IllegalStateException("Resource mismatch "+text);
  System.out.println(text);
 }
}