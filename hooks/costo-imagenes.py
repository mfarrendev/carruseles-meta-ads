#!/usr/bin/env python3
"""PostToolUse — EL CONTADOR DE GENERACIONES (5-ago-2026).

Por qué existe. El 4 y 5 de agosto, para entregar 4 carruseles (20 fotos usadas), pasaron por
Higgsfield **255 generaciones de imagen** + 49 upscales + 6 recortes de fondo — 717 créditos.
En el disco quedaron **21 crudos**. Las otras 234 se generaron, se miraron, se descartaron y
**no dejaron rastro en ninguna parte**: ni un contador, ni el prompt que falló, ni el motivo.

El punto no es que 255 sea mucho o poco. El punto es que NADIE LO SABÍA — ni el agente
mientras las gastaba, ni el director creativo hasta que le llegó la cuenta. Un costo que no se mide no se
puede administrar, y "acordate de no gastar tanto" en un archivo de reglas no frena nada:
regenerar cuesta 2 créditos y 30 segundos, y arreglar el prompt cuesta pensar. Sin un número a
la vista, la salida barata siempre gana.

Este hook corre DESPUÉS de la llamada (PostToolUse), así que anota lo que de verdad se pidió —
no lo que se intentó pedir. La compuerta que FRENA está en `carrusel-gate.py` (PUERTA 1), que
lee este mismo libro antes de dejar gastar. División a propósito:

    PostToolUse (acá)      ANOTA lo que ya pasó       → nunca infla el contador
    PreToolUse  (gate)     FRENA contra el presupuesto → nunca gasta de más

Escribe `_costo.json` en la carpeta del carrusel:
    {"total": 37, "creditos": 74, "presupuesto": 40, "eventos": [
       {"ts": "...", "tool": "generate_image_batch", "n": 6, "modelo": "nano_banana_pro",
        "creditos": 12, "prompts": ["…los primeros 160 caracteres…"]}]}

Los prompts se guardan recortados a propósito: sirven para reconstruir QUÉ se pidió tantas
veces (que es de dónde sale el anti-catálogo de `references/prompts-fallidos.md`), no para
re-ejecutar. Fail-open siempre: un contador que rompe una generación sería peor que el
problema que resuelve.
"""
import sys, json, os, time

PROJ = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()

# Costo medido en el libro real de Higgsfield el 5-ago-2026 (transactions). Referencial:
# la plataforma puede cambiarlo. Sirve para que el número que ve el director creativo sea del orden
# correcto, no para facturar.
CREDITOS = {
    "nano_banana_pro": 2.0, "nano_banana_2": 1.5, "nano_banana": 1.5,
    "gpt_image": 12.0, "gpt_image_2": 12.0,
    "soul_2": 2.0, "soul_cast": 2.0, "marketing_studio_image": 2.0,
}
POR_DEFECTO = 2.0


def salir():
    sys.exit(0)


def costo_de(modelo):
    m = (modelo or "").lower()
    for k, v in CREDITOS.items():
        if k in m:
            return v
    return POR_DEFECTO


def carpeta_activa():
    """Mismo puntero que usan las puertas del gate; mismas defensas (24 h, existe, bajo el
    proyecto). Si no hay carpeta confiable no se anota: el costo de un trabajo suelto no le
    corresponde a ningún carrusel."""
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


def pedidos(ti):
    """Cuántas imágenes pidió ESTA llamada, y con qué modelo.

    `generate_image`       → params.count (1-4)
    `generate_image_batch` → un job por item de requests[] (count está fijado en 1)
    `get_cost: true`       → preflight, NO gasta: devuelve 0
    """
    fuera = []
    reqs = ti.get("requests")
    if isinstance(reqs, list):
        for r in reqs:
            p = (r or {}).get("params") or {}
            if isinstance(p, dict):
                fuera.append(p)
    else:
        p = ti.get("params")
        if isinstance(p, dict):
            fuera.append(p)
        elif isinstance(p, str):
            fuera.append({"prompt": p, "model": ""})
    n = 0
    creditos = 0.0
    modelos, prompts = [], []
    for p in fuera:
        if p.get("get_cost"):
            continue
        c = int(p.get("count") or 1)
        c = max(1, min(4, c))
        n += c
        modelos.append(str(p.get("model") or "?"))
        if not p.get("use_unlim"):
            creditos += costo_de(p.get("model")) * c
        pr = str(p.get("prompt") or "").strip().replace("\n", " ")
        if pr:
            prompts.append(pr[:160])
    modelo = max(set(modelos), key=modelos.count) if modelos else "?"
    return n, round(creditos, 1), modelo, prompts


try:
    d = json.load(sys.stdin)
except Exception:
    salir()

TOOL = d.get("tool_name", "") or ""
if "generate_image" not in TOOL and "generate_video" not in TOOL:
    salir()

# Una llamada que reventó no gastó créditos. `tool_response` con error → no se anota.
resp = d.get("tool_response")
if isinstance(resp, dict) and (resp.get("error") or resp.get("is_error")):
    salir()

cdir = carpeta_activa()
if not cdir:
    salir()

n, creditos, modelo, prompts = pedidos(d.get("tool_input", {}) or {})
if n <= 0:
    salir()

libro = os.path.join(cdir, "_costo.json")
try:
    L = json.load(open(libro, encoding="utf-8"))
except Exception:
    L = {"total": 0, "creditos": 0, "eventos": []}

L["eventos"] = (L.get("eventos") or [])[-199:] + [{
    "ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "tool": TOOL.split("__")[-1],
    "n": n, "modelo": modelo, "creditos": creditos, "prompts": prompts,
}]
L["total"] = int(L.get("total", 0)) + n
L["creditos"] = round(float(L.get("creditos", 0)) + creditos, 1)
L["ts"] = time.strftime("%Y-%m-%dT%H:%M:%S")

try:
    json.dump(L, open(libro, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
except OSError:
    salir()

# Aviso al agente en su propio contexto: el número tiene que estar A LA VISTA mientras se
# gasta, no en un archivo que nadie abre. Es `additionalContext`, no un bloqueo.
pres = 0
try:
    spec = json.load(open(os.path.join(cdir, "carrusel.json"), encoding="utf-8"))
    pres = int(spec.get("presupuesto_imagenes") or 0)
except Exception:
    pass

msg = f"[costo] {os.path.basename(cdir)}: {L['total']} generaciones · ~{L['creditos']} créditos"
if pres:
    msg += f" · presupuesto {pres}"
    if L["total"] >= pres:
        msg += "  ⛔ AGOTADO — la puerta GENERAR va a preguntar antes de la próxima."
    elif L["total"] >= pres * 0.75:
        msg += f"  ⚠️ quedan {pres - L['total']}."
print(json.dumps({"hookSpecificOutput": {
    "hookEventName": "PostToolUse", "additionalContext": msg}}))
sys.exit(0)
