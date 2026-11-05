from PIL import Image
import numpy as np
from scipy import ndimage as ndi
BG=(0xA9,0xCB,0xA6); WHITE=(255,255,255); BLACK=(0x17,0x0C,0x16)
TW,TH=100,112          # 96x80 de FE8 + 2 columnas por lado y +40% de alto

def finish(idx, pal, out):
    """idx: 0 fondo, resto personaje. Agrega línea negra 1 px, blanco 1 px afuera, sube al tope."""
    pal=[BG,WHITE,BLACK]+[p for p in pal if p not in (BG,WHITE,BLACK)]
    P=np.array(pal)
    fig=ndi.binary_fill_holes(idx!=0)
    e1=ndi.binary_erosion(fig); e2=ndi.binary_erosion(e1); e3=ndi.binary_erosion(e2)
    lum=P.sum(1)
    # adelgazar: lo oscuro del original justo adentro de la línea toma el color del interior
    second=e1&~e2
    for y,x in zip(*np.where(second)):
        if lum[idx[y,x]]<240:
            win=idx[max(0,y-2):y+3,max(0,x-2):x+3][e3[max(0,y-2):y+3,max(0,x-2):x+3]]
            win=win[lum[win]>=240]
            if win.size: idx[y,x]=np.bincount(win).argmax()
    idx[fig&~e1]=2                                   # línea negra de 1 px
    idx[ndi.binary_dilation(fig)&~fig]=1             # blanco de 1 px por fuera
    top=np.where((idx!=0).any(axis=1))[0].min(); idx=idx[top:top+TH].copy()
    # borde inferior: sin líneas, el cuerpo sigue
    for r in (-1,-2):
        row=idx[r]; bad=(row==1)|(row==2)
        if bad.any() and r==-1: idx[r][bad]=idx[r-2][bad]
    im=Image.fromarray(idx,"P"); flat=[v for c in pal for v in c]; im.putpalette(flat+[0]*(768-len(flat)))
    im.save(out+".png"); im.convert("RGB").resize((TW*5,TH*5),Image.NEAREST).save(out+"_x5.png")
    return im

def map_palette(C, F, pal):
    """pixeles del personaje (F) al color de paleta más cercano; índices relativos a pal."""
    P=np.array(pal); idx=np.zeros(F.shape,np.uint8)
    d=((C[F][:,None,:]-P[None,:,:])**2).sum(2).argmin(1)
    idx[F]=d; return idx
