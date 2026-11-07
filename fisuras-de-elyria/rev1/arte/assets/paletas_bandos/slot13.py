import numpy as np
from PIL import Image, ImageDraw, ImageFont
gba=lambda h:'%02x%02x%02x'%tuple(int(round(int(h[i:i+2],16)/255*31))*255//31 for i in (0,2,4))
rgb=lambda h:tuple(int(h[i:i+2],16) for i in (0,2,4))
ALI='839c83 101831 e69c31 deacb4 6a4a4a bd8b6a f6d5b4 31206a 5aacee bd419c a4eede 18736a d53131 bd6229 eeeee6 292929'.split()
OPC=[('púrpura','8050c8'),('lavanda','b090e8'),('gris acero','7888a0'),('verde','48b048'),('lima','b0d848')]
base=np.array(Image.open('/home/claude/azul/kairon_quieto_suroeste_azul_32x32.png')); base[base==3]=10
def con(s):
    a=base.copy()
    for r in range(8,13):
        for c in range(1,31):
            if a[r,c]==15 and all(a[r+dr,c+dc]>0 for dr,dc in ((1,0),(-1,0),(0,1),(0,-1))): a[r,c]=s
    return a
S=6; cw=22; fondo=Image.open('/home/claude/paleta/mapa_bs_x2.png').convert('RGBA')
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',12)
cols=[('ámbar (2)',None,2),('rojo (12)',None,12),('magenta (9)',None,9),('verde az. (11)',None,11)]+[(n,h,13) for n,h in OPC]
out=Image.new('RGB',(len(cols)*cw*S,30*S+40),(24,24,30)); d=ImageDraw.Draw(out)
for c,(n,h,s) in enumerate(cols):
    p=list(ALI); p[13]=gba(h) if h else p[13]; a=con(s)
    cell=fondo.crop((40+c*cw,300,40+c*cw+cw,330)).copy()
    im=Image.fromarray(a,'P'); im.putpalette([v for x in p for v in rgb(x)]+[0]*720); im.info['transparency']=0
    ys,xs=np.where(a>0); cell.alpha_composite(im.convert('RGBA'),(cw//2-(xs.min()+xs.max()+1)//2,28-ys.max()))
    out.paste(cell.resize((cw*S,30*S),Image.NEAREST),(c*cw*S,0))
    d.text((c*cw*S+4,30*S+4),n,fill=(230,230,230) if h else (150,150,150),font=f)
    if h: d.text((c*cw*S+4,30*S+19),'#'+p[13],fill=(160,160,160),font=f)
out.save('slot13_x6.png')
