---
name: flujos-con-gates-humanos
description: "Use when designing flows with human approval gates"
tags: [gates, aprobaciones, firma-humana, human-in-the-loop, automatizacion, proceso, campanas]
version: 1.0.0
metadata:
  hermes:
    tags: [gates, aprobaciones, automatizacion, campanas, proceso, firma-humana]
    related_skills: [sesion-pieza-por-pieza, guion-reel-mesa-medida, campanas-qa-integridad]
---

# Flujos con gates humanos (construidos para Yisus)

Clase de trabajo: **disenar o construir un proceso asistido** donde el dueño aprueba paso a paso
(guiones de campana, generacion de piezas, pipelines con gasto, cualquier flujo por etapas). Aqui vive
CÓMO debe comportarse el agente y CÓMO debe quedar la automatizacion. El detalle del proceso de guiones
(40 interacciones, vacios y fases) esta en `references/proceso-interactivo-40-pasos.md`.

## Las 6 reglas que el dueño ya corrigio en carne propia (12-sep-2026)

1. **El freno vive en el script, no en la disciplina del agente.** Cita textual: *"no veo que estes
ejecutando un script del repo"*. Si la unica cosa que impide adelantar trabajo es mi autocontrol, no
existe: el bloqueo va en el codigo (funcion tipo `_exigir_etapa_previa()`), con test, y se muestra la
salida real del comando.
2. **Nunca adelantar etapas.** Escribir concepto + guion + elegir la sede de una pieza "para probar"
termino en: *"generaste completo el guion sin ninguna interaccion conmigo, eso no es lo que estabamos
programando"*. Se hace **solo el paso que toca** y se espera la firma; la sede y cada aprobacion las
firma un humano con su nombre (`--por NOMBRE`).
3. **Pasos = INTERACCIONES, no etapas.** Cuando pide el desglose de un proceso quiere la lista
usuario ⇄ agente numerada 1..N con ramas (`6.1`, `6.2`) y **una linea por paso**. Un desglose por
etapas o por fases lo rechaza: *"te dije muy claro que por pasos"*.
4. **Analizar y planear ANTES de editar.** "No edites, solo realiza el plan" = lectura read-only del
repo y un documento de plan (en `workspace/plans/`), sin commits ni archivos nuevos en el repo del
cliente. El plan lleva unidades de trabajo (WU), aceptacion medible, costo $0, riesgos/no-goals y las
decisiones que le tocan al dueño; cada hallazgo citado con `archivo:linea`.
5. **Evidencia, no promesas.** Al cerrar se pega la salida real (incluido el `ERROR: BLOQUEADO ...`),
`git status`/`git log` del repo tocado, y el conteo de tests. Nada se declara hecho por "deberia
funcionar".
6. **Un solo carril de estado.** No duplicar la maquina de estados en dos sitios (la copia vieja queda
declara como historica): el estado del proceso vive en un lugar y el resto lo lee.

## Como se entrega cada gate

- **Propuesta → correccion → cerrada:** maximo 2 vueltas por paso; si el cambio llega tarde, se dice
  QUE se regenera y CUANTO cuesta **antes** de ejecutarlo.
- **Costo $0 primero:** toda etapa gratis (texto, medicion, lint, plan, dry-run) se cierra antes de
  tocar una API paga, y la etapa paga exige firma explicita con presupuesto maximo (gate fisico tipo
  `.spend-gate.json`: `approved_by` humano + `providers` + TTL corto).
- **Bloqueo activo probado:** se demuestra con un comando que el script **rechaza** lo que no toca
  (`exit=1` + mensaje), y con la suite de tests en verde.

## Al construir el flujo (checklist de diseno)

1. Capa de contexto **generica** (contrato por campana/cliente) separada de la logica: nada de marcas,
   eventos, mecanicas ni rutas de UNA campana dentro del codigo.
2. Filtros iniciales como menus: cliente → campana → tipo → alcance → sede → fecha; el resto se hereda.
3. Estado por pieza en un directorio versionado, con bitacora append-only y hash del artefacto firmado.
4. Un test por paso del flujo (no solo por funcion).
5. Cableado a las piezas que YA existen del pipeline objetivo (motor, lint, publicacion) en vez de
   construir un pipeline paralelo.
6. Prueba de genericidad: un caso ficticio (otro cliente/mes/mecanica) corriendo de punta a punta en
   modo gratis.

## Pitfalls

- **Escribir artefactos "de referencia" sin firma contamina el estado:** si ya se escribio algo sin
  aprobacion, se mueve a `<sesion>/no-aprobado/`, se devuelve la etapa a su punto, y se anota en la
  bitacora que paso. No se borra el trabajo ni se deja contando como etapa.
- **Un scaffold que no pasa su propio linter es deuda inmediata:** si la herramienta genera el archivo
  con un formato que su propio validador rechaza, se arregla en la herramienta (con test), no a mano en
  cada pieza.
- **El "plan" no es un volcado:** en el chat va el resumen (vacios, fases, decisiones); el documento
  completo va adjunto (`MEDIA:`).
