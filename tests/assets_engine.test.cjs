"use strict";
const {test}=require("node:test"),assert=require("node:assert/strict");
const A=require("../demo/engine/assets.js");
const PNG=Uint8Array.from([137,80,78,71,13,10,26,10,1,2,3]);
function legacy(list){
 const chunks=list.map(x=>Uint8Array.from([x.length>>8,x.length&255,...x]));
 return Uint8Array.from(chunks.flatMap(a=>[...a]));
}
test("legacy length prefix is big-endian, with PNG/binary classification",()=>{
 const out=A.legacyEntries(legacy([PNG,Uint8Array.from([4,5,6])]));
 assert.equal(out.length,2);assert.equal(out[0].type,"png");
 assert.equal(out[1].type,"binary");
 assert.deepEqual([...out[0].data],[...PNG]);
});
test("legacy parser refuses truncation and invalid chunk count",()=>{
 assert.throws(()=>A.legacyEntries(Uint8Array.from([0,12,1,2])),RangeError);
 assert.throws(()=>A.legacyEntries(Uint8Array.from([0])),RangeError);
 assert.throws(()=>A.legacyEntries(Uint8Array.from([0,0])),RangeError);
 assert.throws(()=>A.legacyEntries(legacy([PNG,PNG]),{maxEntries:1}),RangeError);
 assert.throws(()=>A.legacyEntries(legacy([[1,2]]),{requirePng:true}),RangeError);
});
test("new PFB1 pack preserves mixed resources exactly",()=>{
 const entries=[{type:"png",data:PNG},{type:"binary",data:Uint8Array.from([0,255,7])}];
 const packed=A.encode(entries),restored=A.decode(packed);
 assert.equal(String.fromCharCode(...packed.slice(0,4)),"PFB1");
 assert.deepEqual(restored,entries);
 assert.equal(packed.length,6+5+PNG.length+5+3);
});
test("new pack rejects invalid entries and trailing data",()=>{
 assert.throws(()=>A.encode([{type:"png",data:Uint8Array.from([1])}]),RangeError);
 assert.throws(()=>A.encode([{type:"sound",data:PNG}]),TypeError);
 const pack=A.encode([{type:"binary",data:Uint8Array.from([1])}]);
 assert.throws(()=>A.decode(pack.slice(0,-1)),RangeError);
 assert.throws(()=>A.decode(Uint8Array.from([...pack,3])),RangeError);
 assert.deepEqual(A.decode(A.encode([])),[]);
});
