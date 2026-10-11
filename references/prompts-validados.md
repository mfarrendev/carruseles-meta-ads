# PROMPTS VALIDADOS — encuadres que produjeron fotos limpias

> **Qué es esto.** Una librería que CRECE. Cada entrada es un encuadre que ya pasó `qa_raw`
> (sin texto inventado, sin logos, zona reservada libre) con el número real medido.
>
> **Regla de oro de esta librería:** *la ilegibilidad se diseña, no se pide.* Pedir "no text"
> no funciona — se comprobó en 3 rondas. Lo que funciona es **quitarle al modelo la superficie
> donde escribir**.
>
> **Cómo se alimenta:** cada vez que una foto pasa `qa_raw` limpia, se agrega acá con su prompt
> textual y su medición. Cada vez que una falla de forma nueva, se agrega a §9.

---

## 1. Teclado (sin legends inventados)

> `qa_raw`: **0.0%** de texto · el intento anterior con "teclado sin legends" dio 0.3% de basura

```
Extreme macro photograph of a single fingertip resting on ONE keycap of a dark mechanical
keyboard, framed so close that only two or three keycaps fill the LOWER HALF of the frame and
their surfaces are smooth and blank — razor-thin depth of field, everything beyond the fingertip
dissolved into bokeh. Above, the dark desk continues as smooth empty negative space, one
continuous scene, no hard edge. Cool-neutral grade with one warm coral highlight. Keycaps
completely unmarked: no letters, no numbers, no legends, no logos.
```
**Por qué funciona:** a esa distancia no hay superficie de tecla donde quepa un glifo.

## 2. Terminal / pantalla encendida (sin pseudo-código)

> `qa_raw`: **0.0%** · los intentos con "pantalla completamente desenfocada" devolvieron la
> pantalla llena de dígitos NÍTIDOS, dos veces

```
Photograph of a dark mechanical keyboard on a wooden desk at night, lit from the front by the
coral-warm glow of a screen that is entirely outside the frame. The keyboard sits in the LOWER
RIGHT of the frame, shot at a low raking angle so the keycap tops are not readable. The dark
room continues up and to the left as empty negative space in the same light, one continuous
scene, no seam. Unbranded generic hardware. Cinematic, shallow depth of field. No screen, no
monitor, no letters, no keycap legends, no logos, no brand marks.
```
**Por qué funciona:** la pantalla está FUERA DE CUADRO; solo entra su luz.
⚠️ **No usar "monitor visto por detrás"** — ahí es justo donde está el logo de la marca.

## 3. Escritorio como fin de jornada (sin logos)

> `qa_raw`: **0.0%** · la versión con laptop traía el logo de Apple grande y centrado

```
Editorial photograph of a mug and a pair of relaxed hands resting on a wooden desk at the end of
the day, everything contained in the LOWER HALF of the frame, warm low window light. NO laptop,
no phone, no screen, no paper. Above, a plain empty wall continues in the same light as calm
negative space, one continuous scene, no hard edge. Quiet resolved mood, shallow depth of field,
warm muted grade. No letters, no logos, no brand marks of any kind.
```
**Por qué funciona:** sin tapa de laptop no hay dónde poner una manzana.

## 4. Objeto de escritorio (cuaderno, libreta)

> `qa_raw`: **0.5%** · la versión con el cuaderno ABIERTO dio **26%** de basura manuscrita

```
Still-life photograph of a dark mechanical keyboard and a closed plain notebook with a blank
unmarked cover, the objects grouped in the RIGHT THIRD of the frame, shot from above at a slight
angle. Nothing is open, nothing is written, no pages visible. The same desk continues to the
LEFT as smooth empty negative space in matching warm dim light, one continuous surface, no cut,
no seam. Shallow depth of field, warm muted grade. Absolutely no letters, no numbers, no
handwriting, no keycap legends, no logos.
```
**Por qué funciona:** cuaderno **cerrado**. Una página abierta es una invitación a escribir.

