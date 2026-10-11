#!/usr/bin/env /usr/local/bin/python3
"""
constantes.py — LA FUENTE ÚNICA DE LOS NÚMEROS (1-ago-2026).

Por qué existe. Los umbrales de la skill vivían escritos en dos sitios a la vez: en la prosa de
la doctrina y, otra vez, dentro de cada script. El propio `RUBRIC.md` lo admitía sobre el piso
del héroe: *"90 es la misma cifra de E8, de qa_typesize.py y de composicion-y-tipografia.md §4.2
— si se cambia, se cambia en los cuatro"*. Eso no es una fuente única: es una duplicación
documentada, y las duplicaciones derivan.

Y derivó. Falla real (31-jul-2026): `composicion-y-tipografia.md` §2 exigía una zona de texto
**≥40% del ancho** y el motor angostaba hasta el **31%**. Nadie mintió — simplemente no había una
constante compartida, así que la doctrina y el código se separaron sin que nada lo notara. El
síntoma fueron titulares apilados de una palabra por línea, que además pasaban todas las
compuertas.

**La regla desde ahora:** si un número aparece en la doctrina Y en el código, vive ACÁ. La
doctrina lo cita por nombre; el código lo importa. Cambiarlo en un solo lugar cambia el sistema
entero.

    from constantes import HERO, MIN_ANCHO_COL, VELO_TECHO
"""

# ─────────────────────────────────────────────────────────── lienzo ──
# Default 1:1 (1080×1080), SIEMPRE — regla de la casa, reconfirmada por el director creativo el
# 3-ago-2026: el 4:5 que la oleada 2.5A puso como default se revierte (Meta lo recomienda
# para Feed, pero la recomendación de plataforma no pisa el gusto del dueño). El 4:5
# queda como opción excepcional por spec ("canvas": "4:5"), no como ley.
CANVAS_W = 1080               # ancho del lienzo — los pisos tipográficos se derivan de ACÁ
CANVAS_H = 1080               # alto del lienzo por defecto (1:1)
CANVAS = CANVAS_W             # alias de compatibilidad: lo que lo importa quiere el ANCHO
MARGEN = 64                   # márgenes laterales seguros · composicion §7
MARGEN_SEGURO = 48            # nada cruza esta línea · RUBRIC E2

# ────────────────────────────────────────── pisos tipográficos @1080 ──
# composicion §4.2 · RUBRIC E3/E8 · qa_typesize.py
PISO_ABSOLUTO = 26            # NINGÚN texto visible por debajo. Tolerancia cero.
PISO_CUERPO = 36              # cuerpo / bajada / lead
PISO_EYEBROW = 27             # badge, pill, kicker
PISO_CTA = 32                 # botón
PISO_TITULO_SEC = 64          # título secundario (sin t-xl)
HERO = 90                     # titular héroe — **por CARRUSEL, no por slide**
T_XL = 104                    # el salto de escala que DOMINA el cuadro · RUBRIC E5

# ──────────────────────────────────────────────── zona de texto ──
# composicion §2: "zona de texto ≥40% del ancho y limpia"
MIN_ANCHO_COL = 0.40          # fracción del lienzo. 432px. Piso duro, no negociable.
MAX_LINEAS_TITULO = 8         # más que esto no es un titular
MAX_LINEAS_OK = 3             # por encima de esto se REENCUADRA la foto, no se aprieta el texto
GAP_MIN = 12                  # aire mínimo entre pastilla y texto · RUBRIC E9

# ───────────────────────────────────────────────── mapa de la foto ──
# photo_map.py · RUBRIC A7
OVERLAP_PROHIBIDO = 0.01      # cabeza/cara + eje central: 0% (1% de tolerancia numérica)
LIMB_TOL_CARD = 0.12          # "una esquina del codo sí" — para tarjetas y badges
LIMB_TOL_TEXTO = 0.06         # MÁS estricto: una extremidad sobre texto ESCONDE letras
LUZ_MAX_CARD = 0.25           # las tarjetas no se ponen sobre el foco de luz
LUZ_MAX_TEXTO = 0.40

# ────────────────────────────────────────────────── velo adaptativo ──
# RUBRIC E10 · composicion §6.3 — el alfa se MIDE, no es constante del template
VELO_OBJETIVO = 0.42          # luminancia a la que queda la zona del texto
VELO_PISO = 0.14              # anclaje mínimo
VELO_TECHO = 0.56             # la foto SIEMPRE respira. Nunca un muro.

# ──────────────────────────────────────────────────────── contraste ──
CONTRASTE_MIN = 4.5           # WCAG AA
CONTRASTE_LARGE = 3.0         # AA large text (≥27px)

# ───────────────────────────────────────────── auditoría del crudo ──
# qa_raw.py — calibrado contra el lote real del test jul-2026
OCR_AREA_MAX = 0.02           # >2% del cuadro en texto = basura de IA
OCR_AREA_WARN = 0.008
OCR_ITEM_MAX = 0.010          # un solo bloque >1% ya se lee de corrido
# Piso de confianza del OCR (5-ago-2026). Vision devuelve `conf` y el gate la ignoraba: un
# acierto de conf 0.30 sobre el BRAZO pixelado de un mascot 8-bit («Т.!"», cirílico + signos)
# reprobaba el carrusel igual que una palabra legible. Con pixel-art eso vuelve al gate
# infalsificable: cualquier contorno blocky se lee como glifos. Por debajo del piso el ítem
# NO cuenta para FAIL pero SÍ deja el gate en WARN — no desaparece en silencio, se manda a
# mirar a tamaño completo. Texto real de IA sale con conf ≫0.5. (APRENDIZAJES §17.d)
OCR_CONF_MIN = 0.50
SUBJ_ZONA_MAX = 0.05          # sujeto dentro de la zona reservada (solo fotos GENERADAS)

# ──────────────────────────────────────────── costura de collage ──
# qa_seam.py — calibrado contra 12 imágenes etiquetadas a mano (31-jul-2026)
SEAM_PICO_MIN = 8.0           # σ del pico de borde
SEAM_PERSIST_FAIL = 0.85      # bloqueante · los 3 collages confirmados dieron 0.92-0.99
SEAM_PERSIST_WARN = 0.55      # mirar a tamaño completo · ninguna foto real pasó de 0.74
SEAM_MARGEN = 0.08            # se ignora el 8% exterior: un salto en el borde es el marco

# ───────────────────────────────────────────────────────────── copy ──
HOOK_MAX_PALABRAS = 12        # COPY.md Paso B · RUBRIC DC2
VARIANTES_HOOK_MIN = 2        # RUBRIC DC7
CLARIDAD_MIN = 4              # mediana del panel · SOLO sitios web (en carruseles el panel
                              # se derogó el 10-ago-2026 · APRENDIZAJES.md §35)

# ─────────────────────────────────────────────────────────── topes ──
# Todos existen porque el ciclo correspondiente NO converge solo.
TOPE_REINTENTOS_SLIDE = 2     # produccion-imagenes §0.3 — 32 generaciones, 3 slides sin pasar
TOPE_RONDAS_COPY = 2          # SOLO sitios web · en carruseles ya no hay panel que topar
TOPE_RONDAS_JUECES = 1        # SKILL Fase 7 — el loop de jueces se comió 30 de 45 min

# ──────────────────────────────────────────────────────── verificación ──
JUECES_DISENO = 2             # instancias independientes de carrusel-qa, sin contexto compartido
LECTORAS_COPY = 3             # mínimo del panel ciego
