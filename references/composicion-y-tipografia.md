# COMPOSICIÓN Y TIPOGRAFÍA — cómo se pone el texto en piezas 1:1 (1080×1080; 4:5 opcional)

> Documento de referencia para skills de producción visual (carruseles, posts, ads).
> Todo lo aquí descrito fue validado en producción (lotes Marca Crema, jul-2026):
> 12 posts + 82 slides QA-doble-juez. Es norma, no consejo.
>
> **Qué legisla y qué no.** Esto es el **CÓMO**: dónde cae el texto sobre la imagen, cómo se lee
> la foto, cómo se quiebran las líneas, cómo se mide. Eso es transversal y aplica a todos los
> clientes. El **QUÉ** — tipografía, paleta, logo, CTA, tono, formato — lo fija el **brand-brain
> del cliente y MANDA siempre** (jerarquía de `SKILL.md`). Los valores concretos de §6.1 y §7
> (Montserrat, crema/beige/berenjena, anclas, gaps) son el sistema de **Marca Crema**: sirven de
> default cuando la marca no tiene ese dato definido, y el brand-brain los reemplaza cuando sí.
>
> **Fuente única.** Para composición y tipografía manda ESTE archivo. `SKILL.md` orquesta el
> proceso y `RUBRIC.md` es la rúbrica del juez; si alguno repite una cifra de acá, la de acá gana.

---

## 0. Principios rectores

1. **Una idea por slide.** Si hay dos ideas, son dos slides.
2. **La foto manda; el blueprint manda antes.** Primero se decide qué dice la slide y
   en qué zona va el texto; la imagen se elige/encuadra/genera PARA ese plan. Nunca
   "generar a ver qué sale y acomodar texto después".
3. **La cara es intocable.** Texto, scrims fuertes, pills y tarjetas: 0% de overlap con
   la cabeza/rostro. Sin excepción, sin borderline.
4. **Se mide todo.** Nada de "se ve bien a ojo": ancho de texto con la fuente real,
   rectángulos reales, máscaras de persona, gates deterministas. *La IA razona, lo
   determinista hace cumplir.*
5. **Legibilidad de teléfono.** Todo se juzga en un feed de iPhone: pisos de tamaño
   no negociables.
6. **Consistencia de sistema.** Los mismos roles, gaps, colores y anclas en todas las
   piezas del lote. La repetición de la estructura ES lo profesional.

---

## 1. Blueprint antes de producir

Por cada pieza/carrusel, ANTES de renderizar:

- **Copy final por slide** + qué debe entender el lector (reverse brief).
- **Zona de texto planificada por slide** (izquierda / abajo / arriba / centro-crema),
  rotada entre slides vecinas: dos slides seguidas NUNCA comparten zona.
- **Qué debe mostrar la imagen** (calce semántico): la foto REPRESENTA el mensaje, no
  decora. Si no existe foto que lo demuestre → otra foto o se genera.
- **Persona y reglas duras del cliente** (buyer persona, vetos: ej. sin trenzas, sede real).

---

## 2. Leer la imagen: el mapa de zonas

Antes de posicionar NADA, la foto se convierte en un mapa. Proceso:

1. **Máscara de la persona** con `~/bin/cutout foto.jpg mask.png --mask` (Vision de
   macOS, ~1s, local). También sirve para validar que la persona es quien debe ser.
2. **Clasificar cada zona del frame** (`photo_map.py`):
   - 🔴 **PROHIBIDO** — cabeza/cara (18% superior de la persona, dilatado) + eje central
     del torso (máscara erosionada) → **0% de overlap** con cualquier elemento.
   - 🟡 **TOLERANTE** — extremidades (persona − eje − cabeza) → ≤12% de roce y SOLO en
     esquinas de elementos. "Una esquina del codo sí; el eje central, no."
   - 🟠 **FOCO** — la luz principal (percentil 88 de luminancia) → las tarjetas NO se
     ponen sobre la luz; el texto encima de luz exige scrim fuerte.
   - 🟢 **LIBRE** — espacio negativo real → ahí vive el texto.
3. **Validar los boxes reales del layout contra el mapa** (`pm.check(elements)`):
   `MAPCHECK: FAIL` = no se muestra.
4. **Head-clear rápido:** con la máscara, la cabeza (18% superior + dilatación) debe
   terminar POR ENCIMA de la zona de texto planificada.

### La foto decide el arquetipo
| Situación de la foto | Arquetipo |
|---|---|
| Persona a un tercio, mitad limpia | Texto en la mitad opuesta |
| Persona arriba, zona baja limpia | Texto abajo (stack bottom) |
| Persona abajo, cielo/techo limpio | **Texto ARRIBA** (`*_top`) |
| Cuerpo entero, ocupa todo el alto | Zona oscura inferior **degradada** (A10) con el texto DENTRO; la persona se ve con cabeza + torso + acción arriba |
| Sujeto centrado sin hueco viable | Cambiar de foto o de arquetipo; NO forzar texto encima |
| Sin foto (ritmo/datos) | Slide crema tipográfica con tarjetas |

### ⛔ 3.1 · SIN PAGINADOR — regla universal (director creativo, 29-jul-2026)
**Ningún carrusel lleva el número de slide en la esquina** (`0X · 0N`, `1/6`, puntitos, ni
ninguna variante). Aplica a TODOS los clientes y a todos los formatos, no solo al preset v2 de
Pilates que ya lo había dejado fuera. Instagram ya muestra su propio indicador de posición;
el nuestro solo suma ruido de esquina y compite con el wordmark.

Lo que da cohesión al carrusel es el **wordmark en la misma posición en todas las slides** y el
sistema tipográfico, no un contador. Si un carrusel necesita señalar avance (una serie, un
paso a paso), eso va **dentro del contenido** —"Paso 2", "Episodio 1"— con la tipografía del
sistema, nunca como chrome de esquina.

### 💸 Diagnóstico BARATO primero — mover el texto, no regenerar la escena

*(Auditoría C2-s4, jun 2026. Se había perdido al migrar la skill; restaurada el 31-jul-2026.)*

Cuando se reporta **texto encima del sujeto**, el reflejo caro es regenerar la imagen. Está mal.
El orden correcto:

1. **MIRAR el PNG a tamaño completo UNA vez y razonar directo.** No adivinar, no pedirle otra
   ronda al juez, no confiar en el lint. Una lectura resuelve la duda en segundos.
2. **El fix por defecto es mover el texto al lado vacío** — un cambio de zona o de `align`, una
   línea de código, cero créditos.
3. **Regenerar la escena es el ÚLTIMO recurso**, y solo si el sujeto u objeto ocupa **ambas
   mitades**.

**No se queman generaciones para arreglar una posición de texto.** Es el mismo principio que el
tope de 2 reintentos por slide: el ciclo de regeneración no converge solo y cada vuelta cuesta.

### ⛔ El panel OPACO no es la salida (RUBRIC E10.b, corrección el director creativo 14-jul-2026)
Cuando el texto choca con la modelo, el orden es **fijo** y el panel opaco **no está en la lista**:

