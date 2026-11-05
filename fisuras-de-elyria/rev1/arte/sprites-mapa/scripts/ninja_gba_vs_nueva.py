# Ninja del usuario pintado con la paleta GBA Ally vs la paleta nueva de 15 colores.
from PIL import Image,ImageDraw
import recolor_ninja as rn
idx=[r[:] for r in rn.idx]
j,i=min(((j,i) for j,r in enumerate(idx) for i,k in enumerate(r) if k==13),key=lambda t:t[1]);idx[j][i]=0
PAL={'GBA Ally':'80a080 584878 90b8e8 d8e8f0 706060 b09058 f8f8d0 383890 3850e0 28a0f8 18f0f8 e81018 f8f840 808870 f8f8f8 403838',
     'Nueva 15':'80a080 3c2c58 8a78c0 d0c8f0 6a4a48 c08a68 f4d8b8 1e2c6c 2f5cc8 3ea0e8 9ce4f8 c02838 f0dd60 7a8878 f0f0e8 241c2c'}
H,W=len(idx),len(idx[0]);s=12;usados=sorted({k for r in idx for k in r if k})
out=Image.new('RGB',(2*(W*s+30)+10,H*s+110),(0x80,0xa0,0x80));d=ImageDraw.Draw(out)
for n_,(n,p) in enumerate(PAL.items()):
    pal=[tuple(int(c[j:j+2],16) for j in (0,2,4)) for c in p.split()]
    im=Image.new('RGBA',(W,H),(0,0,0,0))
    for y,r in enumerate(idx):
        for x,k in enumerate(r):
            if k:im.putpixel((x,y),pal[k]+(255,))
    im.save(f'ninja_{n.split()[0].lower()}.png')
    x0=10+n_*(W*s+30);b=im.resize((W*s,H*s),Image.NEAREST);out.paste(b,(x0,10),b)
    d.text((x0,H*s+16),n,fill='black')
    for k in range(1,16):
        x=x0+(k-1)*15;d.rectangle([x,H*s+32,x+13,H*s+46],fill=pal[k],outline=(0,0,0) if k in usados else None)
    out.paste(im,(x0,H*s+56),im)
out.save('ninja_gba_vs_nueva.png');print('posiciones usadas:',usados)
