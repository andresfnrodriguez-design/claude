# Gestor de arte de Fisuras de Elyria

Especificación para que Claude Code construya la aplicación. Leela completa antes de empezar y construí por etapas, mostrando cada etapa funcionando antes de pasar a la siguiente.

## Qué es

Aplicación de escritorio en **Electron** para organizar, versionar, validar y exportar todo el arte de Fisuras de Elyria, un ROM hack de Fire Emblem 8 hecho sobre la decompilación fireemblem8u. El usuario no sabe programar, así que la interfaz tiene que ser clara, toda en español y sin depender de la terminal para el uso diario.

## Rutas

- Código de la app en `~/gestor-elyria`.
- Biblioteca de arte en `~/elyria-arte`, con su propio repositorio git.
- Decompilación en `~/fireemblem8u`.
- Las tres rutas se pueden cambiar desde una pantalla de Ajustes y se guardan en `ajustes.json`.

## Estructura de la biblioteca

```
elyria-arte/
  estandar.json            reglas de validación (editable sin tocar código)
  personajes/
    kairon/
      ficha.json           datos, clases vinculadas, estado de cada asset
      concepto/
      paleta/
      retrato_escena/
      retrato_escena_espejo/
      poses/<nombre_pose>/
      bocas/
      ojos/
      mini_retrato/
      retrato_estado/
      paleta_batalla/
      voz/
  clases/
    <clase>/
      ficha.json
      mapa_quieto/
      mapa_movimiento/
      batalla/<tipo_de_arma>/<modo>/
      paletas_batalla/
      efecto_hechizo/
      icono_arma/
```

Todo en archivos comunes (PNG, WAV, JSON) para que se pueda ver y respaldar fuera de la app.

## Fichas

**Personaje** con nombre, notas, la descripción usada en el generador de imágenes, clase base, clase promovida y una lista de clases exclusivas. Hay personajes con clase propia (por ejemplo un lord), así que una clase puede marcarse como exclusiva de un personaje y aparece dentro de su ficha.

**Clase** con nombre, tipos de arma, si es montada o grande (cambia el tamaño del sprite de mapa), si usa magia y qué personajes la usan.

Las clases se pueden crear desde la ficha de un personaje o por separado.

## Checklist de assets

Cada ficha muestra su lista de assets con el estado de cada uno, en este orden.

Estados posibles: pendiente, concepto, pixel art, validado, en el juego. Además cada asset puede marcarse como "no aplica" (por ejemplo el espejado real o el efecto de hechizo).

### Personaje

| Asset | Formato |
|---|---|
| Hoja maestra de concepto | Imagen libre. Giro completo, paleta, expresiones, pose de ataque |
| Paleta oficial | 16 colores, índice 0 = #A9CBA6 |
| Retrato de escena | 100x112 |
| Retrato de escena espejado real | 100x112, opcional |
| Poses alternativas | 100x112 cada una, con nombre |
| Bocas | 6 fotogramas de 32x16 (normal cerrada, entreabierta, abierta; sonriendo cerrada, entreabierta, abierta) por cada retrato y pose |
| Ojos | 2 fotogramas de 32x16 (entrecerrado, cerrado) por cada retrato y pose |
| Mini retrato | 32x32 |
| Retrato de pantalla de estado | 80x144 de cuerpo completo |
| Paleta de batalla propia | 16 colores, opcional |
| Sonido de voz | WAV corto, el bip que suena por letra cuando habla |

### Clase

| Asset | Formato |
|---|---|
| Mapa quieto | 3 fotogramas. Figura de 16x16 (16x32 o 32x32 si es grande o montada) |
| Mapa en movimiento | 15 fotogramas en celdas de 32x32, con la figura de 16x16 dentro. 4 izquierda, 4 abajo, 4 arriba, 3 seleccionado. La derecha la voltea el motor |
| Animación de batalla | Por tipo de arma. Modos ataque cuerpo a cuerpo, crítico cuerpo a cuerpo, ataque a distancia, crítico a distancia, esquive cuerpo a cuerpo, esquive a distancia, quieto cuerpo a cuerpo, quieto a distancia, ataque fallado. Lienzo de 248x160 por fotograma, personaje centrado en x=140 con los pies en y=102 |
| Paletas de batalla por bando | 4 (jugador, enemigo, aliado, otro) |
| Efecto de hechizo | Solo si usa magia |
| Ícono de arma única | 16x16, solo si tiene |

