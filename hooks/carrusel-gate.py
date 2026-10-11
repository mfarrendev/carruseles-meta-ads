#!/usr/bin/env python3
"""PreToolUse — GATE de carruseles, fail-closed, CUATRO PUERTAS (31-jul-2026).

Antes vigilaba una sola puerta: el comando `open` de shell. O sea, protegía la VISTA PREVIA —
pero no la billetera ni la publicación. Se podían quemar 30 generaciones de Higgsfield sobre un
copy que nunca pasó el panel, y enterarse recién al final. Y publicar a Meta no pasaba por
ninguna compuerta.

Una compuerta no vigila un proceso: vigila LA PUERTA AL SIGUIENTE.

  ┌ generar imagen  (mcp__higgsfield__generate_image/video)
  │    exige: brief PASS · copy mecánico PASS · blueprint PASS · prompt/zona PASS
  ├ renderizar      (chrome --screenshot)
  │    exige: raw PASS   (texto inventado · zona reservada · costura de collage)
  ├ abrir preview   (open)
  │    exige: gates PASS · 2 jueces PASS
  └ publicar        (mcp__meta-ads__ads_create_ad / ads_creative_upload_*)
       exige: TODO lo anterior, fresco

FALTA EL SPEC = FAIL, NO BYPASS (1-ago-2026). Antes, la adopción era incremental: las puertas
nuevas solo se activaban si la carpeta ya tenía `carrusel.json`. La intención era no bloquear el
trabajo en curso, pero sin fecha de corte quedó como el estado normal — y encima al revés de lo
que hace falta, porque la carpeta que NO tiene spec es justamente la que nadie verificó. Medición
del 1-ago-2026: **79 de 81 carpetas-carrusel del disco no tenían spec**; las 2 que sí eran tests.
O sea, las cuatro puertas estaban apagadas en el 98% del trabajo real. Una compuerta fail-closed
que se apaga sola cuando falta el artefacto es, en los hechos, fail-open.

Ahora: si la carpeta parece carrusel y no tiene `carrusel.json`, eso es un problema con
instrucción (`verify.py init`), no un pase libre.

El escape existe pero es EXPLÍCITO y auditable: `.claude/.carruseles-legacy`, una ruta absoluta
por línea. Lo que está ahí adentro conserva el comportamiento viejo (solo la puerta `open`).
La diferencia con `opt_in` no es el efecto, es quién decide: antes el bypass se lo daba la
carpeta a sí misma por omisión y en silencio; ahora alguien lo escribe, queda con fecha y se
puede leer de un vistazo qué está exento y por qué.

Principio: IA no-determinista razona (los jueces), IA determinista hace cumplir (esto).
"""
import sys, json, os, re, glob, hashlib, time

PROJ = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()


def allow():
    sys.exit(0)


def deny(reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }}))
    sys.exit(0)


def ask(reason):
    """Ni pase libre ni portazo: se lo pregunta al director creativo. Para lo que suele ser un error
    pero a veces es deliberado — y donde bloquear de plano rompería trabajo que ya anda."""
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": reason,
    }}))
    sys.exit(0)


try:
    d = json.load(sys.stdin)
except Exception:
    allow()


def _red(tipo, val, tb):
    """Si el gate se rompe, PREGUNTA — nunca deja pasar en silencio (6-ago-2026).

    Encontrado probando el tope de créditos: un `NameError` en `presupuesto()` mataba el proceso,
    el hook no emitía JSON, y Claude Code interpretaba el silencio como «sin objeción». O sea que
    **un bug en una compuerta abría todas las demás de esa puerta**, que es el peor modo de falla
    posible para algo cuyo trabajo es no dejar pasar. Un gate que se cae tiene que caerse cerrado.
    """
    import traceback
    det = "".join(traceback.format_exception(tipo, val, tb))[-700:]
    ask(f"[Gate carruseles · EL GATE SE ROMPIÓ] La compuerta no pudo evaluar este pedido, así "
        f"que no puede afirmar que sea seguro. Esto es un bug del hook, no del pedido — "
        f"reportalo y arreglalo antes de seguir gastando.\n\n{det}")


sys.excepthook = _red

TOOL = d.get("tool_name", "") or ""
ti = d.get("tool_input", {}) or {}
cwd = d.get("cwd") or os.getcwd()
cmd = next((ti.get(k) for k in ("command", "cmd", "script", "shell_command") if ti.get(k)), "")

SLIDE_RE = re.compile(r"^(?:s|sl|slide)?[-_]?(\d{1,2})(?:[-_][^/]*)?\.(?:html|png)$", re.I)


