#!/usr/bin/env python3
"""
debug_mapa.py — Fisuras de Elyria
Instala el mapa debug (prólogo 3H + banco de prueba de los 64 terrenos FE8)
en el capítulo 0 (Prólogo) de la decompilación fireemblem8u.

Uso, desde la raíz del repo (~/fireemblem8u):
    python3 debug_mapa.py            # instala
    python3 debug_mapa.py --revertir # restaura los originales

Qué toca:
  graphics/map/TileConfiguration9.bin   solo casillas que ningún mapa original usa
  graphics/map/layout/PrologueMap.mar / .json
  src/data/chapter_settings.json        capítulo 0, bloque "map"
Cada archivo se respalda una vez como <archivo>.orig
"""
import json, os, re, shutil, sys, glob
from collections import Counter

GRID = """010101010101010101010101010101010101010101010101010101
0102020303040405050606070701080809090A0A0B0B0C0C0D0D01
012E01010101010101010101010101010101010101010101010E01
012E01010101010C0C0C0C0C0C0C0C0C010101010101010C010E01
012D010101010101010C0C0C0C010C1A010101010101010C010F01
012D0101010101010101010C010C01010101010101010C0C010F01
012C010C0101010101010101010C01010101010101010C0C011001
012C010C0C010101010101010101010101010101010C0C0C011001
012B010C0C0C01010101010C0101010101010C010C0C0C0C011101
012B010C0C010101010101010C010101010C010C0C0C0C0C011101
012A010C0C0101010C010101010101010C010C0C0C0C0C0C011201
012A010C0C0101010C0C01010101010C010C0C0C0C0C0C0C011201
0101010C0C01010C0C1A01011A01010101010C0C0C0C0C0C010101
0129010C0C0101010C0C0C010C010C010101010C0C0C0C0C011301
0129010C0C0101010C0C1A0C010101010101010C0C0C0C0C011301
0128010C01010101010C0C0101010101010101010C0C0C0C011401
012801010101010101010101010101010101010101010C0C011401
01270101010101010101010101010101010101010101010C011501
012701151515151515151515010101151515151515151515011501
0126011A1A1A1A1A1A1A1A1A0101011A1A1A1A1A1A1A1A1A011601
0126011A0101010101010101010101010101010101011A01011601
0125011A0101010101010101010101010101010101011A1A011701
0125011A01010101010101010101010101011A1A1A1A1A1A011701
012401010101010101010101010101010101010101010101011801
012423232222212120201F1F1E011E1D1D1C1C1B1B1A1A19191801
010101010101010101010101010101010101010101010101010101
2F2F30303131323233333434353536363737383839393A3A3B3B3C
010101010101010101010101010101010101010101010101010101
3C3D3D3E3E3F3F4040010101010101010101010101010101010101
010101010101010101010101010101010101010101010101010101"""

TC   = "graphics/map/TileConfiguration9.bin"
MAR  = "graphics/map/layout/PrologueMap.mar"
MJS  = "graphics/map/layout/PrologueMap.json"
CHS  = "src/data/chapter_settings.json"
TC_ASSET, OBJ_ASSET, PAL_ASSET, ANIM_ASSET = 110, 108, 109, 5

# Terrenos que no existen en el tileset 9: se les copia el dibujo de un terreno parecido
DONOR = {0x09:0x05, 0x0E:0x02, 0x0F:0x02, 0x14:0x13, 0x16:0x15, 0x18:0x17, 0x1C:0x25,
         0x22:0x1A, 0x23:0x0B, 0x24:0x05, 0x27:0x01, 0x28:0x01, 0x29:0x01, 0x2A:0x17,
         0x2B:0x17, 0x2F:0x01, 0x30:0x08, 0x31:0x26, 0x32:0x19, 0x33:0x13, 0x36:0x15,
         0x37:0x25, 0x38:0x05, 0x39:0x1A, 0x3A:0x12, 0x3B:0x1A, 0x3D:0x19, 0x3E:0x17,
         0x40:0x1D}

def backup(p):
    if not os.path.exists(p + ".orig"):
        shutil.copy2(p, p + ".orig")

