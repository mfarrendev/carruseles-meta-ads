#!/usr/bin/env /usr/local/bin/python3
"""
aprobar.py — CONGELAR LO QUE DIRECTOR APROBÓ (5-ago-2026)

    aprobar.py <carpeta> --por "esos están buenos, los apruebo"   → aprobado/<fecha>/
    aprobar.py <carpeta> --listar                                 → qué versiones hay
    aprobar.py <carpeta> --comparar                               → ahora vs. lo aprobado
    aprobar.py <carpeta-madre> --lote --por "…"                   → congela todo el lote

POR QUÉ EXISTE
Cuando el director creativo dice *"esos están buenos, yo los apruebo"*, hoy no pasa NADA en el disco. Los
`s-NN.png` siguen siendo los mismos archivos que el próximo `engine.py` va a sobrescribir. Eso
ya costó caro dos veces el 5 de agosto:

  · el preset de marca de Marca Verde desapareció al sincronizar `styles.css` — el render aprobado
    se re-generó con la identidad de otro cliente y no quedó copia del bueno;
  · tres cambios al motor en un día rompieron algo distinto cada vez, y **los tres pasaron las
    siete compuertas en verde**. Sin una copia congelada no había contra qué comparar.

Un OK que no deja artefacto no es un punto de retorno: es una frase en un chat que se pierde
al compactar el contexto.

QUÉ CONGELA
Los PNG finales, los thumbnails, el spec, los recibos y el `_build-report.json` — todo lo que
hace falta para (a) volver a este estado y (b) comparar contra él. Lo pesado (`raw/`,
`_descartados/`) NO se copia: pueden ser cientos de MB y no son la pieza aprobada.

La copia queda en `aprobado/<AAAA-MM-DD-HHMM>/` y se marca **de solo lectura** (chmod 444). No
es una cárcel — un `chmod +w` la abre — es un freno físico contra el sobrescribir distraído,
que es exactamente como se perdió el render bueno.
"""
import sys, os, json, glob, shutil, time, stat

COPIAR = ("s-*.png", "s-*.html", "_thumb-*.png", "carrusel.json", "_brief.md",
          "caption.md", "*-receipt.json", "_build-report.json", "_costo.json",
          "_proceso.md", "styles.css")
NO_COPIAR = ("raw", "_descartados", "aprobado", "__pycache__", "node_modules")


def solo_lectura(ruta):
    for base, dirs, files in os.walk(ruta):
        for f in files:
            p = os.path.join(base, f)
            try:
                os.chmod(p, os.stat(p).st_mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))
            except OSError:
                pass


def cmd_listar(carpeta):
    base = os.path.join(carpeta, "aprobado")
    vers = sorted(glob.glob(os.path.join(base, "*"))) if os.path.isdir(base) else []
    print(f"\n── APROBADOS · {os.path.basename(os.path.abspath(carpeta))} ──")
    if not vers:
        print("  ninguno. Cuando el director creativo diga «lo apruebo», congelarlo:")
        print(f"     aprobar.py {carpeta} --por \"<lo que dijo, textual>\"")
        return 0
    for v in vers:
        meta = {}
        try:
            meta = json.load(open(os.path.join(v, "_aprobacion.json"), encoding="utf-8"))
        except Exception:
            pass
        pngs = len(glob.glob(os.path.join(v, "s-*.png")))
        print(f"  {os.path.basename(v):<22} {pngs} slides   "
              f"«{(meta.get('por') or '—')[:60]}»")
    print(f"\n  Comparar el render de ahora contra el último aprobado:")
    print(f"     aprobar.py {carpeta} --comparar")
    return 0


def cmd_comparar(carpeta):
    """El render de AHORA contra el último aprobado. Es la pregunta que las siete compuertas
    no contestan: no «¿está mal?» sino «¿cambió algo que el director creativo no pidió que cambiara?»."""
    base = os.path.join(carpeta, "aprobado")
    vers = sorted(glob.glob(os.path.join(base, "*"))) if os.path.isdir(base) else []
    if not vers:
        print(f"FAIL: no hay ninguna versión aprobada de {carpeta} contra la cual comparar.")
        return 2
    ref = vers[-1]
    try:
        from PIL import Image
        import numpy as np
    except ImportError:
        print("FAIL: falta PIL/numpy. Correr con /usr/local/bin/python3.")
        return 2

    print(f"\n── AHORA vs. APROBADO {os.path.basename(ref)} ──")
    cambios, faltan = [], []
    for p in sorted(glob.glob(os.path.join(ref, "s-*.png"))):
        n = os.path.basename(p)
        actual = os.path.join(carpeta, n)
        if not os.path.exists(actual):
            faltan.append(n)
            continue
        A = np.asarray(Image.open(p).convert("RGB"), dtype=np.int16)
        B = np.asarray(Image.open(actual).convert("RGB"), dtype=np.int16)
        if A.shape != B.shape:
            print(f"  ⚠️  {n:<12} cambió el TAMAÑO del lienzo: {A.shape[1]}×{A.shape[0]} "
                  f"→ {B.shape[1]}×{B.shape[0]}")
            cambios.append(n)
            continue
        D = np.abs(A - B)
        media, pico = float(D.mean()), float((D.max(axis=2) > 24).mean())
        if media < 0.5:
            print(f"  ·   {n:<12} idéntico")
        else:
            print(f"  ⚠️  {n:<12} dif media {media:6.2f} · {pico:.1%} de los píxeles")
            cambios.append(n)
    for n in faltan:
        print(f"  ⛔  {n:<12} YA NO EXISTE en la carpeta")
    if faltan:
        cambios += faltan
    nuevas = [os.path.basename(p) for p in sorted(glob.glob(os.path.join(carpeta, "s-*.png")))
              if not os.path.exists(os.path.join(ref, os.path.basename(p)))]
    for n in nuevas:
        print(f"  +   {n:<12} slide nueva (no estaba en lo aprobado)")

    if not cambios and not nuevas:
        print(f"\n✅ el render es el que el director creativo aprobó.")
        return 0
    print(f"\n⚠️  {len(cambios) + len(nuevas)} slide(s) distintas de lo aprobado.")
    print(f"   Si el cambio es el que él pidió, congelalo de nuevo con --por «…».")
    print(f"   Si NO lo pidió, es una regresión: los gates no la cazan porque miden lo que")
    print(f"   está mal, no lo que cambió.")
    return 1


