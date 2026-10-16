/* PocketForge TilePack — original bounded binary-level decoder.
 * Data layout based on bytecode study of 7Zwerge's class e.a(InputStream,..):
 * 4 dimension bytes, 1 mode byte, W*H entries of 1/2 bytes, an optional flag
 * and a third per-cell byte layer. No game assets or source code included.
 */
(function(root,factory){
  "use strict";
  const api=factory();
  if(typeof module==="object"&&module.exports)module.exports=api;
  if(root)root.PocketForgeTilePack=api;
})(typeof window!=="undefined"?window:(typeof globalThis!=="undefined"?globalThis:null),function(){
  "use strict";
  function decodeLegacyLevel(input,{maxCells=262144}={}){
    if(!(input instanceof Uint8Array))throw new TypeError("Uint8Array required");
    if(input.length<5)throw new RangeError("incomplete level header");
    const cols=input[0],rows=input[1],tileWidth=input[2],tileHeight=input[3],mode=input[4];
    const cells=cols*rows;
    if(!cols||!rows||!tileWidth||!tileHeight||cells>maxCells)
      throw new RangeError("level dimensions outside budget");
    if(mode!==1&&mode!==2)throw new RangeError("only 8-bit or 16-bit tile encoding supported");
    const dataEnd=5+cells*mode;
    if(input.length<dataEnd)throw new RangeError("truncated tile payload");
    let tiles;
    if(mode===1){
      tiles=input.slice(5,dataEnd);
    } else {
      tiles=new Uint16Array(cells);
      for(let i=0,k=5;i<cells;i++,k+=2)tiles[i]=input[k]|(input[k+1]<<8);
    }
    if(input.length===dataEnd)throw new RangeError("missing optional-layer flag");
    const hasExtra=input[dataEnd];
    if(hasExtra!==0&&hasExtra!==1)throw new RangeError("invalid layer flag");
    const expected=dataEnd+1+(hasExtra?cells:0);
    if(input.length!==expected)throw new RangeError("invalid extra-layer length");
    return {cols,rows,tileWidth,tileHeight,mode,tiles,
      flags:hasExtra?input.slice(dataEnd+1):null};
  }
  // Compact original codec for modern PocketForge projects, explicit magic and
  // version allow format upgrades instead of hard-coding an old J2ME layout.
  function encodePFLevel({cols,rows,tileWidth=16,tileHeight=16,tiles}){
    if(!Number.isInteger(cols)||!Number.isInteger(rows)||cols<1||rows<1||
       cols>255||rows>255||!Number.isInteger(tileWidth)||!Number.isInteger(tileHeight)||
       tileWidth<1||tileWidth>255||tileHeight<1||tileHeight>255)
      throw new RangeError("bad level dimensions");
    if(!tiles||tiles.length!==cols*rows)throw new RangeError("tile count mismatch");
    const out=new Uint8Array(8+tiles.length);
    out.set([0x50,0x46,0x4c,1,cols,rows,tileWidth,tileHeight]);
    for(let i=0;i<tiles.length;i++){
      const x=tiles[i];
      if(!Number.isInteger(x)||x<0||x>255)throw new RangeError("tile ID must fit uint8");
      out[8+i]=x;
    }
    return out;
  }
  function decodePFLevel(data){
    if(!(data instanceof Uint8Array)||data.length<8||data[0]!==0x50||data[1]!==0x46||
       data[2]!==0x4c||data[3]!==1)throw new RangeError("unsupported PF level format");
    const cols=data[4],rows=data[5],tileWidth=data[6],tileHeight=data[7];
    if(!cols||!rows||!tileWidth||!tileHeight||data.length!==8+cols*rows)
      throw new RangeError("invalid level dimensions or data length");
    return {cols,rows,tileWidth,tileHeight,tiles:data.slice(8)};
  }
  return Object.freeze({decodeLegacyLevel,encodePFLevel,decodePFLevel});
});
