#!/usr/bin/env /usr/local/bin/python3
"""
costo.py — LA CUENTA DE LO QUE CUESTA UNA PIEZA (5-ago-2026).

    costo.py estado     <carpeta>                        → cuánto lleva vs. presupuesto
    costo.py presupuesto <carpeta> N                     → declara el tope en carrusel.json
    costo.py descartar  <carpeta> <archivo> --por "…"    → archiva el crudo + anota por qué
    costo.py lote       <carpeta-madre>                  → la cuenta de todo el lote

POR QUÉ EXISTE
Medición del 4-5 de agosto de 2026 (libro de Higgsfield, no estimación): para entregar
4 carruseles Marca Verde —**20 fotos usadas**— pasaron **255 generaciones de imagen**, 49 upscales
y 6 recortes de fondo. **717 créditos.** En el disco quedaron 21 crudos. Las otras 234 se
generaron, se miraron, se descartaron y no dejaron rastro: ni un contador, ni el prompt que
falló, ni el motivo. Tasa de uso: **8%**.

Dos agujeros distintos, y este archivo tapa el segundo:

  1. NADIE CONTABA  → lo arregla el par de hooks `costo-imagenes.py` (PostToolUse, anota) +
     `carrusel-gate.py::presupuesto` (PreToolUse, frena). Automáticos: no dependen de que
     el agente se acuerde de registrar.
  2. EL DESCARTE NO ENSEÑABA → lo arregla `descartar`. Borrar una foto mala destruye la única
     evidencia de por qué el prompt falla; a la media hora el mismo prompt se vuelve a pedir
     con otra semilla y vuelve a salir mal. `prompts-validados.md` solo guardaba los éxitos:
     un catálogo de aciertos sin anti-catálogo hace repetir los errores gratis.

Regla que sale de ahí: **un crudo rechazado se ARCHIVA con su motivo, no se borra.**
El motivo se acumula en `references/prompts-fallidos.md`, que se lee ANTES de regenerar.
"""
import sys, os, json, time, glob, shutil, re

AQUI = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(AQUI)
ANTI = os.path.join(SKILL, "references", "prompts-fallidos.md")

# Motivos canónicos de descarte. Cerrada a propósito: un campo de texto libre produce
# 234 motivos distintos y ninguno agrupable, que es exactamente el problema que no queríamos.
MOTIVOS = {
    "texto-inventado": "letras/números basura en pantallas, teclas, papeles, carteles",
    "anatomia": "manos, dedos, brazos o postura imposibles",
    "logo-real": "logo o marca de un tercero visible (riesgo de baneo en Meta)",
    "personaje": "la mascota/persona no es la misma (falló el Reference Element)",
    "encuadre": "el sujeto queda cortado o fuera de la zona que pedía el blueprint",
    "no-demuestra": "linda, pero no muestra lo que dice el texto de la slide",
    "zona-ocupada": "no dejó libre el hueco donde va el texto",
    "fondo": "fondo plano, sucio o que pelea con la marca",
    "otro": "cualquier otra cosa — describila en --nota",
}


def cargar(carpeta, nombre, x=None):
    try:
        return json.load(open(os.path.join(carpeta, nombre), encoding="utf-8"))
    except Exception:
        return x


def tope_de(carpeta):
    """(tope, declarado?) — el mismo cálculo que usa el hook, para que el número que se ve
    acá y el que frena la puerta no puedan discrepar."""
    spec = cargar(carpeta, "carrusel.json", {}) or {}
    n = max(1, len(spec.get("slides") or []))
    d = spec.get("presupuesto_imagenes")
    # Max, 7-sep-2026: el default es UNA pasada — una generación por slide y se muestra.
    # Antes era slides × 3 (el intento + 2 reintentos automáticos). Los reintentos ya no
    # son automáticos: si algo sale mal se reporta y Max decide si vale gastar otra.
    return (int(d), True) if d else (n, False)


