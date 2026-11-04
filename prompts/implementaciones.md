# Fisuras de Elyria: barras de vida, íconos de amenaza y aggro line en el mapa (FE8 / fireemblem8u)

Trabajo en **Fisuras de Elyria**, un ROM hack de Fire Emblem 8 (The Sacred Stones) hecho sobre la decompilación **fireemblem8u** (C compilado con agbcc, WSL + VS Code, pruebas en mGBA).

Quiero agregar al mapa **tres sistemas visuales** que conviven en pantalla y compiten por los mismos recursos (OAM, paletas de OBJ, VRAM de OBJ, capas BG y CPU):

- **A. Barras de vida** bajo cada unidad, inspiradas en Fire Emblem Fates.
- **B. Íconos** de botín, crítico y efectividad sobre las unidades.
- **C. Aggro line**, inspirada en Fire Emblem Engage: líneas punteadas desde cada enemigo que puede atacar a la unidad seleccionada.

Evalúalos **juntos**, como un solo presupuesto de recursos, no por separado.

**Todo lo visual es provisional (placeholder) y se genera con código.** No hay arte final todavía y no voy a entregar archivos de imagen. Los tiles y paletas de las barras, los íconos (bolsa y `!`) y los puntos de las líneas los defines tú en el código: arreglos `const` de tiles 4bpp y paletas en formato GBA, o funciones que los dibujan píxel a píxel al cargar el mapa. Mantenlos en un archivo o sección separada y bien comentada, para que después pueda reemplazarlos por arte real (PNG convertido con gbagfx) sin tocar la lógica. Indícame en el plan dónde quedarán y cómo se haría ese reemplazo.

---

## ANTES DE ESCRIBIR CÓDIGO: dame feedback

Respóndeme primero, sin implementar nada, con estas secciones:

1. **Lo que entendiste.** Resume cada sistema (A, B y C) con tus palabras: qué muestra, cuándo aparece, sobre quién y dónde va. Incluye la regla de colores y el degradado de A.
2. **Viabilidad.** Para cada sistema: sí / sí con condiciones / no, y por qué. Analiza en concreto:
   - **Paletas de OBJ** libres en FE8 durante el mapa: cuáles usa el juego, cuáles quedan y cómo las repartes entre A, B y C.
   - **VRAM de OBJ** libre en el mapa (hoja de sprites SMS, íconos, cursor, etc.).
   - **OAM**: el límite de 128 entradas con muchas unidades en pantalla y los tres sistemas activos a la vez. Haz la cuenta del peor caso.
   - **Capas BG**: cuáles usa el juego durante la selección de unidad (mapa, rango azul/rojo, UI) y si queda alguna libre o compartible para las líneas de C.
   - **CPU por fotograma** de cada sistema, y qué se calcula una sola vez y se guarda en caché.
   - Cómo detectar la fase en que el jugador eligió una unidad y se ve su rango y la flecha de movimiento: proc, estado o variable global concreta (por ejemplo `gActiveUnit` y el proc de movimiento del jugador).
3. **Sacrificios.** Qué tendrías que simplificar o recortar, ordenado de menor a mayor impacto, indicando a qué sistema afecta y qué alternativa propones.
4. **Conflictos entre sistemas.** Superposición de íconos con la barra, de las líneas con el rango, prioridades de dibujo, choques con los íconos vanilla.
5. **Dudas.** Cualquier ambigüedad que encuentres en la especificación.
6. **Plan.** Archivos y funciones que vas a tocar (por ejemplo `src/bmudisp.c`, `PutUnitSpriteIconsOam`, la carga de paletas del mapa, el proc de selección de unidad) y en qué orden conviene implementar los tres sistemas.

Solo cuando te confirme el plan, implementa.

---

## Especificación A: barras de vida en el mapa (estilo Fates)

### Medidas y posición
- La barra mide **14x3 px**: 1 px de borde alrededor y una fila de relleno de **12 px**.
- Va en las **3 filas inferiores** de la casilla de 16x16 de la unidad, centrada en horizontal (1 px libre a cada lado).
- El objeto es de **16x8** y la barra ocupa sus 3 filas de abajo (o la forma que te resulte más eficiente).

### Colores base (RGB de 24 bits, se convierten a 5 bits por canal)
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
| 4.º bando `FACTION_PURPLE` (0xC0) | morado `#B868E0` (en Fates comparte color con los enemigos; en mi juego NO, tiene el suyo) |

