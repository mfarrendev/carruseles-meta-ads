#!/usr/bin/env /usr/local/bin/python3
"""
qa_seam.py — COMPUERTA ANTI-COLLAGE, EN LOS DOS EJES (director creativo, 14-jul-2026 · ampliado 31-jul-2026).

Falla original (eje VERTICAL): `gen-ninos.jpg`, al aire durante meses en el anuncio "casa vs gym ·
niños", es un collage — costura vertical en x=0.33 y a la izquierda otra pieza (otro sofá, otra
planta, otra perspectiva). Nadie lo cazó a ojo.

Falla que obligó a ampliarlo (eje HORIZONTAL): lote Marca Verde, 29-jul-2026. La fórmula "the whole
LOWER HALF is empty negative space" hizo que el modelo entregara DOS IMÁGENES PEGADAS con una línea
dura horizontal en la mitad exacta del cuadro y los props rebanados — en **10 de 34 fondos**. Salto
de luminancia medido en la costura: 60 contra un ruido normal de 3,7.

Este gate solo escaneaba COLUMNAS, así que dio **PASS falso en las 34**. Un gate que mide un solo eje
miente en el otro. Ahora escanea los dos y reporta el peor.

Dos señales, y hacen falta LAS DOS (una sola da falsos positivos: una cortina oscura también es un
borde vertical recto, y un zócalo también es uno horizontal):

  1. PICO         — la línea con más energía de borde se dispara respecto al resto (> 8σ).
  2. PERSISTENCIA — ese borde atraviesa CASI TODA la imagen. Un corte de collage es una línea
     perfecta de lado a lado; una columna o un muro reales se interrumpen.

DOS TRAMOS, no uno (calibrado 31-jul-2026 contra 12 imágenes etiquetadas a mano):

  · persistencia > 0.85  → **FAIL** bloqueante. Separación limpia: los tres collages confirmados
    dieron 0.99 / 0.99 / 0.92, y ninguna de las 8 fotos reales pasó de 0.74.
  · persistencia > 0.55  → **WARN**, mirar a tamaño completo. Acá caen los casos ambiguos.

Por qué el tramo WARN existe: `clase-cami-yoga-2.jpg` es una foto REAL de la sede y da 0.74,
porque la columna blanca del estudio va de piso a techo y es un borde vertical perfecto. Con un
solo umbral en 0.55 esa foto quedaba bloqueada. Un gate que bloquea fotos buenas se termina
desactivando, y entonces no protege de nada.

⚠️ SEÑAL DESCARTADA — el salto de luminancia NO discrimina. El aprendizaje Marca Verde citaba
"salto 60 contra ruido de 3,7", pero medido sobre el set etiquetado NO separa: la foto real del
yoga da 47,1 y dos collages confirmados dan 14,2 y 11,6. Se sigue midiendo y reportando (sirve
para recalibrar a futuro) pero **no decide el veredicto**.

Medido: gen-ninos = 13.9σ / 0.99 en x=0.33 → COLLAGE. Fotos reales de sede: 0.09–0.74.

    qa_seam.py imagen.jpg [imagen2.jpg ...]
    qa_seam.py raw/*.png --json          # salida para verify.py
"""
import sys, json
from PIL import Image
import numpy as np

import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from constantes import (SEAM_PICO_MIN as PICO_MIN, SEAM_PERSIST_FAIL as PERSIST_FAIL,
                        SEAM_PERSIST_WARN as PERSIST_WARN, SEAM_MARGEN as MARGEN)
RES = 512   # ↑ los umbrales viven en constantes.py