1. **Reencuadrar la foto** (apaisadas se panean en horizontal, verticales en vertical) — resuelve la mayoría.
2. **Angostar la columna de texto** para que TERMINE antes de la modelo.
3. **Bajar el título hasta su piso** (los pisos de `templates/constantes.py` no se negocian).
4. **Cambiar de foto.**
5. **Nunca** un panel opaco que sepulte media imagen. El velo se MIDE (§6.3 / RUBRIC E10) — no se "sube" como remedio anti-choque (orden unificado con SKILL Fase 5 y RUBRIC E10.b, 3-ago-2026).

Un roce del 3-6% no justifica pintar medio cuadro. El logo es **chrome de esquina**:
no se le exige el mapa de persona (exigírselo dispara fallbacks catastróficos por 20px).

### 🔴 Un titular apilado NO es un problema de texto: es un problema de ENCUADRE (director creativo, 1-ago-2026)

Cuando un titular sale partido en una palabra por línea —*"Empezaste / cinco / veces. / No fue /
por floja."*— el reflejo es tocar la tipografía. **Está mal.** el director creativo lo diagnosticó mirando la
comparación con Nano Banana:

> *"Cuando el texto queda cortado solo con una palabra, ¿no crees que acaso el error es la
> disposición de la imagen y dónde aparece la persona?"*

Exacto. El texto se apila porque **la persona no deja una zona ancha libre**, y el motor
—en vez de mover la imagen— apretaba la columna hasta 31% del lienzo, por debajo del piso del
40% que esta misma sección ya exigía. Nano Banana ganaba la comparación tipográfica por una sola
razón: **reencuadraba**, corría a la modelo y liberaba una banda ancha.

**Las dos reglas que salen de esto:**

1. **Piso duro de columna: 40% del lienzo (432px).** Nunca se angosta por debajo. Si una zona
   lateral no llega, esa zona no es candidata — que resuelva el reencuadre.
2. **Un resultado MALO dispara el reencuadre, no solo un resultado imposible.** Antes el motor
   reencuadraba únicamente si NINGUNA zona pasaba; si una pasaba mal, se conformaba. Ahora un
   titular de **más de 3 líneas** también manda a reencuadrar, y se elige el crop que produce
   menos líneas.

Resultado medido en el lote de prueba: 3 de 4 slides pasaron de 4-5 líneas apiladas a 2 líneas
limpias. La que no mejoró informa *"reencuadre no mejoró"* — y ahí la salida correcta es el paso
4 de E10.b: **cambiar de foto**.

### Encuadre primero: mover la IMAGEN, no el texto
Con foto existente, el layout se resuelve REENCUADRANDO (zoom + paneo): sujeto flush a
un borde (≤8% de aire muerto), zona de texto ≥40% del ancho y limpia (`framer.py`).
Si ningún encuadre lateral es factible → cambiar de foto o de arquetipo. Prohibido
dejar franjas muertas >15% del ancho sin contenido.

---

## 3. Arquetipos de layout (los que funcionan en producción)

1. **Foto + stack inferior** — pill/kicker → titular → bajada, anclado a `bottom:112px`,
   logo esquina sup-izq.
2. **Foto + stack superior** (`*_top`) — para personas en la mitad inferior; stack a
   `top:150px` con scrim invertido (fuerte arriba, transparente a ~60%).
3. **Zona de oferta** — franja oscura inferior por **degradado difuminado** (ver §6.3), nunca
   un bloque opaco, con TODO el texto dentro; la persona (cara + torso + acción) siempre
   visible arriba. El corte NUNCA tan alto que la persona quede "solo cara" (regla A10).
4. **Cierre/CTA** — titular + precio (elemento gigante) + condición + botón gradiente.
5. **Crema con tarjetas** — fondo crema, kicker, 2–3 tarjetas blancas radio 28.
6. **Texto protagonista (quotes)** — fondo crema, titular gigante centrado vertical.
7. **Dos tarjetas sobre foto** — etiqueta oscura + etiqueta crema (mito/realidad, vs).

Constantes en TODOS: logo esquina superior izquierda (claro sobre foto; versión
degradado/oscuro sobre crema, si no desaparece) · márgenes 64px. **Sin paginador** (§3.1).

---

## 4. Sistema tipográfico

### 4.1 Familia y jerarquía por PESO
Una sola familia variable (Montserrat en este sistema). La jerarquía es por peso:
- **Display/titular:** 800–900 (ExtraBold/Black).
- **Contexto/bajada:** 400–500 (Light/Regular/Medium).
- **Labels uppercase:** 800 con tracking amplio.
- Máximo 2 "voces" por pieza. Nunca una tercera familia.

### 🔴 4.1.1 · DESTAQUE INLINE: se resalta el fragmento, no el titular (director creativo, 5-ago-2026)

Pedido textual: *"si el título de la slide es «aprovecha tu oferta y entrena por tan solo 990»,
que haya texto en negrita pero solo algunas partes como «oferta» y «por tan solo 990» — que
destaque lo más relevante"*.

**La regla.** Todo titular de ≥5 palabras marca **un solo fragmento**: la oferta, la cifra, el
beneficio o el giro. El resto del titular queda de apoyo. Un titular sin destaque es aceptable;
un titular con **dos** destaques compitiendo, no — si todo destaca, nada destaca.

**El mecanismo, y por qué es al revés de lo que parece.** El titular ya vive en el peso máximo
de la familia (900). *"Más negrita" no existe*: no hay nada por encima del tope. El contraste se
crea **BAJANDO el resto**, no subiendo el fragmento.

```html
<!-- en carrusel.json, campo `titulo` -->
"titulo": "Ahorra <em>tiempo y dinero</em> con Marca Verde."
```
```css
.title em        { color: var(--accent); font-style: normal; font-weight: 900 }
.title:has(em)   { font-weight: 700 }   /* solo los titulares QUE traen destaque */
```

Tres propiedades que hacen que esto sea seguro y no un parche:

1. **`:has(em)` deja intactos los titulares sin destaque.** No hay migración ni riesgo de
   regresión en piezas ya aprobadas: si no hay `<em>`, no cambia nada.
2. **Sale más angosto que lo medido, nunca más ancho.** El motor mide todo a 900 (el peso más
   ancho) y el texto sin destaque renderiza a 700. La línea real es MÁS CORTA que la verificada,
   así que el destaque no puede provocar un desborde. La dirección del error es la segura.
3. **Doble señal: peso + color.** El fragmento sube a 900 *y* toma el acento de marca. A 360px
   (el thumbnail del test móvil) el peso solo no alcanza; el color sí se lee.

**Los tags NO son glifos.** `«<em>tiempo</em>»` mide ~9 caracteres fantasma más que `«tiempo»`.
Todo lo que MIDA un titular tiene que quitar los tags antes: el motor (`engine.py`, helper
`sin_tags`) y el gate de líneas (`qa_lines.py`, en `_lineas_de` — quita todo tag *menos* `<br>`,
que sí es un quiebre real del spec). El día que se agregó el destaque sin esto, `qa_lines`
reprobó cuatro carruseles por líneas que en pantalla entraban de sobra. Relato: `APRENDIZAJES.md` §18.

