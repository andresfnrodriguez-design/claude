# "Sel-out": suaviza el contorno exterior usando el tono oscuro del material vecino, sin colores nuevos.
from PIL import Image
OUT=(0x24,0x1c,0x2c)
# material claro -> tono oscuro de su propia rampa (todos ya están en la paleta)
OSCURO={(0x9c,0xe4,0xf8):(0x1e,0x2c,0x6c),(0x3e,0xa0,0xe8):(0x1e,0x2c,0x6c),(0x2f,0x5c,0xc8):(0x1e,0x2c,0x6c),
        (0xd0,0xc8,0xf0):(0x3c,0x2c,0x58),(0x8a,0x78,0xc0):(0x3c,0x2c,0x58),
        (0xf4,0xd8,0xb8):(0x6a,0x4a,0x48),(0xc0,0x8a,0x68):(0x6a,0x4a,0x48),
        (0xf0,0xf0,0xe8):(0x7a,0x88,0x78),(0xf0,0xdd,0x60):(0x6a,0x4a,0x48)}
im=Image.open('ninja_corregido.png').convert('RGBA');W,H=im.size;src=im.copy()
def px(x,y):return src.getpixel((x,y)) if 0<=x<W and 0<=y<H else (0,0,0,0)
for y in range(H):
    for x in range(W):
        if px(x,y)[:3]!=OUT or not px(x,y)[3]:continue
        # solo en el lado iluminado (arriba/izquierda) y si toca un material claro por dentro
        lado_luz=px(x-1,y)[3]==0 or px(x,y-1)[3]==0
        vec=[px(x+dx,y+dy)[:3] for dx,dy in((1,0),(0,1),(-1,0),(0,-1)) if px(x+dx,y+dy)[3]]
        claros=[v for v in vec if v in OSCURO]
        if lado_luz and claros:im.putpixel((x,y),OSCURO[claros[0]]+(255,))
im.save('ninja_selout.png')
s=10;out=Image.new('RGB',(W*s*2+30,H*s+20),(0x80,0xa0,0x80))
for i,img in enumerate((src,im)):
    b=img.resize((W*s,H*s),Image.NEAREST);out.paste(b,(10+i*(W*s+10),10),b)
out.save('ninja_selout_comparacion.png')
