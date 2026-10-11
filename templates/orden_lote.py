#!/usr/bin/env /usr/local/bin/python3
"""
orden_lote.py — ¿EL LOTE SE ESTÁ CORRIENDO EN COLUMNAS O EN FILAS? (6-ago-2026)

    orden_lote.py medir <carpeta-madre>     → el reparto real del reloj y las vueltas atrás
    orden_lote.py verificar <carpeta-madre> → compuerta: ¿se generó imagen antes del plan?

POR QUÉ EXISTE (director creativo, 6-ago-2026)
    *"necesito que la skill sea más rápida, siento que hacer 10 carruseles no puede demorarse
    horas."*

Se midieron los 48 recibos del lote Marca Verde del 5-ago (4 carruseles, 8 h). El culpable NO era
ninguno de los tres sospechosos previos:
  · los jueces tomaron 9 min por ronda (APRENDIZAJES §25),
  · el tope de imágenes ya estaba puesto (§27),
  · el goteo de ráfagas explicaba 2 h de las 8 (§28).

Lo que explicaba el resto: **se generaron imágenes ANTES de tener brief y blueprint, en los 4
carruseles**. c1 generó su primer crudo a las 14:46 y escribió brief+blueprint a las 17:03 —
dos horas y cuarto DESPUÉS. El plan se redactó para justificar fotos que ya existían. Resultado:
**19 vueltas atrás a fases ya pasadas** en 4 carruseles.

El contraste que lo prueba: el copy de 7 carruseles (c4-c10) tomó **10 minutos**, porque se
corrió como lote y en orden. Las 4 piezas hechas "cada una de punta a punta" se llevaron el día.

LA REGLA QUE MIDE
Un lote se corre en COLUMNAS (una fase para todas las piezas, después la siguiente), no en FILAS
(una pieza de punta a punta). Y ninguna imagen se genera antes del blueprint de todo el lote:
una foto anterior al plan no ahorra tiempo, COMPRA trabajo.
"""
import sys, os, glob, time

# Fase de cada recibo. Es el mismo orden del pipeline de SKILL.md.
FASE = {"_brief-receipt.json": (1, "brief"),
        "_copy-gate-receipt.json": (2, "copy mecánico"),
        "_blueprint-receipt.json": (3, "blueprint"),
        "_prompt-receipt.json": (3, "prompt/zona"),
        "_raw-receipt.json": (4, "crudo script"),
        "_raw-ojo-receipt.json": (4, "crudo ojo"),
        "_gates-receipt.json": (6, "gates"),
        "_qa-receipt.json": (7, "doble juez")}

# El plan tiene que existir ANTES del primer crudo. Estos son los recibos que lo componen.
PLAN = ("_brief-receipt.json", "_blueprint-receipt.json")


def _piezas(madre):
    """Las carpetas-carrusel hijas del lote (las que tienen spec o brief)."""
    out = []
    for d in sorted(glob.glob(os.path.join(madre, "*"))):
        if not os.path.isdir(d):
            continue
        if (os.path.exists(os.path.join(d, "carrusel.json"))
                or os.path.exists(os.path.join(d, "_brief.md"))
                or glob.glob(os.path.join(d, "_*receipt*.json"))):
            out.append(d)
    return out


def _hito(d, nombre):
    p = os.path.join(d, nombre)
    return os.path.getmtime(p) if os.path.exists(p) else None


def _primer_crudo(d):
    raw = [x for x in glob.glob(os.path.join(d, "raw", "**", "*.png"), recursive=True)
           if "_descartados" not in x]
    return min((os.path.getmtime(x) for x in raw), default=None)


def analizar(madre):
    piezas = _piezas(madre)
    fuera_de_orden, vueltas, todos = [], [], []

    for d in piezas:
        nom = os.path.basename(d)
        # (a) ¿se generó imagen antes de que existiera el plan?
        t_raw = _primer_crudo(d)
        if t_raw:
            for r in PLAN:
                t = _hito(d, r)
                if t and t > t_raw:
                    fuera_de_orden.append(
                        {"pieza": nom, "recibo": r.replace("-receipt.json", ""),
                         "crudo": time.strftime("%d-%b %H:%M", time.localtime(t_raw)),
                         "plan": time.strftime("%d-%b %H:%M", time.localtime(t)),
                         "horas": round((t - t_raw) / 3600, 1)})

        # (b) ¿se volvió atrás a una fase ya pasada?
        ev = sorted((os.path.getmtime(p), *FASE[os.path.basename(p)])
                    for p in glob.glob(os.path.join(d, "_*receipt*.json"))
                    if os.path.basename(p) in FASE)
        todos += [(m, nom, f, et) for m, f, et in ev]
        # Solo cuenta como vuelta atrás si pasó TIEMPO REAL entre medio. Varios recibos
        # escritos en la misma tanda (un `verify.py all`, o el panel de copy juzgando 7 piezas)
        # comparten mtime al microsegundo, y el orden entre ellos es el del sistema de archivos,
        # no el del trabajo. Sin este margen, un lote corrido BIEN en columnas — que escribe sus
        # recibos juntos — se reportaría como desordenado: la compuerta castigaría justo la
        # conducta que quiere premiar. Margen de 90 s = lo que tarda una fase real.
        MARGEN = 90
        maxf, t_maxf = 0, 0
        for m, f, et in ev:
            if f < maxf and (m - t_maxf) > MARGEN:
                vueltas.append({"pieza": nom, "fase": et, "estaba_en": maxf,
                                "cuando": time.strftime("%d-%b %H:%M", time.localtime(m))})
            if f > maxf:
                maxf, t_maxf = f, m

    # (c) ¿columnas o filas? Recibos escritos en el mismo minuto = fase corrida en lote.
    porminuto = {}
    for m, nom, f, et in todos:
        porminuto.setdefault(round(m / 60), []).append(nom)
    en_lote = sum(len(v) for v in porminuto.values() if len(v) >= 3)
    total = sum(len(v) for v in porminuto.values())
    pct = round(100 * en_lote / total) if total else 0

    return {"piezas": len(piezas), "recibos": total, "pct_en_lote": pct,
            "fuera_de_orden": fuera_de_orden, "vueltas": vueltas}


