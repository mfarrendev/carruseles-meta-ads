#!/usr/bin/env /usr/local/bin/python3
"""
qa_raw.py — AUDITORÍA DE LA FOTO CRUDA, antes de componer (RUBRIC A11 · pipeline Fase 4b).

Por qué existe (test de ads Claude Code, jul-2026): se compuso sobre 16 fotos recién generadas
sin mirarlas, y 8 traían LETRAS INVENTADAS por la IA (legends de teclas, pseudo-código en
pantallas, escritura en papeles). Los 16 prompts pedían "no text". El desastre apareció recién
en el doble juez, con la pieza ya armada. Esto lo caza en segundos, antes de gastar composición.

Chequea, por foto:
  1. TEXTO INVENTADO  — OCR con Vision (~/bin/ocr). La señal es el ÁREA, no el conteo:
     una foto limpia dio 30 detecciones ocupando 0.5%; una sucia, 20 ocupando 26%.
  2. ZONA RESERVADA   — con la máscara del sujeto (~/bin/cutout), ¿el recuadro donde irá el
     texto quedó realmente libre? El blueprint lo pide en el prompt pero solo se cumple en
     ~3 de cada 4 generaciones; hoy nadie lo mide hasta que la pieza está compuesta.

uso:
  qa_raw.py foto.png                        # solo texto inventado
  qa_raw.py foto.png --zone l               # + zona de texto (l | r | top | bot | cc)
  qa_raw.py c1/raw/*.png --zones c1/slides.json   # lote, leyendo la zona de cada slide
"""
import sys, os, json, subprocess

OCR    = os.path.expanduser("~/bin/ocr")
CUTOUT = os.path.expanduser("~/bin/cutout")

# --- umbrales (calibrados contra el lote real del test jul-2026) ---
# Medidos: fotos sucias 2.6 · 3.6 · 5.3 · 13.2 · 26.0 % · fotos limpias 0.0-0.5 %
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from constantes import (OCR_AREA_MAX as AREA_MAX, OCR_AREA_WARN as AREA_WARN,
                        OCR_ITEM_MAX as ITEM_MAX, OCR_CONF_MIN as CONF_MIN,
                        SUBJ_ZONA_MAX as SUBJ_MAX)

# ⚠️ LÍMITE CONOCIDO: los legends chicos de un teclado miden ~0.3%, por debajo del piso de
# ruido de una foto limpia (0.5%). Este gate caza los bloques que arruinan la pieza, NO el
# microtexto — eso sigue siendo trabajo del ojo a tamaño completo (regla de oro del SKILL).

ZONES = {   # recuadro donde caerá el texto, normalizado (x0, y0, x1, y1)
    "l":   (0.00, 0.00, 0.55, 1.00),
    "r":   (0.45, 0.00, 1.00, 1.00),
    "top": (0.00, 0.00, 1.00, 0.45),
    "bot": (0.00, 0.55, 1.00, 1.00),
    "cc":  (0.15, 0.25, 0.85, 0.75),
}

def _run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr

def texto_inventado(path):
    """→ (ok, detalle). Usa el ÁREA cubierta, no el número de detecciones."""
    if not os.path.exists(OCR):
        return None, "~/bin/ocr no existe (compilar: swiftc -O -o ~/bin/ocr templates/ocr.swift)"
    rc, out, err = _run([OCR, path])
    if rc != 0:
        return None, f"ocr falló: {err.strip()[:60]}"
    d = json.loads(out)
    todos = d.get("items", [])
    # Se separan por confianza: los flojos NO reprueban, pero tampoco se tiran a la basura.
    items = [i for i in todos if i.get("conf", 1.0) >= CONF_MIN]
    flojos = [i for i in todos if i.get("conf", 1.0) < CONF_MIN]
    area  = sum(i["box"][2] * i["box"][3] for i in items)
    peor  = max((i["box"][2] * i["box"][3] for i in items), default=0.0)
    def _muestra(xs):
        return "; ".join(f'«{i["text"][:22]}»' for i in
                         sorted(xs, key=lambda i: -i["box"][2] * i["box"][3])[:3])
    det = f"texto {area*100:.1f}% del cuadro (FAIL >{AREA_MAX*100:.0f}%), mayor bloque {peor*100:.1f}%"
    if area > AREA_MAX or peor > ITEM_MAX:
        return False, det + f" · {_muestra(items)}"
    if flojos:
        cola = (f" · {len(flojos)} detección(es) bajo conf {CONF_MIN} "
                f"({sum(i['box'][2]*i['box'][3] for i in flojos)*100:.1f}% del cuadro): "
                f"{_muestra(flojos)} — mirar a tamaño completo antes de descartarlas")
        return None, det + cola
    if area > AREA_WARN:
        return None, det + f" · zona gris, mirar a tamaño completo · {_muestra(items)}"
    return True, det

def zona_libre(path, zone):
    """→ (ok, detalle). ¿El recuadro planificado para el texto quedó sin sujeto?"""
    if zone not in ZONES:
        return None, f"zona '{zone}' desconocida"
    if not os.path.exists(CUTOUT):
        return None, "~/bin/cutout no existe"
    import tempfile
    from PIL import Image
    import numpy as np
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as t:
        mp = t.name
    rc, _, err = _run([CUTOUT, path, mp, "--mask"])
    if rc != 0:
        os.unlink(mp) if os.path.exists(mp) else None
        return None, "sin sujeto detectado (foto de objeto/escena)"
    m = np.asarray(Image.open(mp).convert("L"), dtype=np.float32) / 255.0
    os.unlink(mp)
    h, w = m.shape
    x0, y0, x1, y1 = ZONES[zone]
    caja = m[int(y0*h):int(y1*h), int(x0*w):int(x1*w)]
    ocup = float((caja > 0.5).mean())
    return ocup <= SUBJ_MAX, f"sujeto ocupa {ocup*100:.1f}% de la zona '{zone}' (máx {SUBJ_MAX*100:.0f}%)"

def main(argv):
    zonas = {}
    if "--zones" in argv:
        i = argv.index("--zones")
        spec = json.load(open(argv[i+1], encoding="utf-8"))
        for n, s in enumerate(spec["slides"], 1):
            zonas[f"s-{n:02d}"] = s.get("zone")
        argv = argv[:i] + argv[i+2:]
    zona_fija = None
    if "--zone" in argv:
        i = argv.index("--zone"); zona_fija = argv[i+1]; argv = argv[:i] + argv[i+2:]

    fail = False
    for f in argv:
        base = os.path.splitext(os.path.basename(f))[0]
        print(f"\n{f}")
        ok, det = texto_inventado(f)
        print(f"  {'PASS' if ok else 'FAIL' if ok is False else 'WARN'}  texto inventado · {det}")
        if ok is False: fail = True
        z = zona_fija or zonas.get(base)
        if z:
            ok2, det2 = zona_libre(f, z)
            print(f"  {'PASS' if ok2 else 'FAIL' if ok2 is False else 'WARN'}  zona reservada · {det2}")
            if ok2 is False: fail = True
    print("\nRAW:", "FAIL" if fail else "PASS")
    return 1 if fail else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
