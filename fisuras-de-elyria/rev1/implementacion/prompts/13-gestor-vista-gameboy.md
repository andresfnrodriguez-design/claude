# Prompt 13 · Vista Game Boy en el gestor de arte

Para Claude Code en Ubuntu, abierto en `~/gestor-elyria`. Correr después del prompt 12. Antes, actualizar el repo con `cd ~/elyria-claude && git pull`.

```
Quiero ver el pixel art en el gestor de arte como se vería en la Game Boy Advance. La especificación actualizada está en ~/elyria-claude/fisuras-de-elyria/rev1/implementacion/ESPEC_GESTOR_ASSETS.md, sección "Vista Game Boy". Léela y cópiala a ~/gestor-elyria/ESPEC_GESTOR_ASSETS.md. Yo no sé programar, así que explícame todo en español y en pocas líneas.

Si el gestor todavía no arranca con npm start, construye primero lo mínimo de la etapa 1 (ventana, lista de personajes leída de ~/elyria-arte y ficha con sus assets) y después la Vista Game Boy. No hagas las demás etapas ahora.

La Vista Game Boy es una pestaña nueva con una pantalla de 240x160 en escala entera (x1 a x6, sin suavizado) y estas escenas, usando la versión vigente de cada asset.
1. Diálogo. Dos retratos de escena de 104x112, uno a cada lado (el de la izquierda usa retrato_escena_espejo si existe), con el cuadro de texto de FE8 y una línea de texto de prueba.
2. Pantalla de estado. Retrato de 108x160 a la izquierda y el resto de la pantalla con cajas de ejemplo.
3. Mapa. Ventana de unidad con el mini retrato de 32x32.
4. Combate. Dos figuras de 80x56 enfrentadas sobre un fondo liso, con las barras de vida de ejemplo.
5. Primer plano. El zoom de 180x120 y un botón para alternar con el herido.

Reglas de color.
- Cada canal se redondea a múltiplos de 8 antes de dibujar, como hace la GBA.
- #A9CBA6 es transparente.
- Interruptor "GBA original" (colores apagados y algo más oscuros, como la pantalla sin luz) y "GBA SP / emulador" (colores directos).
- Interruptor de rejilla de píxeles.

Posiciones. Busca en ~/fireemblem8u (src/face.c, src/cgtext.c, la pantalla de estado y la ventana de unidad) dónde dibuja el juego cada retrato y usa esas coordenadas. Donde el tamaño nuevo no coincida con el original, centra y ajusta lo mínimo. Anota todas las posiciones en estandar.json para que yo pueda cambiarlas sin tocar el código.

Extras. Selector de personaje para cada lado del diálogo y del combate, y un botón que guarda una captura PNG de la pantalla en ~/elyria-arte/capturas/.

Prueba con la archivista, que es la única con el estándar nuevo completo. Al terminar haz commit en ~/gestor-elyria, dime cómo abro la vista y muéstrame qué posiciones sacaste de la decompilación y cuáles aproximaste.
```
