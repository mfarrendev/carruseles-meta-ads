---
name: carruseles-max-final
description: Produce carruseles y posts publicables de principio a fin — elige el formato, escribe el copy, genera o elige las imágenes, compone el texto sobre la foto, verifica con compuertas deterministas y doble juez, y entrega el paquete listo para Meta. Úsala SIEMPRE que el director creativo pida ARMAR, DISEÑAR, HACER, PRODUCIR o CORREGIR un carrusel, un post o un ad de cualquier cliente. EXCLUSIONES (no es esta skill): Marca Cosmética tiene pipeline propio → `carruseles-<marca>` · decidir QUÉ tema hacer → `roadmap-creativo` · idear contenido de valor desde la persona → `ideacion-valor` · ajuste fino manual de una pieza ya producida → `editor-carrusel` · compliance legal del claim → `guardian-de-claims` · cambiar el logo de una imagen ya generada → `swap-logo-ai-image`. Reemplaza a carruseles-max-2-0, diseno-carruseles y carrusel-studio.
---

# Carruseles MAX FINAL

Skill única de producción de carruseles/posts. Orquesta **formato → copy → imagen →
composición → QA → entrega → publicación**, con compuertas que hacen que la calidad no dependa
de que el modelo se acuerde.

> **Principio rector:** *la IA razona, lo determinista hace cumplir.* Todo lo medible se mide
> con un script. Los jueces LLM solo juzgan lo que un script no puede ver.

## Qué hace y qué NO

**Hace:** carruseles y posts **1:1 (1080×1080)** para Meta Ads y feed — regla de la casa,
reconfirmada por el director creativo el 3-ago-2026 (Meta recomienda 4:5 para Feed, pero la
recomendación de plataforma no pisa el gusto del dueño); el 4:5 queda como opción por spec
(`"canvas": "4:5"`), no como ley · copy completo (hooks, slides, primary
text, headline, CTA) · generación/selección de imagen · composición del texto sobre foto ·
QA · paquete de entrega · publicación vía `meta-ads`.

**No hace:** reels y video (→ `reels-animados`) · ajuste fino arrastrando textos a mano
(→ `editor-carrusel`) · diseño de logos (→ `svg-logo-designer`) · decidir *qué tema* postear
este mes (→ `roadmap-creativo`) · compliance legal del claim (→ `guardian-de-claims`).

## Jerarquía de mando (no negociable)

1. **El director creativo.** Lo que él dice pisa cualquier regla escrita acá.
2. **El brand-brain del cliente** (`brand-brain/<cliente>/`) — tipografía, paleta, logo, CTA,
   tono, formato, disciplinas, sede. **Manda sobre todos los archivos de esta skill.**
3. **Los archivos de esta skill** — el método.

*El brand-brain dice CON QUÉ; esta skill dice CÓMO.* Si el cliente no tiene brand-brain, se
construye con el modo descubrimiento de `references/estilo-y-recursos.md` §3 y **se guarda ahí**.

## Mapa de archivos — dónde está cada cosa

| Necesitas… | Archivo |
|---|---|
| **Empezar un carrusel** (crea el spec, primer comando de todo) | `templates/verify.py init` |
| **Piden VARIOS carruseles** (embudo obligatorio: proponer ~5×, elegir, recién ahí producir) | **Fase −1** abajo + `references/fase-menos-1.md` + `templates/deck_ideas.py` |
| **No hay tema decidido** (ideación divergente: grilla deseo × forma, propuestas con TODAS las slides escritas → finalistas por celda) | `references/fase-menos-1.md` + `templates/deck_ideas.py` |
| **Qué formatos le sirven a ESTA marca** (y el reparto de un lote) | `brand-brain/<cliente>/formatos.md` + `templates/plan_lote.py` |
| **Que un lote no repita ángulos** (compuerta de lote) | `templates/qa_lote.py` (vía `verify.py lote`) |
| **Que un lote se corra en el orden correcto** (columnas, no filas; imagen después del plan) | `templates/orden_lote.py` (vía `verify.py lote`) — ver **MODO LOTE** |
| Qué formato hacer (quiz, tutorial, listicle, anuncio…) | `references/tipos-y-formatos.md` |
| Prompts de imagen que ya pasaron el gate | `references/prompts-validados.md` |
| **Pedirle a Higgsfield el hueco donde irá el texto** (cláusula por zona + compuerta) | `templates/prompt_zona.py` |
| **Prompts que FALLAN y por qué** (leer ANTES de generar) | `references/prompts-fallidos.md` |
| **Cuánto lleva gastado este carrusel** (generaciones, créditos, descartes) | `templates/costo.py` |
| **Que el motor no cambie sin que nadie lo note** (test de regresión) | `templates/dorado.py` |
| **Congelar lo que el director creativo aprobó** (copia inmutable + comparar) | `templates/aprobar.py` |
| **Qué pasó con lo publicado** (ad_id → insights → qué decisión gana) | `templates/rendimiento.py` |
| Escribir el copy | `COPY.md` |
| **Puntuar el hook contra rendimiento real** (paso por defecto de la Fase 2) | `references/scorer-rendimiento.md` |
| Chequeo mecánico del copy (AI-tells, hook, estructura) | `verify.py copy` → `_copy-gate-receipt.json` |
| ~~Validar que el copy se ENTIENDA~~ (panel derogado 10-ago-2026) | `APRENDIZAJES.md` §35 |
| De dónde sale la imagen / cómo generarla | `references/produccion-imagenes.md` |
| Dónde va el texto sobre la foto | `references/composicion-y-tipografia.md` |
| Recursos gráficos, "premium", kits tipográficos | `references/estilo-y-recursos.md` |
| Con qué se juzga | `RUBRIC.md` |
| **Registrar la publicación** (carrusel → ad_id de Meta) | `references/publicacion-y-registro.md` + `templates/registrar_publicacion.py` |
| Por qué existe cada regla (historial fechado) | `APRENDIZAJES.md` |
| Herramientas | `templates/` |

**Cada archivo es fuente única de su tema.** Si dos se contradicen, gana el específico y se
corrige el otro **en el mismo turno**. No se resuelve repitiendo la regla en los dos: así fue
como el piso del héroe llegó a tener cuatro cifras distintas.

---

# EL PIPELINE

Tiempo objetivo: **30-40 min** el primer carrusel de una familia (las fases suman eso; antes decía
15-20 y era fantasía) · **10-12 min** los siguientes. Los recibos llevan **timestamp**: la medición
real del tiempo se saca de ellos, no de estimaciones.
Los `[✓ DIRECTOR]` son paradas reales: se espera su OK antes de gastar generaciones.

## Las 4 puertas (fail-closed) — actualizado 31-jul-2026

> Antes había UNA puerta (`open`): se protegía la preview pero no la billetera ni la publicación.
> Ahora son cuatro y cada una exige recibos. El hook `carrusel-gate.py` las hace cumplir en
> Claude Code y en Kimi. Historia: `APRENDIZAJES.md` (31-jul-2026).

| Puerta | Qué se cruza | Recibos que exige | Quién los escribe |
|---|---|---|---|
| `generate_image` | copy → imagen | `_brief-receipt` · `_copy-gate-receipt` · `_blueprint-receipt` · **`_prompt-receipt`** | solo scripts |
| render (Chrome) | crudo → composición | `_raw-receipt` · `_raw-ojo-receipt` | `verify.py raw` + agente `raw-qa` |
| `open` | pieza → el director creativo | `_gates-receipt` | `verify.py gates` (el `_qa-receipt` se derogó el 7-sep-2026) |
| publicar a Meta | pieza → al aire | todos los anteriores, frescos | — |

Los recibos de script van **firmados con el hash** de lo que midieron: si se escriben a mano o
los archivos cambian después, el hook lo detecta y bloquea igual.

> 🔴 **`_copy-receipt.json` ya no existe (director creativo, 10-ago-2026).** El panel ciego de comprensión
> se derogó: quien aprueba que el copy se entiende es el director creativo, en la Fase −1, leyendo las
> propuestas completas. **No lo invoques, no lo escribas y no lo esperes** — ninguna puerta lo
> pide. **Y `copy-craft-qa` se eliminó el mismo día**: el carrusel no tiene ningún juez de texto.
> Queda solo `verify.py copy` (script). El copy lo aprueba el director creativo en la Fase −1.
> Relato completo y método del panel derogado: `APRENDIZAJES.md` §35.

