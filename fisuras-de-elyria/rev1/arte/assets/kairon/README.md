# Kairon, assets de prueba

Assets de Kairon a la resolución del motor, sacados de las hojas de concepto de Nano Banana. Son para probar en el juego antes de pasar por PixelLab. Reemplazan los gráficos de Ephraim.

Todos son PNG indexados de 16 colores con el verde `#A9CBA6` en el índice 0, que el motor toma como transparente. No hay JPG porque la GBA necesita colores exactos y el JPG los mezcla al comprimir.

## Espejado

Gemini dibuja el guantelete en la mano derecha y la batalla mirando a la derecha. El script espeja todo. En el juego el guantelete queda en la mano izquierda, los retratos miran a la izquierda y la batalla ataca hacia la izquierda.

## Archivos

| Archivo | Tamaño | Uso |
|---|---|---|
| `retratos/kairon_escena_104x112.png` | 104x112 (arte de 100x112 en x=2) | Retrato de escena |
| `retratos/kairon_espejo_104x112.png` | 104x112 | Espejo real, mirando a la derecha con el guantelete en la misma mano. Sale de `fuente/espejo_real.png`, generado aparte |
| `retratos/kairon_bocas_32x96.png` | 6 cuadros de 32x16 | Bocas dibujadas sobre el retrato base, en su línea de boca |
| `retratos/kairon_ojos_32x32.png` | 2 cuadros de 32x16 | Ojos entrecerrados y cerrados, dibujados sobre el retrato base |
| `retratos/kairon_coordenadas.json` | | Posición de la boca y los ojos dentro de la hoja de 104x112 |
| `retratos/kairon_mini_32x32.png` | 32x32 | Mini retrato, la cabeza del retrato de escena reducida |
| `retratos/kairon_retrato.agbpal` | 16 colores | Paleta compartida por escena, espejo, bocas, ojos y mini |
| `retratos/kairon_estado_80x144.png` | 80x144 | Retrato de la pantalla de estado, sale del FRENTE de la hoja 1 con cabeza de 28 px |
| `zoom/kairon_zoom_240x160.png` | 240x160 | Fondo del menú de estado |
| `zoom/kairon_herido_240x160.png` | 240x160 | El mismo fondo con menos de 25 % de vida |
| `mapa/kairon_mapa_quieto_16x48.png` | 3 cuadros de 16x16 | Sprite de mapa quieto |
| `mapa/kairon_mapa_movimiento_32x480.png` | 15 cuadros de 32x32 | 4 izquierda, 4 abajo, 4 arriba, 3 seleccionado |
| `mapa/paleta_aliados.agbpal` | 16 colores | Paleta de aliados aprobada, con el mismo orden de posiciones que la de FE8 |
| `batalla/kairon_01_quieto.png` a `kairon_08_impacto.png` | 248x160 | 8 cuadros clave, personaje de 34 px con los pies en y=102 y centrado en x=140 |
| `batalla/kairon_batalla.agbpal` | 16 colores | Paleta única de toda la animación, contorno `#282828` |
| `fuente/` | | Hojas originales de Gemini |
| `script/` | | `build.py`, `core.py` y `reg.py` para regenerar todo |

**Paleta única.** Retratos, espejo, mini, bocas, ojos, estado, zoom, HERIDO y batalla usan la misma paleta de 16 colores (`kairon_paleta.agbpal`, muestra en `vistas/kairon_paleta.png`). El script la arma en una primera pasada con los colores de todas las imágenes, así que hay que correrlo dos veces. Los sprites de mapa usan la paleta de aliados.

**Un solo verde.** El índice 0 es siempre `#A9CBA6` exacto en retratos, zoom y batalla. Los sprites de mapa usan `#80a080`, que es el transparente de la paleta de aliados.

**Sprites de mapa.** Cada píxel de la fuente se clasifica por material en su posición de la paleta de aliados (abrigo en la rampa pastel 1 a 3, granate en el color del bando 7 a 10, piel y bronce en 4 a 6, gema en 10). Se reduce por voto mayoritario, se limpian píxeles sueltos, se agregan ojos de 2 px, contorno grueso por fuera y sombra bajo los pies. Infantería de 16x16 con los pies en la fila 14.

**Vistas animadas.** `vistas/kairon_hablando.gif`, `kairon_hablando_sonriendo.gif` y `kairon_pestaneando.gif` muestran las bocas y los ojos puestos sobre el retrato.

**Bocas.** El orden de los cuadros es el de FE8 (sonrisa abierta, media y cerrada, normal abierta, media y cerrada). La normal cerrada es igual al retrato base.

## Regenerar

Copia las hojas como `h1.jpg` a `h5.jpg` y el espejo real como `espejo.png` en una carpeta y corre esto.

```bash
python3 script/build.py carpeta_con_las_hojas carpeta_de_salida
```

Necesita `numpy`, `pillow`, `scipy` y `opencv-python`.

## Limitaciones conocidas

- Las bocas y los ojos de la hoja 5 no servían a esta escala, así que se dibujan por script sobre el retrato base. Conviene retocarlos a mano.
- Los sprites de mapa de Gemini son angostos (unos 9 px de ancho), así que el resultado queda flaco. El asset final conviene hacerlo en PixelLab o a mano.
- El HERIDO no tiene el mismo encuadre que el zoom.
- Los sprites de batalla son una reducción del concepto. Sirven para probar la posición y la escala, no como arte final.
