# Arte — índice

Concept art, retratos, sprites, paletas, pantalla de estado y tilesets.

> Copia del índice de Arte del proyecto de claude.ai, para que Claude Code en VS Code lo lea al actualizar. Última sincronización 7 nov 2026.

## Documentos

| Archivo | Qué es |
|---|---|
| `estandares-pixel-art.md` | Reglas cortas de concept, sprites, frames y mapas. **Empezar acá** |
| `biblia-visual.md` | Paletas por región, vestuario, objetos recurrentes, ambientaciones y retratos por personaje |
| `GUIA_SPRITES-mapa.md` | Sprites de mapa, paletas por bando, rampas, cuerpo más cabeza, contorno |
| `prompts_nano_banana.md` | Prompts de las tres hojas de plantilla y tres personajes de prueba (Teodora, Lysandros, Ione). El de la hoja 4 está abajo |
| `pantalla-estado/README.md` | Uso de los scripts de la pantalla de estado |
| `pixellab-map-tools.md`, `guia-tilesets-resumen.md` | PixelLab (Create Map y Create Tileset) y cómo se arma un tileset |
| `guia-scripting-resumen.md`, `referencia_imagenes_script.md` | Scripting de animaciones de batalla y tabla de frames de Kairon |
| `scripts/` | Scripts completos en bloques de código, listos para copiar |
| `referencias/guia-scripting-animaciones-original.txt` | Guía original de scripting de animaciones |
| `referencias/pixel_art_andres_aethrall.png` | **Referencia de estilo.** Hoja de pixel art de Andrés (firma Aethrall), ver "Estilo de pixel art" abajo |

## Dirección de arte (desde el 7 nov 2026)

**La línea a seguir es el arte de personajes de *The Banner Saga*.** Andrés lo eligió porque es un mundo visualmente rico y creíble. Esa saga se inspira en la tradición vikinga, y Elyria toma el mismo lenguaje visual pero con su propia cultura, griega y aetherpunk. Se toma el estilo, no los personajes ni los diseños.

Rasgos del estilo.
- **Línea.** Contorno fino y limpio de grosor parejo, oscuro y casi nunca negro puro. Pocas líneas interiores, solo las que definen pliegues y rasgos.
- **Color.** Planos de color con un sombreado suave de uno o dos tonos, sin brillos de anime ni degradados fuertes. Paletas apagadas y terrosas (grises, marrones, azules pizarra, crema) con un solo acento saturado por personaje, como un dorado, un rojo o un turquesa.
- **Proporciones.** Realistas, de 7 a 8 cabezas, nada de chibi ni de ojos grandes. Caras con edad, cansancio y carácter, narices y pómulos marcados, barbas y trenzas con forma.
- **Vestuario.** Telas pesadas en capas (capas, pieles, túnicas, cinturones anudados) con patrones textiles finos. En Elyria los nudos celtas se cambian por motivos griegos (meandros, grecas, rosetas) y el metal y el cuero aetherpunk (engranajes, remaches, frascos, cristales de aether).
- **Objetos.** Armas y bastones con tallado y desgaste. Los adornos son pocos y significativos, como un broche, una cuenta o una pieza de metal.
- **Escenarios.** Formas planas en capas, siluetas recortadas contra cielos de color pleno (turquesa, rojo de atardecer, azul noche), árboles y ramas como manchas oscuras y gráficas, y ejércitos en silueta en el horizonte.
- **Encuadre.** Bustos de tres cuartos con la mirada firme, y figuras de cuerpo entero de frente y de espaldas para las hojas de personaje.

**Qué cambia en la producción.**
- El concept art con Nano Banana deja de ser estilo anime y pasa a este. Las instrucciones del Gem y las plantillas tienen que decir el estilo con palabras, sin nombrar el juego.
- Los retratos de 100x112, el estado y el zoom se piensan con caras de este estilo. Al reducirlos a 16 colores hay que conservar la línea fina y el acento único.
- El pixel art chico (mapa y batalla) sigue la referencia de Andrés, "Estilo de pixel art", que ya es compatible con estas paletas apagadas y con un acento.
- La ficha actual de Kairon es de estilo anime. Conviene rehacerla en esta línea antes de producir más assets.

