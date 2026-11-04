"""Propuesta de paleta oficial 'Fisuras de Elyria' (aetherpunk + Grecia antigua).
16 colores = exactamente una paleta de la GBA (BGR555). El indice 0 es el transparente.
Tambien define los TEMAS de UI (rampas de oscuro a claro) para recolorear la pantalla."""
PALETA = [  # nombre, RGB, significado
    ("transparente",     (0, 0, 0),       "indice 0 de la GBA"),
    ("obsidiana",        (16, 12, 20),    "hollin, sombra, fondo"),
    ("granate profundo", (72, 16, 32),    "Elyria / Kairon, sombra"),
    ("granate",          (144, 32, 56),   "Elyria / Kairon"),
    ("terracota",        (200, 96, 56),   "ceramica griega de figuras rojas"),
    ("marmol",           (240, 228, 200), "marfil de Elyria, columnas"),
    ("bronce oscuro",    (96, 64, 32),    "maquinaria vieja"),
    ("bronce",           (176, 128, 64),  "engranajes, armaduras"),
    ("oro",              (232, 192, 96),  "motivos geometricos, Orden del Cenit"),
    ("egeo profundo",    (24, 40, 88),    "mar, noche, Kaldholt"),
    ("egeo",             (48, 96, 168),   "cielo, agua"),
    ("verdin",           (72, 152, 128),  "cobre oxidado, Ferannor"),
    ("aether",           (88, 216, 224),  "energia de las fisuras"),
    ("aether brillo",    (192, 248, 240), "nucleo de aether, destellos"),
    ("violeta erebos",   (96, 40, 128),   "la amenaza del otro lado"),
    ("blanco",           (248, 248, 248), "texto (fijo)"),
]
C = {n: rgb for n, rgb, _ in PALETA}
# Temas: rampa de 5 tonos de oscuro a claro (solo colores de la paleta)
TEMAS = {
    "granate": None,  # el actual, sin recolorear
    "egeo_aether": [C["obsidiana"], C["egeo profundo"], C["egeo"], C["aether"], C["aether brillo"]],
    "bronce": [C["obsidiana"], C["bronce oscuro"], C["bronce"], C["oro"], C["marmol"]],
    "erebos": [C["obsidiana"], C["granate profundo"], C["violeta erebos"], C["egeo"], C["aether brillo"]],
    "ferannor": [C["obsidiana"], C["egeo profundo"], C["verdin"], C["aether"], C["marmol"]],
    "terracota": [C["obsidiana"], C["granate profundo"], C["terracota"], C["oro"], C["marmol"]],
    "cassaria": [C["obsidiana"], C["granate"], C["terracota"], C["oro"], C["aether brillo"]],
    "kaldholt": [C["obsidiana"], C["granate profundo"], C["egeo profundo"], C["egeo"], C["marmol"]],
    "cenit": [C["obsidiana"], C["bronce oscuro"], C["oro"], C["marmol"], C["blanco"]],
    "verdin_bronce": [C["obsidiana"], C["bronce oscuro"], C["verdin"], C["bronce"], C["oro"]],
    "fisura": [C["obsidiana"], C["violeta erebos"], C["egeo"], C["aether"], C["aether brillo"]],
    "hierro": [C["obsidiana"], C["egeo profundo"], C["bronce oscuro"], C["verdin"], C["marmol"]],
}
if __name__ == "__main__":
    from PIL import Image, ImageDraw
    sw = Image.new("RGB", (16 * 24, 24)); d = ImageDraw.Draw(sw)
    for i, (n, rgb, s) in enumerate(PALETA):
        d.rectangle([i * 24 + 1, 1, i * 24 + 22, 22], fill=rgb)
        r, g, b = rgb; print(f"{i:2} 0x{(b>>3)<<10|(g>>3)<<5|(r>>3):04X}  {n:17} {s}")
    sw.resize((sw.width * 2, sw.height * 2), Image.NEAREST).save("paleta_oficial.png")
