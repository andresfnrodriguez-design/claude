import struct, numpy as np, glob, os
from PIL import Image, ImageDraw, ImageFont
gba=lambda h:tuple(int(round(int(h[i:i+2],16)/255*31)) for i in (0,2,4))
def leer(f):
    d=open(f,'rb').read(); return [((v&31),(v>>5)&31,(v>>10)&31) for (v,) in struct.iter_unpack('<H',d)]
V='/home/claude/fe8u/graphics/unit_icon/palette/unit_icon_pal_%s.agbpal'
PIEL=['6a4a4a','bd8b6a','f6d5b4']; GRIS='7b8b9c'; BLANCO='f0f0e8'; CONT='292929'
B={'player':(['101831','c5e6ee','eef6f6'],['31206a','3a5ac8','5aacee','a4eede']),
   'enemy': (['291018','deacb4','eee6e6'],['390818','6a1029','9c2939','cd626a']),
   'npc':   (['392910','c8b070','f6eec5'],['4a3110','9c7318','deac31','f6ee9c']),
   'p4':    (['200818','e0a0c0','f6e0ee'],['6a186a','bd318b','de5a94','f6b4cd'])}
P={}
for k,(sec,ramp) in B.items():
    v=leer(V%k)
    p=[v[0]]+[gba(c) for c in sec]+[gba(c) for c in PIEL]+[gba(c) for c in ramp]+[v[11],v[12],gba(GRIS),gba(BLANCO),gba(CONT)]
    P[k]=p
    open(f'unit_icon_pal_{k}.agbpal','wb').write(b''.join(struct.pack('<H',r|(g<<5)|(b<<10)) for r,g,b in p))
# vista previa con sprites vanilla
to8=lambda p:[x*255//31 for c in p for x in c]
sheets=sorted(glob.glob('/home/claude/fe8u/graphics/unit_icon/wait/unit_icon_wait_*_sheet.png'))
pick=[s for s in sheets if any(n in s for n in ['Ephraim_Lord','Eirika_Lord','Paladin','Archer_M','Mage_M','Fighter','Knight','Pegasus_Knight','Brigand','Cleric','Myrmidon_M','General'])][:12]
f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',12)
S=4; out=Image.new('RGB',(130+len(pick)*34*S//2*1,5*(32*S//1)+10),(131,164,131)); 
out=Image.new('RGB',(130+len(pick)*18*S,5*34*S),(40,44,40)); d=ImageDraw.Draw(out)
rows=[('original FE8',None)]+[(n,k) for n,k in [('Protagonistas','player'),('Enemigos','enemy'),('Neutrales','npc'),('Cuarta facción','p4')]]
for r,(n,k) in enumerate(rows):
    d.text((6,r*34*S+60),n,fill=(235,235,235),font=f)
    for c,s in enumerate(pick):
        im=Image.open(s)
        if im.mode!='P': continue
        fr=im.crop((0,0,im.width,min(32,im.height)))
        if k: fr.putpalette(to8(P[k])+[0]*720)
        fr=fr.convert('RGBA'); a=np.array(fr); idx=np.array(im.crop((0,0,im.width,min(32,im.height)))); a[idx==0,3]=0
        fr=Image.fromarray(a).resize((fr.width*S,fr.height*S),Image.NEAREST)
        out.paste(fr,(130+c*18*S,r*34*S),fr)
out.save('compat_x4.png'); print([os.path.basename(p) for p in pick])