**Y el partidor de frases tiene que tolerarlos.** La regla madre §5.0 (frase nueva = línea nueva)
se aplica con un lookahead por mayúscula; si la frase siguiente arranca con un tag
(`Le pides las boletas. <em>Él las prepara.</em>`) el lookahead ve `<` y las dos frases quedan
pegadas en el mismo renglón. El patrón lleva `(?:<[^>]+>)?` antes de la mayúscula.

#### 🔴 4.1.2 · Un titular con `<em>` DECLARA sus saltos. Sin excepción.

**Un `<em>` partido por el auto-wrap es peor que no tener destaque.** El fragmento existe
para leerse como una unidad; cortado en la bisagra deja de ser una unidad y encima arrastra
huérfanas — `«…SII sin tu / OK.»`, `«Tú / apruebas.»`, `«Lo / revisas / antes de / que /
exista.»` (dos y tres caracteres, a 88-92px, en el elemento más grande de la slide).

Por eso, **si el `titulo` trae `<em>`, trae también sus `<br>`**. No se deja que el navegador
reparta: el reparto del navegador depende del ancho de la caja, y la caja depende de la foto,
que cambia. Un destaque solo se sostiene si el quiebre es una decisión, no un resultado.

El corte va **antes** o **después** del fragmento completo, nunca adentro:

```html
"titulo": "Nada sale al SII<br><em>sin tu OK</em>."      ✅ el fragmento entero en su línea
"titulo": "Nada se manda al SII <em>sin tu OK</em>."     ❌ el wrap decide, y partió «sin tu / OK.»
```

**Y esto el gate NO lo ve.** `qa_lines` valida los saltos *declarados en el spec*; un titular
sin `<br>` le llega como una sola línea larga y mide un texto que no es el que se pinta. El
día que se estrenó el destaque, las compuertas dieron PASS a seis slides con el fragmento
despedazado y lo cazaron los dos jueces a ojo. Mientras el gate no lea el DOM renderizado,
**declarar el salto es la única defensa**. Relato: `APRENDIZAJES.md` §18.

### 4.2 Pisos de tamaño (lienzo 1080 — SE VE EN TELÉFONO)
| Elemento | Piso | Típico |
|---|---|---|
| Titular héroe (≥1 por carrusel) | **90px** | 95–120 |
| Título secundario | 64px | 64–84 |
| Cuerpo / bajada / lead | 36px | 36–42 |
| Badge / pill / kicker | 27px | 27 |
| Botón CTA | 32px | 34 |
| Meta / caption | 26px (piso absoluto) | 26 |

**Si el texto no cabe al piso, se acorta el copy — NUNCA se encoge la fuente.**

**90 es el piso del HÉROE del carrusel, no el piso de cada slide.** El carrusel necesita además un **salto de escala**: la slide que
manda lleva el titular claramente por encima del resto (RUBRIC E5 lo fija en ~104px / `t-xl`).
Un carrusel donde todos los títulos rondan los 90 se ve plano aunque pase el gate.
`qa_typesize.py` hace cumplir el piso de 90; el salto de escala lo juzga el ojo.

### 4.3 Tracking e interlineado
- Titular display: tracking **−0.02em** (apretado), interlineado **1.0–1.05**.
- Labels en MAYÚSCULA: tracking **+0.15–0.18em**, interlineado 1.0.
- Cuerpo: tracking 0, interlineado **1.25–1.42** (el texto chico necesita aire).
- Bajadas en ESTROFAS (frases separadas por línea en blanco si son varias), nunca
  párrafo corrido de 4 líneas.

### 4.4 Alineación y largo de línea
- Izquierda por defecto. Centrado solo en slides de sistema centrado (quotes, cards).
- Titular: 3–8 palabras. Cuerpo: 40–60 caracteres por línea.

---

## 4.5 El texto va DENTRO de la escena, no encima (jul-2026)

Un overlay HTML siempre queda perfectamente nítido y perfectamente plano: es lo que hace que
una pieza se lea como *"foto con sticker encima"* en vez de *"pieza diseñada"*. Esa era la
única ventaja real del texto horneado por IA — y **se recupera en HTML con la máscara que ya
tenemos**.

Con `~/bin/cutout foto.jpg mask.png --mask` (1 seg) se obtiene la silueta del sujeto. Además de
*prohibir* zonas, esa máscara sirve para **ocluir**: se pinta el titular y encima se recorta la
persona con la máscara, así el texto pasa **por detrás del hombro** como si perteneciera a la
escena — pero con la tipografía real de la marca y con el contraste medible.

```
capa 1: foto full-bleed
capa 2: velo adaptativo
capa 3: TEXTO
capa 4: la persona recortada con su máscara  ← el texto queda detrás
capa 5: EL MISMO VELO, recortado con la misma máscara  ← obligatorio, ver 4.5.1
capa 6: chrome (logo)
```

Sumar grano sutil y el mismo grade sobre la capa de texto termina de integrarlo.

### 🔴 4.5.1 · La capa 5 no es opcional: sin ella el recorte se ve como calcomanía (director creativo, ago-2026)

La capa 4 va **encima** del velo, así que le devuelve al sujeto la luz original mientras el
resto de la foto quedó oscurecido. Con un velo del 52% eso es un escalón de **37% de brillo
siguiendo exactamente su contorno**: la persona se recorta contra su propia foto y se lee como
sticker pegado. El director creativo lo cazó a ojo en `prueba-990/c3·s-05` — *«me aparece como con borde la
mujer»* — y el mapa de oscurecimiento lo confirmó: ratio 1.00 dentro de la silueta, 0.63 fuera.

**Ningún gate lo ve**: el contraste da PASS (el texto está sobre fondo velado), la tapa da 0%
(el texto pasa por detrás), `qa_dom` no mide fotografía. Es un defecto de integración, y los
defectos de integración los caza el ojo o no los caza nadie.

**El arreglo no es sacar la oclusión** —es lo que impide tapar una cara— sino **velar el
recorte igual que a la foto**: los mismos degradados, recortados con el mismo alfa.

⚠️ **La máscara CSS tiene que ir como `data:` URI, no como ruta.** Las máscaras exigen imagen
CORS-limpia y un `file://` cuenta como opaco: Chrome headless **descarta la regla en silencio**
y el render sale idéntico al roto, sin un solo error en consola. Medido con un div rojo:
`url('_mapa/c-05.png')` → cubre el 100% del lienzo; el mismo PNG como `data:` URI → 17,3%, que
es la silueta. Va solo el canal alfa en un PNG gris+alfa (44 KB contra 2,1 MB del recorte en
color): el color de una máscara no lo mira nadie.

**Cómo se verifica que quedó aplicado** — no a ojo, con el cociente de brillo contra el crudo:

```python
r = final / raw                     # por píxel, en luminancia
np.median(r[alfa > 0.9])            # dentro del sujeto
np.median(r[alfa < 0.1])            # fuera
# roto: 1.00 vs 0.63   ·   sano: los dos valores cerca (0.69 vs 0.63 en c3·s-05)
```
No dan idénticos y está bien: el velo es un radial, así que su fuerza depende de dónde caiga
el sujeto respecto del bloque de texto. Lo que importa es que **no haya escalón en el contorno**.

