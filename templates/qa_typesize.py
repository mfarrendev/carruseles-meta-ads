#!/usr/bin/env python3
"""
qa_typesize.py — PISO TIPOGRÁFICO determinista (director creativo, 8-jul-2026; reincidencia = tolerancia cero).

qa_lint.py NO ve los font-size inline de los builders custom → este lint SÍ: escanea TODOS los
`font-size:*px` del HTML final (inline + <style>) y FALLA si alguno queda bajo el piso.
Correr SIEMPRE antes de mostrar cualquier pieza: `python3 qa_typesize.py slide1.html ...`

Pisos en lienzo 1080 (se ve en iPhone dentro del feed):
  - FLOOR absoluto: 26px — NINGÚN texto visible por debajo (burbujas, metas, captions incluidos).
    Excepción consciente: marcar `/*ok-small*/` en la MISMA declaración (p.ej. texto decorativo).
  - Héroe: el conjunto debe tener >=1 texto >=90px (título que domina).
  - E5 salto de escala (3-ago-2026, auditoría T4): el título mayor del carrusel debe llegar a
    T_XL (104px) y saltar sobre la escala del resto. Antes "lo medía" qa_lint buscando
    `class="title t-xl"` — una clase que engine.py NUNCA emite (`<div class="title"
    style="font-size:…">`), así que E5 figuraba como medido y nadie lo medía.
    FAIL si el título mayor < T_XL **y** no hay salto (ratio título mayor / mediana de
    títulos < 1.6). Las dos condiciones juntas, no por separado: un carrusel con héroe t-xl
    y secundarios cercanos (120/92 = ratio 1.3) es una decisión de diseño válida que ya pasa
    el gold-standard; lo que E5 castiga es el carrusel PLANO Y CHICO (todo al mismo tamaño,
    bajo t-xl).
Recordatorio no-determinista (lo juzga el ojo): cuerpo/lead >=36 · CTA >=32 · badge >=27.

El piso del héroe (90) es la MISMA cifra que declaran RUBRIC E3/E5/E8 y
references/composicion-y-tipografia.md §4.2. Si se cambia acá, se cambia en los tres.

Modos:
  qa_typesize.py s-*.html              carrusel completo: piso POR SLIDE + héroe y E5 POR CARRUSEL
  qa_typesize.py --slide s-03.html     una sola: solo piso (omite héroe y E5, son por carrusel)
  qa_typesize.py --hero-only s-*.html  solo los chequeos POR CARRUSEL (héroe + E5), sin el piso
                                       (lo usa verify.py gates --only: re-corre el piso de la
                                       slide tocada y, aparte, héroe+E5 sobre el set completo)
"""
import re, sys, os, statistics

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from constantes import PISO_ABSOLUTO as FLOOR, HERO, T_XL   # fuente única: constantes.py

RATIO_SALTO = 1.6           # E5: salto mínimo título mayor / mediana de títulos
# clases de escala de los builders legacy (pre-engine), por si aparecen sin font-size inline
T_CLASE = {"t-xl": T_XL, "t-l": 80.0, "t-m": 64.0, "t-s": 48.0}

# El piso de 26px es POR SLIDE; el héroe de 90px es POR CARRUSEL (composicion-y-tipografia.md §4.2:
# "Titular héroe (>=1 por carrusel)"). Por eso hay que pasarle TODAS las slides en UNA invocación:
#     qa_typesize.py s-*.html          # <- correcto
#     for f in s-*.html; do qa_typesize.py $f; done   # <- FAIL FALSO en todas menos la portada
# Falla real (Marca Verde c67, 29-jul-2026): corrido en bucle, marcó FAIL en 5 de 6 slides que sí
# cumplían, y el diagnóstico inicial fue "el script está mal" cuando el script estaba bien.
# Desde ahora el gate detecta el uso de a uno y lo dice en vez de mentir con un FAIL.

def with_linked_css(path, html):
    """El gate leía SOLO el HTML: si la escala tipográfica vive en un <link rel=stylesheet>,
    no veía ni un font-size y devolvía un FAIL falso ('ningún héroe') o, peor, un PASS falso
    cuando el CSS enlazado tenía textos bajo el piso. Ahora sigue los <link> locales.
    (Hallazgo del test de ads Claude Code, jul-2026 — mismo tipo de ceguera que la regla 0.7.)"""
    base = os.path.dirname(os.path.abspath(path))
    for href in re.findall(r"""<link[^>]+href\s*=\s*["']([^"']+\.css)["']""", html, re.I):
        if href.startswith(("http://", "https://", "//")):
            continue
        p = href if os.path.isabs(href) else os.path.join(base, href)
        try:
            html += "\n/* <-- " + href + " */\n" + open(p, encoding='utf-8').read()
        except OSError:
            print(f"WARN {path}: no se pudo leer el CSS enlazado {href}")
    return html

