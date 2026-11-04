# Coloca las 5 unidades propuestas sobre el mapa, alineadas a la cuadrícula de 16 px (pies en la base de la casilla).
from PIL import Image
m=Image.open('mapa_prueba.png').convert('RGBA')
U=[('aliado',(3,11)),('enemigo',(13,6)),('neutral',(19,14)),('arena',(6,21)),('usado',(16,23))]
for n,(tx,ty) in U:
    sp=Image.open(f'ninja_propuesta_{n}.png').convert('RGBA')
    b=sp.getbbox();sp=sp.crop(b)
    x=tx*16+(16-sp.width)//2;y=(ty+1)*16-sp.height
    m.alpha_composite(sp,(x,y))
m.save('mapa_unidades.png');m.resize((m.width*2,m.height*2),Image.NEAREST).save('mapa_unidades_x2.png')
