# Implementación — índice

Decompilación, entorno, megaprompts para Claude Code y herramientas propias.

## Entorno

- Proyecto en `~/fireemblem8u` dentro de WSL Ubuntu (usuario `andy`), sobre `FireEmblemUniverse/fireemblem8u`. ROM base *The Sacred Stones (USA, Australia)*, SHA1 `c25b145e37456171ada4b0d440bf88a19f4d509f`.
- Se dejó FEBuilder. Una ROM compilada desde la decomp ya no se puede seguir editando en FEBuilder.
- VS Code abierto siempre desde Ubuntu con `code .` y la extensión WSL. clangd para navegar y C/C++ solo para depurar.
- Claude Code instalado en VS Code y en la terminal (`curl -fsSL https://claude.ai/install.sh | bash`, con `~/.local/bin` en el PATH).
- En mGBA el botón A está en Z y el B en X.

## Compilar, probar y depurar

```bash
cd ~/fireemblem8u && make -j$(nproc) fireemblem8.gba
```

```bash
mgba-qt fireemblem8.gba
```

- Nunca `make` solo ni `make compare`. Comparan con la ROM original y dan `FAILED` con cualquier cambio, sin que sea un error.
- Depurar con la tarea "Abrir juego en mGBA (esperando depurador)" y F5 con "Depurar en mGBA" (GDB en el puerto 2345).
- Los cambios de personajes se ven en una partida nueva.

## Documentos

| Archivo | Qué es |
|---|---|
| `CLAUDE-raiz-fireemblem8u.md` | El `CLAUDE.md` de la raíz del proyecto, con cómo trabajar contigo y datos del código |
| `CLAUDE-carpeta-historia.md` | Instrucciones de la carpeta `historia/` del repo |
| `GUIA_ES.md` | Guía en español del proyecto, instalación, depuración, mapa del código, conceptos |
| `config-vscode.md` | `tasks.json`, `launch.json`, `settings.json`, `extensions.json` y el parche de Eirika |
| `ESPEC_GESTOR_ASSETS.md` | Especificación del gestor de arte en Electron, por etapas |
| `instrucciones-proyecto-mapas.md` | Instrucciones para un proyecto de mapas aparte |
| `taller-mapas/` | README y scripts del Taller de Mapas |
| `mapa-debug/` | Prompt vigente, guía e instalador del mapa debug del Prólogo |
| `aggro-line/alternativas-aggro.html` | Las 4 alternativas animadas de la aggro line |

## Megaprompts

Todos piden primero un plan y feedback de viabilidad, y no escriben código hasta que lo apruebes.

| Archivo | Qué implementa | Estado |
|---|---|---|
| `prompts/01-barras-de-vida-fates.md` | Barras de vida estilo Fates | Sin enviar |
| `prompts/02-iconos-de-amenaza.md` | Bolsa de botín y `!` de crítico y efectividad | Sin enviar |
| `prompts/03-pantalla-de-estado.md` | Pantalla de estado nueva | Sin enviar |
| `prompts/03-pantalla-de-estado-especificacion.md` | Especificación detallada de la 03 | Referencia |
| `prompts/megaprompt-barras-iconos-aggro.md` | 01, 02 y aggro line juntos, porque comparten OAM, paletas y VRAM, con escenario de pruebas | **Usar este en lugar de 01 y 02 por separado** |
| `prompts/registro-implementaciones.md` | Registro con plantilla para pegar el feedback de cada implementación | Plantilla |

**Barras de vida vigentes (estilo Fates).** 14x3 px, borde `#3A3935`, 12 px de relleno y vacío `#525491`, en las 3 filas inferiores de la casilla. La punta izquierda tiene el color del bando y la derecha depende de la vida máxima por tramos, con naranja a la mitad y rojo a un cuarto. Esta especificación reemplaza a la de verde, amarillo y rojo.

**Retratos más grandes.** El prompt de retratos de 100x112 y pantalla de estado de 80x144 está en el chat "Historia para juego de Fire Emblem", sin ejecutar. Hay que confirmar que 4 caras de 104x112 entran en VRAM, y si no el límite pasa a 3.

## Herramientas propias

- **Taller de Mapas** (rama `claude/peaceful-tesla-iy8i1i`). Editor de mapas FE8 con autochequeo de las reglas de diseño, los 49 mapas reales de FE8 con terreno exacto, 96 mapas estimados de FE7, FE6 y FE4, y `TallerMapasElyria.exe` portable. El `.exe` de 75 MB está commiteado y conviene pasarlo a Releases.
- **Mapa debug del Prólogo.** Mapa de 27x30 con el núcleo del prólogo de Three Houses y los 64 terrenos de FE8, sobre el tileset 9. Se instala con `python3 debug_mapa.py` y se revierte con `--revertir`. El prompt vigente es `mapa-debug/prompt_unidades_v2.txt`. La guía muestra todavía la grilla vieja.
- **Gestor de arte en Electron.** Especificado, sin confirmar que la etapa 1 arrancó. Código en `~/gestor-elyria` y biblioteca en `~/elyria-arte`.

## Datos útiles del código

- Personajes en `src/data_characters.c`. Los `base*` del personaje se suman a los de la clase (`src/data_classes.c`) en `UnitLoadStatsFromChracter`, `src/bmunit.c` línea 711.
- 33 jugables con IDs 0x01 a 0x22 (no existe 0x1B). Se reemplazan por el elenco del hack, con Kairon en el slot de Eirika.
- El terreno lo define la tabla del tileset (bytes 0x2000 a 0x23FF de `TileConfigurationN.bin`, indexada con el valor del `.mar` dividido por 32), no el mapa.
- Retratos en `src/face.c` y `src/cgtext.c`. Íconos de unidad en `PutUnitSpriteIconsOam`, `src/bmudisp.c` línea 1023.
- La GBA redondea cada canal de color a múltiplos de 8.

## Cambios hechos al juego

- `baseSpd` de Eirika de 0 a 10, compilado y probado (parche en `config-vscode.md`).
- Comentarios `[ES]` en `include/bmunit.h` y `src/bmbattle.c`.

## Abierto

- Confirmar `git init`, el `.gitignore` sin ROMs ni `.sav` y el primer commit.
- Unificar las siete ramas de GitHub en una y resolver el conflicto de `prompts/implementaciones.md`.
- Merge de la pull request #1 y decidir si Fisuras de Elyria tiene un repo propio.
- Enviar el megaprompt unificado y pegar el feedback en el registro.
- Aggro line. Color final de las líneas (el rojo no sirve) y valor de `AGGRO_MAX_LINES`.
- Eventos del mapa debug (cofres, puertas, aldeas, balistas) y probar la grilla corregida en mGBA.
- Sacar unidades y jefes de los eventos de FE8 para el Taller de Mapas.