**Punta derecha.** Se evalúa en este orden y gana la primera condición que se cumple. Divisiones enteras, redondeadas hacia abajo:
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
- Se comprime **dentro de los píxeles llenos**: el primero es siempre el color del bando y el último es siempre el color de la punta derecha.
- Los píxeles vacíos van en `#525491`.
- Con 1 px de relleno, ese píxel usa el color de la punta derecha.

### Adaptación a la GBA (propuesta, puedes rebatirla)
- Degradado de **4 pasos** en lugar de 12 tonos: color del bando, 2 intermedios y punta derecha.
- **Una paleta de OBJ por bando** (4 en total): transparente + borde + vacío + color del bando + 6 puntas × (2 intermedios + la punta) = 16 colores.
- Los intermedios se calculan al cargar la paleta (interpolación lineal en 5 bits) o se precalculan en tablas constantes.
- Los dibujos de las barras (13 largos × 6 puntas) **no** caben todos en VRAM. Propuesta: reservar unos tiles en la VRAM de OBJ y dibujar ahí solo las combinaciones visibles en ese fotograma, o la alternativa que consideres mejor. Justifícala.

### Comportamiento
- Se actualiza en cada fotograma: baja apenas la unidad recibe daño.
- Se oculta cuando la unidad no se dibuja: rescatada, tapada por niebla de guerra, en movimiento (`US_HIDDEN` y similares) o cuando un evento oculta los íconos de las unidades.
- Si la unidad está bajo techo o detrás de algo, la barra respeta la misma prioridad que su sprite.
- Las unidades que ya actuaron (sprite en gris) mantienen la barra con sus colores normales.

### Configuración
En `#define` o tablas `const` al principio del archivo:
- Colores de bando, de punta, de borde y de vacío.
- Umbrales de vida máxima (39 / 59 / 79) y de vida actual (1/2, 1/4).
- Cantidad de pasos del degradado.
- `HPBAR_ONLY_WHEN_DAMAGED` (0 = siempre visible, 1 = solo con la unidad herida).
- `HPBAR_STYLE`, para pasar después a un estilo sin degradado: un color plano por bando que cambia a naranja o rojo con poca vida.

---

## Especificación B: íconos de botín, crítico y efectividad

### Íconos vanilla que NO se tocan
El estado alterado (silencio, sueño, berserk, veneno) arriba de la unidad, el ícono de rescate y el de jefe. Los íconos nuevos no deben superponerse con ellos ni tapar la barra de vida de A.

### Ícono 1: bolsa de botín (verde, parpadea)
- **Condición:** la unidad soltará un objeto al morir (`unit->state & US_DROP_ITEM`).
- **Cuándo:** **siempre visible** en el mapa, no solo durante la selección (propuesta: avísame si ves algún motivo en contra).
- **Bandos:** cualquier unidad con la marca (en la práctica, enemigos).
- **Posición:** esquina **inferior izquierda** de la casilla, **por encima** de la barra de vida (al menos 3 px más arriba que sin barra).
- **Parpadeo:** 32 fotogramas visible y 32 oculta (configurable).
- **Choque con el ícono de rescate:** si la unidad tiene los dos, se **alternan** con el mismo ritmo de parpadeo.

### Íconos 2 y 3: los `!` de peligro
**Cuándo:** **solo** mientras el jugador tiene elegida una unidad propia y se ve su rango o la flecha de movimiento. Al confirmar o cancelar el movimiento, desaparecen.

**Sobre quién:** todas las unidades **hostiles a la unidad elegida**, de cualquier bando: las que cumplen `!AreUnitsAllied(unidadElegida, otra)`, incluidos enemigos y 4.º bando.

**`!` amarillo (crítico):** el crítico del **arma equipada** del hostil es igual o mayor que el de la Espada asesina (`GetItemCrit(GetUnitEquippedWeapon(u)) >= HPICON_CRIT_MIN`, 30 en vanilla).

**`!` rojo con fondo blanco (efectividad):**
- El **arma equipada** del hostil es **efectiva contra la clase de la unidad elegida**, usando las tablas del juego (`GetItemEffectiveness` y la lógica de `IsItemEffectiveAgainst` o equivalente), incluidas protecciones como el escudo de Hoplon o el de Fili si existen.
- Ejemplos: martillo contra caballero acorazado, matajinetes contra jinetes, matadragones contra wyverns.
- **Arcos:** se incluyen (solo aparecen al mover un volador). `#define HPICON_EFFECTIVE_INCLUDE_BOWS 1` para poder sacarlos.

**Crítico alto y efectiva a la vez:** los dos `!` se **alternan** con el mismo ritmo que la bolsa (propuesta; dime si prefieres que gane el de efectividad).

