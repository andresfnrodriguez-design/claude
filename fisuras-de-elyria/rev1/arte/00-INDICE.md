# Arte — índice

Concept art, retratos, sprites, paletas, pantalla de estado y tilesets.

Hay una copia de este índice en GitHub (rama `claude/nifty-bell-x1mrwv`, `fisuras-de-elyria/rev1/arte/00-INDICE.md`) para que Claude Code en VS Code lo lea al actualizar. Cuando cambie algo acá, se actualiza también allá.

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
| `referencias/sprites-mapa/` | Referencias de proporción y de bandos para sprites de mapa (ninja, guitarrista, sprite alto, señor de la capa, bandos, arquero) |
| `inspo/paletas/` | Paleta del terreno del mapa (7 nov 2026). Imágenes de inspiración, pruebas de cada paleta sobre el capítulo 8 de FE8 y el editor `editor_paleta_mapa.html` (artifact "Paleta del mapa · Fisuras de Elyria"). El terreno usa 5 grupos de 16 colores (75 útiles) y el capítulo 8 usa 68. A Andrés le gustó de momento la de estilo Banner Saga como base. Detalle en su `README.md` |

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

1. **Concept art con Nano Banana.** Decide el diseño, no es el asset final. Estilo según la "Dirección de arte" de arriba (ya no anime), densidad aetherpunk alta (correas, hebillas, herramientas, frascos), gancho narrativo propio y el arma de su clase. Relación 3:2, máxima calidad. Son cuatro hojas. La hoja 1 sale de la plantilla sola, y las hojas 2, 3 y 4 llevan su plantilla más la hoja 1 como referencia. Toda figura de cuerpo entero tiene que entrar completa en su recuadro, con margen de fondo a los lados, porque una figura cortada no sirve como referencia.
2. **Pixel art con PixelLab, no con Claude.** Claude Code no dibuja píxeles. Lo generado no se reduce, porque al reducir se pierden los píxeles clave. PixelLab dibuja ya a la escala final dentro de un lienzo de 32x32 (su mínimo) y solo se recorta. El método aprobado es el de abajo, "Método de sprites con PixelLab".
3. **Estandarización con script** antes de meterlo al juego (paleta por posiciones, hojas, gbagfx).

**Las cuatro plantillas (vigentes desde el 5 nov 2026, `plantillas_elyria.zip`).**

| Hoja | Contenido |
|---|---|
| `hoja1_concepto.png` | Giro completo, paleta de 16, expresiones, pose de ataque y detalles |
| `hoja2_retratos.png` | Escena, espejo real, estado de 80x144 (cabeza de 28 px, corte a media pierna), mini, bocas, ojos y poses alternativas |
| `hoja3_sprites.png` | Sprites de mapa y cuadros clave de batalla |
| `hoja4_zoom.png` | Primer plano grande de la cara que va de fondo a pantalla completa (240x160) en el menú de estado, con la interfaz encima, y su versión HERIDO. Muestra las zonas que tapa la UI, una zona sugerida para los ojos, el ejemplo de Andrés (Kairos) y las reglas. La genera `hoja4_zoom.py` |

La referencia del zoom es la captura de Andrés del menú con Kairos (240x160), con la cara enorme detrás de stats, habilidades e íconos. La primera versión de la hoja 4 (`hoja4_estado.png`, retrato de 80x144 a x5) quedó descartada porque no era lo acordado.

Prompt de la hoja 4 (en inglés, como los otros).

```
Use the first image as the layout template and the second image as the character reference. Keep every box, border and label where it is, and draw only inside the boxes. Box backgrounds stay flat #A9CBA6 green. Remove the guides and the grey UI zones in the final image.

Fill the big ZOOM box with a large close-up of this character's face, used as the full-screen background of the status menu. The face fills a big part of the screen. The pose is free: any expression, gesture, pose or camera angle that shows the character's personality. Face and body can be tilted or leaning, they do not need to be straight or centered. Hair, hands, weapon and shoulders may run off the edges. The grey zones will be covered by the interface, so keep the eyes and mouth out of them. No UI, no text and no frame inside the art. The EJEMPLO image only shows the size of the close-up, do not copy that character or the interface.

Fill the HERIDO box with the same close-up: same pose, same framing, same camera angle. Only the expression changes, to pain, discomfort or sadness depending on the character's personality. No blood, no cuts, no bandages, no marks.

Style: GBA-era pixel art close-up, crisp pixels, 1 px dark lines, flat colors from the reference palette.

[PERSONAJE]
```

