// Copia el editor y el catálogo de la carpeta de arriba para que la app use siempre la última versión.
const fs = require("fs");
const path = require("path");
for (const f of ["editor.html", "catalogo.js", "datos_fe8.js"]) {
  fs.copyFileSync(path.join(__dirname, "..", f), path.join(__dirname, f));
}
console.log("Editor y catálogo copiados.");
