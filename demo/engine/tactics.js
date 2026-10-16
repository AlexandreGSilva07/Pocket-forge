/* PocketForge Tactics Core — original 5-in-a-row local move evaluator.
 * Motivated by disassembly of five.d in 5Chess (SHA 493f99e040...):
 * evaluates four axes and buckets tactical threat scores, then scans cells.
 * NOT a line-by-line port of proprietary code or exact original scoring.
 */
(function(root,factory){
 "use strict";
 const api=factory();
 if(typeof module==="object"&&module.exports)module.exports=api;
 if(root)root.PocketForgeTactics=api;
})(typeof window!=="undefined"?window:(typeof globalThis!=="undefined"?globalThis:null),function(){
 "use strict";
 const DIRS=[[1,0],[0,1],[1,1],[1,-1]];
 function makeBoard(size=11){
  if(!Number.isInteger(size)||size<5||size>32)throw new RangeError("size must be 5..32");
  return {size,cells:new Uint8Array(size*size)};
 }
 function valid(b,x,y){return !!b&&Number.isInteger(x)&&Number.isInteger(y)&&x>=0&&y>=0&&x<b.size&&y<b.size;}
 function get(b,x,y){return valid(b,x,y)?b.cells[y*b.size+x]:-1;}
 function place(b,x,y,player){
  if(!valid(b,x,y)||![1,2].includes(player)||get(b,x,y)!==0)return false;
  b.cells[y*b.size+x]=player;return true;
 }
 function inspectLine(b,x,y,player,dx,dy){
  let span=1,open=0;
  for(const direction of [-1,1]){
   let xx=x+dx*direction,yy=y+dy*direction;
   while(get(b,xx,yy)===player){span++;xx+=dx*direction;yy+=dy*direction;}
   if(get(b,xx,yy)===0)open++;
  }
  return {span,open};
 }
 function winAt(b,x,y,player){
  if(get(b,x,y)!==player)return false;
  return DIRS.some(([dx,dy])=>inspectLine(b,x,y,player,dx,dy).span>=5);
 }
 function threat(span,open){
  if(span>=5)return 1000000;
  if(open===0)return 0;
  if(span===4)return open===2?70000:12000;
  if(span===3)return open===2?4500:600;
  if(span===2)return open===2?250:40;
  return open===2?4:1;
 }
 function placementScore(b,x,y,player){
  if(!valid(b,x,y)||get(b,x,y)!==0)return -Infinity;
  b.cells[y*b.size+x]=player;
  try{
   let total=0;
   for(const [dx,dy] of DIRS){
    const line=inspectLine(b,x,y,player,dx,dy);
    total+=threat(line.span,line.open);
   }
   return total;
  }finally{b.cells[y*b.size+x]=0;}
 }
 function chooseMove(b,player=2){
  if(!b||!(b.cells instanceof Uint8Array)||b.cells.length!==b.size*b.size||![1,2].includes(player))
   throw new TypeError("invalid board or player");
  const opponent=3-player;
  const stones=[];
  for(let y=0;y<b.size;y++)for(let x=0;x<b.size;x++)if(get(b,x,y)!==0)stones.push([x,y]);
  if(!stones.length){
   const middle=Math.floor(b.size/2);
   return {x:middle,y:middle,reason:"center",score:0};
  }
  const shortlist=new Set();
  for(const [x,y] of stones){
   for(let dy=-2;dy<=2;dy++)for(let dx=-2;dx<=2;dx++)
    if(valid(b,x+dx,y+dy)&&get(b,x+dx,y+dy)===0)shortlist.add((y+dy)*b.size+(x+dx));
  }
  let best=null,score=-Infinity;
  for(const index of shortlist){
   const x=index%b.size,y=Math.floor(index/b.size);
   const own=placementScore(b,x,y,player),defend=placementScore(b,x,y,opponent);
   // A forced winning move beats defense; otherwise block immediate loss.
   const win=own>=1000000,block=defend>=1000000;
   const priority=(win?1e9:0)+(block?1e8:0)+own+defend*.9;
   // For ties, prefer squares near the center and then stable row order.
   const dx=x-(b.size-1)/2,dy=y-(b.size-1)/2;
   const adjusted=priority-(dx*dx+dy*dy)*.001;
   if(adjusted>score){score=adjusted;best={x,y,reason:win?"win":block?"block":"pattern",score:priority};}
  }
  return best;
 }
 return Object.freeze({makeBoard,get,place,winAt,placementScore,chooseMove,inspectLine});
});
