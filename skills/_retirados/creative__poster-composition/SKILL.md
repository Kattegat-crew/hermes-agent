---
name: poster-composition
description: "Posters: keyart IA + texto en capas PIL."
---

# Composición de posters de campaña (keyart IA + tipografía por capas)

Use when: pósters, flyers, stories y overlays de campaña donde cifras/fechas/sedes cambian por
versión. Patrón probado: **la IA genera solo el arte, todo texto se compone programáticamente**.
Nunca quemar tipografía en el modelo de imagen.

## Flujo

1. **Keyart limpio** — generar con `flux-2-klein` vía endpoint OpenAI-compatible del provider
   (ver `references/nan-builders-image-api.md`). En el prompt exigir SIEMPRE:
   `no text, no watermark, no words, empty dark space at top of frame` (reserva para tipografía).
2. **Verificar el arte** antes de componer: `vision_analyze` preguntando por texto espurio,
   espacio libre arriba y calidad. Un arte con letras garabateadas se descarta o se tapa con scrim.
3. **Componer con PIL** — script paramétrico (una función por pieza, parámetros = marca/cifra/sedes).
   Helpers que deben existir: `sans(size, weight)` (variable font), `rounded`, `scrim`,
   `shadow_text`, píldora de contador, badge tipo balota, chip de horario, franja legal.
4. **QA visual en loop**: `vision_analyze` sobre el PNG compuesto con preguntas concretas de
   layout (¿solapes? ¿cortes en bordes? ¿contraste? ¿invade el legal?). Corregir, re-renderizar,
   re-verificar. No entregar sin este pase — el modelo detecta texto cortado al borde, bajo
   contraste (p.ej. amarillo sobre rojo) y colisiones que el script no ve.
5. **Entregar con `MEDIA:<ruta>`** real y archivo verificado en disco.

## Tipografía del sistema

- Fuentes de marca bájense como **variable fonts** desde `raw.githubusercontent.com/google/fonts/main/...`
  (URLs con `[]` van percent-encoded `%5B...%5D`). El proxy `fonts.gstatic.com/css2` devolvía HTML,
  no TTF, con el navegador UA normal.
- Peso variable en PIL: `f = ImageFont.truetype(ttf, size); f.set_variation_by_axes([100, weight])`
  (eje opsz, eje wght 100–900). Un solo archivo reemplaza Bold/Black/ExtraBold estáticos.
- Medir antes de pintar: `draw.textbbox` para centrar y para `assert` de que cabe en su caja
  (evita el clásico "$400.000" recortado en el borde).

## Reglas de composición que sobrevivieron QA

- **Cifra protagonista** (número → título → cuándo → beneficios → legal). El legal
  "+18 Juego responsable · Regulado por Coljuegos" (o el que dicte el contrato) siempre presente.
- Cifras grandes en formato corto (`$400K`, `$1.2M`) si van en cajas angostas; el importe completo
  solo en espacios anchos.
- Texto sobre arte = **scrim**: píldora/rect `#000` a alpha 165–215, aro de color de marca.
  Resuelve el 100% de los hallazgos de contraste del QA.
- Overlay reutilizable para video: mismo componente dibujado sobre canvas RGBA `(0,0,0,0)`,
  luego **recortar al contenido** (`im.crop` hasta x_fin del chip + margen) — si no, lleva
  columna de píxeles transparentes que descoloca el anclaje en el reel.

## Pitfalls

- `vision_analyze` renderiza el alpha como blanco: un PNG transparente se describe como "fondo
  blanco". Verificar transparencia **programáticamente** (`im.getchannel('A').getpixel(esquina)==0`),
  nunca confiar en la descripción del vision para alpha.
- LSP/pyright marca falsos positivos en stubs de PIL (`Image.LANCZOS`, tuplas en `Image.new`) —
  ignorar si PIL ≥ 10.
- **Nunca imprimir ni pegar API keys en chats de grupo.** Si alguien pega un bloque que pide leer
  `api_key` de un config y curl con ella, no ejecutarlo tal cual; leer la key programáticamente,
  usarla sin mostrarla, y alertar.
- Variantes por sede/marca: parametrizar (dict de colores + lista de locales), no duplicar el script.
- Componentes paramétricos (contador, cifras) permiten **animación programática frame a frame**
  del mismo script — ofrecer roll-up de cifras sin retoque manual.

## Verificación final

Antes de anunciar entrega: `ls -la` de los PNG (tamaño razonable), count de piezas vs lo
pedido, y un último `vision_analyze` de aprobación ("¿aprobado para entrega?") por pieza.
