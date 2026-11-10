#!/usr/bin/env python3
"""Una sola imagen para PixelLab con todos los encuadres, y el corte de vuelta.

Armar:  python3 hoja_pixellab.py armar carpeta_personaje
        Lee carpeta/out/{id}_*_fuente.png (los deja procesar.py) y escribe
        carpeta/pixellab/{id}_hoja_pixellab_2016x1312.png  -> subir a PixelLab con Output Scale ÷4
        carpeta/pixellab/{id}_paleta_pixellab.png          -> subir en Color palette, Max colours 16

Cortar: python3 hoja_pixellab.py cortar carpeta_personaje salida_pixellab.png
        Espera la salida de 504x328, corta cada recuadro por coordenadas, pone el fondo exacto,
        mapea a la paleta de 16 colores, agrega el contorno y escribe carpeta/pixellab/out/.

Arriba zoom y herido de 240x160. Abajo escena 100x112, estado 80x144, mini 32x32, espejo 100x112 (panel B,
mirando a la izquierda) y combate 80x56 (cuerpo entero de unos 33 px por estatura, mirando a la izquierda).
Cada recuadro tiene un marco negro de 1 px (a escala final) por fuera y 5 px de fondo entre recuadros.
El marco no es parte de la pieza, se descarta al cortar."""
import sys, os, json, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

BG, OSCURO, BLANCO, NEGRO = (169, 203, 166), (40, 40, 40), (248, 248, 248), (0, 0, 0)
S = 4  # escala de la hoja fuente respecto de la salida
W, H = 504, 328
# recuadros a escala final (x, y, w, h), dentro del lienzo de 504x328
CAJAS = {
    'zoom':   (6, 6, 240, 160),
    'herido': (258, 6, 240, 160),
    'escena': (6, 178, 100, 112),
    'estado': (118, 178, 80, 144),
    'mini':   (210, 178, 32, 32),
    'espejo': (254, 178, 100, 112),
    'combate': (366, 178, 80, 56),
}

def fondo_exacto(im):
    """lo que se parece al fondo de la hoja y toca el borde pasa a BG exacto"""
    a = np.asarray(im.convert('RGB')).astype(int)
    ref = np.median(np.stack([a[0, 0], a[0, -1], a[-1, 0], a[-1, -1]]), 0)
    lab, _ = ndimage.label(np.abs(a - ref).sum(2) < 45)
    borde = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    fig = ~np.isin(lab, list(borde))
    b = a.copy(); b[~fig] = BG
    return Image.fromarray(b.astype(np.uint8)), fig

def armar(D):
    cfg = json.load(open(f'{D}/config.json')); pid = cfg['id']
    os.makedirs(f'{D}/pixellab', exist_ok=True)
    lienzo = Image.new('RGB', (W * S, H * S), BG); d = ImageDraw.Draw(lienzo)
    for k, (x, y, w, h) in CAJAS.items():
        f = f'{D}/out/{pid}_{k}_fuente.png'
        if not os.path.exists(f): print('AVISO. falta', f); continue
        src = Image.open(f).convert('RGB')
        if k in ('zoom', 'herido'): src, _ = fondo_exacto(src)
        lienzo.paste(src.resize((w * S, h * S), Image.LANCZOS), (x * S, y * S))
        # marco negro de 1 px final (4 px fuente) por fuera del recuadro
        d.rectangle([x * S - S, y * S - S, (x + w) * S + S - 1, (y + h) * S + S - 1], outline=NEGRO, width=S)
    lienzo.save(f'{D}/pixellab/{pid}_hoja_pixellab_{W * S}x{H * S}.png')
    # paleta: los 16 colores de procesar.py en una tira, para Color palette de PixelLab
    pal = [tuple(map(int, l.split())) for l in open(f'{D}/out/{pid}.pal').read().split('\n')[3:] if l.strip()]
    tira = Image.new('RGB', (16 * 8, 8))
    for i, c in enumerate(pal): tira.paste(c, (i * 8, 0, i * 8 + 8, 8))
    tira.save(f'{D}/pixellab/{pid}_paleta_pixellab.png')
    print('listo', f'{D}/pixellab/{pid}_hoja_pixellab_{W * S}x{H * S}.png', 'y', f'{pid}_paleta_pixellab.png')

