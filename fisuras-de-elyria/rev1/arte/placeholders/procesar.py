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
# escala común de todo el elenco. Si un personaje nuevo no entra, se achica para TODOS o se regenera su pose, nunca se escala uno solo
CABEZA_BUSTO = 34    # px de coronilla a mentón en el busto de 112
ALTURA_ESTADO = 112  # px de coronilla a suela para estatura 1.0 en el estado de 144
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
ERRORES = []
def busto(k, cabeza, nom):
    A = cargar(k)
    if CFG.get('etiquetas'): A = limpiar_etiqueta(A, 40, 360)
    mA = mascara(A)
    ys, xs = np.where(mA); y0 = ys.min()
    W = round(100 * cabeza / CABEZA_BUSTO)   # misma cabeza en todos los bustos
    H = round(W * 112 / 100); top = y0 - round(H * 6 / 112)   # 6 = 3 px de margen + 3 px de contorno
    # centrado en la silueta del busto (no en la cabeza) y con relleno de fondo si la ventana se sale del panel
    banda = mA[y0:y0 + int(H * 0.89)]; cb = np.where(banda.any(0))[0]; cx = (cb.min() + cb.max()) // 2
    pd = max(W, H)
    Ap = np.zeros((A.shape[0] + 2 * pd, A.shape[1] + 2 * pd, 3), A.dtype); Ap[:] = FONDO; Ap[pd:pd + A.shape[0], pd:pd + A.shape[1]] = A
    Mp_ = np.zeros(Ap.shape[:2], bool); Mp_[pd:pd + A.shape[0], pd:pd + A.shape[1]] = mA
    # el busto tiene que salir por el borde de abajo. Si el panel termina antes, la ventana sube y la cabeza baja un poco
    fondo_fig = ys.max()
    if top + H > fondo_fig + 1: top = fondo_fig + 1 - H
    x0 = pd + cx - W // 2; yt = pd + top
    crop = Ap[yt:yt + H, x0:x0 + W]; mc = Mp_[yt:yt + H, x0:x0 + W]
    t, mm = reducir(a_img(crop, mc), mc, 100, 112)
    a_img(crop, mc).save(f'{OUT}/{PID}_{nom}_fuente.png')   # busto encuadrado antes de reducir, para PixelLab
    if mm[:3].any(): ERRORES.append(f'{nom}: la cabeza toca el borde de arriba')
    if not mm[-1].any(): ERRORES.append(f'{nom}: el busto no llega al borde de abajo')
    if mm[:-28, 0].any() or mm[:-28, -1].any(): ERRORES.append(f'{nom}: cabeza u hombros se cortan por un costado')   # el cuarto de abajo puede tocar el borde, como en FE
    piezas[f'{nom}_104x112'] = contorno(t, mm, 104, 112, 2, 0)
    return A, mA, y0, cx

A, mA, y0, cx = busto('A', CFG['cabeza_A'], 'escena')
# ESPEJO real. Panel B (mirando a la izquierda, redibujado), mismo encuadre y misma escala de cabeza
if os.path.exists(f'{RAW}/B.png'):
    busto('B', CFG.get('cabeza_B', CFG['cabeza_A']), 'espejo')
else:
    # nunca se entrega la escena volteada como espejo. Sin panel B no hay espejo
    ERRORES.append('espejo: falta raw/B.png (busto redibujado mirando a la izquierda). No se voltea la escena')

# MINI. Cabeza entera y centrada, unos 22 px de coronilla a mentón en 32, con un poco de hombros
cabA = CFG['cabeza_A']; lado = round(cabA * 32 / 22)
# centro = mitad del ancho del cráneo a la altura de la frente
cab_m = mA[y0 + int(cabA * 0.12): y0 + int(cabA * 0.35)]   # altura de la frente: ancho del cráneo, sin hombros ni carcaj
cols = np.where(cab_m.any(0))[0]
hcx = (cols.min() + cols.max()) // 2 if len(cols) else cx
hcx += CFG.get('mini_dx', 0)
pdm = lado
Am = np.zeros((A.shape[0] + 2 * pdm, A.shape[1] + 2 * pdm, 3), A.dtype); Am[:] = FONDO; Am[pdm:pdm + A.shape[0], pdm:pdm + A.shape[1]] = A
Mm = np.zeros(Am.shape[:2], bool); Mm[pdm:pdm + A.shape[0], pdm:pdm + A.shape[1]] = mA
my = pdm + y0 - round(lado * 2 / 32); mx = pdm + hcx - lado // 2
mcrop = Am[my:my + lado, mx:mx + lado]; mmc = Mm[my:my + lado, mx:mx + lado]
t, mmini = reducir(a_img(mcrop, mmc), mmc, 32, 32)
if mmini[0].any(): ERRORES.append('mini: la cabeza toca el borde de arriba')
piezas['mini_32x32'] = t
a_img(mcrop, mmc).save(f'{OUT}/{PID}_mini_fuente.png')