Todas estas medidas, cantidades de fotogramas y colores van en `estandar.json`, no en el código. Si el usuario cambia el estándar, edita ese archivo y la app lo respeta.

## Versiones

- Al cargar un archivo (arrastrar y soltar o botón) se guarda como `v001.png`, `v002.png`, etc. dentro de la carpeta del asset. Nunca se sobrescribe ni se borra nada.
- Cada versión guarda en la ficha la fecha, una nota opcional y el resultado de la validación.
- Una versión se marca como **vigente**. Es la que se muestra y la que se exporta.
- Se pueden comparar dos versiones lado a lado.
- Botón "Guardar cambios" que hace commit en el git de la biblioteca con un mensaje automático (personaje, asset, versión).

## Validador

Corre al cargar cada archivo y muestra en verde lo que cumple y en rojo lo que no, con el motivo en español.

- Tamaño exacto en píxeles según el asset.
- Cantidad de fotogramas y tamaño de celda en las hojas.
- PNG indexado con 16 colores como máximo.
- #A9CBA6 en el índice 0 de la paleta y que no aparezca dentro del personaje.
- Que los colores usen la paleta oficial del personaje (avisa qué píxeles no).
- Retratos con 3 px de fondo arriba, sin cortes en los costados y contorno negro de 1 px más contorno blanco de 1 px por fuera.

Un asset con errores puede guardarse igual, pero queda en estado "pixel art" hasta que pase la validación.

## Vista previa

- Zoom en píxeles enteros (x1 a x8) sin suavizado.
- Retrato de escena con las bocas y los ojos animados encima, imitando al motor (boca al azar cada 1 a 8 cuadros mientras habla, parpadeo al azar).
- Sprites de mapa y animaciones de batalla reproducidos en bucle a la velocidad del juego.
- Botón para reproducir el sonido de voz.
- Vista del retrato con fondo transparente y con el fondo verde.

## Conversiones

Herramientas para preparar el arte desde el generador de imágenes.

1. Reducir una imagen de 200x224 o 400x448 a 100x112 por voto mayoritario de cada bloque, nunca con suavizado.
2. Pasar a 16 colores usando la paleta oficial del personaje y poner #A9CBA6 en el índice 0.
3. Armar hojas de fotogramas a partir de imágenes sueltas en el orden que pide el estándar.
4. Cada resultado entra como una versión nueva del asset correspondiente.

## Exportar al juego

Botón por asset y botón "Exportar todo lo validado", que copian la versión vigente a las rutas de gráficos de `~/fireemblem8u` con el formato que espera la decompilación. Revisá cómo están organizados los gráficos en el proyecto antes de definir las rutas y anotalas en `estandar.json`. Antes de copiar, mostrá la lista de archivos que se van a reemplazar y pedí confirmación.

## Tablero general

Pantalla de inicio con una tabla de todos los personajes y clases, una columna por asset y un color por estado, para ver de un vistazo qué falta. Filtros por estado y por parte de la historia.

## Generar el .exe

El desarrollo se hace en WSL y se prueba con `npm start` (en Windows 11 la ventana se abre con WSLg). Instalá lo que falte para que Electron arranque en WSL.

Para el .exe portátil de Windows con electron-builder, prepará el script `scripts/copiar-a-windows.sh`, que copia el código sin `node_modules` a `/mnt/c/Users/andre/gestor-elyria`, y en el README dejá los comandos de PowerShell para instalar las dependencias y generar el .exe ahí. El .exe tiene que poder abrir la biblioteca que está en WSL por la ruta `\\wsl.localhost\Ubuntu\home\andy\elyria-arte`.

## Etapas de construcción

1. Proyecto Electron, biblioteca, fichas de personaje y clase, checklist y tablero.
2. Carga de archivos con versiones, vigente y git.
3. Validador con `estandar.json`.
4. Vista previa con animaciones y sonido.
5. Conversiones.
6. Exportar al juego.
7. Empaquetado como .exe.

Al terminar cada etapa, explicá en español y en pocas líneas qué se puede probar y cómo.