> **Corrida canónica completa verificada (3-ago-2026):** `verde-comparativa-skills/a-carruseles-max-final/`
> — pipeline end-to-end con las puertas en PASS y doble juez. Es **anterior a la derogación**:
> ahí todavía hay un `_copy-receipt.json`; hoy ese recibo sobra y no invalida nada.

**WARN aceptado con razón escrita (3-ago-2026).** Los recibos distinguen `fails` y `warns`:
0 fails + N warns → `"status": "PASS_CON_WARNS"` y la puerta pasa igual. Con
`--warn-ok "razón"` la aceptación queda grabada en el recibo; sin el flag el recibo dice
`warns_sin_razon: true` y **la Fase 7 tiene que revisarlos uno por uno**. Y la doctrina que
los gobierna (RUBRIC E11.b): las métricas de densidad/espaciado se satisfacen con contenido
real, **NUNCA con ornamento** — un WARN de densidad se acepta con razón antes que decorar
la slide.

**Falta el spec = FAIL, no bypass** (1-ago-2026). Si la carpeta parece carrusel y no tiene
`carrusel.json`, las puertas lo dicen con instrucción (`verify.py init`) en vez de dejar pasar:
la carpeta sin spec es justamente la que nadie verificó (medición: 79 de 81 carpetas sin spec).
Historia: `APRENDIZAJES.md` §9. El trabajo ya entregado quedó congelado en
`.claude/.carruseles-legacy` (conserva el comportamiento viejo, auditable).

## El spec: `carrusel.json`

Una sola fuente de máquina por carrusel — brief, copy y blueprint juntos. La leen los gates, el
motor y los jueces. El `_brief.md` en prosa sigue siendo obligatorio (RUBRIC F1).

**No se escribe a mano: lo crea `verify.py init <carpeta>` en la Fase 1** (ver abajo).

```jsonc
{ "cliente": "marca-estudio", "linea": "Marca Bronce", "objetivo": "ventas",
  "formato": "anuncio", "framework": "PAS", "segmento": "mujeres 35-45 zona oriente",
  "angulo": "la hora del almuerzo es la única que tienen — y nadie la aprovecha",
  "cta": "Comienza tu clase hoy", "brand": "navy", "canvas": "4:5",
  "presupuesto_imagenes": 18,        // tope de generaciones; por defecto slides × 1
  "tipografia": {"font": "assets/Oswald.woff2", "weight": 700, "size": 92},
  "hook_variantes": ["…", "…"], "primary_text": "…",
  "slides": [{"n": 1, "titulo": "…", "sub": "…", "eyebrow": "…",
              "zone": "l", "v": "mid", "visual_need": "qué debe DEMOSTRAR la foto",
              "zoom": 1.5, "posx": 1.0, "posy": 1.0,   // opcional: acerca el encuadre
              "foto": "raw/s-01.png", "fuente": "real"}] }
```

