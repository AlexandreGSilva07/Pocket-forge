"use strict";
const assert=require("node:assert/strict"),{test}=require("node:test");
const T=require("../demo/engine/tactics.js");
test("empty field starts at the center and never mutates",()=>{
 const b=T.makeBoard();
 assert.deepEqual(T.chooseMove(b),{x:5,y:5,reason:"center",score:0});
 assert.equal(b.cells.reduce((a,x)=>a+x,0),0);
});
test("computer takes immediately winning square",()=>{
 const b=T.makeBoard();
 for(let x=2;x<=5;x++)T.place(b,x,4,2);
 T.place(b,7,2,1);T.place(b,6,8,1);
 const before=[...b.cells],m=T.chooseMove(b,2);
 assert.equal(m.reason,"win");assert.equal(m.y,4);
 assert.ok(m.x===1||m.x===6);
 assert.deepEqual([...b.cells],before);
 assert.equal(T.place(b,m.x,m.y,2),true);
 assert.equal(T.winAt(b,m.x,m.y,2),true);
});
test("computer blocks immediate opponent four",()=>{
 const b=T.makeBoard();
 for(let y=1;y<=4;y++)T.place(b,3,y,1);
 T.place(b,8,9,2);
 const move=T.chooseMove(b,2);
 assert.equal(move.reason,"block");
 assert.equal(move.x,3);assert.ok(move.y===0||move.y===5);
});
test("four open axes are evaluated separately",()=>{
 const b=T.makeBoard();
 for(const [x,y] of [[3,5],[4,5],[6,5],[7,5]])T.place(b,x,y,1);
 const score=T.placementScore(b,5,5,1);
 assert.ok(score>=1000000);
 assert.equal(T.get(b,5,5),0);
});
test("board detects diagonal five and refuses illegal writes",()=>{
 const b=T.makeBoard(9);
 for(let k=0;k<5;k++)T.place(b,k,k,2);
 assert.equal(T.winAt(b,4,4,2),true);
 assert.equal(T.place(b,4,4,1),false);
 assert.equal(T.place(b,-1,0,1),false);
 assert.throws(()=>T.makeBoard(4),RangeError);
});
test("full board returns no legal move",()=>{
 const b=T.makeBoard(5);
 b.cells.fill(1);
 assert.equal(T.chooseMove(b,2),null);
});
