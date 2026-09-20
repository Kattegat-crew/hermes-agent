---
name: hermes-provider-ops
description: "Paraguas consolidado para hermes-provider-ops. curado: fallback y resilience son el mismo problema (Jaccard 0.30+)"
version: 2.0.0
author: NeuralCrew
---

# Hermes Provider Ops

## Propósito y Alcance
Habilidad consolidada de clase que centraliza los flujos de:
- `hermes-model-rotation`
- `hermes-provider-configuration`
- `hermes-provider-fallback`
- `hermes-provider-resilience`
- `hermes-release-adoption`

## Arquitectura y Protocolos
Esta skill opera como despacho unificado. El detalle procedural y gotchas específicos de cada caso se encuentran preservados en:
`references/`

## Casos de Uso Disponibles
- **hermes-model-rotation**: Ver [references/hermes-model-rotation.md](file:///root/hermes-agent/skills/core/hermes-provider-ops/references/hermes-model-rotation.md)
- **hermes-provider-configuration**: Ver [references/hermes-provider-configuration.md](file:///root/hermes-agent/skills/core/hermes-provider-ops/references/hermes-provider-configuration.md)
- **hermes-provider-fallback**: Ver [references/hermes-provider-fallback.md](file:///root/hermes-agent/skills/core/hermes-provider-ops/references/hermes-provider-fallback.md)
- **hermes-provider-resilience**: Ver [references/hermes-provider-resilience.md](file:///root/hermes-agent/skills/core/hermes-provider-ops/references/hermes-provider-resilience.md)
- **hermes-release-adoption**: Ver [references/hermes-release-adoption.md](file:///root/hermes-agent/skills/core/hermes-provider-ops/references/hermes-release-adoption.md)
