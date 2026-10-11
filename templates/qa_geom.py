#!/usr/bin/env python3
"""
qa_geom.py — GEOM GATE (director creativo, 8-jul-2026). Cierra 2 bugs que MAPCHECK/typesize NO ven:
  (1) texto que se SALE de su pastilla/badge/CTA;
  (2) un elemento que CHOCA con otro (título sobre una pastilla, etc.).

⚠️ LEGACY (3-ago-2026, auditoría T6): este parser exige el patrón `class="…" style="…"`
con clases de una lista fija (badge/h/lead/cta…) que el motor canónico `engine.py` NO emite
— engine escribe `<div class="title" style="font-size:…">` dentro de un bloque `.text`, sin
left/top inline. Resultado: sobre la salida del motor parseaba 0 elementos y devolvía PASS
sin medir nada. Las reglas de solape, aire pastilla↔texto y texto-fuera-de-pastilla se
MOVIÉRON a `qa_dom.mjs`, que las mide con getBoundingClientRect() sobre el DOM renderizado.
Esto queda SOLO para builds antiguos (HTML con clases badge/h/lead y left/top inline); sobre
cualquier otro HTML FALLA con "0 elementos revisados" en vez de pasar en falso.

Determinista, sin navegador: parsea el HTML final, y con métricas de fuente (Pillow) calcula
el rect REAL de cada elemento — ancho real de las pastillas (getlength del texto + padding) y
alto real de los bloques de texto (word-wrap al ancho de su caja). Luego: FALLA si algo sale del
área segura o si dos rects se solapan.

Uso: python3 qa_geom.py slide1.html slide2.html ...   (exit 1 si algo falla)
Nota: las pastillas (badge/chip) deben ir con SOLO left/top (auto-ancho); si el HTML les fija un
      width menor al texto, se reporta 'texto fuera de pastilla'.
"""
import re, sys, os, html as _html
from PIL import ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import montwidth as _mw
except Exception:
    _mw = None

CANVAS = 1080
MARGIN = 40
TOL = 8
EDGE_OK = {'logo', 'pag'}
_WOFF2 = None   # set por archivo en main(): mide Montserrat REAL por peso (no el proxy Arial)
# line-height por clase (coincide con el CSS del builder)
LH = {'h': 1.06, 'lead': 1.36, 'small': 1.4, 'micro': 1.2, 'ctaline': 1.3, 'badge': 1.0, 'cta': 1.0}
# padding horizontal total + extras por tipo de pastilla
PILL = {'badge': dict(padx=48, extra=19),   # padding 24*2 + dot(9)+gap(10)
        'cta':   dict(padx=56, extra=54),    # padding 28*2 + arrow(40)+gap(14)
        'chip':  dict(padx=40, extra=0)}

def _font(size):
    for p in ('/System/Library/Fonts/Supplemental/Arial.ttf',
              '/System/Library/Fonts/Helvetica.ttc',
              '/Library/Fonts/Arial.ttf'):
        try: return ImageFont.truetype(p, size)
        except OSError: continue
    return ImageFont.load_default()

def _text_w(size, text, tracking_em=0.0, weight=700):
    # Montserrat REAL por peso si hay woff2 del proyecto; si no, proxy Arial*1.06 (peor pero sirve)
    if _WOFF2 and _mw and _mw.available():
        return _mw.width(text, size, _WOFF2, weight, tracking_em)
    f = _font(size)
    w = f.getlength(text)
    if tracking_em and len(text) > 1:
        w += tracking_em * size * (len(text) - 1)
    return w * 1.06

def _strip(inner):
    inner = inner.replace('<br>', '\n')
    inner = re.sub(r'<[^>]+>', '', inner)
    return _html.unescape(inner).strip()

def _num(style, key, default=None):
    m = re.search(rf'{key}\s*:\s*(-?[\d.]+)px', style)
    return float(m.group(1)) if m else default

