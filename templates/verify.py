#!/usr/bin/env /usr/local/bin/python3
"""
verify.py — EL RUNNER ÚNICO DE COMPUERTAS (31-jul-2026).

Por qué existe. La Fase 6 eran CINCO invocaciones distintas con flags largos, y el aprendizaje
del 29-jul (Marca Verde c67) fue exactamente un gate corrido mal en silencio: `qa_typesize` en bucle,
slide por slide, marcó FAIL en 5 de 6 que sí cumplían — porque el héroe de 90px es POR CARRUSEL.
La conclusión que quedó escrita fue: *"un gate que se puede usar mal en silencio está incompleto"*.

Esto elimina la superficie de mal uso: un comando por fase, los flags correctos por dentro, y
un RECIBO firmado con el hash de lo que midió.

    verify.py init       <carpeta>     → carrusel.json + _brief.md  (ANDAMIO, Fase 1)
    verify.py brief      <carpeta>     → _brief-receipt.json
    verify.py copy       <carpeta>     → _copy-gate-receipt.json   (mecánico; el panel ciego es aparte)
    verify.py blueprint  <carpeta>     → _blueprint-receipt.json
    verify.py prompt     <carpeta>     → _prompt-receipt.json      (el prompt reserva la zona,
                                                                    ANTES de gastar la generación)
    verify.py raw        <carpeta>     → _raw-receipt.json         (qa_raw + qa_seam)
    verify.py gates      <carpeta>     → _gates-receipt.json       (typesize+lint+lines+dom+A8+thumbs)
    verify.py thumbs     <carpeta>     → _thumb-NN.png a 360px (legibilidad móvil, Fase 7)
    verify.py lote       <carpeta-madre> → _lote-receipt.json      (C12: ángulos repetidos entre
                           hermanos → FAIL · ≥3 portadas con el mismo arranque de 3 palabras → WARN)
    verify.py all        <carpeta>     → corre las que puede, en orden

Flags (en `raw`, `gates` y `all`):
    --only s-03          re-corre SOLO esa slide y marca el recibo con scope: ["s-03"]
                         (un re-render de una slide no invalida el set entero — 3-ago-2026)
    --warn-ok "razón"    graba POR QUÉ se aceptan los WARNs del recibo. Sin el flag el recibo
                         queda con warns_sin_razon: true y la Fase 7 tiene que revisarlos.

WARNs con razón escrita (3-ago-2026). Antes los recibos eran binarios: un WARN no dejaba
rastro. Ahora el recibo distingue fails y warns:
    0 fails + 0 warns   → status PASS
    0 fails + N warns   → status PASS_CON_WARNS (la puerta pasa igual: el hook lee `verdict`,
                          que sigue en PASS; el matiz queda en `status` + la lista `warns`)
    ≥1 fail             → status FAIL
Las métricas de densidad/espaciado se satisfacen con contenido real, NUNCA con ornamento:
un WARN de densidad se acepta con --warn-ok antes que decorar la slide.

El hash de entradas es lo que impide falsificar un recibo a mano: el hook `carrusel-gate`
recalcula el hash de los archivos y, si no coincide, trata el recibo como inválido.

`init` existe porque faltaba el eslabón (1-ago-2026). `carrusel.json` es la piedra angular
—lo leen engine.py, las 5 fases de acá y las 4 puertas del hook— pero NINGUNA fase del
pipeline mandaba a escribirlo: la Fase 1 pedía `_brief.md` en prosa y la Fase 5 mandaba correr
el motor, que abre `carrusel.json` y revienta si no está. El agente interpretaba eso como "el
motor no aplica acá" y se escribía su propio `build.py` — sin que ninguna compuerta se enterara,
porque sin spec el hook las daba por no adoptadas. Medición del 1-ago-2026: **79 de 81 carpetas
-carrusel del disco no tenían spec**, y había 10 `build.py` sueltos. Es la misma falla de los
"SIETE build.py" que el motor único decía haber resuelto: no se resolvió, se movió de lugar.

El andamio deja los campos obligatorios VACÍOS a propósito: rellenarlos es el trabajo de la
Fase 1. Un esqueleto que pasara `verify.py brief` con valores de relleno sería peor que no
tenerlo — convertiría la compuerta en un trámite.
"""
import sys, os, json, hashlib, subprocess, glob, time, shutil, re

AQUI = os.path.dirname(os.path.abspath(__file__))
PY = "/usr/local/bin/python3"
REPO = os.path.abspath(os.path.join(AQUI, "..", "..", "..", ".."))
sys.path.insert(0, AQUI)

RECIBO = {"brief": "_brief-receipt.json", "copy": "_copy-gate-receipt.json",
          "blueprint": "_blueprint-receipt.json", "prompt": "_prompt-receipt.json",
          "raw": "_raw-receipt.json",
          "gates": "_gates-receipt.json", "lote": "_lote-receipt.json"}


def sha(path, n=12):
    try:
        with open(path, "rb") as f:
            return hashlib.sha1(f.read()).hexdigest()[:n]
    except OSError:
        return None


def firmar(paths):
    return {os.path.basename(p): sha(p) for p in sorted(paths) if sha(p)}


