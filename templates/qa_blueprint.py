#!/usr/bin/env /usr/local/bin/python3
"""
qa_blueprint.py — EL PLAN ANTES DE GASTAR IMÁGENES (31-jul-2026).

La Fase 3 del pipeline dice: primero se decide QUÉ dice cada slide, EN QUÉ ZONA va el texto y
QUÉ debe mostrar la foto; recién después se genera la imagen PARA ese plan. En la práctica el
orden se invertía — se generaba "una mujer corriendo", salía centrada, y el texto terminaba
encima de la cara porque ya no quedaba hueco. Esta compuerta exige el plan antes de generar.

Chequea:
  1. Toda slide declara su ZONA de texto y su VISUAL_NEED (qué debe DEMOSTRAR la foto).
  2. Dos slides vecinas no comparten zona — comparada POR POSICIÓN, no por etiqueta.
     (composicion-y-tipografia.md §5: dos slides marcadas `top` y `l` cayeron visualmente en la
      MISMA esquina superior izquierda y el check por etiqueta las dejó pasar.)
  3. A8 · cero repetición de imágenes dentro del carrusel.
  4. El nº de slides está en el rango del formato.

  qa_blueprint.py <carpeta-del-carrusel> [--json]
"""
import sys, os, json
from collections import Counter

# Caja normalizada (x0, y0, x1, y1) donde CAE el texto de cada zona. Lo que se compara es esto,
# no la etiqueta: dos etiquetas distintas pueden aterrizar en el mismo rincón.
CAJAS = {
    ("l", "top"): (0.00, 0.00, 0.55, 0.45), ("l", "mid"): (0.00, 0.28, 0.55, 0.72),
    ("l", "bot"): (0.00, 0.55, 0.55, 1.00),
    ("r", "top"): (0.45, 0.00, 1.00, 0.45), ("r", "mid"): (0.45, 0.28, 1.00, 0.72),
    ("r", "bot"): (0.45, 0.55, 1.00, 1.00),
    ("top", "*"): (0.00, 0.00, 1.00, 0.45), ("bot", "*"): (0.00, 0.55, 1.00, 1.00),
    ("cc", "*"):  (0.15, 0.25, 0.85, 0.75),
}
SOLAPE_MAX = 0.60   # dos vecinas que comparten >60% de su caja = misma zona

# realpath, NO abspath (misma razón que en qa_brief.py): la skill vive también como
# symlink en ~/.claude/skills/, y con abspath el rango de slides del brand-brain no se
# encontraba al invocarla por esa ruta. (5-ago-2026)
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                    "..", "..", "..", ".."))
RANGO_SLIDES = {"educativo": (7, 12), "case study": (6, 11), "lista": (5, 14),
                "storytelling": (7, 11), "contrarian": (6, 10), "anuncio": (3, 9)}


def caja(s):
    z = str(s.get("zone", "")).lower()
    v = str(s.get("v", "mid")).lower()
    return CAJAS.get((z, v)) or CAJAS.get((z, "*")) or CAJAS.get((z, "mid"))


def solape(a, b):
    """fracción de la caja MÁS CHICA que comparten (0..1)."""
    if not a or not b:
        return 0.0
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    if inter <= 0:
        return 0.0
    menor = min((a[2] - a[0]) * (a[3] - a[1]), (b[2] - b[0]) * (b[3] - b[1]))
    return inter / menor if menor else 0.0