def cmd_estado(carpeta):
    L = cargar(carpeta, "_costo.json")
    tope, declarado = tope_de(carpeta)
    usados = len([p for p in glob.glob(os.path.join(carpeta, "raw", "*"))
                  if os.path.isfile(p) and not os.path.basename(p).startswith("_")])
    desc = len([p for p in glob.glob(os.path.join(carpeta, "raw", "_descartados", "*.*"))
                if not os.path.basename(p).startswith("_")])
    print(f"\n── COSTO · {os.path.basename(os.path.abspath(carpeta))} ──")
    if not L:
        print("  sin _costo.json — no se generó nada por este agente, o se generó antes del "
              "contador (5-ago-2026).")
    else:
        gen, cr = int(L.get("total", 0)), L.get("creditos", 0)
        barra = "█" * min(30, int(30 * gen / max(1, tope))) + "·" * max(0, 30 - int(30 * gen / max(1, tope)))
        print(f"  generaciones   {gen:>4}   [{barra}]  tope {tope} "
              f"({'declarado' if declarado else 'por defecto'})")
        print(f"  créditos       ~{cr}")
        if gen:
            print(f"  rendimiento    {usados} crudos en disco de {gen} generadas "
                  f"= {usados / gen:.0%} aprovechado")
    print(f"  crudos en raw/ {usados:>4}")
    print(f"  descartados    {desc:>4}   {'(archivados, con motivo)' if desc else '(ninguno archivado)'}")
    if L and int(L.get("total", 0)) >= tope:
        print(f"\n  ⛔ presupuesto agotado — la puerta GENERAR va a preguntar antes de la próxima.")
        print(f"     Si de verdad hacen falta más:  costo.py presupuesto {carpeta} <N>")
    return 0


def cmd_presupuesto(carpeta, n, por=None):
    """Declara el tope. SUBIRLO exige un motivo escrito; bajarlo o fijarlo de entrada, no.

    Por qué la asimetría (6-ago-2026): el tope solo sirve si romperlo cuesta algo. Si subirlo
    fuera un comando mudo, la salida barata seguiría siendo subirlo — que es exactamente el
    bucle que dejó 255 generaciones sin que nadie lo supiera. El motivo queda en el spec."""
    p = os.path.join(carpeta, "carrusel.json")
    spec = cargar(carpeta, "carrusel.json")
    if spec is None:
        print(f"FAIL: no hay carrusel.json en {carpeta} — corré verify.py init primero.")
        return 2
    n_slides = max(1, len(spec.get("slides") or []))
    antes = spec.get("presupuesto_imagenes") or n_slides * 3
    if int(n) > int(antes) and not por:
        print(f"FAIL: subir el tope ({antes} → {n}) exige --por \"<motivo>\".\n"
              f"      Un tope que se sube sin decir por qué no es un tope.\n"
              f"      Antes de subirlo: ¿el prompt que falla está en prompts-fallidos.md?\n"
              f"      ¿Hace falta otra FOTO, o solo otro ENCUADRE (`zoom` = 0 créditos)?")
        return 2
    spec["presupuesto_imagenes"] = int(n)
    if por:
        hist = spec.setdefault("presupuesto_historial", [])
        hist.append({"ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
                     "de": int(antes), "a": int(n), "por": por})
    json.dump(spec, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"✅ presupuesto_imagenes: {antes} → {n}" + (f"\n   motivo: «{por}»" if por else ""))
    print("   Queda declarado en el spec: auditable, y es lo que lee la puerta GENERAR.")
    return 0


