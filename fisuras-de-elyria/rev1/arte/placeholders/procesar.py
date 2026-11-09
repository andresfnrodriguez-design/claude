#!/usr/bin/env python3
"""Convierte los paneles de la hoja de Nemira en assets listos para el juego.
Entrada raw/A.png B.png C.png Z.png H.png (paneles recortados de la hoja de Nano Banana).
Salida out/ con PNG indexados de 16 colores, todos con la misma paleta y #A9CBA6 en el índice 0."""
import os, numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

import sys, json
# uso: python3 procesar.py carpeta_personaje   (lee carpeta/config.json, carpeta/raw, escribe carpeta/out)
D = os.path.abspath(sys.argv[1])
CFG = json.load(open(f'{D}/config.json'))
RAW, OUT = f'{D}/raw', f'{D}/out'
os.makedirs(OUT, exist_ok=True)
BG = (169, 203, 166)          # A9CBA6, índice 0
OSCURO = (40, 40, 40)          # línea de contorno, igual que el slot 15 de los bandos
BLANCO = (248, 248, 248)
PID = CFG['id']
FONDO = tuple(CFG.get('fondo_hoja', [167, 199, 160]))

def cargar(k):
    im = Image.open(f'{RAW}/{k}.png').convert('RGB')
    a = np.asarray(im).copy()
    a[:4, :] = a[-4:, :] = a[:, :4] = a[:, -4:] = FONDO   # marco del panel fuera
    return a

def limpiar_etiqueta(a, alto, ancho):
    a[:alto, :ancho] = FONDO
    return a

