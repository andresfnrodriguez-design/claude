# Fisuras de Elyria — Diseño de mecánicas

Documento vivo, compañero de `BIBLIA.md`. Mismos estados: CANON / PROPUESTA / ABIERTO.

## 1. Último capítulo y epílogo dinámico (PROPUESTA)

Misión de rescate en los escombros después del clímax: combate fácil, presión por límite de turnos.

| Rescatados | Epílogo |
|---|---|
| Ninguno o uno | Final derrotista |
| Varios | Final normal |
| Todos (muy difícil) | Final apenas mejor: una palmadita, no otro final |

- Entre los atrapados hay caras conocidas (campamento, secundarios de capítulos paralelos).
- El epílogo nombra a los que no se rescataron (registro de Demetria), sin comentario.
- **New Game+:** los rescatados de la partida anterior aparecen en la nueva; al hablarles se unen o dan objetos poderosos. Requiere que esos personajes tengan presencia antes del último capítulo.
- Riesgo a vigilar: "rescatar a todos" no debe depender de información que solo da una guía. Debe poder deducirse en el mapa.

**Reglas de implementación (propuesta):**
- Sin azar y sin muerte guionada. Lo difícil sale del diseño del mapa.
- La victoria no es derrotar al jefe ni tomar un punto: el capítulo termina en un turno fijo o al rescatar al último. Ganar rápido no saltea el rescate.
- Rescatar cuesta acciones: cada persona atrapada necesita una unidad que "excave" en casillas adyacentes durante 1-2 turnos. Varias personas, repartidas lejos entre sí.
- El terreno empeora cada turno (derrumbes que bloquean caminos), así que el orden importa.
- Definir qué pasa con bastones de teletransporte, bailarines y movimiento extra: limitarlos en ruinas o contarlos en el diseño del límite de turnos.
- Si el jugador rescata a todos antes del límite, el capítulo termina y obtiene el epílogo "palmadita". Es legítimo: lo ganó.
- Lo que nunca se puede salvar no está en el mapa: el registro de Demetria nombra a gente de otros lugares (fuera de alcance), no a fichas inalcanzables.

**Quiénes están atrapados:**
- Cada rescatable aparece al menos dos veces antes: campamento, conversaciones de base, capítulos paralelos o rescatados de la misión de la evacuación dividida.
- Su presencia en el mapa final tiene que estar justificada por la historia: viajan con el convoy, viven en la zona del clímax o fueron rescatados antes y se quedaron cerca.

## 2. Jefes con varias barras de vida (PROPUESTA, estilo Engage)

- Evita matar al jefe en uno o dos ataques; obliga a planear.
- Normal: jefes comunes 1 barra, jefes de Parte 2, jefe final 3.
- Difícil: una barra más para cada tipo (2 / 3 / 4).
- Vigilar que el jefe final con 4 barras no se vuelva tedioso: cada barra debería cambiar algo.
- ABIERTO: qué pasa al romper una barra (cambio de patrón, refuerzos, cambio de música).

## 3. Veneno (PROPUESTA)

- Estado acumulable (stacks). Daño al inicio de cada turno:

| Stacks | Daño por turno |
|---|---|
| 1 | 1 |
| 2 | 3 |
| 3 | 5 |

- La curva crece más rápido que lineal: el jugador tiene que curar antes del tercer stack.
- **Puede matar** (decidido por ahora).
- ABIERTO: tope de stacks (¿3?), cómo se quita (antídoto, bastón, desaparece solo) y si baja un stack por turno.
- Encaje temático: un estado que persiste le da peso a curar, es decir, a no dejar a nadie atrás.

## 4. Música dinámica (PROPUESTA)

- En capítulos con una escena guionada que cambia el mapa o el objetivo, la música cambia en ese momento.
- Puede ocurrir en el mapa, en una escena durante la misión o justo después de una escena cuyo guion cambia la dinámica de la misión.
- Candidatos: rotura de barra del jefe, colapso de la fisura, traición en mapa, llegada de refuerzos.
- Las transiciones no deben ser cortes bruscos: preparar pistas pensadas para enlazarse.

## 5. Dificultad dinámica (PROPUESTA, estilo Engage)

