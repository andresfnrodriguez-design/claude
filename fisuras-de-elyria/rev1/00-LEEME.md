# Fisuras de Elyria — cómo está organizado este proyecto

ROM hack de Fire Emblem 8 (The Sacred Stones) sobre la decompilación en C `fireemblem8u`, en WSL Ubuntu con VS Code y mGBA. Lo hace Andrés solo, con ayuda de IA para el arte y la programación.

Consolidado el 5 de noviembre de 2026 a partir de 5 chats y 7 sesiones de claude.ai/code. Lo vigente manda sobre lo descartado, y cada índice dice cuál es cuál.

## Fases

Cada fase tiene su carpeta y su chat propio dentro del proyecto. El chat de cada fase arranca leyendo su índice.

| Fase | Índice | Qué cubre |
|---|---|---|
| Escritura | `escritura/00-INDICE.md` | Mundo, historia (versión 2 vigente y versión 1 descartada), personajes, misiones, novela, diálogos |
| Diseño de juego | `diseno/00-INDICE.md` | Clases, armas, stats, mecánicas, IA enemiga, diseño de mapas y niveles |
| Arte | `arte/00-INDICE.md` | Concept art, retratos, sprites de batalla y de mapa, paletas, pantalla de estado, tilesets |
| Música y sonido | `musica/00-INDICE.md` | Temas, prompts de Suno, MIDI, sonido de voz por personaje |
| Implementación | `implementacion/00-INDICE.md` | Decompilación, compilación, CLAUDE.md, megaprompts, herramientas (Taller de Mapas, gestor de arte, mapa debug) |

`sesiones/` tiene el resumen de cada una de las 12 conversaciones originales, por si hace falta saber de dónde salió algo.

## Mensaje para abrir el chat de una fase

```
Este es el chat de [FASE] de Fisuras de Elyria. Lee 00-LEEME.md y [carpeta]/00-INDICE.md del proyecto antes de responder, y trabaja desde lo vigente. Si algo no está en los documentos, búscalo en los chats viejos del proyecto.
```

## Qué no está acá

- **Imágenes y binarios.** Los documentos solo guardan texto. Todo está en la rama `claude/fisuras-de-elyria-rev1`, y las imágenes de arte principales también se pueden subir a los archivos del proyecto con `arte-imagenes-rev1.zip`.
- **ROM, WAV y `.exe`.** No van a GitHub. La ROM y el WAV quedan en la PC, y el `.exe` del Taller de Mapas en la rama `claude/peaceful-tesla-iy8i1i`.
- **Código de la decompilación.** Vive en `~/fireemblem8u` dentro de Ubuntu.

## Dónde está cada cosa en GitHub

Repositorio `andresfnrodriguez-design/claude`.

**Todo junto y ordenado está en la rama `claude/fisuras-de-elyria-rev1`, carpeta `fisuras-de-elyria/rev1/`.** Tiene la misma estructura por fase que este proyecto, más las imágenes, los PDF y los scripts como archivos reales. Es la revisión 1 de la consolidación, y la próxima se arma como `rev2` sin pisar esta.

Una diferencia entre los dos lugares. En el proyecto de claude.ai los scripts van agrupados dentro de archivos `.md` (por ejemplo `arte/scripts/pantalla-estado.md`, `implementacion/config-vscode.md`, `diseno/mapas/grillas-fe3h.md`). En GitHub están como archivos reales en sus carpetas (`arte/pantalla-estado/`, `implementacion/vscode/`, `diseno/mapas/fe3h/`).

Las ramas originales siguen existiendo como respaldo.

| Rama | Contenido |
|---|---|
| `claude/inspiring-cray-78kf19` | `historia/` (BIBLIA v2, DISENO, VERSION-2-LISTA, storyboard) |
| `claude/affectionate-ptolemy-kgpqva` | `gba_status/` (pantalla de estado) y `prompts/03-pantalla-de-estado.md` |
| `claude/clever-franklin-jrw51o` | `prompts/01`, `prompts/02` y el registro `prompts/implementaciones.md` |
| `claude/elegant-mendel-nrhxiq` | Megaprompt `prompts/implementaciones.md` (barras, íconos y aggro line), maquetas aggro, `triangulo-armas.svg` |
| `claude/intelligent-galileo-1kke2f` | `sprites/` (sprites de mapa, paletas por bando) |
| `claude/peaceful-tesla-iy8i1i` | `tools/mapas/` (Taller de Mapas) y `descargas/TallerMapasElyria.exe` |
| `claude/fisuras-clases` | `fisuras-de-elyria/clases-completas.md`, pull request #1 sin merge |

Hay un conflicto pendiente. `prompts/implementaciones.md` existe con contenido distinto en `clever-franklin` (registro) y en `elegant-mendel` (megaprompt). En este proyecto quedaron separados como `registro-implementaciones.md` y `megaprompt-barras-iconos-aggro.md`.

## Reglas de trabajo con Andrés

- Español neutro con tú, conciso, sin relleno y sin dos puntos dentro de las oraciones.
- Toda respuesta empieza con la palabra "Canario".
- Editar antes que reescribir. La solución más simple que funcione.
- Comandos siempre listos para pegar en la terminal. Usuario de Windows `andre`, de Ubuntu `andy`. Las descargas caen en `Downloads` o en `Downloads/Roms Fe`.
- No sabe programar. Explicar cada paso en lenguaje simple.
