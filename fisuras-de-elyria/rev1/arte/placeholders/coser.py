import sys,numpy as np
from PIL import Image
# uso: coser.py salida.png x0 y0 x1 y1 tile1..tile9  (región total en coords de pantalla, grilla 3x3)
out,x0,y0,x1,y1=sys.argv[1],*map(int,sys.argv[2:6]); T=sys.argv[6:]
d='/tmp/claude-tool-results/0ea6749f-feec-5616-8202-b2758e4b37c2/'
xs=[x0+round(i*(x1-x0)/3) for i in range(4)]; ys=[y0+round(i*(y1-y0)/3) for i in range(4)]
s=Image.open(d+T[0]).width/((x1-x0)/3)
can=Image.new('RGB',(round((x1-x0)*s),round((y1-y0)*s)))
for i,f in enumerate(T):
    r,c=divmod(i,3); im=Image.open(d+f).convert('RGB')
    w=round((xs[c+1]-xs[c])*s); h=round((ys[r+1]-ys[r])*s)
    can.paste(im.resize((w,h),Image.LANCZOS),(round((xs[c]-x0)*s),round((ys[r]-y0)*s)))
a=np.asarray(can).astype(int)
# zona de la imagen = filas/columnas donde predomina el verde claro del fondo o la figura (brillo > viewer oscuro)
br=a.mean(2); rows=np.where((br>90).mean(1)>0.5)[0]; cols=np.where((br>90).mean(0)>0.5)[0]
can=can.crop((cols.min(),rows.min(),cols.max()+1,rows.max()+1))
print('recorte',can.size)
(can if "concepto" in out else can.resize((1344,768),Image.LANCZOS)).save(out)
