#!/usr/bin/env /usr/local/bin/python3
"""
engine.py — EL MOTOR CANÓNICO (31-jul-2026). Un solo lugar donde se arregla la composición.

Por qué existe. La composición se reescribía en cada trabajo: se encontraron SIETE `build.py`
distintos en el repo. Tres de ellos —incluido el del test que reprobó por unanimidad el
29-jul— **no llamaban a `photo_map` ni una vez**: tomaban la zona que declaraba el spec, le
ponían el velo y renderizaban A CIEGAS, sin preguntar nunca dónde estaba la persona. Por eso
"el texto queda sobre la cara" pasaba en unos trabajos y en otros no: dependía de con qué copia
del motor se había armado.

Las tres capas del arreglo, todas acá adentro:

  1 · SE VALIDA EL HUECO   — antes de componer se comprueba que la zona planificada esté
      realmente libre (máscara de Vision + PhotoMap).
  2 · EL MAPA ASIGNA       — si la zona planificada está ocupada, NO se fuerza el texto: se
      consulta el mapa y se reubica al hueco real. Si ninguno sirve, se REENCUADRA la foto
      (framer). El orden es fijo: reencuadrar → angostar la columna → bajar el título hasta
      su piso → cambiar de foto. **Nunca un panel opaco ni "subir el velo" como remedio**
      (RUBRIC E10.b: 6 slides quedaron medio negras por usarlo de red de seguridad ante
      roces del 3%; el velo se MIDE, no se sube).
  3 · OCLUSIÓN POR MÁSCARA — el texto se pinta y ENCIMA se pega el recorte de la persona. El
      texto pasa por detrás del hombro. "El texto tapa la cara" deja de ser un error que hay
      que cazar y pasa a ser IMPOSIBLE POR CONSTRUCCIÓN (composicion-y-tipografia §4.5).

Además: velo adaptativo medido POR LÍNEA (no por bloque — el p80 del bloque miente), quiebres
balanceados con la fuente real, y MAPCHECK fail-closed sobre los MISMOS boxes que se renderizan.

    engine.py <carpeta>              # todas las slides
    engine.py <carpeta> --slide 3    # una sola
    engine.py <carpeta> --debug      # + _map-NN.png con el mapa de zonas dibujado
"""
import sys, os, json, subprocess, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

from PIL import Image
import photo_map as PM
import textfit
try:
    import montwidth as MW
except Exception:
    MW = None

from constantes import (CANVAS, CANVAS_W, CANVAS_H, MARGEN, MIN_ANCHO_COL,
                        MAX_LINEAS_TITULO, MAX_LINEAS_OK,
                        LIMB_TOL_TEXTO, MARGEN_SEGURO, PISO_TITULO_SEC, HERO)
CUTOUT = os.path.expanduser("~/bin/cutout")

# Lienzo por spec: 1:1 (1080×1080) por defecto — regla de la casa, reconfirmada por
# el director creativo el 3-ago-2026 (se revierte el default 4:5 de la oleada 2.5A). El spec puede
# pedir "canvas": "4:5" (1080×1350) como opción excepcional (el brand-brain manda). El
# ANCHO no cambia nunca: los pisos tipográficos se derivan de CANVAS_W y por eso no se tocan.
LIENZOS = {"1:1": (CANVAS_W, CANVAS_W), "4:5": (CANVAS_W, 1350)}


# Presets cuya tipografía es OSCURA sobre lienzo CLARO. Para ellos el mapa de riesgo del
# texto se invierte: el peligro no es el foco de luz (regla pensada para tinta blanca sobre
# foto) sino la mancha oscura. Ver photo_map.foco_para(). Relato: APRENDIZAJES.md §35.
BRANDS_TINTA_OSCURA = {"verde-claro", "crema-claro"}


def tinta_de(spec):
    return "dark" if spec.get("brand") in BRANDS_TINTA_OSCURA else "light"


def lienzo_de(spec):
    """→ (ancho, alto) del lienzo de ESTE carrusel. Default 1:1; override por spec."""
    clave = str(spec.get("canvas", "1:1")).strip()
    if clave not in LIENZOS:
        print(f"⚠️  canvas «{clave}» desconocido — usando 1:1 (opciones: {', '.join(LIENZOS)})")
        clave = "1:1"
    return LIENZOS[clave]

# Caja del bloque de texto por zona (x, ancho). Coherente con qa_blueprint.CAJAS y con styles.css.
COLUMNAS = {"l": (MARGEN, 560), "r": (CANVAS - MARGEN - 560, 560),
            "top": (MARGEN, CANVAS - 2 * MARGEN), "bot": (MARGEN, CANVAS - 2 * MARGEN),
            "cc": (MARGEN + 96, CANVAS - 2 * (MARGEN + 96))}
ANCLA_Y = {"top": 150, "mid": None, "bot": None}     # None = calculado con el alto real
GRADIENTE = {"l": "g-left", "r": "g-right", "top": "g-top", "bot": "g-bottom", "cc": "g-bottom"}
# Orden en que el mapa propone alternativas cuando la zona planificada está ocupada.
ALTERNATIVAS = ["l", "r", "top", "bot", "cc"]


# ───────────────────────────────────────────────────────── medición de texto ──
# Fuente por defecto = la del motor. Antes había que declararla en cada carrusel y, si no lo
# hacías (nadie lo hacía), TODO se medía con un proxy Arial. Ahora el default ya es la real.
FONT_DEFAULT = os.path.join(AQUI, "assets", "Oswald.woff2")


import re as _re_tags
# Los titulares llevan destaque inline con <em> (regla el director creativo 5-ago-2026: se resalta el
# fragmento que importa, no el titular entero). Los tags NO son glifos: si se miden, «<em>»
# y «</em>» suman ~9 caracteres de ancho fantasma y el motor quiebra la línea antes de tiempo
# o baja el cuerpo sin necesidad. Se sacan ANTES de medir y se conservan en el HTML.
_TAG = _re_tags.compile(r"<[^>]+>")


def sin_tags(t):
    return _TAG.sub("", t or "")


