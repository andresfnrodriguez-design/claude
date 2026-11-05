# Megaprompt 2 — Íconos de botín, crítico y efectividad en el mapa (FE8 / fireemblem8u)

## Contexto

Trabajo en **Fisuras de Elyria**, un ROM hack de Fire Emblem 8 (The Sacred Stones) hecho sobre la decompilación **fireemblem8u** (C compilado con agbcc, WSL + VS Code, pruebas en mGBA). Quiero agregar íconos sobre las unidades del mapa para avisar al jugador del botín y del peligro, como hacen algunos hacks de GBA.

Hay una segunda implementación en paralelo: una **barra de vida de 14x3 px** en las 3 filas inferiores de la casilla de cada unidad. Los íconos no pueden taparla y los dos sistemas compiten por OAM, paletas y VRAM, así que tenlo en cuenta.

## ANTES DE ESCRIBIR CÓDIGO: dame feedback

Respóndeme primero, sin implementar nada, con estas secciones:

1. **Lo que entendiste.** Resume cada ícono: cuándo aparece, sobre quién y dónde va.
2. **Viabilidad.** Analiza:
   - Cómo detectar en FE8 la fase en que el jugador eligió una unidad y se ve la flecha de movimiento: qué proc, qué estado o qué variable global la identifica (por ejemplo `gActiveUnit` y el proc de movimiento del jugador). Indica la función o el símbolo concreto.
   - Paletas y VRAM de OBJ libres para los gráficos nuevos.
   - Límite de OAM con muchas unidades hostiles en pantalla.
   - Costo de CPU de calcular la efectividad contra la unidad elegida para cada hostil en cada fotograma, y si conviene calcularlo una sola vez al elegir la unidad y guardarlo en caché.
3. **Sacrificios.** Qué tendrías que simplificar y qué alternativa propones.
4. **Dudas.** Cualquier ambigüedad que encuentres.
5. **Plan.** Archivos y funciones que vas a tocar y en qué orden. `PutUnitSpriteIconsOam` en `src/bmudisp.c` ya dibuja los íconos vanilla (estado alterado, rescate, jefe) y es el punto de partida natural.

Solo cuando te confirme el plan, implementa.

## Especificación

### Íconos que ya existen en vanilla, NO se tocan
- El estado alterado (silencio, sueño, berserk, veneno) arriba de la unidad, más el ícono de rescate y el de jefe. Solo hay que evitar que los íconos nuevos se superpongan con ellos.

### Ícono 1: bolsa de botín (verde, parpadea)
- **Condición:** la unidad soltará un objeto al morir (`unit->state & US_DROP_ITEM`).
- **Cuándo:** **siempre visible** en el mapa, no solo durante la selección. Es mi propuesta: avísame si ves algún motivo en contra.
- **Bandos:** cualquier unidad que tenga la marca (en la práctica, enemigos).
- **Posición:** esquina **inferior izquierda** de la casilla, **por encima** de la barra de vida (al menos 3 px más arriba que en un diseño sin barra).
- **Parpadeo:** 32 fotogramas visible y 32 oculta (configurable).
- **Choque con el ícono de rescate vanilla:** si la unidad tiene los dos, se **alternan** usando el mismo ritmo de parpadeo.

### Íconos 2 y 3: los `!` de peligro
**Cuándo aparecen:** **solo** mientras el jugador tiene elegida una unidad propia y se ve la flecha o el rango de movimiento. Al confirmar o cancelar el movimiento, desaparecen.

**Sobre quién:** sobre **todas las unidades hostiles a la unidad elegida**, de cualquier bando. Es decir, las que cumplen `!AreUnitsAllied(unidadElegida, otra)`, incluidos los enemigos y el 4.º bando. Los aliados no.

**`!` amarillo (crítico):**
- **Condición:** el crítico del **arma equipada** del hostil es igual o mayor que el de la Espada asesina (`GetItemCrit(GetUnitEquippedWeapon(u)) >= HPICON_CRIT_MIN`, 30 en vanilla, en un `#define`).

**`!` rojo con fondo blanco (efectividad):**
- **Condición:** el **arma equipada** del hostil es **efectiva contra la clase de la unidad elegida**. Se usan las tablas de efectividad del juego (`GetItemEffectiveness` y la lógica de `IsItemEffectiveAgainst` o equivalente), incluidas las protecciones como el escudo de Hoplon o el de Fili si existen.
- Ejemplos: martillo contra caballero acorazado, matajinetes contra jinetes, matadragones contra wyverns.
- **Arcos:** se incluyen. Como la efectividad se calcula contra la unidad elegida, solo aparecen cuando mueves un volador. Añade un `#define HPICON_EFFECTIVE_INCLUDE_BOWS 1` para poder sacarlos.

**Si el arma tiene crítico alto y es efectiva a la vez:** los dos `!` se **alternan** con el mismo ritmo de parpadeo que la bolsa (es mi propuesta, dime si prefieres que gane el de efectividad).

**Posición de los `!`:** esquina **superior derecha** de la casilla, sin taparse con el ícono de estado alterado, que va arriba y centrado.

### Gráficos
- Los íconos se dibujan en 8x8 (o en el tamaño que me propongas) con 16 colores, en una paleta de OBJ compartida o en la misma de los íconos vanilla si alcanza.
- **Bolsa:** verde con borde oscuro.
- **`!` crítico:** amarillo con borde oscuro.
- **`!` efectividad:** `!` rojo sobre un cuadro blanco con borde oscuro.
- Si hace falta, genera arte provisional; lo reemplazo después. Indica el formato y la ruta (`graphics/...png`) y cómo se convierte en el build (gbagfx o equivalente).

### Configuración
Todo tiene que quedar en `#define` al principio del archivo: umbral de crítico, si se incluyen los arcos, ritmo del parpadeo, posiciones (x, y) de cada ícono y la prioridad cuando se superponen.

## Entregables (después de confirmar el plan)
1. Un parche (`git diff`) aplicable con `patch -p1` sobre fireemblem8u, que conviva con el de las barras de vida.
2. Que compile con `make` sin warnings nuevos.
3. Una captura o maqueta de una casilla con todos los íconos y la barra a la vez, para verificar que no se tapan.
4. Una lista de lo que se probó y lo que falta probar en mGBA. Por ejemplo: elegir un paladín cerca de un enemigo con matajinetes y comprobar que aparece el `!` blanco, y que desaparece al cancelar.
