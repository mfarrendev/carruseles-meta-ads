# RÚBRICA — Definition of Done de un carrusel (todos los aprendizajes)

Esta es la **fuente única de verdad** del QA. El agente `carrusel-qa` evalúa CADA slide contra cada ítem **a tamaño completo**. Regla **fail-closed**: ante cualquier duda, el ítem va **FAIL** con el fix concreto. El carrusel es PASS solo si TODOS los ítems pasan en TODAS las slides.

> **De dónde salen las cifras de composición y tipografía.** Los pisos de tamaño, el tracking, los
> quiebres de línea, el alfa del scrim, las anclas y los gaps **se definen en
> `references/composicion-y-tipografia.md`** (el "cómo poner el texto"). Esta rúbrica los hace
> cumplir; no los redefine. Si un ítem de acá contradice ese archivo, **gana ese archivo** y hay
> que corregir el ítem. Y por encima de los dos manda el **brand-brain del cliente**.

---

# ⚡ QUÉ MIDE EL SCRIPT Y QUÉ JUZGA EL OJO

**El juez NO revisa lo que ya midió una compuerta.** Un script mide contraste, píxeles y anchos
con más precisión que cualquier lectura, y re-juzgarlo es lo que hacía que cada juez tardara
15-20 minutos. Si una compuerta está en verde, esos ítems se dan por buenos.

| Ya lo mide un script — **el juez lo salta** | Compuerta |
|---|---|
| E1 contraste · E2 márgenes | `qa_lint` |
| E3 tamaños · E5 salto de escala · E8 piso absoluto | `qa_typesize` |
| E9 pastillas y solapes · E6 choques de chrome | `qa_geom` |
| Quiebres del spec, huérfanas, línea que termina en conector | `qa_lines` |
| Overflow real · colisión con el chrome · piso computado · densidad por bandas | `qa_dom` |
| A11 texto inventado (bloques ≥2% del cuadro) | `qa_raw` |
| A7 mapa persona+luz · zona reservada libre | `photo_map` / `qa_raw` |
| A8 imágenes distintas · A3 zonas vecinas | motor (conteo de `src`, posición renderizada) |

**Lo que el juez SÍ tiene que mirar** — es lo único que un script no ve, y va a tamaño completo:

| # | Qué |
|---|---|
| **A0** | En qué mitad está la persona y dónde cayó el texto (línea obligatoria en el recibo) |
| **A1 · A2 · A2b · A4** | ¿El texto o el gradiente rozan al sujeto, su cara o el objeto clave? |
| **A10** | Zona oscura de oferta: ¿el corte deja a la persona con cuerpo visible? |
| **A12** | **Logos de marca real** (el OCR no los ve: son imagen, no texto) |
| **A13** | Anatomía: figuras duplicadas, miembros imposibles, cabezas cortadas |
| **B1** | ¿La imagen DEMUESTRA el mensaje o solo decora? — **WARN, ya no bloquea** (director creativo, 10-ago-2026) |
| **B2 · B3** | Pose real de la disciplina · sujeto y objeto completos |
| **C1–C6** | Buyer persona · expresión · sin close-up de cara · misma persona · mascota fiel |
| **D1–D5** | Datos reales · claro · español neutro · lugar real · línea y CTA correctos |
| **DC1–DC8** | Calidad del copy (no suena a IA, hook, deseo, VoC, comprensión) |
| **E4 · E7** | Coherencia de tono y paleta entre slides · sombra direccional |
| **F1 · F2** | Coherencia con el `_brief.md` |
| — | **Microtexto inventado <2% del cuadro** (legends de teclas): queda bajo el piso de ruido del OCR |
| — | **¿Se ve publicable como ad pagado, o se nota generado?** |

*Si una compuerta está en rojo, el juez ni siquiera corre: primero se arregla y se re-mide.*

## ⭐ Excepciones de sistema — las declara el BRAND-BRAIN, no esta rúbrica

Una marca puede tener un sistema visual aprobado que **contradice a propósito** algún ítem de acá
(ej. un preset de columna centrada que no rota la zona del texto, o que acepta el título sobre el
cuerpo de la persona). Eso es legítimo: la jerarquía de mando dice que **el brand-brain manda
sobre esta rúbrica**.

**Cómo funciona:**
1. La excepción se declara en `brand-brain/<cliente>/design-principles.md`, con **qué ítem** relaja,
   **hasta dónde** y **contra qué pieza aprobada** se calibró.
2. El juez `carrusel-qa` **lee ese archivo antes de juzgar**. Si no existe, aplica la rúbrica entera.
3. Lo que una excepción **nunca** puede relajar: tapar un ROSTRO, tapar el objeto clave del que
   habla la slide, y los pisos tipográficos de legibilidad en teléfono.

