# Resumen de sesión — Fisuras de Elyria

ROM hack de FE8 hecho por una sola persona, sobre la decompilación fireemblem8u (WSL, VS Code). Esta sesión abarcó narrativa, diseño de mapas, arte, animación, sonido y el nuevo estándar de retratos.

## Decisiones de diseño

### Narrativa y estructura
- 40 misiones en cuatro partes de 10 (M1-10, M11-20, M21-30, M31-40). M20 es el punto medio y M1 es el cold open de la traición de Halvard en M30.
- Escalera de revelaciones con la numeración nueva. Orestion aparece en M3, Nemira desaparece en M10, Vask traiciona en M14 por coacción, la muerte de Nemira se confirma en M15 y Sael se suma jugable en M16. En M20 está la revelación doble y en M30 traiciona Halvard. Selene es la tercera traidora, por fanatismo, en la ventana M27-30. Érebos se contiene en M39, no se derrota.
- Voss es mujer (ingeniera desertora de Ferannor, se suma en M18).
- Novela en formato casi todo diálogo, con el triple de diálogo que el primer boceto, más un apéndice de documentos del mundo.
- Todas las misiones tienen combate real.

### Clases
- La clase de Kairon era Guantelete → Artífice, única. Como "Guantelete" se lee como objeto, se propusieron reemplazos. Los preferidos son Artífice → Polímetis, Trasteador → Polímetis e Ingenioso → Artífice. **Falta elegir.** "Manitas" (nombre del Tinker en Warcraft III en español) queda descartado como clase.

### Mapas
- Documento de algoritmo con 9 pasos. El camino crítico se dibuja primero, nunca hay emboscadas sin aviso, los refuerzos se anuncian con un turno de anticipación y el esfuerzo fuerte se reserva para M20, M30, M35 y M39.

### Sprites de batalla
- Lienzo de 248x160, fondo `#A9CBA6`, contorno único `#282828`, máximo 16 colores, personaje centrado en x=140 con los pies en y=102, espejado horizontal.
- El script de FEBuilder va en un solo .txt con los 12 modos. El frame 01 es la posición de pie.

### Retratos (estándar nuevo)
- **Escena.** El arte mide 100x112, que son los 96x80 de FE8 más 2 columnas por lado y un 40% más de alto. En el juego va sobre una hoja de 104x112. El personaje sube 32 px, cada retrato va 2 px más hacia el centro que en vanilla, y el globo de texto queda a 4 px del borde superior de la pantalla, con 6 filas menos de margen interno.
- **Pantalla de estado.** El retrato es de 80x144 y va en un marco de 88x152 en x=8, y=4, con márgenes verdes iguales arriba y abajo (4 px) y 8 px a la izquierda. Ahí sí se permiten cortes a los costados, y la escala se iguala por el tamaño de cabeza.
- **Reglas de dibujo.** 16 colores, verde `#A9CBA6` en el índice 0 (transparente), 3 px de margen arriba, la cabeza nunca se corta, la silueta va completa sin cortes laterales en escena, línea negra de 1 px en el borde, contorno blanco puro de 1 px por fuera y encuadre con la proporción de Eirika.
- Si el arte original corta la silueta, se completa primero en negro o con los colores vecinos, se cierra el contorno y recién ahí se escala.
- El arte se genera a 200x224 o 400x448 para reducirlo en un múltiplo exacto y no ensuciar los píxeles.
- La ficha oficial de Kairon es la del abrigo largo crema con lazo granate y guante de bronce (`47afd033-image.png`). La de "Wanderer Investigator" queda descartada.

### Barras de vida en el mapa
- 14x3 px con borde `#3A3935`, relleno de 12 px, vacío `#525491` y color según la vida restante. Aparecen solo con la vida incompleta y se ocultan en movimiento, combate, menús y diálogos.

## Archivos creados o modificados

