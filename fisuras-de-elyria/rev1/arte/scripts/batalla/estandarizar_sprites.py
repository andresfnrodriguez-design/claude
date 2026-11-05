"""
Estandarizador de sprites de batalla GBA — Fisuras de Elyria
================================================================
Toma una carpeta de frames PNG (por ejemplo, extraídos de un GIF de
PixelLab/Nano Banana) y les aplica el estándar técnico del proyecto:

  1. Espejado horizontal (para generar la versión "mirando a la izquierda"
     a partir de la versión "mirando a la derecha", o viceversa)
  2. Reemplazo del fondo chroma-key verde puro (#00FF00) por el verde
     establecido del proyecto (#A9CBA6)
  3. Unificación de todos los negros/contornos oscuros en un solo color
     de contorno (#282828), en vez de dejar varios negros ligeramente
     distintos como suelen salir de los generadores de IA
  4. Reducción a un máximo de 16 colores totales (fondo y contorno incluidos)
  5. Recorte al lienzo completo de 248x160, con el personaje centrado
     horizontalmente en x=140 y los pies apoyados en y=102

Requiere: pip install pillow numpy

Uso:
    python estandarizar_sprites.py carpeta_entrada/ carpeta_salida/

    O importalo y llamá a procesar_carpeta() / procesar_frame() directo
    desde otro script si preferís integrarlo a un pipeline más grande.
"""

from PIL import Image
import numpy as np
import os
import sys

# ---------------------------------------------------------------
# PARÁMETROS DEL ESTÁNDAR — ajustar acá si el proyecto cambia de reglas
# ---------------------------------------------------------------
GREEN_BG = (0xA9, 0xCB, 0xA6)       # #A9CBA6 — verde de fondo del proyecto
CHROMA_GREEN_TOLERANCE = 20         # qué tan estricto detectar el verde puro original
OUTLINE_TARGET = (0x28, 0x28, 0x28)  # #282828 — color de contorno único
DARK_THRESHOLD = 70                  # suma de R+G+B por debajo de esto = "es contorno"
MAX_COLORS = 16                      # incluye fondo y contorno
CANVAS_W, CANVAS_H = 248, 160        # lienzo GBA estándar
CENTER_X = 140                       # centro horizontal del personaje
FEET_Y = 102                         # y donde va el pie más bajo del personaje
FLIP_HORIZONTAL = True               # poné False si el frame ya mira para el lado correcto


def reemplazar_fondo_chroma(img_rgb: Image.Image) -> Image.Image:
    """Reemplaza el verde puro (#00FF00, chroma key típico del generador) por GREEN_BG."""
    arr = np.array(img_rgb)
    mask = (
        (arr[:, :, 0] < CHROMA_GREEN_TOLERANCE)
        & (arr[:, :, 1] > 255 - CHROMA_GREEN_TOLERANCE)
        & (arr[:, :, 2] < CHROMA_GREEN_TOLERANCE)
    )
    arr[mask] = GREEN_BG
    return Image.fromarray(arr)


def unificar_contorno(img_rgb: Image.Image) -> Image.Image:
    """Convierte todos los píxeles muy oscuros (posibles negros/contornos variables) a OUTLINE_TARGET."""
    arr = np.array(img_rgb)
    mask = arr.sum(axis=2) < DARK_THRESHOLD
    arr[mask] = OUTLINE_TARGET
    return Image.fromarray(arr)


def reducir_colores(img_rgb: Image.Image, n: int = MAX_COLORS) -> Image.Image:
    """Cuantiza la imagen a un máximo de n colores, agrupando los más parecidos entre sí primero."""
    quant = img_rgb.quantize(colors=n, method=Image.MEDIANCUT, dither=Image.NONE)
    return quant.convert("RGB")


def encontrar_bbox_personaje(img_rgb: Image.Image, bg=GREEN_BG, tolerancia=10):
    """Devuelve (centro_x, pie_y) del personaje, ignorando todo lo que sea del color de fondo."""
    arr = np.array(img_rgb)
    not_bg = ~(
        (np.abs(arr[:, :, 0].astype(int) - bg[0]) < tolerancia)
        & (np.abs(arr[:, :, 1].astype(int) - bg[1]) < tolerancia)
        & (np.abs(arr[:, :, 2].astype(int) - bg[2]) < tolerancia)
    )
    ys, xs = np.where(not_bg)
    if len(xs) == 0:
        return img_rgb.width // 2, img_rgb.height  # imagen vacía, valor por defecto
    centro_x = (xs.min() + xs.max()) // 2
    pie_y = ys.max()
    return centro_x, pie_y


def procesar_frame(img: Image.Image) -> Image.Image:
    """Aplica el pipeline completo a un solo frame y devuelve el lienzo 248x160 final."""
    img = img.convert("RGB")

    if FLIP_HORIZONTAL:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)

    img = reemplazar_fondo_chroma(img)
    img = unificar_contorno(img)

    if len(img.getcolors(maxcolors=100000)) > MAX_COLORS:
        img = reducir_colores(img, MAX_COLORS)

    centro_x, pie_y = encontrar_bbox_personaje(img)

    canvas = Image.new("RGB", (CANVAS_W, CANVAS_H), GREEN_BG)
    paste_x = CENTER_X - centro_x
    paste_y = FEET_Y - pie_y
    canvas.paste(img, (paste_x, paste_y))

    return canvas


def procesar_carpeta(carpeta_entrada: str, carpeta_salida: str):
    """Procesa todos los .png de una carpeta y guarda los resultados en otra."""
    os.makedirs(carpeta_salida, exist_ok=True)
    archivos = sorted(f for f in os.listdir(carpeta_entrada) if f.lower().endswith(".png"))

    if not archivos:
        print(f"No se encontraron archivos .png en {carpeta_entrada}")
        return

    print(f"{'Archivo':<30} {'Colores finales'}")
    for nombre in archivos:
        ruta_entrada = os.path.join(carpeta_entrada, nombre)
        img = Image.open(ruta_entrada)
        resultado = procesar_frame(img)

        nombre_salida = nombre.replace(".png", "_248x160.png")
        ruta_salida = os.path.join(carpeta_salida, nombre_salida)
        resultado.save(ruta_salida)

        n_colores = len(resultado.getcolors(maxcolors=100000))
        print(f"{nombre:<30} {n_colores}")

    print(f"\nListo. {len(archivos)} frames procesados en: {carpeta_salida}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python estandarizar_sprites.py carpeta_entrada/ carpeta_salida/")
        sys.exit(1)

    procesar_carpeta(sys.argv[1], sys.argv[2])