*Precedente:* el preset **PILATES v2** (carrusel Cyber publicado y aprobado, junio 2026) vivía
escrito acá dentro. Se movió a `brand-brain/marca-pilates/design-principles.md` el 1-ago-2026 —
un sistema de una marca no puede vivir en el archivo que leen las once.

## A. Disposición del texto (revisar a tamaño completo, NO en miniatura)
- **A0 · ¿EN QUÉ MITAD ESTÁ LA PERSONA? (chequeo obligatorio, primero de todos).** ANTES de juzgar A1/A2, abrir la **foto de fondo CRUDA** (`fotos/<slide>.png`, sin texto) y decir EXPLÍCITAMENTE en qué mitad/zona está la persona (izq / der / centro / arriba / abajo). El texto de la slide DEBE estar en la zona OPUESTA y vacía. Si la persona está a la izquierda y el texto también está a la izquierda → **FAIL inmediato** (no importa el contraste ni nada más). Falla grave real (Barralates slide 03, jun 2026): persona en mitad izquierda + texto `l-topleft` en la misma mitad → tapaba cara/torso/brazo y AMBOS jueces dieron PASS. Por eso este chequeo va PRIMERO y se escribe en el recibo ("persona: izquierda · texto: derecha · OK" / "persona: izquierda · texto: izquierda · FAIL"). El verificador NO puede dar PASS sin esta línea por slide.
- **A1 · Título en espacio limpio.** El TÍTULO principal cae en una zona de espacio negativo limpio. NUNCA encima del sujeto (persona) ni del objeto/implemento clave (trampolín, baquetas, barra, reformer, pesas…). Ni rozándolo.
- **A2b · El objeto/extremidad que invade el centro cuenta como "sujeto".** Si el texto va en una columna lateral, el brazo/implemento/objeto clave NO debe cruzar la línea central hacia esa columna (verificar a tamaño completo). Si cruza → mover texto o regenerar con el sujeto+objeto contenidos en su mitad.
- **A2c · La ILUSTRACIÓN no se monta sobre la pastilla CTA (5-ago-2026).** La capa de oclusión
  pinta el recorte del sujeto en `z-index 4`, **encima** del texto (`z-index 3`): una hoja, un
  brazo o un prop que sobresalga se monta sobre la pastilla de oferta y ningún gate del DOM lo
  ve, porque el DOM solo conoce la CAJA de la imagen, no dónde está el contenido dentro de su
  alfa. Exige **≥24px de aire limpio** entre la pastilla y el contenido real de la ilustración.
  Lo mide `qa_pastilla.py` (corre dentro de `verify.py gates`) detectando la pastilla por FORMA
  —una corrida contigua de color >280px— y no por color suelto: con una mascota verde sobre
  marca verde, la máscara de color reporta la pastilla del alto entero del cuadro. Relato:
  `APRENDIZAJES.md` §17.a.
- **A2 · Ni el texto NI el GRADIENTE tapan lo importante.** Eyebrow, body, sub, CTA **y el scrim/gradiente** no tapan al sujeto, **su ROSTRO/cara**, ni el objeto clave. El gradiente debe entrar del lado vacío y **desvanecerse antes del sujeto** (usar `g-left/g-right/g-top/g-bottom`, no `sc-*` anchos). Si el gradiente oscurece parte del cuerpo → FAIL. (Falla histórica: Cool Barre 04 con texto sobre la cara que un verificador suelto dejó pasar — mirar la cara EXPLÍCITAMENTE.)
- **A3 · Disposición variada.** El texto NO está en la misma zona en slides consecutivas; la distribución es variada/asimétrica a lo largo del carrusel. Hay ≥1 salto de escala (título XL o quiebre).
- **A4 · Sujeto centrado = regenerar.** Si el sujeto sale centrado y no deja media imagen libre, NO se fuerza el texto encima: la foto debió regenerarse con el sujeto a un tercio. Si una slide tiene el sujeto centrado y texto encima → FAIL.
- **A8 · IMÁGENES DISTINTAS — CERO REPETICIÓN (regla dura MAX, el director creativo jul-2026).** Dentro de un mismo carrusel, **ninguna imagen se repite**: cada slide con foto/imagen usa una imagen DISTINTA (fotos reales distintas de la sede correcta, o assets generados distintos). Chequeo DETERMINISTA: contar los `src=` de los PNG/HTML del carrusel → si cualquier imagen aparece **2+ veces = FAIL**, no se muestra. Fix correcto: usar otra foto real distinta, **generar la faltante con Higgsfield** (sede/persona reales) o **sacar un frame de un video del brand-brain** (ver A9) — NUNCA rellenar repitiendo la misma foto.
- **A9 · Frames de VIDEO del brand-brain (solo si existen).** Si el brand-brain del cliente contiene videos (`.mp4/.mov/.m4v`), es OBLIGATORIO revisarlos como fuente extra de imágenes: extraer frames NÍTIDOS (sin motion blur, bien encuadrados, sede/persona reales) y tratarlos como una foto real más (mismo QA de imagen: A0–A4, B, mapa persona+luz). Ayuda a cumplir A8 sin repetir ni inventar. **Si el brand-brain NO tiene videos, este ítem no aplica** (N/A en el recibo).

