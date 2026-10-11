# Carruseles para Meta, de punta a punta

Skill para Claude Code que produce carruseles y posts publicables para Instagram y Facebook:
elige el formato, escribe el copy, genera o elige las imágenes, compone el texto sobre la foto,
lo verifica y deja el paquete listo para Ads Manager.

La construí en 2026 en una agencia de marketing digital, donde produjo los lotes de carruseles de
varias marcas. Los nombres de clientes y personas de esta versión están reemplazados por genéricos
(«Marca Verde», «Marca Crema», «el director creativo»).

## La idea

> La IA razona, lo determinista hace cumplir.

Un modelo de lenguaje escribe bien, pero se olvida de las reglas a mitad de camino. Por eso lo que
se puede medir lo mide un script: el tamaño de la letra, el contraste, si el texto pisa la cara de
la persona, si la IA inventó letras en la foto, si dos carruseles del mismo lote repiten ángulo.
El modelo queda solo para lo que un script no ve.

## Cómo funciona

```
Fase −1  embudo creativo     en lotes: propone ~5× las piezas pedidas, con todas las slides escritas; el director elige
Fase 0   formato             quiz, tutorial, listicle, anuncio… según lo que le sirve a la marca
Fase 1   brief               verify.py init → spec del carrusel, con su ángulo declarado
Fase 2   copy                frameworks (PAS, AIDA…), hook puntuado contra el rendimiento real de la cuenta
Fase 3   blueprint           zona del texto por slide; se detiene a esperar aprobación humana
Fase 4   imágenes            generación con el hueco del texto pedido en el prompt, y tope de gasto
Fase 5   composición         engine.py: el mapa de la foto asigna la zona y el texto pasa detrás de la persona
Fase 6   compuertas          chequeos deterministas; cada uno deja un recibo firmado
Fase 8   entrega             paquete para Meta y copia inmutable de lo aprobado
Fase 9   publicación         carrusel → ad_id de Meta
Fase 10  rendimiento         ad_id → métricas → qué decisión de copy o de foto ganó
```
### Cuatro puertas que no se abren sin recibos

| Puerta | Qué cruza | Qué exige |
|---|---|---|
| generar imagen | copy → imagen | brief, copy, blueprint y prompt aprobados |
| render | foto cruda → composición | OCR sin texto inventado y zona libre |
| abrir la pieza | pieza → revisión humana | las compuertas en verde |
| publicar | pieza → al aire | todos los recibos anteriores, frescos |

Cada recibo va firmado con el hash de lo que midió. Si alguien lo escribe a mano o el archivo
cambia después, el hook `hooks/carrusel-gate.py` lo detecta y bloquea la llamada. Lo que se mide
también se cuenta: `hooks/costo-imagenes.py` anota cada imagen generada y corta al llegar al tope.

### Las compuertas (`templates/`)

| Script | Qué mide |
|---|---|
| `qa_brief.py` | brief completo, ángulo declarado, cliente existente |
| `qa_copy.py` | clichés de IA, triadas, hook, cifras sin fuente |
| `qa_blueprint.py` | zonas por posición, cero repetición entre slides |
| `qa_lote.py` | dos carruseles del mismo lote no repiten ángulo |
| `qa_raw.py` | texto inventado por la IA en la foto (OCR con Vision de macOS) |
| `qa_seam.py` | costuras de collage en los dos ejes |
| `qa_typesize.py` | piso de 26 px y titular de 90 px |
| `qa_geom.py` | solapes y límites con las métricas reales de la fuente |
| `qa_lint.py` | contraste WCAG y márgenes seguros |
| `qa_lines.py` | que los quiebres de línea sobrevivan al navegador |
| `qa_dom.mjs` | overflow y colisiones sobre el DOM renderizado (Playwright) |
| `dorado.py` | prueba de regresión: un caso congelado detecta si el motor cambió sin que nadie lo pidiera |

## Qué hay en el repo

| | |
|---|---|
| `SKILL.md` | el pipeline completo, fase por fase |
| `hooks/` | los dos hooks de Claude Code que hacen cumplir las puertas y el tope de gasto |
| `COPY.md` · `RUBRIC.md` · `COMPRENSION.md` | cómo se escribe el copy y con qué se juzga |
| `references/` | formatos, composición y tipografía, producción de imágenes, prompts que funcionaron y que fallaron |
| `templates/` | el motor (`engine.py`), las compuertas y las herramientas: unas 6.500 líneas de Python, Node y Swift |
| `APRENDIZAJES.md` | el historial fechado de por qué existe cada regla |

## Requisitos

- Claude Code: la skill va en `.claude/skills/carruseles-max-final/` y los hooks en `.claude/hooks/`,
  registrados en `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "mcp__[Hh]iggsfield__generate_(image|video)", "hooks": [{ "type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/carrusel-gate.py\"" }] },
      { "matcher": "mcp__meta-ads__ads_(create_ad|create_creative|creative_upload)", "hooks": [{ "type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/carrusel-gate.py\"" }] },
      { "matcher": "Bash", "hooks": [{ "type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/carrusel-gate.py\"" }] }
    ],
    "PostToolUse": [
      { "matcher": "mcp__[Hh]iggsfield__generate_(image|video)", "hooks": [{ "type": "command", "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/costo-imagenes.py\"" }] }
    ]
  }
}
```

- Python 3, Google Chrome (render) y macOS (OCR y recorte con Vision, en `ocr.swift` y `cutout.swift`)
- Opcional: `cd templates && npm i && npx playwright install chromium` para `qa_dom.mjs`
- Para generar imágenes: un proveedor de imágenes por MCP (se usó Higgsfield)

Las fuentes de `templates/assets/` (Inter, Montserrat y Oswald) se distribuyen bajo la SIL Open Font
License; las licencias están en `templates/assets/licencias/`.
