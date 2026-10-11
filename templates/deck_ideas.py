#!/usr/bin/env python3
"""deck_ideas.py — genera el deck HTML de selección de propuestas de la Fase −1.

Recibe un archivo de propuestas (JSON o Markdown) y produce UN deck HTML: una
tarjeta por propuesta, agrupadas por celda (deseo × familia), con checkboxes
visuales para que el director creativo marque las elegidas.

Cada propuesta es un CARRUSEL COMPLETO — el texto real de cada slide, no un hook
con un resumen (director creativo, 6-ago-2026: "en vez de que dé 'ideas' tiene que decir
cada texto de cada slide"). Un resumen no se puede elegir: el desarrollo es donde
el copy se cae. La tarjeta muestra el hook grande y las slides debajo, en orden.

Uso:
    /usr/local/bin/python3 deck_ideas.py ideas.json [-o ideas.html] [--titulo "Marca Verde · 12 propuestas"]
    /usr/local/bin/python3 deck_ideas.py ideas.md   [-o ideas.html]

Entrada JSON — una lista de propuestas, o {"cliente", "titulo", "ideas": [...]}:
    [
      {"celda": "LF8-5 comodidad × problema", "familia": "problema",
       "idea": "El cierre de mes te come dos noches.",
       "slides": [
         {"titulo": "El cierre de mes te come dos noches.",
          "sub": "Y la mitad del trabajo es copiar de un lado a otro."},
         {"titulo": "Lo dictas una vez.", "sub": "…"},
         {"titulo": "Tú apruebas. Ahí se emite.", "sub": "…"},
         {"titulo": "Recupera tus dos noches. Marca Verde.", "cta": true}
       ],
       "notas": "opcional — marca de compliance, ⚙️ función a confirmar, etc."}
    ]

`slides` es opcional por compatibilidad, pero en un lote de Fase −1 es lo que se
espera: sin ella el deck avisa cuántas propuestas llegaron sin slides.

Entrada Markdown — DOS dialectos, los dos válidos.

(a) El CANÓNICO, que es el que `references/fase-menos-1.md` manda escribir al
    generador. Es el que hay que usar en un lote de verdad:

    # D3-a · LIBRE DE DOLOR — Outcome        ← celda (el primer '# ' titula el deck)
    ### D3-F1-a · Outcome ⚙️                 ← una propuesta
    **Celda:** LF8-3 libre de dolor × Outcome
    **s-01 ·** Llega el día 20 y ya tienes <em>todo cuadrado</em>
       ↳ Nada de buscar boletas la noche anterior.     ← «—» = sin subtítulo
    **s-04 · CTA ·** Remate del dolor + marca
    **Marca:** ⚙️ confirmar tal función      ← notas de compliance

(b) El de VIÑETAS, más corto, para notas rápidas a mano:

    ## <celda>                 (una sección por celda)
    - [familia] texto del hook :: notas opcionales
      · Título de la slide :: subtítulo      (líneas indentadas = slides, en orden)
      · Título de la slide de cierre
    - texto del hook           (sin familia ni slides también vale)

⚠️ El parser leía SOLO (b) y devolvía «0 ideas» sobre un archivo canónico
perfectamente válido (6-ago-2026, lote de 5 de Marca Verde). El generador había
seguido la regla escrita; el desalineado era el script. Si mañana cambia el
formato de `fase-menos-1.md`, se cambia ACÁ en el mismo turno.

El `<em>` del destaque inline (regla 5-ago-2026) sobrevive al escape y se
renderiza como destaque — ver `con_destaque()`.

Solo stdlib. Compatible Python 3.9+.
"""

import argparse
import html
import json
import os
import re
import sys
from datetime import date

