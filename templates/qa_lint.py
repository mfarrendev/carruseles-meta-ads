#!/usr/bin/env python3
"""
Auto-lint de carruseles (Capa 1 del protocolo de QA).
Para cada slide HTML mide, sin tocar los archivos del slide:
  1) CONTRASTE WCAG real texto/fondo (renderiza CON y SIN texto, máscara por diferencia).
  2) MÁRGENES seguros / texto cortado.
  3) ⚠ TEXTO SOBRE SUJETO/OBJETO: renderiza la foto CRUDA (sin texto ni scrims) y, bajo
     la caja del texto, mide la "textura" (std de luminancia). Si es alta (zona con
     detalle = probable persona/objeto) y el scrim no es sólido, AVISA para revisar que
     el texto no tape a la persona ni el objeto clave.

Rendimiento (3-ago-2026, auditoría L4 — era el 92% del costo de `gates`, 38,5s de 41,9s
por 3 Chromes por slide en serie):
  - si existe `s-NN.png` junto al HTML y es MÁS NUEVO que el HTML, se reutiliza como el
    render "con texto" (1 de los 3 renders ahorrado; el PNG ya lo produjo el pipeline);
  - las slides se procesan EN PARALELO con ProcessPoolExecutor (cada worker abre sus
    propios Chrome headless sobre archivos temporales propios — sin estado compartido).

Piso de cordura (auditoría T9): si sobre un HTML que existe no se detectó NINGÚN bloque
de texto, la compuerta no midió nada → FAIL, no WARN ("0 elementos revisados").

Uso:  python3 qa_lint.py <slide1.html> <slide2.html> ...
"""
import sys, os, subprocess, re, tempfile, shutil, time
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from PIL import Image

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SAFE = 48
SIZE = 1080          # ancho del lienzo (el ALTO se lee del HTML: 1080 por defecto, 1:1)
DEFAULT_H = 1080     # fallback: alto del default actual (1:1, reconfirmado por el director creativo 3-ago-2026)
MIN_CONTRAST = 4.5
HIDE_TEXT = "<style id='qa-h'>.text,.cta,.sub{visibility:hidden!important}</style>"
# raw = sin texto y sin scrims/bloques/overlays → solo la foto
HIDE_RAW = ("<style id='qa-r'>.text,.cta,.sub,.swipe,.logo,.index,.sc-bottom,.sc-top,"
            ".sc-left,.sc-right,.sc-cap,.tint,.band,.block,.wash{visibility:hidden!important}</style>")
# umbrales heurísticos (luminancia 0..1)
SUBJ_STD = 0.11   # textura alta bajo el texto = probable sujeto/objeto
SCRIM_STD = 0.05  # si el fondo (con scrim) es muy plano = backing sólido → no avisar

_RE_LIENZO = re.compile(r"html,body\{[^}]*?width:\s*(\d+)px[^}]*?height:\s*(\d+)px")
_RE_SLIDE_CSS = re.compile(r"\.slide\{[^}]*?width:\s*(\d+)px[^}]*?height:\s*(\d+)px")

def dims_de(html_path):
    """Lienzo real de la slide, en orden de confianza:
    1. el inline `html,body{width;height}` que engine.py declara desde la oleada 2.5A;
    2. el `.slide{width;height}` del CSS enlazado (builds legacy 1:1 con su styles.css propio);
    3. el default actual (1080×1080).
    Medir con el lienzo equivocado distorsiona la máscara texto/fondo: el PNG reutilizado
    y los renders CON/SIN texto tienen que tener el MISMO tamaño o el diff miente."""
    try:
        src = open(html_path, encoding="utf-8", errors="ignore").read()
    except OSError:
        return SIZE, DEFAULT_H
    m = _RE_LIENZO.search(src)
    if m:
        return int(m.group(1)), int(m.group(2))
    base = os.path.dirname(os.path.abspath(html_path))
    for href in re.findall(r"""<link[^>]+href\s*=\s*["']([^"']+\.css)["']""", src, re.I):
        if href.startswith(("http://", "https://", "//")):
            continue
        p = href if os.path.isabs(href) else os.path.join(base, href)
        try:
            m = _RE_SLIDE_CSS.search(open(p, encoding="utf-8", errors="ignore").read())
        except OSError:
            continue
        if m:
            return int(m.group(1)), int(m.group(2))
    return SIZE, DEFAULT_H