**Nano Banana automatizado (desde el 5 nov 2026).** Se genera con el comando `banana` en Ubuntu, que llama a la API de Gemini. Vive en `~/banana` (`banana.py`, `venv/` y `plantillas/` con las hojas) y la clave va en `GEMINI_API_KEY` dentro de `~/.bashrc`. Las imágenes y el prompt usado caen en `Downloads/Roms Fe/banana`. Claude arma el comando completo con el prompt en un bloque `EOF` y Andrés lo pega. Opciones `--ref` (repetible, rutas relativas a `~/banana`), `--nombre`, `--n` (variantes), `--ratio` (3:2 por defecto), `--tam` (1K por defecto, K mayúscula) y `--modelo` (`gemini-3.1-flash-image` por defecto, `gemini-3-pro-image` para Pro). Se instala desde `banana_setup.zip`. Cada imagen tarda entre 10 y 40 segundos.

**Vía preferida, Chrome con la suscripción.** Andrés tiene Google AI Pro (se pasó de Plus el 5 nov 2026). Claude maneja gemini.google.com en su Chrome dentro del Gem clásico **Elyria Concept** (`gemini.google.com/gem/c3b0cf9cf1b0`), con las cuatro hojas en Conocimiento, instrucciones del proyecto (incluidas la pose libre y la versión herida de la hoja 4) y herramienta predeterminada Imágenes. Claude no puede subir archivos locales a Gemini, así que las imágenes se cargan como capturas desde un artifact (las hojas desde "Plantillas Elyria", una por `#hoja1` a `#hoja4`) por el input oculto que aparece al abrir "Cargas y herramientas". Antes de cada descarga pide confirmación. Hay un Gem de Labs con el mismo nombre que no sirve (Labs deja de funcionar el 17 nov 2026, y desde esa fecha los Gems pasan a ser habilidades). Google AI Pro incluye $10 por mes en créditos de Cloud que se activan en me.developers.google.com/benefits, pero esos créditos se aplican a Vertex AI y no a la clave de AI Studio que usa `banana`.

**Descargas.** La carpeta de descargas de Andrés en Windows es `Downloads/Roms Fe` (`/mnt/c/Users/andre/Downloads/Roms Fe` desde Ubuntu). Los comandos que traen archivos de Gemini o PixelLab buscan ahí.

**Regla de tamaño.** Nunca más de 1K sin preguntarle antes a Andrés. Eso vale para `--tam 2K` o `4K`.

**PixelLab.** Conectado a Claude Code en Ubuntu con el MCP oficial (`https://api.pixellab.ai/mcp`) y usado también desde la web por Andrés. Antes de cada tanda de generaciones se avisa cuántas y cuántos créditos gasta, se confirma el saldo y que no haya otra tanda en curso, y se espera el visto bueno. El 7 nov 2026 se lanzaron dos tandas de `create_image_pro` por error (20 créditos) cuando se había aprobado una.

**Método de sprites con PixelLab (aprobado por Andrés el 7 nov 2026, "ese será el estilo de trabajo").** Andrés lo hace en la web de PixelLab, en Create Character (modo Pro), que da las 8 direcciones de una vez con una sola paleta.
- Camera View **Low Top-Down**, opción **Create with Style/Concept**, lienzo de **32x32**.
- **Referencia 1.** El concepto de cuerpo entero del personaje, sin recortes, con este uso. "Copy only this character's outfit and colors (…). Do not copy the pose, the proportions or the drawing style."
- **Style Character y Style Image vacíos.** Con la hoja de Aethrall como estilo, `create_image_pro` copió su paleta marrón y sacó 64 manchas casi iguales (tanda A del 7 nov). Fue un error de configuración, no de la herramienta.
- **Paleta propia** subida en Color palette (PNG de 15x1 con un color por píxel) y **Max colours 15**, que vale para las 8 direcciones juntas. La paleta no lleva casi negro, porque PixelLab lo usa para contornear toda la silueta.
- **Descripción** en inglés de hasta 2000 caracteres con pose de espera, proporciones, colores en hex y reglas de render. La de Kairon está en `assets/kairon/pixellab/descripcion_kairon.txt`.
- Cuesta 10 generaciones por personaje (las 8 direcciones).
- La vista sur (de frente) es el quieto del mapa y las demás direcciones dan las celdas de movimiento.

