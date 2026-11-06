# Kairon en lugar de Ephraim, con las rutas de la decomp

Esta carpeta copia la estructura de `~/fireemblem8u/graphics/` para que Claude Code encuentre cada archivo donde lo espera la decomp.

| Archivo | Reemplaza a | Nota |
|---|---|---|
| `graphics/portrait/portrait_Ephraim_mouth.png` | El mismo nombre | 6 bocas de 32x16, orden de FE8 |
| `graphics/portrait/portrait_Ephraim_chibi.png` | El mismo nombre | Mini de 32x32 |
| `graphics/portrait/portrait_Ephraim_palette.agbpal` | El mismo nombre | Paleta única de Kairon |
| `graphics/unit_icon/wait/unit_icon_wait_Ephraim_Lord_sheet.png` | El mismo nombre | Es de 16x48 (cuadros de 16x16). El de Ephraim es de 16x96, así que hay que cambiar el tamaño en la tabla de sprites de mapa |
| `graphics/unit_icon/move/unit_icon_move_Ephraim_Lord_sheet.png` | El mismo nombre | 15 cuadros de 32x32 |
| `graphics/elyria/kairon/` | Formatos nuevos del hack | Escena y espejo de 104x112, ojos, estado de 80x144, zoom y HERIDO de 240x160 y las coordenadas de boca y ojos. Van donde el código nuevo de retratos los lea |

No reemplaza `portrait_Ephraim_tileset.png`, porque el retrato de 104x112 no usa el formato de 96x80. El prompt `04-kairon-reemplaza-ephraim.md` explica qué hacer con cada archivo.

Para copiarla al proyecto.

```bash
cp -r para_decomp/graphics/* ~/fireemblem8u/graphics/
```