**Posición de los `!`:** esquina **superior derecha** de la casilla, sin taparse con el ícono de estado alterado (arriba al centro).

### Gráficos
- 8x8 (o el tamaño que propongas), 16 colores, en una paleta de OBJ compartida o la de los íconos vanilla si alcanza.
- **Bolsa:** verde con borde oscuro. **`!` crítico:** amarillo con borde oscuro. **`!` efectividad:** `!` rojo sobre cuadro blanco con borde oscuro.
- Los tres íconos se generan con código como placeholder (ver la nota del inicio), con esos colores y formas simples. No uses archivos PNG por ahora.

### Configuración
En `#define`: umbral de crítico, inclusión de arcos, ritmo del parpadeo, posiciones (x, y) de cada ícono y prioridad cuando se superponen.

---

## Especificación C: aggro line (estilo Engage)

### Qué calcula
1. Al seleccionar una unidad **del jugador** (al presionar A y aparecer su rango azul/rojo), calcular qué unidades **hostiles** (`!AreUnitsAllied`, mismo criterio que B) podrían atacar la casilla **actual** de esa unidad en su próximo turno.
2. "Podría atacar" = la casilla está dentro de (movimiento del hostil + rango de alguna de sus armas utilizables). No es una predicción de la IA.
3. Debe respetar: costo de terreno según la clase, unidades que bloquean el paso (las del jugador y aliadas bloquean como en el juego normal), rango mínimo y máximo de cada arma o tomo del inventario, armas que no puede usar. Los bastones no cuentan.
4. Casos definidos:
   - Hostiles que no pueden actuar el próximo turno (dormidos, petrificados u otro estado que lo impida): NO cuentan.
   - Balistas y armas de rango especial: cuentan según su rango real.
   - Habilidades que cambian el movimiento (atravesar unidades, Canto, etc.): se respetan si es posible; si no, avísame cuáles quedan fuera.
   - Refuerzos que todavía no aparecen: NO cuentan.
   - Hostiles ocultos por la niebla de guerra: NO generan línea (no se revelan).
   - Hostiles con IA que nunca se mueve: se ignoran solo si es fácil detectarlo; si no, se tratan como cualquier otro y me avisas.
5. Máximo **N líneas** (`#define AGGRO_MAX_LINES`, propón un valor). Si hay más amenazas, se muestran las N más cercanas (distancia Manhattan).

### Rendimiento
- Calcular **una sola vez** al seleccionar la unidad, no en cada fotograma ni al mover el cursor para elegir destino.
- Descartar rápido a los hostiles cuya distancia Manhattan sea mayor que (mov + rango máximo) antes de generar su mapa de movimiento.
- Reutilizar las funciones que ya generan mapas de movimiento y rango (Danger Zone, rango al seleccionar) sin romper el mapa de movimiento de la unidad seleccionada. Si los buffers se pisan, propón cómo guardarlos y restaurarlos.
- Si los `!` de B también necesitan recorrer a los hostiles al seleccionar, comparte ese recorrido y esa caché.

### Cómo se dibuja
1. Una línea por amenaza, del centro de la casilla del hostil al centro de la casilla de la unidad seleccionada.
2. **1 píxel de grosor, punteada:** 1 píxel encendido cada 3 (trazado tipo Bresenham), recta o diagonal según corresponda.
3. Dejar libres unos 6-8 px en cada extremo para no tapar los sprites.
4. **Color** con buen contraste sobre pasto, camino, el azul del rango de movimiento y el rojo del rango de ataque. Propón uno (amarillo, blanco o puntos alternados blanco/rojo). El rojo puro NO sirve: se pierde sobre las casillas de ataque.
5. Opcional, solo si no cuesta mucho: animar los puntos desplazándose hacia la unidad.
6. Las líneas siguen al mapa cuando la cámara se desplaza.
7. Si el hostil está fuera de pantalla, la línea se dibuja recortada hasta el borde.
8. **Orden de capas:** por encima del rango azul/rojo y por debajo de los sprites de las unidades, del cursor y de los íconos de B. Si no es posible, dime qué orden queda.
9. Si la línea pasa por encima de otra unidad, se dibuja igual (queda debajo de su sprite).

Evalúa **dos enfoques** y recomienda uno:
- **Sprites OAM:** cada punto o grupo de puntos como sprite. Compite con A y B por las 128 entradas.
- **Capa BG:** tiles generados al vuelo con los píxeles de las líneas en una capa libre o compartida. Indica la VRAM y la paleta que usaría.

