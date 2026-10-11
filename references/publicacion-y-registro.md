# Publicación y registro — `_publicado.json`

> **Qué resuelve.** Hoy un carrusel sale de la Fase 8 y "se publica": nadie deja escrito QUÉ ad
> de Meta le corresponde. Sin ese vínculo no hay forma de traer el rendimiento real de vuelta
> (scorer, hooks.md, cuota creativa) — los 27 carruseles de `verde-ads/carruseles-2026-07`
> y los de Marca Crema están en el aire sin registro local.

## El archivo: `_publicado.json` por carpeta de carrusel

Un JSON por carpeta, al lado del `carrusel.json`:

```json
{
  "ad_id": "120211122233344455",
  "adset_id": "120211122233344400",
  "fecha": "2026-08-03",
  "notas": "Publicado a mano desde Meta Ads Manager. Variante de hook B."
}
```

- `ad_id` — el ID del ad en Meta (string de dígitos). **Es el campo que importa**: con él se
  traen insights vía la skill `meta-ads`.
- `adset_id` — para saber en qué ad set (audiencia) quedó.
- `fecha` — día de publicación (AAAA-MM-DD).
- `notas` — libre: variante de hook que quedó, si se editó el copy al subir, etc.

## Regla dura: NUNCA dentro de `carrusel.json`

El registro de publicación **no se escribe en `carrusel.json` ni en ningún archivo que los
recibos firmen**. Las puertas 3 y 4 (`open` y publicar) comparan la frescura de los recibos
contra el mtime del spec y de las piezas: tocar `carrusel.json` después del QA **vence todos
los recibos** y bloquea la carpeta como si se hubiera re-renderizado. `_publicado.json` es un
archivo aparte justamente porque se escribe DESPUÉS de que las puertas ya pasaron — y los
recibos no lo firman, así que puede actualizarse (un ad_id corregido, una nota) sin romper nada.

## Flujo normal

1. Publicar (a mano en Ads Manager o vía la skill `meta-ads`, Fase 9).
2. Anotar el `ad_id` y `adset_id` que devuelve Meta.
3. Registrar:

```
/usr/local/bin/python3 templates/registrar_publicacion.py <carpeta> --ad-id X --adset-id Y [--notas "..."]
```

El script crea o actualiza el `_publicado.json` con la fecha de hoy y lo re-lee para confirmar.

## Inventario retroactivo (una vez por cliente)

Para las carpetas ya producidas sin registro (verde-ads tiene 27; Marca Crema tiene
`PUBLICADOS-EN-META.md` congelado al 13-jul-2026):

1. **Listar las carpetas producidas.** Carpetas con `carrusel.json` o con PNGs de slides
   (`s-01.png`…) y sin `_publicado.json`.
2. **Traer los ads existentes desde la API de Meta** vía la skill `meta-ads` (o MCP): ads de la
   cuenta con su creative (primary text / body), estado y fecha de creación.
3. **Calzar por copy.** El hook del slide 1 y el primary text de cada carpeta están en el
   `carrusel.json`/`_brief.md`; el creative del ad trae el mismo texto. Calce por fragmento
   literal del hook (los primeros ~40 caracteres del primary text suelen bastar). Un ad que
   calza con dos carpetas se resuelve por fecha de producción de la carpeta.
4. **Escribir el `_publicado.json`** de cada carpeta calzada con
   `registrar_publicacion.py <carpeta> --ad-id X --adset-id Y --fecha <fecha del ad> --notas "calce retroactivo por copy"`.
5. **Dejar la lista de los que no calzaron** (carpetas sin ad — nunca se publicaron — y ads
   sin carpeta — se hicieron fuera del pipeline) en `_inventario-publicacion.md` junto al lote.
   No se inventa un calce: dudoso queda en la lista.

## Lo que este archivo habilita

- `brand-brain/<cliente>/hooks.md` se llena desde `_publicado.json` + insights de Meta.
- El scorer de rendimiento (`references/scorer-rendimiento.md`) deja de ser "los últimos 90
  días de la cuenta" y puede mirar ESTE carrusel.
- La cuota creativa (`brand-brain/<cliente>/cuota-creativa.md`) se mide contra ganadores
  reales, no contra lo producido.
