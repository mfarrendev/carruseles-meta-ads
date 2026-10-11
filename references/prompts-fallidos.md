# Prompts que FALLAN — el anti-catálogo

> **Se lee ANTES de escribir un prompt de imagen.** Va de a pares con
> `prompts-validados.md`: ese guarda los aciertos, este guarda por qué el
> mismo error se repite.

## Por qué existe (5-ago-2026)

Medición del libro de Higgsfield, ventana 4-ago 02:26 → 6-ago 03:08, para
entregar **4 carruseles Marca Verde**:

| | |
|---|---|
| Generaciones de imagen | **255** (nano_banana_pro 195 · nano_banana_2 48 · GPT Image 2.0 12) |
| Upscales (Bytedance) | 49 |
| Recortes de fondo | 6 |
| **Créditos netos** | **717** |
| Crudos en disco | 21 |
| Crudos usados en los renders | **20** |
| **Aprovechamiento** | **8%** |

Las otras 234 se generaron, se miraron, se descartaron y **no dejaron rastro**:
ni un contador, ni el prompt que falló, ni el motivo. `prompts-validados.md`
guardaba solo los éxitos. **Un catálogo de aciertos sin anti-catálogo hace
repetir los errores gratis**: el prompt que falló hoy no está escrito en ningún
lado, así que mañana se vuelve a pedir con otra semilla y vuelve a salir igual.

Regla que sale de ahí: **un crudo rechazado se ARCHIVA con su motivo** —
`costo.py descartar <carpeta> <archivo> --por <motivo> --prompt "…"` →
`raw/_descartados/` + `_motivos.json`. **Si el mismo motivo sale 2 veces en un
carrusel, el problema es el PROMPT, no la semilla**, y la corrección se escribe
acá antes de volver a generar.

---

## Cómo se escribe una entrada

Una entrada por patrón de fallo, no por foto. Formato:

```md
### <motivo> — <qué se pedía>
**Falló así:** …  ·  **Veces:** N  ·  **Créditos quemados:** ~N
**El pedazo de prompt que lo causa:** «…»
**Reemplazo que sí funciona:** «…»
```

El "reemplazo que sí funciona" solo se escribe cuando ya pasó `qa_raw` —
si no, es una hipótesis y va marcada como tal.

---

## §1 · `texto-inventado` — letras basura en pantallas, papeles, carteles

**Falló así:** se pide una escena con un notebook / celular / boleta a la vista
y el modelo llena la pantalla con caracteres que parecen texto pero no lo son.
Es el fallo más repetido del historial (test jul-2026: **8 de 16 fotos**;
relato en `APRENDIZAJES.md` §5).

**El pedazo de prompt que lo causa:** pedir *"no text, no logos"* y creer que
alcanza. **Pedirlo no basta.** El negativo no gobierna lo que el modelo dibuja
dentro de una superficie que él mismo decidió que es una pantalla.

**Reemplazo que sí funciona:** no dejar la superficie vacía — **darle contenido
declarado y no-textual**. En vez de *"laptop screen, no text"*:

> `laptop screen showing a simple abstract dashboard: three colored bars and a
> circle chart, no letters, no numbers, no words anywhere on screen`

O sacar la pantalla del encuadre: de frente al sujeto, la pantalla de espaldas.
El texto real del carrusel lo pone el motor de composición, no la IA.

**Regla dura Marca Verde que agrava esto:** una pantalla con letras inventadas
puede parecer el logo de un tercero (Mercado Libre, Shopify, Meta) → **riesgo
de baneo, ya pasó: cuenta antigua deshabilitada**. Acá el fallo no es estético.

## §2 · `logo-real` — marca de un tercero visible

**Falló así:** 2 fotos con el logo de Apple en el notebook (test jul-2026),
pidiendo explícitamente *"no logos"*.

**Reemplazo que sí funciona:** describir el dispositivo **sin marca y sin la
silueta que la delata**: `plain silver laptop, blank lid facing away, no brand
marks, no logos, no emblems on any surface`. Y auditarlo igual en la Fase 4b:
la tapa del notebook es el punto ciego clásico.

## §3 · `anatomia` — manos, dedos, postura imposibles

**Falló así:** 2 de 16 (jul-2026). Aparece sobre todo cuando el prompt pide una
acción con las manos en primer plano (*"typing"*, *"holding a phone"*,
*"pointing at"*).

**Reemplazo que sí funciona:** sacar las manos del primer plano o del encuadre
— plano medio, manos apoyadas o fuera de cuadro. Si la acción con las manos
**es** el mensaje, es una foto real o no es.

## §4 · `personaje` — la mascota/persona no es la misma

