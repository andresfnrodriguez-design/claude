# Algoritmo de diseño de mapas — Fisuras de Elyria (v2, con fuentes específicas de FE)
*Síntesis de nueve fuentes reales. Las primeras tres son de diseño de cartografía táctica en general (TTRPG de mesa); las seis restantes son específicas de Fire Emblem, más precisas y accionables para nuestro caso. Reddit r/mapmaking y la wiki de r/rpg quedaron bloqueadas para mi acceso, no están incluidas.*

## Fuentes
1. An Angry Guide to Practical Cartography (The Angry GM)
2. Logical Dungeon Design: Tactical Cartography (Roleplaying Tips) — solo tabla de contenidos, libro de pago sin acceso al detalle
3. Pillars of Tactical RPG Design (Michael Burnam-Fink) — modelo OODA
4. Tactical RPG — Game Design Document 1 (Heathrileyo) — estructura de documentación por nivel
5. Hilo de Reddit r/fireemblem sobre por qué Conquest cap. 10 es bueno, con debate extenso
6. Hilo de Reddit r/fireemblem de brainstorm ("¿qué mapa diseñarías vos?")
7. Video "Map Design 101: Monotype Maps" (Mithril Zenith)
8. Video de diseño de mapas de Mangs — la referencia más citada de la propia comunidad de FE
9. "Map Design and You" y "Map Design Discussion Thread" (FEUniverse) — las dos guías técnicas más detalladas y con ejemplos reales de mapas de juegos oficiales

---

## Corrección importante a lo que veníamos asumiendo: "más grande" no es igual a "mejor"

Esto es una corrección real, no solo un agregado. Cuando dijiste que nuestros mapas eran muy chicos, los agrandé bastante (20x13, 22x14, 24x16). Pero **tres fuentes distintas de FE específicamente advierten contra el error opuesto**: "Map Design and You" dice textualmente que la gente asume que "los mapas grandes son más geniales", cuando en realidad "estos mapas suelen estar repletos de espacio muerto" — la solución casi siempre es cortar tamaño, no llenarlo de decoración. Mangs es todavía más directo: la mayoría de sus quejas sobre hacks son mapas demasiado largos, especialmente en las primeras misiones, y remarca "debería haber algo pasando en cada rincón del mapa, si no, es espacio desperdiciado."

**La reconciliación real:** el tamaño correcto no es "chico" ni "grande" — es "lo suficientemente grande para que la CombatScape (el espacio de maniobra táctica) respire, ni un tile más." Anouleth, en el hilo de Reddit, da un número concreto: mapas diseñados para completarse en **4-6 turnos jugados eficientemente**, con el objetivo principal a **no más de 30-40 casillas de distancia** en el early-mid game (esto limita de paso el poder de Warp y voladores). Nuestros mapas de Parte I, siendo misiones tempranas, deberían estar en el extremo más chico de ese rango, no en el más grande.

También hay un dato técnico específico que se me había pasado: los valores de movimiento de la escala GBA (los que usamos nosotros) son más bajos que los de juegos como FE1/FE11 o Genealogy — así que un mapa "grande" de esos juegos, adaptado tal cual a nuestra escala, se sentiría insoportablemente lento de cruzar. El tamaño tiene que calibrarse contra el movimiento real de nuestras clases, no copiarse de otro juego con estadísticas distintas.

## El proceso: dibujar el camino crítico primero

De "Map Design and You": antes de decorar nada, dibujar una línea simple desde el inicio del mapa hasta el objetivo. Todo lo que no toca esa línea ni la modifica es "espacio muerto" candidato a eliminarse. La forma más fácil de arreglar un mapa con mucho espacio muerto es, simplemente, reducir su tamaño.

**Regla derivada, de FlamingZelda (FEUniverse):** está bien tener mucho terreno con penalidad (bosques, ríos, colinas) siempre que NO estén todos apilados sobre el camino crítico. El terreno friccioso vive en las zonas opcionales de exploración; el camino principal se mantiene relativamente despejado para que avanzar no se sienta como caminar en melaza.

## Anti-patrones con nombre propio (para poder señalarlos rápido de acá en más)

