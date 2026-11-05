# Resumen de sesión · Fisuras de Elyria · 4 y 5 de noviembre de 2026

## Qué se hizo

1. Método de producción de arte por personaje y por clase, verificado contra el código de la decompilación fireemblem8u.
2. Especificación del gestor de arte en Electron para que lo construya Claude Code.
3. Instalación de Claude Code en Ubuntu (WSL).
4. Storyboard de Path of Radiance para contrastar con la historia de Elyria.
5. Plantillas y prompts de Nano Banana para probar la generación de arte de 3 clases.
6. Nota de memoria nueva para el diseño de sonido.

## Archivos creados

| Archivo | Para qué |
|---|---|
| `ESPEC_GESTOR_ASSETS.md` | Especificación completa del gestor de arte en Electron (estructura de la biblioteca, fichas de personaje y clase, checklist de assets, versiones, validador, vista previa, conversiones, exportación, .exe). Claude Code la lee y construye por etapas |
| `plantillas/hoja1_concepto.png` | Plantilla de concepto. Giro completo con guías de cabeza, pies y eje, paleta de 16, expresiones, pose de ataque y detalles |
| `plantillas/hoja2_retratos.png` | Plantilla de retratos a escala exacta. Escena y espejo real 400x448 (x4), estado 240x432 (x3), mini 128x128, bocas y ojos 128x64, poses 200x224 (x2) |
| `plantillas/hoja3_sprites.png` | Plantilla de sprites. Mapa quieto 3 de 16x16 (x6), mapa en movimiento 15 celdas de 32x32 (x3), batalla 8 cuadros de 248x160 (x1) con línea de pies |
| `plantillas/plantillas.py` | Script que genera las tres plantillas con Pillow |
| `plantillas/prompts_nano_banana.md` | Prompts de las tres hojas y bloques de 3 personajes de prueba (Teodora, Bastión · Lysandros, Deslizador · Ione, Tejedor) |
| `RESUMEN_SESION.md` | Este archivo |

Fuera del zip.
- **Storyboard de Path of Radiance** (documento de Claude). https://claude.ai/artifact/4EJXFz4m5AKZx28tB4qCwy
- **Memoria** `/areas/sonido-fisuras-de-elyria.md`, sonido de voz por personaje separado de la música.

## Decisiones de diseño

- **Boca y ojos.** El motor los anima solo. La boca cambia al azar entre fotogramas cada 1 a 8 cuadros mientras se escribe el texto (`src/face.c`, `src/cgtext.c`). Se dibujan 6 bocas de 32x16 (normal y sonriendo, cerrada, media y abierta) y 2 ojos (entrecerrados y cerrados).
- **Sonido al hablar.** Suena `SONG_6E` por cada letra (`src/scene.c`, línea 609). No está sincronizado con la boca. Se decidió dar a cada personaje su propio sonido de voz, que es un asset más en su ficha.
- **Espejado real.** El motor voltea por hardware (`OAM1_HFLIP`) y cambiaría de mano los objetos asimétricos. Un espejo redibujado necesita un segundo ID de retrato y un cambio en `StartFace`.
- **Sprites de mapa.** La figura es de 16x16. Quieto 3 cuadros. En movimiento 15 cuadros en celdas de 32x32 (4 izquierda, 4 abajo, 4 arriba, 3 seleccionado). La derecha la voltea el motor.
- **Por clase y por personaje.** Sprites de mapa y animaciones de batalla son por clase. Hay personajes con clase exclusiva. Los retratos, la paleta, la paleta de batalla propia y la voz son por personaje.
- **Gestor de arte.** Electron, construido por Claude Code en `~/gestor-elyria`, biblioteca en `~/elyria-arte` con git, medidas y reglas en `estandar.json` editable, .exe portátil generado desde Windows.
- **Historia de contraste.** Path of Radiance, por cercanía temática (discriminación beorc y laguz). Formato de viñetas más comentario tipo novela. Para Elyria se compararán solo las escenas más importantes.
- **Nano Banana.** Relación 3:2, máxima calidad. Hoja 1 con la plantilla sola. Hojas 2 y 3 con la plantilla y la hoja 1 como referencia, porque Nano Banana no mantiene memoria fiable entre imágenes.

## Comandos que funcionaron

Copiar la especificación desde Descargas (subcarpeta Roms Fe).
```bash
mkdir -p ~/gestor-elyria ~/elyria-arte
cp /mnt/c/Users/andre/Downloads/*/ESPEC_GESTOR_ASSETS.md ~/gestor-elyria/
```

Instalar Claude Code y agregarlo al PATH.
```bash
curl -fsSL https://claude.ai/install.sh | bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
cd ~/gestor-elyria
claude
```

Mensaje para Claude Code.
```
Lee ESPEC_GESTOR_ASSETS.md y construye la aplicación siguiendo sus etapas. Empieza por la etapa 1 y no pases a la siguiente hasta que yo la pruebe y te confirme. No sé programar, así que explícame en español qué probar y cómo.
```

Node para Windows, necesario en la etapa 7 (PowerShell).
```powershell
winget install OpenJS.NodeJS.LTS
```

## Problemas sin resolver

- No está confirmado que `claude` arranque después de agregar `~/.local/bin` al PATH, ni que la etapa 1 del gestor haya empezado.
- Falta definir dónde van las bocas y los ojos dentro del retrato de 100x112 (coordenadas por personaje).
- Falta decidir si el mini retrato se agranda como el de escena o queda en 32x32.
- Los capítulos 9, 12, 14, 16, 17 y 27 del storyboard de Path of Radiance se completaron de memoria y hay que revisarlos.
- No se comprobó cuánto respeta Nano Banana las plantillas, en especial bocas, ojos y sprites chicos.

## Próximos pasos

1. Abrir Claude Code en `~/gestor-elyria`, pegar el mensaje y probar la etapa 1 con `npm start`.
2. Generar las 3 hojas de Teodora en Nano Banana y revisar los resultados antes de probar con Lysandros e Ione.
3. Terminar de arreglar la biblia y subirla para armar el storyboard de Elyria con el mismo formato.
4. Revisar los capítulos marcados del storyboard de Path of Radiance.
5. Sumar al gestor el sonido de voz por personaje cuando llegue la etapa de assets.

## Archivos perdidos

Ninguno. Todos los archivos de la sesión siguen disponibles.
