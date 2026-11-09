from PIL import Image, ImageDraw, ImageFont
W,H=1344,768
# cajas (x,y,w,h) en el molde de 1344x768; el script de recorte usa las mismas
BOX={'A':(12,40,300,336),'B':(12,392,300,336),'C':(324,40,440,688),'Z':(776,40,504,336),'H':(776,392,504,336)}
if __name__=='__main__':
    im=Image.new('RGB',(W,H),(169,203,166)); d=ImageDraw.Draw(im)
    f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',15)
    L=(70,100,70); M=(120,150,118)
    lab={'A':'A dialogue portrait, facing right','B':'B dialogue portrait, facing left','C':'C full body, front','Z':'Z status close-up, personality','H':'H same close-up, hurt expression'}
    for k,(x,y,w,h) in BOX.items():
        d.rectangle([x,y,x+w,y+h],outline=L,width=2); d.text((x+4,y+4),lab[k],fill=L,font=f)
        if k in 'AB': d.line([x+8,y+int(h*3/112)+22,x+w-8,y+int(h*3/112)+22],fill=M)
        if k=='C': d.line([x+8,y+28,x+w-8,y+28],fill=M); d.line([x+8,y+h-14,x+w-8,y+h-14],fill=M)
    d.text((12,10),'ONE CHARACTER',fill=L,font=f)
    im.save('molde_1pj_1344x768.png')
