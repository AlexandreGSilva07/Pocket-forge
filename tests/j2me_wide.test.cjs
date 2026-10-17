"use strict";
const assert = require("node:assert/strict");
const fs=require("node:fs");
const code=fs.readFileSync("dist/j2me-web/js/program_zazu.js","utf8");
const beginning="executors[0xc4] = function (context) {";
const start=code.indexOf(beginning);
assert(start>=0,"wide handler must accept the execution context");
const end=code.indexOf("};",start);
assert(end>start,"wide function not terminated");
const fn=new Function("context",code.slice(start+beginning.length,end));
function execute(op,pointer,value,stack=[],locals=Array(270).fill(0)){
 const context={parameters:[{op,pointer,value}],position:1,stack,locals};fn(context);return context;
}
let a=execute(0x15,260,null,[],Array.from({length:270},(_,i)=>i));assert.equal(a.stack.pop(),260);
a=execute(0x36,260,null,[19]);assert.equal(a.locals[260],19);
a=execute(0x84,260,-4,[],Array.from({length:270},(_,i)=>i));assert.equal(a.locals[260],256);
assert.throws(()=>execute(0xff,260,0),/unsupported wide/);
console.log("PASS: JVM wide load/store/iinc works on 16-bit locals indices");
