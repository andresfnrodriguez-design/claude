#!/usr/bin/env node
// Busca la orientación de impresión de una figura (STL u OBJ) y la entrega como
// --rot de Support Fins: los mismos ángulos "X · Y · Z" que muestra printfins.com.
//
// 1. Muestrea ~1500 direcciones de apoyo y mide, rápido, altura y voladizos.
// 2. A las mejores las evalúa en detalle: tira rayos verticales sobre una grilla y
//    mide soporte desde la cama, soporte apoyado sobre la propia figura, puntas
//    colgantes (islas), apoyo en la cama, área por capa y un tiempo estimado.
// 3. Afina alrededor de las ganadoras y las ordena según --criterio.
import { parseArgs } from 'node:util';
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const FINS_CLI = path.join(HERE, 'vendor', 'support-fins', 'plugins', 'cli', 'support-fins.js');
const BED_EPS = 0.35; // como Support Fins: una cara a menos de esto de la cama apoya en ella
const CAMA_P1S = 250; // mm útiles por eje
const DEG = Math.PI / 180;

// --- argumentos ---------------------------------------------------------------

const AYUDA = `orientar -- orientación de impresión para figuras, con salida para Support Fins

uso: node orientar.mjs --in figura.stl [opciones]
     node orientar.mjs --in carpeta/ [opciones]       (todas las .stl y .obj)

  --in <archivo|carpeta>    STL (binario o ASCII) u OBJ
  --out <carpeta>           dónde escribir (por defecto <carpeta>/orientado/ o junto al archivo)
  --criterio <c>            capas (defecto) | tiempo | soportes
                              capas: la menor cantidad de capas; entre las que están dentro
                                     de --tolerancia, la de menos soporte
                              tiempo: el menor tiempo estimado
                              soportes: el menor soporte; a igualdad, menos capas
  --tolerancia <%>          margen de capas para el criterio "capas", defecto 10
  --capa <mm>               altura de capa, defecto la de maquina.json (0.06)
  --boquilla <mm>           defecto la de maquina.json (0.2)
  --umbral <grados>         ángulo desde la cama por debajo del cual una cara necesita
                            soporte, defecto 45 (igual que Support Fins)
  --escala <factor>         escala el modelo antes de analizar (p. ej. 1000 si viene en metros)
  --alto <mm>               escala el modelo para que mida esto de alto tal como viene (eje Z)
  --top <n>                 opciones a mostrar, defecto 5
  --exportar                guarda el STL ya girado y apoyado en la cama (<nombre>_orientado.stl)
  --fins                    aplica Support Fins con la orientación ganadora (<nombre>-fins.3mf)
  --fins-args "<args>"      opciones extra para Support Fins, p. ej. "--material petg --sway"
  --json                    resultados en JSON
  -h, --help                esta ayuda
`;

function leerArgs(argv) {
  const { values } = parseArgs({
    args: argv,
    options: {
      in: { type: 'string' }, out: { type: 'string' },
      criterio: { type: 'string', default: 'capas' },
      tolerancia: { type: 'string', default: '10' },
      capa: { type: 'string' }, boquilla: { type: 'string' },
      umbral: { type: 'string', default: '45' },
      escala: { type: 'string' }, alto: { type: 'string' },
      top: { type: 'string', default: '5' },
      exportar: { type: 'boolean', default: false },
      fins: { type: 'boolean', default: false },
      'fins-args': { type: 'string', default: '' },
      json: { type: 'boolean', default: false },
      direcciones: { type: 'string', default: '1500' },
      help: { type: 'boolean', short: 'h', default: false },
    },
    strict: true,
  });
  return values;
}

function num(nombre, s, min, max) {
  const v = Number(s);
  if (!Number.isFinite(v) || v < min || v > max) throw new UsoError(`--${nombre} debe estar entre ${min} y ${max}, llegó ${JSON.stringify(s)}`);
  return v;
}

class UsoError extends Error {}

// --- lectura de mallas --------------------------------------------------------

function leerSTL(buf) {
  if (buf.length >= 84) {
    const n = buf.readUInt32LE(80);
    if (84 + n * 50 === buf.length) {
      const pos = new Float64Array(n * 9);
      for (let i = 0; i < n; i++) {
        const o = 84 + i * 50 + 12;
        for (let k = 0; k < 9; k++) pos[i * 9 + k] = buf.readFloatLE(o + k * 4);
      }
      return pos;
    }
  }
  const txt = buf.toString('latin1');
  if (!/^\s*solid/.test(txt)) throw new Error('no parece un STL válido');
  const nums = [];
  for (const m of txt.matchAll(/vertex\s+(\S+)\s+(\S+)\s+(\S+)/g)) nums.push(+m[1], +m[2], +m[3]);
  if (nums.length === 0 || nums.length % 9) throw new Error('STL ASCII sin triángulos');
  return Float64Array.from(nums);
}

function leerOBJ(txt) {
  const v = [];
  const out = [];
  for (const linea of txt.split('\n')) {
    if (linea.startsWith('v ')) {
      const p = linea.trim().split(/\s+/);
      v.push([+p[1], +p[2], +p[3]]);
    } else if (linea.startsWith('f ')) {
      const idx = linea.trim().split(/\s+/).slice(1).map((t) => {
        const i = parseInt(t.split('/')[0], 10);
        return i < 0 ? v.length + i : i - 1;
      });
      for (let k = 1; k + 1 < idx.length; k++) out.push(...v[idx[0]], ...v[idx[k]], ...v[idx[k + 1]]);
    }
  }
  if (out.length === 0) throw new Error('OBJ sin caras');
  return Float64Array.from(out);
}

function leerMalla(archivo) {
  const buf = fs.readFileSync(archivo);
  if (/\.stl$/i.test(archivo)) return leerSTL(buf);
  if (/\.obj$/i.test(archivo)) return leerOBJ(buf.toString('utf8'));
  throw new Error('solo lee .stl y .obj (exporta los .3mf como STL desde Bambu Studio)');
}