def medidor(font_path, weight, tracking):
    """→ (f(texto, size_px) -> ancho px, ¿es la fuente real?)

    Medir con la fuente REAL no es un lujo: es lo que decide si el texto entra en el hueco
    limpio o se monta sobre la persona. El proxy no solo es impreciso, es impreciso en una
    dirección que NO se puede saber de antemano — Arial SOBREESTIMA a Oswald (condensada) en
    ~20% y SUBESTIMA a Montserrat 800 (ancha). Por eso el fallback avisa fuerte."""
    for ruta in (font_path, FONT_DEFAULT):
        if MW and ruta and os.path.exists(ruta) and MW.available():
            def m(t, size, _r=ruta):
                return MW.width(sin_tags(t), size, _r, weight=weight, tracking_em=tracking)
            return m, True
    from PIL import ImageFont
    proxy = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

    def m(t, size):
        t = sin_tags(t)
        try:
            return ImageFont.truetype(proxy, int(size)).getlength(t)
        except OSError:
            return len(t) * size * 0.55
    return m, False


import re as _re

# Corte de frase: punto, interrogación o exclamación que CIERRA una frase (va seguido de
# espacio y de algo que empieza en mayúscula, o es el final del texto).
# El `(?:<[^>]+>)?` deja que la frase siguiente arranque con un tag de destaque
# («Le pides las boletas. <em>Él las prepara.</em>»): sin eso el lookahead veía «<» en vez de
# una mayúscula y las dos frases quedaban en el mismo renglón. (5-ago-2026)
_FIN_FRASE = _re.compile(r'(?<=[.!?])\s+(?=(?:<[^>]+>)?[¿¡"«(]?[A-ZÁÉÍÓÚÑ])')


def frases(texto):
    """Parte un titular en frases. «Una sala. Dieciséis formas» → ['Una sala.', 'Dieciséis formas']"""
    return [f.strip() for f in _FIN_FRASE.split(texto or "") if f.strip()]


def quebrar(texto, size, ancho, med):
    """Quiebres de titular.

    REGLA DURA (director creativo, 31-jul-2026): **después de un punto, la frase siguiente empieza en
    OTRA LÍNEA.** Que las líneas queden desparejas no es problema; que dos frases compartan
    renglón, sí. Por eso el texto se parte PRIMERO por frase y recién dentro de cada frase se
    balancea. Antes se balanceaba el titular entero como un solo bloque, así que un punto
    podía quedar a mitad de renglón («Una sala. Dieciséis / formas»).
    """
    salida = []
    for f in frases(texto) or [texto or ""]:
        pal = f.split()
        # WRAP CODICIOSO = el piso de calidad. Nunca puede salir peor que esto.
        # ⚠️ `textfit.balance_lines` considera "balanceado" un corte de UNA PALABRA POR LÍNEA
        # (todas las líneas miden parecido, así que su regla del 30% se cumple). Falla real
        # (31-jul-2026): "La / clase / de / hoy / ya / está / elegida." — 7 renglones de una
        # palabra, con TODOS los gates en verde porque cada línea cabe y nada se solapa.
        greedy, linea = [], ""
        for w in pal:
            cand = (linea + " " + w).strip()
            if linea and med(cand, size) > ancho:
                greedy.append(linea); linea = w
            else:
                linea = cand
        if linea:
            greedy.append(linea)
        try:
            bal = textfit.balance_lines(f, size, ancho, lambda t: med(t, size))
        except Exception:
            bal = greedy
        # se acepta el balanceado SOLO si no agrega renglones
        salida += bal if len(bal) <= len(greedy) else greedy
    return salida or [texto or ""]


# ─────────────────────────────────────────────────────────────── geometría ──
def caja_texto(zona, v, n_lineas, size, hay_sub, hay_eyebrow, hay_cta=False, alto_lienzo=CANVAS_H):
    x, w = COLUMNAS[zona]
    alto = int(n_lineas * size * 1.04)
    if hay_eyebrow:
        alto += 27 + 16
    if hay_sub:
        alto += int(36 * 1.4) + 18
    if hay_cta:
        alto += 30 + 32 + 24        # pastilla CTA: texto + padding vertical + gap
    if zona == "top" or v == "top":
        y = ANCLA_Y["top"]
    elif zona == "bot" or v == "bot":
        y = alto_lienzo - 112 - alto
    else:
        y = (alto_lienzo - alto) // 2
    return {"x": x, "y": max(48, y), "w": w, "h": alto}


def cajas_por_linea(box, n_lineas=None, size=None, hay_eyebrow=None):
    """Bandas horizontales que cubren TODO el bloque de texto — el velo se mide banda a banda.

    ⚠️ Antes solo cubría los renglones del TÍTULO. El eyebrow, la bajada y el CTA quedaban
    fuera de la medición, así que el velo se dimensionaba para el título y la bajada podía
    caer sobre una zona clara. Falla real (carrusel Estudio, 31-jul-2026): "De empezar de
    nuevo." dio 3.9:1 y el sub del cierre **1.3:1**, con el bloque en verde. Es el mismo error
    que composicion §6.3 ya documentaba —"se mide POR LÍNEA, no por bloque"— cometido a otra
    escala: por sub-bloque en vez de por bloque."""
    BANDA = 40
    n = max(1, int(round(box["h"] / BANDA)))
    h = box["h"] / n
    return [(box["x"], box["y"] + i * h, box["x"] + box["w"], box["y"] + (i + 1) * h)
            for i in range(n)]


# ─────────────────────────────────────────────────────────── piezas de foto ──
def preparar_foto(foto, carpeta):
    """→ (mask_path, cut_path). Los deja cacheados en _cut/ para no re-correr Vision."""
    d = os.path.join(carpeta, "_cut")
    os.makedirs(d, exist_ok=True)
    base = os.path.splitext(os.path.basename(foto))[0]
    mask = os.path.join(d, base + "-mask.png")
    cut = os.path.join(d, base + "-cut.png")
    for salida, extra in ((mask, ["--mask"]), (cut, [])):
        if not os.path.exists(salida) or os.path.getmtime(salida) < os.path.getmtime(foto):
            p = subprocess.run([CUTOUT, foto, salida] + extra, capture_output=True, text=True)
            if p.returncode != 0:
                return None, None      # foto sin sujeto (objeto/escena): no hay que ocluir
    return mask, cut


