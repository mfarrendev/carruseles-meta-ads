# Fase −1 — Ideación divergente (antes de la Fase 0)

> **Por qué existe.** El copy de la agencia salía "competente pero plano" porque el ratio de
> selección era **1:1**: un ángulo, dos paráfrasis, y a producir. Los lotes buenos salieron de
> embudos 100→20 hechos a mano — Marca Verde: `IDEAS.md` 80→16 (`verde-ads/ideas-carruseles-2026-07/`);
> Marca Servicios: 100→8. Los malos salieron de "una semilla, hazme 10": el lote con **6 hooks
> abriendo con "Deja de"** salió así — el generador encontró UNA forma que le gustó y la repitió,
> y como la selección fue por ranking global sobre su propia lista, el sesgo pasó entero.
>
> La Fase −1 es ese embudo, hecho procedimiento: **generación divergente por grilla + corte por
> celda**, con generador y selector en agentes/turnos distintos.

## Regla dura de la fase

**Durante la Fase −1 NO se corre `verify.py init`, no se crea carpeta de carrusel, no se genera
imagen.** La salida es solo texto: un archivo de ideas + el deck HTML de selección
(`templates/deck_ideas.py`). El `verify.py init` (Fase 1) corre recién sobre las ideas que
El director creativo eligió. Una idea sin carpeta no le debe nada a nadie: descartarla cuesta cero, que es
justamente lo que permite generar 80 y quedarse con 12.

## Paso 1 — La grilla: deseo × familia de forma

Dos ejes, y cada celda se llena por separado:

**Eje 1 — DESEO (Paso A de `COPY.md`: LF8 + niveles de conciencia de Schwartz).**
El ángulo. Tomar los deseos LF8 que la marca puede tocar honestamente y cruzarlos con el nivel
de conciencia del público (carrusel = tibio/retargeting → *problem/solution-aware*):

| # | Deseo LF8 | Pregunta que lo traduce a ESTA marca |
|---|---|---|
| 1 | Sobrevivir, seguridad | ¿Qué riesgo/pérdida evita? |
| 2 | Disfrutar (comida, placer, confort) | ¿Qué se siente mejor? |
| 3 | Libre de miedo, dolor, peligro | ¿Qué deja de doler/preocupar? |
| 4 | Pareja, atracción | ¿Cómo cambia cómo se ve/se siente con otros? |
| 5 | Condiciones de vida cómodas | ¿Qué tiempo/plata/espacio recupera? |
| 6 | Estatus, ganar, ser superior | ¿En qué queda por delante / se enorgullece? |
| 7 | Proteger a los suyos | ¿Qué cuida de su familia/equipo/clientes? |
| 8 | Aprobación social | ¿Qué puede mostrar sin vergüenza? |

(No las 8 a la fuerza: quedarse con las 4-6 que la marca puede sostener con datos reales. Un
deseo que la marca no puede respaldar produce claims inventados — regla roja.)

**Eje 2 — FAMILIA DE FORMA (Paso B de `COPY.md`, las 5 fórmulas de titular).**
La forma del hook, no el ángulo:

1. **Outcome** — "{Logra X} sin {dolor}" / "en {tiempo}".
2. **Problema (pregunta retórica)** — "¿{pregunta que apunta al dolor}?" / "Nunca más {evento}".
3. **Audiencia** — "{Producto} para {audiencia}" / "No necesitas {skill} para {outcome}".
4. **Diferenciación** — "La {categoría} que {diferenciador}" / "La forma {opuesta} de {outcome}".
5. **Prueba** — "{Número} {personas} usan {X}…" — **solo con número REAL**.

## Paso 2 — Generación: N candidatos POR CELDA

- El generador recibe la grilla y produce **N candidatos por celda**, trabajando **celda por
  celda, en pasadas separadas** — no la grilla entera de un tirón: la pasada única es la que
  colapsa en una sola forma ("Deja de" ×6).
- **Cada candidato es un carrusel COMPLETO: el texto real de CADA slide.**
  No un hook con un resumen — el copy tal como se va a producir.

### 🔴 Qué trae cada candidato (director creativo, 6-ago-2026)

> *"en vez de que dé 'ideas' tiene que decir cada texto de cada slide"*.

| Campo | Qué es |
|---|---|
| `celda` | deseo × familia (de qué casilla de la grilla salió) |
| `hook` | el titular de la slide 1, ≤12 palabras |
| `slides` | **el texto de TODAS las slides**: `titulo` + `sub` de cada una, en orden |
| `cta` | la slide de cierre con la marca (remate del dolor + nombre de la marca) |
| `marca` | 🔒 dato del cliente · ⚙️ función a confirmar · 🧮 afirmación regulada · ✅ limpia |

**Por qué el texto completo y no un resumen.** Un hook + dos líneas de descripción no se puede
elegir: el que elige está aprobando un carrusel que todavía no existe, y lo que llega a
producción no se parece a lo que aprobó. Peor: **el desarrollo es donde el copy se cae.** El
lote frenado de agosto tenía hooks correctos y falló en las slides 2-4 (pasiva, mecanismo sin
explicar, contradicción entre el titular y el desarrollo) — nada de eso se ve en un resumen.
Escribir las slides es también lo que obliga al generador a **descubrir que la idea no cierra**
antes de que el director creativo la elija.

**Lo único que NO se escribe en esta fase:** el `primary_text` de Meta (es Fase 2, y solo para
las elegidas). Sin blueprint, sin zonas de texto, sin `visual_need`: eso es Fase 3.

