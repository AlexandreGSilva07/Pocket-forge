/* PocketForge adapter for JS2ME: offline, browser-based JAR picker.
 * Uses upstream execution semantics; does not claim 100% Java ME coverage.
 * SPDX-License-Identifier: MIT
 */
(function () {
 "use strict";
 const audit = [];
 let bytecodeExecutions = 0;
 function log(kind, message) {
   const value = String(message && (message.message || message) || "");
   audit.push({kind, message:value, t:Math.round(performance.now())});
   if(audit.length>250)audit.shift();
   const label=document.getElementById("pf-status");
   if(label)label.textContent=kind.toUpperCase()+": "+value;
 }
 window.addEventListener("error",e=>log("error",e.message+" at "+e.filename+":"+e.lineno));
 window.addEventListener("unhandledrejection",e=>log("rejection",e.reason));
 window.addEventListener("load",function(){
   const screen=document.getElementById("screen");
   if(!screen||!window.js2me){log("error","JS2ME não inicializou.");return;}
   // Legacy startup runs bootstrap classes on thread 0; explicitly bind that thread
   // to an isolated static-VM namespace before any class initialization begins.
   const originalSetup = window.js2me.setupJVM;
   window.js2me.setupJVM = function(callback){
     this.VMMapping[0] = 0;
     this.statics0 = {};
     this.currentVM = 0;
     this.statics = this.statics0;
     return originalSetup.call(this,callback);
   };
   // The Firefox-OS era engine may switch to a thread that has no VM mapping
   // while asynchronous class loading resumes. Preserve isolation by creating
   // a dedicated static namespace per valid VM; surface every recovery in log.
   const originalSwitchVM = window.js2me.switchVM;
   window.js2me.switchVM = function(threadId){
     if(this.VMMapping[threadId]===undefined){
       const fallback=Number.isInteger(this.currentVM)?this.currentVM:0;
       this.VMMapping[threadId]=fallback;
       log("compat-warning","Missing VM mapping for thread "+threadId+"; mapped to VM "+fallback);
     }
     originalSwitchVM.call(this,threadId);
     if(!this.statics){
       const key="statics"+this.currentVM;
       this.statics=this[key]||(this[key]={});
       log("compat-warning","Created static storage for VM "+this.currentVM);
     }
   };
   const originalExecute = window.js2me.execute;
   window.js2me.execute = function(){bytecodeExecutions++;return originalExecute.apply(this,arguments);};
   const choose=screen.querySelector("#file-selector");
   if(choose)choose.style.display="none"; // obsolete FirefoxOS MozActivity
   const bar=document.createElement("section");bar.id="pf-panel";
   const heading=document.createElement("strong");heading.textContent="PocketForge · J2ME Runtime";
   const detail=document.createElement("span");detail.textContent="Importe seu JAR local. Sem Java, servidor externo ou upload.";
   const file=document.createElement("input");file.type="file";file.accept=".jar,application/java-archive";file.id="pf-jar-file";
   const status=document.createElement("output");status.id="pf-status";status.textContent="Pronto para importar.";
   const button=document.createElement("button");button.type="button";button.textContent="Exportar diagnóstico";
   button.id="pf-export-diagnostic";button.onclick=()=>{const blob=new Blob([JSON.stringify({
     engine:"JS2ME",upstreamCommit:"828b81b468953c34bb754b59e67c1021754e8bdb",
     manifest:window.js2me.manifest||null,notes:"Startup and API errors only; not proof of compatibility",
     bytecodeExecutions:bytecodeExecutions,events:audit
   },null,2)],{type:"application/json"});
   const u=URL.createObjectURL(blob),a=document.createElement("a");a.href=u;a.download="pocketforge-j2me-diagnostic.json";a.click();setTimeout(()=>URL.revokeObjectURL(u),1000);};
   bar.append(heading,detail,file,status,button);
   document.body.prepend(bar);
   function load(blob){
     if(!blob||!blob.size){log("error","JAR vazio ou inexistente.");return;}
     if(blob.size>64*1024*1024){log("error","JAR acima do limite de 64 MiB.");return;}
     if(window.js2me.manifest)log("warning","Para trocar de JAR, recarregue a página: o runtime legado retém estado.");
     log("loading","Carregando "+blob.name+" ("+blob.size+" bytes)...");
     try {window.js2me.launchJAR(blob);}catch(e){log("error",e);}
     setTimeout(()=>{if(window.js2me.manifest&&window.js2me.manifest["midlet-name"])
       log("manifest","MIDlet localizado: "+window.js2me.manifest["midlet-name"]+"; execução ainda não garantida.");},1600);
   }
   file.onchange=()=>load(file.files[0]);
   document.addEventListener("dragover",e=>e.preventDefault());
   document.addEventListener("drop",e=>{e.preventDefault();const dropped=e.dataTransfer.files[0];if(dropped)load(dropped);});
   const legacy=window.js2me.showError;
   window.js2me.showError=function(value){
     log("engine-error",value);
     const alert=document.getElementById("alert");
     if(alert){alert.style.display="block";const target=alert.querySelector(".message");if(target)target.textContent=String(value);}
     // Do not call legacy: upstream HTML injection through error text.
   };
   window.PocketForgeJ2ME=Object.freeze({
     load:load,diagnostics:()=>audit.slice(),executionCount:()=>bytecodeExecutions,engine:"js2me-mit",offline:true,
     capabilities:{jvm:"JIT+interpreter partial",cldc:"partial",midp:"partial",m3g:false}
   });
   log("ready","Selecione um JAR original para tentar executar.");
 });
})();
