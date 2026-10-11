#!/usr/bin/env /usr/local/bin/python3
"""
dorado.py — EL CASO DORADO DEL MOTOR (5-ago-2026).

    dorado.py fijar      → recompone el caso y CONGELA el resultado como referencia
    dorado.py verificar  → recompone y compara contra la referencia congelada

POR QUÉ EXISTE
El 5 de agosto toqué `engine.py` / `styles.css` / `qa_lines.py` tres veces en un día y cada vez
rompí algo distinto:

  1. el destaque `<em>` en los titulares rompió DOS mediciones (el ancho de línea y el conteo
     de caracteres contaban los tags como texto);
  2. sincronizar `templates/styles.css` sobre la carpeta borró el preset de marca de Marca Verde,
     y el carrusel salió con los colores de otro cliente;
  3. la perilla `zoom` llegaba al análisis pero no al render: `object-fit:cover` mostraba la
     foto entera igual, así que el mapa medía una ventana que el navegador no pintaba.

**Las tres pasaron las siete compuertas en verde.** No es que las compuertas fallaran: miden si
la slide está BIEN (contraste, tamaños, overflow, zona libre), y las tres seguían estando bien
— estaban bien de otra manera. Lo que no existía era algo que dijera *«esto cambió respecto a
ayer, y vos no pediste que cambiara»*. Eso es un test de regresión, y no había ninguno: la
carpeta `evals/` del cerebro tiene tres casos de enrutamiento y cero del motor.

Quien las cazó fue el ojo del director creativo, horas después, mirando el PNG. Ese es el bucle caro: yo
declaro listo → él mira → hay que volver atrás. Cada vuelta son un re-render, siete gates de
nuevo y una lectura más. c1 y c2 llegaron a "gates en verde" CINCO veces.

CÓMO FUNCIONA
El caso no usa fotos de clientes: se genera solo, con una imagen sintética determinista
(gradiente + un "sujeto" con su máscara alfa). Así el test corre en cualquier máquina, no mete
media al repo y no depende de que exista tal o cual carpeta de trabajo.

Compara dos cosas, porque fallan distinto:

  · **NÚMEROS** (`_build-report.json`): tamaño de fuente, zona asignada, crop, zoom, alfa del
    velo. Exactos. Acá aparecen los bugs 1 y 3 — el motor decidió otra cosa.
  · **PÍXELES** (PNG a 360px, el mismo tamaño del thumbnail que ya miran los jueces): diferencia
    media por canal. Acá aparece el bug 2 — el motor decidió lo mismo y lo pintó distinto.

Un cambio deliberado NO es una falla: se corre `fijar`, queda la referencia nueva con fecha, y
el diff del git muestra qué se movió. Lo que el test impide es que se mueva **sin que nadie se
entere**.
"""
import sys, os, json, glob, subprocess, shutil, time

AQUI = os.path.dirname(os.path.abspath(__file__))
CASO = os.path.join(AQUI, "dorado")
TRABAJO = os.path.join(CASO, "_corrida")
REF = os.path.join(CASO, "referencia")
PY = "/usr/local/bin/python3"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Tolerancias. No son cero a propósito: Chrome no es bit-a-bit reproducible entre versiones
# (antialiasing del texto). Se calibraron para que las tres regresiones reales del 5-ago las
# cruzaran con margen — el cambio de preset de marca dio 14.8 de diferencia media.
DIF_MEDIA_MAX = 2.0     # diferencia media por canal, 0-255, sobre el PNG a 360px
DIF_PICO_MIN = 0.004    # fracción de píxeles con diferencia > 24: por encima, cambió el diseño