| Archivo | Para qué |
|---|---|
| `biblia-narrativa.md` | Biblia de trama. Se corrigió la numeración (Parte I de 10 misiones, Sael en M16, Voss en femenino, M40 en la escalera) |
| `desglose-misiones.md` | Las 40 misiones con foco, facción y beat |
| `elenco-asignado.md` | Personajes, clases y misión de ingreso. Bosses corregidos (Kessler y Deacon en M5, Brandt desde M17) |
| `clases-completas.md` | Referencia unificada de clases, armas, skills y personajes. Subido a GitHub |
| `personajes-habilidades.md` | Habilidades de recuerdo y stats. Nemira en M10/M15 e Ines en M13 |
| `lore-clases.md` | Lore de cada clase |
| `biblia-visual.md` | Paletas, retratos por personaje y estándares de sprites y retratos, incluida la regla nueva de retratos |
| `algoritmo-diseno-mapas.md` | Método de diseño de mapas en 9 pasos |
| `notas-ambientacion-mapas.md` | Ambientación por misión |
| `mejores-mapas-fe-y-romhacks-exitosos.md`, `terreno-fe7-y-condiciones-victoria.md` | Investigación de mapas, terrenos y objetivos |
| `guia-tilesets-resumen.md`, `pixellab-map-tools.md`, `guia-scripting-resumen.md` | Guías de tilesets, PixelLab y scripting de animaciones |
| `referencias-sonoras.md` | Referencias de música por región y tema |
| `novela-parte-1.md` a `novela-parte-4.md`, `novela-apendice.md` | Novela en diálogo y documentos del mundo. Se corrigieron las líneas de Voss antes de M18 (pasaron a Demetria) y su género |
| `fisuras-de-elyria-novela-completa.pdf` | Novela completa compilada (no incluye las últimas correcciones) |
| `fisuras-de-elyria-boceto-novela.md`, `fisuras-de-elyria-boceto.docx`, `fisuras-de-elyria-boceto.pdf` | Bocetos en prosa anteriores |
| `estandarizar_sprites.py` | Lleva frames a 248x160, fondo verde, contorno `#282828` y 16 colores |
| `kairon_script_completo.txt`, `kairon_ataque_basico_script.txt`, `kairon_critico_script.txt`, `referencia_imagenes_script.md` | Script de animación de Kairon para FEBuilder y tabla de frames |
| `kairon_melee_frames/`, `kairon_melee_frames_248x160/`, `kairon_crit_frames/` | Frames del ataque y del crítico |
| `parte1-layouts-desde-cero.html` | Layouts vigentes de la Parte I. Las otras versiones .html están reemplazadas |
| `portrait_referencia_100x112.png`, `portrait_kairon_100x112.png` | **Retratos de escena finales para importar** |
| `estado_referencia_80x144.png`, `estado_kairon_80x144.png` | **Retratos de pantalla de estado finales para importar** |
| `mock_soporte_kairon.png`, `mock_soporte_ella.png`, `mock_estado_kairon.png`, `mock_estado_ella.png`, `mocks_4.png` | Los 4 mockups a 240x160 y la hoja con los cuatro juntos |
| Resto de `portrait_*`, `estado_*`, `*_x5.png`, `*_completado.png` | Versiones intermedias y ampliaciones para ver |
| `salida/scratch/` | Scripts de conversión de retratos (`completar.py`, `paleta_material.py`, `portrait2.py`, `hacer_portrait.py`) y pruebas |

## Comandos que funcionaron

Copiar los retratos al proyecto.
```bash
cd "/mnt/c/Users/andre/Downloads/Roms Fe" && cp portrait_referencia_100x112.png portrait_kairon_100x112.png estado_referencia_80x144.png estado_kairon_80x144.png ~/fireemblem8u/ && ls -l ~/fireemblem8u/*_100x112.png ~/fireemblem8u/*_80x144.png
```
Si los archivos quedaron en Descargas, la primera parte es `cd /mnt/c/Users/andre/Downloads`.

Encontrar archivos descargados con otro nombre.
```bash
find /mnt/c/Users/andre -name "*_100x112*" -o -name "*_80x144*" 2>/dev/null
```

Estandarizar frames de batalla.
```bash
python estandarizar_sprites.py carpeta_entrada/ carpeta_salida/
```

En GitHub, `clases-completas.md` se subió a `andresfnrodriguez-design/claude`, rama `claude/fisuras-clases`, con la pull request #1.

## Problemas sin resolver
- Elegir el nombre de la clase de Kairon y actualizarlo en `clases-completas.md`, la biblia, `lore-clases.md` y `personajes-habilidades.md`.
- La pull request #1 está esperando el merge. Falta decidir si Fisuras de Elyria tiene un repo propio.
- El retrato de escena de Kairon sale del cuerpo completo, con la cara de frente. Para la cara ladeada hace falta arte de cintura para arriba en una sola pose.
- El retrato de escena del personaje femenino tiene la cara chica y algo sucia por la reducción. Mejora con arte nuevo hecho al tamaño final.
- La captura del personaje femenino termina en las rodillas, así que no hay pies para la pantalla de estado.
- En los retratos, ojos, boca y cejas necesitan retoque a mano a esta escala.
- Implementar en la decompilación el estándar de retratos (escena, globo y pantalla de estado) y las barras de vida. Los prompts para Claude Code están hechos, pero todavía no se ejecutaron.
- Confirmar si 4 caras de 104x112 entran en la memoria de video a la vez. Si no, el límite pasa a 3.
- Falta el GIF del crítico de Kairon para completar el Mode 3 del script.
- No se pudo abrir fireemblemwod.com ni el short de YouTube sobre pitfalls de diseño. Falta la transcripción o capturas.
- `fisuras-de-elyria-novela-completa.pdf` no tiene las últimas correcciones de la novela.
- Pendientes de canon. Rafael se suma en M14, que es el mapa de Vask solo. Vantor es de Ferannor pero está en un mapa de Los Hijos del Hielo (M34). Los títulos "El agente" (M5) y "El desertor" (M18) siguen en masculino genérico.

## Próximos pasos
1. Elegir el nombre de la clase de Kairon.
2. Hacer el merge de la pull request #1.
3. Copiar los 4 retratos a `~/fireemblem8u` y correr en Claude Code el prompt de retratos, y después el de barras de vida.
4. Generar con Nano Banana el arte de Kairon y del personaje femenino al tamaño final (200x224 o 400x448), con la pose angosta.
5. Pasar el GIF del crítico de Kairon para cerrar el script de animación.

## Archivos perdidos
Ninguno. Todo lo que se creó en la sesión sigue en la carpeta de salida. No se generaron archivos MIDI. La transcripción a MIDI se recomendó hacerla con Basic Pitch, que no se pudo instalar acá.
