// Lectura y escritura de 3MF sin dependencias: un 3MF es un zip con un XML de mallas.
// Lee varios objetos por archivo (las placas que exporta Bambu Studio u otro programa)
// y escribe una placa con varias figuras ya ubicadas, que Bambu Studio abre tal cual.
import fs from 'node:fs';
import zlib from 'node:zlib';

// --- zip ---------------------------------------------------------------------

const TABLA_CRC = (() => {
  const t = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    t[n] = c >>> 0;
  }
  return t;
})();

function crc32(buf) {
  let c = 0xffffffff;
  for (let i = 0; i < buf.length; i++) c = TABLA_CRC[(c ^ buf[i]) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}

function leerZip(buf) {
  let fin = -1;
  for (let i = buf.length - 22; i >= Math.max(0, buf.length - 65557); i--) {
    if (buf.readUInt32LE(i) === 0x06054b50) { fin = i; break; }
  }
  if (fin < 0) throw new Error('no es un zip/3MF válido');
  const n = buf.readUInt16LE(fin + 10);
  let p = buf.readUInt32LE(fin + 16);
  const archivos = new Map();
  for (let k = 0; k < n; k++) {
    if (buf.readUInt32LE(p) !== 0x02014b50) throw new Error('directorio del zip dañado');
    const metodo = buf.readUInt16LE(p + 10);
    const tam = buf.readUInt32LE(p + 20);
    const ln = buf.readUInt16LE(p + 28), le = buf.readUInt16LE(p + 30), lc = buf.readUInt16LE(p + 32);
    const local = buf.readUInt32LE(p + 42);
    const nombre = buf.toString('utf8', p + 46, p + 46 + ln);
    const ini = local + 30 + buf.readUInt16LE(local + 26) + buf.readUInt16LE(local + 28);
    const datos = buf.subarray(ini, ini + tam);
    archivos.set(nombre, () => (metodo === 8 ? zlib.inflateRawSync(datos) : metodo === 0 ? datos : (() => {
      throw new Error(`compresión ${metodo} no soportada`);
    })()));
    p += 46 + ln + le + lc;
  }
  return archivos;
}

function escribirZip(entradas) {
  const partes = [];
  const central = [];
  let offset = 0;
  for (const { nombre, datos } of entradas) {
    const crudo = Buffer.isBuffer(datos) ? datos : Buffer.from(datos, 'utf8');
    const comp = zlib.deflateRawSync(crudo, { level: 6 });
    const n = Buffer.from(nombre, 'utf8');
    const crc = crc32(crudo);
    const h = Buffer.alloc(30);
    h.writeUInt32LE(0x04034b50, 0); h.writeUInt16LE(20, 4); h.writeUInt16LE(0, 6); h.writeUInt16LE(8, 8);
    h.writeUInt32LE(0, 10); h.writeUInt32LE(crc, 14); h.writeUInt32LE(comp.length, 18); h.writeUInt32LE(crudo.length, 22);
    h.writeUInt16LE(n.length, 26); h.writeUInt16LE(0, 28);
    const c = Buffer.alloc(46);
    c.writeUInt32LE(0x02014b50, 0); c.writeUInt16LE(20, 4); c.writeUInt16LE(20, 6); c.writeUInt16LE(0, 8); c.writeUInt16LE(8, 10);
    c.writeUInt32LE(0, 12); c.writeUInt32LE(crc, 16); c.writeUInt32LE(comp.length, 20); c.writeUInt32LE(crudo.length, 24);
    c.writeUInt16LE(n.length, 28); c.writeUInt32LE(offset, 42);
    partes.push(h, n, comp);
    central.push(c, n);
    offset += 30 + n.length + comp.length;
  }
  const tamCentral = central.reduce((s, b) => s + b.length, 0);
  const e = Buffer.alloc(22);
  e.writeUInt32LE(0x06054b50, 0); e.writeUInt16LE(entradas.length, 8); e.writeUInt16LE(entradas.length, 10);
  e.writeUInt32LE(tamCentral, 12); e.writeUInt32LE(offset, 16);
  return Buffer.concat([...partes, ...central, e]);
}

// --- 3MF ---------------------------------------------------------------------

const atributo = (tag, nombre) => {
  const m = new RegExp(`\\s${nombre}="([^"]*)"`).exec(tag);
  return m ? m[1] : null;
};

function desescapar(s) {
  return s.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&apos;/g, "'").replace(/&amp;/g, '&');
}

// Matriz 3MF "m00 m01 m02 m10 m11 m12 m20 m21 m22 m30 m31 m32": p' = [x y z 1] · M
function matriz(txt) {
  return txt ? txt.trim().split(/\s+/).map(Number) : [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0];
}

function componer(a, b) { // primero a, después b
  const r = new Array(12);
  for (let i = 0; i < 4; i++) {
    for (let j = 0; j < 3; j++) {
      r[i * 3 + j] = a[i * 3] * b[j] + a[i * 3 + 1] * b[3 + j] + a[i * 3 + 2] * b[6 + j] + (i === 3 ? b[9 + j] : 0);
    }
  }
  return r;
}

/**
 * Objetos de un 3MF: [{ nombre, pos, verts, caras }], en mm y en su lugar de la placa.
 * pos = sopa de triángulos (9 números por cara); verts/caras = la misma malla indexada,
 * con los índices del archivo, para volver a escribirla sin tocar su topología.
 */
