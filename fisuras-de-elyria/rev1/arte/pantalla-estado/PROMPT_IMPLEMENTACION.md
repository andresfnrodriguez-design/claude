# Prompt para Claude Code (VS Code) — Pantalla de estado de *Fisuras de Elyria*

> Copia todo este archivo como prompt en Claude Code, abierto en la carpeta del decomp del juego.
> Junto a este archivo están las referencias visuales (`tema_gris_final_fisuras_fucsia.png`,
> `tema_gris_final_r3_fisuras_fucsia.png`, `anim_gris_final_fisuras_fucsia.gif`) y el generador
> `generar.py` / `recolorear.py`, que es **la fuente de verdad** de cada coordenada y color.

---

## 1. Tarea

Reemplazar la **primera página de la pantalla de estado** (stat screen) del juego, que está construido
sobre el decomp de Fire Emblem 8 (`fireemblem8u`), por un diseño nuevo de 240×160 px.
El diseño ya está cerrado: el objetivo es que el resultado en el emulador sea **idéntico píxel a píxel**
a `tema_gris_final_fisuras_fucsia.png` (Kairos) y `tema_gris_final_r3_fisuras_fucsia.png` (otro retrato),
con los datos reales de la unidad.

Antes de escribir código:
1. Lee cómo el decomp arma la stat screen (busca `statscreen`, `StatScreen`, `gStatScreen`, el proc que
   dibuja la página 0 y el que cambia de página con L/R) y cómo carga fondos, paletas, OAM y texto.
2. Lee `generar.py` completo: cada bloque comentado corresponde a un elemento de esta especificación.
3. Propón un plan (capas, VRAM, paletas, qué reutilizas del motor) y espera mi OK antes de implementar.

No cambies la lógica de juego ni otras páginas salvo lo necesario para enganchar esta.

---

## 2. Reglas generales

- Resolución 240×160, colores **RGB555** (los valores RGB de abajo ya están cuantizados a 5 bits).
- **El blanco del texto (`#F8F8F8` / `0x7FFF`) es fijo** en todos los temas.
- Origen (0,0) arriba a la izquierda. Las cajas son `[x0, y0, x1, y1]` **inclusivas**.
- Todo lo marcado como *placeholder* es un ícono que se reemplaza por los íconos reales del juego
  (tienen su propia paleta, no forman parte de la paleta de la UI).
- Alineaciones se miden por **la tinta real** de los glifos (no por el avance de la fuente).

---

## 3. Capas propuestas (modo 0)

| Capa | Contenido | Notas |
|---|---|---|
| BG3 | Fondo "fisuras": degradado diagonal teal→fucsia | estático, tiles + 1–2 paletas de 16 |
| OBJ (prioridad detrás de BG2) | **Esquirlas** (triángulos) del fondo, animadas | sprites 8×8/16×16/32×16 |
| BG2 | Retrato grande | 1 paleta de 16 (15 colores + transparente) |
| BG1 | Paneles translúcidos: semicírculo, franja HP, fondo de stats, relleno del banner | se mezclan con BLDCNT |
| BG0 | Texto, números, barras, contornos opacos, botones | sistema de texto del juego o tiles propios |
| OBJ (delante) | Flechas `<` `>` animadas, íconos de armas/hechizos/ítem | |

Si el motor ya usa las capas de otra forma, adapta, pero respeta el orden visual:
fondo → esquirlas → retrato → paneles translúcidos → UI opaca/texto → flechas.

### Transparencias (importante)
La GBA tiene **un solo** par de coeficientes de mezcla (EVA/EVB) para toda la pantalla, pero el diseño
usa varias opacidades:

| Elemento | Opacidad del negro/color sobre lo de atrás |
|---|---|
| Semicírculo negro (derecha) | 45 % |
| Franja negra del HP | 86 % |
| Fondo de stats | 80 % en x=0 → 0 % en x=63, lineal |
| Relleno naranja del banner del arma | 40 % (naranja sobre lo de atrás) |

Propón cómo resolverlo. Opciones válidas: un único EVA/EVB y el resto con **tramado** (patrón Bayer de
píxeles opacos) en la capa BG1; usar la ventana (WIN0/WIN1) para separar regiones; o cambiar EVA/EVB
por scanline con HDMA (sirve para variaciones verticales, no horizontales). El degradado horizontal de los
stats **no** se puede hacer con alfa por píxel: usa tramado o 4–6 franjas de 8 px con densidad decreciente.
Muéstrame el resultado comparado con la referencia antes de cerrar.

---

## 4. Paleta de la UI (tema `gris_final`)

