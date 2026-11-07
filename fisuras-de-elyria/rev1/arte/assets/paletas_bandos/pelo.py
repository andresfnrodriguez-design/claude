import numpy as np
from PIL import Image, ImageDraw, ImageFont
exec(open('bandos.py').read().split("spr=Image.open")[0])  # reutiliza B, gba, rgb
PELO={'11':'f080b8','12':'60d0a0'}   # rosa y menta
k=np.array(Image.open('/home/claude/azul/kairon_quieto_suroeste_azul_32x32.png'))
def con_pelo(slot):
    a=k.copy()
    for r in range(8,13):
        for c in range(1,31):
            if a[r,c]==15 and all(a[r+dr,c+dc]>0 for dr,dc in ((1,0),(-1,0),(0,1),(0,-1))): a[r,c]=slot
    return a
vars_=[k,con_pelo(11),con_pelo(12)]
S=6; fondo=Image.open('/home/claude/paleta/mapa_bs_x2.png').convert('RGBA')
cw=26; W=3*cw
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',13)
out=Image.new('RGB',(4*W*S+3*12,30*S+40),(24,24,30)); d=ImageDraw.Draw(out)
for i,(n,p) in enumerate(B.items()):
    p=list(p); p[11]=gba(PELO['11']); p[12]=gba(PELO['12'])
    strip=fondo.crop((40,300,40+W,300+30)).copy()
    for j,a in enumerate(vars_):
        im=Image.fromarray(a,'P'); im.putpalette([v for c in p for v in rgb(c)]+[0]*720); im.info['transparency']=0
        ys,xs=np.where(a>0); strip.alpha_composite(im.convert('RGBA'),(j*cw+cw//2-(xs.min()+xs.max()+1)//2,28-ys.max()))
    x=i*(W*S+12); out.paste(strip.resize((W*S,30*S),Image.NEAREST),(x,0))
    d.text((x+4,30*S+12),n.split(' (')[0],fill=(230,230,230),font=f)
out.save('pelo_x6.png'); print(gba(PELO['11']),gba(PELO['12']))
