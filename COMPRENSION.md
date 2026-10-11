# ~~Compuerta de COMPRENSIÓN de copy~~ — DEROGADA

> **El director creativo, 10-ago-2026: este paso ya no se corre en carruseles.**
> Si llegaste acá buscando cómo testear que el copy se entienda: **no lo hagas.** No existe la
> compuerta, no se invoca `copy-qa`, no se escribe `_copy-receipt.json` y ninguna puerta de
> `carrusel-gate` lo pide.

## Qué hacer en su lugar

| Necesitas… | Dónde |
|---|---|
| Que el copy se entienda | **Lo aprueba el director creativo en la Fase −1**, leyendo las propuestas con el texto de todas sus slides (`references/fase-menos-1.md`) |
| Chequeo del copy | `verify.py copy` → `_copy-gate-receipt.json` (script). **`copy-craft-qa` también se eliminó** el 10-ago-2026 (§36) |
| Las trampas de redacción que este panel cazó | `COPY.md` § *Lo que el panel cazó mientras existió* |
| Por qué se derogó, qué costó y el método completo por si se revive | `APRENDIZAJES.md` §35 |

## Por qué está derogada

El director creativo: *«soy experto en marketing, si yo apruebo un copy es porque la gente lo entenderá»*, y
desde que la Fase −1 entrega cada propuesta con todas sus slides escritas, él lee el copy
completo antes de que se produzca nada.

Se le presentó el contraargumento (quien conoce el producto no puede medir su propia claridad; en
el lote de agosto el panel cazó un error factual de facturación y una lectura de privacidad) y
reafirmó la decisión. **Manda él** — jerarquía #1 de la skill.

## Si algún día se revive

Revivirlo **separando dos veredictos que este panel mezclaba**: *«no se entiende»* (bloquea) vs
*«falta un dato de producto»* (no bloquea; es una pregunta para el director creativo y la pieza se degrada
marcada INCOMPLETA). Ese defecto es lo que hizo que frenara 6 de 10 carruseles por datos que él
tenía, y es la razón de fondo por la que terminó eliminado. Detalle en `APRENDIZAJES.md` §35.

**En sitios web la compuerta SIGUE VIGENTE** y no se tocó: `sitio-web-cliente` la corre sobre
`copy.md` y `web-gate` la exige. Un sitio que no se entiende queda publicado e indexado.
