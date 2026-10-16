/* PocketForge AI Core — original bounded alpha-beta tree search.
 * Motivated by bytecode study of Xrossing Dice's MinimaxRobot:
 * alternating max/min, pruning, mutate/undo, depth budget.
 * This is not a port of its game rules or implementation.
 */
(function(root,factory){
  "use strict";
  const api=factory();
  if(typeof module==="object"&&module.exports)module.exports=api;
  if(root)root.PocketForgeAI=api;
})(typeof window!=="undefined"?window:(typeof globalThis!=="undefined"?globalThis:null),function(){
  "use strict";
  function searchBestMove({
    state, legalMoves, applyMove, undoMove, evaluate, isTerminal,
    depth=4, maximizing=true, maxNodes=20000
  }={}){
    for(const [name,callback] of Object.entries({legalMoves,applyMove,undoMove,evaluate,isTerminal})){
      if(typeof callback!=="function")throw new TypeError(name+" must be function");
    }
    if(!Number.isSafeInteger(depth)||depth<1||depth>32)throw new RangeError("depth must be 1..32");
    if(!Number.isSafeInteger(maxNodes)||maxNodes<1||maxNodes>10000000)throw new RangeError("invalid node budget");
    let nodes=0,prunes=0,budgetHit=false,move=null,score=maximizing?-Infinity:Infinity;
    // Maximum score is always from a single fixed player's perspective.
    function visit(d,isMax,alpha,beta){
      nodes++;
      if(nodes>=maxNodes){budgetHit=true;return evaluate(state);}
      if(d===0||isTerminal(state))return evaluate(state);
      const moves=legalMoves(state,isMax);
      if(!Array.isArray(moves))throw new TypeError("legalMoves must return an array");
      if(!moves.length)return evaluate(state);
      let best=isMax?-Infinity:Infinity;
      for(const candidate of moves){
        // save/unmake through a game-defined token; unwind even on exceptions.
        const token=applyMove(state,candidate,isMax);
        let value;
        try{value=visit(d-1,!isMax,alpha,beta);}
        finally{undoMove(state,candidate,isMax,token);}
        if(isMax){
          if(value>best)best=value;
          if(best>alpha)alpha=best;
        }else{
          if(value<best)best=value;
          if(best<beta)beta=best;
        }
        if(alpha>=beta){prunes++;break;}
        if(budgetHit)break;
      }
      return best;
    }
    const choices=legalMoves(state,maximizing);
    if(!Array.isArray(choices))throw new TypeError("legalMoves must return an array");
    if(!choices.length)return {move:null,score:evaluate(state),nodes,prunes,budgetHit,complete:true};
    let alpha=-Infinity,beta=Infinity;
    for(const candidate of choices){
      if(nodes>=maxNodes){budgetHit=true;break;}
      const token=applyMove(state,candidate,maximizing);
      let value;
      try{value=visit(depth-1,!maximizing,alpha,beta);}
      finally{undoMove(state,candidate,maximizing,token);}
      if(move===null||(maximizing?value>score:value<score)){
        move=candidate;score=value;
      }
      if(maximizing)alpha=Math.max(alpha,score);else beta=Math.min(beta,score);
      if(budgetHit)break;
    }
    return {move,score,nodes,prunes,budgetHit,complete:!budgetHit};
  }
  return Object.freeze({searchBestMove});
});
