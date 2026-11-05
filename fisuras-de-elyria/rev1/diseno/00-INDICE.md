# Diseño de juego — índice

Clases, armas, stats, mecánicas, IA enemiga y diseño de mapas.

## Documentos

| Archivo | Qué es | Estado |
|---|---|---|
| `DISENO-mecanicas-v2.md` | Mecánicas de la versión 2 y principios de programación para GBA | **Vigente** |
| `clases-completas.md` | 18 clases con arma, promoción, skill y personajes, triángulos y rangos | Vigente en sistema, el reparto de personajes es de la versión 1 |
| `lore-clases.md` | Lore de cada clase por nación | Vigente |
| `personajes-habilidades.md` | Habilidad de recuerdo, stats base y crecimientos por personaje | Versión 1, revisar contra el elenco de la 2 |
| `algoritmo-diseno-mapas.md` | Método de diseño de mapas en 9 pasos | **Vigente** |
| `notas-ambientacion-mapas.md` | Ambientación por misión de la versión 1 | Cantera |
| `mejores-mapas-fe-y-romhacks-exitosos.md` | Qué hace buenos a los mapas famosos, condiciones de victoria y derrota | Referencia |
| `terreno-fe7-y-condiciones-victoria.md` | Terrenos y objetivos de FE7 | Referencia |
| `mapas/parte1-layouts-vigentes.html` | Layouts de la Parte I de la versión 1, rehechos desde cero | Cantera |
| `mapas/catalogo-mapas-fe.js` | Catálogo ponderado de mapas de FE8, FE7, FE6 y FE4 con lección para Fisuras (puntajes sin verificar) | Referencia |
| `mapas/grillas-fe3h.md` | Grillas de Three Houses, capítulos 0 a 8 | Referencia |
| `referencias/` | Transcripciones de videos y hilos de foro sobre diseño de mapas y objetivos | Referencia |

## Mecánicas canon

- **Muerte permanente** con personajes indispensables.
- **Árbol de clases cerrado** estilo Sacred Stones. Tres promociones solo para reclutas. Three Houses y Fortune's Weave descartados.
- **Identidad de unidad.** Habilidades nacidas del carácter, coherencia entre clase y crecimientos, estética única.
- **Principios de programación.** La lógica nueva no toca el hardware, datos fijos en ROM con `const`, sin `malloc`, estructuras compactas y medir la RAM en cada compilación.

## Mecánicas propuestas

- **Jefes con varias barras**, 1/2/3 en normal y 2/3/4 en difícil.
- **Veneno.** 1/3/5 de daño por 1/2/3 stacks, tope 3, puede matar, solo se cura con consumibles o magia.
- **Dificultad dinámica** oculta, solo en difícil y solo sube.
- **Ayuda para remontar** en cada capítulo.
- **Habilidad por rango S** de arma, pendiente de definir con Filo, Asta y Peso.
- **Costo del Olvido.** Hay una tabla propuesta en `DISENO-mecanicas-v2.md`, sin confirmar.
- **Pulso Divino** (retroceder turnos). Una foto inicial y hasta 15 deltas por acción. Recomendado solo con acciones del jugador, sin retroceder antes de un evento con guion y con usos limitados. Faltan tres decisiones, si cuentan las acciones enemigas, si el azar se restaura y si hay límite por capítulo.
- **Aggro line** estilo Engage, líneas punteadas que muestran qué enemigos atacan la casilla. Ya tiene maquetas y megaprompt (ver Implementación).

## Sistema de armas

- **Triángulo cinético.** Asta vence a Filo, Filo vence a Peso, Peso vence a Asta.
- **Efecto propio por categoría.** Filo causa sangrado, Asta ancla (reduce Mov o Spd) y Peso empuja una casilla.
- **Nombres.** Filo y Asta son tradición elyria con nombres griegos (Xiphos, Kopis, Dory, Sarissa, Xyston). Peso es industrial (Percutor, Mayal de Resorte, Hacha de Vapor).
- `triangulo-armas.svg` está en la rama `claude/elegant-mendel-nrhxiq`.

## IA enemiga

Investigación sin archivo propio, resumida en `../sesiones/03-ia-enemigos.md`. Los pesos exactos no están verificados con fuentes.

- La IA de FE tiene dos capas, un comportamiento asignado (agresivo, por rango, estacionario, por grupo o zona, ladrón, curandero) y una puntuación de cada objetivo, casilla y arma.
- Manipular a la IA con cebos es el núcleo deseable del juego. Lo que hay que eliminar son las estrategias degeneradas de costo cero.
- Recomendado para Fisuras. IA de utilidad con riesgo propio, reservas de objetivo, un paso de anticipación con mapa de amenazas, histéresis contra bucles, azar con semilla entre las mejores opciones, retirada con poca vida, refuerzos que no actúan al aparecer y dificultad por pesos y no por trampas.

## Reglas fijas de mapas

- Tamaño para 4 a 6 turnos eficientes y unas 30 a 40 casillas hasta el objetivo en las primeras misiones.
- El terreno tiene función mecánica, no decorativa. Varias rutas viables.
- Nunca emboscadas sin aviso. Los refuerzos se anuncian un turno antes de actuar.
- Un evento narrativo por mapa que una la tensión del juego con la de la historia.
- El esfuerzo fuerte se reserva para las misiones clave.
- El Taller de Mapas chequea solo estas reglas (ver Implementación).

## Abierto

- Nombre de la clase de Kairon. Era Guantelete → Artífice, única. Los candidatos son Artífice → Polímetis, Trasteador → Polímetis e Ingenioso → Artífice. Al elegir, actualizar `clases-completas.md`, `lore-clases.md` y `personajes-habilidades.md`.
- Reasignar clases y stats al elenco de la versión 2.
- Si Orestion es mago o guerrero.
- Rango y tope de la dificultad dinámica.
- Las misiones clave a diseñar primero en la versión 2 (las de la versión 1 eran M20, M30, M35 y M39).