**Falló así:** el Reference Element se pasó pero la mascota sale con otra
proporción, otro color o sin el rasgo que la identifica.

**Reemplazo que sí funciona:** Reference Element + repetir en el prompt los
**tres rasgos no negociables** del personaje (no "el mismo personaje": *qué*
lo hace el mismo). Si el crudo falla dos veces seguidas, el problema es que el
prompt describe una escena que obliga a deformarlo (pose, ángulo, escala), no
la semilla.

## §5 · `zona-ocupada` — no dejó libre el hueco del texto

**Falló así:** la foto es linda pero el sujeto ocupa exactamente la columna
donde el blueprint pone el título. El motor reubica o se rinde con diagnóstico,
pero la foto se descarta.

**Reemplazo que sí funciona:** el prompt declara el hueco como parte de la
composición, no como ausencia: `subject on the right third, left third is
clean empty background with soft gradient, generous negative space on the
left`. La tabla de encuadres por zona está en `produccion-imagenes.md` §0.

**Antes de regenerar por esto: probar `zoom` + `posx`/`posy` en el spec.**
Cuesta 0 créditos y arregla la mitad de estos casos.

## §6 · `fondo` — fondo plano, sucio, o que pelea con la marca

**Falló así (5-ago-2026, Marca Verde, lo cazó el ojo del director creativo, no las
compuertas):** *"está muy plano el fondo, antes, cuando generabas los
verde suaves, atrás ponías como una sombra o algo que era un verde más
clarito"*. Las siete compuertas dieron verde: **miden lo que está mal, no lo
que falta** (memoria `comparar-contra-el-lote-anterior`).

**El pedazo de prompt que lo causa:** `flat solid background` / `plain
background` / dejar el fondo sin describir. El modelo resuelve con un plano
liso, que mide perfecto y se ve barato.

**Reemplazo que sí funciona:** describir el fondo como **profundidad**, no como
color: `soft radial halo behind the character in a lighter tint of the brand
green, gentle falloff to the darker green at the edges, subtle depth, no hard
edges`. El halo simétrico ya estaba resuelto en el lote de Marca Crema
(memoria `crema-fondos-casa`) y se perdió al cambiar de cliente.

## §7 · `no-demuestra` — linda, pero no muestra lo que dice el texto

**Falló así:** la slide dice *"ahorrás 6 horas al mes"* y la foto es una
persona sonriendo frente a un notebook. Podría ilustrar cualquier cosa.

**Reemplazo que sí funciona:** el prompt arranca del `visual_need` del spec
(*qué debe DEMOSTRAR*), no del titular. Si el `visual_need` no se puede
fotografiar, el problema está en el blueprint y se arregla ahí — no con más
generaciones.

### §7.b · El titular NIEGA y la foto AFIRMA (6-ago-2026)

**Falló así:** titular *"Nada se manda al SII sin tu OK"*; la foto muestra
cuatro documentos saliendo solos del notebook **ya marcados con visto bueno
verde**. La imagen ilustra literalmente lo que la frase niega. Los dos jueces
lo cazaron por separado — pero en la Fase 7, con la pieza ya compuesta.

**Por qué pasa siempre con los titulares en negativo:** el prompt se escribe
describiendo *la escena*, y la escena natural de una frase negativa es su
afirmativa. "Nada se manda sin tu OK" se prompt-ea como "documentos
enviándose", porque eso es lo que hay que dibujar.

**Reemplazo que sí funciona:** si el titular niega algo, la foto muestra el
**momento anterior al resultado** — el humano decidiendo, con el resultado
todavía sin ocurrir:

```
the ecommerce owner's hand hovering over the laptop trackpad, cursor resting on
a single "Revisar" button; the documents on screen are still plain, NO green
checkmarks, NO ticks, nothing marked as done or approved — the decision has not
been made yet
```

**Chequeo, que ahora es parte de la Fase 4b:** con el titular a la vista, mirar
la foto sola y contestar *¿muestra lo que la frase afirma, o lo que niega?*
En el crudo cuesta una línea de prompt; en la Fase 7 cuesta regenerar,
recomponer y re-juzgar.

---

## §8 · Fallos de MODELO, no de prompt (5-ago-2026)

Estos no se arreglan escribiendo mejor: se arreglan eligiendo distinto.

| Síntoma | Costo real medido | Qué hacer |
|---|---|---|
| Se usó `gpt_image_2` para un crudo de carrusel | **12 créditos c/u — 6× un `nano_banana_pro`.** 12 imágenes = 144 créditos = 20% del gasto del lote, y ninguna llegó a disco | `nano_banana_pro` para fotografía de persona/producto con Reference Element |
| Se generó chico y se subió con upscale | 49 upscales = 98 créditos | Pedir **2048² en la llamada original**. Un upscale no arregla un encuadre: agranda el mismo error |
| Se regeneró para "agrandar al sujeto" | 2 créditos + 40 s cada intento | `zoom` / `posx` / `posy` en el spec: **0 créditos, 0 espera** (`composicion-y-tipografia.md` §7.1) |

