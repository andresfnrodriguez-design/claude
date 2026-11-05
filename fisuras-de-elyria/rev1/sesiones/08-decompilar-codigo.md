# Resumen de sesión · Decompilación de FE8 para Fisuras de Elyria

Sesión del 2 al 5 de noviembre de 2026.

## Objetivo

Dejar FEBuilder y trabajar el hack *Fisuras de Elyria* como código C en VS Code, con el juego (mGBA) y el código visibles a la vez.

## Qué se hizo

1. Se verificó la ROM subida. Es *Fire Emblem: The Sacred Stones (USA, Australia)* limpia, con SHA1 `c25b145e37456171ada4b0d440bf88a19f4d509f`.
2. Se descargó la decompilación de la comunidad `FireEmblemUniverse/fireemblem8u` (358 archivos .c, casi nada en ensamblador) y el compilador `pret/agbcc`.
3. Se entregó `fe8u-decomp-codigo.zip` (solo src, include y docs).
4. Se preparó el proyecto para VS Code (configuración, guía en español y comentarios `[ES]`) y se entregó completo en `fe8u-vscode.zip`.
5. Se guió paso a paso la instalación en la PC de Andrés (Windows + WSL Ubuntu) hasta compilar con `quickstart.sh`.

## Archivos creados o modificados

| Archivo | Para qué |
|---|---|
| `fireemblem8u/.vscode/extensions.json` | Recomienda clangd (autocompletado y F12), C/C++ (depurador) y WSL |
| `fireemblem8u/.vscode/settings.json` | Apaga el IntelliSense de C/C++ para que no choque con clangd, oculta archivos de compilación |
| `fireemblem8u/.vscode/tasks.json` | Ctrl+Shift+B compila `fireemblem8.gba`. Tareas para verificar contra la original, limpiar y abrir mGBA normal o esperando depurador (`-g`) |
| `fireemblem8u/.vscode/launch.json` | F5 conecta `gdb-multiarch` a mGBA en `localhost:2345` usando `fireemblem8.elf` |
| `fireemblem8u/GUIA_ES.md` | Instalación, depuración, mapa del código, conceptos (unidad/clase/personaje, procs, eventos), primer cambio de prueba, diferencias con FEBuilder |
| `fireemblem8u/include/bmunit.h` | Solo comentarios `[ES]` en `CharacterData`, `ClassData` y `Unit` |
| `fireemblem8u/src/bmbattle.c` | Solo un comentario `[ES]` con todas las fórmulas de combate antes de `ComputeBattleUnitDefense` |
| `fe8u-decomp-codigo.zip` | Primera entrega, código fuente para leer |
| `fe8u-vscode.zip` | Proyecto completo listo para VS Code, sin ROM ni `.git` ni `_site` |
| `RESUMEN_SESION.md` | Este archivo |

Los cambios en `bmunit.h` y `bmbattle.c` son solo comentarios. No alteran la ROM compilada.

## Decisiones de diseño

- **Decomp en lugar de FEBuilder.** Todo queda en texto, versionable y depurable. La ROM resultante ya no se puede seguir editando en FEBuilder, hay que elegir un solo camino.
- **WSL Ubuntu.** El proyecto solo compila en Linux. El proyecto vive en `~/fireemblem8u` dentro de Ubuntu porque compilar desde `/mnt/c` es lento y Windows borra los permisos de ejecución.
- **clangd + C/C++.** clangd usa el `compile_flags.txt` del repo para navegar. C/C++ queda solo para depurar.
- **Depuración con mGBA + gdb.** El Makefile ya compila con `-g`, así que `fireemblem8.elf` permite breakpoints por línea de C. Por la optimización `-O2` algunas variables locales aparecen como `<optimized out>`. Las globales (`gUnitArrayBlue`, `gBattleActor`) se ven bien.
- **Tarea de compilación por defecto** `make fireemblem8.gba` y no `make` a secas, porque `make` verifica el checksum y falla en cuanto hay un cambio propio.
- **Comentarios con `[ES]`** para encontrarlos todos con Ctrl+Shift+F.

## Comandos que funcionaron (en la PC)

