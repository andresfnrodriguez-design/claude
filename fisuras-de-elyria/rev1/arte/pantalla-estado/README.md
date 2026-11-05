# Pantalla de estado estilo GBA

`python3 generar.py` → `estado_gba.png` (240x160, RGB555) y `estado_gba_x4.png`.

Variables:
- `SIN_RETRATO=1`: sin el retrato de Kairos (para estudiar la paleta de la UI).
- `SIN_ICONOS=1`: sin los placeholders de iconos.

`python3 paleta.py <png>` → `paleta.png` / `paleta.txt` (RGB, hex, BGR555).

## Placeholders de iconos (no son parte de la paleta de la UI)
| Lugar | Significado |
|---|---|
| 2 libritos junto a la clase | tipos de arma que puede usar la clase |
| círculo del banner (Leather Shield) | arma/objeto equipado |
| cuadraditos en curva | magias/habilidades de la unidad |
