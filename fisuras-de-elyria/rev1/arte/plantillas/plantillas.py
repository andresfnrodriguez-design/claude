from PIL import Image, ImageDraw, ImageFont

W, H = 1536, 1024
BG = (245, 242, 235)
GREEN = (0xA9, 0xCB, 0xA6)
LINE = (40, 40, 40)
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
title_f = ImageFont.truetype(FB, 30)
lab_f = ImageFont.truetype(FB, 15)
small_f = ImageFont.truetype(F, 13)


def sheet(title, subtitle):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    d.text((40, 22), title, font=title_f, fill=LINE)
    d.text((40, 60), subtitle, font=small_f, fill=(90, 90, 90))
    return im, d


def box(d, x, y, w, h, label, note=None):
    d.rectangle([x, y, x + w, y + h], fill=GREEN, outline=LINE, width=2)
    d.text((x + 5, y + 4), label, font=lab_f, fill=LINE)
    if note:
        d.text((x + 5, y + 22), note, font=small_f, fill=(60, 60, 60))


def dashed(d, x1, y1, x2, y2, color=(200, 60, 60), dash=8, width=2):
    import math
    L = math.hypot(x2 - x1, y2 - y1)
    n = int(L // dash)
    for k in range(0, n, 2):
        a, b = k / n, min((k + 1) / n, 1)
        d.line([x1 + (x2 - x1) * a, y1 + (y2 - y1) * a, x1 + (x2 - x1) * b, y1 + (y2 - y1) * b], fill=color, width=width)


def guide(d, x, y, text, color=(200, 60, 60)):
    d.text((x, y), text, font=small_f, fill=color)


def header(d, x, y, text):
    d.text((x, y), text, font=lab_f, fill=LINE)


# Hoja 1. Concepto
im, d = sheet("HOJA 1 · CONCEPTO", "Giro completo, paleta, expresiones y pose de ataque. Fondo de cada recuadro #A9CBA6.")
header(d, 40, 92, "GIRO COMPLETO (cuerpo entero, misma escala, pies en la línea)")
labels = ["FRENTE", "3/4 DERECHA", "3/4 IZQUIERDA", "ESPALDA"]
for i, l in enumerate(labels):
    box(d, 40 + i * 230, 118, 215, 560, l)
for i in range(4):
    x = 40 + i * 230
    dashed(d, x + 4, 160, x + 211, 160)
    dashed(d, x + 4, 650, x + 211, 650)
    dashed(d, x + 107, 166, x + 107, 644, color=(120, 120, 200))
guide(d, 44, 144, "tope de la cabeza")
guide(d, 44, 654, "pies")
guide(d, 44, 676, "cuerpo entero entre las dos líneas · eje azul = centro del cuerpo", color=(90, 90, 90))

header(d, 990, 92, "PALETA OFICIAL (16 colores)")
for i in range(16):
    x = 990 + (i % 8) * 62
    y = 118 + (i // 8) * 62
    fill = GREEN if i == 0 else (255, 255, 255)
    d.rectangle([x, y, x + 54, y + 54], fill=fill, outline=LINE, width=2)
    d.text((x + 4, y + 36), str(i), font=small_f, fill=LINE)
d.text((990, 244), "0 = fondo #A9CBA6 · 1 = contorno · 2 = blanco del contorno", font=small_f, fill=(60, 60, 60))

header(d, 990, 280, "EXPRESIONES (cabeza y hombros)")
for i, l in enumerate(["NEUTRA", "SONRISA", "HABLANDO", "OJOS CERRADOS"]):
    x, y = 990 + (i % 2) * 255, 306 + (i // 2) * 175
    box(d, x, y, 240, 160, l)
    dashed(d, x + 4, y + 30, x + 236, y + 30, dash=6)
    dashed(d, x + 4, y + 148, x + 236, y + 148, dash=6)
    dashed(d, x + 120, y + 34, x + 120, y + 144, color=(120, 120, 200), dash=6)
guide(d, 990, 646, "arriba = tope de la cabeza · abajo = corte en los hombros", color=(90, 90, 90))

header(d, 40, 700, "POSE DE ATAQUE (cuerpo entero, arma de la clase)")
box(d, 40, 726, 600, 270, "ATAQUE")
dashed(d, 60, 750, 620, 750)
dashed(d, 60, 975, 620, 975)
dashed(d, 60, 750, 60, 975)
dashed(d, 620, 750, 620, 975)
guide(d, 66, 954, "cuerpo y arma completos dentro del recuadro punteado, pies abajo")
header(d, 680, 700, "DETALLES (objetos, arma, texturas)")
for i in range(4):
    box(d, 680 + i * 205, 726, 190, 270, f"DETALLE {i + 1}", "primer plano centrado")
im.save("hoja1_concepto.png")

# Hoja 2. Retratos
im, d = sheet("HOJA 2 · RETRATOS", "Proporciones reales del juego x4 (escena 100x112, estado 80x144, mini 32x32, boca y ojos 32x16).")
box(d, 40, 100, 400, 448, "ESCENA · mira a la derecha", "cintura para arriba, 3 px de fondo arriba")
box(d, 470, 100, 400, 448, "ESPEJO REAL · mira a la izquierda", "redibujado, los objetos NO cambian de lado")
box(d, 900, 100, 240, 432, "ESTADO", "cuerpo completo")
box(d, 1180, 100, 128, 128, "MINI")
header(d, 1180, 250, "BOCAS (32x16)")
mouths = ["NORM. cerrada", "NORM. media", "NORM. abierta", "SONR. cerrada", "SONR. media", "SONR. abierta"]
for i, l in enumerate(mouths):
    col, row = i // 3, i % 3
    box(d, 1180 + col * 150, 276 + row * 80, 128, 64, l)
header(d, 1180, 524, "OJOS (32x16)")
for i, l in enumerate(["ENTRECERR.", "CERRADOS"]):
    box(d, 1180 + i * 150, 550, 128, 64, l)
d.text((40, 570), "Bocas y ojos son recortes de la cara del retrato de ESCENA, misma escala y mismo encuadre, solo cambia la boca o los ojos.", font=small_f, fill=(60, 60, 60))
header(d, 40, 610, "POSES ALTERNATIVAS DE ESCENA (100x112, x2)")
for i in range(3):
    box(d, 40 + i * 300, 636, 200, 224, f"POSE {i + 1}", "mismo encuadre que ESCENA")
im.save("hoja2_retratos.png")

# Hoja 3. Sprites
im, d = sheet("HOJA 3 · SPRITES", "Mapa: figura de 16x16 (celda de 32x32 en movimiento). Batalla: lienzo 248x160, personaje en x=140, pies en y=102.")
header(d, 40, 92, "MAPA QUIETO (3 cuadros de 16x16, x6)")
for i in range(3):
    box(d, 40 + i * 110, 118, 96, 96, str(i + 1))
header(d, 40, 236, "MAPA EN MOVIMIENTO (celdas de 32x32, x3)")
rows = [("IZQUIERDA", 4), ("ABAJO", 4), ("ARRIBA", 4), ("SELECCIONADO", 3)]
for r, (l, n) in enumerate(rows):
    y = 262 + r * 112
    d.text((40, y + 40), l, font=small_f, fill=LINE)
    for i in range(n):
        box(d, 150 + i * 102, y, 96, 96, str(i + 1))
d.text((40, 712), "La derecha la voltea el motor.", font=small_f, fill=(60, 60, 60))

header(d, 600, 92, "BATALLA · cuadros clave (248x160, x1)")
poses = ["QUIETO", "ATAQUE cuerpo a cuerpo", "CRÍTICO cuerpo a cuerpo", "ATAQUE a distancia",
         "CRÍTICO a distancia", "ESQUIVE", "ATAQUE FALLADO", "IMPACTO del arma"]
for i, l in enumerate(poses):
    x = 600 + (i % 3) * 272
    y = 118 + (i // 3) * 184
    box(d, x, y, 248, 160, l)
    d.line([x + 2, y + 102, x + 246, y + 102], fill=(200, 60, 60), width=3)
d.text((600, 720), "Línea roja = pies. El personaje mira a la izquierda, hacia el enemigo.", font=small_f, fill=(200, 60, 60))
im.save("hoja3_sprites.png")
print("ok")
