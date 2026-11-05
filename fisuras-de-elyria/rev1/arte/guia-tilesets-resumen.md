# Tilesets en FE8 — resumen práctico

*Basado en la guía de DerTheVaporeon. Está escrita para importar tilesets de otros juegos FE, pero la estructura técnica aplica igual si dibujás los tuyos propios desde cero — que es probablemente tu caso.*

## La estructura básica

Hay tres piezas separadas que trabajan juntas:

1. **El Object Map (u "hoja chica")** — la imagen fuente real, máximo 256x256 píxeles, donde vos dibujás tus tiles individuales. Esto es lo que vas a crear vos.
2. **El Tile Config** — le dice al juego cómo agarrar pedazos de esa hoja chica y armar el mapa grande que el jugador realmente ve. No dibujás esto directamente, se genera/edita con la herramienta.
3. **La Paleta** — los colores, en una dirección de memoria separada de la imagen en sí.

## El dato nuevo importante: cada tile de 16x16 en realidad son cuatro de 8x8

Ya sabías que un tile completo es 16x16 píxeles. Lo que quizás no sabías: internamente, ese tile se arma con **cuatro sub-tiles de 8x8 cada uno**, y cada uno de esos cuatro pedacitos puede usar su propia fila de paleta de forma independiente. El ejemplo que da la guía es un cofre — sus cuatro cuadrantes de 8x8 se pueden mezclar y combinar con distintas paletas para variar el resultado final.

## Los colores: más margen del que parece

Igual que con los sprites, cada **fila** de paleta tiene máximo 16 colores. Pero un tileset completo tiene **cinco filas de paleta** (más otras cinco filas separadas exclusivamente para el Fog of War, si tu hack lo usa). El índice de cada tile sube de a `0x1000` según qué fila de paleta esté usando.

Esto significa algo útil para vos: **no estás limitado a 16 colores en todo el tileset**, estás limitado a 16 colores *por fila*, con cinco filas disponibles. Si repartís bien qué tiles usan qué fila (por ejemplo, una fila para tonos de piedra, otra para vegetación, otra para agua), el rango de color efectivo de un mapa completo es bastante más amplio de lo que "16 colores" sugiere a primera lectura.

## Terreno: no es solo estética

Cada tile individual tiene asignado un **tipo de terreno** (de una lista desplegable — llanura, bosque, etc.) directamente en el editor. Esto no es decorativo: define el costo de movimiento, si da bonus defensivo, y esas cosas por el estilo. Cuando diseñes tiles nuevos para las ambientaciones que ya definimos (ruinas griegas, nieve de Kaldholt, zonas industriales de Ferannor), vas a tener que asignarles el terreno correspondiente, no solo dibujarlos.

## Animaciones de tile — dos tipos distintos

- **Tipo 1 (por imagen):** varios frames dibujados a mano que se van alternando — así se anima el agua o una antorcha en los juegos vanilla. Hasta 16 frames por animación, cada uno como una imagen separada.
- **Tipo 2 (por ciclado de color):** en vez de cambiar de imagen, se van cambiando los COLORES de la paleta en un rango específico — así se logra el brillo pulsante de la lava en FE8 vanilla, sin necesitar frames de imagen adicionales. Más liviano, pero solo sirve para efectos de "brillo/pulso", no para movimiento real.

Para tu mundo, el Tipo 2 podría ser una forma barata de conseguir el resplandor de una fisura activa (el violeta que definimos en las notas de ambientación) sin tener que animar frame por frame.

## El flujo de trabajo real en FEBuilder (aplica ya sea que importes o dibujes desde cero)

1. Abrís el Tileset Editor (Advanced Editors → Tileset Palette).
2. **Export Image** — te da el archivo base para editar.
3. Editás esa imagen en un programa externo (la guía recomienda GraphicsGale o Usenti específicamente para este tipo de trabajo).
4. **Import Image** de vuelta.
5. **Import Tile Config** — así el juego sabe cómo armar el mapa grande con tus tiles nuevos.
6. Para usar este tileset en un mapa nuevo, en el Chapter Editor asignás qué número de ObjectType/Palette/TileConfig le corresponde a esa misión.

## Lo que la guía NO cubre (y vale la pena saber que falta)

Es explícito en el propio texto: *"A tileset editing tutorial will be on the works soon"* — es decir, esta guía cubre cómo INSERTAR un tileset ya armado, no cómo diseñarlo desde cero pixel por pixel.

## Actualización — encontré la guía de creación real (GBA Map Hacking Suite)

Esta sí cubre el proceso completo de armar un tileset desde cero, con una herramienta separada (basada en Tiled + un runtime de Lua). Confirma exactamente tu dato de que el lienzo completo es 512x512, dividido en máximo 5 franjas de arriba hacia abajo.

**Colores por franja:** acá hay un matiz que corrige lo que veníamos manejando — cada franja tiene **15 colores utilizables, no 16**, porque el primer color de cada una está reservado para transparencia. No es que contradiga la regla de 16 colores de antes, es la misma idea contada distinto: 15 útiles + 1 transparente = 16 total, igual que en los sprites de batalla.

**Las 5 franjas no son arbitrarias:** el ejemplo de la guía las organiza por categoría de terreno — construcciones, agua, bosque, montañas, tierra. No hace falta usar exactamente 5; se puede usar menos (hasta una sola franja), siempre que el ancho total sea 512 y el alto total también sea 512.

**El proceso, resumido:**
1. Armás el tileset como imagen, respetando el límite de color por franja.
2. Lo importás a Tiled (el editor de mapas externo) y le asignás el terreno a cada tile usando la herramienta de terreno de Tiled — cada terreno necesita una propiedad "ID" que coincide con una lista de referencia, así el juego sabe qué tipo de terreno es cada uno.
3. Armás el mapa real en Tiled con tu tileset, nombrando la capa principal "Main". Los eventos de mapa (tomar una puerta, destruir una aldea) van en capas separadas con sus propias coordenadas.
4. Exportás como `.lua`, lo procesás con una herramienta de línea de comandos (`grit`) que convierte cada franja, y hay que sumar el tamaño resultante de las 5 partes y confirmar que quede por debajo de un límite técnico (1024 bytes) antes de poder insertarlo.
5. Terminás con varios archivos `.dmp` (paleta, imagen, configuración, mapa) que se insertan en el ROM y se apuntan desde el editor de capítulos.

**Limitación importante para tener en cuenta:** esta herramienta específica **no soporta animaciones de tile**. El autor explica por qué a nivel técnico — Tiled anima cambiando qué tile se referencia, pero el juego anima sobreescribiendo directamente los píxeles en memoria, y esos dos enfoques no son compatibles entre sí con este método. Esto no contradice lo que ya vimos sobre animaciones Tipo 1 y Tipo 2 en FEBuilder — esas siguen siendo válidas — pero si usás esta herramienta externa para crear el tileset base, cualquier animación (como el brillo de una fisura activa) la vas a tener que agregar después, por separado, directamente en FEBuilder, no con esta suite.

## Pendiente para cuando avancemos
- Definir cuántas filas de paleta le vamos a asignar a cada ambientación de las que ya tenemos en las notas de mapas (Elyria, Kaldholt, Ferannor, etc.).
- Decidir si las 5 franjas de un tileset van a seguir la misma lógica de categoría (construcciones/agua/bosque/montaña/tierra) para todos los biomas, o si cada ambientación necesita su propia repartición.

