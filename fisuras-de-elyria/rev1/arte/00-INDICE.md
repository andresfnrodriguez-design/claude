# Arte — índice

Concept art, retratos, sprites, paletas, pantalla de estado y tilesets.

## Documentos

| Archivo | Qué es |
|---|---|
| `estandares-pixel-art.md` | Reglas cortas de concept, sprites, frames y mapas. **Empezar acá** |
| `biblia-visual.md` | Paletas por región, vestuario, objetos recurrentes, ambientaciones y retratos por personaje |
| `GUIA_SPRITES-mapa.md` | Sprites de mapa, paletas por bando, rampas, cuerpo más cabeza, contorno |
| `prompts_nano_banana.md` | Prompts de las tres hojas de plantilla y tres personajes de prueba |
| `pantalla-estado/README.md` | Uso de los scripts de la pantalla de estado |
| `pixellab-map-tools.md`, `guia-tilesets-resumen.md` | PixelLab (Create Map y Create Tileset) y cómo se arma un tileset |
| `guia-scripting-resumen.md`, `referencia_imagenes_script.md` | Scripting de animaciones de batalla y tabla de frames de Kairon |
| `scripts/` | Scripts completos en bloques de código, listos para copiar |
| `referencias/guia-scripting-animaciones-original.txt` | Guía original de scripting de animaciones |

## Flujo de producción

1. **Concept art con Nano Banana.** Decide el diseño, no es el asset final. Estilo anime para personajes nuevos, densidad aetherpunk alta (correas, hebillas, herramientas, frascos), gancho narrativo propio y el arma de su clase. Relación 3:2, máxima calidad. La hoja 1 sale de la plantilla sola, y las hojas 2 y 3 llevan la plantilla más la hoja 1 como referencia.
2. **Asset final con PixelLab**, subiendo siempre el concept aprobado.
3. **Estandarización con script** antes de meterlo al juego.

## Estándares vigentes

**Retratos de escena.** Arte de 100x112 sobre una hoja de 104x112. 16 colores con `#A9CBA6` en el índice 0. Línea negra de 1 px en el borde y contorno blanco de 1 px por fuera. 3 px de margen arriba, cabeza nunca cortada, silueta completa sin cortes laterales y proporción de Eirika. Se genera a 200x224 o 400x448 y se reduce por múltiplo exacto con voto mayoritario. Si el arte corta la silueta, se completa antes de escalar. El de 96x80 queda descartado.

**Retrato de pantalla de estado.** 80x144 en un marco de 88x152 en x=8, y=4, con 4 px de margen verde arriba y abajo y 8 px a la izquierda. Acá sí se permiten cortes laterales, y la escala se iguala por el tamaño de cabeza.

**Bocas y ojos.** El motor los anima solo. Se dibujan 6 bocas de 32x16 (normal y sonriendo, cerrada, media y abierta) y 2 ojos (entrecerrado y cerrado), editando el pixel art final. Falta fijar sus coordenadas dentro del retrato de 100x112.

**Sprites de batalla.** Lienzo de 248x160, fondo `#A9CBA6`, contorno único `#282828`, máximo 16 colores en toda la animación, personaje centrado en x=140 con los pies en y=102. Ángulo 3/4, iluminación más fuerte del lado que mira a la cámara y sombra con la forma real de la silueta. Altura de unos 34 px para hombres y 32 para mujeres. El script de FEBuilder va en un solo .txt con los 12 modos.

**Sprites de mapa.** Figura de 16 px de ancho, 16 de alto para infantería y hasta 25 a 28 para jinetes. Quieto son 3 cuadros de 16x16. En movimiento son 15 cuadros en celdas de 32x32 (4 a la izquierda, 4 abajo, 4 arriba, 3 seleccionado), y la derecha la voltea el motor. 15 colores más transparente, con la misma estructura de posiciones en todas las paletas. Posiciones 7 a 10 para el color principal y 1 a 3 para el secundario pastel. Contorno interior solo del lado de la sombra.

**Por clase o por personaje.** Sprites de mapa y animaciones de batalla van por clase. Retratos, paleta, paleta de batalla propia y voz van por personaje.

**Pantalla de estado (diseño cerrado).** 240x160, tema `gris_final`, fondo animado `fisuras_fucsia` (degradado teal a fucsia con 40 esquirlas lentas). El detalle de cada elemento está en `../sesiones/01-pantalla-estado.md`.

**Ficha oficial de Kairon.** Abrigo largo crema con lazo granate y guante de bronce (`47afd033-image.png`). La de "Wanderer Investigator" queda descartada.

## Imágenes vigentes

Están en GitHub, rama `claude/fisuras-de-elyria-rev1`, carpeta `fisuras-de-elyria/rev1/arte/`. Las principales también van en `arte-imagenes-rev1.zip` para subir a los archivos del proyecto.

| Ruta | Qué es |
|---|---|
| `imagenes/retratos/portrait_kairon_100x112.png`, `portrait_referencia_100x112.png` | Retratos de escena finales para importar |
| `imagenes/retratos/estado_kairon_80x144.png`, `estado_referencia_80x144.png` | Retratos de pantalla de estado finales |
| `imagenes/retratos/mockups/` | Mockups a 240x160 de soporte y pantalla de estado |
| `pantalla-estado/tema_gris_final_*.png`, `anim_gris_final_*.gif` | Pantalla de estado final con Kairon y con el retrato 3 |
| `pantalla-estado/` | Además todos los scripts, temas y la entrada original |
| `imagenes/kairon/` | Frames del ataque y del crítico de Kairon |
| `sprites-mapa/` | Scripts, paletas aprobadas, rampas, ninja y pícaro de prueba |
| `plantillas/` | Plantillas para Nano Banana y su script |
| `imagenes/referencias/kairon_ficha_oficial.png` | Ficha oficial de Kairon |
| `imagenes/referencias/subidas-chat-historia/` | Concept art y capturas subidas en el chat de historia, sin duplicados |
| `imagenes/historico/` | Versiones intermedias de retratos, sprites y piezas |
| `scripts/` | Scripts de retratos y de batalla como archivos reales |

## Abierto

- Arte de Kairon de cintura para arriba con la cara ladeada, generado a 200x224 o 400x448.
- Arte nuevo del personaje femenino de referencia a tamaño final, con pies para la pantalla de estado.
- Retoque a mano de ojos, boca y cejas en los retratos.
- Si el mini retrato se agranda o queda en 32x32.
- Si se hace el espejado real de retratos (necesita un segundo ID y un cambio en `StartFace`).
- Pantalla de estado. Reducir el render (unos 200 a 300 colores) a paletas de 16 por tile y resolver las cuatro transparencias con un solo EVA/EVB de GBA. El retrato 3 es de un tercero y solo sirve de prueba.
- Sprites de mapa. Conseguir el PNG original del ninja, retocarlo a mano y hacer sus animaciones. El verde neutral se pierde sobre pasto.
- Falta el GIF del crítico de Kairon para completar el Mode 3 del script.
- Colores que quieres cambiar. Pasto y montañas del capítulo 1, azul de las unidades del jugador y azules y blancos de la pantalla de batalla. Las paletas están en `graphics/map/MapPalette*.pal`, `graphics/unit_icon/palette/` y `graphics/player_interface/*.pal`.