def revert():
    for p in (TC, MAR, MJS, CHS):
        if os.path.exists(p + ".orig"):
            shutil.copy2(p + ".orig", p); print("restaurado", p)

def used_metatiles():
    """Metatiles que usan los mapas originales con el tileset 9 (incluye cambios de mapa)."""
    assets = [l.split()[1] for l in open("data/data_8B363C.s") if l.strip().startswith(".word")]
    chs = json.load(open(CHS + ".orig" if os.path.exists(CHS + ".orig") else CHS))["chapters"]
    used = Counter()
    for c in chs:
        m = c["map"]
        if m["tileConfigId"] != TC_ASSET:
            continue
        name = assets[m["mainLayerId"]]
        mar = f"graphics/map/layout/{name}.mar"
        if name == "PrologueMap":
            mar += ".orig" if os.path.exists(mar + ".orig") else ""
        if os.path.exists(mar):
            b = open(mar, "rb").read()
            for i in range(0, len(b), 2):
                used[(b[i] | b[i+1] << 8) >> 5] += 1
        if m["changeLayerId"]:
            for f in glob.glob(f"graphics/map/{assets[m['changeLayerId']]}_change_*.bin"):
                b = open(f, "rb").read()
                for i in range(0, len(b), 2):
                    used[(b[i] | b[i+1] << 8) >> 2] += 1
    return used

def install():
    grid = [[int(r[i:i+2], 16) for i in range(0, len(r), 2)] for r in GRID.strip().split("\n")]
    H, W = len(grid), len(grid[0])
    assert W * H <= 1023, "el mapa supera el búfer de FE8"

    src = open(TC + ".orig" if os.path.exists(TC + ".orig") else TC, "rb").read()
    assert len(src) == 0x2400, "TileConfiguration9.bin con tamaño inesperado"
    gfx, ter = bytearray(src[:0x2000]), bytearray(src[0x2000:])
    used = used_metatiles()

    # 1) un metatile representativo por terreno (el más usado en los mapas originales)
    rep = {}
    for mt, n in used.most_common():
        rep.setdefault(ter[mt], mt)
    for mt in range(1024):
        rep.setdefault(ter[mt], mt)

    # 2) terrenos faltantes en casillas libres, con dibujo prestado
    free = [mt for mt in range(1023, 0, -1) if used[mt] == 0 and mt not in rep.values()]
    for tid in range(1, 0x41):
        if tid in rep:
            continue
        mt = free.pop(0)
        donor = rep[DONOR[tid]]
        gfx[mt*8:mt*8+8] = gfx[donor*8:donor*8+8]
        ter[mt] = tid
        rep[tid] = mt

    # 3) escribir archivos
    for p in (TC, MAR, MJS, CHS):
        backup(p)
    open(TC, "wb").write(bytes(gfx) + bytes(ter))
    mar = bytearray()
    for row in grid:
        for tid in row:
            v = rep[tid] << 5
            mar += bytes((v & 0xFF, v >> 8))
    open(MAR, "wb").write(mar)
    json.dump({"id": "PrologueMap", "width": W, "height": H}, open(MJS, "w"))

    d = json.load(open(CHS, encoding="utf-8"))
    m = d["chapters"][0]["map"]
    m.update(obj1Id=OBJ_ASSET, obj2Id=0, paletteId=PAL_ASSET, tileConfigId=TC_ASSET,
             objAnimId=ANIM_ASSET, paletteAnimId=0, changeLayerId=0)
    json.dump(d, open(CHS, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    open(CHS, "a").write("\n")

    # 4) verificación: el terreno que verá el juego = tabla[metatile]
    bad = [(x, y) for y, row in enumerate(grid) for x, t in enumerate(row) if ter[rep[t]] != t]
    print(f"Mapa {W}x{H} instalado en el capítulo 0. Terrenos: {len(rep)-1 if 0 in rep else len(rep)}. Errores: {len(bad)}")
    print("Ahora: make clean-maps (o make clean) y make")

if __name__ == "__main__":
    if not os.path.exists("data/data_8B363C.s"):
        sys.exit("Correlo desde la raíz de fireemblem8u")
    revert() if "--revertir" in sys.argv else install()
