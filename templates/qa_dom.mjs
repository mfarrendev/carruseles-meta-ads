#!/usr/bin/env node
/**
 * qa_dom.mjs — validación sobre el DOM RENDERIZADO (3-ago-2026).
 *
 * Idea importada del validador de guizang-social-card-skill (medir el DOM real en vez de
 * píxeles). ESE validador es AGPL: esto es una REIMPLEMENTACIÓN desde cero sobre las
 * reglas de ESTA skill — no hay código copiado.
 *
 * Lo que mide, por cada s-NN.html (sobre el lienzo YA renderizado; la altura real la lee
 * del DOM — 1080×1350 por defecto desde la oleada 2.5A, 1080×1080 en specs "canvas":"1:1"):
 *   FAIL · overflow        scrollHeight/scrollWidth > clientHeight/clientWidth de .slide
 *   FAIL · colision_chrome texto/media invadiendo la banda del chrome fijo (.logo/.swipe/CTA fijo)
 *   FAIL · piso_fuente     texto visible bajo 26px (mismo piso que qa_typesize / constantes.PISO_ABSOLUTO)
 *   FAIL · solape          dos elementos texto/badge/pastilla/CTA/logo montados (>4px) — regla de
 *                          qa_geom (T6) medida con getBoundingClientRect(), no parseando HTML
 *   FAIL · aire_pastilla   pastilla a <12px de un texto (constantes.GAP_MIN / RUBRIC E9)
 *   FAIL · desborde_pastilla texto más ancho/alto que su pastilla (scrollWidth/Height > client)
 *   WARN · gap_titulo      titular pegado al bloque siguiente (<16px)
 *   WARN · densidad        banda vacía (de 4) o hueco >25% de la altura entre bloques
 *
 * Salida: UN JSON por stdout {slides:[{slide, fails:[], warns:[]}]}. Exit 0 si corrió,
 * 3 si falta playwright (verify.py lo reporta como WARN declarado, nunca pass silencioso).
 *
 * Uso: node qa_dom.mjs s-01.html s-02.html ...
 */
import { createRequire } from 'node:module';
import { pathToFileURL } from 'node:url';
import path from 'node:path';

const require = createRequire(import.meta.url);

let chromium;
try {
  ({ chromium } = require('playwright'));
} catch {
  console.log(JSON.stringify({ error: 'no_playwright' }));
  process.exit(3);
}

const PISO_FUENTE = 26;   // constantes.PISO_ABSOLUTO — misma cifra que qa_typesize
const GAP_MIN = 16;       // aire mínimo titular → contenido
const BANDAS = 4;
const HUECO_MAX = 0.25;   // fracción de la altura de la slide

const archivos = process.argv.slice(2);
if (!archivos.length) {
  console.error('uso: node qa_dom.mjs s-*.html');
  process.exit(2);
}

