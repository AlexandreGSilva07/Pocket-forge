"use strict";
const assert=require("node:assert/strict"),fs=require("node:fs"),vm=require("node:vm");
const code=fs.readFileSync("dist/j2me-web/js/methodStub.js","utf8");
let observed=null,callbackHit=false;
const context={
 js2me:{
  BufferStream:function(bytes){this.bytes=bytes;},
  currentThread:0,storageName:"",isThreadSuspended:false,
  generateProgram(data){data.content=[];},
  execute(data,locals,constantPool,exceptions,resume,callback){
   observed={locals:locals.slice(),callback:typeof callback};
   if(callback)callback();
   return 17;
  }
 },
 localStorage:{getItem(){return null}},console
};
vm.runInNewContext(code,context);
const parent={prototype:{longJavaMethod:{data:null}}};
const stub=context.js2me.generateMethodStub(parent,new Uint8Array([]),
  "methodWith12Arguments",[],[],15,"longJavaMethod",Array(12).fill("I"),8);
const args=Array.from({length:12},(_,i)=>i+1);
const returned=stub(...args,()=>{callbackHit=true});
assert.equal(returned,17);
assert.equal(observed.locals.length,12,"all JVM arguments must be retained");
assert.deepEqual(Array.from(observed.locals),args);
assert.equal(observed.callback,"function");
assert.equal(callbackHit,true,"async JVM callback must be preserved after 10 args");
console.log("PASS: 12 Java arguments and continuation callback survived in JVM method stub");
