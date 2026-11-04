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
| 2 | 2 o 3 (decidir un valor fijo) |
| 3 | 5 |

- La curva crece más rápido que lineal: el jugador tiene que curar antes del tercer stack.
- ABIERTO: tope de stacks (¿3?), si puede matar o deja en 1 PV, cómo se quita (antídoto, bastón, desaparece solo) y si baja un stack por turno.
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