def mascara(a, umbral=55):
    """figura = lo que no es fondo conectado al borde"""
    d = np.abs(a.astype(int) - np.array(FONDO)).sum(2)
    fondo = d < umbral
    lab, _ = ndimage.label(fondo)
    borde = set(np.unique(np.concatenate([lab[0], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(borde))
    fig = ~bg
    fig = ndimage.binary_opening(fig, iterations=1)
    return ndimage.binary_fill_holes(fig)

def a_img(a, m):
    """pone el fondo exacto donde no hay figura"""
    b = a.copy(); b[~m] = BG
    return Image.fromarray(b.astype(np.uint8))

def reducir(img, m, w, h):
    t = img.resize((w, h), Image.LANCZOS)
    mm = Image.fromarray((m * 255).astype(np.uint8)).resize((w, h), Image.BILINEAR)
    mm = np.asarray(mm) > 127
    t = np.asarray(t).copy(); t[~mm] = BG
    return t, mm

def contorno(t, mm, lienzo_w, lienzo_h, ox, oy):
    """1 px oscuro + 2 px blanco fuera de la silueta, sobre un lienzo más ancho"""
    L = np.zeros((lienzo_h, lienzo_w, 3), np.uint8); L[:] = BG
    M = np.zeros((lienzo_h, lienzo_w), bool)
    h, w = mm.shape
    L[oy:oy + h, ox:ox + w] = t; M[oy:oy + h, ox:ox + w] = mm
    cruz = ndimage.generate_binary_structure(2, 1)
    d1 = ndimage.binary_dilation(M, cruz, 1)
    d3 = ndimage.binary_dilation(M, cruz, 3)
    L[d3 & ~d1] = BLANCO
    L[d1 & ~M] = OSCURO
    return L

piezas = {}

# ESCENA y ESPEJO. Busto A, cabeza de unos 52 px en 112 como Eirika, 3 px de margen arriba
A = cargar('A')
if CFG.get('etiquetas'): A = limpiar_etiqueta(A, 40, 360)
mA = mascara(A)
ys, xs = np.where(mA); y0 = ys.min()
cab = mA[y0:y0 + CFG['alto_cabeza_A']]; cx = int(np.where(cab.any(0))[0].mean())
W = CFG['ancho_escena']; H = round(W * 112 / 100); top = y0 - round(H * 6 / 112)   # 6 = 3 px de margen + 3 px de contorno
x0 = max(0, min(A.shape[1] - W, cx - W // 2))
crop = A[max(0, top):max(0, top) + H, x0:x0 + W]; mc = mA[max(0, top):max(0, top) + H, x0:x0 + W]
t, mm = reducir(a_img(crop, mc), mc, 100, 112)
esc = contorno(t, mm, 104, 112, 2, 0)
piezas['escena_104x112'] = esc
piezas['espejo_104x112'] = esc[:, ::-1].copy()

# MINI. Cara lo más grande posible, corte en los hombros, sin borde blanco
lado = CFG['mini'][0]; my = y0 + CFG['mini'][1]
mx = max(0, cx - lado // 2 + CFG['mini'][2])
mcrop = A[my:my + lado, mx:mx + lado]; mmc = mA[my:my + lado, mx:mx + lado]
t, _ = reducir(a_img(mcrop, mmc), mmc, 32, 32)
piezas['mini_32x32'] = t

# ESTADO. Cuerpo C, cabeza de unos 30 px en 144, corte a media pierna. Va en 88x152 con la figura en x=8 y=4
C = cargar('C')
if CFG.get('etiquetas'): C = limpiar_etiqueta(C, 34, 200)
mC = mascara(C)
ys, xs = np.where(mC); cy0 = ys.min()
cab = mC[cy0:cy0 + CFG['alto_cabeza_C']]; ccx = int(np.where(cab.any(0))[0].mean())
if 'cabeza_C' in CFG: cy0, ccx = CFG['cabeza_C']   # [y de la coronilla, x del centro] si el arma sobresale por arriba
alto = CFG['alto_estado']; ancho = round(alto * 80 / 144); top = max(0, cy0 - 8)
ex = max(0, min(C.shape[1] - ancho, ccx - ancho // 2))
ecrop = C[top:top + alto, ex:ex + ancho]; emc = mC[top:top + alto, ex:ex + ancho]
t, _ = reducir(a_img(ecrop, emc), emc, 80, 144)
est = np.zeros((152, 88, 3), np.uint8); est[:] = BG; est[4:148, 8:88] = t
piezas['estado_88x152'] = est

# ZOOM y HERIDO. Primer plano 240x160, se corta por debajo de la etiqueta
for k, nom in (('Z', 'zoom_240x160'), ('H', 'herido_240x160')):
    a = cargar(k)
    y_a = CFG['zoom_y']; ww = a.shape[1] - 8; hh = round(ww / 1.5)
    if y_a + hh > a.shape[0] - 4: hh = a.shape[0] - 4 - y_a; ww = round(hh * 1.5)
    y_b = y_a + hh; xa = (a.shape[1] - ww) // 2
    img = Image.fromarray(a[y_a:y_b, xa:xa + ww].astype(np.uint8)).resize((240, 160), Image.LANCZOS)
    b = np.asarray(img).copy()
    b[np.abs(b.astype(int) - np.array(FONDO)).sum(2) < 30] = BG
    piezas[nom] = b

# PALETA COMPARTIDA. 13 colores de la figura + oscuro + blanco + fondo en el 0
todo = np.concatenate([p.reshape(-1, 3) for p in piezas.values()])
todo = todo[np.abs(todo.astype(int) - np.array(BG)).sum(1) > 20]
todo = todo[(np.abs(todo.astype(int) - np.array(BLANCO)).sum(1) > 30) & (np.abs(todo.astype(int) - np.array(OSCURO)).sum(1) > 30)]
muestra = Image.fromarray(todo[np.random.default_rng(1).choice(len(todo), 60000)].reshape(300, 200, 3))
# oro reservado. 2 slots para los ribetes dorados si el personaje los tiene
t = todo.astype(int)
oro = todo[(t[:, 0] > 150) & (t[:, 0] - t[:, 2] > 70) & (t[:, 1] - t[:, 2] > 40)]
n_oro = 2 if len(oro) > 300 else 0
cols_oro = []
if n_oro:
    mo = Image.fromarray(oro[np.random.default_rng(2).choice(len(oro), 4000)].reshape(40, 100, 3))
    cols_oro = np.array(mo.quantize(2, method=Image.Quantize.MEDIANCUT, kmeans=3).getpalette()[:6]).reshape(2, 3).tolist()
q = muestra.quantize(13 - n_oro, method=Image.Quantize.MEDIANCUT, kmeans=3)
cols = np.array(q.getpalette()[:3 * (13 - n_oro)]).reshape(13 - n_oro, 3).tolist() + cols_oro
cols = sorted([tuple(int(round(v / 8) * 8 if v < 248 else 248) for v in c) for c in cols], key=lambda c: sum(c))
pal = [BG, OSCURO] + cols + [BLANCO]
pal = [tuple(min(248, (v // 8) * 8 if i else v) for v in c) for i, c in enumerate(pal)]
pal[0] = BG
flat = [v for c in pal for v in c] + list(OSCURO) * 240
pimg = Image.new('P', (1, 1)); pimg.putpalette(flat)

for nom, arr in piezas.items():
    im = Image.fromarray(arr.astype(np.uint8)).quantize(palette=pimg, dither=Image.Dither.NONE)
    # el fondo exacto siempre al índice 0
    ia = np.asarray(im).copy()
    ia[(arr == np.array(BG)).all(2)] = 0
    o = Image.fromarray(ia, 'P'); o.putpalette(flat)
    o.save(f'{OUT}/{PID}_{nom}.png', transparency=0 if False else None)

with open(f'{OUT}/{PID}.pal', 'w', newline='\r\n') as f:
    f.write('JASC-PAL\n0100\n16\n' + ''.join(f'{r} {g} {b}\n' for r, g, b in pal))
print('paleta', ' '.join('%02x%02x%02x' % c for c in pal))
