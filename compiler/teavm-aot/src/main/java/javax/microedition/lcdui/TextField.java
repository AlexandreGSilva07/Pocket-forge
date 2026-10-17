package javax.microedition.lcdui;
public final class TextField extends Item {
 public static final int ANY=0,EMAILADDR=1,NUMERIC=2,PHONENUMBER=3,URL=4,DECIMAL=5;
 private String value;
 private final int size;
 private final int constraints;
 public TextField(String label,String text,int maxSize,int constraints) {
   super(label);this.size=maxSize;this.constraints=constraints;setString(text);
 }
 public void setString(String input){String raw=input==null?"":input;value=raw.length()>size?raw.substring(0,size):raw;}
 public String getString(){return value;}
 public int getMaxSize(){return size;}
 public int getConstraints(){return constraints;}
}