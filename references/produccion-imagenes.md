# PRODUCCIÓN DE IMÁGENES — fotos reales, Higgsfield y pool de assets

> **Qué legisla.** De dónde sale la imagen de cada slide y cómo se genera si no existe.
> Va DESPUÉS de elegir formato (`tipos-y-formatos.md`) y del copy, y ANTES de componer
> (`composicion-y-tipografia.md`). **Lugar siempre real, datos siempre reales.**

---

# 0. AUDITORÍA DE LA FOTO CRUDA — antes de componer, siempre (jul-2026)

> **Por qué existe.** En el test de ads de Claude Code se generaron 16 fotos, se compuso
> encima y recién los jueces vieron el desastre: **8 de 14 traían letras inventadas** dentro
> de la imagen, dos traían el logo de Apple y dos tenían anatomía imposible. Los 16 prompts
> decían *"no text, no logos"*. El pipeline no falló al pedirlo: falló al **no mirar el crudo**.

Entre generar y componer va SIEMPRE este paso. Sobre cada foto de `raw/`:

1. **Hoja de contacto de los crudos + una lectura a tamaño completo.** Barato y caza casi todo.
2. **Texto inventado:** ¿hay glifos en pantallas, teclas, papeles, paredes? → descartar.
   Es el defecto que más delata "generado", sobre todo con público técnico.
3. **Logos de marca real** (manzanas, wordmarks en un laptop) → descartar o retocar.
4. **Anatomía:** manos, cabezas cortadas, figuras duplicadas, miembros imposibles.
5. **¿La zona de texto planificada quedó realmente libre?** (§0.2, es el chequeo que faltaba)

## 0.1 La ilegibilidad se DISEÑA, no se pide

**Pedirle al modelo que no escriba texto no funciona.** Se comprobó en tres rondas: `soul_2`
ignoró *"no readable text"* en 8 de 14 imágenes, y al pedir *"completely out of focus"* devolvió
la pantalla llena de dígitos nítidos igual.

Lo que SÍ funcionó fue quitarle la superficie donde escribir:

| En vez de pedir… | Encuadrar así |
|---|---|
| "teclado sin legends" | **macro extremo**: 2-3 teclas llenan el cuadro, superficie lisa |
| "pantalla sin texto legible" | pantalla **fuera de cuadro**, solo su luz sobre el escritorio; o el monitor **de espaldas** |
| "cuaderno sin escritura" | cuaderno **cerrado** |
| "pared sin carteles" | *"one uninterrupted bare wall, nothing hanging"* explícito |

⚠️ Cada solución trae su propio riesgo: el monitor visto por detrás es justo donde está el
**logo**. Verificar el crudo igual.

## 0.2 ¿La zona reservada sobrevivió? — chequeo determinista

El blueprint pide *"subject in the RIGHT THIRD, the left continues as empty negative space"*.
En el test **11 de 16 lo respetaron**; en 5 el sujeto se corrió al centro o un objeto cruzó
el eje (una tablet llegó al 68% y el texto le cayó encima). O sea: el orden es correcto pero
**no hay garantía**, y hoy nadie lo mide hasta que la pieza ya está compuesta.

Entre generar y componer:

```
~/bin/cutout raw/s-0N.png mask.png --mask      # 1 seg, Vision de macOS
photo_map.check(caja_de_texto_planificada)     # ¿<5% de sujeto y textura baja?
   ├─ OK        → componer
   ├─ roce      → REENCUADRAR con framer.py (mover la imagen, no el texto — E10.b)
   ├─ invadida  → el mapa es ASIGNADOR: reubicar el texto al hueco real (regla 4)
   └─ sin hueco → cambiar de foto o regenerar
```

`photo_map.py` y `framer.py` ya existen y hoy se usan **después** de componer, como compuerta
final. Acá se usan **antes**, que es donde sirven.

## 0.3 Tope de reintentos: 2 por slide

En el test se gastaron 32 generaciones y tres slides nunca pasaron: cada reintento cambiaba un
problema por otro (texto basura → logo → costura visible → anatomía imposible). **El ciclo no
converge solo.** Después de 2 intentos fallidos: cambiar el ENCUADRE del plan (otro objeto,
otro ángulo) o cambiar la slide. Nunca un tercer intento del mismo plan.

---

## 1. Primero: fotos REALES del cliente

