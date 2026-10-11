#!/usr/bin/env /usr/local/bin/python3
"""
rendimiento.py — CERRAR EL BUCLE: lo que se publicó, ¿cómo le fue? (5-ago-2026)

    rendimiento.py pendientes <carpeta-madre> [--dias 7]   → a quién hay que pedirle insights
    rendimiento.py anotar     <carpeta> --json <archivo|-> → guarda _rendimiento.json
    rendimiento.py tabla      <carpeta-madre> [--min 1000] → qué decisión gana, con evidencia

POR QUÉ EXISTE
`publicacion-y-registro.md` guarda el `ad_id` y dice, textual, que existe para *"traer el
rendimiento real de vuelta"*. Ese camino de vuelta **no existía**: el ad_id quedaba escrito y
nadie lo volvía a mirar nunca. Resultado: cada carrusel nuevo se decide por intuición sobre
ángulo, fórmula de titular y foto real vs. generada, teniendo los números en la cuenta de Meta.

POR QUÉ SON TRES COMANDOS Y NO UNO
Un script de Python **no puede llamar al MCP de Meta**. Así que el trabajo se parte:

    1. `pendientes`  (script)  → lee los `_publicado.json` y dice QUÉ ad_ids pedir
    2. el AGENTE               → los pide con `mcp__meta-ads__ads_entity_get_report`
    3. `anotar`      (script)  → guarda la respuesta cruda + los campos normalizados
    4. `tabla`       (script)  → cruza rendimiento contra las DECISIONES del spec

DOS REGLAS QUE NO SE NEGOCIAN
· **Nada se infiere.** Si un carrusel no tiene `_publicado.json`, la tabla dice "sin registro",
  no "no se publicó". El director creativo publica a mano en Ads Manager, por fuera del pipeline: la ausencia
  de `ad_id` en disco NO significa que la pieza no esté al aire.
· **Piso de impresiones.** Ordenar 12 ads por CTR cuando cinco tienen 200 impresiones es leer
  ruido. Todo lo que esté bajo `--min` (1000 por defecto) se lista aparte como *sin volumen*,
  nunca mezclado en el ranking.
"""
import sys, os, json, glob, time

# Métricas que sirven para una pieza estática. Se guardan crudas y normalizadas: si mañana
# Meta cambia un nombre de campo, el crudo sigue estando y se re-normaliza sin volver a pedir.
CAMPOS = ["impressions", "reach", "frequency", "spend", "clicks", "ctr", "cpc", "cpm",
          "inline_link_clicks", "inline_link_click_ctr", "cost_per_inline_link_click",
          "actions", "cost_per_action_type", "date_start", "date_stop"]


def cargar(p, x=None):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return x


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def carruseles(madre):
    return sorted(d for d in glob.glob(os.path.join(madre, "*"))
                  if os.path.isdir(d) and os.path.exists(os.path.join(d, "carrusel.json")))


# ─────────────────────────────────────────────────────────────────────────────
def cmd_pendientes(madre, dias):
    hijos = carruseles(madre)
    if not hijos:
        print(f"FAIL: ninguna subcarpeta de {madre} tiene carrusel.json")
        return 2
    pedir, frescos, sin_reg = [], [], []
    ahora = time.time()
    for h in hijos:
        pub = cargar(os.path.join(h, "_publicado.json"))
        if not pub or not pub.get("ad_id"):
            sin_reg.append(os.path.basename(h))
            continue
        r = os.path.join(h, "_rendimiento.json")
        edad = (ahora - os.path.getmtime(r)) / 86400 if os.path.exists(r) else None
        if edad is not None and edad < dias:
            frescos.append((os.path.basename(h), edad))
        else:
            pedir.append((os.path.basename(h), pub["ad_id"], edad))

    print(f"\n── RENDIMIENTO PENDIENTE · {os.path.basename(os.path.abspath(madre))} ──")
    if pedir:
        print(f"\n  PEDIR INSIGHTS ({len(pedir)}):")
        for n, aid, edad in pedir:
            cuando = "nunca" if edad is None else f"hace {edad:.0f} d"
            print(f"    {n:<32} ad_id {aid:<22} último: {cuando}")
        print(f"\n  El agente los trae así (uno por ad, o en lote):\n")
        print(f"      mcp__meta-ads__ads_entity_get_report")
        print(f"        entity_id: <ad_id>   ·   level: 'ad'   ·   date_preset: 'maximum'")
        print(f"        fields: {', '.join(CAMPOS[:8])}, …\n")
        print(f"  Y los guarda, uno por uno:")
        print(f"      rendimiento.py anotar <carpeta> --json /tmp/insights.json\n")
    else:
        print("\n  ✅ nada que pedir: todos tienen datos de menos de "
              f"{dias} días (o no hay ninguno registrado).")
    if frescos:
        print(f"  frescos ({len(frescos)}): " +
              ", ".join(f"{n} ({e:.0f}d)" for n, e in frescos))
    if sin_reg:
        print(f"\n  SIN REGISTRO ({len(sin_reg)}): {', '.join(sin_reg)}")
        print("    ⚠️  «sin registro» NO es «no se publicó». El director creativo publica a mano en Ads")
        print("        Manager. Para saberlo de verdad hay que mirar la cuenta y hacer el")
        print("        calce retroactivo por copy (publicacion-y-registro.md §Inventario).")
    return 0


