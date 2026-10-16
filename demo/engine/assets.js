/* PocketForge Asset Pack v1.
 * New, independently specified game-resource container plus read-only helper
 * for historical big-endian short-length sequences (3D Balloon Race study).
 * No third-party assets, engine code or Java APIs embedded here.
 */
(function(root, factory){
 "use strict";
 const api=factory();
 if(typeof module==="object"&&module.exports)module.exports=api;
 if(root)root.PocketForgeAssets=api;
})(typeof window!=="undefined"?window:(typeof globalThis!=="undefined"?globalThis:null),function(){
 "use strict";
 const PNG=Uint8Array.from([137,80,78,71,13,10,26,10]);
 const MAX_BYTES=16*1024*1024;
 const isPNG=a=>a.length>=8&&PNG.every((n,i)=>a[i]===n);
 function bytes(v){
   if(v instanceof Uint8Array)return v;
   if(v instanceof ArrayBuffer)return new Uint8Array(v);
   throw new TypeError("Expected ArrayBuffer or Uint8Array");
 }
 function legacyEntries(raw,{maxEntries=256,maxChunkBytes=32767,requirePng=false}={}){
   const data=bytes(raw);
   if(data.byteLength>MAX_BYTES)throw new RangeError("legacy package exceeds budget");
   if(!Number.isInteger(maxEntries)||maxEntries<1||maxEntries>65535)throw new RangeError("bad entry budget");
   if(!Number.isInteger(maxChunkBytes)||maxChunkBytes<1||maxChunkBytes>32767)
      throw new RangeError("bad legacy chunk budget");
   const result=[];let offset=0;
   while(offset<data.length){
     if(result.length>=maxEntries)throw new RangeError("too many entries");
     if(offset+2>data.length)throw new RangeError("truncated big-endian length");
     const size=(data[offset]<<8)|data[offset+1];offset+=2;
     if(size===0||size>maxChunkBytes||offset+size>data.length)throw new RangeError("bad legacy entry size");
     const payload=data.slice(offset,offset+size),type=isPNG(payload)?"png":"binary";
     if(requirePng&&type!=="png")throw new RangeError("non-PNG entry in PNG-only package");
     result.push({type,data:payload});
     offset+=size;
   }
   return result;
 }
 // PFB1 = 4-byte magic, uint16 count, then (type:uint8,length:uint32be, bytes).
 function encode(entries){
   if(!Array.isArray(entries)||entries.length>1024)throw new RangeError("bad entry count");
   let length=6;
   const safe=entries.map(entry=>{
     if(!entry||!["png","binary"].includes(entry.type))throw new TypeError("entry must have png/binary type");
     const d=bytes(entry.data);
     if(entry.type==="png"&&!isPNG(d))throw new RangeError("PNG must have correct signature");
     length+=5+d.length;
     if(d.length>MAX_BYTES||length>MAX_BYTES)throw new RangeError("asset package exceeds budget");
     return {type:entry.type,data:d};
   });
   const out=new Uint8Array(length),view=new DataView(out.buffer);
   out.set([80,70,66,49,entries.length>>>8,entries.length&255]);let offset=6;
   for(const item of safe){
     out[offset++]=item.type==="png"?1:2;
     view.setUint32(offset,item.data.length);offset+=4;
     out.set(item.data,offset);offset+=item.data.length;
   }
   return out;
 }
 function decode(raw){
   const d=bytes(raw);
   if(d.length<6||d.length>MAX_BYTES||d[0]!==80||d[1]!==70||d[2]!==66||d[3]!==49)
     throw new RangeError("invalid PFB1 header");
   const count=(d[4]<<8)|d[5];if(count>1024)throw new RangeError("too many entries");
   const out=[];const view=new DataView(d.buffer,d.byteOffset,d.byteLength);let offset=6;
   for(let i=0;i<count;i++){
     if(offset+5>d.length)throw new RangeError("truncated resource header");
     const kind=d[offset++],size=view.getUint32(offset);offset+=4;
     if((kind!==1&&kind!==2)||size>MAX_BYTES||size>d.length-offset)throw new RangeError("invalid resource");
     const value=d.slice(offset,offset+size);
     if(kind===1&&!isPNG(value))throw new RangeError("PNG signature mismatch");
     out.push({type:kind===1?"png":"binary",data:value});
     offset+=size;
   }
   if(offset!==d.length)throw new RangeError("extra trailing bytes");
   return out;
 }
 return Object.freeze({isPNG,legacyEntries,encode,decode});
});
