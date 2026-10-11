#!/usr/bin/env /usr/local/bin/python3
"""qa_pastilla.py — ¿choca la ILUSTRACIÓN con la pastilla CTA? (5-ago-2026)

`qa_dom` mide cajas del DOM y por eso no puede ver esto: la pastilla es una caja,
pero la ilustración es una imagen de fondo cuyo contenido real vive en su alfa. El
motor pinta el recorte del sujeto en z-index 4, ENCIMA del texto (z-index 3), así que
una hoja que sobresalga se monta sobre la pastilla sin que ningún gate lo note.
Lo cazaron los dos jueces de diseño a ojo; esto lo vuelve determinista.

Mide la intersección real de dos rectángulos:
  · la pastilla, detectada por FORMA (fila con una corrida sólida de color >280px),
    no por color suelto — la mascota es verde y el color solo lo confunde con él.
  · el contenido del crudo, reescalado al lienzo, con tolerancia alta (solo el
    personaje y sus props, no el halo).

  qa_pastilla.py <carpeta-del-carrusel> [--min 24]
"""
import sys, os, glob
import numpy as np
from PIL import Image

MIN_AIRE = 24          # px de aire limpio exigidos (el valor que ya cumplía c8 s-01)
LARGO_BARRA = 280      # px: corrida contigua mínima para llamarle "pastilla" y no "texto"
TOL_CONTENIDO = 100    # distancia al fondo: alta a propósito, para ignorar el glow


def corrida_max(fila):
    best = cur = bi = si = 0
    for i, v in enumerate(fila):
        if v:
            if cur == 0:
                si = i
            cur += 1
            if cur > best:
                best, bi = cur, si
        else:
            cur = 0
    return best, bi


def caja_pastilla(png):
    a = np.array(Image.open(png).convert("RGB")).astype(int)
    m = (a[:, :, 0] > 120) & (a[:, :, 0] < 225) & (a[:, :, 1] > 200) & (a[:, :, 2] < 130)
    filas = []
    for y in range(a.shape[0]):
        L, x0 = corrida_max(m[y])
        if L > LARGO_BARRA:
            filas.append((y, x0, x0 + L))
    if not filas:
        return None
    return (min(f[1] for f in filas), filas[0][0],
            max(f[2] for f in filas), filas[-1][0])


def caja_ilustracion(raw, lado, franja=None):
    im = Image.open(raw).convert("RGB").resize((lado, lado), Image.NEAREST)
    r = np.array(im).astype(float)
    k = 40
    e = np.concatenate([r[:k, :k].reshape(-1, 3), r[:k, -k:].reshape(-1, 3),
                        r[-k:, :k].reshape(-1, 3), r[-k:, -k:].reshape(-1, 3)])
    bg = np.median(e, axis=0)
    m = np.sqrt(((r - bg) ** 2).sum(axis=2)) > TOL_CONTENIDO
    if franja:
        x0, x1 = franja
        m[:, :x0] = False
        m[:, x1:] = False
    ys, xs = np.where(m)
    if not len(ys):
        return None
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))


def correr(carpeta, minimo=MIN_AIRE):
    out = []
    for png in sorted(glob.glob(os.path.join(carpeta, "s-*.png"))):
        if "_thumb" in png or "_map" in png:
            continue
        n = os.path.basename(png)[:-4]
        raw = os.path.join(carpeta, "raw", n + ".png")
        if not os.path.exists(raw):
            continue
        p = caja_pastilla(png)
        if p is None:
            # La mayoría de las slides no lleva pastilla CTA (va en la portada y en el cierre).
            # Eso NO es un aviso: si se reportara WARN, cada carrusel saldría con 3 warns
            # rutinarios y el recibo dejaría de distinguir lo que sí hay que mirar.
            out.append((n, "n/a", "sin pastilla en esta slide — nada que medir"))
            continue
        lado = Image.open(png).size[0]
        # solo interesa la ilustración que cae bajo la franja horizontal de la pastilla
        il = caja_ilustracion(raw, lado, franja=(p[0], p[2]))
        if il is None:
            out.append((n, True, f"pastilla x={p[0]}..{p[2]} — sin ilustración en su franja"))
            continue
        # El sujeto puede estar ABAJO de la pastilla (portadas) o ARRIBA (slides de cierre).
        # El aire es la separación vertical real entre las dos cajas: si se solapan, los dos
        # términos salen negativos y el máximo sigue siendo negativo. Restar siempre
        # "arriba de la ilustración − pie de la pastilla" daba -900px en cada cierre.
        aire = max(p[1] - il[3], il[1] - p[3])
        donde = "bajo" if il[1] > p[3] else "sobre"
        ok = aire >= minimo
        out.append((n, ok, f"pastilla y={p[1]}..{p[3]} x={p[0]}..{p[2]} · "
                           f"ilustración {donde} ella y={il[1]}..{il[3]} · "
                           f"aire={aire:+d}px (mínimo {minimo})"))
    return out


def main(argv):
    minimo = MIN_AIRE
    if "--min" in argv:
        i = argv.index("--min")
        minimo = int(argv[i + 1])
        argv = argv[:i] + argv[i + 2:]
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        print(__doc__)
        return 2
    malas = 0
    for carpeta in paths:
        print(f"\n{os.path.basename(carpeta.rstrip('/'))}")
        for n, ok, det in correr(carpeta, minimo):
            marca = {True: "ok  ", False: "FAIL", None: "WARN", "n/a": "n/a "}[ok]
            if ok is False:
                malas += 1
            print(f"  {marca}  {n}  {det}")
    print(f"\nPASTILLA: {'FAIL' if malas else 'PASS'} ({malas} colisiones)")
    return 1 if malas else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
