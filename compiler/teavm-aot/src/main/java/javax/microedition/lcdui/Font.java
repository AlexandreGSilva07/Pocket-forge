package javax.microedition.lcdui;
public final class Font {
 public static final int FACE_SYSTEM=0,FACE_MONOSPACE=32,FACE_PROPORTIONAL=64;
 public static final int STYLE_PLAIN=0,STYLE_BOLD=1,STYLE_ITALIC=2,STYLE_UNDERLINED=4;
 public static final int SIZE_SMALL=8,SIZE_MEDIUM=0,SIZE_LARGE=16;
 private final int size;
 private Font(int size){this.size=size;}
 public static Font getFont(int face,int style,int size){return new Font(size);}
 public static Font getDefaultFont(){return new Font(SIZE_MEDIUM);}
 public int getHeight(){return size==SIZE_SMALL?12:(size==SIZE_LARGE?20:16);}
 public int charWidth(char c){return size==SIZE_SMALL?7:(size==SIZE_LARGE?12:9);}
 public int charsWidth(char[] chars,int offset,int length){return length*charWidth('M');}
 public int stringWidth(String s){return s==null?0:s.length()*charWidth('M');}
}