- **A10 · ZONA OSCURA/PANEL DE OFERTA — bajo, difuminado y con el texto DENTRO (corrección el director creativo 27-jul-2026, posts Black Week).** Cuando se usa un panel o zona oscura inferior para texto de oferta: (a) **el corte NO puede ser demasiado alto** — si arriba solo queda la cara de la persona y se pierde el cuerpo/contexto, la imagen "pierde sentido" → FAIL: bajar el inicio de la zona oscura hasta que la persona se vea con suficiente cuerpo (como mínimo cabeza + torso + brazos/acción completos, típicamente la zona oscura fuerte parte bajo el ~55-60% del alto); (b) **nunca un bloque negro sólido de borde duro** — usar un **degradado largo y difuminado** que suba suave desde la foto (transparencia → oscuro), la transición no debe verse como un corte; (c) **TODO el texto (logo, eyebrow, titular, precio, bajada) debe quedar DENTRO de la zona suficientemente oscura** y dentro de los márgenes seguros — texto sobre la zona clara/degradada débil o pasándose de los límites = FAIL. Verificar a tamaño completo que ningún elemento "se sale" de la parte oscura.

  - **Logo en posts de oferta (corrección el director creativo 27-jul-2026):** si el bloque de texto va alineado a un lado (diseños tipo A/C con panel inferior), el logo NO va pegado encima del texto → va en la **esquina superior izquierda** del lienzo (con velo superior suave si la foto es clara, para que no se pierda). Si el texto va **centrado** (card tipo B), el logo va **centrado con el texto**. Y ojo con el bug recurrente: un SVG inline sin `width:100%` renderiza a su tamaño natural (320px) desbordando su contenedor → el logo "se corre a la derecha"; SIEMPRE `svg { width:100%; height:auto }` dentro de su caja.

- **A11 · CERO TEXTO INVENTADO DENTRO DE LA FOTO (test jul-2026, bloqueante).** Ninguna imagen
  puede traer glifos generados por la IA: legends falsos en teclas, líneas de pseudo-código en
  pantallas, escritura en papeles o carteles, letras en paredes. Se revisa **en la foto cruda de
  `raw/`, a tamaño completo**, no en la slide compuesta. Un solo bloque de texto basura = FAIL:
  es lo que más delata "generado", sobre todo con público técnico. *Fix: no pedir "no text" —
  rediseñar el encuadre para que no haya superficie donde escribir (`produccion-imagenes.md` §0.1).*
- **A12 · SIN LOGOS DE MARCA REAL.** Manzanas en tapas de laptop, wordmarks en hardware, marcas
  en ropa. Se revisa en el crudo. Falla real: logo de Apple grande y centrado en la slide de
  cierre, con el prompt pidiendo "no logos".
- **A13 · ANATOMÍA Y COHERENCIA FÍSICA.** Sin figuras duplicadas, miembros imposibles, cabezas
  cortadas por el encuadre ni cuerpos sin rostro. Falla real: un torso con un brazo saliendo del
  costado, y una imagen con el mismo sujeto repetido arriba y abajo.
- **A14 · DESTAQUE INLINE — el fragmento correcto, uno solo (director creativo, 5-ago-2026).** Cada titular
  de ≥5 palabras resalta **un** fragmento (peso máximo + acento de marca) y baja el resto. El juez
  verifica cuatro cosas, a tamaño completo y en el thumbnail de 360px:
  (a) **el fragmento es lo más relevante** de esa slide — la oferta, la cifra, el beneficio o el
  giro; si lo destacado es la parte de relleno, FAIL;
  (b) **el contraste se percibe** — si a 360px el destaque no se distingue del resto, no destaca;
  (c) **hay UNO solo** — dos fragmentos compitiendo = ninguno destaca = FAIL;
  (d) **no queda partido raro** por el salto de línea (un destaque cortado a la mitad entre dos
  renglones se lee como error de render, no como énfasis).
  Titular sin destaque: aceptable. Titular **entero** destacado: FAIL — el problema real es que
  el copy es demasiado largo. Mecanismo en `composicion-y-tipografia.md` §4.1.1; quién elige el
  fragmento, en `COPY.md`.

## B. Imagen co-comunica (Espacio creativo)
- **B1 · Representa el mensaje — WARN, NO FAIL.** La foto debería representar lo que dice el texto de esa slide. Ej. "fuerza y flexibilidad" con mujer sentada tranquila.
  🔴 **Desde el 10-ago-2026 esto NO reprueba una pieza.** el director creativo: *«si una slide pasa eso, se puede perdonar»*. Se anota en el recibo como WARN y la pieza pasa igual. Era el hallazgo nº1 del juez de diseño (24 de 100), y su costo era regenerar escenas por una foto que decora en vez de demostrar. Sigue anotándose porque es la señal de que la foto no se generó PARA el plan — pero es información, no puerta.