SPEC = {
    "cliente": "_dorado", "linea": "Caso dorado del motor", "objetivo": "regresion",
    "formato": "anuncio", "framework": "PAS", "segmento": "test",
    "angulo": "caso congelado para detectar que el motor cambió sin que nadie lo pidiera",
    "cta": "Probar el motor", "brand": "verde", "canvas": "1:1",
    "presupuesto_imagenes": 0,
    "tipografia": {"font": "assets/Montserrat.woff2", "weight": 800, "size": 92},
    "hook_variantes": ["Caso dorado"], "primary_text": "Caso dorado del motor.",
    "slides": [
        {"n": 1, "titulo": "Ahorra <em>tiempo y dinero</em> con el motor.",
         "eyebrow": "CASO DORADO", "cta": "PROBAR EL MOTOR",
         "zone": "top", "v": "mid", "hero": True, "zoom": 1.5, "posx": 1.0, "posy": 1.0,
         "size": 120, "visual_need": "sujeto abajo a la derecha, hueco arriba",
         "foto": "raw/s-01.png", "fuente": "sintetica"},
        {"n": 2, "titulo": "Una línea larga que obliga al motor a repartir en varios renglones.",
         "sub": "Y una bajada que ocupa su parte de la caja.", "eyebrow": "DOS",
         "zone": "l", "v": "mid", "visual_need": "sujeto a la derecha, columna izquierda libre",
         "foto": "raw/s-02.png", "fuente": "sintetica"},
        {"n": 3, "titulo": "Cierre que <em>nombra la marca</em>.", "eyebrow": "TRES",
         "cta": "PROBAR EL MOTOR", "zone": "bot", "v": "low",
         "visual_need": "sujeto arriba, franja inferior libre",
         "foto": "raw/s-03.png", "fuente": "sintetica"},
    ],
}


def foto_sintetica(path_foto, path_cutout, sujeto):
    """Imagen determinista de 2048² + su máscara alfa. Sin PIL.random, sin fecha, sin red:
    dos corridas en máquinas distintas tienen que dar el MISMO archivo, o el test compara
    ruido."""
    from PIL import Image, ImageDraw
    import numpy as np
    W = 2048
    y, x = np.mgrid[0:W, 0:W].astype(np.float32) / W
    # gradiente diagonal + una "luz" para que el mapa de foco tenga algo que encontrar
    luz = np.exp(-(((x - .72) ** 2 + (y - .28) ** 2) / 0.05))
    r = (28 + 60 * x + 150 * luz).clip(0, 255)
    g = (52 + 90 * y + 140 * luz).clip(0, 255)
    b = (34 + 40 * (1 - x) + 120 * luz).clip(0, 255)
    img = Image.fromarray(np.dstack([r, g, b]).astype(np.uint8), "RGB")

    # el "sujeto": una cápsula opaca donde diga `sujeto` = (cx, cy, rw, rh) en fracción
    cx, cy, rw, rh = sujeto
    d = ImageDraw.Draw(img)
    caja = [int((cx - rw) * W), int((cy - rh) * W), int((cx + rw) * W), int((cy + rh) * W)]
    d.rounded_rectangle(caja, radius=int(.16 * W), fill=(232, 226, 208))
    cab = int(.10 * W)
    d.ellipse([int(cx * W) - cab, caja[1] - int(1.4 * cab),
               int(cx * W) + cab, caja[1] + int(.6 * cab)], fill=(232, 226, 208))
    img.save(path_foto)

    m = Image.new("L", (W, W), 0)
    dm = ImageDraw.Draw(m)
    dm.rounded_rectangle(caja, radius=int(.16 * W), fill=255)
    dm.ellipse([int(cx * W) - cab, caja[1] - int(1.4 * cab),
                int(cx * W) + cab, caja[1] + int(.6 * cab)], fill=255)
    out = img.convert("RGBA")
    out.putalpha(m)
    out.save(path_cutout)


SUJETOS = [(0.78, 0.72, 0.17, 0.24),   # abajo a la derecha (el caso de la portada con zoom)
           (0.74, 0.55, 0.16, 0.28),   # a la derecha, columna izquierda libre
           (0.50, 0.30, 0.18, 0.22)]   # arriba al centro, franja inferior libre