Primer resultado (Kairon, 7 nov 2026). Pixel art real con sus colores y el píxel cian, pero de 18x28, con contorno casi negro alrededor de toda la silueta (la paleta subida incluía `#1E1A20`) y un guantelete que no se lee. Se corrige editando ese mismo personaje, sin el casi negro en la paleta y con 16 de ancho como máximo.

## Estándares vigentes

**Estilo de pixel art (referencia de Andrés, 7 nov 2026).** La hoja `referencias/pixel_art_andres_aethrall.png` es el estilo a seguir para sprites chicos. Sin contorno negro alrededor de toda la silueta, porque en sprites tan chicos se come píxeles que tienen que mostrar algo (el arma, la cara, el guantelete). Se usa contorno selectivo: el borde de cada zona es un tono más oscuro de su propio material, y solo se marca donde hace falta separar la figura del fondo, sobre todo del lado de la sombra. Cabeza grande, cerca de un tercio de la altura. Ojos sin cejas y sin pestañear. En figuras de 20 a 28 px de alto, como las de la hoja, son de 2 o 3 píxeles en línea vertical. En el sprite de mapa de 16x16 son de 1 píxel o no hay, y de perfil se ve uno solo. Sombreado plano de 2 o 3 tonos por material, sin degradados. Pocos colores por personaje, apagados y con un acento fuerte. Siluetas que se leen por la pose y el arma. Incluye también íconos de ítems, árboles, rocas y cielos en cuatro horarios (nublado, cielo azul, amanecer y atardecer, noche). No se usa como Style Image en PixelLab (ver el método).

