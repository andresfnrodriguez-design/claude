# Referencia cruzada — imágenes ↔ script (Kairon, Mode 1)

## Del código a la imagen (en el orden que aparecen en el script)

| Archivo | Duración | Fase de la animación |
|---|---|---|
| `frame_01_248x160.png` | 1 | Parado, inicio |
| `frame_02_248x160.png` | 2 | Acercamiento |
| `frame_03_248x160.png` | 2 | Acercamiento |
| `frame_04_248x160.png` | 2 | Acercamiento |
| `frame_05_248x160.png` | 2 | Acercamiento |
| `frame_06_248x160.png` | 2 | Acercamiento |
| `frame_07_248x160.png` | 2 | Acercamiento |
| `frame_08_248x160.png` | 2 | Acercamiento, último tramo |
| `frame_09_248x160.png` | 3 | Salto/aire |
| `frame_10_248x160.png` | 3 | Salto/aire |
| `frame_11_248x160.png` | 3 | Salto/aire |
| `frame_12_248x160.png` | 2 | Carga del brazo, justo antes del golpe |
| — | — | **acá disparan C04 / C1A / C1F** |
| `frame_13_248x160.png` | 2 | **Impacto — brazo en extensión completa** |
| `frame_14_248x160.png` | 2 | Retroceso del golpe |
| `frame_15_248x160.png` | 2 | Retroceso del golpe |
| `frame_16_248x160.png` | 2 | Retroceso del golpe |
| — | — | **acá dispara C01 (espera)** |
| `frame_17_248x160.png` | 2 | **Vuelta a la posición de pie — esta ES la standing, no un archivo aparte** |

## Total de archivos únicos usados
**17 imágenes** — las 17 frames reales de tu animación cubren toda la secuencia, incluyendo la vuelta a pie al final. No hace falta ningún archivo adicional.

## Por qué el golpe dispara antes del frame 13, no antes
Revisé el contenido real de las 17 frames: el brazo llega a su extensión completa recién en el frame 13 — antes de eso todavía está en camino (salto, carga). Poner el hit ahí es lo que hace que el flash de daño en el juego coincida visualmente con el puño llegando a destino.

## Pendiente
Cuando tengas el material del crítico (Mode 3), agrego esa sección acá mismo.
