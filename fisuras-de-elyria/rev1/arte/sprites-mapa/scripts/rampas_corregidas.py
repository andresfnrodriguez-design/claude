# Corrige las rampas: junta tonos 3+4, baja saturación de rojo/verde e iguala la luminancia al azul.
import colorsys
from PIL import Image,ImageDraw
from rampas import AZUL,rgb,hx
LUM=lambda c:0.299*c[0]+0.587*c[1]+0.114*c[2]
def mezcla(a,b):return hx(tuple((x+y)/2 for x,y in zip(rgb(a),rgb(b))))
AZ6=[AZUL[0],AZUL[1],mezcla(AZUL[2],AZUL[3]),AZUL[4],AZUL[5],AZUL[6]]
base=colorsys.rgb_to_hls(*rgb('0099d0'))[0]
def ajusta(h,hue,sat):
    hh,l,s=colorsys.rgb_to_hls(*rgb(h));obj=LUM(rgb(h));s*=sat
    lo,hi=0,1
    for _ in range(30):
        m=(lo+hi)/2;c=colorsys.hls_to_rgb(hue%1,m,s)
        lo,hi=(m,hi) if LUM(c)<obj else (lo,m)
    return hx(colorsys.hls_to_rgb(hue%1,m,s))
def gris(h):y=LUM(rgb(h));return hx((y,y,y))
def pastel(h,f):  # rampa secundaria: mismo matiz, desaturada
    hh,l,s=colorsys.rgb_to_hls(*rgb(h));return hx(colorsys.hls_to_rgb(hh,l,s*f))
SAT={'Azul':(None,1),'Rojo':(0/360,0.78),'Verde':(125/360,0.72),'Morado':(275/360,0.9)}
R={}
for n,(hue,sat) in SAT.items():
    R[n]=AZ6 if hue is None else [ajusta(h,hue,sat) for h in AZ6]
R['Gris']=[gris(h) for h in AZ6]
def slots(r):
    return {'principal_7_10':[r[1],r[2],r[3],r[4]],
            'secundaria_1_3':[pastel(r[1],0.45),pastel(r[4],0.55),pastel(r[5],0.5)]}
if __name__=='__main__':
    s=40;W=6*s+30+4*s+3*s+90;im=Image.new('RGB',(W,5*(s+10)+40),(0,0x80,0x40));d=ImageDraw.Draw(im)
    d.text((8,8),'Rampa 6 tonos',fill='white');d.text((6*s+30,8),'7-10 principal',fill='white');d.text((10*s+40,8),'1-3 secundaria',fill='white')
    for r,(n,c) in enumerate(R.items()):
        y=26+r*(s+10);sl=slots(c)
        print(n.ljust(7),'rampa:',' '.join('#'+h for h in c),'| 7-10:',' '.join('#'+h for h in sl['principal_7_10']),'| 1-3:',' '.join('#'+h for h in sl['secundaria_1_3']))
        for i,h in enumerate(c):d.rectangle([8+i*s,y,6+(i+1)*s,y+s-1],fill='#'+h)
        for i,h in enumerate(sl['principal_7_10']):d.rectangle([6*s+30+i*s,y,6*s+28+(i+1)*s,y+s-1],fill='#'+h)
        for i,h in enumerate(sl['secundaria_1_3']):d.rectangle([10*s+40+i*s,y,10*s+38+(i+1)*s,y+s-1],fill='#'+h)
        d.text((13*s+50,y+14),n,fill='white')
    im.save('rampas_corregidas.png')
