"""Pantalla de estado estilo GBA: 240x160, color RGB555.
Posiciones escaladas del original (563x424 -> x*0.426, y*0.377).
Degradados en bandas de 15 bits; semicirculo con mezcla alfa (BLDALPHA)."""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 240, 160
q5 = lambda v: (max(0, min(255, int(v))) >> 3) << 3 | (max(0, min(255, int(v))) >> 5)
def c(r, g, b): return (q5(r), q5(g), q5(b))
def lerp(a, b, k): return c(*(a[i] + (b[i] - a[i]) * k for i in range(3)))

TXT, LBL = c(248, 248, 248), c(240, 200, 208)
DARK, FR = c(48, 8, 20), c(200, 64, 88)

img = Image.new("RGB", (W, H))
f = ImageFont.load_default()

# fondo: degradado radial rojo oscuro (centro claro arriba-izq del retrato)
for y in range(H):
    for x in range(W):
        k = min(1, math.hypot(x - 100, (y - 40) * 1.3) / 170)
        img.putpixel((x, y), lerp((128, 32, 48), (40, 6, 14), k))

# retrato (arte del usuario, fondo morado transparente)
art = Image.open("retrato_busto.png").convert("RGB")
bgc = (77, 26, 77)
# quitar fondo morado y marco gris conectado al borde (flood fill)
fondo = {bgc, (34, 34, 34)}
mask = Image.new("L", art.size, 255)
pila = [(x, y) for x in range(art.width) for y in (0, art.height - 1)] + \
       [(x, y) for y in range(art.height) for x in (0, art.width - 1)]
while pila:
    x, y = pila.pop()
    if 0 <= x < art.width and 0 <= y < art.height and mask.getpixel((x, y)) and art.getpixel((x, y)) in fondo:
        mask.putpixel((x, y), 0); pila += [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
for y in range(art.height):
    for x in range(art.width):
        if art.getpixel((x, y)) == bgc: mask.putpixel((x, y), 0)
        art.putpixel((x, y), c(*art.getpixel((x, y))))
img.paste(art, (44, 26), mask)

# semicirculo negro translucido (centro fuera de pantalla a la derecha)
cx, cy, r = 343, 85, 200
m = Image.new("L", (W, H), 0)
ImageDraw.Draw(m).ellipse([cx - r, cy - r, cx + r, cy + r], fill=150)
img = Image.composite(Image.new("RGB", (W, H)), img, m)
d = ImageDraw.Draw(img); d.fontmode = "1"
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c(232, 216, 216))
d.ellipse([cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3], outline=c(120, 32, 48))

def t(x, y, s, col=TXT): d.text((x, y), s, font=f, fill=col)
def tr(x, y, s, col=TXT): t(x - int(d.textlength(s, font=f)), y, s, col)  # alineado a la derecha
def grad_rect(x0, y0, x1, y1, a, b, vertical=True):
    n = (y1 - y0) if vertical else (x1 - x0)
    for i in range(n + 1):
        col = lerp(a, b, i / max(1, n))
        if vertical: d.line([(x0, y0 + i), (x1, y0 + i)], fill=col)
        else: d.line([(x0 + i, y0), (x0 + i, y1)], fill=col)
def big(x, y, s, col=TXT):
    tmp = Image.new("L", (40, 12)); td = ImageDraw.Draw(tmp); td.fontmode = "1"
    td.text((0, -1), s, font=f, fill=255)
    tmp = tmp.resize((80, 24), Image.NEAREST)
    img.paste(Image.new("RGB", tmp.size, col), (x, y), tmp)

# barra superior con degradado horizontal
grad_rect(0, 0, 239, 11, (176, 56, 80), (96, 16, 32), vertical=False)
d.line([(0, 12), (239, 12)], fill=c(32, 4, 10))
t(3, 0, "Genny")
for x0, x1, lab in [(86, 100, "LV"), (122, 141, "EXP"), (166, 203, "Rating")]:
    d.rectangle([x0, 1, x1, 10], fill=DARK); t(x0 + 2, 0, lab, LBL)
tr(116, 0, "8"); tr(160, 0, "99"); tr(237, 0, "71")

# HP
t(3, 14, "HP", LBL); big(14, 12, "19"); t(40, 17, "/19")
d.rectangle([62, 20, 80, 24], fill=TXT)
d.ellipse([82, 18, 89, 25], outline=TXT); d.point([(84, 21), (87, 21)], fill=TXT)
t(178, 14, "Cleric")
for x in (217, 226):
    d.rectangle([x, 16, x + 6, 23], fill=c(232, 224, 184), outline=c(88, 72, 40))
    d.line([(x + 2, 18), (x + 4, 18)], fill=c(88, 72, 40))

# banner del objeto
d.rounded_rectangle([65, 31, 175, 42], 3, fill=c(96, 16, 32), outline=FR)
d.ellipse([70, 33, 77, 40], fill=c(168, 112, 72), outline=c(88, 56, 32))
t(82, 31, "Leather Shield")

# columna de stats con degradado horizontal oscuro
grad_rect(0, 62, 27, 134, (40, 6, 14), (96, 20, 36), vertical=False)
stats = [("ATK", "11"), ("SKILL", "6"), ("SPD", "7"), ("LCK", "10"),
         ("DEF", "2"), ("RES", "13"), ("MOV", "4")]
for i, (k, v) in enumerate(stats):
    y = 62 + i * 10
    tr(28, y, k, LBL); tr(42, y, v)
y0 = 62 + 40
d.polygon([(45, y0 + 5), (48, y0 + 2), (62, y0 + 2), (62, y0 + 9), (48, y0 + 9)], fill=TXT)
t(49, y0, "+3", DARK)

# libro de comandos
skills = [("Nosferatu", 170, 50, (216, 200, 72)), ("Recover", 166, 62, (176, 224, 176)),
          ("Physic", 162, 73, (176, 224, 176)), ("Invoke", 162, 84, (176, 224, 176)),
          ("????", 160, 95, (216, 176, 96))]
for s, x, y, col in skills:
    d.rectangle([x - 9, y + 3, x - 3, y + 9], fill=c(*col), outline=c(88, 72, 40))
    t(x, y, s)

# barra inferior con degradado vertical
grad_rect(0, 138, 239, 159, (64, 10, 22), (24, 4, 8))
icons = ["+", "o", "#", "="]
for i, ic in enumerate(icons):
    x = 3 + i * 23
    grad_rect(x, 140, x + 18, 157, (200, 64, 88) if i == 2 else (176, 40, 64), (96, 16, 32))
    d.rectangle([x, 140, x + 18, 157], outline=FR)
    t(x + 7, 143, ic)
grad_rect(192, 140, 236, 157, (176, 40, 64), (96, 16, 32))
d.rectangle([192, 140, 236, 157], outline=FR)
d.ellipse([197, 143, 208, 154], outline=TXT); d.ellipse([200, 146, 205, 151], fill=TXT)
big(219, 137, "3")

img = img.point(q5)
img.save("estado_gba.png")
img.resize((W * 4, H * 4), Image.NEAREST).save("estado_gba_x4.png")
print(len(img.getcolors(4096)), "colores")