**Beneficio secundario:** con esto "el texto tapa la cara" se vuelve **imposible por
construcción** — la persona siempre queda por encima. Es la misma lógica del panel opaco
(bulletproof por capas) pero sin sepultar la foto.

**Cuándo NO usarlo:** cuando el sujeto ocupa la zona de texto entera (el titular quedaría
mayormente oculto) o cuando la máscara sale sucia. Ahí se vuelve al scrim normal.

> **Por qué HTML y no texto horneado** (decisión, jul-2026): ningún modelo reproduce una
> tipografía específica — aproxima, y deriva entre slides. Para una marca con sistema
> tipográfico eso es un defecto, no un ahorro. Y la legibilidad del texto horneado **no se
> puede medir ni corregir**. El texto horneado (Nano Banana Pro) se reserva para **piezas
> sueltas** donde el texto es un elemento gráfico y no la voz tipográfica de la marca.

---

## 5. Quiebres de línea (rag) — se deciden a mano

### 🔴 5.0 · REGLA MADRE: una frase nueva SIEMPRE empieza en otra línea (director creativo, 31-jul-2026)

**Después de un punto (o de `?` / `!`), la frase que sigue arranca en un renglón nuevo.** Nunca
dos frases compartiendo línea.

```
❌  Una sala. Dieciséis        ✅  Una sala.
    formas                        Dieciséis formas
```

**Que las líneas queden desparejas NO es problema.** el director creativo fue explícito: *"las frases pueden
quedar cortadas, lo importante es que después de un punto la siguiente frase comience en otra
línea"*. O sea: el rag parejo (regla 1, abajo) es preferencia; esto es **regla dura**, y cuando
chocan, manda esta.

Implementación: `engine.py` parte el titular **por frase** (`frases()`) y recién dentro de cada
frase balancea. Antes se balanceaba el titular entero como un bloque, así que un punto podía caer
a mitad de renglón. Es determinista — no depende de que el modelo se acuerde.

### El resto (preferencias, no reglas duras)

1. **Rag balanceado** — líneas de largo parecido ("Comienza a / entrenar hoy", no
   "Comienza a entrenar / hoy").
2. **Jamás huérfana** — ninguna línea final de 1 palabra si el sintagma tiene 3+
   ("tu clase / cuando tú / quieras" ❌ → "tu clase / cuando tú quieras" ✅).
3. **No cortar sintagmas** — la frase enfatizada va ENTERA en una línea; no terminar
   línea en conector ("y", "que", "de", "vs.").
4. Si no balancea → bajar 4–8px el tamaño (respetando pisos) hasta que quepa con sentido.

### ⚠️ Los `<br>` no bastan: el ancho del contenedor los pisa (test Claude Code, jul-2026)
Poner los quiebres con `<br>` **no impide** que el navegador agregue más si el bloque no cabe
en su `max-width`. Falla real: héroe a 112px en una columna de 560px → 3 líneas del spec
salieron **5**, con huérfanas (`tú.`, `cae`, `tu`, `que`) — y justo en los cuatro hooks de
apertura, que es donde peor se nota. Afectó 10 de 18 slides.

Dos reglas:
1. **Medir con `montwidth.py`** (la fuente real al peso real) que cada línea del spec entra en
   el ancho del contenedor. Si no entra: ensanchar la columna o bajar el tamaño — nunca dejar
   que decida el navegador.
2. **Chequeo determinista de líneas:** comparar `len(title)` del spec contra las líneas
   realmente renderizadas. Si difieren → FAIL. Es barato y caza el 100% de estos casos.

### ⚠️ La zona no se compara por etiqueta, se compara por posición
El check de "dos slides vecinas nunca comparten zona" debe medir **dónde cayó el texto en el
render**, no la clave del spec. Falla real: dos slides marcadas `top` y `l` (etiquetas
distintas → el check pasó) caían visualmente en **la misma esquina superior izquierda**.

---

## 6. Color, contraste y scrim

### 6.1 Roles de color
- Sobre foto/oscuridad: crema `#F7F6F2` (titular) · beige `#A0887C` (precio/énfasis) ·
  berenjena `#924B79` SOLO acentos (pill, bordes) · `text-shadow` suave para despegar.
- Sobre crema: tinta `#1E1E1E` · secundario `#606060` · berenjena para kicker/acentos.
- Dark de marca: `#131110` — **nunca negro puro**.

### 6.2 Contraste
- Mínimo 4.5:1 texto/fondo real (3:1 para large text ≥27px) — se valida contra el
  render, no contra el CSS.

### 6.3 Scrim (regla A10)
- **Degradado largo y difuminado**, nunca bloque negro de borde duro.
- Entra **desde el lado vacío** y se desvanece antes de la persona. Fuerte desde
  ~58–70% del alto.
- **Se mide POR LÍNEA, no por bloque** (test Claude Code, jul-2026). El percentil 80 de la caja
  completa da un promedio que miente: en c1-01 el bloque pasaba y la palabra `Copiar el`, que
  caía justo sobre una pantalla encendida, quedó en **1.4:1**. Y `ejecuta tareas` en coral sobre
  una pared taupe dio **1.35:1** con el bloque en verde. La luminancia se toma bajo **cada
  renglón renderizado**; el alfa lo fija la línea peor, no el promedio.
- **El acento coral no sirve como color de texto sobre fondos claros.** Como énfasis va sobre
  oscuro o se cambia a crema; el coral se reserva para kicker, pastilla y filete.
- **El alfa NO es una constante del template: se MIDE** (RUBRIC E10, corrección el director creativo
  14-jul-2026). Se toma la luminancia real de la foto bajo el bloque de texto (percentil 80)
  y se aplica solo el alfa necesario:

  ```
  A = 1 - 0.42 / L          # deja la zona del texto en ~0.42 de luminancia
  A = clamp(A, 0.14, 0.56)  # piso: anclaje mínimo · TECHO 0.56: la foto SIEMPRE respira
  ```

  Foto oscura (galpón, selva) → A ≈ 0.14, el velo casi no existe. Foto de casa con ventana →
  A ≈ 0.50. **Nunca un muro.** Si no se distingue qué hay al lado del texto, el velo está de más.
- **Una sola capa.** Prohibido apilar scrim + pozo de sombra + panel: se suman y ennegrecen
  (dos scrims de .92 y .62 dieron ~0.97 = muro negro). Si hay que cubrir todo el bloque de
  texto, el gradiente lleva una **meseta plana** hasta el final del texto y recién ahí se apaga.
- El corte NO puede ser tan alto que la persona quede "solo cara": siempre se ven
  cabeza + torso + brazos/acción.
- **TODO el texto DENTRO de la zona suficientemente oscura** y de los márgenes.
- Si el contraste no da con scrim honesto → el problema es el encuadre, no el scrim.
- Cuando el texto va arriba (persona abajo): scrim invertido (fuerte arriba → 0 a ~60%).

### 🔴 6.4 El halo del sujeto: sobre fondo plano, el velo NO puede quedarse solo (director creativo, 5-ago-2026)

> *"siento que está todo excelente pero que está muy plano el fondo, antes, cuando generabas
> los verde suaves, atrás ponías como una sombra o algo que era un verde más clarito."*

