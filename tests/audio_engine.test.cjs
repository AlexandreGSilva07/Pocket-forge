"use strict";
const assert=require("node:assert/strict");
const {test}=require("node:test");
const {createAudio}=require("../demo/engine/audio.js");
function fakeHost(){
  const oscs=[];
  class AC{
    constructor(){this.state="running";this.currentTime=4;this.destination={};}
    createOscillator(){
      const o={frequency:{setValueAtTime(){},exponentialRampToValueAtTime(){}},
        connect(){},disconnect(){},start(){},stop(){},onended:null};
      oscs.push(o);return o;
    }
    createGain(){return {gain:{setValueAtTime(){},exponentialRampToValueAtTime(){}},connect(){},disconnect(){}};}
    close(){this.state="closed";return Promise.resolve();}
  }
  return {AudioContext:AC,oscs};
}
test("lazy audio: no node created before unlock",()=>{
  const h=fakeHost(),a=createAudio(h);assert.equal(a.play(440),false);
  assert.equal(h.oscs.length,0);assert.equal(a.unlock(),true);
  assert.equal(a.play(440),true);assert.equal(h.oscs.length,1);
});
test("voice budget stops burst, and onended frees capacity",()=>{
  const h=fakeHost(),a=createAudio(h,{maxVoices:2});a.unlock();
  assert.equal(a.play(330),true);assert.equal(a.play(550),true);
  assert.equal(a.play(660),false);assert.equal(a.voices,2);
  h.oscs[0].onended();assert.equal(a.voices,1);
  assert.equal(a.play(660),true);assert.equal(a.voices,2);
});
test("muted, unsupported host and disposed audio fail cleanly",()=>{
  const a=createAudio(null);assert.equal(a.unlock(),false);
  const h=fakeHost(),b=createAudio(h);b.unlock();b.setMuted(true);
  assert.equal(b.play(440),false);b.setMuted(false);
  assert.equal(b.play(440),true);b.dispose();
  assert.equal(b.unlock(),false);assert.equal(b.play(440),false);
});
test("invalid parameters cannot create nodes",()=>{
  const h=fakeHost(),a=createAudio(h);a.unlock();
  for(const f of [0,NaN,Infinity,40000])assert.equal(a.play(f),false);
  assert.equal(a.play(440,0),false);
  assert.equal(a.play(440,.1,"invalid"),false);
  assert.equal(a.play(440,.1,"sine",3),false);
  assert.equal(h.oscs.length,0);
});
test("suspended context requests resume without throwing",()=>{
  let called=0;
  class AC{constructor(){this.state="suspended";}resume(){called++;return Promise.reject(new Error("locked"));}}
  const a=createAudio({AudioContext:AC});assert.equal(a.unlock(),true);
  assert.equal(called,1);assert.equal(a.play(500),false);
});