def cmd_descartar(carpeta, archivo, motivo, nota, prompt):
    if motivo not in MOTIVOS:
        print(f"FAIL: motivo «{motivo}» no está en la lista. Elegí uno:\n" +
              "\n".join(f"  {k:<16} {v}" for k, v in MOTIVOS.items()))
        return 2
    src = archivo if os.path.isabs(archivo) else os.path.join(carpeta, archivo)
    if not os.path.isfile(src):
        alt = os.path.join(carpeta, "raw", os.path.basename(archivo))
        if os.path.isfile(alt):
            src = alt
        else:
            print(f"FAIL: no existe {src}")
            return 2
    dest_dir = os.path.join(carpeta, "raw", "_descartados")
    os.makedirs(dest_dir, exist_ok=True)
    base, ext = os.path.splitext(os.path.basename(src))
    dest = os.path.join(dest_dir, f"{base}--{motivo}{ext}")
    i = 2
    while os.path.exists(dest):
        dest = os.path.join(dest_dir, f"{base}--{motivo}-{i}{ext}")
        i += 1
    shutil.move(src, dest)

    reg = os.path.join(dest_dir, "_motivos.json")
    R = cargar(dest_dir, "_motivos.json", []) or []
    R.append({"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "archivo": os.path.basename(dest),
              "motivo": motivo, "nota": nota or "", "prompt": (prompt or "")[:400]})
    json.dump(R, open(reg, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print(f"📦 archivado  {os.path.relpath(dest, carpeta)}")
    print(f"   motivo     {motivo} — {MOTIVOS[motivo]}")
    if nota:
        print(f"   nota       {nota}")
    print(f"\n   El crudo NO se borró: es la evidencia de por qué ese prompt falla.")
    if not prompt:
        print(f"   ⚠️  Sin --prompt no se puede alimentar el anti-catálogo. Si el fallo se "
              f"repite,\n       escribilo a mano en references/prompts-fallidos.md.")
    else:
        print(f"   Si este motivo ya salió 2 veces, va a references/prompts-fallidos.md "
              f"ANTES de regenerar.")
    return 0


def cmd_lote(madre):
    hijos = sorted(d for d in glob.glob(os.path.join(madre, "*"))
                   if os.path.isdir(d) and os.path.exists(os.path.join(d, "carrusel.json")))
    if not hijos:
        print(f"FAIL: ninguna subcarpeta de {madre} tiene carrusel.json")
        return 2
    tg = tc = tu = td = 0
    print(f"\n── COSTO DEL LOTE · {os.path.basename(os.path.abspath(madre))} ──")
    print(f"  {'carrusel':<28} {'gen':>5} {'créd':>7} {'usados':>7} {'desc':>5}  {'aprov':>6}")
    for h in hijos:
        L = cargar(h, "_costo.json", {}) or {}
        g, c = int(L.get("total", 0)), float(L.get("creditos", 0))
        u = len([p for p in glob.glob(os.path.join(h, "raw", "*"))
                 if os.path.isfile(p) and not os.path.basename(p).startswith("_")])
        dd = len([p for p in glob.glob(os.path.join(h, "raw", "_descartados", "*.*"))
                  if not os.path.basename(p).startswith("_")])
        tg, tc, tu, td = tg + g, tc + c, tu + u, td + dd
        ap = f"{u / g:.0%}" if g else "—"
        print(f"  {os.path.basename(h):<28} {g:>5} {c:>7.1f} {u:>7} {dd:>5}  {ap:>6}")
    ap = f"{tu / tg:.0%}" if tg else "—"
    print(f"  {'─' * 62}")
    print(f"  {'TOTAL':<28} {tg:>5} {tc:>7.1f} {tu:>7} {td:>5}  {ap:>6}")
    if tg and tu / tg < 0.35:
        print(f"\n  ⚠️  Aprovechamiento {ap}: se está generando mucho más de lo que se usa. "
              f"Antes de\n      seguir, leer references/prompts-fallidos.md y "
              f"raw/_descartados/_motivos.json:\n      si el mismo motivo se repite, el "
              f"problema es el PROMPT, no la semilla.")
    return 0


def main(argv):
    if not argv or argv[0] not in ("estado", "presupuesto", "descartar", "lote"):
        print(__doc__)
        return 2
    sub = argv[0]
    pos = [a for i, a in enumerate(argv[1:])
           if not a.startswith("--") and (i == 0 or not argv[1:][i - 1].startswith("--"))]
    if not pos:
        print(__doc__)
        return 2
    carpeta = pos[0]
    if not os.path.isdir(carpeta):
        print(f"FAIL: no existe la carpeta {carpeta}")
        return 2

    def flag(n):
        return argv[argv.index(n) + 1] if n in argv and argv.index(n) + 1 < len(argv) else None

    if sub == "estado":
        return cmd_estado(carpeta)
    if sub == "lote":
        return cmd_lote(carpeta)
    if sub == "presupuesto":
        if len(pos) < 2 or not pos[1].isdigit():
            print("Uso: costo.py presupuesto <carpeta> <N> [--por \"<motivo>\"]\n"
                  "     El --por es obligatorio para SUBIR el tope, no para fijarlo o bajarlo.")
            return 2
        return cmd_presupuesto(carpeta, int(pos[1]), flag("--por"))
    if sub == "descartar":
        if len(pos) < 2:
            print("Uso: costo.py descartar <carpeta> <archivo> --por <motivo> "
                  "[--nota '…'] [--prompt '…']\nMotivos:\n" +
                  "\n".join(f"  {k:<16} {v}" for k, v in MOTIVOS.items()))
            return 2
        motivo = flag("--por")
        if not motivo:
            print("FAIL: falta --por <motivo>. Un descarte sin motivo no enseña nada, que es "
                  "justo lo que\n      pasó con las 234 generaciones del 4-5 de agosto.\n" +
                  "\n".join(f"  {k:<16} {v}" for k, v in MOTIVOS.items()))
            return 2
        return cmd_descartar(carpeta, pos[1], motivo, flag("--nota"), flag("--prompt"))
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
