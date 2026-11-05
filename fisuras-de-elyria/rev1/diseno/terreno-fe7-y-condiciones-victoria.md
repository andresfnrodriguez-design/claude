# Terreno real de FE7 y cómo la condición de victoria manda sobre todo

*Datos verificados contra la guía de Triangle Attack para FE7 — no de memoria.*

## La tabla de bonos defensivos (Avo/Def)

| Terreno | Avo | Def | Efecto extra |
|---|---|---|---|
| Arena, Desierto | +5 | +0 | — |
| Casa, Armería, Tienda, Aldea, Ruinas, Arena de combate, Mar, Lago | +10 | +0 | — |
| Bosque, Pilar | +20 | +1 | — |
| Montaña | +30 | +1 | — |
| Pico (Peak) | +40 | +2 | Solo Brigand/voladores pueden pisarlo |
| Fuerte | +20 | +2 | Cura 20% HP máx. por turno |
| Puerta (Gate) | +20 | +3 | Cura 10% HP máx. por turno |
| Trono | +20 | +3 | Cura 10%, restaura estados, +5 Res |

Un dato que cambia cómo pensar el bosque: **da menos defensa que una montaña, pero mucho más movimiento penaliza según la clase** — el bosque es la herramienta para crear fricción pareja entre clases, la montaña es la herramienta para crear una posición defensiva fuerte que solo algunas clases pueden ocupar.

## Costo de movimiento (por tile, agrupado por familia de clase)

| Terreno | Infantería ligera | Blindados | Caballería | Paladines | Nómadas | Voladores | Bandidos/piratas |
|---|---|---|---|---|---|---|---|
| Llanura, camino, puente, arena | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| Aldea destruida | 2 | 2 | 2 | 2 | 2 | 1 | 2 |
| Río | 5 | Impasable | Impasable | Impasable | 5 | 1 | 5 (bandido) / 2 (pirata) |
| Desierto | 2 | 3 | 2 | 2 | 3 | 1 | 2 |
| Bosque | 2 | 2 | 3 | 3 | 2 | 1 | 2 |

**Nota honesta:** la fuente tiene una inconsistencia entre dos filas de "Arena/Sand" — una la lista con costo 1 parejo, otra con costos variables (2-3 según clase). No pude confirmar cuál es la correcta sin acceso al juego, así que no te doy ese número como definitivo — probalo vos mismo en FEBuilder antes de apostarle el diseño de un mapa entero.

**Muros, puertas cerradas y obstáculos** (Outside Wall, Cliff) son impasables para todos menos voladores. Los interiores (Inside Wall, Breakable Wall, Door sin abrir) son impasables incluso para voladores — estos son bloqueos de diseño duro, no terreno difícil.

---

## Ahora la parte que realmente importa: la condición de victoria manda

Esto es lo que separa un mapa que se siente bien de uno que se siente arbitrario. El terreno no se elige por estética, se elige por lo que la condición de victoria le exige al jugador que haga.

**Rout (eliminar a todos):** el mapa entero es el campo de juego, no hay apuro por avanzar a ningún punto específico. Acá el terreno defensivo (fuertes, montañas) se puede repartir generosamente porque el jugador tiene tiempo de jugar a la defensiva si quiere. El río y el bosque como filtros de ritmo funcionan bien acá — ralentizan sin castigar, porque no hay reloj corriendo.

**Seize (tomar el trono):** todo lo contrario. Ahora el terreno que importa es el que está ENTRE el punto de partida y el trono, no el mapa completo. Un Seize con fuertes esparcidos por zonas que el jugador nunca necesita pisar es terreno desperdiciado. Acá conviene concentrar la dificultad en un camino relativamente angosto — ríos y bosques actúan como cuellos de botella reales, no decorativos.

**Defense / sobrevivir X turnos:** el terreno tiene que proteger POSICIONES, no rutas. Fuertes y montañas alrededor del punto que hay que defender, formando un embudo que obligue a los refuerzos enemigos a entrar por pocos accesos en vez de rodear libremente. Si los enemigos pueden llegar por seis lados distintos, no es una defensa interesante, es una carnicería aleatoria.

**Escort (escoltar a alguien):** el terreno alrededor de la unidad escoltada tiene que ser más permisivo que alrededor del resto del mapa — nada de ríos ni bosques pesados en su camino directo, porque ya de por sí esa unidad suele tener movimiento bajo o ninguna capacidad de pelear. El terreno difícil se reserva para los FLANCOS, empujando al jugador a proteger el camino despejado en vez de tener que abrirse paso.

**Boss kill puntual (como buena parte de M1-M39 de nuestro propio diseño):** el terreno le da ventaja al jefe, no al jugador — es lo que hicimos con el afloramiento elevado de M1. La pregunta de diseño acá no es "cómo hago un mapa interesante", es "cómo hago que la ventaja de terreno del jefe se sienta justificada y no injusta".

---

## Aplicado a nuestras propias 40 misiones

Repasando rápido las notas de ambientación que ya tenemos: varias misiones (M8 defensa del campamento, M17 puesto de Brandt, M28 mapa separado de Halvard) son del tipo "resistir/defender" — esas necesitan el enfoque de embudo con terreno defensivo concentrado, no repartido. Las de "combate corto sin objetivo real" como M1 y M30 necesitan lo opuesto: terreno mínimo, justo el que hace falta para que el intercambio no sea dos sprites cruzando campo abierto.

Cuando lleguemos a las misiones más grandes de mitad de juego (M19 "todo a la vez", con presión de varias facciones), ahí sí vale la pena usar el catálogo completo — ríos separando zonas, bosques de transición, quizás un puente como punto de estrangulamiento literal entre dos facciones atacando desde direcciones distintas.