⚠️ **`zoom` acerca el encuadre sin regenerar la foto** (director creativo, 5-ago-2026: *"la portada tiene
mucho texto y poca imagen, podríamos hacer a la mascota más grande"*). Un crudo de 2048² sobre
un lienzo de 1080² se usaba **entero siempre**, así que agrandar al sujeto obligaba a gastar
generaciones. `zoom: 1.5` = 50% más grande de lado, anclado en `posx`/`posy` (1.0/1.0 = abajo a
la derecha). **Acercarse recorta: hay que mirar el PNG.** Reglas y techos medidos:
`references/composicion-y-tipografia.md` §7.1.

⚠️ **`presupuesto_imagenes` es el tope de generaciones de este carrusel** (5-ago-2026). Sin
declararlo el tope es **`slides × 1`: UNA pasada** (Max, 7-sep-2026 — ver la regla de UNA
PASADA más abajo). El hook
`costo-imagenes.py` cuenta cada llamada a Higgsfield en `_costo.json`; al llegar al tope la
puerta GENERAR **pregunta antes de dejar gastar más**. Medición que lo originó: 255 generaciones
para 20 fotos usadas (8%) — `APRENDIZAJES.md` §23. Se declara con
`templates/costo.py presupuesto <carpeta> N` y se mira con `costo.py estado <carpeta>`.

⚠️ **`angulo` es obligatorio** (lo exige `verify.py brief`): la idea central del carrusel en
una línea, declarada. Es lo que la compuerta de lote (`verify.py lote`) compara entre
carruseles hermanos para que dos piezas del mismo lote no salgan con el mismo ángulo.
`canvas` es opcional: por defecto 1:1 (regla de la casa, reconfirmada por el director creativo el
3-ago-2026); `"4:5"` solo si el spec lo declara expresamente.

⚠️ **Declarar `tipografia.font`** (la `.woff2` real del render). Sin eso todo se mide con un proxy
Arial, que es más angosto que Oswald/Montserrat: las líneas se pasan de la caja verificada y
terminan sobre el sujeto. El motor aplica un margen de seguridad, pero achica el título de más.

---

## 🔴 UNA PASADA: se genera una vez, se muestra, y decide Max (7-sep-2026)

> **Max, 7-sep-2026:** *"antes hacíamos todo esto de los jueces y blabla, ahora quiero que solo
> sea un límite de una generación de imágenes, onda que haga el carrusel 1 vez y me lo muestre"*.

**El default pasa de `slides × 3` a `slides × 1`.** Una generación por slide, se compone, se mira
y se muestra. Se acabaron los reintentos automáticos.

| | Antes | Ahora |
|---|---|---|
| Tope por defecto | `slides × 3` | **`slides × 1`** |
| Reintento si un crudo sale mal | automático, hasta 2 por slide (Fase 4b) | **ninguno.** Se reporta y decide Max |
| Fase 7 — doble juez | obligatoria, hasta 2 rondas | **no se corre** |
| Fase 4b — auditar el crudo | compuerta que dispara reintentos | queda como **lectura**, no dispara nada |

**Lo único que sobrevive, porque no cuesta tiempo ni créditos:** mirar el PNG y la hoja de
contacto antes de mostrar (§4 del AGENTS.md, sigue siendo obligatorio) y **decir qué salió mal**.
Reportar un defecto no es pedir permiso ni abrir una ronda: es entregar la pieza con su estado
escrito. *"La slide 2 dice «faltan tan muchas»"* — y Max decide si vale una generación más.

**Lo que esto cuesta, dicho una sola vez y no repetido en cada entrega:** con una pasada, un
garabato del modelo no se arregla solo; llega hasta Max. Es exactamente el intercambio que pidió
—menos ceremonia, menos gasto, más rápido— y él ya sabe leer una hoja de contacto. Si una pieza
en particular necesita colchón, se declara con `costo.py presupuesto <carpeta> N` **antes** de
generar, no a mitad de camino.

Esto **no toca las 4 puertas deterministas** (brief, copy, blueprint, prompt): esas son scripts,
corren en milisegundos y no gastan créditos. Lo que se apaga son los **jueces LLM** y los
**reintentos**.

## MODO LOTE — cómo se hacen 10 carruseles sin que tome un día

> **El director creativo, 6-ago-2026:** *"necesito que la skill sea más rápida, siento que hacer 10 carruseles
> no puede demorarse horas."* Tiene razón, y la medición dice **por qué** se demoró — que no era
> lo que yo suponía.

### Lo que se midió (lote Marca Verde, 4 carruseles, 5-ago)

Reconstruido de los mtimes de los 48 recibos en `verde-ads/carruseles-2026-08-venta/`:

| Síntoma | Medición |
|---|---|
| **Se generaron imágenes ANTES de tener brief y blueprint** | c1: 1er crudo **14:46**, brief y blueprint **17:03** (2 h 17 min después). Igual en c2, c3 y c8: **los 4** |
| **Vueltas atrás a una fase ya pasada** | **19 en 4 carruseles** (c1: 7 · c2: 6 · c3: 4 · c8: 2) |
| Trabajo hecho en lote | solo **52%** — la otra mitad, carrusel por carrusel |
| Copy del lote grande (c4-c10) | 7 carruseles, **10 min** para los 7 (15:07→15:17) ← así se ve cuando SÍ es lote |

**El plan se escribió a las 17:03 para justificar fotos que ya existían desde las 14:46.** Ese es
el hallazgo. No fueron los jueces (§25: 9 min por ronda), no fue el tope de imágenes (§27), y no
fue solo el goteo de ráfagas (§28). Fue **empezar por el final**: generar, después mirar, después
escribir el plan que las explicara, y volver atrás 19 veces a arreglar lo que el plan habría
decidido gratis.

Contraste que lo prueba: **el copy de 7 carruseles tomó 10 minutos** porque se corrió como lote y
en orden. Las 4 piezas que se hicieron "cada una de punta a punta" se llevaron el día.

### Las cuatro reglas del modo lote

**1 · Una fase, todas las piezas, después la siguiente. Sin excepción.**
Los 10 briefs juntos → los 10 copys juntos → los 10 blueprints juntos → **una** ráfaga de
prompts → **una** hoja de contacto → composición de las 10 → gates de las 10 → jueces de las 10.
Nunca "termino el c1 y sigo con el c2". El pipeline es **columnas, no filas**.

**2 · Ninguna imagen antes del blueprint de TODO el lote.** Es lo que se violó en los 4
carruseles y lo que costó las 19 vueltas atrás. Una foto generada antes del plan no ahorra
tiempo: **compra** trabajo — el plan se termina escribiendo para justificarla, y cuando no
calza, se regenera. La puerta GENERAR ya lo bloquea (exige `_brief`, `_copy`, `_blueprint` y
`_prompt`); esta regla es para no intentarlo.

**3 · Las fases 0-3 son texto: van en paralelo, no en serie.** Escribir 10 briefs no son 10
tareas de 2 min encadenadas. Se escriben juntos en una pasada, se verifican con un comando
(`verify.py brief` por carpeta, en un `for`), y el panel de copy juzga las 10 piezas en una
tanda. Medido: 7 copys en 10 min. **Lo que no espera a un modelo externo, no debe tomar horas.**

**4 · El reloj de verdad es el número de RÁFAGAS, no el de slides.** 10 carruseles × 5 slides =
50 imágenes. En ráfagas de 12 eso son **5 viajes**, no 50. Con la regla de lote y `goteo()`
(§28), el costo de reloj de un lote de 10 se parece al de un lote de 4.

### Qué se puede esperar

| Trabajo | Con el pipeline en columnas |
|---|---|
| Fases 0-3 (brief + copy + blueprint) de 10 piezas | **~25-35 min** — es texto, va en tandas |
| Fase 4 (50 imágenes en 5 ráfagas de 12) | **~50-60 min** — dominado por la espera del modelo |
| Fases 5-6 (componer + gates de 50 slides) | **~10-15 min** — es determinista y local |
| Fase 7 (doble juez, 10 piezas en tandas) | **~20-30 min** (§25: 9 min por ronda de 2) |
| **Total realista de 10 carruseles** | **~2 h**, no 8 |

**Lo que NO se puede comprimir, y hay que decirlo:** las ~50-60 min de la Fase 4 son espera de
Higgsfield. Ahí no hay optimización de proceso posible — solo pedir menos imágenes o pedirlas
mejor agrupadas. Todo lo demás sí es nuestro.

---

### Fase −1 — EMBUDO CREATIVO `[✓ DIRECTOR]` — **obligatoria en LOTE** (6-ago-2026)

> **El director creativo, 6-ago-2026:** *"que me proponga 100 carruseles (copys) y yo elegir los 10 mejores;
> cuando diga 'quiero hacer carruseles', que me diga 'cuántos quieres que te proponga'."*
> Es lo que ya hacía a mano: *"si le decía 'haz 20', eran muy malos."*

**Si el pedido es de VARIOS carruseles, esta fase no se salta.** El método completo está en
`references/fase-menos-1.md`; acá va cuándo se dispara y qué se pregunta.

**Lo primero, antes de cualquier otra cosa — preguntarle dos números:**

> *¿Cuántas propuestas te hago?* · *¿Cuántos vas a producir de esas?*

Defaults por tamaño de lote (tabla completa en `fase-menos-1.md`): **2-3 piezas → 10-12
propuestas** · 4-6 → 20-25 · 8+ → 40-60. Lo que hace funcionar al embudo es el **ratio ~5:1**,
no el volumen bruto.

**🔴 Cada propuesta es un carrusel COMPLETO, no una idea** (director creativo, 6-ago-2026:
*"en vez de que dé 'ideas' tiene que decir cada texto de cada slide"*). Va el texto real de
CADA slide — título + subtítulo — más la slide de cierre con la marca. Un hook con un resumen
de dos líneas **no se puede elegir**: el que elige aprueba un carrusel que todavía no existe, y
el desarrollo (slides 2-4) es justamente donde el copy se cae — el lote frenado de agosto tenía
hooks correctos y murió ahí. El `primary_text` sigue siendo Fase 2; el blueprint, Fase 3.

Lo hace cumplir el hook `embudo-creativo.py` (UserPromptSubmit): detecta "carruseles" en plural
con verbo de producción y sin selección previa, y recuerda preguntar antes de entrar en Fase 0.
No se dispara con un carrusel en singular (no hay nada que filtrar), ni si el director creativo ya viene
eligiendo de un deck, ni si dijo "sin preguntar".

**Por qué es obligatoria en lote y no en una pieza suelta.** Pedir directamente N carruseles
produce los N que el generador se atreve a defender — o sea lo seguro, N veces la misma forma.
El descarte es lo que permite que los elegidos sean buenos: una idea sin carpeta no le debe nada
a nadie. El lote con **seis hooks abriendo con "Deja de"** salió de *"una semilla, hazme 10"*.
Una pieza suelta no tiene ese problema, y exigirle embudo sería un trámite.

**Las dos reglas que hacen que funcione** (detalle en `fase-menos-1.md`):
- **Corte POR CELDA, nunca top-N global.** El ranking global reproduce el sesgo del generador:
  si el 60% de la lista salió de una familia, el top-10 es esa familia con disfraces.
- **Generador y selector en turnos distintos.** El que generó ya demostró que le gustan sus
  propias formas.

**Prohibido en esta fase:** `verify.py init`, crear carpetas, generar imágenes. La salida es
**solo texto** — el archivo de ideas + el deck (`templates/deck_ideas.py ideas.md -o ideas.html`).

**Lo elegido se declara.** El spec de cada pieza lleva `procedencia`: la ruta del archivo de
ideas + la celda de la grilla, o `"pedido-directo: <lo que pidió el director creativo>"`. `qa_brief` lo marca
**WARN si el carrusel tiene ≥2 hermanos** y no está declarado (en pieza suelta ni lo pregunta).

### Fase 0 — FORMATO (2 min)
**Si es UNA pieza y el tema ya viene dado** (pedido del director creativo, campaña en curso), se arranca
directo acá. Si son varios carruseles, primero la Fase −1 de arriba.

Partir por el **objetivo** (guardados / comentarios / ventas / confianza / cercanía) y con la
matriz de `references/tipos-y-formatos.md` elegir **familia → formato → framework narrativo →
modo de ejecución → nº de slides**. Sin este paso todo sale "educativo por defecto".
El brand-brain pisa la tabla: **ads en 1:1 (1080×1080), SIEMPRE** (regla de la casa,
reconfirmada por el director creativo el 3-ago-2026; el 4:5 es opción excepcional declarada en el spec,
no ley), y **el nº de slides lo fija
el cliente** en `brand-brain/<cliente>/formatos.md`, no esta tabla. Si esa declaración no existe,
`qa_blueprint` lo dice en vez de inventar un rango.

### Fase 1 — BRIEF (2 min)

**Se abre con el andamio. Es el primer comando de todo carrusel:**

```
/usr/local/bin/python3 templates/verify.py init <carpeta> [--slides N]
```

Deja `carrusel.json` con los campos obligatorios **vacíos a propósito** y un `_brief.md` con la
plantilla. Rellenar los dos es el trabajo de esta fase; están vacíos porque un esqueleto que
pasara la compuerta con valores de relleno la convertiría en un trámite.

> **Por qué es un comando y no "escribí el JSON":** sin una fase que lo mande, nadie creaba el
> spec y el agente terminaba escribiendo su propio `build.py` fuera de las puertas. Relato:
> `APRENDIZAJES.md` §9 (1-ago-2026).

Lo que hay que dejar escrito, en los dos archivos: objetivo y formato (Fase 0) · **cliente** ·
**línea/sede** (Marca Bronce ≠ Pilates ≠ Online ≠ App) · brand-brain leído (ruta) · fotos
fuente reales de ESA sede o plan de generación · disciplina↔línea verificada · CTA de esa
línea · persona/Reference Element. Si algo es "no sé", se resuelve ANTES de seguir.

Cierra con `verify.py brief <carpeta>` en PASS. El andamio arranca en FAIL: eso es lo correcto,
va marcando lo que falta.

Si el cliente tiene `brand-brain/<cliente>/ejemplos-gusto/`, **leerla completa**: son slides que
al director creativo le encantaron (✅) o rechazó (✗), con el porqué. Es vara visual además de la rúbrica.

### Fase 2 — COPY (3-5 min)
Aplicar **`COPY.md`** — no se improvisa ni se delega. Regla #0 anti-IA → **Paso A** (deseo,
LF8, StoryBrand, PAS, voz de la clienta: define el ÁNGULO) → **Paso B** (fórmulas de titular de
Corey Haines: le da la FORMA al hook, ≤12 palabras) → estructura → **~20 candidatos de hook por
familia de fórmula → 3 finalistas de familias DISTINTAS** →
primary text estructurado. Informativos: datos **investigados y reales**, cero cifras inventadas.
Si se importa una fórmula externa, **primero pasa por el filtro de compliance del cliente**
(`COPY.md` § filtro de frameworks de terceros).

