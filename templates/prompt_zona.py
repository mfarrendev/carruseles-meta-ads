#!/usr/bin/env /usr/local/bin/python3
"""
prompt_zona.py — QUE LA FOTO NAZCA CON EL HUECO DEL TEXTO (6-ago-2026)

    prompt_zona.py armar     <carpeta>            → la cláusula exacta por slide, lista para pegar
    prompt_zona.py armar     <carpeta> --only s-03
    prompt_zona.py verificar <carpeta>            → ¿el prompt guardado reserva la zona? (compuerta)

POR QUÉ EXISTE (director creativo, 6-ago-2026)
    *"la skill entiende de qué será el copy y ve cómo lo dispondrá en la imagen; genera una
    imagen con Higgsfield indicándole dónde estará el texto, para así no poner nada ahí; luego
    ver el juez que esté bien. ¿No se está haciendo así?"*

Se estaba haciendo **a veces**. La regla ya era suya (corrección del 7-jul-2026,
`references/produccion-imagenes.md` §112) y estaba bien escrita — pero era PROSA:
  · el `zone` vivía en el spec y el prompt lo tenía que recordar el agente en pleno vuelo;
  · el prompt no se guardaba en ninguna parte (las 5 slides de c1: `prompt` ausente), así que
    después no había forma de saber si se había pedido el hueco o no;
  · `verify.py raw` mide el hueco DESPUÉS de generar — cuando fallaba, ya estaba pagada la
    generación.

Este script cierra las tres: DERIVA la cláusula de la geometría real del motor (no de la
memoria), la deja escrita en el spec, y la VERIFICA antes de que la puerta GENERAR se abra.

LA REGLA FINA QUE MÁS SE OLVIDA
El hueco es **continuidad de la misma escena**, no un recorte. Pedir "empty black space" o
"clean white area" produce medio rectángulo muerto pegado a la foto, y la imagen se ve partida
en dos. Por eso `verificar` trata esas frases como FAIL, no como warn.
"""
import sys, os, json, glob, re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from constantes import CANVAS_W, CANVAS_H, MARGEN

# Geometría REAL del bloque de texto, derivada de la misma tabla que usa engine.COLUMNAS.
# Si mañana cambia la columna, cambia la cláusula: no hay una segunda copia que se desincronice.
_ANCHO_COL = 560
COLUMNAS = {"l":   (MARGEN, _ANCHO_COL),
            "r":   (CANVAS_W - MARGEN - _ANCHO_COL, _ANCHO_COL),
            "top": (MARGEN, CANVAS_W - 2 * MARGEN),
            "bot": (MARGEN, CANVAS_W - 2 * MARGEN),
            "cc":  (MARGEN + 96, CANVAS_W - 2 * (MARGEN + 96))}

# Por zona: dónde va el sujeto, hacia dónde se extiende la escena, y qué palabras exige/prohíbe
# la compuerta. `pide` son sinónimos aceptables — basta uno; el prompt no tiene que ser literal.
ZONAS = {
    "l": dict(lado="left", hacia="to the left", opuesto="right",
              sujeto="subject positioned in the RIGHT portion of the frame",
              pide=(r"\bleft\b",), eje="horizontal"),
    "r": dict(lado="right", hacia="to the right", opuesto="left",
              sujeto="subject positioned in the LEFT portion of the frame",
              pide=(r"\bright\b",), eje="horizontal"),
    "top": dict(lado="upper", hacia="upward", opuesto="lower",
                sujeto="subject positioned in the LOWER half of the frame",
                pide=(r"\btop\b", r"\bupper\b", r"\bsky\b"), eje="vertical"),
    "bot": dict(lado="lower", hacia="downward", opuesto="upper",
                sujeto="subject positioned in the UPPER half of the frame",
                pide=(r"\bbottom\b", r"\blower\b", r"\bfloor\b", r"\bground\b"), eje="vertical"),
    "cc": dict(lado="central", hacia="into the center", opuesto="edges",
               sujeto="subject framing the composition from the EDGES, center kept open",
               pide=(r"\bcent(er|re|ral)\b",), eje="central"),
}

