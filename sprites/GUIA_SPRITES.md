# Guía de diseño: sprites de mapa estilo GBA

Notas aprendidas midiendo hojas de sprites de referencia de tácticas en GBA.

## Tamaños

| Tipo de unidad | Ancho máx. | Alto máx. | Lienzo |
|---|---|---|---|
| Infantería | 16 | 16 | 16 × 16 |
| Jinetes / armaduras / unidades altas | 16 | 25 | 16 × 32 |
| Gigantes (1 casilla) | 16 | 28 | 16 × 32 |
| Unidades de 4 casillas | 32 | 32 | 32 × 32 |

- Una casilla de mapa = 16 × 16. **El ancho nunca pasa de 16** en unidades de 1 casilla.
- Lo que crece es el alto: cabeza, casco o arma sobresalen hacia arriba e invaden la casilla de atrás.
- Los pies van siempre en la base de la casilla de abajo.
- Solo las poses tumbadas/agachadas llegan a ~19 px de ancho.

## Colores

- Límite de GBA: **15 colores + 1 transparente por paleta** (4 bits por píxel).
- Todas las unidades de un bando comparten paleta (azul jugador, rojo enemigo, verde aliado, gris inactivo).
- Paleta medida del bando azul de referencia:
  - Contorno: `#403838` (gris oscuro cálido, no negro puro). Es el color más usado.
  - Azules: `#383890` `#3850e0` `#28a0f8` `#90b8e8`, brillo cian `#18f0f8`
  - Claros / piel: `#f8f8d0` `#d8e8f0` `#f8f8f8`
  - Marrones / metal: `#b09058` `#808870` `#706060` `#584878`
  - Acentos: amarillo `#f8f840`, rojo `#e81018` (muy poco uso)

## Reglas de legibilidad (16 × 16)

1. Cabeza grande: ~6–7 px, casi la mitad del alto.
2. Silueta primero: rellena en un color; si la clase no se reconoce, exagera el arma.
3. Rampas de 3–4 tonos por material, luz desde arriba a la izquierda.
4. Contorno exterior grueso y continuo (incluida la parte de arriba de la cabeza); contorno interior en el tono oscuro de cada material.
5. Ojos = 2 píxeles oscuros separados por 1 de piel. Sin boca.
6. Brillos de 1 px en armadura y metal.
7. 1 px de margen y una sombra pequeña bajo los pies.
8. Fondo transparente, nunca blanco ni gris.
9. Probar siempre al 100 % sobre el fondo del mapa.

## Animaciones por personaje (22 cuadros)

| Animación | Cuadros | Lienzo |
|---|---|---|
| Idle | 3 | 16 × 16 (16 × 32 si es alto) |
| Seleccionado | 3 | 32 × 32 |
| Caminar abajo | 4 | 32 × 32 |
| Caminar arriba | 4 | 32 × 32 |
| Caminar izquierda | 4 | 32 × 32 |
| Caminar derecha | 4 | espejo de izquierda |

Se dibujan 18; la derecha es la izquierda volteada en horizontal.

## Flujo de trabajo

- Herramientas: Aseprite / LibreSprite para editar; PixelLab o Retro Diffusion como borrador (siempre requiere limpieza).
- Las IAs de imagen genéricas no sirven: producen "falso pixel art".
- Generar cada animación por separado, no las 22 de una vez.
- Limpieza: Sprite → Color Mode → Indexed (16), quitar fondo, corregir ojos/manos/arma a mano, onion skin para fijar la línea de los pies.

## Prompt base (Retro Diffusion, reducir 32 → 16 un sprite propio)

```
Downscale the reference sprite to 16x16 pixel art, GBA tactics map sprite style.
Keep the same character, pose and colors; do not add or change features.
Style rules:
- thick continuous outline in dark warm gray (#403838), not pure black,
  including the top of the head
- oversized head, about half the sprite height
- 3/4 view, weapon held away from the body so it reads clearly
- 3-4 tone color ramps per material, light from top-left
- 1-pixel bright highlights on armor and metal
- 2-pixel eyes, no mouth
- small soft shadow under the feet, 1px margin on all sides
- sprite fills 14-16px wide
Transparent background, max 15 colors plus transparent,
crisp pixels, no anti-aliasing, no dithering, no blur.
```

Prompt negativo: `new details, different colors, different pose, extra accessories, background, blur`

Ajuste: fuerza de referencia alta (0.75–0.9) para no inventar rasgos.

## Prompt por animación

```
Pixel art animation sheet, GBA tactics map sprite style.
Use the reference sprite: keep the exact same character, colors and proportions.
[ANIMATION]: [N] frames in a single horizontal row, each frame [W]x[H] px,
character centered with feet on the same baseline in every frame.
Thick dark warm-gray outline (#403838), max 15 colors + transparent,
crisp pixels, no anti-aliasing, no dithering, no blur.
```

- Idle: `idle breathing loop, 3 frames, 16x16, subtle 1-pixel up/down bob`
- Seleccionado: `selected/ready loop, 3 frames, 32x32, character bounces and raises weapon slightly`
- Abajo: `walk cycle facing down (toward camera), 4 frames, 32x32`
- Arriba: `walk cycle facing up (back view), 4 frames, 32x32`
- Izquierda: `walk cycle facing left, side view, 4 frames, 32x32`