def recorte_lienzo(foto, crop, destino, dims):
    """Guarda el crop exacto al tamaño del lienzo — es sobre ESTO que se mide el velo."""
    im = Image.open(foto).convert("RGB")
    cx, cy, cw, ch = crop
    im.crop((cx, cy, cx + cw, cy + ch)).resize(dims).save(destino)
    return destino


def halo_del_sujeto(recorte, ancho=CANVAS_W, caja=None, min_fondo=0.42, max_sujeto=0.55):
    """→ el `<div class="halo">` detrás del sujeto, o "" si esta foto no lo admite.

    POR QUÉ EXISTE (5-ago-2026, corrección del director creativo: *"está muy plano el fondo, antes
    atrás ponías como una sombra, un verde más clarito"*). Tenía razón y se midió:

        glow medio en el fondo, en niveles (0-255), sobre el compuesto final
          lote julio 2026 .......... 7.9      ← el look que él recuerda
          corrida canónica 3-ago ... 6.6
          lote 5-ago (este) ........ 1.5      ← 10 de 20 slides completamente planas

    Dos causas encadenadas, ninguna decidida a propósito:
      1. el prompt de imagen pasó a prohibir el glow (*"NO radial glow, NO lighter band,
         NO horizontal seam"*) — la prohibición era para matar la BANDA/COSTURA que el
         modelo dibujaba, y se llevó puesto el glow de marca en la misma frase;
      2. el gradiente direccional (`.g-*`, hasta .96 de opacidad) aplana lo que quedaba:
         medido crudo 4.9 → compuesto 1.5, un 70% perdido en composición.

    Esta función arregla (2) de forma determinista y gratis. (1) se arregla en el prompt:
    `references/prompts-validados.md` §7.1 nunca dejó de pedir el glow.

    SOLO se pinta sobre fondo PLANO — mascota/ilustración sobre color de marca. Sobre una
    foto real no hay "fondo" que detectar y el centroide sería ruido: ahí devuelve "" y no
    se pinta nada. No es ornamento (RUBRIC E11.b): es luz aditiva que restituye el fondo de
    marca, no rellena una banda vacía ni satisface una métrica de densidad.
    """
    import numpy as np
    a = np.asarray(Image.open(recorte).convert("RGB").resize((256, 256))).astype(np.float32)
    esquinas = np.concatenate([a[:16, :16].reshape(-1, 3), a[:16, -16:].reshape(-1, 3),
                               a[-16:, :16].reshape(-1, 3), a[-16:, -16:].reshape(-1, 3)])
    fondo = np.median(esquinas, axis=0)
    d = np.sqrt(((a - fondo) ** 2).sum(axis=2))
    es_fondo, es_sujeto = d <= 26, d > 60
    # Fondo plano de verdad: casi la mitad del cuadro dentro de la tolerancia y un sujeto
    # que ocupa una fracción razonable. Una foto real no pasa ninguna de las dos.
    if es_fondo.mean() < min_fondo or not (0.015 < es_sujeto.mean() < max_sujeto):
        return ""
    ys, xs = np.nonzero(es_sujeto)
    hx, hy = xs.mean() / 256 * 100, ys.mean() / 256 * 100
    # El radio se deriva del SUJETO, no de un % fijo del lienzo: el look de julio es un
    # bloom que ABRAZA a la mascota, no una piscina de luz de media slide. Con radio fijo
    # el halo de una mascota chica quedaba disperso y el de una grande, corto.
    lado = max(ys.max() - ys.min(), xs.max() - xs.min()) / 256
    r = max(0.16, min(0.52, lado * 0.78)) * ancho          # px de lienzo
    # Color del halo: el propio fondo aclarado. Se conserva el matiz (el canal dominante
    # sube proporcionalmente) para que sea "el mismo verde, más claro", no un gris encima.
    claro = np.clip(fondo + 52 + fondo * 0.55, 0, 255).astype(int)

    im = Image.open(recorte).convert("RGB")
    W, H = im.size
    cx, cy = hx / 100 * W, hy / 100 * H

    paradas = [(0.0, .82), (r * 0.42, .62), (r * 1.0, .30), (r * 1.9, 0.0)]

    # CORTE POR EJE: el halo se apaga ENTRANDO a la caja de texto, y queda entero del otro lado.
    #
    # El velo (`.g-*`) tapa el halo donde va el texto, pero "tapa" no es "anula": el gradiente
    # se desvanece a 0 en el 55% del lienzo y una columna `l-leftmid` llega al 64%, así que
    # esa franja de texto queda SIN velo encima y el halo se le cuela por debajo. Ahí se cayó
    # c1 s-05 a 3.9:1, bajo el mínimo WCAG de 4.5. Subir el velo lo arreglaría y está prohibido
    # (RUBRIC E10.b: *el velo se MIDE, no se sube*), así que se corrige el halo.
    #
    # Primero se probó recortar el RADIO hasta 24px antes de la caja. Pasó la compuerta y mató
    # el efecto: los radios exteriores cayeron de ~800px a ~200px y el glow medido volvió a
    # 1.3 — el mismo fondo plano que el director creativo reclamó. El radio es lo que hace que esto se lea
    # como luz de fondo; recortarlo es no tener halo.
    #
    # Lo que sí funciona es una máscara de UN EJE, la misma lógica que ya usan los `.g-*`:
    # 0 sobre la caja, 1 a RAMPA px hacia el lado del sujeto. El bloom conserva su tamaño
    # completo del lado libre —que es el 100% de lo que se ve— y bajo las letras aporta cero
    # luz. El contraste queda garantizado por construcción, no por medición posterior.
    mask_css, rampa_px = "", 0.0
    if caja:
        bx0, by0 = float(caja["x"]), float(caja["y"])
        bx1, by1 = bx0 + float(caja["w"]), by0 + float(caja["h"])
        if bx0 <= cx <= bx1 and by0 <= cy <= by1:
            return ""                       # el sujeto vive DENTRO del texto: no hay halo posible
        RAMPA = 160.0
        # El eje dominante es aquel por el que el sujeto escapa más de la caja: con el texto a
        # la izquierda el corte es vertical, con el texto abajo es horizontal.
        dx, dy = max(bx0 - cx, 0, cx - bx1), max(by0 - cy, 0, cy - by1)
        if dx >= dy:
            eje, borde, signo = "to right", (bx1 if cx > bx1 else bx0), (1 if cx > bx1 else -1)
        else:
            eje, borde, signo = "to bottom", (by1 if cy > by1 else by0), (1 if cy > by1 else -1)
        if signo > 0:   # el sujeto está DESPUÉS del borde: visible de `borde+RAMPA` en adelante
            mask_css = (f"linear-gradient({eje},transparent {borde:.0f}px,"
                        f"#000 {borde + RAMPA:.0f}px)")
        else:           # el sujeto está ANTES: visible hasta `borde-RAMPA`
            mask_css = (f"linear-gradient({eje},#000 {max(borde - RAMPA, 0):.0f}px,"
                        f"transparent {borde:.0f}px)")
        rampa_px, eje_h, borde_px, sg = RAMPA, (dx >= dy), borde, signo

    # El halo se PINTA además sobre el recorte que se usa para medir el velo. Es el punto
    # entero: el velo adaptativo se dimensiona contra el fondo REAL que va a quedar bajo las
    # letras, y si el halo aclara esa zona, el velo sube solo. Sin esto el motor medía una
    # foto que ya no existía y el contraste se caía sin que nadie lo viera hasta el gate
    # (c1 s-05: 4.5:1 → 3.9:1). Coherente con E10.b: el velo se MIDE, no se sube a ojo.
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    alfa = np.zeros_like(dist)
    for (r0, a0), (r1, a1) in zip(paradas, paradas[1:]):       # interpolación lineal, igual que CSS
        tramo = (dist >= r0) & (dist < r1)
        alfa[tramo] = a0 + (a1 - a0) * ((dist[tramo] - r0) / max(r1 - r0, 1e-6))
    if rampa_px:   # la MISMA máscara de un eje que el CSS, o el velo mediría otra foto
        pos = xx if eje_h else yy
        rampa = np.clip((pos - borde_px) * sg / rampa_px, 0, 1)
        alfa *= rampa
    base = np.asarray(im).astype(np.float32)
    mezcla = base * (1 - alfa[..., None]) + claro.reshape(1, 1, 3) * alfa[..., None]
    Image.fromarray(np.clip(mezcla, 0, 255).astype(np.uint8), "RGB").save(recorte)

    mask = (f"-webkit-mask-image:{mask_css};mask-image:{mask_css};" if mask_css else "")
    return (f'<div class="halo" style="--halo-x:{hx:.1f}%;--halo-y:{hy:.1f}%;'
            f'--halo-r1:{paradas[1][0]:.0f}px;--halo-r2:{paradas[2][0]:.0f}px;'
            f'--halo-r3:{paradas[3][0]:.0f}px;'
            f'--halo-c:{claro[0]},{claro[1]},{claro[2]};{mask}"></div>')


