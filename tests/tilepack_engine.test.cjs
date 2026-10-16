"use strict";
const {test}=require("node:test"),assert=require("node:assert/strict");
const P=require("../demo/engine/tilepack.js");
test("legacy 8-bit 37x30 levels follow observed header/stride",()=>{
 const a=new Uint8Array(5+37*30+1);
 a.set([37,30,16,16,1]);a.fill(7,5,5+37*30);a[a.length-1]=0;
 const d=P.decodeLegacyLevel(a);
 assert.equal(d.tiles.length,1110);assert.equal(d.tiles[1099],7);assert.equal(d.flags,null);
});
test("legacy 16-bit two planes and optional third layer",()=>{
 const count=37*30;
 const a=new Uint8Array(5+count*2+1+count);
 a.set([37,30,16,16,2]);a[5]=0x34;a[6]=0x12;
 a[5+count*2]=1;a[a.length-1]=42;
 const d=P.decodeLegacyLevel(a);
 assert.equal(d.tiles[0],0x1234);assert.equal(d.flags.at(-1),42);
 assert.equal(d.tiles.length,1110);assert.equal(d.flags.length,1110);
});
test("legacy formats reject corruption and bounds violations",()=>{
 assert.throws(()=>P.decodeLegacyLevel(Uint8Array.from([37,30,16,16,2])),RangeError);
 assert.throws(()=>P.decodeLegacyLevel(Uint8Array.from([0,30,16,16,1])),RangeError);
 const a=new Uint8Array(5+4*2+1);a.set([2,2,16,16,2]);a.at(13);
 a[13]=2;assert.throws(()=>P.decodeLegacyLevel(a),RangeError);
});
test("PocketForge own level format roundtrips",()=>{
 const d={cols:8,rows:8,tileWidth:24,tileHeight:24,tiles:Uint8Array.from({length:64},(_,i)=>i%4)};
 const encoded=P.encodePFLevel(d);const restored=P.decodePFLevel(encoded);
 assert.deepEqual([...restored.tiles],[...d.tiles]);
 assert.equal(restored.tileWidth,24);
 assert.throws(()=>P.decodePFLevel(encoded.slice(0,12)),RangeError);
});
