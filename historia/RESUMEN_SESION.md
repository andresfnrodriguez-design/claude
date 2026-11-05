# Resumen de sesión — Fisuras de Elyria

Sesión del 2026-11-03 al 2026-11-05. Rama: `claude/inspiring-cray-78kf19` del repositorio `andresfnrodriguez-design/claude`.

## Qué se hizo

1. Se buscó en Google Drive el material del juego y se leyó: "FE" (biblia original), `fisuras-de-elyria-novela-completa.pdf` (boceto de 40 misiones + apéndice + notas de mapas) y `fisuras-clases-armas.pdf`.
2. Crítica dura de la historia y revisión del boceto misión por misión, con problemas marcados por color.
3. Se tomaron decisiones de historia y diseño (abajo) y se guardaron en documentos del repositorio.
4. Se escribió la versión 2 de la historia (escaleta de 28 misiones con "la lista" como secreto).
5. Se leyó el storyboard de Path of Radiance hecho en otro chat y se armó el de Elyria en el mismo formato, con cuadros dibujados.

## Archivos creados o modificados

| Archivo | Para qué |
|---|---|
| `historia/BIBLIA.md` | Historia: principios de escritura, mundo, personajes, estructura, clímax, decisiones con fecha. |
| `historia/DISENO.md` | Mecánicas y principios de programación (incluye reglas de RAM para GBA). |
| `historia/VERSION-2-LISTA.md` | Escaleta completa de la versión 2. |
| `historia/README.md` | Índice de documentos y enlaces a las páginas publicadas. |
| `historia/CLAUDE.md` | Instrucciones para Claude Code al usar estos documentos. |
| `historia/storyboard-elyria.html` | Storyboard de la versión 2 con viñetas ilustradas. |
| `historia/RESUMEN_SESION.md` | Este archivo. |
| `historia/CHAT_SESION.md` | Registro cronológico condensado de la conversación. |
| Scratchpad: `fisuras-recap.html` | Revisión crítica del boceto con colores (publicada). |
| Scratchpad: `version-2.html` | Versión 2 para leer (publicada). |
| Scratchpad: `novela.txt` | Texto extraído del PDF de la novela, para leerlo. |

Páginas publicadas (privadas, compartir desde "Share"):
- Revisión del boceto: https://claude.ai/artifact/GbwYWvgJSkFC65ZdvcyZvU
- Versión 2: https://claude.ai/artifact/HH17YwBJk8Cp7wX68nKmpV
- Storyboard de Elyria: https://claude.ai/artifact/RxKxabGfduDjCdRkGnXjY7
- Storyboard de Path of Radiance (otro chat): https://claude.ai/artifact/4EJXFz4m5AKZx28tB4qCwy

## Decisiones de historia

- **Principios:** nunca subestimar al jugador; la historia debe aguantar después del giro; no sobreusar el tema; no todo tiene que encajar; cada personaje o grupo tiene una postura ante los conflictos del mundo, de forma orgánica.
- **Orestion tiene razón en parte.** Su secreto (propuesta avanzada): firmó la lista de evacuación hace quince años, con las tablas de viabilidad de Ferannor. Kairon estaba en ella.
- **Sin amenaza sobrenatural.** Se eliminan Érebos, Tálos y la sombra imposible.
- **El Olvido:** usar aether cuesta recuerdos. Es lienzo, no pintura: rasgo normal del mundo, nadie lo explica.
- **Lema:** "Volveremos por la orilla."
- **Estructura:** 28 misiones + ~8 capítulos paralelos, 4 Partes, la IV corta. Parte I autoconclusiva (el caso de Feron).
- **Revelación dividida:** a mitad del juego se descubre la lista; después, quién la firmó.
- **Clímax (propuesta avanzada):** mapa del puerto de Ferannor y mapa de Orestion. El reto es llegar al registro; Kairon cambia la lista y los guardias dejan de obedecer. Barras en crescendo; la última deja a Orestion débil y patético. Solo el aether de Kairon lo daña ahí; el menú muestra **Matar** o **Hablar**.
- **Último capítulo:** rescate en los escombros, sin azar ni muerte guionada. Epílogo según cuántos se rescaten.
- **Final de Kairon:** no revela la lista; deja de vivir según el lema. Escena espejo: repite la frase de Orestion sin que nadie lo señale.
- **Halvard:** rival en la Parte II, jugable en la III, traiciona en la misión 23 (la ejecuta el jugador), vuelve en la IV.
- **Nemira:** nunca "mujer en el refrigerador". Si muere por la muerte permanente, cambian algunos diálogos de Kairon, sin que esa versión sea más rica.
- **Orestion jugable al principio** (estilo Seth); lo reemplaza un personaje de su clase que hereda inventario y estadísticas.