CSS = """
:root{--ground:#F4F4F2;--surface:#FFF;--line:#E2E2DE;--ink:#16161A;--body:#3C3C40;
--muted:#8A8A8E;--accent:#0B6CFF;--accent-soft:#EAF2FF;--sel:#16A34A;--sel-soft:#EAF7EF}
@media (prefers-color-scheme:dark){:root{--ground:#101012;--surface:#1A1A1D;--line:#2C2C30;
--ink:#F2F2F4;--body:#C9C9CD;--muted:#7E7E84;--accent:#5B9BFF;--accent-soft:#15243E;--sel:#4ADE80;--sel-soft:#0E2416}}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--body);
font:15px/1.55 -apple-system,BlinkMacSystemFont,"Inter","Helvetica Neue",sans-serif;
-webkit-font-smoothing:antialiased}
.wrap{max-width:1100px;margin:0 auto;padding:0 20px 120px}
header.top{position:sticky;top:0;z-index:10;background:var(--ground);
border-bottom:1px solid var(--line);padding:14px 20px;display:flex;gap:16px;
align-items:center;justify-content:space-between;flex-wrap:wrap}
header.top h1{font-size:17px;color:var(--ink);margin:0}
.counter{font-variant-numeric:tabular-nums;font-weight:600;color:var(--ink)}
.counter b{color:var(--sel)}
.btn{border:1px solid var(--line);background:var(--surface);color:var(--ink);
border-radius:8px;padding:7px 12px;font-size:13px;cursor:pointer}
.btn:hover{border-color:var(--accent)}
section.celda{margin-top:34px}
section.celda h2{font-size:13px;text-transform:uppercase;letter-spacing:.06em;
color:var(--muted);margin:0 0 4px}
section.celda .n{font-weight:400}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(400px,1fr));gap:12px;margin-top:10px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:12px;
padding:14px 14px 12px;display:flex;gap:10px;align-items:flex-start;
transition:border-color .12s,box-shadow .12s}
.card:hover{border-color:var(--accent)}
.card.sel{border-color:var(--sel);background:var(--sel-soft)}
.card input{margin-top:3px;width:17px;height:17px;accent-color:var(--sel);flex:none;cursor:pointer}
.card .body{min-width:0;flex:1}
.card .txt{color:var(--ink);font-weight:650;font-size:16px;line-height:1.3;text-wrap:balance}
.card .notas{font-size:13px;color:var(--muted);margin-top:8px}
/* Las slides: el copy real, en orden. Es lo que se elige. */
ol.slides{list-style:none;margin:10px 0 0;padding:10px 0 0;border-top:1px solid var(--line);
display:flex;flex-direction:column;gap:8px}
ol.slides li{display:flex;gap:9px;align-items:baseline}
ol.slides li.cta .s-n{color:var(--sel)}
ol.slides li.cta .s-tit{color:var(--sel)}
.s-n{flex:none;width:34px;font-size:10.5px;font-weight:700;letter-spacing:.05em;
color:var(--muted);font-variant-numeric:tabular-nums;text-transform:uppercase}
.s-tit{color:var(--ink);font-weight:550;line-height:1.35}
.s-sub{font-size:13.5px;color:var(--body);margin-top:2px;line-height:1.45}
.sin-slides{margin-top:9px;font-size:12.5px;color:var(--muted);
border-top:1px solid var(--line);padding-top:9px}
.badge{display:inline-block;font-size:11px;font-weight:600;color:var(--accent);
background:var(--accent-soft);border-radius:99px;padding:2px 9px;margin-top:8px}
.ident{display:block;font-size:11px;font-weight:700;letter-spacing:.06em;
color:var(--muted);font-variant-numeric:tabular-nums;margin-bottom:5px}
/* Destaque inline (regla 5-ago-2026): UN fragmento por titular. El contraste se
   hace BAJANDO el resto, no gritando el destaque — por eso el <em> se queda en
   el color del ink y lo que se apaga es el texto que lo rodea.
   Solo se apaga el titular que TIENE destaque: uno sin <em> no tiene por qué
   verse gris. `:has()` lo acota; donde no exista, todo queda como estaba. */
.s-tit:has(em),.card .txt:has(em){color:var(--muted)}
.s-tit em,.card .txt em{font-style:normal;color:var(--ink);font-weight:700}
ol.slides li.cta .s-tit:has(em){color:var(--sel);opacity:.7}
ol.slides li.cta .s-tit em{color:var(--sel);opacity:1}
footer{margin-top:48px;font-size:12px;color:var(--muted)}
"""

