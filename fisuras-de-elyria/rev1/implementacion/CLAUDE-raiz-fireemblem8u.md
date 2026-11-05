# Fisuras de Elyria — guía para Claude

Este repositorio es la decompilación de Fire Emblem 8 (fireemblem8u) que uso como base de **Fisuras de Elyria**, un ROM hack de GBA. Trabajo solo, en VS Code sobre WSL (Ubuntu).

## Sobre mí y cómo trabajar conmigo

- No sé programar. Explicame cada cambio paso a paso, en español y en lenguaje simple.
- Antes de editar, decime qué archivo vas a tocar, qué hace esa parte del código y qué efecto va a tener en el juego.
- Hacé cambios chicos y probables de a uno. Prefiero editar lo existente antes que reescribir archivos enteros.
- Elegí siempre la solución más simple que funcione.
- Respuestas concisas y directas, sin relleno. Evitá los dos puntos dentro de las oraciones.
- Si algo es ambiguo o hay que tomar una decisión de diseño, preguntame antes de hacerlo.

## Entorno

- Proyecto en `~/fireemblem8u` (usuario de Ubuntu `andy`).
- Herramientas instaladas build-essential, mgba-qt y gdb-multiarch.
- `GUIA_ES.md` tiene una guía del proyecto en español. Hay comentarios marcados `[ES]` en `include/bmunit.h` y `src/bmbattle.c`. Leelos cuando sean relevantes y agregá comentarios `[ES]` breves en el código que modifiques.

## Compilar y probar

- Compilar con `make -j$(nproc) fireemblem8.gba`.
- **No usar `make` solo ni `make compare`.** En este proyecto `make` compara la ROM con la original y siempre da `FAILED` cuando hay cambios. Ese mensaje no es un error de compilación.
- Probar con `mgba-qt fireemblem8.gba`. Los cambios de datos de personajes se ven en una partida nueva, no en partidas guardadas.
- Depurar con la tarea **Abrir juego en mGBA (esperando depurador)** y después F5 con la configuración **Depurar en mGBA** (`.vscode/launch.json`, GDB en el puerto 2345).
- Después de cada cambio, compilá vos y revisá que no haya errores antes de decirme que está listo.

## Seguridad

- Antes de un cambio grande, sugerime hacer un commit con git para poder volver atrás.
- No borres archivos ni hagas cambios masivos sin preguntarme.
- Para deshacer un archivo uso `git checkout ruta/del/archivo`.

## Datos útiles del código

- Personajes en `src/data_characters.c` (array `gCharacterData`). Los `base*` del personaje son un bonus que se suma a los `base*` de la clase en `src/data_classes.c`.
- Constantes de personajes en `include/constants/characters.h` (Eirika = 0x01, Seth = 0x02).
- Carga de stats de unidades en `UnitLoadStatsFromChracter` (`src/bmunit.c`).

## El hack (resumen de diseño, todo provisional)

- **Género y tono.** TRPG aetherpunk con temas de migración e identidad. Estética de inspiración griega.
- **Mundo.** Elyria es una nación que colapsó por el aether, y su pueblo (los elirios) vive en diáspora. Ferannor es el imperio que sigue extrayendo aether. Kaldholt es una nación anfitriona recelosa con los refugiados y Cassaria una más receptiva.
- **Personajes principales.** Kairon (protagonista), Vask (mercenario), Halvard (leal a Kaldholt), Orestion (familiar de Kairon que esconde una culpa), Nemira, Sael, Thessa, Kalyx, Voss (desertora de Ferannor), Riona, Doran, Ianna.
- **Regla de diseño.** Todas las misiones tienen combate real, y el tipo de combate surge de lo que pasa en la escena.
- Los nombres de clases, el elenco y las misiones están en documentos de diseño aparte y pueden cambiar. Si necesitás un dato que no está acá, preguntame.

## Primer paso hecho

Cambio de prueba de `baseSpd` de Eirika en `src/data_characters.c` (de 0 a 10), compilado y verificado en mGBA y con el depurador.

## Documentos de diseño

La carpeta `diseno/` es la fuente oficial del diseño del hack (biblia narrativa, desglose de misiones, elenco, clases, habilidades, novela y algoritmo de mapas). Consultala antes de cambiar personajes, clases o misiones. Los estándares de arte están en `arte/estandares-pixel-art.md`, y `arte/estandarizar_sprites.py` procesa los frames de animación.