Texto de estilo para los prompts de imagen (en español, para el Gem).

```
Ilustración de personaje con línea fina y limpia de grosor parejo, oscura pero no negra pura, y pocas líneas interiores. Colores planos con sombreado suave de uno o dos tonos, sin brillos ni degradados. Paleta apagada y terrosa con un solo acento saturado. Proporciones realistas, cara adulta con carácter y marcas de vida, nada de estilo anime. Ropa en capas de tela pesada con patrones griegos finos (meandros, grecas) y detalles aetherpunk de bronce, cuero y cristal de aether. Fondo liso.
```

## Flujo de producción

1. **Concept art con Nano Banana.** Decide el diseño, no es el asset final. Estilo según la "Dirección de arte" de arriba (ya no anime), densidad aetherpunk alta (correas, hebillas, herramientas, frascos), gancho narrativo propio y el arma de su clase. Relación 3:2, máxima calidad. Son cuatro hojas. La hoja 1 sale de la plantilla sola, y las hojas 2, 3 y 4 llevan su plantilla más la hoja 1 como referencia.
2. **Asset final con PixelLab**, subiendo siempre el concept aprobado.
3. **Estandarización con script** antes de meterlo al juego.

**Las cuatro plantillas (vigentes desde el 5 nov 2026, `plantillas_elyria.zip`).**

| Hoja | Contenido |
|---|---|
| `hoja1_concepto.png` | Giro completo, paleta de 16, expresiones, pose de ataque y detalles |
| `hoja2_retratos.png` | Escena, espejo real, estado de 80x144 (cabeza de 28 px, corte a media pierna), mini, bocas, ojos y poses alternativas |
| `hoja3_sprites.png` | Sprites de mapa y cuadros clave de batalla |
| `hoja4_zoom.png` | Primer plano grande de la cara que va de fondo a pantalla completa (240x160) en el menú de estado, con la interfaz encima, y su versión HERIDO |

**Gem Elyria Concept.** Claude maneja gemini.google.com en el Chrome de Andrés, dentro del Gem clásico Elyria Concept (`gemini.google.com/gem/c3b0cf9cf1b0`). Las hojas se cargan como capturas desde el artifact "Plantillas Elyria". Nunca más de 1K sin preguntarle antes a Andrés.

## Estándares vigentes

**Estilo de pixel art (referencia de Andrés, 7 nov 2026).** La hoja `referencias/pixel_art_andres_aethrall.png` es el estilo a seguir para sprites chicos y para pedirle a PixelLab. Contorno negro grueso y continuo alrededor de toda la silueta. Cabeza grande, cerca de un tercio de la altura. Ojos de 2 o 3 píxeles en línea vertical, sin cejas y sin pestañear. Sombreado plano de 2 o 3 tonos por material, sin degradados. Pocos colores por personaje, apagados y con un acento fuerte. Siluetas que se leen por la pose y el arma. Los personajes de la hoja miden entre 20 y 28 px de alto, así que para la infantería de 16x16 hay que achicar más el cuerpo que la cabeza. Incluye también íconos de ítems, árboles, rocas y cielos en cuatro horarios (nublado, cielo azul, amanecer y atardecer, noche).

**Proporciones del sprite de mapa de infantería (7 nov 2026).** 16 de alto con los pies en la fila 15. Cabeza de 6 px contando el contorno, torso y brazos de 5, piernas de 5. Pose de tres cuartos con el peso cargado en una pierna, como el ninja de `sprites-mapa/imagenes/ninja_original_captura.png`. El primer quieto de PixelLab salió con la cabeza de 9 px y quedó descartado.

**Colores del abrigo de Kairon en el mapa.** La luz del abrigo va en el índice 14 (blanco) y la sombra en el 3, así se lee crema y no lavanda. El color del bando (7 a 10) va solo en la faja y los ribetes. El índice 14 casi no cambia entre bandos, así que la identidad del bando la llevan la faja, los ribetes y la sombra.

