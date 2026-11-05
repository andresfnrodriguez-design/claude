# Punto medio: contorno DENTRO de la silueta original (no la engorda) + sel-out en el lado de la luz.
from PIL import Image
OUT=(0x24,0x1c,0x2c,255);SOMBRA=(0x7a,0x88,0x78)
from selout import OSCURO
orig=Image.open('ninja_propuesta_aliado.png').convert('RGBA');orig=orig.crop(orig.getbbox())
W,H=orig.size;im=orig.copy()
def px(img,x,y):return img.getpixel((x,y)) if 0<=x<W and 0<=y<H else (0,0,0,0)
# 1) el píxel de borde (toca el fondo) se vuelve contorno, salvo sombra del suelo
for y in range(H):
    for x in range(W):
        p=px(orig,x,y)
        if not p[3] or p[:3]==SOMBRA:continue
        if any(px(orig,x+dx,y+dy)[3]==0 or px(orig,x+dx,y+dy)[:3]==SOMBRA for dx,dy in((1,0),(-1,0),(0,1),(0,-1))):
            im.putpixel((x,y),OUT)
# 2) sel-out: en el lado de la luz, el borde toma el tono oscuro de su propio material original
for y in range(H):
    for x in range(W):
        if im.getpixel((x,y))!=OUT:continue
        if (px(orig,x-1,y)[3]==0 or px(orig,x,y-1)[3]==0) and px(orig,x,y)[:3] in OSCURO:
            im.putpixel((x,y),OSCURO[px(orig,x,y)[:3]]+(255,))
im.save('ninja_punto_medio.png')
# versión "gorda" sin la línea de la pelvis
g=Image.open('ninja_selout_pelvis.png').convert('RGBA')
for x in range(4,8):g.putpixel((x,13),(0,0,0,0))
g.save('ninja_selout_pelvis.png')
s=10;imgs=[orig,g,im];out=Image.new('RGB',(sum(i.width*s+10 for i in imgs)+10,max(i.height for i in imgs)*s+20),(0x80,0xa0,0x80));x0=10
for i in imgs:
    b=i.resize((i.width*s,i.height*s),Image.NEAREST);out.paste(b,(x0,10+(max(j.height for j in imgs)-i.height)*s),b);x0+=i.width*s+10
out.save('ninja_tres_versiones.png')
