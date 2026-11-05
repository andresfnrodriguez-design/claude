# Sprite original 16x16 dibujado con índices de paleta (0-f) y renderizado con dos paletas.
from PIL import Image
G=[
"............fef.",
"....fffff...fef.",
"...f33322f..fef.",
"..f3322221f.fef.",
"..f326f6f61ffdf.",
"..f256665f..fdf.",
"...ffbbbf...fcf.",
"..fa998b888ff5f.",
".f99877778f.ff..",
".f98cccc8f......",
"..f877778f......",
"..fdf..fdf......",
"..fdf..fdf......",
".ff7f..f7ff.....",
".fff....fff.....",
"................"]
P={'gba':'80a080 584878 90b8e8 d8e8f0 706060 b09058 f8f8d0 383890 3850e0 28a0f8 18f0f8 e81018 f8f840 808870 f8f8f8 403838',
   'nueva':'80a080 3c2c58 8a78c0 d0c8f0 6a4a48 c08a68 f4d8b8 1e2c6c 2f5cc8 3ea0e8 9ce4f8 c02838 c8a048 8890a0 f0f0e8 241c2c'}
s=10;out=Image.new('RGB',(16*s*2+30,16*s+20+40),(0x80,0xa0,0x80))
for i,(n,p) in enumerate(P.items()):
    pal=[tuple(int(h[j:j+2],16) for j in (0,2,4)) for h in p.split()]
    im=Image.new('RGBA',(16,16),(0,0,0,0))
    for y,r in enumerate(G):
        for x,c in enumerate(r):
            if c!='.': im.putpixel((x,y),pal[int(c,16)]+(255,))
    im.save(f'demo_{n}_16x16.png')
    big=im.resize((16*s,16*s),Image.NEAREST);out.paste(big,(10+i*(16*s+10),10),big)
    out.paste(im,(10+i*(16*s+10),16*s+25),im)
out.save('demo_comparacion.png')
