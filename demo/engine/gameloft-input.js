/* Java-free independent port of observed j.class key counters (Asphalt Nitro 1.1.7).
 * Does not claim to implement race physics, input mapping or the complete engine.
 */
(function(root,factory){"use strict";const api=factory();
 if(typeof module==="object"&&module.exports)module.exports=api;
 if(root)root.PocketForgeGameloftInput=api;
})(typeof window!=="undefined"?window:typeof globalThis!=="undefined"?globalThis:null,function(){
 "use strict";
 function keys(n=24){
  if(!Number.isInteger(n)||n<1||n>128)throw new RangeError("invalid key count");
  const current=new Int8Array(n),last=new Int8Array(n);
  function valid(i){if(!Number.isInteger(i)||i<0||i>=n)throw new RangeError("invalid key index");}
  function down(i){valid(i);if(current[i]>0)return;if(current[i]<0)current[i]=0;if(current[i]<126)current[i]++;}
  function up(i){valid(i);if(current[i]>0)current[i]=-current[i];}
  function frame(){for(let i=0;i<n;i++){last[i]=current[i];
   if(current[i]<0)current[i]=0;
   else if(current[i]>0&&current[i]<126){current[i]++;if(i>=18)current[i]=-current[i];}
  }return last.slice();}
  function held(i){valid(i);return last[i]>0;}
  function justPressed(i){valid(i);return last[i]===1;}
  function reset(){current.fill(0);last.fill(0);}
  return Object.freeze({down,up,frame,held,justPressed,reset});
 }
 return Object.freeze({keys});
});
