import numpy as np
from PIL import Image, ImageDraw, ImageFont
gba=lambda h:'%02x%02x%02x'%tuple(int(round(int(h[i:i+2],16)/255*31))*255//31 for i in (0,2,4))
rgb=lambda h:tuple(int(h[i:i+2],16) for i in (0,2,4))
# 0 fondo | 1 oscuro | 2 pelo | 3 pelo | 4-6 piel | 7-10 rampa del bando | 11 12 pelo | 13 gris acero | 14 blanco | 15 contorno
B={
'Protagonistas':('839c83 101831 e69c31 deacb4 6a4a48 c08a68 f4d8b8 31206a 5aacee bd419c a4eede 18736a d53131 7888a0 f0f0e8 282828',
  'negro castaño_osc castaño_cl ámbar índigo celeste magenta menta rosa_pálido verde_azul. rojo gris plata'),
'Enemigos':('839c83 291018 eecd4a ee8bb4 6a4a48 c08a68 f4d8b8 390818 6a1029 9c2939 cd626a 399c5a 3162cd 7888a0 f0f0e8 282828',
  'negro castaño_osc castaño_cl rubio vino_osc. rojo_osc. rojo coral rosa verde azul gris plata'),
'Neutrales':('839c83 201810 3162cd ee8bb4 6a4a48 c08a68 f4d8b8 4a3010 a07018 e0b030 f8eca0 399c5a d53131 7888a0 f0f0e8 282828',
  'negro castaño_osc castaño_cl azul marrón_osc. ocre dorado platino rosa verde rojo gris plata'),
'Cuarta facción':('839c83 140c20 eecd4a 5aacee 6a4a48 c08a68 f4d8b8 2a1450 6a34b0 a868d8 f0c8e8 399c5a d53131 7888a0 f0f0e8 282828',
  'negro castaño_osc castaño_cl rubio violeta_osc. púrpura orquídea lila celeste verde rojo gris plata')}
ORD=[1,4,5,2,7,8,9,10,3,11,12,13,14]
k=np.array(Image.open('/home/claude/azul/kairon_quieto_suroeste_azul_32x32.png')); k[k==3]=10
def con(s):
    a=k.copy()
    for r in range(8,13):
        for c in range(1,31):
            if a[r,c]==15 and all(a[r+dr,c+dc]>0 for dr,dc in ((1,0),(-1,0),(0,1),(0,-1))): a[r,c]=s
    return a
S=4; cw=22; LW=120; RH=30*S; RT=RH+18
fondo=Image.open('/home/claude/paleta/mapa_bs_x2.png').convert('RGBA')
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',11)
out=Image.new('RGB',(LW+13*cw*S,4*RT+4*32+10),(24,24,30)); d=ImageDraw.Draw(out); txt=[]
for r,(n,(ps,ns)) in enumerate(B.items()):
    p=[gba(c) for c in ps.split()]; names=ns.split(); y=r*RT
    d.text((6,y+RH//2-6),n,fill=(235,235,235),font=f)
    for c,s in enumerate(ORD):
        cell=fondo.crop((40+c*cw,300,40+c*cw+cw,330)).copy(); a=con(s)
        im=Image.fromarray(a,'P'); im.putpalette([v for x in p for v in rgb(x)]+[0]*720); im.info['transparency']=0
        ys,xs=np.where(a>0); cell.alpha_composite(im.convert('RGBA'),(cw//2-(xs.min()+xs.max()+1)//2,28-ys.max()))
        out.paste(cell.resize((cw*S,RH),Image.NEAREST),(LW+c*cw*S,y)); d.text((LW+c*cw*S+3,y+RH+2),names[c].replace('_',' ')+f' ({s})',fill=(210,210,210),font=f)
    y2=4*RT+6+r*32; d.text((6,y2+6),n,fill=(200,200,200),font=f)
    for j,x in enumerate(p[1:]): d.rectangle([LW+j*32,y2,LW+j*32+28,y2+26],fill=rgb(x))
    txt.append(n+': '+' '.join('#'+x for x in p))
out.save('paletas_finales_x4.png')
open('paletas_finales.txt','w').write('0 fondo | 1 oscuro | 2,3 pelo | 4-6 piel | 7-10 rampa del bando | 11,12 pelo | 13 gris acero | 14 blanco | 15 contorno\n'+'\n'.join(txt)+'\n')
print(open('paletas_finales.txt').read())
