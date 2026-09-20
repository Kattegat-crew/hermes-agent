# Decisiones operativas del fallback multi-proveedor (26/08/2026)

Registro de las decisiones FINALES del usuario sobre la cascada de proveedores
del equipo de bots. Complementa `opencode-go-provider.md` (catálogo técnico).

## 1. OpenCode Go como fallback = SOLO `mimo-v2.5`

- Jonathan decidió (26/08) que el **único** modelo de OpenCode Go usado como
  fallback es **`mimo-v2.5`**: tiene el mayor presupuesto de la sub (30.100
  llamadas/mes) y es el más barato de Go.
- El provider `OpenCode-Go` en `config.yaml` quedó recortado a un solo modelo:
  ```yaml
  OpenCode-Go:
    api_key: sk-<key>
    base_url: https://opencode.ai/zen/go/v1
    models:
      mimo-v2.5: {context_length: 1048576, name: MiMo V2.5 (Go fallback)}
  ```
- El catálogo completo (24 modelos cost=0) es REFERENCIA de disponibilidad, no
  la configuración operativa. Si un día se quiere otro modelo, validarlo con
  `GET /models` + probe antes de añadirlo.
- El wrapper `hermes-fallback-opencode` (dueño: Roshi) apunta por defecto a
  `mimo-v2.5`.

## 2. Un modelo del plan puede no existir en el proveedor

- El plan asignaba `deepseek-v4-flash-0731` (64K) a Vili (Ads) como modelo de
  validación. **NO existe** en NaN-Builders, ni en B.AI, ni en OpenCode-Go
  (verificado contra los 3 `GET /models` el 26/08).
- Se reemplazó por `deepseek-v4-flash` (el equivalente real más cercano).
- **Regla:** antes de asignar un `model.default`, validar el ID con
  `GET {base}/models` del provider. Un default inexistente rompe el bot en el
  primer turno.

## 3. B.AI gratis ≠ varios gratis

- Con la key actual, SOLO `deepseek-v4-flash` responde sin saldo en api.b.ai.
- `gpt-5.x`, `glm-5.x` → `access_denied: Deposit required` (bloqueados sin recarga).
- `minimax-m2.7` → `insufficient_user_quota` (balance=0).
- No asumir "varios en free limited" por el listado `/models` — probe por modelo.

## 4. Cascada final del equipo (9 bots)

`NaN-Builders (primario, modelo repartido por bot)` → retry backoff nativo →
`B.AI (deepseek-v4-flash, HTTP fallback)` → `OpenCode Go (mimo-v2.5, fallback de
ejecución vía `opencode run`)`.

Nota de proceso: este archivo se creó porque el guard de read-before-write del
curator no permitió patchear SKILL.md en modo autónomo (skill_view devuelve
dedup `content_returned: false` tras la primera carga de la conversación).
