package javax.microedition.midlet;
public abstract class MIDlet {
 protected abstract void startApp();
 protected abstract void pauseApp();
 protected abstract void destroyApp(boolean unconditional);
 public final void __pocketforgeStart(){startApp();}
 public void notifyDestroyed(){} public void notifyPaused(){}
 public final void resumeRequest(){}
 public boolean platformRequest(String url){return false;}
 public String getAppProperty(String key){return null;}
}