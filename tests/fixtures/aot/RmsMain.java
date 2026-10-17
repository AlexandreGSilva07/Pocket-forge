package demo;
import javax.microedition.rms.RecordStore;
/** Persistence fixture, three reloads of the same file:// HTML. */
public final class RmsMain {
 public static void main(String[] args) {
  RecordStore store=RecordStore.openRecordStore("fixture-progress",true);
  int before=store.getNumRecords();
  if(before==0){
   int id=store.addRecord(new byte[]{42,9},0,2);
   if(id!=1)throw new AssertionError("first record id");
  } else {
   if(before!=1||store.getRecord(1)[0]!=42)throw new AssertionError("persisted payload");
   store.setRecord(1,new byte[]{42,9},0,2);
  }
  if(store.getNextRecordID()!=2||store.getSize()!=2)throw new AssertionError("RMS bookkeeping");
  store.closeRecordStore();
  System.out.println("RMS_BEFORE="+before+" RMS_AFTER=1");
 }
}