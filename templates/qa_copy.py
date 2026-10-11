#!/usr/bin/env /usr/local/bin/python3
"""
qa_copy.py — COMPUERTA DETERMINISTA DEL COPY (31-jul-2026).

Por qué existe. Hasta el 5-ago-2026 el copy tenía UNA sola compuerta que se hiciera cumplir: el
panel de comprensión (`copy-qa`, 3 lectores ciegos), hoy derogado (APRENDIZAJES.md §35). Ese
panel medía si el lector ENTIENDE — no si el copy es bueno. Un copy plano, correcto y olvidable lo pasa con nota perfecta. Por eso el director creativo venía
diciendo "los copy no salen muy buenos": lo único que se medía era comprensión.

La calidad (DC1-DC7 de RUBRIC.md) sí estaba escrita, pero la juzgaba `carrusel-qa` AL FINAL,
mirando PNG ya compuestos — o sea, después de gastar todas las generaciones de imagen.

Esto adelanta la parte MECÁNICA de esa rúbrica a segundos y cero costo. Lo que queda para el
juez `copy-craft-qa` es lo que ningún regex puede ver: deseo, registro real, pendiente
resbaladiza y la única pregunta que importa — "¿este hook pararía el scroll o se me olvida?".

  qa_copy.py carrusel.json
  qa_copy.py carrusel.json --json
"""
import sys, json, re, unicodedata

# ─────────────────────────── listas literales (COPY.md Regla #0) ──
# Se escriben CON tilde una sola vez: la comparación pasa por _norm(), que quita tildes, así que
# agregar la variante sin tilde solo duplica el reporte del mismo hallazgo.
CLICHES = [
    "tu viaje", "tu mejor versión", "transforma tu vida", "el método correcto",
    "descubre cómo", "la clave está en", "es importante destacar", "cabe destacar",
    "en el mundo actual", "profundicemos", "vale la pena mencionar", "sumérgete",
    "que se sostienen", "lleva tu", "al siguiente nivel", "no se trata solo de",
    "imagina por un momento", "en la era de",
]
VAGUEDAD = ["resultados reales", "de verdad", "realmente", "muy pronto", "lo mejor de"]
HEDGING = ["quizás", "tal vez", "podría ser", "casi siempre"]

# español neutro (D3): voseo y "chicos/chicas" como tamaño
#
# ⚠️ El voseo se detecta por la TILDE, no por la terminación. Bug real (31-jul-2026, primer uso
# sobre copy de Marca Crema): el patrón `sab[ée]s` marcaba «sabes» como voseo — y «sabes» es
# tuteo correcto. Lo mismo pasaba con `hac[ée]s` y «haces». Las formas voseantes SIEMPRE llevan
# tilde en la última sílaba (sabés, hacés, tenés, querés, podés); sin tilde son tuteo y están bien.
VOSEO = re.compile(r"\b(ten[ée]s|quer[ée]s|pod[ée]s|sabés|hacés|ponés|venís|decís|vivís|"
                   r"salís|sentís|volvés|sos|vos|andá|mirá|escuchá|vení|decí|hacé|poné)\b")
CHICOS_TAM = re.compile(r"\b(movimientos|m[úu]sculos|grupos|espacios|detalles|pasos)\s+"
                        r"(chicos|chicas|chiquitos)\b", re.I)

import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from constantes import HOOK_MAX_PALABRAS as MAX_PALABRAS_HOOK, VARIANTES_HOOK_MIN


