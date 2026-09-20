# Entorno Orca de DEV — hechos verificados (11/09/2026)

## Servicio y red

- Unit: `orca-serve.service` (systemd, host DEV). `User=orca`, `ExecStart=/opt/orca/orca-linux.AppImage
  serve --port 6768 --pairing-address <tailscale-ip>`, `Environment=LIBGL_ALWAYS_SOFTWARE=1`.
- Escucha en `0.0.0.0:6768` (proceso `orca-ide`) y además un puerto local efímero (`127.0.0.1:38xxx`).
- `Web client URL: http://<tailscale-ip>:6768/web-index.html#pairing=orca%3A%2F%2Fpair%3Fcode%3D…`
  y `Pairing URL: orca://pair?code=…` salen en `journalctl -u orca-serve.service -o cat`. El código de
  emparejamiento se recupera del journal (no lo imprimas en informes: es una credencial).
- Directorios: `/home/orca` (dueño `orca:orca`), `/home/orca/.orca` (estado del entorno).

## Usuarios y permisos (clave para worktrees)

| usuario | uid | gid | notas |
|---|---|---|---|
| `hermes` | 10000 | 10000 | dueño del repo del pipeline en DEV |
| `orca` | 997 | 987 | corre la app/CLI de Orca |

`git worktree add` (y por tanto `orca worktree create`) necesita escribir en `.git/worktrees`: con el repo en
`hermes:10000`, la app de Orca no puede. Receta segura: grupo compartido + `chmod g+ws` recursivo en `.git`
+ ACL por defecto, con el rollback anotado (`chown -R hermes:10000 .git` + quitar ACL) y verificando los tres
escritores (contenedor uid 10000, worker systemd, agente del worktree). El usuario root ignora permisos, así
que el contenedor (root) no se ve afectado.

## CLIs y formatos

- `orca status --json` → `{app: {running}, runtime: {state, reachable, runtimeId}}`. Si el CLI dice
  `stale_bootstrap` / `reachable: false` pero `systemctl is-active orca-serve.service` = `active`, NO está
  roto: el bootstrap local está obsoleto. Solución verificada: `orca <cmd> --environment <env>`.
- Commands útiles: `open`, `serve`, `status`, `diagnostics memory`, `agent-context`, `account`, `skills
  list|get|install`, `environment add|list|show|rm`, `vm recipe doctor`, `automations *`, `project *`,
  `repo list|add|show|set-base-ref|search-refs`, `worktree list|show|current|create|set|rm|ps`,
  `file open|diff|open-changed`, `terminal list|show|read|send|wait|stop|create|rename|split|switch|close`,
  `orchestration run-create|run-use`.
- **Parsear siempre**: `orca repo list --json` incrusta `repoIcon.src` en base64 (~100 KB con 8 repos).
  Ejemplo de impresión compacta: leer `result.repos[]` y mostrar `displayName`, `path`, `worktreeBaseRef`.

## Skills que Orca trae incluidas

`orca-cli` (worktrees, terminales, artifacts, browser embebido), `orchestration` (DAG, dispatch, gates,
coordinator loops), `computer-use`, `orca-per-workspace-env`, `orca-linear`, `orca-emulator[-android]`.
Consultables con `orca skills list` / `orca skills get <name>` — útiles para no reinventar comandos.

## Estado observado (11/09/2026)

- 8 repos registrados; worktrees vivos: 2 (main de `activepieces` y de `golden-game-landing`).
- Registro obsoleto corregido: el antiguo registro `video-ai-generator` fue purgado de la configuración de Orca y `marketing-campaign-generator` quedó normalizado a su ruta física `/root/marketing-campaign-generator`.
