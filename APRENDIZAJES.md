# APRENDIZAJES — historial fechado (NO es procedimiento)

> Acá vive el **por qué** de las reglas: las fallas reales, con fecha y con el fix que
> produjeron. El `SKILL.md` dice qué hacer; esto dice qué pasó cuando no se hizo.
> **Regla:** cuando una corrección se convierte en regla, la regla va al SKILL/RUBRIC y el
> relato queda acá. Nunca al revés — así el procedimiento no vuelve a inflarse.

---

## 1. Diseño y proceso

- **2026-06-09** — El lint cazó una regresión mía: oscurecí un bloque y BAJÉ el contraste de texto navy (3.9 vs 4.7). Lección: para texto oscuro sobre bloque, el bloque debe ir más **claro**. El lint ve lo que el ojo no.
- **2026-06-09** — Slide "Cool Barre" con foto de aro de pilates + bloque que amputaba el cuerpo: doble error (sujeto cortado + foto no era la disciplina). Ni el lint (mecánico) ni el squint (miniatura) lo cazan → de ahí la **regla global de integridad de imagen** revisada a tamaño full. Se resolvió generando la foto correcta con Higgsfield.
- Implementación de referencia: `marca-carruseles/marca-estudio/carruseles/disciplinas-valor/version-c-sistema/`.
- **2026-07-10** — *El copy salía estándar porque estaba solo delegado en 1 línea, sin gate.* El diseño tenía ~30 compuertas deterministas; el copy, una delegación a `copywriting-carruseles` que podía no invocarse (o hacerlo superficial) y ninguna rúbrica fallaba un hook genérico. Fix (pedido del director creativo): (1) el **método de copy completo se embebió acá en `COPY.md`** (Regla #1 anti-IA + 7 pasos + hooks problema-primero + primary text + compuerta de comprensión + checklist); el paso 2 del pipeline lo aplica SIEMPRE, sin depender de invocar la otra skill; (2) se agregó la sección **`D-CALIDAD` a `RUBRIC.md`** que FALLA copy genérico/AI-sounding (hook del montón, sin deseo/VoC, triadas, párrafo corrido…) + juez de distintividad. Ahora la calidad del copy se hace CUMPLIR, no queda a criterio. `copywriting-carruseles` sigue como espejo con el mismo contenido.

---

## 2. Copy

- **2026-06-09** — *Carruseles informativos = datos REALES investigados, no inventados ni clichés.* Para "¿Conoces el X?" / tips / curiosidades: investigar en internet info ya creada (artículos, estudios, posts/carruseles de Instagram efectivos) y traer datos verificados; copiar el enfoque de un carrusel que ya funciona. Cada slide un dato interesante real (ej. Poundfit: "nació de un banquito roto", "baquetas verdes a propósito porque el cerebro atiende más al verde", "15.000 golpes por clase"), NO frases-beneficio genéricas ("el ritmo te desconecta"). Cero cifras/claims inventados. Es parte del procedimiento, no opcional.
- **2026-06-09** — *El dato hay que EXPLICARLO, no dejarlo críptico.* Un titular-dato suelto no se entiende ("Tu linfa no tiene bomba", "Hasta 3x tu peso", "68% más eficiente que correr" → ¿qué significa?). Cada slide informativa necesita una **línea de cuerpo que explique el dato en simple** para que cualquiera lo entienda (qué es la linfa y por qué importa moverse; qué se gana con el 87% de impacto absorbido; a qué se refiere "más eficiente"). Si el dato necesita más texto, usar el arquetipo **`l-band`** (listón inferior con room para texto explicativo). Mejor "informar claro" que "punchy pero incomprensible".
- **2026-06-09** — *Comprimir, no explicar (redacción).* el director creativo corrigió "Fuerza que notas fuera de la clase, no solo dentro" → **"Fuerza para el día a día"**. Mi error: describir literal con muletillas en vez de dejar la frase que se queda. Regla en paso 7: cortar calificadores, preferir sustantivo+imagen concreta. Tener el concepto correcto NO basta; hay que saber redactarlo corto y con punch.
- **2026-06-09** — *Copy "competente pero plano".* el director creativo rechazó los textos del carrusel Marca Crema: cumplían especificidad y problema-primero, pero les faltaba **deseo emocional (LF8)** y **palabras de la clienta (VoC)** — sonaban a "buen copy de marca", no a algo que pega. → de ahí el **método de profundidad de 7 pasos** (arriba). Ejemplo de reescritura: "Quieres soltar la cabeza / Subes pulsaciones, baja el estrés" → "Para dejar el día afuera / Entras con la cabeza llena. Sales liviana. Y se te pasó la hora." En `marca-carruseles/marca-estudio/carruseles/disciplinas-valor/version-c-sistema/`.
- **2026-06-02** — *No sonar a IA es la prioridad #1.* el director creativo rechazó una estructura por "se siente muy IA" (triadas, "no eres tú es que…", lenguaje de transformación). → Regla #1 arriba.
- **2026-06-02** — *Investigar antes de asumir.* Asumí que Marca Crema era pilates; es **home workout / plataforma de entrenamiento online** (metodología propia "Fitnovation", clases en vivo + on-demand, +500 clases, +10.000 mujeres, app, recetas, planes mensual/anual con registro gratis). Siempre validar el producto en la web real primero.
- **2026-06-02** — *Carrusel = mid-funnel.* Confirmar etapa de público; para frío sugerir otro formato.
- **2026-06-05** — *Verificar visualmente el render antes de aprobar copy nuevo en una slide existente.* Cuando el director creativo pide cambiar el texto de una slide (cualquier cliente, no solo carrusel — también portadas), el ciclo OBLIGATORIO antes de declarar "listo" o pasar a publicar:
  1. Editar el copy en el render (HTML o Nano Banana, según el flujo del cliente).
  2. Ejecutar el render.
  3. **Yo mismo leer el PNG resultante con la `Read` tool** (Claude lo procesa como imagen multimodal).
  4. Auditar la composición como diseñador: jerarquía, espacio negativo, balance arriba/abajo, líneas que se rompen mal, texto sobre productos, tamaños inconsistentes entre titulares paralelos.
  5. Iterar el CSS hasta que la composición esté limpia, **antes** de abrir al usuario o subir a Meta.
  6. Recién ahí mostrar la versión final.
  Razón: El director creativo detectó dos veces seguidas problemas obvios (titulares de distinto número de líneas, texto saliéndose del slide, "y extendimos" tapado por el laptop) que yo no había revisado porque le abrí el render sin auditarlo primero. La memoria `feedback_imagenes_abrir_no_revisar` aplica cuando el render YA fue iterado/aprobado; mientras estás iterando, sí debes mirarlo tú.
- **2026-06-02** — *Producción visual de carruseles tutorial de Marca Crema (cómo le gusta al director creativo):*
  - El **texto va integrado en la imagen con Nano Banana Pro** (`nano_banana_pro`), NO en HTML. El HTML/los mockups solo sirven de guion previo.
  - Estética: **tarjetas y texto translúcidos tipo vidrio esmerilado (glassmorphism)**, nunca texto plano sobre bloques sólidos.
  - **Mujer realista** haciendo el ejercicio (foto, no ilustración), estilo **limpio/editorial** igual a las referencias de Higgsfield (hueso/crema + vino, Playfair, luz natural, casa minimalista).
  - Generar **con imagen de referencia** para mantener mujer/vestuario/ambiente; pedir explícito NO copiar textos/botones de la referencia.
  - Formato carrusel niveles: 1 nivel por slide (Nivel 1→4, progresión fácil→difícil), tarjeta translúcida con eyebrow "NIVEL X", nombre del ejercicio y 2-3 tips de postura cortos.
  - 1:1, validar params del modelo y saldo antes de disparar.

---

## 3. Generación de imagen (Higgsfield) — lecciones de producción

1. **Higgsfield reinventa packaging** — probado: ni con `social_carousel` ni con `marketing_studio_image` ni con producto registrado por URL. Solución: foto real OR `nano_banana_2` con prompt explícito + referencia, pero validar siempre. Si el packaging es crítico → no usar IA.
2. **Filtro NSFW del `product-photoshoot lifestyle_scene` es agresivo** — frase "mujer 28-35" lo dispara. Solución: prompt en inglés neutro O saltar a `nano_banana_2` directo (más permisivo).
3. **OneDrive y enlaces autenticados** no se pueden bajar por API. Pedir al usuario que descargue y deje en `~/Downloads`.
4. **Drive MCP no puede subir archivos grandes** — base64 cae sobre límites del Read tool. Solución: crear carpetas en Drive y dejar que el usuario arrastre desde Finder.
5. **OG image text con gradient SVG no alinea bien** con texto plano → usar CSS `background-clip: text` (probado, perfecto alineamiento).
6. **El scrim negro arruina fotos claras** del salón. Siempre cream scrim.

---

## 4. Diagnóstico del proceso v2 (7-jul-2026)

Origen: feedback del director creativo tras el piloto "Reloj y ciclo" (Marca Crema): *"te estás demorando
+40 minutos en un carrusel; creo que algo se rompió en la validación de jueces; no sé si seguir
con HTML o irnos a nano-banana; quiero re-armar el proceso completo y blindado"*.

---

## 1. Diagnóstico del piloto (con números reales)

Tiempo total ≈ 45-50 min. Desglose:

| Fase | Tiempo | ¿Problema? |
|---|---|---|
| Generación de imágenes (6 gens Higgsfield) | ~9 min | No (paralelo posible) |
| Copy + panel de comprensión (2 rondas × 3 lectoras) | ~6 min | No — cazó 5 problemas reales |
| Colocar texto en HTML + render + lint | ~2 min | **No — esto es rápido** |
| **Jueces de diseño: 4 rondas × 2 jueces (3-13 min c/u)** | **~30 min** | **SÍ — el cuello de botella** |

Por qué los jueces se comieron 30 min:
1. **Hallazgos incrementales:** cada ronda encontró UN problema nuevo (texto sobre reloj → tamaños
   de fuente → corona rosada → huérfanas → roce con la malla) en vez de reportar TODO en una pasada.
2. **Ruido/contradicción:** el juez 1 afirmó "corona rosada real" y el juez 2 (ronda siguiente)
   la desmintió ("reflejo ambiental"). Yo la medí con numpy en 5 segundos y fue concluyente.
3. **Regla amplificadora del skill:** "cualquier re-render invalida recibos → re-juzgar TODO con
   2 jueces" = loop sin tope. 1 palabra huérfana costaba una ronda completa de 10 min.

**Dato clave:** el 100% de lo que cazaron los jueces en 4 rondas era chequeable por código:
tamaños de fuente (DOM), huérfanas (line boxes), frase enfatizada partida (DOM), texto tocando
el objeto (intersección máscara-texto vs bordes), logo saltando de posición (DOM), paginador
ausente (DOM), deriva de color de la corona (muestreo RGB). **Nada de eso necesitaba un LLM.**

## 2. Decisión: ¿texto en HTML o texto nano-banana?

**Recomendación: HTML para el texto de ADS. Nano-banana solo para las escenas.**

| Criterio | HTML overlay | Texto nano-banana |
|---|---|---|
| Tipografía de marca | Exacta (Montserrat real, px exactos, gradiente exacto) | Aproximada, deriva entre slides |
| Consistencia 36 slides (9 carruseles × 4) | Garantizada por código | No garantizable |
| Corregir un texto | Segundos, gratis | Regenerar imagen: créditos + la escena cambia |
| Typos/idioma | Imposible | Real: HOY escribió "CYCLE-PHASE" en inglés sin pedirlo |
| Edición manual posterior (editor-carrusel) | Sí | No |
| Velocidad | Segundos | ~1.5 min por intento |

El HTML NO era el problema de los 40 min (2 min del total). El loop de jueces sí.
*Opcional:* test A/B de 1 slide con texto nano para decidir con evidencia (1-2 créditos).

## 3. Pipeline v2 (blindado)

> ⚠️ **Tabla histórica (jul-2026), no el pipeline de hoy.** La fase 3 «Compuerta de comprensión»
> quedó **derogada el 10-ago-2026** (§35) y el paginador de la fase 5 está prohibido desde el
> 29-jul-2026. El pipeline vigente está en `SKILL.md`.

| # | Fase | Quién | Qué hace | Tiempo |
|---|---|---|---|---|
| 0 | **Investigación** | **AGENTE `carrusel-researcher`** (nuevo) | Metodología del director creativo: buscar carruseles PROBADOS en nichos adyacentes (inglés, marcas personales > empresas), extraer la ESTRUCTURA (patrón de hook, arco narrativo, nº slides) y definir el "punto de conexión" con nuestro producto. Herramientas: WebSearch + Meta Ads Library (`ads_library_search`). Output: 2-3 estructuras probadas + conexión. Se corre 1 vez por FAMILIA de carruseles, no por carrusel. | 3-5 min |
| 1 | **Brief** | Skill (main thread) | Cliente/línea + brand brain (tipografías, colores, estilo) + oferta/CTA + estructura elegida. `_brief.md`. | 1 min |
| 2 | **Copy + brief de imagen** | **AGENTE copywriter** (con brand brain inyectado) | UNA misma cabeza escribe: copy por slide (adaptando la estructura probada) + qué muestra la imagen de cada slide + dónde va el texto (blueprint). Reglas anti-"texto sin sentido": decir QUÉ es el producto en slide 1, cero jerga, títulos que un humano entiende a la primera, reverse brief. | 2-3 min |
| 3 | **Compuerta de comprensión** | 3 AGENTES `copy-qa` en paralelo, **UNA ronda** | Lectores ciegos del público real. Esto resuelve "la gente no entiende el anuncio" — en el piloto cazó 5 problemas antes de diseñar. | 2-3 min |
| 4 | **Imágenes** | Higgsfield (nano-banana) | Gancho aprobado → slides 2-3 por **image-to-image** (consistencia validada: mismo reloj/device). Composición device-en-un-tercio según blueprint. Gens en paralelo. | 3-6 min |
| 5 | **Texto** | Motor HTML (script) | Overlay tipografía de marca + logo top-center + paginador. | 1 min |
| 6 | **QA determinista** | **`qa_lint` v2** (script) | TODO lo mecánico en segundos: contraste, márgenes, texto-en-zona-limpia, **+ nuevos:** tamaños mínimos (aunque sea font-size inline), huérfanas, frase enfatizada partida, gap texto↔objeto, logo consistente, paginador, deriva de color del device (RGB). FAIL = fix inmediato + re-lint (segundos). | <1 min |
| 7 | **QA semántico** | 2 AGENTES `carrusel-qa` en paralelo, **UNA ronda** | SOLO lo que el código no puede juzgar: ¿la imagen co-comunica? ¿se ve premium? ¿algo uncanny? Instrucción: reportar TODO de una vez, solo bloqueantes que un espectador real notaría. Fixes se verifican con lint + lectura propia a tamaño completo. **Tope: 1 ronda extra máx.** | 5-8 min |
| 8 | **Entrega** | Main thread | Contact sheet + open al director creativo. | 1 min |

**Tiempo objetivo: ~15-20 min el primer carrusel de una familia; ~10-12 min los siguientes**
(fase 0 y 1 se amortizan). Los 8 carruseles de funcionalidades restantes: en paralelo vía
workflow ≈ 1 hora total de pared.

## 4. Regla simple: qué es skill, qué es agente, qué es script

- **Skill** = el conocimiento del proceso (este pipeline, arquetipos, reglas de marca). Lo que
  debe ser IGUAL siempre. No ejecuta: instruye.
- **Agente** = trabajo que necesita ojos frescos/independientes o paralelismo: investigador,
  lectores ciegos, jueces semánticos, copywriter con contexto limpio.
- **Script (determinista)** = todo lo medible: lint v2, render, contact sheet, muestreo RGB.
  *La IA razona, lo determinista hace cumplir.* Un juez LLM jamás debe volver a medir un font-size.

## 5. Qué se implementa (al OK del director creativo)

1. **`qa_lint.py` v2** — codificar los 7 chequeos nuevos (el trabajo más importante).
2. **Reescribir la sección QA de el SKILL de la skill de diseño de entonces** — jueces: 1 ronda, todo de una
   vez, solo semántica; re-render NO re-gatilla jueces si el fix fue mecánico y el lint pasa
   (solo re-lectura propia a tamaño completo); tope 1 ronda extra.
3. **Crear `.claude/Agents/carrusel-researcher.md`** — la metodología de investigación del director creativo.
4. **Actualizar `copywriting-carruseles/SKILL.md`** — copy + brief de imagen salen de la misma
   cabeza; reglas de títulos inteligentes (ya registradas hoy).
5. **Hook `carrusel-gate`** — aceptar el recibo v2 (lint v2 + 1 ronda de jueces).

---
## 🔴 FALLA CRÍTICA detectada (7-jul-2026): el investigador FABRICÓ su evidencia
Auditoría del director creativo al piloto Estudio: el agente investigador (Fase 0) citó nombres de gimnasios,
frases exactas de hooks y 3 snapshot URLs de Ads Library como "prueba" de carruseles que funcionaban.
Verificados contra la Ads Library real (4 búsquedas) + los URLs: **NINGUNO existe**. El LLM alucinó
evidencia plausible. Lo único real era consejo genérico de un blog (no un carrusel replicable).

Reglas duras que quedan (enforce en la Fase 0):
1. **CERO citas sin fuente en la respuesta del tool.** El investigador solo puede citar un ad si el
   `ad_snapshot_url` y el `page_name` vienen LITERALES de un resultado de `ads_library_search` de ESA
   corrida. Prohibido "recordar" o construir IDs/nombres/quotes.
2. **Verificación obligatoria antes de confiar:** el orquestador re-chequea 2-3 links citados con
   `ads_library_search`/WebFetch. Si no resuelven → se descarta TODA la investigación y se rehace.
3. **La Ads Library está inundada de spam de novelas** ("Must read novels", "Reading-time", "Romantic
   Lover") → la búsqueda por keyword genérica NO sirve para fitness. Mejor: buscar por page_ids de
   cuentas reales de competidores/estudios, o que el director creativo dé las cuentas de referencia que él confía.
4. **No presentar como "replicamos un carrusel probado" si solo hay marco genérico.** Ser explícito:
   "esto es un ángulo estándar" vs "esto está modelado en tal carrusel real (link verificado)".
Nunca más pasar evidencia de un subagente sin verificarla. Aprendizaje transversal → memoria.


---

## 5. Test de ads Claude Code (29-jul-2026) — 3 carruseles spec, 32 generaciones

Prueba de la skill de punta a punta sin brand-brain. Veredicto: **FAIL en los tres**, por
unanimidad de dos jueces independientes. Lo que enseñó:

**La capa de texto funciona; la capa de imagen no.** `qa_typesize` y `qa_geom` pasaron 18/18,
las zonas rotaron sin repetir, el velo adaptativo dio 0.14-0.25 (ninguna foto sepultada) y
cero repetición de imágenes. Lo que se cayó fue todo lo que entra por la foto.

**Pedirle a la IA que no escriba texto no funciona.** 16 prompts decían "no text, no logos" y
8 de 14 fotos volvieron con letras inventadas. Al pedir "completely out of focus" la pantalla
volvió llena de dígitos nítidos. Lo que funcionó fue **quitarle la superficie**: macro extremo,
cuaderno cerrado, pantalla fuera de cuadro. → regla `produccion-imagenes.md` §0.1 + RUBRIC A11.

**Nadie miraba el crudo.** Se componía directo sobre la foto recién generada; el desastre
aparecía recién en el doble juez, con la pieza ya armada. → Fase 4b del pipeline.

**El ciclo de regeneración no converge solo.** 32 generaciones y 3 slides nunca pasaron: cada
reintento cambiaba un problema por otro (texto basura → logo de Apple en la espalda del monitor
→ costura visible → anatomía imposible). → tope de 2 reintentos por slide.

**Dos mediciones estaban mal planteadas.** (a) El velo medía el percentil 80 del BLOQUE: una
línea sobre una pantalla encendida quedó en 1.4:1 con el bloque en verde. (b) Los `<br>` del
spec no impedían el re-wrap del navegador: 3 líneas salieron 5, con huérfanas, en 10 de 18
slides — y `textfit.py`/`montwidth.py` existían para eso y el builder no los usaba.

**`qa_typesize.py` era ciego al CSS enlazado.** Daba FAIL falso ("ningún héroe") cuando la
escala vivía en un `<link rel=stylesheet>` — y habría dado **PASS falso** con texto de 12px ahí.
Parcheado: ahora sigue los `<link>` locales.

**La compuerta de copy no tenía tope** y el panel estaba mal calibrado: dos rondas completas sin
una sola imagen, con la mediana hundida por un lector que no era del público objetivo. → tope de
2 rondas + la mediana se calcula sobre el segmento declarado en el brief.

**Hay claims que no se resuelven escribiendo.** Los tres lectores leyeron "vive en tu repo" como
retención de código. La salida correcta no era inventar una promesa de privacidad: era quitar la
ambigüedad y escalar la línea al cliente.

**Decisión de método:** el texto va en HTML, no horneado por la IA — ningún modelo reproduce una
tipografía específica y la legibilidad del texto horneado no se puede medir ni corregir. La única
ventaja del horneado (integrarse a la escena) se recupera en HTML **usando la máscara del sujeto
para que el texto pase por detrás** (`composicion-y-tipografia.md` §4.5).

---

## 6. El gate correcto, corrido mal (29-jul-2026 · Marca Verde c67)

Verifiqué el primer carrusel de Marca Verde corriendo `qa_typesize.py` **en un bucle, slide por
slide**. Marcó FAIL en 5 de 6. Mi primera conclusión fue "el script es más estricto que la
norma" — y era falsa: el script acumula el máximo entre **todos los archivos de una misma
invocación**, justamente porque el héroe de 90px es por carrusel. Con las 6 juntas: PASS, héroe
de 96px en la portada.

Dos lecciones:
1. **Antes de declarar roto un gate, leerlo.** Un FAIL inesperado es más veces mal uso que un bug.
   Acusar a la herramienta lleva a "arreglarla" bajando el estándar, que es el peor final posible.
2. **Un gate que se puede usar mal en silencio está incompleto.** El fix no fue tocar el umbral:
   fue que el propio gate detecte la corrida de a una y lo diga ("el héroe es por carrusel, pasale
   todas las slides"), más un `--slide` explícito para cuando de verdad quieres una sola. La
   documentación del comando en `SKILL.md` y en `composicion-y-tipografia.md` §8 ahora muestra el
   uso correcto con `s-*.html`.

---

## 7. Lote Marca Verde de 6 carruseles (29-jul-2026): FAIL unánime por DOS bugs de motor

Dos jueces independientes reprobaron los 6 (34 slides). No fueron 34 errores distintos: fueron
**dos defectos del motor**, más un vicio de prompt. Los tres se arreglan una vez.

**Bug 1 · La zona de texto se elegía por "la banda menos ocupada", sin TECHO absoluto.**
El motor medía la ocupación de cada banda y tomaba la menor — pero la menor puede tener 30%. En
`c75` cayó texto sobre el objeto clave en **4 de 6 slides** (bottom con 33,7% y 43,9% de ocupación
medida y elegida igual), y en `c64-s4` el titular quedó sobre el calendario, que era el objeto del
que hablaba la slide. Fix: **umbral duro** — si la banda más limpia supera ~12%, no se compone: se
reencuadra el prop o se regenera la escena. Un mínimo relativo no es un criterio de calidad.

**Bug 2 · El scrim se pintaba ENCIMA de la mascota compuesta.**
la mascota se pegaba dentro del PNG de la escena y el velo HTML iba sobre la foto completa: en toda
slide donde la mascota caía en la banda de texto, **perdía el lima de marca**. Medido por los dos
jueces: cara en (114,145,14) contra (195,233,11) en la misma pieza — el personaje de marca cambiando
de color entre slides. Fix: la mascota va como **capa HTML propia por encima del scrim**, no
horneada en la escena.

**Vicio de prompt · "the whole LOWER HALF is empty negative space" produce una COSTURA.**
En 10 de 34 fondos apareció una línea dura horizontal en la mitad exacta del cuadro (salto de
luminancia medido 60 contra un ruido de 3,7), con los props rebanados. Es el mismo error que
`produccion-imagenes.md` §2.3 ya documentaba para el eje vertical — pedir "la mitad vacía" hace que
el modelo entregue dos imágenes pegadas. Hay que pedir **caída gradual del glow**, nunca una mitad.

**Y una compuerta ciega:** `qa_seam.py` solo escanea COLUMNAS, así que no vio ninguna de las 10
costuras horizontales. Un gate que mide un solo eje da PASS falso en el otro.

---

## 8. Auditoría completa de la skill (31-jul-2026): las reglas estaban, la ejecución no

El director creativo: *"pone los textos muy mal, se superponen a la imagen, no sé qué hacer"* y *"los copy no
salen muy buenos"*. Auditando la skill entera —incluido el `_archive/`— la conclusión fue que
**casi ninguna de las dos cosas era un problema de reglas faltantes**. Estaban todas escritas.
Lo que faltaba era que algo las ejecutara.

**El juez de diseño apuntaba a archivos que no existen.** `carrusel-qa.md` mandaba leer
`skills/diseno-carruseles/RUBRIC.md` (archivada, 91 líneas, sin A8-A13 ni E10 — y **exigiendo
paginador**, hoy prohibido) y correr `marca-carruseles/_qa_lint.py`, que no existe. El juez del
que cuelga todo el QA quedó huérfano al consolidar las skills, y nadie lo notó porque igual
devolvía veredictos.

**Tres de los siete motores no llamaban a `photo_map` ni una vez.** `test-cc-ads-claude/build.py`
—el del lote que reprobó por unanimidad— toma la zona que declara el spec, le pone el velo y
renderiza **a ciegas**. Lo único que chequea es que dos vecinas no compartan zona, que es ritmo,
no personas. De ahí que el texto sobre la cara aparezca en unos trabajos y en otros no: depende
de con qué copia del motor se armó. → `templates/engine.py`, motor único.

**`qa_lint.py` nunca devolvía código de salida.** Imprimía `❌ HAY FAILS` con contrastes de 3.1:1
y el proceso salía 0. Cualquier automatización que mirara el exit code recibía un PASS falso.
Lo cazó `verify.py` al integrarlo. Un gate que falla en la salida pero sale 0 es peor que no
tener gate.

**La única compuerta de copy que se hacía cumplir medía comprensión, no calidad.** Un copy plano
y olvidable pasa el panel de lectores ciegos con nota perfecta: los tres lo entienden. DC1-DC7
existía, pero la juzgaba el juez de DISEÑO al final, sobre PNG ya compuestos — o sea después de
gastar todas las generaciones. → `qa_copy.py` (lo mecánico, en segundos) + agente
`copy-craft-qa` (deseo, VoC, distintividad), los dos ANTES de generar.

**No existe banco de voz de la clienta en ningún brand-brain — y se decidió que NO hace falta.**
*(Cierre del 31-jul-2026: El director creativo descartó construir un banco por cliente. La vía por defecto es
la escena concreta; la frase textual es un atajo opcional cuando ya está a mano. DC3 acepta
"palabra O escena", así que ninguna compuerta lo exige. Lo que sigue es el diagnóstico original,
que llevó a esa decisión.)*

`COPY.md` declara la VoC *"EL
antídoto al copy-IA"* y DC3 falla el copy que no la use — sin fuente de donde sacarla. El director creativo
objetó, con razón, que no es un bloqueador: el método ya trae el fallback (*"si no hay
testimonios, escribir escenas concretas en SU registro"*) y DC3 acepta **palabra O escena**. Y el
ejemplo que él aprobó ("Y se te pasó la hora") no parece VoC literal sino escena bien escrita.
Queda como insumo deseable, no obligatorio: para negocios físicos las palabras son públicas
(reseñas de Google, comentarios de IG).

**Los formatos no se elegían por evidencia.** El menú tiene ~55 formatos y la elección era un
paso mental; todo salía "educativo por defecto" y un lote de 6 abría seis veces igual. La
evidencia ya estaba en el brand-brain sin que nadie la leyera: `audience.md` de Estudio dice
*"responden a ofertas de TIEMPO por sobre % de descuento"* y *"no comparten promos de %"*. →
`brand-brain/<cliente>/formatos.md` + `plan_lote.py`.

### Lo que se calibró midiendo, no opinando

- **`qa_seam` en dos ejes**, con dos tramos. Un solo umbral en 0.55 bloqueaba
  `clase-cami-yoga-2.jpg`, que es una foto REAL de la sede: su columna blanca va de piso a techo
  y da persistencia 0.74. Separación limpia contra 12 imágenes etiquetadas: **FAIL >0.85**
  (los 3 collages confirmados dieron 0.99/0.99/0.92, ninguna foto real pasó de 0.74), **WARN
  >0.55**. Un gate que bloquea fotos buenas se termina desactivando.
- **El salto de luminancia NO discrimina** y se descartó como criterio. El aprendizaje Marca Verde
  citaba "60 contra 3,7", pero sobre el set etiquetado la foto real del yoga da 47,1 y dos
  collages confirmados dan 14,2 y 11,6. Se sigue midiendo e informando; no decide.
- **Se ignora el 8% exterior** al buscar costuras: un salto en el borde es un marco, no un
  collage — en una franja del 3% no cabe una segunda imagen.

### Lo que enseñó probar el motor sobre fotos reales

Con un plan deliberadamente equivocado (texto al centro, sobre la persona), el motor reubicó
solo. Pero la primera pieza salió con "acompañada" metida detrás de una pierna: **la oclusión
funcionó** —se ve el corte siguiendo el contorno de la cadera— **y aun así la pieza estaba mal.**
Dos lecciones:

1. **La oclusión hace imposible tapar una cara; no hace bueno el layout.** Una palabra escondida
   detrás de una pierna es ilegible igual.
2. **La caja que se valida tiene que ser la que el texto ocupa DE VERDAD.** Una palabra sola más
   larga que la columna no se puede quebrar: `textfit` la devuelve entera y el bloque se sale de
   la caja que MAPCHECK aprobó. Ahora el motor mide el ancho real de cada línea, baja el título
   de a 6px hasta su piso, y si ni así entra **no compone**: informa que el problema es el COPY
   (con los px exactos) y no la foto. Diagnóstico accionable en vez de pieza rota.

Corolario del proxy: medir con Arial cuando el render usa Oswald/Montserrat **sigue siendo la
falla más silenciosa del sistema**. Declarar `tipografia.font` en `carrusel.json`.

---

## 9. La piedra angular que nadie ponía (1-ago-2026)

El director creativo: *"estoy armando una skill de carruseles, pero no funciona muy bien"*. La skill estaba
sana: los 17 scripts compilaban, `~/bin/ocr` y `~/bin/cutout` compilados, numpy/PIL/fontTools
presentes, Chrome instalado, los hooks cableados en `settings.json`. No fallaba nada de eso.

**Faltaba un eslabón.** `carrusel.json` es la piedra angular real —lo abren `engine.py:530`, las
5 fases de `verify.py` y las 4 puertas de `carrusel-gate.py`— pero **ninguna fase del pipeline
mandaba a escribirlo**. Aparecía 2 veces en el `SKILL.md`: en la línea de "adopción incremental"
y en el título de su propia sección. La Fase 1 pedía `_brief.md` en prosa; la Fase 5 mandaba
correr el motor, que abre el spec y revienta si no está.

La cascada, tal como ocurría: el agente escribe el `_brief.md` → llega a la Fase 5 → `engine.py`
tira `FileNotFoundError` → lo interpreta como *"el motor no aplica a este trabajo"* → **se
escribe su propio `build.py`** → y como sin spec `opt_in()` daba la carpeta por no adoptada,
ninguna compuerta se enteraba. La calidad volvía a depender de que el modelo se acordara, que es
exactamente lo que las compuertas existen para evitar.

El conteo sobre el disco, que es lo que cerró el diagnóstico:

| | |
|---|---|
| Carpetas-carrusel | 81 |
| …con `carrusel.json` | **2** — y las dos eran `_test-html-vs-nano` |
| `build*.py` sueltos (fuera del venv) | **10** |

Es la misma falla de los "SIETE `build.py`" del §7. El motor único la resolvió en el papel pero
la dejó detrás de una puerta cuya llave nadie fabricaba: no se resolvió, se movió de lugar.

**Los tres arreglos:**

1. **`verify.py init <carpeta>`** — genera el andamio (`carrusel.json` + plantilla de
   `_brief.md`), detecta la `.woff2` cercana para que `tipografia.font` no quede vacío, y es
   ahora el primer comando de la Fase 1. Los campos obligatorios salen **vacíos a propósito**:
   un esqueleto que pasara `verify.py brief` con relleno convertiría la compuerta en trámite.
2. **Muerte de `opt_in()`** — falta el spec = problema con instrucción, no pase libre. El escape
   sigue existiendo pero es explícito: `.claude/.carruseles-legacy`, una ruta por línea, con las
   101 carpetas ya entregadas congeladas. La diferencia no es el efecto, es quién decide: antes
   la carpeta se daba el bypass a sí misma por omisión y en silencio.
3. **Aviso de motor paralelo** — correr cualquier `build*.py` abre una confirmación. `ask` y no
   `deny` porque varios de esos motores son de lotes entregados y siguen siendo la forma correcta
   de re-generarlos; bloquear de plano rompía trabajo que anda.

**La lección de método, que es la que vale para la próxima:** la primera versión del arreglo
ensanchaba `is_carousel()` para que `_brief.md` contara como señal de carrusel — necesario,
porque en Fase 4 todavía no hay slides renderizadas y la puerta GENERAR (la que cuida la
billetera) no podía disparar nunca. Correr las dos versiones del hook sobre las 83 carpetas del
disco y **diffear decisión por decisión** mostró 11 carpetas ya entregadas que pasaban de ALLOW
a DENY. Se acotó el criterio a trabajo no-congelado y el diff volvió a 0 sobre 164 decisiones.

> Un gate nuevo se mide contra el trabajo que ya existe, no solo contra el caso que lo motivó.
> Si rompe lo entregado, se desactiva a la semana — y entonces no protege de nada. Que es,
> literalmente, cómo había nacido `opt_in()`.

---

## 10. Robar con criterio: el experimento comparativo Marca Verde (3-ago-2026)

Se corrió el mismo brief de Marca Verde contra dos skills externas con estrellas
(`verde-comparativa-skills/_COMPARATIVA.md`): **guizang-social-card-skill** (5.7k★) y
**charlie947/social-media-skills** (2.1k★). El veredicto confirmó a esta skill como la única
end-to-end publicable — pero las dos externas ganaban cada una en algo, y esas dos cosas se
importaron:

- **De guizang: validar sobre el DOM renderizado, no solo sobre píxeles.** Su validador midió
  el layout real y pilló un error que pasó limpio acá. Atención: **ese validador es AGPL — se
  REIMPLEMENTÓ desde cero** como `templates/qa_dom.mjs` (Node + Playwright), sin copiar código:
  overflow real con los px y el fix, colisión con el chrome fijo, piso de fuente computado de
  26px (FAIL), gap título-contenido y densidad por bandas (WARN). Lo que NO se importó: su
  formato 3:4 (no entra a Meta 1:1) y sus 10 temas cerrados (quedó "otro cliente" en el test).
- **De charlie947: puntuar el copy contra rendimiento real.** Su scorer de hooks era buena idea
  con mala dependencia (Apify): sin API key degradaba a checklist genérico (35/50 en el test).
  Versión agencia en `references/scorer-rendimiento.md`: el top de ads reales de la cuenta vía
  `meta-ads` (90 días, CTR/CPA/gasto) → qué estructuras de hook ganan → el copy nuevo se evalúa
  contra eso. Procedimiento para el agente, sin script nuevo, paso POR DEFECTO de la Fase 2
  (era opcional y por eso nunca corría; corregido el 3-ago-2026 — ver §11 M4).
- **Y la lección inversa, que es la más importante:** su fórmula base de hooks exige marcas y
  cifras — **prohibidas en Marca Verde: 2 de 6 hooks salieron inutilizables**. De ahí el filtro de
  compliance de `COPY.md`: todo framework externo pasa primero por las reglas rojas del
  cliente; la fórmula se adapta al filtro, nunca al revés.

El experimento también dejó tres cambios estructurales propios:

1. **WARN aceptado con razón escrita.** Los recibos eran binarios y los WARN no dejaban rastro.
   Ahora `status: PASS_CON_WARNS` + `--warn-ok "razón"` en `verify.py` (RUBRIC E11). Con la
   doctrina anti-ornamento (E11.b): las métricas de densidad se satisfacen con contenido real,
   nunca decorando — decorar para que el script dé verde es la falla que el script previene.
2. **Thumbnails 360px** (`verify.py thumbs`, con `sips`, cero dependencias): los jueces de la
   Fase 7 leen la slide como se ve en el feed, no solo a 1080px.
3. **Re-verificación por slide** (`--only s-03`): antes cualquier re-render invalidaba los
   recibos del set entero; ahora el scope queda marcado en el recibo y solo se re-juzga esa
   slide. El hash firmado ya cubría lo medido — la granularidad era artificial.

> La forma de robar importa tanto como lo robado: reimplementar lo que tiene licencia
> incompatible, adaptar lo que choca con compliance, y convertir en script lo que la otra
> skill dejaba en prosa. Robar la idea, no el texto.

---

## 11. Auditoría 46-agentes (rev. 2 el director creativo): oleada 1 aplicada (2026-08-03)

Auditoría del cerebro corregida por el director creativo. Esta entrada registra SOLO el frente de
agentes + docs + brand-brains; los frentes de hooks y gates los registran otros.

**Agentes (`.claude/agents/`)**
- **C8** — `copy-qa.md`: el panel de lectores ciegos tenía `Bash, Grep, Glob` (podía
  "des-cegarse" investigando). Quedó `tools: Read, Write`.
- **F5** — `copy-qa.md`: no declaraba modelo → el panel heredaba el más caro. Quedó
  `model: sonnet`, como los otros agentes de QA.
- **C10** — `copy-qa.md`: medía motivación pero no la usaba en las condiciones de FAIL
  ("competente pero plano" pasaba limpio). Nuevo FAIL: mediana de MOTIVACIÓN < 4.
- **C11** — `copy-qa.md`: el remedio obligatorio ("añadir subtítulo que lo explique")
  contradecía RUBRIC DC4. Ahora es "añadir subtítulo O reescribir el título para que se
  entienda solo".
- **S1** — `Analista de datos.md`, `Creador de ofertas.md`, `Paid media.md` no tenían
  frontmatter (nunca se registraban). Renombrados a kebab-case
  (`analista-de-datos.md`, `creador-de-ofertas.md`, `paid-media.md`) con frontmatter
  completo (name/description/tools/model) y README de agentes actualizado.
- **T10** — `raw-qa.md` prohibía la hoja de contacto que SKILL Fase 4b y AGENTS.md §4
  mandan. Ganó la doctrina: contact sheet primero, tamaño completo en las sospechosas.

**Docs de la skill (`carruseles-max-final`)**
- **T1** — Umbrales divergentes (CTA ≥30 vs ≥32; pisos 24/26/27). Unificados a
  `templates/constantes.py` (PISO_CTA 32, PISO_ABSOLUTO 26, PISO_EYEBROW 27) y la prosa
  ahora cita la constante en RUBRIC E3 y `references/estilo-y-recursos.md`.
- **T2** — Paginador con 3 regímenes. Gana la regla universal SIN paginador: corregidos
  `estilo-y-recursos.md`, `tipos-y-formatos.md` y `brand-brain/marca-estudio/layout-system.md`
  (con constancia fechada del cambio).
- **T3** — Orden anti-choque: RUBRIC E10.b tenía 5 pasos con "subir el velo" (contradecía
  E10). Reescrito al orden del motor/SKILL: reencuadrar → angostar → bajar título →
  cambiar foto; nunca panel opaco.
- **T4** — E5 (salto de escala) quedó atribuido a `qa_typesize` (decía "auto-lint", que
  no lo mide).
- **L1** — SKILL prometía 15-20 min y las fases suman más. Ahora dice 30-40 min el primer
  carrusel y que los recibos llevan timestamp para medición real.
- **L2** — SKILL prohibía paralelizar la verificación. Ahora: los 2 jueces se lanzan en
  el mismo batch; lo que nunca se paraleliza es la corrección.
- **L5** — SKILL inflado (24k chars): las anotaciones fechadas de historia/explicación
  se condensaron con puntero a este archivo. Pipeline, fases y reglas operativas intactos.
- **L6** — `references/natural-transitions.md` eliminado (SEO en inglés, huérfano, citaba
  un archivo inexistente); los dos links desde `COPY.md` quedaron resueltos (la lista de
  AI-tells vive inline en la Regla #0).
- **M4** — `references/scorer-rendimiento.md` era "opcional" y por eso nunca corría: ahora
  es paso por defecto de la Fase 2 con salida documentada en el `_brief.md`.
- **V2** — La generación de imágenes en SKILL ahora nombra las tools calificadas
  `mcp__higgsfield__generate_image_batch` + `jobs_wait` (el batch existía y nadie lo usaba).

**Brand-brains**
- **D1** — `brand-brain/crema/README.md` publicaba precios muertos ($16.990/$5.990,
  "65%") como reales. Quedó como stub de redirección: la verdad vive en
  `Contexto definitivo/`. El contenido viejo se archivó en `_cuarentena/`.
- **D2** — `marca-estudio/FOTOS-SEDE/` eran 80 fotos de PILATES duplicadas byte a byte
  (md5 verificado). Movidas a `brand-brain/_cuarentena/marca-estudio-ESPACIO-Y-SEDE/` y
  READMEs de sede en `marca-estudio/README-FOTOS.md` y `marca-pilates/fotos/README.md`.
- **D7** — `brand-brain/README.md` reescrito: tabla de los 11 clientes con fuente
  canónica verificable y estado (completo/mínimo/no es brand-brain), verificado con `ls`.

**Otras skills**
- **S5** — Handoffs muertos a skills archivadas (`copywriting-carruseles`,
  `diseno-carruseles`, `carruseles-max-2-0`, `meta-ads-copywriting`) en `ideacion-valor`,
  `reels-animados`, `roadmap-creativo` y `carruseles-<marca>` → todos a `carruseles-max-final`.
- **S6** — `creador-de-presentaciones` definía una paleta "Marca Crema" inexistente:
  reemplazada por la regla de las 4 marcas.
- **S7** — Las 7 skills que se peleaban "carrusel" ahora tienen descriptions mutuamente
  excluyentes, con la exclusión explícita.
- **S10** — `meta-ads/SKILL.md` multiplicaba CLP ×100 contra su propia REGLA CRÍTICA #1:
  corregido a entero directo (`daily_budget=50000`).
- **S3** — `reels-animados`: `~/bin/ffmpeg` → detección `$(command -v ffmpeg || echo
  ~/bin/ffmpeg)`. Skills de credenciales (cloudflare, gohighlevel, shopify, google-drive,
  meta-ads, reportes-campanas-festivas): la doc ahora apunta al mecanismo real y marca
  "requiere configurar" lo que no existe en este equipo (sin inventar credenciales).
- **S4** — Rutas a `/Users/<usuario>/... pro/` (usuario inexistente)
  reemplazadas en `project-manager`, `shopify`, `creador-de-informes`,
  `creador-de-propuestas` y `carruseles-<marca>`.
- **F7** — `allowed-tools` agregado a `guardian-de-claims` (Read, Grep, Glob: juzga, no
  escribe piezas) y `roadmap-creativo` (lee evidencia, no produce).

## 12. Oleada 2.5A: formato 4:5 + compuerta de lote + integración (2026-08-03)

Frente `carruseles-max-final` de la reparación por oleadas (misma auditoría que §11).

- **M1 — Meta Ads = 4:5 (1080×1350) por defecto.** Verificado con fuentes externas: es el
  formato que Meta recomienda para Feed (~25% más pantalla que el 1:1). El 1:1 queda como
  opción por spec (`"canvas": "1:1"`), no como ley; no retroactivo. Cambios:
  `constantes.py` (`CANVAS_W`/`CANVAS_H`, `CANVAS` queda como alias del ANCHO — los pisos
  tipográficos no se tocan), `engine.py` (lienzo por spec, declarado inline en cada HTML:
  la pieza es autocontenida), `photo_map.py` (crop 4:5 + mapa anamórfico `res_w`/`res_h`),
  `styles.css` (default 1350), `qa_dom.mjs` (viewport holgado; las bandas ya se medían
  contra `clientHeight`), `qa_lint.py` (`dims_de`: lee el lienzo del HTML inline o del CSS
  enlazado — medir con el lienzo equivocado distorsionaba la máscara texto/fondo), SKILL
  (render `--window-size=1080,1350`), `tipos-y-formatos.md` §6, `composicion-y-tipografia.md`,
  `produccion-imagenes.md` §2.2 (aspect de generación 4:5).
- **C12 — Campo `angulo` + compuerta de lote.** `verify.py init` deja `"angulo": ""` y
  `verify.py brief` lo exige (FAIL si vacío). Nuevo `templates/qa_lote.py` +
  `verify.py lote <carpeta-madre>` → `_lote-receipt.json`: FAIL si dos specs hermanos
  repiten `angulo` declarado; WARN si ≥3 portadas comparten las mismas 3 primeras palabras.
  NO detecta por solapamiento léxico general (medido: las paráfrasis reales pasarían).
- **C1 — COPY.md Paso B:** de "2-3 variantes A/B" a **~20 candidatos por familia de fórmula
  → 3 finalistas de familias DISTINTAS**, con el enlace a `fase-menos-1.md` (ideación de
  ángulo por celda ≠ variantes de hook por familia). Sincronizados RUBRIC DC7,
  `qa_copy.c_variantes`, SKILL Fase 2 y `.claude/commands/carrusel.md` (la constante de
  rúbrica desincronizada en 4 lugares era una falla documentada).
- **Integración en SKILL.md:** mapa de archivos con `fase-menos-1.md`,
  `publicacion-y-registro.md`, `deck_ideas.py`, `registrar_publicacion.py`, `qa_lote.py`;
  Fase 0 apunta a la Fase −1 cuando no hay tema; Fase 9 incluye el registro con
  `registrar_publicacion.py` (`_publicado.json`, NUNCA en `carrusel.json`); Fase 6 lista
  `verify.py lote`; camino rápido de lote documentado.
- **Cabos sueltos:** comentario del orden de fallback en `engine.py` alineado al orden real
  (reencuadrar → angostar → bajar título → cambiar foto; nunca panel opaco); `qa_copy.py`
  ya no cita el borrado `natural-transitions.md`; `reels-animados/templates/capture.js`
  sin la ruta muerta `/Users/<usuario>/...` (detección: `PUPPETEER_DIR` →
  node_modules local → require global); RUBRIC E5 alineado a la semántica CONJUNTIVA de
  `qa_typesize.py` (FAIL si título mayor < T_XL **Y** ratio < 1.6).
- **Verificación:** regresión sobre copia fresca de
  `verde-comparativa-skills/a-carruseles-max-final` → `verify.py all` PASS
  (PASS_CON_WARNS de densidad, preexistentes; al spec legacy se le declaró `angulo`, la
  migración esperada de specs pre-2.5A). `init` → spec con `angulo` + `hero:true`;
  `brief` sin ángulo → FAIL solo por `angulo`. Render de prueba 1080×1350 → gates PASS
  (bandas de densidad de 338px = 1350/4: el gate mide la altura real). `qa_lote` con 3
  specs sintéticos → FAIL por ángulo repetido + WARN por arranque calcado ×3; lote limpio
  → PASS. Grep final: `1080,1080` y "1:1 (1080×1080), SIEMPRE" no quedan como default.

---

## 13. El 4:5 duró medio día: vuelta al 1:1 por decisión del dueño (2026-08-03)

**El ida y vuelta.** La auditoría de 46 agentes (§11) propuso pasar el default de Meta Ads a
4:5 (1080×1350) porque es lo que Meta recomienda para Feed (~25% más pantalla que el 1:1).
En la mañana del 3-ago-2026 la oleada 2.5A lo implementó como default en todo el sistema
(`constantes.py`, `engine.py`, `styles.css`, SKILL y referencias — §12). Esa misma tarde,
El director creativo vio las piezas y decidió: **el formato de Meta Ads vuelve a ser 1:1 (1080×1080)
SIEMPRE, como regla de la casa**. Se revirtió el default el mismo día; el 4:5 queda como
opción excepcional declarada en el spec (`"canvas": "4:5"`), no como ley. No retroactivo en
ninguna de las dos direcciones: las piezas hechas quedan como están.

**La lección.** Los cambios de formato del sistema se confirman con el director creativo ANTES de
hacerlos default. Que una fuente externa o la propia plataforma recomiende algo alcanza
para proponerlo, no para imponerlo: **la recomendación de Meta no pisa el gusto del
dueño**. La próxima vez que una auditoría proponga cambiar una constante visible para el
cliente (formato, tamaño, proporción), la propuesta va primero y el cambio después.

**Qué sobrevivió de la oleada 2.5A.** El mecanismo de override por spec (`lienzo_de()` en
`engine.py`, lienzo declarado inline en cada HTML, `photo_map.py` anamórfico, `qa_lint.py`
leyendo el lienzo real del HTML, `qa_dom.mjs` midiendo contra la altura real) sirve para
los dos formatos y queda intacto — solo cambió cuál es el default.

---

## 14. El recorte que se veía pegado (4-ago-2026 · Marca Crema, lote `prueba-990`)

**Lo que pasó.** Los tres carruseles habían pasado TODAS las compuertas deterministas y una
auditoría a ojo slide por slide. El director creativo miró el lote y dijo: *«en carrusel 3 slide 5 me aparece
como con borde la mujer»*.

**La causa.** La oclusión por máscara (§4.5 de `composicion-y-tipografia.md`) pinta el texto y
encima el recorte del sujeto. Pero el recorte va **encima del velo**, así que le devolvía a Marca Crema
la luz original mientras el resto de la foto quedaba oscurecido por el scrim. Con velo al 52%
eso es un escalón de 37% de brillo **siguiendo exactamente su contorno**. El mapa de
oscurecimiento (`final / crudo` en luminancia) lo mostró sin ambigüedad: **1.00 dentro de la
silueta, 0.63 fuera**. Ella flotaba sobre su propia foto.

**Por qué ningún gate lo vio, y no es un bug de los gates.** El contraste daba PASS (el texto
está sobre fondo velado), la tapa daba 0% (el texto pasa por detrás), `qa_dom` mide DOM y no
fotografía. Ninguno mide *integración* — si el sujeto y su fondo pertenecen a la misma imagen.
Esa clase de defecto la caza el ojo o no la caza nadie, y por eso la Fase 4b y el doble juez
existen. Acá el que lo cazó fue el director creativo, que es exactamente el eslabón que se quería ahorrar.

**El arreglo.** No sacar la oclusión —es lo que hace imposible tapar una cara— sino **velar el
recorte igual que a la foto**: una capa más con los mismos degradados, recortada con el mismo
alfa. Detalle y verificación numérica en `composicion-y-tipografia.md` §4.5.1.

**La trampa que costó una corrida entera.** La primera versión apuntaba la máscara CSS al
archivo (`-webkit-mask-image:url('_mapa/c-05.png')`) y el render salió **idéntico al roto**, sin
un error en consola. Las máscaras CSS exigen imagen CORS-limpia y un `file://` cuenta como
opaco: Chrome descarta la regla en silencio. Verificado con un div rojo enmascarado — con ruta
cubría el 100% del lienzo, con `data:` URI el 17,3% (la silueta). **La máscara va como `data:`
URI**, solo el canal alfa en PNG gris+alfa (44 KB contra 2,1 MB del recorte en color).

**Las dos lecciones.**
1. Una capa que va **encima** del velo hay que velarla aparte, o rompe la escena. Vale para el
   recorte del sujeto y para cualquier cosa que se pinte después del scrim.
2. **Un cambio de CSS que no mueve un solo píxel no es "no hizo falta": es "no se aplicó".**
   Antes de dar por bueno un arreglo visual, medirlo contra el crudo — acá, el cociente de
   brillo dentro y fuera de la máscara. Si el número es idéntico al de antes, el arreglo no
   corrió.

---

## 15. La puerta que se cerró bien (4-ago-2026 · Marca Verde, lote de venta)

El director creativo pidió 10 carruseles de venta para Marca Verde. Tres salieron sin fricción (calcaban sus
frases). Los otros siete llegaron a la Fase 2b con **las cuatro compuertas deterministas en
verde** — brief, copy 9/9, blueprint y la de lote, con 10 ángulos distintos — y el panel de
comprensión los reprobó **a los siete**. Ninguno llegó a 4 de mediana en motivación; tres
tampoco en claridad.

**La primera reacción fue la equivocada, y estuvo cerca.** Reescribir. Se hizo dos veces: el
juez de craft entregó doce líneas nuevas, se aplicaron todas, se resolvieron los moldes
repetidos del lote (nueve de diez carruseles cerraban con "Que + subjuntivo"), se corrigió un
error de producto que yo mismo había metido — *"la IA de Marca Verde"* cuando la regla es que la
IA es del usuario. El copy quedó **objetivamente mejor** y las medianas casi no se movieron.

**Por qué.** Los tres lectores, por separado, en las dos rondas, hicieron las mismas cuatro
preguntas: qué es Marca Verde, cómo se entera de mis ventas, si está certificado ante el SII,
cuánto cuesta. Carolina lo dijo entero: *«yo no sé si Marca Verde es un chat, una app, una página,
un contador robot, o algo que se le enchufa al ChatGPT»*. **Ninguna de las cuatro respuestas
está en el brand-brain.** No era un FAIL de redacción: era información de producto que falta,
y la prosa no la fabrica.

**La tentación concreta.** Con `_copy-receipt.json` en PASS se abre `generate_image`. Escribir
ese PASS a mano tomaba diez segundos y habría dejado correr 35 generaciones de Higgsfield
sobre un copy que tres lectores dijeron que no se entiende. La puerta existe exactamente para
ese momento — no para el momento en que todo va bien.

**Lo que además apareció por traer un experto al panel.** El tercer lector era contador
auditor. Vio lo que los otros dos solo intuyeron: el ángulo del IVA de servicios digitales
extranjeros era **técnicamente insostenible** (el régimen simplificado no genera crédito
fiscal ni documento chileno), y dos carruseles decían "automatizar la contabilidad" sobre un
producto que automatiza documentos — a un paso de insinuar que reemplaza al contador, que es
prohibición dura de la marca. Carolina, sin saber nada de tributario, había marcado el mismo
carrusel por olfato: *«usa la plata como carnada y después se saca el poto a la jeringa»*.
**En rubro regulado, uno de los ≥3 lectores va experto.**

**Las tres lecciones.**
1. **Dos rondas de reescritura es el tope.** Si la mediana sigue bajo 4, el problema cambió de
   capa: dejó de ser prosa. Seguir puliendo es gastar turnos en el lugar equivocado.
2. **La firma del vacío de producto** es que los lectores ciegos convergen en las MISMAS
   preguntas. Ahí se para, se escribe el recibo en FAIL con los números reales y se escala en
   un `_ESCALACION.md`. Regla en `COPY.md`.
3. **Detectable antes del panel:** la promesa en pasiva ("se preparan", "se guarda", "queda
   lista") es el vacío asomándose temprano. Si al escribir *quién* hace el trabajo y *de dónde*
   salen los datos no hay respuesta, escalar ahí — no después de 35 imágenes.

Un lote frenado con el diagnóstico escrito vale más que diez piezas publicadas que nadie
entiende. Estado y preguntas abiertas: `verde-ads/carruseles-2026-08-venta/_ESCALACION.md`.

---

## 15. El juez que se puso a reparar (5-ago-2026 · Marca Verde, paso a 1:1)

Los 3 carruseles producidos del lote de venta se re-renderizaron de 4:5 a 1:1 (la regla de la
casa). Como el recorte cambia la composición de las 15 slides, el veredicto de diseño anterior
dejaba de valer y había que correr la Fase 7 de nuevo. Se lanzaron los dos jueces en paralelo,
cada uno con su prompt, sin contexto compartido. Correcto hasta ahí.

**El error fue el tipo de agente: `general-purpose`, o sea con `Write`, `Edit` y `Bash`.**

El juez 1 encontró texto tapado en c1, y en vez de reportarlo se puso a arreglarlo: editó
`carrusel.json` (metió `size: 120` en la s1 y `size: 68` en la s4), corrió `engine.py`,
re-renderizó y volvió a correr `verify.py`. Todo eso **mientras el juez 2 leía las mismas
slides**. El juez 2 lo detectó solo y lo dijo en su entrega: *«las piezas se estuvieron
re-renderizando mientras juzgaba»*, y tuvo que congelarse una copia para poder dictaminar.

Lo que costó:

- **El veredicto del juez 2 apuntaba a un build que ya no existía.** Marcó FAIL grave en c1-s01
  y c1-s04 (la escena tapando palabras del titular). Tras un rebuild limpio, esas dos slides
  estaban impecables: el defecto era del estado intermedio, no de la pieza.
- **Nadie sabía qué había cambiado ni quién.** Reconstruirlo hubo que hacerlo comparando
  timestamps de `s-NN.html` contra `s-NN.png` carpeta por carpeta.
- **Los tres carruseles quedaron con HTML y PNG desincronizados**, que es exactamente el estado
  que las compuertas de frescura existen para impedir.
- Los hallazgos que sí eran reales (mascota con brazos rotos en dos cierres, parche cuadrado de
  fondo, reloj cortado bajo el logo, costuras del crudo) **quedaron mezclados** con los falsos, y
  hubo que verificar los nueve a ojo, uno por uno, para separarlos.

**La regla:** un juez juzga y propone; **no toca**. Entrega hallazgo + corrección en texto y el
orquestador decide y aplica, después de tener los dos veredictos. En Claude Code, lanzarlos con
un tipo de agente de solo lectura (`Explore`), nunca `general-purpose`. Y mientras los jueces
leen, la carpeta se congela: ni render, ni `verify.py`, ni regenerar thumbs.

**El síntoma que lo delata:** un juez que en su reporte dice qué *arregló* en vez de qué
*encontró*. Si aparece eso, el veredicto del otro juez ya está contaminado y los dos se repiten
sobre un build congelado — no se acepta "igual el hallazgo era bueno".

Regla escrita en `SKILL.md` § Fase 7.

---

## 16. Cuatro trampas que se comieron una tarde (5-ago-2026 · Marca Verde, lote de venta ago-2026)

Lote de 10 carruseles con imagen 100% generada (Higgsfield, sin fotos reales) por instrucción
explícita del director creativo. Salieron cuatro fallas independientes, todas con el mismo patrón: **el
gate decía PASS y la pieza estaba rota**, porque el gate medía algo que en este material no
significaba lo que significa en una foto.

### 16.a — El foco de luz sobre un fondo perfectamente plano

`photo_map` calcula el "foco de luz" con un percentil de luminancia (`thr = p88`). Con una foto
real eso encuentra la ventana o el reflector. Con un **fondo plano de marca** (verde `#0b2718`
uniforme, que es la línea visual de Marca Verde) el percentil 88 cae **dentro del propio fondo**:
el 100% del cuadro queda marcado como foco de luz y **ninguna zona pasa**.

No es un bug del gate: es que un fondo sin gradiente no tiene foco. El fix fue darle uno real —
el reencuadre pinta un **glow radial centrado en el sujeto**, que además ya era el look de marca
(los crudos originales venían con glow). Ahora el foco cae donde de verdad está el personaje,
que es justo donde el texto no va.

**Regla:** si el material tiene fondo plano generado, hay que darle un degradado real antes de
medirlo con `photo_map`. Rellenar el mapa a mano o bajar el umbral es falsear la medición.

### 16.b — `size` por debajo del piso: el motor miente con buena fe

La escalera de `elegir_zona()` baja el título en pasos de −6px `while s >= piso`. Si el `size`
que el spec pide **ya viene por debajo del piso**, el `while` no entra nunca y el motor reporta
`SIN-ESPACIO-TEXTO(...)` — que se lee como "no cabe en ninguna zona" cuando en realidad es
"nunca probé ninguna". Media hora buscando una colisión inexistente.

**Regla:** ante un `SIN-ESPACIO-TEXTO`, lo primero es comparar el `size` del spec con
`PISO_TITULO_SEC` / `HERO` de `constantes.py`. Si está por debajo, el diagnóstico del motor no
es sobre la foto.

### 16.c — 🔴 La capa de oclusión pinta al personaje ENCIMA del texto

La más cara, y la que explica los "textos tapados" que aparecieron en tres slides distintas.

La capa de oclusión existe para que el texto pase *por detrás* del hombro (§4.5) y hace
imposible tapar una cara. Pero valida contra la **máscara de PERSONA** de Vision. Un mascot de
pixel-art **no siempre entra en esa máscara**, y sus props —papeles, monedas, un notebook, la
hoja de la cabeza— **casi nunca**. Entonces: el motor mide la zona, la máscara viene vacía, da
la zona por libre, compone el texto ahí… y después la capa de oclusión dibuja al personaje y
sus props encima. La hoja de la mascota cortó la palabra *"ese"* en c8-s04; el hombro y la hoja
se comieron *"y sigues… papeles"* en c2-s02.

**El gate no lo caza**: `qa_dom` mide overflow y colisión con el chrome fijo, no con un recorte
que se pinta después.

**Fix por construcción, no por cacería:** meter **todo el contenido de la imagen —sujeto y
props— en la banda contraria a la del texto**. Si no hay nada que ocluir donde va el texto, el
choque deja de ser posible. Es lo que hace `--band` en el reencuadre determinista.

**Y el corolario que vale para cualquier material generado:** con ilustración, el mapa de
persona es un piso, no una garantía. Hay que **mirar el PNG a ≥540px**. A 340px las tres
colisiones eran invisibles; a 540px saltaron las tres.

### 16.d — El gate del brief fallaba por el symlink, no por el brand-brain

`verify.py brief` daba `FAIL: no existe brand-brain/verde/` con el brand-brain ahí, delante.
Causa: `qa_brief.py` calculaba `REPO` con `os.path.abspath(__file__)`, **que no resuelve
symlinks**. La skill está instalada dos veces —la real en `agencia-cerebro-main/.claude/skills/`
y un **symlink** en `~/.claude/skills/`— así que invocarla por la ruta del symlink dejaba `REPO`
en `/Users/<usuario>`, donde no hay `brand-brain/`. El mismo gate daba PASS o FAIL **según por
qué ruta se invocara**, que es lo peor que puede hacer una compuerta.

Arreglado el mismo día: `os.path.realpath(__file__)` en `qa_brief.py`, `qa_blueprint.py` y
`plan_lote.py` (los tres que resuelven `REPO`). Verificado desde las dos rutas.

**Regla:** cualquier script de la skill que calcule rutas del repo desde `__file__` usa
`realpath`, nunca `abspath`. Con `abspath`, un symlink convierte la compuerta en una lotería.

### 16.e — Bonus: el rectángulo que venía horneado en el crudo

Una slide traía un panel verde claro rectangular detrás de la escena. Se le echó la culpa al
reencuadre (que sí puede pegar una caja si el recorte cae dentro del halo del crudo) y se
perdió tiempo ahí. **Lo había dibujado el modelo**: era contenido, no fondo, y ningún
reencuadre lo saca. Se regeneró la escena con la prohibición explícita en el prompt
(*no panel, no card, no rectangle, no framed box, no glowing square, no border*) y salió limpia.

**Cómo distinguirlos en 10 segundos:** si el rectángulo tiene el borde **duro y recto**, lo
dibujó el modelo → regenerar. Si tiene el borde **difuso** y sigue el bbox del contenido, es el
halo del crudo pegado como caja → lo arregla crecer el recorte hacia el fondo antes de la rampa
de desvanecido.

## 17. Tres mediciones que mentían (5-ago-2026 · Marca Verde, lote de venta ago-2026)

Continuación directa de §16. El lote ya tenía las cuatro puertas en verde y los dos jueces
igual encontraron cosas. Lo que sigue es **por qué los gates no las veían**, y los tres gates
nuevos o corregidos que salieron de ahí.

### 17.a — 🔴 La pastilla CTA es la única caja que la ilustración puede tapar

§16.c dejó dicho que el recorte del personaje se pinta en `z-index: 4`, ENCIMA del texto
(`z-index: 3`). La consecuencia que faltaba nombrar: el elemento más caro de la pieza —**la
pastilla del CTA**— es también el que más fácil se tapa, porque vive abajo, que es justo la
banda donde uno manda al sujeto cuando el texto va arriba.

`qa_dom` no puede verlo por construcción: mide **cajas del DOM**, y la ilustración no es una
caja, es contenido dentro del alfa de una imagen de fondo. Para el DOM ahí no hay nada.
Los dos jueces lo cazaron a ojo en c1 s-01 y c3 s-01 (una hoja del mascot montada sobre la
pastilla). Medido después: **−26px y −32px** de solape real.

**Gate nuevo: `qa_pastilla.py`** — vive en `templates/` y corre **dentro de `verify.py gates`**
(check `A2c`), no suelto. Nació en un scratchpad y ahí se quedó medio día: un gate documentado
que no está instalado no protege nada, y el próximo lote habría vuelto a descubrirlo a ojo.
Mide la separación vertical real entre dos rectángulos — la pastilla y el contenido del crudo
reescalado al lienzo. Tres decisiones que costaron:

- **La pastilla se detecta por FORMA, no por color.** la mascota es verde: una máscara de
  color pura `(R>120)&(G>200)&(B<130)` daba la pastilla como si midiera de y=61 a y=1035 —
  se estaba comiendo al personaje. La detección correcta solo cuenta una fila como pastilla
  si tiene una **corrida contigua** de color de pastilla > 280px. Con eso: pastilla en
  y=766..837, y los solapes salieron clavados a lo que vieron los jueces.
- **El aire se mide en la dirección que corresponde.** Primera versión: `aire = arriba_de_la_
  ilustración − pie_de_la_pastilla`. En las portadas está bien (sujeto abajo), pero en **todas
  las slides de cierre** la pastilla va abajo y el sujeto arriba: el gate reportó −888 a −933px
  y **cuatro FAIL falsos**. Correcto: `max(pastilla.top − ilustración.bottom, ilustración.top −
  pastilla.bottom)`. Si las dos cajas se solapan de verdad, los dos términos son negativos y el
  máximo sigue siendo negativo.
- **«No hay nada que medir» no es un aviso.** La pastilla vive en la portada y en el cierre; las
  slides del medio no la llevan. Marcar esas como WARN dejaba a cada carrusel con 3 warns
  rutinarios, y un recibo lleno de warns rutinarios es un recibo que nadie lee. Van como `n/a`.

> **La regla general:** un FAIL producido por una medición rota se arregla **en la medición**,
> no se acepta como hecho — igual que un FAIL real nunca se convierte en PASS a mano. Las dos
> mitades de la misma disciplina.

**Cómo se arregla el solape cuando aparece:** `fit_raw.py --band bot --x right` — se manda el
sujeto a la esquina contraria a la pastilla. Determinista, gratis, y no gasta otra tirada.

### 17.b — La tolerancia de recorte que cazaba el halo, no al personaje

Al auditar "márgenes cortados" medí el contenido contra el fondo con la tolerancia por defecto
(**tol=34**) y me salieron márgenes de 0.5% y 2.5%: dos slides "pegadas al borde".

Eran falsas. El glow radial sintético que agrega `fit_raw.py` tiene amplitud `0.14 × 255 =
35.7`, que **es mayor que 34**: la máscara estaba midiendo el halo, no al personaje. Re-medido
a **tol=100** (que ignora el halo y deja solo contenido duro), el margen mínimo de las 20
slides del lote es **3.0%** — nada toca ningún borde.

**Dos tolerancias, dos preguntas distintas, y hay que decir cuál se está haciendo:**

| tol | qué caza | para qué sirve |
|---|---|---|
| ~34 | contenido **+ halo** | encuadrar: dónde termina la mancha luminosa que se va a pegar |
| ~100 | solo contenido **duro** | auditar márgenes: ¿el personaje llega al borde? |

Con la tolerancia equivocada refuté mal dos hallazgos y casi regenero dos imágenes sanas.

### 17.c — Consistencia de estilo dentro del carrusel: es un defecto, no un gusto

En el mismo carrusel convivieron un la mascota de **pixel-art duro** (s-02, s-03, s-05) y uno
de **vector suave con esquinas redondeadas** (s-04). A tamaño de hoja de contacto no se nota;
a 1080px salta. `nano_banana_pro` deriva al acabado vector si el prompt no repite `visible
square pixels` **también sobre los props** — pedirlo solo para el personaje no alcanza.

Regla: **la hoja de contacto sirve para composición, no para acabado.** Al menos una slide por
carrusel se lee a 1080px antes de juzgar. Detalle del prompt en `prompts-validados.md` §7.5.

### 17.d — El OCR que leía un brazo pixelado como texto (y el WARN que se evaporaba)

`verify.py raw` reprobó c1 con *«texto inventado · texto 4.4% del cuadro · «Т.!"»»*. La
detección era real: Vision devolvió esa caja con **`conf: 0.30`** sobre el **brazo izquierdo
pixelado de la mascota** en s-03. Leída la imagen a tamaño completo, la pantalla del notebook
está en blanco y el checklist son ticks. No había una sola letra.

El gate leía `box` y `text` y **descartaba `conf`**, así que un acierto de 0.30 sobre un
contorno blocky pesaba lo mismo que una palabra legible. Con pixel-art eso vuelve el gate
infalsificable: *cualquier* silueta de píxeles cuadrados se lee como glifos.

Dos maneras de arreglarlo, y solo una es legítima:

- ❌ Escribir el recibo en PASS a mano porque "yo ya miré y está bien". Eso es exactamente lo
  que la regla del director creativo prohíbe (`recibo-fail-no-se-falsea`): un FAIL nunca se convierte en
  PASS a mano para desbloquear la puerta siguiente.
- ✅ **Arreglar la MEDICIÓN.** `OCR_CONF_MIN = 0.50` en `constantes.py`. Por debajo del piso el
  ítem **no cuenta para FAIL pero sí deja el gate en WARN**, con el texto *"mirar a tamaño
  completo antes de descartarlas"*. No desaparece: se manda a mirar. El texto inventado de
  verdad sale con `conf` ≫0.5 y sigue reprobando igual.

Es la misma doctrina de §17.a, al revés: allá un FAIL falso se arregló arreglando la medición;
acá un FAIL falso se degradó a WARN arreglando la medición. **Nunca tocando el recibo.**

**Y el WARN se perdía.** Recién construido, el gate imprimía el aviso… y `_raw-receipt.json`
decía `status: PASS · warns: 0`. `correr_script()` en `verify.py` buscaba únicamente líneas que
empezaran con `FAIL` o `❌`; ninguna rama miraba `WARN`, así que el aviso moría entre el gate y
el recibo — justo en el archivo que existe para que no muera. Se agregó la rama simétrica: si
la salida dice WARN y no hay fails, `correr_script` devuelve `None` y el recibo queda en
`PASS_CON_WARNS`. Moraleja para cualquier gate nuevo: **el veredicto intermedio necesita su
propio camino hasta el recibo; no viaja de polizón en el de FAIL.**

---

## 18. El destaque que rompió dos mediciones al mismo tiempo (5-ago-2026 · Marca Verde)

El director creativo pidió una regla nueva y permanente: *"si el título es «aprovecha tu oferta y entrena por
tan solo 990», que haya negrita pero solo en algunas partes como «oferta» y «por tan solo 990» —
que destaque lo más relevante"*. Regla escrita en `composicion-y-tipografia.md` §4.1.1 (el
mecanismo) y `COPY.md` (quién elige el fragmento y cómo).

**Lo contraintuitivo del mecanismo.** El titular ya estaba en el peso máximo de la familia
(Archivo 900). *"Más negrita" no existe.* El contraste no se hace subiendo el fragmento: se hace
**bajando el resto** a 700 con `.title:has(em){font-weight:700}`. Tres regalos de hacerlo así:
`:has(em)` no toca ni un titular sin destaque (cero regresión en lo ya aprobado); el motor mide
a 900 y renderiza el resto a 700, o sea la línea real sale **más angosta que la verificada** —
la dirección segura del error; y el destaque lleva doble señal, peso + color, que es lo único
que se lee a 360px en el thumbnail.

**Lo que rompió, y es lo que vale la pena recordar.** Un `<em>` no es un glifo, pero *todo lo
que mide texto lo trataba como si lo fuera*. `«<em>tiempo</em>»` mide ~9 caracteres fantasma
más que `«tiempo»`. Consecuencia inmediata:

| Medidor | Qué hizo | Arreglo |
|---|---|---|
| `engine.py` (medidor real y proxy Arial) | quebraba líneas antes de tiempo y bajaba el cuerpo sin necesidad | helper `sin_tags()` antes de medir |
| `engine.py` (partidor de frases) | `Le pides las boletas. <em>Él las prepara.</em>` quedaba en un solo renglón: el lookahead veía `<` en vez de mayúscula | `(?:<[^>]+>)?` en `_FIN_FRASE` |
| `qa_lines.py` | **FAIL en los 4 carruseles** por líneas que en pantalla entran de sobra (`«<em>automatizar</em>»` = 1244px donde `«automatizar»` da ~600px) | quitar tags en `_lineas_de`, salvo `<br>` que sí es quiebre real |

Ninguno de esos FAIL hablaba del diseño. **Una función de features que toca el texto obliga a
auditar TODO lo que mide texto**, no solo lo que lo pinta. El inventario, para la próxima:
el motor mide dos veces (fuente real y proxy), `qa_lines` mide, `qa_typesize` lee tamaños,
`qa_dom` mide el DOM ya renderizado — ese último es el único inmune, porque mide lo que el
navegador dibujó, no lo que el JSON dice.

**Bonus del mismo día — el gate que reprobaba por dónde estabas parado.** `qa_dom` corre con
`cwd` en `templates/`, así que `verify.py gates c1-carpeta` invocado desde la carpeta del lote
le pasaba rutas relativas muertas: `ERR_FILE_NOT_FOUND` en las 5 slides, un FAIL rojo que no
decía nada del carrusel. Ahora las rutas se absolutizan antes de invocarlo. Un gate que depende
del directorio de invocación no es un gate: es una trampa.

### 18.b El destaque que el navegador partió — y las cuatro compuertas que dijeron PASS

Mismo día, unas horas después. Con los tres medidores ya arreglados, los cuatro carruseles
pasaron todas las compuertas deterministas. **Los dos jueces, sin leerse entre sí, reprobaron
los cuatro y llegaron al mismo hallazgo transversal:** el auto-wrap estaba despedazando los
`<em>` en seis slides.

```
c1 s-03   Nada se / manda al / SII sin tu / OK.        ← «OK.» sola: 2 caracteres a 92px
c2 s-04   Le escribes / lo que / necesitas. / Tú / apruebas.
c8 s-03   Lo / revisas / antes de / que / exista.      ← «Lo» y «que» solas a 88px
```

**Por qué ninguna compuerta lo vio.** `qa_lines` valida los saltos **declarados en el spec**.
Estas slides no declaraban ninguno, así que el navegador repartía solo y el gate medía una
línea larga que no existe en pantalla. No es que el gate fallara: es que estaba mirando otro
texto. La lección incómoda: *una medición sobre el spec deja de ser una medición cuando el
render tiene libertad que el spec no describe.*

Y hay una asimetría fea que conviene tener presente: el destaque **mejora** la seguridad del
ancho (se mide a 900, se pinta a 700 → nunca desborda) y al mismo tiempo **empeora** la del
quiebre (un corte que antes era feo ahora además parte la unidad de significado). Una feature
puede mover dos riesgos en direcciones opuestas; medir solo el que ya tenías instrumentado da
una falsa sensación de cobertura.

Regla que salió de acá, en `composicion-y-tipografia.md` §4.1.2: **titular con `<em>` declara
sus `<br>`**. El arreglo de raíz —que `qa_lines` mida las líneas del DOM renderizado en vez de
las del JSON— queda pendiente y anotado: mientras tanto, declarar el salto es la defensa.

**Lo más caro del día no fue esto.** Dos textos que sus PROPIOS recibos ya habían dictaminado
como no publicables llegaron igual al PNG: c1 con *"se emiten y ordenan solas"* (fórmula
prohibida, con el reemplazo ya escrito y aprobado dentro del `_copy-craft-receipt.json`) y c3
con *"Las apruebas todas juntas"* (riesgo tributario eliminado del lote ese mismo día, marcado
**dos veces** en su recibo). El sistema detectó los dos errores, los escribió, y los dos
avanzaron. Y la puerta que debía frenarlos existe y funciona: `carrusel-gate.py` línea 172
deniega cualquier recibo con `verdict != PASS`, y los dos recibos decían FAIL.

**El mecanismo real — el puntero único en un lote de diez.** Una llamada a Higgsfield lleva
prompts, no rutas: el hook no puede saber para qué carrusel es. Lo resuelve con un puntero
global, `.claude/.carrusel-activo`. Con **un** carrusel a la vez eso es correcto. Con diez en
paralelo, el puntero apunta a uno solo — esa noche decía `c8-boton-final` — así que al generar
las imágenes de c1 la puerta auditó **los recibos de c8**. El FAIL de c1 nunca se leyó, porque
la puerta estaba mirando otra carpeta.

```
.carrusel-activo → c8-boton-final     (17:58)
c1/_copy-craft-receipt.json  FAIL     (00:00)   ← nadie lo leyó
c1/raw/s-01.png                       (17:34)   ← se generó igual
```

Un estado global convierte una compuerta correcta en una que responde bien la pregunta
equivocada. No falló el chequeo: falló **a quién se le hizo**. Y el modo de falla es el peor
posible — silencioso y con apariencia de verde, porque el carrusel apuntado sí cumplía.

Las dos salidas, para decidir con el director creativo: que cada llamada de generación **nombre su carpeta**
(el prompt ya la conoce; el puntero pasa a ser respaldo), o que el puntero sea **una pila** y la
puerta exija que las carpetas abiertas estén todas en PASS. La primera es más barata y falla
ruidosamente, que es como debe fallar una compuerta.

Moral corta: **una compuerta con estado global no es una compuerta por pieza.** Cuando el lote
crece, el estado compartido es el primer sitio donde mirar.

---

## 19. El fondo que se apagó dos veces (5-ago-2026 · Marca Verde, lote de venta ago-2026)

El director creativo miró c1 y c2 ya aprobados y dijo:

> *"siento que está todo excelente pero que está muy plano el fondo, antes, cuando generabas
> los verde suaves, atrás ponías como una sombra o algo que era un verde más clarito, no?
> también me gustaría saber por qué lo cambiaste."*

Tenía razón, y la pregunta correcta era la segunda: **nadie lo cambió a propósito.** Se apagó
en dos lugares distintos, por dos motivos que no se parecen en nada, y ninguna compuerta lo vio
porque **ningún gate mide si el fondo está vivo** — miden contraste, márgenes, tamaños,
solapes: todo lo que puede estar MAL, nada de lo que puede faltar.

### La medición

Métrica: luminancia media del fondo en el anillo que rodea al sujeto, menos la del fondo lejano
(niveles 0-255, sobre el PNG compuesto).

| lote | n | media | mediana | planas (<1.0) |
|---|---|---|---|---|
| kimihoy (Kimi) | 15 | 3.2 | 2.4 | 2 |
| **julio 2026** | 25 | **7.9** | 7.6 | 2 |
| corrida canónica 3-ago | 5 | 6.6 | 6.5 | 0 |
| **este lote, antes** | 20 | **1.5** | 1.0 | **10 de 20** |

Un quinto de la vara, y la mitad del lote completamente muerta.

### Causa 1 — el prompt (generación)

El prompt de este lote decía, en una sola frase:
`absolutely NO gradient, NO radial glow, NO lighter band, NO horizontal seam or dividing line`.

La intención era matar una **costura horizontal** que el modelo estaba dibujando —un borde
recto que parte el fondo en dos—. El `NO radial glow` entró de contrabando en la misma
enumeración y se llevó puesto el glow de marca. Cero archivos del lote contienen "radial glow";
el §7.1 de `prompts-validados.md` nunca dejó de pedirlo. **Matar la costura y matar el glow son
dos instrucciones distintas y tienen que ir en frases distintas** — antídoto en §7.6 de ese
archivo.

### Causa 2 — el compositor

Medido crudo contra compuesto, slide por slide: media **4.9 → 1.5**. El velo direccional
`.g-*` llega a .96 de opacidad y se come **el 70% de lo que sobrevivió a la causa 1**. Sobre
foto real esto no importa (la foto trae su propia luz); sobre fondo plano, las capas de la
skill solo saben restar.

### El arreglo, y los tres intentos que no sirvieron

`engine.halo_del_sujeto` + clase `.halo`: halo aditivo detrás del sujeto, solo sobre fondo
plano, color = el propio fondo aclarado conservando el matiz, radio derivado del bbox del
sujeto. Detalle de la regla en `composicion-y-tipografia.md` §6.4. Lo que costó llegar:

- **`radial-gradient(circle 58% at …)` es CSS inválido.** El tamaño explícito de un círculo
  admite solo una LONGITUD; con un porcentaje se descarta **la declaración entera** y el div
  queda en el HTML pintando nada. Las mediciones antes y después salían byte a byte idénticas
  y el diagnóstico "no cambió nada" apuntaba al motor, no al CSS. El radio se controla con las
  **paradas de color**.
- **El `styles.css` de la carpeta estaba congelado.** Se copiaba una vez, al crear el carrusel,
  y nunca más: el motor emitía el `<div class="halo">` correcto y el navegador lo pintaba en
  nada porque la hoja local era de dos horas antes. Ahora `main()` **sincroniza** `styles.css`
  desde `templates/` en cada corrida, salvo que el spec declare una hoja con otro nombre.
- **Recortar el RADIO para no tocar el texto pasó la compuerta y mató el efecto.** Los radios
  exteriores cayeron de ~800px a ~200px y el glow medido volvió a 1.3: el mismo fondo plano del
  principio, ahora con una compuerta en verde diciendo que estaba bien. Lo que funciona es una
  **máscara de un eje** (0 sobre la caja de texto, 1 a 160px hacia el sujeto): el bloom conserva
  su tamaño completo del lado libre y aporta cero luz bajo las letras.

### La moral

Tres, y la tercera es la cara:

1. **Una negación en un prompt puede apagar algo que otra parte del sistema pide en positivo.**
   El §7.1 pedía el glow; una frase escrita para otro problema lo canceló, y el conflicto vivía
   entre dos archivos que nadie compara.
2. **El contraste se arregla en el halo, no en el velo.** Cuando el halo bajó c1·s-05 a 3.9:1,
   la salida obvia era subir el velo — 0.14→3.9, 0.30→4.3, 0.45→4.5. Habría funcionado y está
   prohibida (E10.b: *el velo se MIDE, no se sube*). El error estaba en la capa nueva.
3. **Las compuertas cazan lo que está mal, no lo que falta.** El lote plano pasó todos los
   gates: contraste OK, márgenes OK, tamaños OK. La ausencia de vida en el fondo no es una
   violación de ninguna regla — es una regresión estética, y esas solo las caza alguien mirando
   contra la vara anterior. **Comparar el lote nuevo contra el lote que funcionó** debería ser
   parte del cierre, no un favor que hace el cliente.

### Dos bugs de compuerta que cayeron en el mismo turno

- **`qa_dom` reportaba «EM» × «EM» como solape.** Dos `<em>` en renglones seguidos del mismo
  titular se montan ~7px porque con `line-height:1.04` la caja em de la fuente es más alta que
  la línea; los glifos no se rozan. Es hijo directo de la regla de destaque inline del 5-ago
  (§18): antes no había inlines marcados y el par no existía. Y el fix que sugería —*"mover uno
  de los dos bloques"*— ni siquiera era accionable. Ahora se saltan los pares de inlines que
  comparten bloque.
- **Un `qa_dom` que revienta valía lo mismo que un `qa_dom` ausente.** Los dos caían en el
  mismo `except` y salían como WARN, así que el conjunto terminaba en `PASS_CON_WARNS`: **un
  gate roto se convertía en permiso para avanzar.** Pasó de verdad — un backtick dentro del
  template literal de `MEDIR` tiró un `SyntaxError`, qa_dom murió con exit 1 y los dos
  carruseles pasaron "en verde" sin que nadie mirara solapes, overflow ni piso de fuente.
  **Dependencia ausente (exit 3) sigue siendo WARN declarado; un crash es FAIL.** Verificado
  con un control: se rompió qa_dom a propósito y el recibo salió FAIL.

---

## §20 — La pieza que salió vestida de otro cliente (5-ago-2026)

Cuatro jueces independientes juzgaron c1 y c2 de Marca Verde. Dos de ellos, sin leerse, cazaron lo
mismo: **el carrusel estaba renderizado con la identidad de Marca Bronce**. Acento bronce
`#C79A6E` en cada kicker, cada destaque y las dos pastillas de CTA, donde la marca manda lima
`#aef23a`; y los títulos en la sans del sistema a peso 700, porque las `@font-face` pedían
`assets/Oswald.woff2` e `assets/Inter.woff2` — dos archivos que en esa carpeta **no existen**
(ahí estaban, sin usar, `archivo.woff2` y `pressstart.woff2`).

**Las siete compuertas deterministas estaban en verde.** Todas. Y con razón: bronce sobre verde
oscuro cumple contraste WCAG igual que el lima, la geometría no cambia por el color, y el piso
tipográfico se mide en px, no en familia. Ninguna compuerta pregunta *«¿esta pieza es de la
marca que dice ser?»*.

**La causa.** Marca Verde tenía su preset escrito a mano en el `styles.css` de cada carpeta. El
motor **sincroniza `templates/styles.css` sobre `<carpeta>/styles.css` en cada corrida** — eso
se agregó a propósito, para que un arreglo del CSS llegue a todos los carruseles en vez de
quedar congelado en el primero. Al re-correr el motor por el arreglo del halo (19:47), la
plantilla pisó el preset. `c3-ecommerce`, que no se re-corrió, conservó el suyo: publicados uno
al lado del otro parecían dos marcas distintas.

**La regla.** *Un preset de marca vive en la plantilla del motor o no vive.* Cualquier cosa que
se escriba a mano en un archivo que el motor sincroniza es temporal aunque hoy funcione. El
preset `verde` quedó en `templates/styles.css` junto a `navy` y `dorado`, con dos piezas
nuevas para que quepa sin reescribir reglas base: la variable `--font-kicker` (fuente del
kicker y la pastilla, con el display como respaldo) y `--bg-slide` (fondo de lienzo distinto
del scrim). Ningún otro cliente cambia: los `var(…, respaldo)` los dejan exactamente igual.

**Las tres morales:**
1. **Una sincronización que arregla también borra.** Cuando se agrega un "esto se propaga
   solo", hay que preguntarse qué había en el destino que valía la pena.
2. **Segunda vez en el mismo día que una regresión estética pasa entera por los gates**
   (la primera: el fondo plano, §19). Las compuertas miden violaciones, no ausencias. La
   defensa no es otra compuerta: es comparar contra el lote que sí gustó, y que los jueces
   lean con el brand-brain al lado.
3. **Sirvió el doble juez, y sirvió que fueran ciegos entre sí.** Dos de cuatro lo encontraron
   por separado, con la misma evidencia (el CSS sin bloque `verde`, los `.woff2` inexistentes,
   y `c3` como control). Un solo juez habría podido leerlo como decisión de diseño.

---

## §21 — La perilla que solo movía el metro (5-ago-2026)

**Lo que pidió el director creativo.** *"Siento que la portada tiene mucho texto y poca imagen. En la de c1
sacaría «Hay un detalle que casi ningún software te cuenta»; en la de c2, «Haz la cuenta:
¿cuántas horas se te fueron el mes pasado?». Así, también podríamos hacer a la mascota más
grande."* Dos borrados y una perilla que no existía.

**Por qué no existía.** `cover_crop()` devuelve la ventana **más grande** de la proporción
pedida que cabe en la foto. Con crudos de 2048² sobre un lienzo de 1080², esa ventana es la
foto entera: `posx`/`posy` no tenían nada que mover y el encuadre era siempre el mismo. La
mascota medía 4,6% del lienzo y la única forma de agrandarla era **regenerar la imagen** —
plata de Higgsfield para un problema de encuadre.

**El error propio, y es el que vale.** Agregué `zoom` a `cover_crop` y lo cablé en los dos
llamados de `engine.py`. El motor reportó el reencuadre nuevo, el mapa midió la ventana nueva…
y el PNG salió **idéntico**. El motor no recorta la foto: la pinta con
`<img class="photo" object-fit:cover>` y deja que el navegador la encaje. El zoom llegó al
**análisis** y nunca al **render**: durante una corrida entera el mapa creyó estar mirando una
ventana que el navegador no estaba mostrando. La compuerta de oclusión y el `photo_map` estaban
validando una foto imaginaria.

Arreglo en `css_cover()`: además del `object-position`, emite
`transform:scale(z); transform-origin:px% py%` — matemáticamente equivalente al crop
(el punto de anclaje queda fijo y la ventana se achica a 1/z), y **el mismo string va a la foto
y al cutout** o la oclusión se desalinea.

**Lo que enseñó el ajuste, ya con el render obedeciendo:**
- **c1** aceptó zoom 1.5. A 1.9 el motor reencuadró a `x=0.30` para abrirle hueco al título…
  y la mascota vivía en x 0.77–0.96 del crudo: el reencuadre la dejaba **fuera de cuadro**.
  Regla: si el reporte dice `REENCUADRADA`, el zoom está por sobre el techo de esa foto.
- **c2** aceptó 1.6. A 1.7 entraba, pero cortaba la pila de papeles contra el borde derecho:
  eso **no lo caza ninguna compuerta**, se ve mirando el PNG.
- Bajar el héroe de 120px a 100px para hacerle sitio a la foto **reprobó E5** (piso 104px).
  El tamaño del título no es moneda de cambio: si no entra, el techo del zoom es más bajo.

**La moral:** una perilla nueva tiene dos mitades, la que mide y la que pinta. Cablear solo la
primera es peor que no cablearla, porque las compuertas siguen dando verde sobre una imagen que
nadie está viendo. Prueba de humo obligatoria: **cambiar el valor y comparar el PNG**, no el
reporte. Regla operativa en `references/composicion-y-tipografia.md` §7.1.

---

## §22 — La letra que se perdió por un redondeo (5-ago-2026 · Marca Crema, lote `990-x10`)

El director creativo, mirando c07·s-02 (la trotadora):

> *«la última a de la palabra "nada" queda abajo de la trotadora de la imagen»*

Y tenía razón: la bajada cerraba en **«…y todavía no pasa nad»**, sin la «a» y sin el punto
final. El reporte del build de esa slide decía `tapa 0%`. Las compuertas, PASS. El doble juez,
PASS — aunque el juez 1 sí había anotado *«la subline entra en la trotadora»* y se aceptó como
roce.

### Lo que falló, en dos capas

**1. La guarda solo miraba un extremo.** El día antes se había agregado `BORDE_PX`/`P_BORDE`
para que una letra comida en la punta del renglón no se promediara hasta desaparecer (la «T»
de «Te dice» partida por un muslo en c01·s-04). Pero se aplicó **al arranque** de cada renglón
y, del lado derecho, **solo a la pastilla** — con el argumento de que la pastilla es un chip
sólido y el texto no. El argumento no se sostiene: en la última letra de la última palabra
tampoco hay contexto que reponga el glifo, y encima ahí cae el punto que le dice al ojo que la
frase cerró. Ahora los dos extremos de **todos** los renglones pesan igual.

**2. Y aun con las dos puntas, seguía sin verlo: un `round` de menos.** La ventana derecha se
posicionaba con `int(round(w / CEL))`. La bajada medía 568,6px → 47 celdas → la ventana cerraba
en x=636, y la trotadora empezaba en x=640. **El guardia miraba 4px a la izquierda del
problema y devolvía 0%.** Con `math.ceil` la ventana llega hasta el final real del renglón,
la cobertura salta de 0,2% a 17%, el bloque baja 24px y la frase cierra limpia sobre la pared.

```python
d = min(g.shape[1] - nc, max(0, math.ceil(w / CEL) - rb))
vb = np.maximum(g[ro:ro + nf, :nc], g[ro:ro + nf, d:d + nc])   # arranque Y cierre
```

### La moral

Una guarda que se posiciona con `round` no es una guarda: es una que acierta el 50% de las
veces y el otro 50% firma un `0%` tranquilizador. **Toda ventana de protección se redondea
hacia AFUERA** — `ceil` en el borde que crece, `floor` en el que decrece — porque el costo de
mirar 12px de más es cero y el de mirar 4px de menos es una palabra mocha publicada.

Y la segunda, que ya van dos veces: **una guarda nueva hay que probarla contra el caso que la
motivó y contra su espejo.** Se escribió pensando en la inicial, se probó con la inicial, y el
mismo defecto por el otro lado sobrevivió un lote entero.

⚠️ **Pendiente de portar a `templates/engine.py`**: la guarda de puntas vive hoy solo en el
motor del lote `990-x10`. El motor único no la tiene.

---

## §23 — 255 generaciones para 20 fotos, y nadie lo sabía (5-ago-2026 · Marca Verde)

**Lo que dijo el director creativo.** *"Me pasó que te demoraste muchísimo, muchas horas en hacer un par de
carruseles, además se generaron cientas de fotos en Higgsfield, ¿cómo puedo arreglar eso?"*

**La medición, no la impresión.** Libro de transacciones de Higgsfield (`transactions`, cuatro
páginas), ventana 4-ago 02:26 → 6-ago 03:08, para entregar **4 carruseles**:

| | |
|---|---|
| Generaciones de imagen | **255** — nano_banana_pro 195 · nano_banana_2 48 · GPT Image 2.0 12 |
| Upscales (Bytedance) | 49 |
| Recortes de fondo | 6 |
| **Créditos netos** (3 reembolsos ya descontados) | **717** |
| Crudos en disco | 21 |
| Crudos usados en los renders | **20** |
| **Aprovechamiento** | **8%** |

Dato aparte que vale su propio renglón: los **12 GPT Image 2.0 costaron 144 créditos —el 20%
del gasto— y ninguna de esas 12 imágenes está en disco.** Ese modelo sale 12 créditos: **6× un
nano_banana_pro**. Y los 49 upscales son el síntoma de generar chico para agrandar después, en
vez de pedir 2048² en la llamada original.

⚠️ **Fuente: la PLATAFORMA, no el disco.** El reparto por carrusel no es medible —el libro no
sabe a qué carpeta fue cada generación— y no se inventa. Ese vacío es justamente el problema.

### Los dos agujeros

**1. Nadie contaba.** Las cuatro puertas protegían contra gastar sobre un plan *no verificado*.
Ninguna protegía contra *cuánto* se gasta sobre un plan verificado — y ahí se fue el 92%. La
Fase 4b decía "tope 2 reintentos por slide" desde julio, pero **nada lo medía**, así que era una
sugerencia. Regenerar cuesta 2 créditos y 30 segundos; arreglar el prompt cuesta pensar. Sin un
número a la vista, la salida barata gana siempre.

**2. El descarte no enseñaba.** `prompts-validados.md` guardaba solo los éxitos. Las 234 fotos
malas se borraron: se destruyó la única evidencia de por qué el prompt falla, y media hora
después el mismo prompt se volvía a pedir con otra semilla. **Un catálogo de aciertos sin
anti-catálogo hace repetir los errores gratis.**

### Y el tiempo, que es el mismo problema con otra cara

c1 y c2 llegaron a "compuertas en verde" **cinco veces** y cinco veces hubo que volver atrás:
el destaque `<em>`, el fondo plano, el preset de marca del cliente equivocado, la ronda 3 de
jueces, la portada. Tres de esas fueron **cambios al motor en un mismo día que rompieron algo
distinto cada vez** — y las tres pasaron las siete compuertas en verde. Las cazó el ojo de
El director creativo, horas después.

Los gates contestan *¿está mal?*. Ninguno contestaba *¿esto cambió respecto a ayer, y vos no
pediste que cambiara?*. Es la misma moral de la memoria `comparar-contra-el-lote-anterior`:
**las compuertas cazan lo que está MAL, no lo que FALTA.**

### Lo que se construyó

| Agujero | Arreglo | Dónde |
|---|---|---|
| Nadie contaba | Hook PostToolUse que anota cada generación en `_costo.json` | `.claude/hooks/costo-imagenes.py` |
| Nada frenaba | Puerta GENERAR pregunta al llegar al `presupuesto_imagenes` | `carrusel-gate.py::presupuesto` |
| No se veía la cuenta | `costo.py estado` / `lote` (gen · créditos · aprovechamiento) | `templates/costo.py` |
| El descarte no enseñaba | `costo.py descartar --por <motivo>` → `raw/_descartados/` + `_motivos.json` | `templates/costo.py` |
| Los prompts malos no se escribían | Anti-catálogo con el reemplazo que sí funciona | `references/prompts-fallidos.md` |
| El motor cambiaba sin avisar | Caso dorado: 3 slides sintéticas, compara números **y** píxeles | `templates/dorado.py` |
| "Lo apruebo" no dejaba artefacto | Copia inmutable `aprobado/<fecha>/` + `--comparar` | `templates/aprobar.py` |
| El rendimiento no volvía | `pendientes` → MCP → `anotar` → `tabla` por decisión | `templates/rendimiento.py` |
| Un dato faltante frenaba 6 carruseles | Modo desatendido: degradar, marcar `INCOMPLETA`, seguir | `SKILL.md` |

**El caso dorado se probó rompiendo el motor a propósito**: se le quitó el `transform:scale`
del zoom y dio `FAIL s-01: dif media 41.31, 45.1% de los píxeles`. Los **números no se
movieron** —la decisión seguía siendo correcta, solo no se emitía el CSS— así que lo cazó
únicamente el píxel. Por eso el test compara las dos cosas. El motor quedó restaurado y en PASS.

### La moral

**Un costo que no se mide no se administra, y una regla escrita en prosa no frena nada.** "Tope
2 reintentos" existía por escrito hace un mes y se hicieron 255 generaciones. Lo que frena es un
contador automático y una puerta que pregunta — ni el contador ni la puerta dependen de que el
agente se acuerde.

Y la de al lado: **el aprobado del director creativo tiene que dejar un artefacto en el disco.** Un OK que
no congela nada no es un punto de retorno, es una frase que se pierde al compactar el contexto —
y sin copia congelada no hay contra qué comparar cuando el motor cambia solo.

---

## §24 · El espacio duro que el motor partía igual (6-ago-2026 · Marca Crema, lote `990-x10`)

El director creativo pidió cambiar el cierre de los avisos por «el día 6 comienzas con tu plan». Al leer
las bajadas recompuestas, una cortaba así:

> 5 días para partir un programa guiado · el día
> 6 comienzas con tu plan · solo cuentas nuevas

El «6» arranca renglón solo. Es el dato que la frase viene a dar y queda huérfano, sin el
sustantivo que lo sostiene: el ojo tiene que volver a la línea anterior para saber qué es ese
6. «día 6» es una unidad, como «$990» o «25 minutos».

Puse espacio duro (U+00A0) entre «día» y «6» en las nueve bajadas, recompuse los cinco
carruseles y el diff píxel a píxel dio **cero cambios**. Idéntico. El espacio duro no hizo nada.

**Por qué:** `str.split()` de Python considera whitespace al U+00A0 y lo parte igual que a un
espacio normal. `quiebra()` tokenizaba con `texto.split()` y volvía a unir con `" ".join(...)`,
así que el carácter ni siquiera sobrevivía hasta el HTML. El motor llevaba **desde siempre**
ignorando en silencio el único mecanismo que existe para decir «esto no se separa» — y como no
avisaba, la única forma de enterarse era comparar contra la versión anterior y ver que no había
cambiado nada.

**Arreglo:** un helper `palabras(t)` que corta con `re.split(r"[ \t\r\n]+", …)` — espacio, tab
y salto de línea, nada más — usado en el tokenizador y en los tres castigos de `quiebra()` que
cuentan palabras (conector al final, huérfana sola, primera línea de una palabra). Un par unido
por espacio duro cuenta como UNA palabra, que es lo que es para el ojo.

Efecto medido: de las diez bajadas del lote solo cambió la que estaba mal. Las otras nueve,
idénticas al píxel.

### Las dos morales

1. **Una función que ignora su entrada en silencio es peor que una que falla.** Si el spec trae
   un carácter con significado tipográfico y el motor lo descarta sin decir nada, el que escribe
   el copy cree que puso una regla y no puso nada. Vale para el espacio duro, el guion de no
   separación (U+2011) y el `<wbr>`.

2. **El diff contra la versión anterior no es solo para cazar regresiones: es lo que detecta que
   un arreglo NO hizo nada.** Sin ese diff yo habría entregado los cinco convencido de haber
   arreglado el quiebre, con el defecto intacto. Un cambio que no mueve un solo píxel es una
   señal, no un alivio — o el arreglo era innecesario, o no se aplicó.

⚠️ **Pendiente de portar a `templates/engine.py`**, igual que la guarda de §22: el motor único
tokeniza con `.split()` en `quebrar()` y tiene exactamente el mismo agujero.

---

## §25 — Las 8 horas no se fueron generando (6-ago-2026 · Marca Verde)

El director creativo, después de la medición de las 255 generaciones: *"como puedo arreglar
esas dos cosas? 1) Exceso de creación de imágenes con Higgsfield. 2) Exceso de
tiempo que se demora (quizá los jueces son muy estrictos con las imágenes)."*

La hipótesis era razonable y **la medición dice que no**. Vale escribir las dos
mediciones porque cada una apunta a un arreglo distinto del que uno supondría.

### Dónde se fue el reloj

Libro de transacciones de Higgsfield, sesión del 5-ago 14:37 → 23:08 (hora de
Chile), agrupando las generaciones en ráfagas (corte: hueco > 90 s):

| | |
|---|---|
| Generaciones | 190 |
| Ráfagas (viajes de ida y vuelta al modelo) | 32 |
| Reloj total | 8,5 h |
| Suma de los huecos ENTRE ráfagas | 8,4 h = **99% del reloj** |

Las ráfagas mandan 11-12 imágenes **en el mismo segundo**. Generar no es el
cuello de botella: lo caro es el viaje, no la imagen. Cuatro huecos concentran
6,1 de las 8,5 h — y dos de ellos (158 min y 70 min) son la pausa por tokens
agotados que pidió el propio el director creativo, **no el pipeline**. Etiquetarlos como
"lentitud del proceso" habría sido inventar.

### Lo que sí es el pipeline: la ráfaga inicial

| Tramo | Ráfagas | Generaciones |
|---|---|---|
| **14:37 → 15:48 (71 min)** | 15 | **147 (77%)** |
| 15:48 → 23:08 (7,3 h) | 17 | 43 |

**El 77% de todo lo generado salió en los primeros 71 minutos, antes de que
ningún juez viera una sola imagen.** De eso quedaron 21 crudos. No fue mal
criterio al elegir: fue generar el catálogo primero y mirar después.
→ arreglo: **dos tandas** (una imagen por slide → auditar → tanda buena),
Fase 4. Una tanda de prueba de 5 imágenes cuesta 10 créditos y contesta lo
mismo que 147.

### Los jueces no eran el problema — pero corren tarde

`_qa-receipt.json` de c1, ronda 3: **22:31–22:40, nueve minutos** para 4 agentes
independientes sobre 2 carruseles. Tres rondas ≈ 30 min de 8,5 h. Y sus 5
bloqueos no fueron exigencia estética: 1 bug del motor (preset de otro cliente),
3 de copy/compliance, **1 solo de imagen** — y ese era una contradicción
semántica real (`s-03`, §7.b de `prompts-fallidos.md`), no un capricho.

Además los 6 carruseles congelados murieron en la compuerta de **copy** (15:17),
no en la de imagen: aflojar los jueces de imagen no habría salvado ninguno.

Y la razón de fondo para no tocarlos, textual del recibo: *"El auto-wrap parte
los `<em>`… Los DOS jueces lo encontraron por separado. Es E3 y ninguna
compuerta lo ve."* Los jueces cazan justo la clase de defecto que ningún script
puede ver. Bajarles la vara no compra horas: compra defectos publicados.

**Lo que sí era cierto de la intuición del director creativo:** los jueces corren **tarde**,
con la pieza ya compuesta, así que todo lo que cazan cuesta regenerar +
recomponer + re-juzgar. El arreglo no es aflojarlos: es **mover el chequeo
imagen-vs-mensaje a la Fase 4b**, sobre el crudo, donde cuesta una línea de
prompt.

### La moral

Cuando algo tarda, la intuición culpa al paso que se *ve* trabajar. Los jueces
se ven trabajar (escriben veredictos largos); las 15 ráfagas de las 15:00 no se
veían en ninguna parte. **Medir primero cambió el arreglo entero**: la respuesta
no estaba en la fase que se sospechaba.

---

## §26 — La regla que existía hace un mes y se cumplía a veces (6-ago-2026 · Marca Verde)

El director creativo, describiendo cómo *debería* funcionar: *"la skill entiende de qué será el copy y ve
cómo lo dispondrá en la imagen; genera una imagen con Higgsfield indicándole dónde estará el
texto, para así no poner nada ahí; luego ver el juez que esté bien. ¿No se está haciendo así?"*

Lo que encontré al ir a mirar, y por qué la respuesta honesta era *"a medias"*:

| | |
|---|---|
| ¿El `zone` está decidido antes de generar? | **Sí** — las 5 slides de c1 lo tenían |
| ¿La regla de pedirle el hueco a Higgsfield existe? | **Sí**, y es suya: corrección del 7-jul-2026, `produccion-imagenes.md` §112, con el matiz fino de que el hueco es *continuidad de escena*, nunca `"empty black"` |
| ¿El prompt quedaba guardado? | **No.** `prompt_guardado=NO` en las 5 slides |
| ¿Algún gate miraba el prompt antes de generar? | **No** |

O sea: la regla era **prosa que el agente tenía que acordarse en pleno vuelo**, y después no
quedaba rastro de si se había cumplido. Y la compuerta que mide el mismo hueco —`verify.py raw`,
§0.2— corre **después de generar**: cuando falla, la generación ya está pagada.

### El arreglo

`templates/prompt_zona.py` + `verify.py prompt` + `_prompt-receipt.json` exigido por la puerta
GENERAR. Tres decisiones que valen aparte:

1. **La cláusula se DERIVA, no se recuerda.** `armar` la calcula desde `COLUMNAS` y `MARGEN` —
   los mismos que usa `engine.py`. Para `zone: "l"` sale *"subject in the RIGHT portion, leaving
   the left 52% (from 6% to 58% across) as open negative space…"*. Si mañana la columna cambia
   de ancho, la cláusula cambia sola: no hay una segunda copia que se desincronice.
2. **El prompt se guarda en el spec** (`slides[].prompt`). Sin eso no hay nada que verificar, ni
   nada que reusar cuando el mismo encuadre sirve otra vez.
3. **`"empty black space"` es FAIL, no warn.** Es la frase que produce medio rectángulo muerto
   pegado a la escena y parte la foto en dos. Ya costó un lote; no merece un warn.

### La moral

**Una regla escrita en prosa se cumple cuando el agente se acuerda; una regla con recibo se
cumple siempre.** Es el principio rector de la skill —*la IA razona, lo determinista hace
cumplir*— aplicado al único lugar donde todavía no estaba: el prompt. Y es la **única compuerta
del pipeline que corre sobre algo que todavía no se pagó**. Todas las demás miden después.

---

## §27 — El tope que frenaba la ráfaga siguiente (6-ago-2026 · Marca Verde)

El director creativo: *"¿debería poner un límite de creación de imágenes?"* Ya había uno —`slides × 3`,
puesto el día anterior— así que la pregunta útil era **si el que había servía**. No servía, por
tres motivos, y ninguno era el número.

### 1. Frenaba la ráfaga siguiente, no la que se pasa
El chequeo era `gastado >= tope`. Con el contador en 14 y tope 15, **una batch de 24 pasaba
entera**: el hook corre antes de la llamada y solo miraba el pasado. Y la ráfaga más grande del
lote real fueron exactamente **24 imágenes de un saque**. Ahora evalúa `gastado + pide`.

### 2. Contaba imágenes, y las imágenes no cuestan lo mismo
12 generaciones con `gpt_image_2` son **144 créditos**; 12 con `nano_banana_pro`, 24. El contador
las sumaba igual. En el lote Marca Verde ese renglón fue el **20% del gasto total** sin mover el
contador un punto. Ahora hay un techo de créditos en paralelo (`tope × 2 × 1.25`).

### 3. Era ASK, y desatendido un ASK no frena nada
Se había puesto ASK "porque hay carruseles que legítimamente necesitan más". Cierto — pero el
momento en que el tope importa es **justo** el desatendido, donde nadie contesta el ASK. Ahora
es DENY con escape auditable: `costo.py presupuesto <carpeta> N --por "<motivo>"`, que deja el
cambio fechado en `presupuesto_historial`. **Bajar el tope no pide nada; subirlo sí.**

### El número, medido contra lo que pasó de verdad

| tope/carrusel | se habría frenado en | ahorro sobre 190 generaciones |
|---|---|---|
| 10 | ráfaga 4 | −77% |
| **15 (el actual)** | **ráfaga 5, 15:11 h** | **−64%** |
| 20 | ráfaga 7 | −56% |
| 30 | ráfaga 13 | −29% |

**El 15 por defecto ya alcanzaba.** No faltaba un número más chico: faltaba que se cumpliera.

### El hallazgo que valió más que el tope

Probando el techo de créditos apareció un `NameError` en `presupuesto()` (escribí `TI` donde la
variable era `ti`). El hook murió, no emitió JSON, y Claude Code **interpretó el silencio como
«sin objeción»**: los cuatro casos de prueba salieron `ALLOW`. O sea que **un bug en cualquier
compuerta abría todas las demás de esa puerta** — el peor modo de falla posible para algo cuyo
trabajo es no dejar pasar, y completamente invisible porque el síntoma es que todo funciona.

Arreglo: `sys.excepthook` → `ask()` con la traza adentro. **Un gate que se cae, se cae cerrado.**
Verificado inyectando un bug a propósito: ASK con el `NameError` en el mensaje.

### La moral

Un límite tiene tres partes y sólo una es el número: **qué mide** (imágenes ≠ plata), **cuándo
mira** (antes del gasto, no después) y **qué pasa si se rompe** (cerrado, no abierto). El número
era el que estaba bien.


---

## §28 · El tope cuidaba la plata; nadie cuidaba el reloj (6-ago-2026)

**El director creativo, después de que le mostré el tope de imágenes:** *"pero no entiendo, ahora no cambiamos
nada, si es que mando a hacer 10 carruseles ¿volverá a demorarse horas? ¿o cambiaste algo para
que no pase de nuevo?"*

La respuesta honesta era **no**: había arreglado el gasto, no el reloj. Y peor — un tope de
gasto **sin** arreglar el reloj cambia horas por menos imágenes, que es el peor de los dos
mundos.

### La medición que lo separó en dos

La sesión del 5-ago (14:37 → 23:08) no fue un solo tramo lento. Fueron dos, con
comportamientos opuestos:

| Tramo | Ráfagas | Generaciones | Media | min/ráfaga | ¿Arreglado? |
|---|---|---|---|---|---|
| 14:37 → 15:48 · exploración inicial | 14 | 135 (**77% del día**) | 9,6 | 5 | **Sí** — el tope corta en la ráfaga 5 |
| **15:48 → 17:40 · iteración** | **11** | **41** | **3,7** | **10,2** | **No — era el hueco** |

**5 de esas 11 ráfagas fueron de UNA sola imagen.** 41 imágenes costaron 112 minutos: el bucle
*mirar → no gustar → regenerar → esperar 10 min → mirar*. Proyectado a 10 carruseles: **~27
ráfagas × 10,2 min ≈ 4,6 h sólo iterando fotos.**

### Por qué ningún tope lo caza

Porque **cada pedido es chico y barato**. El tope pregunta *¿cuánto llevás gastado?*; acá el
problema es *¿de a cuánto lo pedís?*. Una ráfaga de Higgsfield manda 11-12 imágenes **en el
mismo segundo** — el costo de reloj es **el viaje, no la imagen**. Doce viajes de una imagen
cuestan doce esperas; un viaje de doce cuesta una.

### El arreglo

Prosa en `SKILL.md` (*"Regla de LOTE — todas las slides de una fase juntas, nunca de a una"*)
**más su recibo**: `goteo()` en `carrusel-gate.py`. Lee el `eventos[]` que `_costo.json` ya
venía guardando (con timestamp y tamaño de cada ráfaga — el dato estaba, nadie lo miraba),
cuenta cuántas ráfagas de ≤2 imágenes se encadenaron, y a la **tercera** pregunta.

Tres decisiones con su razón:

- **ASK, no DENY.** Hay regeneraciones sueltas legítimas (la última slide que no cerró, un
  pedido puntual del director creativo). Lo que no puede pasar es encadenar cinco sin que nadie lo note.
- **Se dispara con el patrón, no con la primera.** Una ráfaga chica no es un problema; cinco
  seguidas son 50 minutos.
- **Un pedido de >2 imágenes pasa siempre**, aunque venga de una racha de chicas. Es exactamente
  la conducta que se quiere premiar: juntar las correcciones y mandarlas juntas.

Verificado en 6 casos (4 chicas + 1 → ASK · mismo historial pidiendo 8 → pasa · 2 chicas → pasa
· una ráfaga de 12 corta la racha → pasa · sin historial → pasa · 6 chicas → ASK contando 6), y
con `goteo()` roto a propósito → ASK, no fail-open (§27).

### La moral

Las siete compuertas medían **calidad** y la octava medía **plata**. Ninguna medía **tiempo** —
y el tiempo era lo que el director creativo estaba reclamando. Cuando alguien dice *"se demoró muchísimo"*,
la pregunta no es qué fase apretar sino **qué no está midiendo nadie**. Corolario de §25 (los
jueces no eran el cuello de botella) y de §26: una regla escrita sin recibo se cumple cuando
el agente se acuerda — que es justo cuando no.

---

## §29 · El plan se escribió para justificar las fotos (6-ago-2026)

**El director creativo:** *"necesito que la skill sea más rápida, siento que hacer 10 carruseles no puede
demorarse horas."*

Tiene razón. Y la causa no era ninguno de los tres sospechosos que ya habíamos investigado.

### Lo que se midió

48 recibos de `verde-ads/carruseles-2026-08-venta/`, por mtime. El hallazgo:

| Pieza | 1er crudo generado | brief + blueprint escritos | Diferencia |
|---|---|---|---|
| c1 | **14:46** | 17:03 | **+2,3 h** |
| c2 | 16:49 | 17:03 | +0,2 h |
| c3 | **04-ago 23:47** | 17:03 | **+17,3 h** |
| c8 | 15:20 | 17:03 / 17:16 | +1,7 h |

**En los cuatro carruseles se generaron imágenes antes de existir el plan.** El brief y el
blueprint se escribieron a las 17:03 — todos juntos, en la misma tanda — para fotos que ya
llevaban horas en disco. Eso no es planificar: es documentar hacia atrás.

Consecuencia medida: **18 vueltas atrás** a fases ya pasadas (c1: 6 · c2: 5 · c3: 3 · c8: 2),
cada una con su re-verificación y su re-render.

### El contraste que lo prueba

El copy de **7 carruseles** (c4-c10) tomó **10 minutos** — 15:07 el gate mecánico de los 7,
15:17 el panel de los 7. Corrido en lote y en orden, el texto de siete piezas cuesta lo mismo
que el de una.

Las 4 piezas que se hicieron "cada una de punta a punta" se llevaron el día. **La diferencia no
fue la dificultad: fue el orden.**

### Por qué una foto anterior al plan es cara

Porque **no ahorra trabajo: lo compra**. Cuando la foto existe primero, el blueprint se escribe
para que le calce, el copy se acomoda a lo que la foto muestra, y cuando algo no encaja — que es
lo normal — se regenera. El plan deja de ser una decisión y pasa a ser una justificación. Las 18
vueltas atrás son exactamente eso: decisiones que el orden correcto habría tomado gratis, en
texto, antes de pagar una sola generación.

### El arreglo

**Prosa:** sección "MODO LOTE" en `SKILL.md`, antes de la Fase 0, con las cuatro reglas
(columnas y no filas · ninguna imagen antes del blueprint del lote · las fases 0-3 van en
paralelo porque son texto · el reloj lo fija el nº de ráfagas, no el de slides) y la tabla de
tiempos esperables: **~2 h para 10 carruseles**, de las cuales ~1 h es espera de Higgsfield y
no se puede comprimir.

**Recibo:** `templates/orden_lote.py`, enganchado en `verify.py lote`. Mide tres cosas sobre la
carpeta madre: imagen-antes-del-plan (**FAIL**), vueltas atrás (WARN) y % de trabajo corrido en
lote (WARN si <50%). Corrido sobre el lote real reproduce la medición: 8 casos, 18 vueltas, 52%.

**FAIL solo para lo primero**, y a propósito: volver atrás tiene motivos legítimos (director creativo
cambia un copy, un juez encuentra algo real). Pagar una generación antes de saber qué tiene que
mostrar, no.

### El bug que casi invierte la compuerta

La primera versión marcaba "vuelta atrás" en un lote **perfectamente ordenado**. Causa: los
recibos de una misma tanda comparten mtime al microsegundo, y el desempate lo daba el orden del
sistema de archivos, no el del trabajo. **La compuerta habría castigado justo la conducta que
quiere premiar** — correr la fase para todas las piezas juntas. Arreglado con un margen de 90 s:
solo cuenta como vuelta atrás si pasó tiempo real. Verificado en los dos sentidos (lote limpio →
PASS sin warns · vuelta atrás real de 10 min → detectada).

### La moral

Llevo tres entradas seguidas buscando el tiempo perdido en el lugar equivocado: los jueces
(§25), el gasto (§27), el tamaño de las ráfagas (§28). Las tres mediciones eran correctas y
ninguna era la causa principal. **El reloj no se fue en ninguna fase: se fue en el ORDEN entre
fases** — y eso no se ve mirando una fase por vez, que es justo lo que hacía cada investigación
anterior. Cuando el síntoma es "todo tarda", la unidad de análisis no es la fase: es la
secuencia.

---

## §30 · Nueve rondas contra un tope de dos (6-ago-2026 · Marca Crema, lote `990-x10`)

**El director creativo:** *"no entiendo porque si se supone que tengo un limite de iteraciones, ahora no se
respetó"*.

Tenía razón, y la respuesta es más sencilla y más fea de lo que parecía: **el límite existía
solo como frase**. Estaba escrito en tres archivos —`COMPRENSION.md:44`, `COPY.md:247`,
`SKILL.md:549`— desde julio. El lote `990-x10` hizo **9 rondas de panel de comprensión**.

### Por qué nadie avisó

`"ronda": 9` es un número que el agente escribe **a mano** en `_copy-receipt.json`. Nada lo
incrementa y nada lo lee: `carrusel-gate.py` verifica que los recibos existan, que el hash
cuadre, que estén frescos y que haya 2 jueces — la palabra `ronda` no aparece en ninguna de sus
líneas. Para todo el sistema automático **la ronda 9 y la ronda 1 son idénticas**.

Costo medido sobre el transcript de la sesión (5-ago 11:13 → 6-ago 00:48):

| | |
|---|---|
| Reloj total | 13,6 h |
| Pausas (incluidas las del director creativo) | 3,8 h |
| Trabajo efectivo | **9,8 h** |
| Dentro de herramientas | 3,5 h (Bash 135 min · agentes 53 · Higgsfield **1**) |
| **Yo pensando entre llamada y llamada** | **6,3 h — el 64%** |
| Llamadas a herramientas | **2.042** = 204 por carrusel |

De esas 9,8 h, ~3 se fueron en el bucle de comprensión. Generar las 50 imágenes costó **un
minuto** de llamadas.

### Lo que lo hacía sentir razonable

En cada ronda encontraba **algo real** que arreglar, así que cada ronda parecía avance. Lo que
nunca me pregunté fue lo único que importaba: *¿es la misma causa que la vez pasada?* Las
rondas 2 a la 9 fallaron todas por el mismo dato faltante — «cómo se cancela antes del día 6»,
que es un dato de producto que solo tiene el director creativo. Desde la ronda 3 la información nueva era
cero. **Sentirse productivo es exactamente cómo uno gira tres horas.**

### El arreglo

`hooks/rondas.py`, con la misma división que ya había probado servir en `costo-imagenes.py`:

    PostToolUse   ANOTA la ronda gastada       → nunca infla el número
    PreToolUse    FRENA contra el tope         → nunca se gasta la de más

Enganchado a `Task|Agent`, porque **la ronda se cuenta donde de verdad se gasta** — al lanzar
las lectoras o los jueces— y no donde yo me acuerde de anotarla. Cuatro decisiones con su razón:

- **Cuenta ráfagas, no agentes.** Las 3 lectoras de un panel son UNA ronda (hueco > 12 min).
- **No topa las compuertas deterministas.** Un desborde de 12px converge y se arregla en
  segundos; toparlo sería publicar la pieza rota. Solo se topan los bucles que dependen de
  criterio o de un dato que falta.
- **Misma causa dos veces = se para**, aunque quede cupo. Para que la regla pueda existir, la
  ronda 2 **exige que la causa de la ronda 1 esté declarada**: el hook no puede adivinar por qué
  falló un panel, pero sí puede cobrar la declaración como precio de la segunda ronda.
- **Topar no congela.** Se entrega marcado NO APROBADO con el recibo en FAIL. Congelar es lo que
  dejó 6 carruseles de Marca Verde esperando. Textual del director creativo: *«si el juez rechaza; se muestra
  el resultado final pero se menciona que no está aprobado»*.

Verificado en 12 casos: agente normal no se cuenta · ronda 1 pasa y queda anotada · las otras 2
lectoras del mismo panel no suman ronda · ronda 2 sin causa declarada → DENY · con causa → pasa
· misma causa → DENY **en la ronda 2, antes del tope duro** · jueces y comprensión cuentan
aparte · carpeta con espacios y tildes detectada · y el hook **roto a propósito → ASK**, nunca
fail-open (§27), mientras que del lado que anota el mismo bug falla en silencio sin romper la
corrida.

Dos bugs aparecieron probándolo, los dos del mismo tipo —**una función que devolvía algo
plausible en vez de fallar**—: el extractor de carpeta truncaba las rutas a 120 caracteres (las
de esta agencia llevan espacios, así que el match se comía la frase entera) y no anotaba nada; y
`misma_causa` daba 0,57 entre «falta el dato de cancelación» y «sigue faltando el dato de la
cancelación», o sea trataba la misma queja como dos causas distintas. Se arreglaron podando
palabras por los dos extremos hasta dar con la carpeta, y comparando raíces de 5 letras.

### La moral

Es la cuarta entrada seguida buscando el mismo reloj (§25 los jueces, §27 el gasto, §28 el
tamaño de las ráfagas, §29 el orden), y la lección se repite con otra cara: **una regla sin
contador no es una regla, es una intención.** El tope de imágenes se cumplió desde el día en que
tuvo quién lo contara; el de rondas llevaba un mes escrito y no se cumplió ni una vez. Cuando
El director creativo pregunta *"¿por qué no se respetó el límite?"*, la respuesta casi nunca es que alguien
lo olvidó: es que **nadie lo estaba midiendo, y acordarse no es un mecanismo.**

---

## §31 · La fase que existía y nunca se disparaba (6-ago-2026 · el embudo creativo)

**El director creativo:** *"creo que quizá sería mejor hacer un filtro creativo para la skill, es decir, que
me proponga 100 carruseles (copys) y yo elegir los 10 mejores, entonces cuando diga / quiero
hacer carruseles, se active la skill y me diga «cuantos quieres que te proponga»"*.

Lo pidió como una función nueva. **Ya estaba escrita.** `references/fase-menos-1.md` existe
desde julio, 104 líneas: la grilla deseo LF8 × familia de fórmula de titular, 2-4 candidatos
por celda generados en pasadas separadas, el corte **por celda y nunca top-N global**, el
generador y el selector en turnos distintos. Está completa y es correcta.

**Nada la llamaba.** Un prompt que dice *"hazme 10 carruseles para verde"* entraba directo a
la Fase 0, y la Fase 0 tenía escrito el permiso para saltársela: *"si el tema ya viene dado
(pedido del director creativo, campaña en curso), se arranca directo acá"*. Un pedido de 10 carruseles
**es** un tema dado. La cláusula que existía para no estorbar una pieza suelta terminó
cubriendo exactamente el caso que el embudo tenía que atrapar.

### Lo que costó no llamarla

El lote que abría con **seis hooks empezando con "Deja de"** salió de *"una semilla, hazme 10"*
— está anotado en el propio `fase-menos-1.md` como el caso que lo originó. Pedir N piezas de
una vez no produce N ideas: produce **N variantes de la forma que el generador se atreve a
defender**. El generador no explora, converge.

Y la evidencia del lado bueno también estaba medida: Marca Verde **80 → 16**, Marca Servicios
**100 → 8**. Cuando el embudo se corrió, funcionó. El problema nunca fue el método.

### Es §9 otra vez, con otra ropa

`carrusel.json` estaba especificado en el spec, lo necesitaban las 5 compuertas y las 4
puertas, y **79 de 81 carpetas no lo tenían** — porque ninguna fase mandaba a crearlo. Se
arregló el día que `verify.py init` pasó a ser el primer comando obligatorio.

Misma forma exacta: **una regla que ningún paso ejecuta no es una regla, es documentación.**
La diferencia entre las dos mitades de este archivo es esa — las reglas que se cumplen tienen
un comando o un hook detrás; las que se olvidan están escritas en prosa esperando que alguien
se acuerde.

### El arreglo, en tres capas

| Capa | Qué hace | Dónde |
|---|---|---|
| **Gatillo** | hook `UserPromptSubmit`: pedido en PLURAL + verbo de producir → inyecta las dos preguntas (¿cuántas ideas propongo? ¿cuántas producimos?) antes de que el modelo entre en Fase 0 | `.claude/hooks/embudo-creativo.py` |
| **Rastro** | campo `procedencia` en el spec: de dónde salió esta idea — archivo de ideas + celda de la grilla, o `pedido-directo: <lo que pidió el director creativo>` | `verify.py init` + `qa_brief` check 3b |
| **Cierre del atajo** | la cláusula "si el tema ya viene dado se arranca directo" ahora aplica **solo a una pieza**; con varios carruseles pasa por la Fase −1 | `SKILL.md`, nueva sección Fase −1 |

**Por qué en el hook y no como una línea más del SKILL.md:** una línea más del SKILL.md es
precisamente lo que ya había y no se cumplió. El hook corre **antes** de que exista carpeta,
spec o decisión — es el único lugar donde todavía se puede preguntar sin haber gastado nada.

**Por qué `procedencia` es WARN y no FAIL:** la compuerta dura es el hook. El campo es el
rastro para que la Fase 7 pregunte *"¿de dónde salió esta idea?"* cuando nadie la escribió. Y
un lote puede nacer legítimamente de un pedido directo — el director creativo pisa cualquier regla escrita
(jerarquía de mando #1), así que la única respuesta correcta del gate es marcar, no bloquear.

**Y solo en LOTE (≥2 carruseles hermanos):** el embudo existe para lo que el volumen rompe.
Exigirle procedencia a una pieza suelta sería el trámite que convierte una compuerta en
burocracia — el mismo error que el andamio con valores de relleno.

### Dos trampas que aparecieron probándolo

**`json.dumps` escapa los acentos.** `grep "¿Cuántas IDEAS"` sobre la salida cruda del hook no
matchea nunca: el JSON trae `á`. Estuve a punto de "arreglar" un hook que funcionaba
perfecto. La eval ahora decodifica antes de buscar, y el comentario que explica por qué está
escrito ahí mismo para que nadie lo vuelva a diagnosticar desde cero.

**El silencio de un `UserPromptSubmit` es ALLOW.** Acá eso solo significa "sin contexto extra"
—no desbloquea ninguna puerta—, pero la disciplina de §27 vale igual:
`sys.excepthook = lambda *a: sys.exit(0)`, y la eval D incluye el caso de romperlo a propósito.

### La moral

Antes de escribir una regla nueva, buscar si ya está escrita. Estaba, dos veces seguidas en
este archivo (§9 el spec, §31 el embudo). **Lo que faltaba no era la regla: era el paso que la
ejecuta.** Y ese paso casi nunca es prosa — es un comando obligatorio o un hook que corre antes
de que el modelo tenga la oportunidad de no acordarse.

---

## §32 · Una propuesta que no se puede leer, no se puede elegir (6-ago-2026)

> **El director creativo, cortando la corrida en la mitad:** *"nono, hay que arreglar la skill, en vez de
> que dé 'ideas' tiene que decir cada texto de cada slide."*

### Qué pasó

La Fase −1 corrió por primera vez de verdad (lote Marca Verde): 40 propuestas en 4 celdas, cada
una un hook de ≤12 palabras más un resumen de 2-4 líneas. El director creativo abrió el archivo y lo paró
antes de elegir nada.

**No fue un error de ejecución: la regla decía eso.** `fase-menos-1.md` línea 59, textual:

> *"Cada candidato: `celda`, `familia`, `hook` (≤12 palabras, una idea) y la idea en 2-4
> líneas. **Sin slides completos, sin primary text: es ideación, no Fase 2.**"*

O sea la fase estaba diseñada para producir exactamente lo que no sirve. Yo la escribí así
pensando en el costo — 80 candidatos con slides completas cuestan 4-5× más que 80 hooks.

### Por qué el resumen no sirve, con la evidencia de esta misma carpeta

Elegir un hook + dos líneas es **aprobar un carrusel que todavía no existe**. Lo que llega a
producción después no se parece a lo aprobado, y la conversación termina siendo "esto no era
lo que dije".

Pero el argumento fuerte es otro, y está medido acá al lado: **el desarrollo es donde el copy
se cae.** El lote frenado de agosto (`carruseles-2026-08-venta/`) tenía **hooks correctos** —
6 de 10 quedaron trabados por lo que pasaba en las slides 2-4: voz pasiva ("se preparan, se
guarda, queda lista"), el mecanismo nunca explicado, contradicción entre el titular y el
desarrollo. Un resumen de dos líneas **esconde justo esa parte**.

Y hay un efecto de segundo orden: escribir las cuatro slides es lo que obliga al generador a
**descubrir que la idea no cierra** — antes de que el director creativo la elija, no después.

### El arreglo

| Capa | Qué cambió |
|---|---|
| `references/fase-menos-1.md` | Se borró la línea prohibitiva. Cada candidato lleva `slides` (título + sub de TODAS) + `cta`. Formato literal escrito, y el nº de slides sale de `formatos.md`, no se inventa |
| `SKILL.md` (Fase −1 + mapa) | La pregunta ya no es "¿cuántas ideas?" sino "¿cuántas propuestas?", con el bloque 🔴 del carrusel completo |
| `.claude/hooks/embudo-creativo.py` | El mensaje inyectado dice "CADA PROPUESTA ES UN CARRUSEL COMPLETO" — el hook corre antes de que el modelo alcance a improvisar |
| `templates/deck_ideas.py` | Renderiza las slides en la tarjeta (s-01…CTA), parsea slides indentadas en MD y objetos `slides` en JSON, y **avisa cuántas propuestas llegaron sin slides** |
| `evals/README.md` (eval D) | Nuevo caso 1b: el hook debe exigir el carrusel completo |

### El volumen bajó; el ratio se quedó

Con slides completas cada propuesta cuesta 4-5× más, así que el default cambió: **lote chico
de 2-3 piezas → 10-12 propuestas** (director creativo, mismo turno), 4-6 → 20-25, 8+ → 40-60. El embudo
Marca Verde de julio era 80→16 (5:1) y el nuevo es 12→2 (6:1): **el ratio se mantiene**.

Eso es lo que hay que proteger. Lo que hace funcionar el embudo es **descartar mucho**, no
generar mucho — y 80 candidatos que nadie puede juzgar valen menos que 12 que sí.

### La moral

Una fase de selección se diseña **desde el que elige**, no desde el que genera. Yo optimicé el
costo de producir candidatos y en el camino dejé al que decide sin nada que leer. La pregunta
correcta al escribir una compuerta de elección no es *"¿cuánto cuesta generar esto?"* sino
**"¿alcanza esto para decir que sí?"**

---

## §33 · El generador cumplió la regla y el script la desconocía (6-ago-2026)

Al día siguiente de reescribir la Fase −1 para que cada propuesta trajera **el texto completo
de todas sus slides** (§32), corrí el primer lote real con el formato nuevo: 24 propuestas de
Marca Verde, 6 generadores en pasadas separadas. Al armar el deck:

```
ERROR: 0 ideas en IDEAS.md — revisa el formato (ver docstring).
```

Cero. Sobre un archivo de 24 propuestas correctas, completas y en el formato que la regla
manda. El primer reflejo —el peligroso— es "el generador escribió mal el archivo".

**No.** `references/fase-menos-1.md` dicta el formato canónico con encabezados:
`### D3-F1-a`, `**Celda:**`, `**s-01 ·**`, `↳`, `**Marca:**`. El parser de `deck_ideas.py`
seguía leyendo el contrato viejo — `## celda` + viñetas `- hook`. **El generador siguió la
regla escrita al pie de la letra; el desalineado era el script.**

Es exactamente la misma familia que §9 (`carrusel.json`: la regla existía, ninguna fase la
mandaba) pero con el signo cambiado: acá la regla mandaba, y la herramienta que la consume
nunca se enteró de que había cambiado. Ayer edité seis archivos para el fix de §32 —
`fase-menos-1.md`, el hook, `SKILL.md`, `deck_ideas.py`, las evals, este archivo. Toqué
`deck_ideas.py` para que **renderizara** slides. No revisé si sabía **leerlas** en el formato
nuevo, porque lo probé con fixtures que yo mismo escribí en el dialecto viejo.

> **La lección:** cuando se cambia el formato que un agente debe PRODUCIR, hay que correr el
> consumidor contra una muestra REAL del formato nuevo — no contra el fixture que uno escribe
> de memoria, que sale en el dialecto que uno ya tenía en la cabeza. Un test escrito por el
> mismo que cambió la regla hereda su punto ciego.

**Segundo hallazgo, en el mismo turno y solo por mirar el PNG.** Con el parser arreglado el
deck salió, y ahí se veía impreso, literal:

    Llega el día 20 y ya tienes <em>todo cuadrado</em>

`html.escape()` no distingue el destaque inline (regla del 5-ago) del contenido del usuario:
escapaba el marcado y el deck mostraba **los tags en vez del destaque**, justo en la fase donde
El director creativo tiene que juzgar cómo se va a LEER el titular. Se arregló con `con_destaque()` — escapa
todo y reabre solo el par `<em>…</em>`, que es marcado nuestro — más el CSS que baja el resto
del titular en vez de gritar el destaque (E-inline). El `<title>` y los atributos siguen con
escape estricto.

Las dos fallas se cazaron igual: **corriendo la herramienta y leyendo su salida renderizada.**
La primera reventó fuerte y era imposible de ignorar; la segunda pasaba todos los chequeos —
HTML válido, 24 propuestas, cero errores— y solo se veía mirando el PNG. Es §4 del AGENTS.md
otra vez: *ninguna pieza visual se declara lista sin leer lo renderizado*, y un deck de
selección **es** una pieza visual.

Arreglado en `templates/deck_ideas.py`: los dos dialectos de Markdown conviven (el canónico y
el de viñetas para notas a mano), con el docstring diciendo cuál manda y por qué. Regresión
verificada contra el deck viejo de 36 propuestas: sigue leyéndose.

---

## §34 · La compuerta que reprobaba su propia salida (10-ago-2026 · Marca Verde, lote de 2 estéticas)

`prompt_zona.py` tiene dos mitades: `armar` escribe la cláusula que reserva el hueco del texto, y
`verificar` (vía `verify.py prompt`) comprueba que el prompt la lleve. La cláusula que emite
`armar` termina así, palabra por palabra:

> *"…one continuous atmosphere with depth. **It is NOT a black block, NOT a flat panel**, no hard
> edge, no seam, no cut."*

Y la lista de venenos de `verificar` contiene `black (?:box|block|rectangle|band|bar)\b`, buscada
con un `re.search` sin contexto. O sea: **pegar la cláusula canónica hacía FAIL la compuerta.**

Las 21 slides del lote fallaron a la primera, las 5 carpetas en rojo, con el mensaje *«pide un
bloque muerto → sale la foto partida en dos»* señalando justo la frase que dice lo contrario.

**Por qué importa más de lo que parece.** Esta es la única compuerta del pipeline que corre sobre
algo que todavía no se pagó (§ Fase 4a). Una compuerta que no se puede pasar usando la
herramienta que la propia skill manda usar tiene un solo destino: que el siguiente la esquive
escribiendo el prompt a mano sin la cláusula — que es exactamente el fallo que la compuerta
existía para impedir. Un gate imposible no es estricto: es un gate que se va a saltar.

**Arreglo:** `_veneno_real()` en `prompt_zona.py`. Un veneno solo cuenta si NO viene precedido de
una negación (`not / never / no / avoid / without / nothing`, con artículo opcional) en los 24
caracteres anteriores. Distingue *"leave an empty black block"* (FAIL, sigue cazándose) de
*"NOT a black block"* (correcto, pasa).

Verificado con seis casos antes de dar por bueno el arreglo: la cláusula canónica pasa, el veneno
clásico (`empty black space`), el explícito (`place a black block at the bottom`) y `clean empty
area` siguen fallando, y las formas negadas con `no` y con `avoid` pasan.

**La regla general que deja:** cuando una compuerta busca una frase prohibida por regex, hay que
probarla contra el texto que el propio pipeline genera, no solo contra el error que se quiere
cazar. Un detector de frases sin manejo de negación reprueba justo a quien siguió la instrucción.

---

## §35 · La compuerta que el director creativo derogó (10-ago-2026 · panel ciego de comprensión)

**Qué se eliminó.** El panel de lectores ciegos que validaba que el copy se ENTENDIERA antes de
diseñar: reverse brief → ≥3 instancias del agente `copy-qa` leyendo solo el texto → síntesis →
`_copy-receipt.json` en PASS, exigido por `carrusel-gate` en las puertas GENERAR, ABRIR y
PUBLICAR. Corrió desde junio-2026.

**Por qué existía.** el director creativo reportó: *«la gente me dice que el anuncio no se entiende /
interpreta otra cosa»*. Esos anuncios los había aprobado él.

**Por qué se fue, con sus palabras.** *«Yo al inicio, cuando me propone los carruseles, ya vemos
que haga sentido»* y *«soy experto en marketing, si yo apruebo un copy es porque la gente lo
entenderá»*. Desde que la Fase −1 entrega cada propuesta con el texto de todas sus slides (§32),
él lee el copy completo antes de que se produzca nada. Se le presentó dos veces el
contraargumento —el dueño no puede medir su propia claridad, y el panel de agosto había cazado
un error factual y una lectura de privacidad— y reafirmó. Jerarquía #1: manda el director creativo.

**Qué costó mientras existía, medido.** 6 de 10 carruseles frenados en agosto en 0/7 (§ la regla
de degradar). En el lote de 2 estéticas: los 5 en FAIL con claridad 3,0 y motivación 2,5, y el
propio recibo diciendo *«datos de producto, no redacción»* — el panel reprobó por falta de datos
que el director creativo tenía, con el mismo veredicto que si el copy estuviera mal escrito. Nunca re-leyó
tras sus respuestas porque el tope son 2 rondas: el FAIL describía un texto que ya no existía.

**El defecto de diseño que nadie arregló a tiempo.** El panel mezclaba dos veredictos que son
distintos: *«no se entiende»* (problema de copy, debe bloquear) y *«falta un dato de producto»*
(pregunta para el dueño, no debería bloquear). Se propuso separarlos y mover el panel a la Fase
−1; el director creativo prefirió eliminarlo. **Si algún día se revive, revivirlo con esa separación.**

**Qué sobrevivió… unas horas.** `copy-craft-qa` heredó la exactitud factual — y el director creativo lo eliminó
el mismo día (§36). Hoy no queda ningún juez de texto. Y las heurísticas que el panel acumuló, que se movieron a
`COPY.md` § "Lo que el panel cazó mientras existió" para que no se pierdan con el método.

**El método completo, por si se revive.** Reverse brief por slide (qué mensaje DEBE dejar) →
≥3 lectores ciegos calibrados al público del brief, que leen SOLO el texto, sin imágenes y sin
saber qué se quiso decir → puntúan claridad, relevancia, credibilidad y motivación (mínimo 4 de
mediana) → una instancia en modo SÍNTESIS emite el veredicto → tope 2 rondas, contado por
`hooks/rondas.py`. Los lectores iban **sin herramientas de escritura**: un juez que puede
escribir repara en vez de juzgar.

**La regla general que deja:** una compuerta que no distingue *«esto está mal»* de *«nos falta un
dato»* termina castigando al que hizo bien su trabajo, y quien la sufre pide eliminarla entera en
vez de arreglarla. Un veredicto sin causa accionable es una compuerta a medio diseñar.

---

## §36 · Los dos jueces de texto, y B1 (10-ago-2026 · el director creativo)

Mismo día que §35, más tarde y en el mismo hilo. Le mostré, medido sobre los recibos reales del
workspace, **qué rechaza más cada juez**. Con ese dato en la mano eliminó dos cosas más.

### B1 baja de FAIL a WARN

**B1** —*«¿la imagen DEMUESTRA el mensaje o solo decora?»*— era el hallazgo nº1 del juez de
diseño: **24 de 100**. El director creativo: *«elimina eso de que la imagen no lo representa, si una slide
pasa eso, se puede perdonar»*.

Se implementó como **WARN, no como borrado**: se sigue anotando en el recibo (es la señal más
clara de que la foto no se generó PARA el plan) pero no reprueba la pieza. Sobrevive **una sola
excepción como FAIL**: que la imagen comunique **lo OPUESTO** al mensaje — el caso canónico del
cierre que decía *"no eliges una, las rotas, +16 disciplinas"* con la foto de una mujer sola
saliendo del gimnasio. Perdonar que decore no es lo mismo que dejar pasar que contradiga.

### `copy-craft-qa` eliminado

El director creativo: *«elimina esta copy-craft-qa»*. Con §35 ya fuera, **el carrusel queda sin ningún juez de
texto**. Lo único que corre sobre el copy es `verify.py copy` → `_copy-gate-receipt.json`, que es
un script: AI-tells, triadas, clichés, hook >12 palabras, estructura del primary text.

**Qué se perdió, con el número delante.** Su hallazgo nº1 no era la calidad sino **D1 — claims
que la marca no puede sostener: 19 de sus 47 hallazgos, el 40%**. Ejemplos textuales de sus
recibos:

- *«lista para el SII»* no equivale a ser emisor de DTE certificado
- *«La multa que ya no llega»* promete eliminar una multa que el producto no controla
- *«Marca Verde emite y ordena todo mientras tú vendes»* — «todo» es un absoluto insostenible

Se le advirtió que eso pasaba en un cliente **tributario**, con **14 anuncios ya rechazados** en
esa cuenta de Meta y la cuenta anterior inhabilitada. Decidió igual. Manda él; queda anotado, no
discutido. Se le ofreció mudar la parte de claims a `guardian-de-claims` sin devolver el juez.

**La lección de proceso, que es la que importa:** el juez se llamaba «craft» y en los hechos
funcionaba como **compliance**. Nadie lo notó hasta que se contaron sus hallazgos. Un agente cuyo
nombre no describe lo que de verdad hace se elimina por lo que dice el nombre, no por lo que
hacía — y se lleva puesto algo que nadie quería eliminar. **Nombrar el agente por su hallazgo
dominante, no por su intención de diseño.**

## §37 · El énfasis a mitad de línea se lee como otra tipografía (13-ago-2026 · Airā)

Lote Airā (cliente nuevo, extensiones de pelo). La referencia de la marca (post IG) usa
titulares Didone con una palabra de énfasis en bold itálica — **pero en su propia línea**
("¿QUÉ HACE QUE TU / *TAPE-IN* / SE VEA PERFECTA?"). Al replicar el patrón, el énfasis se
aplicó a mitad de frase y el salto de línea automático lo partió donde quiso: líneas con
palabras roman e itálicas mezcladas. El director creativo: *"pusiste distintas tipografías en la misma
línea"*. Y tenía razón: roman + itálica de la misma familia, en la misma línea, se leen
como dos fuentes.

**La falla de origen:** se copió el PATRÓN (palabra enfatizada) sin copiar la REGLA que lo
hace funcionar (el énfasis ocupa una línea completa). Cuando se toma una referencia visual,
hay que extraer la estructura, no solo el estilo.

**Fix aplicado:** los 15 titulares del lote recompuestos con `<br>` antes del cambio de
estilo. Regla permanente: `references/composicion-y-tipografia.md` §8.

Mismo lote, otras correcciones del director creativo que ya son regla de la marca
(`brand-brain/marca-pelo/estilo.md`): sin números de página "01/04" ni flechas rosadas
(la referencia las tenía y aun así las vetó — la referencia no se copia entera), y las
cajas de texto sobre foto nunca tapan la cara/cabeza del sujeto: van arriba o a ancho
completo.