def correr_script(nombre, args):
    """Ejecuta un gate y devuelve (ok, resumen).

    NO se confía solo en el exit code. Motivo real (31-jul-2026): `qa_lint.py` imprimía
    "❌ HAY FAILS — corregir" con un contraste de 3.1:1 y aun así salía 0, porque su main()
    no devolvía nada. Este runner lo dio por PASS. Se arregló qa_lint, pero la lección es que
    un runner no debe depender de que cada gate esté bien terminado: si la SALIDA dice FAIL,
    es FAIL, aunque el proceso diga que todo bien."""
    p = subprocess.run([PY, os.path.join(AQUI, nombre)] + args,
                       capture_output=True, text=True)
    salida = (p.stdout or "") + (p.stderr or "")
    cola = [l for l in salida.strip().split("\n") if l.strip()]
    resumen = cola[-1] if cola else "sin salida"
    fallos = [l for l in cola if l.strip().startswith("FAIL") or l.strip().startswith("❌")][:4]
    if fallos:
        resumen = " · ".join(f.strip()[:110] for f in fallos)
    ok = p.returncode == 0 and not fallos
    # Mismo criterio que arriba, para el otro veredicto: si la SALIDA dice WARN, el recibo
    # lleva WARN. Antes esto se perdía — `qa_raw` avisaba «1 detección bajo conf 0.5, mirar a
    # tamaño completo» y el recibo quedaba PASS con 0 warns, o sea el aviso desaparecía justo
    # en el archivo que existe para que no desaparezca. (5-ago-2026)
    if ok:
        avisos = [l for l in cola if l.strip().startswith("WARN") or l.strip().startswith("⚠")][:4]
        if avisos:
            return None, " · ".join(a.strip()[:140] for a in avisos)
    if p.returncode != 0 and not fallos:
        resumen = f"exit {p.returncode} · {resumen}"
    return ok, resumen


def slides_html(carpeta):
    h = sorted(glob.glob(os.path.join(carpeta, "s-*.html")))
    return h or sorted(p for p in glob.glob(os.path.join(carpeta, "*.html"))
                       if not os.path.basename(p).startswith("_"))


def raws(carpeta):
    for sub in ("raw", "fotos", "assets"):
        f = sorted(glob.glob(os.path.join(carpeta, sub, "*.png")) +
                   glob.glob(os.path.join(carpeta, sub, "*.jpg")))
        if f:
            return f
    return []


def filtrar(paths, only):
    """--only s-03: deja solo los archivos de ESA slide. Re-render de una slide no
    invalida el set entero (3-ago-2026) — el hash firmado cubre exactamente lo medido."""
    if not only:
        return paths
    token = only.replace(".html", "").replace(".png", "")
    sel = [p for p in paths if token in os.path.basename(p)]
    return sel


def correr_qa_dom(html):
    """Validación sobre el DOM renderizado (qa_dom.mjs, Node + Playwright).

    → (ok, detalle) con ok True/False/None. Si node o Playwright no están, devuelve
    (None, 'qa_dom no corrió: falta playwright'): WARN declarado — nunca un pass
    silencioso, nunca fail-closed por una dependencia ausente."""
    node = shutil.which("node") or ("/usr/local/bin/node" if os.path.exists("/usr/local/bin/node")
                                    else None)
    if not node:
        return None, "qa_dom no corrió: falta node", []
    # Rutas ABSOLUTAS: qa_dom corre con cwd=AQUI (templates/), así que un `verify.py gates
    # c1-carpeta` invocado desde la carpeta del lote le llegaba como ruta relativa muerta y
    # Playwright devolvía ERR_FILE_NOT_FOUND en las 5 slides — un FAIL que no habla del diseño
    # sino de dónde estabas parado al invocar. (5-ago-2026)
    html = [os.path.abspath(h) for h in html]
    try:
        p = subprocess.run([node, os.path.join(AQUI, "qa_dom.mjs")] + html,
                           capture_output=True, text=True, cwd=AQUI, timeout=180)
    except subprocess.TimeoutExpired:
        return None, "qa_dom no corrió: timeout 180s", []
    salida = (p.stdout or "").strip()
    try:
        data = json.loads(salida[salida.index("{"):])
    except (ValueError, json.JSONDecodeError):
        # DEPENDENCIA AUSENTE ≠ GATE ROTO. Las dos cosas caían acá y las dos salían como WARN,
        # así que el conjunto terminaba en PASS_CON_WARNS: un gate que revienta se convertía en
        # permiso para avanzar. Pasó de verdad el 5-ago-2026 — un backtick en un comentario
        # dentro del template literal de `MEDIR` tiró un SyntaxError, qa_dom murió con exit 1
        # y los dos carruseles pasaron "en verde" sin que nadie mirara solapes, overflow ni
        # piso de fuente. Es exactamente el fail-open que la skill prohíbe (recibo-fail-no-se-
        # falsea). Ausencia declarada (exit 3 / falta node) sigue siendo WARN; un crash es FAIL.
        err = (p.stderr or "").strip().split("\n")
        pista = next((l for l in err if "Error" in l or "error" in l), err[-1] if err else "")
        return False, (f"qa_dom REVENTÓ (exit {p.returncode}) — el gate no midió nada. "
                       f"{pista[:120]} · fix: arreglar qa_dom.mjs, no seguir sin él"), []
    if data.get("error"):
        return None, ("qa_dom no corrió: falta playwright "
                      "(templates/: npm i playwright && npx playwright install chromium)"), []
    fails, warns = [], []
    for s in data.get("slides", []):
        fails += [f"{s['slide']} · {f['rule']}: {f['detalle']}" for f in s["fails"]]
        warns += [f"{s['slide']} · {w['rule']}: {w['detalle']}" for w in s["warns"]]
    if fails:
        return False, " · ".join(f[:160] for f in fails[:4]), warns
    if warns:
        return None, " · ".join(w[:160] for w in warns[:4]), warns
    return True, f"{len(data.get('slides', []))} slides sin overflow, colisiones con el " \
                 "chrome ni texto bajo piso", warns


