#!/usr/bin/env /usr/local/bin/python3
"""
qa_lote.py — COMPUERTA DE LOTE (3-ago-2026, oleada 2.5A · auditoría C12).

Por qué existe. Un lote de carruseles hermanos puede pasar CADA compuerta individual y aun
así salir repetido: mismos ángulos, mismos arranques de portada. Ninguna puerta por carpeta
lo ve, porque la repetición vive ENTRE carpetas. Caso medido: el lote con 6 hooks abriendo
con "Deja de" — cada carrusel pasó su QA y el lote era uno solo repetido seis veces.

Qué chequea (y qué NO, a propósito):

  FAIL · angulo_repetido   dos `carrusel.json` hermanos declaran el MISMO `angulo`
                           (normalizado). Es el ángulo DECLARADO el que se compara —
                           obligar a declararlo es justamente lo que hace que la repetición
                           sea visible. Un `angulo` vacío no cuenta (eso lo persigue
                           `verify.py brief` en cada carpeta).
  WARN · arranque_portada  ≥3 títulos de portada (slide 1) comparten las mismas 3 PRIMERAS
                           PALABRAS. Es el chequeo barato de arranque: las paráfrasis reales
                           lo pasan; el arranque calcado, no.

NO se detecta por solapamiento léxico general (medido en la auditoría: con cualquier umbral
de solapamiento las paráfrasis reales de un mismo tema también caían — el falso positivo
obligaba a variar lo que ya variaba). El check es sobre el ángulo DECLARADO + el arranque
literal, y nada más.

  qa_lote.py <carpeta-madre-del-lote>
  qa_lote.py <carpeta-madre> --json
"""
import sys, os, json, glob, re, unicodedata
from collections import defaultdict


def _norm(s):
    """minúsculas sin tildes ni signos — la comparación no depende de acentuación."""
    s = unicodedata.normalize("NFD", (s or "").lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", s)).strip()


def _arranque(titulo, n=3):
    palabras = _norm(re.sub(r"<[^>]+>", " ", titulo or "")).split()
    return " ".join(palabras[:n]) if len(palabras) >= n else None


def specs_del_lote(madre):
    """Los carrusel.json hermanos: un nivel bajo la carpeta madre (y la madre misma, por si
    el lote es plano). Devuelve [(ruta, spec)]."""
    rutas = sorted(glob.glob(os.path.join(madre, "*", "carrusel.json")))
    propio = os.path.join(madre, "carrusel.json")
    if os.path.exists(propio):
        rutas.append(propio)
    out = []
    for r in rutas:
        try:
            out.append((r, json.load(open(r, encoding="utf-8"))))
        except (OSError, json.JSONDecodeError) as e:
            print(f"WARN  {r}: spec ilegible ({e}) — se salta")
    return out


def correr(madre):
    checks = []

    def add(ok, nombre, detalle):
        checks.append({"check": nombre, "ok": ok, "detalle": detalle})

    specs = specs_del_lote(madre)
    if len(specs) < 2:
        add(None, "hay lote que comparar",
            f"{len(specs)} spec(s) bajo {madre} — la compuerta de lote necesita ≥2 "
            f"carruseles hermanos (*/carrusel.json)")
        return {"gate": "lote", "verdict": "PASS", "checks": checks}

    # 1 · ángulos declarados repetidos → FAIL
    por_angulo = defaultdict(list)
    for r, s in specs:
        a = _norm(str(s.get("angulo", "")))
        if a:
            por_angulo[a].append(os.path.basename(os.path.dirname(r)) or r)
    repetidos = {a: cs for a, cs in por_angulo.items() if len(cs) > 1}
    sin_angulo = [os.path.basename(os.path.dirname(r)) for r, s in specs
                  if not _norm(str(s.get("angulo", "")))]
    if repetidos:
        det = " · ".join(f"«{a[:60]}» × {len(cs)} ({', '.join(cs)})"
                         for a, cs in sorted(repetidos.items()))
        add(False, "C12 · ángulos declarados distintos",
            f"ángulo repetido: {det} — dos piezas del mismo lote con el mismo ángulo son "
            f"UNA pieza: cambiar el ángulo de una (Fase −1), no las palabras")
    else:
        add(True, "C12 · ángulos declarados distintos",
            f"{len(por_angulo)} ángulos distintos en {len(specs)} specs"
            + (f" · {len(sin_angulo)} SIN ángulo declarado (verify.py brief lo exige): "
               f"{', '.join(sin_angulo)}" if sin_angulo else ""))

    # 2 · arranque de portada calcado (≥3 con las mismas 3 primeras palabras) → WARN
    por_arranque = defaultdict(list)
    for r, s in specs:
        slides = s.get("slides") or []
        portada = next((sl for sl in slides if sl.get("n") == 1), slides[0] if slides else {})
        arr = _arranque(portada.get("titulo", ""))
        if arr:
            por_arranque[arr].append(os.path.basename(os.path.dirname(r)) or r)
    calcados = {a: cs for a, cs in por_arranque.items() if len(cs) >= 3}
    if calcados:
        det = " · ".join(f"«{a}…» × {len(cs)} ({', '.join(cs)})"
                         for a, cs in sorted(calcados.items()))
        add(None, "C12 · arranques de portada variados",
            f"≥3 portadas arrancan igual: {det} — WARN: variar el arranque o aceptar con "
            f"--warn-ok si es deliberado (serie episódica, mismo open-loop)")
    else:
        add(True, "C12 · arranques de portada variados",
            f"ningún arranque de 3 palabras se repite en ≥3 portadas")

    fail = any(c["ok"] is False for c in checks)
    return {"gate": "lote", "verdict": "FAIL" if fail else "PASS", "checks": checks}


def main(argv):
    como_json = "--json" in argv
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        print("uso: qa_lote.py <carpeta-madre-del-lote> [--json]")
        return 2
    r = correr(paths[0])
    if como_json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        for c in r["checks"]:
            print(f"  {'PASS' if c['ok'] else 'FAIL' if c['ok'] is False else 'WARN'}  "
                  f"{c['check']:<40} {c['detalle']}")
        print("LOTE:", r["verdict"])
    return 1 if r["verdict"] == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
