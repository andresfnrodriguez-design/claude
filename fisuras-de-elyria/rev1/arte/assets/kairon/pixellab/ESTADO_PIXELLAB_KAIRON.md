# Estado del sprite de mapa de Kairon con PixelLab (7 nov 2026)

Léelo entero antes de tocar PixelLab. Resume lo que Andrés probó en la web de PixelLab, qué funcionó, qué no, y qué falta.

## Objetivo

Sprite de mapa de Kairon para FE8 (reemplaza a Ephraim). Infantería, **16 de alto, nunca más de 17**, 14 o 15 de ancho como máximo, con piernas y botas. Paleta azul de aliados con contorno `#282828`. Túnica blanca con ribetes y faja del bando. Las unidades vanilla del mapa miden entre 15 y 17.

## Referencia objetivo de Andrés

`ref_objetivo_hoja_espadachin.png` (captura ampliada x6) y `ref_objetivo_hoja_espadachin_nativo.png` (a 1x). Es el nivel que hay que lograr. Hoja de un espadachín azul en celdas de 32x32, con la figura de unos 14 a 15 px de alto contando una sombra suave bajo los pies, cabeza grande, 2 tonos por color, contorno oscuro y siluetas muy simples. Columnas con quieto, caminata de costado, hacia abajo, hacia arriba y ataque, en 4 cuadros cada una. Úsala como referencia de **tamaño, simplicidad y lectura**, no de colores ni de arma.

## Lo que funcionó (en la web, lo hizo Andrés)

**Create from Text, modo Pro (Create Character).** Es la única configuración que dio pixel art bueno y con el diseño correcto.
- Camera View Low Top-Down, opción Create with Style/Concept, Character Size 32px.
- Sin Style Character ni Style Image.
- Paleta propia subida en Color palette, Max colours igual a la cantidad de colores de la paleta.
- Referencias con texto de uso explícito ("copy only outfit and colors", "do not copy pose, proportions or style").
- Descripción en inglés con colores en hex, proporciones y reglas de render.

Resultados, en esta carpeta.
- `v2/fuente_pixellab_8dir_v2.gif`. Primer resultado bueno, paleta crema original. 23 a 24 de alto.
- `v4/kairon_v4_8dir.gif` y `v4/kairon_v4_<dir>_completo_32x32.png`. **El mejor hasta ahora.** Paleta azul de 11 colores, túnica blanca, faja azul, guantelete de bronce con gema. 20 a 21 de alto, 11 a 15 de ancho. En las vistas sur, sureste, este y noreste PixelLab dejó un rectángulo marrón de fondo, que ya está borrado en los PNG `_completo`.

## Lo que no funcionó

- **El tamaño por texto.** Character Size es la altura aproximada del personaje y le gana a la descripción. Con 32px salieron personajes de 20 a 28 aunque el texto pidiera 16. El mínimo en Pro es 32.
- **Standard (24px).** Salió de 27, ignoró el diseño y usó 21 colores.
- **Create from Reference (v3 y Standard).** Usa la imagen tal como está dibujada y saca el personaje del mismo tamaño del lienzo. No achica. Sirve para completar direcciones de un sprite que ya tenga la medida final.
- **Recortar filas de abajo** a 17 deja a Kairon sin piernas, y así no se puede animar la caminata.
- **`create_image_pro` con la hoja de Aethrall como style_image** (tanda A, 64 candidatos, 10 créditos). Copió la paleta marrón y salieron 64 manchas casi iguales. No usar Aethrall como estilo.
- **Paleta con casi negro `#1E1A20`.** PixelLab lo usó para contornear toda la silueta.

## Lo que falta probar (tu tarea)

`create_image_pro` con **lienzo de 16x16**, que la web no ofrece. Así PixelLab no tiene lugar para dibujarlo más grande y tiene que hacerlo entero, con piernas, en 16.

Archivos de esta carpeta para la llamada.
- `kairon_paleta_azul_aliados.png`. Paleta de 11 colores, un color por píxel: `#282828 #3C2C58 #1E2C6C #2F5CC8 #3EA0E8 #9CE4F8 #D0C8F0 #F0F0E8 #F4D8B8 #C08A68 #6A4A48`.
- `descripcion_kairon_16x16.txt`. Descripción para el lienzo de 16x16.
- `v4/kairon_v4_sur_completo_32x32.png`. Referencia principal (diseño, colores y estilo que Andrés aprobó).
- `kairon_ref_sur_256_nitida.png`. Ilustración de frente de Nano Banana con el mismo diseño, ya pasada a la paleta. Referencia secundaria de diseño.

## Reglas

- Claude Code no dibuja ni retoca píxeles. Solo lanza PixelLab, ordena y convierte con scripts.
- Antes de cualquier generación dices cuántos créditos quedan y si hay alguna tanda en curso, y esperas el "dale" de Andrés.
- Una sola llamada por aprobación. Nunca dos tandas seguidas.
- Lo generado no se reduce.
- Resultados x8 y numerados para que Andrés elija.

## Después de elegir

1. Pasar el elegido a la paleta de aliados (índice 15 = `#282828`), con el script de `../mapa_pixellab_azul/`.
2. Subirlo como Front en Create from Reference para completar las direcciones a ese tamaño.
3. Animar la caminata (oeste, sur, norte) y armar `unit_icon_wait` (16x96, cuadros de 16x32) y `unit_icon_move` (32x480).
4. Probar en el mapa con la barra de vida tapando la base de los pies, como las unidades vanilla.
