#!/usr/bin/env python3
"""Recorta una hoja generada con molde_1pj y saca las piezas del juego como placeholders.
Uso: python3 recortar.py hoja.png id_personaje carpeta_salida
Saca escena_100x112 (A), espejo_100x112 (B), cuerpo (C), estado_80x144 y mini_32x32 calculados por regla,
zoom_240x160 (Z) y herido_240x160 (H). Fondo #A9CBA6."""
import sys,os,numpy as np
from PIL import Image
from molde import BOX
BG=np.array([169,203,166])
def figura(im):
    a=np.asarray(im.convert('RGB')).astype(int); m=np.abs(a-BG).sum(2)>60
    ys,xs=np.where(m)
    return (xs.min(),ys.min(),xs.max()+1,ys.max()+1) if len(xs) else (0,0,im.width,im.height)
def encajar(im,w,h,top_margin=0):
    """escala para llenar el ancho w x alto h, sobre fondo verde"""
    out=Image.new('RGB',(w,h),tuple(BG)); r=min(w/im.width,(h-top_margin)/im.height)
    t=im.resize((max(1,round(im.width*r)),max(1,round(im.height*r))),Image.LANCZOS)
    out.paste(t,((w-t.width)//2,top_margin)); return out
src,pid,dst=sys.argv[1],sys.argv[2],sys.argv[3]; os.makedirs(dst,exist_ok=True)
im=Image.open(src).convert('RGB'); sx,sy=im.width/1344,im.height/768
P={k:im.crop((round(x*sx)+3,round(y*sy)+3,round((x+w)*sx)-3,round((y+h)*sy)-3)) for k,(x,y,w,h) in BOX.items()}
for k,nom in (('A','escena'),('B','espejo')):
    p=P[k]; x0,y0,x1,y1=figura(p)
    # 3 px de margen arriba a escala 100x112, cabeza entera, corte abajo
    ww=x1-x0; hh=round(ww*112/100); c=p.crop((max(0,(x0+x1)//2-ww//2), max(0,y0-round(hh*3/112)), min(p.width,(x0+x1)//2+ww//2), max(0,y0-round(hh*3/112))+hh))
    c.resize((100,112),Image.LANCZOS).save(f'{dst}/{pid}_{nom}_100x112.png')
c=P['C']; x0,y0,x1,y1=figura(c); fh=y1-y0
c.crop((x0,y0,x1,y1)).save(f'{dst}/{pid}_cuerpo.png')
# estado. Cabeza de unos 28 px en 144 y corte a media pierna, o sea el 2/3 superior de la figura
alto=round(fh*0.68); ancho=round(alto*80/140); cx=(x0+x1)//2
e=c.crop((cx-ancho//2,y0,cx+ancho//2,y0+alto))
encajar(e,80,144,top_margin=4).save(f'{dst}/{pid}_estado_80x144.png')
# mini. Cara lo más grande posible, corte en los hombros: cuadrado sobre la cabeza del busto A
a=P['A']; x0,y0,x1,y1=figura(a); lado=round((x1-x0)*0.55); cx=(x0+x1)//2
a.crop((cx-lado//2,y0,cx+lado//2,y0+lado)).resize((32,32),Image.LANCZOS).save(f'{dst}/{pid}_mini_32x32.png')
for k,nom in (('Z','zoom'),('H','herido')): P[k].resize((240,160),Image.LANCZOS).save(f'{dst}/{pid}_{nom}_240x160.png')
print('listo',pid)
