# Resumen de sesión — Fisuras de Elyria sobre el decomp de FE8

Fecha 3 de noviembre de 2026. Punto de partida, fireemblem8u ya compilado en Ubuntu (WSL) en `~/fireemblem8u`.

## Qué se logró

- Primer cambio real al juego desde el código, compilado y verificado en mGBA y con el depurador.
- Depuración con VS Code + mGBA + F5 funcionando.
- Claude Code instalado en VS Code (WSL) y con contexto del proyecto vía `CLAUDE.md`.
- Documentos de diseño de septiembre recuperados y copiados al proyecto.
- Estructura de carpetas del hack definida (`arte/`, `diseno/`, `musica/`).

## Archivos modificados o creados en el proyecto (`~/fireemblem8u`)

| Archivo | Qué cambió | Para qué |
|---|---|---|
| `src/data_characters.c` (línea 23) | `.baseSpd` de Eirika de 0 a 10 | Prueba del ciclo editar, compilar, probar. En el juego da Spd 19 (10 propio + 9 de la clase Lord, tope 20) |
| `CLAUDE.md` (raíz, nuevo) | Guía para Claude Code, más una sección final "Documentos de diseño" agregada con `cat >>` | Que Claude Code arranque con contexto del hack, del entorno y de cómo explicarte |
| `arte/estandares-pixel-art.md` (nuevo) | Reglas de concept art, sprites, frames de animación y mapas | Referencia fija de arte |
| `arte/estandarizar_sprites.py` | Copiado del chat de septiembre | Procesar frames de animación al estándar |
| `diseno/*.md` (8 archivos) | Copiados del chat de septiembre | Fuente oficial del diseño para Claude Code |
| `musica/*.mid` | MIDIs copiados desde Descargas | Para integrarlos como música del juego |
| `.vscode/launch.json` | Sin cambios, ya existía y sirve tal cual | Configuración "Depurar en mGBA" |

En `salida/proyecto/cambio_eirika_baseSpd.patch` está el cambio de Eirika como parche.

## Decisiones

- **Herramienta de trabajo.** Claude Code dentro de VS Code edita, compila y lee errores. Este chat queda para diseño y para destrabar pasos.
- **Compilación.** Siempre `make -j$(nproc) fireemblem8.gba`. El `make` solo compara con la ROM original y da `FAILED` cuando hay cambios, sin ser un error.
- **Fuente del diseño.** Los archivos de `diseno/` mandan. Numeración vigente Nemira desaparece en M10, muerte confirmada en M15, Vask traiciona en M14, Selene es la tercera traidora, Voss es mujer.
- **Personajes.** Los 33 slots jugables de FE8 se reemplazan por el elenco del hack, en vez de crear personajes desde cero.
- **Mapas.** Se diseñan en un proyecto aparte de claude.ai con instrucciones fijas (texto en `salida/instrucciones-proyecto-mapas.md`).
- **Música.** Se integra desde MIDI con `mid2agb`, no desde WAV. El WAV de prueba dura 12:48 y pesa 135 MB, y aun a la peor calidad de GBA ocuparía unos 10 MB.
- **Colores.** Querés cambiar el pasto y las montañas del mapa del capítulo 1, el azul de las unidades del jugador en el mapa y los azules y blancos de la pantalla de batalla.
- **mGBA.** Botón A en Z y botón B en X.

## Comandos que funcionaron

```bash
# Abrir el proyecto en VS Code
cd ~/fireemblem8u
code .

# Compilar sin la comparación
make -j$(nproc) fireemblem8.gba

# Probar el juego
mgba-qt fireemblem8.gba

# Abrir la carpeta actual en el Explorador de Windows
explorer.exe .

# Crear un archivo pegando su contenido (heredoc)
cat > ~/fireemblem8u/CLAUDE.md << 'EOF'
...contenido...
EOF

# Copiar desde Windows a Ubuntu (Roms Fe o Descargas)
cp "/mnt/c/Users/andre/Downloads/Roms Fe/"estandares*.md ~/fireemblem8u/arte/
cp /mnt/c/Users/andre/Downloads/*.mid ~/fireemblem8u/musica/

# Borrar un duplicado con espacio en el nombre
rm ~/fireemblem8u/arte/"estandares-pixel-art (1).md"
```

Depuración. Tarea "Abrir juego en mGBA (esperando depurador)", después F5 con "Depurar en mGBA" (GDB en el puerto 2345). En la Consola de depuración va una expresión por línea, por ejemplo `character->number`, `character->baseSpd`, `unit->spd`.

## Datos técnicos útiles

- Eirika es `CHARACTER_EIRIKA = 0x01`. Los `base*` del personaje se suman a los de la clase en `src/data_classes.c`. La suma ocurre en `UnitLoadStatsFromChracter`, `src/bmunit.c` línea 711.
- 33 jugables con IDs 0x01 a 0x22 (no existe 0x1B) y 10 de postgame con IDs 0x23 a 0x2C.
- Paletas de terreno en `graphics/map/MapPalette1.pal` a `MapPalette19.pal`. Son texto JASC-PAL con 160 colores y cambiarlas afecta a todos los mapas que las usan.
- Paleta de las unidades del jugador en el mapa en `graphics/unit_icon/palette/unit_icon_pal_player.agbpal` (binario). Enemigo, NPC y "ya actuó" al lado.
- Ventanas y UI en `graphics/player_interface/*.pal`.
- Música en `sound/songs/midi`, regla de conversión en `songs.mk` (`-G` grupo de instrumentos, `-V` volumen, `-R` reverb, `-P` prioridad), registro en `sound/song_table.s`, música de cada capítulo en `mapBgmIds` de los datos del capítulo (`src/data/chapter_settings.json.txt`).
- El proyecto tiene unas 340.000 líneas de C en 358 archivos. Para el hack se tocan sobre todo los archivos de datos.
- La GBA redondea cada canal de color a múltiplos de 8.

## Problemas sin resolver

- **Git.** Claude Code avisó que la carpeta no es un repositorio. Falta confirmar que hizo `git init`, el `.gitignore` (sin ROMs ni `.sav`) y el primer commit. Hasta entonces `git checkout` no sirve para deshacer.
- **Música.** No está confirmado que Claude Code haya integrado el MIDI del capítulo 1. La segunda canción no tiene destino definido.
- **Paletas.** Ningún color cambiado todavía. Falta la vista previa de las paletas del capítulo 1 y de las unidades.
- **Arte.** El concept art y los sprites no están en el proyecto. Están en tu PC, en Nano Banana o en PixelLab.
- **Proyecto de mapas.** Falta confirmar que esté creado con las instrucciones y los cinco archivos subidos.
- **Descargas.** Los archivos a veces bajan a `Downloads` y a veces a `Downloads/Roms Fe`. Revisar ambas si un `cp` falla.

## Próximos pasos

1. Confirmar git y hacer el primer commit.
2. Integrar el MIDI del capítulo 1, probarlo y ajustar instrumentos, volumen y reverb.
3. Pedir a Claude Code las vistas previas de paletas y aplicar los colores nuevos.
4. Crear el proyecto de mapas y diseñar la M2.
5. Empezar a reemplazar personajes de FE8 por el elenco (Kairon en el slot de Eirika).

## Archivos perdidos

Ninguno de los archivos que subiste se perdió. Quedan fuera del zip estos, porque nunca llegaron a este chat.

- Los MIDI de música. Solo están en tu PC (`Descargas` y `~/fireemblem8u/musica`).
- GIF de animaciones. No se subió ninguno en esta sesión.
- Concept art y sprites de chats anteriores. No se pueden recuperar desde acá.
