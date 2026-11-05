"""Prepara retrato_3.png desde retrato_3_fuente.webp: recorta cabeza y hombros, quita el fondo
morado y el contorno blanco/negro del sprite (relleno desde los bordes), escala y cuantiza a RGB555."""
from PIL import Image
src = Image.open("retrato_3_fuente.webp").convert("RGB").crop((100, 20, 440, 320))
ESC = 0.86
img = src.resize((round(src.width * ESC), round(src.height * ESC)), Image.LANCZOS)
W, H = img.size; px = img.load()
def es_fondo(p):
    r, g, b = p
    return (b > r + 5 and b > g) or min(p) > 190 or max(p) < 60   # morado, contorno blanco o negro
fondo = set(); pila = [(x, y) for x in range(W) for y in (0, H - 1)] + [(x, y) for y in range(H) for x in (0, W - 1)]
while pila:
    x, y = pila.pop()
    if 0 <= x < W and 0 <= y < H and (x, y) not in fondo and es_fondo(px[x, y]):
        fondo.add((x, y)); pila += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
q5 = lambda v: (v >> 3) << 3 | (v >> 5)
for y in range(H):
    for x in range(W):
        px[x, y] = (255, 0, 255) if (x, y) in fondo else tuple(q5(v) for v in px[x, y])
img.save("retrato_3.png"); print(img.size)