JS = """
function refresh(){
  const sel=document.querySelectorAll('input.pick:checked').length;
  const tot=document.querySelectorAll('input.pick').length;
  document.getElementById('cnt').innerHTML='<b>'+sel+'</b> / '+tot+' elegidas';
  document.querySelectorAll('input.pick').forEach(cb=>{
    cb.closest('.card').classList.toggle('sel',cb.checked);
  });
  document.querySelectorAll('section.celda').forEach(sec=>{
    const s=sec.querySelectorAll('input.pick:checked').length;
    const t=sec.querySelectorAll('input.pick').length;
    sec.querySelector('.n').textContent='· '+s+'/'+t+' elegidas';
  });
}
function copiar(){
  const out=[];
  document.querySelectorAll('input.pick:checked').forEach(cb=>{
    const card=cb.closest('.card');
    const id=card.dataset.id;
    const txt=card.querySelector('.txt').textContent.trim();
    out.push(id?id+' — '+txt:txt);
  });
  const txt=out.map(t=>'- '+t).join('\\n');
  navigator.clipboard.writeText(txt).then(()=>{
    const b=document.getElementById('btn-copiar');
    b.textContent='Copiadas '+out.length+' ✓'; setTimeout(()=>b.textContent='Copiar elegidas',1500);
  });
}
document.addEventListener('change',e=>{if(e.target.classList.contains('pick'))refresh();});
document.addEventListener('DOMContentLoaded',refresh);
"""


def normalizar_slides(bruto, origen):
    """Lista de {titulo, sub, cta} — acepta dicts o strings sueltos."""
    if not bruto:
        return []
    if not isinstance(bruto, list):
        raise ValueError("propuesta #%s: 'slides' debe ser una lista" % origen)
    out = []
    for i, s in enumerate(bruto, 1):
        if isinstance(s, str):
            s = {"titulo": s}
        if not isinstance(s, dict):
            raise ValueError("propuesta #%s, slide %d: ni objeto ni texto" % (origen, i))
        titulo = (s.get("titulo") or s.get("title") or "").strip()
        if not titulo:
            raise ValueError("propuesta #%s, slide %d: sin 'titulo'" % (origen, i))
        out.append({"titulo": titulo,
                    "sub": (s.get("sub") or s.get("subtitulo") or "").strip(),
                    "cta": bool(s.get("cta"))})
    return out


def normalizar_idea(d, origen):
    """Devuelve {celda, familia, idea, slides, notas} o lanza ValueError."""
    if not isinstance(d, dict):
        raise ValueError("propuesta #%s no es un objeto" % origen)
    slides = normalizar_slides(d.get("slides"), origen)
    # El hook explícito manda; si no viene, es el título de la primera slide.
    idea = (d.get("idea") or d.get("hook") or d.get("texto") or "").strip()
    if not idea and slides:
        idea = slides[0]["titulo"]
    if not idea:
        raise ValueError("propuesta #%s sin texto ('idea'/'hook') ni slides" % origen)
    return {
        "celda": (d.get("celda") or "Sin celda").strip(),
        "familia": (d.get("familia") or "").strip(),
        "idea": idea,
        "slides": slides,
        "notas": (d.get("notas") or "").strip(),
        "id": (d.get("id") or "").strip(),
    }


def cargar_json(ruta):
    with open(ruta, encoding="utf-8") as f:
        data = json.load(f)
    titulo = None
    if isinstance(data, dict):
        titulo = data.get("titulo") or data.get("cliente")
        data = data.get("ideas", [])
    if not isinstance(data, list):
        raise ValueError("el JSON debe ser una lista de ideas o un objeto con 'ideas'")
    return titulo, [normalizar_idea(d, i + 1) for i, d in enumerate(data)]


