#!/usr/bin/env python3
"""registrar_publicacion.py — escribe/actualiza el `_publicado.json` de una carpeta de carrusel.

Vínculo carrusel → ad de Meta. Formato y reglas: `references/publicacion-y-registro.md`.
NUNCA toca `carrusel.json` (su mtime firma la frescura de las puertas 3 y 4).

Uso:
    /usr/local/bin/python3 registrar_publicacion.py <carpeta> --ad-id X --adset-id Y \
        [--fecha AAAA-MM-DD] [--notas "..."]

Solo stdlib. Compatible Python 3.9+.
"""

import argparse
import json
import os
import re
import sys
from datetime import date

ARCHIVO = "_publicado.json"
RE_ID = re.compile(r"^\d{5,25}$")
RE_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def main():
    p = argparse.ArgumentParser(description="Registra la publicación de un carrusel en Meta.")
    p.add_argument("carpeta", help="carpeta del carrusel (donde vive carrusel.json)")
    p.add_argument("--ad-id", required=True, help="ID del ad en Meta (dígitos)")
    p.add_argument("--adset-id", required=True, help="ID del ad set en Meta (dígitos)")
    p.add_argument("--fecha", help="AAAA-MM-DD (por defecto: hoy)")
    p.add_argument("--notas", default="", help="nota libre (variante de hook, calce retroactivo…)")
    args = p.parse_args()

    if not os.path.isdir(args.carpeta):
        sys.exit("ERROR: no existe la carpeta %s" % args.carpeta)
    for nombre, valor in (("ad-id", args.ad_id), ("adset-id", args.adset_id)):
        if not RE_ID.match(valor):
            sys.exit("ERROR: --%s debe ser un ID de Meta (5-25 dígitos), recibido: %r"
                     % (nombre, valor))
    fecha = args.fecha or date.today().isoformat()
    if not RE_FECHA.match(fecha):
        sys.exit("ERROR: --fecha debe ser AAAA-MM-DD, recibido: %r" % fecha)

    if not os.path.isfile(os.path.join(args.carpeta, "carrusel.json")):
        print("AVISO: la carpeta no tiene carrusel.json (¿es un carrusel? ¿predata el spec?). "
              "Se registra igual.", file=sys.stderr)

    ruta = os.path.join(args.carpeta, ARCHIVO)
    datos = {}
    if os.path.isfile(ruta):
        try:
            with open(ruta, encoding="utf-8") as f:
                datos = json.load(f)
        except json.JSONDecodeError:
            sys.exit("ERROR: %s existe pero no es JSON válido — revisarlo a mano." % ruta)

    datos.update({
        "ad_id": args.ad_id,
        "adset_id": args.adset_id,
        "fecha": fecha,
        "notas": args.notas or datos.get("notas", ""),
    })

    tmp = ruta + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(tmp, ruta)

    # Re-leer para confirmar que quedó bien escrito.
    with open(ruta, encoding="utf-8") as f:
        leido = json.load(f)
    assert leido == datos, "el archivo re-leído no coincide con lo escrito"
    print("OK · %s → %s" % (json.dumps(leido, ensure_ascii=False), ruta))


if __name__ == "__main__":
    main()
