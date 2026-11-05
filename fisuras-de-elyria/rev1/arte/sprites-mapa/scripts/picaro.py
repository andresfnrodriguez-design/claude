# Pícaro encapuchado original, 16x16, dibujado con índices de paleta y renderizado en 5 bandos.
from PIL import Image,ImageDraw
from rampas_corregidas import R,slots
G=[
"................",
".....ffff.......",
"....f8998f......",
"...f89aa98f.....",
"...f8566658f....",
"...f86f6f68f....",
"...ff8bbb8ff....",
"..f7bb8988f.ef..",
".f6f7899987fef..",
"..ff7ccc7f5f....",
"...f72227f......",
"...f71117f......",
"...f7f.f7f......",
"..ff7f.f7ff.....",
"..fff...fff.....",
"..dddddddd......"]
base='80a080 3c2c58 8a78c0 d0c8f0 6a4a48 c08a68 f4d8b8 1e2c6c 2f5cc8 3ea0e8 9ce4f8 c02838 c8a048 7a8878 f0f0e8 241c2c'.split()
s=8;W=16*s+20;out=Image.new('RGB',(W*5,16*s+60),(0x80,0xa0,0x80));d=ImageDraw.Draw(out)
for i,(n,r) in enumerate(R.items()):
    p=base[:];sl=slots(r);p[1:4]=sl['secundaria_1_3'];p[7:11]=sl['principal_7_10']
    pal=[tuple(int(c[j:j+2],16) for j in (0,2,4)) for c in p]
    im=Image.new('RGBA',(16,16),(0,0,0,0))
    for y,row in enumerate(G):
        for x,c in enumerate(row):
            if c!='.':im.putpixel((x,y),pal[int(c,16)]+(255,))
    im.save(f'picaro_{n.lower()}_16x16.png')
    big=im.resize((16*s,16*s),Image.NEAREST);out.paste(big,(i*W+10,8),big)
    out.paste(im,(i*W+10,16*s+16),im);d.text((i*W+40,16*s+20),n,fill='black')
out.save('picaro_bandos.png')