RE_TITULO = re.compile(r"^#\s+(.+)$")
RE_CELDA = re.compile(r"^##\s+(.+)$")
RE_ITEM = re.compile(r"^[-*]\s+(?:\[([^\]]+)\]\s*)?(.*?)(?:\s*::\s*(.+))?$")
# Slide: línea indentada que abre con ·, ↳, > o s-NN. Va DENTRO de la propuesta anterior.
RE_SLIDE = re.compile(r"^\s+(?:[·>↳]|s-?\d+\s*[·:.-])\s*(.*?)(?:\s*::\s*(.+))?$")

# ── Dialecto canónico de la Fase −1 (references/fase-menos-1.md, 6-ago-2026) ──
# El formato que el generador tiene MANDATADO escribir usa encabezados, no viñetas:
#     # D3-a · LIBRE DE DOLOR — Outcome        ← celda (H1, no H2)
#     ### D3-F1-a · Outcome ⚙️                 ← propuesta (H3)
#     **Celda:** LF8-3 libre de dolor × Outcome
#     **s-01 ·** Título de la slide
#        ↳ Subtítulo de la slide anterior
#     **s-04 · CTA ·** Remate + marca
#     **Marca:** ⚙️ confirmar tal función      ← notas de compliance
# El parser leía el contrato viejo (`## celda` + `- viñeta`) y devolvía 0 ideas
# sobre un archivo perfectamente válido. Se soportan LOS DOS: el que manda la
# regla y el de viñetas, que sigue sirviendo para notas rápidas a mano.
RE_PROP = re.compile(r"^###\s+(.+)$")
RE_CELDA_CAMPO = re.compile(r"^\*\*Celda:\*\*\s*(.+)$")
RE_SLIDE_NEG = re.compile(
    r"^\*\*s-?(\d+)\s*·\s*(?:(CTA)\s*·\s*)?\*\*\s*(.*?)(?:\s*::\s*(.+))?$")
RE_SUB_NEG = re.compile(r"^\s+↳\s*(.*)$")
RE_MARCA = re.compile(r"^\*\*Marca:\*\*\s*(.+)$")
# El ID trae la familia y el semáforo pegados: "D3-F1-a · Outcome ⚙️".
RE_ID_FAMILIA = re.compile(r"^(\S+)\s*·\s*(.+)$")


def cargar_md(ruta):
    titulo, ideas, celda = None, [], "Sin celda"
    # Encabezado de celda pendiente: en el dialecto canónico el `# D3-a · …` es la
    # celda, salvo el primero del archivo, que es el título del deck.
    with open(ruta, encoding="utf-8") as f:
        for n, linea in enumerate(f, 1):
            linea = linea.rstrip()

            # ── Dialecto canónico ────────────────────────────────────────────
            m = RE_PROP.match(linea)
            if m:
                crudo = m.group(1).strip()
                mid = RE_ID_FAMILIA.match(crudo)
                ideas.append({
                    "celda": celda,
                    "familia": (mid.group(2).strip() if mid else ""),
                    "idea": (mid.group(1).strip() if mid else crudo),
                    "slides": [],
                    "notas": "",
                })
                continue
            m = RE_CELDA_CAMPO.match(linea)
            if m and ideas:
                # La celda declarada dentro de la propuesta manda sobre el H1.
                ideas[-1]["celda"] = m.group(1).strip()
                continue
            m = RE_SLIDE_NEG.match(linea)
            if m and ideas:
                ideas[-1]["slides"].append({"titulo": m.group(3).strip(),
                                            "sub": (m.group(4) or "").strip(),
                                            "cta": bool(m.group(2))})
                continue
            m = RE_SUB_NEG.match(linea)
            if m and ideas and ideas[-1]["slides"]:
                # «—» es el marcador de "esta slide no lleva subtítulo".
                sub = m.group(1).strip()
                if sub and sub != "—":
                    ideas[-1]["slides"][-1]["sub"] = sub
                continue
            m = RE_MARCA.match(linea)
            if m and ideas:
                ideas[-1]["notas"] = m.group(1).strip()
                continue

            # ── Dialecto de viñetas (contrato original) ──────────────────────
            m = RE_CELDA.match(linea)
            if m:
                celda = m.group(1).strip()
                continue
            m = RE_TITULO.match(linea)
            if m:
                # El primer H1 titula el deck; los siguientes son celdas.
                if titulo is None:
                    titulo = m.group(1).strip()
                else:
                    celda = m.group(1).strip()
                continue
            # Antes que RE_ITEM: una slide es una línea indentada, no una propuesta nueva.
            m = RE_SLIDE.match(linea)
            if m and m.group(1).strip() and ideas:
                ideas[-1]["slides"].append({"titulo": m.group(1).strip(),
                                            "sub": (m.group(2) or "").strip(),
                                            "cta": False})
                continue
            m = RE_ITEM.match(linea)
            if m and m.group(2).strip():
                ideas.append({
                    "celda": celda,
                    "familia": (m.group(1) or "").strip(),
                    "idea": m.group(2).strip(),
                    "slides": [],
                    "notas": (m.group(3) or "").strip(),
                })
    # El hook grande de la tarjeta es la PORTADA, no el ID: en el dialecto
    # canónico el H3 es "D3-F1-a", que no se puede juzgar. El ID pasa a ser
    # etiqueta y el titular de la s-01 ocupa su lugar — igual que en la vía JSON.
    for it in ideas:
        if it["slides"] and RE_ID_FAMILIA.match(it["idea"]):
            it["id"] = it["idea"]
            it["idea"] = it["slides"][0]["titulo"]
    return titulo, ideas


