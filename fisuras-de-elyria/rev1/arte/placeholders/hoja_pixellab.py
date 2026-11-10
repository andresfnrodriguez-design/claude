#!/usr/bin/env python3
"""Hojas para PixelLab con los encuadres marcados, y el corte de vuelta.
PixelLab entrega como máximo 288x184, así que son 3 hojas por personaje, todas con Output Scale ÷4.

Armar:  python3 hoja_pixellab.py armar carpeta_personaje
        carpeta/pixellab/{id}_cuerpo_1152x736_sale_288x184.png   escena, espejo, estado, mini y combate
        carpeta/pixellab/{id}_zoom_968x648_sale_242x162.png      zoom
        carpeta/pixellab/{id}_herido_968x648_sale_242x162.png    herido
        carpeta/pixellab/{id}_paleta_pixellab.png                para Color palette, Max colours 16

Cortar: python3 hoja_pixellab.py cortar carpeta_personaje salida_cuerpo.png salida_zoom.png salida_herido.png
        (en ese orden, o con cuerpo/zoom/herido en el nombre del archivo)

Cada recuadro tiene un marco negro de 1 px (a escala final) por fuera, que se descarta al cortar."""
import sys, os, json, numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

BG, OSCURO, BLANCO, NEGRO = (169, 203, 166), (40, 40, 40), (248, 248, 248), (0, 0, 0)
S = 4  # escala de la hoja fuente respecto de la salida
# PixelLab entrega como máximo 288x184, así que van 3 hojas. Recuadros a escala final (x, y, w, h)
# con marco negro de 1 px por fuera y 1 px de separación
HOJAS = {
    'todo':   ((290, 258), {
        'zoom':    (1, 1, 120, 80),
        'herido':  (124, 1, 120, 80),
        'escena':  (1, 85, 100, 112),
        'espejo':  (104, 85, 100, 112),
        'estado':  (207, 85, 80, 144),
        'mini':    (35, 200, 32, 32),
        'combate': (104, 200, 80, 56),
    }),
    'cuerpo': ((288, 184), {
        'escena':  (1, 1, 100, 112),
        'espejo':  (104, 1, 100, 112),
        'estado':  (207, 1, 80, 144),
        'mini':    (35, 116, 32, 32),   # centrado bajo la escena
        'combate': (104, 116, 80, 56),
    }),
    'caras':  ((245, 82), {'zoom': (1, 1, 120, 80), 'herido': (124, 1, 120, 80)}),
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
    if not os.path.exists(f'{D}/out/{pid}_espejo_fuente.png'): print('AVISO. falta el espejo real (panel B), su recuadro queda vacío. No se voltea la escena')
    for hoja, ((W, H), cajas) in HOJAS.items():
        lienzo = Image.new('RGB', (W * S, H * S), BG); d = ImageDraw.Draw(lienzo)
        for k, (x, y, w, h) in cajas.items():
            f = f'{D}/out/{pid}_{k}_fuente.png'
            if not os.path.exists(f): print('AVISO. falta', f, '(el recuadro queda vacío)')
            else:
                src = Image.open(f).convert('RGB')
                if k in ('zoom', 'herido'): src, _ = fondo_exacto(src)
                lienzo.paste(src.resize((w * S, h * S), Image.LANCZOS), (x * S, y * S))
            d.rectangle([x * S - S, y * S - S, (x + w) * S + S - 1, (y + h) * S + S - 1], outline=NEGRO, width=S)
        lienzo.save(f'{D}/pixellab/{pid}_{hoja}_{W * S}x{H * S}_sale_{W}x{H}.png')
    pal = [tuple(map(int, l.split())) for l in open(f'{D}/out/{pid}.pal').read().split('\n')[3:] if l.strip()]
    tira = Image.new('RGB', (16 * 8, 8))
    for i, c in enumerate(pal): tira.paste(c, (i * 8, 0, i * 8 + 8, 8))
    tira.save(f'{D}/pixellab/{pid}_paleta_pixellab.png')
    print('listo, 3 hojas y la paleta en', f'{D}/pixellab/')

def cortar(D, *salidas):
    cfg = json.load(open(f'{D}/config.json')); pid = cfg['id']
    out = f'{D}/pixellab/out'; os.makedirs(out, exist_ok=True)
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
    trabajos = []
    for i, salida in enumerate(salidas):
        im = Image.open(salida).convert('RGB')
        nombre = os.path.basename(salida)
        hoja = next((h for h in HOJAS if h in nombre), None)
        if hoja is None and abs(im.width / im.height - 290 / 258) < 0.02: hoja = 'todo'
        if hoja is None:   # por tamaño: 288x184 es cuerpo, 242x162 es zoom o herido según el orden
            hoja = 'cuerpo' if abs(im.width / im.height - 288 / 184) < 0.02 else 'caras'
        (W, H), cajas = HOJAS[hoja]
        if im.size != (W, H):
            if abs(im.width / im.height - W / H) > 0.02: sys.exit(f'NO ENTREGAR. {nombre} mide {im.size}, se esperaba {W}x{H}')
            im = im.resize((W, H), Image.NEAREST)
        trabajos.append((hoja, im, cajas))
    for hoja, im, cajas in trabajos:
      for k, (x, y, w, h) in cajas.items():
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
    elif sys.argv[1] == 'cortar': cortar(sys.argv[2], *sys.argv[3:])
