"use strict";
const {test}=require("node:test"),assert=require("node:assert/strict");
const P=require("../demo/engine/pixels.js");
test("RGBA4444 packing roundtrip is exact at nibble endpoints",()=>{
 assert.equal(P.pack(255,0,0,255),0xf00f);
 assert.deepEqual(P.unpack(0x84cf),[136,68,204,255]);
 assert.deepEqual(P.unpack(P.pack(0,255,128,255)),[0,255,136,255]);
});
test("byte budget and clipped draw",()=>{
 const s=P.createSurface(10,10);
 assert.equal(s.pixels.byteLength,200);
 assert.equal(s.set(-1,2,10),false);
 assert.equal(s.rect(-2,-2,5,5,0xf00f),9);
 assert.equal(s.get(0,0),0xf00f);
 assert.equal(s.get(4,4),0);
 assert.throws(()=>P.createSurface(2000,2000),RangeError);
});
test("Bresenham line respects clip and endpoints",()=>{
 const s=P.createSurface(8,8);
 assert.equal(s.line(0,0,7,7,0xffff),8);
 assert.equal(s.get(7,7),0xffff);
 assert.equal(s.line(-2,4,4,4,0xf00f),5);
 assert.equal(s.get(0,4),0xf00f);
});
test("Canvas conversion and upload are exact",()=>{
 const s=P.createSurface(2,1);
 s.set(0,0,0xf00f);s.set(1,0,0x08ff);
 assert.deepEqual([...s.rgba()],[255,0,0,255,0,136,255,255]);
 let uploaded=null;
 const ctx={createImageData(w,h){return {data:new Uint8ClampedArray(w*h*4),width:w,height:h}},
            putImageData(image,x,y){uploaded={image,x,y}}};
 s.flush(ctx,3,4);
 assert.equal(uploaded.x,3);assert.equal(uploaded.y,4);
 assert.deepEqual([...uploaded.image.data],[...s.rgba()]);
});
test("clear resets all 16-bit cells",()=>{
 const s=P.createSurface(4,2);s.clear(0xffff);
 assert.deepEqual([...s.pixels],new Array(8).fill(65535));
 s.clear();assert.deepEqual([...s.pixels],new Array(8).fill(0));
});
