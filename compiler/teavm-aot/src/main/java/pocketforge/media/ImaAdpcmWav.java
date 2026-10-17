package pocketforge.media;

import java.io.ByteArrayOutputStream;
import java.io.IOException;

/**
 * Generic RIFF/WAVE IMA ADPCM (format 0x0011) to 16-bit PCM decoder.
 * Supports mono and stereo block layouts (4-byte groups/channel).
 *
 * Works offline in TeaVM AOT JavaScript; original game media is neither
 * rewritten nor copied to a game-specific asset table.
 */
public final class ImaAdpcmWav {
 private ImaAdpcmWav() {}
 private static final int[] STEP={
  7,8,9,10,11,12,13,14,16,17,19,21,23,25,28,31,
  34,37,41,45,50,55,60,66,73,80,88,97,107,118,130,143,
  157,173,190,209,230,253,279,307,337,371,408,449,494,544,
  598,658,724,796,876,963,1060,1166,1282,1411,1552,1707,1878,2066,
  2272,2499,2749,3024,3327,3660,4026,4428,4871,5358,5894,6484,7132,
  7845,8630,9493,10442,11487,12635,13899,15289,16818,18500,20350,
  22385,24623,27086,29794,32767
 };
 private static final int[] CHANGE={-1,-1,-1,-1,2,4,6,8};

 public static boolean isImaAdpcm(byte[] src) {
  return src!=null&&src.length>=36&&
   match(src,0,"RIFF")&&match(src,8,"WAVE")&&
   findFormatTag(src)==17;
 }
 private static boolean match(byte[] v,int i,String ascii) {
  if(i<0||i+ascii.length()>v.length)return false;
  for(int j=0;j<ascii.length();j++)if((v[i+j]&255)!=(int)ascii.charAt(j))return false;
  return true;
 }
 private static int u16(byte[] b,int p) {return (b[p]&255)|((b[p+1]&255)<<8);}
 private static int s16(byte[] b,int p){return (short)u16(b,p);}
 private static long u32(byte[] b,int p){
  return ((long)b[p]&255)|(((long)b[p+1]&255)<<8)|
         (((long)b[p+2]&255)<<16)|(((long)b[p+3]&255)<<24);
 }
 private static int findFormatTag(byte[] b){
  int p=12;
  while(p+8<=b.length){
   long size=u32(b,p+4);
   if(size>b.length-p-8)return -1;
   if(match(b,p,"fmt ")&&size>=16)return u16(b,p+8);
   p+=(int)(8+size+(size&1));
  }
  return -1;
 }
 private static int bound(int v,int min,int max){return Math.max(min,Math.min(max,v));}
 private static final class Channel{
  int predictor,index;
  Channel(int predictor,int index){this.predictor=predictor;this.index=index;}
  int step(int code){
   int step=STEP[index];
   // Round once, after summing nibble bits, as specified by IMA DVI ADPCM.
   int delta=(step*((code&7)*2+1))>>3;
   predictor=bound(predictor+((code&8)!=0?-delta:delta),-32768,32767);
   index=bound(index+CHANGE[code&7],0,88);
   return predictor;
  }
 }