function escribirSTL(archivo, pos, nombre) {
  const n = pos.length / 9;
  const buf = Buffer.alloc(84 + n * 50);
  buf.write(nombre.slice(0, 79), 0, 'latin1');
  buf.writeUInt32LE(n, 80);
  for (let i = 0; i < n; i++) {
    const p = i * 9;
    const ux = pos[p + 3] - pos[p], uy = pos[p + 4] - pos[p + 1], uz = pos[p + 5] - pos[p + 2];
    const vx = pos[p + 6] - pos[p], vy = pos[p + 7] - pos[p + 1], vz = pos[p + 8] - pos[p + 2];
    let nx = uy * vz - uz * vy, ny = uz * vx - ux * vz, nz = ux * vy - uy * vx;
    const l = Math.hypot(nx, ny, nz) || 1;
    nx /= l; ny /= l; nz /= l;
    const o = 84 + i * 50;
    buf.writeFloatLE(nx, o); buf.writeFloatLE(ny, o + 4); buf.writeFloatLE(nz, o + 8);
    for (let k = 0; k < 9; k++) buf.writeFloatLE(pos[p + k], o + 12 + k * 4);
  }
  fs.writeFileSync(archivo, buf);
}

// --- preparación: soldar vértices, normales, volumen ---------------------------

function preparar(pos) {
  const mapa = new Map();
  const V = [];
  const F = [];
  const q = 1e4; // soldar a 0,1 micra
  const indice = (x, y, z) => {
    const k = `${Math.round(x * q)},${Math.round(y * q)},${Math.round(z * q)}`;
    let i = mapa.get(k);
    if (i === undefined) { i = V.length / 3; mapa.set(k, i); V.push(x, y, z); }
    return i;
  };
  for (let p = 0; p < pos.length; p += 9) {
    const a = indice(pos[p], pos[p + 1], pos[p + 2]);
    const b = indice(pos[p + 3], pos[p + 4], pos[p + 5]);
    const c = indice(pos[p + 6], pos[p + 7], pos[p + 8]);
    if (a !== b && b !== c && a !== c) F.push(a, b, c);
  }
  const verts = Float64Array.from(V);
  const caras = Int32Array.from(F);
  const nF = caras.length / 3;

  // volumen con signo y centro de masa (tetraedros contra el origen)
  let vol = 0, cx = 0, cy = 0, cz = 0;
  for (let f = 0; f < nF; f++) {
    const [ax, ay, az] = vtx(verts, caras[f * 3]);
    const [bx, by, bz] = vtx(verts, caras[f * 3 + 1]);
    const [qx, qy, qz] = vtx(verts, caras[f * 3 + 2]);
    const v6 = ax * (by * qz - bz * qy) - ay * (bx * qz - bz * qx) + az * (bx * qy - by * qx);
    vol += v6; cx += v6 * (ax + bx + qx); cy += v6 * (ay + by + qy); cz += v6 * (az + bz + qz);
  }
  let invertida = false;
  if (vol < 0) {
    // normales hacia adentro: dar vuelta todas las caras
    invertida = true;
    for (let f = 0; f < nF; f++) { const t = caras[f * 3 + 1]; caras[f * 3 + 1] = caras[f * 3 + 2]; caras[f * 3 + 2] = t; }
  }
  const volumen = Math.abs(vol) / 6;
  const centro = Math.abs(vol) > 1e-9 ? [cx / (4 * vol), cy / (4 * vol), cz / (4 * vol)] : centroideVertices(verts);

  // normales y áreas por cara
  const normales = new Float64Array(nF * 3);
  const areas = new Float64Array(nF);
  let areaTotal = 0;
  for (let f = 0; f < nF; f++) {
    const [ax, ay, az] = vtx(verts, caras[f * 3]);
    const [bx, by, bz] = vtx(verts, caras[f * 3 + 1]);
    const [qx, qy, qz] = vtx(verts, caras[f * 3 + 2]);
    const ux = bx - ax, uy = by - ay, uz = bz - az, wx = qx - ax, wy = qy - ay, wz = qz - az;
    const nx = uy * wz - uz * wy, ny = uz * wx - ux * wz, nz = ux * wy - uy * wx;
    const l = Math.hypot(nx, ny, nz);
    areas[f] = l / 2; areaTotal += l / 2;
    if (l > 0) { normales[f * 3] = nx / l; normales[f * 3 + 1] = ny / l; normales[f * 3 + 2] = nz / l; }
  }

  // bordes abiertos (malla no cerrada)
  const aristas = new Map();
  for (let f = 0; f < nF; f++) {
    for (let k = 0; k < 3; k++) {
      const a = caras[f * 3 + k], b = caras[f * 3 + (k + 1) % 3];
      const key = a < b ? a * 4294967296 + b : b * 4294967296 + a;
      aristas.set(key, (aristas.get(key) || 0) + 1);
    }
  }
  let bordes = 0;
  for (const c of aristas.values()) if (c !== 2) bordes++;

  // vecinos de cada vértice y caras de cada vértice (para islas)
  const nV = verts.length / 3;
  const grado = new Int32Array(nV + 1);
  for (let i = 0; i < caras.length; i++) grado[caras[i] + 1]++;
  for (let i = 0; i < nV; i++) grado[i + 1] += grado[i];
  const carasDe = new Int32Array(caras.length);
  const llenado = grado.slice(0, nV);
  for (let i = 0; i < caras.length; i++) carasDe[llenado[caras[i]]++] = (i / 3) | 0;

  return { verts, caras, normales, areas, areaTotal, volumen, centro, invertida, bordes, inicioCaras: grado, carasDe };
}

const vtx = (V, i) => [V[i * 3], V[i * 3 + 1], V[i * 3 + 2]];

function centroideVertices(V) {
  let x = 0, y = 0, z = 0;
  const n = V.length / 3;
  for (let i = 0; i < V.length; i += 3) { x += V[i]; y += V[i + 1]; z += V[i + 2]; }
  return [x / n, y / n, z / n];
}

