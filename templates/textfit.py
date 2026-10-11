#!/usr/bin/env python3
"""
textfit.py — Quiebres de título BALANCEADOS y con sentido (director creativo, 8-jul-2026).
Reglas duras aprendidas de fallas reales:
  · jamás una línea huérfana corta ("quieras" / "¿y") — toda línea ≥ 30% del ancho de la mayor
  · jamás terminar una línea en conector ("y", "o", "de", "tu", "¿y"…) — el sintagma viaja junto
  · la ALTURA devuelta siempre es real (nº de líneas devuelto = nº de líneas renderizadas):
    si no hay corte estético, se devuelve el corte menos-malo QUE QUEPA (estética < altura correcta)
Uso:  lines = balance_lines(texto, size, ancho_px, measure)  ·  measure(str)->px
"""

STOP_END = {'y','o','a','e','u','de','del','la','el','los','las','tu','tus','un','una','en',
            'con','que','al','se','mi','sin','por','para','como','más','ya','no','si'}

def _clean(w): return w.strip('¿?¡!.,;:«»"\'').lower()

def _ok(lines, w, measure):
    ws = [measure(l) for l in lines]
    if any(x > w for x in ws): return False
    if min(ws) < 0.30 * max(ws): return False
    for l in lines[:-1]:
        if _clean(l.split()[-1]) in STOP_END: return False
    for l in lines:
        toks = l.split()
        if len(toks) == 1 and len(_clean(toks[0])) <= 2: return False
    return True

def balance_lines(text, size, w, measure):
    words = text.split()
    if measure(text) <= w or len(words) == 1:
        return [text]
    best = None
    for k in range(1, len(words)):
        cand = [' '.join(words[:k]), ' '.join(words[k:])]
        if _ok(cand, w, measure):
            score = abs(measure(cand[0]) - measure(cand[1]))
            if best is None or score < best[0]: best = (score, cand)
    if best: return best[1]
    n = len(words)
    for a in range(1, n-1):
        for b in range(a+1, n):
            cand = [' '.join(words[:a]), ' '.join(words[a:b]), ' '.join(words[b:])]
            if _ok(cand, w, measure): return cand
    # degradado (altura correcta manda): 2 líneas que quepan, aunque feas
    for k in range(n-1, 0, -1):
        cand = [' '.join(words[:k]), ' '.join(words[k:])]
        if measure(cand[0]) <= w and measure(cand[1]) <= w: return cand
    return words
