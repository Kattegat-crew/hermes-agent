---
name: peer-report-verification
description: "Use when a peer agent's report needs verifying."
version: 1.0.0
category: devops
metadata:
  author: curator-ragnar
---

# Verificar el informe de un par (claim por claim, antes de opinar)

**Cuándo:** alguien te reenvía el informe, la auditoría o el resumen de **otro agente** —otro perfil
(Roshi, Bragi, Sindri), un subagente, un revisor externo— y pregunta «¿qué opinas?». También cuando
tú eres el par que va a *citar* ese informe dentro de una decisión.

No es una tarea de cortesía ni de redacción: es verificación de claims con una capa extra, porque el
objeto a verificar es un **documento** y su autor puede haber medido en otro namespace, otro uid u otro
`HOME` que los tuyos.

**Regla base:** un informe de par es un *self-report*. Se verifica, no se aprueba por lo bien escrito
que esté. El entregable es `verificado X/N` con el comando detrás de cada verificación — nunca
adjetivos («excelente informe») antes de la evidencia.

## Método (5 pasos)

1. **Localiza el artefacto y su paquete de evidencia.** Casi siempre trae adjuntos (logs, JSON, el
   binario producido). Léelos primero: son la parte reproducible del informe.
2. **Re-valida el baseline que el informe declara.** Si dice «repo `abc123`, limpio, al día»,
   compruébalo (`git log -1`, `git status --short`, `git status -sb`). Un baseline viejo invalida en
   silencio todo lo demás.
3. **Convierte cada afirmación en un check ejecutable y corre los baratos.** Conteos con Python sobre
   el JSONL/DB (no a ojo sobre una tabla), `grep` para constantes del código, `which` en **cada**
   namespace. Lo que no puedas ejecutar se reporta como no verificado.
4. **Reproduce SU experimento desde SU evidencia archivada**, no desde uno nuevo tuyo: lee su
   `logs.jsonl` (cadena de etapas + modo), haz `ffprobe` a su artefacto, abre su `audit-report.json`.
5. **Lo que vive en otro sistema se consulta en la fuente, read-only.** «El orquestador está roto» se
   cierra con SQL a la DB del orquestador (corridas agrupadas por flow y estado, con `max(created)`),
   nunca con la UI ni con su palabra.

## Las tres reglas que cambian el veredicto

- **Un run verde de dry-run valida el cableado, no la calidad.** En dry-run el artefacto puede ser un
  **placeholder sintético** y la auditoría de audio pasar **por silencio** (LUFS ≈ −70). «Cadena
  completa» ≠ «se ve bien»: dilo explícito o el usuario leerá de más.
- **El paquete de evidencia debe ser autocontenido.** Comprueba que el input archivado (brief/guion)
  corresponde a los logs y al artefacto entregado. Si no cuadra, es **matiz de rigor, no refutación**
  — separa las dos cosas.
- **Fallo aislado ≠ incidente, y tampoco se esconde.** 1 de 65 corridas fallando por un permiso
  transitorio, en un tick que no tenía nada que hacer, se reporta como transitorio + el estado
  **actual** + «vigilancia», no como alarma.

## Pitfalls

- **Namespace ajeno al leer la evidencia del par.** Sus rutas son de **su** entorno: el workspace de un
  perfil no existe en el host bajo la misma ruta. Resuélvelo por su equivalente
  (contenedor `/opt/data/...` = host `/root/hermes-agent/data/...`) o córrelo donde él lo ve. Un
  `No such file or directory` al medir su artefacto suele ser esto, no un archivo faltante.
- **Su `.venv` puede ser del host**: usarlo desde el contenedor da
  `Could not find platform independent libraries`. Corre por `ssh dev`.
- **Recuenta con `ORDER BY` temporal, nunca por `id`.** Las filas de ejecuciones se insertan fuera de
  orden tras un reinicio y el «último» run sale viejo.
- **Payload inline bloqueado (`BLOCKED (hardline)`).** Un one-liner largo con comillas anidadas,
  sustitución `$(…)` o varias sentencias con `;` se rechaza por **forma** del payload, no por la
  operación. El harness guarda lo bloqueado en `cache/blocked-scripts/` y se puede correr con
  `bash <archivo>`, pero lo correcto es partir en comandos pequeños o usar `search_files`.
- **Reconoce lo que el informe hace bien con el mismo detalle que los matices.** El veredicto incómodo
  («no es desatendido todavía») vale tanto como el crédito por haberlo medido; el usuario valora ambos.
- **Si el informe te corrige, incorpóralo en la misma respuesta** («me corrijo: …») y **retracta**
  cualquier hallazgo tuyo que su evidencia invalide.

## Vocabulario que el usuario espera al explicar un sistema vivo

`construido` (existe y está cableado) ≠ `operado` (corre de verdad, con evidencia) ≠ `pagado`
(estrenado con firma humana). Y al explicar el flujo, separa **quién tiene cada llave**: idea/guión,
  firma del gasto, aprobación de calidad y aprobación de publicación. Sin ese desglose, cualquier
  respuesta se lee como «todo funciona».

## Forma del entregable

1. Veredicto corto («acertado en todo lo que pude comprobar») + la lista de claims verificados con su
   comando.
2. 2–4 matices que le añadiría, cada uno con su razón (rigor, no objeciones).
3. Recomendación operativa concreta: archivar el informe **en el repo**
   (`docs/auditorias/AAAA-MM-DD-…md`, versionado y con commit), no en el workspace del perfil del
   autor — ese no es durable ni lo ve nadie.
4. Qué queda sin verificar y por qué (BLOCKED honesto antes que un verde parcial).

## Soporte

- `references/worked-case-2026-09-12-generador.md` — caso trabajado: auditoría de un par sobre el repo
  del generador de campañas (tabla claim → comando de verificación, los matices que le añadí y el
  hallazgo real de la DB del orquestador).

## Relación con otras skills

`capability-claim-verification` (verificar «ya está configurado») e `independent-infra-audit`
(auditoría read-only de un pipeline) cubren territorio adyacente y son **user-owned**: si necesitas
extenderlas, pide `hermes curator adopt <nombre>` en vez de duplicar su contenido aquí.
