"""Pantalla de estado estilo GBA: 240x160, color RGB555 (15 bits)."""
from PIL import Image, ImageDraw, ImageFont

W, H = 240, 160
def c(r, g, b):  # cuantiza a 5 bits por canal (paleta GBA)
    q = lambda v: (v >> 3) << 3 | (v >> 5)
    return (q(r), q(g), q(b))

BG, BG2 = c(56, 16, 24), c(88, 24, 40)
BAR, FR = c(120, 32, 56), c(200, 120, 136)
TXT, LBL, HL = c(248, 248, 248), c(248, 176, 192), c(248, 216, 96)
DARK = c(32, 8, 16)
SKIN, HAIR, HAIR2, EYE = c(248, 216, 184), c(240, 136, 104), c(200, 88, 72), c(112, 56, 32)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img); d.fontmode = "1"
f = ImageFont.load_default()  # fuente bitmap pequeña
def t(x, y, s, col=TXT): d.text((x, y), s, font=f, fill=col)

# fondo con franjas
for y in range(14, 144, 4): d.line([(0, y), (W, y)], fill=BG2)

# barra superior
d.rectangle([0, 0, 239, 12], fill=BAR); d.line([(0, 13), (239, 13)], fill=FR)
t(3, 1, "Genny"); t(62, 1, "LV", LBL); t(76, 1, "8")
t(92, 1, "EXP", LBL); t(112, 1, "99"); t(136, 1, "RTG", LBL); t(158, 1, "71")
t(196, 1, "Cleric", HL)

# HP
t(3, 16, "HP", LBL); t(16, 16, "19/19")
d.rectangle([2, 26, 58, 29], fill=DARK); d.rectangle([3, 27, 57, 28], fill=c(120, 232, 120))

# retrato simplificado (placeholder pixel)
px, py = 70, 32
d.rectangle([px, py, px + 80, py + 96], fill=BG2, outline=FR)
d.ellipse([px + 14, py + 8, px + 66, py + 66], fill=HAIR)
d.ellipse([px + 22, py + 22, px + 58, py + 66], fill=SKIN)
d.rectangle([px + 22, py + 18, px + 58, py + 30], fill=HAIR2)
d.rectangle([px + 30, py + 40, px + 34, py + 46], fill=EYE)
d.rectangle([px + 46, py + 40, px + 50, py + 46], fill=EYE)
d.line([(px + 37, py + 56), (px + 43, py + 56)], fill=c(200, 96, 96))
d.ellipse([px + 6, py + 50, px + 26, py + 80], fill=HAIR)
d.ellipse([px + 54, py + 50, px + 74, py + 80], fill=HAIR)
d.rectangle([px + 20, py + 78, px + 60, py + 95], fill=c(72, 64, 136))

# objeto equipado
d.rectangle([62, 18, 160, 28], fill=DARK, outline=FR)
d.ellipse([65, 20, 71, 26], fill=c(176, 112, 64)); t(75, 18, "Leather Shield")

# stats
stats = [("ATK", "11"), ("SKL", "6"), ("SPD", "7"), ("LCK", "10"),
         ("DEF", "2+3"), ("RES", "13"), ("MOV", "4")]
for i, (k, v) in enumerate(stats):
    y = 32 + i * 14
    d.rectangle([2, y, 60, y + 11], fill=DARK)
    t(5, y, k, LBL); t(30, y, v, HL if "+" in v else TXT)

# habilidades
skills = [("Nosferatu", c(232, 200, 80)), ("Recover", c(200, 232, 160)),
          ("Physic", c(200, 232, 160)), ("Invoke", c(200, 232, 160)), ("????", c(160, 160, 160))]
for i, (s, col) in enumerate(skills):
    y = 34 + i * 16
    d.rectangle([158, y, 236, y + 12], fill=DARK, outline=FR)
    d.rectangle([161, y + 3, 167, y + 9], fill=col); t(171, y + 1, s)

# barra inferior de iconos
d.rectangle([0, 146, 239, 159], fill=BAR); d.line([(0, 145), (239, 145)], fill=FR)
for i, lab in enumerate(["L", "R", "SEL", "INFO"]):
    x = 3 + i * 34; d.rectangle([x, 147, x + 31, 158], fill=DARK, outline=FR)
    t(x + 3, 146, lab, LBL)
t(196, 147, "TURN 3", HL)

img.save("estado_gba.png")
img.resize((W * 4, H * 4), Image.NEAREST).save("estado_gba_x4.png")
print(len(img.getcolors()), "colores")
