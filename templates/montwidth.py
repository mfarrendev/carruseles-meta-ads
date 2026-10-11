#!/usr/bin/env python3
"""
montwidth.py — ancho REAL del texto en la fuente del render (variable font, POR PESO).
Motivo (bug real, yoga-s4, 8-jul-2026): el builder medía el wrap con Arial (proxy) pero el CSS
renderiza Montserrat. Montserrat es más ancha — y la NEGRITA (wght 800) más aún — así que una
línea que el builder creyó de 1 renglón se RE-PARTE en el navegador → el título queda más alto de
lo calculado → "empieza hoy" cae encima del CTA. Ni el builder ni el GEOM lo veían (ambos Arial).

Fix: medir con la MISMA .woff2/.ttf del CSS, instanciada al PESO real de cada tramo (light 350 vs
bold 800). Requiere fontTools + brotli (para .woff2). Si no están, `available()` devuelve False y el
que llama cae a su proxy Arial.

API:
  available() -> bool
  width(text, size_px, font_path, weight=400, tracking_em=0.0) -> float (px al tamaño pedido)
"""
import os
from functools import lru_cache

try:
    from fontTools.ttLib import TTFont
    from fontTools.varLib.instancer import instantiateVariableFont
    _OK = True
except Exception:
    _OK = False


def available():
    return _OK


@lru_cache(maxsize=64)
def _advances(font_path, weight):
    """{codepoint: advance/upm} instanciando el variable font al peso pedido. Cacheado."""
    f = TTFont(font_path)
    if 'fvar' in f:
        axes = {a.axisTag: (a.minValue, a.maxValue) for a in f['fvar'].axes}
        if 'wght' in axes:
            lo, hi = axes['wght']
            w = max(lo, min(hi, weight))
            try:
                instantiateVariableFont(f, {'wght': w}, inplace=True)
            except Exception:
                pass
    cmap = f.getBestCmap()
    hmtx = f['hmtx']
    upm = f['head'].unitsPerEm or 1000
    adv = {cp: hmtx[g][0] / upm for cp, g in cmap.items() if g in hmtx.metrics}
    f.close()
    return adv


def width(text, size_px, font_path, weight=400, tracking_em=0.0):
    if not _OK or not text:
        # proxy grosero si no hay fontTools: ~0.55*size por glifo
        return len(text) * size_px * 0.55
    adv = _advances(os.path.abspath(font_path), int(weight))
    fb = adv.get(ord('x'), 0.5)  # glifo ausente en un subset → ancho medio
    tot = sum(adv.get(ord(ch), fb) for ch in text) * size_px
    if tracking_em and len(text) > 1:
        tot += tracking_em * size_px * (len(text) - 1)
    return tot


def measurer(font_path, weight=400, tracking_em=0.0):
    """Devuelve f(text, size)->px, útil para pasarlo a textfit.balance_lines."""
    def m(text, size):
        return width(text, size, font_path, weight, tracking_em)
    return m
