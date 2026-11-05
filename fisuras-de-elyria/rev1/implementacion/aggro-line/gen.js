const {chromium}=require('playwright');const fs=require('fs');
const lib=fs.readFileSync(__dirname+'/lib.js','utf8');
const scenes={
 a:{p:{x:7,y:5},e:[[5,5,1],[7,1,1],[9,7,1],[3,1,1],[12,5,1],[11,9,1],[1,8,0],[14,0,0]]},
 b:{p:{x:3,y:7},e:[[3,5,1],[5,7,1],[4,8,1],[9,2,1],[12,8,1],[8,4,1],[13,1,0],[1,1,0]]}};
const kinds=["lance","bow","axe","sword"];
(async()=>{const b=await chromium.launch();const pg=await b.newPage();
for(const [n,s] of Object.entries(scenes)){
 const url=await pg.evaluate(([lib,s,kinds])=>{
  (0,eval)(lib.replace(/const PLAYER=.*\n/,'').replace(/const ENEMIES=.*\n/,''));
  const PLAYER=s.p;const ENEMIES=s.e.map((e,i)=>({x:e[0],y:e[1],threat:!!e[2],k:kinds[i%4]}));
  const cv=document.createElement('canvas');cv.width=240;cv.height=160;const c=cv.getContext('2d');c.imageSmoothingEnabled=false;
  for(let j=0;j<10;j++)for(let i=0;i<15;i++)tile(c,MAP[j][i],i*16,j*16);
  const cost={g:1,r:1,f:2,m:3,w:99},occ=new Set(ENEMIES.map(e=>e.x+','+e.y));
  const dist={},q=[[PLAYER.x,PLAYER.y,0]];dist[PLAYER.x+','+PLAYER.y]=0;
  while(q.length){q.sort((a,b)=>a[2]-b[2]);const[x,y,d]=q.shift();
   for(const[ax,ay]of[[1,0],[-1,0],[0,1],[0,-1]]){const nx=x+ax,ny=y+ay;if(nx<0||ny<0||nx>14||ny>9)continue;
    const k=nx+','+ny;if(occ.has(k))continue;const nd=d+cost[MAP[ny][nx]];if(nd>5||(dist[k]!==undefined&&dist[k]<=nd))continue;dist[k]=nd;q.push([nx,ny,nd]);}}
  const atk=new Set();for(const k in dist){const[x,y]=k.split(',').map(Number);
   for(const[ax,ay]of[[1,0],[-1,0],[0,1],[0,-1]]){const nk=(x+ax)+','+(y+ay);if(x+ax<0||y+ay<0||x+ax>14||y+ay>9)continue;if(dist[nk]===undefined)atk.add(nk);}}
  const ov=(k,f,s)=>{const[x,y]=k.split(',').map(Number);c.fillStyle=f;c.fillRect(x*16,y*16,16,16);c.fillStyle=s;c.fillRect(x*16,y*16,16,1);c.fillRect(x*16,y*16,1,16);};
  for(const k in dist)ov(k,"rgba(70,120,255,.55)","rgba(170,200,255,.8)");
  for(const k of atk)ov(k,"rgba(255,70,60,.5)","rgba(255,170,160,.8)");
  for(const e of ENEMIES)unit(c,e,"#c83a3a","#7a1c1c",0);unit(c,{...PLAYER,k:"sword"},"#3a6ad8","#1c347a",0);
  const [x1,y1]=[PLAYER.x*16+8,PLAYER.y*16+8];
  for(const e of ENEMIES.filter(e=>e.threat)){let [x,y]=[e.x*16+8,e.y*16+8];
   const dx=Math.abs(x1-x),dy=-Math.abs(y1-y),sx=x<x1?1:-1,sy=y<y1?1:-1;let err=dx+dy,i=0;
   while(!(x===x1&&y===y1)){
     if(i%3===0&&i>5){const fx=Math.abs(x-x1)+Math.abs(y-y1);if(fx>7){c.fillStyle="#ff3030";c.fillRect(x,y,1,1);}}
     i++;const e2=2*err;if(e2>=dy){err+=dy;x+=sx}if(e2<=dx){err+=dx;y+=sy}}}
  // cursor
  const X=PLAYER.x*16,Y=PLAYER.y*16;c.fillStyle="#fff";
  for(const[a,b2,w,h]of[[X-1,Y-1,4,1],[X-1,Y-1,1,4],[X+13,Y-1,4,1],[X+16,Y-1,1,4],[X-1,Y+16,4,1],[X-1,Y+13,1,4],[X+13,Y+16,4,1],[X+16,Y+13,1,4]])c.fillRect(a,b2,w,h);
  return cv.toDataURL();},[lib,s,kinds]);
 fs.writeFileSync(`/home/user/claude/aggro-${n}-sel-240x160.png`,Buffer.from(url.split(',')[1],'base64'));}
await b.close();})();
