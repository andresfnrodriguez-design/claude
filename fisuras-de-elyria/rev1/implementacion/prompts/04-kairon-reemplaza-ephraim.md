# Megaprompt 4. Gráficos de Kairon en lugar de los de Ephraim

## Contexto

Trabajo en **Fisuras de Elyria**, un ROM hack de Fire Emblem 8 hecho sobre la decompilación `fireemblem8u`, en `~/fireemblem8u`. Compilo con `make -j$(nproc) fireemblem8.gba` y pruebo en mGBA. Nunca uses `make` solo ni `make compare`, porque comparan con la ROM original y fallan con cualquier cambio.

Ya cambiamos en el código el tamaño de algunos gráficos respecto de FE8 original. Los estándares del proyecto son estos.

- Retrato de escena con arte de 100x112 en una hoja de 104x112, en lugar de la cara de 96x80.
- Retrato de la pantalla de estado de 80x144.
- Zoom de estado de 240x160 como fondo del menú de estado, con una variante HERIDO cuando la vida baja del 25 %.
- Mini retrato de 32x32.
- Sprites de mapa de 16x16 quieto y celdas de 32x32 en movimiento.

Los assets están en `elyria_assets/kairon/` dentro del proyecto. Lee su `README.md` antes de empezar.

## Tarea

Reemplazar los gráficos de **Ephraim** por los de **Kairon**. El retrato, el mini retrato, las bocas, los ojos, el retrato de estado y el zoom van por personaje. El sprite de mapa va por clase, así que reemplaza el de la clase de Ephraim (Lord). La animación de batalla no se toca por ahora.

| Asset | Reemplaza a |
|---|---|
| `retratos/kairon_escena_104x112.png` | La cara de Ephraim (IDs de retrato 19 y 20 en `src/portrait_data.c`, y 45 el de recuerdo) |
| `retratos/kairon_bocas_32x96.png` | `portrait_Ephraim_mouth`. El orden de los cuadros ya es el de FE8 |
| `retratos/kairon_ojos_32x32.png` | Los ojos entrecerrados y cerrados del parpadeo |
| `retratos/kairon_coordenadas.json` | Los valores `xMouth`, `yMouth`, `xEyes` e `yEyes`. Están en píxeles y en tiles dentro de la hoja de 104x112 |
| `retratos/kairon_mini_32x32.png` | `portrait_Ephraim_chibi`. Sus ojos no pestañean |
| `retratos/kairon_retrato.agbpal` | `portrait_Ephraim_palette`. Es la paleta única de Kairon y la usan también el estado y el zoom. Para `portrait_Ephraim_flashback_palette` genera una versión en tonos sepia de esta |
| `retratos/kairon_estado_80x144.png` | El retrato de la pantalla de estado de Ephraim |
| `zoom/kairon_zoom_240x160.png` y `zoom/kairon_herido_240x160.png` | El zoom de estado de Ephraim y su variante HERIDO |
| `mapa/kairon_mapa_quieto_16x48.png` | `unit_icon_wait_Ephraim_Lord_sheet`. Ojo, el de Ephraim es de 16x32 por cuadro y este es de 16x16, así que hay que cambiar el tamaño en la tabla de sprites de mapa |
| `mapa/kairon_mapa_movimiento_32x480.png` | `unit_icon_move_Ephraim_Lord_sheet` |

Los sprites de mapa usan el mismo orden de posiciones de color que la paleta de jugador de FE8. `mapa/paleta_aliados.agbpal` es la paleta de aliados aprobada para el hack. No la apliques sin preguntarme, porque cambia el color de todas las unidades aliadas.

## ANTES DE ESCRIBIR CÓDIGO, dame feedback

Respóndeme primero, sin implementar nada, con estas secciones.

1. **Estado actual.** Revisa `git log`, `src/face.c`, `src/portrait_data.c`, la pantalla de estado y los sprites de mapa. Dime qué cambios de tamaño ya están aplicados en el código (retrato de 104x112, estado de 80x144, zoom de 240x160, HERIDO). Si alguno no está, dímelo y no lo implementes todavía.
2. **Lo que entendiste.** Qué archivo va a qué lugar.
3. **Viabilidad.** Formato de cada asset, cómo los convierte el Makefile (`gbagfx` u otra herramienta) y dónde hay que cambiar tablas o tamaños.
4. **Dudas.** Por ejemplo si cambio también el nombre de Ephraim por Kairon, y cómo implementar el espejo real (`kairon_espejo_104x112.png`). Cuando el retrato de Kairon aparece del lado que lo voltearía, en vez de voltearlo hay que mostrar este otro. Necesita un segundo ID de retrato y un cambio en `StartFace`.
5. **Plan.** Archivos y funciones que vas a tocar, en orden, separando lo que es solo cambiar gráficos de lo que necesita código nuevo.

Solo cuando te confirme el plan, implementa.

## Al terminar

1. Compila con `make -j$(nproc) fireemblem8.gba` y confirma que no hay errores.
2. Dime qué ver en mGBA para probar cada asset. Los cambios de personajes se ven en una partida nueva.
3. Lista lo que quedó pendiente o aproximado.
4. Agrega una entrada en `registro-implementaciones.md` con lo que cambiaste.

Responde en español neutro, tuteando.
