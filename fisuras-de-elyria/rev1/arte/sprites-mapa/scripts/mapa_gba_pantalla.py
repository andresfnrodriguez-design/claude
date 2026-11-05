# Recorta el mapa con unidades a pantallas de GBA (240x160 = 15x10 casillas de 16 px).
from PIL import Image
m=Image.open('mapa_unidades.png')
for n,(tx,ty) in {'arriba':(2,4),'abajo':(5,14)}.items():
    c=m.crop((tx*16,ty*16,tx*16+240,ty*16+160));c.save(f'gba_pantalla_{n}.png')
    c.resize((720,480),Image.NEAREST).save(f'gba_pantalla_{n}_x3.png')
