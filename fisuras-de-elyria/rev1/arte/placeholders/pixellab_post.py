#!/usr/bin/env python3
"""Deja una salida de PixelLab lista para el juego.
Uso: python3 pixellab_post.py entrada.png id carpeta_salida
Toma el busto de 100x112 que devuelve PixelLab, pone el fondo exacto #A9CBA6, reduce a 16 colores
(fondo en el índice 0, oscuro, 13 de la figura, blanco), agrega el contorno de 1 px oscuro + 2 px blanco
y guarda la escena de 104x112 indexada. El espejo se procesa aparte desde su propio busto, más la paleta .pal."""
import sys, os, numpy as np
from PIL import Image
from scipy import ndimage
from skimage.color import rgb2lab, lab2rgb
from sklearn.cluster import KMeans

BG, OSCURO, BLANCO = (169, 203, 166), (40, 40, 40), (248, 248, 248)
src, pid, dst = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(dst, exist_ok=True)
im = Image.open(src).convert('RGB')
if im.size != (100, 112):
    sys.exit(f'NO ENTREGAR. Se esperaba 100x112 y llegó {im.size[0]}x{im.size[1]}')
a = np.asarray(im).astype(int)

# fondo = lo parecido al color de las esquinas y conectado al borde
ref = np.median(np.stack([a[0, 0], a[0, -1], a[-1, 0], a[-1, -1]]), 0)
lab_f, _ = ndimage.label(np.abs(a - ref).sum(2) < 40)
borde = set(np.unique(np.concatenate([lab_f[0], lab_f[:, 0], lab_f[:, -1]]))) - {0}
fig = ndimage.binary_fill_holes(~np.isin(lab_f, list(borde)))

# PixelLab a veces deja 1 o 2 filas de fondo abajo. Se rellenan repitiendo la última fila de figura
for _ in range(2):
    if not fig[-1].any() and fig[-2].any():
        a[-1] = a[-2]; fig[-1] = fig[-2]
    elif not fig[-1].any() and fig[-3].any():
        a[-2:] = a[-3]; fig[-2:] = fig[-3]
errores = []
if fig[:3].any(): errores.append('la cabeza toca el borde de arriba')
if not fig[-1].any(): errores.append('el busto no llega al borde de abajo')
if fig[:-28, 0].any() or fig[:-28, -1].any(): errores.append('cabeza u hombros cortados por un costado')

# paleta de 13 colores de figura, k-means en Lab con el croma pesado al doble
px = a[fig]
px = px[(np.abs(px - BLANCO).sum(1) > 30) & (np.abs(px - OSCURO).sum(1) > 30)]
lab = rgb2lab(px.reshape(-1, 1, 3) / 255.0).reshape(-1, 3)
w = np.array([1.0, 2.0, 2.0])
km = KMeans(13, n_init=4, random_state=0).fit(lab * w)
cols = (np.clip(lab2rgb((km.cluster_centers_ / w).reshape(-1, 1, 3)).reshape(-1, 3), 0, 1) * 255).round().astype(int)
cols = sorted({tuple(min(248, int(round(v / 8) * 8)) for v in c) for c in cols}, key=sum)
pal = [BG, OSCURO] + cols + [BLANCO]
while len(pal) < 16: pal.insert(-1, OSCURO)

# mapear la figura a la paleta (sin el fondo)
palab = rgb2lab(np.array(pal[1:]).reshape(-1, 1, 3) / 255.0).reshape(-1, 3)
alab = rgb2lab(a.astype(np.uint8) / 255.0).reshape(-1, 3)
d = (((alab[:, None, :] - palab[None]) * np.array([1.0, 1.4, 1.4])) ** 2).sum(2)
idx = (d.argmin(1) + 1).reshape(112, 100).astype(np.uint8)
idx[~fig] = 0

# contorno sobre el lienzo de 104x112, figura en x=2
L = np.zeros((112, 104), np.uint8); M = np.zeros((112, 104), bool)
L[:, 2:102] = idx; M[:, 2:102] = fig
cruz = ndimage.generate_binary_structure(2, 1)
d1 = ndimage.binary_dilation(M, cruz, 1); d3 = ndimage.binary_dilation(M, cruz, 3)
L[d3 & ~d1] = 15; L[d1 & ~M] = 1

flat = [v for c in pal for v in c] + [0] * (768 - 48)
# el espejo real sale de otro busto (panel B), nunca se voltea la escena. Para el espejo, correr de nuevo con el busto B e id_espejo
for nom, arr in (('escena_104x112', L),):
    o = Image.fromarray(np.ascontiguousarray(arr), 'P'); o.putpalette(flat)
    o.save(f'{dst}/{pid}_{nom}.png')
with open(f'{dst}/{pid}_escena.pal', 'w', newline='\r\n') as f:
    f.write('JASC-PAL\n0100\n16\n' + ''.join(f'{r} {g} {b}\n' for r, g, b in pal))
print('paleta', ' '.join('%02x%02x%02x' % c for c in pal))
if errores:
    print('NO ENTREGAR. ' + ' | '.join(errores)); sys.exit(1)
print('OK, 16 colores con #A9CBA6 en el índice 0')
