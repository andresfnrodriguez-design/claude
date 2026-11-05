import re, collections
src=open('/home/claude/fireemblem8u/src/data_terrains.c').read()
tabs={m.group(1):dict((k,int(v)) for k,v in re.findall(r'\[TERRAIN_(\w+)\] = (-?\d+)',m.group(2)))
      for m in re.finditer(r'CONST_DATA s8 (\w+)\[\] = \{(.*?)\};',src,re.S)}
names=list(tabs['TerrainTable_MovCost_CommonT2Normal'])
ID={n:i for i,n in enumerate(names)}
inf=[tabs['TerrainTable_MovCost_CommonT2Normal'][n] for n in names]
fly=[tabs['TerrainTable_MovCost_FlyNormal'][n] for n in names]
ES={'NONE':'—','PLAINS':'Llanura','ROAD':'Camino','VILLAGE_REGULAR':'Aldea','VILLAGE_CLOSED':'Aldea cerrada','HOUSE':'Casa','ARMORY':'Armería','VENDOR':'Tienda','ARENA_REGULAR':'Arena (coliseo)','C_ROOM_09':'Sala C (sin uso)','FORT':'Fuerte','GATE_CASTLE':'Puerta de castillo','FOREST':'Bosque','THICKET':'Matorral','SAND':'Arena (suelo)','DESERT':'Desierto','RIVER':'Río','MOUNTAIN':'Montaña','PEAK':'Pico','BRIDGE_REGULAR':'Puente','BRIDGE_14':'Puente levadizo alzado','SEA':'Mar','LAKE':'Lago','FLOOR_REGULAR':'Suelo','FLOOR_MAGIC':'Suelo mágico (FE6)','FENCE_REGULAR':'Cerca','WALL_REGULAR':'Muro','WALL_DAMAGED':'Muro dañado (rompible)','RUBBLE':'Escombros','PILLAR':'Pilar','DOOR':'Puerta (llave)','THRONE':'Trono','CHEST_EMPTY':'Cofre vacío','CHEST_FULL':'Cofre lleno','ROOF':'Techo','GATE_REGULAR':'Portón','CHURCH':'Iglesia','RUINS_REGULAR':'Ruinas','CLIFF':'Acantilado','BALLISTA_REGULAR':'Balista','BALLISTA_LONG':'Balista larga','BALLISTA_KILLER':'Balista asesina','SHIP_FLAT':'Barco','SHIP_WRECK':'Barco naufragado','TILE_2C':'Casilla 2C (sin uso)','STAIRS':'Escaleras','TILE_2E':'Casilla 2E (sin uso)','GLACIER':'Glaciar','ARENA_30':'Arena 30 (sin uso)','VALLEY':'Valle','FENCE_32':'Cerca 2','SNAG':'Tronco roto','BRIDGE_SNAG':'Puente de tronco','SKY':'Cielo','DEEPS':'Abismo','RUINS_VILLAGE':'Aldea en ruinas (FE7)','INN':'Posada','BARREL':'Barril','BONE':'Hueso','DARK':'Oscuridad','WATER':'Agua','GUNNELS':'Borda','DECK':'Cubierta','BRACE':'Riostra','MAST':'Mástil'}
# core: prólogo de 3H
core=[r.replace(',','.') for r in open('/home/claude/fe3h/00_prologo.txt').read().split('\n')[1:21]]
cmap={'.':ID['PLAINS'],'F':ID['FOREST'],'~':ID['FENCE_REGULAR'],'#':ID['CLIFF'],'X':ID['WALL_REGULAR']}
W,H=27,30
P=ID['PLAINS']
g=[[P]*W for _ in range(H)]
for y,row in enumerate(core):
    for x,ch in enumerate(row):
        g[y+3][x+3]=cmap[ch]
# torre (2x2) y obstáculos sueltos: muro. barranco y fila inferior: acantilado
ringB=[(x,1) for x in range(1,26)]+[(25,y) for y in range(2,25)]+[(x,24) for x in range(24,0,-1)]+[(1,y) for y in range(23,1,-1)]
gaps={(13,1),(25,12),(13,24),(1,12)}
slots=[p for p in ringB if p not in gaps]+[(x,26) for x in range(W)]+[(x,28) for x in range(W)]
types=[i for i in range(1,len(names)) if i!=P]
place={}
k=0
for t in types:
    for _ in range(2):
        x,y=slots[k]; g[y][x]=t; place.setdefault(t,[]).append((x,y)); k+=1
place[P]=sorted(gaps)
left=slots[k:]
# verificación: BFS de infantería y de voladores desde el despliegue (x=10,y=21)
def reach(cost):
    S=(13,21); seen={S}; q=[S]
    while q:
        x,y=q.pop()
        for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
            nx,ny=x+dx,y+dy
            if 0<=nx<W and 0<=ny<H and (nx,ny) not in seen and cost[g[ny][nx]]>0:
                seen.add((nx,ny)); q.append((nx,ny))
    return seen
ri=reach(inf); rf=reach(fly)
bad=[]
for t,ps in place.items():
    for (x,y) in ps:
        if inf[t]>0 and (x,y) not in ri: bad.append(('inf',names[t],x,y))
        adj=any((x+dx,y+dy) in ri for dx,dy in((1,0),(-1,0),(0,1),(0,-1)))
        if not adj: bad.append(('noadj',names[t],x,y))
print("start tile",core[18][10],"tiles",W*H,"tipos",len(place),"slots libres",len(left),"problemas",bad)
open('grid.txt','w').write("\n".join(" ".join(f"{v:02X}" for v in r) for r in g)+"\n")
import json; json.dump({'g':g,'place':{names[t]:ps for t,ps in place.items()},'ES':ES,'names':names,'inf':inf,'fly':fly},open('data.json','w'))