// --- rotaciones, en la convención de Support Fins / three.js ------------------

/** Igual que plugins/cli/cli.js rotationMatrix: Euler XYZ en grados, R = Rx·Ry·Rz. Fila mayor. */
function matrizDeEuler([ax, ay, az]) {
  const [cx, sx, cy, sy, cz, sz] = [Math.cos(ax * DEG), Math.sin(ax * DEG), Math.cos(ay * DEG),
    Math.sin(ay * DEG), Math.cos(az * DEG), Math.sin(az * DEG)];
  return [
    cy * cz, -cy * sz, sy,
    cx * sz + sx * sy * cz, cx * cz - sx * sy * sz, -sx * cy,
    sx * sz - cx * sy * cz, sx * cz + cx * sy * sz, cx * cy,
  ];
}

/** three.js Euler.setFromRotationMatrix, orden XYZ. */
function eulerDeMatriz(m) {
  const y = Math.asin(Math.max(-1, Math.min(1, m[2])));
  let x, z;
  if (Math.abs(m[2]) < 0.9999999) { x = Math.atan2(-m[5], m[8]); z = Math.atan2(-m[1], m[0]); }
  else { x = Math.atan2(m[7], m[4]); z = 0; }
  return [x / DEG, y / DEG, z / DEG];
}

/** Rotación que lleva la dirección d (unitaria, del modelo) a -Z: esa cara queda mirando a la cama. */
function rotacionHaciaCama(d) {
  const [ax, ay, az] = d;
  const c = -az; // d · (0,0,-1)
  if (c < -0.999999) return [1, 0, 0, 0, -1, 0, 0, 0, -1];
  const vx = -ay, vy = ax, vz = 0; // d × (0,0,-1)
  const k = 1 / (1 + c);
  return [
    1 - (vy * vy + vz * vz) * k, -vz + vx * vy * k, vy + vx * vz * k,
    vz + vx * vy * k, 1 - (vx * vx + vz * vz) * k, -vx + vy * vz * k,
    -vy + vx * vz * k, vx + vy * vz * k, 1 - (vx * vx + vy * vy) * k,
  ];
}

const redondear = (x, d = 2) => Math.round(x * 10 ** d) / 10 ** d;

/** Candidato con ángulos ya redondeados: lo que se mide es exactamente lo que se escribe en --rot. */
function candidato(d) {
  const rot = eulerDeMatriz(rotacionHaciaCama(d)).map((a) => redondear(a) + 0);
  const R = matrizDeEuler(rot);
  // dirección del modelo que queda abajo con los ángulos redondeados: -(fila 3 de R)
  const abajo = [-R[6], -R[7], -R[8]];
  return { rot, R, abajo };
}

function fibonacci(n) {
  const out = [];
  const ga = Math.PI * (3 - Math.sqrt(5));
  for (let i = 0; i < n; i++) {
    const z = 1 - (2 * (i + 0.5)) / n;
    const r = Math.sqrt(1 - z * z);
    out.push([Math.cos(ga * i) * r, Math.sin(ga * i) * r, z]);
  }
  return out;
}

const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const normalizar = (a) => { const l = Math.hypot(...a); return [a[0] / l, a[1] / l, a[2] / l]; };

// --- etapa 1: barrido rápido -------------------------------------------------

function barrido(m, dirs, cosU) {
  const { verts, normales, areas, caras } = m;
  const nF = areas.length;
  // submuestra de caras para que el barrido no dependa del tamaño de la malla
  const paso = Math.max(1, Math.floor(nF / 30000));
  const cent = [];
  const nor = [];
  const ar = [];
  for (let f = 0; f < nF; f += paso) {
    const [a, b, c] = [caras[f * 3], caras[f * 3 + 1], caras[f * 3 + 2]];
    cent.push((verts[a * 3] + verts[b * 3] + verts[c * 3]) / 3, (verts[a * 3 + 1] + verts[b * 3 + 1] + verts[c * 3 + 1]) / 3,
      (verts[a * 3 + 2] + verts[b * 3 + 2] + verts[c * 3 + 2]) / 3);
    nor.push(normales[f * 3], normales[f * 3 + 1], normales[f * 3 + 2]);
    ar.push(areas[f] * paso);
  }
  const nV = verts.length / 3;
  return dirs.map((d) => {
    const up = [-d[0], -d[1], -d[2]];
    let zmin = Infinity, zmax = -Infinity;
    for (let i = 0; i < nV; i++) {
      const z = verts[i * 3] * up[0] + verts[i * 3 + 1] * up[1] + verts[i * 3 + 2] * up[2];
      if (z < zmin) zmin = z; if (z > zmax) zmax = z;
    }
    let voladizo = 0, soporte = 0;
    for (let j = 0; j < ar.length; j++) {
      const nz = nor[j * 3] * up[0] + nor[j * 3 + 1] * up[1] + nor[j * 3 + 2] * up[2];
      if (nz >= -cosU) continue;
      const z = cent[j * 3] * up[0] + cent[j * 3 + 1] * up[1] + cent[j * 3 + 2] * up[2] - zmin;
      if (z < BED_EPS) continue;
      voladizo += ar[j];
      soporte += ar[j] * -nz * z; // hasta la cama: sobreestima el soporte que apoya en la figura
    }
    return { d, alto: zmax - zmin, voladizo, soporte };
  });
}

/** Caras planas grandes (bases, peanas): apoyarlas en la cama es un candidato obvio. */
function carasPlanas(m) {
  const { normales, areas, areaTotal } = m;
  const orden = [...areas.keys()].sort((a, b) => areas[b] - areas[a]).slice(0, 4000);
  const grupos = [];
  for (const f of orden) {
    const n = [normales[f * 3], normales[f * 3 + 1], normales[f * 3 + 2]];
    const g = grupos.find((x) => dot(x.n, n) > 0.996);
    if (g) g.area += areas[f]; else grupos.push({ n, area: areas[f] });
  }
  return grupos.filter((g) => g.area > areaTotal * 0.005).sort((a, b) => b.area - a.area).slice(0, 8).map((g) => g.n);
}

