# Contorno interior solo en el lado de la sombra (abajo/derecha); el lado de la luz conserva el color original.
from PIL import Image
OUT=(0x24,0x1c,0x2c,255);SOMBRA=(0x7a,0x88,0x78)
orig=Image.open('ninja_propuesta_aliado.png').convert('RGBA');orig=orig.crop(orig.getbbox())
W,H=orig.size;im=orig.copy()
def vacio(x,y):
    if not(0<=x<W and 0<=y<H):return True
    p=orig.getpixel((x,y));return p[3]==0 or p[:3]==SOMBRA
for y in range(H):
    for x in range(W):
        p=orig.getpixel((x,y))
        if p[3] and p[:3]!=SOMBRA and (vacio(x+1,y) or vacio(x,y+1)):im.putpixel((x,y),OUT)
im.save('ninja_lado_sombra.png')
mid=Image.open('ninja_punto_medio.png').convert('RGBA')
s=10;imgs=[orig,mid,im];h=max(i.height for i in imgs)
out=Image.new('RGB',(sum(i.width*s+10 for i in imgs)+10,h*s+20),(0x80,0xa0,0x80));x0=10
for i in imgs:
    b=i.resize((i.width*s,i.height*s),Image.NEAREST);out.paste(b,(x0,10+(h-i.height)*s),b);x0+=i.width*s+10
out.save('ninja_lado_sombra_comparacion.png')
# en el mapa
m=Image.open('mapa_prueba.png').convert('RGBA').crop((32,64,272,224))
for sp,(cx,cy) in ((orig,(1,7)),(im,(3,7)),(orig,(9,4)),(im,(11,4))):
    m.alpha_composite(sp,(cx*16+(16-sp.width)//2,(cy+1)*16-sp.height))
m.resize((720,480),Image.NEAREST).save('ninja_lado_sombra_mapa_x3.png')
