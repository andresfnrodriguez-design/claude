# Megaprompt 1 — Barras de vida en el mapa estilo Fates (FE8 / fireemblem8u)

## Contexto

Trabajo en **Fisuras de Elyria**, un ROM hack de Fire Emblem 8 (The Sacred Stones) hecho sobre la decompilación **fireemblem8u** (C compilado con agbcc, WSL + VS Code, pruebas en mGBA). Quiero agregar una barra de vida bajo cada unidad en el mapa, inspirada en la de Fire Emblem Fates (3DS), adaptada a los límites de la GBA.

## ANTES DE ESCRIBIR CÓDIGO: dame feedback

Respóndeme primero, sin implementar nada, con estas secciones:

1. **Lo que entendiste.** Resume la especificación con tus palabras, incluida la regla de colores y el degradado.
2. **Viabilidad.** ¿Es posible en GBA tal cual? Analiza en concreto:
   - Paletas de OBJ libres en FE8 durante el mapa (cuáles usa el juego y cuáles quedan).
   - Espacio libre en la VRAM de OBJ en el mapa (hoja de sprites del mapa SMS, íconos, cursor, etc.).
   - Límite de OAM con muchas unidades en pantalla (128 entradas en total).
   - Costo de CPU por fotograma.
3. **Sacrificios.** Qué tendrías que simplificar o recortar, ordenado de menor a mayor impacto, y qué alternativa propones para cada uno.
4. **Dudas.** Cualquier ambigüedad que encuentres en esta especificación.
5. **Plan.** Archivos y funciones que vas a tocar (por ejemplo `src/bmudisp.c`, `PutUnitSpriteIconsOam`, la carga de paletas del mapa) y en qué orden.

Solo cuando te confirme el plan, implementa.

## Especificación

### Medidas y posición
- La barra mide **14x3 px**: 1 px de borde alrededor y una fila de relleno de **12 px**.
- Va en las **3 filas inferiores** de la casilla de 16x16 de la unidad, centrada en horizontal (1 px libre a cada lado).
- El objeto es de **16x8** y la barra ocupa sus 3 filas de abajo (o la forma que te resulte más eficiente).

### Colores base (valores RGB de 24 bits, que se convierten a 5 bits por canal en la GBA)
| Elemento | Color |
|---|---|
| Borde | `#3A3935` |
| Parte vacía | `#525491` |

### Regla de color del relleno
El relleno es un **degradado horizontal entre dos puntas**.

**Punta izquierda: siempre el color del bando de la unidad.**
| Bando (`UNIT_FACTION`) | Color |
|---|---|
| Jugador `FACTION_BLUE` (0x00) | cian `#50D0D8` |
| Aliado `FACTION_GREEN` (0x40) | verde `#48F848` |
| Enemigo `FACTION_RED` (0x80) | coral `#E87870` |
| 4.º bando `FACTION_PURPLE` (0xC0) | morado `#B868E0` (en Fates este bando comparte color con los enemigos; en mi juego NO, tiene el suyo) |

**Punta derecha.** Se evalúa en este orden y gana la primera condición que se cumple. Las divisiones son enteras, redondeadas hacia abajo:
| Condición | Color |
|---|---|
| `hp <= maxHp / 4` | rojo `#E82020` |
| `hp <= maxHp / 2` | naranja `#E0A048` |
| `maxHp <= 39` | amarillo `#F0F050` |
| `maxHp <= 59` | verde `#48E848` |
| `maxHp <= 79` | azul `#4098F8` |
| `maxHp >= 80` | morado `#B050E8` |

Ejemplo: una unidad con 27 de vida máxima tiene la punta amarilla de 14 a 27 PV, naranja de 7 a 13 PV y roja de 1 a 6 PV.

**Largo del relleno.**
- `relleno = ceil(12 * hp / maxHp)`, con mínimo 1 si `hp > 0`.
- La barra está llena (12 px) **solo** si `hp == maxHp`. Si la unidad perdió aunque sea 1 PV, el relleno es como máximo 11.

**Degradado.**
- Se comprime **dentro de los píxeles llenos**: el primer píxel lleno es siempre el color del bando y el último es siempre el color de la punta derecha.
- Los píxeles vacíos van en `#525491`.
- Con 1 px de relleno, ese píxel usa el color de la punta derecha (el que avisa del peligro).

### Adaptación a la GBA (propuesta, puedes rebatirla)
- El degradado es de **4 pasos** en lugar de 12 tonos: color del bando, 2 tonos intermedios y punta derecha.
- **Una paleta de OBJ por bando** (4 en total), con este reparto: transparente + borde + vacío + color del bando + 6 puntas × (2 intermedios + la punta) = 16 colores.
- Los tonos intermedios se calculan al cargar la paleta (interpolación lineal en el espacio de 5 bits) o se precalculan en tablas constantes.
- Los dibujos de las barras (13 largos × 6 puntas) **no** caben todos en VRAM. Propuesta: reservar unos tiles en la VRAM de OBJ y dibujar ahí solo las combinaciones visibles en ese fotograma, o la alternativa que consideres mejor. Justifícala.

### Comportamiento
- La barra se actualiza en cada fotograma, así que baja apenas la unidad recibe daño.
- Se oculta cuando la unidad no se dibuja: está rescatada, la tapa la niebla de guerra, se está moviendo (`US_HIDDEN` y similares) o un evento oculta los íconos de las unidades.
- Si la unidad está bajo techo o detrás de algo, la barra respeta la misma prioridad que su sprite.
- Las unidades que ya actuaron (sprite en gris) mantienen la barra con sus colores normales.

### Configuración
Todo tiene que quedar en `#define` o tablas `const` al principio del archivo, para poder cambiar:
- Los colores de bando, de punta y de borde y vacío.
- Los umbrales de vida máxima (39 / 59 / 79) y de vida actual (1/2, 1/4).
- La cantidad de pasos del degradado.
- `HPBAR_ONLY_WHEN_DAMAGED` (0 = siempre visible, 1 = solo cuando la unidad está herida).
- `HPBAR_STYLE`, para poder pasar después a un estilo alternativo sin degradado: un color plano por bando que cambia a naranja o rojo con poca vida.

## Entregables (después de confirmar el plan)
1. Un parche (`git diff`) aplicable con `patch -p1` sobre fireemblem8u.
2. Que compile con `make` sin warnings nuevos.
3. Una imagen PNG ampliada con todas las variantes: 4 bandos × 4 tramos × vida al 1, 25, 50, 75 y 100 %.
4. Una lista de lo que se probó y lo que falta probar en mGBA.