def generar_thumbs(carpeta, pngs):
    """_thumb-NN.png a 360px por slide, con sips (cero dependencias nuevas).

    La miniatura a 360px es el test de legibilidad móvil de la Fase 7: si a ese tamaño
    no se entiende qué domina, la jerarquía falló. → (ok, detalle)"""
    if not shutil.which("sips"):
        return None, "thumbs no corrió: falta sips"
    hechos, fallidos = [], []
    for p in pngs:
        base = os.path.basename(p)                       # s-03.png
        suf = base.split("-", 1)[-1]                     # 03.png
        out = os.path.join(carpeta, f"_thumb-{suf}")
        r = subprocess.run(["sips", "-Z", "360", p, "--out", out],
                           capture_output=True, text=True)
        if r.returncode == 0 and os.path.exists(out):
            hechos.append(os.path.basename(out))
        else:
            fallidos.append(base)
    if fallidos:
        return None, f"sips falló en {', '.join(fallidos)}"
    if not hechos:
        return None, "no hay s-*.png renderizados para miniaturizar"
    return True, f"{len(hechos)} thumbnails 360px: {', '.join(hechos)}"


def fotos_renderizadas(html_paths):
    """→ {src: [slides]} con los `<img class="photo" …>` de las slides RENDERIZADAS.

    A8 (cero imágenes repetidas) se atribuía al motor y nadie lo verificaba sobre el render
    (auditoría T5): el spec puede declarar 5 fotos distintas y aun así la misma imagen
    terminar compuesta en 2 slides. Se cuentan SOLO las .photo — el logo y el cutout se
    repiten por diseño."""
    usos = {}
    for p in html_paths:
        try:
            t = open(p, encoding="utf-8").read()
        except OSError:
            continue
        for tag in re.findall(r"<img\b[^>]*>", t):
            cls = re.search(r'class="([^"]*)"', tag)
            src = re.search(r'src="([^"]*)"', tag)
            if not src or not cls or "photo" not in cls.group(1).split():
                continue
            usos.setdefault(src.group(1), []).append(os.path.basename(p))
    return usos


# ───────────────────────────────────────────────────────────────── fases ──
def fase_brief(carpeta):
    import qa_brief
    r = qa_brief.correr(carpeta)
    r["inputs"] = firmar([os.path.join(carpeta, "carrusel.json"),
                          os.path.join(carpeta, "_brief.md")])
    return r


def fase_copy(carpeta):
    import qa_copy
    sp = os.path.join(carpeta, "carrusel.json")
    if not os.path.exists(sp):
        return {"gate": "copy", "verdict": "FAIL",
                "checks": [{"check": "existe carrusel.json", "ok": False,
                            "detalle": "falta el spec"}], "inputs": {}}
    r = qa_copy.correr(json.load(open(sp, encoding="utf-8")))
    r["inputs"] = firmar([sp])
    return r


def fase_blueprint(carpeta):
    import qa_blueprint
    r = qa_blueprint.correr(carpeta)
    r["inputs"] = firmar([os.path.join(carpeta, "carrusel.json")])
    return r


def fase_prompt(carpeta, only=None):
    """El prompt reserva el hueco del texto ANTES de generar (director creativo, 6-ago-2026).

    Es la única compuerta del pipeline que corre sobre algo que TODAVÍA NO SE PAGÓ. `raw` mide
    el hueco después: cuando falla, la generación ya está gastada. Acá se lee el `prompt` que va
    a salir y se contesta si nombra el lado de su `zone` y si pide continuidad de escena en vez
    de un bloque muerto. Detalle y la cláusula ya calculada: `prompt_zona.py`."""
    import prompt_zona
    r = prompt_zona.cmd_verificar(carpeta, only)
    checks = [{"check": f"{c['slide']} · {c['detalle']}",
               "ok": None if c["estado"] == "N/A" else (c["estado"] == "PASS"),
               "detalle": c["detalle"]} for c in r["checks"]]
    return {"gate": "prompt", "verdict": r["status"], "checks": checks,
            "inputs": firmar([os.path.join(carpeta, "carrusel.json")])}


