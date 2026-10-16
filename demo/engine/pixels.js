/* PocketForge Pixel Surface — original 16-bit software framebuffer.
 * Motivated by finding short[][] and drawPixels(444/4444) in 3D-Adventure.
 * Our RGBA4444 packing is defined independently; not a clone of Nokia format.
 * Measure RAM and frame-time before using it in production.
 */
(function(root,factory){
 "use strict";
 const api=factory();
 if(typeof module==="object"&&module.exports)module.exports=api;
 if(root)root.PocketForgePixels=api;
})(typeof window!=="undefined"?window:(typeof globalThis!=="undefined"?globalThis:null),function(){
 "use strict";
 const nibble=n=>Math.round(Math.max(0,Math.min(255,Number(n)||0))/17);
 function pack(r,g,b,a=255){
   return (nibble(r)<<12)|(nibble(g)<<8)|(nibble(b)<<4)|nibble(a);
 }
 function unpack(p){
   return [(p>>>12&15)*17,(p>>>8&15)*17,(p>>>4&15)*17,(p&15)*17];
 }
 function createSurface(width,height,{maxPixels=1048576}={}){
   if(!Number.isSafeInteger(width)||!Number.isSafeInteger(height)||width<=0||height<=0||
      !Number.isSafeInteger(maxPixels)||width*height>maxPixels)
      throw new RangeError("pixel surface budget exceeded or invalid dimensions");
   const pixels=new Uint16Array(width*height);
   function at(x,y){
     return Number.isInteger(x)&&Number.isInteger(y)&&x>=0&&y>=0&&x<width&&y<height?
       y*width+x:-1;
   }
   function set(x,y,color){const i=at(x,y);if(i<0)return false;pixels[i]=color&65535;return true;}
   function get(x,y){const i=at(x,y);return i<0?null:pixels[i];}
   function clear(color=0){pixels.fill(color&65535);}
   function rect(x,y,w,h,color){
     if(![x,y,w,h].every(Number.isFinite)||w<=0||h<=0)return 0;
     const x0=Math.max(0,Math.floor(x)),y0=Math.max(0,Math.floor(y));
     const x1=Math.min(width,Math.ceil(x+w)),y1=Math.min(height,Math.ceil(y+h));
     for(let yy=y0;yy<y1;yy++)pixels.fill(color&65535,yy*width+x0,yy*width+x1);
     return Math.max(0,x1-x0)*Math.max(0,y1-y0);
   }
   function line(x0,y0,x1,y1,color){
     for(const n of [x0,y0,x1,y1])if(!Number.isInteger(n)||Math.abs(n)>32768)
       throw new RangeError("line coordinates out of bounds");
     const dx=Math.abs(x1-x0),sx=x0<x1?1:-1;
     const dy=-Math.abs(y1-y0),sy=y0<y1?1:-1;
     let err=dx+dy,steps=0,draws=0;
     while(steps++<131073){
       if(set(x0,y0,color))draws++;
       if(x0===x1&&y0===y1)break;
       const e=2*err;
       if(e>=dy){err+=dy;x0+=sx;}
       if(e<=dx){err+=dx;y0+=sy;}
     }
     return draws;
   }
   function rgba(){
     const out=new Uint8ClampedArray(pixels.length*4);
     for(let i=0;i<pixels.length;i++){
       const p=pixels[i],j=i*4;
       out[j]=(p>>>12&15)*17;out[j+1]=(p>>>8&15)*17;
       out[j+2]=(p>>>4&15)*17;out[j+3]=(p&15)*17;
     }
     return out;
   }
   function flush(ctx,dx=0,dy=0){
     if(!ctx||typeof ctx.createImageData!=="function"||typeof ctx.putImageData!=="function")
       throw new TypeError("2D Canvas context required");
     const image=ctx.createImageData(width,height);
     image.data.set(rgba());
     ctx.putImageData(image,dx,dy);
   }
   return Object.freeze({width,height,pixels,set,get,clear,rect,line,rgba,flush});
 }
 return Object.freeze({pack,unpack,createSurface});
});
