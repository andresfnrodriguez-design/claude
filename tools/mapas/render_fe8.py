#!/usr/bin/env python3
"""Dibuja los mapas de FE8 con sus gráficos reales a partir de la decomp fireemblem8u.

Sirve para dos cosas. Ver los mapas extraídos tal como se ven en el juego, y armar el set de casillas de ejemplo
(imagen de 16x16 + terreno exacto) que usa estimar_mapas.py para estimar mapas de otros juegos desde imágenes.

Uso: python3 render_fe8.py RUTA_A_FIREEMBLEM8U CARPETA_SALIDA
Salida: un PNG por capítulo y ejemplos_fe8.npz con las casillas y su terreno.
"""
import json, os, struct, sys
import numpy as np
from PIL import Image

RAIZ, SAL = sys.argv[1], sys.argv[2]
os.makedirs(SAL, exist_ok=True)
G = os.path.join(RAIZ, "graphics/map")
assets = [l.split(".word")[1].strip() for l in open(os.path.join(RAIZ, "data/data_8B363C.s")) if ".word" in l]


def paleta(nombre):
    l = open(os.path.join(G, nombre + ".pal")).read().split("\n")
    n = int(l[2])
    return np.array([[int(v) for v in l[3 + i].split()] for i in range(n)], dtype=np.uint8)


def tiles(nombre):
    im = np.array(Image.open(os.path.join(G, nombre + ".png"))) // 17
    t = im.reshape(im.shape[0] // 8, 8, im.shape[1] // 8, 8).transpose(0, 2, 1, 3).reshape(-1, 8, 8)
    return t


def render(ch):
    m = ch["map"]
    conf = open(os.path.join(G, assets[m["tileConfigId"]] + ".bin"), "rb").read()
    meta = struct.unpack("<4096H", conf[:0x2000])
    terr = conf[0x2000:0x2400]
    pal = paleta(assets[m["paletteId"]].replace("Palette", "Palette") if os.path.exists(os.path.join(G, assets[m["paletteId"]] + ".pal")) else assets[m["paletteId"]])
    t = tiles(assets[m["obj1Id"]])
    if m.get("obj2Id"):
        t = np.concatenate([t, tiles(assets[m["obj2Id"]])])
    capa = assets[m["mainLayerId"]]
    base = os.path.join(G, "layout", capa)
    info = json.load(open(base + ".json"))
    w, h = info["width"], info["height"]
    d = open(base + ".mar", "rb").read()
    vals = struct.unpack("<%dH" % (len(d) // 2), d)
    img = np.zeros((h * 16, w * 16, 3), dtype=np.uint8)
    ter = np.zeros((h, w), dtype=np.uint8)
    for y in range(h):
        for x in range(w):
            idx = vals[y * w + x] >> 5
            ter[y, x] = terr[idx]
            for k in range(4):
                e = meta[idx * 4 + k]
                ti, hf, vf, pi = e & 0x3FF, (e >> 10) & 1, (e >> 11) & 1, e >> 12
                px = t[ti] if ti < len(t) else np.zeros((8, 8), dtype=np.uint8)
                if hf: px = px[:, ::-1]
                if vf: px = px[::-1, :]
                colores = pal[((pi % 10) * 16 + px) % len(pal)]
                oy, ox = y * 16 + (k // 2) * 8, x * 16 + (k % 2) * 8
                img[oy:oy + 8, ox:ox + 8] = colores
    return capa, img, ter


if __name__ == "__main__":
    caps = json.load(open(os.path.join(RAIZ, "src/data/chapter_settings.json")))["chapters"]
    X, Y, hechos = [], [], set()
    for ch in caps:
        n = ch.get("internalName")
        if not n or n.startswith("D") or n == "C00":
            continue
        capa, img, ter = render(ch)
        if capa in hechos:
            continue
        hechos.add(capa)
        Image.fromarray(img).save(os.path.join(SAL, capa + ".png"))
        h, w = ter.shape
        for y in range(h):
            for x in range(w):
                X.append(img[y * 16:(y + 1) * 16, x * 16:(x + 1) * 16])
                Y.append(ter[y, x])
    np.savez_compressed(os.path.join(SAL, "ejemplos_fe8.npz"), X=np.array(X), Y=np.array(Y))
    print(len(hechos), "mapas,", len(X), "casillas de ejemplo")