Tenía razón y es medible. **Glow medio en el fondo del compuesto final**, en niveles 0-255
(luminancia del fondo en el anillo que rodea al sujeto menos la del fondo lejano):

| lote | n | media | mediana | slides planas (<1.0) |
|---|---|---|---|---|
| julio 2026 (la vara) | 25 | **7.9** | 7.6 | 2 |
| corrida canónica 3-ago | 5 | 6.6 | 6.5 | 0 |
| lote 5-ago, antes del arreglo | 20 | **1.5** | 1.0 | **10 de 20** |

**Sobre foto real esto no aparece** — la foto ya trae su propia luz. Aparece cuando el fondo
es PLANO (mascota o ilustración sobre color de marca): ahí el único modelado que existe es el
que ponemos nosotros, y las capas de esta skill solo saben RESTAR luz. El velo direccional
`.g-*` llega a .96 de opacidad; medido slide por slide, del glow que traía el crudo (media
4.9) al compuesto sobrevivía 1.5 — **se perdía el 70% en composición**, sin que ninguna
compuerta lo viera, porque ningún gate mide "qué tan vivo está el fondo".

**Regla:** sobre fondo plano el motor pinta un **halo aditivo detrás del sujeto**
(`engine.halo_del_sujeto`, clase `.halo`). No es ornamento — E11.b prohíbe decorar para
satisfacer una métrica de densidad, y esto no rellena una banda vacía: **restituye el fondo de
marca** que la composición apagó. Se pinta solo si el fondo es plano de verdad (≥42% del cuadro
dentro de la tolerancia de color y un sujeto que ocupa entre 1.5% y 55%); si es una foto, la
función devuelve `""` y no toca nada.

Cuatro cosas que hay que respetar, cada una porque falló primero:

1. **El radio sale del SUJETO, no de un % del lienzo.** El look que el director creativo recuerda es un
   bloom que ABRAZA a la mascota, no una piscina de luz de media slide. Con radio fijo, el halo
   de una mascota chica queda disperso y el de una grande, corto.
2. **El color es el propio fondo aclarado, conservando el matiz** (`fondo + 52 + fondo*0.55`).
   Un gris encima no es "el mismo verde más claro": es suciedad.
3. **Va DEBAJO del velo direccional** (`z-index` 1, el velo es 2). Encima, c1 s-05 se fue a
   3.7:1.
4. **Y aun debajo del velo hay que apagarlo hacia el texto, con máscara de UN EJE.** El velo
   se desvanece a 0 en el 55% del lienzo y una columna `l-leftmid` llega al 64%: esa franja de
   texto queda sin velo encima y el halo se le cuela por debajo (3.9:1, otra vez bajo el
   mínimo). La máscara es `linear-gradient` a 0 sobre la caja y a 1 a 160px hacia el sujeto.
   **No se recorta el radio**: se probó y los radios exteriores cayeron de ~800px a ~200px, el
   glow volvió a 1.3 y el fondo quedó igual de plano que al principio. El radio ES el efecto.

Y lo que NO se hace, nunca: subir el velo para tapar el problema. **El velo se mide, no se
sube** (E10.b). Acá se corrige el halo, que es lo que sobra, no el velo, que ya está medido.

⚠️ **El halo se pinta TAMBIÉN sobre el recorte con el que se mide el velo**, antes de medirlo.
Si no, el motor dimensiona el velo contra una foto que ya no existe y el contraste se cae sin
que nadie lo vea hasta el gate.

⚠️ El halo arregla la mitad de composición. La otra mitad es de **generación** y vive en
`prompts-validados.md` §7.6: un prompt que prohíbe el glow entrega un crudo plano, y esto no
lo puede inventar.

---

## 7. Geometría y espaciado

- **Márgenes seguros:** 64px laterales, ≥48px verticales; nada cruza el borde.
- **Anclas fijas:** stack inferior a `bottom:112px` · stack superior a `top:150px` ·
  logo `left:64px; top:56px`. (No hay ancla de paginador: no se usa — §3.1.)
- **Gaps del stack (ritmo vertical constante):** pill → título +22px · título → bajada
  +16–18px · precio → botón +30px · tarjetas entre sí +20px.
- **Pills/badges: SIEMPRE auto-ancho** (solo `left/top`, nunca `width` fijo) — así el
  texto no puede desbordarlas.
- **Tarjetas:** radio 28px, padding 26–34px, sombra sutil; texto dentro con aire real.
- **Botón CTA:** gradiente de marca (`90deg beige→berenjena`), radius 100, padding
  20×52, sombra del color del acento.
- **Logo como imagen real** (SVG/PNG, nunca generado por IA): `svg{width:100%;height:auto}`
  dentro de su caja (sin esto, el SVG desborda y "se corre a la derecha").
- Texto sobre foto lleva `text-shadow` discreto; sobre crema no.

### 🔴 7.1 · `zoom`: acercar el encuadre cuando el sujeto queda chico (director creativo, 5-ago-2026)

*"Siento que la portada tiene mucho texto y poca imagen… podríamos hacer a la mascota más
grande."* Tenía razón y no había perilla: un crudo de 2048² sobre un lienzo de 1080² se usaba
**entero siempre** (`object-fit:cover` no recorta nada cuando las proporciones coinciden), así
que la mascota medía 4,6% del lienzo y la única forma de agrandarla era regenerar la imagen.

Ahora el spec acepta `"zoom": 1.5` por slide. Achica la ventana a `1/zoom` y la ancla en
`posx`/`posy` — la mascota vive casi siempre abajo a la derecha, o sea `posx: 1.0, posy: 1.0`.
Zoom 1.5 = el sujeto se ve **50% más grande de lado**, 2,25× en área.

```jsonc
{"n": 1, "foto": "raw/s-01.png", "zoom": 1.5, "posx": 1.0, "posy": 1.0}
```

Tres cosas que hay que saber antes de usarlo:

1. **Acercarse RECORTA.** Lo que sale del encuadre no vuelve. Después de subir el zoom se MIRA
   el PNG: el sujeto no puede quedar cortado por el borde. En Marca Verde c2 el zoom 1.7 cortaba la
   pila de papeles contra el borde derecho y 1.6 no — la diferencia no la ve ninguna compuerta,
   solo el ojo.
2. **El zoom pelea con el hueco del texto.** Al agrandar al sujeto, el sujeto sube y se come la
   zona planificada; el motor reacciona **reencuadrando en x**, y ese reencuadre puede llevarse
   al sujeto fuera de cuadro (c1: zoom 1.9 → `REENCUADRADA (x=0.30)`, la mascota quedaba en
   x 0.77–0.96 del crudo y la ventana terminaba en 0.67). Si el reporte dice REENCUADRADA,
   **bajar el zoom** hasta que diga `planificada`: ese es el techo real de esa foto con ese copy.
3. **No se compensa bajando el titular.** Achicar el héroe para hacerle sitio a la foto reprueba
   E5 (salto de escala; en c1, 100px < el piso de 104px). Si no entra, el techo del zoom es más
   bajo — o el que sobra es el copy, no el tamaño del título.