# Frases que producen el bloque muerto. Son FAIL, no warn: ya costaron un lote entero.
VENENO = (r"empty black", r"black (?:box|block|rectangle|band|bar)\b", r"clean empty",
          r"empty white", r"white (?:box|block|rectangle|band|bar)\b", r"solid colou?r block",
          r"blank (?:space|area)", r"copy ?space block")
# Lo que hace que el hueco sea escena y no corte. Basta una.
CONTINUIDAD = (r"continu", r"extend", r"same (?:scene|background|atmosphere)",
               r"fad(?:e|es|ing)", r"gradual", r"smooth", r"soft(?:ly)? (?:falls?|falloff)")

# Negadores que convierten un veneno en su contrario. La cláusula canónica que emite `armar`
# dice literalmente «It is NOT a black block, NOT a flat panel», así que sin esto la compuerta
# rechazaba su propia salida y NINGÚN prompt podía pasarla. Caza el veneno pedido
# («leave an empty black block») y deja pasar el veneno prohibido («NOT a black block»).
NEGADORES = r"(?:not|never|no|avoid|without|nothing)\s+(?:an?\s+|any\s+)?$"


def _veneno_real(low, patron):
    """True si el patrón aparece SIN una negación inmediatamente antes."""
    for m in re.finditer(patron, low):
        if not re.search(NEGADORES, low[max(0, m.start() - 24):m.start()]):
            return True
    return False


def _pct(v, total):
    return round(100 * v / total)


def clausula(zone):
    """La cláusula de espacio reservado para ESTA zona, con los porcentajes reales del lienzo."""
    z = ZONAS[zone]
    x, w = COLUMNAS[zone]
    if z["eje"] == "horizontal":
        a, b = _pct(x, CANVAS_W), _pct(x + w, CANVAS_W)
        donde = f"the {z['lado']} {b - a}% of the frame (from {a}% to {b}% across)"
    elif zone == "top":
        donde = "the upper 40% of the frame"
    elif zone == "bot":
        donde = "the lower 40% of the frame"
    else:
        a, b = _pct(x, CANVAS_W), _pct(x + w, CANVAS_W)
        donde = f"the central band (from {a}% to {b}% across)"
    return (
        f"{z['sujeto']}, leaving {donde} as open negative space. "
        f"That reserved area is the SAME scene continuing {z['hacia']} — same background, "
        f"same light, the glow gently fading toward that side, one continuous atmosphere with "
        f"depth. It is NOT a black block, NOT a flat panel, no hard edge, no seam, no cut. "
        f"Nothing important — no face, no hands, no product, no text — inside that area."
    )


def _slides(carpeta, only=None):
    p = os.path.join(carpeta, "carrusel.json")
    if not os.path.exists(p):
        print(f"FAIL: falta {p}. Correr primero: verify.py init {carpeta}")
        sys.exit(2)
    spec = json.load(open(p, encoding="utf-8"))
    ss = spec.get("slides") or []
    if only:
        n = int(re.sub(r"\D", "", only) or 0)
        ss = [s for s in ss if int(s.get("n", 0)) == n]
    return spec, ss


def cmd_armar(carpeta, only=None):
    spec, ss = _slides(carpeta, only)
    if not ss:
        print("FAIL: el spec no tiene slides (o --only no encontró ninguna).")
        return 2
    print(f"\n── CLÁUSULA DE ZONA · {os.path.basename(os.path.abspath(carpeta))} ──")
    print("   Pegar al FINAL del prompt de cada slide, después de describir la escena.\n")
    malas = 0
    for s in ss:
        n, zone = int(s.get("n", 0)), (s.get("zone") or "").strip()
        if zone not in ZONAS:
            print(f"  s-{n:02d}  ⛔ zone «{zone or '—'}» inválida. Válidas: {', '.join(ZONAS)}")
            malas += 1
            continue
        print(f"  ┌─ s-{n:02d} · zone «{zone}» · «{(s.get('titulo') or '')[:52]}»")
        print(f"  │  {(s.get('visual_need') or '⚠️ sin visual_need en el spec')[:74]}")
        print(f"  └─ {clausula(zone)}\n")
    if malas:
        return 2
    print("   Después de generar, guardar el prompt REAL en el spec (`slides[].prompt`):")
    print("   sin eso no se puede verificar nada ni reusarlo, y el gate GENERAR lo va a pedir.")
    return 0