// --- etapa 2: evaluación detallada por rayos verticales ------------------------

function evaluar(m, cand, cfg) {
  const { verts, caras, normales, areas, centro } = m;
  const { R } = cand;
  const h = cfg.capa, c = cfg.celda, cosU = cfg.cosU;
  const nV = verts.length / 3, nF = areas.length;

  // vértices girados, apoyados en z = 0
  const P = new Float64Array(nV * 3);
  let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity, z0 = Infinity, z1 = -Infinity;
  for (let i = 0; i < nV; i++) {
    const x = verts[i * 3], y = verts[i * 3 + 1], z = verts[i * 3 + 2];
    const px = R[0] * x + R[1] * y + R[2] * z, py = R[3] * x + R[4] * y + R[5] * z, pz = R[6] * x + R[7] * y + R[8] * z;
    P[i * 3] = px; P[i * 3 + 1] = py; P[i * 3 + 2] = pz;
    if (px < x0) x0 = px; if (px > x1) x1 = px; if (py < y0) y0 = py; if (py > y1) y1 = py;
    if (pz < z0) z0 = pz; if (pz > z1) z1 = pz;
  }
  for (let i = 2; i < P.length; i += 3) P[i] -= z0;
  const alto = z1 - z0;
  const capas = Math.ceil(alto / h - 1e-9);
  const nB = capas + 2;

  const nx = Math.max(1, Math.ceil((x1 - x0) / c)), ny = Math.max(1, Math.ceil((y1 - y0) / c));
  // normal z de cada cara ya girada
  const nzF = new Float64Array(nF);
  for (let f = 0; f < nF; f++) nzF[f] = R[6] * normales[f * 3] + R[7] * normales[f * 3 + 1] + R[8] * normales[f * 3 + 2];

  // rayos verticales en el centro de cada celda: dónde cortan a cada cara
  let cap = Math.max(1024, nF * 2);
  let eCelda = new Int32Array(cap), eZ = new Float64Array(cap), eCara = new Int32Array(cap);
  let nE = 0;
  const perim = new Float64Array(nB); // largo de contorno por capa (paredes)
  const piel = new Float64Array(nB); // largo de relleno sólido de tapas y pisos
  const ancho = cfg.boquilla * 1.1;
  for (let f = 0; f < nF; f++) {
    const a = caras[f * 3], b = caras[f * 3 + 1], q = caras[f * 3 + 2];
    const ax = P[a * 3], ay = P[a * 3 + 1], az = P[a * 3 + 2];
    const bx = P[b * 3], by = P[b * 3 + 1], bz = P[b * 3 + 2];
    const qx = P[q * 3], qy = P[q * 3 + 1], qz = P[q * 3 + 2];
    const nz = nzF[f];
    // paredes: el contorno que deja esta cara en todas las capas que atraviesa
    const zlo = Math.min(az, bz, qz), zhi = Math.max(az, bz, qz);
    const b0 = Math.floor(zlo / h), b1 = Math.min(nB - 1, Math.floor(zhi / h));
    const largo = (areas[f] * Math.sqrt(Math.max(0, 1 - nz * nz))) / h;
    for (let k = b0; k <= b1; k++) perim[k] += largo / (b1 - b0 + 1);
    piel[Math.min(nB - 1, Math.floor((az + bz + qz) / 3 / h))] += (areas[f] * Math.abs(nz) * cfg.espesorTapas) / (ancho * h);

    const s = (bx - ax) * (qy - ay) - (by - ay) * (qx - ax); // 2 × área proyectada, con signo
    if (Math.abs(s) < 1e-12) continue;
    const i0 = Math.max(0, Math.ceil((Math.min(ax, bx, qx) - x0) / c - 0.5));
    const i1 = Math.min(nx - 1, Math.floor((Math.max(ax, bx, qx) - x0) / c - 0.5));
    const j0 = Math.max(0, Math.ceil((Math.min(ay, by, qy) - y0) / c - 0.5));
    const j1 = Math.min(ny - 1, Math.floor((Math.max(ay, by, qy) - y0) / c - 0.5));
    for (let j = j0; j <= j1; j++) {
      const py = y0 + (j + 0.5) * c;
      for (let i = i0; i <= i1; i++) {
        const px = x0 + (i + 0.5) * c;
        const w0 = ((bx - px) * (qy - py) - (by - py) * (qx - px)) / s;
        const w1 = ((qx - px) * (ay - py) - (qy - py) * (ax - px)) / s;
        const w2 = 1 - w0 - w1;
        if (w0 < 0 || w1 < 0 || w2 < 0) continue;
        if (nE === cap) {
          cap *= 2;
          const c2 = new Int32Array(cap); c2.set(eCelda); eCelda = c2;
          const z2 = new Float64Array(cap); z2.set(eZ); eZ = z2;
          const f2 = new Int32Array(cap); f2.set(eCara); eCara = f2;
        }
        eCelda[nE] = j * nx + i; eZ[nE] = w0 * az + w1 * bz + w2 * qz; eCara[nE] = f; nE++;
      }
    }
  }

  // agrupar los cortes por celda
  const nC = nx * ny;
  const ini = new Int32Array(nC + 1);
  for (let e = 0; e < nE; e++) ini[eCelda[e] + 1]++;
  for (let k = 0; k < nC; k++) ini[k + 1] += ini[k];
  const pos = ini.slice(0, nC);
  const orden = new Int32Array(nE);
  for (let e = 0; e < nE; e++) orden[pos[eCelda[e]]++] = e;

  const c2 = c * c;
  const dSolido = new Float64Array(nB + 1); // área sólida por capa (diferencias)
  const dSoporte = new Float64Array(nB + 1);
  let volSolido = 0, volSopCama = 0, volSopFigura = 0, areaSopFigura = 0, apoyo = 0;
  const apoyoPts = [];
  const lista = [];
  for (let k = 0; k < nC; k++) {
    const a = ini[k], b = ini[k + 1];
    if (a === b) continue;
    lista.length = 0;
    for (let t = a; t < b; t++) lista.push(orden[t]);
    lista.sort((p, q) => eZ[p] - eZ[q]);
    let prof = 0, entrada = 0, ultimaSalida = -1;
    for (const e of lista) {
      const z = eZ[e], nz = nzF[eCara[e]];
      if (nz < 0) { // entra al sólido desde abajo
        if (prof === 0) {
          const piso = ultimaSalida < 0 ? 0 : ultimaSalida;
          if (ultimaSalida < 0 && z < BED_EPS) {
            apoyo += c2;
            apoyoPts.push(x0 + ((k % nx) + 0.5) * c, y0 + (((k / nx) | 0) + 0.5) * c);
          } else if (nz < -cosU && z - piso >= h) {
            const v = (z - piso) * c2;
            if (ultimaSalida < 0) volSopCama += v; else { volSopFigura += v; areaSopFigura += c2; }
            dSoporte[Math.floor(piso / h)] += c2; dSoporte[Math.min(nB, Math.floor(z / h) + 1)] -= c2;
          }
          entrada = z;
        }
        prof++;
      } else if (prof > 0) { // sale por arriba
        prof--;
        if (prof === 0) {
          volSolido += (z - entrada) * c2;
          dSolido[Math.floor(entrada / h)] += c2; dSolido[Math.min(nB, Math.floor(z / h) + 1)] -= c2;
          ultimaSalida = z;
        }
      }
    }
  }

  // islas: puntas que cuelgan (mínimos locales) rodeadas de caras que no piden soporte
  let islas = 0, volIslas = 0;
  for (let v = 0; v < nV; v++) {
    const z = P[v * 3 + 2];
    if (z < BED_EPS) continue;
    let minimo = true, cubierta = false;
    for (let t = m.inicioCaras[v]; t < m.inicioCaras[v + 1] && minimo; t++) {
      const f = m.carasDe[t];
      if (nzF[f] < -cosU) cubierta = true;
      for (let k = 0; k < 3; k++) {
        const u = caras[f * 3 + k];
        if (u !== v && P[u * 3 + 2] <= z + 1e-4) { minimo = false; break; }
      }
    }
    if (minimo && !cubierta) { islas++; volIslas += z * 0.8; } // columna fina de ~0,8 mm²
  }

  // centro de masa girado
  const cmz = R[6] * centro[0] + R[7] * centro[1] + R[8] * centro[2] - z0;
  const cmx = R[0] * centro[0] + R[1] * centro[1] + R[2] * centro[2];
  const cmy = R[3] * centro[0] + R[4] * centro[1] + R[5] * centro[2];
  const estable = apoyo >= 4 && dentroDeCasco(cascoConvexo(apoyoPts), cmx, cmy);

  // tiempo estimado: por capa, lo que lleva extruir o el tiempo mínimo de capa
  let tiempo = 0, solida = 0, sop = 0;
  for (let k = 0; k < capas; k++) {
    solida += dSolido[k]; sop += dSoporte[k];
    const paredes = cfg.paredes * perim[k];
    const relleno = Math.max(0, solida - perim[k] * cfg.paredes * ancho) * cfg.relleno / ancho + piel[k];
    const soporte = sop * cfg.densidadSoporte / ancho;
    const t = paredes / cfg.velParedes + relleno / cfg.velRelleno + soporte / cfg.velSoporte;
    tiempo += Math.max(t, cfg.tiempoMinCapa) + cfg.cambioCapa;
  }
  tiempo *= cfg.factor;

  const volSoporte = volSopCama + volSopFigura + volIslas;
  return {
    ...cand,
    alto, capas, ancho: x1 - x0, fondo: y1 - y0,
    centroMasa: cmz,
    volSopCama, volSopFigura, areaSopFigura, islas, volSoporte,
    penal: volSopCama + 2 * volSopFigura + volIslas + 2 * islas, // apoyar en la figura deja marcas: pesa doble
    apoyo, estable, tiempo, volSolido,
    entraEnCama: Math.max(x1 - x0, y1 - y0, alto) <= CAMA_P1S,
  };
}

