---
name: agent-worktree-orchestration
description: "Use when parallel agents share one repo (worktrees)."
tags: [worktrees, orca, agentes, paralelismo, git, aislamiento, orquestacion, ramas]
version: 1.0.0
author: curator-ragnar
triggers:
  - "usa worktrees"
  - "agents en paralelo en el mismo repo"
  - "cómo usarías orca"
  - "worktree por tarea"
  - "ramas que no llevan a ningún lado"
  - "plan con muchos cambios en un repo"
---

# Agent Worktree Orchestration — un worktree por unidad de trabajo

Clase de tarea: hay que ejecutar **varias unidades de trabajo** sobre un mismo repo (saneamiento, features
paralelas, un plan por fases) y se quiere (a) paralelismo real sin pisarse y (b) higiene de ramas.
Lección central: **la rama debe nacer y morir con su unidad**; el worktree es el mecanismo que lo garantiza.

## Por qué worktree y no rama suelta

- Aislamiento de **sistema de ficheros**: cada agente tiene su copia de trabajo; dos agentes no compiten
  por el mismo archivo ni por el mismo `__pycache__`/artefacto de build.
- **Trazabilidad**: la unidad = worktree = rama = PR = commit(s). Al fusionar se borra el worktree y con él
  la rama: cero ramas huérfanas *por construcción*, que es exactamente lo que suele pedir el usuario
  ("sin ramas que no lleven a ningún lado").
- Encaja con planes grandes: `WU-nn` (work unit) ↔ worktree ↔ agente ↔ evidencia.

## Reglas duras

1. **Un fichero, un worktree.** Si dos unidades tocan el mismo archivo, se serializan (no hay merge sin dolor).
2. **El orden importa más que el paralelismo.** Primero el prerequisito que todo el mundo necesita
   (runtime/deps reproducibles), después las unidades independientes en paralelo.
3. **Cada worktree debe poder correr los tests del repo solo.** Si el entorno no es reproducible
   (`requirements.txt` + bootstrap que verifique imports), un worktree limpio no sirve para nada: arregla
   eso ANTES de paralelizar. Un `.venv` no trackeado y no reconstruible es el bloqueo clásico.
4. **Revisar antes de fusionar**: `diff` del worktree + salida del agente (terminal) — la autodeclaración del
   agente no es evidencia.
5. **Cerrar el ciclo**: fusionar → `rm` del worktree → verificar `git status` limpio y la rama borrada
   (local y remoto). Sin este paso el plan reintroduce la basura que venía a limpiar.
6. **Nada de worktrees para arreglos de una línea** ni para cambios que toquen sistemas en vivo
   (prod/deploy): eso se hace directo, con backup y evidencia.

## Orca (orquestador instalado en el host DEV)

Orca = app + CLI que crea worktrees gestionados, lanza un agente dentro de cada uno y expone sus
terminales. Es la implementación concreta del patrón en esta casa (complementa a `delegate_task`: éste da
contexto aislado en el mismo gateway; Orca da aislamiento de ficheros + terminal controlable).

```bash
# el servidor corre como usuario `orca`: unit orca-serve.service, ws://<tailscale>:6768
orca environment list --json                  # entornos emparejados
orca repo list --json --environment <env>     # repos registrados (nombre + ruta)
orca repo add /ruta/al/repo && orca repo set-base-ref --repo name:<repo> main
orca worktree create --repo name:<repo> --name wu-06-refiner --agent opencode --prompt '<prompt>'
orca worktree ps --json --environment <env>   # resumen de worktrees vivos
orca terminal read --terminal <handle> --json # qué hizo el agente
orca file diff                               # cambio antes de fusionar
orca worktree rm --worktree id:<id> --force --json
orca orchestration run-create                # Run/DAG para dependencias entre unidades
orca automations list|create|run|runs        # tareas programadas
```

Hechos operativos que cuestan tiempo si se ignoran (verificados 11/09/2026):

- **El CLI puede decir `stale_bootstrap` / `runtime_unavailable` con el servidor VIVO.** El bootstrap local
  queda obsoleto tras reiniciar la app; apunta al entorno emparejado con `--environment <nombre>`
  (verificado funcionando) o `--pairing-code` (sale en el journal del unit). No concluyas «Orca está roto».
- **`--json` no basta: la salida incrusta iconos en base64** (~100 KB en un `repo list`). Parsea en Python e
  imprime solo los campos que necesitas; volcar el JSON crudo inunda la sesión.
- **Permisos**: `.git` debe ser escribible por el usuario que corre Orca. En DEV, `orca` es uid 997/gid 987 y
  el repo suele ser de `hermes` (uid 10000): sin grupo/ACL compartido, `worktree create` falla.
  Alternativa sin tocar permisos: rama por unidad en el árbol único (secuencial, cero riesgo).
- **Los worktrees no heredan el entorno del repo** (`.venv`, `.env`): bootstrap obligatorio.
- **Registro obsoleto**: tras mover un repo, Orca conserva el nombre y la ruta viejos; `orca repo list`
  muestra la ruta muerta. Audítalo al reorganizar y retira la entrada vieja.

## Cómo se ve en un plan

Cada work unit lleva: objetivo · entregable · **criterio de aceptación** · **evidencia (comando + salida)** ·
riesgo · worktree/rama asignada. El paralelismo se decide por colisión de ficheros, no por entusiasmo.
Delegar el diseño del plan a un modelo externo y pedirle que intente **demolerlo** (huecos, orden, riesgos
mal mitigados, criterios de aceptación tautológicos) es la verificación más barata que existe antes de
escribir código: plantilla en la skill `capability-claim-verification` →
`templates/plan-review-prompt.md`.

## Pitfalls

- No confundir aislamiento de **contexto** (`delegate_task`) con aislamiento de **ficheros** (worktree):
  dos subagentes en el mismo gateway siguen escribiendo en el mismo repo.
- Los hijos reportan éxito por autodeclaración: verifica los artefactos (fichero/rama/diff) tú mismo.
- Un worktree absorbido por otro (rename/movimiento) deja `worktreeId` apuntando a una ruta muerta.
- Si el plan promete «cero ramas huérfanas», el criterio de aceptación debe ser comprobable:
  `git branch -a` → solo la canónica, local **y** remoto.

## Soporte

- `references/orca-dev-environment.md` — hechos del entorno Orca de DEV (usuarios, entorno emparejado,
  comandos exactos verificados, salida a parsear).