# ─────────────────────────────────────────────────────────────────────────────
def cmd_anotar(carpeta, origen):
    crudo = sys.stdin.read() if origen == "-" else open(origen, encoding="utf-8").read()
    try:
        data = json.loads(crudo)
    except Exception as e:
        print(f"FAIL: el JSON no se pudo leer ({e})")
        return 2
    # La API devuelve {"data":[{…}]} o directamente la fila. Se acepta cualquiera.
    fila = data
    if isinstance(data, dict) and isinstance(data.get("data"), list) and data["data"]:
        fila = data["data"][0]
    if isinstance(data, list) and data:
        fila = data[0]
    if not isinstance(fila, dict):
        print("FAIL: no se encontró una fila de insights en el JSON")
        return 2

    pub = cargar(os.path.join(carpeta, "_publicado.json"), {}) or {}
    m = {k: fila.get(k) for k in CAMPOS if k in fila}
    R = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
         "ad_id": fila.get("ad_id") or pub.get("ad_id"),
         "fuente": "plataforma (Meta Ads API vía MCP meta-ads)",
         "metricas": m, "crudo": fila}
    json.dump(R, open(os.path.join(carpeta, "_rendimiento.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)

    imp, sp = num(m.get("impressions")), num(m.get("spend"))
    ctr, cpc = num(m.get("ctr")), num(m.get("cpc"))
    print(f"✅ _rendimiento.json · {os.path.basename(os.path.abspath(carpeta))}")
    print(f"   ad_id        {R['ad_id']}")
    print(f"   impresiones  {imp:,.0f}" if imp is not None else "   impresiones  —")
    print(f"   gasto        {sp:,.2f}" if sp is not None else "   gasto        —")
    print(f"   CTR          {ctr:.2f}%" if ctr is not None else "   CTR          —")
    print(f"   CPC          {cpc:,.2f}" if cpc is not None else "   CPC          —")
    print(f"   fuente       {R['fuente']}  ← etiquetada a propósito: es dato de plataforma,")
    print(f"                no de disco ni inferencia.")
    if imp is not None and imp < 1000:
        print(f"\n   ⚠️  {imp:,.0f} impresiones: NO alcanza para comparar contra otros ads.")
        print(f"       La tabla lo va a listar aparte, no en el ranking.")
    return 0


# ─────────────────────────────────────────────────────────────────────────────
def decisiones(spec):
    """Las decisiones del pipeline que vale la pena correlacionar con el resultado."""
    slides = spec.get("slides") or []
    fuentes = [str(s.get("fuente") or "?") for s in slides]
    gen = sum(1 for f in fuentes if f.startswith("gener") or f == "ia")
    real = sum(1 for f in fuentes if f.startswith("real"))
    if gen and not real:
        img = "generada"
    elif real and not gen:
        img = "real"
    elif gen or real:
        img = "mixta"
    else:
        img = "?"
    return {"angulo": (spec.get("angulo") or "?")[:52],
            "formato": spec.get("formato") or "?",
            "framework": spec.get("framework") or "?",
            "imagen": img, "slides": len(slides)}


def cmd_tabla(madre, minimo):
    filas, sin_vol, sin_datos = [], [], []
    for h in carruseles(madre):
        spec = cargar(os.path.join(h, "carrusel.json"), {}) or {}
        R = cargar(os.path.join(h, "_rendimiento.json"))
        d = decisiones(spec)
        d["carrusel"] = os.path.basename(h)
        if not R:
            pub = cargar(os.path.join(h, "_publicado.json"))
            d["estado"] = "publicado, sin insights" if pub else "sin registro"
            sin_datos.append(d)
            continue
        m = R.get("metricas") or {}
        d.update({"imp": num(m.get("impressions")) or 0, "ctr": num(m.get("ctr")),
                  "cpc": num(m.get("cpc")), "spend": num(m.get("spend"))})
        (filas if d["imp"] >= minimo else sin_vol).append(d)

    print(f"\n── RENDIMIENTO · {os.path.basename(os.path.abspath(madre))} ──")
    print(f"   Fuente: PLATAFORMA (Meta) para las cifras · DISCO (carrusel.json) para las "
          f"decisiones.\n   Piso de volumen: {minimo:,} impresiones.")
    if filas:
        filas.sort(key=lambda x: (x["ctr"] is None, -(x["ctr"] or 0)))
        print(f"\n  {'carrusel':<26} {'imp':>9} {'CTR':>7} {'CPC':>8}  "
              f"{'img':<9} {'fórmula':<10} ángulo")
        for f in filas:
            ctr = f"{f['ctr']:.2f}%" if f["ctr"] is not None else "—"
            cpc = f"{f['cpc']:,.0f}" if f["cpc"] is not None else "—"
            print(f"  {f['carrusel']:<26} {f['imp']:>9,.0f} {ctr:>7} {cpc:>8}  "
                  f"{f['imagen']:<9} {f['framework']:<10} {f['angulo']}")

        # Agregados: la pregunta real no es qué ad ganó, es qué DECISIÓN gana.
        for eje, etiqueta in (("imagen", "foto real vs. generada"),
                              ("framework", "framework narrativo"),
                              ("formato", "formato")):
            g = {}
            for f in filas:
                g.setdefault(f[eje], []).append(f)
            if len(g) < 2:
                continue
            print(f"\n  ── por {etiqueta} ──")
            for k, v in sorted(g.items(), key=lambda kv: -sum(
                    (x["ctr"] or 0) for x in kv[1]) / len(kv[1])):
                ctrs = [x["ctr"] for x in v if x["ctr"] is not None]
                med = f"{sum(ctrs) / len(ctrs):.2f}%" if ctrs else "—"
                imp = sum(x["imp"] for x in v)
                print(f"     {k:<12} CTR medio {med:>7}   ({len(v)} pieza(s), "
                      f"{imp:,.0f} impresiones)")
            if min(len(v) for v in g.values()) < 3:
                print(f"     ⚠️  algún grupo tiene menos de 3 piezas: es una señal, "
                      f"no una conclusión.")
    else:
        print("\n  Ninguna pieza supera el piso de volumen todavía.")

    if sin_vol:
        print(f"\n  SIN VOLUMEN (<{minimo:,} impresiones — no entran al ranking):")
        for f in sin_vol:
            print(f"     {f['carrusel']:<26} {f['imp']:>9,.0f} impresiones")
    if sin_datos:
        print(f"\n  SIN DATOS ({len(sin_datos)}):")
        for f in sin_datos:
            print(f"     {f['carrusel']:<26} {f['estado']}")
        print("     «sin registro» ≠ «no se publicó»: El director creativo publica a mano.")
    print()
    return 0


# ─────────────────────────────────────────────────────────────────────────────
def main(argv):
    if not argv or argv[0] not in ("pendientes", "anotar", "tabla"):
        print(__doc__)
        return 2
    sub, resto = argv[0], argv[1:]

    def flag(n, d=None):
        return resto[resto.index(n) + 1] if n in resto and resto.index(n) + 1 < len(resto) else d

    pos = [a for i, a in enumerate(resto)
           if not a.startswith("--") and (i == 0 or not resto[i - 1].startswith("--"))]
    if not pos:
        print(__doc__)
        return 2
    carpeta = pos[0]
    if not os.path.isdir(carpeta):
        print(f"FAIL: no existe la carpeta {carpeta}")
        return 2

    if sub == "pendientes":
        return cmd_pendientes(carpeta, int(flag("--dias", 7)))
    if sub == "tabla":
        return cmd_tabla(carpeta, int(flag("--min", 1000)))
    origen = flag("--json")
    if not origen:
        print("Uso: rendimiento.py anotar <carpeta> --json <archivo|->")
        return 2
    return cmd_anotar(carpeta, origen)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
