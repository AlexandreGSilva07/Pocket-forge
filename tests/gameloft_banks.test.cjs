"use strict";
const {test}=require("node:test"),assert=require("node:assert/strict"),P=require("../demo/engine/gameloft-banks.js");
function pack(records,starts=null){
 const base=starts?4+2*starts.length:0,end=base+4*(records.length+1),out=new Uint8Array(end+records.reduce((s,r)=>s+r.length,0)),v=new DataView(out.buffer);
 if(starts){out[2]=starts.length;starts.forEach((s,i)=>v.setUint16(4+2*i,s,true));}
 let pos=end;v.setUint32(base,pos,true);for(let i=0;i<records.length;i++){out.set(records[i],pos);pos+=records[i].length;v.setUint32(base+4*(i+1),pos,true);}
 return out;
}
test("single piece: exact bytes, sprite and PNG tags",()=>{
 const a=Uint8Array.from([2,223,5,7,9]),b=Uint8Array.from([1,137,80,78,71,13,10,26,10]);
 const file=pack([a,b],[0]);new DataView(file.buffer).setUint16(0,2,true);
 const entries=P.parse(file);assert.equal(entries.length,2);
 assert.deepEqual([...entries[0].data],[...a]);assert.equal(entries[0].type,"gameloft_sprite");assert.equal(entries[1].type,"png");
 assert.equal(entries[1].begin,18+a.length);
});
test("split pieces: original global resource index and typed bytes",()=>{
 const a=Uint8Array.from([1,77,84,104,100]),b=Uint8Array.from([2,1,2]),c=Uint8Array.from([0,82,73,70,70]);
 const first=pack([a],[0,1]);new DataView(first.buffer).setUint16(0,3,true);
 const entries=P.parse(first,{1:pack([b,c])});
 assert.deepEqual(entries.map(x=>x.index),[0,1,2]);assert.deepEqual(entries.map(x=>x.type),["midi","binary","wave"]);
 assert.deepEqual([...entries[2].data],[...c]);
});
test("corrupt offsets, missing data and truncated resource rejected",()=>{
 const file=pack([[1,2,3]],[0]);new DataView(file.buffer).setUint16(0,1,true);
 assert.throws(()=>P.parse(file.slice(0,-1)),RangeError);
 const bad=file.slice();new DataView(bad.buffer).setUint32(6,2,true);assert.throws(()=>P.parse(bad),RangeError);
 const multipart=pack([[1,2,3]],[0,1]);new DataView(multipart.buffer).setUint16(0,2,true);
 assert.throws(()=>P.parse(multipart,{}),TypeError);
});