| Uso | RGB | GBA BGR555 |
|---|---|---|
| Texto valores (blanco fijo) | (248,248,248) | 0x7FFF |
| Etiquetas (HP, ATK, SKL, SPD, LCK, DEF, RES, MOV, LV, EXP) | (184,184,192) gris neutro | — |
| Texto del banner del arma | (248,248,248) | 0x7FFF |
| Paneles grises (rampa oscuro→claro) | (12,12,16) (44,44,52) (96,96,108) (160,160,172) (232,232,236) | — |
| Contorno opaco del banner | (240,120,40) naranja | — |
| Línea por fuera del contorno del banner | (16,8,8) | — |
| Relleno del banner (rampa, 40 % de opacidad) | (96,32,8) (200,72,16) (232,104,32) (248,140,56) | — |
| Flechas | negro (0,0,0) + brillo (88,88,96); en la izquierda brillo 2º y 3º píxel (150,150,160) y contorno (88,88,96) | — |
| Placas LV/EXP | gris oscuro de la rampa | — |
| Fondo fisuras | teal (40,150,150) → fucsia (200,24,96), centro oscurecido hacia (14,26,30) | — |

Los valores exactos de cada píxel salen de `recolorear.py` aplicado a `generar.py`; ante cualquier duda,
**muestrea la imagen de referencia**.

---

## 5. Elementos, posiciones y lógica

### 5.1 Fondo "fisuras" (BG3 + esquirlas)
- Degradado diagonal a **30°**: `u = (x + 1.732·y) / (240 + 1.732·160)`; color = lerp(teal, fucsia, u);
  luego oscurecer hacia (14,26,30) con `k = max(0, 1 − |u − 0.5| / 0.35) · 0.75`.
- **Esquirlas**: 40 triángulos (lado 6–22 px, aplastados 0.6 en vertical), semilla fija.
  - Se mueven **muy lento** (0,15–0,35 px por cuadro de animación), **cada una en su propia dirección**,
    con un giro mínimo; al salir por un borde reaparecen por el opuesto.
  - **Su color es el del fondo que tienen detrás en ese momento**, ×1,35 o ×0,7, con tope 200 por canal:
    sobre teal solo hay esquirlas teal, sobre fucsia solo fucsia; **nunca blancas**.
  - En hardware: sprites con un pequeño set de formas pre-rotadas (o affine con pocas matrices);
    el color se puede resolver eligiendo entre 3–4 paletas de sprite según la zona (teal / centro / fucsia).
- Solo se mueven las esquirlas; el degradado y la UI quedan quietos.

### 5.2 Retrato (BG2)
- Imagen grande que sangra por debajo de la UI; el punto medio entre los ojos cae en ~(110, 84).
- 15 colores + transparente, **1 píxel del arte = 1 píxel de pantalla** (sin escalar).
- Cada unidad tendrá su retrato grande (no es el mug de 96×80 de FE8). Prepara un formato/tabla por unidad
  con: tiles, mapa, paleta y offset (x, y). Ejemplos: `retrato_busto.png` (Kairos) y `retrato_3.png`.

### 5.3 Barra superior (y 0–12)
- Degradado horizontal claro (izq.) → oscuro (der.) en la rampa gris; línea oscura en y = 13.
- **Flechas de cambio de página** (sustituyen a "L" y "R"; sin letras):
  - Forma: punta rellena con muesca, caja 9×11, puntos `(0,1) (3,1) (8,6) (3,11) (0,11) (4,6)` para `>`;
    espejo para `<`. Negra, brillo en (1,2) (2,2) (3,3) (4,4).
  - `<` en x = 2, `>` en x = 229, y = 1–11.
  - **Compensación óptica**: la de la izquierda está sobre fondo claro → contorno gris (88,88,96) solo en
    sus 4 columnas izquierdas (la punta) y brillo con el 2º y 3º píxel más claros (150,150,160).
  - **Animación**: se desplazan 1 px hacia afuera y vuelven, alternando cada ~3 cuadros de la animación
    de las esquirlas (lento). Indican que L/R cambia de página.
- **Nombre** de la unidad: x = 40, y = 0, dibujado dos veces (x y x+1) para que sea más grueso, blanco.
- **LV**: placa redondeada [140,2,156,11] con "LV" un punto más chico, centrado; valor alineado a la
  derecha en x = 170.
- **EXP**: placa [178,2,198,11] con "EXP" igual; valor alineado a la derecha en x = 219.

