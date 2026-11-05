# Resumen de sesión

## Qué se hizo
Una sola tarea: investigar cómo funciona la IA enemiga en Fire Emblem y en juegos tácticos parecidos, para sacar criterios de diseño que la hagan justa y no explotable de forma degenerada. La respuesta quedó solo en el chat. No escribí ningún archivo y no busqué en la web: todo salió de mi conocimiento previo, así que los pesos numéricos exactos hay que verificarlos.

## Archivos modificados
- Ninguno durante la investigación. El repositorio (`placas_fire_emblem/`, `tools/`, `README.md`) quedó sin tocar.
- Creado al cierre: `RESUMEN_SESION.md` (este archivo) y `SESION_ARCHIVOS.zip`.

## Contenido y decisiones de diseño
- **IA de Fire Emblem en dos capas:** un comportamiento asignado por el diseñador (agresivo, aggro por rango, estacionario, activación por grupo, zona o turno, ladrón, curandero, objetivo) y una elección táctica que puntúa cada combinación objetivo × casilla × arma.
- **Factores de la puntuación:** poder matar (el peso más alto), daño esperado, probabilidad de acierto, contraataque recibido, terreno, prioridad del objetivo y desempate determinista.
- **Sin información oculta:** la IA de FE no lee el RNG antes de decidir. El 2RN de GBA y 3DS ajusta el acierto que percibe el jugador.
- **Exploits típicos:** cebo con tanque, desequipar el arma, unidad a la que no puede dañar, sacar a los aggro de uno en uno, cuellos de botella, bucles, manipulación del RNG.
- **Criterio central:** manipular la IA con cebos es el núcleo deseable del juego. Lo que hay que eliminar son las estrategias degeneradas de coste cero.
- **Referentes:** Advance Wars/Wargroove, Into the Breach, XCOM, FFT/Tactics Ogre, Battle Brothers/Darkest Dungeon.
- **Recomendación:**
  - IA de utilidad con término de riesgo propio
  - contraataque real del defensor
  - reservas de objetivo y concentración de fuego
  - mirar un paso adelante con un mapa de amenazas
  - histéresis para evitar bucles
  - aleatoriedad con semilla entre las N mejores opciones
  - retirada con poca vida
  - refuerzos que no actúan el turno en que aparecen
  - zona de peligro visible
  - dificultad por pesos, no por trampas
- Incluye un pseudocódigo del sistema de puntuación.

## Comandos que funcionaron
- `git status --short`: confirmó que no había cambios de la sesión.
- `zip -r SESION_ARCHIVOS.zip entrada salida`: armó el paquete.

## Sin resolver
- Los pesos exactos por entrada (GBA, Tellius, 3DS, Switch) no están verificados con fuentes.
- No hay prototipo implementado.

## Próximos pasos
1. Verificar los datos contra FEUniverse y Serenes Forest.
2. Pasar la investigación a un documento de diseño dentro del repo.
3. Implementar un prototipo de la IA de utilidad y probarlo con bots que usen los exploits conocidos.

## Archivos perdidos
- Ninguno. No subiste archivos en esta sesión, así que `entrada/` va vacía.
