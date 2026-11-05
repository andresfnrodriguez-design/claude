"""Convierte las hojas de concepto de Kairon a assets del motor.
Todo se espeja: Gemini dibuja el guantelete en la mano derecha y el script
lo pasa a la izquierda, con los retratos mirando a la izquierda."""
import json, os, sys
from reg import *

SRC=sys.argv[1] if len(sys.argv)>1 else '.'
OUT=sys.argv[2] if len(sys.argv)>2 else 'out'
for d in ['retratos','zoom','mapa','batalla','vistas']: os.makedirs(f'{OUT}/{d}',exist_ok=True)
h1=load(f'{SRC}/h1.jpg'); h2=load(f'{SRC}/h2.jpg'); h3=load(f'{SRC}/h3.jpg'); h4=load(f'{SRC}/h4.jpg'); h5=load(f'{SRC}/h5.jpg')
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
esp=load(f'{SRC}/espejo.png')[4:-4,4:-4]; pp=portrait_params(esp)
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
ex,ey=32,8    # caja de ojos alineada a tiles, no se pisa con la de la boca
def cut(a,x,y): return a[y:y+16,x:x+32]
# Las bocas de la hoja 5 casi no se distinguen a esta escala, así que se dibujan
# sobre el retrato base, en la línea de boca que tiene el arte (más oscura de la zona).
def find_mouth():
    sk=10  # tono de piel más común de la cara
    zone=base_idx[30:42, 38:60].astype(int)
    vals,cnt=np.unique(base_idx[20:40,40:60],return_counts=True); sk=int(vals[np.argmax(cnt)])
    lum=np.array([sum(PAL[i]) for i in range(16)])
    best=None
    for y in range(31,40):
        row=base_idx[y,40:58]; d=np.where((lum[row]<lum[sk]*0.6)&(row!=0)&(row!=1))[0]
        if len(d)>=3 and (best is None or len(d)>best[1]): best=(y,len(d),40+int(np.median(d)))
    return best[0],best[2],sk
MY,MX=28,48   # línea de boca medida a mano en el retrato de 104x112 (ojos en y=20-21)
LINE=13; IN=14; TEETH=9; SKIN=10; SHADE=11; LASH=12
def mouth(kind):
    a=base_idx.copy(); y=MY; x0=MX-1; x1=MX+2
    def put(yy,xs,c):
        for x in xs: a[yy,x]=c
    if kind=='normal_cerrada': return a
    if kind=='normal_media':  put(y,range(x0,x1+1),LINE); put(y+1,range(x0+1,x1),IN)
    if kind=='normal_abierta': put(y,range(x0,x1+1),LINE); put(y+1,range(x0,x1+1),IN); put(y+2,range(x0+1,x1),LINE)
    if kind=='sonrisa_cerrada': put(y,range(x0,x1+1),LINE); a[y-1,x0-1]=LINE; a[y-1,x1+1]=LINE
    if kind=='sonrisa_media':  put(y,range(x0,x1+1),LINE); put(y+1,range(x0+1,x1),TEETH); a[y-1,x0-1]=LINE; a[y-1,x1+1]=LINE
    if kind=='sonrisa_abierta': put(y,range(x0,x1+1),LINE); put(y+1,range(x0,x1+1),TEETH); put(y+2,range(x0+1,x1),IN); a[y-1,x0-1]=LINE; a[y-1,x1+1]=LINE
    return a
# ojos dibujados sobre el retrato: párpado a la mitad y cerrado (ojo visible en x 43-50, filas 20-22)
EX0,EX1,EY=44,49,21
def eyes(kind):
    a=base_idx.copy()
    if kind=='entrecerrados':
        for x in range(EX0,EX1+1): a[EY,x]=LASH
    else:
        for x in range(EX0-1,EX1+2):
            for y in (EY,EY+1):
                if a[y,x] not in (SKIN,SHADE,9): a[y,x]=SKIN
        for x in range(EX0,EX1+1): a[EY+1,x]=LASH
        a[EY,EX0-1]=SHADE
    return a
