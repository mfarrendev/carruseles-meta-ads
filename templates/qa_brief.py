#!/usr/bin/env /usr/local/bin/python3
"""
qa_brief.py — LA PRIMERA PUERTA: ¿el brief está completo? (31-jul-2026)

RUBRIC F1 exige un `_brief.md` y F2 exige que el carrusel sea coherente con él — pero eso lo
chequeaba el juez AL FINAL. Si el brief estaba incompleto (sin línea/sede, sin CTA, sin segmento),
el error ya había costado el carrusel entero.

El caso caro es Marca Crema: "Marca Crema" son CUATRO marcas distintas (Estudio, Pilates, Online, App) con
estética, CTA, disciplinas y sede diferentes. Un brief que dice "Marca Crema" y no la línea ya arrancó mal.

Chequea el spec `carrusel.json` + la existencia del `_brief.md` en prosa.

  qa_brief.py <carpeta-del-carrusel>
  qa_brief.py <carpeta> --json
"""
import sys, os, json

REQUERIDOS = {
    "cliente":   "qué cliente (carpeta de brand-brain/)",
    "linea":     "qué línea/sede — Marca Bronce ≠ Pilates ≠ Online ≠ App",
    "objetivo":  "guardados / comentarios / ventas / confianza / cercanía",
    "formato":   "familia y formato de tipos-y-formatos.md",
    "framework": "PAS / AIDA / BAB / PPPP / listicle / contrarian",
    "segmento":  "el público objetivo — la mediana del panel se calcula SOLO sobre él",
    "angulo":    "la idea central del carrusel en una línea — la compuerta de lote "
                 "(verify.py lote) FAIL si dos carruseles hermanos la repiten",
    "cta":       "el CTA de esa línea (lo fija el brand-brain)",
}
# raíz del repo = 4 niveles arriba de templates/
# realpath, NO abspath: la skill está instalada además como symlink en
# ~/.claude/skills/carruseles-max-final. Con abspath, invocarla por ahí deja REPO
# en /Users/<usuario> — sin brand-brain/ — y el check "el cliente tiene brand-brain"
# daba FAIL aunque el brand-brain existiera. realpath resuelve el symlink y el gate
# mide el mismo repo se invoque por donde se invoque. (5-ago-2026)
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                    "..", "..", "..", ".."))


def correr(carpeta):
    checks = []

    def add(ok, nombre, detalle):
        checks.append({"check": nombre, "ok": ok, "detalle": detalle})

    # 1 · _brief.md en prosa (RUBRIC F1)
    bp = os.path.join(carpeta, "_brief.md")
    add(os.path.exists(bp), "F1 · existe _brief.md",
        "presente" if os.path.exists(bp) else "falta el _brief.md en la carpeta del carrusel")

    # 2 · spec de máquina
    sp = os.path.join(carpeta, "carrusel.json")
    if not os.path.exists(sp):
        add(False, "existe carrusel.json", "falta el spec de máquina (carrusel.json)")
        return {"gate": "brief", "verdict": "FAIL", "checks": checks}
    try:
        spec = json.load(open(sp, encoding="utf-8"))
    except Exception as e:
        add(False, "carrusel.json legible", f"JSON inválido: {e}")
        return {"gate": "brief", "verdict": "FAIL", "checks": checks}
    add(True, "existe carrusel.json", "presente y legible")

    # 3 · campos obligatorios
    faltan = [f"{k} ({d})" for k, d in REQUERIDOS.items() if not str(spec.get(k, "")).strip()]
    add(not faltan, "campos obligatorios del brief",
        "; ".join(f"FALTA {f}" for f in faltan) if faltan else
        f"los {len(REQUERIDOS)} campos declarados")

    # 3b · procedencia de la idea — SOLO en lote (Fase −1, 6-ago-2026)
    #
    # De dónde salió esta idea: el archivo de ideas + la celda de la grilla, o
    # "pedido-directo: <lo que pidió el director creativo>". Se exige solo si el carrusel tiene
    # HERMANOS (≥2 carpetas-carrusel bajo la misma madre), porque el embudo existe
    # para lo que el volumen rompe: pedir N piezas de una vez produce N variantes de
    # la forma que el generador se atreve a defender. El lote con SEIS hooks abriendo
    # con "Deja de" salió así. Una pieza suelta no tiene ese problema y exigirle
    # procedencia sería un trámite.
    #
    # WARN y no FAIL: la compuerta dura del embudo es el hook `embudo-creativo.py`,
    # que pregunta ANTES de que exista carpeta. Acá se deja la marca para que la
    # Fase 7 la revise si nadie escribió la razón — un lote puede nacer legítimamente
    # de un pedido directo del director creativo, y él pisa cualquier regla escrita.
    madre = os.path.dirname(os.path.abspath(carpeta))
    try:
        hermanos = [d for d in os.listdir(madre)
                    if os.path.isfile(os.path.join(madre, d, "carrusel.json"))]
    except OSError:
        hermanos = []
    if len(hermanos) >= 2:
        proc = str(spec.get("procedencia", "")).strip()
        add(bool(proc) or None, "procedencia de la idea (lote)",
            proc if proc else
            f"lote de {len(hermanos)} piezas sin `procedencia` declarada — de dónde salió "
            f"esta idea: ruta del archivo de ideas + celda de la grilla (Fase −1), o "
            f"«pedido-directo: <lo que pidió el director creativo>». Un lote pedido de una vez repite "
            f"la forma que el generador prefiere (6 hooks «Deja de», jul-2026)")

    # 4 · el cliente existe como brand-brain
    cli = str(spec.get("cliente", "")).strip()
    bb = os.path.join(REPO, "brand-brain", cli)
    if cli:
        ok = os.path.isdir(bb)
        add(ok, "el cliente tiene brand-brain",
            f"brand-brain/{cli}/" if ok else
            f"no existe brand-brain/{cli}/ — crearlo con el modo descubrimiento "
            f"(estilo-y-recursos.md §3) antes de producir")
    else:
        add(False, "el cliente tiene brand-brain", "sin cliente declarado")

    # 5 · desambiguación de Marca Crema (la trampa más cara del repo)
    if "mal" in cli.lower() or "mal" in str(spec.get("linea", "")).lower():
        lineas_ok = ("marca-estudio", "marca-pilates", "crema", "marca-app")
        ok = cli in lineas_ok
        add(ok, "línea de Marca Crema desambiguada",
            f"{cli}" if ok else
            "«Marca Crema» son 4 marcas distintas: cliente debe ser una de "
            + ", ".join(lineas_ok))

    # 6 · fuente de imágenes declarada por slide (corrección el director creativo jul-2026)
    slides = spec.get("slides") or []
    sin_fuente = [s.get("n") for s in slides if not str(s.get("fuente", "")).strip()]
    add(not sin_fuente, "fuente de imagen declarada por slide",
        f"slides sin declarar (real/generada/frame): {sin_fuente}" if sin_fuente
        else f"{len(slides)} slides con fuente declarada")

    fail = any(c["ok"] is False for c in checks)
    return {"gate": "brief", "verdict": "FAIL" if fail else "PASS", "checks": checks}


def main(argv):
    como_json = "--json" in argv
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        print("uso: qa_brief.py <carpeta-del-carrusel> [--json]")
        return 2
    r = correr(paths[0])
    if como_json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        for c in r["checks"]:
            print(f"  {'PASS' if c['ok'] else 'FAIL' if c['ok'] is False else 'WARN'}  "
                  f"{c['check']:<38} {c['detalle']}")
        print("BRIEF:", r["verdict"])
    return 1 if r["verdict"] == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
