import numpy as np
from PIL import Image, ImageDraw, ImageFont
gba=lambda h:'%02x%02x%02x'%tuple(int(round(int(h[i:i+2],16)/255*31))*255//31 for i in (0,2,4))
rgb=lambda h:tuple(int(h[i:i+2],16) for i in (0,2,4))
ALI='839c83 101831 eecd4a deacb4 6a4a4a bd8b6a f6d5b4 31206a 315ac5 29a4b4 a4eede 399c5a d53131 e68339 eeeee6 292929'.split()
OPC=[('actual','e68339'),('cobre','c0602c'),('naranja quemado','a84818'),('mandarina','f07020'),('ámbar','e8a030'),('durazno','f0a070')]
k=np.array(Image.open('/home/claude/azul/kairon_quieto_suroeste_azul_32x32.png')); k[k==3]=10
for r in range(8,13):
    for c in range(1,31):
        if k[r,c]==15 and all(k[r+dr,c+dc]>0 for dr,dc in ((1,0),(-1,0),(0,1),(0,-1))): k[r,c]=13
S=6; cw=22; fondo=Image.open('/home/claude/paleta/mapa_bs_x2.png').convert('RGBA')
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',12)
out=Image.new('RGB',(len(OPC)*cw*S,30*S+40),(24,24,30)); d=ImageDraw.Draw(out)
for c,(n,h) in enumerate(OPC):
    p=list(ALI); p[13]=gba(h)
    cell=fondo.crop((40+c*cw,300,40+c*cw+cw,330)).copy()
    im=Image.fromarray(k,'P'); im.putpalette([v for x in p for v in rgb(x)]+[0]*720); im.info['transparency']=0
    ys,xs=np.where(k>0); cell.alpha_composite(im.convert('RGBA'),(cw//2-(xs.min()+xs.max()+1)//2,28-ys.max()))
    out.paste(cell.resize((cw*S,30*S),Image.NEAREST),(c*cw*S,0))
    d.rectangle([c*cw*S+4,30*S+6,c*cw*S+20,30*S+22],fill=rgb(p[13])); d.text((c*cw*S+26,30*S+4),n,fill=(230,230,230),font=f); d.text((c*cw*S+26,30*S+19),'#'+p[13],fill=(160,160,160),font=f)
out.save('naranjas_x6.png')
