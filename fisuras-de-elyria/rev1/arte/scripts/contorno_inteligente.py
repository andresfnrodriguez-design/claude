"""Contorno inteligente (selective outline) para sprites de mapa.

Agrega 1 px por fuera de la figura (solo vecinos ortogonales, así no engorda las diagonales).
Cada píxel del borde toma un tono oscuro del material que tiene al lado.
Lado de sombra (abajo y derecha, luz desde arriba a la izquierda) más oscuro que el lado de luz.
El metal y los blancos (poca saturación, mucha luz) usan gris oscuro en vez de su propio tono.
La figura crece 1 px por lado: generar de 15 de alto para terminar en 17 como máximo.

Uso: python3 contorno_inteligente.py entrada.png salida.png
"""
import sys, colorsys
import numpy as np
from PIL import Image
from scipy import ndimage

def oscuro(c, f):
    h, l, s = colorsys.rgb_to_hls(*(np.array(c) / 255))
    r, g, b = colorsys.hls_to_rgb(h, max(0, l * f), s)
    return [int(r * 255), int(g * 255), int(b * 255)]

def contorno(a):
    a = a.astype(int); m = a[..., 3] > 0; out = a.copy()
    H, W = m.shape
    anillo = ndimage.binary_dilation(m, structure=[[0, 1, 0], [1, 1, 1], [0, 1, 0]]) & ~m
    for y, x in zip(*np.where(anillo)):
        orto = [(dy, dx) for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1))
                if 0 <= y + dy < H and 0 <= x + dx < W and m[y + dy, x + dx]]
        c = np.mean([a[y + dy, x + dx, :3] for dy, dx in orto], 0)
        sombra = (-1, 0) in orto or (0, -1) in orto
        h, l, s = colorsys.rgb_to_hls(*(c / 255))
        if l > 0.72 or (s < 0.25 and l > 0.6):   # metal y blancos
            out[y, x, :3] = [40, 40, 40] if sombra else [72, 72, 80]
        else:
            out[y, x, :3] = oscuro(c, 0.35 if sombra else 0.6)
        out[y, x, 3] = 255
    return out.astype(np.uint8)

if __name__ == '__main__':
    a = np.array(Image.open(sys.argv[1]).convert('RGBA'))
    Image.fromarray(contorno(a)).save(sys.argv[2])
