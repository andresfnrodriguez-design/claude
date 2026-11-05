from PIL import Image
import numpy as np
from scipy import ndimage as ndi
BG=(0xA9,0xCB,0xA6); WHITE=(255,255,255); BLACK=(0x17,0x0C,0x16)
TOP=3   # margen verde arriba

def extend(fig, frac=0.14, bottom=0):
    """Completa en negro la silueta donde la imagen original la corta (costados y arriba).
    Devuelve (fig_ext, ext, pad) sobre un lienzo agrandado."""
    H,W=fig.shape; E=int(W*frac)+4
    pad=E
    F=np.zeros((H+pad+bottom,W+2*pad),bool); F[pad:pad+H,pad:pad+W]=fig
    ext=np.zeros_like(F)
    if bottom:
        # el cuerpo sigue hacia abajo, en negro, con el ancho de la última fila
        last=fig[-12:].all(0)
        for y in range(bottom): ext[pad+H+y,pad:pad+W]=last
    for side in ("L","R"):
        col=fig[:,0] if side=="L" else fig[:,-1]
        rows=np.where(col)[0]
        if not len(rows): continue
        y_t=rows.min()
        # pendiente del contorno en las filas previas al contacto
        ys=[];xs=[]
        for y in range(max(0,y_t-20),y_t):
            xx=np.where(fig[y])[0]
            if len(xx): ys.append(y); xs.append(xx.min() if side=="L" else W-1-xx.max())
        slope=max(0.15,-np.polyfit(ys,xs,1)[0]) if len(ys)>3 else 0.4
        e=np.zeros(H)
        for y in rows: e[y]=min(E-2,slope*(y-y_t+1))
        e=ndi.uniform_filter1d(e,9)                   # para que entre y salga suave
        for y in range(H):
            n=int(round(e[y]))
            if n<=0 or not col[y]: continue
            if side=="L": ext[pad+y,pad-n:pad]=True
            else: ext[pad+y,pad+W:pad+W+n]=True
    top=np.where(fig[0])[0]
    if len(top):
        c=(top.min()+top.max())/2; w=(top.max()-top.min())/2+1; hcap=min(pad-2,int(w*0.35))
        for x in range(top.min(),top.max()+1):
            if fig[0,x]:
                h=int(round(hcap*np.sqrt(max(0,1-((x-c)/w)**2))))
                ext[pad-h:pad,pad+x]=True
    ext=ndi.binary_closing(ext|F,iterations=2)&~F
    return F|ext, ext, pad

