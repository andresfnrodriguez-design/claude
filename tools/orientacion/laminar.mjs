// Lamina un STL con PrusaSlicer (el mismo motor del que deriva Bambu Studio) y
// devuelve tiempo, filamento y cuánto de ese filamento es soporte. Se usa para
// elegir entre orientaciones con un tiempo real de laminador y no con una estimación.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawn, spawnSync } from 'node:child_process';

export function prusaDisponible() {
  return spawnSync('prusa-slicer', ['--help'], { encoding: 'utf8' }).status === 0;
}

function segundos(txt) {
  let s = 0;
  for (const [, n, u] of txt.matchAll(/(\d+)([dhms])/g)) s += Number(n) * { d: 86400, h: 3600, m: 60, s: 1 }[u];
  return s;
}

/** Lee el G-code: tiempo, gramos y la parte de soporte (por los ;TYPE: de PrusaSlicer). */
export function leerGcode(texto, densidad = 1.24, diametro = 1.75) {
  const tiempo = /; estimated printing time \(normal mode\) = (.+)/.exec(texto);
  const gramos = /; filament used \[g\] = ([\d.]+)/.exec(texto);
  const seccion = Math.PI * (diametro / 2) ** 2;
  let relativo = false, e = 0, tipo = '', soporte = 0, total = 0, capas = 0;
  for (const linea of texto.split('\n')) {
    const c = linea.charCodeAt(0);
    if (c === 59) { // ;
      if (linea.startsWith(';TYPE:')) tipo = linea.slice(6);
      else if (linea.startsWith(';LAYER_CHANGE')) capas++;
      continue;
    }
    if (linea.startsWith('M83')) { relativo = true; continue; }
    if (linea.startsWith('M82')) { relativo = false; continue; }
    if (linea.startsWith('G92')) { const m = / E([-\d.]+)/.exec(linea); if (m) e = Number(m[1]); continue; }
    if (linea.startsWith('G1 ') || linea.startsWith('G0 ')) {
      const m = / E([-\d.]+)/.exec(linea);
      if (!m) continue;
      const v = Number(m[1]);
      const d = relativo ? v : v - e;
      if (!relativo) e = v;
      // solo movimientos que extruyen mientras se desplazan: fuera retracciones y des-retracciones
      if (d > 0 && / [XY]/.test(linea)) { total += d; if (tipo.startsWith('Support material')) soporte += d; }
    }
  }
  const g = (mm) => (mm * seccion * densidad) / 1000;
  return {
    tiempo_s: tiempo ? segundos(tiempo[1]) : null,
    filamento_g: gramos ? Number(gramos[1]) : g(total),
    soporte_g: g(soporte),
    capas,
  };
}

/**
 * Lamina `stl` con el perfil `ini`, con la capa y la boquilla pedidas encima del perfil.
 * Devuelve { tiempo_s, filamento_g, soporte_g, capas } o { error }.
 */
export function laminar(stl, ini, capa, boquilla) {
  const extra = [];
  if (capa) extra.push('--layer-height', String(capa));
  if (boquilla) {
    // ancho de línea ~110% de la boquilla; caudal máximo de los perfiles de Bambu para PLA
    const ancho = Math.round(boquilla * 1.1 * 100) / 100;
    const caudal = boquilla <= 0.2 ? 2 : boquilla <= 0.4 ? 21 : 30;
    extra.push('--nozzle-diameter', String(boquilla), '--extrusion-width', String(ancho),
      '--first-layer-extrusion-width', String(Math.round(ancho * 1.15 * 100) / 100), '--filament-max-volumetric-speed', String(caudal));
  }
  return new Promise((resolve) => {
    const gcode = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'orientar-')), 'salida.gcode');
    const p = spawn('prusa-slicer', ['--export-gcode', '--load', ini, ...extra, '-o', gcode, stl], { stdio: ['ignore', 'ignore', 'pipe'] });
    let err = '';
    p.stderr.on('data', (d) => { err += d; });
    p.on('close', (code) => {
      try {
        if (code !== 0 || !fs.existsSync(gcode)) return resolve({ error: err.trim().split('\n').pop() || `código ${code}` });
        resolve(leerGcode(fs.readFileSync(gcode, 'utf8')));
      } finally {
        fs.rmSync(path.dirname(gcode), { recursive: true, force: true });
      }
    });
  });
}
