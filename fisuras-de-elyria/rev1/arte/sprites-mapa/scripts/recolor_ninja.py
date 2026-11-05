# Reconstruye el sprite del usuario (captura ampliada) a su resolución real y lo recolorea por bando.
from PIL import Image,ImageDraw
from rampas_corregidas import R,slots
src=Image.open('ninja_original_captura.png').convert('RGB')
px,py,ox,oy=7.1,7.2,6,4
xs,ys=int((src.width-ox)/px),int((src.height-oy)/py)
# color representativo -> posición de paleta
MAP={'6d6f96':0,'474574':13,'140904':15,'000907':15,'472384':1,'536fde':8,'4175dc':9,
     '8298e8':2,'51c0fc':10,'b6c7fe':3,'dc8665':5,'fabf92':6,'fbb53e':12,'fdfef9':14}
reps=[(tuple(int(k[i:i+2],16) for i in (0,2,4)),v) for k,v in MAP.items()]
def slot(c):return min(reps,key=lambda r:sum((a-b)**2 for a,b in zip(c,r[0])))[1]
idx=[[slot(src.getpixel((min(int(ox+i*px+px/2),src.width-1),min(int(oy+j*py+py/2),src.height-1)))) for i in range(xs)] for j in range(ys)]
base='80a080 3c2c58 8a78c0 d0c8f0 6a4a48 c08a68 f4d8b8 1e2c6c 2f5cc8 3ea0e8 9ce4f8 c02838 c8a048 7a8878 f0f0e8 241c2c'.split()
s=8;W=xs*s+20;out=Image.new('RGB',(W*5,ys*s+50),(0x80,0xa0,0x80));d=ImageDraw.Draw(out)
for i,(n,r) in enumerate(R.items()):
    p=base[:];sl=slots(r);p[1:4]=sl['secundaria_1_3'];p[7:11]=sl['principal_7_10']
    pal=[tuple(int(c[j:j+2],16) for j in (0,2,4)) for c in p]
    im=Image.new('RGBA',(xs,ys),(0,0,0,0))
    for y,row in enumerate(idx):
        for x,k in enumerate(row):
            if k:im.putpixel((x,y),pal[k]+(255,))
    im.save(f'ninja_{n.lower()}.png')
    big=im.resize((xs*s,ys*s),Image.NEAREST);out.paste(big,(i*W+10,8),big)
    out.paste(im,(i*W+10,ys*s+16),im);d.text((i*W+40,ys*s+20),n,fill='black')
out.save('ninja_bandos.png');print(xs,ys)