### Cuándo aparece y desaparece
- Aparece al seleccionar una unidad del jugador, junto con su rango.
- NO aparece al pasar el cursor sobre una unidad sin seleccionarla, ni al ver el rango de un enemigo o de un aliado verde.
- Desaparece al cancelar con B, confirmar el movimiento, abrir el menú de acción, entrar a un combate o cambiar de fase.
- Convive sin parpadeos con el rango, la flecha de movimiento, el cursor, las ventanas de información de unidad y terreno, y el desplazamiento de la cámara.
- Mejora opcional, evaluada aparte: recalcular las líneas para la casilla bajo el cursor mientras se elige destino. Dime su costo.
- Opción para activarla o desactivarla desde el menú de Opciones si es razonable; si no, `#define AGGRO_ENABLED`.

### Referencia visual
Adjunto `aggro-a-sel-x4.png` y `aggro-b-sel-x4.png` (ampliadas x4) y sus versiones a tamaño real 240x160: unidad seleccionada con su rango y las líneas. **Las líneas de las imágenes son rojas, pero ese no es el color final** (ver punto 4). Las imágenes no incluyen las barras de A ni los íconos de B.

---

## Entregables (después de confirmar el plan)
1. Un parche (`git diff`) aplicable con `patch -p1` sobre fireemblem8u, con los tres sistemas. Si conviene, en commits o parches separados por sistema, que se puedan aplicar juntos.
2. Que compile con `make` sin warnings nuevos.
3. Imágenes de verificación:
   - Todas las variantes de la barra: 4 bandos × 4 tramos × vida al 1, 25, 50, 75 y 100 %.
   - Una casilla con todos los íconos y la barra a la vez, para comprobar que no se tapan.
   - Una escena con una unidad seleccionada, su rango, aggro lines, `!` y barras a la vez.
4. Una lista de lo que se probó y lo que falta probar en mGBA. Por ejemplo:
   - Elegir un paladín cerca de un enemigo con matajinetes: aparece el `!` blanco y su aggro line, y ambos desaparecen al cancelar.
   - Mapa con muchos enemigos en pantalla: que no falten sprites ni haya lag al seleccionar.
   - Enemigos cerca y lejos, en recto y en diagonal, fuera de pantalla y con niebla de guerra.

---

## Prueba final: escenario de pruebas en el mapa de debug o en el prólogo

Cuando los tres sistemas estén implementados (y solo después de que yo apruebe el plan), prepara un escenario para probarlos todos en mGBA sin tener que jugar varios capítulos.

1. **Dónde:** usa el mapa de debug si el proyecto tiene uno accesible; si no, el capítulo del prólogo. Dime cuál elegiste y por qué, y cómo se llega a él desde el inicio del juego. Los cambios de prueba deben quedar aislados (por ejemplo detrás de un `#define AGGRO_TEST_MAP` o en un archivo de eventos aparte), para poder quitarlos sin tocar la lógica de los sistemas.
2. **Unidades del jugador:** al menos un jinete (paladín o caballero), un volador (pegaso o wyvern) y una unidad de infantería con espada.
3. **Enemigos**, colocados para cubrir todos los casos:
   - Cerca y lejos de las unidades del jugador, en línea recta y en diagonal.
   - Al menos uno fuera de la pantalla inicial, para probar el recorte de la línea.
   - Uno con matajinetes, uno con arco y uno con martillo (efectividad).
   - Uno con Espada asesina u otra arma de crítico alto, y uno con un arma que sea a la vez de crítico alto y efectiva (alternancia de los `!`).
   - Uno o dos con objeto para soltar (bolsa de botín), y uno que además lleve a alguien rescatado (alternancia con el ícono de rescate).
   - Uno dormido o petrificado (no debe generar línea).
   - Uno fuera de alcance (no debe generar línea).
   - Suficientes enemigos en pantalla para probar el peor caso de sprites (OAM).
4. **Otros bandos:** al menos un aliado verde y una unidad del 4.º bando, para verificar los colores de las barras y que las aliadas no generen línea ni `!`.
5. **Vida variada:** unidades con vida máxima en cada tramo (hasta 39, 40-59, 60-79 y 80 o más) y con la vida actual en distintos porcentajes, para ver todos los colores de la barra.
6. **Niebla de guerra:** si el mapa elegido no la tiene, indica cómo activarla para probar que los enemigos ocultos no generan línea.
7. **Lista de comprobación:** entrégame una lista paso a paso de qué hacer en mGBA y qué debería verse en cada paso (por ejemplo: "selecciona al paladín → aparecen 3 líneas y el `!` blanco sobre el enemigo con matajinetes; presiona B → desaparecen").