function cascoConvexo(pts) {
  const p = [];
  for (let i = 0; i < pts.length; i += 2) p.push([pts[i], pts[i + 1]]);
  p.sort((a, b) => a[0] - b[0] || a[1] - b[1]);
  if (p.length < 3) return p;
  const cruz = (o, a, b) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);
  const lo = [], hi = [];
  for (const q of p) { while (lo.length >= 2 && cruz(lo[lo.length - 2], lo[lo.length - 1], q) <= 0) lo.pop(); lo.push(q); }
  for (const q of p.reverse()) { while (hi.length >= 2 && cruz(hi[hi.length - 2], hi[hi.length - 1], q) <= 0) hi.pop(); hi.push(q); }
  return lo.slice(0, -1).concat(hi.slice(0, -1));
}

function dentroDeCasco(h, x, y) {
  if (h.length < 3) return false;
  for (let i = 0; i < h.length; i++) {
    const a = h[i], b = h[(i + 1) % h.length];
    if ((b[0] - a[0]) * (y - a[1]) - (b[1] - a[1]) * (x - a[0]) < 0) return false;
  }
  return true;
}

// --- orden según el criterio ---------------------------------------------------

function ordenar(res, criterio, tol) {
  const ok = res.filter((r) => r.entraEnCama);
  const lista = ok.length ? ok : res;
  if (criterio === 'tiempo') return [...lista].sort((a, b) => a.tiempo - b.tiempo || a.penal - b.penal);
  if (criterio === 'soportes') return [...lista].sort((a, b) => a.penal - b.penal || a.capas - b.capas);
  // capas: dentro de la tolerancia gana el de menos soporte; afuera, el de menos capas
  const minCapas = Math.min(...lista.map((r) => r.capas));
  const limite = Math.floor(minCapas * (1 + tol / 100));
  const dentro = lista.filter((r) => r.capas <= limite).sort((a, b) => a.penal - b.penal || a.capas - b.capas);
  const fuera = lista.filter((r) => r.capas > limite).sort((a, b) => a.capas - b.capas || a.penal - b.penal);
  return dentro.concat(fuera);
}