export function leer3MF(archivo) {
  const zip = leerZip(fs.readFileSync(archivo));
  const ruta = [...zip.keys()].find((k) => /^3D\/[^/]+\.model$/i.test(k));
  if (!ruta) throw new Error('el 3MF no tiene 3D/*.model');
  const xml = zip.get(ruta)().toString('utf8');
  const unidad = atributo(/<model[^>]*>/.exec(xml)?.[0] ?? '', 'unit') || 'millimeter';
  const factor = { micron: 0.001, millimeter: 1, centimeter: 10, inch: 25.4, foot: 304.8, meter: 1000 }[unidad] ?? 1;

  const objetos = new Map();
  for (const m of xml.matchAll(/<object\b([^>]*)>([\s\S]*?)<\/object>/g)) {
    const id = atributo(m[1], 'id');
    const nombre = desescapar(atributo(m[1], 'name') || `objeto_${id}`);
    const cuerpo = m[2];
    const obj = { id, nombre, verts: null, tris: null, componentes: [] };
    const malla = /<mesh>([\s\S]*?)<\/mesh>/.exec(cuerpo);
    if (malla) {
      const v = [];
      for (const t of malla[1].matchAll(/<vertex\b([^>]*)\/?>/g)) v.push(+atributo(t[1], 'x'), +atributo(t[1], 'y'), +atributo(t[1], 'z'));
      const f = [];
      for (const t of malla[1].matchAll(/<triangle\b([^>]*)\/?>/g)) f.push(+atributo(t[1], 'v1'), +atributo(t[1], 'v2'), +atributo(t[1], 'v3'));
      obj.verts = v; obj.tris = f;
    }
    for (const c of cuerpo.matchAll(/<component\b([^>]*)\/?>/g)) {
      obj.componentes.push({ id: atributo(c[1], 'objectid'), m: matriz(atributo(c[1], 'transform')) });
    }
    objetos.set(id, obj);
  }

  // junta la malla indexada de un objeto y sus componentes, ya transformada
  const juntar = (id, M, out) => {
    const o = objetos.get(id);
    if (!o) return;
    if (o.verts) {
      const base = out.verts.length / 3;
      const v = o.verts;
      for (let i = 0; i < v.length; i += 3) {
        const x = v[i], y = v[i + 1], z = v[i + 2];
        out.verts.push((M[0] * x + M[3] * y + M[6] * z + M[9]) * factor, (M[1] * x + M[4] * y + M[7] * z + M[10]) * factor,
          (M[2] * x + M[5] * y + M[8] * z + M[11]) * factor);
      }
      for (const t of o.tris) out.caras.push(t + base);
    }
    for (const c of o.componentes) juntar(c.id, componer(c.m, M), out);
  };

  const items = [...xml.matchAll(/<item\b([^>]*)\/?>/g)].map((m) => ({ id: atributo(m[1], 'objectid'), m: matriz(atributo(m[1], 'transform')) }));
  const lista = items.length ? items : [...objetos.keys()].map((id) => ({ id, m: matriz(null) }));
  const out = [];
  for (const it of lista) {
    const malla = { verts: [], caras: [] };
    juntar(it.id, it.m, malla);
    if (!malla.caras.length) continue;
    const verts = Float64Array.from(malla.verts), caras = Int32Array.from(malla.caras);
    const pos = new Float64Array(caras.length * 3);
    for (let i = 0; i < caras.length; i++) {
      pos[i * 3] = verts[caras[i] * 3]; pos[i * 3 + 1] = verts[caras[i] * 3 + 1]; pos[i * 3 + 2] = verts[caras[i] * 3 + 2];
    }
    out.push({ nombre: objetos.get(it.id).nombre, pos, verts, caras });
  }
  if (!out.length) throw new Error('el 3MF no tiene mallas');
  return out;
}

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const n6 = (x) => {
  const s = x.toFixed(5);
  return s.includes('.') ? s.replace(/0+$/, '').replace(/\.$/, '') : s;
};

/**
 * Escribe una placa: objetos [{ nombre, verts, caras }] (malla indexada, ya ubicada
 * en coordenadas de la cama). Se conservan los índices tal cual: nada se suelda ni
 * se descarta, así una malla cerrada sigue cerrada.
 */
export function escribir3MF(archivo, objetos) {
  const partes = ['<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xml:lang="es-AR" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">\n',
    ' <metadata name="Application">taller-impresion3d orientar</metadata>\n <resources>\n'];
  objetos.forEach((o, k) => {
    partes.push(`  <object id="${k + 1}" name="${esc(o.nombre)}" type="model">\n   <mesh>\n    <vertices>\n`);
    const lv = [];
    for (let i = 0; i < o.verts.length; i += 3) lv.push(`     <vertex x="${n6(o.verts[i])}" y="${n6(o.verts[i + 1])}" z="${n6(o.verts[i + 2])}"/>`);
    partes.push(lv.join('\n'), '\n    </vertices>\n    <triangles>\n');
    const lt = [];
    for (let i = 0; i < o.caras.length; i += 3) lt.push(`     <triangle v1="${o.caras[i]}" v2="${o.caras[i + 1]}" v3="${o.caras[i + 2]}"/>`);
    partes.push(lt.join('\n'), '\n    </triangles>\n   </mesh>\n  </object>\n');
  });
  partes.push(' </resources>\n <build>\n');
  objetos.forEach((o, k) => partes.push(`  <item objectid="${k + 1}"/>\n`));
  partes.push(' </build>\n</model>\n');
  const zip = escribirZip([
    { nombre: '[Content_Types].xml', datos: '<?xml version="1.0" encoding="UTF-8"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>\n' },
    { nombre: '_rels/.rels', datos: '<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>\n' },
    { nombre: '3D/3dmodel.model', datos: Buffer.from(partes.join(''), 'utf8') },
  ]);
  fs.writeFileSync(archivo, zip);
}
