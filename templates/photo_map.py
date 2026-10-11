#!/usr/bin/env python3
"""
photo_map.py — EL MAPA DE LA FOTO (idea del director creativo, 8-jul-2026).

"Cuando pongo quitar fondo, me mantiene a la persona → con eso puedes MAPEAR dónde está,
 y así sabes qué puede taparse y qué no. Una esquina del codo sí; el eje central, no."

Dado: foto + su cutout (alpha de remove-background) + el crop del frame (1080×1080 por
defecto — regla de la casa, reconfirmada por el director creativo el 3-ago-2026; 4:5 queda como opción
por spec).
Produce un mapa de zonas y un verificador determinista de layout:

  PROHIBIDO  (rojo)     cabeza/cara + eje central del cuerpo (masa erosionada) → 0% de overlap
  TOLERANTE  (amarillo) extremidades (brazos/manos/pies = máscara - eje) → ≤12% del elemento, en esquina
  FOCO       (naranja)  la luz principal de la imagen (percentil de luminancia) → cards NO encima
  LIBRE      (verde)    espacio negativo real → aquí vive el texto

El diseño debe CONVERSAR con la imagen: la luz y la persona mandan; el HTML se acomoda.

Uso:
    from photo_map import cover_crop, PhotoMap
    crop = cover_crop(w, h, posx=.50, posy=.42, aspect=(4, 5))   # = object-fit:cover 4:5
    pm = PhotoMap('foto.jpg', 'cutout.png', crop, canvas=(1080, 1350))
    results = pm.check([{'name':'title','x':56,'y':270,'w':600,'h':180,'kind':'text'}, ...])
    pm.overlay('_map-debug.png', elements)                # mapa visual para revisar/mostrar
"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import numpy as np

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from constantes import (CANVAS_W, LIMB_TOL_CARD, LUZ_MAX_CARD, LUZ_MAX_TEXTO,
                        OVERLAP_PROHIBIDO, VELO_OBJETIVO, VELO_PISO, VELO_TECHO)
RES = 270  # resolución del mapa en X (la Y se deriva del aspecto del lienzo)

def cover_crop(w, h, posx=0.5, posy=0.5, aspect=None, zoom=1.0):
    """Ventana equivalente a object-fit:cover + object-position:posx% posy%.

    Sin `aspect` devuelve (cx, cy, s) cuadrada — el comportamiento de siempre
    (compatibilidad con asset_catalog y builders legacy).
    Con `aspect=(aw, ah)` —ej. (4, 5) para el lienzo 1080×1350— devuelve
    (cx, cy, cw, ch): la ventana MÁS GRANDE de esa proporción que cabe en la foto.

    `zoom` (>1) achica la ventana y por lo tanto AGRANDA al sujeto al escalar al
    lienzo: zoom 1.5 = el sujeto se ve 50% más grande. Existe porque un crudo de
    2048² sobre un lienzo de 1080² se usaba entero SIEMPRE, así que la única forma
    de agrandar a la mascota era regenerar la imagen (director creativo, 5-ago-2026: *"la
    portada tiene mucho texto y poca imagen, podríamos hacer a verde suave más
    grande"*). `posx`/`posy` deciden hacia qué lado se acerca: 1.0/1.0 = abajo a la
    derecha, que es donde suele vivir la mascota.
    ⚠️ Acercarse RECORTA: lo que queda fuera del encuadre no vuelve. Después de
    subir el zoom hay que MIRAR el PNG — el sujeto no puede quedar cortado."""
    z = max(1.0, float(zoom or 1.0))
    if aspect is None:
        s = max(1, int(min(w, h) / z))
        return (int((w - s) * posx), int((h - s) * posy), s)
    aw, ah = aspect
    cw = min(w, int(round(h * aw / ah)))
    ch = int(round(cw * ah / aw))
    if ch > h:
        ch = h
        cw = int(round(ch * aw / ah))
    cw, ch = max(1, int(cw / z)), max(1, int(ch / z))
    return (int((w - cw) * posx), int((h - ch) * posy), cw, ch)

class PhotoMap:
    def __init__(self, photo_path, alpha_path, crop, canvas=CANVAS_W):
        # crop: (cx, cy, s) cuadrado (legacy) o (cx, cy, cw, ch) · canvas: int o (w, h)
        if len(crop) == 3:
            cx0, cy0, cw, ch = crop[0], crop[1], crop[2], crop[2]
        else:
            cx0, cy0, cw, ch = crop
        if isinstance(canvas, (tuple, list)):
            self.canvas_w, self.canvas_h = int(canvas[0]), int(canvas[1])
        else:
            self.canvas_w = self.canvas_h = int(canvas)
        self.canvas = self.canvas_w          # lo que lee el ancho (asset_catalog, overlay)
        self.res_w = RES
        self.res_h = max(1, int(round(RES * self.canvas_h / self.canvas_w)))
        photo = Image.open(photo_path).convert('RGB')
        w, h = photo.size
        alpha = Image.open(alpha_path).split()[-1].resize((w, h))
        box = (cx0, cy0, cx0 + cw, cy0 + ch)
        self.photo = photo.crop(box).resize((self.res_w, self.res_h))
        a = np.asarray(alpha.crop(box).resize((self.res_w, self.res_h)), dtype=np.uint8)
        self.person = a > 40

        # --- zonas de la persona ---
        ys, xs = np.where(self.person)
        if len(ys) == 0:
            self.head = self.core = self.limbs = np.zeros_like(self.person)
        else:
            top, bot = ys.min(), ys.max()
            left, right = xs.min(), xs.max()
            ph, pw = bot - top + 1, right - left + 1
            # cabeza: franja superior de la persona (18% de su alto), dilatada
            head = np.zeros_like(self.person)
            hrows = slice(max(0, top - self.res_h // 50), top + max(3, int(.18 * ph)))
            head[hrows, :] = self.person[hrows, :]
            head_img = Image.fromarray((head * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9))
            self.head = np.asarray(head_img) > 0
            # eje central: erosión de la máscara (queda la masa del torso/caderas/muslos)
            r = max(3, int(.11 * pw)) | 1  # impar
            core_img = Image.fromarray((self.person * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(r))
            self.core = np.asarray(core_img) > 0
            # extremidades: persona - (eje ∪ cabeza)
            self.limbs = self.person & ~(self.core | self.head)
        self.forbidden = self.head | self.core

        # --- foco de luz (luminancia alta, suavizada, fuera es LIBRE) ---
        # La regla es "el texto no va sobre el foco", y existe porque la tinta por defecto es
        # BLANCA: blanco sobre un reflejo brillante no se lee. Con tinta OSCURA sobre un lienzo
        # claro (preset `verde-claro`, 10-ago-2026) la condición se invierte: el peligro deja
        # de ser la luz y pasa a ser la mancha oscura. Por eso el foco se calcula por INK y no
        # como constante — ver `foco_para()`. `self.light` conserva el significado de siempre
        # para que nada de lo ya producido cambie.
        self._lum = np.asarray(self.photo.convert('L').filter(ImageFilter.GaussianBlur(10)),
                               dtype=float)
        self.light = self._lum >= np.percentile(self._lum, 88)
        # ⚠️ El percentil es RELATIVO y sobre una imagen casi uniforme no señala nada: en un
        # flat-lay crema el "12% más oscuro" es fondo liso imperceptiblemente más gris, y el
        # gate reportaba «sobre la MANCHA oscura 100%» de un cuadro vacío. Por eso la mancha
        # lleva además un piso ABSOLUTO: una zona que no es de verdad oscura no puede esconder
        # tinta negra. Si la imagen no tiene ninguna zona bajo ese piso, la máscara queda vacía
        # y la única restricción que manda es el sujeto. (10-ago-2026, lote Marca Verde crema.)
        self.dark = (self._lum <= np.percentile(self._lum, 12)) & (self._lum < 128)

    def foco_para(self, ink):
        """El mapa de riesgo que corresponde a la tinta: 'light' (blanca) → el foco de luz;
        'dark' (negra) → la mancha oscura. Cualquier otro valor cae en el de siempre."""
        return self.dark if ink == 'dark' else self.light

    # ---------- verificación ----------
    def _frac(self, mask, x, y, w, h):
        fx = self.res_w / self.canvas_w
        fy = self.res_h / self.canvas_h
        x0, y0 = max(0, int(x * fx)), max(0, int(y * fy))
        x1, y1 = min(self.res_w, int((x + w) * fx)), min(self.res_h, int((y + h) * fy))
        if x1 <= x0 or y1 <= y0: return 0.0
        sub = mask[y0:y1, x0:x1]
        return float(sub.mean())

    def check(self, elements, limb_tol=LIMB_TOL_CARD, light_card=LUZ_MAX_CARD,
              light_text=LUZ_MAX_TEXTO, ink='light'):
        """elements: [{'name','x','y','w','h','kind': 'text'|'card'}]. FAIL si tapa lo prohibido.

        `ink` es el color de la tipografía que va a ir encima: 'light' (blanca, el default de
        siempre) o 'dark' (negra, presets de fondo claro). Decide contra qué foco se mide.
        """
        foco = self.foco_para(ink)
        etiqueta = 'la MANCHA oscura' if ink == 'dark' else 'el FOCO de luz'
        out = []
        for e in elements:
            fb = self._frac(self.forbidden, e['x'], e['y'], e['w'], e['h'])
            lm = self._frac(self.limbs, e['x'], e['y'], e['w'], e['h'])
            lt = self._frac(foco, e['x'], e['y'], e['w'], e['h'])
            kind = e.get('kind', 'text')
            verdict = 'PASS'; why = []
            if fb > OVERLAP_PROHIBIDO: verdict = 'FAIL'; why.append(f'tapa cabeza/eje central {fb:.0%}')
            if lm > limb_tol: verdict = 'FAIL'; why.append(f'tapa extremidad {lm:.0%} (>tolerancia {limb_tol:.0%})')
            elif lm > 0.005 and verdict != 'FAIL': why.append(f'roza extremidad {lm:.0%} (ok, esquina)')
            lmax = light_card if kind == 'card' else light_text
            if lt > lmax:
                verdict = 'FAIL'; why.append(f'sobre {etiqueta} {lt:.0%} (max {lmax:.0%} para {kind})')
            elif lt > 0.15 and verdict == 'PASS':
                why.append(f'toca {etiqueta} {lt:.0%} (vigilar contraste)')
            out.append({'name': e['name'], 'verdict': verdict, 'forbidden': round(fb, 3),
                        'limbs': round(lm, 3), 'light': round(lt, 3), 'why': '; '.join(why) or 'zona libre'})
        return out

    # ---------- visualización ----------
    def overlay(self, out_path, elements=None, results=None):
        base = self.photo.resize((self.canvas_w, self.canvas_h)).convert('RGBA')
        ov = np.zeros((self.res_h, self.res_w, 4), dtype=np.uint8)
        ov[self.light] = (255, 150, 30, 90)
        ov[self.limbs] = (255, 220, 40, 110)
        ov[self.forbidden] = (230, 30, 40, 130)
        layer = Image.fromarray(ov).resize((self.canvas_w, self.canvas_h))
        base.alpha_composite(layer)
        d = ImageDraw.Draw(base)
        try: fnt = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 30)
        except OSError: fnt = ImageFont.load_default()
        for i, e in enumerate(elements or []):
            r = (results or [{}] * len(elements))[i]
            col = (80, 220, 120) if r.get('verdict', '?') == 'PASS' else (255, 60, 60)
            d.rectangle([e['x'], e['y'], e['x'] + e['w'], e['y'] + e['h']], outline=col, width=5)
            d.text((e['x'] + 8, e['y'] + 6), f"{e['name']} {r.get('verdict','')}", fill=col, font=fnt)
        base.convert('RGB').save(out_path)
        return out_path


# ---------------------------------------------------------------------------
# VELO POR LÍNEA (composicion-y-tipografia.md §6.3 · test jul-2026)
# El percentil 80 del BLOQUE miente: en c1-01 el bloque pasaba y la palabra que caía
# sobre una pantalla encendida quedó en 1.4:1. El alfa lo fija la línea PEOR.
# ---------------------------------------------------------------------------
def alpha_por_linea(img_path, cajas, objetivo=VELO_OBJETIVO, piso=VELO_PISO, techo=VELO_TECHO):
    """cajas = [(x0,y0,x1,y1), ...] en píxeles, UNA por renglón renderizado.
    Devuelve (alfa_final, [alfa_por_caja]) — el alfa final es el máximo."""
    from PIL import Image
    import numpy as np
    im = Image.open(img_path).convert("RGB")
    a = np.asarray(im, dtype=np.float32) / 255.0
    lum = 0.2126*a[:,:,0] + 0.7152*a[:,:,1] + 0.0722*a[:,:,2]
    H, W = lum.shape
    out = []
    for (x0, y0, x1, y1) in cajas:
        x0 = max(0, min(W-1, int(x0))); x1 = max(x0+1, min(W, int(x1)))
        y0 = max(0, min(H-1, int(y0))); y1 = max(y0+1, min(H, int(y1)))
        L = max(float(np.percentile(lum[y0:y1, x0:x1], 80)), 0.05)
        out.append(round(min(max(1 - objetivo / L, piso), techo), 3))
    return (max(out) if out else piso), out