Techos medidos en el lote de venta de Marca Verde (ago-2026), sirven de punto de partida:
**1.5** con héroe de 120px y 3 líneas · **1.6** con titular de 90px y 4 líneas.

---

## 8. Medición real (la parte que todos saltan)

- **Ancho de texto con la fuente REAL al peso REAL** (`montwidth.py`): instancia la
  misma `.woff2` del render a 350 (light) u 800 (bold). Montserrat 800 es mucho más
  ancha que cualquier proxy → los quiebres calculados con otra fuente FALLAN en el
  render (texto que se monta sobre el CTA, caso real).
- **Rectángulos reales** (`qa_geom.py`): alto real de cada bloque por word-wrap al
  ancho de su caja + ancho real de pastillas → FALLA si algo sale del área segura,
  si el texto desborda su pill, o si dos elementos chocan (≥12px entre pastilla y texto).
- **Piso tipográfico** (`qa_typesize.py`): escanea TODOS los `font-size` (inline + style) →
  FAIL con cualquier texto <26px. El héroe ≥90px se exige **por CARRUSEL**, así que hay que
  pasarle **todas las slides en una sola corrida** (`qa_typesize.py s-*.html`): corrido en bucle,
  slide por slide, marca FAIL en todas las que no son la portada. Para chequear una sola a
  propósito, `--slide` (omite el chequeo de héroe).
- **Persona** (`~/bin/cutout` + `photo_map.py`): la cabeza nunca entra en la zona de texto.
  El *head-clear* del §2.4 **no es un script aparte**: es el chequeo de cabeza que hace
  `pm.check()` dentro de MAPCHECK. No hay binario `head-clear` que correr.

> **Intérprete:** estas herramientas necesitan `numpy`/`Pillow`/`fontTools`, que NO están en el
> `python3` del sistema (3.9.6). Correrlas con **`/usr/local/bin/python3`** o con el 3.13 del
> login shell — si no, salen `ModuleNotFoundError` y el gate parece "pasar" sin haber corrido.

---

## 9. Reglas duras (checklist previo a mostrar)

- [ ] Lienzo del spec (1080×1080 por defecto — regla de la casa, reconfirmada por el director creativo el 3-ago-2026; 1080×1350 solo si el spec pide `"canvas":"4:5"`), una idea por slide, nada <26px, ≥1 héroe ≥90px por carrusel.
- [ ] Cara 100% libre (nivel píxel, no estimado).
- [ ] Texto dentro de la zona oscura / tarjeta y de los márgenes; sin huérfanas.
- [ ] Scrim difuminado (A10), sin bloque negro duro; persona con cuerpo visible.
- [ ] Logo legible en su fondo (claro vs degradado), en su esquina, sin choques.
- [ ] Copy LITERAL (tildes incluidas) — si el cliente lo congeló, palabra por palabra.
- [ ] Precios/claims según reglas de marca (condición del precio, prohibidos).
- [ ] Calce semántico: la foto demuestra el mensaje; personas disfrutando.
- [ ] Vetos del cliente verificados con zoom (ej. sin trenzas).

---

## 🔴 9.1 · Un mockup de documento/interfaz se DIBUJA, no se genera (director creativo, 10-ago-2026)

El director creativo rediseñó el c1 de Marca Verde en Claude Design y cambió lo que yo hacía: los mockups de
factura, formulario y pantalla los armó **en HTML/CSS** — tarjeta blanca con `border-radius` y
`box-shadow`, y barras grises de 12-16px como texto simulado — en vez de pedírselos a Higgsfield.

**Tiene razón, y las razones son medibles:**

| | Mockup generado por IA | Mockup en HTML/CSS |
|---|---|---|
| Texto en inglés horneado | pasó en 2 slides de 21 (`Invoice`, `Total`, `Date`, `Client`) | **imposible** |
| Logo de terceros colado | pasó (`Google Ads` en la referencia) | **imposible** |
| Corregir una línea | regenerar, ~10 min de espera y créditos | editar y re-renderizar, segundos |
| Encuadre / hueco para el texto | hay que pedirlo en el prompt y verificarlo | es el layout, no se negocia |

**Regla:** si lo que va en la slide es una **interfaz o un documento** (factura, boleta, formulario,
tabla, chat, pantalla de app), se dibuja en HTML/CSS. Higgsfield es para **escenas** — personas,
lugares, mascota de marca — que es donde una IA aporta lo que el CSS no puede. Esto también
elimina de raíz la Fase 4b para esas piezas: no hay crudo que auditar.

### 9.2 · Y lo dibujado se mira al tamaño real, no en el canvas de diseño

Los dos defectos de su diseño **no se veían en el canvas** y aparecieron al render 1080×1080:

1. **El logo superpuesto cayó encima de un elemento del mockup.** Un `position:absolute` centrado
   sobre una tarjeta que ocupa el centro del lienzo siempre va a chocar: la tarjeta dejaba 245px
   de margen a cada lado y el logo mide ~150px de ancho, así que "centrado" es "encima". Se
   resolvió bajándolo al aire de abajo de la franja (y agrandando la franja de 352 a 406px).
2. **Un listón rotado dentro de `overflow:hidden` se recorta y lee mal.** «BORRADOR» rotado −45°
   dentro de la tarjeta salía como «ORRADOR». La mitad del ancho del texto se proyecta
   `±w/2·cos45° ≈ ±0.71·w/2` en X **y en Y**: hay que dejar ese margen en los dos ejes, o el
   recorte se come la primera letra. Igual que la regla de siempre: **se lee el PNG, no el
   editor** (§10).

---

## 10. Validación en capas

1. **Gates deterministas** (`qa_typesize` · `qa_geom` · MAPCHECK, que incluye el head-clear) —
   segundos, cazan el ~90%. Se itera contra ellos, no contra el ojo.
2. **Contact sheet + squint** (todo el lote en una lectura + fila gris/blur): si borroso
   no se entiende qué domina, la jerarquía falló.
3. **Lectura a tamaño completo** de cada pieza con foto nueva/pose nueva — la miniatura
   ESCONDE los roces.
4. **Doble juez independiente** (`carrusel-qa` ×2, sin compartir contexto) contra la
   rúbrica. Un FAIL de cualquiera = FAIL. Recibo `_qa-receipt.json` con `judges: 2`.
5. **Chequeo mecánico del copy** (`verify.py copy` → `_copy-gate-receipt.json` en PASS).
   Los dos jueces de texto que ocupaban este lugar se eliminaron el 10-ago-2026
   (`APRENDIZAJES.md` §35 y §36).
6. **Re-render = recibos vencidos** → re-verificar lo tocado antes de mostrar.

---

## 11. Errores reales que este sistema ya cazó (para no repetirlos)

- Texto 16–22px ilegible en iPhone → nació el piso determinista.
- Título calculado con Arial proxy que se repartía distinto en Montserrat 800 y caía
  ENCIMA del CTA → medición con la fuente real.
- Logo SVG sin `width:100%` que desbordaba su caja y "se corría a la derecha".
- Bloque negro sólido demasiado alto: la persona quedaba "solo cara" → regla A10.
- Entidades HTML (`&gt;`, `&amp;`) renderizadas literal en el titular → sanitizar DATA.
- Huérfana de 1 palabra ("$990." solo en la última línea) → quiebres manuales.
- Texto sobre la cara porque el sujeto invadía la zona → arquetipo texto-arriba / panel.
- Foto de persona con rasgo vetado por el cliente (trenzas) → verificación con zoom en QA.

