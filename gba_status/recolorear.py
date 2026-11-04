"""Recolorea la UI con un tema de paleta_oficial.TEMAS sin tocar el retrato, los iconos ni el blanco.
Uso: python3 recolorear.py [tema ...]   (sin argumentos: todos)"""
import sys, subprocess, os
from PIL import Image
from paleta_oficial import TEMAS
env = dict(os.environ)
subprocess.run([sys.executable, "generar.py"], check=True, env=env, capture_output=True)
subprocess.run([sys.executable, "generar.py"], check=True, env={**env, "SIN_RETRATO": "1", "SIN_ICONOS": "1"}, capture_output=True)
full = Image.open("estado_gba.png").convert("RGB"); ui = Image.open("estado_gba_sin_retrato_sin_iconos.png").convert("RGB")
W, H = full.size
q5 = lambda v: (int(v) >> 3) << 3 | (int(v) >> 5)
lum = lambda p: (p[0] * 299 + p[1] * 587 + p[2] * 114) / 1000
uis = [ui.getpixel((x, y)) for y in range(H) for x in range(W)]
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
                if min(p) > 200 and max(p) - min(p) < 40: continue  # blancos fijos
                out.putpixel((x, y), rampa(stops, (lum(p) - lo) / (hi - lo)))
    out.save(f"tema_{nombre}.png"); out.resize((W * 4, H * 4), Image.NEAREST).save(f"tema_{nombre}_x4.png")
    print(nombre, len(out.getcolors(4096)), "colores")