**Retratos de escena.** Arte de 100x112 sobre una hoja de 104x112. 16 colores con `#A9CBA6` en el índice 0. Línea negra de 1 px en el borde y contorno blanco de 2 px por fuera (era de 1 px hasta el 7 nov 2026). 3 px de margen arriba, cabeza nunca cortada, silueta completa sin cortes laterales y proporción de Eirika. Se genera a 200x224 o 400x448 y se reduce por múltiplo exacto con voto mayoritario. Si el arte corta la silueta, se completa antes de escalar. El de 96x80 queda descartado.

**Retrato de pantalla de estado.** 80x144 en un marco de 88x152 en x=8, y=4. El de Kairon es de cuerpo entero, sin cortes laterales.

**Mini retrato.** 32x32 con la cara lo más grande posible y corte en los hombros. Sin borde blanco, ojos fijos de líneas verticales que no pestañean y sin cejas.

**Zoom del menú de estado.** Primer plano grande de la cara a pantalla completa (240x160) detrás de la interfaz. La pose, el gesto y el ángulo son libres para mostrar la personalidad. Solo conviene que ojos y boca no queden bajo la UI. Cada personaje lleva dos versiones, la normal y HERIDO, que el juego muestra cuando la vida baja del 25 %. La herida es la misma imagen con otra expresión, sin sangre, cortes, vendas ni marcas.

**Bocas y ojos.** El motor los anima solo. Se dibujan 6 bocas de 32x16 (normal y sonriendo, cerrada, media y abierta) y 2 ojos (entrecerrado y cerrado) sobre el pixel art final. Los de Kairon hechos por script quedaron mal y se rehacen con inpainting de PixelLab.

**Sprites de batalla.** Lienzo de 248x160, fondo `#A9CBA6`, contorno único `#282828`, máximo 16 colores en toda la animación, personaje centrado en x=140 con los pies en y=102. Altura de unos 34 px para hombres y 32 para mujeres. Quedan para más adelante.

**Sprites de mapa.** Figura de 16 px de ancho, 16 de alto para infantería y hasta 25 a 28 para jinetes. Quieto son 3 cuadros de 16x16. En movimiento son 15 cuadros en celdas de 32x32 (4 a la izquierda, 4 abajo, 4 arriba, 3 seleccionado), y la derecha la voltea el motor. 15 colores más transparente, con la misma estructura de posiciones en todas las paletas. Posiciones 7 a 10 para el color principal y 1 a 3 para el secundario pastel. Sin sombra bajo los pies.

**Por clase o por personaje.** Sprites de mapa y animaciones de batalla van por clase. Retratos, zoom de estado (normal y herido), paleta, paleta de batalla propia y voz van por personaje.

**PixelLab.** Antes de cada tanda de generaciones, Claude Code avisa cuántas y cuántos créditos gasta, y espera el visto bueno de Andrés.

## Assets de prueba de Kairon

Carpeta `assets/kairon/` en esta misma rama. La subcarpeta `para_decomp/graphics/` tiene las rutas y los nombres de la decomp, con el prompt `04-kairon-reemplaza-ephraim.md`. El trabajo con PixelLab va en `~/fireemblem8u/elyria_assets/kairon/pixellab/` de la computadora de Andrés.

## Abierto

- Rehacer la ficha de Kairon con la dirección de arte nueva y actualizar las instrucciones del Gem.
- Rehacer con inpainting de PixelLab el espejo real de Kairon y sus 6 bocas y 2 ojos.
- Sprite de mapa de Kairon. Corregir abrigo, postura y pelo del quieto v2, armar los 3 cuadros y después la hoja de movimiento con las proporciones nuevas.
- Implementación del zoom herido en el menú de estado.
- Personaje nuevo usuario de magia, a partir de la chica de anteojos y capa dorada de la escena grupal (no es Nemira).