def _norm(s):
    """minúsculas sin tildes, para buscar clichés sin depender de la acentuación."""
    s = unicodedata.normalize("NFD", (s or "").lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def _palabras(s):
    # El markup NO es copy (auditoría C13): "<br>", "<em>" etc. se desnudan antes de contar,
    # si no DC2 (≤12 palabras) castigaba el HTML del título como si fueran palabras.
    s = re.sub(r"<[^>]+>", " ", s or "")
    return [w for w in re.split(r"\s+", re.sub(r"[^\wáéíóúñü¿?¡!\s-]", " ", s)) if w]


def normalizar(spec):
    """Acepta los DOS formatos de spec que existen en el disco (auditoría C9):
      - dict con "slides" (carrusel.json del pipeline) — clave `titulo`;
      - LISTA de slides (los slides.json de verde-ads y builds antiguos) — clave `title`,
        a veces sin "n". Antes esto reventaba con AttributeError en `spec.get(...)`.
    Devuelve siempre un dict con "slides" normalizadas (`title` → `titulo`, `n` numerada)."""
    if isinstance(spec, list):
        spec = {"slides": spec}
    slides = []
    for i, s in enumerate(spec.get("slides") or [], 1):
        s = dict(s)
        if "titulo" not in s and "title" in s:
            s["titulo"] = s["title"]
        s.setdefault("n", i)
        slides.append(s)
    spec = dict(spec)
    spec["slides"] = slides
    return spec


# ─────────────────────────────────────────────────────────────────── chequeos ──
def c_cliches(spec):
    """DC1 — clichés, relleno, AI-tells, vaguedad y hedging."""
    hits = []
    for s in spec["slides"]:
        texto = " ".join(filter(None, [s.get("titulo"), s.get("sub")]))
        n = _norm(texto)
        for frase in CLICHES + VAGUEDAD + HEDGING:
            if _norm(frase) in n:
                hits.append(f"s{s['n']}: «{frase}»")
    n_pt = _norm(spec.get("primary_text", ""))
    for frase in CLICHES:
        if _norm(frase) in n_pt:
            hits.append(f"primary_text: «{frase}»")
    return (not hits, "DC1 · clichés / relleno / AI-tells",
            "; ".join(hits) if hits else "sin clichés de la lista")


def c_triadas(spec):
    """DC1 — triadas y paralelismos perfectos: 'más X, más Y, más Z'."""
    pat = re.compile(r"\b(m[áa]s|menos|sin|con|tu|para)\b[^,.;]{2,30},\s*"
                     r"\b\1\b[^,.;]{2,30},\s*(y\s+)?\b\1\b", re.I)
    hits = [f"s{s['n']}" for s in spec["slides"]
            if pat.search(" ".join(filter(None, [s.get("titulo"), s.get("sub")])) or "")]
    return (not hits, "DC1 · triadas / paralelismo perfecto",
            f"triada en {', '.join(hits)}" if hits else "sin triadas")


def c_hook(spec):
    """DC2 — hook ≤12 palabras, una idea, y NO abre con la marca."""
    s1 = spec["slides"][0]
    hook = s1.get("titulo", "") or ""
    problemas = []
    n = len(_palabras(hook))
    if n > MAX_PALABRAS_HOOK:
        problemas.append(f"{n} palabras (máx {MAX_PALABRAS_HOOK})")
    # ¿abre nombrando la marca/producto?
    marca = _norm(spec.get("linea") or spec.get("cliente") or "")
    tokens = [t for t in marca.replace("-", " ").split() if len(t) > 3]
    if tokens and _norm(hook).startswith(tuple(tokens)):
        problemas.append("abre nombrando la marca (el hook debe nombrar el PROBLEMA)")
    # OJO: no se cuenta el nº de puntos. El staccato ("Pegar el error. Copiar el fix. Volver.")
    # es un antídoto EXPLÍCITO de COPY.md ("imperfección controlada, frases cortas") — penalizarlo
    # sería castigar justo el estilo que el método pide. "Una sola idea" lo juzga copy-craft-qa.
    return (not problemas, "DC2 · hook problema-primero, ≤12 palabras",
            "; ".join(problemas) if problemas else f"{n} palabras, problema-primero")


_IMPERATIVOS_IRREG = {"haz", "pon", "ven", "sal", "di", "hazlo", "hacé", "vení", "mirá"}


def _familia_hook(v):
    """Familia de una variante de hook — heurística simple y documentada (auditoría C4):
    (primera palabra normalizada, estructura), donde estructura es:
      'pregunta'    abre con ¿ o cierra con ?
      'imperativo'  la primera palabra tiene forma de imperativo tuteo: está en el set de
                    irregulares frecuentes, o termina en a/e/i con ≥4 letras (mira, entrena,
                    siente, conecta)
      'declarativa' cualquier otra
    Solo se usa en una dirección: FAIL cuando TODAS las variantes caen en la misma familia
    (misma primera palabra Y misma estructura = misma familia). Un falso positivo de la
    heurística exige variedad donde ya había; un falso negativo deja el hallazgo al juez."""
    t = (v or "").strip()
    if t.startswith("¿") or t.endswith("?"):
        est = "pregunta"
    else:
        primera = _norm(t.split()[0]) if t.split() else ""
        if (primera in {_norm(x) for x in _IMPERATIVOS_IRREG}
                or (len(primera) >= 4 and primera[-1] in "aei")):
            est = "imperativo"
        else:
            est = "declarativa"
    return (_norm(t.split()[0]) if t.split() else "", est)


def c_variantes(spec):
    """DC7 — finalistas del hook de familias DISTINTAS, no paráfrasis del mismo ángulo (C4).

    La doctrina (COPY.md Paso B, oleada 2.5A): ~20 candidatos por familia de fórmula → 3
    finalistas de familias distintas. El piso mecánico queda en VARIANTES_HOOK_MIN; lo que
    esta compuerta caza de verdad es el colapso en UNA familia."""
    v = [x for x in (spec.get("hook_variantes") or []) if str(x).strip()]
    if len(v) < VARIANTES_HOOK_MIN:
        return (False, "DC7 · finalistas del hook (familias distintas)",
                f"{len(v)} variantes — faltan (mínimo {VARIANTES_HOOK_MIN}; la doctrina son "
                f"3 finalistas de familias distintas)")
    familias = {_familia_hook(x) for x in v}
    if len(familias) == 1:
        pw, est = next(iter(familias))
        return (False, "DC7 · finalistas del hook (familias distintas)",
                f"{len(v)} variantes pero TODAS de la misma familia («{pw}…», {est}): "
                f"paráfrasis del mismo ángulo no son un A/B — variar el ángulo, no las palabras")
    return (True, "DC7 · finalistas del hook (familias distintas)",
            f"{len(v)} variantes en {len(familias)} familias distintas")


def c_primary(spec):
    """DC6 — apertura + punteos con emoji + cierre, separados con enters."""
    pt = spec.get("primary_text", "") or ""
    if not pt.strip():
        return False, "DC6 · primary text estructurado", "no hay primary_text"
    bloques = [b for b in re.split(r"\n\s*\n", pt) if b.strip()]
    lineas = [l for l in pt.split("\n") if l.strip()]
    emoji = re.compile("[\U0001F300-\U0001FAFF✅❤✨•➡\U0001F49C]")
    con_emoji = [l for l in lineas if emoji.search(l)]
    problemas = []
    if len(bloques) < 3:
        problemas.append(f"{len(bloques)} bloques (se esperan 3: apertura / punteos / cierre)")
    if len(con_emoji) < 2:
        problemas.append(f"{len(con_emoji)} líneas con emoji (se esperan ≥2 punteos)")
    return (not problemas, "DC6 · primary text estructurado",
            "; ".join(problemas) if problemas else
            f"{len(bloques)} bloques, {len(con_emoji)} punteos")


def c_neutro(spec):
    """D3 — español neutro: sin voseo, sin 'chicos' como tamaño."""
    todo = " ".join(filter(None, [s.get("titulo") for s in spec["slides"]] +
                                 [s.get("sub") for s in spec["slides"]] +
                                 [spec.get("primary_text")]))
    problemas = []
    if VOSEO.search(todo):
        problemas.append(f"voseo: «{VOSEO.search(todo).group(0)}»")
    if CHICOS_TAM.search(todo):
        problemas.append(f"«{CHICOS_TAM.search(todo).group(0)}» → usar pequeños/pequeñas")
    return (not problemas, "D3 · español neutro",
            "; ".join(problemas) if problemas else "neutro, sin voseo")


def c_exclamacion(spec):
    """Corey writing rules — sin signos de exclamación en el ARTE."""
    hits = [f"s{s['n']}" for s in spec["slides"]
            if "!" in (s.get("titulo", "") + s.get("sub", "") or "")]
    return (not hits, "estilo · sin signos de exclamación en el arte",
            f"exclamación en {', '.join(hits)}" if hits else "sin exclamaciones")


def c_cifras(spec):
    """D1 — toda cifra necesita respaldo. WARN: lo confirma un humano/el juez."""
    cifras = set()
    for s in spec["slides"]:
        for m in re.finditer(r"\b\d[\d.,]*\s*(%|mil|k\b|años|clases|mujeres|min)?",
                             " ".join(filter(None, [s.get("titulo"), s.get("sub")]))):
            if len(m.group(0).strip()) > 1:
                cifras.add(m.group(0).strip())
    declaradas = {str(x).strip() for x in (spec.get("cifras_con_fuente") or [])}
    sin = sorted(cifras - declaradas)
    # ⚠️ `cifras_con_fuente` es una AUTODECLARACIÓN: el script no puede verificar la fuente,
    # solo constatar que alguien dijo que la tiene. Agujero real (31-jul-2026, c2-cabeza): se
    # declaró "40" para «Cuarenta minutos» y el gate calló — pero la marca dice "desde 25
    # minutos" en decenas de copys y construye su ángulo CONTRA la clase larga. Lo cazó el juez
    # de craft contrastando con el brand-brain. Por eso esto NUNCA es PASS silencioso: si hay
    # cifras, siempre queda WARN para que un ojo las contraste.
    if sin:
        return None, "D1 · cifras con fuente", f"SIN declarar, verificar a mano: {', '.join(sin)}"
    if declaradas:
        return None, "D1 · cifras con fuente", (
            f"declaradas sin verificar: {', '.join(sorted(declaradas))} — contrastarlas contra "
            f"el brand-brain (el script no puede; lo hace copy-craft-qa)")
    return True, "D1 · cifras con fuente", "sin cifras"


def c_repetidos(spec):
    """Ninguna slide repite el titular de otra (delata copy de relleno)."""
    vistos, dup = {}, []
    for s in spec["slides"]:
        k = _norm(s.get("titulo", ""))
        if k and k in vistos:
            dup.append(f"s{vistos[k]}≡s{s['n']}")
        vistos[k] = s["n"]
    return (not dup, "titulares no repetidos",
            "; ".join(dup) if dup else "todos distintos")


CHEQUEOS = [c_hook, c_cliches, c_triadas, c_variantes, c_primary,
            c_neutro, c_exclamacion, c_repetidos, c_cifras]


def correr(spec):
    spec = normalizar(spec)
    checks = []
    for fn in CHEQUEOS:
        try:
            ok, nombre, detalle = fn(spec)
        except Exception as e:
            ok, nombre, detalle = None, fn.__name__, f"error: {e}"
        checks.append({"check": nombre, "ok": ok, "detalle": detalle})
    fail = any(c["ok"] is False for c in checks)
    return {"gate": "copy", "verdict": "FAIL" if fail else "PASS", "checks": checks}


def main(argv):
    como_json = "--json" in argv
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        print("uso: qa_copy.py carrusel.json [--json]")
        return 2
    spec = normalizar(json.load(open(paths[0], encoding="utf-8")))
    if not spec.get("slides"):
        print("FAIL: el spec no tiene 'slides'")
        return 1
    r = correr(spec)
    if como_json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        for c in r["checks"]:
            print(f"  {'PASS' if c['ok'] else 'FAIL' if c['ok'] is False else 'WARN'}  "
                  f"{c['check']:<45} {c['detalle']}")
        print("COPY:", r["verdict"])
    return 1 if r["verdict"] == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
