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

import os, random
FONDO = os.environ.get("FONDO", "luz")
def fondo_fisuras(c_izq, c_der, c_centro):
    """Degradado diagonal c_izq -> c_der con el centro oscurecido hacia c_centro, + esquirlas.
    Logica de las esquirlas:
      - se mueven muy lento, cada una en su propia direccion (y giran apenas); T = cuadro
      - su color sale del fondo que tienen DETRAS en ese momento (un poco mas claro u oscuro),
        asi sobre cyan solo hay esquirlas cyan y sobre magenta solo magenta; nunca blanco."""
    def raw(x, y):
        u = (x + y * 1.732) / (W + H * 1.732)   # franjas a 30 grados
        b_ = [c_izq[i] + (c_der[i] - c_izq[i]) * u for i in range(3)]
        k = max(0, 1 - abs(u - 0.5) / 0.35) * 0.75
        return [b_[i] + (c_centro[i] - b_[i]) * k for i in range(3)]
    for y in range(H):
        for x in range(W):
            img.putpixel((x, y), c(*raw(x, y)))
    T = float(os.environ.get("T", "0"))
    rnd = random.Random(7); dd = ImageDraw.Draw(img)
    for n in range(40):
        x0, y0 = rnd.randrange(W), rnd.randrange(H); L = rnd.randint(6, 22)
        a0 = rnd.random() * math.tau; giro = rnd.uniform(-0.008, 0.008)
        ang = rnd.random() * math.tau; vel = rnd.uniform(0.15, 0.35)      # px por cuadro: muy lento
        f = rnd.choice((1.35, 0.7))
        x0 = (x0 + math.cos(ang) * vel * T) % (W + 40) - 20
        y0 = (y0 + math.sin(ang) * vel * T) % (H + 40) - 20
        a0 += giro * T
        pts = [(x0 + L * math.cos(a0 + t), y0 + L * math.sin(a0 + t) * 0.6) for t in (0, 2.4, 3.6)]
        col = [min(200, v * f) for v in raw(x0, y0)]                     # color del fondo detras
        dd.polygon(pts, fill=c(*col))
if FONDO == "luz":
    # fondo: luz tinta que sale de la esquina superior izquierda
    for y in range(H):
        for x in range(W):
            dist = math.hypot(x, y * 1.2)
            ang = abs(math.atan2(y, x) - math.radians(35))  # haz hacia abajo-derecha
            k = dist / 260 + ang * 0.35
            img.putpixel((x, y), lerp((150, 40, 60), (36, 5, 12), min(1, k)))
elif FONDO == "fisuras":   # teal a la izquierda, brasa a la derecha
    fondo_fisuras((40, 150, 150), (216, 88, 48), (14, 26, 30))
elif FONDO == "fisuras_fucsia":   # teal a la izquierda, fucsia a la derecha
    fondo_fisuras((40, 150, 150), (200, 24, 96), (14, 26, 30))
elif FONDO == "negro":
    pass

# retrato (arte del usuario, fondo morado transparente)
# retratos disponibles: archivo, color de fondo a quitar, posicion y escala
# (el punto medio entre los ojos cae en ~(110, 84) de la pantalla)
RETRATOS = {
    "kairos": ("retrato_busto.png", (77, 26, 77), -26, 17, 3.2),
    "3": ("retrato_3.png", (255, 0, 255), -4, -1, 1.0),
    "2": ("retrato_2.png", (169, 203, 166), 1, 25, 2.4),
}
_arch, bgc, RX, RY, ESC_R = RETRATOS[os.environ.get("RETRATO", "kairos")]
art = Image.open(_arch).convert("RGB")
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
ESC = ESC_R  # cabeza grande, cortada bajo los hombros
art = art.resize((int(art.width * ESC), int(art.height * ESC)), Image.NEAREST)
mask = mask.resize(art.size, Image.NEAREST)
import os
if not os.environ.get("SIN_RETRATO"): img.paste(art, (RX, RY), mask)

# semicirculo negro translucido (centro fuera de pantalla a la derecha)
cx, cy, r = 337, 85, 180
m = Image.new("L", (W, H), 0)
ImageDraw.Draw(m).ellipse([cx - r, cy - r, cx + r, cy + r], fill=115)
img = Image.composite(Image.new("RGB", (W, H)), img, m)
d = ImageDraw.Draw(img); d.fontmode = "1"
ARC = c(232, 216, 216)
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ARC)
# x real de la linea blanca en cada fila (medida en pixeles, no por formula)
ARCX = {y: min((x for x in range(100, W) if img.getpixel((x, y)) == ARC), default=None) for y in range(H)}
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
def _tinta(txt):
    m_ = Image.new("L", (80, 20), 0); md = ImageDraw.Draw(m_); md.fontmode = "1"
    md.text((10, 0), txt, font=f, fill=255); return m_.getbbox()
