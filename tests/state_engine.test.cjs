"use strict";
const assert = require("node:assert/strict");
const { test } = require("node:test");
const { createStore } = require("../demo/engine/state.js");
function storage() {
  const data = new Map();
  return { getItem:k=>data.has(k)?data.get(k):null, setItem:(k,v)=>data.set(k,v), data };
}
test("durable versioned save across new store instances", () => {
  const s=storage();
  assert.equal(createStore(s,{namespace:"game"}).writeNumber("score",123),true);
  assert.equal(createStore(s,{namespace:"game"}).readNumber("score"),123);
  assert.equal(createStore(s,{namespace:"game",version:2}).readNumber("score",7),7);
});
test("corrupt snapshots are rejected without crashing the game", () => {
  const s=storage();s.setItem("game:v1:score","{broken");
  assert.equal(createStore(s,{namespace:"game"}).readNumber("score",0),0);
  s.setItem("game:v1:score",JSON.stringify({schema:99,data:100}));
  assert.equal(createStore(s,{namespace:"game"}).readNumber("score",0),0);
});
test("block all storage access: in-memory session fallback works", () => {
  const deny={getItem(){throw Error("blocked")},setItem(){throw Error("blocked")}};
  const store=createStore(deny,{namespace:"offline"});
  assert.equal(store.writeNumber("best",42),false);
  assert.equal(store.readNumber("best"),42);
  const second=createStore(deny,{namespace:"offline"});
  assert.equal(second.readNumber("best"),0);
});
test("snapshots have size budget and validate record keys", () => {
  const s=storage(),store=createStore(s,{namespace:"game",maxBytes:150});
  assert.throws(()=>store.writeJSON("state",{big:"x".repeat(200)}),RangeError);
  assert.throws(()=>store.readNumber("../secret"),TypeError);
  assert.throws(()=>store.writeNumber("score",NaN),RangeError);
  assert.throws(()=>store.writeNumber("score",-10),RangeError);
});
test("legacy score migrates once, without destroying old key", () => {
  const s=storage();s.setItem("pocketforge-lumen-best","85");
  const store=createStore(s,{namespace:"lumen-shift"});
  assert.equal(store.migrateLegacyNumber("pocketforge-lumen-best","best"),true);
  assert.equal(store.readNumber("best"),85);
  assert.equal(store.migrateLegacyNumber("pocketforge-lumen-best","best"),false);
  assert.equal(s.getItem("pocketforge-lumen-best"),"85");
});
test("JSON snapshots roundtrip with independent namespaces", () => {
  const s=storage(),a=createStore(s,{namespace:"a"}),b=createStore(s,{namespace:"b"});
  a.writeJSON("state",{level:2,items:[1,4]});
  assert.deepEqual(createStore(s,{namespace:"a"}).readJSON("state"),{level:2,items:[1,4]});
  assert.equal(b.readJSON("state"),null);
});