# ─────────────────────────────────────────────────────── utilidades ──
def slides_in(dd, ext):
    try:
        return [os.path.join(dd, fn) for fn in os.listdir(dd)
                if fn.lower().endswith("." + ext) and not fn.startswith("_")
                and SLIDE_RE.match(fn)]
    except OSError:
        return []


def is_carousel(dd):
    if (len(slides_in(dd, "html")) >= 3
            or os.path.exists(os.path.join(dd, "carrusel.json"))):
        return True
    # `_brief.md` cuenta desde el 1-ago-2026: en Fase 4 (generar imágenes) todavía no hay slides
    # renderizadas, y si nadie escribió el spec tampoco hay spec — así que la puerta GENERAR no
    # podía disparar nunca, justo la que cuida la billetera. El brief es la primera huella de
    # que acá se está produciendo un carrusel.
    #
    # Solo para trabajo NUEVO. Medido al aplicarlo: ensanchar el criterio a secas convertía en
    # carrusel a 11 carpetas ya entregadas que antes ni se miraban (los c9x de Marca Verde,
    # entrenar-acompanada) y las dejaba bloqueadas al abrir. Un arreglo que rompe trabajo
    # terminado se desactiva a la semana.
    return (os.path.exists(os.path.join(dd, "_brief.md")) and not es_legacy(dd))


def _limpiar_ref(r):
    """Normaliza una ruta sacada de una línea de comando.

    Sin esto, la puerta RENDER no disparaba: el comando de Chrome trae las rutas como
    `--screenshot=/ruta/s-01.png` y `file:///ruta/s-01.html`, y el dirname de eso daba una
    carpeta inventada — así que el gate no encontraba el carrusel y dejaba pasar el render
    con el crudo en FAIL (cazado probando el hook, 31-jul-2026)."""
    r = r.strip().strip('"').strip("'")
    if "=" in r:                      # --screenshot=/ruta/x.png
        r = r.rsplit("=", 1)[-1]
    if r.startswith("file://"):       # file:///ruta/x.html
        r = r[len("file://"):]
    return r


def find_refs(text, exts):
    out = []
    for p in (r'"([^"]+\.(?:%s))"' % exts, r"'([^']+\.(?:%s))'" % exts,
              r"(?<![\"'\w])([^\s\"'&|;]+\.(?:%s))" % exts):
        out += re.findall(p, text)
    return [_limpiar_ref(r) for r in out]


def carpeta_activa():
    """Puntero a la carpeta-carrusel en curso (lo escribe verify.py).

    3-ago-2026 (auditoría P6): el puntero quedó apuntando a un test en /tmp y
    bloqueaba TODA generación citando esa carpeta. Ahora se descarta si:
    (a) el puntero tiene más de 24 h (un carrusel en curso no dura más que eso),
    (b) la ruta ya no existe, o (c) no está bajo el proyecto.
    Sin carpeta confiable, las puertas PREGUNTAN (ask), no bloquean — ver
    PUERTA 1 y PUERTA 4.
    """
    p = os.path.join(PROJ, ".claude", ".carrusel-activo")
    try:
        if time.time() - os.path.getmtime(p) > 24 * 3600:
            return None
        c = open(p, encoding="utf-8").read().strip()
        if not c or not os.path.isdir(c):
            return None
        real, raiz = os.path.realpath(c), os.path.realpath(PROJ)
        if real != raiz and not real.startswith(raiz + os.sep):
            return None
        return c
    except OSError:
        return None


def sha(path, n=12):
    try:
        with open(path, "rb") as f:
            return hashlib.sha1(f.read()).hexdigest()[:n]
    except OSError:
        return None


def leer_recibo(cdir, nombre, verificar_hash=True):
    """→ (estado, detalle). estado: 'ok' | 'falta' | 'fail' | 'ilegible' | 'adulterado'"""
    p = os.path.join(cdir, nombre)
    if not os.path.exists(p):
        return "falta", f"falta {nombre}"
    try:
        r = json.load(open(p, encoding="utf-8"))
    except Exception:
        return "ilegible", f"{nombre} ilegible"
    if str(r.get("verdict", "")).upper() != "PASS":
        fallos = [c.get("check") for c in (r.get("checks") or []) if c.get("ok") is False]
        return "fail", f"{nombre} en FAIL" + (f" → {', '.join(filter(None, fallos))[:160]}"
                                              if fallos else "")
    # El hash es lo que impide escribir un recibo a mano: si los archivos medidos cambiaron
    # (o nunca se midieron), no coincide.
    #
    # 10-ago-2026: esto decía `if verificar_hash and r.get("by") == "script"`, o sea que el
    # chequeo entero se saltaba omitiendo un campo que el falsificador controla. Verificado
    # corriendo `leer_recibo()`: `{"verdict":"PASS"}` pelado devolvía `ok` y abría la puerta.
    # Mismo agujero que tenía `web-gate.py`. Ahora la firma se EXIGE en los recibos de script
    # (los de agente entran por `verificar_hash=False`, que es otra rama). `escribir()` de
    # verify.py garantiza que todo PASS lleve al menos la firma del spec.
    if verificar_hash:
        if r.get("by") != "script" or not r.get("inputs"):
            return "adulterado", (f"{nombre} dice PASS pero no lo firmó verify.py "
                                  f"(le falta {'by:script' if r.get('by') != 'script' else 'inputs'}). "
                                  f"Un recibo a mano no abre la puerta: correr la fase de verdad")
        for base, h in (r.get("inputs") or {}).items():
            reales = glob.glob(os.path.join(cdir, "**", base), recursive=True)
            if not reales:
                return "adulterado", f"{nombre}: firmó «{base}» y ese archivo ya no está"
            if not any(sha(x) == h for x in reales):
                return "adulterado", (f"{nombre}: «{base}» cambió después de medirlo "
                                      f"— re-correr verify.py")
    return "ok", ""


