import cv2, numpy as np
from core import *
def gray(a): return cv2.cvtColor(a.astype(np.uint8),cv2.COLOR_RGB2GRAY)
def register(src, tpl_img, tpl_box, scales=np.linspace(0.85,1.18,34)):
    """Busca la región tpl_box de tpl_img dentro de src probando escalas.
    Devuelve (s, tx, ty, score): punto p en tpl_img -> p*s + t en src."""
    x0,y0,x1,y1=tpl_box; T=gray(tpl_img[y0:y1,x0:x1]); S=gray(src)
    best=None
    for s in scales:
        Ts=cv2.resize(T,None,fx=s,fy=s,interpolation=cv2.INTER_AREA)
        if Ts.shape[0]>=S.shape[0] or Ts.shape[1]>=S.shape[1]: continue
        r=cv2.matchTemplate(S,Ts,cv2.TM_CCOEFF_NORMED)
        _,v,_,loc=cv2.minMaxLoc(r)
        if best is None or v>best[3]: best=(s,loc[0]-x0*s,loc[1]-y0*s,v)
    return best
def warp(img, s, tx, ty, W, H):
    M=np.float32([[s,0,tx],[0,s,ty]])
    return cv2.warpAffine(img.astype(np.float32),M,(W,H),flags=cv2.INTER_AREA,borderMode=cv2.BORDER_CONSTANT,borderValue=tuple(float(v) for v in SRC_BG))