def titulos_de(t):
    """Los font-size de los TÍTULOS (`class="title…"`), no de todo el texto.

    engine.py emite `<div class="title" style="font-size:120px">`; los builders legacy usaban
    `class="title t-xl"` (clase de escala, sin px inline). Se aceptan los dos órdenes de
    atributos y las clases legacy mapeadas a su px."""
    out = []
    for m in re.finditer(r'class="title[^"]*"[^>]*?font-size:\s*([\d.]+)px', t):
        out.append(float(m.group(1)))
    for m in re.finditer(r'font-size:\s*([\d.]+)px[^>]*?class="title[ "]', t):
        out.append(float(m.group(1)))
    for m in re.finditer(r'class="title\s+(t-(?:xl|l|m|s))"', t):
        out.append(T_CLASE[m.group(1)])
    return out


def main(argv):
    solo_slide = '--slide' in argv
    solo_hero = '--hero-only' in argv
    paths = [a for a in argv if not a.startswith('--')]
    if not paths:
        print("uso: qa_typesize.py s-*.html        (TODAS las slides del carrusel, juntas)")
        print("     qa_typesize.py --slide s-03.html   (una sola: omite héroe y E5)")
        print("     qa_typesize.py --hero-only s-*.html   (solo héroe + E5, sin el piso)")
        return 2
    fail = False
    hero_max = 0.0
    titulos = []
    for f in paths:
        try:
            t = open(f, encoding='utf-8').read()
        except OSError as e:
            print(f"FAIL {f}: no se pudo leer ({e})"); fail = True; continue
        t = with_linked_css(f, t)
        titulos += titulos_de(t)
        sizes = []
        for m in re.finditer(r'font-size:\s*([\d.]+)px', t):
            v = float(m.group(1))
            sizes.append(v)
            if solo_hero:
                continue                    # --hero-only: el piso por slide no corre acá
            ctx = t[max(0, m.start() - 120):m.end() + 40]
            if v < FLOOR and 'ok-small' not in ctx:
                snippet = ' '.join(t[max(0, m.start() - 60):m.end()].split())
                print(f"FAIL {f}: font-size {v:g}px < {FLOOR:g}px  …{snippet}")
                fail = True
        if sizes:
            hero_max = max(hero_max, max(sizes))
            if not solo_hero:
                print(f"{f}: {len(sizes)} tamaños · min {min(sizes):g}px · max {max(sizes):g}px")
        elif not solo_hero:
            print(f"WARN {f}: sin font-size declarados")
    if solo_slide:
        print(f"NOTA: modo --slide, chequeos de héroe y E5 OMITIDOS (son por carrusel). "
              f"Max de esta slide: {hero_max:g}px.")
        print('TYPESIZE:', 'FAIL' if fail else 'PASS')
        return 1 if fail else 0
    if hero_max < HERO:
        if len(paths) == 1:
            # No mentimos con un FAIL: casi siempre es el gate corrido en bucle, slide por slide.
            print(f"FAIL {paths[0]}: ningún texto >= {HERO:g}px (max {hero_max:g}px).")
            print("  ↳ El héroe de 90px es POR CARRUSEL, no por slide. Si estás verificando un")
            print("    carrusel, pásale TODAS las slides en una sola corrida:")
            print("       qa_typesize.py s-*.html")
            print("    Si de verdad querés chequear una sola slide, usá --slide.")
        else:
            print(f"FAIL: ningún héroe >= {HERO:g}px en las {len(paths)} slides "
                  f"(max encontrado {hero_max:g}px) — el carrusel se ve plano sin salto de escala.")
        fail = True
    elif len(paths) > 1:
        print(f"héroe del carrusel: {hero_max:g}px en {len(paths)} slides")
    # ── E5 · salto de escala (auditoría T4): medido de verdad sobre los .title ──
    if titulos:
        tmax = max(titulos)
        med = statistics.median(titulos)
        ratio = tmax / med if med else 0.0
        if tmax < T_XL and ratio < RATIO_SALTO:
            print(f"FAIL E5 · salto de escala: título mayor {tmax:g}px < {T_XL:g}px (t-xl) y "
                  f"sin salto sobre la escala (ratio {ratio:.2f} < {RATIO_SALTO} vs mediana "
                  f"de títulos {med:g}px) — el carrusel queda plano y chico. Subí el título "
                  f"estrella a t-xl.")
            fail = True
        else:
            print(f"E5 · salto de escala: título mayor {tmax:g}px · ratio {ratio:.2f} "
                  f"vs mediana {med:g}px ({len(titulos)} títulos)")
    else:
        # Piso de cordura (T9): si no se identificó NI UN título, E5 no midió nada.
        # No se exige sobre builds sin class="title" (el chequeo de héroe genérico ya corrió).
        print("WARN E5: 0 títulos identificados (sin class=\"title\") — E5 no midió nada")
    print('TYPESIZE:', 'FAIL' if fail else 'PASS')
    return 1 if fail else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
