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

# fondo: luz tinta que sale de la esquina superior izquierda
for y in range(H):
    for x in range(W):
        dist = math.hypot(x, y * 1.2)
        ang = abs(math.atan2(y, x) - math.radians(35))  # haz hacia abajo-derecha
        k = dist / 260 + ang * 0.35
        img.putpixel((x, y), lerp((150, 40, 60), (36, 5, 12), min(1, k)))

# retrato (arte del usuario, fondo morado transparente)
RX, RY = -26, 17  # ojos alineados con la guia
art = Image.open("retrato_busto.png").convert("RGB")
bgc = (77, 26, 77)
# quitar fondo morado y marco gris conectado al borde (flood fill)
fondo = {bgc}  # solo el morado; el gris oscuro es pelo
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
ESC = 3.2  # cabeza grande, cortada bajo los hombros
art = art.resize((int(art.width * ESC), int(art.height * ESC)), Image.NEAREST)
mask = mask.resize(art.size, Image.NEAREST)
img.paste(art, (RX, RY), mask)

# semicirculo negro translucido (centro fuera de pantalla a la derecha)
cx, cy, r = 337, 85, 180
m = Image.new("L", (W, H), 0)
ImageDraw.Draw(m).ellipse([cx - r, cy - r, cx + r, cy + r], fill=115)
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
MINI = {"+": ["000","010","111","010","000"], "3": ["111","001","011","001","111"],
        "H": ["101","101","111","101","101"], "P": ["110","101","110","100","100"]}
def mini(x, y, s, col):
    for ch in s:
        for j, fila in enumerate(MINI[ch]):
            for i, b in enumerate(fila):
                if b == "1": d.point((x + i, y + j), fill=col)
        x += 4

# barra superior
for x in range(W):
    for y in range(13):
        k = min(1, x / 140) * 0.7 + y / 13 * 0.3
        d.point((x, y), fill=lerp((214, 96, 128), (110, 18, 40), k))
d.line([(0, 13), (239, 13)], fill=c(32, 4, 10))
t(3, 1, "Kairos")
for x0, x1, lab in [(150, 166, "LV"), (190, 210, "EXP")]:
    d.rectangle([x0, 2, x1, 11], fill=DARK); t(x0 + (x1 - x0 - d.textlength(lab, font=f)) // 2, 1, lab, LBL)
tr(182, 1, "8"); tr(236, 1, "99")

# HP: franja vinotinto translucida bajo el HP, con extremo derecho curvo
fr = Image.new("L", (W, H), 0); fd = ImageDraw.Draw(fr)
fd.rectangle([0, 14, 150, 30], fill=220); fd.ellipse([130, -10, 170, 30], fill=0)
fd.pieslice([120, 14, 152, 46], 270, 360, fill=220)
img.paste(Image.new("RGB", (W, H), c(28, 2, 8)), (0, 0), fr)
# HP
fb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
mini(4, 18, "HP", LBL)  # fuente 3x5, la mas chica legible
def tinta(x, y, txt, fnt):  # dibuja con la esquina de la tinta en (x, y)
    bx = d.textbbox((0, 0), txt, font=fnt); d.text((x - bx[0], y - bx[1]), txt, font=fnt, fill=TXT)
tinta(19, 17, "19", ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14))
tinta(48, 19, "19", ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 9))
for i in range(4): d.line([(45 - i, 19 + 2 * i), (45 - i, 20 + 2 * i)], fill=TXT)  # "/" recta 1:2
d.rectangle([65, 19, 87, 24], fill=TXT)  # barra 100% blanca
tr(213, 18, "Cleric")  # TODO: clase de la biblia
for x in (218, 227):
    d.rectangle([x, 20, x + 6, 27], fill=c(232, 224, 184), outline=c(88, 72, 40))
    d.line([(x + 2, 22), (x + 4, 22)], fill=c(88, 72, 40))

# banner del objeto
d.rounded_rectangle([65, 32, 175, 43], 6, fill=c(30, 4, 10), outline=c(176, 40, 64))
for x in range(100, 172):  # oscuro a la izquierda, se aclara a tinto hacia la derecha
    d.line([(x, 34), (x, 41)], fill=lerp((30, 4, 10), (110, 18, 36), (x - 100) / 72))
fs = ImageFont.load_default(size=10)  # letra chica para banner y hechizos
d.ellipse([69, 34, 76, 41], fill=c(168, 112, 72), outline=c(88, 56, 32))
d.text((80, 33), "Leather Shield", font=fs, fill=TXT)

# stats: etiquetas alineadas a la izquierda, valores a la derecha
sm = Image.new("L", (W, H), 0); smd = ImageDraw.Draw(sm)
for x in range(35): smd.line([(x, 62), (x, 136)], fill=int(170 - x * 3))  # translucido, se desvanece
img.paste(Image.new("RGB", (W, H), c(30, 4, 10)), (0, 0), sm)
stats = [("ATK", "11"), ("SKL", "6"), ("SPD", "7"), ("LCK", "10"),
         ("DEF", "2"), ("RES", "13"), ("MOV", "4")]
for i, (k, v) in enumerate(stats):
    y = 62 + round(i * 10.5)
    t(4, y, k, LBL); tr(42, y, v)
d.polygon([(44, 109), (47, 106), (56, 106), (56, 112), (47, 112)], fill=TXT)
mini(48, 107, "+3", DARK)

# libro de comandos: interlineado fijo, inicio sigue la curva del arco con separacion fija
SEP, PASO, Y0 = 5, 12, 48
skills = [("Nosferatu", (216, 200, 72)), ("Recover", (176, 224, 176)),
          ("Physic", (176, 224, 176)), ("Invoke", (176, 224, 176)), ("????", (216, 176, 96))]
for i, (s_, col) in enumerate(skills):
    y = Y0 + i * PASO; ym = y + 6
    xa = cx - math.sqrt(r * r - (ym - cy) ** 2)  # x del arco a esa altura
    x = int(xa) + SEP
    d.rectangle([x, y + 2, x + 7, y + 9], fill=c(*col), outline=c(88, 72, 40))
    d.text((x + 11, y), s_, font=fs, fill=TXT)

# barra inferior
# (sin franja inferior: los botones flotan sobre el retrato)
for i, ic in enumerate(["+", "o", "#", "="]):
    x = 4 + i * 23.5; x = int(x)
    grad_rect(x, 139, x + 21, 158, (120, 24, 44), (72, 12, 26))
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
