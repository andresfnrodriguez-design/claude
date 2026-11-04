# Prompts: Aggro Line para Fire Emblem GBA

Tres prompts independientes, pensados para pegarse en orden.
Cada uno pide primero una **evaluación de factibilidad** antes de escribir código.
Rellena los campos entre `[corchetes]` antes de enviarlos.

---

## Prompt 1 — Cálculo de amenazas (lógica)

```
Contexto del proyecto:
- Juego base: [FE6 / FE7 / FE8], versión [US / JP].
- Herramientas: [decomp fireemblem8u / FEBuilderGBA + Custom Build / Skill System / Event Assembler + lyn].
- Otros hacks ya instalados que podrían interferir: [lista o "ninguno"].

Quiero implementar una "aggro line" al estilo de Fire Emblem Engage. Esta primera parte es SOLO la lógica, sin nada visual.

Qué debe hacer:
1. Cuando el jugador selecciona una unidad aliada (al presionar A sobre ella y aparecer su rango de movimiento azul/rojo), calcular qué enemigos podrían atacar la casilla ACTUAL de esa unidad en su próximo turno.
2. "Podría atacar" significa: la casilla de la unidad está dentro de (movimiento del enemigo + rango de alguna de sus armas utilizables). No es una predicción de la IA: no importa si el enemigo realmente elegiría atacarla.
3. Debe respetar: costo de terreno según la clase del enemigo, unidades que bloquean el paso, rango mínimo y máximo de cada arma o tomo del inventario, armas que el enemigo no puede usar (rango de arma, bloqueos) y bastones (no cuentan como ataque).
4. Ignorar enemigos con IA que nunca se mueven SOLO si es fácil detectarlo; si no, tratarlos como cualquier otro y avisarme.
5. Guardar el resultado en una lista accesible (máx. [N, p. ej. 8] enemigos) con, para cada uno: puntero a la unidad y su posición en pantalla, para que otra rutina dibuje las líneas.

Rendimiento:
- No recalcular en cada frame. Calcular una vez al seleccionar la unidad.
- Descartar rápido a los enemigos cuya distancia Manhattan sea mayor que (mov + rango máximo) antes de generar su mapa de movimiento.
- Reutilizar las funciones del juego que ya generan mapas de movimiento y de rango (las del Danger Zone y del rango al seleccionar), sin romper el mapa de movimiento de la unidad seleccionada. Si se pisan los buffers, propón cómo guardarlos y restaurarlos.

ANTES DE ESCRIBIR CÓDIGO, respóndeme con este formato:
1. **Lo que entendí**: resume la funcionalidad en 3 a 5 líneas.
2. **¿Es posible?**: sí / sí con condiciones / no, y por qué.
3. **Funciones y memoria del juego que usarías**: nombres o direcciones concretas para mi versión.
4. **Riesgos**: lag, conflictos con otros hacks, buffers compartidos, casos raros (unidades rescatadas, niebla de guerra, enemigos invisibles).
5. **Qué tendrías que sacrificar o simplificar**, si algo, y alternativas.
6. **Preguntas** que necesites que conteste antes de empezar.

Espera mi confirmación antes de escribir el código.
```

---

## Prompt 2 — Dibujo de las líneas punteadas de 1 píxel