1. **Investigar fotos reales del cliente.** Leer (Read) las fotos candidatas. Clasificar bien (ej. Marca Crema: Pilates ≠ Estudio, ver memoria del cliente). Si falta una foto → **generar con Higgsfield**, sin texto, **respetando el buyer persona** (edad/género/cuerpo — ej. Marca Crema = mujer 35-45, esbelta, nunca jóvenes; ver memoria).

### 1.1 Videos del brand-brain = fuente extra de imágenes
**🎬 REVISAR VIDEOS del brand-brain (solo si existen).** Buscar `.mp4/.mov/.m4v` en la carpeta del brand-brain del cliente. Si hay → mirarlos y extraer **frames nítidos** (`ffmpeg -i video.mp4 -vf fps=1 out_%03d.jpg`) que muestren la sede/persona reales y sirvan de imagen adicional. Es una fuente extra clave para cumplir A8 (imágenes distintas) sin repetir ni inventar. Si NO hay videos, saltar. (RUBRIC A9.)

### 1.2 Imágenes DISTINTAS — cero repetición (regla dura A8)
**🖼️ IMÁGENES DISTINTAS (regla dura A8):** cada slide con imagen usa una imagen DISTINTA — cero repetición dentro del carrusel. Antes de renderizar, listar la imagen asignada a cada slide y confirmar que NO se repite ninguna; si faltan imágenes distintas → generar con Higgsfield o sacar frames de video, nunca repetir. Verificación determinista: contar `src=` de los PNG (2+ = FAIL).

### 1.3 Catálogo del pool + anti-repetición
**CATÁLOGO COMPLETO DEL POOL + ANTI-REPETICIÓN (director creativo, 8-jul-2026).** Falla real: con 82 fotos del cliente disponibles, el motor usó 1 foto en el 31% de los slides. Regla: antes de un lote, correr **`templates/asset_catalog.py <fotos> <assets> <tags.json>`** — mapea el pool ENTERO (máscara local + bbox + score de limpieza por región + tags semánticos por patrón de archivo) a `catalog.json`. El motor elige del catálogo con: (a) filtro de FACTIBILIDAD dura (≥1 región limpia), (b) **tope de usos** (máx 2 por lote, 1 por carrusel), (c) orden por menos-usada, y (d) **fallback de hermanas semánticas** (si una foto no da espacio, prueba las siguientes del mismo tag y variantes de encuadre). Rotar de verdad es parte del diseño, no un nice-to-have.

### 1.4 Diversidad del cierre en lotes
**DIVERSIDAD DEL CIERRE en lotes (director creativo, 8-jul-2026).** El cierre repite MENOS imágenes que el contenido porque hay pocas fotos con "lado limpio" para el panel. Con 3 fotos de cierre en un lote de 20, cada una sale ~7× → se nota. Regla: armar el **pool de cierre con ≥6 escenas DISTINTAS** (playa, tropical, galpón, desierto, barn, neón…) cada una con un lado lateral genuinamente libre (`max(bbox.x0, 1-bbox.x2) ≥ 0.30`), rotándolas → cada cierre baja a ~3×. Medir la repetición real del lote (contar `src=` de los PNG) y si alguna imagen supera ~4× de 80, diversificar antes de mostrar.

---

## 2. Generar con Higgsfield cuando la foto no existe

### 2.1 Qué se genera y qué NO — decisión por slide
| Tipo de slide | Cómo se genera |
|---|---|
| Cover con persona | Higgsfield Nano Banana Pro (`nano_banana_2`) — generar UN slide ancla primero |
| Resto de slides con la misma persona | Higgsfield con el slide ancla como referencia (`--image generados/.../ancla.png`) para mantener consistencia |
| Slide tipográfico puro | HTML+CSS solo. NO Higgsfield (es malo con tipografía precisa en español) |
| Slide con producto del kit | **Foto oficial real** (`imagenes-oficiales/`) sobre fondo HTML, o `kit-marca-fondo-crema.png` (kit completo con fondo editorial ya hecho) |
| Slide con salón real | Foto real de Cami (`fotos-salon-reales/cami-nuevas/`). Si no hay → Higgsfield modo `lifestyle_scene` |
| Mockup/diagrama | HTML+CSS solo |