---

## Cómo alimentarlo

1. Descartar con motivo: `costo.py descartar … --por <motivo> --prompt "…"`.
2. Al cerrar el carrusel, leer `raw/_descartados/_motivos.json`.
3. **Motivo repetido ≥2 veces → entrada acá**, con el pedazo de prompt que lo
   causa y el reemplazo (marcado como hipótesis si todavía no pasó `qa_raw`).
4. Cuando el reemplazo pase limpio, la versión buena va a
   `prompts-validados.md` y acá queda el par: qué falla, qué lo reemplaza.

---

## Placa institucional → LÁPIDA (10-ago-2026 · Marca Verde c4, Nano Banana)

**Prompt que falló:** *"a stylised institutional plaque: a simple upright stone-grey panel with
the three sans-serif capital letters S I I engraved on it"*.

**Qué salió:** las 4 slides con una **lápida de cementerio** — gris piedra, canto superior
redondeado, proporción de tumba, apoyada en el suelo. la mascota parado al lado de la tumba del
SII, en un ad de un servicio tributario.

**Por qué:** «stone-grey panel» + «engraved» + «upright» es la descripción literal de una
headstone, y es la imagen más frecuente en el entrenamiento para esa combinación. «Plaque» no
alcanza a corregirla.

**Lo que sí funciona:** nombrar el objeto por su categoría real y prohibir la silueta —
*"a tall MODERN OFFICE SIGN: rectangular vertical panel with square corners and a slim metal
frame, mounted on two visible legs like a building directory sign… CRITICAL SHAPE RULE: must NOT
look like a tombstone or gravestone — no rounded or arched top, no headstone silhouette, no
weathered stone, no grass at its base"*.

**La regla general:** cuando un objeto genérico tiene un vecino semántico siniestro (placa/lápida,
caja/ataúd, sala de espera/velatorio), el prompt tiene que **nombrar la silueta prohibida**, no
solo describir la correcta.

## Palabras reales en inglés dentro de mockups (10-ago-2026 · Marca Verde c1-c3, Nano Banana)

**Prompt que falló:** *"No paragraphs, no labels, no numbers, no **invented** words anywhere."*

**Qué salió:** «Invoice» rotulando dos documentos y «Unsigned lines» al pie de otro — en inglés,
en piezas de una marca chilena.

**Por qué:** prohibir palabras *inventadas* le deja libre el camino a las palabras **correctas**.
El modelo entendió que un rótulo real y bien escrito cumplía la regla.

**Lo que sí funciona:** *"the image must contain ZERO readable words… NO English words anywhere —
not 'Invoice', not 'Total', not 'Date', not menu items, not column headers"*, y declarar la
excepción con el deletreo exacto (*"the ONLY exception is BORRADOR, spelled B-O-R-R-A-D-O-R"*).

## «Same hair» conserva las TRENZAS de la foto fuente (11-ago-2026 · Marca Crema, lote resenas-990)

**Prompt que falló:** *"Keep the woman from the reference photo exactly as she is — same face, same hair, …"*
en image-to-image para cambiar solo el fondo.

**Qué salió:** dos generaciones seguidas (desde `DSC06645.jpg` y desde `Marca Crema retocado 2 alta-13.jpg`)
conservaron fielmente las **trenzas/cornrows** de la foto original — vetadas por la cliente (regla de
Marca Crema, jul-2026). En la hoja de contacto chica ninguna de las dos fuentes *parecía* tenerlas; a tamaño
completo sí. Costo: 2 crudos descartados.

**Por qué:** «same hair» es una orden de fidelidad: el modelo obedece y copia el peinado prohibido.
Y la verificación "sin trenzas" hecha sobre una miniatura no detecta cornrows — hay que hacer zoom a
la cabeza de la fuente ANTES de subirla.

**Lo que sí funciona:** (1) zoom a la cabeza de la foto fuente antes de elegirla; (2) nombrar el
peinado permitido y la prohibición explícita en el mismo prompt: *"same hair tied back in a low bun
(no braids, absolutely no braided hair)"*. Con esa cláusula, las dos regeneraciones salieron limpias.


## Las comillas que delimitan el titular se HORNEAN dentro de la imagen (2-sep-2026)

**Prompt fallido:**

    The ONLY text in the image is the Spanish headline «Clientes felices», set in a very heavy
    grotesque sans-serif...