function distintos(lista, n, angulo = 10) {
  const out = [];
  const cosA = Math.cos(angulo * DEG);
  for (const r of lista) {
    if (out.every((o) => dot(o.abajo, r.abajo) < cosA)) out.push(r);
    if (out.length === n) break;
  }
  return out;
}

function vecinos(d, grados) {
  const t1 = normalizar(Math.abs(d[2]) < 0.9 ? [-d[1], d[0], 0] : [0, -d[2], d[1]]);
  const t2 = [d[1] * t1[2] - d[2] * t1[1], d[2] * t1[0] - d[0] * t1[2], d[0] * t1[1] - d[1] * t1[0]];
  const tg = Math.tan(grados * DEG);
  const out = [];
  for (let k = 0; k < 8; k++) {
    const a = (k * Math.PI) / 4;
    out.push(normalizar([0, 1, 2].map((i) => d[i] + tg * (Math.cos(a) * t1[i] + Math.sin(a) * t2[i]))));
  }
  return out;
}

// --- una figura ---------------------------------------------------------------

function analizar(archivo, op) {
  let pos = leerMalla(archivo);
  let escala = op.escala ?? 1;
  if (op.alto) {
    let zmin = Infinity, zmax = -Infinity;
    for (let i = 2; i < pos.length; i += 3) { if (pos[i] < zmin) zmin = pos[i]; if (pos[i] > zmax) zmax = pos[i]; }
    escala = op.alto / (zmax - zmin);
  }
  if (escala !== 1) pos = pos.map((v) => v * escala);
  const m = preparar(pos);

  let r2 = 0;
  for (let i = 0; i < m.verts.length; i += 3) {
    r2 = Math.max(r2, (m.verts[i] - m.centro[0]) ** 2 + (m.verts[i + 1] - m.centro[1]) ** 2 + (m.verts[i + 2] - m.centro[2]) ** 2);
  }
  const diametro = 2 * Math.sqrt(r2);
  const cfg = { ...op.maquina, capa: op.capa, boquilla: op.boquilla, cosU: Math.cos(op.umbral * DEG),
    celda: Math.min(2, Math.max(0.1, diametro / 220)) };

  // etapa 1
  const dirs = [[0, 0, -1], ...carasPlanas(m), ...fibonacci(op.direcciones)];
  const rapido = barrido(m, dirs, cfg.cosU);
  const altoMin = Math.min(...rapido.map((r) => r.alto));
  const sopMax = Math.max(...rapido.map((r) => r.soporte)) || 1;
  const elegir = (clave, n) => distintos([...rapido].sort((a, b) => clave(a) - clave(b)).map((r) => ({ ...r, abajo: r.d })), n, 6);
  const pre = [
    { abajo: [0, 0, -1] },
    ...carasPlanas(m).map((n) => ({ abajo: n })),
    ...elegir((r) => r.alto, 14),
    ...elegir((r) => r.soporte, 14),
    ...elegir((r) => r.alto / altoMin + r.soporte / sopMax, 14),
  ];
  const vistos = [];
  const evaluados = [];
  const probar = (d) => {
    const cand = candidato(d);
    if (vistos.some((v) => dot(v, cand.abajo) > 0.99999)) return;
    vistos.push(cand.abajo);
    evaluados.push(evaluar(m, cand, cfg));
  };
  for (const p of pre) probar(p.abajo);

  // etapa 3: afinar alrededor de las mejores
  for (const grados of [4, 1.5]) {
    for (const r of distintos(ordenar(evaluados, op.criterio, op.tolerancia), 4)) for (const d of vecinos(r.abajo, grados)) probar(d);
  }
  const ranking = ordenar(evaluados, op.criterio, op.tolerancia);
  const original = evaluados.find((r) => r.rot.every((a) => a === 0)) ?? evaluar(m, candidato([0, 0, -1]), cfg);
  return { archivo, m, escala, pos, cfg, original, ranking, mejores: distintos(ranking, op.top), evaluados: evaluados.length };
}

// --- salida -------------------------------------------------------------------

const hm = (s) => { const mi = Math.round(s / 60); return mi >= 60 ? `${Math.floor(mi / 60)} h ${String(mi % 60).padStart(2, '0')} min` : `${mi} min`; };
const cm3 = (mm3) => (mm3 / 1000).toFixed(2);
const fmtRot = (r) => r.rot.map((a) => (Math.abs(a) < 0.005 ? 0 : a)).join(',');

function fila(etq, r) {
  return [etq.padEnd(9), fmtRot(r).padEnd(22), String(r.capas).padStart(6), r.alto.toFixed(1).padStart(7),
    r.centroMasa.toFixed(1).padStart(7), cm3(r.volSopCama).padStart(7), cm3(r.volSopFigura).padStart(8),
    String(r.islas).padStart(6), r.apoyo.toFixed(0).padStart(7), (r.estable ? 'sí' : 'no').padStart(7),
    hm(r.tiempo).padStart(12)].join(' ');
}

