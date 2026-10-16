/* PocketForge Audio Core v0.2
 * Bounded, lazy WebAudio synthesis. Self-contained; no J2ME assets copied.
 */
(function (root, factory) {
  "use strict";
  const api=factory();
  if (typeof module==="object"&&module.exports)module.exports=api;
  if (root)root.PocketForgeAudio=api;
})(typeof window!=="undefined"?window:(typeof globalThis!=="undefined"?globalThis:null),function(){
  "use strict";
  function createAudio(host, {maxVoices=8}={}) {
    if (!Number.isInteger(maxVoices)||maxVoices<1||maxVoices>64)throw new RangeError("invalid voice budget");
    let context=null, active=0, muted=false, closed=false;
    function unlock(){
      if(closed||muted)return false;
      try {
        const C=host&&(host.AudioContext||host.webkitAudioContext);
        if(!C)return false;
        if(!context)context=new C();
        if(context.state==="suspended"){
          const p=context.resume();
          if(p&&typeof p.catch==="function")p.catch(()=>{});
        }
        return true;
      }catch(_){return false;}
    }
    function play(freq,dur=.13,type="sine",volume=.04){
      if(closed||muted||active>=maxVoices)return false;
      if(!Number.isFinite(freq)||freq<20||freq>20000)return false;
      if(!Number.isFinite(dur)||dur<=0||dur>3)return false;
      if(!["sine","square","sawtooth","triangle"].includes(type))return false;
      if(!Number.isFinite(volume)||volume<=0||volume>.5)return false;
      if(!context||context.state!=="running")return false;
      let o,g,playing=false;
      try {
        o=context.createOscillator();g=context.createGain();
        const t=context.currentTime;
        o.type=type;
        o.frequency.setValueAtTime(freq,t);
        o.frequency.exponentialRampToValueAtTime(Math.max(20,freq*.68),t+dur);
        g.gain.setValueAtTime(Math.max(.001,volume),t);
        g.gain.exponentialRampToValueAtTime(.001,t+dur);
        o.connect(g);g.connect(context.destination);
        o.onended=()=>{ if(playing){playing=false;active=Math.max(0,active-1);} try{o.disconnect();g.disconnect();}catch(_){} };
        o.start(t);playing=true;active++;
        o.stop(t+dur);
        return true;
      }catch(_){
        if(playing)active=Math.max(0,active-1);
        try{if(o)o.disconnect();if(g)g.disconnect();}catch(__){}
        return false;
      }
    }
    function setMuted(value){muted=!!value;return muted;}
    function dispose(){
      closed=true;muted=true;
      if(context&&typeof context.close==="function"){try{const p=context.close();if(p&&p.catch)p.catch(()=>{});}catch(_){}}
      context=null;
    }
    return Object.freeze({unlock,play,setMuted,dispose,get muted(){return muted;},get voices(){return active;}});
  }
  return Object.freeze({createAudio});
});
