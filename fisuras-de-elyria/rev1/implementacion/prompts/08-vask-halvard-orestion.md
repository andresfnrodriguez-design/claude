# Megaprompt 8. Retratos de Vask, Halvard y Orestion (placeholders)

## Contexto

Trabajo en **Fisuras de Elyria**, un ROM hack de Fire Emblem 8 hecho sobre la decompilación `fireemblem8u`, en `~/fireemblem8u`. Compilo con `make -j$(nproc) fireemblem8.gba` y pruebo en mGBA. Nunca uses `make` solo ni `make compare`.

Es el mismo tipo de trabajo que el megaprompt 4 (Kairon en lugar de Ephraim). Si ese ya está implementado, reutiliza el mismo código de retratos de 104x112, estado de 80x144 y zoom de 240x160 con HERIDO. Si no está, dímelo antes de tocar nada.

Estándares del proyecto.

- Retrato de escena con arte de 100x112 en una hoja de 104x112, en lugar de la cara de 96x80.
- Retrato de la pantalla de estado de 80x144, cuerpo entero.
- Zoom de estado de 240x160 como fondo del menú de estado, con la variante HERIDO cuando la vida baja del 25 %.
- Mini retrato de 32x32.
- Cada personaje usa una sola paleta de 16 colores con `#A9CBA6` en el índice 0 para todos sus gráficos.
- Todos los personajes están dibujados a la misma escala. No los reescales por separado.

Los assets están en el repositorio `andresfnrodriguez-design/claude`, rama `claude/nifty-bell-x1mrwv`, carpeta `fisuras-de-elyria/rev1/arte/placeholders/para_decomp/`. Ya tiene las rutas y nombres de la decomp. Lee su `LEEME.md`.

## Tarea

Reemplazar los gráficos por personaje de estos tres personajes de FE8. Son placeholders para probar cómo se ven en el juego.

| Personaje nuevo | Reemplaza a | Por qué |
|---|---|---|
| Vask (mercenario de pelo rosa) | Joshua | Mercenario que juega con una moneda |
| Halvard (oficial con lanza y escudo) | Gilliam | Soldado con lanza y escudo |
| Orestion (guardián mayor, lanza) | Seth | Veterano que aparece desde el principio, sirve para probar rápido |

Para cada uno.

| Asset | Reemplaza a |
|---|---|
| `graphics/elyria/<id>/<id>_escena_104x112.png` | La cara del personaje en `src/portrait_data.c` (todos sus IDs, incluido el de recuerdo si tiene) |
| `graphics/elyria/<id>/<id>_espejo_104x112.png` | Por ahora es el mismo retrato espejado. Si el espejo real del megaprompt 4 ya existe, conéctalo. Si no, ignóralo |
| `graphics/portrait/portrait_<Nombre>_chibi.png` | El mini retrato del mismo nombre |
| `graphics/portrait/portrait_<Nombre>_palette.agbpal` | La paleta del retrato del mismo nombre. Para la paleta de recuerdo genera una versión en sepia de esta |
| `graphics/elyria/<id>/<id>_estado_80x144.png` | El retrato de la pantalla de estado |
| `graphics/elyria/<id>/<id>_zoom_240x160.png` y `<id>_herido_240x160.png` | El zoom de estado y su variante HERIDO |

`<id>` es `vask`, `halvard` u `orestion`, y `<Nombre>` es `Joshua`, `Gilliam` o `Seth`.

**Bocas y ojos.** Estos placeholders no traen bocas ni ojos. No uses las bocas originales de FE8, porque no coinciden con el dibujo. Desactiva la animación de boca y parpadeo para estos tres personajes, o deja la boca fija en el cuadro base, lo que sea más simple. No cambies `portrait_<Nombre>_mouth.png` ni `portrait_<Nombre>_tileset.png`.

**No toques** los nombres de los personajes, sus clases, los sprites de mapa ni las animaciones de batalla.

## ANTES DE ESCRIBIR CÓDIGO, dame feedback

Respóndeme primero, sin implementar nada.

1. **Estado actual.** Si el código de retratos de 104x112, estado de 80x144, zoom de 240x160 y HERIDO ya está en el repo (revisa `git log`, `src/face.c`, `src/portrait_data.c` y la pantalla de estado).
2. **Lo que entendiste.** Qué archivo va a qué lugar.
3. **Viabilidad.** Si entran en la memoria de video, cómo los convierte el Makefile y qué tablas hay que tocar.
4. **Dudas.**
5. **Plan.** Archivos y funciones en orden.

Solo cuando te confirme el plan, implementa.

## Al terminar

1. Compila con `make -j$(nproc) fireemblem8.gba` y confirma que no hay errores.
2. Dime dónde ver cada uno en mGBA (capítulo y escena). Seth sale en el prólogo, Gilliam en el capítulo 1 y Joshua en el capítulo 3.
3. Lista lo que quedó pendiente o aproximado.
4. Agrega una entrada en `registro-implementaciones.md`.

Responde en español neutro, tuteando.
