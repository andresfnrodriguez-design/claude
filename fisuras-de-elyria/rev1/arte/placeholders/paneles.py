import sys,numpy as np
from PIL import Image
from scipy import ndimage
# uso: paneles.py carpeta  -> corta raw/hoja.png en A B C Z H segun huecos de fondo
D=sys.argv[1]; im=Image.open(f'{D}/raw/hoja.png').convert('RGB'); a=np.asarray(im).astype(int)
bg=np.median(np.concatenate([a[:3].reshape(-1,3),a[-3:].reshape(-1,3)]),0)
m=ndimage.binary_opening(np.abs(a-bg).sum(2)>45,iterations=2)
col=m.sum(0); xs=np.where(col>0)[0]
# huecos de columnas
gaps=[];inside=False
for x in range(xs.min(),xs.max()):
    if col[x]==0 and not inside: st=x;inside=True
    if col[x]>0 and inside: gaps.append((st,x));inside=False
gaps=sorted(gaps,key=lambda g:g[1]-g[0],reverse=True)[:2]; gaps.sort()
cx=[(g[0]+g[1])//2 for g in gaps]; print('cortes x',cx,gaps)
def corte_y(x0,x1):
    r=m[:,x0:x1].sum(1); ys=[y for y in range(150,620) if r[y]==0]
    if not ys: return int(np.argmin(r[150:620])+150)
    # hueco mas largo
    best=[];cur=[ys[0]]
    for y in ys[1:]:
        if y==cur[-1]+1: cur.append(y)
        else: best=max(best,cur,key=len); cur=[y]
    best=max(best,cur,key=len); return (best[0]+best[-1])//2
yl=corte_y(0,cx[0]); yr=corte_y(cx[1],1344); print('cortes y',yl,yr)
P={'A':(0,0,cx[0],yl),'B':(0,yl,cx[0],768),'C':(cx[0],0,cx[1],768),'Z':(cx[1],0,1344,yr),'H':(cx[1],yr,1344,768)}
for k,b in P.items(): im.crop(b).save(f'{D}/raw/{k}.png')
print('fondo',bg.astype(int).tolist())
