from PIL import Image
import numpy as np
from scipy import ndimage as ndi
BG=np.array((0xA9,0xCB,0xA6)); WHITE=(0xFD,0xF7,0xF0); TW,TH=96,104

def portrait(rgb, bgmask, cx, W, y0, forced, n_auto, out):
    """rgb y bgmask a tamaño fuente; el fondo se decide solo por la máscara, nunca por color."""
    sc=W/TW; big=125; Hs=round(big*sc)
    PT=200; Hc=PT+max(rgb.shape[0],y0+Hs)+10; Wc=rgb.shape[1]+2*W
    can=np.zeros((Hc,Wc,3),int); can[:]=BG; m=np.ones((Hc,Wc),bool)
    can[PT:PT+rgb.shape[0],W:W+rgb.shape[1]]=rgb; m[PT:PT+rgb.shape[0],W:W+rgb.shape[1]]=bgmask; y0=y0+PT
    x0=W+cx-W//2
    arr=can[y0:y0+Hs,x0:x0+W]; msk=m[y0:y0+Hs,x0:x0+W]
    fig=arr[~msk]
    q=Image.fromarray(fig.reshape(1,-1,3).astype(np.uint8)).quantize(colors=n_auto,method=Image.MEDIANCUT,dither=Image.NONE)
    pc=q.getpalette()[:3*n_auto]; pc=pc[:len(pc)//3*3]
    pal=[tuple(int(v) for v in BG),WHITE]+[tuple(int(v) for v in c) for c in forced]+[tuple(int(v) for v in pc[i:i+3]) for i in range(0,len(pc),3)]
    P=np.array(pal[1:]); idx=np.zeros((big,TW),np.uint8)
    for j in range(big):
        for i in range(TW):
            ys=slice(int(j*Hs/big),int((j+1)*Hs/big)); xs=slice(int(i*W/TW),int((i+1)*W/TW))
            bm=msk[ys,xs].reshape(-1); blk=arr[ys,xs].reshape(-1,3)
            if bm.mean()>0.5: continue                     # bloque de fondo -> índice 0
            b=blk[~bm]
            d=((b[:,None,:]-P[None,:,:])**2).sum(2).argmin(1)
            idx[j,i]=1+np.bincount(d,minlength=len(P)).argmax()
    fill=ndi.binary_fill_holes(idx!=0)
    idx[fill&(idx==0)]=1                                   # huecos interiores nunca transparentes
    idx[ndi.binary_dilation(fill,iterations=1)&~fill]=1    # contorno blanco continuo de 2 px
    top=np.where((idx!=0).any(axis=1))[0].min(); idx=idx[top:top+TH]
    p=Image.fromarray(idx,"P"); flat=[v for c in pal for v in c]; p.putpalette(flat+[0]*(768-len(flat)))
    p.save(out+".png"); p.convert("RGB").resize((TW*5,TH*5),Image.NEAREST).save(out+"_x5.png")
    return p

def flood(bgcand, seeds):
    lab,_=ndi.label(bgcand); keep=np.unique(lab[seeds&bgcand]); keep=keep[keep>0]
    return np.isin(lab,keep)
