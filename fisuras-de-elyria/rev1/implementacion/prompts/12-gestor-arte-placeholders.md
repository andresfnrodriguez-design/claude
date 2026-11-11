# Prompt 12 · Cargar los placeholders en el gestor de arte

Para Claude Code en Ubuntu, abierto en `~/gestor-elyria`. Antes de abrirlo, actualizar el repo con `cd ~/elyria-claude && git fetch origin && git checkout claude/nifty-bell-x1mrwv && git pull`.

```
Vamos a cargar los retratos placeholder en el gestor de arte de Fisuras de Elyria. La especificación original está en ESPEC_GESTOR_ASSETS.md. Yo no sé programar, así que explícame todo en español y en pocas líneas.

PASO 0. Diagnóstico
Revisa ~/gestor-elyria y ~/elyria-arte y dime qué etapas de la especificación ya funcionan (1 a 7). Si ~/gestor-elyria está vacío o no arranca, NO construyas la app ahora. En ese caso haz solo los pasos 1 y 3 dentro de ~/elyria-arte (estructura, estandar.json, fichas y archivos v001), para que la app los lea cuando exista.

PASO 1. Estándar nuevo de retratos
El estándar de retratos cambió. Actualiza estandar.json (y, si la app ya existe, el checklist y el validador que lo leen) para que cada personaje tenga estos assets, con estas medidas exactas.

| Asset (carpeta) | Medida | Notas |
|---|---|---|
| concepto/ | libre | Hoja de concepto o la hoja unificada de Nano Banana / Gemini |
| paleta/ | 16 colores | Archivo .pal, índice 0 = #A9CBA6 |
| retrato_zoom/ | 180x120 | Primer plano, expresión normal |
| retrato_herido/ | 180x120 | El mismo primer plano, herido en combate |
| retrato_escena/ | 104x112 | Busto mirando a la derecha, contorno negro de 1 px y blanco de 2 px |
| retrato_escena_espejo/ | 104x112 | Redibujado mirando a la izquierda, nunca volteado. Mismo contorno |
| retrato_estado/ | 108x160 | Cuerpo entero con pies |
| mini_retrato/ | 32x32 | Cabeza centrada |
| combate/ | 80x56 | Figura de combate mirando a la izquierda, pies en y=52 |

Se mantienen bocas, ojos, poses, paleta de batalla y voz como estaban. Las medidas viejas (100x112, 80x144, 88x152, 240x160) dejan de ser válidas. Todos los PNG son indexados de 16 colores con #A9CBA6 en el índice 0.

PASO 2. Origen de los archivos
Todo está en ~/elyria-claude/fisuras-de-elyria/rev1/arte/placeholders/. Hay una carpeta prueba_<nombre> por personaje (archivista, bjorn, halvard, nemira, orestion, rafael, riona, rook, vask). Ignora prueba_archivista_baston y para_decomp.

PASO 3. Carga
Para cada personaje crea o completa su ficha en ~/elyria-arte/personajes/<nombre>/ y carga cada archivo como versión nueva (v001, v002...) en la carpeta del asset que corresponde según su nombre (zoom, herido, escena, espejo, estado, mini, combate, .pal, concepto.png, *_hoja_combinada.png). Busca tanto en la raíz de cada prueba_<nombre> como en su subcarpeta out/ y pixellab/out/. Si un archivo no encaja con ningún asset, no lo cargues y lístalo al final.
- La archivista (prueba_archivista/pixellab/out/) es la única que ya cumple el estándar nuevo. Sus 7 piezas y su .pal quedan como versión vigente y en estado "validado" si pasan el validador.
- Los demás personajes tienen piezas con medidas viejas. Cárgalas igual como versión vigente en estado "pixel art", con la nota "estándar viejo, rehacer con hoja unificada". Si el validador ya existe, deja que las marque en rojo.
- Los assets que falten quedan en "pendiente".
Nunca borres ni sobrescribas nada que ya esté en ~/elyria-arte.

PASO 4. Cierre
Haz commit en el git de ~/elyria-arte con el mensaje "Placeholders de retratos con el estándar nuevo". Después muéstrame una tabla con una fila por personaje, una columna por asset y el estado de cada uno, más la lista de archivos que no cargaste. Dime también cómo abro el gestor para verlo.
```
