# Rampa azul de 7 tonos medida en SoV, rotada de matiz a rojo/verde/morado y pasada a gris.
import colorsys
from PIL import Image,ImageDraw
AZUL=['003250','004471','005591','0067a0','0099d0','5fdcf0','91eef0']
def rgb(h):return tuple(int(h[i:i+2],16)/255 for i in (0,2,4))
def hx(c):return '%02x%02x%02x'%tuple(round(max(0,min(1,v))*255) for v in c)
def rot(h,deg):
    hh,l,s=colorsys.rgb_to_hls(*rgb(h));return hx(colorsys.hls_to_rgb((hh+deg/360)%1,l,s))
def gris(h):
    r,g,b=rgb(h);y=0.299*r+0.587*g+0.114*b;return hx((y,y,y))
base=colorsys.rgb_to_hls(*rgb('0099d0'))[0]*360
R={'Azul':AZUL,
   'Rojo':[rot(h,0-base) for h in AZUL],
   'Verde':[rot(h,120-base) for h in AZUL],
   'Morado':[rot(h,275-base) for h in AZUL],
   'Gris':[gris(h) for h in AZUL]}
if __name__=='__main__':
    s=48;im=Image.new('RGB',(7*s+110,5*(s+8)+8),(0,0x80,0x40));d=ImageDraw.Draw(im)
    for r,(n,c) in enumerate(R.items()):
        print(n.ljust(7),' '.join('#'+h for h in c))
        for i,h in enumerate(c):d.rectangle([8+i*s,8+r*(s+8),6+(i+1)*s,8+r*(s+8)+s-1],fill='#'+h)
        d.text((7*s+18,8+r*(s+8)+18),n,fill='white')
    im.save('rampas_7tonos.png')