 public static byte[] toPcm16Wav(byte[] wav) throws IOException {
  if(!isImaAdpcm(wav))return wav;
  int fmt=-1,data=-1,bytes=0,channels=0,rate=0,align=0,samplesPerBlock=0;
  int fact=-1;
  int p=12;
  while(p+8<=wav.length){
   long size=u32(wav,p+4);
   if(size>wav.length-p-8)throw new IOException("Truncated RIFF chunk");
   if(match(wav,p,"fmt ")){
    if(size<20)throw new IOException("Truncated IMA ADPCM fmt");
    fmt=p+8;
    channels=u16(wav,fmt+2);
    rate=(int)u32(wav,fmt+4);
    align=u16(wav,fmt+12);
    if(u16(wav,fmt+14)!=4)throw new IOException("IMA ADPCM must be 4-bit");
    samplesPerBlock=u16(wav,fmt+18);
   }else if(match(wav,p,"data")){data=p+8;bytes=(int)size;}
   else if(match(wav,p,"fact")&&size>=4){
    long val=u32(wav,p+8);
    if(val<=Integer.MAX_VALUE)fact=(int)val;
   }
   p+=(int)(8+size+(size&1));
  }
  if(fmt<0||data<0||channels<1||channels>2||rate<1000||rate>192000||
    align<=4*channels||align>16384)
   throw new IOException("Unsupported IMA ADPCM WAV layout");
  int capacity=(align-4*channels)*2/channels+1;
  if(samplesPerBlock<1||samplesPerBlock>capacity)throw new IOException("Invalid samplesPerBlock");
  long nblocks=(bytes+align-1L)/align;
  long maximumFrames=nblocks*samplesPerBlock;
  if(maximumFrames>8_000_000L)throw new IOException("Audio duration exceeds decoder limit");
  int limit=(int)(fact>0?Math.min(maximumFrames,fact):maximumFrames);
  if((long)limit*channels*2>32*1024*1024L)throw new IOException("Decoded media exceeds 32 MiB");
  ByteArrayOutputStream pcm=new ByteArrayOutputStream(limit*channels*2);
  int emitted=0;
  for(int block=data;block<data+bytes&&emitted<limit;block+=align){
   int end=Math.min(data+bytes,block+align);
   if(end-block<4*channels)throw new IOException("Incomplete ADPCM channel headers");
   Channel[] states=new Channel[channels];
   int[][] values=new int[channels][samplesPerBlock];
   int[] counts=new int[channels];
   for(int ch=0;ch<channels;ch++){
    int start=block+ch*4;
    int predictor=s16(wav,start);
    int idx=wav[start+2]&255;
    if(idx>88)throw new IOException("Invalid IMA ADPCM step index");
    states[ch]=new Channel(predictor,idx);
    values[ch][0]=predictor;counts[ch]=1;
   }
   int ptr=block+4*channels;
   if(channels==1){
    while(ptr<end&&counts[0]<samplesPerBlock){
     int value=wav[ptr++]&255;
     values[0][counts[0]++]=states[0].step(value&15);
     if(counts[0]<samplesPerBlock)values[0][counts[0]++]=states[0].step(value>>>4);
    }
   }else{
    // IMA WAV stereo interleaves 4-byte groups from each channel.
    while(ptr<end&&counts[0]<samplesPerBlock&&counts[1]<samplesPerBlock){
     for(int ch=0;ch<channels;ch++){
      for(int k=0;k<4&&ptr<end&&counts[ch]<samplesPerBlock;k++){
       int value=wav[ptr++]&255;
       values[ch][counts[ch]++]=states[ch].step(value&15);
       if(counts[ch]<samplesPerBlock)values[ch][counts[ch]++]=states[ch].step(value>>>4);
      }
     }
    }
   }
   int frames=Math.min(counts[0],samplesPerBlock);
   if(channels==2)frames=Math.min(frames,counts[1]);
   frames=Math.min(frames,limit-emitted);
   for(int i=0;i<frames;i++){
    for(int ch=0;ch<channels;ch++){
     int sample=values[ch][i];
     pcm.write(sample&255);pcm.write((sample>>>8)&255);
    }
   }
   emitted+=frames;
  }
  byte[] raw=pcm.toByteArray();
  byte[] out=new byte[44+raw.length];
  writeAscii(out,0,"RIFF");write32(out,4,36+raw.length);
  writeAscii(out,8,"WAVE");writeAscii(out,12,"fmt ");
  write32(out,16,16);write16(out,20,1);write16(out,22,channels);
  write32(out,24,rate);write32(out,28,rate*channels*2);
  write16(out,32,channels*2);write16(out,34,16);
  writeAscii(out,36,"data");write32(out,40,raw.length);
  System.arraycopy(raw,0,out,44,raw.length);
  return out;
 }
 private static void writeAscii(byte[] dest,int start,String text){
  for(int i=0;i<text.length();i++)dest[start+i]=(byte)text.charAt(i);
 }
 private static void write16(byte[] dest,int start,int value){
  dest[start]=(byte)value;dest[start+1]=(byte)(value>>>8);
 }
 private static void write32(byte[] dest,int start,int value){
  write16(dest,start,value);write16(dest,start+2,value>>>16);
 }
}