def agrupar(ideas):
    """Agrupa por celda conservando el orden de primera aparición."""
    grupos, orden = {}, []
    for it in ideas:
        if it["celda"] not in grupos:
            grupos[it["celda"]] = []
            orden.append(it["celda"])
        grupos[it["celda"]].append(it)
    return [(c, grupos[c]) for c in orden]


def con_destaque(texto):
    """Escapa el texto pero deja vivo el <em> del destaque inline.

    Regla del 5-ago-2026: todo titular de ≥5 palabras marca UN fragmento con
    `<em>` (la oferta, la cifra, el beneficio). Si el deck lo escapa entero,
    el director creativo ve «ya tienes <em>todo cuadrado</em>» impreso como texto — o sea el
    deck muestra el marcado en vez del destaque, justo en la fase donde tiene
    que juzgar cómo se va a LEER el titular. Se escapa todo y después se
    reabre solo el par <em>…</em>, que es marcado nuestro, no del usuario.
    """
    escapado = html.escape(texto)
    return escapado.replace("&lt;em&gt;", "<em>").replace("&lt;/em&gt;", "</em>")


def render(titulo, ideas):
    # `e` deja vivo el destaque (va en contenido de texto); `esc` escapa a secas
    # y es el que se usa en <title> y en atributos, donde un <em> sería inválido.
    e = con_destaque
    esc = html.escape
    partes = ["<!DOCTYPE html><html lang=\"es\"><head><meta charset=\"utf-8\">",
              "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">",
              "<title>%s</title><style>%s</style></head><body>" % (esc(titulo), CSS)]
    partes.append(
        "<header class=\"top\"><h1>%s</h1>"
        "<div><span class=\"counter\" id=\"cnt\"></span> "
        "<button class=\"btn\" id=\"btn-copiar\" onclick=\"copiar()\">Copiar elegidas</button></div>"
        "</header><div class=\"wrap\">" % e(titulo))
    for celda, items in agrupar(ideas):
        partes.append("<section class=\"celda\"><h2>%s <span class=\"n\"></span></h2>"
                      "<div class=\"grid\">" % e(celda))
        for it in items:
            badge = "<span class=\"badge\">%s</span>" % e(it["familia"]) if it["familia"] else ""
            notas = "<div class=\"notas\">%s</div>" % e(it["notas"]) if it["notas"] else ""
            slides = it.get("slides") or []
            if slides:
                filas = []
                for i, s in enumerate(slides, 1):
                    etq = "CTA" if (s["cta"] or i == len(slides)) else "s-%02d" % i
                    sub = ("<div class=\"s-sub\">%s</div>" % e(s["sub"])) if s["sub"] else ""
                    filas.append("<li%s><span class=\"s-n\">%s</span>"
                                 "<div><div class=\"s-tit\">%s</div>%s</div></li>"
                                 % (" class=\"cta\"" if etq == "CTA" else "",
                                    etq, e(s["titulo"]), sub))
                cuerpo = "<ol class=\"slides\">%s</ol>" % "".join(filas)
            else:
                cuerpo = ("<div class=\"sin-slides\">⚠️ sin slides — no se puede elegir "
                          "un carrusel que no está escrito (Fase −1)</div>")
            # El ID (D3-F4-a) es con lo que el director creativo nombra la elegida: va visible.
            ident = ("<span class=\"ident\">%s</span>" % e(it["id"])) if it.get("id") else ""
            partes.append(
                "<label class=\"card\" data-id=\"%s\"><input type=\"checkbox\" class=\"pick\">"
                "<div class=\"body\">%s<div class=\"txt\">%s</div>%s%s%s</div></label>"
                % (esc(it.get("id") or ""), ident, e(it["idea"]), cuerpo, notas, badge))
        partes.append("</div></section>")
    partes.append("<footer>Generado con templates/deck_ideas.py el %s · %d ideas · "
                  "Fase −1 de carruseles-max-final: el corte es POR CELDA, nunca por ranking "
                  "global.</footer></div><script>%s</script></body></html>"
                  % (date.today().isoformat(), len(ideas), JS))
    return "\n".join(partes)


