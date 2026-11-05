"""Convierte las hojas de concepto de Kairon a assets del motor.
Todo se espeja: Gemini dibuja el guantelete en la mano derecha y el script
lo pasa a la izquierda, con los retratos mirando a la izquierda."""
import json, os, sys
from reg import *

SRC=sys.argv[1] if len(sys.argv)>1 else '.'
OUT=sys.argv[2] if len(sys.argv)>2 else 'out'
for d in ['retratos','zoom','mapa','batalla','vistas']: os.makedirs(f'{OUT}/{d}',exist_ok=True)
h2=load(f'{SRC}/h2.jpg'); h3=load(f'{SRC}/h3.jpg'); h4=load(f'{SRC}/h4.jpg'); h5=load(f'{SRC}/h5.jpg')
CYAN=[(72,224,240),(24,144,168)]
HAIR_C=[(64,60,60),(96,92,88),(136,132,124)]
def crop(a,b,label=0,pad=3):
    x0,y0,x1,y1=b; return a[y0+label:y1-pad, x0+pad:x1-pad]
def save(im,path,zoom=4):
    im.save(f'{OUT}/{path}')
    w,h=im.size; im.convert('RGB').resize((w*zoom,h*zoom),0).save(f'{OUT}/vistas/'+os.path.basename(path).replace('.png','_x%d.png'%zoom))

# ---------- RETRATO DE ESCENA 100x112 en hoja de 104x112 ----------
ESC_BOX=(102,204,740,1138); ESP_BOX=(772,204,1438,1138)
def portrait_params(r):
    m=fgmask(r)[:, ::-1]; ys,xs=np.where(m); top,bot=ys.min(),ys.max()
    s=109/(bot-top+1); _,mm=reduce(r[top:bot+1,::-1],m[top:bot+1],s)
    xs2=np.where(mm.any(0))[0]; dx=int(round(52-(xs2.min()+xs2.max())/2))
    return dict(top=int(top),bot=int(bot),s=s,dx=dx)
def portrait(r,p,m=None):
    if m is None: m=fgmask(r)
    r=r[:, ::-1]; m=m[:, ::-1]
    col,mm=reduce(r[p['top']:p['bot']+1],m[p['top']:p['bot']+1],p['s'])
    C,M=place(104,112,col,mm,p['dx'],3)
    return outline(C,M)
esc=crop(h2,ESC_BOX,55); pe=portrait_params(esc)
C,M=portrait(esc,pe)
escena,PAL=quantize(C,M,n=15,fixed=[(0,0,0),(248,248,248)]+CYAN+HAIR_C)
PAL=gba_round(PAL); escena,_=quantize(C,M,pal=PAL)
save(escena,'retratos/kairon_escena_104x112.png')
esp=crop(h2,ESP_BOX,55); pp=portrait_params(esp)
C,M=portrait(esp,pp); espejo,_=quantize(C,M,pal=PAL)
save(espejo,'retratos/kairon_espejo_104x112.png')
agbpal(PAL,f'{OUT}/retratos/kairon_retrato.agbpal')

# ---------- BOCAS Y OJOS (recortes del retrato, mismo ángulo) ----------
base5=crop(h5,(102,204,740,893),50)
m5=fgmask(base5); top5=np.where(m5.any(1))[0].min()
hx=np.where(m5[top5:top5+120].any(0))[0]
HAIR=(int(hx.min()),int(top5+10),int(hx.max()),int(top5+130))
s0,tx0,ty0,_=register(esc,base5,(int(hx.min()),int(top5),int(hx.max()),int(top5+330)))
def to_escena(img):
    s,tx,ty,sc=register(img,base5,HAIR)
    # variante -> base5 -> escena
    S=s0/s; TX=tx0-tx*s0/s; TY=ty0-ty*s0/s
    W,H=esc.shape[1],esc.shape[0]
    w=warp(img,S,TX,TY,W,H)
    M=np.float32([[S,0,TX],[0,S,TY]])
    v=cv2.warpAffine(np.ones(img.shape[:2],np.float32),M,(W,H),flags=cv2.INTER_LINEAR)
    v=cv2.erode((v>0.999).astype(np.uint8),np.ones((9,9),np.uint8))>0
    w[~v]=esc[~v]
    return w,v,sc
VAR={'normal_media':(772,204,1411,893),'normal_abierta':(1442,204,1951,849),
     'sonrisa_cerrada':(1983,204,2486,699),'sonrisa_media':(102,920,740,1662),
     'sonrisa_abierta':(772,920,1411,1662),
     'ojos_entrecerrados':(1443,919,1951,1138),'ojos_cerrados':(1983,919,2486,1138)}
base_idx=np.asarray(escena)
var_idx={}
for k,b in VAR.items():
    w,v,sc=to_escena(crop(h5,b,50))
    C,M=portrait(w,pe,fgmask(w)); im,_=quantize(C,M,pal=PAL)
    var_idx[k]=np.asarray(im); print(k,'registro',round(sc,3))
