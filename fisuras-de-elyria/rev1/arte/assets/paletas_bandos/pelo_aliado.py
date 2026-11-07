import numpy as np
from PIL import Image, ImageDraw, ImageFont
exec(open('bandos.py').read().split("spr=Image.open")[0])
p=list(B['Protagonistas (blanco y cian)'])
p[2]=gba('3c9c5c')   # verde
# 11 rojo se mantiene
# 12 rubio se mantiene
p[13]=gba('7c48c0')  # púrpura (reemplaza gris)
OP=[(1,'azul marino'),(4,'castaño oscuro'),(5,'castaño claro'),(12,'rubio'),(11,'rojo'),
    (2,'verde'),(13,'púrpura'),(7,'azul acero'),(8,'celeste'),(9,'cian pálido'),
    (3,'hielo'),(10,'blanco azulado'),(14,'blanco plata'),(6,'rubio fresa')]
k=np.array(Image.open('/home/claude/azul/kairon_quieto_suroeste_azul_32x32.png'))
def con(slot):
    a=k.copy()
    for r in range(8,13):
        for c in range(1,31):
            if a[r,c]==15 and all(a[r+dr,c+dc]>0 for dr,dc in ((1,0),(-1,0),(0,1),(0,-1))): a[r,c]=slot
    return a
S=5; cw=24; cols=7
fondo=Image.open('/home/claude/paleta/mapa_bs_x2.png').convert('RGBA')
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',12)
CH=30*S+22; out=Image.new('RGB',(cols*cw*S,2*CH+60),(24,24,30)); d=ImageDraw.Draw(out)
for n,(s,nom) in enumerate(OP):
    r,c=divmod(n,cols); cell=fondo.crop((40+c*cw,300,40+c*cw+cw,330)).copy()
    a=con(s); im=Image.fromarray(a,'P'); im.putpalette([v for x in p for v in rgb(x)]+[0]*720); im.info['transparency']=0
    ys,xs=np.where(a>0); cell.alpha_composite(im.convert('RGBA'),(cw//2-(xs.min()+xs.max()+1)//2,28-ys.max()))
    out.paste(cell.resize((cw*S,30*S),Image.NEAREST),(c*cw*S,r*CH)); d.text((c*cw*S+4,r*CH+30*S+3),f'{nom} ({s})',fill=(230,230,230),font=f)
for j,x in enumerate(p[1:]): d.rectangle([4+j*30,2*CH+14,4+j*30+28,2*CH+42],fill=rgb(x)); d.text((10+j*30,2*CH+44),str(j+1),fill=(160,160,160),font=f)
out.save('pelo_aliado_x5.png')
open('paleta_aliado_pelos.txt','w').write('Aliados con pelos: '+' '.join('#'+x for x in p)+'\n')
print(' '.join('#'+x for x in p))