def tinta_izq(x, y, txt, col): b_ = _tinta(txt); t(x - (b_[0] - 10), y, txt, col)
def tinta_der(x, y, txt, col=TXT): b_ = _tinta(txt); t(x - (b_[2] - 1 - 10), y, txt, col)
# botones de hombro L / R en las esquinas (cambiar de ventana)
def hombro(x0, letra, izq):
    x1 = x0 + 12
    d.rounded_rectangle([x0, 1, x1, 11], 3, fill=c(232, 216, 216))
    b_ = _tinta(letra); t(x0 + (13 - (b_[2] - b_[0])) // 2 - (b_[0] - 10), 1, letra, c(48, 8, 20))
# indicadores de cambio de ventana (L/R): solo puntas de flecha negras "<" y ">", animadas
# (se desplazan 1 px hacia afuera en cuadros alternos; T = cuadro)
_off = int(float(os.environ.get("T", "0")) / 18) % 2  # cambia cada 3 cuadros
def punta(cx, izq):
    # flecha rellena con muesca atras (chevron grueso), negra con un brillo gris arriba
    pts = [(0, 1), (3, 1), (8, 6), (3, 11), (0, 11), (4, 6)]          # ">" en caja 9x11
    if izq: pts = [(8 - px_, py_) for px_, py_ in pts]                 # espejo para "<"
    if not izq:   # compensacion optica: sobre fondo oscuro la flecha se ve mas chica -> halo gris de 1 px
        for ox, oy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            d.polygon([(cx + px_ + ox, py_ + oy) for px_, py_ in pts], fill=c(120, 120, 128))
    d.polygon([(cx + px_, py_) for px_, py_ in pts], fill=(0, 0, 0))
    luz = [(1, 2), (2, 2), (3, 3), (4, 4)]                               # brillo en el borde superior
    for px_, py_ in luz:
        d.point((cx + (8 - px_ if izq else px_), py_), fill=c(88, 88, 96))
punta(2 - _off, True); punta(229 + _off, False)
t(40, 0, "Kairos"); t(41, 0, "Kairos")  # mas grueso (doble pasada) y corrido a la derecha
for x0, x1, lab in [(140, 156, "LV"), (178, 198, "EXP")]:
    d.rounded_rectangle([x0, 2, x1, 11], 3, fill=DARK)
    fl = ImageFont.load_default(size=9)                      # un punto mas chica
    bb_ = d.textbbox((0, 0), lab, font=fl)
    d.text((x0 + (x1 - x0 + 1 - (bb_[2] - bb_[0])) // 2 - bb_[0], 2 + (10 - (bb_[3] - bb_[1])) // 2 - bb_[1]), lab, font=fl, fill=LBL)
tr(170, 1, "8"); tr(219, 1, "99")

# HP: franja vinotinto translucida bajo el HP, con extremo derecho curvo
fr = Image.new("L", (W, H), 0); fd = ImageDraw.Draw(fr)
fd.rectangle([0, 14, 150, 30], fill=220); fd.ellipse([130, -10, 170, 30], fill=0)
fd.pieslice([120, 14, 152, 46], 270, 360, fill=220)
img.paste(Image.new("RGB", (W, H), c(28, 2, 8)), (0, 0), fr)
# HP
fb = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
mini(8, 19, "HP", LBL)  # fuente 3x5; centrada en la franja (y 14-30) y corrida a la derecha
def tinta(x, y, txt, fnt):  # dibuja con la esquina de la tinta en (x, y)
    bx = d.textbbox((0, 0), txt, font=fnt); d.text((x - bx[0], y - bx[1]), txt, font=fnt, fill=TXT)
HP_ACT, HP_MAX = 13, 19
tinta(19, 17, str(HP_ACT), ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14))
tinta(48, 19, str(HP_MAX), ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 9))
for i in range(4): d.line([(45 - i, 19 + 2 * i), (45 - i, 20 + 2 * i)], fill=TXT)  # "/" recta 1:2
d.rectangle([65, 19, 87, 24], fill=c(96, 96, 104))                     # vacio en gris
lleno = round(23 * HP_ACT / HP_MAX)
if lleno: d.rectangle([65, 19, 65 + lleno - 1, 24], fill=TXT)          # parte proporcional en blanco
tr(213, 18, "Artifice")
# PLACEHOLDERS de iconos (tienen su propia paleta; con SIN_ICONOS=1 no se dibujan):
#  - 2 libritos junto a la clase = tipos de arma que puede usar la clase
#  - circulo del banner = arma/objeto equipado
#  - cuadraditos en curva = magias/habilidades de la unidad
ICONOS_ON = not os.environ.get("SIN_ICONOS")
for x in ((218, 227) if ICONOS_ON else ()):
    d.rectangle([x, 20, x + 6, 27], fill=c(232, 224, 184), outline=c(88, 72, 40))
    d.line([(x + 2, 22), (x + 4, 22)], fill=c(88, 72, 40))

# banner del objeto: una sola figura (placa redondeada + lente eliptica), simetrica
# en ambos ejes. Dos variantes de color (argumento A o B):
#  A: rojo al centro -> gris a los extremos, contorno vinotinto
#  B: vinotinto oscuro al centro -> rojo claro a los extremos, contorno negro
import sys
VAR = sys.argv[1] if len(sys.argv) > 1 else "A"
BX0, BY0, BX1, BY1 = 64, 32, 176, 42
EL = (66, 28, 174, 46)
ecx, ecy = (EL[0] + EL[2]) / 2, (EL[1] + EL[3]) / 2
ea, eb = (EL[2] - EL[0]) / 2, (EL[3] - EL[1]) / 2
fm = Image.new("L", (W, H), 0); fmd = ImageDraw.Draw(fm)
import atexit; atexit.register(lambda: fm.save("mascara_banner.png"))
fmd.rounded_rectangle([BX0, BY0, BX1, BY1], 5, fill=255)
for y in range(EL[1], EL[3] + 1):
    for x in range(EL[0], EL[2] + 1):
        if ((x - ecx) / ea) ** 2 + ((y - ecy) / eb) ** 2 <= 0.9: fm.putpixel((x, y), 255)
VINO, ROJO, GRIS, NEGRO = (130, 14, 34), (190, 32, 56), (110, 100, 106), (16, 2, 6)
for y in range(H):
    for x in range(W):
        if not fm.getpixel((x, y)): continue
        borde = any(not fm.getpixel((x + i, y + j)) for i, j in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        u = abs(x - ecx) / (BX1 - ecx)       # 0 centro, 1 extremos (simetrico)
        # mismos tonos y degradado vertical que los botones de abajo, mismo borde
        col = FR if borde else lerp((120, 24, 44), (72, 12, 26), u)  # claro al centro, oscuro a los extremos
        if not os.environ.get("SIN_BANNER"): d.point((x, y), fill=col)
BY0, BY1 = 28, 46
fs = ImageFont.load_default(size=10)  # letra chica para banner y hechizos
# tinta real del texto (medida en pixeles) para centrar el bloque escudo+texto
tm = Image.new("L", (200, 30), 0); tmd = ImageDraw.Draw(tm); tmd.fontmode = "1"
tmd.text((0, 0), "Leather Shield", font=fs, fill=255); ib = tm.getbbox()
tw, th = ib[2] - ib[0], ib[3] - ib[1]
FX0, FX1 = 64, 176                                   # extremos reales de la figura
blk = 10 + 4 + tw
tx = FX0 + (FX1 - FX0 + 1 - tw) // 2                  # texto centrado solo
bx = tx - 14                                          # escudo a su izquierda
my = (BY0 + BY1) / 2
if ICONOS_ON: d.ellipse([bx, round(my - 5), bx + 9, round(my + 4)], fill=c(208, 176, 128), outline=c(96, 72, 40))
d.text((bx + 14 - ib[0], round(my - th / 2) - ib[1]), "Leather Shield", font=fs, fill=c(248, 224, 232))

# stats: etiquetas alineadas a la izquierda, valores a la derecha
sm = Image.new("L", (W, H), 0); smd = ImageDraw.Draw(sm)
STY = 55  # bloque de stats centrado entre el fin de la franja negra (30) y el inicio de los botones (139)
for x in range(80): smd.line([(x, STY), (x, STY + 74)], fill=int(230 if x < 44 else max(0, 230 - (x - 44) * 6.4)))  # opaco bajo los numeros, se desvanece despues
img.paste(Image.new("RGB", (W, H), c(30, 4, 10)), (0, 0), sm)
stats = [("ATK", "11"), ("SKL", "6"), ("SPD", "7"), ("LCK", "10"),
         ("DEF", "2"), ("RES", "13"), ("MOV", "4")]
for i, (k, v) in enumerate(stats):
    y = STY + round(i * 10.5)
    tinta_izq(4, y, k, LBL); tinta_der(41, y, v)  # alineado por tinta real
dy = STY - 62
d.polygon([(44, 109 + dy), (47, 106 + dy), (56, 106 + dy), (56, 112 + dy), (47, 112 + dy)], fill=TXT)
mini(48, 107 + dy, "+3", DARK)

# libro de comandos: interlineado fijo, inicio sigue la curva del arco con separacion fija
DIST, PASO, Y0 = 11, 12, 48  # DIST: del centro del cuadrado a la linea blanca
GUIAS = []
skills = [("Nosferatu", (216, 200, 72)), ("Recover", (176, 224, 176)),
          ("Physic", (176, 224, 176)), ("Invoke", (176, 224, 176)), ("????", (216, 176, 96))]
for i, (s_, col) in enumerate(skills):
    y = Y0 + i * PASO; ym = y + 5                 # fila del centro del cuadrado (7x7)
    # centro sobre un circulo concentrico a la linea blanca: distancia perpendicular
    # (por la normal) siempre igual a DIST; se redondea hacia arriba
    x = ARCX[y + 2] + DIST  # esquina superior izquierda sobre la linea blanca corrida DIST px
    x += {2: -1, 4: 1}.get(i, 0)  # compensacion optica
    xc = x + 3
    if ICONOS_ON: d.rectangle([x, y + 2, x + 6, y + 8], fill=c(*col), outline=c(88, 72, 40))
    GUIAS.append((xc, ym))
    d.text((x + 10, y), s_, font=fs, fill=TXT)

# barra inferior
# (sin franja inferior: los botones flotan sobre el retrato)
def boton(x0, y0, x1, y1, rad=5):  # caja redondeada con degradado vertical
    g = Image.new("RGB", (x1 - x0 + 1, y1 - y0 + 1))
    for j in range(g.height):
        ImageDraw.Draw(g).line([(0, j), (g.width, j)], fill=lerp((120, 24, 44), (72, 12, 26), j / g.height))
    mk = Image.new("L", g.size, 0); ImageDraw.Draw(mk).rounded_rectangle([0, 0, g.width - 1, g.height - 1], rad, fill=255)
    img.paste(g, (x0, y0), mk)
    d.rounded_rectangle([x0, y0, x1, y1], rad, outline=FR)
# iconos de habilidad: 4 del negativo (fila de abajo de iconos_skills.webp)
hoja = Image.open("iconos_skills.webp").convert("L")
def icono(n, lado=12):
    # silueta = lo negro del cuadro negativo; se recorta a su caja y se ajusta a lado x lado
    x0 = round(18 + n * 141.7)
    t_ = hoja.crop((x0 + 6, 332, x0 + 112, 442)).point(lambda v: 255 if v < 110 else 0)
    t_ = t_.crop(t_.getbbox())
    k = lado / max(t_.size)
    t_ = t_.resize((max(1, round(t_.width * k)), max(1, round(t_.height * k))), Image.LANCZOS)
    t_ = t_.point(lambda v: 255 if v > 110 else 0)
    m_ = Image.new("L", (lado, lado), 0)
    m_.paste(t_, ((lado - t_.width) // 2, (lado - t_.height) // 2))
    return m_
ICONOS = [icono(n) for n in (0, 1, 4, 9)]  # fuego, frasco, espadas, gota
for i, ic in enumerate(ICONOS):
    x = 4 + i * 23.5; x = int(x)
    boton(x, 139, x + 21, 158)
    # icono en blanco sobre el degradado, centrado en el boton (22x20)
    ib_ = ic.getbbox(); iw, ih = ib_[2] - ib_[0], ib_[3] - ib_[1]  # centrar por la silueta real
    img.paste(Image.new("RGB", ic.size, TXT), (x + 1 + (20 - iw) // 2 - ib_[0], 140 + (18 - ih) // 2 - ib_[1]), ic)
boton(193, 139, 236, 158)
d.ellipse([197, 142, 210, 155], outline=TXT); d.ellipse([201, 146, 206, 151], fill=TXT)
d.text((218, 140), "3", font=fb, fill=TXT)

img = img.point(q5)
suf = "_sin_retrato" if os.environ.get("SIN_RETRATO") else ""
if os.environ.get("RETRATO", "kairos") != "kairos" and not os.environ.get("SIN_RETRATO"): suf += "_r" + os.environ["RETRATO"]
if os.environ.get("SIN_BANNER"): suf += "_sin_banner"
if not ICONOS_ON: suf += "_sin_iconos"
if FONDO != "luz": suf += "_" + FONDO
img.save(f"estado_gba{suf}.png")
img.resize((W * 4, H * 4), Image.NEAREST).save(f"estado_gba{suf}_x4.png")
print(len(img.getcolors(4096)), "colores")

g = Image.open("guia.png").convert("RGB").resize((W, H), Image.LANCZOS)
Image.blend(g, img, 0.5).resize((W * 4, H * 4), Image.NEAREST).save("comparacion_x4.png")

dbg = img.copy(); dd = ImageDraw.Draw(dbg)
for y in range(40, 110):  # linea blanca corrida DIST px (verde) y centros
    dd.point((ARCX[y] + DIST, y), fill=(0, 255, 0))
dbg.crop((140, 40, 240, 110)).resize((600, 420), Image.NEAREST).save("guias_hechizos_x6.png")
