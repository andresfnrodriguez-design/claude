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
    # inspirados en el contraste carmesi / turquesa sobre pizarra (complementarios)
    "pizarra_turquesa": [(10, 20, 24), (28, 56, 60), (40, 110, 110), (40, 184, 160), (200, 248, 232)],
    "carmesi": [(16, 6, 10), (96, 8, 32), (224, 24, 64), (240, 96, 128), (252, 210, 220)],
    "carmesi_turquesa": [(10, 20, 24), (28, 56, 60), (40, 150, 140), (224, 24, 64), (252, 210, 220)],
    "turquesa_carmesi": [(16, 6, 10), (96, 8, 32), (180, 20, 56), (40, 184, 160), (200, 248, 232)],
    # fondo verde azulado (pizarra/teal) con distintos acentos en los tonos claros
    "teal_oro": [(8, 20, 22), (24, 60, 62), (40, 120, 116), (232, 192, 96), (248, 236, 200)],
    "teal_coral": [(8, 20, 22), (24, 60, 62), (40, 120, 116), (240, 104, 88), (252, 220, 208)],
    "teal_marfil": [(8, 20, 22), (24, 60, 62), (48, 128, 120), (160, 208, 192), (240, 228, 200)],
    "teal_violeta": [(8, 20, 22), (24, 60, 62), (40, 120, 116), (152, 72, 176), (232, 200, 248)],
    "teal_profundo_aether": [(4, 12, 16), (16, 44, 52), (24, 88, 96), (88, 216, 224), (192, 248, 240)],
    "teal_granate": [(8, 20, 22), (24, 60, 62), (40, 120, 116), (144, 32, 56), (240, 160, 176)],
    # grises para usar sobre el fondo "fisuras", con un toque de acento
    "gris": [(12, 12, 16), (44, 44, 52), (96, 96, 108), (160, 160, 172), (232, 232, 236)],
    "gris_rosa": [(12, 12, 16), (44, 44, 52), (96, 96, 108), (240, 112, 176), (248, 216, 232)],
    "gris_morado": [(12, 12, 16), (44, 44, 52), (96, 96, 108), (168, 96, 216), (232, 208, 248)],
    "gris_lima": [(12, 12, 16), (44, 44, 52), (96, 96, 108), (184, 232, 56), (236, 248, 200)],
    "gris_mix": [(12, 12, 16), (44, 44, 52), (96, 96, 108), (160, 160, 172), (232, 232, 236)],
    "gris_carmesi": [(12, 12, 16), (44, 44, 52), (96, 96, 108), (224, 24, 64), (252, 210, 220)],
    "gris_turquesa": [(12, 12, 16), (44, 44, 52), (96, 96, 108), (40, 184, 160), (200, 248, 232)],
    "gris_dual": [(12, 12, 16), (44, 44, 52), (96, 96, 108), (160, 160, 172), (232, 232, 236)],
    "pizarra_carmesi": [(10, 20, 24), (28, 56, 60), (60, 96, 100), (224, 24, 64), (252, 210, 220)],
    "hierro": [C["obsidiana"], C["egeo profundo"], C["bronce oscuro"], C["verdin"], C["marmol"]],
}
if __name__ == "__main__":
    from PIL import Image, ImageDraw
    sw = Image.new("RGB", (16 * 24, 24)); d = ImageDraw.Draw(sw)
    for i, (n, rgb, s) in enumerate(PALETA):
        d.rectangle([i * 24 + 1, 1, i * 24 + 22, 22], fill=rgb)
        r, g, b = rgb; print(f"{i:2} 0x{(b>>3)<<10|(g>>3)<<5|(r>>3):04X}  {n:17} {s}")
    sw.resize((sw.width * 2, sw.height * 2), Image.NEAREST).save("paleta_oficial.png")

# Toques de acento por zona (x0, y0, x1, y1): dentro de cada caja se usa otra rampa.
FUCSIA = [(12, 12, 16), (60, 8, 32), (150, 16, 64), (232, 24, 96), (252, 200, 220)]
MORADO = [(12, 12, 16), (44, 24, 64), (100, 56, 150), (168, 96, 216), (232, 208, 248)]
LIMA   = [(12, 12, 16), (40, 56, 16), (110, 150, 32), (184, 232, 56), (236, 248, 200)]
ZONAS = {
    "gris_mix": [
        ((0, 0, 239, 13), FUCSIA),      # barra del nombre
        ((60, 26, 180, 48), FUCSIA),    # arma equipada
        ((3, 138, 27, 159), LIMA),      # boton seleccionado
        ((192, 138, 238, 159), MORADO), # turno
    ],
}
CARMESI = [(12, 12, 16), (96, 8, 32), (180, 20, 56), (224, 24, 64), (252, 210, 220)]
TURQUESA = [(10, 20, 24), (28, 56, 60), (40, 120, 116), (40, 184, 160), (200, 248, 232)]
ZONAS["gris_dual"] = [((0, 0, 239, 13), TURQUESA), ((60, 26, 180, 48), CARMESI)]
TEMAS["gris_final"] = TEMAS["gris"]
ZONAS["gris_final"] = [((60, 26, 180, 48), CARMESI)]  # solo el arma equipada en carmesi
# sin contorno rosa: el tono mas claro del recuadro queda igual al carmesi
ZONAS["gris_final"] = [((60, 26, 180, 48), [(12, 12, 16), (96, 8, 32), (150, 16, 48), (150, 16, 48), (150, 16, 48)])]

# color de las etiquetas (HP, ATK, LV, EXP...) y del texto del arma, por tema (si no, quedan las originales)
COLOR_ETIQUETAS = {"gris_final": (184, 184, 192)}   # gris neutro
NARANJA = [(12, 12, 16), (88, 30, 10), (168, 64, 24), (216, 88, 48), (216, 88, 48)]
ZONAS["gris_final"] = [((60, 26, 180, 48), NARANJA)]  # arma equipada en naranja brasa, sin contorno claro
