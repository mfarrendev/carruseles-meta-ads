#!/usr/bin/env /usr/local/bin/python3
"""
plan_lote.py — QUÉ CARRUSEL HACER, según la marca (31-jul-2026).

El menú de `references/tipos-y-formatos.md` tiene ~55 formatos en 9 familias. Elegir a ojo
termina siempre igual: todo sale "educativo por defecto", y un lote de 6 abre seis veces de la
misma manera. La Fase 0 existía, pero era un paso mental sin nada que la hiciera cumplir.

Esto lo vuelve determinista: lee `brand-brain/<cliente>/formatos.md` — que declara qué formatos
sirven para ESE negocio y con qué peso, **derivado de la evidencia del propio brand-brain**
(`winners.md`, `audience.md`) — y reparte N carruseles entre ellos sin repetir vecinos.

    plan_lote.py marca-estudio 6
    plan_lote.py marca-estudio 6 --objetivo guardados
    plan_lote.py marca-estudio 6 --json
"""
import sys, os, json, re

# realpath, NO abspath (misma razón que en qa_brief.py): con la skill instalada como
# symlink en ~/.claude/skills/, abspath dejaba REPO en el home y no encontraba
# brand-brain/<cliente>/formatos.md. (5-ago-2026)
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                    "..", "..", "..", ".."))


def cargar(cliente):
    p = os.path.join(REPO, "brand-brain", cliente, "formatos.md")
    if not os.path.exists(p):
        raise SystemExit(
            f"FAIL: no existe brand-brain/{cliente}/formatos.md\n"
            f"      Sin esa declaración no se puede elegir formato por evidencia.\n"
            f"      Copiá el de marca-estudio como plantilla y llenalo desde winners.md /\n"
            f"      audience.md de ese cliente — cada formato con SU evidencia citada.")
    txt = open(p, encoding="utf-8").read()
    m = re.search(r"```json\s*(\{.*?\})\s*```", txt, re.S)
    if not m:
        raise SystemExit(f"FAIL: {p} no tiene bloque ```json")
    return json.loads(m.group(1))


def repartir(formatos, n):
    """Cuota proporcional al peso, por restos mayores. Determinista."""
    total = sum(f.get("peso", 1) for f in formatos) or 1
    exacto = [(f, n * f.get("peso", 1) / total) for f in formatos]
    cuota = {f["id"]: int(v) for f, v in exacto}
    resto = n - sum(cuota.values())
    # Desempate: primero el resto mayor, después el PESO mayor, y recién ahí el id (para que
    # sea reproducible). Sin el peso, un formato de peso 1 le ganaba el cupo sobrante a uno de
    # peso 3 solo por ir antes en el alfabeto.
    orden = sorted(exacto, key=lambda x: (-(x[1] - int(x[1])), -x[0].get("peso", 1), x[0]["id"]))
    for f, _ in orden[:resto]:
        cuota[f["id"]] += 1
    return cuota


def intercalar(cuota, formatos):
    """Ordena para que no salgan dos del mismo formato seguidos: siempre el que más queda."""
    por_id = {f["id"]: f for f in formatos}
    quedan = dict(cuota)
    out, ultimo = [], None
    while sum(quedan.values()) > 0:
        opciones = sorted((k for k, v in quedan.items() if v > 0),
                          key=lambda k: (-quedan[k], k))
        elegido = next((k for k in opciones if k != ultimo), opciones[0])
        out.append(por_id[elegido])
        quedan[elegido] -= 1
        ultimo = elegido
    return out


def planificar(cliente, n, objetivo=None):
    bb = cargar(cliente)
    formatos = bb["formatos"]
    if objetivo:
        filtrados = [f for f in formatos if f.get("objetivo") == objetivo]
        if not filtrados:
            raise SystemExit(f"FAIL: ningún formato de {cliente} apunta a «{objetivo}». "
                             f"Disponibles: {sorted({f.get('objetivo') for f in formatos})}")
        formatos = filtrados
    orden = intercalar(repartir(formatos, n), formatos)
    lote = []
    for i, f in enumerate(orden, 1):
        lote.append({
            "n": i,
            "carrusel": f"c{i:02d}-{f['id']}",
            "formato": f["formato"], "formato_id": f["id"], "familia": f["familia"],
            "framework": f["framework"], "objetivo": f["objetivo"],
            "slides": max(bb["slides"]["min"], min(f["slides"], bb["slides"]["max"])),
            "hook": f["hook"], "cta": bb["cta"], "evidencia": f["evidencia"],
        })
    return {"cliente": cliente, "n": n, "aspect": bb["aspect"], "cta": bb["cta"],
            "cta_prohibidos": bb.get("cta_prohibidos", []),
            "angulos_prohibidos": bb.get("angulos_prohibidos", []),
            "lote": lote}


def main(argv):
    como_json = "--json" in argv
    obj = None
    if "--objetivo" in argv:
        i = argv.index("--objetivo")
        obj = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    args = [a for a in argv if not a.startswith("--")]
    if len(args) < 2:
        print(__doc__)
        return 2
    p = planificar(args[0], int(args[1]), obj)
    if como_json:
        print(json.dumps(p, ensure_ascii=False, indent=2))
        return 0
    print(f"\nLOTE · {p['cliente']} · {p['n']} carruseles · {p['aspect']}")
    print(f"CTA de marca: «{p['cta']}»")
    if p["angulos_prohibidos"]:
        print(f"⛔ ángulos prohibidos: {', '.join(p['angulos_prohibidos'])}")
    if p["cta_prohibidos"]:
        print(f"⛔ CTA prohibidos: {', '.join(p['cta_prohibidos'])}")
    print()
    for c in p["lote"]:
        print(f"  {c['n']}. {c['carrusel']}")
        print(f"     {c['formato']} · {c['framework']} · {c['slides']} slides · "
              f"objetivo: {c['objetivo']}")
        print(f"     hook: {c['hook']}")
        print(f"     ↳ {c['evidencia']}")
    print("\nCada uno arranca escribiendo su carrusel.json y corriendo: verify.py brief <carpeta>\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