# ESTADO. Cuerpo C, cabeza de unos 30 px en 144, corte a media pierna. Va en 88x152 con la figura en x=8 y=4
C = cargar('C')
if CFG.get('etiquetas'): C = limpiar_etiqueta(C, 34, 200)
mC = mascara(C)
# figura principal = componente conexa más grande (descarta restos de otros paneles)
lab_c, n_c = ndimage.label(mC)
if n_c > 1:
    tam = ndimage.sum(mC, lab_c, range(1, n_c + 1)); mC = lab_c == (int(np.argmax(tam)) + 1)
ys, xs = np.where(mC); cy0, pies = ys.min(), ys.max()
if 'cabeza_C' in CFG: cy0 = CFG['cabeza_C'][0]   # y de la coronilla si el arma sobresale por arriba
# escala común a todo el elenco. Una figura de estatura 1.0 mide 128 px de coronilla a suela y entra entera con los pies, así todos quedan proporcionados entre sí
esc = ALTURA_ESTADO * CFG.get('estatura', 1.0) / (pies - cy0)   # figura entera, de coronilla a suela
cxv = (xs.min() + xs.max()) // 2   # centrado en la silueta completa
Wv, Hv = round(80 / esc), round(144 / esc)
tv = min(cy0, ys.min()) - round(4 / esc)   # 4 px de margen sobre lo más alto (cabeza o arma)
pad = max(Wv, Hv)
Cp = np.zeros((C.shape[0] + 2 * pad, C.shape[1] + 2 * pad, 3), C.dtype); Cp[:] = FONDO; Cp[pad:pad + C.shape[0], pad:pad + C.shape[1]] = C
Mp = np.zeros(Cp.shape[:2], bool); Mp[pad:pad + C.shape[0], pad:pad + C.shape[1]] = mC
ex = pad + cxv - Wv // 2; ey = pad + tv
ecrop = Cp[ey:ey + Hv, ex:ex + Wv]; emc = Mp[ey:ey + Hv, ex:ex + Wv]
t, me = reducir(a_img(ecrop, emc), emc, 80, 144)
a_img(ecrop, emc).save(f'{OUT}/{PID}_estado_fuente.png')
if me[:3].any(): ERRORES.append('estado: la cabeza o el arma tocan el borde de arriba')
if me[:, 0].any() or me[:, -1].any(): ERRORES.append('estado: la figura se corta por un costado')
if me[-1].any(): ERRORES.append('estado: los pies tocan el borde de abajo')
est = np.zeros((152, 88, 3), np.uint8); est[:] = BG; est[4:148, 8:88] = t
piezas['estado_88x152'] = est

# COMBATE. Panel F (cuerpo entero en guardia, mirando a la izquierda). 33 px de coronilla a suela para estatura 1.0,
# en un recuadro de 80x56 con la suela en y=52, para la animación de batalla
ALTURA_COMBATE = 33
if os.path.exists(f'{RAW}/F.png'):
    F = cargar('F'); mF = mascara(F)
    lab_f, n_f = ndimage.label(mF)
    if n_f > 1:
        tam = ndimage.sum(mF, lab_f, range(1, n_f + 1)); mF = lab_f == (int(np.argmax(tam)) + 1)
    ys, xs = np.where(mF); fy0, fpies = ys.min(), ys.max()
    if 'cabeza_F' in CFG: fy0 = CFG['cabeza_F']
    escf = ALTURA_COMBATE * CFG.get('estatura', 1.0) / (fpies - fy0)
    Wf, Hf = round(80 / escf), round(56 / escf)
    cxf = (xs.min() + xs.max()) // 2
    padf = max(Wf, Hf)
    Fp = np.zeros((F.shape[0] + 2 * padf, F.shape[1] + 2 * padf, 3), F.dtype); Fp[:] = FONDO; Fp[padf:padf + F.shape[0], padf:padf + F.shape[1]] = F
    Mf = np.zeros(Fp.shape[:2], bool); Mf[padf:padf + F.shape[0], padf:padf + F.shape[1]] = mF
    fx = padf + cxf - Wf // 2; fy = padf + fpies - round(52 / escf)
    fcrop = Fp[fy:fy + Hf, fx:fx + Wf]; fmc = Mf[fy:fy + Hf, fx:fx + Wf]
    a_img(fcrop, fmc).save(f'{OUT}/{PID}_combate_fuente.png')
    t, mf = reducir(a_img(fcrop, fmc), fmc, 80, 56)
    if mf[:2].any() or mf[:, 0].any() or mf[:, -1].any(): ERRORES.append('combate: la figura toca un borde')
    piezas['combate_80x56'] = t