**Contorno inteligente en sprites de mapa (aprobado por Andrés el 7 nov 2026, "me encanta").** Se aplica por script después de generar, con `scripts/contorno_inteligente.py`. Agrega 1 px por fuera de la figura, solo en vecinos ortogonales. Cada píxel del borde toma un tono oscuro del material que tiene al lado. El lado de sombra (abajo y derecha, con luz desde arriba a la izquierda) va más oscuro que el lado de luz. El metal y los blancos usan gris oscuro (#282828 en sombra, #484850 en luz). Como la figura crece 1 px por lado, se genera de unos 15 de alto para terminar en 16 o 17. Probado sobre el ninja de Andrés (`assets/kairon/pixellab/ninja_contorno_inteligente_32x32.png`).

**Escala objetivo (7 nov 2026).** La hoja de espadachín azul que mostró Andrés (`assets/kairon/pixellab/ref_objetivo_hoja_espadachin.png`) es el nivel a lograr, con figuras de 14 a 15 px en celdas de 32x32. El ninja de Andrés (15x16) encaja exacto al lado de las unidades vanilla en el mapa. Para cada clase hace falta una pose a esa medida, y después Create from Reference (v3) de PixelLab completa las direcciones copiando el tamaño.

**Proporciones del sprite de mapa de infantería (7 nov 2026).** 16 de alto con los pies en la fila 15. Cabeza de unos 6 o 7 px de alto y 7 de ancho, torso angosto de 4 o 5 px, brazos y piernas finos con aire entre las piernas, y silueta irregular. Se toma de los sprites de Andrés (ninja, pícaro, hoja de Aethrall), no solo de las medidas escritas, porque con las medidas solas sale un bloque cuadrado. Sin sombra bajo los pies. Queda pendiente decidir si se pasa a 16 de ancho por unos 20 a 28 de alto en cuadros de 16x32, el formato del Ephraim original, porque las referencias que le gustan a Andrés y el primer Kairon de PixelLab miden entre 18 y 28 de alto.

**Pose del quieto (7 nov 2026).** El ninja da el estilo y las proporciones, pero no es el modelo de pose para todos. La pose se imagina para cada sprite según la clase o el personaje (cómo se para, cómo sostiene el arma, qué dice de su carácter) y se escribe en su descripción antes de generar. Con el método de PixelLab el quieto sale de frente (vista sur), como en FE.

**Colores del abrigo de Kairon en el mapa.** La luz del abrigo va en el índice 14 (blanco) y la sombra en el 3, así se lee crema y no lavanda. El color del bando (7 a 10) va en la faja y los ribetes. El índice 14 casi no cambia entre bandos. Queda pendiente decidir si el abrigo toma el color del bando, como en las referencias de bandos de Andrés.

**Retratos de escena.** Arte de 100x112 sobre una hoja de 104x112. 16 colores con `#A9CBA6` en el índice 0. Línea negra de 1 px en el borde y contorno blanco de 2 px por fuera (era de 1 px hasta el 7 nov 2026). 3 px de margen arriba, cabeza nunca cortada, silueta completa sin cortes laterales y proporción de Eirika. Se genera a 200x224 o 400x448 y se reduce por múltiplo exacto con voto mayoritario. Si el arte corta la silueta, se completa antes de escalar. El de 96x80 queda descartado.

**Retrato de pantalla de estado.** 80x144 en un marco de 88x152 en x=8, y=4, con 4 px de margen verde arriba y abajo y 8 px a la izquierda. El de Kairon es de cuerpo entero, sin cortes laterales.

**Mini retrato.** 32x32 con la cara lo más grande posible y corte en los hombros. Sin borde blanco, ojos fijos de líneas verticales que no pestañean y sin cejas.

**Zoom del menú de estado.** Primer plano grande de la cara a pantalla completa (240x160) detrás de la interfaz, según la captura de Kairos de Andrés. Acá el arte casi no tiene reglas de cámara. La pose, el gesto y el ángulo son libres para mostrar la personalidad, y la cara puede ir ladeada o inclinada, sin centrar. Solo conviene que ojos y boca no queden bajo la UI. Cada personaje lleva dos versiones, la normal y HERIDO, que el juego muestra cuando la vida baja del 25 %. La herida es la misma imagen con otra expresión (dolor, incomodidad o tristeza según la personalidad), sin sangre, cortes, vendas ni marcas.

**Bocas y ojos.** El motor los anima solo. Se dibujan 6 bocas de 32x16 (normal y sonriendo, cerrada, media y abierta) y 2 ojos (entrecerrado y cerrado), editando el pixel art final. Falta fijar sus coordenadas dentro del retrato de 100x112.

**Sprites de batalla.** Lienzo de 248x160, fondo `#A9CBA6`, contorno único `#282828`, máximo 16 colores en toda la animación, personaje centrado en x=140 con los pies en y=102. Ángulo 3/4, iluminación más fuerte del lado que mira a la cámara y sombra con la forma real de la silueta. Altura de unos 34 px para hombres y 32 para mujeres. El script de FEBuilder va en un solo .txt con los 12 modos. Los 16 colores se cuentan sumando todos los cuadros y todos los modos, no cuadro por cuadro. Los efectos (estallidos, destellos) se pintan con colores de la misma paleta.

**Sprites de mapa.** Figura de 16 px de ancho, 16 de alto para infantería y hasta 25 a 28 para jinetes. Quieto son 3 cuadros de 16x16. En movimiento son 15 cuadros en celdas de 32x32 (4 a la izquierda, 4 abajo, 4 arriba, 3 seleccionado), y la derecha la voltea el motor. 15 colores más transparente, con la misma estructura de posiciones en todas las paletas. Posiciones 7 a 10 para el color principal y 1 a 3 para el secundario pastel. Contorno selectivo, solo del lado de la sombra.

**Por clase o por personaje.** Sprites de mapa y animaciones de batalla van por clase. Retratos, zoom de estado (normal y herido), paleta, paleta de batalla propia y voz van por personaje. Queda pendiente decidir si los personajes con nombre tienen un quieto propio.

**Pantalla de estado (diseño cerrado).** 240x160, tema `gris_final`, fondo animado `fisuras_fucsia` (degradado teal a fucsia con 40 esquirlas lentas). El detalle de cada elemento está en `../sesiones/01-pantalla-estado.md`.

**Ficha oficial de Kairon.** Abrigo largo crema con lazo granate y guante de bronce (`47afd033-image.png`). La de "Wanderer Investigator" queda descartada. Está en estilo anime y hay que rehacerla con la dirección de arte nueva. El concepto de cuerpo entero sin recortes que se usa como referencia de PixelLab es `assets/kairon/pixellab/kairon_concepto_completo.jpg` (1792x2400, mira a la izquierda con el guantelete en su mano izquierda).

## Imágenes vigentes

Están en GitHub, rama `claude/fisuras-de-elyria-rev1`, carpeta `fisuras-de-elyria/rev1/arte/`. Las principales también van en `arte-imagenes-rev1.zip` para subir a los archivos del proyecto.

| Ruta | Qué es |
|---|---|
| `imagenes/retratos/portrait_kairon_100x112.png`, `portrait_referencia_100x112.png` | Retratos de escena finales para importar |
| `imagenes/retratos/estado_kairon_80x144.png`, `estado_referencia_80x144.png` | Retratos de pantalla de estado finales |
| `imagenes/retratos/mockups/` | Mockups a 240x160 de soporte y pantalla de estado |
| `pantalla-estado/tema_gris_final_*.png`, `anim_gris_final_*.gif` | Pantalla de estado final con Kairon y con el retrato 3 |
| `pantalla-estado/` | Además todos los scripts, temas y la entrada original |
| `imagenes/kairon/` | Frames del ataque y del crítico de Kairon (crudos) |
| `kairon_batalla_paleta_unica.zip` (5 nov 2026) | **Vigente para batalla.** Melee y crítico de Kairon a 248x160 con una sola paleta de 15 colores, GIF del crítico y script `paleta_unica_kairon.py`. Reemplaza a `imagenes/kairon/kairon_melee_frames_248x160/`, que sumaba 115 colores entre cuadros |
| `plantillas_elyria.zip` (5 nov 2026) | **Vigente para plantillas.** Las cuatro hojas y `hoja4_zoom.py`. Reemplaza a `plantillas/` del rev1 |
| `assets/kairon/` en la rama principal `claude/nifty-bell-x1mrwv` (también en `claude/kairon-assets`) | **Vigente para pruebas en el juego.** Assets de Kairon a la resolución del motor, que reemplazan a Ephraim. Detalle en la sección siguiente |
| `assets/kairon/pixellab/` en la rama principal | Método de PixelLab de Kairon. Concepto completo, paleta de mapa, descripción y primer resultado |
| `referencias/pixel_art_andres_aethrall.png` y `referencias/sprites-mapa/` en la rama principal | Referencias de estilo y de proporción de Andrés |
| `sprites-mapa/` | Scripts, paletas aprobadas, rampas, ninja y pícaro de prueba |
| `plantillas/` | Plantillas viejas de tres hojas para Nano Banana y su script |
| `imagenes/referencias/kairon_ficha_oficial.png` | Ficha oficial de Kairon |
| `imagenes/referencias/subidas-chat-historia/` | Concept art y capturas subidas en el chat de historia, sin duplicados |
| `imagenes/historico/` | Versiones intermedias de retratos, sprites y piezas |
| `scripts/` | Scripts de retratos y de batalla como archivos reales |

Las imágenes de *The Banner Saga* que mostró Andrés el 7 nov 2026 no se guardan en GitHub porque son de un tercero. La dirección de arte queda descrita con palabras arriba.

## Assets de prueba de Kairon

Rama principal `claude/nifty-bell-x1mrwv` (y `claude/kairon-assets`), carpeta `fisuras-de-elyria/rev1/arte/assets/kairon/`. Salen de las hojas de Gemini con `script/build.py`, que espeja todo (el guantelete queda en la mano izquierda) y arma una paleta única. El script se corre dos veces, la primera arma la paleta. La subcarpeta `para_decomp/graphics/` tiene las rutas y los nombres de la decomp, con el prompt `04-kairon-reemplaza-ephraim.md`, para que Claude Code en VS Code los recupere actualizando.

**Sprite de mapa de Kairon (en curso, 7 nov 2026).** Los quietos a mano de Claude Code (hasta `kairon_quieto_v5_16x16.png`) y las tandas de `create_image_pro` con el estilo de Aethrall quedan descartados. Con el método de PixelLab de arriba salió el primer personaje que sirve como estilo (`assets/kairon/pixellab/kairon_pixellab_sur_32x32.png`, 18x28 dentro del lienzo). Falta corregir ancho, contorno y guantelete sobre ese personaje, y después armar el quieto de 3 cuadros y las 15 celdas de movimiento.

| Archivo (versión por script, reemplazada) | Qué es |
|---|---|
| `mapa/kairon_mapa_quieto_16x48.png` | Quieto por script, 3 cuadros de 16x16 |
| `mapa/kairon_mapa_movimiento_32x480.png` | Movimiento por script, 15 cuadros en celdas de 32x32 |
| `mapa/paleta_aliados.agbpal` | Paleta de aliados aprobada. No se aplica sin preguntar, porque cambia a todas las unidades aliadas |

**Resto de los assets.** Escena y espejo real de 104x112 con contorno blanco de 2 px, bocas (6 de 32x16, dibujadas por script en y=24) y ojos (2 de 32x16 en y=8), mini de 32x32 sin borde blanco, con ojos fijos de líneas verticales y sin cejas, estado de 80x144 de cuerpo entero, y zoom y HERIDO de 240x160. Todos usan una sola paleta (`kairon_paleta.agbpal`) con `#A9CBA6` exacto en el índice 0. El espejo real (cambio de mano del guantelete por recoloreo) y las bocas y ojos dibujados por script quedaron mal. Se rehacen con inpainting de PixelLab sobre el retrato final. La animación de batalla queda para más adelante.

## Abierto

- Corregir el personaje de PixelLab de Kairon (16 de ancho como máximo, paleta sin casi negro, guantelete legible) y decidir si el alto de 28 entra en cuadros de 16x32 como el Ephraim original.
- Armar con ese personaje el quieto de 3 cuadros y las 15 celdas de movimiento, y pasarlo por el script de paleta de aliados.
- Aplicar el mismo método a cada clase o personaje (concepto completo, descripción, paleta propia).
- Decidir si el abrigo de Kairon toma el color del bando y si los personajes con nombre tienen quieto propio.
- Rehacer la ficha de Kairon con la dirección de arte nueva y actualizar las instrucciones del Gem Elyria Concept (hoy piden estilo anime).
- Primera prueba en el Gem con Teodora (Bastión), las cuatro hojas.
- Implementación del zoom herido. El menú de estado tiene que cambiar al zoom HERIDO cuando la vida actual baja del 25 % de la máxima. Pasarlo al chat de Implementación.
- Arte de Kairon de cintura para arriba con la cara ladeada, generado a 200x224 o 400x448.
- Arte nuevo del personaje femenino de referencia a tamaño final para la pantalla de estado.
- Rehacer con inpainting de PixelLab el espejo real de Kairon y sus 6 bocas y 2 ojos.
- Si el mini retrato se agranda o queda en 32x32.
- Si se hace el espejado real de retratos (necesita un segundo ID y un cambio en `StartFace`).
- Pantalla de estado. Reducir el render (unos 200 a 300 colores) a paletas de 16 por tile y resolver las cuatro transparencias con un solo EVA/EVB de GBA. El retrato 3 es de un tercero y solo sirve de prueba. Falta definir cómo convive el zoom de la cara con el diseño `gris_final`.
- Sprites de mapa. El verde neutral se pierde sobre pasto.
- Mode 3 de Kairon. Los cuadros del crítico ya están estandarizados. Falta escribir el Mode 3 en el script de FEBuilder y probarlo en el juego.
- Colores que quieres cambiar. Pasto y montañas del capítulo 1, azul de las unidades del jugador y azules y blancos de la pantalla de batalla. Las paletas están en `graphics/map/MapPalette*.pal`, `graphics/unit_icon/palette/` y `graphics/player_interface/*.pal`.
- Personaje nuevo usuario de magia, a partir de la chica de anteojos y capa dorada de la escena grupal (no es Nemira).
