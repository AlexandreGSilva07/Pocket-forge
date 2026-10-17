package javax.microedition.lcdui;
public abstract class Item {
 protected String label;
 protected Item(String label){this.label=label;}
 public String getLabel(){return label;}
 public void setLabel(String label){this.label=label;}
}