function informe(res, op) {
  const { m, original, mejores } = res;
  const L = [];
  L.push(`\n${path.basename(res.archivo)}  (${m.areas.length.toLocaleString('es-AR')} triángulos, ${cm3(m.volumen)} cm³${res.escala !== 1 ? `, escala ×${redondear(res.escala, 4)}` : ''})`);
  if (m.invertida) L.push('  aviso: las normales venían hacia adentro; se analizaron dadas vuelta (revisa el modelo)');
  if (m.bordes) L.push(`  aviso: ${m.bordes} aristas abiertas o no-manifold: repáralo en Bambu Studio antes de imprimir; el soporte medido puede fallar`);
  if (Math.max(original.ancho, original.fondo, original.alto) < 5) L.push('  aviso: mide menos de 5 mm: ¿viene en metros o centímetros? usa --escala o --alto');
  L.push(`  capa ${op.capa} mm · umbral ${op.umbral}° · criterio "${op.criterio}"${op.criterio === 'capas' ? ` (tolerancia ${op.tolerancia}%)` : ''}`);
  L.push('');
  L.push(['', '--rot X,Y,Z'.padEnd(22), 'capas', 'alto', 'c.masa', 'sop.cama', 'sop.fig', 'islas', 'apoyo', 'estable', 'tiempo est.'].map((s, i) => (i < 2 ? s.padEnd(i ? 22 : 9) : s.padStart([6, 7, 7, 7, 8, 6, 7, 7, 12][i - 2]))).join(' '));
  L.push(['', '', '', 'mm', 'mm', 'cm³', 'cm³', '', 'mm²', '', ''].map((s, i) => (i < 2 ? s.padEnd(i ? 22 : 9) : s.padStart([6, 7, 7, 7, 8, 6, 7, 7, 12][i - 2]))).join(' '));
  L.push(fila('como viene', original).replace(/^como viene/, 'original '));
  mejores.forEach((r, i) => L.push(fila(i === 0 ? 'MEJOR' : `#${i + 1}`, r)));
  const b = mejores[0];
  const masRapida = [...res.ranking].sort((x, y) => x.tiempo - y.tiempo)[0];
  L.push('');
  L.push(`  Support Fins: --rot ${fmtRot(b)}   (en printfins.com: X ${b.rot[0]} · Y ${b.rot[1]} · Z ${b.rot[2]})`);
  const dc = original.capas - b.capas;
  L.push(`  frente a como viene: ${dc >= 0 ? `${dc} capas menos` : `${-dc} capas más`}, tiempo ${hm(original.tiempo)} → ${hm(b.tiempo)}`);
  if (masRapida !== b && masRapida.tiempo < b.tiempo * 0.95) {
    L.push(`  ojo: la más rápida estimada es --rot ${fmtRot(masRapida)} (${masRapida.capas} capas, ${hm(masRapida.tiempo)}); prueba --criterio tiempo`);
  }
  if (!b.estable) L.push('  apoyo chico o centro de masa fuera del apoyo: deja el bed pad de Support Fins en Auto (o brim) para que no se despegue');
  if (b.volSopFigura >= 50) L.push(`  ${cm3(b.volSopFigura)} cm³ de soporte apoyan sobre la propia figura (${b.areaSopFigura.toFixed(0)} mm² de marcas posibles)`);
  if (!b.entraEnCama) L.push('  no entra en la cama del P1S en ninguna orientación evaluada: escálalo o córtalo');
  L.push(`  (${res.evaluados} orientaciones evaluadas en detalle)`);
  return L.join('\n');
}

function resumenJSON(res) {
  const limpio = (r) => ({ rot: r.rot, capas: r.capas, alto_mm: redondear(r.alto), centro_masa_mm: redondear(r.centroMasa),
    soporte_cama_mm3: Math.round(r.volSopCama), soporte_figura_mm3: Math.round(r.volSopFigura), islas: r.islas,
    apoyo_mm2: Math.round(r.apoyo), estable: r.estable, tiempo_s: Math.round(r.tiempo), entra_en_cama: r.entraEnCama });
  return { archivo: res.archivo, escala: res.escala, original: limpio(res.original), mejores: res.mejores.map(limpio) };
}

// --- Support Fins --------------------------------------------------------------

function aplicarFins(res, op, carpeta) {
  if (!fs.existsSync(FINS_CLI)) throw new Error('falta Support Fins: corre "bash setup.sh" en tools/orientacion');
  const b = res.mejores[0];
  const base = path.basename(res.archivo).replace(/\.(stl|obj)$/i, '');
  let entrada = res.archivo;
  if (!/\.stl$/i.test(entrada) || res.escala !== 1) {
    // Support Fins lee STL: se le pasa el modelo escalado, sin girar, y el giro va en --rot
    entrada = path.join(carpeta, `${base}_${res.escala !== 1 ? 'escalado' : 'convertido'}.stl`);
    escribirSTL(entrada, res.pos, base);
  }
  const salida = path.join(carpeta, `${base}-fins.3mf`);
  let capaFins = Math.min(0.4, Math.max(0.08, op.capa));
  const avisos = [];
  if (capaFins !== op.capa) avisos.push(`Support Fins acepta capas de 0,08 a 0,4 mm: los dientes se hicieron para ${capaFins} mm. Lamina las aletas a ${capaFins} o usa altura de capa variable en esa zona`);
  const args = [FINS_CLI, entrada, '--rot', fmtRot(b), '--layer-height', String(capaFins), '--threshold', String(op.umbral),
    '-o', salida, '--json', ...op.finsArgs];
  const r = spawnSync(process.execPath, args, { encoding: 'utf8' });
  if (r.status !== 0 && !r.stdout) throw new Error(`Support Fins falló: ${(r.stderr || '').trim()}`);
  let datos = null;
  try { datos = JSON.parse(r.stdout.trim().split('\n').pop()); } catch { /* sin JSON */ }
  return { salida, avisos, informe: datos?.report ?? r.stdout.trim(), stats: datos?.stats ?? null, error: (r.stderr || '').trim() };
}

// --- principal ----------------------------------------------------------------

function cargarMaquina() {
  const j = JSON.parse(fs.readFileSync(path.join(HERE, 'maquina.json'), 'utf8'));
  return {
    boquilla: j.boquilla, capa: j.capa, paredes: j.paredes, relleno: j.relleno, densidadSoporte: j.densidad_soporte,
    espesorTapas: j.espesor_tapas_mm, velParedes: j.vel_paredes, velRelleno: j.vel_relleno, velSoporte: j.vel_soporte,
    tiempoMinCapa: j.tiempo_min_capa_s, cambioCapa: j.cambio_capa_s, factor: j.factor,
  };
}

