#!/usr/bin/env /usr/local/bin/python3
"""
qa_lines.py — LOS QUIEBRES DEL SPEC SE RESPETAN (composicion-y-tipografia.md §5).

Por qué existe (test de ads Claude Code, jul-2026): el builder unía las líneas con <br>
("nada de wrap del navegador") pero el contenedor era más angosto que la línea más larga,
así que **el navegador re-partía igual**. 3 líneas del spec salieron 5, con huérfanas
(`tú.`, `cae`, `tu`, `que`) — en 10 de 18 slides, y justo en los cuatro hooks de apertura.
Ni el ojo ni los otros gates lo veían: el texto estaba "bien" y el spec también.

Mide con la FUENTE REAL al PESO REAL (montwidth) que cada línea entra en su contenedor.
Si no entra, el navegador la va a partir → FAIL antes de renderizar.

uso:
  qa_lines.py slides.json --font assets/SpaceGrotesk-700.woff2 --width 640 \\
              --size 92 --hero 100 --small 68 [--weight 700] [--tracking -0.02]
"""
import sys, os, json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import montwidth

CONECTORES = {"y","o","u","e","de","del","la","el","los","las","un","una","que","con",
              "por","para","en","al","se","su","sus","lo","como","más","mas","a","sin"}

# el ancho disponible NO es uno solo: depende de la zona (columna lateral vs cuadro completo)
LATERALES = {"l", "r"}

def _lineas_de(s):
    """Las líneas del título de UNA slide → (lineas, explícitas).

    El spec real usa la clave `titulo` (string, los quiebres los hace el motor); los specs
    antiguos usan `title` (a veces lista de líneas ya quebradas). Bug de auditoría (T9):
    acá se leía SOLO `title`, así que sobre los specs actuales `lineas` salía [] y el gate
    devolvía PASS sin medir una sola línea — para siempre.
    - lista, o string con <br>/\\n  → quiebres EXPLÍCITOS del spec: se respetan y se miden
      línea por línea (es lo que este gate existe para proteger).
    - string plano  → el wrap lo hace el motor/navegador: se simula el wrap codicioso con la
      fuente real y se verifica que NINGUNA línea resultante se pase (solo puede fallar una
      palabra larga inquebrable)."""
    import re as _re
    # Los títulos llevan destaque inline con <em> (regla el director creativo, 5-ago-2026). Los tags NO son
    # glifos: medirlos suma ~9 caracteres fantasma y este gate reprobaba líneas que en pantalla
    # entran de sobra («<em>tiempo</em>» daba 898px donde «tiempo» da ~330px). Se quitan DESPUÉS
    # de partir por <br> — ese sí es un quiebre real del spec — y antes de medir nada.
    quita = lambda x: _re.sub(r"<(?!br\b)[^>]+>", "", str(x))
    t = s.get("titulo") or s.get("title") or []
    if isinstance(t, list):
        return [quita(x) for x in t], True
    partes = [quita(p) for p in _re.split(r"<br\s*/?>|\n", t) if p.strip()]
    return (partes, len(partes) > 1)

def _wrap(lineas, px, width_px, font, weight, tracking):
    """Wrap codicioso con la fuente real: lo mínimo que hará el navegador."""
    out = []
    for ln in lineas:
        cur = ""
        for w in ln.replace("_", "").split():
            cand = (cur + " " + w).strip()
            if cur and montwidth.width(cand, px, font, weight=weight, tracking_em=tracking) > width_px:
                out.append(cur); cur = w
            else:
                cur = cand
        if cur:
            out.append(cur)
    return out

def revisar(spec_path, font, w_side, w_full, size, hero, small, weight, tracking):
    spec = json.load(open(spec_path, encoding="utf-8"))
    fail = False
    medidos = 0                     # piso de cordura: cuántas líneas se midieron de verdad
    for n, s in enumerate(spec["slides"], 1):
        lineas, explicitas = _lineas_de(s)
        px = hero if s.get("hero") else (small if s.get("small") else size)
        width_px = w_side if s.get("zone") in LATERALES else w_full
        if lineas and not explicitas:
            lineas = _wrap(lineas, px, width_px, font, weight, tracking)
        for i, ln in enumerate(lineas, 1):
            texto = ln.replace("_", "")            # el _acento_ no cambia el ancho
            if not texto.strip():
                continue
            medidos += 1
            w = montwidth.width(texto, px, font, weight=weight, tracking_em=tracking)
            if w > width_px:
                print(f"  FAIL s-{n:02d} L{i}: «{texto}» mide {w:.0f}px > {width_px}px "
                      f"→ el navegador la va a re-partir  (bajar a ~{px*width_px/w:.0f}px o ensanchar)")
                fail = True
        if not explicitas:
            continue    # huérfanas/conectores aplican a quiebres ELEGIDOS en el spec
        # huérfana: última línea de 1 palabra cuando el bloque tiene 3+
        if len(lineas) >= 3:
            ult = lineas[-1].replace("_", "").strip().rstrip(".,;:»")
            if ult and len(ult.split()) == 1:
                print(f"  FAIL s-{n:02d}: última línea huérfana «{lineas[-1]}»")
                fail = True
        # ninguna línea puede terminar en conector
        for i, ln in enumerate(lineas[:-1], 1):
            ultima = ln.replace("_", "").strip().rstrip(".,;:«»").split()
            if ultima and ultima[-1].lower() in CONECTORES:
                print(f"  FAIL s-{n:02d} L{i}: termina en conector «{ultima[-1]}» → mover a la línea siguiente")
                fail = True
    if not medidos:
        # PISO DE CORDURA (regla de clase entera, auditoría T9): una compuerta tiene que
        # AFIRMAR que vio algo. "0 elementos revisados" sobre un spec que existe no es PASS:
        # es que la compuerta no midió nada — y un gate que no mide nada no puede pasar.
        print("  FAIL 0 elementos revisados: la compuerta no midió nada "
              "(¿el spec tiene 'titulo' en las slides?)")
        fail = True
    return fail

def main(a):
    if not a:
        print(__doc__); return 2
    spec = a[0]
    def opt(name, default, cast=float):
        return cast(a[a.index(name)+1]) if name in a else default
    font = a[a.index("--font")+1] if "--font" in a else None
    if not font or not os.path.exists(font):
        print(f"FAIL: falta --font o no existe ({font})"); return 2
    if not montwidth.available():
        print("FAIL: montwidth necesita fontTools+brotli (usar /usr/local/bin/python3)"); return 2
    w_side = opt("--width", 640.0)      # columna lateral (.stack.l/.r)
    w_full = opt("--width-full", 952.0) # cuadro completo menos márgenes (.stack.c/.cc)
    size  = opt("--size", 92.0)
    hero  = opt("--hero", size)
    small = opt("--small", size)
    weight= opt("--weight", 700, int)
    track = opt("--tracking", -0.02)
    print(f"=== QUIEBRES · {spec} · lateral {w_side:.0f}px / completo {w_full:.0f}px · {os.path.basename(font)} @{weight} ===")
    fail = revisar(spec, font, w_side, w_full, size, hero, small, weight, track)
    print("LINES:", "FAIL" if fail else "PASS")
    return 1 if fail else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
