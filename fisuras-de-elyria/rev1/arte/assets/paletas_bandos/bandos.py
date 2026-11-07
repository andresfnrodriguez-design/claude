import numpy as np
from PIL import Image, ImageDraw, ImageFont
ALLY=['80a080','3c2c58','8a78c0','d0c8f0','6a4a48','c08a68','f4d8b8','1e2c6c','2f5cc8','3ea0e8','9ce4f8','c02838','f0dd60','7a8878','f0f0e8','282828']
def pal(sec,main):
    p=list(ALLY); p[1:4]=sec; p[7:11]=main; return p
B={'Protagonistas (blanco y cian)':pal(['1e3a4a','4aa8c0','c8e8f0'],['3a6a80','6ab8c8','bfeef0','f4ffff']),
   'Enemigos (vinotinto)':pal(['2a0e18','7a3a48','e0b0b8'],['3a0a18','6e1428','a02a3c','d0606a']),
   'Neutrales (amarillo)':pal(['3a2a10','a89058','f0e4b8'],['5a4210','a07a1c','e0b830','f8e890']),
   'Cuarta facción (púrpura)':pal(['1e1438','7a62a8','dcd0f4'],['2a1450','5a2a96','8e54d0','c8a0f0'])}
gba=lambda h:'%02x%02x%02x'%tuple(int(round(int(h[i:i+2],16)/255*31))*255//31 for i in (0,2,4))
B={k:[gba(c) for c in v] for k,v in B.items()}
rgb=lambda h:tuple(int(h[i:i+2],16) for i in (0,2,4))
spr=Image.open('/home/claude/azul/kairon_quieto_suroeste_azul_32x32.png'); k=np.array(spr)
fondo=Image.open('/home/claude/paleta/mapa_bs_x2.png').resize((320,320),Image.NEAREST).convert('RGBA')
tile=fondo.crop((96,232,96+4*40,232+40))  # franja de terreno
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',12)
S=5; W=4*44*S
out=Image.new('RGB',(W,52*S+70+4*26),(24,24,30)); d=ImageDraw.Draw(out)
strip=Image.new('RGBA',(4*44,52),(0,0,0,0)); strip.paste(fondo.crop((20,150,20+176,150+52)),(0,0))
for i,(n,p) in enumerate(B.items()):
    im=Image.fromarray(k,'P'); im.putpalette([v for c in p for v in rgb(c)]+[0]*720); im.info['transparency']=0
    s=im.convert('RGBA'); ys,xs=np.where(k>0); cx=(xs.min()+xs.max()+1)//2
    strip.alpha_composite(s,(i*44+22-cx,44-ys.max()))
    # barra de vida simple bajo los pies
    dd=ImageDraw.Draw(strip); dd.rectangle([i*44+15,45,i*44+29,47],fill=(57,57,49)); dd.rectangle([i*44+16,46,i*44+28,46],fill=(247,247,82))
out.paste(strip.resize((W,52*S),Image.NEAREST),(0,0))
for i,(n,p) in enumerate(B.items()):
    y=52*S+10+i*26; d.text((6,y+4),n,fill=(230,230,230),font=f)
    for j,c in enumerate(p[1:]): d.rectangle([260+j*22,y,260+j*22+20,y+20],fill=rgb(c))
out.save('bandos_x5.png')
with open('paletas_bandos.txt','w') as fo:
    for n,p in B.items(): fo.write(n+': '+' '.join('#'+c for c in p)+'\n')
print(open('paletas_bandos.txt').read())
