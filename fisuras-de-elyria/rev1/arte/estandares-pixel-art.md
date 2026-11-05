# Fisuras de Elyria — estándares de arte

Reglas visuales confirmadas para todo el arte del hack. Aplican a cualquier imagen nueva o modificada.

## Flujo de trabajo

1. **Concept art** con Nano Banana. Sirve para decidir el diseño, no es el asset final.
2. **Sprite final** con PixelLab, usando el concept art aprobado como imagen de referencia.
3. **Estandarización** de los frames (paleta, contorno, lienzo) antes de meterlos al juego.

## Concept art (Nano Banana)

- Personajes nuevos en estilo anime/manga. Los diseños anteriores se quedan en su estilo pintado original, no se rehacen.
- Densidad aetherpunk alta. Capas de objetos sobre el personaje (correas, hebillas, herramientas, engranajes, frascos), no un solo detalle de acento.
- Cada diseño necesita un gancho narrativo concreto y propio del personaje. Evitar arquetipos genéricos ("sabio anciano", "mercenario").
- Cada personaje lleva el arma específica de su clase según la tabla de armas, no un arma genérica.
- Sin restricciones técnicas de sprite (colores, fondo, cel-shading). Puede ser ilustrativo y con renderizado.
- Formato recomendado. Hoja de personaje (turnaround) de frente y de costado, pose neutra.

## Sprites de batalla (PixelLab)

- **Ángulo.** 3/4 hacia la cámara, nunca perfil estricto.
- **Paleta.** Máximo 16 colores en total, fondo y contorno incluidos.
- **Contorno.** Un único color oscuro `#282828` en todo el sprite, nunca negro puro ni varios negros distintos.
- **Fondo.** Verde plano `#A9CBA6`, sin escenario, para recortarlo después.
- **Estilo.** Cel-shading duro, bloques de color planos, sin degradés ni anti-aliasing.
- **Iluminación.** Asimétrica. El lado del personaje que mira a la cámara es más claro que el lado opuesto.
- **Sombras.** Siguen la forma real de la silueta, no manchas genéricas.
- **Altura del personaje** (de la punta del pie a la cabeza). Unos 34 px para hombres adultos y unos 32 px para mujeres. Nemira es una excepción deliberada de 60 px.
- **Tamaño de lienzo.** Se define en la interfaz de PixelLab, no en el prompt. Para Kairon se usó 36×64.
- Subir siempre el concept art aprobado junto con el prompt, para que respete cara, colores y silueta.

## Frames de animación de batalla

- **Lienzo.** 248×160 px.
- **Posición.** Personaje centrado horizontalmente en x = 140, con el pie más bajo apoyado en y = 102.
- **Paleta.** Los mismos 16 colores como máximo en todos los frames de una animación. Si un frame se pasa, hay que corregir toda la secuencia.
- **Sin muestra de paleta dentro de la imagen.** Los frames van limpios.

### Proceso de estandarización de cada frame

Los generadores de IA suelen entregar fondo verde puro y varios negros distintos, por eso cada frame pasa por estos pasos en orden.

1. Espejar horizontalmente si el frame mira hacia el lado incorrecto.
2. Reemplazar el fondo `#00FF00` por `#A9CBA6`.
3. Convertir todos los píxeles muy oscuros (suma R+G+B menor a 70) en `#282828`.
4. Reducir a 16 colores como máximo, sin dithering.
5. Colocar en el lienzo de 248×160 con el centro en x = 140 y los pies en y = 102.

## Mapas

- Sprites de mapa entre 16×16 y 32×32 según la unidad (las montadas ocupan más).
- Tiles de terreno de 16×16 px.
- Para bajar pixel art generado a su resolución real, usar "Unzoom pixel art" de PixelLab, no un redimensionado común.

## Revisión

- Espejar el sprite horizontalmente en algún momento para detectar errores que de frente cuestan ver.
- Pedir una mirada fresca de otra persona cuando el sprite esté armado.