def render(html_path, out_png, dims=(SIZE, DEFAULT_H)):
    # Perfil TEMPORAL por render: varios Chrome headless con el MISMO user-data-dir se
    # bloquean entre sí por el singleton del perfil (colgó la primera paralelización de
    # L4, 3-ago-2026). Y con perfil fresco Chrome ESCRIBE el screenshot pero a veces no
    # sale del proceso (segundo cuelgue, mismo día): se espera el ARCHIVO, no el proceso,
    # y en cuanto el PNG está completo en disco se termina Chrome a mano.
    prof = tempfile.mkdtemp(prefix=".qa_chrome_")
    p = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
        "--no-first-run", "--no-default-browser-check", "--disable-background-networking",
        "--disable-component-update", "--disable-sync", f"--user-data-dir={prof}",
        "--force-device-scale-factor=1", f"--window-size={dims[0]},{dims[1]}",
        "--virtual-time-budget=4000", f"--screenshot={out_png}",
        f"file://{os.path.abspath(html_path)}"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    tam = -1
    for _ in range(1200):                       # hasta ~2 min por render (piso del pipeline)
        if os.path.exists(out_png):
            t = os.path.getsize(out_png)
            if t > 0 and t == tam:              # tamaño estable dos lecturas seguidas
                break
            tam = t
        if p.poll() is not None:                # Chrome salió solo (perfil no fresco, etc.)
            break
        time.sleep(0.1)
    if p.poll() is None:
        p.terminate()
        try:
            p.wait(timeout=5)
        except subprocess.TimeoutExpired:
            p.kill()
    shutil.rmtree(prof, ignore_errors=True)

def lin(c):
    c = c/255.0
    return np.where(c <= 0.03928, c/12.92, ((c+0.055)/1.055)**2.4)

def rel_lum(rgb):
    r,g,b = lin(rgb[...,0]), lin(rgb[...,1]), lin(rgb[...,2])
    return 0.2126*r + 0.7152*g + 0.0722*b

def contrast(l1, l2):
    a,b = max(l1,l2), min(l1,l2)
    return (a+0.05)/(b+0.05)

def variant(html, base, suffix, hide, dims):
    d = os.path.dirname(os.path.abspath(html))
    tmp = os.path.join(d, f".qa_{base}_{suffix}.html")
    src = open(html, encoding="utf-8").read()
    open(tmp, "w", encoding="utf-8").write(re.sub(r"</head>", hide+"</head>", src, count=1))
    png = os.path.join(d, f".qa_{base}_{suffix}.png")
    render(tmp, png, dims)
    arr = np.asarray(Image.open(png).convert("RGB").resize(dims), dtype=np.int16)
    return arr, tmp, png

