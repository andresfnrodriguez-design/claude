# Prompts de prueba para Nano Banana · Fisuras de Elyria

## Cómo usarlos

Cada personaje lleva tres generaciones, una por hoja.

1. **Hoja 1.** Sube `hoja1_concepto.png` como imagen de referencia y pega el prompt de la hoja 1 con el bloque del personaje al final.
2. **Hoja 2.** Sube `hoja2_retratos.png` y también el resultado de la hoja 1 de ese personaje, para que mantenga la cara, la ropa y los colores. Pega el prompt de la hoja 2 con el mismo bloque.
3. **Hoja 3.** Igual que la hoja 2, pero con `hoja3_sprites.png`.

Los prompts van en inglés porque el generador los respeta mejor. Donde dice `[PERSONAJE]` pegas el bloque del personaje completo.

## Prompt hoja 1 · Concepto

```
Fill this character sheet template exactly as laid out. Keep every box, border and label where it is, and draw only inside the boxes. Box backgrounds stay flat #A9CBA6 green. Respect the dashed guides: red dashed lines mark the top of the head and the feet (or the shoulder cut in the expressions), the blue dashed line is the body's center axis, and in the attack box the whole body and weapon stay inside the dashed frame. Remove the dashed guides in the final image.

Style: anime/manga character design for a Fire Emblem GBA-era tactical RPG, aetherpunk with Greek inspiration. Clean lineart, cel shading in 2 to 3 tones, no gradients on the background. High object density: straps, buckles, tools, gears, small vials and pouches layered on the outfit.

- TURNAROUND row: the same character full body in the four views (front, 3/4 right, 3/4 left, back), same scale, feet on the red line, neutral standing pose. Asymmetric details (glove, shoulder piece, weapon) stay on the same body side in every view.
- PALETTE: fill the 16 squares with the character's flat colors. Square 0 stays #A9CBA6, square 1 is the dark outline color, square 2 is pure white, squares 3 to 15 are the skin, hair, clothing and metal colors from darkest to lightest per material.
- EXPRESSIONS: head and shoulders, same angle in all four (neutral, smiling, talking with mouth open, eyes closed).
- ATTACK POSE: full body attacking with the class weapon, dynamic.
- DETAILS: close-ups of the weapon and of three signature objects of the outfit.

[PERSONAJE]
```

## Prompt hoja 2 · Retratos

```
Use the first image as the layout template and the second image as the character reference. Keep every box, border and label where it is, and draw only inside the boxes. Box backgrounds stay flat #A9CBA6 green.

Style: pixel-art-ready anime portrait in the Fire Emblem GBA style. 1 px black line on the silhouette edge and a 1 px pure white outline outside it. Flat colors only, limited to the 16 colors of the reference palette. Head and sides never cropped, only the bottom edge cuts the body, small green margin above the head.

- ESCENA: waist-up portrait, body slightly turned, face looking to the right.
- ESPEJO REAL: the same portrait redrawn facing left. This is NOT a flipped copy. Asymmetric objects stay on the same body side as in the reference, so the lighting and the visible details change.
- ESTADO: full body standing, same outfit, fits the tall box from head to feet.
- MINI: tiny chibi head only, readable at 32x32.
- BOCAS: six crops of the same mouth area from the ESCENA face, same scale and framing: normal closed, normal half open, normal open, smiling closed, smiling half open, smiling open.
- OJOS: two crops of the same eye area from the ESCENA face, same scale and framing: half closed, closed.
- POSES: three alternate waist-up portraits with the same framing as ESCENA (for example angry, wounded, laughing).

[PERSONAJE]
```

## Prompt hoja 3 · Sprites

```
Use the first image as the layout template and the second image as the character reference. Keep every box, border and label where it is, and draw only inside the boxes. Box backgrounds stay flat #A9CBA6 green.

Style: Game Boy Advance pixel art, Fire Emblem GBA sprite style, crisp pixels, no anti-aliasing, single dark outline color #282828, maximum 16 colors from the reference palette. The camera-facing side of the body is brighter than the side facing away.

- MAPA QUIETO: tiny 16x16 chibi map sprite, three idle frames with a small breathing bob.
- MAPA EN MOVIMIENTO: the same tiny sprite walking. Four frames facing left, four facing down, four facing up, and three "selected" frames where the unit raises its weapon or reacts.
- BATALLA: battle animation key frames, full body about 34 px tall in the original size, standing on the red line and facing LEFT toward the enemy. Poses: idle, melee attack, melee critical with a stronger windup, ranged attack, ranged critical, dodge (quick step back), missed attack, weapon impact frame.

[PERSONAJE]
```

## Personajes de prueba

Uno por clase base, para probar tres siluetas distintas.

### 1 · Bastión

```
Character: Teodora, Bastion class (heavy tank). Elyrian refugee woman in her forties, broad and solid, short dark curly hair with a single grey streak. Wears heavy armor improvised from salvaged scrap: riveted plates of mismatched metal, a riveted bronze pauldron on her LEFT shoulder only, exposed aether valves on the back venting faint teal steam, leather straps holding a tool belt with wrenches and spare rivets. Weapon: a large hammer-axe built from a machine part. Palette: dark iron grey, oxidized bronze, worn brown leather, muted teal aether glow, olive skin. Expression: tired but protective.
```

### 2 · Deslizador

```
Character: Lysandros, Glider class (fast mobility). Young Cassarian courier, slim and agile, messy light brown hair tied back, goggles pushed up on the forehead. Wears a light leather and canvas flight suit with a rigid folding wing harness on the back made of brass ribs and stretched sailcloth, small aether thrusters on the boots leaving a thin white vapor trail. Many pouches, map tubes and a signal whistle on cords. Weapon: a short spear that folds in half. Palette: sand beige, sky blue cloth, polished brass, dark brown leather, fair tanned skin. Expression: confident, half smile.
```

### 3 · Tejedor

```
Character: Ione, Weaver class (aether magic). Elyrian woman in her twenties, long black hair with several silver-grey strands from memories lost to the aether. Wears a dark violet layered robe with Greek-style draped cloth over a fitted vest full of straps, glass vials of glowing aether and a small brass channeling gauntlet on her RIGHT hand. Visible teal aether conduits run under the skin of her right forearm and neck. Unstable teal glow in her eyes when casting. Weapon: the gauntlet projects aether threads. Palette: deep violet, black, brass, bright teal aether, pale skin. Expression: focused and melancholic.
```