- Solo en modo difícil. Quien lo elige busca un reto.
- Nunca se le dice al jugador: la sensación buscada es que el desafío está atado a cómo juega.
- Objetivo: que entrenar de más no vuelva el juego trivial (una unidad sola barriendo el mapa sin tensión).
- Toma el promedio de nivel de todas las unidades y ajusta estadísticas, objetos o habilidades enemigas.
- ABIERTO: rango y tope del ajuste. Que la variación sea moderada.
- Complemento: limitar las fuentes de experiencia infinitas (escaramuzas, arena) ataca el entrenamiento excesivo de raíz.
- Solo sube. Si el jugador va mal, la dificultad es la base.
- Encaje: con despliegue obligatorio, el promedio es de todo el ejército y no se puede manipular dejando unidades débiles en el banco.
- Riesgos: que entrenar se sienta inútil; que se note el "rubber banding". Preferir ajustar habilidades, armas, cantidad de enemigos o IA antes que estadísticas puras. Poner un tope.

## 6. Ayuda para remontar (PROPUESTA)

- Cada capítulo ofrece algo (una unidad o un objeto) que permite recuperarse si se juega con cabeza.
- Importante con muerte permanente y despliegue obligatorio: si el ejército se achica, estas unidades sostienen la partida.

## Abierto

- Muerte permanente: ¿sí o no? Afecta casi todo lo anterior.
- Motor: ¿hack de FE8 o motor propio? Define la viabilidad de las barras múltiples y la dificultad dinámica.

## 7. Identidad de unidad (CANON como principio)

**Principio:** la mecánica de cada unidad expresa su personalidad y su historia. Si dos unidades se sienten iguales al jugarlas, una sobra.

Referencia: video "unit identity" (fuentes de identidad: estadísticas, clase, momento de unión, habilidades y estética).

**Reglas:**
1. **Habilidad personal nacida del carácter.** Solitario o egoísta: habilidades que solo lo potencian a él. Servicial: habilidades que potencian al equipo.
2. **Las habilidades pueden cambiar con el arco del personaje** (PROPUESTA). Ejemplo: Vask empieza con una habilidad egoísta y, si decide quedarse, cambia a una de equipo. "Juramento" de Halvard ya va en esta línea.
3. **Nada de cambio de clase indiscriminado.** Rompe la identidad (caso Jean en Engage: médico por historia, pero su habilidad de crecimiento empuja a sacarlo de curador). Opciones: sin cambio de clase, o pocas clases alternativas por personaje que digan algo de él (como Awakening).
4. **Coherencia entre crecimientos y clase inicial.** Caso a evitar: Anna en Engage, con el mejor crecimiento mágico en una clase de fuerza, sin que el jugador lo sepa. Los crecimientos son invisibles: la clase, la animación y la presentación deben comunicarlos.
5. **Los nichos (ladrón, bailarín, curador) tienen personalidad y pasado acordes.**
6. **Limitar la versatilidad del ejército.** Si todos son buenos en todo, nadie es especial. Pocas fuentes de estadísticas extra para que los umbrales altos sigan siendo un rasgo de alguien.
7. **Cuidar el momento de unión.** Una unidad fuerte que se une en un capítulo difícil queda como "la mejor" por contexto y opaca a las alternativas cercanas. Diseñar cada unión pensando en la primera impresión, incluidas las unidades que se quieren destacar.
8. **Estética única.** Animaciones, sprites o vestimentas personales hacen memorables a los personajes. Clases exclusivas de un solo personaje cuando sea posible. Si hay cambio de clase, que la ropa personal se mantenga.

