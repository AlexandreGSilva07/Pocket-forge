"use strict";
const {test}=require("node:test"),assert=require("node:assert/strict"),zlib=require("node:zlib");
const ZIP=require("../demo/engine/zip-jar.js");
function makeZip(name,data,method=8){
 const n=Buffer.from(name),src=Buffer.from(data),deflated=method===8?zlib.deflateRawSync(src):src,crc=ZIP.crc32(src);
 const local=Buffer.alloc(30+n.length);
 local.writeUInt32LE(0x04034b50,0);local.writeUInt16LE(20,4);local.writeUInt16LE(method,8);
 local.writeUInt32LE(crc,14);local.writeUInt32LE(deflated.length,18);local.writeUInt32LE(src.length,22);
 local.writeUInt16LE(n.length,26);n.copy(local,30);
 const central=Buffer.alloc(46+n.length);
 central.writeUInt32LE(0x02014b50,0);central.writeUInt16LE(20,4);central.writeUInt16LE(20,6);
 central.writeUInt16LE(method,10);central.writeUInt32LE(crc,16);
 central.writeUInt32LE(deflated.length,20);central.writeUInt32LE(src.length,24);
 central.writeUInt16LE(n.length,28);n.copy(central,46);
 const end=Buffer.alloc(22);end.writeUInt32LE(0x06054b50,0);end.writeUInt16LE(1,8);end.writeUInt16LE(1,10);
 end.writeUInt32LE(central.length,12);end.writeUInt32LE(local.length+deflated.length,16);
 return Buffer.concat([local,deflated,central,end]);
}
for(const method of [0,8])test("JAR reader decodes method "+method+" without JVM",async()=>{
 const input=Buffer.from([2,223,5,9,0,255,7]),zip=makeZip("6",input,method),reader=ZIP.readZIP(zip);
 assert.deepEqual(reader.names,["6"]);assert.deepEqual([...await reader.get("6")],[...input]);
});
test("ZIP CRC mismatch is rejected",async()=>{
 const zip=makeZip("6",Buffer.from([1,2,3]),0);zip[31]^=1;
 await assert.rejects(()=>ZIP.readZIP(zip).get("6"),RangeError);
});
test("missing central directory / size caps rejected",()=>{
 assert.throws(()=>ZIP.readZIP(Uint8Array.from([1,2,3])),RangeError);
 assert.throws(()=>ZIP.readZIP(new Uint8Array(23),{maxArchive:22}),RangeError);
});