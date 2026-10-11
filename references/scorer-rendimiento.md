# Scorer de copy contra rendimiento REAL (paso OPCIONAL de la Fase 2 · 3-ago-2026)

> **Origen.** Idea robada de `charlie947/social-media-skills` (su scorer de hooks), en versión
> agencia: el de ellos dependía de una API externa (Apify) y sin ella degradaba a checklist
> genérico no accionable (35/50 en el test — ver `verde-comparativa-skills/_COMPARATIVA.md`).
> Acá el puntaje sale del rendimiento REAL de la cuenta del cliente, vía la skill `meta-ads`,
> que ya está autenticada. **No hay script nuevo: es un procedimiento para el agente.**

## Cuándo usarlo

Antes de escribir las variantes del hook (Fase 2), cuando la cuenta del cliente tiene
historial de ads suficiente (≥10 ads con gasto en los últimos 90 días). Si la cuenta es
nueva o no hay acceso, **se salta y se anota en el `_brief.md`** — no se frena el carrusel.

## Procedimiento

1. **Traer el top real.** Con la skill `meta-ads`, listar los ads del cliente de los
   últimos **90 días**, ordenados por CTR (y de respaldo CPA / gasto). Tomar los 5-10
   mejores Y los 3-5 peores — los dos extremos enseñan.
2. **Extraer la estructura, no el texto.** De cada hook ganador, anotar la ESTRUCTURA:
   ¿pregunta o afirmación? ¿problema-primero o resultado-primero? ¿cifra, escena o
   contrarian? ¿largo en palabras? Lo que se reutiliza es la forma que el público real
   de ESA cuenta ya premió, no el copy literal.
3. **Puntuar el copy nuevo contra eso.** Cada variante de hook del Paso B se evalúa
   contra las estructuras ganadoras: ¿es de una familia que ya rindió en esta cuenta?
   ¿o se parece a las que perdieron? El hook que no se parece a nada que haya rendido
   **no se descarta** (puede ser la próxima estructura ganadora) pero se declara como
   apuesta en el `_brief.md`.
4. **Dejarlo escrito.** En el `_brief.md`, sección "Decisiones": 3 líneas con los top
   ads consultados (IDs), las estructuras que ganan, y cómo quedó el hook elegido
   contra eso.

## Reglas

- **Rendimiento real > intuición.** El scorer existe porque "este hook suena bien" no es
  evidencia. Si choca con el gusto del agente, gana el dato.
- **El filtro de compliance manda sobre la estructura ganadora** (ver `COPY.md` § filtro
  de frameworks externos): si lo que rinde usa cifras o claims que el cliente no puede
  decir, se adapta la forma, no se copia el claim.
- Nunca inventar métricas: si `meta-ads` no devuelve datos, el paso se salta, no se simula.