def frescura(cdir, recibo, patrones):
    """El recibo tiene que ser más nuevo que lo que verifica."""
    p = os.path.join(cdir, recibo)
    if not os.path.exists(p):
        return None
    ref = []
    for pat in patrones:
        ref += glob.glob(os.path.join(cdir, pat))
    # 3-ago-2026 (auditoría H6): los artefactos `_…` (p.ej. `_TODAS-LAS-SLIDES-*.png`,
    # `_thumb-NN.png`) se generan DESPUÉS de verificar (Fase 8); contarlos dejaba
    # todo recibo perpetuamente DESACTUALIZADO.
    ref = [x for x in ref if not os.path.basename(x).startswith("_")]
    nuevo = max((os.path.getmtime(x) for x in ref), default=0)
    if nuevo and os.path.getmtime(p) < nuevo - 1:
        return f"{recibo} DESACTUALIZADO (cambiaste archivos después de verificar)"
    return None


def n_jueces(r):
    """Nº de jueces/lectores declarado en un recibo de agente.

    3-ago-2026 (auditoría C14): 15 de 22 recibos reales escriben `lectores` o
    `readers` en vez de `judges`; leer solo `judges` caía al default 1 y bloqueaba
    mintiendo ("solo 1 lector").
    """
    for k in ("judges", "lectores", "readers"):
        if r.get(k) is not None:
            try:
                return int(r[k])
            except (TypeError, ValueError):
                pass
    return 1


def es_legacy(cdir):
    """¿Esta carpeta está exenta a propósito? Solo si figura en `.claude/.carruseles-legacy`.

    Exento = comportamiento viejo: únicamente la puerta `open` con sus dos recibos de juez.
    Se usa para trabajo YA ENTREGADO, que no tiene sentido re-verificar hacia atrás.
    """
    p = os.path.join(PROJ, ".claude", ".carruseles-legacy")
    try:
        real = os.path.realpath(cdir)
        for l in open(p, encoding="utf-8"):
            l = l.split("#", 1)[0].strip()
            if not l:
                continue
            # 3-ago-2026 (auditoría P10): la lista llegó a 101 rutas exentas — la
            # excepción se comió la regla. Una entrada solo exime si la carpeta
            # EXISTE y se tocó en los últimos 60 días (trabajo realmente reciente
            # en curso); lo viejo o borrado vuelve a pasar por las puertas.
            exp = os.path.realpath(os.path.expanduser(l))
            if exp == real and os.path.isdir(exp):
                try:
                    if time.time() - os.path.getmtime(exp) <= 60 * 86400:
                        return True
                except OSError:
                    pass
    except OSError:
        pass
    return False


def falta_spec(cdir):
    """El spec es la piedra angular: sin él ni el motor ni las compuertas pueden correr."""
    if os.path.exists(os.path.join(cdir, "carrusel.json")):
        return []
    return ["falta carrusel.json — es el spec que leen engine.py, verify.py y estas puertas. "
            "Creá el andamio con: verify.py init <carpeta>  (y rellená la Fase 1). "
            "Si es trabajo viejo ya entregado, agregá su ruta a .claude/.carruseles-legacy"]


def exigir(cdir, requisitos):
    """requisitos: [(archivo, etiqueta), ...] → lista de problemas."""
    problemas = []
    for arch, etiqueta in requisitos:
        estado, detalle = leer_recibo(cdir, arch)
        if estado != "ok":
            problemas.append(f"{etiqueta}: {detalle}")
    return problemas


