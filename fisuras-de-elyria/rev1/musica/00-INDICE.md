# Música y sonido — índice

Es la fase con menos material escrito. Casi todo salió de conversaciones sueltas dentro de "Historia para juego de Fire Emblem" y "FE8 decomp".

## Documentos

| Archivo | Qué es |
|---|---|
| `referencias-sonoras.md` | Temas por nación y por concepto, con instrumentación, misiones donde suena cada uno y cómo se reparten en las Partes |

## Música

**Principio.** Pocos temas que vuelven reorquestados en lugar de 40 piezas sueltas. Inspiración en Sakimoto (metales con función rítmica) y Wardruna para Kaldholt.

**Temas definidos.** Elyria, Kaldholt, Ferannor, Cassaria, Ordun y el Olvido. El tema de Érebos y las fisuras era de la versión 1 de la historia, que eliminó a Érebos. Hay que decidir si se reconvierte, por ejemplo en tema de la fisura o del puerto de Ferannor, o se descarta.

**Prompt de Suno para el tema principal** (191 caracteres).

```
16-bit GBA JRPG main theme, epic orchestral chiptune. Greek modal strings clash with industrial percussion, building to climax. Fire Emblem GBA soundfont style. Bittersweet, tragic undertone.
```

Estilo para el campo de género.

```
16-bit chiptune, orchestral, epic cinematic, JRPG soundtrack
```

**Música dinámica.** Propuesta en `../diseno/DISENO-mecanicas-v2.md`. Cambia en escenas que modifican el mapa.

## Integrar música al juego

- La música de GBA no es audio sino una partitura que la consola toca, parecida a un MIDI. Un WAV no sirve. El de prueba duraba 12:48, pesaba 135 MB y aun a la peor calidad ocuparía unos 10 MB.
- **Camino vigente, desde MIDI.** Los MIDI están en `~/fireemblem8u/musica/`. Se convierten con `mid2agb`, se copian a `sound/songs/midi`, la regla va en `songs.mk` (`-G` grupo de instrumentos, `-V` volumen, `-R` reverb, `-P` prioridad), se registran en `sound/song_table.s` y se asignan en `mapBgmIds` de `src/data/chapter_settings.json.txt`.
- Si solo hay audio de Suno, se pasa a MIDI con un transcriptor como Basic Pitch y se limpia a mano.

## Sonido

- **Sonido de voz por personaje.** En FE8 suena un bip por letra (`PlaySoundEffect(SONG_6E)` en `src/scene.c`, línea 609), no sincronizado con la boca. Se decidió que cada personaje tenga su propio sonido de voz, como en Undertale, y que sea un asset más en su ficha del gestor de arte.
- **Efectos de sonido.** Apartado separado de la música. Pisadas, impactos, interfaz y sonidos de arma de los scripts de animación (C1B, C1F, etc.).
- **Sonido del aether.** El tema del Olvido se usa como efecto corto en cada habilidad de aether.

## Abierto

- Confirmar que Claude Code integró el MIDI del capítulo 1 y ajustar instrumentos, volumen y reverb.
- Destino de la segunda canción.
- Qué hacer con el tema de Érebos.
- Si cada nación tiene variante de combate propia o solo Elyria.
- Elegir los sonidos de voz de cada personaje y cómo se asignan en el código.
