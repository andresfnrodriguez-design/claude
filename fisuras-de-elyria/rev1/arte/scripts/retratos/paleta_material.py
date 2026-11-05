import numpy as np
ANCHORS={"crema":((239,233,207),3),"granate":((100,36,52),2),"marron":((60,34,45),2),
         "bronce":((150,112,73),2),"cian":((120,168,168),1),"piel":((235,165,125),2),"pelo":((53,52,51),1)}
def tonos(pixels):
    """13 colores agrupados por material de la ficha: cada píxel va a su material más cercano
    y dentro de cada material se toman tonos por luminosidad."""
    names=list(ANCHORS); A=np.array([ANCHORS[n][0] for n in names])
    lum=pixels.sum(1)
    keep=lum>90                      # lo muy oscuro es línea, va al negro aparte
    px=pixels[keep]
    d=((px[:,None,:]-A[None,:,:])**2).sum(2).argmin(1)
    out=[]
    for i,n in enumerate(names):
        g=px[d==i]; k=ANCHORS[n][1]
        if len(g)<20: out+= [A[i]]*k; continue
        L=g.sum(1); qs=np.quantile(L,np.linspace(0,1,k+1))
        for a,b in zip(qs[:-1],qs[1:]):
            sel=g[(L>=a)&(L<=b)]; out.append(np.median(sel,axis=0))
    return out
