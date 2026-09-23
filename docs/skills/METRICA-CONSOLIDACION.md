# Métrica oficial de consolidación (F6)

| Campo | Valor |
|---|---|
| Documento | `docs/skills/METRICA-CONSOLIDACION.md` |
| Fecha de medición | 2026-09-23 16:11:15-0500 |
| Comando | `python3 scripts/f6_metrica_oficial.py --canon /root/hermes-agent/skills --umbral 0.45` |
| Umbral | **0.45** |
| Método | TF-IDF (sublinear_tf, min_df=1) sobre nombre + descripción + cuerpo; similitud coseno; grupos = componentes conexas |
| Catálogo medido | 707 `SKILL.md` |

## Resultado

| Métrica | Hoy | Referencia 22-sep-2026 |
|---|---|---|
| Pares sobre el umbral | **56** | 85 |
| Grupos (componentes conexas) | **29** | 45 |
| Skills implicadas | **71** | 115 |
| Porcentaje del catálogo | **10.04 %** | 16,0 % |

Objetivo de F6: bajar el porcentaje implicado **sin pérdida de contenido**,
lote por lote, con ledger de hash antes/después por skill.

## Top 25 de pares por similitud

| # | A | B | Similitud |
|---|---|---|---|
| 1 | `specialists/hermes-internal/hermes-bible-study` | `specialists/marketing/hermes-bible` | 0.9994 |
| 2 | `specialists/ai-ml/pytorch-fsdp` | `specialists/ai-ml/unsloth` | 0.6850 |
| 3 | `productivity/colombia-juegos-promocionales` | `specialists/marketing-ads/colombia-promociones-legales` | 0.6354 |
| 4 | `software-development/amazon-sp-api` | `software-development/amazon-spapi-integration` | 0.6221 |
| 5 | `autonomous-ai-agents/sdd-apply` | `autonomous-ai-agents/sdd-tasks` | 0.6136 |
| 6 | `autonomous-ai-agents/sdd-explore` | `autonomous-ai-agents/sdd-propose` | 0.5859 |
| 7 | `autonomous-ai-agents/sdd-propose` | `autonomous-ai-agents/sdd-spec` | 0.5837 |
| 8 | `autonomous-ai-agents/sdd-design` | `autonomous-ai-agents/sdd-explore` | 0.5730 |
| 9 | `autonomous-ai-agents/sdd-design` | `autonomous-ai-agents/sdd-propose` | 0.5489 |
| 10 | `autonomous-ai-agents/sdd-explore` | `autonomous-ai-agents/sdd-init` | 0.5453 |
| 11 | `specialists/marketing/3-statement-model` | `specialists/marketing/lbo-model` | 0.5417 |
| 12 | `autonomous-ai-agents/sdd-design` | `autonomous-ai-agents/sdd-spec` | 0.5415 |
| 13 | `autonomous-ai-agents/sdd-design` | `autonomous-ai-agents/sdd-tasks` | 0.5356 |
| 14 | `autonomous-ai-agents/writing-plans` | `specialists/hermes-internal/plan` | 0.5344 |
| 15 | `specialists/marketing/form-cro` | `specialists/marketing/signup` | 0.5197 |
| 16 | `autonomous-ai-agents/sdd-explore` | `autonomous-ai-agents/sdd-spec` | 0.5158 |
| 17 | `autonomous-ai-agents/sdd-apply` | `autonomous-ai-agents/sdd-verify` | 0.5147 |
| 18 | `specialists/marketing-ads/meta-ads-campaigns` | `specialists/marketing-ads/meta-ads-operations` | 0.5118 |
| 19 | `devops/aws-solution-architect` | `devops/gcp-cloud-architect` | 0.5086 |
| 20 | `specialists/hermes-internal/skill-creator` | `specialists/hermes-internal/skill-improver` | 0.5059 |
| 21 | `specialists/data-vector/pinecone` | `specialists/data-vector/pinecone-research` | 0.5051 |
| 22 | `devops/agent-connection-governance` | `specialists/devops-infra/oauth-connection-door` | 0.5029 |
| 23 | `devops/hermes-specialist-agents-deploy` | `specialists/hermes-internal/hermes-roster-implementation` | 0.4990 |
| 24 | `autonomous-ai-agents/sdd-onboard` | `autonomous-ai-agents/sdd-propose` | 0.4982 |
| 25 | `autonomous-ai-agents/sdd-propose` | `autonomous-ai-agents/sdd-tasks` | 0.4934 |