## Decisiones de diseño

- Muerte permanente, con tres categorías de personajes indispensables y escenas dinámicas (líneas reasignables o eliminables).
- Árbol de clases cerrado estilo Sacred Stones; tres promociones solo para reclutas. Descartados Three Houses y Fortune's Weave.
- Identidad de unidad: habilidades nacidas del carácter, coherencia entre clase y crecimientos, estética única.
- Jefes con varias barras (normal 1/2/3, difícil 2/3/4).
- Veneno: 1/3/5 de daño por 1/2/3 stacks, tope 3, puede matar, solo se cura con consumibles o magia.
- Música dinámica en escenas que cambian el mapa.
- Dificultad dinámica oculta, solo en difícil, solo sube.
- Ayuda para remontar en cada capítulo.
- Habilidad por rango S de arma (detalles más adelante, con Filo/Asta/Peso).
- **Motor:** decompilación de Fire Emblem 8 en C (`make fireemblem8.gba`).
- **Programación:** la lógica nueva no toca el hardware; datos independientes de la plataforma; diseñar para los límites de la GBA; datos fijos en ROM con `const`; sin `malloc`; estructuras compactas; medir la RAM en cada compilación.

## Comandos que funcionaron

Traer la carpeta `historia/` al proyecto local:

```bash
git fetch https://github.com/andresfnrodriguez-design/claude.git claude/inspiring-cray-78kf19
```

```bash
git checkout FETCH_HEAD -- historia
```

Tarea de VS Code agregada a `.vscode/tasks.json`: **Actualizar historia** (los mismos dos comandos). Sobrescribe la copia local de `historia/`.

Mensaje para Claude Code: agregar `@historia/CLAUDE.md`, `@historia/BIBLIA.md` y `@historia/DISENO.md` al `CLAUDE.md` de la raíz del proyecto.

## Sin resolver

- Confirmar si "la lista" convence como secreto de Orestion.
- Decisión de Kairon sobre el asesino de Feron (capítulo 7).
- Cómo vuelve Halvard después de la misión 23.
- Rostro y nombre de la directora de Ferannor.
- Qué se juega en la misión 25 (escena espejo).
- Nombres que se confunden: Vask/Voss, Kairon/Kallion, los dos Ilarion.
- Costo mecánico exacto del Olvido (tabla propuesta sin confirmar).
- Si Orestion es mago (como en el documento de clases) o guerrero.
- Habilidades de rango S con Filo/Asta/Peso.
- Rango y tope de la dificultad dinámica.
- Seis capítulos del storyboard de Path of Radiance escritos de memoria, sin verificar (9, 12, 14, 16, 17 y 27).
- Los documentos viven en este repositorio y no en el del proyecto en C: hay que copiarlos con la tarea cada vez.

## Críticas recientes (sin resolver)

- El storyboard no dice qué hace el jugador: falta una línea "En el mapa" por capítulo.
- El mundo no justifica el conflicto. Propuesta: el consejo quemó con aether el recuerdo de la orilla.
- El ejército no tiene motivo. Propuesta: una expedición colectiva al sur.

## Próximos pasos

1. Leer la versión 2 y el storyboard; decidir si se queda la lista.
2. Verificar los capítulos dudosos de Path of Radiance y compartir los dos storyboards con los dos lectores.
3. Resolver los pendientes de la Parte I y la misión 25.
4. Considerar abrir el repositorio del proyecto en C en la próxima sesión, para tener una sola copia de los documentos.

## Archivos de entrada

No se subieron archivos a esta sesión. El material leído vino de Google Drive (sigue ahí, sin cambios) y de texto pegado en el chat (transcripciones de dos videos y respuestas de otro chat), que no son archivos.

## Archivos perdidos

- `fisuras-historia-2026-11-04.zip`: zip anterior de los documentos, borrado del repositorio después de enviarlo. Este zip lo reemplaza.
