# F6 · Lote 4 — pares del tramo 0,51–0,59 y declaración de falsos positivos

| Campo | Valor |
|---|---|
| Documento | `docs/skills/F6-LOTE4-EJECUCION.md` |
| Fecha | 2026-09-23 |
| Comando | `python3 scripts/f6_lote4_ejecutar.py --firma <TOKEN>` |
| Motor | `scripts/f6_lote4_ejecutar.py` (candado en código) |

## Absorbido (5)

| Absorbida | Superviviente | Motivo | Hash antes |
|---|---|---|---|
| `creative/neuralcrew-bot-avatars` | `creative/bot-avatar-config` | Misma tarea (instalar/actualizar el avatar de un bot). La absorbida te | `258514c4be3495ff` |
| `specialists/hermes-internal/hermes-desktop-windows-troubleshooting` | `specialists/hermes-internal/hermes-windows-install` | Mismo problema (fallo de instalación de Hermes Desktop en Windows). Su | `5f7c062133cb9f63` |
| `specialists/hermes-internal/hermes-provider-fallback` | `specialists/hermes-internal/hermes-provider-resilience` | Misma clase (redundancia/fallback multi-proveedor LLM). Superviviente  | `5ceabf71403ef1f5` |
| `specialists/hermes-internal/client-agent-soul-survey` | `specialists/hermes-internal/client-agent-onboarding` | Mismo proceso (/soul para perfilar clientes y armar su SOUL.md) y mism | `3781390dfaa173a8` |
| `specialists/hermes-internal/hermes-desktop-remote-setup` | `specialists/hermes-internal/hermes-desktop-remote-gateway` | Mismo asunto en dos fases (montaje / diagnóstico), igual que el par ba | `365e9e503d77c999` |

## Declarado FALSO POSITIVO (no se fusiona)

- **`autonomous-ai-agents/sdd-*`** (sim máx 0.6135, NO fusionar): Son FASES de un flujo (init, explore, propose, spec, design, tasks, apply, verify, onboard) con disparador propio y distinto: el orquestador las lanza por nombre. El parecido viene del andamiaje compartido (## Execution Role, ## Language Domain Contract, ## Purpose, ## What You Receive), que además ya está factorizado en specialists/hermes-internal/_shared/sdd-phase-common.md. Tamaños de 4.164 a 14.949 B: no son plantilla repetida. chained-pr entró al grupo sólo por el encabezado. Fusionarlas rompería disparadores legítimos.

- **`specialists/ai-ml/pytorch-fsdp <-> specialists/ai-ml/unsloth`** (sim máx 0.6850, NO fusionar): Herramientas distintas: FSDP (entrenamiento distribuido con sharding) frente a Unsloth (fine-tuning LoRA/QLoRA acelerado). El solape es del andamiaje de skills de ML. Cada una arrastra su propio references/ (486 KB y 1,86 MB).

- **`specialists/devops/aws-solution-architect <-> gcp-cloud-architect`** (sim máx 0.5087, NO fusionar): Proveedores distintos (AWS vs GCP): mismo andamiaje de skill de arquitectura, arquitecturas distintas. Fusionarlas borraría la mitad de la cobertura.

- **`specialists/marketing/3-statement-model <-> lbo-model`** (sim máx 0.5419, NO fusionar): Modelos financieros distintos (integrado IS/BS/CF vs LBO con IRR/MOIC). El parecido es del andamiaje de modelado en Excel.

- **`specialists/marketing/form-cro <-> signup`** (sim máx 0.5199, NO fusionar): Separación DELIBERADA: la descripción de form-cro dice "cualquier formulario que NO sea signup/registro" y la de signup cubre justo ese caso. Se cruzaron para no solaparse; fusionarlas reintroduce el solape que sus autores evitaron.


## Diferido con evidencia


## Verificación

| Comprobación | Resultado |
|---|---|
| Aduana | **SUPERADA** · 0 errores críticos |
| Métrica oficial | 712 → **707** skills · 61 → **56** pares · 33 → **29** grupos · 11,24 % → **10,04 %** |
| Ledger | `data/state/f6_lote4_ledger.jsonl` |