- **One-tiling:** un pasaje de un solo tile de ancho (una puerta, un puente, una grieta) genera un embotellamiento real — las unidades hacen fila en vez de maniobrar. Cuidado también con el one-tiling **diagonal** (dos tiles impasables que se tocan solo por la esquina). Solución: al menos dos tiles de ancho en cualquier cuello de botella — **salvo que sea una excepción deliberada** (ver más abajo, nuestro M6 con el callejón es un caso justificado, no un error).
- **Fly-skipping:** cuando un terreno pensado para frenar unidades terrestres no sirve de nada porque los voladores simplemente lo cruzan por arriba. Se arregla con terreno que ni los voladores puedan cruzar, o con arqueros/magia de viento/ballistas que específicamente amenacen a quien vuele.
- **Terrain spam:** demasiado terreno de penalización EN SECUENCIA, que convierte cruzar una zona en un arrastre. Se arregla sacando algo de terreno, no agregando más.
- **Espacio muerto:** cualquier área del mapa que el jugador nunca visita ni usa. Se corrige recortando el tamaño del mapa, no llenándolo de decoración que no cambia nada.
- **Ambush spawns (refuerzos que se mueven y atacan el mismo turno que aparecen):** confirmado como mal diseño por TRES fuentes independientes de esta investigación. Regla dura de acá en más: nunca en nuestras 40 misiones. Si hay refuerzos, se telegrafían — el jefe amenaza con ellos, o el jugador recibe alguna pista — y aparecen con al menos un turno de aviso antes de poder actuar.

## Diseño según el tipo de objetivo (de Map Design and You)

- **Sellar / Derrotar al jefe:** debería ser más lineal que otros tipos (sin llegar a ser un pasillo recto) — el objetivo es ir de A a B, así que evitar impedimentos de terreno excesivos en el camino.
- **Aniquilar:** objetivo más abierto, ya que hay que llegar a todos los enemigos — pero cuidado con que "abierto" se vuelva "vacío y aburrido de cruzar" (cita Awakening y Birthright como ejemplos de este problema).
- **Defender:** permite mapas más cerrados — pero ojo, **una sola casilla tapada con un tanque no es más divertida en un mapa de defensa que en cualquier otro lado**. Villages/cofres siguen siendo la herramienta correcta para incentivar avanzar en vez de atrincherarse.

## El modelo OODA aplicado (Pillars of Tactical RPG Design)

El punto más aplicable para nosotros es **Decide**: ni parálisis por exceso de opciones, ni "la respuesta obvia" sin tensión real. Un buen mapa da 2-4 rutas genuinamente comparables. Esto conecta directo con el criterio de las 4 cualidades de abajo.

## Las 4 cualidades de un mapa sólido (FEUniverse, con ejemplos reales de juegos oficiales)

1. Más de una forma de progresar.
2. Áreas abiertas donde las unidades puedan enfrentarse (y curarse/comerciar entre sí).
3. Pasillos o callejones que el jugador PUEDA convertir en cuellos de botella si quiere — no que esté forzado a hacerlo.
4. Terreno con el que jugar y que dé ventaja, pero que no trabe el avance del camino principal.

**No hace falta que un mapa tenga las 4 para ser bueno — pero si le falta alguna, tiene que ser la excepción deliberada, no el estándar.** Nuestro M6 (el callejón angosto, sin flancos) es un ejemplo legítimo de excepción: rompe la regla de one-tiling y la cualidad #3 a propósito, porque la escena narrativamente pide justo eso — un enfrentamiento sin salida. Eso lo hace una excepción justificada, no un error.

**Excepciones legítimas adicionales, con ejemplos reales:** capítulos tutoriales (decoración mínima a propósito, para enseñar lo básico sin ruido), capítulos "válvula de escape" en medio de una campaña larga (campo abierto, sin presión de objetivo, simplemente para que el jugador disfrute pelear después de muchas misiones tensas), y capítulos que son casi cinemáticas jugables (el diseño de bajo impacto táctico es aceptable si la escena es sobre el impacto narrativo, no sobre el rompecabezas).

## El diagnóstico rápido: "como se ve el mapa, así juega"

