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
RX, RY = -12, 22
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
ESC = 2.0  # cabeza grande, cortada bajo los hombros
art = art.resize((int(art.width * ESC), int(art.height * ESC)), Image.NEAREST)
mask = mask.resize(art.size, Image.NEAREST)
img.paste(art, (RX, RY), mask)

# semicirculo negro translucido (centro fuera de pantalla a la derecha)
cx, cy, r = 337, 85, 180
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

# mini fuente 3x5 para la etiqueta +3
MINI = {"+": ["000","010","111","010","000"], "3": ["111","001","011","001","111"]}
def mini(x, y, s, col):
    for ch in s:
        for j, fila in enumerate(MINI[ch]):
            for i, b in enumerate(fila):
                if b == "1": d.point((x + i, y + j), fill=col)
        x += 4

# barra superior
grad_rect(0, 0, 239, 12, (176, 56, 80), (96, 16, 32), vertical=False)
d.line([(0, 13), (239, 13)], fill=c(32, 4, 10))
t(3, 1, "Genny")
for x0, x1, lab in [(93, 113, "LV"), (143, 164, "EXP"), (183, 218, "Rating")]:
    d.rectangle([x0, 2, x1, 11], fill=DARK); t(x0 + (x1 - x0 - d.textlength(lab, font=f)) // 2, 1, lab, LBL)
tr(138, 1, "8"); tr(182, 1, "99"); tr(236, 1, "71")

# HP
t(3, 15, "HP", LBL); fb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
d.text((18, 12), "19", font=fb, fill=TXT); t(42, 16, "/19")
d.rectangle([65, 19, 87, 24], fill=c(248, 224, 232))
d.ellipse([89, 17, 97, 25], outline=TXT); d.point([(91, 20), (95, 20)], fill=TXT)
tr(214, 16, "Cleric")
for x in (217, 226):
    d.rectangle([x, 18, x + 6, 25], fill=c(232, 224, 184), outline=c(88, 72, 40))
    d.line([(x + 2, 20), (x + 4, 20)], fill=c(88, 72, 40))

# banner del objeto
d.rounded_rectangle([65, 32, 175, 43], 3, fill=c(96, 16, 32), outline=FR)
d.ellipse([79, 34, 87, 42], fill=c(168, 112, 72), outline=c(88, 56, 32))
t(92, 32, "Leather Shield")

# stats: etiquetas alineadas a la izquierda, valores a la derecha
grad_rect(0, 62, 34, 136, (40, 6, 14), (88, 18, 32), vertical=False)
stats = [("ATK", "11"), ("SKL", "6"), ("SPD", "7"), ("LCK", "10"),
         ("DEF", "2"), ("RES", "13"), ("MOV", "4")]
for i, (k, v) in enumerate(stats):
    y = 62 + round(i * 10.5)
    t(4, y, k, LBL); tr(42, y, v)
d.polygon([(44, 109), (47, 106), (56, 106), (56, 112), (47, 112)], fill=TXT)
mini(48, 107, "+3", DARK)

# libro de comandos
skills = [("Nosferatu", 176, 47, (216, 200, 72)), ("Recover", 171, 59, (176, 224, 176)),
          ("Physic", 168, 71, (176, 224, 176)), ("Invoke", 168, 83, (176, 224, 176)),
          ("????", 169, 94, (216, 176, 96))]
for s_, x, y, col in skills:
    d.rectangle([x - 10, y + 2, x - 3, y + 9], fill=c(*col), outline=c(88, 72, 40))
    t(x, y, s_)

# barra inferior
grad_rect(0, 137, 239, 159, (64, 10, 22), (24, 4, 8))
for i, ic in enumerate(["+", "o", "#", "="]):
    x = 4 + i * 23.5; x = int(x)
    grad_rect(x, 139, x + 21, 158, (200, 64, 88) if i == 0 else (120, 24, 44), (72, 12, 26))
    d.rectangle([x, 139, x + 21, 158], outline=FR)
    t(x + 8, 143, ic)
grad_rect(193, 139, 236, 158, (120, 24, 44), (72, 12, 26))
d.rectangle([193, 139, 236, 158], outline=FR)
d.ellipse([197, 142, 210, 155], outline=TXT); d.ellipse([201, 146, 206, 151], fill=TXT)
d.text((218, 140), "3", font=fb, fill=TXT)

img = img.point(q5)
img.save("estado_gba.png")
img.resize((W * 4, H * 4), Image.NEAREST).save("estado_gba_x4.png")
print(len(img.getcolors(4096)), "colores")

g = Image.open("guia.png").convert("RGB").resize((W, H), Image.LANCZOS)
Image.blend(g, img, 0.5).resize((W * 4, H * 4), Image.NEAREST).save("comparacion_x4.png")
