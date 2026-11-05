# Maqueta: ninja del usuario en 5 paletas GBA y 5 paletas propuestas, usando las 15 posiciones.
from PIL import Image,ImageDraw
import recolor_ninja as rn
from rampas_corregidas import R,slots
idx=[r[:] for r in rn.idx]
j,i=min(((j,i) for j,r in enumerate(idx) for i,k in enumerate(r) if k==13),key=lambda t:t[1]);idx[j][i]=0
H,W=len(idx),len(idx[0])
# 1) acento rojo: un adorno en la capucha
idx[1][8]=11
# 2) azul más oscuro de la ropa (posición 8 junto al contorno) -> 7, para dar volumen
src=[r[:] for r in idx]
for y in range(H):
    for x in range(W):
        if src[y][x]==8 and any(0<=y+dy<H and 0<=x+dx<W and src[y+dy][x+dx]==15 for dy,dx in((1,0),(-1,0),(0,1),(0,-1))):
            idx[y][x]=7
# 3) sombra de piel en la mano izquierda (lado izquierdo de la imagen)
for x,y in((4,8),(5,8)):idx[y][x]=4
# 4) sombra de piel en el lado derecho de la cara y el cuello
for y in range(2,7):
    xs=[x for x in range(W) if idx[y][x] in(5,6)]
    if xs:idx[y][max(xs)]=4
print('posiciones usadas:',sorted({k for r in idx for k in r if k}))
GBA={'Aliado':'80a080 584878 90b8e8 d8e8f0 706060 b09058 f8f8d0 383890 3850e0 28a0f8 18f0f8 e81018 f8f840 808870 f8f8f8 403838',
     'Enemigo':'80a080 684860 c0a8b8 e0e0e0 706060 b09058 f8f8d0 602820 a83028 e01010 f85048 38d030 f8f840 808870 f8f8f8 403838',
     'Neutral':'80a080 385038 98c880 d8f8b8 585850 a08840 f8f8c0 205010 089000 18d010 50f838 0078c8 e0f828 808870 f8f8f8 384038',
     'Usado':'80a080 404040 787878 b8b8b8 505050 808080 c8c8c8 484848 585858 989898 b8b8b8 707070 c8c8c8 808870 d0d0d0 403838',
     'Arena':'80a080 584068 a8a8e8 e0e0f8 786050 c08848 f8f8c8 584060 806090 b898e0 d0c0f8 e81018 f8f828 808870 f8f8f8 482840'}
MEJ='80a080 3c2c58 8a78c0 d0c8f0 6a4a48 c08a68 f4d8b8 1e2c6c 2f5cc8 3ea0e8 9ce4f8 c02838 f0dd60 7a8878 f0f0e8 241c2c'.split()
def prop(rampa,acento):
    p=MEJ[:];sl=slots(R[rampa]);p[1:4]=sl['secundaria_1_3'];p[7:11]=sl['principal_7_10'];p[11]=acento;return ' '.join(p)
def gris(p):
    out=[]
    for h in p.split():
        r,g,b=(int(h[i:i+2],16) for i in (0,2,4));y=round(.299*r+.587*g+.114*b);out.append('%02x%02x%02x'%(y,y,y))
    out[0]=MEJ[0];return ' '.join(out)
PROP={'Aliado':' '.join(MEJ),'Enemigo':prop('Rojo','38a048'),'Neutral':prop('Verde','3070c8'),
      'Usado':gris(' '.join(MEJ)),'Arena':' '.join(MEJ[:1]+'584068 a8a8e8 e0e0f8'.split()+MEJ[4:7]+'584060 806090 b898e0 d0c0f8'.split()+['c02838']+MEJ[12:])}
s=6;cw=W*s+16;out=Image.new('RGB',(cw*5+110,2*(H*s+60)+10),(0x80,0xa0,0x80));d=ImageDraw.Draw(out)
for row,(titulo,P) in enumerate((('GBA',GBA),('Propuesta',PROP))):
    y0=10+row*(H*s+60);d.text((cw*5+12,y0+H*s//2),titulo,fill='black')
    for c,(n,p) in enumerate(P.items()):
        pal=[tuple(int(h[j:j+2],16) for j in (0,2,4)) for h in p.split()]
        im=Image.new('RGBA',(W,H),(0,0,0,0))
        for y,r in enumerate(idx):
            for x,k in enumerate(r):
                if k:im.putpixel((x,y),pal[k]+(255,))
        im.save(f'ninja_{titulo.lower()}_{n.lower()}.png')
        x0=8+c*cw;b=im.resize((W*s,H*s),Image.NEAREST);out.paste(b,(x0,y0),b)
        out.paste(im,(x0,y0+H*s+6),im);d.text((x0+W+6,y0+H*s+8),n,fill='black')
        for k in range(1,16):d.rectangle([x0+(k-1)*7,y0+H*s+30,x0+(k-1)*7+5,y0+H*s+42],fill=pal[k])
out.save('ninja_maqueta.png')
