---
name: infografia-cliente-html-png
description: "Use when a client needs an explanatory infographic."
tags: [infografia, html, png, chrome-headless, cliente, vision]
version: 1.0.0
author: ragnar
triggers:
  - "explicame graficamente"
  - "de la manera mas simple"
  - "para cualquier persona"
  - "infografia"
  - "como funciona todo"
---

# Infografia para cliente: HTML -> PNG

Para explicar "como funciona todo" a alguien NO tecnico: una sola imagen, en palabras llanas, con las cifras REALES del sistema. Validado con el Admin 11-sep-2026 (generador de campanas).

## Regla de oro del contenido

- **El texto grande es para cualquiera** (cero jerga). La jerga va SOLO en una etiqueta gris pequena debajo (`<span class="tech">`): da credibilidad tecnica sin estorbar.
- Cada paso = **titulo llano + 1-2 frases de beneficio + etiqueta tecnica**. Nada mas.
- **Verifica las cifras ANTES de dibujar** (piezas por estado, servicios vivos, canales). Nunca inventes un numero en una imagen que el cliente va a mirar.
- Incluye las **reglas duras** del sistema (aqui: "nada se paga sin su firma") y los **estados** de una pieza como cadena de pildoras.
- Separa al final **que ya opera** de **que falta**: el cliente necesita saber donde esta el borde real.

## Estructura que funciono

1. Cabecera: titulo de 2 lineas + "quien eres" a la derecha.
2. **Flujo vertical numerado** (8-9 pasos): circulo de color + tarjeta blanca con borde izquierdo del color de la fase, unidas por una linea vertical (la ultima tarjeta no lleva raya).
3. **Columna lateral**: "quien hace que" (humanos vs IA), la regla dura en recuadro de alerta, y los 4 estados.
4. Pie oscuro con el resumen y 2-3 cifras grandes.

Paleta por FASES: idea/plan = azul `#1F3A5F`, produccion = oro `#B8860B`, control = rojo `#AB0F15`, publicacion = verde `#0E6B3A`. Fondo `#EEF2F7`, tarjetas blancas.

## Render (DEV)

```bash
/opt/chrome-for-testing/chrome-linux64/chrome --headless=new --no-sandbox --disable-gpu \
  --hide-scrollbars --force-device-scale-factor=2 --window-size=1400,1620 \
  --screenshot=/root/hermes-agent/data/drafts/salida.png file:///root/hermes-agent/data/drafts/salida.html
chown hermes:10000 /root/hermes-agent/data/drafts/salida.{html,png}
```

Escribe el HTML en `/opt/data/drafts/` (= `/root/hermes-agent/data/drafts/` en el host): el mismo archivo se ve desde los dos lados, y el PNG queda listo para `MEDIA:`.

## Pitfalls verificados

1. **Sin emojis si no hay fuente de color**: `fc-list | grep -i emoji` vacio => salen cuadros. Usa numeros y formas CSS.
2. **Verifica SIEMPRE con vision antes de enviar**: la imagen completa (¿falta algo? ¿texto encimado?) y una **region del pie**. En la primera version la frase del pie se partio en dos lineas: se arregla con `white-space:nowrap` + acortando el texto, y el corte NO se ve en el HTML, solo en el PNG.
3. El **chromium del sistema puede ser un snap inservible headless**: usa Chrome for Testing.
4. Entrega **imagen + resumen en palabras**: el Admin pidio las dos cosas ("en palabras y graficamente"). El texto del chat sigue el mismo orden que los pasos de la imagen.
5. **Higiene**: chown a hermes y no dejar el HTML/PNG como root (rompe el reclamo de cero archivos ajenos).