function main() {
  let a;
  try { a = leerArgs(process.argv.slice(2)); } catch (e) { console.error(`orientar: ${e.message}`); return 2; }
  if (a.help || !a.in) { console.log(AYUDA); return a.help ? 0 : 2; }
  const maquina = cargarMaquina();
  let op;
  try {
    if (!['capas', 'tiempo', 'soportes'].includes(a.criterio)) throw new UsoError(`--criterio: capas, tiempo o soportes, llegó ${a.criterio}`);
    op = {
      maquina, criterio: a.criterio,
      tolerancia: num('tolerancia', a.tolerancia, 0, 100),
      boquilla: a.boquilla ? num('boquilla', a.boquilla, 0.1, 1.2) : maquina.boquilla,
      capa: a.capa ? num('capa', a.capa, 0.02, 1) : maquina.capa,
      umbral: num('umbral', a.umbral, 20, 80),
      escala: a.escala ? num('escala', a.escala, 1e-6, 1e6) : undefined,
      alto: a.alto ? num('alto', a.alto, 1, 256) : undefined,
      top: Math.round(num('top', a.top, 1, 20)),
      direcciones: Math.round(num('direcciones', a.direcciones, 50, 20000)),
      finsArgs: a['fins-args'].split(/\s+/).filter(Boolean),
    };
    if (op.capa > op.boquilla * 0.75 + 1e-9) {
      throw new UsoError(`capa de ${op.capa} mm con boquilla de ${op.boquilla} mm: el máximo práctico es ~${redondear(op.boquilla * 0.75)} mm (75% de la boquilla)`);
    }
  } catch (e) { console.error(`orientar: ${e.message}`); return 2; }

  let archivos;
  let carpetaSalida;
  const st = fs.existsSync(a.in) ? fs.statSync(a.in) : null;
  if (!st) { console.error(`orientar: no existe ${a.in}`); return 2; }
  if (st.isDirectory()) {
    archivos = fs.readdirSync(a.in).filter((f) => /\.(stl|obj)$/i.test(f) && !/_orientado\.stl$|_escalado\.stl$|_convertido\.stl$/i.test(f)).sort().map((f) => path.join(a.in, f));
    carpetaSalida = a.out ?? path.join(a.in, 'orientado');
    if (!archivos.length) { console.error(`orientar: no hay .stl ni .obj en ${a.in}`); return 2; }
  } else {
    archivos = [a.in];
    carpetaSalida = a.out ?? path.dirname(a.in);
  }
  if (a.exportar || a.fins || archivos.length > 1) fs.mkdirSync(carpetaSalida, { recursive: true });

  const filasCSV = ['archivo,rot_x,rot_y,rot_z,capas,alto_mm,soporte_cama_cm3,soporte_figura_cm3,islas,estable,tiempo_min,capas_original,tiempo_original_min'];
  const salidaJSON = [];
  let fallas = 0;
  for (const archivo of archivos) {
    try {
      const t0 = Date.now();
      const res = analizar(archivo, op);
      const b = res.mejores[0];
      const extra = {};
      if (a.exportar) {
        const base = path.basename(archivo).replace(/\.(stl|obj)$/i, '');
        const P = new Float64Array(res.pos.length);
        let zmin = Infinity, x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
        for (let i = 0; i < P.length; i += 3) {
          const x = res.pos[i], y = res.pos[i + 1], z = res.pos[i + 2], R = b.R;
          P[i] = R[0] * x + R[1] * y + R[2] * z; P[i + 1] = R[3] * x + R[4] * y + R[5] * z; P[i + 2] = R[6] * x + R[7] * y + R[8] * z;
          zmin = Math.min(zmin, P[i + 2]); x0 = Math.min(x0, P[i]); x1 = Math.max(x1, P[i]); y0 = Math.min(y0, P[i + 1]); y1 = Math.max(y1, P[i + 1]);
        }
        for (let i = 0; i < P.length; i += 3) { P[i] -= (x0 + x1) / 2; P[i + 1] -= (y0 + y1) / 2; P[i + 2] -= zmin; }
        extra.stl = path.join(carpetaSalida, `${base}_orientado.stl`);
        escribirSTL(extra.stl, P, base);
      }
      if (a.fins) extra.fins = aplicarFins(res, op, carpetaSalida);
      if (a.json) {
        salidaJSON.push({ ...resumenJSON(res), ...(extra.stl ? { stl: extra.stl } : {}), ...(extra.fins ? { fins: extra.fins } : {}) });
      } else {
        console.log(informe(res, op));
        if (extra.stl) console.log(`  STL orientado: ${extra.stl}`);
        if (extra.fins) {
          for (const av of extra.fins.avisos) console.log(`  aviso: ${av}`);
          console.log(`  Support Fins → ${extra.fins.salida}\n    ${extra.fins.informe}`);
          if (extra.fins.error) console.log(`    ${extra.fins.error}`);
        }
        console.log(`  (${((Date.now() - t0) / 1000).toFixed(1)} s)`);
      }
      filasCSV.push([path.basename(archivo), ...b.rot, b.capas, redondear(b.alto), cm3(b.volSopCama), cm3(b.volSopFigura), b.islas,
        b.estable ? 'si' : 'no', Math.round(b.tiempo / 60), res.original.capas, Math.round(res.original.tiempo / 60)].join(','));
    } catch (e) {
      fallas++;
      console.error(`orientar: ${archivo}: ${e.message}`);
    }
  }
  if (a.json) console.log(JSON.stringify(salidaJSON.length === 1 ? salidaJSON[0] : salidaJSON, null, 1));
  if (archivos.length > 1) {
    const csv = path.join(carpetaSalida, 'orientaciones.csv');
    fs.writeFileSync(csv, filasCSV.join('\n') + '\n');
    if (!a.json) console.log(`\nResumen: ${csv}`);
  }
  return fallas ? 1 : 0;
}

process.exitCode = main();