def parse(html_path):
    html = open(html_path, encoding='utf-8').read()
    html = re.sub(r'<span class="dot"></span>', '', html)
    html = re.sub(r'<span class="arw">.*?</span>', '', html)
    els = []
    for m in re.finditer(r'<(?:div|span)\s+class="([a-z][\w-]*)[^"]*"\s+style="([^"]*)">(.*?)</(?:div|span)>', html, re.S):
        cls, style, inner = m.group(1), m.group(2), m.group(3)
        if cls not in ('badge','h','lead','small','micro','chips','chat','cta','ctab','ctaline','logo','pag'):
            continue
        x = _num(style, 'left'); y = _num(style, 'top')
        w = _num(style, 'width')
        if x is None or y is None:
            continue
        size = _num(style, 'font-size', {'h':80,'lead':36,'small':28,'micro':30,'cta':32,'ctab':112,'ctaline':32,
                                         'badge':28,'chips':30}.get(cls, 30))
        txt = _strip(inner)
        els.append(dict(c=cls, x=x, y=y, w=w, size=size, style=style, text=txt, inner=inner))
    # <img class="logo"> (es img, no div) — clave para cazar choques badge/texto ↔ logo
    for m in re.finditer(r'<img\s+class="(logo)[^"]*"\s+src="[^"]*"\s+style="([^"]*)"', html):
        style = m.group(2); x=_num(style,'left'); y=_num(style,'top')
        if x is None or y is None: continue
        h=_num(style,'height',46) or 46; w=_num(style,'width')
        if w is None: w = h*3.745  # aspecto del wordmark de la marca (320.2×85.5)
        els.append(dict(c='logo', x=x, y=y, w=w, size=0, style=style, text='(logo)'))
    return els

def rects(els):
    out, fails = [], []
    for e in els:
        c, x, y, w, size, txt = e['c'], e['x'], e['y'], e['w'], e['size'], e['text']
        if c in ('badge', 'cta', 'chip'):
            up = txt.upper() if 'uppercase' in e['style'] or c == 'badge' else txt
            tw = _text_w(size, up, tracking_em=0.14 if c == 'badge' else 0.0)
            p = PILL[c]
            need = p['padx'] + p['extra'] + tw
            rw = need if w is None else w
            if w is not None and need > w + TOL:
                fails.append(f"TEXTO FUERA DE PASTILLA {c} '{txt}' (necesita {need:.0f}px, caja {w:.0f}px)")
            rh = size * 1.0 + 28
            out.append(dict(c=c, t=txt, x=x, y=y, w=rw, h=rh))
        elif c in ('logo', 'pag'):
            rw = w if w else 340
            out.append(dict(c=c, t=txt, x=x, y=y, w=rw, h=(size*1.2 if c=='pag' else 46)))
        elif c == 'chat':
            # alto REAL de la tarjeta: header + burbujas (word-wrap al ancho útil)
            bubs = re.findall(r'class="bub [uc]">(.*?)</div>', e.get('inner',''), re.S)
            hh = 50 + 12 + 42  # avatar/header + margen + padding vertical
            if 'chat__hd' in e.get('inner','') and 'span' in e.get('inner',''): hh += 34  # subtítulo del header
            bw = (w or 400) - 44
            for btxt in bubs:
                bt = _strip(btxt); lines = 0; cur = ''
                for wd in bt.split(' '):
                    t2 = (cur+' '+wd).strip()
                    if _text_w(29, t2) <= bw*0.88 or not cur: cur = t2
                    else: lines += 1; cur = wd
                lines += 1
                hh += lines*37 + 27 + 10
            out.append(dict(c=c, t=txt[:22], x=x, y=y, w=w or 400, h=hh))
        elif c == 'chips':
            out.append(dict(c=c, t=txt, x=x, y=y, w=w or 400, h=None))
        elif c == 'ctab':   # CTA grande (título+precio): caja fija declarada por el builder
            hh = _num(e['style'], 'height', 162) or 162
            out.append(dict(c=c, t=txt or 'CTA', x=x, y=y, w=w or 520, h=hh))
        elif c == 'h':      # TÍTULO: cada tramo se envuelve a SU peso (light 350 / bold 800)
            inner = e.get('inner', '')
            mb = re.search(r'<b\b[^>]*>(.*?)</b>', inner, re.S)
            light_html = inner[:mb.start()] if mb else inner
            bold_html = mb.group(1) if mb else ''
            def _seglines(seg_html, weight):
                seg = _html.unescape(re.sub(r'<[^>]+>', '', seg_html.replace('<br>', '\n'))).strip()
                n = 0
                for para in seg.split('\n'):
                    if para == '':
                        continue
                    cur = ''
                    for wd in para.split(' '):
                        test = (cur + ' ' + wd).strip()
                        if _text_w(size, test, weight=weight) <= (w or CANVAS) or not cur:
                            cur = test
                        else:
                            n += 1; cur = wd
                    n += 1
                return n
            lines = _seglines(light_html, 350) + _seglines(bold_html, 800)
            out.append(dict(c=c, t=txt, x=x, y=y, w=w or 200, h=lines * size * LH['h']))
        else:  # bloques de texto: alto real por word-wrap
            lh = LH.get(c, 1.3)
            lines = 0
            for para in txt.split('\n'):
                words = para.split(' ') or ['']
                cur = ''
                for wd in words:
                    test = (cur + ' ' + wd).strip()
                    if _text_w(size, test) <= (w or CANVAS) or not cur:
                        cur = test
                    else:
                        lines += 1; cur = wd
                lines += 1
            rh = lines * size * lh
            out.append(dict(c=c, t=txt, x=x, y=y, w=w or 200, h=rh))
    return out, fails

