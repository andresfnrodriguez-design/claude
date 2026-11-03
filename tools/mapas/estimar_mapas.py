#!/usr/bin/env python3
"""Estima el terreno de mapas de Fire Emblem a partir de sus imágenes.

Cómo funciona. Se entrena con capturas de mapas de FE8 cuyo terreno exacto ya se conoce (datos_fe8.js, sacado de
la decomp). Cada casilla de 16x16 se resume en sus colores, y cada casilla de un mapa nuevo recibe el terreno de las
casillas de FE8 que más se le parecen (vecinos más cercanos). Funciona mejor con juegos de GBA, que comparten estilo.
Las casillas tapadas por unidades salen mal y hay que corregirlas a mano.

Uso:
  python3 estimar_mapas.py entrenar PARES.json modelo.npz
  python3 estimar_mapas.py estimar modelo.npz imagen.png ANCHO ALTO
PARES.json es una lista de {"img": ruta, "interno": código de capítulo de FE8}.
"""
import json, os, re, sys
import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))


def cargar_fe8():
    t = open(os.path.join(AQUI, "datos_fe8.js"), encoding="utf-8").read()
    return json.loads(re.search(r"window\.FE8 = (.*);\s*$", t, re.S).group(1))


def casillas(ruta, w, h):
    im = Image.open(ruta).convert("RGB").resize((w * 16, h * 16), Image.BILINEAR)
    a = np.asarray(im, dtype=np.float32) / 255.0
    return a.reshape(h, 16, w, 16, 3).transpose(0, 2, 1, 3, 4)


def rasgos(c):
    """c: (..., 16, 16, 3) -> vector de rasgos."""
    s = c.shape[:-3]
    p = c.reshape(*s, 4, 4, 4, 4, 3).mean(axis=(-4, -2))          # colores en grilla 4x4
    hsv_v = c.max(axis=-1)
    extra = np.stack([c.std(axis=(-3, -2)).mean(-1), hsv_v.mean(axis=(-2, -1)),
                      (c[..., 2] - c[..., 0]).mean(axis=(-2, -1)), (c[..., 1] - c[..., 0]).mean(axis=(-2, -1))], -1)
    return np.concatenate([p.reshape(*s, -1), extra * 2.0], -1)


def entrenar(pares, salida):
    fe8 = {m["interno"]: m for m in cargar_fe8()["mapas"]}
    X, Y, G = [], [], []
    for i, p in enumerate(pares):
        m = fe8[p["interno"]]
        c = casillas(p["img"], m["w"], m["h"])
        X.append(rasgos(c).reshape(-1, rasgos(c).shape[-1]))
        Y.append(np.array(m["ids"]).reshape(-1))
        G.append(np.full(m["w"] * m["h"], i))
    np.savez_compressed(salida, X=np.concatenate(X), Y=np.concatenate(Y), G=np.concatenate(G))


def predecir(X, Y, q, k=5):
    out = np.empty(len(q), dtype=np.int64)
    for i in range(0, len(q), 256):
        d = ((q[i:i + 256, None, :] - X[None, :, :]) ** 2).sum(-1)
        nn = np.argpartition(d, k, axis=1)[:, :k]
        for j, fila in enumerate(nn):
            votos = {}
            for n in fila:
                votos[Y[n]] = votos.get(Y[n], 0) + 1.0 / (1e-3 + d[j, n])
            out[i + j] = max(votos, key=votos.get)
    return out


def estimar(modelo, img, w, h):
    M = np.load(modelo)
    q = rasgos(casillas(img, w, h)).reshape(w * h, -1)
    return predecir(M["X"], M["Y"], q).reshape(h, w).tolist()


if __name__ == "__main__":
    if sys.argv[1] == "entrenar":
        entrenar(json.load(open(sys.argv[2])), sys.argv[3])
    elif sys.argv[1] == "estimar":
        print(json.dumps(estimar(sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]))))