## 5. Persona en un tercio, con la otra mitad limpia

> `qa_raw`: **0.0%** de texto · zona reservada con **1.4%** de sujeto (máx 5%)

```
Editorial photograph of a developer seated at a desk reviewing a monitor, entire body AND the
desk contained strictly within the LEFT THIRD of the frame, three-quarter back view, nothing
crossing the centre line, no held objects. The RIGHT two thirds is empty dim wall continuing the
same room, one continuous scene, no seam. Screen glow only, screen surface not visible to
camera. Warm muted grade, shallow depth of field. No letters, no numbers, no screen content,
no logos.
```
**Claves:** *"entire body AND the desk"*, *"nothing crossing the centre line"*, *"no held
objects"*. Sin esas tres, un brazo o una tablet cruzan el eje y el texto les cae encima.

## 6. Pared de fondo verdaderamente vacía

Cuando la zona de texto es una pared, hay que decirlo con redundancia o aparecen papeles:
```
The LEFT two thirds is a completely plain dark wall in the same dim light — nothing on it,
no posters, no whiteboard, no notes, no sheets — one continuous room, no seam.
```

---

## 7. Mascota pixel-art sobre fondo plano de marca (Marca Verde · 5-ago-2026)

> Material 100% generado, sin fotos reales. `qa_raw` en PASS · 20 slides compuestas sin
> colisión de texto. Modelo `nano_banana_pro`, **`resolution: "2k"` explícito**,
> `aspect_ratio: "1:1"` nativo.

### 7.1 El esqueleto que funciona

```
8-bit pixel-art mascot character <<<REFERENCE-ELEMENT-UUID>>> — keep ALL characteristics of
the reference character exactly: <lista de rasgos estructurales, 5-6 ítems>.
<ACCIÓN: qué está haciendo, en una frase; la acción ES el mensaje de la slide>.
<PROPS: 1-2 objetos, descritos como pixel-art, sin texto>.
<EXPRESIÓN>.

STYLE: flat 8-bit pixel-art illustration, crisp hard pixel edges, no gradients on the
character, no 3D shading, thick dark outlines.

BACKGROUND: absolutely flat <color de marca>, completely empty, with one soft radial glow
behind the character. No panel, no card, no rectangle, no framed box, no glowing square,
no border, no floor line, no horizon, no shadow rectangle.

FRAMING RULE: native 1:1 square. The complete character and <props> must sit entirely inside
the frame with clear empty margin on ALL FOUR sides — nothing touching or crossing any edge,
no cropped leaf, no cropped feet, no cropped hands. The whole subject group occupies roughly
the middle 55% of the square.

STRICTLY FORBIDDEN: any text, letters, numbers, words, logos, brand marks, UI, watermarks;
broken, detached, floating, duplicated or dislocated limbs; impact stars or motion streaks
over the body; more than one character.
```

### 7.2 Los cuatro bloques que no se pueden sacar

- **`resolution: "2k"` explícito.** Sin ese parámetro la API degrada en silencio a
  `nano_banana_flash` y devuelve 1024×1024. No avisa: el job sale `completed` igual.
- **`aspect_ratio: "1:1"` nativo — nunca generar en 4:5 y recortar.** Ése fue el origen exacto
  del defecto de "imágenes cortadas" que el director creativo reportó: los crudos venían en 4:5 / 2:3 y el
  recorte al lienzo cuadrado se comía hasta un 30% vertical, anclado abajo → cabezas cortadas.
- **El párrafo `BACKGROUND` con las prohibiciones enumeradas una por una.** Pedir "flat
  background" no basta: el modelo dibuja un panel/card claro detrás de la escena y ese
  rectángulo queda **horneado en el crudo** — es contenido, no fondo, y ningún reencuadre lo
  saca. Con la lista explícita (*no panel, no card, no rectangle, no framed box, no glowing
  square, no border*) sale limpio a la primera.