**Paso por defecto, con evidencia:** puntuar las variantes del hook contra el rendimiento REAL de la
cuenta (`references/scorer-rendimiento.md` — top ads 90 días vía `meta-ads` → qué estructuras
ganan → el copy nuevo se evalúa contra eso, no contra intuición) **y dejar el resultado documentado
en el `_brief.md`** (qué estructura ganó y por qué se eligió el hook). Si no hay historial o
acceso, se salta y se anota en el `_brief.md` el motivo.

Luego **`verify.py copy` → `_copy-gate-receipt.json`**: el chequeo mecánico (AI-tells, triadas,
clichés, hook >12 palabras, estructura del primary text). Es lo ÚNICO que revisa el texto.

🔴 **Los dos jueces de texto están eliminados** (director creativo, 10-ago-2026): el panel ciego de
comprensión (`copy-qa`) y el juez de craft (`copy-craft-qa`). No los invoques ni esperes sus
recibos. **Quien aprueba el copy es el director creativo en la Fase −1**, leyendo las propuestas con todas
sus slides escritas. Historia: `APRENDIZAJES.md` §35 y §36.

### Fase 3 — BLUEPRINT `[✓ DIRECTOR]` (2 min)
Antes de generar UNA sola imagen, decidir por slide: **qué dice**, **en qué zona va el texto**
(rotando entre slides vecinas) y **qué debe MOSTRAR la foto**. La imagen se elige o se encuadra
PARA el plan, nunca al revés.

**Mostrarle al director creativo en un mensaje corto:** copy slide por slide + variantes del hook +
blueprint + CTA, y **esperar su OK**. Corregir texto cuesta segundos; corregirlo después de 20
imágenes cuesta la tarde. Si dijo "dale sin preguntar" para ese trabajo, se salta y se anota en
el `_brief.md`.

### Fase 4 — IMÁGENES `[✓ DIRECTOR: preguntar la fuente]` (3-6 min)

**Antes de generar o elegir nada, PREGUNTARLE qué fuente usar en este trabajo** (corrección
El director creativo, jul-2026). No se asume: hay marcas con banco de fotos y marcas que no tienen ninguna,
y lo habitual es **mezclar** — fotos reales donde existen, generadas donde falta la escena.

Mostrarle qué hay disponible y proponer el reparto:
> *"Para este carrusel: slides 1, 2 y 5 tengo fotos reales de la sede; para las 3, 4 y 6 no hay
> nada que muestre eso. ¿Genero esas tres con Higgsfield, uso otras reales aunque encajen peor,
> o cambiamos el mensaje de esas slides?"*

El reparto elegido se anota en el `_brief.md`, slide por slide.

**Orden de preferencia cuando él no indique otra cosa:** fotos reales de la sede correcta →
frames de videos del brand-brain → Higgsfield (`mcp__higgsfield__generate_image_batch`).
*(La evidencia respalda ese orden — los aprobados del historial usaron fotos reales; ver
`APRENDIZAJES.md`.)* Generar no está prohibido — está declarado.

**Si se genera:** partir de **`references/prompts-validados.md`** (encuadres que ya pasaron
`qa_raw`, con su medición) en vez de escribir el prompt desde cero. Cada foto nueva que pase
limpia se agrega ahí. Y **leer antes `references/prompts-fallidos.md`**: el catálogo de aciertos
sin anti-catálogo hace repetir los errores gratis (§23).

**Antes de la primera llamada: declarar el presupuesto** —
`costo.py presupuesto <carpeta> N`. Sin número declarado el tope es `slides × 3` (15 para un
carrusel de 5). El contador (`_costo.json`) es automático.

**El tope tiene DOS techos y los dos son DENY** (endurecido 6-ago-2026):

| Techo | Cuánto | Por qué |
|---|---|---|
| Imágenes | `presupuesto_imagenes`, por defecto `slides × 1` | UNA pasada (Max, 7-sep-2026) |
| Créditos | `tope × 2 × 1.25` | un contador de imágenes es **ciego al modelo**: 12 `gpt_image_2` son 144 créditos y cuentan igual que 12 `nano_banana_pro` (24). En el lote Marca Verde ese renglón fue el 20% del gasto y no movió el contador |

**Se cuenta el pedido que está por ejecutarse, no solo lo ya gastado.** El chequeo viejo era
`gastado >= tope`, así que con el contador en 14 y tope 15 **una batch de 24 pasaba entera** —
y la ráfaga más grande del lote Marca Verde fueron exactamente 24 imágenes de un saque. Ahora se
evalúa `gastado + pide`.

**Subir el tope exige motivo escrito:**

```
costo.py presupuesto <carpeta> <N> --por "escena difícil, 3 encuadres fallados"
```

Queda fechado en `presupuesto_historial` dentro del spec. Bajarlo o fijarlo de entrada no pide
nada; **subirlo sí**, porque un tope que se sube en silencio no es un tope — es el mismo bucle
"regenerar es más barato que pensar" con un paso extra.

> **Por qué DENY y no ASK.** Era ASK "porque hay carruseles que legítimamente necesitan más" —
> y eso sigue siendo cierto, por eso hay escape. Pero desatendido, que es **justo** cuando el
> bucle corre solo, un ASK sin nadie mirando no frena nada. Fail-closed para la billetera, igual
> que para publicar. (Esto NO contradice *degradar en vez de frenar*: ahí se degrada el CLAIM
> que falta un dato; acá se frena el GASTO, que es otra cosa.)

> **Cuánto habría ahorrado, medido sobre el lote real** (190 generaciones, 4 carruseles vivos):
> tope 10 → corta en la ráfaga 4 (**−77%**) · **tope 15 (el actual) → corta en la ráfaga 5,
> 15:11 h (−64%)** · tope 20 → ráfaga 7 (−56%) · tope 30 → ráfaga 13 (−29%). El 15 por defecto
> ya alcanza: lo que faltaba no era un número más chico, era que se cumpliera.

**Generar a 2048² DE UNA, no generar chico y agrandar después** (5-ago-2026). En el lote Marca Verde
salieron 49 upscales: 98 créditos gastados en subir de tamaño lo que se podía haber pedido a 2K
en la misma llamada, y un upscale no arregla un encuadre — solo agranda el mismo error. El
upscale queda para rescatar un crudo bueno que ya existe, no como paso del pipeline.

**Nunca `gpt_image_2` para un crudo de carrusel.** Cuesta **12 créditos: 6× un
`nano_banana_pro`.** En el lote del 4-5 de agosto se fueron 144 créditos (20% del gasto total)
en 12 imágenes de ese modelo que no llegaron a disco. Para fotografía de producto/persona con
Reference Element, `nano_banana_pro` rinde igual o mejor por un sexto.

#### Regla de LOTE — todas las slides de una fase juntas, nunca de a una

Si el pedido es un lote (2+ carruseles), **cada fase se corre para TODAS las piezas antes de
pasar a la siguiente.** Los prompts de las 50 slides se escriben juntos, se verifican juntos, se
generan en ráfagas de 12 (el máximo de `generate_image_batch`), se auditan en UNA hoja de
contacto, y recién ahí se compone. Nunca carrusel por carrusel de punta a punta.