- El filtro de compliance del cliente se aplica **en la generación** (reglas rojas del
  brand-brain): es más barato no escribir la idea prohibida que descartarla después.
- **Nada de rellenar celdas con paráfrasis.** Si una celda no da, queda con 1 o vacía y se
  anota — una celda débil fuerza exactamente la repetición que la grilla existe para evitar.

### Cuántos candidatos: el volumen depende del tamaño del lote

| Se van a producir | Propuestas | Ratio | Grilla sugerida |
|---|:--:|:--:|---|
| **2-3 carruseles** (lote chico) | **10-12** | ~5:1 | 3-4 deseos × 3-4 familias, 1 por celda |
| 4-6 carruseles | 20-25 | ~4:1 | 4-5 deseos × 5 familias, 1 por celda |
| 8+ carruseles (lote grande) | 40-60 | ~5:1 | 5 deseos × 5 familias, 2 por celda |

Default de lote chico fijado por el director creativo el 6-ago-2026. Con slides completas cada candidato
cuesta 4-5× más que un hook suelto, así que el volumen bajó y **el ratio se mantuvo**: lo que
hace funcionar al embudo es descartar mucho, no generar mucho. 80 hooks que no se pueden juzgar
valen menos que 12 carruseles que sí.

### Formato de cada candidato (así, literal)

```markdown
### {ID} · {familia} {✅|🔒|⚙️|🧮}
**Celda:** {deseo} × {familia}
**s-01 ·** {título de la portada}
   ↳ {subtítulo, o «—» si no lleva}
**s-02 ·** {título}
   ↳ {subtítulo}
**s-03 ·** {título}
   ↳ {subtítulo}
**s-04 · CTA ·** {remate del dolor de ESTE carrusel} + {nombre de la marca}
**Marca:** {✅ limpia · 🔒 falta <qué dato> · ⚙️ confirmar <qué función> · 🧮 revisar <qué claim>}
```

El nº de slides sale de `brand-brain/<cliente>/formatos.md`, no se inventa. Si el cliente
declara un rango (ej. Marca Verde: venta 4 / educativo 6-7), cada candidato usa el de SU formato.

> ⚠️ **Este formato es un contrato con `templates/deck_ideas.py`.** El deck lo parsea tal
> cual está escrito arriba (`### ID`, `**Celda:**`, `**s-NN ·**`, `↳`, `**Marca:**`). Si se
> cambia el formato acá, **se cambia el parser en el mismo turno y se corre contra un archivo
> real** — no contra un fixture escrito de memoria, que sale en el dialecto viejo. El 6-ago-2026
> el deck devolvió «0 ideas» sobre 24 propuestas perfectamente válidas por saltarse esto
> (`APRENDIZAJES.md` §33).

Salida: `ideas-<cliente>-<mes>.md` o `.json` (formato de entrada de `templates/deck_ideas.py`)
en la carpeta de ideación del lote (ej. `verde-ads/ideas-carruseles-2026-07/IDEAS.md`), y el
deck HTML generado con:

```
/usr/local/bin/python3 templates/deck_ideas.py ideas-<cliente>-<mes>.md -o ideas.html
```

## Paso 3 — Selección: corte POR CELDA, nunca por ranking global

- **Generador y selector son agentes/turnos distintos.** El que generó ya demostró que le
  gustan sus propias formas; el selector llega sin ese apego.
- El selector corta **K finalistas por celda (1-2)**, no un top-N global. El ranking global
  reproduce el sesgo del generador: si el 60% de la lista salió de una sola familia, el top-10
  global es esa familia con disfraces. El corte por celda garantiza **cobertura**: el lote final
  toca varios deseos y varias formas aunque una celda domine en "calidad" — la variedad ES el
  objetivo de la fase.
- **Insumo del selector: el scorer de rendimiento** (`references/scorer-rendimiento.md`).
  Si la cuenta tiene ≥10 ads con gasto en 90 días, el selector pondera las estructuras que ya
  rindieron EN ESA CUENTA al elegir los finalistas de cada celda (y declara como "apuesta" el
  finalista que no se parece a nada que haya rendido). Sin historial: se salta y se anota en
  el encabezado del archivo de ideas.
- El director creativo elige sobre el deck (o sobre los finalistas por celda) — esa es la parada
  `[✓ DIRECTOR]` de esta fase.

## Paso 4 — Lo que pasa a producción

Solo las ideas elegidas entran al pipeline normal: **Fase 0 (formato) → Fase 1
(`verify.py init`) → …**. La compuerta de comprensión y el resto de las puertas corren sobre
esas, nunca sobre las 80. El archivo de ideas completo se conserva: es el banco del que salen
los lotes siguientes (Marca Verde siguió produciendo de su `IDEAS.md` durante semanas).

## Resumen operativo

1. Grilla deseo (LF8/Schwartz) × familia (5 fórmulas del Paso B). Volumen según el
   tamaño del lote (tabla del Paso 2: **lote chico de 2-3 piezas → 10-12 propuestas**).
2. Generador (turno A): 1-2 por celda, pasadas separadas, compliance aplicado, y
   **cada candidato con el texto completo de TODAS sus slides** (título + sub + CTA),
   no un hook con un resumen.
3. `deck_ideas.py` → deck HTML agrupado por celda.
4. Selector (turno B): 1-2 finalistas POR CELDA + scorer de rendimiento como insumo.
5. `[✓ DIRECTOR]` elige → recién ahí Fase 0/1.
6. **Prohibido en esta fase:** `verify.py init`, carpetas, imágenes.