def jueces(cdir):
    """DEROGADO · doble juez de diseño (Max, 7-sep-2026).

    Textual: *"antes hacíamos todo esto de los jueces y blabla, ahora quiero que solo sea un
    límite de una generación de imágenes, onda que haga el carrusel 1 vez y me lo muestre"*.

    La Fase 7 ya no se corre, así que `_qa-receipt.json` no se escribe nunca. Dejar la
    exigencia en pie no protegería nada: convertiría ABRIR y PUBLICAR en un bloqueo muerto,
    imposible de satisfacer, y la salida sería inventar el recibo a mano — que es justo lo
    que prohíbe `recibo-fail-no-se-falsea`. Por eso se apaga acá y no solo en la skill.

    Lo que sigue vigilando esta puerta: spec, brief, blueprint, crudo y compuertas de render.
    Todos son SCRIPTS. Lo que se apagó son los jueces LLM y los reintentos automáticos.

    El código original queda abajo, inerte, por si se quiere revivir — igual que el panel
    ciego de copy que el director creativo derogó el 10-ago-2026.
    """
    return []


def _jueces_derogado(cdir):
    problemas = []
    estado, detalle = leer_recibo(cdir, "_qa-receipt.json", verificar_hash=False)
    if estado != "ok":
        problemas.append(f"jueces de diseño: {detalle}")
    else:
        r = json.load(open(os.path.join(cdir, "_qa-receipt.json"), encoding="utf-8"))
        n = n_jueces(r)
        if n < 2:
            problemas.append(f"jueces de diseño: solo {n} — el estándar "
                             f"exige 2 independientes en PASS")
    # 3-ago-2026 (auditoría H6): se sacó el comodín `*.png` del patrón — capturaba
    # artefactos POSTERIORES de Fase 8 (`_TODAS-LAS-SLIDES-*.png`, `_thumb-NN.png`)
    # y dejaba los recibos siempre DESACTUALIZADOS.
    f = frescura(cdir, "_qa-receipt.json", ["s-*.png", "[0-9][0-9]-*.png"])
    if f:
        problemas.append(f"jueces de diseño: {f}")
    return problemas


# ── DEROGADO · panel ciego de comprensión de copy (director creativo, 10-ago-2026) ──
#
# Existió desde junio-2026 porque el director creativo reportó «la gente me dice que el anuncio no se
# entiende / interpreta otra cosa». Exigía `_copy-receipt.json` en PASS con ≥3 lectores
# ciegos antes de GENERAR, ABRIR y PUBLICAR.
#
# el director creativo lo eliminó el 10-ago-2026, con este argumento: desde que la Fase −1 entrega cada
# propuesta con el texto de TODAS sus slides, él lee el copy completo antes de que se
# produzca nada, y su experiencia en marketing cubre ese juicio.
#
# Se le señaló dos veces el contraargumento (quien conoce el producto no puede medir su
# propia claridad; el panel de este lote pescó un error factual del contador y una lectura
# de privacidad) y reafirmó la decisión. Manda él: jerarquía #1 de la skill.
#
# ── Y el 10-ago-2026, más tarde, también se eliminó `copy-craft-qa` ──
# el director creativo: «elimina esta copy-craft-qa». Con eso el carrusel queda SIN ningún juez de
# texto. Lo único que sobrevive es `verify.py copy` → `_copy-gate-receipt.json`, que es
# un SCRIPT (AI-tells, triadas, largo del hook, estructura del primary text), no un juez.
#
# Se le advirtió el riesgo concreto y decidió igual: el hallazgo nº1 de copy-craft-qa era
# D1 —claims que la marca no puede sostener— con 19 de sus 47 hallazgos, en un cliente
# tributario y con 14 anuncios ya rechazados en la cuenta. Queda anotado, no discutido.
#
# Qué NO se derogó: la exactitud tributaria/factual seguía siendo obligatoria — pasaba a
# `_copy-craft-receipt.json` — que TAMBIÉN se eliminó el 10-ago-2026 (ver bloque de abajo).
#
# Para revertir: `git log` de este archivo, o `APRENDIZAJES.md` §35, que conserva el método
# completo del panel. La función se borró en vez de neutralizarse a propósito: un
# `return []` con nombre de compuerta es justo la trampa que documenta
# `un-gate-que-se-cae-se-cae-cerrado`.


