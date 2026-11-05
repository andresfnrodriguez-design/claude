# Scripting de animaciones GBA — resumen para principiantes

## La idea básica

Un script es un archivo de texto (.txt) que le dice al juego, en orden, qué imagen mostrar y por cuánto tiempo, más algunos comandos especiales para cosas como "acá empieza el golpe" o "reproducí este sonido". Nada más complicado que eso — es una lista de instrucciones, de arriba hacia abajo.

## Las dos piezas que vas a usar todo el tiempo

**1. Líneas de imagen** — así se ven:
```
3 p- ataque01.png
```
- El primer número (`3`) es cuántos frames dura esa imagen en pantalla. El juego corre a 60 frames por segundo, así que `3` significa "mostrala durante 3/60 de segundo". Más alto = más tiempo en pantalla.
- `p-` va siempre igual, no lo toques.
- El nombre del archivo es el de tu imagen. Nombralas en orden (`ataque01.png`, `ataque02.png`...) para no perderte.

**2. Comandos (empiezan con C)** — le dicen al juego que haga algo en vez de solo mostrar una imagen. Por ejemplo, `C09` dispara el golpe crítico, `C01` le dice "esperá acá". Todo lo que sigue a un `#` es solo un comentario para vos, el juego lo ignora.

## Las "secciones" del script

Todo el archivo se divide en bloques, uno por cada tipo de animación. Cada bloque empieza así:
```
/// - Mode 1 #Melee Animation
```
y termina así:
```
~~~
```

Hay 12 números de "Mode" en total, pero en la práctica solo escribís contenido real en 10 de ellos (dos son automáticos y no hace falta tocarlos). Los que sí importan:

| Mode | Qué es |
|---|---|
| 1 | Ataque cuerpo a cuerpo |
| 3 | Crítico cuerpo a cuerpo |
| 5 | Ataque a distancia |
| 6 | Crítico a distancia |
| 7 y 8 | Esquivar (van con el mismo contenido en los dos) |
| 9, 10, 11 | Parado con el arma equipada (los tres son un solo frame quieto, iguales entre sí) |
| 12 | Cuando falla el ataque |

## El esqueleto de un ataque cuerpo a cuerpo, explicado paso a paso

Este es el orden real de lo que pasa en Mode 1 (y Mode 3 es exactamente igual, cambiando un solo comando):

1. **Arranca la animación** — dos comandos fijos que siempre van juntos: `C03` seguido de `C07`.
2. **Mostrás el frame parado**, después todos los frames de movimiento hasta el instante justo antes de que el golpe conecte.
3. **Tres comandos justo cuando conecta:** `C04` (le avisa al juego "preparate para bajar la vida del enemigo"), después `C1A` si es golpe normal o `C09` si es crítico, y `C1F` (el sonido del golpe).
4. **Más frames** — lo que pasa justo después del impacto, mientras la vida del enemigo todavía no bajó.
5. **`C01`** — es una pausa: "quedate acá hasta que la vida del enemigo termine de bajar en pantalla".
6. **Frames de vuelta a la posición normal.**
7. **Cierre fijo:** `C06` seguido de `C0D`.

Ejemplo armado con nombres de archivo de mentira:
```
/// - Mode 1 #Melee Animation
C03
C07

1 p- parado.png
3 p- ataque01.png
3 p- ataque02.png

C04
C1A
C1F

3 p- ataque03.png

C01

3 p- vuelta01.png

C06
C0D
~~~
```

**¿Y el crítico (Mode 3)?** Copiás exactamente esto, cambiás `C1A` por `C09`, y metés tus frames del golpe crítico en vez de los del ataque normal. Nada más cambia.

## Ataques a distancia y magia (Mode 5 y 6)

Misma estructura, pero en vez de `C1A`/`C09` + `C1F`, usás un solo comando: `C05` (esto dispara el hechizo o el arma arrojadiza asociada). Y esta vez el MISMO comando sirve tanto para golpe normal como crítico — no hay que cambiar nada entre Mode 5 y Mode 6 salvo los frames.

## Esquivar (Mode 7 y 8)

Más corto todavía: frame parado → comando `C0E` (arranca la esquiva) → un frame de transición → el frame ya esquivado → `C01` → otro frame de transición → cierre con `C06`/`C0D`. Se usa el mismo contenido para Mode 7 y Mode 8.

## Parado con arma (Mode 9, 10, 11)

Lo más simple de todo: un solo frame parado, seguido de `C01`. Los tres modes llevan exactamente lo mismo.

## Cuando falla el golpe (Mode 12)

Copiás entero el Mode 1, le sacás las líneas de `C1A` y `C1F` (el golpe y su sonido), y listo. Para magia/arco ni siquiera hay que sacar nada — se copia tal cual.

## Casos especiales, resumidos

- **Hachas:** necesitan DOS scripts separados — uno para el golpe cuerpo a cuerpo, otro para cuando se tira el hacha a distancia. En el script de cuerpo a cuerpo, dejás el Mode 5 vacío (solo el frame parado); en el script separado de tirar el hacha, ahí sí metés la animación completa en Mode 1 y 5.
- **Capas u objetos que se mueven en loop:** existe el comando `L`, que hace que un grupo de frames se repita en bucle hasta que la animación principal termine — útil para que algo (como una capa) se siga moviendo mientras el personaje sostiene una pose.

## Tips prácticos para no perderte

- Nombrá los frames en orden numerado (`ataque001.png`, `ataque002.png`...) — así es imposible confundir el orden al armar el script.
- Guardá el script y todas las imágenes en la misma carpeta.
- Para probarlo: abrís FEBuilder → Image editors → Battle animations → importás tu script. Si algo está mal, FEBuilder te dice exactamente qué imagen o qué línea tiene el problema — leé ese mensaje con atención antes de asumir que tenés que rehacer todo.