def css_cover(foto, crop, zoom=1.0):
    """object-position equivalente al crop, para que <img> y cutout queden ALINEADOS.

    Con `zoom` > 1 agrega el `transform` que hace que el RENDER vea la misma ventana
    que midió `cover_crop`. ⚠️ No basta con calcular el crop: el motor pinta la foto con
    `object-fit:cover`, que sobre un crudo cuadrado en un lienzo cuadrado muestra la
    imagen ENTERA — el zoom se quedaba en el análisis y el PNG salía igual que antes
    (5-ago-2026). `scale(z)` alrededor de `transform-origin:px% py%` es exactamente
    equivalente: el punto de anclaje queda fijo y la ventana se achica a 1/z.
    El mismo string se aplica a la foto Y al cutout, o la oclusión se desalinea."""
    w, h = Image.open(foto).size
    cx, cy, cw, ch = crop
    px = 0 if w == cw else cx / (w - cw)
    py = 0 if h == ch else cy / (h - ch)
    css = f"object-position:{px*100:.1f}% {py*100:.1f}%"
    if float(zoom or 1.0) > 1.001:
        css += (f";transform:scale({float(zoom):.3f})"
                f";transform-origin:{px*100:.1f}% {py*100:.1f}%")
    return css


# ────────────────────────────────────────────────────────────── asignación ──
# E10.b paso 2: estrechar la columna — PERO CON PISO.
#
# 🔴 composicion-y-tipografia.md §2: "zona de texto **≥40% del ancho** y limpia".
# El motor angostaba hasta el 60% de una columna de 560px = 336px = 31% del lienzo, por debajo
# de ese piso. Consecuencia: titulares apilados de una palabra por línea.
#
# Observación del director creativo (1-ago-2026) que lo destapó: *"cuando el texto queda cortado con una
# sola palabra, ¿no será que el error es la disposición de la imagen y dónde aparece la
# persona?"* — exacto. Si la foto no ofrece 40% limpio, la respuesta NO es apretar el texto:
# es REENCUADRAR (mover la imagen, no el texto) y, si no da, CAMBIAR DE FOTO. Apretar la
# columna era tratar el síntoma y esconder el problema real, que es el encuadre.
MIN_ANCHO = int(CANVAS * MIN_ANCHO_COL)   # 432px — el número vive en constantes.py
ANCHOS = (1.00, 0.90, 0.80)


