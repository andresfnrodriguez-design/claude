# Reglas de encuadre y escala (obligatorias)

Ningún personaje se entrega si no cumple esto. `procesar.py` lo verifica y corta con "NO ENTREGAR" si algo falla.

## Escala común
- Un solo juego de valores para todo el elenco, en la cabecera de `procesar.py`.
- `CABEZA_BUSTO = 34`, px de coronilla a mentón en el busto de 112.
- `ALTURA_ESTADO = 112`, px de coronilla a suela en el estado de 144 para estatura 1.0.
- Cada personaje tiene `estatura` en su `config.json` (ej. 1.06 alto, 0.93 baja) y `cabeza_A`, la cabeza medida en su panel A.
- Si un personaje nuevo no entra, se achica la escala para todos o se regenera su pose. Nunca se escala uno solo.

## Busto de diálogo (escena y espejo)
- Cabeza entera con margen arriba.
- Cabeza y hombros sin cortes a los costados. Solo el cuarto de abajo, los brazos a la altura de la cintura, puede tocar el borde.
- El busto sale por el borde de abajo.

## Estado
- Cuerpo completo, de la cabeza (o la punta del arma) a los pies, con margen arriba y a los costados.

## Prompt del panel C
- Pose compacta, brazos cerca del cuerpo, arma vertical, capa y escudo cerrados, margen de fondo a los dos lados.