def cmd_verificar(carpeta, only=None):
    spec, ss = _slides(carpeta, only)
    checks, fails, warns = [], [], []
    for s in ss:
        n, zone = int(s.get("n", 0)), (s.get("zone") or "").strip()
        et = f"s-{n:02d}"
        if (s.get("fuente") or "").strip() == "real":
            checks.append({"slide": et, "estado": "N/A", "detalle": "foto real, no se prompt-ea"})
            continue
        # Slide TIPOGRAFICA (sin `foto`): el motor la soporta desde siempre — engine.py la
        # compone con fondo de marca, sin photo_map, sin velo y sin oclusion, porque no hay
        # persona a quien tapar. Este gate no la conocia y la reprobaba por "prompt ausente",
        # pidiendo el prompt de una imagen que nunca se va a generar.
        # Falla real (27-ago-2026, lote ciclorama de Marca Crema): los 3 carruseles cierran
        # con una slide tipografica sobre color plano y los 3 daban FAIL. Un gate que reprueba
        # una forma legitima del spec empuja a inventarle una foto a la slide para pasarlo.
        if not (s.get("foto") or "").strip():
            checks.append({"slide": et, "estado": "N/A",
                           "detalle": "slide tipografica sin foto, no se prompt-ea"})
            continue
        pr = (s.get("prompt") or "").strip()
        if not pr:
            fails.append(f"{et}: sin `prompt` en el spec. La imagen se generó (o se va a generar) "
                         f"sin dejar rastro de si se pidió el hueco de la zona «{zone}».")
            checks.append({"slide": et, "estado": "FAIL", "detalle": "prompt ausente"})
            continue
        if zone not in ZONAS:
            fails.append(f"{et}: zone «{zone or '—'}» inválida (válidas: {', '.join(ZONAS)}).")
            checks.append({"slide": et, "estado": "FAIL", "detalle": "zone inválida"})
            continue
        low = pr.lower()
        det = []
        if not any(re.search(p, low) for p in ZONAS[zone]["pide"]):
            det.append(f"no nombra el lado «{ZONAS[zone]['lado']}» de la zona «{zone}»")
        if not any(re.search(p, low) for p in CONTINUIDAD):
            det.append("no pide continuidad de escena (continues/extends/fading/same background)")
        veneno = [v for v in VENENO if _veneno_real(low, v)]
        if veneno:
            det.append(f"pide un bloque muerto: «{veneno[0]}» → sale la foto partida en dos")
        if det:
            fails.append(f"{et} (zone «{zone}»): " + " · ".join(det))
            checks.append({"slide": et, "estado": "FAIL", "detalle": "; ".join(det)})
        else:
            checks.append({"slide": et, "estado": "PASS", "detalle": f"reserva la zona «{zone}»"})

    print(f"\n── PROMPT vs. ZONA · {os.path.basename(os.path.abspath(carpeta))} ──")
    for c in checks:
        icono = {"PASS": "✅", "FAIL": "⛔", "N/A": "· "}[c["estado"]]
        print(f"  {icono} {c['slide']:<6} {c['detalle']}")
    if fails:
        print(f"\n⛔ {len(fails)} slide(s) generarían sin el hueco pedido:\n")
        for f in fails:
            print(f"   · {f}")
        print(f"\n   La cláusula correcta, ya calculada:  prompt_zona.py armar {carpeta}")
        print(f"   Esto se caza ANTES de gastar la generación — después ya está pagada.")
    else:
        print(f"\n✅ cada slide generada pide el hueco de su zona.")
    return {"gate": "prompt_zona", "status": "FAIL" if fails else "PASS",
            "checks": checks, "fails": fails, "warns": warns}


def main(argv):
    if len(argv) < 2 or argv[0] not in ("armar", "verificar"):
        print(__doc__)
        return 2
    modo, carpeta = argv[0], argv[1]
    only = argv[argv.index("--only") + 1] if "--only" in argv else None
    if not os.path.isdir(carpeta):
        print(f"FAIL: no existe la carpeta {carpeta}")
        return 2
    if modo == "armar":
        return cmd_armar(carpeta, only)
    r = cmd_verificar(carpeta, only)
    return 0 if r["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
