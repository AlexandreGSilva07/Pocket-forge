"use strict";
const assert=require("node:assert/strict"),fs=require("node:fs"),vm=require("node:vm");
function loadClass(path) {
 let proto;
 const context={js2me:{createClass(o){proto=o;},markUnsafe:fn=>fn},
 javaRoot:{$java:{$lang:{$NullPointerException:class extends Error{},$IndexOutOfBoundsException:class extends Error{}}}},
 console};
 vm.runInNewContext(fs.readFileSync("dist/j2me-web/js/me/"+path,"utf8"),context);
 return proto;
}
const buffer=loadClass("java/lang/StringBuffer.js");
const append=buffer["$append$_CII$Ljava_lang_StringBuffer_"];
assert.equal(typeof append,"function");
let value={string:"R"};
assert.strictEqual(append.call(value,[65,66,67],1,2),value);
assert.equal(value.string,"RBC");
assert.throws(()=>append.call(value,[1],1,4),/Error/);
let nullValue={string:"abc"};
buffer["$append$Ljava_lang_Object_$Ljava_lang_StringBuffer_"].call(nullValue,null);
assert.equal(nullValue.string,"abcnull");
const player=loadClass("javax/microedition/media/PlayerImpl.js");
const media=player["$getMediaTime"+"$"+"$J"];
assert.equal(typeof media,"function");
let t=media.call({element:{currentTime:1.25}});
assert.equal(t.hi,0);assert.equal(t.lo,1250000);
t=media.call({element:{currentTime:0}});
assert.equal(t.lo,0);
console.log("PASS: StringBuffer.append(char[],int,int) and MMAPI Player.getMediaTime()");
