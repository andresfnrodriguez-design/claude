// Ventana de escritorio para el Taller de Mapas. Carga el mismo editor.html.
const { app, BrowserWindow } = require("electron");
const path = require("path");

app.whenReady().then(() => {
  const ventana = new BrowserWindow({
    width: 1440,
    height: 920,
    autoHideMenuBar: true,
    backgroundColor: "#14161c",
    title: "Taller de Mapas Elyria",
  });
  ventana.loadFile(path.join(__dirname, "editor.html"));
});

app.on("window-all-closed", () => app.quit());