- **B2 · Pose real de la disciplina.** La pose es real y reconocible de esa disciplina, controlada y segura (no improvisada/colapsada).
- **B3 · Integridad.** El sujeto y el objeto clave se ven completos, no cortados por encuadre, bloque o scrim.

## C. Sujeto / modelo
- **C1 · Buyer persona.** Coincide con el cliente (ej. Marca Crema = mujer ~35-45, esbelta no musculosa; nunca jóvenes/adolescentes).
- **C2 · Sonrisa sutil.** Expresión disfrutando con **sonrisa sutil y natural**; NUNCA carcajada exagerada ni cara seria/incómoda.
- **C3 · Sin close-up de cara.** Encuadre cuerpo entero o 3/4; evitar primer plano del rostro (la IA lo hace uncanny).
- **C4 · Misma persona.** La modelo es la MISMA en todas las slides (Reference Element).
- **C5 · Encuadre variado.** Ángulos/acercamientos distintos entre slides (no la misma toma repetida).
> **⚠️ El brand-brain del cliente puede fijar el UMBRAL de C6.** Hay marcas donde la mascota es
> un activo gráfico fijo (calco) y otras donde es un personaje que ACTÚA. Si el brand-brain
> declara "expresividad > fidelidad literal" (caso Marca Verde, corrección del director creativo 29-jul-2026),
> C6 se juzga como **"¿es reconociblemente el personaje?"** y solo falla si la IA devolvió un
> genérico que ya no se identifica con la marca — no por grosor de contorno, estilo de sombreado
> ni ángulo de un accesorio. Sin declaración en el brand-brain, sigue el criterio estricto de
> abajo. El juez debe LEER el brand-brain antes de aplicar C6.

- **🔴 C6 · FIDELIDAD a la mascota/personaje de marca (anti-deriva, jun 2026).** Cuando el cliente tiene una mascota/personaje OFICIAL (ej. la mascota 8-bit), en CADA slide el personaje debe ser **EL MISMO de la imagen de referencia**, no un primo parecido. El juez DEBE abrir la imagen de referencia oficial (ruta en el `_brief.md`) y compararla contra el personaje de CADA slide, a tamaño completo. **Distinguir dos clases de rasgo:**
  - **RASGOS ESTRUCTURALES (no-negociables, deben estar SIEMPRE):** la SILUETA/forma del personaje (cuerpo cuadrado pixel-art), **dos tonos de verde** (cara lima clara + lateral verde oscuro), **contorno negro grueso**, **hoja con nervaduras** en la cabeza, **ojos negros ovalados**. Si falta cualquiera de estos → el personaje "derivó" a un cubo genérico → **FAIL C6**.
  - **PROPS/EXPRESIÓN ACCESORIOS (situacionales, NO obligatorios en cada slide):** la **moneda dorada "0"** (es un accesorio, no tiene que estar en la mano en TODAS las poses — exigirla durmiendo o saltando es absurdo), la boca **abierta con lengua** (puede sonreír con boca cerrada según la emoción), el brazo apuntando. La ausencia de un prop accesorio o una sonrisa distinta **NO es FAIL** si los rasgos estructurales están intactos. NO inflar C6 con props.
  - Síntoma de deriva real: cuanto más extrema la POSE (saltar, dormir), más inventa la IA → revisar con LUPA, pero juzgar por los ESTRUCTURALES. Un "cubo verde genérico" sin los dos verdes / sin contorno grueso / con otra silueta = FAIL. La MISMA mascota sonriendo sin moneda en una pose = PASS. Separado de C4 (misma entre slides) y D1 (no inventar): aquí se compara contra la REFERENCIA EXTERNA.

## D. Copy / contenido
- **D1 · Datos reales, no inventados.** En carruseles informativos, los datos son REALES e investigados de fuentes ya creadas; cero cifras/claims/testimonios/marcas inventadas.
- **D2 · Explicado claro.** Cada dato se entiende (no críptico, no frase-beneficio cliché). Si necesita contexto, lo da en una línea.
- **D3 · Español neutro.** Español mexicano/neutro, sin voseo. **Prohibido "chicos/chicas" como tamaño → "pequeños/pequeñas".**
- **D5 · LUGAR REAL, nunca inventado.** Para un negocio físico, el escenario/locación debe ser **real** (fotos reales de ESA sede), nunca un estudio generado por IA que no existe. Si se genera con IA, que sea con la sede real como referencia de entorno — jamás inventar el lugar.
  - **Dónde están las fotos de cada sede lo declara el brand-brain**, no esta rúbrica: `brand-brain/<cliente>/sede-real.md` (o el `README.md` del cliente). El juez debe abrirlo y verificar contra ESA ruta.
  - ⚠️ Cuidado con los clientes de varias líneas: una misma marca puede tener **sedes distintas con estética distinta**, y usar la foto de la otra sede es un FAIL de D5 aunque la foto sea real. El caso canónico es Marca Crema (Estudio ≠ Pilates ≠ Online ≠ App).