def check(rlist, extra_fails):
    fails = list(extra_fails)
    for r in rlist:
        if r['h'] is None or r['w'] <= 0: continue
        if r['c'] not in EDGE_OK:
            if (r['x'] < MARGIN-TOL or r['y'] < MARGIN-TOL
                    or r['x']+r['w'] > CANVAS-MARGIN+TOL or r['y']+r['h'] > CANVAS-MARGIN+TOL):
                fails.append(f"FUERA DE ÁREA {r['c']} '{r['t']}' → ({r['x']:.0f},{r['y']:.0f},{r['x']+r['w']:.0f},{r['y']+r['h']:.0f})")
    for i in range(len(rlist)):
        for j in range(i+1, len(rlist)):
            a, b = rlist[i], rlist[j]
            if a['h'] is None or b['h'] is None: continue
            if {a['c'], b['c']} <= {'logo', 'pag'}: continue
            ix = min(a['x']+a['w'], b['x']+b['w']) - max(a['x'], b['x'])
            iy = min(a['y']+a['h'], b['y']+b['h']) - max(a['y'], b['y'])
            pills={'badge','cta','chip'}; texts={'h','lead','small','micro','ctaline'}
            near = ({a['c'],b['c']} & pills) and ({a['c'],b['c']} & texts)
            lim = -12 if near else TOL   # pastilla↔texto: exigir 12px de aire; resto: solape estricto
            if ix > lim and iy > lim:
                rel = 'CHOCA/MUY CERCA' if near and (ix<=TOL or iy<=TOL) else 'SOLAPE'
                fails.append(f"{rel} {a['c']}'{a['t']}' × {b['c']}'{b['t']}' ({ix:.0f}×{iy:.0f}px)")
    return fails

def _find_woff2(html_path):
    d = os.path.dirname(os.path.abspath(html_path))
    for base in (d, os.path.dirname(d)):
        cand = os.path.join(base, 'assets', 'montserrat-var.woff2')
        if os.path.exists(cand):
            return cand
    return None

def main(paths):
    global _WOFF2
    bad = False
    for p in paths:
        _WOFF2 = _find_woff2(p)
        els = parse(p)
        if not els:
            # PISO DE CORDURA (auditoría T9): 0 elementos parseados sobre un archivo que
            # existe = la compuerta NO midió nada. Eso es FAIL, no PASS. Casi siempre es
            # HTML del motor canónico (sin clases legacy): sus reglas viven en qa_dom.mjs.
            print(f"{os.path.basename(p)}: FAIL\n   ✗ 0 elementos revisados: la compuerta "
                  f"no midió nada (¿HTML de engine.py? sus reglas de solape/pastilla las "
                  f"mide qa_dom.mjs sobre el DOM real)")
            bad = True
            continue
        r, ef = rects(els)
        f = check(r, ef)
        print(f"{os.path.basename(p)}: {'PASS' if not f else 'FAIL'}" + ''.join(f"\n   ✗ {x}" for x in f))
        if f: bad = True
    print('GEOM:', 'FAIL' if bad else 'PASS')
    return 1 if bad else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