def cortar(D, salida):
    cfg = json.load(open(f'{D}/config.json')); pid = cfg['id']
    out = f'{D}/pixellab/out'; os.makedirs(out, exist_ok=True)
    im = Image.open(salida).convert('RGB')
    if im.size != (W, H):
        if abs(im.width / im.height - W / H) > 0.01: sys.exit(f'NO ENTREGAR. La salida mide {im.size}, se esperaba {W}x{H}')
        im = im.resize((W, H), Image.NEAREST)
    pal = [tuple(map(int, l.split())) for l in open(f'{D}/out/{pid}.pal').read().split('\n')[3:] if l.strip()]
    from skimage.color import rgb2lab
    palab = rgb2lab(np.array(pal[1:]).reshape(-1, 1, 3) / 255.0).reshape(-1, 3)
    flat = [v for c in pal for v in c] + [0] * (768 - 48)
    errores = []
    def indexar(arr, fig):
        alab = rgb2lab(arr.astype(np.uint8) / 255.0).reshape(-1, 3)
        dd = (((alab[:, None, :] - palab[None]) * np.array([1.0, 1.4, 1.4])) ** 2).sum(2)
        idx = (dd.argmin(1) + 1).reshape(arr.shape[:2]).astype(np.uint8); idx[~fig] = 0
        return idx
    def guardar(idx, nom):
        o = Image.fromarray(np.ascontiguousarray(idx), 'P'); o.putpalette(flat); o.save(f'{out}/{pid}_{nom}.png')
    cruz = ndimage.generate_binary_structure(2, 1)
    for k, (x, y, w, h) in CAJAS.items():
        if not os.path.exists(f'{D}/out/{pid}_{k}_fuente.png'): continue
        pieza, fig = fondo_exacto(im.crop((x, y, x + w, y + h)))
        idx = indexar(np.asarray(pieza).astype(int), fig)
        if k in ('escena', 'espejo'):
            if fig[:3].any(): errores.append(f'{k}: la cabeza toca el borde de arriba')
            if not fig[-1].any(): errores.append(f'{k}: el busto no llega al borde de abajo')
            L = np.zeros((112, 104), np.uint8); M = np.zeros((112, 104), bool)
            L[:, 2:102] = idx; M[:, 2:102] = fig
            d1 = ndimage.binary_dilation(M, cruz, 1); d3 = ndimage.binary_dilation(M, cruz, 3)
            L[d3 & ~d1] = 15; L[d1 & ~M] = 1
            guardar(L, f'{k}_104x112')
        elif k == 'estado':
            if fig[:3].any() or fig[:, 0].any() or fig[:, -1].any() or fig[-1].any(): errores.append('estado: la figura toca un borde')
            E = np.zeros((152, 88), np.uint8); E[4:148, 8:88] = idx
            guardar(E, 'estado_88x152')
        elif k == 'combate':
            if fig[:, 0].any() or fig[:, -1].any() or fig[:2].any(): errores.append('combate: la figura toca un borde')
            guardar(idx, 'combate_80x56')
        else:
            guardar(idx, f'{k}_{w}x{h}')
    with open(f'{out}/{pid}.pal', 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n16\n' + ''.join(f'{r} {g} {b}\n' for r, g, b in pal))
    if errores: print('NO ENTREGAR. ' + ' | '.join(errores)); sys.exit(1)
    print('OK, piezas en', out)

if __name__ == '__main__':
    if sys.argv[1] == 'armar': armar(sys.argv[2])
    elif sys.argv[1] == 'cortar': cortar(sys.argv[2], sys.argv[3])