- **D4 · Línea + estética correctas.** La disciplina pertenece a la línea correcta del cliente y usa SU estética y SU CTA. (Ej. Lagree/reformer = **Pilates** → estética cream/Helvetica + CTA "Agenda tu visita"; Estudio = navy + "Comienza tu clase hoy / +16 disciplinas". Ver memoria sobre las lÃ­neas de la marca.)

## D-CALIDAD. Copy — el hook y el texto NO pueden ser genéricos (FALLA lo estándar)
> **Por qué existe (director creativo, jul-2026):** la sección D de arriba solo chequeaba HIGIENE (real, claro, español neutro, línea correcta) — un copy podía cumplir todo eso y ser **estándar/plano**, y nada lo rebotaba. Estos checks igualan el rigor del copy al del diseño: un FAIL = reescribir el copy y re-verificar, NO se muestra. El método completo está en **`COPY.md`**; acá se hace CUMPLIR.
- **DC1 · No suena a IA (Regla #1) — FALLA si aparece:** triadas/paralelismos perfectos ("más X, más Y, más Z"), clichés de transformación ("tu viaje/mejor versión/transforma tu vida/el método correcto"), relleno ("descubre cómo/la clave está en/es importante"), vaguedad ("resultados reales/de verdad/que se sostienen"), o promesa demasiado simétrica y pulida.
- **DC2 · Hook problema-primero.** El slide 1 nombra el **problema/estado**, NO la marca ni la solución; **auto-selecciona a la clienta** O es **contrarian/dato que choca**; **≤12 palabras** visibles; una sola idea. FAIL si el hook abre con la marca/solución, es genérico o dice dos cosas.
- **DC3 · Deseo + voz de la clienta (el antídoto al "competente pero plano").** El copy toca un **deseo emocional** (LF8), no solo una feature; usa al menos **una palabra/escena que la clienta diría** (VoC). FAIL si suena a "buen copy de marca" abstracto sin deseo ni registro real de la clienta.
- **DC4 · Comprimido, no explicado.** Sin muletillas/calificadores recortables ("no solo dentro", "que se nota cuando…"); prefiere sustantivo+imagen concreta. FAIL si una frase necesita una coma explicativa para entenderse (casi siempre sobra).
- **DC5 · Pendiente resbaladiza.** Cada slide termina con curiosidad/beneficio acumulado y empuja al swipe; NINGUNA slide intermedia "cierra" el tema antes del cierre. FAIL si una slide se auto-completa y mata el swipe.
- **DC6 · Primary text estructurado.** Apertura (1 línea gancho) + punteos con emoji + cierre CTA/promo, **separados con enters** — nunca párrafo corrido. FAIL si va en bloque.
- **DC7 · Variantes + método aplicado.** Se entregaron **3 finalistas del hook de familias DISTINTAS** (el embudo de ~20 candidatos por familia del Paso B de `COPY.md`) y el copy pasó el **checklist de calidad de `COPY.md`**.
- **DC8 · ~~Recibo de un juez de copy~~ — SIN COMPUERTA.** Los dos jueces de texto se eliminaron el 10-ago-2026 por decisión del director creativo: el panel de comprensión (§35) y el de craft (§36). Lo único que corre sobre el texto es `verify.py copy` (script mecánico) → `_copy-gate-receipt.json`. **Nadie revisa hoy que un claim sea sostenible.**
  - ~~Recibo de comprensión (`_copy-receipt.json`, ≥3 lectores ciegos, claridad ≥4)~~ — **derogado por el director creativo el 10-ago-2026**. Ya no se juzga comprensión en carruseles: la aprueba él en la Fase −1. Historia: `APRENDIZAJES.md` §35.
> **Juez de distintividad:** al leer el copy, además de "¿se entiende?" preguntar **"¿este hook es del montón / se me olvida / pararía el scroll?"** → si es olvidable = FAIL, aunque sea claro y correcto.

## E. Mecánica (lo cubre el auto-lint, debe ir 0 FAIL)
- **E1 · Contraste** texto/fondo legible. (Excepción documentada: preset Pilates corre más etéreo; juzgar legibilidad real al ojo, no solo el número.)
- **E2 · Márgenes seguros** (nada cortado).
- **E3 · Tipografía (tamaños mínimos):** cuerpo/**subtítulo** **≥36px**, **titular HÉROE ≥90px** (típico 95–150; el/los que llevan `t-xl` y DOMINAN el cuadro; debe haber ≥1 por carrusel), eyebrow ≥27px, CTA ≥32px. *Las cifras viven en `templates/constantes.py` (`HERO`, `PISO_CTA`, `PISO_CUERPO`, `PISO_EYEBROW`, `PISO_ABSOLUTO`) — si se cambia, se cambia AHÍ y los scripts lo importan.* **Títulos SECUNDARIOS (no-héroe, sin `t-xl`) pueden ir 64–94px** siempre que (a) DOMINEN claramente a su subtítulo —contraste de escala ≥1.6×— y (b) el carrusel tenga ≥1 `t-xl`. Un título marcado `t-xl` SIEMPRE debe ser ≥95px (si está bajo eso, o se sube el tamaño o se le quita el `t-xl`). **Ningún preset baja el cuerpo de 36** (ej. el preset Pilates estaba en 32 = MAL). Rag balanceado, frase enfatizada (`<em>`) sin partir, sin huérfanas.
- **E5 · Salto de escala (gold-standard; semántica CONJUNTIVA, 3-ago-2026):** `templates/qa_typesize.py` FALLA el carrusel solo si se cumplen **las dos cosas a la vez**: el título mayor **< `t-xl` (104px)** **Y** no hay salto sobre la escala del resto (ratio título mayor / mediana de títulos **< 1.6**). Un carrusel con héroe t-xl y secundarios cercanos (120/92 = ratio 1.3) es una decisión de diseño válida que pasa — la disyuntiva anterior ("t-xl o ratio") reprobaba trabajo ya aprobado. Lo que E5 castiga es el carrusel PLANO Y CHICO: todos los títulos al mismo tamaño y bajo t-xl (falla real en Cool Barre/Dance, que se quedó en t-m/t-l). El `qa_lint` no mide salto de escala. Vara visual: `disciplinas-valor/version-c-sistema`.
- **E4 · Consistencia:** logo presente y en la MISMA posición en todas las slides; tono coherente; CTA claro. **SIN paginador** (regla universal, el director creativo 29-jul-2026): cualquier número de slide en una esquina (`0X · 0N`, `1/6`, puntitos) = **FAIL**. La cohesión la da el wordmark repetido, no un contador.
- **E6 · Logo/wordmark SIN CHOQUES (verificar SIEMPRE, a tamaño completo).** El wordmark NO debe solaparse ni rozar NINGÚN texto (kicker, título, subtítulo, CTA) ni un objeto clave. **El logo NO está "arreglado para siempre" por ponerlo en una esquina:** cada texto/escena nueva puede invadir su zona (caso real jun 2026: en slides de banda superior el kicker arrancaba a la misma altura del wordmark y chocaban). Revisar la franja del logo en CADA slide; si un texto entra en la caja del wordmark → **FAIL** (bajar el bloque de texto o reubicar el logo).

- **E7 · Sombra de texto = color del FONDO pero OSCURO, nunca negro, y DIRECCIONAL abajo-derecha (regla del director creativo, jun 2026).** Cuando el texto lleva sombra para legibilidad: (1) el color de la sombra es el **color del fondo de esa zona pero oscurecido** (ej. fondo lavanda `#EDE4F8` → sombra ciruela-lavanda `#2E1B40`), **JAMÁS negro** (el negro ensucia y "despega" el texto del fondo). (2) La sombra es **direccional, proyectada hacia la esquina INFERIOR-DERECHA** (offset positivo `x` e `y`), NO un glow/halo que rodea las letras por los 4 lados. Forma correcta: `text-shadow: 3px 3px 4px rgba(<fondo-oscuro>,.55)` (offset diagonal, blur bajo). MAL: `text-shadow:0 2px 10px ...` (centrado/halo, se sale por arriba). El director creativo: "la sombra se sale un poco por arriba; quiero que salga solo en la esquina inferior derecha".

- **E8 · PISO tipográfico ABSOLUTO (director creativo, 8-jul-2026 — reincidencia, tolerancia cero):** NINGÚN texto visible bajo **26px @1080** (burbujas de chat, metas y captions incluidos); cuerpo/lead ≥36px; CTA ≥32px; ≥1 héroe ≥90px. Se hace cumplir con `templates/qa_typesize.py` (determinista, correr en todo render custom porque `qa_lint.py` no ve font-size inline) ADEMÁS del ojo del juez: si dudas de que un texto se lea en un iPhone dentro del feed → FAIL.

- **A7 · El diseño CONVERSA con la imagen — mapa persona+luz (director creativo, 8-jul-2026):** ningún elemento (texto, tarjeta, CTA, badge) sobre la **cabeza/cara ni el eje central** de la persona (0%); extremidades solo roce ≤12% en esquina; **tarjetas NUNCA sobre el FOCO de luz** de la imagen (la luz es parte del mensaje visual). Se hace cumplir con `templates/photo_map.py` + máscara local `~/bin/cutout` (Vision macOS): el builder valida los MISMOS boxes que renderiza (`MAPCHECK` fail-closed). El juez además mira el `_map-*.png` de debug si existe.

- **A6 · Encuadre sin ESPACIO PERDIDO — la imagen se mueve, no el texto (director creativo, 8-jul-2026):** (1) el sujeto va FLUSH a su borde: ≤8% de aire muerto detrás de su espalda/lado; (2) **ninguna franja vertical >15% del ancho sin contenido** (ni sujeto ni texto) = FAIL "espacio perdido"; (3) la mano/objeto del sujeto NO invade la columna de texto (el bbox se mide COMPLETO, extremidades y objetos incluidos — falla real: mancuerna al centro casi tapada por el texto); (4) el fix por defecto es **REENCUADRAR la imagen** (zoom/pan con `templates/framer.py`), no mover el texto; si el encuadre no da → cambiar la foto.

- **E9 · Pastillas contienen su texto + CERO choque entre elementos (director creativo, 8-jul-2026):** toda pastilla/badge/CTA CONTIENE su texto (auto-ancho `width:max-content` / solo left+top — NUNCA ancho fijo que deje el texto afuera); ningún elemento (texto, badge, pastilla, CTA, tarjeta, chip, logo) se solapa con otro, y entre **pastilla y texto se exige ≥12px de aire** (no basta con no-solapar: 2px de roce ya se ve mal). Se hace cumplir con `templates/qa_geom.py` (modela el rect REAL con métricas de fuente: ancho real de la pastilla y alto real del texto por word-wrap). Fallas reales que lo motivaron: badge "ESCÁNER DE COMIDA" con texto fuera de su pastilla, y título "¿Y qué cocino hoy?" pegado (2px) a la pastilla "RECETAS".

## F. Brief (coherencia con el pre-flight)
- **F1 · Existe `_brief.md`** en la carpeta del carrusel (cliente, línea/sede, brand brain, fotos fuente, CTA, modelo).
- **F2 · El carrusel ES coherente con su brief:** la línea/estética/CTA/locación de las slides coinciden con lo declarado. Disciplina pertenece a esa línea. Si el brief dice una sede y las fotos muestran otra (o una inventada) → FAIL.

---
**Salida del verificador:** `_qa-receipt.json` en la carpeta del carrusel, con `verdict` (PASS/FAIL), `lint_fail` (n°), y por slide los ítems que fallan con el fix. El **hook `carrusel-gate`** bloquea abrir la preview si el recibo no existe, está desactualizado (cambiaste slides después) o es FAIL.

---
## ⚙️ Press Start 2P solo soporta ASCII — kickers/CTA SIN tildes ni ¿¡ (jun 2026)
La fuente pixel **Press Start 2P** (kickers, CTA, paginador) NO tiene glifos para vocales acentuadas (Á É Í Ó Ú) ni `¿¡`: Chrome los renderiza como un símbolo roto (caso real: "AQUÍ" salió "AQUI±"). Por eso los textos en Press Start van **en MAYÚSCULAS y SIN tildes** ("AQUI ENTRA VERDE", "GAME OVER" sin "?"). En español, las mayúsculas pueden ir sin tilde, así que es ortográficamente válido. El cuerpo y el título (Archivo) SÍ aceptan tildes normalmente. El verificador debe leer el kicker/CTA en el PNG y marcar FAIL si ve un glifo corrupto.

## ⚙️ Regla de RENDER — NUNCA base64 en los HTML de trabajo (ahorro de tokens, auditoría jun 2026)
El `build.py` de CUALQUIER cliente debe referenciar las imágenes por **ruta relativa** (`<img src="../raw/s1.png">`, wordmark `../../logo.png`), **NO** `data:image/png;base64,…` inline. Chrome headless con `file://` renderiza **byte-idéntico** (verificado: mismo MD5 de píxeles). Motivo: el base64 inflaba cada slide HTML a **6-7 MB ≈ 1,6M tokens**; un solo `Read` del HTML reventaba la ventana. El base64 se reserva SOLO para el **artefacto final** de entrega a terceros (un HTML portable), nunca para los HTML que el agente/jueces/editor tocan.
- **El juez `carrusel-qa` y el orquestador NUNCA hacen `Read` de un slide `.html`** — el copy ya está en el PNG; leerlo se hace mirando el PNG (o el `copy.md`/`_brief.md` para texto plano). Forzado por el hook determinista `no-read-base64.py`.
- Esto NO cambia el QA: los jueces siguen leyendo TODOS los PNG a tamaño completo. Solo elimina desperdicio puro.

---

## E10 · VELO ADAPTATIVO — se MIDE la luz, no se pone un scrim fijo (director creativo, 14-jul-2026)

**Falla que lo originó (dos veces, dos marcas):** en Marca Bronce el navy tapaba a las mujeres; en Marca Crema
Online el scrim lateral (.92) MÁS un pozo de sombra (.62) se apilaban → ~0.97 de opacidad, un muro negro
sobre media foto. El director creativo, las dos veces: *"es demasiado lo que tapa, se ve mal, revisa la transparencia"*.

**La regla:** el oscurecimiento detrás del texto NO es una constante del template. Se **mide la luminancia
real de la foto bajo el bloque de texto** (percentil 80) y se aplica **solo el alfa necesario** para que el
texto se lea:

```
A = 1 - 0.42 / L        # deja la zona del texto en ~0.42 de luminancia
A = clamp(A, 0.14, 0.56) # piso: anclaje mínimo · techo: la foto SIEMPRE respira
```

Resultado real: foto oscura (galpón, selva) → **A ≈ 0.14**, el velo casi no existe. Foto de casa con
ventana → **A ≈ 0.50**. Nunca un muro.

**Corolarios:**
- **Una sola capa.** Prohibido apilar scrim + pozo + panel: se suman y ennegrecen. Si hace falta cubrir todo
  el bloque de texto, el gradiente lleva una **meseta plana** hasta el final del texto y recién ahí se apaga.
- **El panel opaco (`l-block`) NO es red de seguridad — ver E10.b.** Si se usa "por si acaso" en el
  cierre, el resultado es una slide negra con la modelo sepultada. Como arquetipo deliberado de
  quiebre (bloque de color, 1 vez por carrusel, elegido a propósito y no como fallback) sí es válido.
- Verificar SIEMPRE mirando el PNG: si no se distingue qué hay al lado del texto, el velo está de más.

### E10.b · El PANEL OPACO queda PROHIBIDO como red de seguridad (director creativo, 14-jul-2026)

El director creativo marcó 6 slides como "la mitad de la imagen se ve negra". Eran **exactamente** las 6 que caían al
panel opaco (`l-block`) — ninguna otra. El velo adaptativo funcionaba; lo que arruinaba las piezas era el
fallback.

Peor aún: los fallos que lo disparaban eran **mínimos** (3%, 5%, 6%, 10% de roce) y uno era el **número de
página**. Por un roce del 3% el motor pintaba medio cuadro de negro.

**El orden correcto cuando el texto choca con la modelo** (`references/composicion-y-tipografia.md` §2, "mover la imagen, no el texto"; el mismo orden del motor y de SKILL.md):
1. **REENCUADRAR la foto.** Las apaisadas se panean en horizontal, las verticales en vertical. Con esto se
   arreglaron 4 de las 6 solas: la modelo sale de la zona del texto por sí misma.
2. **Angostar la columna de texto** para que TERMINE antes de la modelo (arregló las 2 restantes).
3. **Bajar el título hasta su piso** (los pisos de `templates/constantes.py` no se negocian).
4. Cambiar de foto.
5. **Nunca** un panel opaco. El velo se MIDE (E10) — no se "sube" como remedio anti-choque.

Además: el **logo es chrome de esquina** — no se le exige el mapa de persona. Exigírselo
dispara fallbacks catastróficos por un elemento de 20px que a nadie le molesta.

---

## E11 · WARN ACEPTADO CON RAZÓN ESCRITA — los recibos no son binarios (3-ago-2026)

Los recibos de `verify.py` distinguen `fails` y `warns` (campo `status`):
**0 fails + N warns → `PASS_CON_WARNS`** — la puerta pasa igual (el hook lee `verdict`,
que sigue en PASS), pero los warns quedan listados en el recibo. Dos formas de cerrarlos:

- Con `--warn-ok "razón"`: la razón queda grabada en el recibo (`warn_ok`) y el WARN queda
  aceptado **por escrito**. Es la forma correcta de cerrar un WARN deliberado.
- Sin el flag: el recibo dice `warns_sin_razon: true` y **los jueces de la Fase 7 tienen
  que revisarlos uno por uno** — un WARN sin razón no es un pass, es una pregunta abierta.

Lo que es WARN y no FAIL (lo decide el script, no el agente): gap título-contenido <16px,
densidad por bandas, qa_dom sin correr por dependencia ausente, costuras dudosas. Un WARN
nunca se "resuelve" borrándolo del recibo: se corrige la causa o se acepta con razón.

## E11.b · DOCTRINA ANTI-ORNAMENTO — la densidad se satisface con contenido, nunca con decoración (3-ago-2026)

Las métricas de densidad y espaciado (bandas vacías, huecos entre bloques) existen para
cazar slides pobres de contenido, **no para exigir relleno**. Si una slide es deliberada
(un arquetipo `l-topleft` que concentra el bloque arriba y deja respirar la foto abajo),
el WARN de densidad **se acepta con `--warn-ok` y ya**. Lo que está PROHIBIDO es
satisfacer la métrica agregando ornamento: separadores decorativos, bullets de relleno,
iconos que no comunican, una línea extra que no dice nada. *Decorar para que el script
dé verde es exactamente la falla que el script quería prevenir.* Razón escrita > ornamento.
