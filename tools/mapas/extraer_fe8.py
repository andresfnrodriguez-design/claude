#!/usr/bin/env python3
"""Extrae de la decompilación fireemblem8u los datos reales que usa el Taller de Mapas.

Genera datos_fe8.js con
- los 65 terrenos de FE8 (enum de include/constants/terrains.h),
- los costos de movimiento de cada tabla, con clima normal (src/data_terrains.c),
- las clases con su movimiento base y su tabla (src/data_classes.c),
- el terreno de cada mapa de capítulo, casilla por casilla.

Uso: python3 extraer_fe8.py RUTA_A_FIREEMBLEM8U [salida.js]

Cómo se resuelve el terreno de una casilla. El valor del .mar dividido por 8 es el valor del mapa
(scripts/mar_to_map.py). Ese valor dividido por 4 es el índice del metatile, y el terreno sale de la tabla
de terreno del tileset del capítulo, en el byte 0x2000 de TileConfigurationN.bin (src/bmmap.c).
"""
import json
import os
import re
import struct
import sys

RAIZ = sys.argv[1] if len(sys.argv) > 1 else "fireemblem8u"
SALIDA = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos_fe8.js")


def leer(ruta):
    with open(os.path.join(RAIZ, ruta), encoding="utf-8") as f:
        return f.read()


# Terrenos
terrenos = {}
for nombre, valor in re.findall(r"TERRAIN_(\w+)\s*=\s*(0x[0-9A-Fa-f]+)", leer("include/constants/terrains.h")):
    if nombre != "COUNT":
        terrenos[int(valor, 16)] = nombre
N_TER = max(terrenos) + 1

# Tablas de costo (solo clima normal y la del Rey Demonio)
fuente = leer("src/data_terrains.c")
tablas = {}
for nombre, cuerpo in re.findall(r"CONST_DATA s8 TerrainTable_MovCost_(\w+)\[\] = \{(.*?)\};", fuente, re.S):
    if nombre.endswith("Rain") or nombre.endswith("Snow"):
        continue
    costos = [-1] * N_TER
    for ter, v in re.findall(r"\[TERRAIN_(\w+)\]\s*=\s*(-?\d+)", cuerpo):
        ids = [i for i, n in terrenos.items() if n == ter]
        if ids:
            costos[ids[0]] = int(v)
    tablas[nombre.replace("Normal", "")] = costos

# Clases
clases = []
for nombre, cuerpo in re.findall(r"\[CLASS_(\w+) - 1\] = \{(.*?)\n    \},", leer("src/data_classes.c"), re.S):
    mov = re.search(r"\.baseMov = (\d+)", cuerpo)
    tabla = re.search(r"pMovCostTable = \{\s*TerrainTable_MovCost_(\w+)", cuerpo)
    if mov and tabla and int(mov.group(1)) > 0:
        clases.append({"clase": nombre, "mov": int(mov.group(1)), "tabla": tabla.group(1).replace("Normal", "")})

# Tabla de assets de capítulo: índice -> símbolo
assets = [l.split(".word")[1].strip() for l in leer("data/data_8B363C.s").splitlines() if ".word" in l]

# Capítulos jugables. Ruta, número visible y nombre en inglés.
CAPS = {
    "L00": ("Prólogo", "común", "The Fall of Renais"), "L01": ("1", "común", "Escape!"),
    "L02": ("2", "común", "The Protected"), "L03": ("3", "común", "The Bandits of Borgo"),
    "L04": ("4", "común", "Ancient Horrors"), "L05": ("5", "común", "The Empire's Reach"),
    "I05": ("5x", "común", "Unbroken Heart"), "L06": ("6", "común", "Victims of War"),
    "L07": ("7", "común", "Waterside Renvall"), "L08": ("8", "común", "It's a Trap!"),
    "E09": ("9", "Eirika", "Distant Blade"), "E10": ("10", "Eirika", "Revolt at Carcino"),
    "E10x": ("11", "Eirika", "Creeping Darkness"), "E11": ("12", "Eirika", "Village of Silence"),
    "E12": ("13", "Eirika", "Hamill Canyon"), "E13": ("14", "Eirika", "Queen of White Dunes"),
    "I09": ("9", "Ephraim", "Fort Rigwald"), "I10": ("10", "Ephraim", "Turning Traitor"),
    "I10x": ("11", "Ephraim", "Phantom Ship"), "I11": ("12", "Ephraim", "Landing at Taizel"),
    "I12": ("13", "Ephraim", "Fluorspar's Oath"), "I13": ("14", "Ephraim", "Father and Son"),
    "E14": ("15", "común", "Scorched Sand"), "E15": ("16", "común", "Ruled by Madness"),
    "E16": ("17", "común", "River of Regrets"), "E17": ("18", "común", "Two Faces of Evil"),
    "E18": ("19", "común", "Last Hope"), "E19": ("20", "común", "Darkling Woods"),
    "E20": ("Final", "común", "Sacred Stone"), "E20B": ("Final 2", "común", "Sacred Stone (parte 2)"),
    "H00": ("Postgame", "postgame", "Melkaen Coast"),
}
for i in range(1, 9):
    CAPS["T%02d" % i] = ("Valni %d" % i, "postgame", "Tower of Valni, piso %d" % i)
for i in range(1, 11):
    CAPS["R%02d" % i] = ("Lagdou %d" % i, "postgame", "Lagdou Ruins, piso %d" % i)

configs = {}
def config(nombre):
    if nombre not in configs:
        with open(os.path.join(RAIZ, "graphics/map", nombre + ".bin"), "rb") as f:
            configs[nombre] = f.read()[0x2000:0x2400]
    return configs[nombre]

mapas = []
for c in json.loads(leer("src/data/chapter_settings.json"))["chapters"]:
    interno = c.get("internalName")
    if interno not in CAPS:
        continue
    capa = assets[c["map"]["mainLayerId"]]
    conf = assets[c["map"]["tileConfigId"]]
    base = os.path.join(RAIZ, "graphics/map/layout", capa)
    info = json.load(open(base + ".json"))
    datos = open(base + ".mar", "rb").read()
    valores = struct.unpack("<%dH" % (len(datos) // 2), datos)
    lookup = config(conf)
    w, h = info["width"], info["height"]
    grilla = [[lookup[valores[y * w + x] >> 5] for x in range(w)] for y in range(h)]
    cap, ruta, nombre = CAPS[interno]
    mapas.append({"interno": interno, "cap": cap, "ruta": ruta, "nombre": nombre, "capa": capa, "tileset": conf,
                  "niebla": c.get("initialFogLevel", 0), "w": w, "h": h, "ids": grilla})

datos = {"fuente": "fireemblem8u", "terrenos": [terrenos.get(i, "UNUSED_%02X" % i) for i in range(N_TER)],
         "tablas": tablas, "clases": clases, "mapas": mapas}
with open(SALIDA, "w", encoding="utf-8") as f:
    f.write("// Generado por extraer_fe8.py desde la decompilación fireemblem8u. No editar a mano.\n")
    f.write("window.FE8 = " + json.dumps(datos, ensure_ascii=False, separators=(",", ":")) + ";\n")
print(f"{len(mapas)} mapas, {len(clases)} clases, {len(tablas)} tablas de costo -> {SALIDA}")