### 2.2 Reglas de prompt (validadas en producción)
- Aspect ratio **1:1 (1080×1080)** por defecto — regla de la casa, reconfirmada por el director creativo el 3-ago-2026 (Meta recomienda 4:5 para Feed, pero la recomendación de plataforma no pisa el gusto del dueño); 4:5 solo si el spec pide `"canvas":"4:5"`
- Sin "vacío"/"negative space" literal → IA lo interpreta como banda blanca real abajo (visto en CE1 slide 9)
- Pedir "fill the entire frame edge to edge"
- Con referencia: "Keep all visual characteristics from the reference image: face, hair texture, palette"
- NO describir marca por nombre cuando hay referencia (la IA lo reinventa)
- NSFW filter del modo `lifestyle_scene` es agresivo con "mujer 28-35" → usar inglés neutro o saltar a `nano_banana_2` directo

### 2.3 Espacio negativo: continuidad de escena, NO un corte
**ESPACIO NEGATIVO AL GENERAR CON HIGGSFIELD — es CONTINUIDAD de la escena, NO un corte (corrección el director creativo 7-jul-2026).** **Desde el 6-ago-2026 esto NO se escribe de memoria:** `templates/prompt_zona.py armar <carpeta>` deriva la cláusula exacta de la geometría real del motor (`COLUMNAS`+`MARGEN`) para el `zone` de cada slide, y `verify.py prompt <carpeta>` la verifica **antes** de gastar la generación (recibo `_prompt-receipt.json`, exigido por la puerta GENERAR). Lo de abajo es el porqué; el script es el cómo. El blueprint (0.5) decide la zona de texto ANTES de generar; acá va cómo pedírselo al modelo. En el prompt: posición del sujeto (`subject/device in the RIGHT THIRD`) + la zona reservada como **extensión suave de la MISMA escena** (`the same dark studio scene continues toward the left as smooth empty negative space — same background + the glow gently FADING to that side, one continuous atmosphere with particles/depth, NOT a hard black block, no cut or seam`), con el glow entrando del lado del sujeto. ⚠️ **NUNCA pedir "empty black / clean empty space" a secas:** la IA lo interpreta como medio rectángulo NEGRO MUERTO pegado a la escena y la imagen se ve cortada en dos. **Si ya hay una imagen que GUSTÓ pero con el sujeto mal ubicado → NO regenerar de cero:** usarla como referencia image-to-image (`medias` role `image` con su `job_id`) y pedir *"keep the phone and its on-screen UI EXACTLY as the reference, reposition it to the right third, and extend the same scene continuously to the left"*. Preserva lo aprobado y solo recompone. Para un carrusel: **storyboard de layouts de TODAS las slides primero** (zona de texto de cada una, sin repetir la vecina), y generar cada imagen con SU espacio reservado.

### 2.3b NUNCA pedir "la mitad vacía": pedir CAÍDA GRADUAL (29-jul-2026)

Falla real (lote Marca Verde, 10 de 34 fondos): la fórmula *"the whole LOWER HALF is the same scene
continuing as smooth empty negative space"* hizo que el modelo entregara **dos imágenes pegadas**,
con una línea dura horizontal en la mitad exacta del cuadro y los props rebanados a media pieza.
Salto de luminancia medido en la costura: **60 contra un ruido normal de 3,7**.

Es el mismo error que §2.3 documenta para el eje vertical, y aparece igual aunque se diga
"smooth", "no cut", "no seam", "no border": nombrar **"la mitad"** ya le da al modelo un borde.

| En vez de… | Pedir |
|---|---|
| "the whole LOWER HALF is empty negative space" | "the glow falls off **gradually** toward the bottom edge, the props sitting high in the frame with progressively emptier space below — one continuous gradient, no midpoint, no dividing line" |
| "the RIGHT HALF is empty" | "the scene **thins out** toward the right edge" |

Y al verificar: **medir la costura en los DOS ejes.** `qa_seam.py` solo escanea columnas.

### 2.4 Misma persona entre slides = Reference Element
**⚠️ MISMA PERSONA entre slides = Reference Element, NO medias sueltas.** Cuando un carrusel necesita la MISMA modelo en varias slides: (a) generar/elegir 1 foto buena de la persona; (b) crear un **Reference Element** (`show_reference_elements action=create`, category character) con esa imagen subida como `media_input`; (c) en cada `generate_image` embeber **`<<<element_id>>>`** en el prompt y describir SOLO la escena/pose/disciplina — NO las características físicas de la persona. Pasar la persona como `medias` suelta + describirla en texto DERIVA (sale otra persona cada vez). Proceso completo en memoria `reference_higgsfield_personajes_coherentes`. La referencia de **entorno** sí puede ir como media aparte.