def elegir_zona(pm, slide, size, med, fuente_real=True, zona_previa=None, alto_lienzo=CANVAS_H,
                ink='light'):
    """Capa 2: el mapa ASIGNA.

    Orden fijo de E10.b, y ninguno de los pasos es un panel opaco:
      (a) la zona planificada, (b) las otras zonas, y dentro de cada una
      (c) la columna cada vez más angosta, hasta que TERMINE antes de la modelo.
    Sin (c) el motor declaraba "sin hueco" en fotos que sí tenían un costado limpio,
    solo porque la columna venía con ancho fijo. → devuelve (zona, box, lineas, motivo, intentos)"""
    plan = slide.get("zone", "l")
    # Una zona que no existe reventaba con `KeyError: 'b'` doce líneas más abajo, sin decir
    # de qué slide ni cuáles son las válidas (encontrado al montar el caso dorado, 5-ago-2026:
    # escribí "b" en vez de "bot"). El motor está para rendirse CON DIAGNÓSTICO, no con un
    # traceback: un typo en el spec no puede costar diez minutos de leer el stack.
    if plan not in COLUMNAS:
        raise SystemExit(
            f"⛔ slide {slide.get('n', '?')}: zone «{plan}» no existe.\n"
            f"   Zonas válidas: {', '.join(sorted(COLUMNAS))}  "
            f"(l=columna izquierda · r=derecha · top=franja superior · bot=inferior · "
            f"cc=centro angosto)\n"
            f"   Corregilo en carrusel.json → slides[].zone")
    v = slide.get("v", "mid")
    orden = [plan] + [z for z in ALTERNATIVAS if z != plan]
    # A3: la zona de la slide ANTERIOR va al final de la cola. Reubicar slide por slide sin
    # mirar a la vecina hacía que dos seguidas terminaran en el mismo lado (visto en el
    # carrusel real: s-02 reubicada a 'r' y s-03 también 'r').
    if zona_previa and zona_previa in orden and len(orden) > 1:
        orden = [z for z in orden if z != zona_previa] + [zona_previa]
    intentos = []
    # Piso tipográfico del título al angostar/bajar (E3). La slide héroe (portada) NO puede
    # bajar de HERO (90px): antes el default era siempre PISO_TITULO_SEC (64px), así que el
    # motor podía dejar el titular de portada en 64px y el carrusel se quedaba sin héroe
    # (auditoría T7). `verify.py init` marca hero:true en la slide 1 del spec.
    piso = int(slide.get("piso", HERO if slide.get("hero") else PISO_TITULO_SEC))
    candidatos = []
    for z in orden:
        x0, w0 = COLUMNAS[z]
        for f in ANCHOS:
            # Margen de seguridad cuando se mide con el proxy Arial: la fuente real (Oswald,
            # Montserrat) es MÁS ANCHA que el proxy. Declarar 'tipografia.font' lo elimina.
            w = int(w0 * f * (1.0 if fuente_real else 0.88))
            if w < MIN_ANCHO and z in ("l", "r"):
                # columna lateral bajo el piso del 40% → no se aprieta: que resuelva el
                # reencuadre o el cambio de foto.
                if f == ANCHOS[-1]:
                    intentos.append(f"{z}:COLUMNA-BAJO-PISO({w}px < {MIN_ANCHO}px)")
                continue
            s = size
            while s >= piso:
                lineas = quebrar(slide.get("titulo", ""), s, w, med)
                # ⚠️ El ancho REAL manda, no el nominal. Una palabra sola más larga que la
                # columna NO se puede quebrar: textfit la devuelve igual y el bloque se sale
                # de la caja que MAPCHECK validó. Falla vista en la primera prueba del motor:
                # "acompañada" a 92px en una columna de 336px terminó detrás de la pierna —
                # la oclusión funcionó, pero la palabra quedó ilegible. La caja que se valida
                # tiene que ser la que el texto ocupa DE VERDAD.
                real = max((med(l, s) for l in lineas), default=0)
                # Solo se exige que ENTRE. Que las líneas queden desparejas está BIEN
                # (director creativo, 31-jul-2026): lo que no puede pasar es que una frase nueva arranque
                # en el renglón donde terminó la anterior — eso lo garantiza quebrar(), que
                # parte por frase antes de balancear. Una heurística de "rag parejo" acá solo
                # achicaba títulos sin arreglar nada.
                if real <= w:
                    break
                s -= 6                          # doctrina: bajar 4-8px hasta que quepa
            if s < piso:
                if f == ANCHOS[-1]:
                    intentos.append(f"{z}:SIN-ESPACIO-TEXTO(ni a {piso}px entra en {w}px)")
                continue
            if len(lineas) > MAX_LINEAS_TITULO:
                if f == ANCHOS[-1]:
                    intentos.append(f"{z}:DEMASIADAS-LINEAS({len(lineas)})")
                continue                        # ni al piso entra: probar columna más angosta
            # +10px de holgura: si la caja mide EXACTAMENTE el ancho de la línea más larga,
            # el navegador re-parte igual por diferencias de subpíxel/letter-spacing. Falla real
            # (31-jul-2026, c1-s03): el spec tenía 9 líneas y el render salió con ~15, y la caja
            # pasó de 1015px de alto. Los <br> no impiden el re-wrap (composicion §5).
            wr = int(min(w, max(real, 1) + 10))
            x = CANVAS - MARGEN - wr if z == "r" else x0
            box = caja_texto(z, v, len(lineas), s, bool(slide.get("sub")),
                             bool(slide.get("eyebrow")), bool(slide.get("cta")),
                             alto_lienzo=alto_lienzo)
            box["x"], box["w"] = x, wr
            # BOUNDS-AWARE (regla 0.21 del skill original, que el motor no implementaba).
            # MAPCHECK solo mira "no tapar a la persona": un bloque puede no tapar a nadie y
            # aun así salirse del cuadro. Falla real (31-jul-2026, c1-s03): la caja iba de
            # y=33 a y=1048 con el área segura en 48..1032 — lo cazó qa_lint DESPUÉS de
            # renderizar. El borde se respeta en la COLOCACIÓN, no solo en el gate final.
            if box["y"] < MARGEN_SEGURO or box["y"] + box["h"] > alto_lienzo - MARGEN_SEGURO:
                if f == ANCHOS[-1]:
                    intentos.append(f"{z}:FUERA-DE-MARGEN(alto {box['h']}px no entra)")
                continue
            # limb_tol MÁS ESTRICTO para texto que el default de 12%.
            # El 12% de photo_map se calibró para "una esquina del codo" bajo una tarjeta o un
            # badge. Pero una extremidad que cruza un BLOQUE DE TEXTO esconde letras: con la
            # oclusión activa, la pierna se dibuja ENCIMA y se come la palabra. Falla real
            # (31-jul-2026, c1-plan s-02): "Cada día decides" pasó con las piernas al 11% y en
            # el render la "d" de «decides» quedó tapada. Para texto: 6% (4% dejaba fotos sin ninguna zona).
            # ⚠️ SE MIDE POR LÍNEA, NO POR BLOQUE — tercera vez que aparece este mismo error.
            # Una pierna delgada que cruza un bloque de 952×200px cubre ~5% y pasa cualquier
            # umbral de bloque, pero sobre UN RENGLÓN cubre 25% y esconde una letra entera.
            # Falla real (31-jul-2026, c1-plan s-02): "Cada día decides" pasó con el bloque en
            # verde y en el render la pierna se comió la "d" de «decides».
            # (Ya había pasado con el velo —composicion §6.3— y con el sub fuera de la medición.)
            cajas = [{"name": "bloque", **box, "kind": "text"}]
            _l = cajas_por_linea(box)
            for i, (x0, y0, x1, y1) in enumerate(_l):
                cajas.append({"name": f"linea{i}", "x": x0, "y": y0,
                              "w": x1 - x0, "h": y1 - y0, "kind": "text"})
            rs = pm.check(cajas, limb_tol=LIMB_TOL_TEXTO, ink=ink)
            r = next((x for x in rs if x["verdict"] == "FAIL"), rs[0])
            if all(x["verdict"] == "PASS" for x in rs):
                extra = "" if f == 1.0 else f" · columna al {f:.0%}"
                extra += "" if s == size else f" · título {size}→{s}px"
                motivo = ("planificada" if z == plan else
                          f"REUBICADA {plan}→{z} · la planificada estaba ocupada") + extra
                intentos.append(f"{z}@{f:.0%}/{s}px:PASS")
                box["size"] = s
                return z, box, lineas, motivo, intentos
            if f == ANCHOS[-1]:
                intentos.append(f"{z}:FAIL({r['why']})")
    if candidatos:
        n, _s, z, box, lineas, motivo = min(candidatos, key=lambda c: (c[0], c[1]))
        return z, box, lineas, motivo + f" · {n} líneas (mejor de {len(candidatos)} opciones)", intentos
    return None, None, None, "sin hueco", intentos