def fase_raw(carpeta, only=None):
    """A11 texto inventado + zona reservada (qa_raw) · costura de collage (qa_seam)."""
    import qa_seam
    fotos = filtrar(raws(carpeta), only)
    checks = []
    if not fotos:
        return {"gate": "raw", "verdict": "FAIL", "inputs": {},
                "checks": [{"check": "hay fotos crudas", "ok": False,
                            "detalle": f"no encontré fotos para {only}" if only else
                                       "no encontré raw/ ni fotos/ con imágenes"}]}

    # qa_raw: OCR de texto inventado (SIEMPRE) + zona reservada (solo en fotos GENERADAS)
    #
    # ⚠️ La zona reservada solo es un CONTRATO cuando la foto se generó para el plan: el prompt
    # pidió "sujeto en el tercio derecho, la izquierda vacía" y hay que verificar que el modelo
    # obedeció (produccion-imagenes §0.2 — se cumple en ~3 de cada 4 generaciones).
    # Con una foto REAL que ya existe, la zona del spec es una preferencia, no un contrato: el
    # motor mira dónde está la persona y REASIGNA. Exigirla acá bloqueaba fotos perfectamente
    # usables. Bug real: el primer lote de Marca Crema falló 6 zonas sobre fotos del banco que
    # el motor después resolvió sin problema.
    args = fotos[:]
    sp = os.path.join(carpeta, "carrusel.json")
    zonas = os.path.join(carpeta, "_zonas.json")
    n_gen = 0
    if os.path.exists(sp):
        spec = json.load(open(sp, encoding="utf-8"))
        z = []
        for s in spec.get("slides", []):
            generada = str(s.get("fuente", "")).lower().startswith("gener")
            n_gen += generada
            z.append({"zone": s.get("zone") if generada else None})
        if n_gen:
            json.dump({"slides": z}, open(zonas, "w", encoding="utf-8"))
            args += ["--zones", zonas]
    ok, res = correr_script("qa_raw.py", args)
    detalle = res + (f" · zona reservada verificada en {n_gen} foto(s) generada(s)" if n_gen
                     else " · zonas NO verificadas: todas las fotos son reales, la zona la "
                          "asigna el motor mirando dónde está la persona")
    checks.append({"check": "A11 · texto inventado" + (" + zona reservada" if n_gen else ""),
                   "ok": ok, "detalle": detalle})
    if os.path.exists(zonas):
        os.unlink(zonas)

    # qa_seam: collage en los DOS ejes
    peor, detalles = "PASS", []
    for f in fotos:
        try:
            c = qa_seam.costura(f)
        except Exception as e:
            c = {"veredicto": "WARN", "archivo": f, "error": str(e)[:60]}
        if c["veredicto"] != "PASS":
            e = c.get("ejes", {}).get(c.get("peor_eje"), {})
            detalles.append(f"{os.path.basename(f)} {c['veredicto']} "
                            f"({c.get('peor_eje')} {e.get('persistencia')})")
        if c["veredicto"] == "FAIL":
            peor = "FAIL"
        elif c["veredicto"] == "WARN" and peor == "PASS":
            peor = "WARN"
    checks.append({"check": "costura de collage (2 ejes)",
                   "ok": True if peor == "PASS" else (False if peor == "FAIL" else None),
                   "detalle": "; ".join(detalles) or f"{len(fotos)} fotos sin costura"})

    fail = any(c["ok"] is False for c in checks)
    r = {"gate": "raw", "verdict": "FAIL" if fail else "PASS",
         "checks": checks, "inputs": firmar(fotos)}
    if only:
        r["scope"] = [only.replace(".html", "").replace(".png", "")]
    return r