```
Contexto del proyecto:
- Juego base: [FE6 / FE7 / FE8], versión [US / JP].
- Herramientas: [decomp / FEBuilderGBA / etc.].
- Ya existe (o existirá) una rutina que entrega una lista de enemigos que amenazan a la unidad seleccionada, con sus posiciones en el mapa.

Quiero dibujar "aggro lines" estilo Fire Emblem Engage, pero a resolución real de GBA (240x160).

Cómo deben verse:
1. Una línea por cada enemigo que amenaza, desde el centro de su casilla hasta el centro de la casilla de la unidad seleccionada.
2. Línea de 1 píxel de grosor, punteada: 1 píxel encendido cada 3 píxeles (trazado tipo Bresenham), en diagonal o recta según corresponda.
3. Dejar libres unos 6-8 píxeles en cada extremo para no tapar los sprites.
4. Color con buen contraste sobre pasto, camino, el azul del rango de movimiento y el rojo del rango de ataque. Propón uno (amarillo, blanco o puntos alternados blanco/rojo). El rojo puro NO sirve porque se pierde sobre las casillas de ataque.
5. Opcional, solo si no cuesta mucho: animar los puntos desplazándose hacia la unidad.
6. Las líneas deben seguir correctamente al mapa cuando la cámara se desplaza.

Quiero que evalúes DOS enfoques y recomiendes uno:
A) Sprites OAM: cada punto o grupo de puntos como sprite. Límite de 128 sprites compartidos con cursor, unidades y UI.
B) Capa de fondo (BG): generar tiles al vuelo con los píxeles de las líneas en una capa libre. Revisar qué capas usa el juego durante la selección de unidad (mapa, rango de movimiento/ataque, UI) y si queda alguna libre o se puede compartir.
Considera también la VRAM disponible para los tiles y la paleta libre que se usaría.

ANTES DE ESCRIBIR CÓDIGO, respóndeme con este formato:
1. **Lo que entendí**: resumen en 3 a 5 líneas.
2. **¿Es posible?**: sí / sí con condiciones / no, para cada enfoque (A y B).
3. **Recomendación**: cuál enfoque y por qué.
4. **Límites concretos**: cuántas líneas simultáneas soporta, cuánta VRAM, qué paleta y qué capa.
5. **Qué tendrías que sacrificar o simplificar** (por ejemplo, máximo de líneas, sin animación, líneas más cortas, dibujar solo las N amenazas más cercanas).
6. **Preguntas** antes de empezar.

Espera mi confirmación antes de escribir el código.
```

---

## Prompt 3 — Integración dinámica al seleccionar la unidad

```
Contexto del proyecto:
- Juego base: [FE6 / FE7 / FE8], versión [US / JP].
- Herramientas: [decomp / FEBuilderGBA / etc.].
- Ya existen (o existirán) dos partes: (1) la lógica que calcula qué enemigos amenazan a una unidad y (2) la rutina que dibuja las líneas punteadas de 1 píxel.

Quiero integrar ambas en el flujo normal del juego para que funcione de forma dinámica.

Comportamiento esperado:
1. Al presionar A sobre una unidad aliada y aparecer su rango de movimiento (azul) y ataque (rojo), también aparecen las aggro lines desde cada enemigo que puede atacarla.
2. Las líneas se calculan con la posición ACTUAL de la unidad (no se recalculan mientras el jugador mueve el cursor para elegir destino). [Si es viable, como mejora opcional: recalcularlas para la casilla bajo el cursor mientras se elige destino; evalúa el costo por separado.]
3. Las líneas desaparecen al: cancelar con B, confirmar el movimiento, abrir el menú de acción, entrar a un combate o cambiar de fase.
4. No deben aparecer al pasar el cursor por encima de una unidad sin seleccionarla (solo al seleccionarla).
5. Deben convivir sin parpadeos ni glitches con: el rango azul/rojo, la flecha de camino de movimiento, el cursor, las ventanas de información de unidad y terreno, y la cámara desplazándose.
6. Opción para activarlas o desactivarlas desde el menú de Opciones si es razonable; si no, una constante en el código.
7. Debe funcionar igual con niebla de guerra activada (sin revelar enemigos ocultos: los no visibles no generan línea).

ANTES DE ESCRIBIR CÓDIGO, respóndeme con este formato:
1. **Lo que entendí**: resumen en 3 a 5 líneas.
2. **¿Es posible?**: sí / sí con condiciones / no, y por qué.
3. **Puntos de enganche (hooks)**: en qué procesos o funciones del juego conectarías la aparición, actualización y limpieza de las líneas.
4. **Conflictos previsibles**: con la flecha de movimiento, el uso de capas BG y OAM, la UI, la cámara, otros hacks, el rendimiento (lag al seleccionar).
5. **Qué tendrías que sacrificar o simplificar** (por ejemplo, la mejora opcional del punto 2, la opción en el menú, o el soporte de niebla).
6. **Plan de pruebas**: qué escenarios probarías (muchos enemigos, enemigos lejos y cerca, en diagonal y recto, mapa con scroll, niebla).
7. **Preguntas** antes de empezar.

Espera mi confirmación antes de escribir el código.
```