**Sistema de clases (CANON):** árbol cerrado estilo Sacred Stones. Sin cambio de clase libre. Cada clase base promociona a una de dos clases.
- Descartado: cualquier sistema donde todos pueden ser cualquier clase (Three Houses, Fortune's Weave). También las habilidades de maestría transferibles entre clases: igualan a todo el ejército.
- Rescatable de Fortune's Weave: clases exclusivas de un personaje (atadas a su historia) y bonos pasivos personales en ciertos roles (por ejemplo, +1 de movimiento a quien lleva armadura pesada por su pasado). Idea de mecánica: carga en línea recta que golpea a varios enemigos (carro de guerra).
- **Tres promociones solo para reclutas** (PROPUESTA): como los reclutas de Sacred Stones, unas pocas unidades novatas tienen un árbol de tres niveles. Da la sensación de "de cero a héroe" sin multiplicar el trabajo artístico en todo el ejército, y la clase de recluta ya cuenta su historia (jóvenes de la diáspora, por ejemplo).

## 8. Habilidad por rango S de arma (PROPUESTA)

- Al llegar a rango S en un arma, la unidad gana una habilidad que refuerza la naturaleza de esa arma (hace mejor lo que el arma ya hace).
- Ejemplo: arco (preciso) → más precisión, o +1 de alcance.
- Regla sugerida: un solo rango S por unidad, como en los GBA. Así el arma S se vuelve parte de la identidad del personaje.
- Cuidado con el +1 de alcance automático en arcos: cambia mucho el equilibrio, probar antes de fijarlo.
- ABIERTO: definir la habilidad de cada tipo de arma (espada, lanza, hacha, arco, magias, bastones).

## 9. Muerte permanente (CANON)

Como en todos los Fire Emblem.

**Implicaciones:**
- Los capítulos paralelos de un personaje no se pueden jugar si murió.
- Personajes indispensables para la trama, tres categorías:
  1. Condición de derrota (game over) si caen. Reservar para Kairon y, en su Parte, el deuteragonista de turno.
  2. Al caer se retiran mal heridos: siguen en la historia pero ya no son jugables.
  3. Directamente no jugables.
- Si un jugable tiene que salir del grupo por la trama:
  - vuelve a unirse uno o dos capítulos después, o
  - lo reemplaza otra unidad de la misma clase que hereda sus objetos y estadísticas (las habilidades personales pueden cambiar). Referencia: el caso de Nils al final de FE7.
- Consecuencia natural: con menos unidades, la evacuación dividida y el rescate en los escombros son más difíciles. Las ayudas para remontar (sección 6) sostienen la partida.

**Escenas dinámicas:**
- Las líneas no esenciales de secundarios se escriben pensando en que ese personaje puede estar muerto: se le asignan a otro personaje o se quitan si la escena funciona sin ellas.
- Regla de escritura: cada línea de un secundario no indispensable debe tener un reemplazo o poder eliminarse.
- Las líneas esenciales para la trama solo las dicen personajes de las categorías 1-3.

## 10. Material previo: `fisuras-clases-armas.pdf` (Drive, 31 ago)

Ya definido ahí (vigente salvo choque con decisiones nuevas):
- **Triángulo cinético:** Asta > Filo > Peso > Asta. Filo y Asta son tradición elíria; Peso es invención industrial. Efectos: Filo = Sangrado, Asta = Anclaje, Peso = Empuje.
- **Neutrales:** Arco, Rifle (retroceso: cuesta PV propio), Daga, Herramienta, Guante (Kairon), Lámpara Ritual.
- **Triángulo de diarios (magia):** Ritual (Elyria) > Oral (Cassaria/Ordun) > Cristalino (Ferannor) > Ritual.
- **18 clases** con promoción cerrada (encaja con la sección 7).
- **Habilidad de aether única por personaje, que arriesga un tipo de recuerdo:** trivial/feliz (débil), apego, traumático, culpa, el viaje, lo no dicho, romántico (el más fuerte). "La diferencia entre dos personajes de la misma clase es el tipo de recuerdo que arriesgan."

Pendiente: qué pasa mecánicamente cuando se pierde el recuerdo (el documento no lo define). Ver propuesta en la sección 11.

**Choques con decisiones nuevas (revisar):**
- "Su Nombre" de Kairon (olvidar a Nemira) ya no puede resolver el clímax.
- Orestion figura como jugable desde M35; ahora es el jefe final.
- Halvard se une en M21 y traiciona en M30; la nueva estructura lo adelanta.
- Las habilidades de rango S (sección 8) deben usar Filo/Asta/Peso, no espada/lanza/hacha.

## 11. Costo del Olvido (PROPUESTA)

Usar la habilidad de aether gasta el recuerdo: **cada personaje tiene usos limitados en toda la partida** (por ejemplo 3). El costo escala con la categoría del recuerdo:

| Categoría | Poder | Costo al usarla |
|---|---|---|
| Trivial / feliz | Bajo | Pierde puntos de apoyo |
| Apego | Medio | Pierde un rango de apoyo con una persona concreta y estadísticas leves de forma permanente |
| Culpa / traumático | Medio | Puede quitarle un rasgo negativo: olvidar alivia (el atractivo del culto de Kallion) |
| Romántico | Máximo | Pierde la relación: apoyo, escenas y final compartido |

- La experiencia como costo: posible en forma de rango de arma ("olvida la técnica"). Perder niveles parece demasiado castigo; probar con cuidado.
- Debe verse en el juego, no explicarse: diálogos de apoyo que cambian, una línea que el personaje ya no recuerda.
