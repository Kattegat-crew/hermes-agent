# Métrica oficial de consolidación (F6)

| Campo | Valor |
|---|---|
| Documento | `docs/skills/METRICA-CONSOLIDACION.md` |
| Fecha de medición | 2026-09-23 15:12:18-0500 |
| Comando | `python3 scripts/f6_metrica_oficial.py --canon /root/hermes-agent/skills --umbral 0.45` |
| Umbral | **0.45** |
| Método | TF-IDF (sublinear_tf, min_df=1) sobre nombre + descripción + cuerpo; similitud coseno; grupos = componentes conexas |
| Catálogo medido | 716 `SKILL.md` |

## Resultado

| Métrica | Hoy | Referencia 22-sep-2026 |
|---|---|---|
| Pares sobre el umbral | **66** | 85 |
| Grupos (componentes conexas) | **37** | 45 |
| Skills implicadas | **89** | 115 |
| Porcentaje del catálogo | **12.43 %** | 16,0 % |

Objetivo de F6: bajar el porcentaje implicado **sin pérdida de contenido**,
lote por lote, con ledger de hash antes/después por skill.

## Top 25 de pares por similitud

| # | A | B | Similitud |
|---|---|---|---|
| 1 | `specialists/hermes-internal/hermes-bible-study` | `specialists/marketing/hermes-bible` | 0.9994 |
| 2 | `creative/social-content` | `specialists/marketing/social` | 0.7729 |
| 3 | `software-development/hermes-desktop-ssh-backend` | `software-development/hermes-desktop-ssh-diagnostico` | 0.7261 |
| 4 | `specialists/ai-ml/pytorch-fsdp` | `specialists/ai-ml/unsloth` | 0.6848 |
| 5 | `specialists/marketing/ads` | `specialists/marketing/paid-ads` | 0.6462 |
| 6 | `productivity/colombia-juegos-promocionales` | `specialists/marketing-ads/colombia-promociones-legales` | 0.6353 |
| 7 | `software-development/amazon-sp-api` | `software-development/amazon-spapi-integration` | 0.6220 |
| 8 | `devops/open-design-deployment` | `devops/open-design-selfhost-ops` | 0.6154 |
| 9 | `autonomous-ai-agents/sdd-apply` | `autonomous-ai-agents/sdd-tasks` | 0.6135 |
| 10 | `creative/bot-avatar-config` | `creative/neuralcrew-bot-avatars` | 0.5867 |
| 11 | `autonomous-ai-agents/sdd-explore` | `autonomous-ai-agents/sdd-propose` | 0.5857 |
| 12 | `autonomous-ai-agents/sdd-propose` | `autonomous-ai-agents/sdd-spec` | 0.5838 |
| 13 | `autonomous-ai-agents/sdd-design` | `autonomous-ai-agents/sdd-explore` | 0.5729 |
| 14 | `specialists/hermes-internal/hermes-desktop-windows-troubleshooting` | `specialists/hermes-internal/hermes-windows-install` | 0.5727 |
| 15 | `specialists/hermes-internal/client-agent-onboarding` | `specialists/hermes-internal/client-agent-soul-survey` | 0.5497 |
| 16 | `autonomous-ai-agents/sdd-design` | `autonomous-ai-agents/sdd-propose` | 0.5488 |
| 17 | `autonomous-ai-agents/sdd-explore` | `autonomous-ai-agents/sdd-init` | 0.5451 |
| 18 | `specialists/marketing/3-statement-model` | `specialists/marketing/lbo-model` | 0.5417 |
| 19 | `autonomous-ai-agents/sdd-design` | `autonomous-ai-agents/sdd-spec` | 0.5414 |
| 20 | `autonomous-ai-agents/sdd-design` | `autonomous-ai-agents/sdd-tasks` | 0.5355 |
| 21 | `autonomous-ai-agents/writing-plans` | `specialists/hermes-internal/plan` | 0.5346 |
| 22 | `specialists/hermes-internal/hermes-provider-fallback` | `specialists/hermes-internal/hermes-provider-resilience` | 0.5277 |
| 23 | `specialists/hermes-internal/hermes-desktop-remote-gateway` | `specialists/hermes-internal/hermes-desktop-remote-setup` | 0.5217 |
| 24 | `specialists/marketing/form-cro` | `specialists/marketing/signup` | 0.5199 |
| 25 | `autonomous-ai-agents/sdd-explore` | `autonomous-ai-agents/sdd-spec` | 0.5157 |

## Grupos detectados (37)

