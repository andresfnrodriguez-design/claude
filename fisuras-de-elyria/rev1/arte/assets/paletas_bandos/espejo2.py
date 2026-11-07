import numpy as np
from PIL import Image, ImageDraw, ImageFont
gba=lambda h:'%02x%02x%02x'%tuple(int(round(int(h[i:i+2],16)/255*31))*255//31 for i in (0,2,4))
rgb=lambda h:tuple(int(h[i:i+2],16) for i in (0,2,4))
ENE='839c83 291018 eecd4a deacb4 6a4a4a bd8b6a f6d5b4 390818 6a1029 9c2939 cd626a 399c5a 3162cd 7b4abd eeeee6 292929'.split()
ALI=list(ENE)
ALI[1]='141c30'                                   # negro azulado
ALI[3]='ee8bb4'                                   # rosa
ALI[7:11]=['34206e','2f5cc8','2aa8b8','a8f0dc']   # rampa con giro de tono: índigo, azul, turquesa, menta hielo
ALI[13]='e68339'                                  # naranja (el púrpura lo cubre el índigo)
ALI[12]='d83030'                                  # rojo (el azul ya lo da la rampa)
ALI=[gba(c) for c in ALI]
OPS={'Aliados':(ALI,[(1,'negro'),(4,'castaño osc.'),(5,'castaño cl.'),(2,'rubio'),(7,'índigo'),(8,'azul'),(9,'turquesa'),
                    (10,'menta'),(3,'rosa'),(11,'verde'),(12,'rojo'),(13,'naranja'),(14,'plata')]),
     'Enemigos':(ENE,[(1,'negro'),(4,'castaño osc.'),(5,'castaño cl.'),(2,'rubio'),(7,'vino osc.'),(8,'rojo osc.'),(9,'rojo'),
                    (10,'coral'),(3,'rosa pálido'),(11,'verde'),(12,'azul'),(13,'púrpura'),(14,'plata')])}
k=np.array(Image.open('/home/claude/azul/kairon_quieto_suroeste_azul_32x32.png')); k[k==3]=10  # el claro del abrigo pasa al 10
def con(s):
    a=k.copy()
    for r in range(8,13):
        for c in range(1,31):
            if a[r,c]==15 and all(a[r+dr,c+dc]>0 for dr,dc in ((1,0),(-1,0),(0,1),(0,-1))): a[r,c]=s
    return a
S=4; cw=22; LW=90; RH=30*S
fondo=Image.open('/home/claude/paleta/mapa_bs_x2.png').convert('RGBA')
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',11)
out=Image.new('RGB',(LW+13*cw*S,2*(RH+20)+70),(24,24,30)); d=ImageDraw.Draw(out)
for r,(n,(p,ops)) in enumerate(OPS.items()):
    y=r*(RH+20); d.text((6,y+RH//2-6),n,fill=(230,230,230),font=f)
    for c,(s,nom) in enumerate(ops):
        cell=fondo.crop((40+c*cw,300,40+c*cw+cw,330)).copy(); a=con(s)
        im=Image.fromarray(a,'P'); im.putpalette([v for x in p for v in rgb(x)]+[0]*720); im.info['transparency']=0
        ys,xs=np.where(a>0); cell.alpha_composite(im.convert('RGBA'),(cw//2-(xs.min()+xs.max()+1)//2,28-ys.max()))
        out.paste(cell.resize((cw*S,RH),Image.NEAREST),(LW+c*cw*S,y)); d.text((LW+c*cw*S+3,y+RH+3),f'{nom} ({s})',fill=(220,220,220),font=f)
for r,(n,(p,_)) in enumerate(OPS.items()):
    y=2*(RH+20)+8+r*30
    for j,x in enumerate(p[1:]): d.rectangle([LW+j*30,y,LW+j*30+26,y+24],fill=rgb(x)); 
    d.text((6,y+5),n,fill=(200,200,200),font=f)
out.save('espejo2_x4.png')
open('paletas_espejo2.txt','w').write(''.join(n+': '+' '.join('#'+x for x in p)+'\n' for n,(p,_) in OPS.items()))
print(open('paletas_espejo2.txt').read())