### 5.4 HP (franja negra, y 14–30)
- Franja negra translúcida [0,14,150,30] con el extremo derecho curvo (ver `generar.py`, bloque "HP: franja").
- Etiqueta "HP" en fuente mini 3×5 en (8, 19).
- HP actual: número grande (≈11 px de alto), tinta empezando en (19, 17).
- "/" recta en escalones 1:2, de (45,19) a (42,26).
- HP máximo: número chico (≈7 px de alto), tinta empezando en (48, 19).
- Barra [65,19,87,24]: **blanca** en la parte proporcional `round(23 · HP / HPmax)` px desde la izquierda,
  **gris (96,96,104)** en el resto.

### 5.5 Clase y tipos de arma
- Nombre de la clase alineado a la derecha en x = 213, y = 18 (ej. "Artifice"/"Artífice").
- Dos íconos de **tipo de arma que puede usar la clase** en x = 218 y 227, y = 20 (7×8) — *placeholder*.

### 5.6 Banner del arma equipada
- Figura = placa redondeada [64,32,176,42] (radio 5) ∪ elipse [66,28,174,46] (≤ 0,9 del radio):
  simétrica en ambos ejes.
- Relleno naranja **translúcido (40 %)**, más claro al centro y más oscuro hacia los extremos.
- Contorno de 1 px **naranja opaco** (240,120,40) + 1 px oscuro (16,8,8) por fuera (separa el banner de
  cualquier retrato).
- **Texto del nombre del ítem centrado** en la figura (por tinta), blanco.
- **Ícono del ítem** (10×10, *placeholder* = círculo) a la izquierda del texto, separado 4 px.
- El arco gris del semicírculo que cruza el banner **no** se pinta de naranja.

### 5.7 Stats (columna izquierda)
- Bloque de 7 filas (ATK, SKL, SPD, LCK, DEF, RES, MOV), paso 10,5 px, primera fila en y = 57.
- Etiquetas: **inicio de la tinta** alineado en x = 4, gris neutro.
- Valores: **final de la tinta** alineado en x = 41, blancos.
- Bonificación (ej. DEF +3): etiqueta blanca en forma de flecha [44..56] a la altura de DEF, con "+3"
  en fuente mini 3×5 oscura. Solo aparece si hay bonus.
- Fondo: negro translúcido de [0, 57] a [63, 131], **80 % en x=0 que baja lineal a 0 % en x=63**.
- Mapeo de datos de FE8: ATK = Pow/Str (o Mag según arma), SKL, SPD, LCK, DEF (+bonus), RES, MOV.

### 5.8 Semicírculo y hechizos/habilidades (derecha)
- Círculo negro translúcido (45 %) de centro (337, 85) y radio 180, con contorno claro (232,216,216)
  y un segundo anillo oscuro (120,32,48) a r + 3.
- Lista de **magias/habilidades de la unidad** (hasta 5), una por fila: y0 = 48, paso 12 px.
  - Cada ícono 7×7 (*placeholder*): su **esquina superior izquierda** está sobre la línea blanca del arco
    **desplazada 11 px a la derecha** (mismo y). Compensación óptica: fila 3 un píxel a la izquierda,
    fila 5 un píxel a la derecha.
  - Texto a 10 px a la derecha del ícono, blanco.
  - Si la unidad no tiene más entradas, la fila muestra "????" (o se oculta, a definir).

### 5.9 Botones inferiores
- 4 botones redondeados (radio 5) de 22×20 en x = 4, 27, 51, 74 (paso 23,5), y = 139–158, degradado
  vertical gris + borde. Íconos **blancos de 12×12 centrados por su silueta** (fuego, frasco, espadas,
  gota de `iconos_skills.webp`): son accesos/íconos de habilidad — *placeholder* de funcionalidad.
- Recuadro derecho [193,139,236,158] con ícono (círculo) y número grande "3" — contador/indicador
  (conservar el que use la página original o definir).

---

## 6. Datos que hay que leer de la unidad

Nombre, clase, nivel, experiencia, HP actual/máximo, los 7 stats (y bonus por ítem/estado), arma
equipada (ícono + nombre), tipos de arma de la clase, lista de magias/habilidades, retrato grande.
Usa las funciones/estructuras del decomp (`GetUnit…`, `GetItem…`, `GetClass…`, etc.).

---

## 7. Entregables

1. Código de la nueva página enganchada a la stat screen (cambio de página con L/R funcionando).
2. Script/regla de build que convierta los PNG (fondo, retratos, íconos, flechas, esquirlas) a tiles,
   mapas y paletas (grit o la herramienta que use el decomp).
3. Captura del emulador comparada con la referencia (superposición 50 %) para Kairos y para otro retrato.
4. Lista de lo que no se pudo replicar exacto en hardware y cómo se aproximó.