---

## 12. Correcciones el director creativo 3-ago-2026 (lote prueba-990, Marca Crema)

1. **El pill/etiqueta de sección ("PRUEBA 5 DÍAS", "EN VIVO Y ON-DEMAND", "¿TE PASA?")
   va PEGADO al bloque de texto, justo encima de él** (gap visual mínimo, ~16-24px) —
   nunca flotando alto desconectado del contenido que nombra. Si el texto está abajo,
   el pill baja con él.
2. **En carruseles de oferta estilo Black Week, el "recuadro negro" (tarjeta oscura
   translúcida con logo + pill + precio) es el arquetipo de la PRIMERA slide**, no del
   cierre. La portada lleva la oferta dentro de la tarjeta; la última slide mantiene
   su propio cierre con CTA.
3. **La foto de portada no se repite NUNCA entre carruseles del mismo cliente** (no
   solo dentro de uno — A8 es intra-carrusel; esto es entre trabajos): antes de elegir
   la foto de s-01, revisar las portadas ya producidas/publicadas del cliente (Black
   Week usó la palapa → vetada como portada de este lote). Chequeo a ojo en el brief;
   pendiente hacerlo determinista en `qa_lote`.
4. **Las fotos deben mostrar ACCIÓN (haciendo deporte), no solo poses estáticas.**
   Al elegir del banco, priorizar tomas de movimiento (zancada, salto, clase en curso)
   sobre retrato posado; si el banco no tiene la escena, se genera con Higgsfield
   (cuando el MCP esté conectado) en vez de conformarse con la pose estática.
5. **En un lote de oferta, TODAS las portadas llevan el mismo arquetipo de oferta**
   (corrección el director creativo 3-ago-2026): la tarjeta oscura centrada con pill de oferta +
   hook + precio visible — no solo la del carrusel "de oferta". Cambian la foto y el
   ángulo del hook, pero la portada siempre lee "oferta" al primer vistazo y mantiene
   el texto centrado con el mismo estilo. El ángulo propio de cada carrusel se
   desarrolla en las slides medias. **La tarjeta de cierre (última slide) también va
   centrada**, nunca alineada a un lado (corrección el director creativo sobre prueba-990-2, s-05).
6. **Vocabulario Marca Crema (correcciones el director creativo 3-ago-2026):** se dice
   **"clases online y grabadas"**, NO "en vivo y on demand"; y la enumeración de
   disciplinas va como **"clases de yoga, fuerza, pilates y mucho más"** (sin "dance"
   suelto, con "y mucho más" de cierre).