def construir_slide(carpeta, spec, slide, med, usa_fuente_real, debug=False, zona_previa=None):
    n = slide["n"]
    foto = slide.get("foto")
    fp = os.path.join(carpeta, foto) if foto and not os.path.isabs(foto) else foto
    size = int(slide.get("size", spec.get("tipografia", {}).get("size", 92)))
    informe = {"slide": n, "zona_plan": slide.get("zone"), "ok": False}
    cw_l, ch_l = lienzo_de(spec)            # lienzo de ESTE carrusel (default 1:1)
    aspecto = (cw_l, ch_l)
    informe["canvas"] = f"{cw_l}x{ch_l}"

    if not foto:
        # Slide tipográfica: fondo de marca, sin foto. No hay persona a quien tapar, así que
        # no corre photo_map ni el velo ni la oclusión. Sirve para manifiestos, datos y cierres.
        lineas = quebrar(slide.get("titulo", ""), size, COLUMNAS["cc"][1], med)
        cuerpo = "".join(filter(None, [
            f'<div class="eyebrow">{slide["eyebrow"]}</div>' if slide.get("eyebrow") else "",
            f'<div class="title" style="font-size:{size}px">{"<br>".join(lineas)}</div>',
            f'<div class="body">{slide["sub"]}</div>' if slide.get("sub") else "",
            f'<div class="cta">{slide["cta"]}</div>' if slide.get("cta") else ""]))
        logo = f'<img class="logo" src="{spec["logo"]}" alt="">' if spec.get("logo") else ""
        dims_css = (f"<style>html,body{{width:{cw_l}px;height:{ch_l}px}}"
                    f".slide{{width:{cw_l}px;height:{ch_l}px}}</style>")
        html = (f'<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">'
                f'<link rel="stylesheet" href="{spec.get("css","styles.css")}">{dims_css}</head>'
                f'<body data-brand="{spec.get("brand","navy")}">'
                f'<div class="slide l-leftmid">{logo}<div class="text">{cuerpo}</div></div>'
                f'</body></html>')
        informe.update({"ok": True, "zona_final": "tipográfica", "motivo": "slide sin foto",
                        "lineas": len(lineas), "alfa_velo": None, "ocluido": False,
                        "intentos": [], "fuente_real": usa_fuente_real})
        return html, informe
    if not os.path.exists(fp):
        informe["error"] = f"no existe la foto {foto}"
        return None, informe

    mask, cut = preparar_foto(fp, carpeta)
    w, h = Image.open(fp).size
    # `zoom` en el spec (>1) acerca el encuadre y agranda al sujeto sin regenerar la foto.
    zoom = float(slide.get("zoom", 1.0) or 1.0)
    crop = PM.cover_crop(w, h, slide.get("posx", .5), slide.get("posy", .5), aspect=aspecto, zoom=zoom)

    if mask:
        pm = PM.PhotoMap(fp, mask, crop, canvas=(cw_l, ch_l))
        zona, box, lineas, motivo, intentos = elegir_zona(pm, slide, size, med, usa_fuente_real, zona_previa, alto_lienzo=ch_l,
                                                       ink=tinta_de(spec))
        # 🔴 REENCUADRAR TAMBIÉN CUANDO EL RESULTADO ES MALO, no solo cuando es imposible.
        #
        # Observación del director creativo (1-ago-2026), mirando la comparación con Nano Banana:
        # *"cuando el texto queda cortado con una sola palabra, ¿no será que el error es la
        # disposición de la imagen y dónde aparece la persona?"* — sí. Nano ganaba la
        # comparación tipográfica porque RE-ENCUADRABA: corría a la modelo y liberaba una
        # banda ancha. Este motor solo reencuadraba si NINGUNA zona pasaba; si una zona pasaba
        # MAL (columna angosta, título apilado en 5 líneas), se conformaba.
        # Ahora un titular de más de 3 líneas también dispara el reencuadre.
        if zona is not None and len(lineas) > MAX_LINEAS_OK:
            intentos.append(f"{zona} daba {len(lineas)} líneas → probando reencuadre")
            zona = None
            forzar_reencuadre = True
        else:
            forzar_reencuadre = False

        if zona is None:
            # PASO 1 de E10.b: REENCUADRAR — mover la IMAGEN, no el texto.
            # "Las apaisadas se panean en horizontal, las verticales en vertical"
            # (composicion-y-tipografia §2). Se barre el eje largo y se prueba cada crop.
            # ⚠️ Esto antes usaba un bbox del sujeto HARDCODEADO, así que el reencuadre era
            # decorativo: nunca encontraba nada. Cazado probando foto-salto.jpg — una foto
            # vertical con medio cielo limpio arriba que el motor declaró "sin hueco".
            # El eje del paneo es el que tiene HOLGURA con el crop del lienzo (con el 1:1
            # una foto cuadrada no deja holgura; una vertical la deja en X y una apaisada
            # puede dejarla en los dos).
            slack_x, slack_y = w - crop[2], h - crop[3]
            eje = "y" if slack_y > slack_x else "x"
            for t in (0.0, 0.15, 0.3, 0.7, 0.85, 1.0):
                if (eje == "y" and slack_y <= 0) or (eje == "x" and slack_x <= 0):
                    break
                c2 = PM.cover_crop(w, h, t if eje == "x" else slide.get("posx", .5),
                                   t if eje == "y" else slide.get("posy", .5),
                                   aspect=aspecto, zoom=zoom)
                if c2 == crop:
                    continue
                pm2 = PM.PhotoMap(fp, mask, c2, canvas=(cw_l, ch_l))
                z2, b2, l2, m2, i2 = elegir_zona(pm2, slide, size, med, usa_fuente_real, zona_previa, alto_lienzo=ch_l,
                                             ink=tinta_de(spec))
                if z2:
                    intentos += [f"reencuadre {eje}={t:.2f} → {z2} ({len(l2)}L)"]
                    mejor_prev = len(lineas) if (forzar_reencuadre and lineas) else 99
                    if len(l2) < mejor_prev:
                        crop, pm, zona, box, lineas = c2, pm2, z2, b2, l2
                        motivo = f"REENCUADRADA ({eje}={t:.2f}) · " + m2
                        mejor_prev = len(l2)
                        if len(l2) <= MAX_LINEAS_OK:
                            break
                intentos.append(f"reencuadre {eje}={t:.2f}: sin hueco")
        if zona is None and forzar_reencuadre:
            # ningún reencuadre mejoró: se vuelve a la mejor opción original (apilada, pero
            # existe) en vez de descartar la slide.
            pm = PM.PhotoMap(fp, mask, crop, canvas=(cw_l, ch_l))
            zona, box, lineas, motivo, _i = elegir_zona(pm, slide, size, med, usa_fuente_real,
                                                        zona_previa, alto_lienzo=ch_l,
                                                        ink=tinta_de(spec))
            if zona:
                motivo += " · reencuadre no mejoró"
        if zona is None:
            # Diagnóstico accionable: ¿el problema es la FOTO (sujeto sin costado limpio) o el
            # COPY (una palabra más larga que cualquier columna libre)? Son fixes distintos.
            # ¿Por qué falló? La respuesta está en los intentos, no en una heurística.
            # Bug real (31-jul-2026, lote Marca Crema): el diagnóstico estimaba el ancho de la
            # palabra más larga contra una columna HARDCODEADA y culpaba al COPY, cuando los
            # intentos mostraban que las 5 zonas y los 6 reencuadres habían fallado por
            # "tapa extremidad/cabeza" — o sea el problema era la FOTO. Un diagnóstico que
            # apunta al lado equivocado hace perder más tiempo que no dar ninguno.
            por_texto = sum("SIN-ESPACIO-TEXTO" in i for i in intentos)
            por_sujeto = sum(("tapa" in i or "FOCO" in i) for i in intentos)
            palabras = (slide.get("titulo", "") or "").split()
            larga = max(palabras, key=lambda p: med(p, size)) if palabras else ""
            if por_texto and por_texto >= por_sujeto:
                fix = (f"es el COPY: ni bajando al piso de {int(slide.get('piso',64))}px entra "
                       f"en las columnas libres que deja esta foto (la palabra más larga es "
                       f"«{larga}», {med(larga, size):.0f}px a {size}px). Acortá el título "
                       f"— COPY.md: comprimir, no explicar.")
            else:
                fix = (f"es la FOTO: el sujeto invade las {por_sujeto} zonas probadas y ningún "
                       f"reencuadre abre un costado limpio. Cambiar de foto, o regenerarla con "
                       f"el sujeto contenido estrictamente en un tercio (prompts-validados §5).")
            informe.update({"error": "ninguna zona quedó libre ni reencuadrando",
                            "intentos": intentos,
                            "fix": fix + " NO se compone con panel opaco (E10.b)."})
            return None, informe
    else:
        # foto sin sujeto detectado (objeto/escena): no hay a quién tapar ni a quién ocluir
        pm, motivo, intentos = None, "sin sujeto (escena/objeto)", []
        zona = slide.get("zone", "l")
        # A3 también acá: sin sujeto no hay mapa que consultar, pero la vecina igual manda.
        # (Falla real: s-03 sin sujeto se quedó en 'r' justo después de que s-02 fuera
        #  reubicada a 'r' — dos slides seguidas con el texto del mismo lado.)
        if zona_previa and zona == zona_previa:
            zona = next(z for z in ALTERNATIVAS if z != zona_previa)
            motivo += f" · zona rotada {zona_previa}→{zona} (A3, vecina)"
        lineas = quebrar(slide.get("titulo", ""), size, COLUMNAS[zona][1], med)
        box = caja_texto(zona, slide.get("v", "mid"), len(lineas), size,
                         bool(slide.get("sub")), bool(slide.get("eyebrow")),
                         bool(slide.get("cta")), alto_lienzo=ch_l)

    # velo adaptativo POR LÍNEA sobre el crop real
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as t:
        tmp = t.name
    recorte_lienzo(fp, crop, tmp, (cw_l, ch_l))
    # ANTES de medir el velo: el halo se pinta sobre `tmp`, así que todo lo que se mida más
    # abajo (velo por línea, velo del logo) ya ve el fondo definitivo. Se le pasa `box` para
    # que el halo se apague antes de llegar al texto — el contraste WCAG queda garantizado
    # por geometría, no por subir el velo (E10.b).
    halo_html = halo_del_sujeto(tmp, cw_l, caja=box)
    size_final = int(box.get("size", size))
    alfa, por_linea = PM.alpha_por_linea(
        tmp, cajas_por_linea(box))

    if debug and pm:
        pm.overlay(os.path.join(carpeta, f"_map-{n:02d}.png"),
                   [{"name": "texto", **box}], pm.check([{"name": "texto", **box, "kind": "text"}], ink=tinta_de(spec)))

    # ── HTML: 5 capas, el texto DEBAJO del recorte de la persona ──
    pos = css_cover(fp, crop, zoom)
    titulo = "<br>".join(lineas)
    partes = [
        f'<img class="photo" src="{foto}" style="{pos}" alt="">',
        # El halo va ANTES del gradiente (z-index 1): el gradiente ya se desvaneció donde
        # está el sujeto, y tapa el halo donde va el texto. Devuelve "" si el fondo no es plano.
        halo_html,
        f'<div class="{GRADIENTE[zona]}" style="opacity:{alfa}"></div>',
        f'<div class="text" style="width:{box["w"]}px">',
        f'  <div class="eyebrow">{slide["eyebrow"]}</div>' if slide.get("eyebrow") else "",
        # font-size explícito: es el tamaño que el motor VALIDÓ contra el mapa, no el de la
        # clase. Si la clase mandara, el texto renderizaría más grande que la caja verificada.
        f'  <div class="title" style="font-size:{size_final}px">{titulo}</div>',
        f'  <div class="body">{slide["sub"]}</div>' if slide.get("sub") else "",
        # El CTA es parte del bloque de texto: su alto entra en la caja que MAPCHECK valida,
        # así que la pastilla tampoco puede caer sobre la persona.
        f'  <div class="cta">{slide["cta"]}</div>' if slide.get("cta") else "",
        '</div>',
    ]
    if cut and slide.get("ocluir", True):
        # CAPA 4 · la persona por encima del texto → tapar una cara es imposible
        partes.append(f'<img class="cutout" src="_cut/{os.path.basename(cut)}" '
                      f'style="{pos}" alt="">')
    if spec.get("logo"):
        # El logo es bronce: sobre una foto clara se pierde. Se mide la franja superior y, si
        # está clara, entra el velo de cap. (Visto en el carrusel real: el wordmark casi
        # invisible en 3 de 6 slides con techo/pared claros.)
        _, top_alpha = PM.alpha_por_linea(tmp, [(0, 0, cw_l, int(ch_l * 0.15))])
        if top_alpha and top_alpha[0] > 0.25:
            partes.append('<div class="sc-cap"></div>')
        partes.append(f'<img class="logo" src="{spec["logo"]}" alt="">')

    # El lienzo queda declarado EN EL HTML: la pieza es autocontenida y no depende del
    # default que tenga styles.css ese día (1:1 por regla de la casa; 4:5 por spec).
    estilo_extra = (f"<style>html,body{{width:{cw_l}px;height:{ch_l}px}}"
                    f".slide{{width:{cw_l}px;height:{ch_l}px}}"
                    ".cutout{position:absolute;inset:0;width:100%;height:100%;"
                    "object-fit:cover;z-index:4;pointer-events:none}"
                    ".text{z-index:3}</style>")
    html = (f'<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">'
            f'<link rel="stylesheet" href="{spec.get("css","styles.css")}">{estilo_extra}</head>'
            f'<body data-brand="{spec.get("brand","navy")}">'
            f'<div class="slide l-{ "leftmid" if zona=="l" else "botright" if zona=="r" else "topleft" if zona=="top" else "botbig" if zona=="bot" else "leftcol" }">'
            + "\n".join(p for p in partes if p) +
            '</div></body></html>')

    os.unlink(tmp)
    informe.update({"ok": True, "zona_final": zona, "motivo": motivo, "lineas": len(lineas),
                    "alfa_velo": alfa, "alfa_por_linea": por_linea,
                    "ocluido": bool(cut), "intentos": intentos,
                    "fuente_real": usa_fuente_real})
    return html, informe