- **La `FRAMING RULE` con "margin on ALL FOUR sides" y el `middle 55%`.** El porcentaje es lo
  que evita que el sujeto llegue al borde; sin él, "margen" es opinión del modelo.

### 7.3 Anatomía: la negación tiene que ser específica

`broken, detached, floating, duplicated or dislocated limbs` + `impact stars or motion streaks
over the body`. Un cierre salió con los dos brazos partidos en segmentos sueltos y estrellitas
de impacto encima del cuerpo, con un prompt que solo decía "celebrating". Pedir la pose en
positivo y completa —*"both arms simple and unbroken, one arm raised in a gentle friendly wave,
the other resting at its side with a normal blocky hand"*— arregló la toma siguiente.

### 7.4 El reencuadre NO se pide, se calcula

El sujeto tiene que quedar en la **banda contraria a la del texto** (razón en
`APRENDIZAJES.md` §16.c: la capa de oclusión valida contra la máscara de PERSONA y un mascot de
pixel-art con props no entra ahí, así que el motor da la zona por libre y después pinta al
personaje encima del texto).

Eso **no se le pide al modelo** — se hace después, determinista, sobre el PNG:
recortar el contenido contra el fondo plano, escalarlo, y pegarlo en la banda que toca sobre un
fondo nuevo del color de marca con su glow radial. Repetible y gratis; una tirada más del
modelo no lo es.

Dos detalles que costaron descubrir:

- **Crecer el recorte hacia el fondo antes de desvanecer el borde.** El crudo trae su propio
  halo radial y ese halo entra en el bbox del contenido: pegado en duro dibuja un **rectángulo
  claro** alrededor del personaje. Si el recorte se agranda ~35% hacia fondo puro, la rampa de
  desvanecido se gasta sobre fondo y el sujeto no se toca.
- **La tolerancia del recorte se mide, no se asume.** Con el halo muy abierto, la tolerancia por
  defecto devolvía un bbox del ancho completo del cuadro. Se prueban 2-3 tolerancias y se elige
  la que da el bbox ceñido; si la relación entre dos tolerancias es ≈1.0, el crudo no tiene ese
  problema y se deja como está.

Implementación de referencia: `fit_raw.py` de la corrida de Marca Verde (documentado en el
`_brief.md` de cada carpeta del lote `verde-ads/carruseles-2026-08-venta/`).

### 7.5 El acabado se deriva a vector si no se nombra en CADA objeto (5-ago-2026)

`nano_banana_pro` respeta el pixel-art del Reference Element **en el personaje** y se olvida de
él **en los props**. Salió una slide (c1·s-04) con la mascota correcto y todo lo demás —
monedas, papeles, sombras — en ilustración vectorial suave: entre cuatro slides pixeladas se ve
como si fuera de otro carrusel. El Reference Element ancla al personaje, no al mundo.

**El bloque que lo arregla**, y va SIEMPRE, no solo cuando falla:

> `8-bit pixel art style with visible square pixels — the pixel grid must be visible on EVERY
> element of the scene, including all props, coins, papers, shadows and the background glow, not
> only on the character. Hard-edged pixel blocks, no anti-aliasing, no smooth vector shapes, no
> gradients inside objects.`

La frase que carga el peso es **«on EVERY element … including all props … not only on the
character»**. Nombrar los props uno por uno (monedas, papeles, sombras) funciona mejor que
decir "toda la escena": el modelo trata la enumeración como restricción y el genérico como
adorno.

**Y una negación de moneda, para clientes chilenos:**

> `gold coins only — NO green banknotes, NO dollar bills, NO paper money of any currency`