const MEDIR = `([PISO, GAPMIN, NBANDAS, HUECOMAX]) => {
  const slide = document.querySelector('.slide') || document.body;
  const W = slide.clientWidth, H = slide.clientHeight;
  const fails = [], warns = [];
  const rectOf = el => el.getBoundingClientRect();
  const visible = el => {
    const cs = getComputedStyle(el);
    const r = rectOf(el);
    return cs.display !== 'none' && cs.visibility !== 'hidden' &&
           parseFloat(cs.opacity) > 0 && r.width > 0 && r.height > 0;
  };
  const textoDirecto = el => [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
  const okSmall = el => el.closest('.ok-small, [data-ok-small]');
  const cruza = (a, b, pad = 0) =>
    a.left < b.right + pad && a.right > b.left - pad && a.top < b.bottom + pad && a.bottom > b.top - pad;

  // ── 1 · overflow real del contenedor de slide ─────────────────────────
  const dx = slide.scrollWidth - slide.clientWidth;
  const dy = slide.scrollHeight - slide.clientHeight;
  if (dy > 2 || dx > 2) {
    let culpable = '';
    let peor = 0;
    for (const el of slide.querySelectorAll('*')) {
      if (!visible(el)) continue;
      const r = rectOf(el);
      // el texto en nowrap desborda el contenido sin ensanchar la caja del div:
      // por eso también se mide scrollWidth/scrollHeight del propio elemento
      const exceso = Math.max(r.bottom - H, r.right - W,
                              el.scrollWidth - el.clientWidth, el.scrollHeight - el.clientHeight);
      if (exceso > peor) { peor = exceso; culpable = el.className || el.tagName; }
    }
    fails.push({ rule: 'overflow',
      detalle: 'desborda ' + Math.max(dx, dy) + 'px (' +
        (dy > 2 ? 'alto +' + dy + 'px' : '') + (dy > 2 && dx > 2 ? ' · ' : '') +
        (dx > 2 ? 'ancho +' + dx + 'px' : '') + ')' +
        (culpable ? ' · lo empuja «' + String(culpable).split(' ')[0] + '»' : '') +
        ' · fix: bajar el font-size del bloque que desborda, acortar el copy o subir el bloque' });
  }

  // ── 2 · colisión con el chrome fijo (logo / swipe / CTA fijo) ─────────
  const chrome = [...slide.querySelectorAll('.logo, .swipe, [class*="pagin"]')];
  // una pastilla CTA solo es chrome si NO vive dentro del flujo de texto (.text)
  for (const cta of slide.querySelectorAll('.cta')) {
    if (!cta.closest('.text') && getComputedStyle(cta).position !== 'static') chrome.push(cta);
  }
  for (const ch of chrome) {
    if (!visible(ch)) continue;
    const rCh = rectOf(ch);
    for (const el of slide.querySelectorAll('*')) {
      if (el === ch || ch.contains(el) || el.contains(ch)) continue;
      if (!visible(el) || !textoDirecto(el)) continue;
      if (cruza(rectOf(el), rCh, 4)) {
        const nombre = (el.className || el.tagName).toString().split(' ')[0];
        const chNom = (ch.className || ch.tagName).toString().split(' ')[0];
        fails.push({ rule: 'colision_chrome',
          detalle: '«' + nombre + '» invade la banda de «' + chNom + '» (' +
            Math.round(rectOf(el).top) + '–' + Math.round(rectOf(el).bottom) +
            'px vs chrome ' + Math.round(rCh.top) + '–' + Math.round(rCh.bottom) +
            'px) · fix: bajar/mover el bloque de texto o reubicar el chrome' });
      }
    }
  }

  // ── 3 · piso de fuente computado (texto visible < 26px) ───────────────
  const textos = [];
  for (const el of slide.querySelectorAll('*')) {
    if (!visible(el) || !textoDirecto(el) || okSmall(el)) continue;
    const px = parseFloat(getComputedStyle(el).fontSize);
    if (px < PISO) {
      const nom = (el.className || el.tagName).toString().split(' ')[0];
      fails.push({ rule: 'piso_fuente',
        detalle: '«' + nom + '» a ' + px + 'px < ' + PISO + 'px computados · fix: subir el ' +
          'tamaño o marcar /*ok-small*/ si es decorativo' });
    }
    textos.push({ el, r: rectOf(el), px });
  }

  // ── 4 · gap titular → contenido (<16px = pegado) ──────────────────────
  const titulo = slide.querySelector('.title, h1');
  if (titulo && visible(titulo)) {
    const rT = rectOf(titulo);
    let siguiente = null;
    for (const cand of slide.querySelectorAll('.body, .sub, .cta, .bubs')) {
      if (!visible(cand) || titulo.contains(cand) || cand.contains(titulo)) continue;
      const r = rectOf(cand);
      if (r.top >= rT.bottom - 2 && (!siguiente || r.top < siguiente.top)) siguiente = r;
    }
    if (siguiente) {
      const gap = Math.round(siguiente.top - rT.bottom);
      if (gap < GAPMIN) warns.push({ rule: 'gap_titulo',
        detalle: 'titular pegado al contenido (' + gap + 'px < ' + GAPMIN +
          'px) · fix: margin-bottom del título' });
    }
  }

  // ── 5 · densidad por bandas (WARN — se satisface con contenido, nunca ornamento) ──
  const contenido = [];
  for (const t of textos) contenido.push(t.r);
  for (const m of slide.querySelectorAll('img, video')) {
    if (!visible(m) || m.classList.contains('photo')) continue;   // la foto de fondo no cuenta
    const r = rectOf(m);
    if (r.width >= W * 0.95 && r.height >= H * 0.95) continue;    // full-bleed tampoco
    contenido.push(r);
  }
  for (let b = 0; b < NBANDAS; b++) {
    const y0 = (H / NBANDAS) * b, y1 = (H / NBANDAS) * (b + 1);
    const hay = contenido.some(r => r.top < y1 && r.bottom > y0);
    if (!hay) warns.push({ rule: 'densidad',
      detalle: 'banda ' + (b + 1) + '/' + NBANDAS + ' vacía (' + Math.round(y0) + '–' +
        Math.round(y1) + 'px) · WARN: se acepta con razón, NO se ornamenta para satisfacerlo' });
  }
  const intervalos = contenido.map(r => [r.top, r.bottom]).sort((a, b) => a[0] - b[0]);
  for (let i = 1; i < intervalos.length; i++) {
    const hueco = intervalos[i][0] - intervalos[i - 1][1];
    if (hueco > H * HUECOMAX) warns.push({ rule: 'densidad',
      detalle: 'hueco de ' + Math.round(hueco) + 'px (>' + Math.round(H * HUECOMAX) +
        'px, 25% del alto) entre bloques · WARN: se acepta con razón, NO se ornamenta' });
  }

  // ── 6 · solapes, aire pastilla↔texto y desborde de pastilla (auditoría T6) ──
  // Estas reglas vivían en qa_geom.py, que las medía parseando el HTML con un patrón
  // (class="…" style="left/top…") y unas clases legacy que engine.py NO emite: parseaba
  // 0 elementos y E9/E6 pasaban en falso. Acá se miden rects REALES del DOM renderizado.
  const PILLS = '.badge, .chip, .pill, .bub, .cta';
  const GAP_PASTILLA = 12;    // constantes.GAP_MIN · RUBRIC E9
  const esChromeEl = el => !!el.closest('.logo, .swipe, [class*="pagin"]') ||
    (el.matches('.cta') && !el.closest('.text') && getComputedStyle(el).position !== 'static');
  const nomCorto = el => (el.className || el.tagName).toString().split(' ')[0];
  // ¿son dos inlines que el navegador repartió dentro del MISMO bloque de texto?
  const bloqueDe = el => { let n = el.parentElement;
    while (n && getComputedStyle(n).display.startsWith('inline')) n = n.parentElement;
    return n; };
  const mismoBloqueInline = (a, b) =>
    getComputedStyle(a).display.startsWith('inline') &&
    getComputedStyle(b).display.startsWith('inline') &&
    bloqueDe(a) && bloqueDe(a) === bloqueDe(b);
  const piezas = [];
  const enPiezas = new Set();
  for (const t of textos) { piezas.push({ el: t.el, r: t.r, pill: t.el.matches(PILLS) }); enPiezas.add(t.el); }
  for (const p of slide.querySelectorAll(PILLS + ', .logo')) {
    if (enPiezas.has(p) || !visible(p)) continue;
    piezas.push({ el: p, r: rectOf(p), pill: p.matches(PILLS) });
  }
  // 6a · texto desbordando su pastilla (la caja es más chica que el contenido)
  for (const p of piezas) {
    if (!p.pill) continue;
    const ddx = p.el.scrollWidth - p.el.clientWidth, ddy = p.el.scrollHeight - p.el.clientHeight;
    if (ddx > 2 || ddy > 2) fails.push({ rule: 'desborde_pastilla',
      detalle: '«' + nomCorto(p.el) + '» desborda su pastilla +' + Math.max(ddx, ddy) +
        'px · fix: quitar el width/height fijo de la pastilla o acortar su texto' });
  }
  // 6b/6c · solapes y aire pastilla↔texto
  for (let i = 0; i < piezas.length; i++) {
    for (let j = i + 1; j < piezas.length; j++) {
      const a = piezas[i], b = piezas[j];
      if (a.el.contains(b.el) || b.el.contains(a.el)) continue;
      // Dos FRAGMENTOS INLINE del mismo bloque no colisionan: los reparte el navegador en
      // flujo. Con line-height:1.04 la caja em de la fuente (ascent+descent ≈ 1.2em) es más
      // alta que la línea, así que los rects de dos <em> en renglones seguidos se montan ~7px
      // aunque los glifos no se rocen. Esto salió con la regla de destaque inline del 5-ago
      // (.title em): antes no había inlines marcados y el par no existía. Y el fix que
      // sugería la regla —"mover uno de los dos bloques"— no es ni siquiera accionable, porque
      // no son bloques. Un solape real entre inlines se ve igual, pero entre PADRES distintos.
      if (mismoBloqueInline(a.el, b.el)) continue;
      const ix = Math.min(a.r.right, b.r.right) - Math.max(a.r.left, b.r.left);
      const iy = Math.min(a.r.bottom, b.r.bottom) - Math.max(a.r.top, b.r.top);
      if (ix > 4 && iy > 4) {
        // texto/pastilla ↔ chrome ya lo reporta colision_chrome: no duplicar el hallazgo
        if ((esChromeEl(a.el) || esChromeEl(b.el)) && (textoDirecto(a.el) || textoDirecto(b.el))) continue;
        fails.push({ rule: 'solape',
          detalle: '«' + nomCorto(a.el) + '» × «' + nomCorto(b.el) + '» montados ' +
            Math.round(ix) + '×' + Math.round(iy) + 'px · fix: mover uno de los dos bloques' });
        continue;
      }
      if (a.pill === b.pill) continue;   // el aire de 12px es pastilla↔texto, no pastilla↔pastilla
      const sep = Math.max(Math.max(a.r.left - b.r.right, b.r.left - a.r.right, 0),
                           Math.max(a.r.top - b.r.bottom, b.r.top - a.r.bottom, 0));
      if (sep < GAP_PASTILLA) fails.push({ rule: 'aire_pastilla',
        detalle: 'pastilla «' + nomCorto(a.pill ? a.el : b.el) + '» a ' + Math.round(sep) +
          'px de «' + nomCorto(a.pill ? b.el : a.el) + '» (< ' + GAP_PASTILLA +
          'px de aire, RUBRIC E9) · fix: separar la pastilla del texto' });
    }
  }

  return { fails, warns };
}`;

const medir = (0, eval)(MEDIR);   // string → función real: evaluate(string) NO la invoca con args

const browser = await chromium.launch();
const out = { slides: [] };
try {
  // Viewport holgado en altura: las bandas y el hueco se miden contra slide.clientHeight,
  // así que el lienzo real (1350 por defecto, 1080 en 1:1) manda, no el viewport.
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const f of archivos) {
    const url = pathToFileURL(path.resolve(f)).href;
    try {
      await page.goto(url, { waitUntil: 'networkidle', timeout: 20000 });
      const r = await page.evaluate(medir, [PISO_FUENTE, GAP_MIN, BANDAS, HUECO_MAX]);
      out.slides.push({ slide: path.basename(f), ...r });
    } catch (e) {
      out.slides.push({ slide: path.basename(f),
        fails: [{ rule: 'render', detalle: 'no se pudo renderizar: ' + String(e).slice(0, 120) }],
        warns: [] });
    }
  }
} finally {
  await browser.close();
}
console.log(JSON.stringify(out));