def main():
    p = argparse.ArgumentParser(description="Deck HTML de selección de ideas (Fase −1).")
    p.add_argument("entrada", help="archivo de ideas (.json o .md)")
    p.add_argument("-o", "--salida", help="HTML de salida (por defecto: <entrada>.html)")
    p.add_argument("--titulo", help="título del deck (por defecto: el del archivo o el nombre)")
    args = p.parse_args()

    if not os.path.isfile(args.entrada):
        sys.exit("ERROR: no existe %s" % args.entrada)
    ext = os.path.splitext(args.entrada)[1].lower()
    try:
        if ext == ".json":
            titulo, ideas = cargar_json(args.entrada)
        elif ext in (".md", ".markdown"):
            titulo, ideas = cargar_md(args.entrada)
        else:
            sys.exit("ERROR: extensión %s no soportada (usa .json o .md)" % ext)
    except (ValueError, json.JSONDecodeError) as ex:
        sys.exit("ERROR leyendo %s: %s" % (args.entrada, ex))

    if not ideas:
        sys.exit("ERROR: 0 ideas en %s — revisa el formato (ver docstring)." % args.entrada)

    titulo = args.titulo or titulo or os.path.splitext(os.path.basename(args.entrada))[0]
    salida = args.salida or os.path.splitext(args.entrada)[0] + ".html"
    with open(salida, "w", encoding="utf-8") as f:
        f.write(render(titulo, ideas))

    celdas = agrupar(ideas)
    print("OK · %d propuestas en %d celdas → %s" % (len(ideas), len(celdas), salida))
    for celda, items in celdas:
        print("  %-40s %d propuestas" % (celda, len(items)))

    # Fase −1: una propuesta sin slides no se puede elegir. Se avisa, no se bloquea:
    # el deck también sirve para material viejo en formato hook suelto.
    sin = [it["idea"] for it in ideas if not it.get("slides")]
    if sin:
        print("\n⚠️  %d de %d propuestas llegaron SIN slides escritas." % (len(sin), len(ideas)))
        print("   La Fase −1 pide el texto real de CADA slide: un hook con un resumen no se")
        print("   puede elegir, y el desarrollo es donde el copy se cae (fase-menos-1.md).")
        for t in sin[:5]:
            print("   · %s" % t[:78])
        if len(sin) > 5:
            print("   · … y %d más" % (len(sin) - 5))


if __name__ == "__main__":
    main()
