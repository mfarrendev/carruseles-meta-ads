# `templates/` — qué es cada archivo

Están todos en la misma carpeta a propósito: `verify.py` los invoca por nombre y `engine.py`
los importa como módulos hermanos. Moverlos a subcarpetas rompería esas dos cosas y las rutas
documentadas en `SKILL.md`, a cambio de nada más que orden visual. Este índice da el orden sin
el riesgo.

## 🔢 La fuente de los números

| | |
|---|---|
| **`constantes.py`** | **Todos los umbrales del sistema.** Si un número aparece en la doctrina Y en el código, vive acá. La doctrina lo cita por nombre; el código lo importa. |

## ⚙️ El motor

| | |
|---|---|
| `engine.py` | **El motor canónico.** Valida el hueco, el mapa ASIGNA la zona, y el texto pasa por detrás de la persona con la máscara. |
| `styles.css` · `slide.html` | Arquetipos de layout (`l-*`), escalas (`t-*`) y la plantilla base. |
| `assets/` | Las fuentes locales (`.woff2`). Sin CDN: si no están en disco, no se pueden MEDIR. |

## 🚪 Las compuertas

| | |
|---|---|
| **`verify.py`** | **El runner único.** Un comando por fase, los flags correctos por dentro, y un recibo firmado con el hash de lo que midió. Nunca invocar los gates sueltos. Flags: `--only s-03` (re-corre una sola slide y marca `scope` en el recibo) · `--warn-ok "razón"` (graba por qué se aceptan los WARNs; sin él queda `warns_sin_razon: true` y la Fase 7 los revisa). Los recibos distinguen `fails`/`warns`: 0 fails + N warns → `status: PASS_CON_WARNS`. |
| `qa_brief.py` | Puerta 1 — ¿el brief está completo (incluido el **`angulo`**) y el cliente existe? |
| `qa_copy.py` | Lo mecánico del copy: clichés, triadas, hook, primary text, voseo, cifras. |
| `qa_blueprint.py` | Zonas por posición, `visual_need`, A8 cero repetición, nº de slides. |
| **`qa_lote.py`** | **Compuerta de LOTE (C12)** — corre sobre la carpeta madre (`verify.py lote`): FAIL si dos specs hermanos repiten `angulo` declarado · WARN si ≥3 portadas comparten las mismas 3 primeras palabras. NO detecta por solapamiento léxico general (las paráfrasis reales pasarían). |
| `qa_raw.py` | Texto inventado por la IA (OCR) + zona reservada en fotos generadas. |
| `qa_seam.py` | Costura de collage, en los DOS ejes. |
| `qa_typesize.py` | Piso de 26px y héroe de 90px — **por carrusel**, no por slide. |
| `qa_geom.py` | Rects reales con métricas de fuente: solapes, pastillas, bounds. |
| `qa_lint.py` | Contraste WCAG real y márgenes seguros. |
| `qa_lines.py` | Que los quiebres del spec sobrevivan al navegador. |
| **`qa_dom.mjs`** | **Validación sobre el DOM renderizado (Node + Playwright).** Overflow real con px y fix, colisión con el chrome fijo (logo/CTA), piso de fuente computado 26px → FAIL · gap título-contenido y densidad por bandas → WARN. Idea de guizang-social-card-skill, **reimplementada** (su validador es AGPL). Si falta node/Playwright, `verify.py` lo reporta WARN "qa_dom no corrió" — nunca pass silencioso. Se instala una vez: `cd templates && npm i playwright && npx playwright install chromium`. |

## 🧰 Los helpers (los usa el motor, no se corren solos)

| | |
|---|---|
| `photo_map.py` | El mapa de la foto: prohibido / tolerante / foco / libre. Y el velo por línea. |
| `framer.py` | Reencuadre determinista — mover la imagen, no el texto. |
| `textfit.py` | Quiebres balanceados, sin huérfanas ni conectores colgando. |
| `montwidth.py` | Ancho REAL con la fuente real al peso real. |
| `asset_catalog.py` | Cataloga el pool entero de fotos de un cliente para rotar de verdad. |

## 📋 Planificación y vistas

| | |
|---|---|
| `plan_lote.py` | Qué formato hacer, leído del `formatos.md` de la marca. |
| `deck_ideas.py` | El deck HTML de selección de la Fase −1 (una tarjeta por idea, agrupadas por celda). |
| `registrar_publicacion.py` | Escribe/actualiza el `_publicado.json` (carrusel → ad_id de Meta). NUNCA toca `carrusel.json`. |
| `preview.html` · `qa-contact.html` | Hoja de contacto y squint. |
| `_thumb-NN.png` | Miniaturas 360px por slide (`verify.py thumbs`, con `sips`, ya incluido en `gates`): el test de legibilidad móvil que leen los jueces en la Fase 7. |

## 🛠️ Binarios de Vision (macOS, se compilan una vez)

```bash
swiftc -O -o ~/bin/ocr    templates/ocr.swift      # OCR local, sin dependencias
swiftc -O -o ~/bin/cutout templates/cutout.swift   # máscara y recorte del sujeto
```
