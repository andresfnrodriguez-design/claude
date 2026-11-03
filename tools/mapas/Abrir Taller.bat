@echo off
rem Abre el Taller de Mapas en una ventana propia de Edge, sin barra de navegador.
start "" msedge --app="file:///%~dp0editor.html" --window-size=1440,920
