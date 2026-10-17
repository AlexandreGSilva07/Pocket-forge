package demo;
public class Calculator {
  public static int compute(int n){int[] data={1,2,3,4,5}; int sum=0;for(int i=0;i<data.length;i++){if((i&1)==0)sum+=data[i]*n;else sum-=data[i];}return sum;}
  public static void main(String[] args){System.out.println("CALCULATOR="+compute(7));}
}