def montar():
    """Deja `_corrida/` con el spec, los crudos sintéticos y los assets que pide el motor."""
    shutil.rmtree(TRABAJO, ignore_errors=True)
    os.makedirs(os.path.join(TRABAJO, "raw"), exist_ok=True)
    os.makedirs(os.path.join(TRABAJO, "assets"), exist_ok=True)
    for i, s in enumerate(SUJETOS, 1):
        foto_sintetica(os.path.join(TRABAJO, "raw", f"s-{i:02d}.png"),
                       os.path.join(TRABAJO, "raw", f"s-{i:02d}-cutout.png"), s)
    for f in glob.glob(os.path.join(AQUI, "assets", "*")):
        if os.path.isfile(f):
            shutil.copy2(f, os.path.join(TRABAJO, "assets", os.path.basename(f)))
    json.dump(SPEC, open(os.path.join(TRABAJO, "carrusel.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)


def componer():
    """engine.py + Chrome. Devuelve (ok, log)."""
    p = subprocess.run([PY, os.path.join(AQUI, "engine.py"), TRABAJO],
                       capture_output=True, text=True)
    log = (p.stdout or "") + (p.stderr or "")
    if p.returncode != 0:
        return False, f"engine.py salió {p.returncode}\n{log[-1500:]}"
    if not os.path.exists(CHROME):
        return False, f"no está Chrome en {CHROME} — el caso dorado necesita el render real"
    for h in sorted(glob.glob(os.path.join(TRABAJO, "s-*.html"))):
        png = h[:-5] + ".png"
        r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                            "--force-device-scale-factor=1", "--window-size=1080,1080",
                            "--virtual-time-budget=4000", f"--screenshot={png}",
                            f"file://{os.path.abspath(h)}"],
                           capture_output=True, text=True)
        if not os.path.exists(png):
            return False, f"Chrome no dejó {os.path.basename(png)}\n{(r.stderr or '')[-800:]}"
    return True, log


def miniaturas(destino):
    """Los PNG a 360px — el mismo tamaño del thumbnail que ya miran los jueces. A tamaño
    completo el archivo pesa 8× y no caza nada que a 360 no se vea."""
    from PIL import Image
    os.makedirs(destino, exist_ok=True)
    fuera = []
    for png in sorted(glob.glob(os.path.join(TRABAJO, "s-*.png"))):
        if os.path.basename(png).startswith("_"):
            continue
        d = os.path.join(destino, os.path.basename(png))
        Image.open(png).convert("RGB").resize((360, 360), Image.LANCZOS).save(d)
        fuera.append(d)
    return fuera


def numeros():
    """Los campos del _build-report.json que describen una DECISIÓN del motor.

    Se filtra a propósito: el reporte trae rutas absolutas y timestamps que cambian en cada
    corrida y en cada máquina. Un test que compara eso da rojo siempre y a la semana lo apaga
    alguien."""
    r = json.load(open(os.path.join(TRABAJO, "_build-report.json"), encoding="utf-8"))
    INTERESA = ("size", "font_size", "zona", "zone", "crop", "zoom", "alfa", "alpha", "velo",
                "lineas", "lines", "ancho", "width", "reencuadr", "x", "y", "w", "h",
                "columna", "piso", "escala", "scale", "brand", "titulo_px", "sub_px")

    def podar(o, prof=0):
        if prof > 6:
            return None
        if isinstance(o, dict):
            d = {}
            for k, v in o.items():
                kl = str(k).lower()
                if any(t in kl for t in ("path", "ruta", "file", "ts", "time", "fecha", "hash")):
                    continue
                pv = podar(v, prof + 1)
                if isinstance(v, (int, float, bool)) and any(t in kl for t in INTERESA):
                    d[k] = round(v, 3) if isinstance(v, float) else v
                elif isinstance(v, str) and any(t in kl for t in INTERESA):
                    d[k] = v
                elif pv:
                    d[k] = pv
            return d or None
        if isinstance(o, list):
            l = [podar(v, prof + 1) for v in o]
            l = [v for v in l if v]
            return l or None
        return None
    return podar(r) or {}


def comparar_png(a, b):
    from PIL import Image, ImageChops
    import numpy as np
    A = np.asarray(Image.open(a).convert("RGB"), dtype=np.int16)
    B = np.asarray(Image.open(b).convert("RGB"), dtype=np.int16)
    if A.shape != B.shape:
        return 255.0, 1.0
    D = np.abs(A - B)
    return float(D.mean()), float((D.max(axis=2) > 24).mean())


def cmd_fijar():
    montar()
    ok, log = componer()
    if not ok:
        print(f"FAIL  no se pudo componer el caso dorado:\n{log}")
        return 2
    shutil.rmtree(REF, ignore_errors=True)
    pngs = miniaturas(REF)
    json.dump(numeros(), open(os.path.join(REF, "_numeros.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2, sort_keys=True)
    open(os.path.join(REF, "_fijado.txt"), "w").write(
        f"{time.strftime('%Y-%m-%dT%H:%M:%S')}\n"
        f"Referencia congelada del motor. Si `dorado.py verificar` da FAIL y el cambio ERA\n"
        f"a propósito, se vuelve a correr `fijar` y el diff del git muestra qué se movió.\n")
    print(f"✅ referencia congelada · {len(pngs)} slides a 360px + _numeros.json")
    print(f"   {os.path.relpath(REF, os.path.dirname(AQUI))}")
    print("\n   A partir de acá, después de CUALQUIER cambio a engine.py / styles.css /")
    print("   photo_map.py / textfit.py:  dorado.py verificar")
    return 0


def cmd_verificar():
    if not os.path.isdir(REF) or not glob.glob(os.path.join(REF, "s-*.png")):
        print("⚠️  no hay referencia congelada todavía.\n"
              "    Corré:  /usr/local/bin/python3 templates/dorado.py fijar\n"
              "    (con el motor en el estado que HOY se considera correcto)")
        return 2
    montar()
    ok, log = componer()
    if not ok:
        print(f"FAIL  el motor ya ni compone el caso dorado:\n{log}")
        return 1
    actual = os.path.join(CASO, "_actual")
    shutil.rmtree(actual, ignore_errors=True)
    miniaturas(actual)

    fallas, avisos = [], []
    print("\n── CASO DORADO ──")
    for r in sorted(glob.glob(os.path.join(REF, "s-*.png"))):
        n = os.path.basename(r)
        a = os.path.join(actual, n)
        if not os.path.exists(a):
            fallas.append(f"{n}: el motor ya no la genera")
            print(f"  FAIL  {n:<12} no se generó")
            continue
        media, pico = comparar_png(r, a)
        mal = media > DIF_MEDIA_MAX or pico > DIF_PICO_MIN
        print(f"  {'FAIL' if mal else 'PASS'}  {n:<12} dif media {media:5.2f} "
              f"(max {DIF_MEDIA_MAX}) · píxeles cambiados {pico:.2%} (max {DIF_PICO_MIN:.2%})")
        if mal:
            fallas.append(f"{n}: el PNG cambió (dif media {media:.2f}, {pico:.1%} de píxeles)")

    try:
        viejo = json.load(open(os.path.join(REF, "_numeros.json"), encoding="utf-8"))
    except Exception:
        viejo = {}
    nuevo = numeros()
    v, n2 = json.dumps(viejo, sort_keys=True), json.dumps(nuevo, sort_keys=True)
    if v != n2:
        p = os.path.join(CASO, "_numeros-actual.json")
        json.dump(nuevo, open(p, "w", encoding="utf-8"), ensure_ascii=False,
                  indent=2, sort_keys=True)
        fallas.append("las decisiones del motor cambiaron (_build-report)")
        print(f"  FAIL  {'números':<12} el motor decide distinto — "
              f"diff: {os.path.relpath(p, os.path.dirname(AQUI))} vs referencia/_numeros.json")
    else:
        print(f"  PASS  {'números':<12} el motor decide exactamente lo mismo")

    if fallas:
        print(f"\n⛔ EL MOTOR CAMBIÓ ({len(fallas)}):")
        for f in fallas:
            print(f"   · {f}")
        print("\n   Si el cambio NO era a propósito: es una regresión, arreglala antes de "
              "seguir\n   produciendo — las compuertas no la van a cazar (miden si está BIEN, "
              "no si CAMBIÓ).\n   Si SÍ era a propósito:  dorado.py fijar  (queda con fecha y "
              "el git muestra qué).")
        return 1
    print("\n✅ el motor compone igual que la referencia congelada "
          f"({open(os.path.join(REF, '_fijado.txt')).readline().strip()})")
    return 0


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] not in ("fijar", "verificar"):
        print(__doc__)
        sys.exit(2)
    sys.exit(cmd_fijar() if a[0] == "fijar" else cmd_verificar())
