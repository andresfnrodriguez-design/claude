# Kairon, assets de prueba

Assets de Kairon a la resolución del motor, sacados de las hojas de concepto de Nano Banana. Son para probar en el juego antes de pasar por PixelLab. Reemplazan los gráficos de Ephraim.

Todos son PNG indexados de 16 colores con el verde `#A9CBA6` en el índice 0, que el motor toma como transparente. No hay JPG porque la GBA necesita colores exactos y el JPG los mezcla al comprimir.

## Espejado

Gemini dibuja el guantelete en la mano derecha y la batalla mirando a la derecha. El script espeja todo. En el juego el guantelete queda en la mano izquierda, los retratos miran a la izquierda y la batalla ataca hacia la izquierda.

## Archivos

| Archivo | Tamaño | Uso |
|---|---|---|
| `retratos/kairon_escena_104x112.png` | 104x112 (arte de 100x112 en x=2) | Retrato de escena |
| `retratos/kairon_espejo_104x112.png` | 104x112 | Espejo real, mismo retrato mirando a la derecha con el guantelete en la misma mano |
| `retratos/kairon_bocas_32x96.png` | 6 cuadros de 32x16 | Bocas, recortadas del retrato con su mismo ángulo |
| `retratos/kairon_ojos_32x32.png` | 2 cuadros de 32x16 | Ojos entrecerrados y cerrados |
| `retratos/kairon_coordenadas.json` | | Posición de la boca y los ojos dentro de la hoja de 104x112 |
| `retratos/kairon_mini_32x32.png` | 32x32 | Mini retrato |
| `retratos/kairon_retrato.agbpal` | 16 colores | Paleta compartida por escena, espejo, bocas, ojos y mini |
| `retratos/kairon_estado_80x144.png` | 80x144 | Retrato de la pantalla de estado, con su propia paleta |
| `zoom/kairon_zoom_240x160.png` | 240x160 | Fondo del menú de estado |
| `zoom/kairon_herido_240x160.png` | 240x160 | El mismo fondo con menos de 25 % de vida |
| `mapa/kairon_mapa_quieto_16x48.png` | 3 cuadros de 16x16 | Sprite de mapa quieto |
| `mapa/kairon_mapa_movimiento_32x480.png` | 15 cuadros de 32x32 | 4 izquierda, 4 abajo, 4 arriba, 3 seleccionado |
| `mapa/paleta_aliados.agbpal` | 16 colores | Paleta de aliados aprobada, con el mismo orden de posiciones que la de FE8 |
| `batalla/kairon_01_quieto.png` a `kairon_08_impacto.png` | 248x160 | 8 cuadros clave, personaje de 34 px con los pies en y=102 y centrado en x=140 |
| `batalla/kairon_batalla.agbpal` | 16 colores | Paleta única de toda la animación, contorno `#282828` |
| `fuente/` | | Hojas originales de Gemini |
| `script/` | | `build.py`, `core.py` y `reg.py` para regenerar todo |

**Bocas.** El orden de los cuadros es el de FE8 (sonrisa abierta, media y cerrada, normal abierta, media y cerrada). La normal cerrada es igual al retrato base.

## Regenerar

Copia las hojas como `h2.jpg`, `h3.jpg`, `h4.jpg` y `h5.jpg` en una carpeta y corre esto.

```bash
python3 script/build.py carpeta_con_las_hojas carpeta_de_salida
```

Necesita `numpy`, `pillow`, `scipy` y `opencv-python`.

## Limitaciones conocidas

- Los ojos de la hoja 5 salieron como recortes chicos. Se alinearon por el pelo y sirven para probar, pero conviene retocarlos a mano.
- A este tamaño la boca mide unos 3 px, así que las 6 bocas se diferencian poco.
- El HERIDO no tiene el mismo encuadre que el zoom.
- Los sprites de batalla son una reducción del concepto. Sirven para probar la posición y la escala, no como arte final.
