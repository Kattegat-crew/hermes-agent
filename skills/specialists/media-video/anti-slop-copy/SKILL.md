---
name: anti-slop-copy
description: Audita copy para quitar tells de IA antes de publicar.
category: creative
metadata:
  author: Ragnar
  version: "1.0"
  created: "2026-08-21"
  tags: [copy, slop, humanizing, marketing, anti-ai]
  related_skills: [humanizer, no-ai-slop, anti-ai-slop-writing, anti-slop]
---

# Anti-Slop Copy — quitar el tinte de IA del copy

## Cuándo usar

Cualquier copy que vaya a publicarse para el negocio (NeuralCrew, Golden, Lucky,
Bendabal, Digital Expressions, Guaya Racing): web, ads, reels, social media, email.
Sin importar si lo generaste tú o un subagente — **correr anti-slop antes de entregar**.

Los textos con "tells" de IA erosionan la confianza del cliente exactamente donde
más importa (hero, CTA, prueba social). La web de NeuralCrew ya pide que el copy
"no parezca de IA" — esta skill es el mecanismo para lograrlo.

## Skills instaladas (21/08/2026) en `creative/`

El library de Hermes ya tiene estas 4 skills de escritura anti-slop. Cárgalas según
el trabajo:

| Skill | Enfoque | Cuándo |
|-------|---------|--------|
| `no-ai-slop` | Edición mínima preservando voz + modo *detect* que cita cada tell con evidencia | Copy de tajadas, revisar un draft sin reescribir |
| `anti-ai-slop-writing` | Directiva v2: banned-words + anti rule-of-three, parataxis, em-dash, uniformidad | Redacción desde cero con reglas firmes (copy largo) |
| `anti-slop` | Catálogo de tells + guardrail de box: no aplanar la voz | Auditar prosa/marketing copy |
| `humanizer` | Quita AI-isms, añade voz real | YA instalada antes; para texto suelto |

Ver el listado real con `skills_list(category="creative")` — los 3 nuevos se ven ahí.

## Flujo recomendado

1. **Redactar** con `anti-ai-slop-writing` activo (banned-words, variar longitud de
   frase, no rule-of-three salvo que sea real).
2. **Detectar** con `no-ai-slop detect` — que cite cada patrón con la línea exacta
   y el fix en 1 frase. Patrones nombrados = evidencia.
3. **Corregir cirujano** con `anti-slop`/`no-ai-slop`: el mínimo cambio efectivo,
   preserva el tono de la marca. No reemplazar una pieza con otras.
4. **Verificar** cadencia: sin parataxis de 3+ frases cortas seguidas, ≤1 em-dash
   por 500 palabras, sin banned word.

## Tells que matan el copy

- **Banned words**: delve, foster, leverage, seamless, robust, cutting-edge, empower,
  unlock, elevate, tapestry, realm.
- **Hedging**: "one might argue". **Inflación**: "marks a pivotal moment", "testament".
- **Setup falso**: "What nobody tells you", "the part everyone misses".
- **Colon reveal**: "The best part: it learns." → reescribir en prosa.
- **Rule-of-three fabricado** — solo si hay tres de verdad.
- **Metacomentario**: "In this article", "let's dive in", "It's worth noting".
- **Empaquetado**: copy en UN solo bloque, sin viñetas (preferencia de Jonathan).

## Referencia: catálogo del rank anti-slop

Ver `references/slop-skill-catalog.md` — las 10 skills del rank de @juampitech
(2026-08-21), con fuente, estado (instalada/omitida/rota) y método de instalación.
Útil para evaluar skills anti-slop futuras sin volver a rastrear la web.

## Pitfalls

- **No confundir copy con diseño visual.** Las anti-slop de texto no cazan slop
  visual (glassmorphism decorativo, grids genéricas, animaciones por defecto). Para
  diseño web usar `popular-web-designs` + `claude-design`.
- **No instalar duplicados.** Si `humanizer` ya existe, saltar otra skill del mismo
  tipo. Verificar con `skills list`.
- **Repos rotos se omiten** (ej. `unslop` de poteto → 404 en skills.sh): no inventar.
- **Instalar no es fabricar**: los SKILL.md se extraen del repo real clonado, no se
  reescriben de memoria.

## Referencias

- Skills: `no-ai-slop`, `anti-ai-slop-writing`, `anti-slop`, `humanizer` (todas `creative/`).
- Referencia: `references/slop-skill-catalog.md`.