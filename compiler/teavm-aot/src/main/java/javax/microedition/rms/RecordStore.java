package javax.microedition.rms;

import java.util.ArrayList;
import java.util.HashMap;
import org.teavm.jso.JSBody;

/** Synchronous, persistent, record-id-stable MIDP RMS adapter.
 * Stores are isolated by an AOT-generated application namespace and backed by
 * localStorage within the browser's current file:// origin.
 * No record data leaves the browser. Throws on denied/full storage.
 */
public final class RecordStore {
 private static final HashMap<String,RecordStore> STORES=new HashMap<String,RecordStore>();
 private static final int MAX_RECORD_BYTES=1024*1024;
 private final String name;
 private final ArrayList<byte[]> records=new ArrayList<byte[]>();
 private boolean closed;
 private RecordStore(String name){this.name=name;}

 @JSBody(params={"name"},script=
  "try{var ns=window.PocketForgeConfig.storageNamespace;return localStorage.getItem('PF:RMS:v1:'+ns+':'+encodeURIComponent(name))}"+
  "catch(e){return null;}")
 private static native String readStorage(String name);
 @JSBody(params={"name","value"},script=
  "try{var ns=window.PocketForgeConfig.storageNamespace;localStorage.setItem('PF:RMS:v1:'+ns+':'+encodeURIComponent(name),value);return true}"+
  "catch(e){console.warn('RMS save failed:',e.message);return false}")
 private static native boolean writeStorage(String name,String value);
 @JSBody(params={"name"},script=
  "try{var ns=window.PocketForgeConfig.storageNamespace;localStorage.removeItem('PF:RMS:v1:'+ns+':'+encodeURIComponent(name));return true}"+
  "catch(e){console.warn('RMS delete failed:',e.message);return false}")
 private static native boolean removeStorage(String name);

 private static char nibble(int i){return "0123456789abcdef".charAt(i&15);}
 private static String hex(byte[] data){
  StringBuilder s=new StringBuilder(data.length*2);
  for(byte b:data){s.append(nibble((b&255)>>4));s.append(nibble(b));}
  return s.toString();
 }
 private static int hexDigit(char c){
  int n=Character.digit(c,16);
  if(n<0)throw new IllegalStateException("Corrupt RMS hex");
  return n;
 }
 private static byte[] unhex(String s){
  if((s.length()&1)!=0)throw new IllegalStateException("Corrupt RMS record");
  byte[] out=new byte[s.length()/2];
  for(int i=0;i<out.length;i++)out[i]=(byte)((hexDigit(s.charAt(i*2))<<4)|hexDigit(s.charAt(i*2+1)));
  return out;
 }
 private static RecordStore decode(String name,String text){
  if(!text.startsWith("v1;"))throw new IllegalStateException("Unknown RMS storage format");
  String[] items=text.split(";",-1);
  if(items.length<2)throw new IllegalStateException("Truncated RMS storage");
  int count=Integer.parseInt(items[1]);
  if(count<0||count>100000||items.length!=count+2)throw new IllegalStateException("Corrupt RMS record IDs");
  RecordStore store=new RecordStore(name);
  for(int i=2;i<items.length;i++){
   store.records.add(items[i].equals("-")?null:unhex(items[i]));
  }
  return store;
 }
 private String serialize(){
  StringBuilder sb=new StringBuilder("v1;").append(records.size());
  for(byte[] record:records)sb.append(';').append(record==null?"-":hex(record));
  return sb.toString();
 }
 private void persist(){
  if(!writeStorage(name,serialize()))throw new IllegalStateException("RMS persistent storage denied or full");
 }
 private void checkOpen(){if(closed)throw new IllegalStateException("RecordStore closed");}
 private static void checkSlice(byte[] src,int offset,int length){
  if(src==null)throw new NullPointerException();
  if(offset<0||length<0||offset>src.length-length||length>MAX_RECORD_BYTES)
   throw new IllegalArgumentException("Invalid RMS record slice");
 }
 private byte[] recordAt(int id){
  checkOpen();
  if(id<1||id>records.size()||records.get(id-1)==null)
   throw new IllegalArgumentException("Invalid RMS record ID "+id);
  return records.get(id-1);
 }
 public static RecordStore openRecordStore(String name,boolean create){
  if(name==null||name.length()==0)throw new IllegalArgumentException("Invalid RMS name");
  RecordStore existing=STORES.get(name);
  if(existing!=null){existing.closed=false;return existing;}
  String encoded=readStorage(name);
  if(encoded==null&&!create)throw new IllegalStateException("RecordStore missing: "+name);
  RecordStore store=encoded==null?new RecordStore(name):decode(name,encoded);
  if(encoded==null)store.persist();
  STORES.put(name,store);
  return store;
 }
 public int addRecord(byte[] src,int offset,int length){
  checkOpen();checkSlice(src,offset,length);
  byte[] copy=new byte[length];System.arraycopy(src,offset,copy,0,length);
  records.add(copy);
  try{persist();}catch(RuntimeException ex){records.remove(records.size()-1);throw ex;}
  return records.size();
 }
 public int getNumRecords(){
  checkOpen();int count=0;for(byte[] item:records)if(item!=null)count++;return count;
 }
 public int getNextRecordID(){checkOpen();return records.size()+1;}
 public int getSize(){checkOpen();int size=0;for(byte[] a:records)if(a!=null)size+=a.length;return size;}
 public byte[] getRecord(int id){return recordAt(id).clone();}
 public int getRecord(int id,byte[] buffer,int offset){
  byte[] src=recordAt(id);
  if(buffer==null)throw new NullPointerException();
  if(offset<0||offset>buffer.length-src.length)throw new IllegalArgumentException("RMS buffer too small");
  System.arraycopy(src,0,buffer,offset,src.length);
  return src.length;
 }
 public int getRecordSize(int id){return recordAt(id).length;}
 public void setRecord(int id,byte[] src,int offset,int length){
  checkSlice(src,offset,length);recordAt(id);
  byte[] copy=new byte[length];System.arraycopy(src,offset,copy,0,length);
  byte[] previous=records.set(id-1,copy);
  try{persist();}catch(RuntimeException ex){records.set(id-1,previous);throw ex;}
 }
 public void deleteRecord(int id){
  recordAt(id);byte[] previous=records.set(id-1,null);
  try{persist();}catch(RuntimeException ex){records.set(id-1,previous);throw ex;}
 }
 public void closeRecordStore(){closed=true;}
 public static void deleteRecordStore(String name){
  if(name==null)throw new NullPointerException();
  if(!removeStorage(name))throw new IllegalStateException("RMS deletion denied");
  STORES.remove(name);
 }
}