# ─────────────────────────────────────────────── resolver la puerta ──
def carpetas_del_comando():
    base = cwd
    m = re.search(r"cd\s+(\"[^\"]+\"|'[^']+'|[^\s&|;]+)", cmd)
    if m:
        base = os.path.expanduser(m.group(1).strip().strip('"').strip("'"))
    cands = {os.path.abspath(base)} if os.path.isdir(base) else set()
    for ref in find_refs(cmd, "html|png"):
        p = ref if os.path.isabs(ref) else os.path.join(base, ref)
        cands.add(os.path.dirname(os.path.abspath(p)))
    dirs = {c for c in cands if os.path.isdir(c) and is_carousel(c)}
    # index/combinado: mirar qué carpetas-carrusel referencia el HTML abierto
    for ref in find_refs(cmd, "html"):
        fp = os.path.abspath(ref if os.path.isabs(ref) else os.path.join(base, ref))
        if os.path.isfile(fp) and not is_carousel(os.path.dirname(fp)):
            try:
                html = open(fp, encoding="utf-8", errors="ignore").read()
            except OSError:
                continue
            for src in re.findall(r"""(?:src|href)\s*=\s*["']([^"']+)["']""", html):
                c = os.path.abspath(os.path.join(os.path.dirname(fp), os.path.dirname(src)))
                if is_carousel(c):
                    dirs.add(c)
    return dirs


def carpeta_de_mcp():
    """Para tools MCP no hay ruta de slides: se usa el puntero que deja verify.py."""
    for v in ti.values():
        if isinstance(v, str) and ("/" in v) and os.path.isdir(os.path.dirname(v) or ""):
            dd = os.path.dirname(os.path.abspath(v))
            if is_carousel(dd):
                return dd
    a = carpeta_activa()
    if a and is_carousel(a):
        return a
    return None


FLUJO = ("Flujo: verify.py brief/copy/blueprint → generar imágenes → "
         "verify.py raw → renderizar → verify.py gates → 2× 'carrusel-qa' → abrir → publicar.")


# Tabla de créditos por modelo — misma que `costo-imagenes.py`. Aproximada para nano_banana_2
# (el libro muestra cargos de 1.5 y de 2 para ese modelo); se redondea hacia arriba a propósito:
# un presupuesto que subestima no es un presupuesto.
CREDITOS = {"nano_banana_pro": 2.0, "nano_banana_2": 2.0, "gpt_image_2": 12.0}


def pide_esta_llamada(ti):
    """Cuántas imágenes y cuántos créditos pide el pedido que está por ejecutarse.

    Sin esto el tope solo frenaba la ráfaga SIGUIENTE (6-ago-2026): el chequeo era
    `gastado >= tope`, así que con el contador en 14 y tope 15, una batch de 24 pasaba entera.
    Medido: la ráfaga más grande del lote Marca Verde fueron 24 imágenes de un saque."""
    fuera = []
    reqs = ti.get("requests")
    if isinstance(reqs, list):
        fuera = [(r or {}).get("params") or {} for r in reqs]
    elif isinstance(ti.get("params"), dict):
        fuera = [ti["params"]]
    n, cred = 0, 0.0
    for q in fuera:
        if not isinstance(q, dict) or q.get("get_cost"):
            continue                                   # preflight: no gasta
        c = max(1, min(4, int(q.get("count") or 1)))
        n += c
        if not q.get("use_unlim"):
            cred += CREDITOS.get(str(q.get("model") or "").strip(), 2.0) * c
    return n, round(cred, 1)


def goteo(cdir, pide):
    """¿Se está regenerando de a UNA, en vez de juntar las correcciones? (6-ago-2026)

    Esta es la compuerta del RELOJ, no de la billetera — la única. Las demás miden cuánto se
    gasta; ésta mide CÓMO, que es donde se fueron las horas.

    Medición del lote Marca Verde (5-ago): el día tuvo dos tramos. El inicial generó 135 imágenes en
    14 ráfagas (media 9,6, 5 min por ráfaga). El de iteración generó 41 en 11 ráfagas — media
    3,7, **10,2 min por ráfaga, y 5 de las 11 fueron de UNA sola imagen**. 41 imágenes costaron
    112 minutos. Proyectado a 10 carruseles: ~4,6 h solo iterando.

    Ningún tope de gasto lo caza, porque cada pedido es chico y barato. Por eso es una compuerta
    aparte: el costo de reloj es el VIAJE, no la imagen (una ráfaga manda 12 en el mismo segundo).

    ASK, no DENY, y a propósito: hay regeneraciones sueltas legítimas (la última slide que no
    cerró, un pedido puntual del director creativo). Lo que no puede pasar es encadenar cinco sin que nadie
    lo note. Se dispara con el patrón —N ráfagas chicas seguidas—, no con la primera.
    """
    if pide > 2:
        return None                       # es una ráfaga de verdad: justo lo que queremos
    try:
        L = json.load(open(os.path.join(cdir, "_costo.json"), encoding="utf-8"))
    except Exception:
        return None
    ev = [e for e in (L.get("eventos") or []) if int(e.get("n") or 0) > 0]
    chicas = 0
    for e in reversed(ev):                # cuántas ráfagas chicas seguidas viene encadenando
        if int(e.get("n") or 0) <= 2:
            chicas += 1
        else:
            break
    if chicas < 3:
        return None
    ult = [f"{e.get('ts', '?')[11:16]} · {e.get('n')} img" for e in ev[-(chicas):]][-5:]
    return (f"[Gate carruseles · GOTEO DE GENERACIONES] Van **{chicas} ráfagas seguidas de ≤2 "
            f"imágenes** y ésta pide {pide}: {' → '.join(ult)}.\n\n"
            f"Éste es el bucle que se comió las horas del 5-ago (mirar → no gustar → regenerar "
            f"→ esperar → mirar): 41 imágenes en 112 min, 10 min por viaje. El costo de reloj es "
            f"el VIAJE, no la imagen — una ráfaga manda 12 en el mismo segundo.\n\n"
            f"  · ¿Podés juntar ESTA corrección con las otras slides que también hay que "
            f"rehacer, y mandarlas en una sola llamada?\n"
            f"  · ¿Es otra FOTO lo que falta, o solo otro ENCUADRE? Un `zoom` en el spec cuesta "
            f"0 créditos y 0 segundos.\n"
            f"  · Si el mismo motivo ya salió 2 veces, el problema es el PROMPT: corregilo para "
            f"TODAS las slides que lo comparten (`references/prompts-fallidos.md`).\n\n"
            f"Si de verdad es una corrección suelta y puntual, confirmá y seguí.")


