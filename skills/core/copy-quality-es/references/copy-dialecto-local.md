---
name: copy-dialecto-local
description: "Use when el copy debe sonar local (dialecto regional)."
version: 1.0.0
author: Ragnar (NeuralCrew Labs)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    category: creative
    tags: [copy, dialecto, regionalismo, perifoneo, guion, espanol, colombia, localizacion]
    related_skills: [anti-slop-copy, humanizer, guion-video-campana, no-ai-slop]
---

# Copy con dialecto local — humanizar sin caricaturizar

Para cuando el encargo es *"que suene de acá"*: cuñas de perifoneo, guiones de reel,
locuciones, copy de redes o volantes dirigidos a un municipio o región concreta.

**Regla madre: el dialecto es sal, no plato principal.** Un marcador bien puesto hace
que el oyente reconozca su tierra; cinco lo hacen reírse del anuncio.

---

## 0. Primero los datos duros: derivar del material aprobado, no del brain

Antes de escribir una sola línea, asegurar **qué** se anuncia y **con qué cifras**:

1. Buscar la **pieza aprobada y vigente** del cliente (afiche, banners de TV, volante,
   reel ya publicado) en Drive — es la fuente de verdad de fechas, premios, mecánica,
   dirección y letras legales obligatorias.
2. Si la pieza es imagen, **transcribirla con `vision_analyze`** ("transcribe literalmente
   TODO el texto visible": titular, promos, precios, fechas, dirección, avisos legales).
   El afiche es más confiable que cualquier resumen previo.
3. **No confiar en el brain/planes cuando contradicen el material vigente.** Caso real:
   las fichas decían "sede X cerrada y excluida del bingo" y el afiche aprobado de esa
   sede anunciaba precisamente el bingo. Ante conflicto, gana la pieza publicada; y si la
   discrepancia afecta plata o cumplimiento, avisarlo explícitamente al Admin.
4. Separar lo **verificado** de lo **pedido por el cliente** (sus frases de marca se
   respetan literales) y de lo **inventado** (prohibido).

## 1. Perfilar el habla del lugar (investigación con fuente, no con intuición)

Lanzar subagentes en paralelo (`delegate_task`), uno por ángulo, y exigir **fuente por
hallazgo + `confianza`** en el `output_schema`. Reparto que funcionó:

| Ángulo | Qué entrega |
|---|---|
| Glosario del habla local | 25-40 entradas con significado, registro, zona y URL de fuente |
| Registro oral (cómo invita/vende/atiende) | fórmulas de apertura, invitación, cierre + 3 ejemplos de estructura |
| Límites de la humanización | clichés a evitar, errores de foráneos, **regla de dosis** |
| Contexto del lugar | qué es la ciudad, su gente, comercio, días fuertes, referencias auténticas vs. invento de agencia |

Fuentes que rinden: corpus académicos (p. ej. Instituto Caro y Cuervo, ALEC, tesis de
universidades), artículos de sociolingüística, prensa y radio local, sitios de alcaldía y
cámara de comercio. **Los subtítulos de YouTube suelen estar bloqueados desde servidor** —
no es excusa para inventar: se documentan los patrones desde corpus y prensa y se dice
que la validación en audio queda pendiente.

Guardar el resultado como insumo reutilizable del lugar (p. ej.
`/opt/data/brain/concepts/habla-<lugar>.md`) para que el próximo copy no vuelva a
investigar de cero.

## 2. Regla de dosis 1-1-1 (el corazón de esta skill)

- Máximo **1 marcador dialectal cada 15 s** de cuña → 20 s = 2; 30 s = 2; 45 s = 3.
- **1 marcador en la apertura** (0-5 s: vocativo de barrio, saludo local) y **1 en el cierre**
  (últimos 4-6 s: despedida cálida o guiño local).
- **El cuerpo va en español estándar**: oferta, premios, cifras, fechas, horarios,
  dirección y letra pequeña (+18, juego responsable, autoridad de regulación) no llevan
  dialecto — en la calle, con ruido, la claridad manda.
- Reglas duras: nunca dos marcadores en la misma frase; nunca repetir el mismo marcador;
  nunca apilar cortesías ("sumercé + a la orden + mijo" = pastiche de mostrador).
- **El tratamiento se decide con evidencia, no por folclor.** Ejemplo verificado: en
  Chiquinquirá la forma base es **usted** (48,2 % del corpus sociolingüístico local, y el
  núcleo comercial no usa tú ni vos) → escribir en tuteo *delata* texto hecho fuera, aunque
  el tuteo sea la convención de la marca en otras plazas.

## 3. Ritmo y longitud (audio de calle)

Perifoneo pausado ≈ **130 palabras/min (2,17 pal/s)**:

| Duración | Palabras |
|---|---|
| 20 s | 40-50 |
| 30 s | 60-70 |
| 45 s | 90-100 |

Medir con conteo real de palabras (no a ojo) y declarar la duración estimada en la entrega.
En cuña de calle el dato clave (día, hora, lugar) **se dice dos veces**: la gente escucha
fracciones del mensaje.

## 4. Pruebas de control antes de entregar

1. **Sustracción** — tachar los 2-3 marcadores: el cuerpo debe seguir entendiéndose solo.
   Si no, el dialecto era muleta.
2. **Oído** — leer en voz alta: si suena a imitación o burla, se cambia la redacción o la voz.
3. **Conteo 1-2-3** — contar marcadores; si superó el tope, recortar.

## 5. Prohibiciones (con respaldo, no gustos)

- Llamar al público con el gentilicio despectivo ("boyaco" → "boyacense").
- Acento fingido: alargar vocales, forzar la "r", carraspera campesina. El acento es marca
  de territorio y clase: se nota en el primer segundo.
- Léxico de otra región pegado al local (en Colombia: "parce", "¿quihubo?", "bacano", "ve",
  voseo) creyéndolo del lugar.
- "Pues" al final de toda frase y diminutivo -ito/-ico en cada sustantivo: son caricatura,
  además de robar segundos.
- Folclor decorativo (ruana, sombrero, carranga) **tapando la oferta**: si el cliché tapa el
  mensaje, no hay aviso.
- Humor que se ríe del público (el "provinciano tonto"): clasista y mata credibilidad.

## 6. Perifoneo (formato de cuña)

Estructura, ciclo de emisión, variantes y pauta de grabación: ver
`references/perifoneo-cuna-formato.md`.
Perfil verificado de Boyacá/Chiquinquirá (usted base, glosario, referencias locales y
fuentes): ver `references/boyaca-chiquinquira.md`.

## Pitfalls

- **No humanizar ≠ folclorizar.** "Humanizar" es usar la voz y los códigos reales del barrio,
  no vestir el aviso de campesino.
- **No cambiar el tratamiento sin avisar.** Si la marca viene en tuteo y la evidencia local
  dice usted, el cambio se explica al Admin con el dato (no se hace en silencio ni se ignora).
- **No creer cifras de memoria.** Premios, fechas y direcciones salen de la pieza aprobada;
  si no hay fuente, va `[CONFIRMAR]` en el guion, nunca un número inventado.
- **Una sola idea comercial por cuña corta.** Si hay dos mensajes (p. ej. novedad + evento),
  se resuelven con una cuña mixta larga **y** versiones cortas de un solo tema.
- **La voz es parte del guion.** Guion local con locutor de acento neutro o imitado = trabajo
  perdido; especificar "locutor de la región, ritmo pausado, sin acento fingido".
- **Música del lugar, no la de moda.** En el altiplano cundiboyacense: popular/carrilera, no
  reggaetón.

## Related

- `anti-slop-copy` — quita tells de IA (aplicar después de humanizar el dialecto).
- `humanizer` — voz y ritmo en prosa.
- `guion-video-campana` — piezas audiovisuales de campaña (reels).