def build(rgb, fig, out, TW, TH, n_auto=12, forced=(), s_fixed=None, dry=False, bottom=0, pal_fixed=None):
    F,ext,pad=extend(fig,bottom=bottom)
    H,W=fig.shape
    C=np.zeros(F.shape+(3,),int); C[:]=BG; C[pad:pad+H,pad:pad+W]=rgb
    # completar lo agregado con los colores vecinos en vez de negro
    if bottom:
        src=np.median(C[pad+H-14:pad+H-4, :], axis=0)          # la ropa sigue hacia abajo
        rows=np.where(ext[pad+H:].any(1))[0]
        C[pad+H:pad+H+len(rows)] = src[None,:,:]
        # sombra suave hacia abajo, como pliegue de tela
    for y in range(F.shape[0]):
        xs=np.where(ext[y])[0]
        if not len(xs): continue
        fx=np.where(F[y]&~ext[y])[0]
        if not len(fx): continue
        L=xs[xs<fx.min()]; Rr=xs[xs>fx.max()]
        if len(L): C[y,L]=np.median(C[y,fx.min():fx.min()+4],axis=0)
        if len(Rr): C[y,Rr]=np.median(C[y,fx.max()-3:fx.max()+1],axis=0)
    top_ext=ext.copy(); top_ext[pad:]=False
    for x in np.where(top_ext.any(0))[0]:
        ys=np.where(top_ext[:,x])[0]; C[ys,x]=C[ys.max()+1,x]
    top=np.where(F.any(1))[0].min()
    # escala máxima con la que toda la silueta visible entra a lo ancho (con su contorno blanco)
    s=1.0 if s_fixed is None else s_fixed
    while True:
        rows=int((TH-TOP-1)/s)
        vis=F[top:top+rows]; xx=np.where(vis.any(0))[0]
        if s_fixed is not None or (xx.max()-xx.min()+1)*s+2<=TW: break
        s-=0.002
    if dry: return s
    x0=(xx.min()+xx.max()+1)/2-(TW/s)/2
    gw,gh=TW,int((TH-TOP)/s*s)+0; gh=TH-TOP+2
    figpix=C[F&~ext]
    q=Image.fromarray(figpix.reshape(1,-1,3).astype(np.uint8)).quantize(colors=n_auto,method=Image.MEDIANCUT,dither=Image.NONE)
    pc=q.getpalette()[:3*n_auto]
    pal=[BG,WHITE,BLACK]+[tuple(int(v) for v in c) for c in forced]+[tuple(pc[i:i+3]) for i in range(0,3*n_auto,3)]
    if pal_fixed is not None: pal=[BG,WHITE,BLACK]+[tuple(int(v) for v in c) for c in pal_fixed]
    P=np.array(pal[1:])
    idx=np.zeros((gh,gw),np.uint8); cell=1/s
    for j in range(gh):
        for i in range(gw):
            ya=int(top+j*cell); yb=max(ya+1,int(top+(j+1)*cell)); xa=int(x0+i*cell); xb=max(xa+1,int(x0+(i+1)*cell))
            if xa<0 or xb>F.shape[1] or yb>F.shape[0]: continue
            m=F[ya:yb,xa:xb].reshape(-1)
            if m.mean()<=0.5: continue
            b=C[ya:yb,xa:xb].reshape(-1,3)[m]
            idx[j,i]=1+np.bincount(((b[:,None,:]-P[None,:,:])**2).sum(2).argmin(1),minlength=len(P)).argmax()
    # líneas: negro 1 px en el borde de la silueta, blanco 1 px por fuera
    fg=ndi.binary_fill_holes(idx!=0)
    lab,n=ndi.label(fg); sz=ndi.sum(fg,lab,range(1,n+1))
    for k,v in enumerate(sz,1):
        if v<10: fg[lab==k]=False; idx[lab==k]=0
    e1=ndi.binary_erosion(fg); e2=ndi.binary_erosion(e1); e3=ndi.binary_erosion(e2)
    lum=np.array(pal).sum(1)
    for y,x in zip(*np.where(e1&~e2)):
        if lum[idx[y,x]]<240:
            win=idx[max(0,y-2):y+3,max(0,x-2):x+3][e3[max(0,y-2):y+3,max(0,x-2):x+3]]
            win=win[lum[win]>=240]
            if win.size: idx[y,x]=np.bincount(win).argmax()
    idx[fg&~e1]=2
    idx[ndi.binary_dilation(fg)&~fg]=1
    # margen de TOP filas arriba; abajo corta el cuadro
    t=np.where((idx!=0).any(1))[0].min()
    outi=np.zeros((TH,TW),np.uint8); part=idx[t:t+TH-TOP]; outi[TOP:TOP+part.shape[0]]=part
    last=outi[-1]; bad=(last==1)|(last==2); last[bad]=outi[-3][bad]
    im=Image.fromarray(outi,"P"); flat=[v for c in pal for v in c]; im.putpalette(flat+[0]*(768-len(flat)))
    im.save(out+".png"); im.convert("RGB").resize((TW*5,TH*5),Image.NEAREST).save(out+"_x5.png")
    # vista de control de la silueta completada, antes de escalar
    v=C.copy(); v[~F]=BG
    Image.fromarray(v.astype(np.uint8)).save(out+"_completado.png")
    return s
