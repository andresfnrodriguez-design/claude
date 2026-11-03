# Taller de mapas · Fisuras de Elyria

Editor de mapas para el ROM hack de FE8 y catálogo de referencia de mapas de Fire Emblem.

Abrí `editor.html` en el navegador. No necesita instalación. `catalogo.js` tiene que estar en la misma carpeta.

## Editor

- **Pintar.** Elegí un terreno FE8 y arrastrá sobre la grilla.
- **Unidad.** Pone unidades de jugador, enemigas o aliadas, con su clase de movimiento, la marca de jefe y el turno de refuerzo con o sin aviso. Un clic sobre una unidad la borra.
- **Objetivo.** Marca la casilla objetivo. Si ponés un jefe se marca solo.
- **Rango.** Muestra hasta dónde llega una clase en un turno desde la casilla que toques.
- **Marco 15×10.** Muestra lo que entra en una pantalla de GBA.

El autochequeo se actualiza con cada cambio y revisa estas cosas.
- El porcentaje de terreno especial.
- El costo y los turnos de la infantería hasta el objetivo, contra la referencia de 30 a 40 casillas y 4 a 6 turnos.
- El fly-skipping, que se marca cuando un volador llega 3 turnos o más antes que la infantería.
- Los pasillos de ancho 1 y el one-tiling en diagonal.
- Los refuerzos sin aviso.
- Las unidades sobre terreno intransitable o superpuestas.

El chequeo mide el mapa. Que sea divertido lo tenés que decidir vos.

## Exportar

- **Grilla de texto.** Filas y columnas numeradas, leyenda y lista de unidades. Es el formato para pasarle un mapa a Claude.
- **IDs FE8.** Matriz de IDs de terreno (0x0C = bosque). Son IDs de terreno y no tiles. Para el mapa real armá los tiles en Tiled o FEBuilder con ese terreno como guía.
- **JSON.** Mapa completo para volver a importarlo. Los guardados del navegador son locales, así que exportá el JSON como respaldo.

## Costos de movimiento

Los costos son aproximados. Reemplazalos con los valores de `src/data_terrains.c` de fireemblem8u en el panel de costos. Quedan guardados en el navegador.

## Referencia FE

`catalogo.js` asigna a cada mapa tres puntajes de 1 a 5 (memorable, dificultad y justicia) y la lección que deja para Fisuras. Los puntajes son estimaciones y no datos oficiales. Las fichas marcadas con `?` todavía no están verificadas. Para agregar juegos, sumá entradas con el mismo formato.

Estado: lote 1 con FE8 completo. Faltan FE7, FE6 y el resto de la serie.
