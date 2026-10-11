#!/usr/bin/env python3
"""
framer.py — Encuadre determinista: "MOVER LA IMAGEN, NO EL TEXTO" (director creativo, 8-jul-2026).

Dado el bbox del sujeto (fracciones, INCLUYENDO extremidades/objetos), calcula si un layout
es FACTIBLE y devuelve el crop exacto (zoom+pan) que deja al sujeto FLUSH a su borde y la
zona de texto limpia. Si ningún layout lateral es factible → el veredicto es CAMBIAR DE FOTO
o usar layout centro/banda, NUNCA forzar el texto sobre el sujeto ni dejar espacio muerto.

Uso típico en un builder:
    from framer import plan, css_for, zone_texture
    p = plan(w, h, subj=(x0,y0,x1,y1), side='left')     # None => no factible
    style = css_for(p, w, h)                             # estilo del <img> (px absolutos)
"""
from PIL import Image
import numpy as np

CANVAS = 1080

def plan(w, h, subj, side='left', text_min=0.40, flush=0.08, head_margin=0.07, steps=40):
    """Busca el crop cuadrado (s, cx0, cy0) en px fuente tal que:
    - el sujeto queda pegado a su borde (aire detrás <= flush)
    - la zona de texto (lado opuesto) mide >= text_min del ancho
    Prefiere el sujeto MÁS GRANDE posible (s mínimo). None si no es factible."""
    x0, y0, x1, y1 = subj
    ws = (x1 - x0) * w
    smax = min(w, h)
    smin = ws / max(1e-6, (1 - text_min - flush))
    if smin > smax:
        return None
    for s in np.linspace(smin, smax, steps):
        span = ws / s
        a = (1 - flush - span) if side == 'right' else flush   # borde izq del sujeto en el frame
        cx0 = x0 * w - a * s
        if cx0 < -1 or cx0 + s > w + 1:
            continue
        cx0 = min(max(cx0, 0), w - s)
        cy0 = min(max(y0 * h - head_margin * s, 0), max(h - s, 0))
        tz = (a + span + 0.04, 0.97) if side == 'left' else (0.03, a - 0.04)
        return dict(s=float(s), cx0=float(cx0), cy0=float(cy0),
                    subj_frame=(a, a + span), text_zone=tz, side=side)
    return None

def plan_center(w, h, subj, head_margin=0.06):
    """Layout centro (sujeto centrado, texto en bandas sup/inf o costados si el sujeto es chico)."""
    s = min(w, h)
    x0, y0, x1, y1 = subj
    cx = ((x0 + x1) / 2) * w
    cx0 = min(max(cx - s / 2, 0), w - s)
    cy0 = min(max(y0 * h - head_margin * s, 0), max(h - s, 0))
    return dict(s=float(s), cx0=float(cx0), cy0=float(cy0),
                subj_frame=((x0 * w - cx0) / s, (x1 * w - cx0) / s), text_zone=None, side='center')

def css_for(p, w, h, canvas=CANVAS):
    """CSS del <img> posicionado en px absolutos (determinista, no object-position)."""
    scale = canvas / p['s']
    return (f"position:absolute;left:{-p['cx0']*scale:.0f}px;top:{-p['cy0']*scale:.0f}px;"
            f"width:{w*scale:.0f}px;max-width:none")

def zone_texture(img_path, p, zone_x, zone_y=(0.12, 0.88)):
    """Textura media (std local 0-255) de la zona de texto DENTRO del crop. <20 ≈ limpia."""
    im = Image.open(img_path).convert('L')
    s, cx0, cy0 = p['s'], p['cx0'], p['cy0']
    box = (int(cx0 + zone_x[0] * s), int(cy0 + zone_y[0] * s),
           int(cx0 + zone_x[1] * s), int(cy0 + zone_y[1] * s))
    z = np.asarray(im.crop(box).resize((160, 160)), dtype=float)
    blocks = z.reshape(20, 8, 20, 8)
    return float(blocks.std(axis=(1, 3)).mean())

def report(w, h, subj, img_path=None):
    """Informe de factibilidad: qué layouts admite esta foto. Úsalo ANTES de elegir foto."""
    out = {}
    for side in ('left', 'right'):
        p = plan(w, h, subj, side=side)
        if p and img_path:
            p['texture'] = round(zone_texture(img_path, p, p['text_zone']), 1)
        out[side] = p
    out['center'] = plan_center(w, h, subj)
    x0, _, x1, _ = subj
    out['verdict'] = ('lateral OK' if (out['left'] or out['right'])
                      else ('centro/banda (sujeto ancho ' + f"{x1-x0:.0%} del frame) — o CAMBIAR FOTO"))
    return out
