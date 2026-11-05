# Guía en español · FE8 decomp en VS Code

Esta carpeta es el código C reconstruido de *Fire Emblem: The Sacred Stones (USA)*. En lugar de editar la ROM con FEBuilder, editás código y datos en VS Code y compilás una ROM nueva. Todo queda en texto, con historial de cambios (git) y búsqueda.

Los comentarios marcados con `[ES]` en el código están en español y explican lo más importante. Para encontrarlos, buscá `[ES]` con Ctrl+Shift+F.

---

## 1. Instalación (una sola vez)

### En Windows 10/11 (con WSL)

1. En PowerShell como administrador corré `wsl --install` y reiniciá. Esto instala Ubuntu.
2. En VS Code instalá la extensión **WSL** de Microsoft.
3. Abrí Ubuntu y copiá esta carpeta dentro de Linux (por ejemplo a `~/fireemblem8u`). Compilar desde `C:\` a través de WSL es mucho más lento.
4. Copiá tu ROM a la carpeta con el nombre `baserom.gba`.
5. En la terminal de Ubuntu, dentro de la carpeta, corré esto.

```bash
./scripts/quickstart.sh
sudo apt install -y mgba-qt gdb-multiarch
code .
```

`quickstart.sh` instala el compilador del proyecto (agbcc), compila y verifica que la ROM salga idéntica a la original. Tarda hasta 15 minutos la primera vez. `code .` abre VS Code conectado a Ubuntu. Con Windows 11 la ventana de mGBA se abre sola desde Linux.

6. VS Code te va a ofrecer instalar las extensiones recomendadas (clangd, C/C++ y WSL). Aceptá.

### En Linux

Los mismos pasos 4 a 6, sin WSL.

---

## 2. Ver el juego y el código a la vez

La idea es tener mGBA a un lado y VS Code al otro, conectados. Cuando el juego pasa por una línea marcada, se pausa y VS Code te muestra esa línea con los valores de las variables.

1. Compilá con **Ctrl+Shift+B** (tarea "Compilar ROM"). Genera `fireemblem8.gba` y `fireemblem8.elf`. El `.elf` contiene el mapa entre la ROM y cada línea de C.
2. **Ctrl+Shift+P → Run Task → "Abrir juego en mGBA (esperando depurador)"**. mGBA abre y queda en pausa.
3. Apretá **F5**. VS Code se conecta y el juego arranca.
4. Hacé clic a la izquierda de un número de línea para poner un punto rojo (*breakpoint*). Cuando el juego llegue ahí, se congela.
5. En el panel **Ejecutar y depurar** tenés
   - **Variables**, con los valores en ese momento
   - **Inspección (Watch)**, donde podés escribir cualquier variable global, por ejemplo `gUnitArrayBlue[0]` (tu primera unidad), `gUnitArrayRed[0]` (primer enemigo) o `gBattleActor` (quien ataca)
   - **Pila de llamadas**, que muestra qué función llamó a cuál
6. F10 avanza una línea, F11 entra en la función, F5 continúa.

**Prueba recomendada.** Abrí `src/bmbattle.c`, poné un breakpoint en `ComputeBattleUnitAttack`, iniciá un combate en el juego y mirá `attacker->unit` en Variables.

**Aviso.** El juego está compilado con optimización, así que algunas variables locales aparecen como `<optimized out>`. Las globales y las estructuras (`gUnitArrayBlue`, `gBattleActor`) se ven siempre bien.

---

## 3. Mapa del código

| Qué querés cambiar | Dónde está |
|---|---|
| Stats, crecimientos y rangos de personajes | `src/data_characters.c` |
| Clases (bases, topes, promoción, movimiento) | `src/data_classes.c` |
| Armas e items | `src/data_items.c` |
| Terrenos (evasión, defensa, costo de movimiento) | `src/data_terrains.c` |
| Apoyos | `src/data_supports.c` |
| Fórmulas de combate, subida de nivel | `src/bmbattle.c` |
| Estructura de una unidad y sus banderas | `include/bmunit.h` |
| Eventos y diálogos de cada capítulo | `src/events/chN-eventscript.h` |
| Qué unidades aparecen en cada capítulo | `src/events/chN-eventudefs.h` |
| Condiciones de los eventos (hablar, visitar, turnos) | `src/events/chN-eventinfo.h` |
| Configuración de capítulos (mapa, música, objetivo) | `data/chapter_settings.json` |
| Textos del juego | `texts/texts.txt` |
| IA enemiga | `src/cp_*.c` |
| Mapa de mundo | `src/worldmap_*.c` |
| Pantalla de stats | `src/statscreen.c` |
| Menús del mapa | `src/bmmenu.c`, `src/menu_def.c` |
| Animaciones de batalla | `src/banim-*.c` |
| Arranque del juego | `src/main.c` (`AgbMain`) |
| Listas de IDs (personajes, clases, items, canciones) | `include/constants/` |

**Navegar.** Con F12 sobre cualquier nombre vas a su definición. Con Shift+F12 ves todos los lugares donde se usa. Con Ctrl+P buscás archivos por nombre.

---

## 4. Conceptos que conviene entender primero

### Personaje, clase y unidad
Están explicados con comentarios en `include/bmunit.h`. En resumen, `CharacterData` y `ClassData` son fichas fijas en la ROM, y `Unit` es la unidad viva en RAM durante la partida.

### Procs (el "motor" del juego)
Casi todo lo que pasa en pantalla es un *proc*. Un proc es una lista de pasos que se ejecuta un poco en cada cuadro. Se definen así.

```c
struct ProcCmd CONST_DATA ProcScr_Ejemplo[] = {
    PROC_CALL(FuncionA),      // ejecuta una vez
    PROC_SLEEP(30),           // espera 30 cuadros (medio segundo)
    PROC_REPEAT(FuncionB),    // ejecuta cada cuadro hasta que la funcion avance el proc
    PROC_END,
};
```

Cuando busques "qué pasa cuando hago X", buscá el proc. Los comandos están en `include/proc.h`.

### Eventos
Los eventos de capítulo son listas de macros, iguales en espíritu a las de Event Assembler y FEBuilder. Por ejemplo `MUSC` cambia la música, `LOAD1` carga unidades, `MOVE` mueve una unidad y `Text_BG` muestra un diálogo con fondo. Mirá `src/events/ch1-eventscript.h` como ejemplo completo.

---

## 5. Primer cambio de prueba

1. Abrí `src/data_characters.c` y buscá `[CHARACTER_EIRIKA - 1]`.
2. Cambiá `.baseSpd = 0,` por `.baseSpd = 10,`.
3. Ctrl+Shift+B para compilar.
4. Abrí el juego en mGBA, empezá partida nueva y mirá la velocidad de Eirika.

Desde que cambiás algo, la ROM ya no es idéntica a la original. Es lo esperado. Usá siempre la tarea "Compilar ROM" y no "Compilar y verificar".

---

## 6. Diferencias con FEBuilder

- No podés abrir en FEBuilder la ROM que sale de acá y seguir editándola en los dos lados. Elegí uno de los dos caminos.
- Agregar contenido nuevo (clases, personajes, capítulos) implica agregar entradas a las tablas y constantes en `include/constants/`. Es más trabajo inicial que FEBuilder, pero todo queda documentado y versionado.
- Gráficos y retratos se manejan como archivos PNG en `graphics/`. Se convierten solos al compilar.
- Usá git para guardar cada cambio (`git add -A && git commit -m "descripcion"`). Si algo se rompe, volvés atrás.
