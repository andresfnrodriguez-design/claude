import numpy as np
from PIL import Image, ImageDraw, ImageFont
gba=lambda h:'%02x%02x%02x'%tuple(int(round(int(h[i:i+2],16)/255*31))*255//31 for i in (0,2,4))
rgb=lambda h:tuple(int(h[i:i+2],16) for i in (0,2,4))
COMUN={0:'80a080',4:'6a4a48',5:'c08a68',6:'f4d8b8',14:'f0f0e8',15:'282828',
       2:'eecd4a',10:'e68339',11:'d83030',9:'ee8bb4',12:'399c5a',13:'3162cd'}   # pelos fijos
BANDO={'Protagonistas':['20394a','c5e6ee','396a83','6ab4c5'],
       'Enemigos':['291018','deacb4','6a1029','9c2939'],
       'Neutrales':['392910','f6e694','9c7b18','deb431'],
       'Cuarta facción':['201039','decdf6','5a2994','8b52cd']}   # slots 1,3,7,8
P={}
for n,(a,b,c,d) in BANDO.items():
    p=dict(COMUN); p.update({1:a,3:b,7:c,8:d}); P[n]=[gba(p[i]) for i in range(16)]
OP=[(1,'bando'),(4,'castaño'),(5,'cast. claro'),(2,'rubio'),(10,'naranja'),(11,'rojo'),(9,'rosa'),(12,'verde'),(13,'azul'),(14,'plata')]
k=np.array(Image.open('/home/claude/azul/kairon_quieto_suroeste_azul_32x32.png')); k[k==10]=14
def con(s):
    a=k.copy()
    for r in range(8,13):
        for c in range(1,31):
            if a[r,c]==15 and all(a[r+dr,c+dc]>0 for dr,dc in ((1,0),(-1,0),(0,1),(0,-1))): a[r,c]=s
    return a
S=4; cw=22; LW=130
fondo=Image.open('/home/claude/paleta/mapa_bs_x2.png').convert('RGBA')
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',12)
RH=30*S; out=Image.new('RGB',(LW+len(OP)*cw*S,22+4*RH+4*30),(24,24,30)); d=ImageDraw.Draw(out)
for c,(s,nom) in enumerate(OP): d.text((LW+c*cw*S+4,4),nom,fill=(230,230,230),font=f)
for r,(n,p) in enumerate(P.items()):
    y=22+r*RH; d.text((6,y+RH//2-6),n,fill=(230,230,230),font=f)
    for c,(s,_) in enumerate(OP):
        cell=fondo.crop((40+c*cw,300,40+c*cw+cw,330)).copy(); a=con(s)
        im=Image.fromarray(a,'P'); im.putpalette([v for x in p for v in rgb(x)]+[0]*720); im.info['transparency']=0
        ys,xs=np.where(a>0); cell.alpha_composite(im.convert('RGBA'),(cw//2-(xs.min()+xs.max()+1)//2,28-ys.max()))
        out.paste(cell.resize((cw*S,RH),Image.NEAREST),(LW+c*cw*S,y))
for r,(n,p) in enumerate(P.items()):
    y=22+4*RH+6+r*30; d.text((6,y+5),n,fill=(200,200,200),font=f)
    for j,x in enumerate(p[1:]): d.rectangle([LW+j*30,y,LW+j*30+26,y+24],fill=rgb(x))
out.save('unificada_x4.png')
with open('paletas_unificadas.txt','w') as fo:
    fo.write('Slots 1,3,7,8 bando | 4-6 piel | 2,9-13 pelo fijo | 14 blanco | 15 contorno\n')
    for n,p in P.items(): fo.write(n+': '+' '.join('#'+x for x in p)+'\n')
print(open('paletas_unificadas.txt').read())