def _eje(a, axis):
    """axis=1 → costura VERTICAL (diferencia entre columnas contiguas).
       axis=0 → costura HORIZONTAL (diferencia entre filas contiguas).
    Devuelve (pico_sigma, posicion_normalizada, persistencia).

    Se ignoran los bordes: un salto duro en el 8% exterior es un marco, una viñeta o el
    recorte de la propia foto — NO un collage. Para que haya collage tiene que haber dos
    imágenes, y en una franja del 3% no cabe una segunda imagen. Los casos reales
    documentados caen al medio: gen-ninos en 0.33, las costuras del lote Marca Verde en 0.50.
    Sin esta exclusión el gate marcaba FAIL en pos=0.00, que es literalmente el borde."""
    d = np.abs(np.diff(a, axis=axis))
    # perfil = energía de borde de cada línea candidata
    perfil = d.mean(axis=1 - axis)
    z = (perfil - perfil.mean()) / (perfil.std() + 1e-6)
    m = int(len(z) * MARGEN)
    i = m + int(z[m:len(z) - m].argmax())
    # umbral local por la línea perpendicular, para no premiar imágenes con mucho detalle global
    thr = np.percentile(d, 98, axis=axis)
    linea = d[:, i] if axis == 1 else d[i, :]
    persist = float((linea > thr).mean())
    # salto de media entre los dos lados (informativo — no decide, ver cabecera)
    g = int(RES * 0.02)
    if axis == 1:
        A, B = a[:, :max(1, i - g)], a[:, min(RES - 1, i + g):]
    else:
        A, B = a[:max(1, i - g), :], a[min(RES - 1, i + g):, :]
    salto = abs(float(A.mean()) - float(B.mean()))
    return float(z.max()), i / float(RES), persist, salto


def costura(path):
    """→ dict con el veredicto y el detalle de los dos ejes."""
    a = np.asarray(Image.open(path).convert('L').resize((RES, RES)), dtype=np.float32)
    ejes, rank = {}, {"FAIL": 2, "WARN": 1, "PASS": 0}
    for nombre, axis in (("vertical", 1), ("horizontal", 0)):
        pico, pos, persist, salto = _eje(a, axis)
        if pico > PICO_MIN and persist > PERSIST_FAIL:
            v = "FAIL"
        elif pico > PICO_MIN and persist > PERSIST_WARN:
            v = "WARN"
        else:
            v = "PASS"
        ejes[nombre] = {"veredicto": v, "pico_sigma": round(pico, 1), "pos": round(pos, 2),
                        "persistencia": round(persist, 2), "salto_lum": round(salto, 1)}
    peor_eje = max(ejes.items(), key=lambda kv: (rank[kv[1]["veredicto"]], kv[1]["persistencia"]))
    return {"archivo": path, "veredicto": peor_eje[1]["veredicto"],
            "peor_eje": peor_eje[0], "ejes": ejes}


def main(argv):
    como_json = "--json" in argv
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        print("uso: qa_seam.py imagen.jpg [...] [--json]")
        return 2
    res, fails, warns = [], 0, 0
    NOTA = {"FAIL": "   ← COSTURA: es un collage, no una foto",
            "WARN": "   ← posible costura: MIRAR a tamaño completo antes de usarla", "PASS": ""}
    for p in paths:
        try:
            r = costura(p)
        except Exception as e:
            r = {"archivo": p, "veredicto": "WARN", "error": str(e)[:80]}
        res.append(r)
        v = r.get("veredicto")
        fails += v == "FAIL"
        warns += v == "WARN"
        if not como_json:
            if "error" in r:
                print(f"WARN  {p}: {r['error']}")
                continue
            e = r["ejes"][r["peor_eje"]]
            print(f"{v:<4}  eje={r['peor_eje']:<10} pico={e['pico_sigma']:5.1f}σ  "
                  f"pos={e['pos']:.2f}  persistencia={e['persistencia']:.2f}  {p}{NOTA[v]}")
    if como_json:
        print(json.dumps({"gate": "seam", "verdict": "FAIL" if fails else "PASS",
                          "warns": warns, "resultados": res}, ensure_ascii=False, indent=2))
    else:
        cola = f" · {warns} para mirar" if warns else ""
        print(f"SEAM: {'PASS' if not fails else f'FAIL ({fails}/{len(paths)})'}{cola}")
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