def presupuesto(cdir):
    """¿Este pedido se pasa del presupuesto de generaciones declarado? (5-ago-2026)

    Medición que lo originó: 4 carruseles Marca Verde, 20 fotos usadas, **255 generaciones** en
    Higgsfield (717 créditos). En disco quedaron 21 crudos. Las 234 restantes se generaron, se
    miraron, se descartaron y no dejaron rastro: ni contador, ni prompt fallido, ni motivo.

    Las cuatro puertas ya cuidaban que no se gastara sobre un plan SIN VERIFICAR. No cuidaban
    CUÁNTO se gasta sobre un plan verificado — y ahí se fue el 92%. La Fase 4b dice "tope 2
    reintentos por slide" desde julio, pero nada lo contaba, y una regla que nadie mide es una
    sugerencia.

    Devuelve un texto para `ask()` o None. Es ASK y no DENY a propósito: hay carruseles que
    legítimamente necesitan más (una escena difícil, un cambio de ángulo del director creativo). Lo que
    no puede seguir pasando es que se pase de largo EN SILENCIO.
    """
    try:
        spec = json.load(open(os.path.join(cdir, "carrusel.json"), encoding="utf-8"))
    except Exception:
        return None
    n_slides = max(1, len(spec.get("slides") or []))
    declarado = spec.get("presupuesto_imagenes")
    tope = int(declarado) if declarado else n_slides * 3   # 1 intento + los 2 reintentos de §4b
    try:
        L = json.load(open(os.path.join(cdir, "_costo.json"), encoding="utf-8"))
    except Exception:
        return None                      # aún no se generó nada: no hay nada que frenar
    gastado = int(L.get("total", 0))
    creditos = float(L.get("creditos", 0) or 0)
    pide, pide_cred = pide_esta_llamada(ti)
    if pide == 0:
        return None                      # preflight (get_cost) o llamada sin params: no gasta

    # Techo de CRÉDITOS en paralelo al de imágenes. Un contador de imágenes solo es ciego al
    # modelo: 12 generaciones con gpt_image_2 son 144 créditos y cuentan igual que 12
    # nano_banana_pro (24). En el lote Marca Verde ese renglón fue el 20% del gasto total y no
    # movió el contador ni un punto.
    tope_cred = tope * 2.0 * 1.25        # el tope en nano_banana_pro + 25% de holgura
    por_imagenes = gastado + pide > tope
    por_creditos = creditos + pide_cred > tope_cred
    if not (por_imagenes or por_creditos):
        return None
    motivo = (f"pediría {gastado + pide} generaciones y el tope es {tope}" if por_imagenes
              else f"pediría ~{creditos + pide_cred:.0f} créditos y el techo es "
                   f"~{tope_cred:.0f} (contás {gastado} imágenes, pero el MODELO las encarece)")
    fuente = (f"declarado en carrusel.json ({tope})" if declarado
              else f"por defecto: {n_slides} slides × 3 intentos = {tope} "
                   f"(el tope de 2 reintentos por slide de la Fase 4b)")
    return (f"[Gate carruseles · PRESUPUESTO DE IMÁGENES] {os.path.basename(cdir)} lleva "
            f"**{gastado} generaciones** (~{creditos:.0f} créditos) y esta llamada pide "
            f"**{pide} más** (~{pide_cred:.0f} créditos): {motivo}. Presupuesto: {fuente}.\n\n"
            f"Antes de gastar más, la pregunta que evita repetir el 4-5 de agosto (255 "
            f"generaciones para 20 fotos usadas):\n"
            f"  · ¿El prompt que falla está escrito en `references/prompts-fallidos.md`? "
            f"Si no, regenerar es repetir el mismo error con otra semilla.\n"
            f"  · ¿Los descartes están en `raw/_descartados/` o se borraron? Lo que se borra "
            f"no enseña nada y no se puede contar.\n"
            f"  · ¿Esta slide necesita otra FOTO, u otro TEXTO/encuadre? Un `zoom` en el spec "
            f"cuesta 0 créditos.\n\n"
            f"Si de verdad hacen falta más, subí el tope DEJANDO EL MOTIVO ESCRITO:\n"
            f"    costo.py presupuesto {cdir} <N> --por \"<por qué hacen falta>\"\n"
            f"Queda en el spec con fecha (`presupuesto_historial`). Un tope que se sube sin "
            f"decir por qué no es un tope.")

