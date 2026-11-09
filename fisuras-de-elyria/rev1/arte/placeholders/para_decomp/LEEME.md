# Vask, Halvard y Orestion con las rutas de la decomp

Esta carpeta copia la estructura de `~/fireemblem8u/graphics/`. El prompt es `implementacion/prompts/08-vask-halvard-orestion.md`.

| Personaje | Reemplaza a | Carpeta propia |
|---|---|---|
| Vask | Joshua | `graphics/elyria/vask/` |
| Halvard | Gilliam | `graphics/elyria/halvard/` |
| Orestion | Seth | `graphics/elyria/orestion/` |

| Archivo | Qué es |
|---|---|
| `graphics/portrait/portrait_<Nombre>_chibi.png` | Mini de 32x32, reemplaza al del mismo nombre |
| `graphics/portrait/portrait_<Nombre>_palette.agbpal` | Paleta única del personaje, 16 colores BGR555, `#A9CBA6` en el índice 0 |
| `graphics/elyria/<id>/<id>_escena_104x112.png` y `_espejo_104x112.png` | Retrato de diálogo y su espejo |
| `graphics/elyria/<id>/<id>_estado_80x144.png` | Retrato de estado de cuerpo entero |
| `graphics/elyria/<id>/<id>_zoom_240x160.png` y `_herido_240x160.png` | Zoom del menú de estado y su variante HERIDO |
| `graphics/elyria/<id>/<id>_paleta.agbpal` | Copia de la paleta |

Todos los PNG están indexados con la paleta del personaje y a la escala común del elenco. No traen bocas ni ojos, y no reemplazan `portrait_<Nombre>_mouth.png` ni `portrait_<Nombre>_tileset.png`.