def fase_gates(carpeta, only=None):
    """Lo mecánico del render: piso tipográfico, E5, contraste, quiebres, DOM, A8, thumbs."""
    html = filtrar(slides_html(carpeta), only)
    checks = []
    if not html:
        return {"gate": "gates", "verdict": "FAIL", "inputs": {},
                "checks": [{"check": "hay slides renderizadas", "ok": False,
                            "detalle": f"no encontré {only}.html" if only else
                                       "no encontré s-*.html"}]}

    # ⚠️ TODAS juntas: el héroe de 90px y el salto de escala (E5) son POR CARRUSEL
    # (lección Marca Verde c67, 29-jul-2026). Con --only (auditoría T8): el piso corre en modo
    # --slide SOLO sobre la tocada, pero héroe+E5 NO se pueden omitir en silencio — segunda
    # pasada --hero-only sobre el set completo, anotada en el recibo, y la firma cubre
    # TODAS las slides que se midieron (no solo la tocada).
    if only:
        ok, res = correr_script("qa_typesize.py", ["--slide"] + html)
        checks.append({"check": f"E3/E8 · piso tipográfico (solo {only})", "ok": ok,
                       "detalle": res})
        ok, res = correr_script("qa_typesize.py", ["--hero-only"] + slides_html(carpeta))
        checks.append({"check": "E5/E8 · héroe y salto de escala del carrusel "
                                "(pasada completa, --only no la exime)", "ok": ok,
                       "detalle": res})
    else:
        ok, res = correr_script("qa_typesize.py", html)
        checks.append({"check": "E3/E5/E8 · piso tipográfico y salto de escala", "ok": ok,
                       "detalle": res})

    # E9/E6 (solapes, aire pastilla↔texto, texto fuera de pastilla) los mide qa_dom más
    # abajo, sobre el DOM renderizado. qa_geom.py quedó LEGACY (auditoría T6): parseaba 0
    # elementos sobre la salida de engine.py y pasaba en falso; solo sirve para builds
    # antiguos y ya no forma parte de las compuertas.

    ok, res = correr_script("qa_lint.py", html)
    checks.append({"check": "E1/E2 · contraste WCAG y márgenes", "ok": ok, "detalle": res})

    # A8 · cero imágenes repetidas EN EL RENDER (auditoría T5: lo daba por hecho el motor
    # y nadie lo medía). Corre sobre el set completo aun con --only: una repetición
    # involucra dos slides, mirar solo la tocada no la ve.
    usos = fotos_renderizadas(slides_html(carpeta))
    repetidas = {src: slides for src, slides in usos.items() if len(slides) > 1}
    if repetidas:
        det = " · ".join(f"{src} × {len(sl)} ({', '.join(sl)})"
                         for src, sl in sorted(repetidas.items()))
        checks.append({"check": "A8 · cero imágenes repetidas en el render", "ok": False,
                       "detalle": f"imagen repetida: {det}"})
    else:
        checks.append({"check": "A8 · cero imágenes repetidas en el render", "ok": True,
                       "detalle": (f"{len(usos)} fotos distintas en las slides" if usos else
                                   "sin <img class=\"photo\"> (carrusel tipográfico)")})

    # qa_lines necesita la tipografía real: solo corre si el spec la declara
    sp = os.path.join(carpeta, "carrusel.json")
    tipo = (json.load(open(sp, encoding="utf-8")).get("tipografia")
            if os.path.exists(sp) else None)
    if tipo and tipo.get("font"):
        fp = tipo["font"] if os.path.isabs(tipo["font"]) else os.path.join(carpeta, tipo["font"])
        ok, res = correr_script("qa_lines.py", [
            sp, "--font", fp, "--width", str(tipo.get("width", 640)),
            "--size", str(tipo.get("size", 92)), "--hero", str(tipo.get("hero", 100)),
            "--weight", str(tipo.get("weight", 700)),
            "--tracking", str(tipo.get("tracking", -0.02))])
        checks.append({"check": "quiebres del spec respetados", "ok": ok, "detalle": res})
    else:
        checks.append({"check": "quiebres del spec respetados", "ok": None,
                       "detalle": "sin bloque 'tipografia' en carrusel.json → qa_lines NO corrió. "
                                  "Los <br> no impiden el re-wrap del navegador (composicion §5)."})

    # qa_dom: validación sobre el DOM renderizado (overflow, colisión con el chrome,
    # piso de fuente computado, solapes, aire pastilla↔texto y desborde de pastilla → FAIL ·
    # gap título y densidad por bandas → WARN). Las reglas de solape/pastilla se movieron
    # acá desde qa_geom (auditoría T6).
    # Si falta node/Playwright se reporta como WARN, nunca pass silencioso ni fail-closed.
    ok, res, _warns_dom = correr_qa_dom(html)
    checks.append({"check": "DOM renderizado · overflow, chrome, piso, solapes, pastillas, "
                            "densidad (qa_dom)", "ok": ok, "detalle": res})

    # qa_pastilla: la ILUSTRACIÓN encima de la pastilla CTA. qa_dom no puede verlo — mide cajas
    # del DOM, y la ilustración es una imagen de fondo cuyo contenido real vive en su alfa, que
    # el motor además pinta en z-index 4, ENCIMA del texto. Una hoja que sobresalga se monta
    # sobre la pastilla sin que ningún gate del DOM lo note. Lo cazaron dos jueces a ojo; esto
    # lo vuelve determinista. (APRENDIZAJES §17.a — el gate existía y vivía fuera de la skill)
    if os.path.isdir(os.path.join(carpeta, "raw")):
        ok, res = correr_script("qa_pastilla.py", [carpeta])
        checks.append({"check": "A2c · la ilustración no invade la pastilla CTA (qa_pastilla)",
                       "ok": ok, "detalle": res})
    else:
        checks.append({"check": "A2c · la ilustración no invade la pastilla CTA (qa_pastilla)",
                       "ok": None, "detalle": "sin carpeta raw/ → qa_pastilla NO corrió (necesita "
                                              "el crudo para medir el contenido real, no la caja)"})

    # thumbnails 360px: el test de legibilidad móvil que leen los jueces en la Fase 7
    pngs = filtrar(sorted(glob.glob(os.path.join(carpeta, "s-*.png"))), only)
    ok, res = generar_thumbs(carpeta, pngs)
    checks.append({"check": "thumbnails 360px (legibilidad móvil, Fase 7)", "ok": ok,
                   "detalle": res})

    fail = any(c["ok"] is False for c in checks)
    # Con --only la firma cubre TODAS las slides: la pasada --hero-only y A8 las midieron
    # enteras (T8/T5). Firmar solo la tocada sería mentir sobre lo que se midió.
    r = {"gate": "gates", "verdict": "FAIL" if fail else "PASS",
         "checks": checks, "inputs": firmar(slides_html(carpeta) if only else html)}
    if only:
        r["scope"] = [only.replace(".html", "").replace(".png", "")]
    return r


FASES = {"brief": fase_brief, "copy": fase_copy, "blueprint": fase_blueprint,
         "prompt": fase_prompt, "raw": fase_raw, "gates": fase_gates}