def patch_box(keys, rows):
    """Caja de 32x16 alineada a tiles (8 px) que cubre los cambios."""
    d=np.zeros_like(base_idx,bool)
    for k in keys: d|=(var_idx[k]!=base_idx)
    d[:rows[0]]=False; d[rows[1]:]=False
    ys,xs=np.where(d); cx=np.median(xs); cy=np.median(ys)
    x=int(round((cx-16)/8))*8; y=int(round((cy-8)/8))*8
    return x,y
# zonas de búsqueda: ojos en la cara, boca debajo
face_rows=(18,30)
ex,ey=patch_box(['ojos_entrecerrados','ojos_cerrados'],face_rows)
mx,my=patch_box(['normal_media','normal_abierta','sonrisa_media','sonrisa_abierta'],(ey+12,46))
def cut(a,x,y): return a[y:y+16,x:x+32]
orden=['sonrisa_abierta','sonrisa_media','sonrisa_cerrada','normal_abierta','normal_media',None]
frames=[cut(var_idx[k] if k else base_idx,mx,my) for k in orden]
bocas=Image.fromarray(np.vstack(frames),'P'); bocas.putpalette(escena.getpalette())
save(bocas,'retratos/kairon_bocas_32x96.png')
ojos=Image.fromarray(np.vstack([cut(var_idx['ojos_entrecerrados'],ex,ey),cut(var_idx['ojos_cerrados'],ex,ey)]),'P'); ojos.putpalette(escena.getpalette())
save(ojos,'retratos/kairon_ojos_32x32.png')
coords=dict(hoja='104x112',arte_x=2,
  boca=dict(x=mx,y=my,w=32,h=16,tile_x=mx//8,tile_y=my//8,
            orden_frames=['sonrisa abierta','sonrisa media','sonrisa cerrada','normal abierta','normal media','normal cerrada (= base)']),
  ojos=dict(x=ex,y=ey,w=32,h=16,tile_x=ex//8,tile_y=ey//8,orden_frames=['entrecerrados','cerrados']))
json.dump(coords,open(f'{OUT}/retratos/kairon_coordenadas.json','w'),indent=2,ensure_ascii=False)
print('boca',mx,my,'ojos',ex,ey)

# ---------- ESTADO 80x144 y MINI 32x32 ----------
st=crop(h2,(1475,204,1859,1138),0)[:, ::-1]; m=fgmask(st); ys,xs=np.where(m)
s=144/(ys.max()-ys.min()+1); col,mm=reduce(st[ys.min():ys.max()+1],m[ys.min():ys.max()+1],s)
cx=(np.where(mm.any(0))[0].min()+np.where(mm.any(0))[0].max())/2
C,M=place(80,144,col,mm,int(round(40-cx)),0); C,M=outline(C,M,do_outer=False)
estado,_=quantize(C,M,n=15,fixed=[(0,0,0)]+CYAN); save(estado,'retratos/kairon_estado_80x144.png')
mi=crop(h2,(1917,204,2083,370),0,4)[:, ::-1]; m=fgmask(mi)
st=mi.shape[1]/32; yy=((np.arange(32)+0.5)*mi.shape[0]/32).astype(int); xx=((np.arange(32)+0.5)*st).astype(int)
C=mi[yy][:,xx].astype(np.float32); M=m[yy][:,xx]; C[~M]=BG
mini,_=quantize(C,M,pal=PAL); save(mini,'retratos/kairon_mini_32x32.png',8)

# ---------- ZOOM DE ESTADO 240x160 y HERIDO ----------
def zoom(b,label):
    z=crop(h4,b,label,4)[:, ::-1].copy()
    s=240/z.shape[1]; m=fgmask(z,70)
    col,mm=reduce(z,m,s)
    C,M=place(240,160,col[:160],mm[:160],0,0)
    return quantize(C,M,n=15,fixed=[(24,24,24)]+CYAN)[0]
save(zoom((102,204,1411,1138),0),'zoom/kairon_zoom_240x160.png',2)
save(zoom((835,1230,1415,1662),45),'zoom/kairon_herido_240x160.png',2)
print('ok retratos y zoom')

# ---------- SPRITES DE MAPA (paleta de aliados) ----------
import colorsys
ALLY=['80a080','3c2c58','8a78c0','d0c8f0','6a4a48','c08a68','f4d8b8','1e2c6c','2f5cc8','3ea0e8','9ce4f8','c02838','f0dd60','7a8878','f0f0e8','241c2c']
ALLY=[tuple(int(h[i:i+2],16) for i in (0,2,4)) for h in ALLY]
def ally_index(c):
    r,g,b=[v/255 for v in c]; h,s,v=colorsys.rgb_to_hsv(r,g,b); h*=360; L=0.3*r+0.59*g+0.11*b
    if L<0.17: return 15
    if 160<=h<=210 and s>0.35: return 10 if L>0.55 else 9          # gema cian
    if s<0.16:                                                      # grises y crema claro
        if L>0.70: return 14
        if L>0.48: return 13
        return 1
    if (h<18 or h>320):                                             # granate -> color del bando
        return 7 if L<0.25 else 8 if L<0.42 else 9
    if 18<=h<=55:
        if s<0.32 and L>0.55: return 14 if L>0.75 else 3            # abrigo crema
        if L>0.70: return 6
        if L>0.45: return 5
        return 4                                                    # piel, bronce, cuero
    return min(range(1,15),key=lambda i:sum((a-b)**2 for a,b in zip(c,ALLY[i])))
def map_sprite(b, H, cw, ch, feet_y, cx):
    r=crop(h3,b,0,6)[:, ::-1].copy(); m=fgmask(r); ys,xs=np.where(m)
    r=r[ys.min():ys.max()+1, xs.min():xs.max()+1]; m=m[ys.min():ys.max()+1, xs.min():xs.max()+1]
    s=H/m.shape[0]
    if m.shape[1]*s>16: s=16/m.shape[1]
    col,mm=reduce(r,m,s); h,w=mm.shape
    C,M=place(cw,ch,col,mm,int(round(cx-w/2)),feet_y+1-h)
    idx=np.zeros((ch,cw),np.uint8)
    for y,x in zip(*np.where(M)): idx[y,x]=ally_index(C[y,x])
    er=ndimage.binary_erosion(M,np.ones((3,3)),border_value=0); idx[M&~er]=15
    return idx
def sheet(frames,path,zoom):
    im=Image.fromarray(np.vstack(frames),'P'); im.putpalette([v for c in ALLY for v in c]+[0]*720); save(im,path,zoom)
quieto=[(100,219,227,350),(253,219,380,350),(407,219,534,350)]
sheet([map_sprite(b,16,16,16,15,8) for b in quieto],'mapa/kairon_mapa_quieto_16x48.png',6)
cols=[(100,266),(294,460),(488,654),(682,848)]
filas=[(490,656),(732,898),(973,1139),(1215,1380)]
mov=[]
for fi,(y0,y1) in enumerate(filas):
    for ci,(x0,x1) in enumerate(cols[:3 if fi==3 else 4]):
        mov.append(map_sprite((x0,y0,x1,y1),16 if fi<3 else 18,32,32,31,16))
sheet(mov,'mapa/kairon_mapa_movimiento_32x480.png',4)
with open(f'{OUT}/mapa/paleta_aliados.agbpal','wb') as f: pass
agbpal(ALLY,f'{OUT}/mapa/paleta_aliados.agbpal')

# ---------- BATALLA 248x160, una sola paleta ----------
BCOL=[(998,1464),(1494,1960),(1990,2456)]
BROW=[(290,615),(728,1052),(1155,1478)]
NOMBRES=['01_quieto','02_ataque_cuerpo','03_critico_cuerpo','04_ataque_distancia','05_critico_distancia','06_esquive','07_ataque_fallado','08_impacto']
def bmask(r):
    m=fgmask(r)
    rr,gg,bb=r[...,0],r[...,1],r[...,2]
    lines=((rr>150)&(gg<90)&(bb<90))|((bb>120)&(rr<90))     # guías roja y azul
    return m&~lines
raw=[]
for i in range(8):
    (x0,x1),(y0,y1)=BCOL[i%3],BROW[i//3]
    r=h3[y0:y1, x0+4:x1-4][:, ::-1].copy(); raw.append((r,bmask(r)))
q_r,q_m=raw[0]; ys,xs=np.where(q_m)
S=34/(ys.max()-ys.min()+1); CX=(xs.min()+xs.max())/2; FEET=q_r.shape[0]-1
frames=[]
for r,m in raw:
    col,mm=reduce(r,m,S); h,w=mm.shape
    C,M=place(248,160,col,mm,int(round(140-CX*S)),int(round(102-FEET*S)))
    er=ndimage.binary_erosion(M,np.ones((3,3)),border_value=0); C[M&~er]=(40,40,40)
    frames.append((C,M))
allfg=np.concatenate([C[M] for C,M in frames]).reshape(1,-1,3).astype(np.uint8)
q=Image.fromarray(allfg).quantize(colors=13,method=Image.Quantize.MEDIANCUT,kmeans=3).getpalette()[:39]
BPAL=gba_round([BG,(40,40,40)]+CYAN[:1]+[tuple(q[i:i+3]) for i in range(0,39,3)])
for n,(C,M) in zip(NOMBRES,frames):
    im,_=quantize(C,M,pal=BPAL); save(im,f'batalla/kairon_{n}.png',2)
agbpal(BPAL,f'{OUT}/batalla/kairon_batalla.agbpal')
print('ok mapa y batalla, escala batalla',round(S,4))
