"""Anima el fondo de fisuras (solo se mueven las esquirlas) y arma un GIF.
Uso: FONDO=fisuras_fucsia python3 animar.py gris_final [cuadros]"""
import os, sys, subprocess
from PIL import Image
tema = sys.argv[1] if len(sys.argv) > 1 else "gris_final"; N = int(sys.argv[2]) if len(sys.argv) > 2 else 16
FONDO = os.environ.get("FONDO", "fisuras_fucsia"); sr = "_sin_retrato" if os.environ.get("SIN_RETRATO") else ""
cuadros = []
for i in range(N):
    subprocess.run([sys.executable, "recolorear.py", tema], check=True, capture_output=True,
                   env={**os.environ, "FONDO": FONDO, "T": str(i * 4)})
    cuadros.append(Image.open(f"tema_{tema}{sr}_{FONDO}.png").convert("RGB").resize((480, 320), Image.NEAREST))
nombre = f"anim_{tema}{sr}_{FONDO}.gif"
cuadros[0].save(nombre, save_all=True, append_images=cuadros[1:], duration=120, loop=0)
print(nombre)