El modelo dibuja "dinero" como billetes verdes tipo dólar por defecto. En una pieza chilena eso
es un error de marca, no un detalle: el producto habla de pesos y del SII. Las monedas de oro
son neutras y además leen mejor en pixel-art (formas redondas y macizas, sin texto encima —
un billete invita al modelo a inventarle letras y a reprobar `qa_raw`).

⚠️ **Los dos defectos anteriores son INVISIBLES en una hoja de contacto a 420px.** El acabado
solo se juzga leyendo al menos una slide del carrusel a 1080px. Relato: `APRENDIZAJES.md` §17.c.

### 🔴 7.6 Matar la COSTURA no es matar el GLOW: son dos cosas y van en frases separadas (5-ago-2026)

El §7.1 pide, desde siempre, *"with one soft radial glow behind the character"*. En el lote de
venta de agosto el prompt salió así:

> ❌ `BACKGROUND: one completely flat, uniform, plain deep dark green (#0a2417) filling the whole
> square edge to edge — absolutely NO gradient, NO radial glow, NO lighter band, NO horizontal
> seam or dividing line anywhere, no floor line, no shadow.`

La intención era legítima: el modelo estaba dibujando una **banda más clara con costura
horizontal** —un borde recto que parte el fondo en dos y se ve como un error de compresión— y
la negación se escribió de corrido, en una sola frase, junto con `NO radial glow`. Resultado:
**cero archivos del lote con "radial glow" y 20 crudos con el fondo muerto.** el director creativo lo notó al
verlos: *"está muy plano el fondo, antes atrás ponías como una sombra, un verde más clarito."*

El problema es que `NO gradient` + `NO radial glow` + `NO lighter band` + `NO horizontal seam`
describen para el modelo **una sola instrucción**: "el fondo no tiene luz". Y no hay reencuadre
ni composición que devuelva luz que nunca se generó.

**La forma correcta separa lo que se quiere de lo que se prohíbe, en dos frases:**

> ✅ `BACKGROUND: flat <color de marca> filling the whole square edge to edge, with ONE soft
> radial glow centred behind the character — a slightly lighter version of the same colour,
> fading smoothly in all directions with no visible edge.`
> `FORBIDDEN IN THE BACKGROUND: no horizontal seam or dividing line, no straight-edged lighter
> band, no rectangular panel, card or framed box, no border, no floor line, no horizon, no
> vignette, no shadow rectangle.`

Lo que hace la diferencia es **`no visible edge` + `fading smoothly in all directions`**: eso es
exactamente lo que distingue un glow de una banda. La costura es un borde RECTO; el glow es
radial y sin borde. Nombrar el borde —y no la luz— es lo que había que negar.

**Regla:** antes de agregar una negación al bloque `BACKGROUND`, comprobar que no esté pisando
algo que el §7.1 pide en positivo. Si la negación y el pedido hablan del mismo elemento, la
negación va acotada al **defecto** (borde recto, panel, banda), nunca al elemento.

El lado de composición está en `composicion-y-tipografia.md` §6.4 (el halo del motor). El motor
puede restituir el glow sobre un crudo plano, pero es un parche determinista: **el crudo bien
generado se ve mejor.** Relato completo: `APRENDIZAJES.md` §19.

---

## 9. Fallas conocidas y su antídoto