### 2.5 Anti-deriva del personaje de marca (mascota/avatar oficial)
**🔴 ANTI-DERIVA del personaje de marca (mascota/avatar oficial — auditoría jun 2026).** Con una mascota OFICIAL (ej. la mascota), el `<<<ref>>>` solo en un prefijo NO basta: cuando la POSE de la escena se aleja de la pose neutra de la referencia (saltando, durmiendo, sentado de perfil, sujetando algo), el modelo INVENTA un primo parecido (cubo verde genérico) que pierde los rasgos. Reglas obligatorias para evitarlo:

     1. **Re-anclar `<<<ref>>>` en CADA mención del personaje** dentro del prompt. No escribir "the cube mascot" suelto: escribir "`<<<ref>>>` the la mascota mascot".
     2. **Listar los rasgos NO-NEGOCIABLES en cada prompt**, como checklist literal. Ej. la mascota: *"exact same character — leaf with veins, TWO greens lime face + dark-green side, THICK black outline, oval black eyes + open mouth with red tongue, little gold coin with a 0, square pixel body"*. Cerrar con *"do NOT redesign or simplify the character; it must be identical to the reference."*
     3. **Mantener la pose CERCA de la neutra** cuando se pueda. Las poses extremas (dormir, saltar) son las que más derivan → si son necesarias, reforzar los rasgos ×2 y revisar esa slide con lupa contra la referencia (RUBRIC **C6**).
     4. Tras generar, **comparar cada escena contra la imagen de referencia oficial.** No asumir que el `<<<ref>>>` funcionó. Si derivó → regenerar con los rasgos reforzados; **NO** seguir al diseño con un personaje que no es el de marca.

     > ⚠️ **Estas 4 reglas se habían PERDIDO** al migrar la skill: la sección quedaba cortada justo en "Reglas obligatorias para evitarlo:" sin ninguna regla debajo. Restauradas desde `DISENO_CARRUSELES_PROBAR` el 31-jul-2026. Existen porque 4 slides de Marca Verde pasaron DOS jueces con un cubo verde genérico que ya no era la mascota — nadie comparó contra la referencia.

### 2.6 Gráfica extra (device/objeto) = por referencia
**Gráfica extra (device/objeto) = Higgsfield POR REFERENCIA (rápido, el director creativo 8-jul).** Si una slide necesita una gráfica añadida (ej. un teléfono con la app al lado de Marca Crema), NO dibujarla a mano ni describirla por texto: generarla con Higgsfield **image-to-image usando como referencia un asset YA generado** del mismo objeto (un mockup previo del teléfono/UI) para que CALCE en estilo/ángulo/UI; o si el asset previo sirve tal cual, **reutilizarlo** (cutout local `~/bin/cutout` + composición) = aún más rápido y 100% consistente. Es rápido — usarlo sin miedo. Regla de consistencia: [[reference higgsfield]] / `brand-brain/crema/ads-consistencia-visual.md`.

---

## 3. La imagen tiene que DEMOSTRAR el mensaje

### Espacio creativo — la imagen co-comunica (OBLIGATORIO, antes de elegir/generar cada foto)
La imagen NO es decoración: debe **representar y reforzar el mensaje de la slide**. Antes de elegir o generar la foto de CADA slide, responder dos preguntas:
1. **¿Qué comunica el texto, y qué le falta?** ¿Qué quiero transmitir que el texto no dice? ¿Qué puedo comunicar SIN texto, dejando que la imagen lo diga (una sensación, una idea, una prueba visual)?
2. **¿La imagen apoya o contradice el texto?** ¿Hace de soporte visual al mensaje, o muestra otra cosa? Si es neutra/decorativa o lo contradice → cambiarla o generarla.

**Investigar las poses/movimientos reales de la disciplina ANTES de generar (obligatorio).** No basta con decirle a Higgsfield "es entrenamiento X, varía ángulos" — eso hace que la IA improvise poses raras/incómodas (ej. una tela que quedó lánguida, "como desmayada"). Antes de generar: investigar (web si no las conoces) los **nombres de las poses reales** de esa disciplina y pedirlas explícitas por slide (ej. tela: hip key, gazelle, straddle/split, hammock/cradle, footlock; NUNCA "suspendida genérica"). La pose debe verse **controlada y segura**, nunca colapsada.

