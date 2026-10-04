#!/usr/bin/env node
/*
 * Aplica texturas de desplazamiento de BumpMesh (CNC Kitchen) a modelos STL
 * sin abrir el navegador. Usa el mismo motor que bumpmesh.com
 * (vendor/stlTexturizer/js/exportPipeline.js, AGPL-3.0).
 *
 *   node texturize.mjs --in pieza.stl --preset agarre
 *   node texturize.mjs --in carpeta/ --out salida/ --texture knurling --tile 20 --depth 0.5
 */
import { readFileSync, writeFileSync, existsSync, statSync, readdirSync, mkdirSync } from 'node:fs';
import { join, dirname, basename, extname, resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { parseArgs } from 'node:util';

const HERE = dirname(fileURLToPath(import.meta.url));
const ENGINE = join(HERE, 'vendor', 'stlTexturizer');

const MAPPING = {
  'planar-xy': 0, 'planar-xz': 1, 'planar-yz': 2,
  cylindrical: 3, spherical: 4, triplanar: 5, cubic: 6,
};

const HELP = `Uso: node texturize.mjs --in <stl|carpeta> [opciones]

  --in <ruta>         STL de entrada, o carpeta con varios STL
  --out <ruta>        STL de salida o carpeta (por defecto: <nombre>_textura.stl)
  --preset <nombre>   preset de presets.json (ver --list-presets)
  --texture <nombre>  textura incluida (ver --list-textures) o ruta a un PNG propio
  --mapping <modo>    triplanar | cubic | cylindrical | spherical | planar-xy | planar-xz | planar-yz
  --tile <mm>         tamaño de una repetición de la textura
  --depth <mm>        relieve máximo
  --nozzle <mm>       boquilla (0.4 por defecto); escala los presets
  --invert            hunde la textura en lugar de sobresalir
  --symmetric         gris medio neutro: sobresale y se hunde (conserva volumen)
  --bottom-angle <°>  no texturizar caras de apoyo hasta este ángulo (5 por defecto)
  --top-angle <°>     no texturizar caras superiores hasta este ángulo (0 = texturizar)
  --refine <mm>       largo máximo de arista al subdividir (mitad de --nozzle por defecto)
  --max-tris <n>      triángulos máximos de salida (1000000 por defecto)
  --list-presets | --list-textures | --help`;

const { values: opt } = parseArgs({
  options: {
    in: { type: 'string' }, out: { type: 'string' },
    preset: { type: 'string' }, texture: { type: 'string' }, mapping: { type: 'string' },
    tile: { type: 'string' }, depth: { type: 'string' }, nozzle: { type: 'string' },
    invert: { type: 'boolean' }, symmetric: { type: 'boolean' },
    'bottom-angle': { type: 'string' }, 'top-angle': { type: 'string' },
    refine: { type: 'string' }, 'max-tris': { type: 'string' },
    'list-presets': { type: 'boolean' }, 'list-textures': { type: 'boolean' },
    help: { type: 'boolean', short: 'h' },
  },
});

const presets = JSON.parse(readFileSync(join(HERE, 'presets.json'), 'utf8'));
delete presets._nota;

if (opt.help) { console.log(HELP); process.exit(0); }
if (opt['list-presets']) {
  for (const [k, p] of Object.entries(presets)) {
    console.log(`${k.padEnd(16)} ${p.texture.padEnd(12)} ${p.mapping.padEnd(12)} mosaico ${p.tile} mm, relieve ${p.depth} mm — ${p.descripcion}`);
  }
  process.exit(0);
}
if (!existsSync(join(ENGINE, 'js', 'exportPipeline.js')) || !existsSync(join(HERE, 'node_modules', 'three'))) {
  console.error('Falta el motor de BumpMesh. Ejecuta primero:  bash setup.sh');
  process.exit(1);
}
if (opt['list-textures']) {
  const names = readdirSync(join(ENGINE, 'textures')).filter(f => f.endsWith('.png')).map(f => f.slice(0, -4));
  console.log(names.join('\n'));
  process.exit(0);
}
if (!opt.in) { console.error(HELP); process.exit(1); }

const num = (v, name) => {
  if (v === undefined) return undefined;
  const n = Number(v);
  if (!Number.isFinite(n)) { console.error(`--${name} debe ser un número`); process.exit(1); }
  return n;
};

// ── Parámetros: preset → escalado por boquilla → overrides explícitos ──────────
const nozzle = num(opt.nozzle, 'nozzle') ?? 0.4;
let base = { texture: undefined, mapping: 'triplanar', tile: undefined, depth: undefined };
if (opt.preset) {
  const p = presets[opt.preset];
  if (!p) { console.error(`Preset desconocido: ${opt.preset}. Usa --list-presets.`); process.exit(1); }
  const k = nozzle / 0.4;
  const round = (x, d) => Math.round(x * 10 ** d) / 10 ** d;
  base = { texture: p.texture, mapping: p.mapping, tile: round(p.tile * k, 1), depth: round(p.depth * k, 2) };
}
const params = {
  texture: opt.texture ?? base.texture,
  mapping: opt.mapping ?? base.mapping,
  tile: num(opt.tile, 'tile') ?? base.tile,
  depth: num(opt.depth, 'depth') ?? base.depth,
};
if (!params.texture || params.tile === undefined || params.depth === undefined) {
  console.error('Indica --preset, o bien --texture, --tile y --depth.');
  process.exit(1);
}
if (!(params.mapping in MAPPING)) {
  console.error(`--mapping inválido: ${params.mapping}. Opciones: ${Object.keys(MAPPING).join(', ')}`);
  process.exit(1);
}
// Detalles más finos que medio ancho de línea no se imprimen: no tiene sentido subdividir más.
const refine = num(opt.refine, 'refine') ?? nozzle / 2;
const maxTris = num(opt['max-tris'], 'max-tris') ?? 1_000_000;

// ── Motor de BumpMesh ──────────────────────────────────────────────────────────
const engine = (f) => import(pathToFileURL(join(ENGINE, 'js', f)).href);
const THREE = await import('three');
const { unzlibSync } = await import('fflate');
const { runExportPipeline } = await engine('exportPipeline.js');
const { buildFaceWeights } = await engine('exclusion.js');

// ── Lectura de STL (binario y ASCII) ───────────────────────────────────────────
function loadSTL(path) {
  const b = readFileSync(path);
  const n = b.length >= 84 ? b.readUInt32LE(80) : 0;
  let pos;
  if (b.length === 84 + n * 50) {
    pos = new Float32Array(n * 9);
    let o = 84;
    for (let i = 0; i < n; i++) {
      o += 12;
      for (let v = 0; v < 9; v++) { pos[i * 9 + v] = b.readFloatLE(o); o += 4; }
      o += 2;
    }
  } else {
    const nums = [...b.toString('utf8').matchAll(/vertex\s+(\S+)\s+(\S+)\s+(\S+)/g)]
      .flatMap(m => [+m[1], +m[2], +m[3]]);
    if (!nums.length || nums.length % 9) throw new Error(`${path}: no es un STL válido`);
    pos = Float32Array.from(nums);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  g.computeVertexNormals();
  return g;
}

// ── Lectura de PNG (8 bits; gris, gris+alfa, RGB, RGBA) ────────────────────────
function decodePNG(path) {
  const d = readFileSync(path);
  if (d.readUInt32BE(0) !== 0x89504e47) throw new Error(`${path}: solo se admiten texturas PNG`);
  let p = 8, w, h, ct, bd, interlace;
  const idat = [];
  while (p < d.length) {
    const len = d.readUInt32BE(p), type = d.toString('ascii', p + 4, p + 8), s = p + 8;
    if (type === 'IHDR') { w = d.readUInt32BE(s); h = d.readUInt32BE(s + 4); bd = d[s + 8]; ct = d[s + 9]; interlace = d[s + 12]; }
    else if (type === 'IDAT') idat.push(d.subarray(s, s + len));
    else if (type === 'IEND') break;
    p = s + len + 4;
  }
  const ch = { 0: 1, 2: 3, 4: 2, 6: 4 }[ct];
  if (bd !== 8 || !ch || interlace) throw new Error(`${path}: PNG no soportado (usa 8 bits, sin entrelazado, sin paleta)`);
  const raw = unzlibSync(Buffer.concat(idat));
  const stride = w * ch, out = new Uint8ClampedArray(w * h * 4);
  let cur = new Uint8Array(stride), prev = new Uint8Array(stride), rp = 0;
  const paeth = (a, b, c) => { const q = a + b - c, pa = Math.abs(q - a), pb = Math.abs(q - b), pc = Math.abs(q - c); return pa <= pb && pa <= pc ? a : pb <= pc ? b : c; };
  for (let y = 0; y < h; y++) {
    const f = raw[rp++];
    for (let x = 0; x < stride; x++) {
      const a = x >= ch ? cur[x - ch] : 0, b = prev[x], c = x >= ch ? prev[x - ch] : 0, r = raw[rp++];
      cur[x] = (f === 0 ? r : f === 1 ? r + a : f === 2 ? r + b : f === 3 ? r + ((a + b) >> 1) : r + paeth(a, b, c)) & 0xff;
    }
    for (let x = 0; x < w; x++) {
      const si = x * ch, di = (y * w + x) * 4;
      const g = cur[si];
      out[di] = ch >= 3 ? cur[si] : g;
      out[di + 1] = ch >= 3 ? cur[si + 1] : g;
      out[di + 2] = ch >= 3 ? cur[si + 2] : g;
      out[di + 3] = ch === 4 ? cur[si + 3] : ch === 2 ? cur[si + 1] : 255;
    }
    [prev, cur] = [cur, prev];
  }
  return { data: out, width: w, height: h };
}

function texturePath(name) {
  if (existsSync(name)) return resolve(name);
  const builtin = join(ENGINE, 'textures', `${name}.png`);
  if (existsSync(builtin)) return builtin;
  throw new Error(`Textura no encontrada: ${name}. Usa --list-textures o la ruta a un PNG.`);
}

// Pesos por vértice: 1 = sin textura. Enmascara caras de apoyo y superiores por ángulo.
function faceWeightsFor(geometry, s) {
  const w = buildFaceWeights(geometry, new Set(), false);
  if (!(s.bottomAngleLimit > 0 || s.topAngleLimit > 0)) return w;
  const pa = geometry.attributes.position.array;
  for (let t = 0; t < pa.length / 9; t++) {
    const i = t * 9;
    const ux = pa[i + 3] - pa[i], uy = pa[i + 4] - pa[i + 1], uz = pa[i + 5] - pa[i + 2];
    const vx = pa[i + 6] - pa[i], vy = pa[i + 7] - pa[i + 1], vz = pa[i + 8] - pa[i + 2];
    const nx = uy * vz - uz * vy, ny = uz * vx - ux * vz, nz = ux * vy - uy * vx;
    const len = Math.hypot(nx, ny, nz);
    if (len < 1e-12) continue;
    const ang = Math.acos(Math.abs(nz / len)) * 180 / Math.PI;
    const limit = nz < 0 ? s.bottomAngleLimit : s.topAngleLimit;
    if (limit > 0 && ang <= limit) w[t * 3] = w[t * 3 + 1] = w[t * 3 + 2] = 1;
  }
  return w;
}

function writeBinarySTL(path, pos) {
  const n = pos.length / 9, buf = Buffer.alloc(84 + n * 50);
  buf.write('BumpMesh CLI', 0, 'ascii');
  buf.writeUInt32LE(n, 80);
  let o = 84;
  for (let t = 0; t < n; t++) {
    const i = t * 9;
    const ux = pos[i + 3] - pos[i], uy = pos[i + 4] - pos[i + 1], uz = pos[i + 5] - pos[i + 2];
    const vx = pos[i + 6] - pos[i], vy = pos[i + 7] - pos[i + 1], vz = pos[i + 8] - pos[i + 2];
    let nx = uy * vz - uz * vy, ny = uz * vx - ux * vz, nz = ux * vy - uy * vx;
    const len = Math.hypot(nx, ny, nz) || 1;
    for (const v of [nx / len, ny / len, nz / len]) { buf.writeFloatLE(v, o); o += 4; }
    for (let v = 0; v < 9; v++) { buf.writeFloatLE(pos[i + v], o); o += 4; }
    o += 2;
  }
  writeFileSync(path, buf);
}

async function texturize(inPath, outPath, img) {
  const t0 = performance.now();
  const geometry = loadSTL(inPath);
  geometry.computeBoundingBox();
  const bb = geometry.boundingBox;
  const size = new THREE.Vector3().subVectors(bb.max, bb.min);
  const bounds = { min: bb.min.clone(), max: bb.max.clone(), size, center: new THREE.Vector3().addVectors(bb.min, bb.max).multiplyScalar(0.5) };
  const minDim = Math.min(size.x, size.y, size.z);

  const settings = {
    mappingMode: MAPPING[params.mapping],
    scaleU: params.tile, scaleV: params.tile, lockScale: true,
    textureHeight: params.depth,
    amplitude: (opt.invert ? -1 : 1) * params.depth,
    invertDisplacement: !!opt.invert, invertTexture: false,
    offsetU: 0, offsetV: 0, rotation: 0,
    refineLength: refine, maxTriangles: maxTris,
    bottomAngleLimit: num(opt['bottom-angle'], 'bottom-angle') ?? 5,
    topAngleLimit: num(opt['top-angle'], 'top-angle') ?? 0,
    mappingBlend: 1, seamBandWidth: 0.5, textureSmoothing: 0,
    blendNormalSmoothing: 32, capAngle: 20,
    boundaryFalloff: 0, boundaryFalloffCurve: 'ease',
    symmetricDisplacement: !!opt.symmetric, noDownwardZ: false,
    smoothBottom: true, harvestFlatFaces: true, harvestTol: 0.005,
    preserveUntextured: true, snapSeamlessWrap: true,
    cylinderCenterX: null, cylinderCenterY: null, cylinderRadius: null,
    regularizeEnabled: true, regularizeAspectThreshold: 5, regularizeSlack: 3.0,
    regularizeAggressiveSlack: 8.0, regularizeExtremeAspect: 8,
    regularizeNormalDeg: 15, regularizeAggressiveNormalDeg: 25, regularizeSecondPassMul: 1.1,
  };

  const warnings = [];
  if (params.depth > minDim * 0.1) warnings.push(`relieve ${params.depth} mm supera el 10% de la medida menor (${minDim.toFixed(1)} mm): puede deformar la pieza`);
  if (params.depth < 0.2) warnings.push(`relieve ${params.depth} mm: con boquilla de ${nozzle} mm puede no verse`);

  const result = await runExportPipeline({
    positions: geometry.attributes.position.array,
    faceWeights: faceWeightsFor(geometry, settings),
    imageData: img, imgWidth: img.width, imgHeight: img.height,
    settings, bounds,
    regularizeOpts: {
      aspectThreshold: settings.regularizeAspectThreshold,
      slack: settings.regularizeSlack, aggressiveSlack: settings.regularizeAggressiveSlack,
      extremeSliverAspect: settings.regularizeExtremeAspect,
      maxNormalDeltaCos: Math.cos(settings.regularizeNormalDeg * Math.PI / 180),
      aggressiveNormalDeltaCos: Math.cos(settings.regularizeAggressiveNormalDeg * Math.PI / 180),
    },
    mode: 'export',
  });

  if (result.safetyCapHit) warnings.push('se alcanzó el límite de subdivisión de BumpMesh: sube --refine');
  const rs = result.repairStats;
  if (rs && (rs.open || rs.nonManifold)) warnings.push(`malla con defectos: ${rs.open} bordes abiertos, ${rs.nonManifold} no-manifold`);

  writeBinarySTL(outPath, result.positions);
  const secs = ((performance.now() - t0) / 1000).toFixed(1);
  console.log(`✓ ${basename(inPath)} → ${outPath}  (${result.positions.length / 9} triángulos, ${secs} s)`);
  for (const w of warnings) console.log(`  ⚠ ${w}`);
}

// ── Entrada única o carpeta ────────────────────────────────────────────────────
const img = decodePNG(texturePath(params.texture));
console.log(`Textura ${params.texture} · ${params.mapping} · mosaico ${params.tile} mm · relieve ${params.depth} mm · arista ${refine.toFixed(2)} mm`);

const inPath = resolve(opt.in);
let jobs;
if (statSync(inPath).isDirectory()) {
  const outDir = resolve(opt.out ?? join(inPath, 'texturizado'));
  mkdirSync(outDir, { recursive: true });
  jobs = readdirSync(inPath).filter(f => extname(f).toLowerCase() === '.stl')
    .map(f => [join(inPath, f), join(outDir, f)]);
  if (!jobs.length) { console.error(`No hay STL en ${inPath}`); process.exit(1); }
} else {
  jobs = [[inPath, resolve(opt.out ?? inPath.replace(/\.stl$/i, '') + '_textura.stl')]];
}

let failed = 0;
for (const [src, dst] of jobs) {
  try { await texturize(src, dst, img); }
  catch (e) { failed++; console.error(`✗ ${basename(src)}: ${e.message}`); }
}
process.exit(failed ? 1 : 0);
