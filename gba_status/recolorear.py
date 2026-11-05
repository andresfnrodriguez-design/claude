"""Recolorea la UI con un tema de paleta_oficial.TEMAS sin tocar el retrato, los iconos ni el blanco.
Uso: python3 recolorear.py [tema ...]   (sin argumentos: todos)"""
import sys, subprocess, os
from PIL import Image
from paleta_oficial import TEMAS, ZONAS, COLOR_ETIQUETAS
env = dict(os.environ); FONDO = env.get("FONDO", "luz")
sf = "" if FONDO == "luz" else "_" + FONDO
run = lambda **e: subprocess.run([sys.executable, "generar.py"], check=True, env={**env, **e}, capture_output=True)
run(); run(SIN_RETRATO="1", SIN_ICONOS="1"); run(FONDO="negro")
full = Image.open(f"estado_gba{sf}.png").convert("RGB"); ui = Image.open(f"estado_gba_sin_retrato_sin_iconos{sf}.png").convert("RGB")
negro = Image.open("estado_gba_negro.png").convert("RGB")  # para saber que pixeles dependen del fondo
W, H = full.size
TEXTOS_FIJOS = {(247, 206, 214), (255, 231, 239)}  # etiquetas (HP, ATK, LV...) y texto del arma
q5 = lambda v: (int(v) >> 3) << 3 | (int(v) >> 5)
lum = lambda p: (p[0] * 299 + p[1] * 587 + p[2] * 114) / 1000
uis = [ui.getpixel((x, y)) for y in range(H) for x in range(W)]
uis = [p for p, q in zip(uis, [negro.getpixel((x, y)) for y in range(H) for x in range(W)]) if FONDO == 'luz' or p == q] or uis
lo, hi = min(map(lum, uis)), max(lum(p) for p in uis if not min(p) > 200)
def rampa(stops, t):
    t = max(0, min(1, t)) * (len(stops) - 1); i = min(int(t), len(stops) - 2); k = t - i
    return tuple(q5(stops[i][j] + (stops[i + 1][j] - stops[i][j]) * k) for j in range(3))
for nombre in (sys.argv[1:] or TEMAS):
    stops = TEMAS[nombre]; out = full.copy()
    if stops:
        for y in range(H):
            for x in range(W):
                p, u = full.getpixel((x, y)), ui.getpixel((x, y))
                if p != u: continue                       # retrato o icono: no se toca
                if FONDO != "luz" and p != negro.getpixel((x, y)): continue  # fondo o translucido: se deja
                if p in TEXTOS_FIJOS:                     # etiquetas y texto del arma
                    if COLOR_ETIQUETAS.get(nombre): out.putpixel((x, y), COLOR_ETIQUETAS[nombre])
                    continue
                if min(p) > 200 and max(p) - min(p) < 40: continue  # blancos fijos
                st = next((r for (x0, y0, x1, y1), r in ZONAS.get(nombre, []) if x0 <= x <= x1 and y0 <= y <= y1), stops)
                out.putpixel((x, y), rampa(st, (lum(p) - lo) / (hi - lo)))
    out.save(f"tema_{nombre}{sf}.png"); out.resize((W * 4, H * 4), Image.NEAREST).save(f"tema_{nombre}{sf}_x4.png")
    print(nombre, len(out.getcolors(4096)), "colores")