> **Por qué, medido en el lote Marca Verde del 5-ago.** El día tuvo dos tramos muy distintos:
>
> | Tramo | Ráfagas | Media | min/ráfaga |
> |---|---|---|---|
> | 14:37→15:48 (generación inicial) | 14 | 9,6 img | 5 |
> | **15:48→17:40 (iteración)** | **11** | **3,7 img** | **10,2** |
>
> En el segundo tramo **5 de las 11 ráfagas fueron de UNA sola imagen**: mirar, no gustar,
> regenerar, esperar, mirar. 41 imágenes en 112 minutos. Proyectado a 10 carruseles con la
> misma forma de trabajo: **~4,6 h solo iterando imágenes**, y ningún tope lo evita — cada
> pedido es chico, así que el presupuesto ni se entera. Peor: **cortar el gasto sin cambiar
> esto cambia horas por menos imágenes**, que es el mal negocio.

**Las tres reglas que lo hacen cumplir:**

1. **Una ráfaga por fase y por lote, no por slide.** Si hay que regenerar 6 slides de 4
   carruseles distintos, es **una** llamada de 6, no seis llamadas de 1. El costo de reloj es el
   viaje, no la imagen (las ráfagas mandan 12 en el mismo segundo).
2. **Prohibido regenerar de a una para "ver cómo queda".** Si una slide no convence, se anota y
   se sigue con el resto del lote; las correcciones se juntan y salen en la ráfaga siguiente.
   Mirar-regenerar-mirar es el bucle de 10 min que produjo las 2 h.
3. **Antes de cada ráfaga de corrección, el descarte va con motivo** (`costo.py descartar`). Si
   el mismo motivo aparece 2 veces en el lote, se corrige el PROMPT para todas las slides que lo
   comparten — no se regenera una por una con otra semilla.

**Lo que NO arregla esto, y hay que decirlo:** el reloj de un lote grande sigue estando dominado
por las esperas del modelo. La regla no lo vuelve instantáneo — lo vuelve **proporcional al
número de fases (≈6 ráfagas) en vez de al número de slides (≈50)**.

**Y tiene compuerta, no solo prosa** (6-ago-2026). `goteo()` en `carrusel-gate.py` lee el
`eventos[]` de `_costo.json` (cada ráfaga queda ahí con su hora y su tamaño) y **a la tercera
ráfaga seguida de ≤2 imágenes, PREGUNTA** — con el historial a la vista y las tres salidas:
juntar la corrección con las otras pendientes · `zoom`/`posx` en vez de otra foto · si el motivo
ya salió 2 veces, corregir el PROMPT para todas las slides que lo comparten. Es **ASK y no
DENY** a propósito: hay regeneraciones sueltas legítimas; lo que no puede pasar es encadenar
cinco sin que nadie lo note. **Un pedido de más de 2 imágenes pasa siempre**, aunque venga de
una racha — es justo la conducta que se quiere. Relato y medición: `APRENDIZAJES.md` §28.

#### Fase 4a — EL PROMPT RESERVA EL HUECO DEL TEXTO `[compuerta, antes de pagar]`

Regla del director creativo (7-jul-2026, reafirmada el 6-ago-2026): *"la skill entiende de qué será el
copy y ve cómo lo dispondrá en la imagen; genera una imagen con Higgsfield indicándole dónde
estará el texto, para así no poner nada ahí."* El `zone` ya está decidido en el blueprint —
esta fase lo mete DENTRO del prompt y lo verifica.

```
/usr/local/bin/python3 templates/prompt_zona.py armar <carpeta>   # la cláusula exacta por slide
# …se pega al final del prompt de cada slide y el prompt REAL se guarda en slides[].prompt…
/usr/local/bin/python3 templates/verify.py prompt <carpeta>       # → _prompt-receipt.json
```

`armar` **deriva la cláusula de la geometría real del motor** (`COLUMNAS` + `MARGEN`), no de la
memoria: para `zone: "l"` sale *"subject in the RIGHT portion, leaving the left 52% (from 6% to
58% across) as open negative space…"*. Si mañana la columna cambia de ancho, la cláusula cambia
sola.

**Los dos FAIL que caza, y por qué son FAIL y no warn:**
- el prompt **no nombra el lado** de su zona → la foto va a nacer con el sujeto encima del texto;
- el prompt pide **`"empty black space"` / `"clean empty area"`** → sale medio rectángulo muerto
  pegado a la escena y la imagen se ve **partida en dos**. El hueco es *continuidad de la misma
  escena* (mismo fondo, misma luz, el glow desvaneciéndose hacia ese lado), nunca un recorte.

> **Por qué es una compuerta y no un párrafo** (6-ago-2026): la regla existía desde julio y
> estaba bien escrita, pero era prosa que el agente tenía que recordar en pleno vuelo. Medido en
> el lote Marca Verde: **las 5 slides de c1 tenían su `zone` en el spec y ninguna tenía el `prompt`
> guardado** — después no había forma de saber si se había pedido el hueco. Y `verify.py raw`
> mide el mismo hueco **después de generar**: cuando falla, la generación ya está pagada.
> Ésta es la única compuerta del pipeline que corre sobre algo que todavía no se gastó.

**DOS TANDAS, NUNCA UNA SOLA GRANDE** (6-ago-2026). Primero **una imagen por slide** (tanda de
prueba, `slides` generaciones). Se audita esa tanda con la Fase 4b **completa** — incluido el
chequeo imagen-vs-mensaje. Recién con los prompts corregidos se pide la tanda buena. Nunca al
revés: no se explora generando 24 variantes de una escena para elegir después.

> **Por qué, medido en el libro de Higgsfield** (sesión del 5-ago, 14:37→23:08): **147 de las 190
> generaciones —el 77%— salieron en los primeros 71 minutos**, en 15 ráfagas, *antes de que
> ningún juez hubiera visto una sola imagen*. De todo eso quedaron 21 crudos en disco. No fue
> un problema de criterio al elegir: fue generar el catálogo primero y mirar después. Una tanda
> de prueba de 5 imágenes cuesta 10 créditos y contesta lo mismo que 147.

Reglas duras en las dos vías: **imágenes distintas, cero repetición** dentro de un carrusel ·
**misma persona = Reference Element** · lugar real, nunca inventado · la imagen DEMUESTRA el
mensaje, no decora. Las generaciones se paralelizan con las tools calificadas
**`mcp__higgsfield__generate_image_batch`** (1-12 prompts independientes en una sola llamada)
y se esperan con **`mcp__higgsfield__jobs_wait`**; el set terminado se muestra con una sola
`show_generation_by_ids`. Detalle en `references/produccion-imagenes.md`.

### Fase 4b — MIRAR EL CRUDO `[lectura, ya NO dispara reintentos]` (1 min)

> 🔴 **Cambió el 7-sep-2026.** Sigue siendo obligatorio mirar el crudo antes de componer — eso es gratis y caza garabatos del modelo. Lo que ya **no** hace es regenerar sola: el defecto se anota y se entrega con la pieza. Regenerar lo decide Max. Ver «UNA PASADA» arriba.
**Ninguna foto pasa a composición sin mirarla sola.** Hoja de contacto de `raw/` + una lectura,
y por cada foto: ¿letras inventadas en pantallas/teclas/papeles? ¿logo de marca real? ¿anatomía
rota? ¿la zona de texto planificada quedó libre (`cutout` + `photo_map`)? Detalle y tabla de
encuadres en `references/produccion-imagenes.md` §0.

**La quinta pregunta, y la que más caro sale si se saltea — B1, imagen vs. mensaje**
(6-ago-2026). Con el titular de esa slide a la vista, leer la foto sola y contestar:
**¿esta imagen muestra lo que la frase afirma, o muestra justo lo que la frase niega?**

> Caso que lo originó: `c1/s-03` decía *«Nada se manda al SII sin tu OK»* y la foto mostraba
> cuatro documentos saliendo solos del notebook **ya marcados con visto bueno verde**. La imagen
> ilustraba exactamente lo que la frase negaba. Ninguna compuerta determinista lo ve —ni la va a
> ver, es semántica— y lo cazaron los dos jueces **en la Fase 7, con la pieza ya compuesta**: a
> esa altura arreglarlo cuesta regenerar + recomponer + re-juzgar. En el crudo cuesta reescribir
> una línea de prompt.

Ojo con el patrón: los titulares en negativo (*«nada se manda…», «sin que tú…», «no vas a…»*) son
los que más se contradicen con la imagen, porque el prompt se escribe describiendo la escena y la
escena natural es la afirmativa. Si el titular niega algo, la foto tiene que mostrar el **momento
anterior** (el humano decidiendo), no el resultado.