def main(argv):
    debug = "--debug" in argv
    solo = None
    if "--slide" in argv:
        i = argv.index("--slide")
        solo = int(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    carpeta = args[0]
    spec = json.load(open(os.path.join(carpeta, "carrusel.json"), encoding="utf-8"))

    # El CSS de la carpeta se SINCRONIZA en cada corrida desde templates/. Antes se copiaba
    # una vez y quedaba congelado: un arreglo de styles.css no llegaba nunca a un carrusel
    # ya creado. Costó una tarde (5-ago-2026) — el motor emitía el `<div class="halo">`
    # correcto y el navegador lo pintaba en nada porque la .css local era de dos horas antes.
    # Solo un css con OTRO nombre cuenta como override del spec: "css": "styles.css" es el
    # default escrito a mano y sincronizarlo es exactamente lo que hay que hacer.
    if spec.get("css", "styles.css") == "styles.css":
        import shutil
        origen = os.path.join(AQUI, "styles.css")
        destino = os.path.join(carpeta, "styles.css")
        if os.path.exists(origen) and os.path.abspath(origen) != os.path.abspath(destino):
            shutil.copyfile(origen, destino)

    tipo = spec.get("tipografia", {})
    fp = tipo.get("font")
    if fp and not os.path.isabs(fp):
        fp = os.path.join(carpeta, fp)
    med, real = medidor(fp, tipo.get("weight", 700), tipo.get("tracking", -0.02))
    if not real:
        print("⚠️  midiendo con proxy Arial: los quiebres pueden re-partirse en el navegador.\n"
              "    Declará 'tipografia.font' (.woff2/.ttf del render) en carrusel.json.")

    informes, fallos, zona_previa = [], 0, None
    for s in spec["slides"]:
        if solo and s["n"] != solo:
            continue
        html, inf = construir_slide(carpeta, spec, s, med, real, debug, zona_previa)
        zona_previa = inf.get("zona_final") if inf.get("ok") else zona_previa
        informes.append(inf)
        if html:
            open(os.path.join(carpeta, f"s-{s['n']:02d}.html"), "w", encoding="utf-8").write(html)
            marca = "·" if inf["motivo"] == "planificada" else "↻"
            print(f"  ✅ s-{s['n']:02d}  zona={inf['zona_final']:<4} {marca} {inf['motivo']}"
                  f"  velo={inf['alfa_velo']}  {'ocluido' if inf['ocluido'] else 'sin recorte'}")
        else:
            fallos += 1
            print(f"  ⛔ s-{s['n']:02d}  {inf.get('error')}")
            if inf.get("fix"):
                print(f"      ↳ {inf['fix']}")
    json.dump({"motor": "engine.py", "slides": informes},
              open(os.path.join(carpeta, "_build-report.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(f"\nMOTOR: {'FAIL' if fallos else 'PASS'} "
          f"({len(informes) - fallos}/{len(informes)} slides) → _build-report.json")
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
