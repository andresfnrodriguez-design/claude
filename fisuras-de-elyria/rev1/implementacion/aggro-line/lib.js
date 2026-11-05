var T=16, W=15, H=10;
// map: g grass, f forest, w water, m mountain, r road
var MAP=[
"gggfffgggggwwww",
"ggfffggrrrggwww",
"ggggggrrggggggw",
"gmmgggrggggfggg",
"gmgggrrggggffgg",
"ggggrrgggggggmm",
"gfggrggggggggmm",
"ffggrgggggfgggg",
"fgggrrrrgggggww",
"gggggggrrggggww"];
var PLAYER={x:7,y:5};
var ENEMIES=[{x:3,y:5,k:"lance",threat:true},{x:8,y:1,k:"bow",threat:true},{x:13,y:7,k:"axe",threat:false},{x:1,y:1,k:"sword",threat:false}];
var COL={g:["#5fa84a","#549a40"],f:["#2f6e32","#3d8a3c"],w:["#3a78c8","#5a98e0"],m:["#8c7a5a","#a8926a"],r:["#c8b07a","#b89e68"]};

function px(c,x,y,w,h,col){c.fillStyle=col;c.fillRect(x,y,w,h)}
function tile(c,t,x,y){const[a,b]=COL[t];px(c,x,y,T,T,a);
  if(t==="g"){px(c,x+3,y+4,1,1,b);px(c,x+11,y+9,1,1,b);px(c,x+6,y+13,1,1,b)}
  if(t==="f"){px(c,x+2,y+3,12,8,b);px(c,x+5,y+1,6,3,b);px(c,x+7,y+11,2,3,"#5a3a20")}
  if(t==="w"){px(c,x+2,y+5,5,1,b);px(c,x+9,y+10,5,1,b)}
  if(t==="m"){c.fillStyle=b;c.beginPath();c.moveTo(x+1,y+15);c.lineTo(x+8,y+2);c.lineTo(x+15,y+15);c.fill();px(c,x+7,y+3,2,2,"#eee")}
  if(t==="r"){px(c,x+4,y+7,2,1,b);px(c,x+10,y+3,2,1,b)}}
function unit(c,u,col,dark,f){const x=u.x*T,y=u.y*T,bob=(f>>4)&1;
  px(c,x+4,y+13,8,2,"rgba(0,0,0,.35)");
  px(c,x+5,y+5-bob,6,8,col);px(c,x+5,y+11-bob,6,2,dark);
  px(c,x+5,y+1-bob,6,5,"#f2c9a0");px(c,x+5,y+1-bob,6,2,dark);
  px(c,x+6,y+3-bob,1,1,"#000");px(c,x+9,y+3-bob,1,1,"#000");
  const wx=x+12,wy=y+2-bob;
  if(u.k==="lance"){px(c,wx,wy,1,12,"#ddd");px(c,wx-1,wy,3,2,"#fff")}
  else if(u.k==="bow"){px(c,wx,wy+1,1,10,"#a06a30");px(c,wx-2,wy+5,2,1,"#ddd")}
  else if(u.k==="axe"){px(c,wx,wy,1,12,"#a06a30");px(c,wx-2,wy,4,4,"#ccc")}
  else {px(c,wx,wy,1,9,"#eee");px(c,wx-1,wy+8,3,1,"#c9a030")}}
function cursor(c,f){const x=PLAYER.x*T,y=PLAYER.y*T,o=(f>>3)&1?0:1,col="#fff";
  for(const[dx,dy,sx,sy]of[[0,0,1,1],[T,0,-1,1],[0,T,1,-1],[T,T,-1,-1]]){
    const cx=x+dx-sx*o-(sx<0?1:0),cy=y+dy-sy*o-(sy<0?1:0);
    px(c,cx,cy,sx*4,sy*1||1,col);px(c,cx,cy,1,sy*4,col);}}
function base(c,f){for(let j=0;j<H;j++)for(let i=0;i<W;i++)tile(c,MAP[j][i],i*T,j*T);}
function units(c,f){for(const e of ENEMIES)unit(c,e,"#c83a3a","#7a1c1c",f);unit(c,{...PLAYER,k:"sword"},"#3a6ad8","#1c347a",f);}
function hud(c,label){px(c,2,142,96,16,"rgba(16,20,48,.85)");c.strokeStyle="#c8b878";c.strokeRect(2.5,142.5,95,15);
  c.fillStyle="#fff";c.font="8px monospace";c.fillText(label,7,153);}
var center=u=>[u.x*T+8,u.y*T+8];