Falla que lo originó (test jul-2026): 16 fotos compuestas sin auditarlas — 8 con texto basura,
2 con el logo de Apple, 2 con anatomía imposible, pidiendo "no text, no logos". **Pedirlo no
basta: hay que mirarlo** (relato: `APRENDIZAJES.md` §5). Tope 2 reintentos por slide; al tercero
se cambia el encuadre del plan o la slide.

**Un crudo rechazado se ARCHIVA con su motivo, no se borra** (5-ago-2026):

```
/usr/local/bin/python3 templates/costo.py descartar <carpeta> raw/s-03.png \
    --por texto-inventado --nota "letras basura en la pantalla" --prompt "…"
```

Va a `raw/_descartados/s-03--texto-inventado.png` + `_motivos.json`. Borrar la foto mala destruye
la única evidencia de por qué el prompt falla; a la media hora el mismo prompt se vuelve a pedir
con otra semilla y vuelve a salir igual. **Si el mismo motivo sale 2 veces, el problema es el
PROMPT, no la semilla**: se escribe en `references/prompts-fallidos.md` ANTES de regenerar.
Motivos válidos (lista cerrada): `costo.py descartar` los lista.

**Antes de regenerar, preguntarse si hace falta otra FOTO o solo otro ENCUADRE.** Un `zoom` en el
spec cuesta 0 créditos y 0 segundos; una generación cuesta 2 créditos y ~40 s de espera. La mitad
de los "no se ve bien" del lote Marca Verde eran encuadre, no foto.

### Fase 5 — COMPOSICIÓN Y RENDER (2 min)

**Se compone con `templates/engine.py`. No se escribe un `build.py` nuevo.**
Desde el 1-ago-2026 el hook lo **pregunta**: correr cualquier `build*.py` abre una confirmación
con el recordatorio del motor único. Es pregunta y no bloqueo porque varios motores de lotes ya
entregados (`build_dolores2.py` y compañía) siguen siendo la forma correcta de re-generarlos.

```
/usr/local/bin/python3 templates/engine.py <carpeta>          # → s-NN.html + _build-report.json
/usr/local/bin/python3 templates/engine.py <carpeta> --debug  # + _map-NN.png con el mapa dibujado
```

> **Por qué existe el motor único:** había SIETE `build.py` distintos y tres no llamaban a
> `photo_map` ni una vez — renderizaban a ciegas. Relato: `APRENDIZAJES.md` §8 (31-jul-2026).

> ### ⚠️ Se toca el motor → se corre el CASO DORADO (5-ago-2026)
>
> ```
> /usr/local/bin/python3 templates/dorado.py verificar   # ANTES y DESPUÉS de tocar el motor
> /usr/local/bin/python3 templates/dorado.py fijar       # solo si el cambio es INTENCIONAL
> ```
>
> Monta un carrusel sintético de 3 slides (zoom + `<em>` + las tres zonas), lo compone, lo
> renderiza y compara **números** (`_build-report.json`) **y píxeles** (PNG a 360px) contra una
> referencia congelada. Sin fotos de cliente, sin tocar el repo de media.
>
> **Por qué existe:** el 5 de agosto el motor se tocó tres veces en un día y se rompió algo
> distinto cada vez — el destaque `<em>` rompió dos mediciones, la sincronización de
> `styles.css` borró el preset de marca de Marca Verde, el `zoom` no llegaba al render. **Las tres
> pasaron las siete compuertas en verde.** Las cazó el ojo del director creativo, horas después. Los gates
> contestan *¿está mal?*; ninguno contestaba *¿esto cambió respecto a ayer, y vos no pediste
> que cambiara?*.
>
> Las dos mitades son necesarias: el bug del zoom **no movió un solo número** (la decisión era
> correcta, no se emitía el CSS) y lo cazó solo el píxel. Aplica a `engine.py`, `styles.css`,
> `slide.html`, `textfit.py`, `photo_map.py` y `constantes.py`. `fijar` re-congela la
> referencia — es el "sí, este cambio lo pedí yo".

Las tres capas que trae adentro:

1. **Se valida el hueco** — máscara de Vision + PhotoMap antes de componer.
2. **El mapa ASIGNA** — si la zona planificada está ocupada, reubica al hueco real. Si no hay,
   el orden es fijo: **reencuadrar → angostar la columna → bajar el título hasta su piso →
   cambiar de foto. Nunca un panel opaco** (E10.b).
3. **Oclusión por máscara** — el texto se pinta y encima va el recorte de la persona, así pasa
   *por detrás* del hombro. **Tapar una cara se vuelve imposible por construcción**, no un error
   que haya que cazar (§4.5).

Cuando nada entra, el motor **no compone**: dice exactamente qué lo bloqueó y qué hacer
(ej. *«acompañada» mide 595px a 92px y la columna más angosta que deja esta foto es de 336px:
acortá el título o cambiá de foto*). Un motor que se rinde con diagnóstico es mejor que uno que
entrega la pieza rota.

Render a PNG 1080×1080 (1:1, la regla de la casa) con Chrome headless (comando abajo).

### Fase 6 — COMPUERTAS DETERMINISTAS (<1 min)

**Un comando por fase.** No se invocan los gates sueltos: `verify.py` los corre con los flags
correctos y escribe el recibo firmado.

```
/usr/local/bin/python3 templates/verify.py init       <carpeta>   # → carrusel.json + _brief.md (Fase 1)
/usr/local/bin/python3 templates/verify.py brief      <carpeta>   # → _brief-receipt.json
/usr/local/bin/python3 templates/verify.py copy       <carpeta>   # → _copy-gate-receipt.json
/usr/local/bin/python3 templates/verify.py blueprint  <carpeta>   # → _blueprint-receipt.json
/usr/local/bin/python3 templates/verify.py prompt     <carpeta>   # → _prompt-receipt.json (ANTES de generar)
/usr/local/bin/python3 templates/verify.py raw        <carpeta>   # → _raw-receipt.json  (qa_raw + qa_seam)
/usr/local/bin/python3 templates/verify.py gates      <carpeta>   # → _gates-receipt.json (typesize+geom+lint+lines+dom+pastilla+thumbs)
/usr/local/bin/python3 templates/verify.py thumbs     <carpeta>   # → _thumb-NN.png a 360px (ya incluido en gates)
/usr/local/bin/python3 templates/verify.py lote       <carpeta-madre>  # → _lote-receipt.json (ángulos + ORDEN del lote)
/usr/local/bin/python3 templates/orden_lote.py medir  <carpeta-madre>  # dónde se fue el reloj: imagen-antes-del-plan, vueltas atrás, % en lote
/usr/local/bin/python3 templates/verify.py all        <carpeta>   # todas, cortando en el primer FAIL
```

Flags (en `raw`, `gates` y `all`):
- **`--only s-03`** — re-corre SOLO esa slide y marca el recibo con `scope: ["s-03"]`. Un
  re-render de una slide ya no invalida los recibos del set entero: el hash firmado cubre
  exactamente lo que se midió.
- **`--warn-ok "razón"`** — acepta los WARNs del recibo con la razón escrita (ver E11).

`gates` corre además **`qa_dom`** (Node + Playwright, `templates/qa_dom.mjs`): valida el DOM
ya renderizado — overflow real con los px exactos y fix sugerido, colisión con el chrome fijo
(logo/pastilla CTA), piso de fuente computado de 26px (todo FAIL), gap título-contenido y
densidad por bandas (WARN, se aceptan con `--warn-ok`, nunca se ornamentan). Si falta node o
Playwright, el gate se reporta como WARN **"qa_dom no corrió: falta playwright"** — nunca un
pass silencioso, nunca fail-closed por dependencia ausente. Se instala una vez:
`cd templates && npm i playwright && npx playwright install chromium`.

> **Por qué un runner y no cinco comandos:** `qa_typesize` corrido suelto, slide por slide,
> marcó FAIL en 5 de 6 que sí cumplían (el héroe de 90px es POR CARRUSEL). Relato:
> `APRENDIZAJES.md` §6 (29-jul-2026).

> Corre con **`/usr/local/bin/python3`**: el `python3` del sistema (3.9.6) no tiene
> numpy/PIL/fontTools y los gates fallarían en silencio. `qa_raw` necesita además
> `~/bin/ocr` y `~/bin/cutout`:
> `swiftc -O -o ~/bin/ocr templates/ocr.swift` · `swiftc -O -o ~/bin/cutout templates/cutout.swift`

Cazan ~90% en segundos. **Se itera contra ellas, no contra el ojo de un agente.** FAIL = se
corrige y se re-corre; no se muestra.