def lint(html):
    d = os.path.dirname(os.path.abspath(html))
    base = os.path.splitext(os.path.basename(html))[0]
    dims = dims_de(html)                     # (ancho, alto) REAL del lienzo de esta slide
    W, H = dims
    # Preset Pilates v2: todo el texto es large-text WCAG (≥27px) → mínimo AA large = 3.0
    # (excepción documentada en RUBRIC.md E1; el sistema aprobado corre más etéreo)
    src_preset = open(html, encoding="utf-8", errors="ignore").read()
    min_c = 3.0 if 'data-brand="pilates"' in src_preset else MIN_CONTRAST
    # L4: reutilizar s-NN.png si existe y es más nuevo que el HTML — es el mismo render
    # "con texto" que haría el primer Chrome. NUNCA se borra: es un archivo del pipeline.
    candidato = os.path.join(d, base + ".png")
    if os.path.exists(candidato) and os.path.getmtime(candidato) >= os.path.getmtime(html):
        full_png = None
        full = np.asarray(Image.open(candidato).convert("RGB").resize(dims), dtype=np.int16)
    else:
        full_png = os.path.join(d, f".qa_{base}_full.png")
        render(html, full_png, dims)
        full = np.asarray(Image.open(full_png).convert("RGB").resize(dims), dtype=np.int16)
    bg, tmp_bg, bg_png = variant(html, base, "bg", HIDE_TEXT, dims)
    raw, tmp_raw, raw_png = variant(html, base, "raw", HIDE_RAW, dims)
    diff = np.abs(full-bg).sum(axis=2)
    mask = diff > 45
    issues = []
    if mask.sum() < 200:
        # PISO DE CORDURA (T9): sobre un HTML que existe, "sin bloque de texto" significa
        # que la compuerta no midió NADA — contraste, márgenes y textura quedaron sin correr.
        issues.append("FAIL 0 elementos revisados: la compuerta no midió nada "
                      "(no se detectó bloque de texto en el render)")
    else:
        txt = rel_lum(full[mask].astype(float)); bgl = rel_lum(bg[mask].astype(float))
        cr = contrast(float(np.median(txt)), float(np.median(bgl)))
        issues.append(f"{'PASS' if cr>=min_c else 'FAIL'} contraste texto/fondo = {cr:.1f}:1 (min {min_c})")
        ys, xs = np.where(mask)
        x0,x1,y0,y1 = xs.min(), xs.max(), ys.min(), ys.max()
        if x0<SAFE or y0<SAFE or x1>W-SAFE or y1>H-SAFE:
            issues.append(f"FAIL margen: caja [{x0},{y0}]-[{x1},{y1}], seguro={SAFE}..{W-SAFE}×{H-SAFE}")
        else:
            issues.append(f"PASS márgenes ({x0},{y0}-{x1},{y1})")
        # ⚠ texto sobre sujeto/objeto: textura de la foto cruda bajo la caja del texto
        raw_box = rel_lum(raw[y0:y1, x0:x1].astype(float))
        bg_box  = rel_lum(bg[y0:y1, x0:x1].astype(float))
        raw_std, bg_std = float(np.std(raw_box)), float(np.std(bg_box))
        if raw_std > SUBJ_STD and bg_std > SCRIM_STD:
            issues.append(f"WARN texto sobre zona con detalle (textura {raw_std:.2f}) — "
                          f"revisar a tamaño completo que NO tape persona ni objeto clave")
        else:
            issues.append(f"PASS texto en zona limpia (textura {raw_std:.2f})")
    for f in (full_png, bg_png, raw_png, tmp_bg, tmp_raw):
        if not f:               # full_png es None cuando se reutilizó s-NN.png (no se borra)
            continue
        try: os.remove(f)
        except: pass
    return issues

def _trabajo(html):
    """Worker del pool (L4): tiene que ser top-level para que ProcessPoolExecutor lo pickelee."""
    return os.path.basename(html), lint(html)

def main():
    files = sys.argv[1:]
    print(f"\n=== AUTO-LINT QA · {len(files)} slides ===")
    any_fail = False
    # L4: las slides se lintean EN PARALELO. Cada worker escribe sus propios .qa_* temporales
    # y abre sus propios Chrome headless — no hay estado compartido que pisar.
    resultados = {}
    if len(files) > 1:
        with ProcessPoolExecutor(max_workers=min(len(files), os.cpu_count() or 4)) as ex:
            for nombre, res in ex.map(_trabajo, files):
                resultados[nombre] = res
    else:
        for h in files:
            nombre, res = _trabajo(h)
            resultados[nombre] = res
    for h in files:     # se imprime en el ORDEN de los argumentos, no en el de llegada
        res = resultados[os.path.basename(h)]
        flag = "❌" if any("FAIL" in r for r in res) else ("⚠️" if any("WARN" in r for r in res) else "✅")
        if "❌" in flag: any_fail = True
        print(f"\n{flag} {os.path.basename(h)}")
        for r in res: print(f"    {r}")
    # El salto de escala (E5) se movió a qa_typesize.py (auditoría T4): acá buscaba
    # `class="title t-xl"`, una clase que engine.py no emite — nunca midió nada.
    print(f"\n=== {'HAY FAILS — corregir' if any_fail else 'sin FAILs (revisar WARNs)'} ===\n")
    print("LINT:", "FAIL" if any_fail else "PASS")
    # ⚠️ 31-jul-2026: esto NO devolvía nada, así que el proceso salía 0 SIEMPRE — aunque
    # imprimiera "❌ HAY FAILS". Cualquier runner que mirara el exit code recibía un PASS
    # falso (lo cazó verify.py con un contraste de 3.1:1 reportado como gate en verde).
    # Un gate que falla en la salida pero sale 0 es peor que no tener gate.
    return 1 if any_fail else 0

if __name__ == "__main__":
    sys.exit(main())