# ── PUERTA 1 · generar imagen ───────────────────────────────────────
if re.search(r"generate_(image|video)", TOOL, re.I):
    cdir = carpeta_de_mcp()
    if not cdir:
        # 3-ago-2026 (auditoría P6): sin carpeta confiable se PREGUNTA, no se
        # deniega — el puntero stale a /tmp bloqueaba toda generación citando
        # una carpeta de test.
        ask("[Gate carruseles · puerta GENERAR IMAGEN] No encontré la carpeta del "
            "carrusel: el puntero .carrusel-activo está vacío, tiene más de 24 h "
            "o apunta fuera del proyecto.\n\nSi esto NO es para un carrusel, "
            "confirma y sigue. Si ES para un carrusel: corre `verify.py init "
            "<carpeta>` para fijar la carpeta activa y completar el flujo "
            "(brief → copy → blueprint) antes de gastar créditos.")
    if es_legacy(cdir):
        allow()
    problemas = falta_spec(cdir) or (
        exigir(cdir, [("_brief-receipt.json", "brief"),
                      ("_copy-gate-receipt.json", "copy (mecánico)"),
                      ("_blueprint-receipt.json", "blueprint"),
                      # 6-ago-2026 · el prompt reserva el hueco del texto ANTES de pagarlo.
                      # Es la única compuerta que corre sobre algo todavía no gastado: `raw`
                      # mide el mismo hueco después, cuando la generación ya está paga.
                      ("_prompt-receipt.json", "el prompt reserva la zona de texto "
                                               "(verify.py prompt · prompt_zona.py armar)")]))
    if problemas:
        deny("[Gate carruseles · puerta GENERAR IMAGEN] Generar cuesta créditos: no se gasta "
             "sobre un plan sin verificar.\n- " + "\n- ".join(problemas) +
             f"\n\n{FLUJO}\nCarpeta: {cdir}")
    # El plan está verificado; falta la otra mitad de la billetera: CUÁNTO se lleva gastado.
    # DENY, no ASK (6-ago-2026). Era ASK "porque hay carruseles que legítimamente necesitan
    # más" — y eso sigue siendo cierto, por eso hay escape. Pero desatendido (que es JUSTO
    # cuando el bucle "regenerar es más barato que pensar" corre solo) un ASK sin nadie mirando
    # no frena nada. El escape ahora deja rastro: subir el tope exige un motivo escrito que
    # queda fechado en el spec. Fail-closed para la billetera, igual que para publicar.
    sobregiro = presupuesto(cdir)
    if sobregiro:
        deny(sobregiro)
    # Compuerta del RELOJ (6-ago-2026). Va DESPUÉS del presupuesto: si además hay sobregiro,
    # manda el deny; si no, avisa del patrón de goteo antes de encadenar la quinta ráfaga de una.
    lento = goteo(cdir, pide_esta_llamada(ti)[0])
    if lento:
        ask(lento)
    allow()

