/* PocketForge: original JavaScript implementation of the resource-bank layout
 * verified against the user's Asphalt Nitro 1.1.7 JAR.
 * No JVM, third-party resources, Java bytecode or MIDP runtime required.
 */
(function(root, factory){
 "use strict";const api=factory();
 if(typeof module==="object" && module.exports)module.exports=api;
 if(root)root.PocketForgeGameloftBanks=api;
})(typeof window!=="undefined"?window:typeof globalThis!=="undefined"?globalThis:null,function(){
 "use strict";
 const MAX_PARTS=32,MAX_RECORDS=10000,MAX_BYTES=64*1024*1024;
 function bytes(x){if(x instanceof Uint8Array)return x;if(x instanceof ArrayBuffer)return new Uint8Array(x);throw new TypeError("part must be ArrayBuffer or Uint8Array");}
 function u16(a,i){return a[i]|(a[i+1]<<8);}
 function u32(a,i){return (a[i]|(a[i+1]<<8)|(a[i+2]<<16)|(a[i+3]<<24))>>>0;}
 function classify(payload){
  const b=payload;if(!b.length)return {type:"empty",tag:null};
  const tag=b[0],ofs=tag<=2?1:0;
  function prefix(seq){return b.length>=ofs+seq.length&&seq.every((v,k)=>b[ofs+k]===v);}
  if(prefix([137,80,78,71,13,10,26,10]))return {type:"png",tag};
  if(prefix([77,84,104,100]))return {type:"midi",tag};
  if(prefix([82,73,70,70]))return {type:"wave",tag};
  if(prefix([255,216,255]))return {type:"jpeg",tag};
  if(prefix([223,5]))return {type:"gameloft_sprite",tag};
  return {type:"binary",tag};
 }
 // Input consists of uncompressed JAR ZIP entries: base ("6") and parts ("6.1"...).
 // No ZIP parser is embedded; callers may use unzip or an independent ZIP adapter.
 function parse(main,tail={}, {maxParts=MAX_PARTS,maxRecords=MAX_RECORDS,maxBytes=MAX_BYTES}={}){
  const header=bytes(main);
  if(header.length<8||header.length>maxBytes)throw new RangeError("invalid bank header or size");
  const total=u16(header,0),count=header[2];
  if(!count||count>maxParts||count>MAX_PARTS)throw new RangeError("invalid part count");
  if(!total||total>maxRecords||total>MAX_RECORDS)throw new RangeError("invalid record count");
  const headEnd=4+2*count;
  if(header.length<headEnd)throw new RangeError("truncated split index");
  const starts=[];for(let i=0;i<count;i++)starts.push(u16(header,4+2*i));
  starts.push(total);
  if(starts[0]!==0||starts.some((s,i)=>i>0&&s<=starts[i-1]))throw new RangeError("non-monotonic part indices");
  const out=[];
  for(let part=0;part<count;part++){
   const raw=part===0?header:bytes(tail instanceof Map?tail.get(part):Array.isArray(tail)?tail[part]:(tail[part]??tail[String(part)]));
   if(raw.length>maxBytes)throw new RangeError("part exceeds byte limit");
   const n=starts[part+1]-starts[part],beginTable=part===0?headEnd:0;
   const afterTable=beginTable+4*(n+1);
   if(afterTable>raw.length)throw new RangeError("truncated offset table");
   let prev=u32(raw,beginTable);
   if(prev<afterTable)throw new RangeError("offset table overlaps resource");
   const offsets=[prev];
   for(let i=1;i<=n;i++){
    const next=u32(raw,beginTable+4*i);
    if(next<prev||next>raw.length)throw new RangeError("invalid offsets");
    offsets.push(next);prev=next;
   }
   if(offsets[n]!==raw.length)throw new RangeError("unexpected tail bytes");
   for(let i=0;i<n;i++){
    const begin=offsets[i],end=offsets[i+1],data=raw.slice(begin,end);
    out.push({index:starts[part]+i,part,begin,end,data,...classify(data)});
   }
  }
  if(out.length!==total)throw new RangeError("record count mismatch");
  return out;
 }
 return Object.freeze({parse,classify});
});
