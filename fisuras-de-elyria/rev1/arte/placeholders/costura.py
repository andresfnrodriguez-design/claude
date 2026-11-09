import sys,numpy as np
from PIL import Image
# uso: costura.py hoja.png  -> interpola sobre bandas horizontales oscuras de la captura
f=sys.argv[1]; a=np.asarray(Image.open(f).convert('RGB')).astype(float)
br=a.mean(2); dark=(br<100).mean(1)
bad=[y for y in range(3,765) if dark[y]-dark[y-3]>0.4]
for y in bad:
    y0,y1=y-4,y+4
    for yy in range(y0+1,y1): t=(yy-y0)/(y1-y0); a[yy]=a[y0]*(1-t)+a[y1]*t
Image.fromarray(a.round().astype(np.uint8)).save(f); print('costuras',bad)
