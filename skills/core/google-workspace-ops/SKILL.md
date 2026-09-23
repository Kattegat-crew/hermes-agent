---
name: google-workspace-ops
description: "Paraguas consolidado para google-workspace-ops. verificado: 4 de ellas en un mismo cluster Jaccard>=0.30"
version: 2.0.0
author: NeuralCrew
---

# Google Workspace Ops

## Propósito y Alcance
Habilidad consolidada de clase que centraliza los flujos de:
- `activepieces-google-access`
- `gdrive-via-activepieces`
- `gmail-mailbox-organization`
- `gmail-smtp-app-password`
- `google-docs-api`
- `google-drive-access`
- `google-drive-sheets-ops`
- `google-workspace`

- `activepieces-flows-ops`

## Arquitectura y Protocolos
Esta skill opera como despacho unificado. El detalle procedural y gotchas específicos de cada caso se encuentran preservados en:
`references/`

## Casos de Uso Disponibles
- **activepieces-google-access**: Ver [references/activepieces-google-access.md](file:///root/hermes-agent/skills/core/google-workspace-ops/references/activepieces-google-access.md)
- **gdrive-via-activepieces**: Ver [references/gdrive-via-activepieces.md](file:///root/hermes-agent/skills/core/google-workspace-ops/references/gdrive-via-activepieces.md)
- **gmail-mailbox-organization**: Ver [references/gmail-mailbox-organization.md](file:///root/hermes-agent/skills/core/google-workspace-ops/references/gmail-mailbox-organization.md)
- **gmail-smtp-app-password**: Ver [references/gmail-smtp-app-password.md](file:///root/hermes-agent/skills/core/google-workspace-ops/references/gmail-smtp-app-password.md)
- **google-docs-api**: Ver [references/google-docs-api.md](file:///root/hermes-agent/skills/core/google-workspace-ops/references/google-docs-api.md)
- **google-drive-access**: Ver [references/google-drive-access.md](file:///root/hermes-agent/skills/core/google-workspace-ops/references/google-drive-access.md)
- **google-drive-sheets-ops**: Ver [references/google-drive-sheets-ops.md](file:///root/hermes-agent/skills/core/google-workspace-ops/references/google-drive-sheets-ops.md)
- **google-workspace**: Ver [references/google-workspace.md](file:///root/hermes-agent/skills/core/google-workspace-ops/references/google-workspace.md)
- **activepieces-flows-ops**: operar y reparar flows de ActivePieces: MCP, quitar o pausar pasos, reinyectar filas al Sheet y auditar la integridad — ver [references/activepieces-flows-ops.md](file:///root/hermes-agent/skills/core/google-workspace-ops/references/activepieces-flows-ops.md)
