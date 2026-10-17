/* Bounded Java-free JAR ZIP reader: stored/deflate-raw, CRC32, central directory.
 * Independent implementation; doesn't execute Java bytecode or ship game assets.
 * Rejects encrypted, multi-disk and ZIP64 files.
 */
(function(root,factory){"use strict";const api=factory();
 if(typeof module==="object"&&module.exports)module.exports=api;
 if(root)root.PocketForgeJarReader=api;
})(typeof window!=="undefined"?window:typeof globalThis!=="undefined"?globalThis:null,function(){
"use strict";
const TABLE=Uint32Array.from({length:256},(_,i)=>{let c=i;for(let j=0;j<8;j++)c=(c&1)?(0xEDB88320^(c>>>1)):(c>>>1);return c>>>0;});
function crc32(a){let c=0xffffffff;for(const x of a)c=TABLE[(c^x)&255]^(c>>>8);return (c^0xffffffff)>>>0;}
function readZIP(input,{maxArchive=64*1024*1024,maxEntry=32*1024*1024,maxEntries=10000}={}){
 const a=input instanceof Uint8Array?input:new Uint8Array(input);
 if(a.length<22||a.length>maxArchive)throw new RangeError("invalid JAR size");
 const d=new DataView(a.buffer,a.byteOffset,a.byteLength),u16=i=>d.getUint16(i,true),u32=i=>d.getUint32(i,true);
 let eocd=-1;
 for(let i=a.length-22;i>=Math.max(0,a.length-65557);i--){if(u32(i)===0x06054b50&&i+22+u16(i+20)===a.length){eocd=i;break;}}
 if(eocd<0)throw new RangeError("ZIP directory not found");
 if(u16(eocd+4)!==0||u16(eocd+6)!==0)throw new RangeError("multi-disk ZIP unsupported");
 const count=u16(eocd+10),offset=u32(eocd+16),size=u32(eocd+12);
 if(count>maxEntries||offset+size>eocd)throw new RangeError("invalid central directory");
 const entries=new Map();let pos=offset;
 for(let i=0;i<count;i++){
  if(pos+46>eocd||u32(pos)!==0x02014b50)throw new RangeError("corrupt central header");
  const flags=u16(pos+8),method=u16(pos+10),packed=u32(pos+20),raw=u32(pos+24);
  const nameLen=u16(pos+28),extra=u16(pos+30),comment=u16(pos+32),local=u32(pos+42);
  const next=pos+46+nameLen+extra+comment;
  if(next>eocd||local+30>a.length||u32(local)!==0x04034b50)throw new RangeError("invalid local member");
  if(flags&1||raw===0xffffffff||packed===0xffffffff||local===0xffffffff)throw new RangeError("encrypted/ZIP64 not supported");
  if(method!==0&&method!==8)throw new RangeError("ZIP compression method not supported");
  if(raw>maxEntry||packed>maxArchive)throw new RangeError("ZIP entry exceeds size cap");
  const name=new TextDecoder("utf-8").decode(a.subarray(pos+46,pos+46+nameLen));
  if(!name.endsWith("/")){
   if(entries.has(name))throw new RangeError("duplicate ZIP member");
   const start=local+30+u16(local+26)+u16(local+28);
   if(start+packed>offset)throw new RangeError("ZIP entry overlaps directory");
   entries.set(name,{name,method,crc:u32(pos+16),compressedBytes:packed,uncompressedBytes:raw,start});
  }
  pos=next;
 }
 return {names:[...entries.keys()],async get(name){
  const e=entries.get(name);if(!e)throw new Error("missing JAR member: "+name);
  const chunk=a.subarray(e.start,e.start+e.compressedBytes);
  let out;
  if(e.method===0)out=chunk.slice();
  else {
   if(typeof DecompressionStream!=="function")throw new Error("Browser needs DecompressionStream(deflate-raw)");
   const stream=new Blob([chunk]).stream().pipeThrough(new DecompressionStream("deflate-raw"));
   const reader=stream.getReader(),chunks=[];let amount=0;
   try{while(true){const {value,done}=await reader.read();if(done)break;amount+=value.byteLength;if(amount>maxEntry){await reader.cancel();throw new RangeError("ZIP expanded beyond cap");}chunks.push(value);}}finally{reader.releaseLock();}
   out=new Uint8Array(amount);let at=0;for(const c of chunks){out.set(c,at);at+=c.byteLength;}
  }
  if(out.length!==e.uncompressedBytes||out.length>maxEntry)throw new RangeError("ZIP expanded size mismatch");
  if(crc32(out)!==e.crc)throw new RangeError("ZIP CRC32 mismatch");
  return out;
 }};
}
return Object.freeze({readZIP,crc32});
});