## Grupos detectados (29)

- **grupo_01** (10): `autonomous-ai-agents/sdd-apply`, `autonomous-ai-agents/sdd-design`, `autonomous-ai-agents/sdd-explore`, `autonomous-ai-agents/sdd-init`, `autonomous-ai-agents/sdd-onboard`, `autonomous-ai-agents/sdd-propose`, `autonomous-ai-agents/sdd-spec`, `autonomous-ai-agents/sdd-tasks`, `autonomous-ai-agents/sdd-verify`, `specialists/general/chained-pr`
- **grupo_02** (4): `software-development/github-code-review`, `software-development/github-issues`, `software-development/github-pr-workflow`, `software-development/github-repo-management`
- **grupo_03** (3): `autonomous-ai-agents/claude-code`, `autonomous-ai-agents/codex`, `specialists/hermes-internal/grok`
- **grupo_04** (3): `specialists/ai-ml/axolotl`, `specialists/ai-ml/pytorch-fsdp`, `specialists/ai-ml/unsloth`
- **grupo_05** (3): `specialists/marketing/marketing-calendar-publishing`, `specialists/marketing/monthly-campaign-calendar-playbook`, `specialists/marketing/social-piece-publishing-ops`
- **grupo_06** (2): `autonomous-ai-agents/writing-plans`, `specialists/hermes-internal/plan`
- **grupo_07** (2): `core/agent-roster-ops`, `core/hermes-fleet-operations`
- **grupo_08** (2): `core/hermes-provider-ops`, `core/vps-deployment-ops`
- **grupo_09** (2): `creative/bot-avatar-config`, `creative/bot-avatar-pipeline`
- **grupo_10** (2): `devops/agent-connection-governance`, `specialists/devops-infra/oauth-connection-door`
- **grupo_11** (2): `devops/aws-solution-architect`, `devops/gcp-cloud-architect`
- **grupo_12** (2): `devops/cloudflare-dns-cutover`, `devops/cloudflare-email-auth-dns`
- **grupo_13** (2): `devops/hermes-specialist-agents-deploy`, `specialists/hermes-internal/hermes-roster-implementation`
- **grupo_14** (2): `productivity/colombia-juegos-promocionales`, `specialists/marketing-ads/colombia-promociones-legales`
- **grupo_15** (2): `productivity/document-reader`, `specialists/hermes-internal/local-vision-toolkit`
- **grupo_16** (2): `productivity/github-push-container`, `productivity/github-ro-mount-workflow`
- **grupo_17** (2): `productivity/specification-handoff`, `software-development/service-agent-code-handoff`
- **grupo_18** (2): `software-development/amazon-sp-api`, `software-development/amazon-spapi-integration`
- **grupo_19** (2): `software-development/hermes-desktop-remote-backend`, `specialists/hermes-internal/hermes-desktop-remote-connection`
- **grupo_20** (2): `software-development/hermes-desktop-ssh-backend`, `specialists/marketing/hermes-vps-home-bind`
- **grupo_21** (2): `specialists/ai-ml/serving-llms-vllm`, `specialists/ai-ml/tensorrt-llm`
- **grupo_22** (2): `specialists/comms/notification-delivery-reliability`, `specialists/marketing/cron-delivery-routing`
- **grupo_23** (2): `specialists/data-vector/pinecone`, `specialists/data-vector/pinecone-research`
- **grupo_24** (2): `specialists/hermes-internal/hermes-bible-study`, `specialists/marketing/hermes-bible`
- **grupo_25** (2): `specialists/hermes-internal/skill-creator`, `specialists/hermes-internal/skill-improver`
- **grupo_26** (2): `specialists/marketing/3-statement-model`, `specialists/marketing/lbo-model`
- **grupo_27** (2): `specialists/marketing/copywriting`, `specialists/marketing/cro`
- **grupo_28** (2): `specialists/marketing/form-cro`, `specialists/marketing/signup`
- **grupo_29** (2): `specialists/marketing-ads/meta-ads-campaigns`, `specialists/marketing-ads/meta-ads-operations`

## Salida cruda

El detalle completo —pares, grupos y el hash sha256 corto de cada skill—
queda en `data/state/f6_metrica.json`, que es la fuente que consumen los
lotes de consolidación y su ledger.