def correr(carpeta):
    checks = []

    def add(ok, nombre, detalle):
        checks.append({"check": nombre, "ok": ok, "detalle": detalle})

    sp = os.path.join(carpeta, "carrusel.json")
    if not os.path.exists(sp):
        add(False, "existe carrusel.json", "falta el spec")
        return {"gate": "blueprint", "verdict": "FAIL", "checks": checks}
    spec = json.load(open(sp, encoding="utf-8"))
    slides = spec.get("slides") or []
    if not slides:
        add(False, "hay slides", "el spec no tiene slides")
        return {"gate": "blueprint", "verdict": "FAIL", "checks": checks}

    # 1 · zona + visual_need por slide
    sin_zona = [s.get("n") for s in slides if not caja(s)]
    add(not sin_zona, "toda slide declara ZONA de texto válida",
        f"slides sin zona válida (l|r|top|bot|cc): {sin_zona}" if sin_zona
        else f"{len(slides)} zonas válidas")

    sin_vn = [s.get("n") for s in slides if not str(s.get("visual_need", "")).strip()]
    add(not sin_vn, "toda slide declara VISUAL_NEED",
        f"slides sin visual_need: {sin_vn} — sin esto el asset se elige por estética "
        f"y la foto no DEMUESTRA el mensaje (produccion-imagenes §3.1)" if sin_vn
        else "qué debe mostrar cada foto, declarado")

    # 2 · vecinas: por POSICIÓN, no por etiqueta
    choques = []
    for i in range(1, len(slides)):
        s = solape(caja(slides[i - 1]), caja(slides[i]))
        if s > SOLAPE_MAX:
            choques.append(f"s{slides[i-1].get('n')}·s{slides[i].get('n')} "
                           f"({slides[i-1].get('zone')}/{slides[i].get('zone')} "
                           f"solapan {s:.0%})")
    add(not choques, "A3 · vecinas no comparten zona (por posición)",
        "; ".join(choques) if choques else "todas rotan")

    # 3 · A8 cero repetición
    fotos = [s.get("foto") for s in slides if s.get("foto")]
    rep = [f"{f} ×{n}" for f, n in Counter(fotos).items() if n > 1]
    add(not rep, "A8 · imágenes distintas, cero repetición",
        "; ".join(rep) if rep else f"{len(set(fotos))} imágenes distintas")

    # 4 · nº de slides — EL BRAND-BRAIN PISA LA TABLA GENÉRICA
    #
    # tipos-y-formatos §6: "Ads de Marca Crema: 3-6 slides (lo fija el brand-brain), no los 6-8 de la
    # tabla. Si el brand-brain del cliente dice otra cosa, GANA EL BRAND-BRAIN."
    # ⚠️ Bug real (31-jul-2026, primer uso): este check leía solo la tabla genérica y falló un
    # carrusel de 4 slides de Marca Crema, que es exactamente su convención (lote-20: 4 slides
    # c/u). Un gate que ignora la jerarquía de mando de la propia skill es un gate roto.
    fmt = str(spec.get("formato", "")).lower()
    rango, origen = None, ""
    fm = os.path.join(REPO, "brand-brain", str(spec.get("cliente", "")), "formatos.md")
    if os.path.exists(fm):
        try:
            import re as _re
            bb = json.loads(_re.search(r"```json\s*(\{.*?\})\s*```",
                                       open(fm, encoding="utf-8").read(), _re.S).group(1))
            rango = (bb["slides"]["min"], bb["slides"]["max"])
            origen = f"brand-brain/{spec['cliente']}/formatos.md"
        except Exception:
            rango = None
    if rango is None and spec.get("slides_rango"):
        rango, origen = tuple(spec["slides_rango"]), "carrusel.json"
    if rango is None:
        rango = next((r for k, r in RANGO_SLIDES.items() if k in fmt), None)
        origen = f"tabla genérica ({fmt})"
    if rango:
        ok = rango[0] <= len(slides) <= rango[1]
        add(ok, "nº de slides dentro del rango",
            f"{len(slides)} slides · rango {rango[0]}-{rango[1]} según {origen}")
    else:
        add(None, "nº de slides dentro del rango",
            f"formato «{fmt}» sin rango declarado — {len(slides)} slides. "
            f"Declaralo en brand-brain/<cliente>/formatos.md o en 'slides_rango'.")

    fail = any(c["ok"] is False for c in checks)
    return {"gate": "blueprint", "verdict": "FAIL" if fail else "PASS", "checks": checks}


def main(argv):
    como_json = "--json" in argv
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        print("uso: qa_blueprint.py <carpeta-del-carrusel> [--json]")
        return 2
    r = correr(paths[0])
    if como_json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        for c in r["checks"]:
            print(f"  {'PASS' if c['ok'] else 'FAIL' if c['ok'] is False else 'WARN'}  "
                  f"{c['check']:<45} {c['detalle']}")
        print("BLUEPRINT:", r["verdict"])
    return 1 if r["verdict"] == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
