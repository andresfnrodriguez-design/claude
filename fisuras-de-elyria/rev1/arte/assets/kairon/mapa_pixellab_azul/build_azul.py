from PIL import Image, ImageSequence
import numpy as np, sys
ALLY=['80a080','3c2c58','8a78c0','d0c8f0','6a4a48','c08a68','f4d8b8','1e2c6c','2f5cc8','3ea0e8','9ce4f8','c02838','f0dd60','7a8878','f0f0e8','282828']
PAL=[tuple(int(h[i:i+2],16) for i in (0,2,4)) for h in ALLY]
MAP={'1e1a20':15,'f2e6c8':14,'c9b48e':3,'8f7a58':13,'3a3f48':13,'4a1220':8,'7a2234':8,
     '2e2428':1,'4a3a33':4,'e8b796':6,'b97f62':5,'b8863b':5,'7a5524':4,'3fe0e6':10,'6b7280':13}
g=Image.open(sys.argv[1]); fr=[f.convert('RGBA') for f in ImageSequence.Iterator(g)]
def idx(f):
    a=np.array(f); k=np.zeros(a.shape[:2],np.uint8)
    for y in range(a.shape[0]):
        for x in range(a.shape[1]):
            if a[y,x,3]: k[y,x]=MAP['%02x%02x%02x'%tuple(a[y,x,:3])]
    return k
V={'abajo':idx(fr[0]),'derecha':idx(fr[2]),'arriba':idx(fr[4]),'izquierda':idx(fr[6])}
def P(k):
    im=Image.fromarray(k,'P'); im.putpalette([v for c in PAL for v in c]+[0]*720); im.info['transparency']=0; return im
def crop(k,w,h):  # figura centrada en x, pies abajo
    ys,xs=np.where(k>0); cx=(xs.min()+xs.max()+1)//2; out=np.zeros((h,w),np.uint8)
    sub=k[:ys.max()+1]; y0=h-sub.shape[0]
    src=sub[max(0,-y0):, :]; y0=max(0,y0)
    x0=w//2-cx
    for y in range(src.shape[0]):
        for x in range(32):
            if src[y,x] and 0<=x+x0<w: out[y0+y,x+x0]=src[y,x]
    return out
for n,k in V.items():
    c=crop(k,32,32); P(c).save(f'kairon_{n}_32x32.png')
# quieto formato Ephraim 16x96 (3 cuadros 16x32, pies en la fila 31 de cada cuadro)
q=crop(V['abajo'],16,32); P(np.vstack([q,q,q])).save('unit_icon_wait_Kairon_16x96.png')
# movimiento 32x480: 4 izquierda, 4 abajo, 4 arriba, 3 seleccionado (celdas 32x32, pies en la fila 31)
L,D,U=[crop(V[n],32,32) for n in ('izquierda','abajo','arriba')]
P(np.vstack([L]*4+[D]*4+[U]*4+[D]*3)).save('unit_icon_move_Kairon_32x480.png')
# vista previa
S=8; prev=Image.new('RGBA',(4*(32*S+16),32*S),(110,150,90,255))
for i,n in enumerate(['abajo','izquierda','arriba','derecha']):
    im=Image.open(f'kairon_{n}_32x32.png').convert('RGBA').resize((32*S,32*S),Image.NEAREST); prev.alpha_composite(im,(i*(32*S+16),0))
prev.save('vista_azul_x8.png')
with open('paleta_aliados_contorno282828.agbpal','wb') as f:
    for r,gg,b in PAL: v=(r>>3)|((gg>>3)<<5)|((b>>3)<<10); f.write(bytes([v&255,v>>8]))
print('ok')
