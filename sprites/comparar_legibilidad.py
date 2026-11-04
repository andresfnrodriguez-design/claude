# Compara en el mapa: ninja actual, ninja con contorno exterior + interior aclarado, y el pícaro original estilo GBA.
from PIL import Image
OUT=(0x24,0x1c,0x2c,255)
def contorno(im):
    im=im.copy();W,H=im.size;g=Image.new('RGBA',(W+2,H+2),(0,0,0,0));g.paste(im,(1,1));src=g.copy()
    for y in range(H+2):
        for x in range(W+2):
            if src.getpixel((x,y))[3]==0 and any(0<=x+dx<W+2 and 0<=y+dy<H+2 and src.getpixel((x+dx,y+dy))[3] and src.getpixel((x+dx,y+dy))[:3]!=(0x7a,0x88,0x78) for dx,dy in((1,0),(-1,0),(0,1),(0,-1))):
                g.putpixel((x,y),OUT)
    return g
def aclarar(im,de=(0x3c,0x2c,0x58),a=(0x2f,0x5c,0xc8)):
    im=im.copy()
    for y in range(im.height):
        for x in range(im.width):
            if im.getpixel((x,y))[:3]==de and (x+y)%2==0:im.putpixel((x,y),a+(255,))
    return im
ninja=Image.open('ninja_propuesta_aliado.png').convert('RGBA');ninja=ninja.crop(ninja.getbbox())
fijo=contorno(aclarar(ninja));fijo=fijo.crop(fijo.getbbox())
pic=Image.open('picaro_azul_16x16.png').convert('RGBA');pic=pic.crop(pic.getbbox())
fijo.save('ninja_corregido.png')
m=Image.open('mapa_prueba.png').convert('RGBA')
tx,ty=2,4;fr=m.crop((tx*16,ty*16,tx*16+240,ty*16+160))
for sp,(cx,cy) in ((ninja,(1,7)),(fijo,(3,7)),(pic,(5,7)),(ninja,(9,4)),(fijo,(11,4)),(pic,(13,4))):
    fr.alpha_composite(sp,(cx*16+(16-sp.width)//2,(cy+1)*16-sp.height))
fr.save('comparar_legibilidad.png');fr.resize((720,480),Image.NEAREST).save('comparar_legibilidad_x3.png')
