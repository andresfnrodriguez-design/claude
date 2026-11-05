"""Prepara retrato_3.png desde retrato_3_fuente.webp: recorta cabeza y hombros, quita el fondo
morado y el contorno blanco/negro del sprite (relleno desde los bordes), escala y cuantiza a RGB555."""
from PIL import Image
src = Image.open("retrato_3_fuente.webp").convert("RGB").crop((100, 20, 440, 320))
ESC = 0.7
img = src.resize((round(src.width * ESC), round(src.height * ESC)), Image.LANCZOS)
W, H = img.size; px = img.load()
def es_fondo(p):
    r, g, b = p
    return (b >= r and b > g) or min(p) > 190 or max(p) < 60   # morado, contorno blanco o negro
fondo = set(); pila = [(x, y) for x in range(W) for y in (0, H - 1)] + [(x, y) for y in range(H) for x in (0, W - 1)]
while pila:
    x, y = pila.pop()
    if 0 <= x < W and 0 <= y < H and (x, y) not in fondo and es_fondo(px[x, y]):
        fondo.add((x, y)); pila += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
# paleta de 15 colores (+1 transparente = una paleta de 16 de la GBA), sin tramado:
# 1 pixel del arte = 1 pixel de pantalla
q5 = lambda v: (v >> 3) << 3 | (v >> 5)
fig = [px[x, y] for y in range(H) for x in range(W) if (x, y) not in fondo]
muestra = Image.new("RGB", (len(fig), 1)); muestra.putdata(fig)
# 12 tonos por corte de mediana (piel y pelo dominan) + 3 reservados para que no se pierdan
# los acentos: dorado claro, dorado oscuro (ojos, diadema, aretes) y el contorno mas oscuro
base = muestra.quantize(colors=12, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
colores = [tuple(base.getpalette()[i * 3:i * 3 + 3]) for i in range(12)]
oro = [q for q in fig if q[0] > 170 and q[1] > 140 and q[2] < 120 and q[1] - q[2] > 70]
oro.sort(key=sum); m = len(oro) // 2
media = lambda L: tuple(sum(c_[i] for c_ in L) // len(L) for i in range(3))
colores += [media(oro[m:]), media(oro[:m]), min(fig, key=sum)]
colores = [tuple(q5(v) for v in col) for col in colores]
cerca = lambda q: min(colores, key=lambda col: sum((q[i] - col[i]) ** 2 for i in range(3)))
for y in range(H):
    for x in range(W):
        px[x, y] = (255, 0, 255) if (x, y) in fondo else cerca(px[x, y])
Image.new("RGB", (15 * 16, 16)).save("retrato_3_paleta.png")
sw = Image.new("RGB", (15 * 16, 16)); [sw.paste(col, (i * 16, 0, i * 16 + 16, 16)) for i, col in enumerate(colores)]
sw.resize((15 * 32, 32), Image.NEAREST).save("retrato_3_paleta.png")
print("paleta:", ["#%02x%02x%02x" % col for col in colores])
img.save("retrato_3.png"); print(img.size)