mx=int(np.clip(round((MX-16)/8)*8,0,104-32)); my=int(np.clip(round((MY+1-8)/8)*8,0,112-16))
orden=['sonrisa_abierta','sonrisa_media','sonrisa_cerrada','normal_abierta','normal_media','normal_cerrada']
frames=[cut(mouth(k),mx,my) for k in orden]
bocas=Image.fromarray(np.vstack(frames),'P'); bocas.putpalette(escena.getpalette())
save(bocas,'retratos/kairon_bocas_32x96.png')
ojos=Image.fromarray(np.vstack([cut(eyes('entrecerrados'),ex,ey),cut(eyes('cerrados'),ex,ey)]),'P'); ojos.putpalette(escena.getpalette())
save(ojos,'retratos/kairon_ojos_32x32.png')
coords=dict(hoja='104x112',arte_x=2,
  boca=dict(x=mx,y=my,w=32,h=16,tile_x=mx//8,tile_y=my//8,
            orden_frames=['sonrisa abierta','sonrisa media','sonrisa cerrada','normal abierta','normal media','normal cerrada (= base)']),
  ojos=dict(x=ex,y=ey,w=32,h=16,tile_x=ex//8,tile_y=ey//8,orden_frames=['entrecerrados','cerrados']))
json.dump(coords,open(f'{OUT}/retratos/kairon_coordenadas.json','w'),indent=2,ensure_ascii=False)
print('boca',mx,my,'ojos',ex,ey)

# ---------- ESTADO 80x144 y MINI 32x32 ----------
fr=crop(h1,(102,204,406,1137),60)[:, ::-1].copy()
rr,gg,bb=fr[...,0],fr[...,1],fr[...,2]
m=fgmask(fr)&~((rr>150)&(gg<110)&(bb<110)&(rr-gg>60))
lab,n=ndimage.label(m); sz=ndimage.sum(m,lab,range(1,n+1)); m=lab==(1+int(np.argmax(sz)))
ys,xs=np.where(m); top=ys.min()
HEAD=0.135*(ys.max()-top)
s=28/HEAD; cut=top+int(141/s)
col,mm=reduce(fr[top:cut],m[top:cut],s)
cx=(np.where(mm.any(0))[0].min()+np.where(mm.any(0))[0].max())/2
C,M=place(80,144,col,mm,int(round(40-cx)),3); C,M=outline(C,M,do_outer=False)
estado,_=quantize(C,M,n=15,fixed=[(0,0,0)]+CYAN+HAIR_C); save(estado,'retratos/kairon_estado_80x144.png')
ea=np.asarray(escena); ys,xs=np.where(ea[:50]!=0)
hx=int(round((xs.min()+xs.max())/2)); hy=max(0,ys.min()); S0=46
x0=min(max(0,hx-S0//2),104-S0); sub=ea[hy:hy+S0,x0:x0+S0]
rgb=np.array(PAL,np.float32)[sub]; col,mm=reduce(rgb,sub!=0,32/S0)
C,M=place(32,32,col,mm,0,1)
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
def classify(r,m):
    """Cada píxel de la fuente a su posición de la paleta de aliados (rol del material)."""
    f=r/255; mx=f.max(2); mn=f.min(2); L=0.3*f[...,0]+0.59*f[...,1]+0.11*f[...,2]
    sat=(mx-mn)/np.maximum(mx,1e-6)
    hsv=np.asarray(Image.fromarray(r.astype(np.uint8)).convert('HSV')).astype(np.float32); h=hsv[...,0]*360/255
    k=np.zeros(m.shape,np.uint8)
    dark=L<0.13; grey=(sat<0.18)&~dark
    cyan=(h>160)&(h<215)&(sat>0.35)
    red=((h<16)|(h>320))&(sat>0.25)&~dark
    warm=(h>=16)&(h<=60)&~dark&~grey
    cream=warm&(sat<0.35)&(L>0.58)
    k[grey&(L<0.30)]=1; k[grey&(L>=0.30)&(L<0.45)]=2   # pelo
    k[grey&(L>=0.45)&(L<0.72)]=2
    k[grey&(L>=0.72)]=3
    k[cream]=3; k[cream&(L>0.80)]=14       # abrigo crema -> rampa pastel
    sk=warm&~cream
    k[(sk|(dark==0)&(sat>=0.18)&(h>=16)&(h<=60))&(L<0.42)]=4; k[sk&(L>=0.42)&(L<0.66)]=5; k[sk&(L>=0.66)]=6   # piel y bronce
    k[red&(L<0.22)]=7; k[red&(L>=0.22)]=8; k[red&(L>=0.40)]=9  # granate -> color del bando
    k[cyan]=10
    k[dark]=15
    k[~m]=0
    return k
def vote(k,W,H):
    """Reduce por voto mayoritario: cada píxel destino toma el material más común."""
    h,w=k.shape; out=np.zeros((H,W),np.uint8)
    for y in range(H):
        for x in range(W):
            c=k[int(y*h/H):max(int((y+1)*h/H),int(y*h/H)+1), int(x*w/W):max(int((x+1)*w/W),int(x*w/W)+1)].ravel()
            fg=c[c!=0]
            if len(fg)<0.45*len(c): continue
            v=np.bincount(fg,minlength=16).astype(float); v[15]*=0.35
            if v[10]>0 and v[10]>=0.15*len(fg): out[y,x]=10; continue   # la gema siempre se ve
            out[y,x]=v.argmax()
    return out
def map_sprite(b, maxw, maxh, cw, ch, feet_y, cx, view='frente'):
    r=crop(h3,b,0,6)[:, ::-1].copy(); m=fgmask(r); ys,xs=np.where(m)
    r=r[ys.min():ys.max()+1, xs.min():xs.max()+1]; m=m[ys.min():ys.max()+1, xs.min():xs.max()+1]
    k=classify(r,m)
    s=min(maxh/k.shape[0], maxw/k.shape[1])
    W=max(1,round(k.shape[1]*s)); H=max(1,round(k.shape[0]*s))
    small=vote(k,W,H)
    M=small!=0
    M=ndimage.binary_fill_holes(M)
    small[M&(small==0)]=15
    # limpieza: un píxel suelto rodeado por un mismo color toma ese color
    for y in range(1,H-1):
        for x in range(1,W-1):
            n=[small[y-1,x],small[y+1,x],small[y,x-1],small[y,x+1]]
            if n[0]==n[1]==n[2]==n[3]!=small[y,x] and n[0]!=0 and small[y,x] not in (10,): small[y,x]=n[0]
    # el cian de los ojos que dibujó Gemini no es la gema: pasa a ojo oscuro
    if view!='sel':
        top=small[:int(H*0.55)]; top[top==10]=15
    if view=='sel': view='frente'
    # ojos de 2 píxeles oscuros sobre la piel de la cara (sin boca)
    if view!='espalda':
        rows=[(int(np.isin(small[y],[5,6]).sum()),y) for y in range(1,int(H*0.6))]
        cnt,ey=max(rows)
        if cnt>=2:
            xs=np.where(np.isin(small[ey],[5,6]))[0]
            if view=='frente' and cnt>=3: c=int(round((xs.min()+xs.max())/2)); small[ey,c-1]=15; small[ey,c+1]=15; small[ey,c]=6
            elif view=='perfil': small[ey,xs.min()+(1 if cnt>2 else 0)]=15
            else: small[ey,xs.min()]=15
    # contorno grueso por fuera, en el color de contorno
    pad=np.zeros((H+2,W+2),np.uint8); pad[1:-1,1:-1]=small
    PM=pad!=0; ring=ndimage.binary_dilation(PM,[[0,1,0],[1,1,1],[0,1,0]])&~PM
    pad[ring]=15
    # interior: el borde que toca al contorno queda en el tono oscuro de su material
    idx=np.zeros((ch,cw),np.uint8)
    hh,ww=pad.shape; x0=int(round(cx-ww/2)); y0=feet_y-hh+1
    idx[max(0,y0):y0+hh, max(0,x0):x0+ww]=pad[max(0,-y0):, max(0,-x0):][:ch-max(0,y0),:cw-max(0,x0)]
    # sombra pequeña bajo los pies (posición 13)
    fy=min(ch-1,feet_y+1); row=np.where(idx[feet_y]!=0)[0]
    if len(row) and fy>feet_y:
        for x in range(row.min()+1,row.max()):
            if idx[fy,x]==0: idx[fy,x]=13
    return idx
def sheet(frames,path,zoom):
    im=Image.fromarray(np.vstack(frames),'P'); im.putpalette([v for c in ALLY for v in c]+[0]*720); save(im,path,zoom)
quieto=[(100,219,227,350),(253,219,380,350),(407,219,534,350)]
# infantería: cabe en 16x16 con el contorno, pies en la fila 14 y sombra en la 15
sheet([map_sprite(b,14,13,16,16,14,8) for b in quieto],'mapa/kairon_mapa_quieto_16x48.png',8)
cols=[(100,266),(294,460),(488,654),(682,848)]
filas=[(490,656),(732,898),(973,1139),(1215,1380)]
mov=[]
for fi,(y0,y1) in enumerate(filas):
    for ci,(x0,x1) in enumerate(cols[:3 if fi==3 else 4]):
        mov.append(map_sprite((x0,y0,x1,y1),14,13 if fi<3 else 15,32,32,30,16,['perfil','frente','espalda','sel'][fi]))
sheet(mov,'mapa/kairon_mapa_movimiento_32x480.png',4)
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

# ---------- VISTAS: hablando y pestañeando ----------
def frame_with(patch,x,y):
    a=base_idx.copy(); a[y:y+16,x:x+32]=patch; im=Image.fromarray(a,'P'); im.putpalette(escena.getpalette())
    return im.convert('RGB').resize((416,448),0)
bf=np.asarray(bocas); of=np.asarray(ojos)
def gif(fr,name,ms): fr[0].save(f'{OUT}/vistas/{name}.gif',save_all=True,append_images=fr[1:],duration=ms,loop=0)
gif([frame_with(bf[i*16:(i+1)*16],mx,my) for i in (5,4,3,4)],'kairon_hablando',140)
gif([frame_with(bf[i*16:(i+1)*16],mx,my) for i in (2,1,0,1)],'kairon_hablando_sonriendo',140)
gif([frame_with(bf[80:96],mx,my)]*12+[frame_with(of[0:16],ex,ey),frame_with(of[16:32],ex,ey),frame_with(of[0:16],ex,ey)],'kairon_pestaneando',90)
print('ok vistas')
