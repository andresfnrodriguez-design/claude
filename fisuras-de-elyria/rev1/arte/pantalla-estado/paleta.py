"""Lee los colores de estado_gba.png y genera paleta.png + paleta.txt (RGB888, hex y BGR555 de la GBA)."""
from PIL import Image, ImageDraw
img = Image.open(__import__("sys").argv[1] if len(__import__("sys").argv) > 1 else "estado_gba.png").convert("RGB")
cols = sorted(img.getcolors(4096), reverse=True)
lado, por_fila = 24, 16
filas = (len(cols) + por_fila - 1) // por_fila
sw = Image.new("RGB", (por_fila * lado, filas * lado), (0, 0, 0)); d = ImageDraw.Draw(sw)
lineas = ["#  n_pix  RGB            hex      GBA(BGR555)"]
for i, (n, (r, g, b)) in enumerate(cols):
    x, y = (i % por_fila) * lado, (i // por_fila) * lado
    d.rectangle([x + 1, y + 1, x + lado - 2, y + lado - 2], fill=(r, g, b))
    gba = (b >> 3) << 10 | (g >> 3) << 5 | (r >> 3)
    lineas.append(f"{i:<3}{n:>6}  ({r:3},{g:3},{b:3})  #{r:02x}{g:02x}{b:02x}  0x{gba:04X}")
sw.resize((sw.width * 2, sw.height * 2), Image.NEAREST).save("paleta.png")
open("paleta.txt", "w").write("\n".join(lineas) + "\n")
print(len(cols), "colores")
