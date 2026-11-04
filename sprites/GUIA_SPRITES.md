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

### Paletas por bando (16 slots, el 0 es transparente)

Cada slot cumple la misma función en todos los bandos: se dibuja una vez
con índices y se cambia de bando cambiando la paleta.

| Slot | Función | Aliado | Enemigo | Neutral | Usado | Arena |
|---|---|---|---|---|---|---|
| 0 | Transparente | `#80a080` | `#80a080` | `#80a080` | `#80a080` | `#80a080` |
| 1 | Pelo/tela oscuro | `#584878` | `#684860` | `#385038` | `#404040` | `#584068` |
| 2 | Pelo/tela medio | `#90b8e8` | `#c0a8b8` | `#98c880` | `#787878` | `#a8a8e8` |
| 3 | Pelo/tela claro | `#d8e8f0` | `#e0e0e0` | `#d8f8b8` | `#b8b8b8` | `#e0e0f8` |
| 4 | Piel/cuero oscuro | `#706060` | `#706060` | `#585850` | `#505050` | `#786050` |
| 5 | Piel/cuero medio | `#b09058` | `#b09058` | `#a08840` | `#808080` | `#c08848` |
| 6 | Piel claro | `#f8f8d0` | `#f8f8d0` | `#f8f8c0` | `#c8c8c8` | `#f8f8c8` |
| 7 | Color de bando 1 (sombra) | `#383890` | `#602820` | `#205010` | `#484848` | `#584060` |
| 8 | Color de bando 2 | `#3850e0` | `#a83028` | `#089000` | `#585858` | `#806090` |
| 9 | Color de bando 3 | `#28a0f8` | `#e01010` | `#18d010` | `#989898` | `#b898e0` |
| 10 | Color de bando 4 (brillo) | `#18f0f8` | `#f85048` | `#50f838` | `#b8b8b8` | `#d0c0f8` |
| 11 | Acento (contrario al bando) | `#e81018` | `#38d030` | `#0078c8` | `#707070` | `#e81018` |
| 12 | Amarillo/oro | `#f8f840` | `#f8f840` | `#e0f828` | `#c8c8c8` | `#f8f828` |
| 13 | Gris metal/sombra | `#808870` | `#808870` | `#808870` | `#808870` | `#808870` |
| 14 | Blanco | `#f8f8f8` | `#f8f8f8` | `#f8f8f8` | `#d0d0d0` | `#f8f8f8` |
| 15 | Contorno | `#403838` | `#403838` | `#384038` | `#403838` | `#482840` |

- El color de bando son 4 tonos (slots 7–10): sombra, medio, claro, brillo.
- El acento (slot 11) es siempre el color "contrario": rojo en aliados, verde en enemigos, azul en neutrales.
- Piel (4–6), metal (13), blanco (14) y contorno (15) casi no cambian entre bandos.
- "Usado" = unidad que ya actuó en el turno: todo en grises.

## Cuerpo de clase + cabeza de personaje

Técnica para ahorrar trabajo: se dibuja un cuerpo genérico por clase
(con sus 22 cuadros) y los personajes con nombre solo cambian la cabeza.

- **Capas en Aseprite:** `cuerpo` (de la clase) y `cabeza` (del personaje), separadas.
- **Zona de cabeza fija:** definir en cada clase la caja donde va la cabeza
  (ej. 8 × 7 px arriba al centro) y un punto de anclaje (píxel del cuello).
- **Anclaje por cuadro:** en idle, seleccionado y caminar, la cabeza sube/baja
  con el cuerpo; guardar el desplazamiento (x, y) del cuello en cada cuadro.
- **Cabezas por dirección:** cada personaje necesita 3 cabezas (frente, espalda,
  perfil izquierdo; el derecho es espejo).
- **Paleta:** pelo en slots 1–3 o en slots propios del personaje; el cuerpo usa
  los slots de bando (7–10) para que el cambio de bando siga funcionando.
- **Casco:** si la clase lleva casco, la cabeza del personaje solo cambia la
  cara y el pelo que asoma, o la clase se dibuja sin casco.
- **Coste:** 1 clase = 18 cuadros; cada personaje nuevo = 3 cabezas en vez de 18 cuadros.

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