def fase_lote(madre):
    """C12 · compuerta ENTRE carpetas: recorre los carrusel.json hermanos del lote.

    Corre sobre la carpeta MADRE, no sobre un carrusel: la repetición de ángulos vive
    entre hermanos y ninguna puerta por carpeta la puede ver. Por eso no forma parte de
    `all` (que corre por carpeta)."""
    import qa_lote
    r = qa_lote.correr(madre)

    # 6-ago-2026 · el ORDEN del lote, además de los ángulos. El director creativo: *"necesito que la skill
    # sea más rápida"*. Medido en el lote del 5-ago: los 4 carruseles generaron imágenes ANTES
    # de tener brief y blueprint (c1: 2,3 h antes), y eso costó 19 vueltas atrás a fases ya
    # pasadas. Una foto anterior al plan no ahorra tiempo: COMPRA trabajo, porque el plan
    # termina escribiéndose para justificarla. Relato: APRENDIZAJES.md §29.
    import orden_lote
    o = orden_lote.analizar(madre)
    for f in o["fuera_de_orden"]:
        r["checks"].append({
            "check": f"{f['pieza']} · plan antes que imagen",
            "ok": False,
            "detalle": (f"generó el {f['crudo']} y su {f['recibo']} se escribió "
                        f"{f['horas']} h después")})
        r.setdefault("fails", []).append(
            f"{f['pieza']}: imagen antes del plan (+{f['horas']} h)")
    if not o["fuera_de_orden"]:
        r["checks"].append({"check": "orden: plan antes que imagen", "ok": True, "detalle": ""})
    if o["vueltas"]:
        d = f"{len(o['vueltas'])} vueltas atrás a fases ya pasadas (el lote corrió en filas)"
        r["checks"].append({"check": "orden: vueltas atrás", "ok": None, "detalle": d})
        r.setdefault("warns", []).append(d)
    if o["recibos"] and o["pct_en_lote"] < 50:
        d = (f"solo {o['pct_en_lote']}% del trabajo se corrió en lote — pipeline en FILAS "
             f"en vez de COLUMNAS (una fase para todas las piezas)")
        r["checks"].append({"check": "orden: columnas vs filas", "ok": None, "detalle": d})
        r.setdefault("warns", []).append(d)
    if o["fuera_de_orden"]:
        r["verdict"] = "FAIL"

    r["inputs"] = firmar(glob.glob(os.path.join(madre, "*", "carrusel.json")))
    return r


# ─────────────────────────────────────────────────────────────── init ──
AYUDA = {
    "cliente":   "carpeta exacta de brand-brain/ (marca-estudio | marca-pilates | crema | "
                 "marca-app | verde | marca-cosmetica | "
                 "marca-deportiva | marca-servicios | agencia)",
    "linea":     "la línea/sede en palabras — «Marca Crema» son 4 marcas distintas y el apellido NO "
                 "desambigua",
    "objetivo":  "guardados | comentarios | ventas | confianza | cercanía",
    "formato":   "familia y formato de references/tipos-y-formatos.md",
    "framework": "PAS | AIDA | BAB | PPPP | listicle | contrarian",
    "segmento":  "el público real — la mediana del panel ciego se calcula SOLO sobre él",
    "angulo":    "la idea central del carrusel en una línea (de la Fase −1 o del Paso A). "
                 "La compuerta de lote FAIL si dos carruseles hermanos la repiten",
    "cta":       "el CTA de ESA línea (lo fija el brand-brain, no se inventa)",
    "brand":     "clave de paleta en templates/styles.css",
    "zone":      "l | r | top | bot — dónde va el texto. Rotar entre slides vecinas",
    "v":         "top | mid | bot — altura del bloque dentro de la zona",
    "fuente":    "real | generada | frame — se declara por slide (corrección el director creativo jul-2026)",
    "visual_need": "qué debe DEMOSTRAR la foto, no qué se ve en ella",
}

PLANTILLA_BRIEF = """# Brief — {nombre}

> Andamio creado por `verify.py init`. Rellenar y correr `verify.py brief`.
> Este archivo en prosa es obligatorio (RUBRIC F1); `carrusel.json` es su versión de máquina.
> Los dos tienen que decir lo mismo.

## Qué y para quién
- **Cliente / línea:** (Marca Bronce ≠ Pilates ≠ Online ≠ App — decidirlo ACÁ)
- **Objetivo:** (guardados / comentarios / ventas / confianza / cercanía)
- **Segmento:**
- **Ángulo (idea central en una línea):** (de la Fase −1 o del Paso A de COPY.md — la compuerta de lote FAIL si otro carrusel hermano lo repite)
- **Formato y framework:** (Fase 0, con references/tipos-y-formatos.md)

## De dónde sale la marca
- **brand-brain leído:** `brand-brain/<cliente>/` ← poner la ruta que se leyó de verdad
- **CTA de esta línea:**
- **`ejemplos-gusto/` revisados:** sí / no existe

## Imágenes  `[✓ DIRECTOR: preguntarle la fuente ANTES de generar]`
- **Reparto acordado, slide por slide:**
- **Sede/lugar real:**
- **Disciplina ↔ línea verificada:**
- **Persona / Reference Element:**

## Decisiones y desvíos
- (checkpoints saltados con permiso, cambios de plan, lo que se resolvió al vuelo)
"""


