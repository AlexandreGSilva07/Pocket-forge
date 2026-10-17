"use strict";
const {test}=require("node:test"),assert=require("node:assert/strict");
const {keys}=require("../demo/engine/gameloft-input.js");
test("press-hold-release matches bytecode counter transitions",()=>{
 const k=keys();k.down(2);assert.equal(k.frame()[2],1);assert.equal(k.held(2),true);
 k.down(2);assert.equal(k.frame()[2],2);k.up(2);assert.equal(k.frame()[2],-3);
 assert.equal(k.held(2),false);assert.equal(k.frame()[2],0);
 k.down(2);assert.equal(k.frame()[2],1);
});
test("indices >=18 emit short pulses",()=>{const k=keys();k.down(18);assert.equal(k.frame()[18],1);assert.equal(k.frame()[18],-2);assert.equal(k.frame()[18],0);});
test("held time stops at 126, reset and invalid IDs are checked",()=>{
 const k=keys(1);k.down(0);for(let i=0;i<150;i++)k.frame();
 assert.equal(k.frame()[0],126);k.reset();assert.equal(k.frame()[0],0);assert.throws(()=>k.down(7),RangeError);
});