Heurística directa de FlamingZelda: si un mapa SE VE denso y apretado, VA A JUGAR denso y apretado. Si se ve disperso y vacío, así va a jugar. Sirve como autochequeo rápido antes de dar un mapa por terminado — mirarlo con ojos frescos y preguntarse qué promete visualmente, después confirmar que el gameplay cumple esa promesa (ni más denso ni más vacío de lo que se ve).

## Lo más importante de todo: el mapa es solo la mitad de la batalla

De la fuente más rica de esta tanda (FEUniverse, análisis de FE9 "Blood Runs Red"): la diferencia entre un mapa bueno y uno inolvidable casi nunca está en el layout del terreno — está en el diseño de encuentro que se le pone encima. El caso de estudio real: un mapa objetivamente simple (tres caminos, nada de fancy) se vuelve una de las misiones más recordadas de la saga porque (a) los refuerzos de wyvern obligan a que cada escuadrón que el jugador arme tenga alguien cuidando la retaguardia, y (b) a mitad de mapa, el antagonista principal del juego sale caminando de una de las casas que el jugador ya había visitado, convirtiendo en tiempo real un "matar al jefe" en un "sacar a todos con vida". El terreno no cambió una sola casilla — lo que cambió todo fue el evento narrativo puesto exactamente ahí.

**Aplicado a nosotros:** ya tenemos el material perfecto para esto — Selene en M38, Halvard en M28/M30, la propia estructura de traiciones escalonadas. La pregunta correcta para las misiones de mayor peso no es solo "¿qué terreno pongo?" sino "¿qué evento puedo hacer que ocurra EN el mapa, en el momento justo, que una la tensión mecánica con la tensión narrativa?"

## Sobre mapas de un solo tipo de enemigo (monotype)

Útiles como herramienta de enseñanza temprana (aislar una sola mecánica, como el triángulo de armas, contra un solo tipo de enemigo) — pero fallan en el midgame si no tienen una válvula de escape o un propósito narrativo claro. El ejemplo de fracaso citado (Wooden Cavalry, FE11) es un mapa monotype de ballistas donde NINGUNA estrategia del jugador se siente satisfactoria. El ejemplo de éxito narrativo (Kitsune Layer, Conquest) es un monotype deliberadamente punitivo que funciona PORQUE la miseria mecánica refuerza el peso emocional de la escena.

## No todas las misiones necesitan ser una obra maestra

Permiso explícito, y realista, de la última fuente: está perfectamente bien que la mayoría de las 40 misiones sean simplemente "buenas" o "sólidas" — el objetivo no es que las 40 sean un Conquest capítulo 10. Guardar el esfuerzo de diseño más inspirado para los puntos de la trama que genuinamente lo piden (los que ya identificamos: M20, M30, M35, M39) es más sano que intentar que cada misión individual sea perfecta.

---

## El algoritmo completo, actualizado

1. **Clasificar el tipo de mapa** (Práctico vs. Táctico vs. Artístico — Angry GM). Solo el Táctico necesita todo lo que sigue.
2. **Dibujar el camino crítico primero.** Todo lo que no lo toca es candidato a espacio muerto — cortarlo, no decorarlo.
3. **Dimensionar contra el objetivo, no contra un número fijo.** Referencia: 4-6 turnos eficientes, ~30-40 casillas para misiones tempranas, calibrado contra el movimiento real de nuestras clases GBA, no copiado de otro juego.
4. **Chequear las 4 cualidades** (múltiples rutas, áreas abiertas de combate, cuellos de botella opcionales, terreno que no trabe el camino principal). Cualquier ausencia debe ser una excepción justificada por la escena, no un descuido.
5. **Filtrar terreno por función mecánica real**, evitando específicamente one-tiling (incluso diagonal), fly-skipping, y terrain spam.
6. **Nunca ambush spawns.** Refuerzos siempre telegrafiados, con al menos un turno de aviso.
7. **Preguntar qué EVENTO puede ocurrir en el mapa** que una la tensión mecánica con la narrativa — no solo qué terreno poner.
8. **Autochequeo final:** ¿el mapa juega como se ve? ¿Y es de verdad necesario que esta misión sea excepcional, o está bien que sea sólida y ya?
9. Mantener zonas de despliegue/reclutamiento reales, dimensionadas al roster de esa misión (ya establecido, se mantiene).