else:
    print('AVISO. combate: falta raw/F.png')

# ZOOM y HERIDO. Primer plano de 120x80, media pantalla de GBA
for k, nom in (('Z', 'zoom_120x80'), ('H', 'herido_120x80')):
    a = cargar(k)
    y_a = CFG['zoom_y']; ww = a.shape[1] - 8; hh = round(ww / 1.5)
    if y_a + hh > a.shape[0] - 4: hh = a.shape[0] - 4 - y_a; ww = round(hh * 1.5)
    y_b = y_a + hh; xa = (a.shape[1] - ww) // 2
    fz = Image.fromarray(a[y_a:y_b, xa:xa + ww].astype(np.uint8)); fz.save(f'{OUT}/{PID}_{nom.split("_")[0]}_fuente.png')
    img = fz.resize((120, 80), Image.LANCZOS)
    b = np.asarray(img).copy()
    b[np.abs(b.astype(int) - np.array(FONDO)).sum(2) < 30] = BG
    piezas[nom] = b

# saturación opcional antes de cuantizar, para dibujos muy apagados
from PIL import ImageEnhance
fs = CFG.get('saturacion', 1.0)
if fs != 1.0:
    for k in piezas:
        m = (piezas[k] == np.array(BG)).all(2)
        e = np.asarray(ImageEnhance.Color(Image.fromarray(piezas[k].astype(np.uint8))).enhance(fs)).copy()
        e[m] = BG; piezas[k] = e
# PALETA COMPARTIDA. 13 colores de la figura + oscuro + blanco + fondo en el 0
# cada pieza aporta la misma cantidad de muestras, así los primeros planos no se comen la paleta
rng = np.random.default_rng(1)
def figura_px(p):
    x = p.reshape(-1, 3); x = x[np.abs(x.astype(int) - np.array(BG)).sum(1) > 20]
    x = x[(np.abs(x.astype(int) - np.array(BLANCO)).sum(1) > 30) & (np.abs(x.astype(int) - np.array(OSCURO)).sum(1) > 30)]
    return x[rng.choice(len(x), 12000)] if len(x) else x
todo = np.concatenate([figura_px(p) for p in piezas.values()])
t = todo.astype(int)
croma = t.max(1) - t.min(1)
# k-means en espacio Lab, con el croma pesado al doble para que pelo, tela y oro no se pierdan en los grises
from skimage.color import rgb2lab, lab2rgb
from sklearn.cluster import KMeans
lab = rgb2lab((todo.reshape(-1, 1, 3) / 255.0)).reshape(-1, 3)
peso = CFG.get('peso_croma', 2.0)
X = lab * np.array([1.0, peso, peso])
km = KMeans(13, n_init=4, random_state=0).fit(X[rng.choice(len(X), min(len(X), 40000), replace=False)])
centros = km.cluster_centers_ / np.array([1.0, peso, peso])
cols = (np.clip(lab2rgb(centros.reshape(-1, 1, 3)).reshape(-1, 3), 0, 1) * 255).round().astype(int).tolist()
cols = sorted([tuple(int(round(v / 8) * 8 if v < 248 else 248) for v in c) for c in cols], key=lambda c: sum(c))
pal = [BG, OSCURO] + cols + [BLANCO]
pal = [tuple(min(248, (v // 8) * 8 if i else v) for v in c) for i, c in enumerate(pal)]
pal[0] = BG
flat = [v for c in pal for v in c] + list(OSCURO) * 240
pimg = Image.new('P', (1, 1)); pimg.putpalette(flat)

for nom, arr in piezas.items():
    palab = rgb2lab((np.array(pal).reshape(-1, 1, 3) / 255.0)).reshape(-1, 3)
    plab = rgb2lab(arr.astype(np.uint8) / 255.0).reshape(-1, 3)
    d = ((plab[:, None, :] - palab[None, 1:, :]) * np.array([1.0, 1.4, 1.4])) ** 2
    ia = (d.sum(2).argmin(1) + 1).reshape(arr.shape[:2]).astype(np.uint8)
    ia[(arr == np.array(BG)).all(2)] = 0
    o = Image.fromarray(ia, 'P'); o.putpalette(flat)
    o.save(f'{OUT}/{PID}_{nom}.png', transparency=0 if False else None)

with open(f'{OUT}/{PID}.pal', 'w', newline='\r\n') as f:
    f.write('JASC-PAL\n0100\n16\n' + ''.join(f'{r} {g} {b}\n' for r, g, b in pal))
print('paleta', ' '.join('%02x%02x%02x' % c for c in pal))

if ERRORES:
    print('NO ENTREGAR. ' + ' | '.join(ERRORES))
    sys.exit(1)
print('OK, todo entra en sus recuadros a escala común')
