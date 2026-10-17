package javax.microedition.rms;
import java.util.ArrayList;
import java.util.HashMap;
public final class RecordStore {
 private static final HashMap<String,RecordStore> STORES=new HashMap<String,RecordStore>();
 private final ArrayList<byte[]> records=new ArrayList<byte[]>();
 private RecordStore(){}
 public static RecordStore openRecordStore(String name,boolean create){
   RecordStore store=STORES.get(name);
   if(store==null&&create){store=new RecordStore();STORES.put(name,store);}
   if(store==null)throw new IllegalStateException("RecordStore missing: "+name);
   return store;
 }
 public int addRecord(byte[] src,int offset,int length){byte[] item=new byte[length];
   System.arraycopy(src,offset,item,0,length);records.add(item);return records.size();}
 public int getNumRecords(){return records.size();}
 public byte[] getRecord(int id){return records.get(id-1).clone();}
 public void setRecord(int id,byte[] src,int offset,int length){byte[] item=new byte[length];
   System.arraycopy(src,offset,item,0,length);records.set(id-1,item);}
 public void closeRecordStore(){}
 public static void deleteRecordStore(String name){STORES.remove(name);}
}