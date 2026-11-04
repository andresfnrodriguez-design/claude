# Ninja azul sin la fila de sombra (19x17) y mapa de tipos de color por posición de paleta.
from PIL import Image,ImageDraw
import recolor_ninja as rn
idx=[r[:] for r in rn.idx]
# quita solo el píxel de sombra más a la izquierda
j,i=min(((j,i) for j,r in enumerate(idx) for i,k in enumerate(r) if k==13),key=lambda t:t[1]);idx[j][i]=0;print('quitado',i,j)
H,W=len(idx),len(idx[0]);print(W,H)
from rampas_corregidas import R,slots
p=rn.base[:];sl=slots(R['Azul']);p[1:4]=sl['secundaria_1_3'];p[7:11]=sl['principal_7_10']
pal=[tuple(int(c[j:j+2],16) for j in (0,2,4)) for c in p]
TIPOS={'Principal (7-10)':((7,8,9,10),(40,90,220)),'Secundaria (1-3)':((1,2,3),(170,200,240)),
       'Piel (4-6)':((4,5,6),(240,170,120)),'Oro (12)':((12,),(230,190,40)),
       'Blanco (14)':((14,),(255,255,255)),'Contorno (15)':((15,),(30,20,40)),'Sombra suelo (13)':((13,),(110,130,110))}
im=Image.new('RGBA',(W,H),(0,0,0,0));tm=Image.new('RGBA',(W,H),(0,0,0,0))
for y,row in enumerate(idx):
    for x,k in enumerate(row):
        if not k:continue
        im.putpixel((x,y),pal[k]+(255,))
        for n,(ks,c) in TIPOS.items():
            if k in ks:tm.putpixel((x,y),c+(255,))
im.save('ninja_azul.png')
s=12;out=Image.new('RGB',(W*s*2+40+170,H*s+60),(0x80,0xa0,0x80));d=ImageDraw.Draw(out)
for i,img in enumerate((im,tm)):
    b=img.resize((W*s,H*s),Image.NEAREST);out.paste(b,(10+i*(W*s+20),10),b)
out.paste(im,(10,H*s+25),im)
for j,(n,(ks,c)) in enumerate(TIPOS.items()):
    y=14+j*24;x=W*s*2+50
    d.rectangle([x,y,x+16,y+16],fill=c,outline=(0,0,0));d.text((x+22,y+3),n,fill='black')
    for i,k in enumerate(ks):d.rectangle([x+22+i*18,y+14,x+38+i*18,y+20],fill=pal[k])
out.save('ninja_azul_tipos.png')