def cmd_medir(madre):
    r = analizar(madre)
    print(f"\n── ORDEN DEL LOTE · {os.path.basename(os.path.abspath(madre))} ──")
    print(f"   {r['piezas']} piezas · {r['recibos']} recibos")
    if not r["recibos"]:
        print("   (sin recibos todavía: el lote no arrancó)")
        return 0
    print(f"   trabajo corrido en LOTE (≥3 piezas en la misma tanda): {r['pct_en_lote']}%")
    print(f"      100% = columnas (una fase para todas) · 0% = filas (una pieza de punta a punta)")

    if r["fuera_de_orden"]:
        print(f"\n   ⛔ {len(r['fuera_de_orden'])} caso(s) de IMAGEN ANTES DEL PLAN:")
        for f in r["fuera_de_orden"]:
            print(f"      {f['pieza']:28} crudo {f['crudo']} · {f['recibo']} {f['plan']} "
                  f"(+{f['horas']} h después)")
        print("      El plan escrito DESPUÉS de la foto se escribe para justificarla.")
    else:
        print("\n   ✅ ninguna imagen se generó antes de su plan")

    if r["vueltas"]:
        print(f"\n   ⚠️  {len(r['vueltas'])} vuelta(s) atrás a una fase ya pasada:")
        for v in r["vueltas"][:12]:
            print(f"      {v['cuando']}  {v['pieza']:28} volvió a «{v['fase']}» "
                  f"estando en fase {v['estaba_en']}")
        if len(r["vueltas"]) > 12:
            print(f"      … y {len(r['vueltas']) - 12} más")
        print("      Cada vuelta atrás es trabajo que el orden correcto habría evitado gratis.")
    else:
        print("   ✅ ninguna vuelta atrás")
    return 0


def cmd_verificar(madre):
    """Compuerta. FAIL solo por imagen-antes-del-plan: es el error caro y objetivo.

    Las vueltas atrás y el % de lote se reportan como WARN — hay motivos legítimos para
    volver atrás (director creativo cambia un copy, un juez encuentra algo real), y castigarlos
    convertiría la compuerta en un estorbo. Lo que nunca es legítimo es pagar una
    generación antes de saber qué tiene que mostrar.
    """
    r = analizar(madre)
    checks, fails, warns = [], [], []

    for f in r["fuera_de_orden"]:
        d = (f"{f['pieza']}: generó imagen el {f['crudo']} pero su {f['recibo']} se escribió "
             f"{f['horas']} h DESPUÉS ({f['plan']})")
        fails.append(d)
        checks.append({"check": f"{f['pieza']} · plan antes que imagen", "ok": False, "detalle": d})
    if not r["fuera_de_orden"]:
        checks.append({"check": "ninguna imagen antes de su plan", "ok": True, "detalle": ""})

    if r["vueltas"]:
        d = (f"{len(r['vueltas'])} vueltas atrás a fases ya pasadas "
             f"(medido 5-ago: 19 en 4 carruseles = el lote se corrió en filas)")
        warns.append(d)
        checks.append({"check": "vueltas atrás", "ok": None, "detalle": d})
    if r["recibos"] and r["pct_en_lote"] < 50:
        d = (f"solo {r['pct_en_lote']}% del trabajo se corrió en lote — el pipeline va en FILAS "
             f"(una pieza de punta a punta) en vez de COLUMNAS (una fase para todas)")
        warns.append(d)
        checks.append({"check": "columnas vs filas", "ok": None, "detalle": d})

    print(f"\n── COMPUERTA DE ORDEN · {os.path.basename(os.path.abspath(madre))} ──")
    for c in checks:
        print(f"  {'⛔' if c['ok'] is False else ('✅' if c['ok'] else '⚠️ ')} "
              f"{c['check']}{(' · ' + c['detalle']) if c['detalle'] else ''}"[:150])
    if fails:
        print(f"\n⛔ Una foto generada antes del plan no ahorra tiempo: COMPRA trabajo.")
        print(f"   El plan termina escribiéndose para justificarla, y cuando no calza, se")
        print(f"   regenera. Medido el 5-ago: 19 vueltas atrás en 4 carruseles.")
        print(f"   Orden correcto: brief → copy → blueprint → prompt_zona → recién ahí generar.")
    return {"gate": "orden_lote", "status": "FAIL" if fails else ("PASS_CON_WARNS" if warns else "PASS"),
            "checks": checks, "fails": fails, "warns": warns}


def main(argv):
    if len(argv) < 2 or argv[0] not in ("medir", "verificar"):
        print(__doc__)
        return 2
    modo, madre = argv[0], argv[1]
    if not os.path.isdir(madre):
        print(f"FAIL: no existe la carpeta {madre}")
        return 2
    if modo == "medir":
        return cmd_medir(madre)
    r = cmd_verificar(madre)
    return 0 if r["status"].startswith("PASS") else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
