# Orientación automática de figuras

`orientar.mjs` busca la orientación de impresión de cada figura y deja **placas 3MF listas para Bambu Studio**: figuras giradas, apoyadas y repartidas en la cama. No hay que pintar soportes. Con `--laminar`, cada candidata se lamina de verdad con PrusaSlicer (el motor del que deriva Bambu Studio) y gana la de menor tiempo real.

También da los ángulos para [Support Fins](https://printfins.com) (`--rot`, el mismo `X · Y · Z` de la web) y puede hornear las aletas con `--fins`. Pero en figuras orgánicas las aletas no alcanzan: ver [Support Fins en figuras](#support-fins-en-figuras).

## Instalación (una vez)

Requiere Node.js 20.10 o más. No usa paquetes de npm.

```bash
# para --laminar (recomendado): PrusaSlicer por línea de comandos
sudo apt install prusa-slicer          # Ubuntu/Debian; en Windows/Mac, instálalo y deja prusa-slicer en el PATH

# solo para --fins
cd tools/orientacion && bash setup.sh  # descarga Support Fins en una versión fija
```

## Uso

```bash
# el flujo completo: placas de Bambu/3MF con varias figuras → placas orientadas
node orientar.mjs --in figuras/ --laminar --placas

# una figura suelta, solo el análisis
node orientar.mjs --in roy.stl

# los modelos de Meshy suelen venir en otra escala: llévalos a 60 mm de alto
node orientar.mjs --in figuras/ --alto 60 --laminar --placas
```

Lee STL, OBJ y 3MF. En un 3MF, **cada objeto es una figura**. Los resultados van a `<carpeta>/orientado/` (o a `--out`):

- `<placa>_orientado.3mf`: las figuras de esa placa ya orientadas y ubicadas. Si no entran en una cama, `_orientado_1.3mf`, `_orientado_2.3mf`…
- `orientaciones.csv`: una fila por figura, con la rotación, las capas, el tiempo y el filamento.

La malla se escribe con los mismos vértices y triángulos que el original: una figura cerrada sigue cerrada.

## En Bambu Studio

1. Abre el `_orientado.3mf`. Si pregunta, cárgalo como geometría.
2. Perfil de proceso de la boquilla de 0,2 con **capa de 0,06 mm**.
3. **Soporte → Habilitar soporte**, tipo **tree(auto)**, estilo **Tree Organic** (o *Tree Hybrid*). Ángulo de umbral 30°.
4. Lamina. No hace falta pintar: el soporte automático cubre todo lo que cuelga.

Las figuras acostadas tocan poco la cama: deja el **brim** en automático.

## Cómo elige

1. **Barrido** de ~1500 direcciones de apoyo: altura y voladizos de cada una.
2. **Evaluación detallada** de las mejores (~100): rayos verticales sobre una grilla miden el soporte que nace en la cama, el que apoya sobre la propia figura, las puntas colgantes, el apoyo y el área de cada capa. Con eso hace un tiempo estimado.
3. **Laminado real** (`--laminar`): lamina la orientación original y las mejores según tres criterios (menos capas, menos tiempo estimado, menos soporte), unas 6–7 por figura, y se queda con la de **menor tiempo real**.

Sin `--laminar`, ordena por `--criterio`:

- **`capas`** (por defecto): la menor cantidad de capas. Entre las que están a no más de `--tolerancia` (10%) del mínimo, gana la de menos soporte.
- **`tiempo`**: el menor tiempo estimado.
- **`soportes`**: el menor soporte. A igualdad, menos capas.

### Menos capas no siempre es más rápido

En una figura chica, muchas capas quedan frenadas por el **tiempo mínimo de capa** (el plástico tiene que enfriarse). Por eso acostarla ahorra mucho tiempo. Pero entre dos orientaciones acostadas, la de menos capas puede ser más lenta si necesita más soporte. Con Lucina, la orientación con menos capas (462) tardó 2 h 52 min y una con 562 capas tardó 2 h 21 min. Por eso el criterio final es el tiempo real de laminado y no la cantidad de capas.

## Columnas del análisis

| Columna | Qué es |
|---|---|
| `capas` | Altura ÷ altura de capa. |
| `c.masa` | Altura del centro de masa. Bajo = más estable. Las capas las define la altura total, no el centro de masa. |
| `sop.cama` | Volumen envolvente bajo voladizos que apoya en la cama (el filamento real es una fracción). |
| `sop.fig` | Volumen envolvente de soporte que **apoya sobre la propia figura**. Cuenta doble porque deja marcas. |
| `islas` | Mínimos locales que cuelgan en el aire. En mallas de IA con mucho detalle el número es alto y ruidoso: sirve para comparar. |
| `apoyo` | Área en contacto con la cama. |
| `estable` | Si el centro de masa cae dentro del apoyo. Si dice "no", usa brim. |
| `tiempo est.` | Estimación propia (`maquina.json`), solo para comparar. |
| tiempo real | Con `--laminar`: el de PrusaSlicer con `perfiles/p1s_02_006.ini`. |

## El perfil de laminado

`perfiles/p1s_02_006.ini` aproxima el P1S con boquilla de 0,2: capa 0,06, PLA, 2 paredes, 15% de relleno, caudal máximo 2 mm³/s, aceleraciones del P1S, tiempo mínimo de capa 4 s y soporte orgánico automático a 30°. `--capa` y `--boquilla` lo ajustan solos. El tiempo de Bambu Studio no va a ser idéntico, pero la comparación entre orientaciones sí vale. Puedes usar otro perfil con `--perfil`.

## Lo que la herramienta no decide por ti

- **Dónde quedan las líneas de capa.** Acostada, la cara y el pecho se imprimen de costado y el lado de la cama queda con marcas. Para pintar está bien. Para vitrina conviene parada.
- **La resistencia.** Lanzas y espadas finas aguantan más si quedan paralelas a la cama.
- **Cabeza abajo.** A veces lo más rápido es dar vuelta la figura (la cabeza contra la cama). Si no lo quieres, usa `--sin-invertir`: descarta las poses giradas más de 120° respecto de como viene.

## Support Fins en figuras

Support Fins pone aletas que se quiebran a mano, pensadas para piezas con aristas. Se probó con Lucina en 10 orientaciones distintas: en todas quedaron entre 4 y 14 zonas de voladizo sin aleta posible, más miles de caras en zonas demasiado chicas para una aleta. Para que no haya que pintar nada, el flujo automático usa el soporte de árbol del laminador y no las aletas.

`--fins` sigue disponible para piezas mecánicas o con aristas:

```bash
node orientar.mjs --in soporte.stl --fins --fins-args "--material petg"
```

Con capa de 0,06 los dientes se generan para 0,08 mm, el mínimo que acepta Support Fins, y la herramienta lo avisa.

## Licencia

Support Fins es de [gittrahan/support-fins](https://github.com/gittrahan/support-fins) (MIT). `setup.sh` lo descarga aparte en `vendor/`. PrusaSlicer (AGPL-3.0) se usa como programa externo y no se incluye.
