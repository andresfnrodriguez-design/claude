#!/usr/bin/env python3
"""Aplica al decomp la paleta copiada del editor "Paleta del mapa".

Uso
  python3 aplicar_paleta_mapa.py paleta.txt RUTA_DECOMP [MapPaletteN.pal]

paleta.txt es lo que da el botón "Copiar paleta" (líneas "#original -> #nuevo").
Por defecto escribe graphics/map/MapPalette1.pal, que es la del mapa de prueba.
Antes de escribir guarda una copia .bak del archivo original (solo la primera vez).
Solo cambia los colores que aparecen en paleta.txt; el resto queda igual.
"""
import sys, re, shutil, os

txt, decomp = sys.argv[1], sys.argv[2]
nombre = sys.argv[3] if len(sys.argv) > 3 else 'MapPalette1.pal'
ruta = os.path.join(decomp, 'graphics', 'map', nombre)

cambios = {}
for l in open(txt, encoding='utf-8'):
    m = re.search(r'(#[0-9a-fA-F]{6})\s*->\s*(#[0-9a-fA-F]{6})', l)
    if m:
        cambios[m.group(1).lower()] = m.group(2).lower()
if not cambios:
    sys.exit('No encontré líneas "#original -> #nuevo" en ' + txt)

if not os.path.exists(ruta + '.bak'):
    shutil.copy(ruta, ruta + '.bak')

lineas = open(ruta, encoding='utf-8').read().split('\n')
cab, cols = lineas[:3], [l for l in lineas[3:] if l.strip()]
n = 0
for i, l in enumerate(cols):
    h = '#%02x%02x%02x' % tuple(int(v) for v in l.split())
    if h in cambios:
        nuevo = cambios[h]
        # redondeo a 15 bits como la GBA
        r, g, b = (round(int(nuevo[k:k + 2], 16) / 255 * 31) * 255 // 31 for k in (1, 3, 5))
        cols[i] = f'{r} {g} {b}'
        n += 1
open(ruta, 'w', encoding='utf-8', newline='\r\n' if '\r' in open(ruta + '.bak', encoding='utf-8', newline='').read() else '\n').write('\n'.join(cab + cols) + '\n')
print(f'{n} entradas cambiadas en {ruta}. Copia original en {nombre}.bak')
