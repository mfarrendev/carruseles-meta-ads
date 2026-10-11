#!/usr/bin/env python3
"""
asset_catalog.py — CATÁLOGO COMPLETO del pool de fotos de un cliente (director creativo, 8-jul-2026).
Motivo (falla real): con 82 fotos disponibles, el motor usó 1 en el 31% de los slides.
El catálogo mapea el pool ENTERO una sola vez para que el motor pueda ROTAR de verdad:
  por foto → máscara (cutout local Vision) + bbox del sujeto + score de limpieza por región
  (persona 3× + luz, como photo_map) + tags semánticos (de un tags.json por patrón).
Uso:
  python3 asset_catalog.py <dir_fotos> <dir_out_assets> [tags.json]
Escribe <dir_out_assets>/catalog.json y copia máscaras a <dir_out_assets>/.
"""
import os, sys, json, subprocess, fnmatch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from photo_map import PhotoMap, cover_crop
from PIL import Image
import numpy as np

RES = 270
REGION_AREA = {'top':(56,116,1024,540), 'bottom':(56,540,1024,1004),
               'left':(40,116,600,940), 'right':(480,116,1040,940)}
CUTOUT = os.path.expanduser('~/bin/cutout')

def region_scores(pm):
    f = RES/1080.0; out = {}
    for r,(x0,y0,x1,y1) in REGION_AREA.items():
        a,b,c,d = int(x0*f),int(y0*f),int(x1*f),int(y1*f)
        out[r] = round(float(pm.forbidden[b:d,a:c].mean())*3 + float(pm.light[b:d,a:c].mean()), 4)
    return out

def main(src, out, tagsfile=None):
    os.makedirs(out, exist_ok=True)
    tags_map = json.load(open(tagsfile)) if tagsfile else {}
    entries = []
    fotos = sorted(f for f in os.listdir(src) if f.lower().endswith(('.jpg','.jpeg','.png')) and not f.startswith('_'))
    for i, f in enumerate(fotos):
        ph = os.path.join(src, f)
        stem = os.path.splitext(f)[0].replace(' ','_')
        mask = os.path.join(out, f'cat-mask-{stem}.png')
        if not os.path.exists(mask):
            r = subprocess.run([CUTOUT, ph, mask, '--mask'], capture_output=True)
            if r.returncode != 0:
                print(f'  skip (sin sujeto): {f}'); continue
        try:
            w, h = Image.open(ph).size
            pm = PhotoMap(ph, mask, cover_crop(w, h, .5, .38 if h > w else .5))
            ys, xs = np.where(pm.person)
            subj = [round(float(xs.min())/RES,3), round(float(ys.min())/RES,3),
                    round(float(xs.max())/RES,3), round(float(ys.max())/RES,3)] if len(ys) else None
            tags = []
            for pat, tg in tags_map.items():
                if fnmatch.fnmatch(f, pat): tags += tg
            entries.append(dict(file=f, path=ph, mask=mask, w=w, h=h,
                                regions=region_scores(pm), subject=subj, tags=sorted(set(tags))))
        except Exception as e:
            print(f'  error {f}: {e}')
        if (i+1) % 10 == 0: print(f'  {i+1}/{len(fotos)}…')
    json.dump(entries, open(os.path.join(out,'catalog.json'),'w'), ensure_ascii=False, indent=1)
    print(f'catalog.json: {len(entries)} fotos mapeadas')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
