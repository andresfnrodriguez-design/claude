# BumpMesh en el flujo de trabajo

[BumpMesh](https://bumpmesh.com) (CNC Kitchen) aplica **texturas de relieve reales** a un STL: moleteado, arenado, hexágonos, cuero y 90 más. Sirve para tres cosas que ya veníamos usando como reglas de diseño:

- **Ocultar líneas de capa** y la línea de contracción de cajas y contenedores.
- **Agarre** en mangos, perillas y superficies de apoyo.
- **Rigidez**: las pruebas de CNC Kitchen muestran que el relieve hace las paredes bastante más rígidas.

Hay dos formas de usarlo. Las dos usan el mismo motor y dan el mismo resultado.

| | Navegador ([bumpmesh.com](https://bumpmesh.com)) | Línea de comandos (`texturize.mjs`) |
|---|---|---|
| Para qué | Piezas únicas, elegir textura a ojo, pintar zonas | Lotes, presets repetibles, pipeline automático |
| Enmascarar zonas | Pintando caras, por ángulo, capas de textura | Solo por ángulo (base y caras superiores) |
| Formatos de entrada | STL, OBJ, 3MF, STEP | STL |

## Dónde va en el flujo

```
CAD / reglas de diseño (filetes, chaflanes, tolerancias)
        │
        ▼
BumpMesh  ← acá: la textura va sobre la geometría ya terminada
        │
        ▼
Bambu Studio (cortes, conectores, Color Mixing, laminado)
```

Texturiza **después** de cerrar la geometría y **antes** de laminar. Corta la pieza y agrega conectores en Bambu Studio después de texturizar.

## Qué NO texturizar

La textura cambia las medidas, así que deja lisas:

- **Superficies que encajan con otra pieza**: agujeros, ejes, snap-fits, grip fins, tapas.
- **La cara de apoyo en la cama.** La línea de comandos ya la protege por defecto (`--bottom-angle 5`).
- **Zonas donde van los dientes de aletas de soporte.**

Para excluir caras puntuales, usa el navegador y píntalas como excluidas.

## Línea de comandos

### Instalación (una vez)

Requiere Node.js 18 o más y git.

```bash
cd tools/bumpmesh
bash setup.sh        # descarga BumpMesh en una versión fija e instala three.js y fflate
```

### Uso

```bash
# con un preset
node texturize.mjs --in pieza.stl --preset agarre

# una carpeta entera, boquilla de 0,6 (escala mosaico y relieve)
node texturize.mjs --in piezas/ --out piezas_texturizadas/ --preset ocultar-capas --nozzle 0.6

# a mano: cualquier textura incluida o un PNG propio en escala de grises
node texturize.mjs --in perilla.stl --texture knurling --mapping cylindrical --tile 20 --depth 0.5

node texturize.mjs --list-presets
node texturize.mjs --list-textures
node texturize.mjs --help
```

Sin `--out`, guarda `<nombre>_textura.stl` junto al original.

### Presets (`presets.json`)

Los valores están pensados para boquilla de 0,4 mm. Con `--nozzle 0.6`, el tamaño de mosaico y el relieve se multiplican por 1,5.

| Preset | Textura | Proyección | Mosaico | Relieve | Uso |
|---|---|---|---|---|---|
| `agarre` | knurling | triplanar | 20 mm | 0,5 mm | Mangos, zonas de agarre |
| `agarre-cilindro` | knurling | cylindrical | 20 mm | 0,5 mm | Perillas y mangos redondos |
| `antideslizante` | gripSurface | triplanar | 30 mm | 0,6 mm | Apoyos, superficies de pisado |
| `ocultar-capas` | sandMatte | triplanar | 60 mm | 0,35 mm | Disimular capas y líneas de contracción |
| `marca` | hexagons | triplanar | 30 mm | 0,5 mm | Aspecto industrial o de marca |

El **mosaico** es el tamaño en mm de una repetición de la imagen. Cada imagen trae varios motivos por repetición: el moleteado tiene unos 8 rombos, así que con mosaico de 20 mm cada rombo mide ~2,5 mm. Puedes agregar presets propios editando el JSON.

### Opciones útiles

- `--top-angle 10`: deja lisa la tapa superior (útil en perillas con `agarre-cilindro`).
- `--invert`: la textura se hunde en vez de sobresalir; la pieza no crece.
- `--symmetric`: sobresale y se hunde a partes iguales; conserva el volumen.
- `--max-tris 500000`: archivos más livianos. Una pieza de 30 mm texturizada ronda los 300 000 triángulos (~15 MB).

### Advertencias que da la herramienta

- **Relieve mayor al 10% de la medida más chica de la pieza** (el mismo límite que usa BumpMesh): puede deformarla.
- **Relieve menor a 0,2 mm**: probablemente no se note impreso.
- **Bordes abiertos o malla no-manifold** en el resultado: revísalo en Bambu Studio antes de imprimir.

## En Bambu Studio

- **No combines con fuzzy skin**: la textura ya reemplaza esa función.
- El relieve sale con las paredes, así que **2–3 paredes** alcanzan; no hace falta más relleno.
- Con Color Mixing, la textura y el color son independientes: puedes usar las dos.

## Licencia

BumpMesh es software libre bajo **AGPL-3.0**. `setup.sh` lo descarga aparte y no se copia en este repositorio. `texturize.mjs` usa sus módulos, por eso está marcado con la misma licencia. Para uso personal no hay ninguna obligación. Si algún día publicas la herramienta o la ofreces como servicio, tienes que publicar también su código. Los STL que generas son tuyos.