Aprendizaje fundacional (2026-06-09): el cierre decía *"No eliges una. Las rotas. +16 disciplinas, una membresía"* (idea = variedad/abundancia) pero la foto era una mujer caminando/saliendo → comunicaba "una/individual", lo OPUESTO. La representación correcta: un **plano amplio con varias disciplinas a la vez** (variedad en un frame). La foto debe REPRESENTAR la idea, no solo acompañar.


### 3.1 Calce semántico en motores batch
**CALCE SEMÁNTICO EN MOTORES BATCH — la imagen DEMUESTRA el mensaje (director creativo, 8-jul-2026).** Falla real: a escala de 20 carruseles, el motor eligió fotos por rotación/espacio y una slide "entrenan juntas aunque estén lejos" mostró un pantallazo de clase (no demuestra nada). El paso "Espacio creativo" del skill aplica TAMBIÉN al motor: **cada slide de la receta declara su `visual_need`** (qué debe MOSTRAR la imagen: "amigas entrenando por videollamada", "mujer entrenando en su living frente a la clase", "mamá entrenando con su hijo al lado") y el asset se elige por **etiqueta semántica, nunca por rotación estética**. Si NO existe un asset que lo demuestre → **generarlo en Higgsfield** (blueprint de espacio negativo + persona 35-45 disfrutando + por referencia si hay objeto que deba calzar) o cambiar el mensaje. Un motor sin esta etapa queda PROHIBIDO.

### 3.2 Vista previa de clase = lower-third de video
**VISTA PREVIA DE CLASE = LOWER-THIRD DE VIDEO, nunca foto de fondo (director creativo, 8-jul-2026; refinado 8-jul PM).** Cuando una slide muestra una clase real, debe LEERSE como video: chip ▶, **barra de reproducción con progreso**, caption de la clase. **La forma robusta es un lower-third** (scrim inferior fuerte `.s-prev` + badge + caption + barra en el tercio inferior, como chrome de video): así la clase se ve ENTERA arriba y NO hay que buscar zona limpia para el texto → **todos los frames de clase sirven** (variedad real) y ninguno cae a un fallback tipo "living con TV". Falla que lo motivó: poner la caption ARRIBA la chocaba con la cabeza del sujeto (frames de gente parada/sentada) → el 48% de los previews caía a `gen-livingtv` (no es una clase) y solo 2 frames pasaban. Con lower-third: 21/21 previews con clase real, 7 frames distintos. **Duración:** NO inventar minutos si la vista previa no dura eso — el badge dice "Vista previa en el sitio web" y la barra va SIN tiempos (director creativo: "la vista previa no es de 30 min"). El caption/badge del lower-third se validan con GEOM (que no choquen/desborden), pero NO con MAPCHECK-persona (es chrome deliberado sobre scrim, como la barra).

---

## 4. Al colocar: el mapa asigna, no solo bloquea
**EL MAPA ES ASIGNADOR, no solo compuerta (director creativo, 8-jul-2026).** El photo_map de cada slide queda EN MEMORIA del builder: cuando un elemento queda APRETADO (gap < mínimo, columna saturada, CTA "muy apretado"), NO encoger ni apretujar → **consultar las zonas LIBRES del mapa y REUBICAR elementos ahí** (ej. mover el kicker/badge al espacio libre sobre la cabeza del sujeto). Redistribuir > comprimir, siempre.

## 5. Velocidad
**VELOCIDAD (director creativo 8-jul).** (a) Las 3 compuertas deterministas (MAPCHECK persona+luz · qa_typesize · qa_geom bounds/solape/pastillas) corren en segundos y cazan el ~90% → iterar contra ELLAS, no contra el ojo de un agente. (b) Jueces LLM = pase LIGERO y ÚLTIMO, solo para lo que la máquina no ve (contenido semántico de la imagen, expresión, jerarquía); con las deterministas en verde basta 1 pase (o 2 baratos), no re-juzgar geometría. (c) **Re-render solo la(s) slide(s) tocada(s)**, nunca el carrusel entero por un fix de 1 slide.
