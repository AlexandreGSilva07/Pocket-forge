"use strict";
const assert = require("node:assert/strict");
const { test } = require("node:test");
const P = require("../demo/engine/compact.js");

test("RLE is lossless for alternating, long runs and zeros", () => {
  for (const source of [
    Uint8Array.from([0,0,1,1,2,3,3,3,0]),
    new Uint8Array(500).fill(255),
    new Uint8Array(0),
    Uint8Array.from({ length: 200 }, (_, i) => i % 2)
  ]) {
    assert.deepEqual(P.decodeRLE(P.encodeRLE(source), source.length), source);
  }
});
test("RLE refuses malformed or dangerous input", () => {
  assert.throws(() => P.decodeRLE(Uint8Array.from([0,1]),1));
  assert.throws(() => P.decodeRLE(Uint8Array.from([5,1]),2));
  assert.throws(() => P.decodeRLE(Uint8Array.from([1,1,2]),2));
  assert.throws(() => P.decodeRLE(Uint8Array.from([1,1]),2));
  assert.throws(() => P.encodeRLE([256]));
});
test("tile generator creates ordered rectangular typed map", () => {
  assert.deepEqual([...P.createTileMap(3,2,(x,y)=>x+y*3).tiles],[0,1,2,3,4,5]);
  assert.throws(() => P.createTileMap(0,2,()=>1));
  assert.throws(() => P.createTileMap(2,2,()=>-1));
});
test("renderer culls offscreen tiles and skips empty cells", () => {
  const draws = [];
  const ctx={drawImage(...args){draws.push(args)}};
  const atlas={width:48*4,height:48};
  const map=P.createTileMap(10,10,(x,y)=>x===4&&y===4?0:1);
  const count=P.drawTileMap(ctx,atlas,map,{size:48,cameraX:48*3,cameraY:48*3,viewWidth:96,viewHeight:96});
  assert.equal(count,3);
  assert.equal(draws.length,3);
  assert.deepEqual(draws[0].slice(1),[48,0,48,48,0,0,48,48]);
});
test("generator and RLE roundtrip preserve deterministic tilemap", () => {
  const map=P.createTileMap(50,20,(x,y)=>((x*17+y*29)%13===0?2:1));
  const binary=P.encodeRLE(map.tiles);
  assert.deepEqual(P.decodeRLE(binary,1000),map.tiles);
});
