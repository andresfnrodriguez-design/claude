# Archivista en pixel art con el MCP de PixelLab (Claude Code en Ubuntu)

Trabajo en **Fisuras de Elyria**. En este Claude Code ya está conectado el MCP oficial de PixelLab (`https://api.pixellab.ai/mcp`). Quiero convertir a pixel art las 4 hojas de la archivista **con el tamaño exacto de salida**, que en la web no puedo fijar porque el modo Pro escala solo. Explícame cada paso en español simple.

## Antes de generar

1. `git pull` en la rama `claude/nifty-bell-x1mrwv`. Las hojas están en `fisuras-de-elyria/rev1/arte/placeholders/prueba_archivista/pixellab/pro/`.
2. Lista las herramientas del MCP de PixelLab y dime cuál convierte una imagen a pixel art aceptando **ancho y alto exactos** (y si acepta paleta, descripción e init strength). Si la de "pro" no acepta tamaño, usa la que sí lo acepta.
3. Consulta el saldo, dime cuántas generaciones gasta cada llamada y el total de las 4, confirma que no haya otra tanda en curso y **espera mi visto bueno**. Una sola tanda por aprobación.

## Las 4 llamadas

| Archivo de entrada | Salida exacta |
|---|---|
| `archivista_pro1_960x464_sale_240x116.png` | 240 × 116 |
| `archivista_pro2_752x640_sale_188x160.png` | 188 × 160 |
| `archivista_zoom_728x488_sale_182x122.png` | 182 × 122 |
| `archivista_herido_728x488_sale_182x122.png` | 182 × 122 |

- Paleta: `archivista_paleta_pixellab.png` (16 colores), si la herramienta acepta paleta o imagen de paleta.
- Init strength alto, alrededor de 0.75, para que respete la imagen.
- Descripción: el prompt de cada hoja en `prompts_pro.txt` (el texto completo de la hoja + la base común).
- Guarda cada salida en `pro/salidas/` con el mismo nombre de entrada y `_pixel` al final.

## Después

1. Verifica con Python que cada salida mida exactamente lo de la tabla. Si alguna no coincide, avísame y no la uses.
2. Corta las piezas:

```
cd fisuras-de-elyria/rev1/arte/placeholders
python3 hoja_pixellab.py cortar prueba_archivista prueba_archivista/pixellab/pro/salidas/archivista_pro1_*_pixel.png prueba_archivista/pixellab/pro/salidas/archivista_pro2_*_pixel.png prueba_archivista/pixellab/pro/salidas/archivista_zoom_*_pixel.png prueba_archivista/pixellab/pro/salidas/archivista_herido_*_pixel.png
```

3. Muéstrame las piezas de `prueba_archivista/pixellab/out/` ampliadas x3 y, si te digo que están bien, haz commit y push.