# ── PUERTA 4 · publicar a Meta ──────────────────────────────────────
if re.search(r"meta-ads__ads_(create_ad|create_creative|creative_upload)", TOOL, re.I):
    cdir = carpeta_de_mcp()
    if not cdir:
        # 3-ago-2026 (auditoría P6): sin carpeta confiable se PREGUNTA, no se
        # deniega ni se deja pasar en silencio.
        ask("[Gate carruseles · puerta PUBLICAR] No encontré la carpeta del "
            "carrusel: el puntero .carrusel-activo está vacío, tiene más de 24 h "
            "o apunta fuera del proyecto.\n\nSi este anuncio NO viene de un "
            "carrusel, confirma y sigue. Si SÍ viene: corre `verify.py init "
            "<carpeta>` y completa el flujo antes de salir al aire.")
    if es_legacy(cdir):
        allow()
    problemas = falta_spec(cdir) or (
        exigir(cdir, [("_brief-receipt.json", "brief"),
                      ("_blueprint-receipt.json", "blueprint"),
                      ("_raw-receipt.json", "crudo"),
                      ("_gates-receipt.json", "compuertas de render")])
        + jueces(cdir))
    if problemas:
        deny("[Gate carruseles · puerta PUBLICAR] Esto sale al aire con dinero detrás.\n- "
             + "\n- ".join(problemas) + f"\n\n{FLUJO}\nCarpeta: {cdir}")
    allow()

# ── de acá en adelante, solo comandos de shell ──────────────────────
if not cmd:
    allow()

# ── AVISO · un build.py paralelo al motor único ─────────────────────
# El motor se reescribía en cada trabajo: llegaron a convivir SIETE `build.py`, y tres NO
# llamaban a `photo_map` ni una vez — tomaban la zona del spec y renderizaban a ciegas, sin
# preguntar nunca dónde estaba la persona. Por eso "el texto queda sobre la cara" pasaba en
# unos trabajos y en otros no: dependía de con qué copia se hubiera armado. Al 1-ago-2026
# quedaban 10 sueltos.
#
# Es AVISO y no bloqueo a propósito: varios de esos motores son de lotes ya entregados y
# siguen siendo la forma correcta de re-generarlos (build_dolores2.py, entre otros). Bloquear
# de plano rompería trabajo que anda; preguntar deja que el director creativo distinga el caso deliberado
# del descuido, que es exactamente donde un humano decide mejor que una regla.
_build = re.search(r"(?:^|[\s/])((?:[\w.-]*/)*build[\w-]*\.py)\b", cmd)
if _build and not re.search(r"site-packages|_distutils|setuptools|\.venv", cmd):
    ask(f"[Gate carruseles · aviso] Esto corre «{os.path.basename(_build.group(1))}», un motor "
        f"de composición propio.\n\nEl motor único del skill es `templates/engine.py`: es el que "
        f"consulta `photo_map` para ver dónde está la persona, reubica el texto al hueco real y "
        f"lo pasa POR DETRÁS del hombro con la máscara. Un build.py paralelo normalmente se "
        f"saltea eso y compone a ciegas.\n\n  engine.py <carpeta>          → s-NN.html\n"
        f"  engine.py <carpeta> --debug  → + el mapa dibujado\n\n"
        f"¿Es a propósito (motor de un lote ya entregado) o debería ir por engine.py?")

# ── PUERTA 2 · renderizar ───────────────────────────────────────────
if re.search(r"--screenshot|--headless", cmd):
    for cdir in carpetas_del_comando():
        if es_legacy(cdir):
            continue
        problemas = falta_spec(cdir) or exigir(
            cdir, [("_raw-receipt.json", "crudo (script)"),
                   ("_raw-ojo-receipt.json", "crudo a ojo (agente raw-qa)")])
        if problemas:
            deny("[Gate carruseles · puerta RENDERIZAR] Ninguna foto pasa a composición sin "
                 "mirarla sola (Fase 4b).\n- " + "\n- ".join(problemas) +
                 "\n\n(1) verify.py raw <carpeta> — texto inventado, zona reservada, costura. "
                 "(2) agente 'raw-qa' — logos de marca y anatomía, que el OCR NO ve.\n"
                 f"Carpeta: {cdir}")
    allow()

# ── PUERTA 3 · abrir la preview ─────────────────────────────────────
if not re.search(r"(?:^|[;&|]\s*|&&\s*|\|\|\s*)open\s+\S", cmd):
    allow()

caredirs = carpetas_del_comando()
if not caredirs:
    allow()

problemas = []
for cdir in sorted(caredirs):
    name = os.path.basename(cdir)
    ps = jueces(cdir)
    if not es_legacy(cdir):
        ps += falta_spec(cdir) or exigir(
            cdir, [("_gates-receipt.json", "compuertas de render")])
    problemas += [f"{name} · {p}" for p in ps]

if problemas:
    deny("[Gate carruseles · puerta ABRIR · fail-closed] No puedo mostrar el carrusel hasta "
         "verificación OK:\n- " + "\n- ".join(problemas) +
         "\n\n(1) COPY — verify.py copy (script mecánico, único chequeo de texto que queda); "
         "(2) RENDER — verify.py gates. Los jueces de diseño se derogaron el "
         "7-sep-2026: se genera UNA vez, se mira el PNG y se muestra.")
allow()