def cmd_aprobar(carpeta, razon):
    slides = glob.glob(os.path.join(carpeta, "s-*.png"))
    if not slides:
        print(f"FAIL: no hay ningún s-NN.png en {carpeta}. No se congela una carpeta sin pieza.")
        return 2

    # El recibo de QA se copia tal cual esté — incluso en FAIL. Un aprobado del director creativo pisa
    # la compuerta (jerarquía de mando #1), pero el recibo NO se maquilla: queda el registro
    # de que se aprobó con el QA en rojo, que es un dato, no una vergüenza.
    qa = os.path.join(carpeta, "_qa-receipt.json")
    estado_qa = "sin recibo"
    if os.path.exists(qa):
        try:
            R = json.load(open(qa, encoding="utf-8"))
            # Los recibos de los jueces usan `verdict`; los de script, `status`. Mirar los dos:
            # leer solo uno reportaba «?» sobre un FAIL real, que es peor que no reportar nada.
            estado_qa = R.get("verdict") or R.get("status") or "sin veredicto"
        except Exception:
            estado_qa = "ilegible"

    destino = os.path.join(carpeta, "aprobado", time.strftime("%Y-%m-%d-%H%M"))
    if os.path.exists(destino):
        print(f"FAIL: ya existe {destino} (mismo minuto). Esperá 60 s o borralo a mano.")
        return 2
    os.makedirs(destino)

    copiados = 0
    for patron in COPIAR:
        for p in glob.glob(os.path.join(carpeta, patron)):
            if not os.path.isfile(p) or os.path.basename(p) in NO_COPIAR:
                continue
            shutil.copy2(p, os.path.join(destino, os.path.basename(p)))
            copiados += 1

    meta = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "por": razon, "quien": "El director creativo",
            "carpeta_origen": os.path.abspath(carpeta),
            "slides": len(slides), "archivos": copiados,
            "qa_receipt_al_aprobar": estado_qa,
            "nota": ("Copia inmutable del render aprobado. Si el motor cambia, ESTA es la "
                     "referencia contra la que se compara. Los raw/ no se copian a propósito.")}
    json.dump(meta, open(os.path.join(destino, "_aprobacion.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    solo_lectura(destino)

    print(f"\n🔒 CONGELADO · {os.path.relpath(destino, carpeta)}")
    print(f"   slides       {len(slides)}")
    print(f"   archivos     {copiados} (+ _aprobacion.json)")
    print(f"   QA al aprobar {estado_qa}")
    if estado_qa not in ("PASS", "PASS_CON_WARNS"):
        print(f"   ⚠️  se congeló con el QA en «{estado_qa}». Queda registrado tal cual:")
        print(f"       el director creativo pisa la compuerta, pero el recibo no se maquilla.")
    print(f"   razón        «{razon}»")
    print(f"\n   Solo lectura. El próximo engine.py ya no puede pisar esta copia.")
    return 0


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    carpeta = argv[0]
    if not os.path.isdir(carpeta):
        print(f"FAIL: no existe la carpeta {carpeta}")
        return 2
    resto = argv[1:]

    def flag(n, d=None):
        return resto[resto.index(n) + 1] if n in resto and resto.index(n) + 1 < len(resto) else d

    if "--listar" in resto:
        return cmd_listar(carpeta)
    if "--comparar" in resto:
        return cmd_comparar(carpeta)
    razon = flag("--por")
    if not razon:
        print("FAIL: falta --por \"<lo que dijo el director creativo, textual>\".\n"
              "      Un congelado sin la frase que lo motivó no dice QUÉ se aprobó ni bajo\n"
              "      qué condición (ej. «los apruebo pero bajá a verde suave en la última»).")
        return 2

    if "--lote" in resto:
        hijos = sorted(d for d in glob.glob(os.path.join(carpeta, "*"))
                       if os.path.isdir(d) and glob.glob(os.path.join(d, "s-*.png")))
        if not hijos:
            print(f"FAIL: ninguna subcarpeta de {carpeta} tiene slides renderizadas")
            return 2
        malos = 0
        for h in hijos:
            malos += 1 if cmd_aprobar(h, razon) else 0
        print(f"\n── {len(hijos) - malos} de {len(hijos)} carruseles congelados ──")
        return 2 if malos else 0
    return cmd_aprobar(carpeta, razon)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