- **grupo_01** (10): `autonomous-ai-agents/sdd-apply`, `autonomous-ai-agents/sdd-design`, `autonomous-ai-agents/sdd-explore`, `autonomous-ai-agents/sdd-init`, `autonomous-ai-agents/sdd-onboard`, `autonomous-ai-agents/sdd-propose`, `autonomous-ai-agents/sdd-spec`, `autonomous-ai-agents/sdd-tasks`, `autonomous-ai-agents/sdd-verify`, `specialists/general/chained-pr`
- **grupo_02** (4): `software-development/github-code-review`, `software-development/github-issues`, `software-development/github-pr-workflow`, `software-development/github-repo-management`
- **grupo_03** (3): `autonomous-ai-agents/claude-code`, `autonomous-ai-agents/codex`, `specialists/hermes-internal/grok`
- **grupo_04** (3): `creative/bot-avatar-config`, `creative/bot-avatar-pipeline`, `creative/neuralcrew-bot-avatars`
- **grupo_05** (3): `software-development/hermes-desktop-ssh-backend`, `software-development/hermes-desktop-ssh-diagnostico`, `specialists/marketing/hermes-vps-home-bind`
- **grupo_06** (3): `specialists/ai-ml/axolotl`, `specialists/ai-ml/pytorch-fsdp`, `specialists/ai-ml/unsloth`
- **grupo_07** (3): `specialists/marketing/marketing-calendar-publishing`, `specialists/marketing/monthly-campaign-calendar-playbook`, `specialists/marketing/social-piece-publishing-ops`
- **grupo_08** (2): `autonomous-ai-agents/writing-plans`, `specialists/hermes-internal/plan`
- **grupo_09** (2): `core/agent-roster-ops`, `core/hermes-fleet-operations`
- **grupo_10** (2): `core/hermes-provider-ops`, `core/vps-deployment-ops`
- **grupo_11** (2): `creative/social-content`, `specialists/marketing/social`
- **grupo_12** (2): `devops/agent-connection-governance`, `specialists/devops-infra/oauth-connection-door`
- **grupo_13** (2): `devops/aws-solution-architect`, `devops/gcp-cloud-architect`
- **grupo_14** (2): `devops/cloudflare-dns-cutover`, `devops/cloudflare-email-auth-dns`
- **grupo_15** (2): `devops/hermes-specialist-agents-deploy`, `specialists/hermes-internal/hermes-roster-implementation`
- **grupo_16** (2): `devops/open-design-deployment`, `devops/open-design-selfhost-ops`
- **grupo_17** (2): `productivity/colombia-juegos-promocionales`, `specialists/marketing-ads/colombia-promociones-legales`
- **grupo_18** (2): `productivity/document-reader`, `specialists/hermes-internal/local-vision-toolkit`
- **grupo_19** (2): `productivity/github-push-container`, `productivity/github-ro-mount-workflow`
- **grupo_20** (2): `productivity/specification-handoff`, `software-development/service-agent-code-handoff`
- **grupo_21** (2): `software-development/amazon-sp-api`, `software-development/amazon-spapi-integration`
- **grupo_22** (2): `software-development/hermes-desktop-remote-backend`, `specialists/hermes-internal/hermes-desktop-remote-connection`
- **grupo_23** (2): `specialists/ai-ml/accelerate`, `specialists/ai-ml/pytorch-lightning`
- **grupo_24** (2): `specialists/ai-ml/serving-llms-vllm`, `specialists/ai-ml/tensorrt-llm`
- **grupo_25** (2): `specialists/comms/notification-delivery-reliability`, `specialists/marketing/cron-delivery-routing`
- **grupo_26** (2): `specialists/data-vector/pinecone`, `specialists/data-vector/pinecone-research`
- **grupo_27** (2): `specialists/hermes-internal/client-agent-onboarding`, `specialists/hermes-internal/client-agent-soul-survey`
- **grupo_28** (2): `specialists/hermes-internal/hermes-bible-study`, `specialists/marketing/hermes-bible`
- **grupo_29** (2): `specialists/hermes-internal/hermes-desktop-remote-gateway`, `specialists/hermes-internal/hermes-desktop-remote-setup`
- **grupo_30** (2): `specialists/hermes-internal/hermes-desktop-windows-troubleshooting`, `specialists/hermes-internal/hermes-windows-install`
- **grupo_31** (2): `specialists/hermes-internal/hermes-provider-fallback`, `specialists/hermes-internal/hermes-provider-resilience`
- **grupo_32** (2): `specialists/hermes-internal/skill-creator`, `specialists/hermes-internal/skill-improver`
- **grupo_33** (2): `specialists/marketing/3-statement-model`, `specialists/marketing/lbo-model`
- **grupo_34** (2): `specialists/marketing/ads`, `specialists/marketing/paid-ads`
- **grupo_35** (2): `specialists/marketing/copywriting`, `specialists/marketing/cro`
- **grupo_36** (2): `specialists/marketing/form-cro`, `specialists/marketing/signup`
- **grupo_37** (2): `specialists/marketing-ads/meta-ads-campaigns`, `specialists/marketing-ads/meta-ads-operations`

## Salida cruda

El detalle completo —pares, grupos y el hash sha256 corto de cada skill—
queda en `data/state/f6_metrica.json`, que es la fuente que consumen los
lotes de consolidación y su ledger.