Usuario de Windows `andre`, usuario de Ubuntu `andy`. Ejecutar de a uno.

```bash
cp -r "/mnt/c/Users/andre/Downloads/Roms Fe/fe8u-vscode/fireemblem8u" ~/
```

```bash
cp "/mnt/c/Users/andre/Downloads/Roms Fe/Fire Emblem - The Sacred Stones (USA, Australia).gba" ~/fireemblem8u/baserom.gba
```

```bash
cd ~/fireemblem8u
chmod +x scripts/*.sh *.sh
```

```bash
sudo apt install -y build-essential git
```

```bash
./scripts/quickstart.sh
```

```bash
sudo apt install -y mgba-qt gdb-multiarch
```

```bash
cd ~/fireemblem8u
code .
```

## Problemas encontrados y resueltos

- **El espacio en "Roms Fe"** hacía fallar las rutas. Se resolvió con comillas.
- **Ctrl+Z pausa, no cancela.** Dejó una copia en pausa (`[1]+ Stopped`). Se cerró con `kill %1`. Para cancelar se usa Ctrl+C.
- **Comandos escritos mientras otro corría** quedaron en cola y se ejecutaron después. Conviene escribir uno por vez y esperar el prompt `andy@Portatil`.
- **Nombre de la ROM distinto** al del archivo subido. El real es `Fire Emblem - The Sacred Stones (USA, Australia).gba`.
- **`make: not found`** en la primera compilación. Se resolvió instalando `build-essential`.
- **VS Code compiló con PowerShell** (`nproc no se reconoce`). VS Code estaba abierto desde Windows y no conectado a Ubuntu. Solución indicada, instalar la extensión WSL y abrir siempre con `code .` desde Ubuntu.

## Sin resolver

- **Compilación en este entorno.** No se pudo compilar agbcc ni el proyecto acá porque se bloqueó la ejecución de scripts descargados. Las configuraciones de `.vscode` no se probaron en este entorno.
- **Confirmación de `fireemblem8.gba: OK`.** Andrés respondió "listo" pero no mostró la línea final del segundo `quickstart.sh`.
- **Extensión WSL.** No está confirmado que se haya instalado ni que VS Code muestre **WSL: Ubuntu** abajo a la izquierda.
- **Cambio de prueba de Eirika.** Probablemente se editó la copia de Windows en "Roms Fe" y no la de Ubuntu. Hay que repetirlo en `~/fireemblem8u`.
- **Depurador (F5) sin probar.** Falta comprobar que mGBA con `-g` y `gdb-multiarch` conecten.
- **Copia duplicada en Windows.** `Downloads/Roms Fe/fe8u-vscode/fireemblem8u` ya no se usa y puede confundir. Conviene borrarla o no abrirla nunca.
- **Git.** El proyecto se entregó sin `.git`, así que todavía no hay historial de cambios.

## Próximos pasos

1. Instalar la extensión **WSL** en VS Code (Ctrl+Shift+X, buscar `WSL`, la de Microsoft).
2. Abrir el proyecto desde Ubuntu y verificar **WSL: Ubuntu** abajo a la izquierda.
   ```bash
   cd ~/fireemblem8u
   code .
   ```
3. Inicializar git para poder volver atrás.
   ```bash
   cd ~/fireemblem8u
   git init && git add -A && git commit -m "Base FE8 decomp con config VS Code"
   ```
4. Cambio de prueba. En `src/data_characters.c`, en `[CHARACTER_EIRIKA - 1]`, cambiar `.baseSpd = 0,` por `.baseSpd = 10,`. Guardar, Ctrl+Shift+B y probar.
   ```bash
   mgba-qt fireemblem8.gba
   ```
5. Probar el depurador con un breakpoint en `ComputeBattleUnitAttack` (`src/bmbattle.c`), la tarea "Abrir juego en mGBA (esperando depurador)" y F5.
6. Empezar los cambios reales de *Fisuras de Elyria* por datos (clases en `src/data_classes.c`, personajes en `src/data_characters.c`) antes de tocar eventos o código.

## Archivos perdidos

Ninguno. Todos los archivos subidos y creados en la sesión seguían disponibles al armar el zip.
