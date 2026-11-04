#!/usr/bin/env python3
"""Baja las imágenes de los mapas de las guías de fireemblemwod.com y estima su terreno.

Uso: python3 bajar_wod.py JUEGO CARPETA_TRABAJO
JUEGO es el código del índice del sitio (fe7, fe6, ...). Guarda las imágenes en imagenes/JUEGO/ y agrega
o reemplaza las entradas del juego en mapas_estimados.js, junto a este script.
Necesita modelo.npz (ver estimar_mapas.py) en CARPETA_TRABAJO.
"""
import html, json, os, re, subprocess, sys
from PIL import Image
import estimar_mapas as E

SITIO = "https://www.fireemblemwod.com/"
AQUI = os.path.dirname(os.path.abspath(__file__))
JUEGO, TRAB = sys.argv[1], sys.argv[2]
NOMBRE = JUEGO.upper()


def get(url):
    return subprocess.run(["curl", "-sS", "-L", url], capture_output=True).stdout


def texto(url):
    return get(url).decode("utf-8", "ignore")


def limpiar(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()


indice = texto(SITIO + JUEGO + ".htm")
m_c = re.search(r'href="(' + re.escape(JUEGO) + r'/guia[^/"]*/)[^"]+\.htm"', indice)
carpeta_guia = m_c.group(1) if m_c else JUEGO + "/guia" + JUEGO + "/"
pags = list(dict.fromkeys(re.findall(r'href="' + re.escape(carpeta_guia) + r'([^"]+\.htm)"', indice)))
os.makedirs(os.path.join(AQUI, "imagenes", JUEGO), exist_ok=True)

mapas, vistos = [], set()
for p in pags:
    t = texto(SITIO + carpeta_guia + p)
    m = re.search(r'<img src="[^"]*s\.png"[^>]*?width="(\d+)" height="(\d+)"[^>]*>\s*(?:</div>)?\s*<img src="([^"]+)"', t)
    h1 = re.search(r"<h1>(.*?)</h1>", t, re.S)
    if not m or not h1:
        print("sin mapa:", p)
        continue
    titulo = limpiar(h1.group(1))
    cap, _, nombre = titulo.partition(":")
    nombre = nombre.strip() or titulo
    clave = re.sub(r'\W', '', nombre.lower())
    if clave in vistos:  # el mismo mapa en otro modo de juego
        continue
    vistos.add(clave)
    W, H = int(m.group(1)), int(m.group(2))
    w, h = round(W / 16), round(H / 16)
    url = SITIO + carpeta_guia + m.group(3)
    nombre_img = re.sub(r"[^\w.-]", "_", p.replace(".htm", "")) + os.path.splitext(m.group(3))[1]
    ruta_img = os.path.join(AQUI, "imagenes", JUEGO, nombre_img)
    open(ruta_img, "wb").write(get(url))
    try:
        Image.open(ruta_img).verify()
    except Exception:
        print("imagen inválida:", p)
        continue
    ids = E.estimar(os.path.join(TRAB, "modelo.npz"), ruta_img, w, h)
    cap = cap.replace("Cap.", "").replace("Capítulo", "").strip() or titulo
    mapas.append({"juego": NOMBRE, "cap": cap, "nombre": nombre, "ruta": "estimado", "fuente": SITIO + carpeta_guia + p, "imagen": "imagenes/" + JUEGO + "/" + nombre_img,
                  "w": w, "h": h, "ids": ids})
    print(f"{cap} | {nombre} | {w}x{h}")

destino = os.path.join(AQUI, "mapas_estimados.js")
previos = []
if os.path.exists(destino):
    previos = json.loads(re.search(r"window\.MAPAS_EST = (.*);\s*$", open(destino, encoding="utf-8").read(), re.S).group(1))
todos = [m for m in previos if m["juego"] != NOMBRE] + mapas
with open(destino, "w", encoding="utf-8") as f:
    f.write("// Mapas estimados desde imágenes de fireemblemwod.com con estimar_mapas.py. Son aproximados.\n")
    f.write("window.MAPAS_EST = " + json.dumps(todos, ensure_ascii=False, separators=(",", ":")) + ";\n")
print(len(mapas), "mapas de", NOMBRE, "->", destino)