| Falla | Qué la dispara | Antídoto |
|---|---|---|
| Pseudo-código nítido en pantalla | pedir la pantalla de frente, aunque se pida desenfoque | pantalla fuera de cuadro |
| Legends inventados en teclas | plano medio del teclado | macro extremo (2-3 teclas) |
| Escritura a mano inventada | papel/cuaderno abierto | cerrado, o sacarlo |
| Logo de marca real | tapa de laptop, dorso de monitor | hardware genérico, sin tapas |
| Sujeto que se corre al centro | pedir solo "right third" | agregar *"entire body contained strictly within"* |
| Objeto que cruza el eje | no mencionar los objetos | *"no held objects"* / *"nothing crossing the centre line"* |
| Figura duplicada o partida | prompts largos con muchas negaciones | *"Single continuous photograph, one subject only, no repetition, no split frame"* |
| Anatomía imposible | escenas con poses forzadas | volver a una pose neutra o cambiar de plano |
| Rectángulo/panel claro detrás de la escena | fondo "flat" pedido en una sola frase | enumerar: *no panel, no card, no rectangle, no framed box, no glowing square, no border* |
| Imagen "cortada" (cabeza o pies fuera) | generar en 4:5 o 2:3 y recortar a 1:1 | generar **1:1 nativo** + *"margin on ALL FOUR sides"* + *"middle 55% of the square"* |
| Crudo en 1024 sin avisar | no pasar `resolution` | `resolution: "2k"` **explícito** en cada request |
| Miembros partidos o sueltos, estrellitas de impacto | pedir solo la emoción ("celebrating") | describir la pose completa en positivo + negar *broken, detached, floating, duplicated, dislocated limbs* |
| Props en vector entre un personaje pixelado | nombrar el pixel-art una sola vez, al principio | *"visible square pixels on EVERY element … including all props … not only on the character"* (§7.5) |
| Billetes verdes tipo dólar en pieza chilena | pedir "money" / "cash" a secas | *"gold coins only — NO green banknotes, NO dollar bills"* (§7.5) |


## Póster neo-brutalista blanco/verde con titular horneado (Marca Verde, 2-sep-2026)

Sirve cuando el titular tiene que salir **dentro de la imagen generada** y no compuesto encima.
Probado en 4 piezas: Nano Banana escribió correctamente «facturación», «¿Te sumas a ser el
siguiente?» y «No pierdas el tiempo, trabaja mejor con Marca Verde», con tildes y signos de apertura.

    <<<REFERENCE_ELEMENT>>> Keep ALL characteristics of the reference character: [rasgos].
    [pose concreta]. He stands on the right side of the middle band.
    Flat 2D vector graphic-design poster in NEO-BRUTALIST style. PURE WHITE background. Only two
    colors besides white: bright lime green and very dark forest green. Thick dark-green outlines,
    hard offset drop shadows with NO blur, sharp corners, no rounded edges, no gradients, no glow,
    no photorealism, NO 3D shading, NO isometric platform, NO perspective, no texture. The
    character stands directly on the white background with a hard flat offset shadow behind him —
    he is NOT standing on a pedestal, platform, box or slab. There are NO empty coloured
    rectangles anywhere: every block of color has type inside it. Square 1:1 composition.
    The top 12% band of the image is completely empty pure white — absolutely nothing in it, no
    text and no shape, it is reserved.
    The only text in the image is this Spanish headline, set in a very heavy grotesque sans-serif
    with tight letter-spacing, dark forest green, aligned left, filling the left two thirds of the
    middle band: [TITULAR] — reproduce those words EXACTLY, with every accent and every
    punctuation mark, and with NO quotation marks and NO guillemets of any kind around them or
    anywhere else in the image. The words [DESTACADO] sit inside a lime-green rectangle with a
    thick dark-green border and a hard offset dark-green shadow, tight around the letters.
    No other words, no letters, no numbers, no logo, no watermark, no UI, no captions anywhere
    else in the image.
    [cláusula de zona de prompt_zona.py]

**Límite medido:** con un titular de **más de cuatro líneas** el modelo lo baja hasta ~65% del alto
y se come lo que venga después, aunque el prompt diga «todo el texto entre 12% y 52%». Pedirle
tres líneas cortas, y si aun así invade, **corregirlo en la composición** (bajar y achicar lo que
se monta encima) en vez de gastar otra generación.

**Lo que este prompt NO evita:** `verify.py raw` va a reprobar por «texto inventado», porque el
gate asume que el crudo no lleva texto. Es un FAIL esperado en este modo de producción y se
documenta en el `_FALTA.md` del lote — no se falsea el recibo.
