# Fisuras de Elyria: registro de implementaciones

Aquí van todos los megaprompts de implementación del hack, junto con lo que respondió el modelo y lo que se decidió en cada caso.

**Cómo se usa**
1. Cada implementación tiene su propio archivo `NN-nombre.md` en esta carpeta, con el megaprompt completo.
2. Mandas el prompt y **pegas la respuesta de feedback** en la sección de esa implementación.
3. Anotas las decisiones y cambias el estado.
4. Para una implementación nueva, copias la plantilla del final.

**Estados:** `Borrador` → `Enviado` → `Feedback recibido` → `Plan aprobado` → `Implementado` → `Probado en mGBA`

## Índice

| # | Implementación | Prompt | Estado |
|---|---|---|---|
| 01 | Barras de vida en el mapa (estilo Fates) | [01-barras-de-vida-fates.md](01-barras-de-vida-fates.md) | Borrador |
| 02 | Íconos de botín, crítico y efectividad | [02-iconos-de-amenaza.md](02-iconos-de-amenaza.md) | Borrador |

---

## 01 · Barras de vida en el mapa (estilo Fates)

**Estado:** Borrador
**Prompt:** [01-barras-de-vida-fates.md](01-barras-de-vida-fates.md)

### Feedback del modelo
<!-- Pega aquí la respuesta completa. -->

```
(pendiente)
```

### ¿Entendió bien?
- [ ] Sí
- [ ] Hay malentendidos (anótalos):

### Sacrificios que propuso
| Funcionalidad | Qué propone | ¿Lo acepto? |
|---|---|---|
| | | |

### Decisiones
-

### Resultado
- Parche / commit:
- Probado en mGBA:
- Notas:

---

## 02 · Íconos de botín, crítico y efectividad

**Estado:** Borrador
**Prompt:** [02-iconos-de-amenaza.md](02-iconos-de-amenaza.md)

**Propuestas para confirmar:** la efectividad se calcula contra la unidad elegida; si hay crítico y efectividad a la vez, los dos `!` se alternan; la bolsa se ve siempre.

### Feedback del modelo
<!-- Pega aquí la respuesta completa. -->

```
(pendiente)
```

### ¿Entendió bien?
- [ ] Sí
- [ ] Hay malentendidos (anótalos):

### Sacrificios que propuso
| Funcionalidad | Qué propone | ¿Lo acepto? |
|---|---|---|
| | | |

### Decisiones
-

### Resultado
- Parche / commit:
- Probado en mGBA:
- Notas:

---

## Plantilla para una implementación nueva

```markdown
## NN · Nombre

**Estado:** Borrador
**Prompt:** [NN-nombre.md](NN-nombre.md)

### Feedback del modelo
(pegar aquí)

### ¿Entendió bien?
- [ ] Sí
- [ ] Hay malentendidos (anótalos):

### Sacrificios que propuso
| Funcionalidad | Qué propone | ¿Lo acepto? |
|---|---|---|

### Decisiones
-

### Resultado
- Parche / commit:
- Probado en mGBA:
- Notas:
```