def _fuente_cercana(carpeta):
    """Busca una .woff2/.ttf real cerca de la carpeta y devuelve la ruta RELATIVA a usar.

    Importa más de lo que parece: sin `tipografia.font` la fase `gates` no corre `qa_lines`
    (deja el check en WARN) y el motor mide con un proxy Arial, más angosto que Oswald o
    Montserrat — las líneas se pasan de la caja verificada y terminan sobre el sujeto.
    """
    for rel in ("assets", "../assets", "../../assets", "."):
        d = os.path.normpath(os.path.join(carpeta, rel))
        for ext in ("*.woff2", "*.ttf", "*.otf"):
            f = sorted(glob.glob(os.path.join(d, ext)))
            if f:
                return os.path.join(rel, os.path.basename(f[0])).replace("./", "")
    # Nada cerca: la del propio skill, en absoluto para que resuelva igual
    f = sorted(glob.glob(os.path.join(AQUI, "assets", "*.woff2")))
    return f[0] if f else ""


def cmd_init(carpeta, n_slides=5, forzar=False):
    os.makedirs(carpeta, exist_ok=True)
    sp = os.path.join(carpeta, "carrusel.json")
    if os.path.exists(sp) and not forzar:
        print(f"Ya existe {sp} — no lo piso.\n"
              f"Si querés regenerarlo desde cero: verify.py init {carpeta} --force")
        return 1

    font = _fuente_cercana(carpeta)
    slides = []
    for i in range(1, n_slides + 1):
        slides.append({
            "n": i,
            "eyebrow": "",
            "titulo": "",
            "sub": "",
            "zone": ["l", "r"][(i - 1) % 2],   # rotar zona entre slides vecinas
            "v": "mid",
            "visual_need": "",
            "foto": f"raw/s-{i:02d}.png",
            "fuente": "",
            # la portada es el héroe del carrusel: el motor no la deja bajar de HERO (90px)
            # cuando angosta o achica el título (auditoría T7)
            **({"hero": True} if i == 1 else {}),
        })

    spec = {
        "_ayuda": AYUDA,
        "carrusel": os.path.basename(os.path.abspath(carpeta)),
        "cliente": "", "linea": "", "objetivo": "", "formato": "", "framework": "",
        "segmento": "", "angulo": "", "cta": "", "brand": "",
        # De dónde salió la idea (Fase −1, 6-ago-2026). Ruta al archivo de ideas
        # + la celda de la grilla, o "pedido-directo: <lo que pidió el director creativo>".
        # Vacío es FAIL solo en LOTE (≥2 carruseles hermanos): una pieza suelta no
        # necesita embudo, un lote sí — es donde el generador colapsa en una forma.
        "procedencia": "",
        "tipografia": {"font": font, "weight": 700, "size": 92,
                       "width": 640, "hero": 100, "tracking": -0.02},
        "hook_variantes": [],
        "primary_text": "",
        "slides": slides,
    }
    json.dump(spec, open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    bp = os.path.join(carpeta, "_brief.md")
    brief_nuevo = not os.path.exists(bp)
    if brief_nuevo:
        open(bp, "w", encoding="utf-8").write(
            PLANTILLA_BRIEF.format(nombre=os.path.basename(os.path.abspath(carpeta))))

    marcar_activo(carpeta)
    print(f"✅ carrusel.json     {n_slides} slides, campos obligatorios VACÍOS a propósito")
    print(f"{'✅' if brief_nuevo else '·  '} _brief.md         "
          f"{'plantilla nueva' if brief_nuevo else 'ya existía, no lo toqué'}")
    if font:
        print(f"✅ tipografia.font   {font}")
    else:
        print("⚠️  tipografia.font  VACÍO — sin esto qa_lines no corre y el motor mide con un "
              "proxy Arial (más angosto): las líneas se pasan de la caja")
    print("\nAhora (Fase 1): rellenar los campos obligatorios (cliente, línea, objetivo, "
          "formato, framework, segmento, ANGULO, cta) y el reparto de fotos, y después:\n"
          f"  /usr/local/bin/python3 templates/verify.py brief {carpeta}")
    return 0


def escribir(carpeta, r, warn_ok=None):
    """Escribe el recibo firmado y le deriva la semántica fails/warns (3-ago-2026).

    `verdict` queda en PASS/FAIL — es lo que lee el hook carrusel-gate, y PASS_CON_WARNS
    tiene que pasar la puerta igual. El matiz va en `status` + las listas `fails`/`warns`:
    0 fails + N warns → PASS_CON_WARNS. Con --warn-ok la razón queda grabada; sin el flag
    el recibo dice warns_sin_razon: true y la Fase 7 (jueces) tiene que revisarlos."""
    r["by"] = "script"
    r["runner"] = "verify.py"
    r["ts"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    # Firma mínima garantizada (10-ago-2026): algunos gates pueden quedarse sin `inputs`
    # legítimamente (el gate `raw` de un carrusel 100% generado no tiene fotos crudas), y un
    # recibo en PASS con `inputs` vacío no le daba nada que verificar al hook. El spec SIEMPRE
    # existe en una carpeta gobernada, así que se firma él: así todo PASS lleva al menos una
    # firma y `carrusel-gate.py` puede exigirla sin falsos positivos.
    if r.get("verdict") == "PASS" and not r.get("inputs"):
        spec = os.path.join(carpeta, "carrusel.json")
        if os.path.isfile(spec):
            r["inputs"] = firmar([spec])
    fails = [c["check"] for c in r.get("checks", []) if c["ok"] is False]
    warns = [c["check"] for c in r.get("checks", []) if c["ok"] is None]
    r["fails"] = fails
    r["warns"] = warns
    r["status"] = "FAIL" if fails else ("PASS_CON_WARNS" if warns else "PASS")
    if warns:
        if warn_ok:
            r["warn_ok"] = warn_ok
        else:
            r["warns_sin_razon"] = True
    p = os.path.join(carpeta, RECIBO[r["gate"]])
    json.dump(r, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return p


def marcar_activo(carpeta):
    """Deja el puntero que usan las puertas sin ruta en su tool_input (generate_image)."""
    try:
        d = os.path.join(REPO, ".claude")
        if os.path.isdir(d):
            open(os.path.join(d, ".carrusel-activo"), "w").write(os.path.abspath(carpeta))
    except OSError:
        pass


def main(argv):
    if len(argv) < 2 or argv[0] not in list(FASES) + ["all", "init", "thumbs", "lote"]:
        print(__doc__)
        return 2
    fase = argv[0]

    # flags: --slides N (init) · --force (init) · --only s-03 (raw/gates/all) ·
    # --warn-ok "razón" (gates/all). La carpeta es el primer argumento posicional tras la fase.
    flags_con_valor = ("--slides", "--only", "--warn-ok")
    pos = [a for i, a in enumerate(argv[1:])
           if not a.startswith("--") and (i == 0 or argv[1:][i - 1] not in flags_con_valor)]
    if not pos:
        print(__doc__)
        return 2
    carpeta = pos[0]
    only = warn_ok = None
    for i, a in enumerate(argv):
        if a == "--only" and i + 1 < len(argv):
            only = argv[i + 1].replace(".html", "").replace(".png", "")
        if a == "--warn-ok" and i + 1 < len(argv):
            warn_ok = argv[i + 1]

    if fase == "init":
        n = 5
        for i, a in enumerate(argv):
            if a == "--slides" and i + 1 < len(argv):
                n = max(2, min(10, int(argv[i + 1])))
        return cmd_init(carpeta, n, forzar="--force" in argv)

    if not os.path.isdir(carpeta):
        print(f"FAIL: no existe la carpeta {carpeta}")
        return 2

    if fase == "thumbs":
        ok, res = generar_thumbs(carpeta, filtrar(
            sorted(glob.glob(os.path.join(carpeta, "s-*.png"))), only))
        m = "PASS" if ok else "WARN"
        print(f"{m}  {res}")
        return 0 if ok else 1

    if fase == "lote":
        # corre sobre la carpeta MADRE del lote: no exige carrusel.json propio
        r = fase_lote(carpeta)
        p = escribir(carpeta, r, warn_ok=warn_ok)
        print(f"\n── LOTE ──")
        for c in r["checks"]:
            m = "PASS" if c["ok"] else "FAIL" if c["ok"] is False else "WARN"
            print(f"  {m}  {c['check']:<48} {c['detalle']}")
        extra = f" · status {r['status']}" if r["status"] != r["verdict"] else ""
        if r.get("warn_ok"):
            extra += f" · warn-ok: «{r['warn_ok']}»"
        elif r.get("warns_sin_razon"):
            extra += " · warns_sin_razon (se revisan antes de generar)"
        print(f"  → {r['verdict']}{extra}  ({os.path.basename(p)})")
        return 1 if r["verdict"] == "FAIL" else 0

    if not os.path.exists(os.path.join(carpeta, "carrusel.json")):
        print(f"⛔ falta carrusel.json en {carpeta} — es el spec que leen el motor, estas "
              f"compuertas y las 4 puertas del hook.\n"
              f"   Creá el andamio:  /usr/local/bin/python3 templates/verify.py init {carpeta}")
        return 2
    marcar_activo(carpeta)
    fases = list(FASES) if fase == "all" else [fase]
    peor = 0
    for f in fases:
        r = FASES[f](carpeta, only) if f in ("raw", "gates") else FASES[f](carpeta)
        p = escribir(carpeta, r, warn_ok=warn_ok)
        print(f"\n── {f.upper()} ──")
        for c in r["checks"]:
            m = "PASS" if c["ok"] else "FAIL" if c["ok"] is False else "WARN"
            print(f"  {m}  {c['check']:<48} {c['detalle']}")
        extra = f" · status {r['status']}" if r["status"] != r["verdict"] else ""
        if r.get("warn_ok"):
            extra += f" · warn-ok: «{r['warn_ok']}»"
        elif r.get("warns_sin_razon"):
            extra += " · warns_sin_razon (Fase 7 los revisa)"
        if r.get("scope"):
            extra += f" · scope {r['scope']}"
        print(f"  → {r['verdict']}{extra}  ({os.path.basename(p)})")
        if r["verdict"] == "FAIL":
            peor = 1
            if fase == "all":
                print(f"\n⛔ {f} en FAIL — se corta acá: las fases siguientes miden sobre "
                      f"algo que ya hay que corregir.")
                break
    return peor


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
