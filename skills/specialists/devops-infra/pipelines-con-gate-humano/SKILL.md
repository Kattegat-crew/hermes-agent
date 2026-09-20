---
name: pipelines-con-gate-humano
description: "Use when construyendo un flujo por etapas con OK humano."
version: 1.0.0
author: Roshi
metadata:
  hermes:
    tags: [gates, aprobacion-humana, pipelines, etapas, genericidad, yisus]
    related_skills: [sesion-pieza-por-pieza, guion-reel-mesa-medida, hermes-agent]
---

# Flujos por etapas con gate humano (el freno vive en el código)

Clase de trabajo: el usuario pide **un proceso por etapas donde él aprueba cada paso** (producción de
piezas, documentos, publicaciones, despliegues, generaciones pagas). La lección que gobierna esta clase,
y que Yisus tuvo que corregir dos veces el 12-sep-2026:

> *"Generaste completo el guion sin ninguna interacción conmigo, eso no es lo que estábamos programando"*
> *"Siento que simplemente vas a trabajar en el orden que hablamos, pero no veo que estés ejecutando un
> script del repo"*

Traducción operativa: **no basta con portarse bien; el bloqueo tiene que estar en el código.**
Un pedido de "flujo asistido paso a paso" es un pedido de software con estados y firmas, no una promesa
verbal de disciplina.

## Reglas duras

1. **Nunca escribir una etapa cuyo predecesor no esté `aprobada`.** Se puede leer la especificación,
   medir, preparar candidatas y dejar todo listo — pero **no** redactar el entregable ni elegir por
   cuenta propia las decisiones que el usuario se reservó (sede, tema, alcance, gasto).
2. **Nunca firmar en nombre del usuario.** Los comandos de aprobación llevan `--por NOMBRE` y ese nombre
   solo se usa cuando él lo dio explícitamente (`--por Yisus` cuando dijo "la sede es X").
3. **El freno se implementa, no se promete.** Función de bloqueo en el script (ej. `_exigir_etapa_previa()
   en `guion_session.py`): cada comando de escritura verifica que la etapa anterior esté firmada, la
   aprobación no permite saltar etapas, y las etapas pagadas exigen un candado con presupuesto máximo.
   Si el hueco aparece en una sesión, se tapa **antes** de seguir produciendo.
4. **Antes de editar código: análisis y plan.** Yisus lo dijo textual: *"no edites nada, primero analicemos
   y planifiquemos"*. Primero inventario con evidencia (archivo:línea), después propuesta, después OK.
5. **Ritmo de 2 vueltas por etapa**: propuesta → corrección → cerrada. Cada cierre de etapa termina con
   el artefacto, el costo estimado y la pregunta `¿OK, ajuste o STOP?`. Nunca dos etapas en un mensaje.
6. **Si te adelantaste, sé honesto y no destruyas nada**: devuelve el estado a la etapa real, mueve lo
   no firmado a una carpeta `no-aprobado/`, anótalo en la bitácora y dilo en el chat. Yisus premia la
   honestidad; castiga el maquillaje.

## La máquina debe ser genérica (segundo pedido del 12-sep)

Un flujo atado a la instancia actual (una campaña, un cliente, un mes) es deuda: cuando la instancia
cambia hay que reescribirlo. El entregable de esta clase es una **máquina + un contrato por instancia**:

- Los datos duros, fechas, catálogos, plantillas, vetos y personajes salen del **contrato de la
  instancia** (ej. `planning/<slug>/campaign.yaml`), nunca de constantes en el código ni de rutas de un
  solo mes.
- El CLI arranca con **filtros iniciales** que cargan el contrato (`nueva --campaign <slug>`) y de ahí
  resuelve todo lo demás.
- **Prueba de genericidad obligatoria**: correr la máquina completa con una instancia **ficticia**
  (otro mes, otro evento, sin los elementos particulares de hoy) en modo dry-run. Si pasa, es genérica.
- Cómo auditar una máquina existente (búsqueda de constantes clavadas, quién invoca a quién, si el
  handoff con el pipeline real existe): `references/auditoria-de-genericidad.md`.

## Cómo cerrar cada etapa en el chat

```
ETAPA <n> · <NOMBRE> — <id de la pieza>
· qué se produjo (una línea) y dónde vive el artefacto
· costo real / estimado de la etapa
· lo que falta o cambió respecto a la etapa anterior
[adjunto o ruta del artefacto]
¿OK, ajuste o STOP?
```

## Señales de que el flujo está mal construido

- El agente puede escribir la etapa N sin que la N-1 esté firmada (hueco de bloqueo).
- La aprobación no deja rastro: sin hash del artefacto, sin nombre de quien firmó, sin bitácora.
- El estado real y el estado declarado difieren (artefactos escritos que "no cuentan" sin marcarlos).
- La máquina solo corre para la instancia de hoy (mes/campaña/cliente clavados en el código).
- El pipeline siguiente nunca se invoca desde la máquina: el handoff es un archivo que nadie lee.
