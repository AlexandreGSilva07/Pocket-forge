"use strict";
const assert=require("node:assert/strict");
const {test}=require("node:test");
const {searchBestMove}=require("../demo/engine/ai.js");

function stones(n){
  const state={remaining:n,turn:0};
  const opts={
    state,depth:12,maxNodes:100000,maximizing:true,
    legalMoves:s=>Array.from({length:Math.min(3,s.remaining)},(_,i)=>i+1),
    applyMove(s,n){const saved=s.remaining;s.remaining-=n;s.turn++;return saved;},
    undoMove(s,n,who,old){s.remaining=old;s.turn--;},
    isTerminal:s=>s.remaining<=0,
    evaluate:s=>s.remaining===0?(s.turn%2===1?100:-100):0
  };
  return {state,opts};
}
test("AI decides winning move without modifying game state",()=>{
  const {state,opts}=stones(6);
  const before=structuredClone(state);
  const r=searchBestMove(opts);
  assert.equal(r.move,2);
  assert.deepEqual(state,before);
  assert.equal(r.budgetHit,false);
  assert.ok(r.nodes>0);
});
test("minimizing side is supported",()=>{
  const s={value:0};
  const o={
    state:s,depth:1,maximizing:false,
    legalMoves:()=>[3,1,2],
    applyMove:(x,n)=>{const old=x.value;x.value=n;return old;},
    undoMove:(x,n,p,old)=>{x.value=old;},
    isTerminal:()=>false,evaluate:x=>x.value
  };
  assert.equal(searchBestMove(o).move,1);
  assert.equal(s.value,0);
});
test("cutoff budget and branching bounded",()=>{
  const {state,opts}=stones(20);
  opts.depth=20;opts.maxNodes=7;
  const before=state.remaining;
  const r=searchBestMove(opts);
  assert.equal(r.budgetHit,true);
  assert.ok(r.nodes<=7);
  assert.equal(state.remaining,before);
});
test("undoMove runs even if evaluation fails",()=>{
  const {state,opts}=stones(6);
  opts.evaluate=()=>{throw Error("evaluation unavailable");};
  assert.throws(()=>searchBestMove(opts),/evaluation unavailable/);
  assert.equal(state.remaining,6);
  assert.equal(state.turn,0);
});
test("reject invalid configuration",()=>{
  const {opts}=stones(6);
  for(const n of [0,-1,Infinity,1.5,33]){
    assert.throws(()=>searchBestMove({...opts,depth:n}),RangeError);
  }
  assert.throws(()=>searchBestMove({...opts,legalMoves:7}),TypeError);
});
test("at least one pruned subtree in ordered game",()=>{
  const {opts}=stones(9);
  const r=searchBestMove(opts);
  assert.ok(r.prunes>0);
});
