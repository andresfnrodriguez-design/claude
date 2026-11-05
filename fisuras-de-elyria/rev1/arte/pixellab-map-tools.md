# PixelLab — Create Map vs. Create Tileset

*Dos herramientas con inputs completamente distintos. Resumen de la documentación oficial de PixelLab.*

## Create Map (pixflux) — pintar y expandir una escena

**No es "un prompt, un mapa completo".** Es un proceso iterativo de varios pasos, basado en inpainting (relleno guiado por selección).

**Los inputs que maneja en cada paso:**
- **Imagen inicial (init image):** el punto de partida — al principio puede estar vacío, después es lo que ya generaste en pasos anteriores.
- **Selección:** un área del lienzo (por ejemplo, 4x4 tiles = 64x64px, ya que el modelo está entrenado sobre tiles de 16x16) que le dice al modelo qué región mirar.
- **Capa de inpaint:** pintás de negro las zonas DENTRO de la selección que querés que el modelo genere de nuevo. Lo que dejás sin pintar de negro se mantiene como referencia.
- **Descripción (texto):** qué querés que aparezca — importante: describe lo que va en el **centro** de la zona seleccionada, no la zona completa.
- **Init image strength:** un dial que controla cuánto peso tiene la imagen ya existente contra la generación nueva.

**El flujo real, paso a paso:**
1. Seleccionás una zona (ej. 4x4 tiles), la pintás toda de negro en la capa de inpaint (porque es la primera generación, no hay nada que preservar todavía), escribís la descripción, generás.
2. Para expandir: seleccionás una zona nueva que se **superponga parcialmente** con lo ya generado, hacés un boceto tosco adentro, y pintás de negro en el inpaint **solo la parte nueva** (nunca toda la selección — si tapás todo de negro, el modelo pierde la referencia de estilo y no va a conectar bien con lo anterior).
3. Repetís ese paso hasta cubrir todo el lienzo.
4. Al final, hacés una pasada más de inpainting normal para corregir detalles sueltos.

**Para qué sirve realmente:** escenas ilustradas puntuales (el ejemplo oficial es una cueva con escalera y cofre) — algo que se ve una sola vez, no algo pensado para repetirse/tilearse infinitamente.

---

## Create Tileset — tiles conectables desde dos descripciones de terreno

Un paradigma mucho más directo, y — para lo que necesitamos en FE — probablemente la herramienta correcta.

**Los inputs:**
- **Terreno inferior y terreno superior** (para modo Top-Down): dos descripciones de texto, por ejemplo "nieve" y "roca". El modelo genera automáticamente una transición fluida entre ambos.
- **Descripción de transición** (opcional): cómo se ve específicamente la franja límite entre los dos terrenos.
- **Tamaño de tile:** 16x16 o 32x32 en el plan Standard (16x16 es exactamente lo que usa FE GBA). El plan Pro agrega 64x64 experimental.
- **Tamaño de transición:** 0 = los terrenos se tocan directo, sin gradiente; más alto = banda de transición más ancha, a veces con diferencia de altura visible.
- **Forma del borde:** cuadrado (esquinas en escalón) o redondo (arcos reales), con dos diales adicionales — redondez y "raggedness" (qué tan irregular/orgánico se ve el borde).
- **Grosor y ubicación de pared lateral** (Top-Down): qué tan grueso se ve el borde en la parte superior y en el frente, y si sobresale del terreno o queda tallado hacia adentro.
- **Mejorar descripciones con IA** (activado por defecto): reescribe tu descripción de texto ajustando nivel de detalle y sombreado, y elige colores base automáticamente. Tu texto original queda guardado en los metadatos del tileset igual.

**Para plataformas (Sidescroller)** es un modo distinto: describís el material interior de la plataforma y qué aparece en la superficie de arriba (por ejemplo, "tierra" con "pasto" encima).

**Exporta a:** Wang tileset, dual-grid de 15 tiles, y grilla 3x3 — formatos pensados justo para que los bordes conecten sin costuras, algo que Create Map no resuelve automáticamente.

**Costo:** una sola llamada genera la hoja completa de una vez (16 o 25 tiles), así que cuesta más que una imagen suelta — Standard Top-Down: 1 a 4 generaciones (usualmente 3-4). Requiere plan pago Tier 1 o superior.

---

## Cuál conviene para Fisuras de Elyria

**Create Tileset** encaja mejor con lo que necesitamos: tiles de 16x16 que tienen que conectar sin costuras entre distintos tipos de terreno (nieve/roca en Kaldholt, tierra/piedra en el campamento elirio, etc.) — exactamente el caso de uso para el que está diseñada. Create Map tiene más sentido si en algún momento necesitás una escena única e ilustrada que no se vaya a repetir como tileset (por ejemplo, un fondo de cutscene), no para el terreno base de las 40 misiones.

Dicho esto, Create Tileset trabaja con **dos terrenos por generación**. Si un mapa necesita más de dos tipos de superficie (nieve + roca + vegetación muerta, como en M1), probablemente haga falta generar varios pares de transiciones por separado y combinarlos vos mismo en Tiled, en vez de esperar que una sola llamada resuelva las tres a la vez.
