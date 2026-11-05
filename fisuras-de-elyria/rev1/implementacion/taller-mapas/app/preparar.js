// Copia el editor, los datos y las imágenes de la carpeta de arriba para que la app use siempre la última versión.
const fs = require("fs");
const path = require("path");
for (const f of ["editor.html", "catalogo.js", "datos_fe8.js", "mapas_estimados.js"]) {
  fs.copyFileSync(path.join(__dirname, "..", f), path.join(__dirname, f));
}
fs.cpSync(path.join(__dirname, "..", "imagenes"), path.join(__dirname, "imagenes"), { recursive: true });
console.log("Editor, datos e imágenes copiados.");
