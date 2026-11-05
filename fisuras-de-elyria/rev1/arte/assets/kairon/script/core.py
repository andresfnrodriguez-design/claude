import numpy as np
from PIL import Image
from scipy import ndimage
BG=(0xA9,0xCB,0xA6)
SRC_BG=np.array([160,195,150])

def load(p): return np.asarray(Image.open(p).convert('RGB')).astype(np.float32)

def fgmask(a, tol=55):
    m=np.abs(a-SRC_BG).sum(2)>tol
    m=ndimage.binary_opening(m,iterations=1)
    lab,n=ndimage.label(m)
    if n==0: return m
    sizes=ndimage.sum(m,lab,range(1,n+1))
    keep=np.isin(lab,1+np.where(sizes>=60)[0])
    return ndimage.binary_fill_holes(keep) & m | keep

def reduce(rgb, m, scale, out_w=None, out_h=None):
    """Escala con promedio solo sobre el personaje (sin halo verde)."""
    h,w=m.shape
    W=max(1,round(w*scale)); H=max(1,round(h*scale))
    mf=m.astype(np.float32)
    pm=Image.fromarray(np.uint8(mf*255)).resize((W,H),Image.BOX)
    al=np.asarray(pm).astype(np.float32)/255
    ch=[]
    for c in range(3):
        x=Image.fromarray(rgb[...,c]*mf).resize((W,H),Image.BOX)
        ch.append(np.asarray(x))
    col=np.stack(ch,2)/np.maximum(al[...,None],1e-6)
    return np.clip(col,0,255), al>0.5

def place(canvas_w, canvas_h, col, m, x, y):
    """Pega col/m en un lienzo en (x,y), recortando lo que sobre."""
    C=np.zeros((canvas_h,canvas_w,3),np.float32); C[:]=BG
    M=np.zeros((canvas_h,canvas_w),bool)
    h,w=m.shape
    x0,y0=max(0,x),max(0,y); x1,y1=min(canvas_w,x+w),min(canvas_h,y+h)
    if x1<=x0 or y1<=y0: return C,M
    sm=m[y0-y:y1-y, x0-x:x1-x]
    C[y0:y1,x0:x1][sm]=col[y0-y:y1-y, x0-x:x1-x][sm]
    M[y0:y1,x0:x1]=sm
    return C,M

def outline(C,M,inner=(0,0,0),outer=(255,255,255),do_outer=True):
    """Línea interior de 1 px en el borde de la silueta y contorno blanco por fuera."""
    C=C.copy(); M=M.copy()
    er=ndimage.binary_erosion(M,structure=np.ones((3,3)),border_value=0)
    edge=M&~er
    C[edge]=inner
    if do_outer:
        dil=ndimage.binary_dilation(M,structure=[[0,1,0],[1,1,1],[0,1,0]])
        ring=dil&~M
        C[ring]=outer; M=M|ring
    return C,M

def quantize(C,M,n=15,fixed=None,pal=None):
    """Devuelve imagen P con BG en índice 0. fixed = colores obligatorios.
    pal = paleta completa ya decidida (lista de 16 RGB) para forzar."""
    fg=C[M].astype(np.uint8)
    if pal is None:
        fixed=fixed or []
        k=n-len(fixed)
        if len(fg)==0: cols=[]
        else:
            px=Image.fromarray(fg.reshape(1,-1,3))
            q=px.quantize(colors=k,method=Image.Quantize.MEDIANCUT,kmeans=3)
            p=q.getpalette()[:k*3]
            cols=[tuple(p[i:i+3]) for i in range(0,len(p),3)]
        pal=[BG]+list(fixed)+cols
        pal=pal[:16]
        while len(pal)<16: pal.append((0,0,0))
    P=np.array(pal[1:],np.float32)
    d=((C[...,None,:]-P[None,None])**2).sum(-1)
    idx=(d.argmin(-1)+1).astype(np.uint8)
    idx[~M]=0
    im=Image.fromarray(idx,'P')
    flat=[v for c in pal for v in c]
    im.putpalette(flat+[0]*(768-len(flat)))
    return im, pal

def gba_round(pal): return [tuple((v>>3)<<3 for v in c) for c in pal]

def agbpal(pal, path):
    with open(path,'wb') as f:
        for r,g,b in pal:
            f.write(((r>>3)|((g>>3)<<5)|((b>>3)<<10)).to_bytes(2,'little'))