### Fase 7 — DOBLE JUEZ — 🔴 NO SE CORRE (Max, 7-sep-2026)

**Apagada.** Ver «UNA PASADA» arriba: *"antes hacíamos todo esto de los jueces y blabla"*. No se
invoca `carrusel-qa`, no se escribe `_qa-receipt.json` y la puerta `open` no lo pide. El método
queda escrito acá abajo por si algún día se quiere revivir, igual que se hizo con el panel de
copy en `APRENDIZAJES.md` §35.

<details><summary>El método del doble juez, congelado</summary>

#### Fase 7 — DOBLE JUEZ (5-8 min)
Con las deterministas en verde: **dos instancias independientes** del agente `carrusel-qa` (sin
contexto compartido; el juez 2 no lee el veredicto del 1). Cada uno lee cada slide **a tamaño
completo** contra `RUBRIC.md` y contra los `ejemplos-gusto/` del cliente. **Ambos deben dar
PASS.** Recibo `_qa-receipt.json` con `"judges": 2`.

- **Los jueces leen también los thumbnails `_thumb-NN.png` (360px)** — el test de legibilidad
  móvil: si a 360px no se entiende qué domina la slide, la jerarquía falló aunque a tamaño
  completo se vea bien. Es la versión determinista del squint: el feed de Instagram se ve así.
- **Si el recibo de gates tiene `warns_sin_razon: true`, los jueces revisan esos WARNs uno por
  uno** y los cierran con veredicto escrito. Un WARN sin razón no es un pass: es una pregunta
  abierta (RUBRIC E11). Los que ya traen `warn_ok` se dan por aceptados.
- **Reportar TODO de una pasada**, no un hallazgo por ronda. Tope: 1 ronda extra — es decir
  **2 rondas de jueces**, y desde el 6-ago-2026 las cuenta `hooks/rondas.py`: la 3ª es DENY, y
  si dos rondas rechazan **por la misma causa** se para en la 2ª aunque quedara cupo.
  **Topar no congela la pieza: se entrega marcada NO APROBADO**, con el `_qa-receipt.json` en
  FAIL y lo que quedó abierto en una sola lista para el director creativo (textual suyo, 6-ago-2026: *«si el
  juez rechaza; se muestra el resultado final pero se menciona que no está aprobado»*). La causa
  de cada ronda se declara con `rondas.py causa <carpeta> jueces "…"`. (El tope aplica hoy solo a
  los jueces de diseño: el contador de rondas de copy quedó sin uso al derogarse el panel.)
- **🔴 Los jueces van SIN herramientas de escritura** (5-ago-2026). Un juez con `Write`/`Edit`/`Bash`
  deja de juzgar y se pone a reparar: edita el `carrusel.json`, corre `engine.py` y re-renderiza
  **mientras el otro juez está leyendo**. Resultado: el juez 2 dictamina sobre un build que ya no
  existe, sus hallazgos no se pueden reproducir, y nadie sabe qué cambió ni quién lo cambió.
  El juez entrega **hallazgo + corrección propuesta, en texto**; quien corrige es el orquestador,
  después de los dos veredictos. En Claude Code eso es lanzarlos con un tipo de agente de solo
  lectura (`Explore`), nunca `general-purpose`. Relato: `APRENDIZAJES.md` §15.
- **Nadie toca la carpeta mientras los jueces leen.** Ni re-render, ni `verify.py`, ni regenerar
  thumbs: el veredicto tiene que apuntar a un build congelado.
- **Los 2 jueces se lanzan en el mismo batch** (son instancias independientes; paralelizarlos es
  lo correcto). Lo que **nunca** se paraleliza es la **corrección**: se corrige un hallazgo a la
  vez y se re-mide antes de tocar el siguiente.
- **Re-render = recibos vencidos — pero POR SLIDE (3-ago-2026).** Re-renderizar UNA slide solo
  exige re-correr `verify.py gates --only s-NN` (y `raw --only s-NN` si cambió la foto) y
  re-juzgar ESA slide, no el set completo. El hook `carrusel-gate` compara fechas y bloquea
  `open` fail-closed — no se elude por vías que salten la compuerta.

</details>

### Fase 8 — ENTREGA (1 min)
El paquete es **siempre**:
- **Un PNG por slide numerado** en orden de publicación (`s-01.png`, `s-02.png`…).
- **`_TODAS-LAS-SLIDES-<carrusel>.png`** — todas juntas, en fila si son ≤6 o grilla de 3-4
  columnas si son más, etiqueta `SLIDE 01` **fuera** de la pieza, nunca encima. Es la vista con
  la que el director creativo aprueba o pide cambios sin abrir 10 archivos.
- **Caption / primary text** (apertura + punteos con emoji + cierre CTA, separados con enters).
- `_brief.md` · `_copy-gate-receipt.json` · `_qa-receipt.json`.
- Si fueron varios carruseles: **`_TODOS-LOS-CARRUSELES.png`** con las portadas, para ver de un
  golpe si dos abren con la misma imagen.

### Fase 8b — CUANDO EL DIRECTOR APRUEBA: CONGELAR (5-ago-2026)

**Su "lo apruebo" tiene que dejar un artefacto en el disco.** Hasta hoy no dejaba ninguno: los
`s-NN.png` seguían siendo los mismos archivos que el próximo `engine.py` sobrescribe.

```
/usr/local/bin/python3 templates/aprobar.py <carpeta> --por "<lo que dijo, TEXTUAL>"
/usr/local/bin/python3 templates/aprobar.py <carpeta-madre> --lote --por "…"
/usr/local/bin/python3 templates/aprobar.py <carpeta> --comparar    # ahora vs. lo aprobado
```

Copia PNGs + thumbs + spec + recibos a `aprobado/<AAAA-MM-DD-HHMM>/` y la deja en **solo
lectura**. Lo pesado (`raw/`) no se copia. `--por` es obligatorio y va con la frase textual:
un aprobado suele venir condicionado (*"los apruebo pero en c2 bajá a verde suave"*) y la
condición se pierde si se resume.

**`--comparar` es la pregunta que las siete compuertas no contestan.** Los gates miden *¿está
mal?*; esto mide *¿cambió algo que él no pidió que cambiara?* — que es como se perdió el preset
de marca de Marca Verde (§23). Correrlo después de tocar el motor, `styles.css` o el spec.