7. **El precio en pastilla va LIMPIO (corrección el director creativo 3-ago-2026):** el "$990"
   berenjena sobre pastilla blanca NO lleva sombra (el morado con sombra blanca "queda
   sucio"). Texto sólido, sin text-shadow ni contorno. Y nada de elementos sueltos
   flotando bajo la tarjeta (un "·" huérfano, un punto decorativo).
   **Y la pastilla NO es pill redonda (corrección el director creativo 3-ago-2026, segunda pasada):**
   `border-radius:100px` se ve informal y el peso 900 con tracking distinto se lee como
   otra tipografía. Rectángulo formal: `border-radius` ~10px, **misma Montserrat y
   mismo peso que el título** (800), tracking neutro.
   **Tratamiento definitivo elegido por el director creativo (3-ago-2026, variante V4):** el precio
   NO va en pastilla blanca ni berenjena sólida — va con el **mismo tratamiento del pill
   de oferta**: fondo `rgba(146,75,121,.28)`, borde 1px berenjena `#924b79`, texto crema.
   Y **subordinado al título** (~58-60px en portada): el título domina, el precio
   acompaña. Aplica a portada y cierre de todo carrusel de oferta.
8. **Nunca mezclar roman + itálica/negrita dentro de la misma línea de un titular**
   (corrección el director creativo, 13-ago-2026, lote Airā): "Que tus extensiones *no se noten*"
   envuelto a mitad de frase deja palabras roman e itálicas en la misma línea y se lee
   como dos tipografías distintas. El énfasis va EN SU PROPIA LÍNEA — román una línea,
   itálica la siguiente ("Que tus extensiones<br>*no se noten*"), como hace la marca en
   sus posts. Al maquetar un titular con énfasis, el `<br>` va ANTES del cambio de
   estilo, nunca después de que la línea ya mezcló.

---

## §12 · Dos trampas del texto compuesto en HTML (1-sep-2026, lote Marca Verde)

### 12.1 Un `.woff2` de Google Fonts puede venir sin las letras que necesitas

Max rechazó un lote entero con *"tienes distintas tipografías… como si lo hubiese hecho alguien
que no sabe nada"*. Yo diagnostiqué que era culpa de la IA que horneaba el texto. **Lo era en
parte, pero había un segundo defecto y estaba en MI composición**: el `.woff2` que había bajado
pesaba **5.212 bytes** y **no traía la A mayúscula**. Chrome cayó al fallback en silencio, así
que «**A**provecha» y «OFERT**A**» salían en otra letra dentro de una pieza que yo mismo había
compuesto.

**Por qué pasa:** `fonts.googleapis.com/css2` devuelve la fuente **partida por unicode-range**
(latin, latin-ext, vietnamese…). Si copias UNA sola URL de ahí sin su `unicode-range`, te llevas
un subset arbitrario. El latin completo de Archivo pesa **34.940 bytes**: si tu archivo pesa
5 KB, te falta media fuente.

**Cómo se hace bien:**

```
curl -s -A "Mozilla/5.0 … Chrome/120" "https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;900"
```

y bajar **las URLs de todos los bloques que necesites**, declarando cada una con **su
`unicode-range` textual**. Para español bastan `latin` (que ya trae á é í ó ú ñ ¿ ¡, todo en
U+0000-00FF) y `latin-ext`.

**Cómo se caza antes de mostrar:** un fallback tipográfico **no da error**. La única señal es
mirar el PNG buscando una letra suelta con otro grosor. Regla: al bajar una fuente, **mirar el
tamaño del archivo** — un subset de <10 KB para una familia de texto es sospechoso, no normal.

### 12.2 Contra un borde diagonal, el ancho del titular se MIDE, no se estima

En la dirección neo-brutalista de Marca Verde hay una banda diagonal: el ancho disponible del
titular **cambia con la altura de cada línea**. Estimé «≈0,55em por carácter» y en la hoja de
contacto **4 de 6 piezas** tenían el titular cruzando el filo.

El método que sí funciona, dos medidas deterministas:

1. **El ancho del texto**, con Chrome: una página que carga la fuente real, mide con
   `canvas.measureText` a 100px y descuenta el `letter-spacing` (`-0.042em × nº de caracteres`),
   y devuelve el **ancho por px de font-size**. Se lee con `--headless=new --dump-dom`.
2. **El filo del fondo**, con Pillow: renderizar el fondo **solo** (sin texto) y, fila por fila,
   buscar el primer píxel que deja de ser blanco.

Con los dos números, el cuerpo máximo de cada pieza sale de una desigualdad, no de un ojímetro:
`margen_izq + ancho_por_px × fs + aire ≤ filo(y_de_esa_línea)`, con `aire = 16px`.

Resultado: el mismo cuerpo (60px) en las 6 piezas y ninguna tocando el filo. Y la pieza que no
cabía a ningún tamaño razonable (una línea de 21 caracteres) **no se achicó entera**: se le bajó
solo esa línea a 46px, convirtiéndola en la entrada de la frase. La restricción se resolvió con
jerarquía, no encogiendo todo.

**Corolario:** cuando una pieza tiene un fondo que invade la caja de texto (diagonal, foto,
degradado, sujeto), la caja segura es una **función de y**, no un rectángulo. Medirla cuesta dos
scripts y cero créditos.


## §13 · Un lote NO es la misma plantilla seis veces (Max, 1-sep-2026)

Entregué 6 posts con la dirección visual aprobada y Max los rechazó en bloque:

> *"PERO LOS HICISTE EXACTAMENTE IGUALES, DEBES CAMBIAR EL LA MASCOTA, COMO SE DISPONE EL TEXTO,
> ALGUNOS A LA IZQUIERDA, OTROS AL CENTRO, OTROS SIN LA LINEA DIAGONAL, OTROS CON OTRAS COSAS"*

**Lo que hice mal:** leí «dirección de diseño aprobada» como «plantilla aprobada». Escribí un
generador con UN template y seis titulares. Todas las compuertas dieron PASS —ninguna mide la
monotonía de un lote— y la hoja de contacto la miré para cazar defectos, no para ver que las seis
eran la misma imagen con otro texto.

**La regla:** una dirección visual es un **vocabulario** (paleta, tipografía, tratamiento del
destacado, lenguaje de sombras), no una **maqueta**. Dentro de la misma dirección, cada pieza de
un lote cambia al menos **dos** de estas tres:

1. **La estructura del fondo** — diagonal / corte horizontal / marco / círculo / franja superior /
   sin bloque.
2. **La posición del texto** — izquierda / centrado / alineado a la derecha / abajo.
3. **La pose del personaje o del sujeto** — elegida **por el mensaje de ESA pieza**, no la que
   había a mano (agobio para «la lata que es facturar», celebración para «empiezas a crecer»,
   corona para «al siguiente nivel»).

**Trampa que aparece al hacerlo:** al cambiar el bloque de color, el sujeto puede quedar del mismo
color que el fondo. la mascota es lima: sobre un piso lima desaparece. Se resuelve **invirtiendo
el bloque a tinta** —no poniéndole un halo—, y entonces el recuadro de oferta también se invierte
para no quedar tinta sobre tinta. Un cambio de fondo arrastra la paleta de todo lo que se apoya
en él.

**Cómo verlo antes de entregar:** la hoja de contacto sirve para las dos cosas, pero hay que
mirarla dos veces con preguntas distintas — *"¿esta pieza tiene un defecto?"* y, entrecerrando
los ojos, *"¿podría decir cuál es cuál sin leer el texto?"*. Si la respuesta a la segunda es no,
el lote no está listo.


## §14 · El globo de diálogo va COMPUESTO, y es un solo path (4-sep-2026)

Higgsfield dibuja la escena; la letra es nuestra. Pedirle el diálogo horneado da una tipografía
distinta por slide — el mismo defecto estructural del §13, pero dentro de una misma pieza.

**El error de bulto:** armar el globo con un `div` (borde + `border-radius`) y pegarle la cola
como un triángulo aparte. La costura entre los dos siempre se ve, y con sombra dura del
neobrutalismo se ve el doble.

**Lo que funciona:** el globo es **un solo `<path>` SVG** — rectángulo redondeado con la cola
fundida en el borde inferior — dibujado dos veces: primero relleno tinta desplazado 11×11 (la
sombra dura), encima el mismo path en blanco con `stroke` de 8px. Borde continuo, sin costura, y
la punta de la cola es un parámetro: se apunta a la **cara** del que habla, no a su pelo ni al
aire. El texto es un `div` en flex encima del rectángulo.

```python
f"M {r},0 L {w-r},0 A {r},{r} 0 0 1 {w},{r} L {w},{h-r} "
f"A {r},{r} 0 0 1 {w-r},{h} L {bx2},{h} L {tx},{ty} L {bx1},{h} "
f"L {r},{h} A {r},{r} 0 0 1 0,{h-r} L 0,{r} A {r},{r} 0 0 1 {r},0 Z"
```

**Dos cosas que hay que mirar, no calcular:** el texto se desborda del globo en silencio (el
`flex` centra y sigue de largo — pasó en la slide 1, con «jefe» fuera de la caja), y la punta
puede caer sobre el sujeto equivocado. Las dos se ven en la hoja de contacto y en ningún recibo.

**Y hay que pedir la escena vacía:** el crudo se genera con `ABSOLUTELY NO TEXT anywhere` +
un cuadrante declarado libre para el globo. Escena implica volver a generar, así que la decisión
de componer se toma **antes** de la Fase 4, no después.


## El recorte del marco fantasma se puede comer el texto (7-sep-2026)

`sin_marco.py` recorta la banda-panel de arriba y despues vuelve a cuadrar **anclando al lado
donde esta el sujeto**. Ese default es correcto para el dibujo y **falso para el globo**: en una
slide donde el personaje esta a la derecha pero habla desde un globo pegado al borde izquierdo,
anclar a la derecha corta el arranque de la frase. Paso literal: «Yo te ayudo» quedo como
**«o te ayudo»**, y el gate no lo vio porque el gate mide marcos, no palabras.

**La regla:** antes de cuadrar hay que medir **los dos** limites — donde empieza el texto y donde
termina el sujeto — y sacar los pixeles sobrantes del lado que solo tiene relleno.

    globo empieza en x = 138 · contenido termina en x = 2035 → 1897 px de contenido
    ventana cuadrada posible = 1695 px → sobran 202, y salen de la DERECHA (columna de papeles)

Cuando el contenido no cabe entero en el cuadrado, la prioridad es: **texto completo > cara del
sujeto > relleno**. Y despues se mira el PNG, siempre: esto se caza en la hoja de contacto en dos
segundos y no lo caza ningun recibo.

## El logo no va "en una esquina": va donde el fondo esta plano (7-sep-2026)

Fijar el logo arriba a la izquierda funciona hasta que una slide pone ahi el globo. Elegir "la
otra esquina" tampoco alcanza: en la slide del abrazo la de la derecha tenia la ventana encima.

**Lo que funciona es barrer las dos franjas de seguridad** (arriba y abajo) posicion por
posicion, puntuar cada candidata por la **desviacion estandar** de ese recorte —una pared o un
piso plano dan <2, una pila de papeles da >60— y elegir el minimo, con una penalizacion suave
que empate a favor de arriba y de la izquierda. El brillo medio de esa misma caja decide **que
version del logo** va: blanca bajo 128, tinta sobre 128.

Un logo ilegible es peor que uno que cambia de esquina entre slides.
