"""Pantalla de estado estilo GBA: 240x160, color RGB555 (15 bits).
El semicirculo usa mezcla alfa 50% (equivalente a BLDALPHA de la GBA)."""
from PIL import Image, ImageDraw, ImageFont

W, H = 240, 160
def c(r, g, b):
    q = lambda v: (v >> 3) << 3 | (v >> 5)
    return (q(r), q(g), q(b))

BG, BG2 = c(72, 16, 32), c(96, 24, 40)
BAR, FR = c(136, 32, 56), c(216, 112, 136)
TXT, LBL, HL = c(248, 248, 248), c(240, 184, 196), c(248, 216, 96)
DARK = c(40, 8, 16)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img); d.fontmode = "1"
f = ImageFont.load_default()
def t(x, y, s, col=TXT, dd=None): (dd or d).text((x, y), s, font=f, fill=col)
def big(x, y, s, col=TXT):  # texto 2x estilo pixel
    tmp = Image.new("L", (60, 14)); td = ImageDraw.Draw(tmp); td.fontmode = "1"
    td.text((0, 0), s, font=f, fill=255)
    tmp = tmp.resize((120, 28), Image.NEAREST)
    img.paste(Image.new("RGB", tmp.size, col), (x, y), tmp)

# fondo con viñeta diagonal sutil
for y in range(H):
    for x in range(0, W, 2):
        if (x + y) % 8 == 0: img.putpixel((x, y), BG2)

# retrato grande detrás (arte del usuario)
art = Image.open("retrato.png").convert("RGB")
bgc = art.getpixel((0, 0))
mask = Image.new("L", art.size, 0)
for y in range(art.height):
    for x in range(art.width):
        p = art.getpixel((x, y))
        if sum(abs(p[i] - bgc[i]) for i in range(3)) >= 40: mask.putpixel((x, y), 255)
        art.putpixel((x, y), c(*p))
img.paste(art, (66, 16), mask)

# semicirculo negro translucido a la derecha (alpha 50%)
cx, cy, r = 250, 80, 82
ov = Image.new("RGB", (W, H), (0, 0, 0)); m = Image.new("L", (W, H), 0)
ImageDraw.Draw(m).ellipse([cx - r, cy - r, cx + r, cy + r], fill=150)
img = Image.composite(ov, img, m)
img = img.point(lambda v: (v >> 3) << 3 | (v >> 5))  # re-cuantizar a RGB555
d = ImageDraw.Draw(img); d.fontmode = "1"
d.arc([cx - r, cy - r, cx + r, cy + r], 90, 270, fill=c(200, 200, 200))
d.arc([cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3], 100, 260, fill=FR)

# barra superior
d.rectangle([0, 0, 239, 11], fill=BAR)
t(3, 0, "Genny")
for x, lab, val in [(90, "LV", "8"), (132, "EXP", "99"), (180, "Rating", "71")]:
    d.rectangle([x, 1, x + len(lab) * 6 + 3, 10], fill=DARK); t(x + 2, 0, lab, LBL)
    t(x + len(lab) * 6 + 8, 0, val)

# HP grande + barra
t(3, 14, "HP", LBL); big(16, 12, "19"); t(42, 20, "/19")
d.rectangle([62, 22, 88, 27], fill=DARK); d.rectangle([63, 23, 87, 26], fill=TXT)

# clase con iconos de libro
t(192, 15, "Cleric")
for x in (226, 233):
    d.rectangle([x, 17, x + 5, 24], fill=c(232, 224, 176), outline=c(96, 80, 48))

# banner de objeto
d.rectangle([62, 32, 170, 43], fill=c(88, 16, 32), outline=c(200, 48, 72))
d.ellipse([66, 34, 73, 41], fill=c(176, 112, 64)); t(78, 32, "Leather Shield")

# stats (sin cajas, etiqueta en columna oscura)
stats = [("ATK", "11"), ("SKILL", "6"), ("SPD", "7"), ("LCK", "10"),
         ("DEF", "2"), ("RES", "13"), ("MOV", "4")]
d.rectangle([0, 50, 33, 50 + 7 * 13], fill=DARK)
for i, (k, v) in enumerate(stats):
    y = 51 + i * 13
    t(33 - len(k) * 6, y, k, LBL); t(48 - len(v) * 6 + 6, y, v)
d.polygon([(52, 108), (56, 105), (68, 105), (68, 112), (56, 112)], fill=TXT)
t(56, 103, "+3", DARK)

# libro de comandos sobre el semicirculo
skills = [("Nosferatu", c(232, 200, 80)), ("Recover", c(200, 232, 160)),
          ("Physic", c(200, 232, 160)), ("Invoke", c(200, 232, 160)), ("????", c(200, 160, 120))]
for i, (s, col) in enumerate(skills):
    y = 46 + i * 14; x = 176 - (8 if i in (0, 4) else 4 if i == 1 else 0) + (i == 4) * 0
    x = [174, 170, 168, 168, 170][i]
    d.rectangle([x, y + 2, x + 6, y + 9], fill=col, outline=c(96, 80, 48))
    t(x + 10, y, s)

# barra inferior
d.rectangle([0, 146, 239, 159], fill=DARK)
for i in range(4):
    x = 2 + i * 18
    d.rectangle([x, 147, x + 15, 158], fill=BAR if i != 2 else c(176, 48, 72), outline=FR)
t(6, 147, "+"); t(24, 147, "o"); t(41, 147, "#"); t(60, 147, "=")
d.rectangle([194, 147, 237, 158], fill=BAR, outline=FR)
d.ellipse([199, 149, 207, 157], outline=TXT); t(222, 147, "3")

img.save("estado_gba.png")
img.resize((W * 4, H * 4), Image.NEAREST).save("estado_gba_x4.png")
print(len(img.getcolors(4096)), "colores")