Si él aprueba con el `_qa-receipt.json` en FAIL, se congela igual y **el recibo se copia en
FAIL**: El director creativo pisa la compuerta (jerarquía #1), pero el recibo no se maquilla.

### Fase 9 — PUBLICACIÓN Y REGISTRO (opcional)
`editor-carrusel` si hace falta ajuste fino a mano, después `meta-ads`. Campos del ad: primary
text (front-load los primeros 80-125 caracteres) · headline ~40-45 · description ~27 · CTA del
enum de Meta. **Nunca pasar `degrees_of_freedom_spec`** (Meta lo deja en OPT_OUT por default).
Crear el ad **dentro del ad set existente** para heredar audiencia probada.

**Publicar no termina en Meta: se REGISTRA.** Con el `ad_id` y `adset_id` que devuelve Meta
(o los del Ads Manager, si se subió a mano):

```
/usr/local/bin/python3 templates/registrar_publicacion.py <carpeta> --ad-id X --adset-id Y [--notas "..."]
```

Escribe `_publicado.json` **al lado** del `carrusel.json` — **NUNCA dentro de él**: tocar el
spec después del QA vence todos los recibos firmados y bloquea la carpeta. Sin ese vínculo
carrusel → ad no hay forma de traer el rendimiento real de vuelta (scorer, hooks.md, cuota
creativa). Formato e inventario retroactivo: `references/publicacion-y-registro.md`.

### Fase 10 — EL RENDIMIENTO VUELVE (5-ago-2026)

`_publicado.json` decía que existía para *"traer el rendimiento real de vuelta"*, y **ese camino
de vuelta no existía**: el `ad_id` quedaba escrito y nadie lo miraba nunca. Cada carrusel nuevo
se decidía por intuición sobre ángulo, fórmula y foto real vs. generada, con los números
sentados en la cuenta de Meta.

Un script de Python no puede llamar al MCP, así que el bucle se cierra en tres pasos:

```
templates/rendimiento.py pendientes <carpeta-madre>      # 1. qué ad_ids hay que pedir
   → el AGENTE los trae con mcp__meta-ads__ads_entity_get_report
templates/rendimiento.py anotar <carpeta> --json …       # 2. guarda _rendimiento.json
templates/rendimiento.py tabla <carpeta-madre>           # 3. qué DECISIÓN gana
```

`tabla` no rankea ads: cruza el resultado contra las decisiones del spec (**imagen real vs.
generada · framework · formato · ángulo**), que es lo que sirve para el próximo carrusel.

Dos reglas del bucle: **nada bajo 1.000 impresiones entra al ranking** (se lista aparte —
ordenar por CTR con 200 impresiones es leer ruido), y **"sin registro" nunca se reporta como
"no se publicó"**: El director creativo publica a mano en Ads Manager, la ausencia de `ad_id` en disco no
dice nada de la plataforma. Toda cifra sale etiquetada con su fuente.

Con 3+ carruseles medidos, esto alimenta `references/scorer-rendimiento.md` (Fase 2) con datos
de ESTAS piezas en vez de "los últimos 90 días de la cuenta".

---

## Modo desatendido — DEGRADAR, no frenar (5-ago-2026)

Cuando el director creativo dice *"no me preguntes nada, no estaré en el computador"*, el pipeline entra en
modo desatendido. La regla es una sola y cambia el default:

> **Fail-closed sigue valiendo para PUBLICAR. Para PRODUCIR, se degrada.**

Qué pasó sin esta regla (lote Marca Verde, 4-5 ago): faltaban **4 datos de producto** y el pipeline
paró **6 de 10 carruseles en 0/7 de comprensión**. El director creativo volvió a 4 piezas y 6 carpetas
congeladas. Los 6 no estaban mal escritos: les faltaba un dato que él tenía. La compuerta hizo
lo correcto y el resultado fue el peor posible. (Esa compuerta se derogó el 10-ago-2026 — §35 —
pero la regla de degradar vale igual para cualquier otra que reprueba por falta de un dato.)

**Qué hacer con un dato de producto que falta, en desatendido:**

1. **Producir la pieza sin el claim que depende del dato.** Un carrusel de 5 slides con 4 sólidas
   y una reemplazada por un beneficio ya verificado es entregable; 0 carruseles no lo es.
2. **Marcarla `"estado": "INCOMPLETA"` en el spec** + `_FALTA.md` en la carpeta, con la pregunta
   exacta y qué slide la necesita.
3. **Seguir con el resto del lote.** Un dato faltante frena UNA slide, no diez carruseles.
4. **La puerta de PUBLICAR sigue cerrada** para una pieza `INCOMPLETA`. Se degrada la producción,
   nunca la publicación: un claim sin verificar no sale al aire por comodidad.
5. **Al volver, una sola lista.** Todas las preguntas juntas en un `LAS-PREGUNTAS.md` del lote,
   no una escalación por carpeta.

Lo que **no** se degrada nunca, ni desatendido: cifras, claims o testimonios inventados para
tapar el hueco (regla dura del cliente) · un recibo en FAIL escrito como PASS (memoria
`recibo-fail-no-se-falsea`) · el doble juez · la lectura del PNG renderizado (§4 del AGENTS.md).

**Y el presupuesto de imágenes es obligatorio en desatendido.** Sin nadie mirando, el bucle
"regenerar es más barato que pensar" corre solo: así se llegó a 255 generaciones. Se declara
antes de arrancar, para todo el lote.

---

## Camino rápido (trabajo repetido)

Si es otro carrusel de una **familia ya producida** para el mismo cliente y línea: se saltan las
Fases 0 y 1 (heredan el `_brief.md` de la familia) y el checkpoint de la Fase 3 se reduce a
mostrar solo el copy. **Nunca se saltan** las Fases 6, 7 y 8.

**Camino rápido de LOTE.** Cuando se producen varios carruseles hermanos bajo una carpeta
madre (ej. `verde-ads/carruseles-2026-08/c01…c06`): cada uno declara su **`angulo`** en el
spec y, antes de generar imágenes, se corre la **compuerta de lote**:

```
/usr/local/bin/python3 templates/verify.py lote <carpeta-madre>
```

FAIL si dos specs repiten el mismo `angulo` declarado; WARN si ≥3 títulos de portada arrancan
con las mismas 3 palabras (el chequeo barato: paráfrasis reales pasan, arranques calcados no).
Detalle: `templates/qa_lote.py` (ángulos) y `templates/orden_lote.py` (orden). Este último es
el que caza que se haya generado una imagen **antes** del brief/blueprint: FAIL, porque un plan
escrito después de la foto se escribe para justificarla (medición y relato: `APRENDIZAJES.md`
§29). Para ver el reparto del reloj sin compuerta: `orden_lote.py medir <carpeta-madre>`.

## Arquetipos de layout

Motor: `templates/styles.css` (clases `l-*` de layout, `t-*` de escala). El arquetipo se elige
por **dónde está la persona en la foto** (tabla en `composicion-y-tipografia.md` §2), rotando
para no repetir zona con la slide vecina.

⚠️ **El preset de marca va en `templates/styles.css`, NUNCA en el `styles.css` de la carpeta.**
El motor **sincroniza** la plantilla sobre `<carpeta>/styles.css` en cada corrida (para que un
arreglo del CSS llegue a todos los carruseles), así que un preset escrito a mano en la carpeta
dura hasta la próxima corrida y desaparece **sin que ninguna compuerta lo note**: le pasó a
Marca Verde el 5-ago-2026, salió con el bronce de Marca Bronce y las siete compuertas en verde
(relato: `APRENDIZAJES.md` §20). Marca nueva = un bloque `body[data-brand="<cliente>"]` en la
plantilla, junto a `navy`, `dorado` y `verde`. Para tipografías fuera de lo normal existen
`--font-kicker` (fuente del kicker y la pastilla) y `--bg-slide` (fondo distinto del scrim).

| Clave | Arquetipo | Uso |
|---|---|---|
| `l-leftmid` | Texto izquierda, centrado vertical | hooks; sujeto a la derecha |
| `l-topleft` | Kicker+título+cuerpo arriba-izquierda | foto con espacio arriba |
| `l-botright` | Bloque abajo-derecha | romper el eje izquierdo |
| `l-leftcol` | Columna izquierda + título XL | disciplina estrella / dato |
| `l-botbig` | Cierre grande abajo + CTA pill | última slide |
| `l-band` | Banda inferior con cuerpo largo | slides informativas |
| `l-block` | Bloque de color, texto invertido | 1 vez por carrusel, **elegido a propósito**. ⛔ nunca como fallback cuando el texto choca (RUBRIC E10.b) |

## QA — las 3 capas

1. **Determinista** (Fase 6) — segundos, caza el 90%.
2. **Contact sheet + squint** — `templates/qa-contact.html`: todas las slides en UNA lectura,
   más una fila en gris+blur. Si borroso no se entiende qué domina, la jerarquía falló.
3. **Tamaño completo** — cada slide con foto o pose nueva se lee entera. La miniatura ESCONDE
   los roces y el lint es ciego a "el texto tapa a la persona".

## Render

```
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
  --window-size=1080,1080 --virtual-time-budget=4000 --screenshot="s-01.png" "file://$PWD/s-01.html"
```

El `--window-size` es el del lienzo del spec: **1080×1080 por defecto (1:1)**; `1080,1350`
solo para un spec con `"canvas": "4:5"`.

**Nunca base64 en los HTML de trabajo** — inflaba cada slide a 6-7 MB ≈ 1,6M tokens y un solo
`Read` reventaba la ventana. Rutas relativas. El base64 se reserva para el artefacto portable
de entrega. Los jueces leen los **PNG**, nunca el `.html`.

## Regla de oro

"Aplicar" incluye **ver lo aplicado**. No se declara listo ni se abre al director creativo sin haber:
resuelto los FAIL deterministas, leído el contact sheet, leído a tamaño completo las slides con
foto o pose nueva, y confirmado **por escrito, slide por slide**, que la imagen elegida
REPRESENTA lo que dice el texto. Ese checklist no se asume: se ejecuta y se deja escrito.

## Cuando el director creativo corrige algo

La corrección se registra **en su fuente canónica el mismo turno**, no solo en la pieza:
regla de composición → `references/composicion-y-tipografia.md` · regla de copy → `COPY.md` ·
criterio del juez → `RUBRIC.md` · marca/cliente → `brand-brain/<cliente>/` · el relato de la
falla → `APRENDIZAJES.md`. Y si se puede hacer cumplir con un script o un hook, **se prefiere
eso sobre la prosa**. Al cerrar, decir dónde quedó registrada.