**Qué salió:** la imagen decía, literalmente, **«Clientes felices»** — con las comillas angulares
dentro del arte. Igual en las otras dos piezas del lote: «…problemas», «en facturación». Nano
Banana no distingue entre un delimitador de cita y un carácter que hay que dibujar: si está en el
prompt, lo pinta.

**Prompt corregido:**

    The only text in the image is this Spanish headline, set in a very heavy grotesque sans-serif
    with tight letter-spacing, dark forest green, aligned left: Clientes felices — reproduce those
    words EXACTLY, with every accent and every punctuation mark, and with NO quotation marks and
    NO guillemets of any kind around them or anywhere else in the image.

El titular entra **después de dos puntos, sin envolver**, y se prohíben las comillas de forma
explícita. Vale para « », " " y ' '.

## «He stands on a large flat block» produce rectángulos vacíos y plataformas 3D (2-sep-2026)

Pedir que el personaje se pare **sobre un bloque** de color hizo dos daños en el mismo lote:
en dos piezas apareció un **rectángulo lima grande y vacío** flotando en el medio (el bloque, sin
nada dentro), y en una tercera el bloque se convirtió en una **plataforma isométrica con sombreado
3D**, rompiendo el estilo plano.

**Lo que sí funciona:**

    The character stands directly on the white background with a hard flat offset shadow behind
    him — he is NOT standing on a pedestal, platform, box or slab. There are NO empty coloured
    rectangles anywhere: every block of color has type inside it.

La segunda frase es la importante: **todo bloque de color tiene texto dentro**. Sin esa regla el
modelo usa los bloques como relleno decorativo.

## Reservar la esquina del logo, no solo la zona del texto (2-sep-2026)

La cláusula de `prompt_zona.py` reserva la zona donde irá el texto compuesto — pero el **logo**
también se compone, y en tres de cuatro piezas quedó encima del titular horneado. Cuando el logo
va compuesto sobre una escena con texto generado, el prompt tiene que reservarle su franja:

    The top 12% band of the image is completely empty pure white — absolutely nothing in it,
    no text and no shape, it is reserved.


## El marco fantasma: pedir una "franja reservada" hace que dibuje un panel de cómic (4-sep-2026)

**Prompt fallido:**

    Square 1:1 composition. The top 12% band of the image is completely empty light background,
    absolutely nothing in it, it is reserved.

**Qué salió:** Nano Banana interpretó «franja reservada» como **una viñeta vacía**: dibujó una
banda blanca en el borde superior **con línea negra divisoria**, y de paso un **marco negro
alrededor de toda la imagen**. La pieza quedó pareciendo una página de cómic con un cuadro vacío
arriba. Pasó en 3 de 5 generaciones del lote.

Es una trampa fina, porque la cláusula existe justamente para dejarle sitio al logo compuesto — y
el modelo la cumple, pero dibujándola.

**Prompt corregido:**

    The illustration BLEEDS to all four edges of the square: there is NO panel border, NO frame,
    NO outer black line, NO dividing line and NO white margin anywhere. It is one single
    continuous drawing, not a comic page with panels. Keep the upper twelve percent of the scene
    free of any object and any text, showing only plain background there, but do NOT draw a box,
    band or line around it.

**Y aun así se cuela.** Baja mucho, no a cero. Por eso el arreglo definitivo no es de prompt sino
de composición: `sin_marco.py` detecta la línea divisoria y el marco por columnas/filas oscuras,
recorta por debajo y vuelve a cuadrar anclando al lado donde está el sujeto. **Cuesta cero
créditos y siempre funciona**, así que conviene correrlo por defecto sobre todo crudo de este
estilo en vez de regenerar.

## Anclar un personaje que NO tiene Reference Element (4-sep-2026)

El brand-brain de Marca Verde solo tiene Reference Element de la mascota. Este carrusel necesitaba
además **el mismo hombre en las 4 slides**, y generar las 4 en paralelo da cuatro hombres
distintos.

**Método que funcionó:** generar la slide 1 **sola**, y pasar su `job_id` como `medias` en las
siguientes (`role: image` — el backend lo convierte solo a `image_references`), junto con el
`<<<uuid>>>` de la mascota en el texto del prompt. Los dos mecanismos conviven sin pelearse.

En el prompt de cada slide siguiente hay que **nombrar lo que se repite**, no solo decir «el mismo
hombre»: *same face shape, same short dark brown hair, same light stubble, same light blue
rolled-up shirt, same cartoon style and line weight*.

**Costo de la regla:** este carrusel NO se puede generar en una sola ráfaga, que es lo contrario
de lo que manda el modo lote. Acá la ráfaga rompe la pieza.
