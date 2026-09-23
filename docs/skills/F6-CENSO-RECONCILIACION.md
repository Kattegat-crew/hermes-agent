# F6 · Reconciliación del censo de auditoría

| Campo | Valor |
|---|---|
| Documento | `docs/skills/F6-CENSO-RECONCILIACION.md` |
| Fecha | 2026-09-23T13:47:35-0500 |
| Fuente | `data/profiles/roshi/workspace/reports/censo-skills-20260920` |
| Comando | `python3 scripts/f6_censo_reconciliacion.py` |
| **Estado** | **medición — no muta nada** |

## El «hueco de 62», explicado

| Métrica | Valor |
|---|---|
| Entradas repartidas en los 8 lotes | **395** |
| Skills **únicas** juzgadas | **333** |
| Consolidados en `plan_limpieza.json` | **333** |
| Auditadas en **más de un lote** | **56** |
| **Hueco real (únicas − consolidadas)** | **0** |

**Conclusión:** la consolidación está **completa** (`333/333`). La diferencia de 62 no era un veredicto perdido: es **doble conteo por diseño de los lotes**.

```
395 entradas  =  333 skills únicas  +  62 entradas repetidas
               (56 skills aparecen en más de un lote:
                51 en dos lotes · 4 en tres lotes · 1 en cuatro)
```

Una skill *vendor* que además no tiene referencias se audita en `A*` y en `B*`; en la población suma dos entradas, pero en el plan de limpieza se consolida una sola vez. La hipótesis anterior —«51 del lote B que nunca volvieron + 11 solapes»— queda **refutada**: los 8 archivos de veredicto existen y los 333 destinos únicos están en el plan. **No hay veredicto perdido.**

## Por lote

| Lote | Entradas | Veredictos |
|---|---|---|
| `A1_vendor` | 53 | 53 |
| `A2_vendor` | 52 | 52 |
| `B1_sin_referencias` | 54 | 54 |
| `B2_sin_referencias` | 54 | 54 |
| `B3_sin_referencias` | 54 | 54 |
| `B4_sin_referencias` | 52 | 52 |
| `C_grandes` | 30 | 30 |
| `D_casi_duplicados` | 46 | 46 |

## Las 56 skills auditadas en más de un lote

| Skill | Lotes | Estado hoy |
|---|---|---|
| `autonomous-ai-agents/hermes-agent` | A2_vendor, C_grandes | en el canon |
| `autonomous-ai-agents/system-onboarding` | B3_sin_referencias, D_casi_duplicados | en el canon |
| `core/brain-knowledge-ops` | B3_sin_referencias, C_grandes, D_casi_duplicados | en el canon |
| `core/github-workflow` | B3_sin_referencias, D_casi_duplicados | en el canon |
| `core/google-workspace-ops` | B3_sin_referencias, C_grandes, D_casi_duplicados | en el canon |
| `core/hermes-desktop-ops` | B3_sin_referencias, D_casi_duplicados | en el canon |
| `core/hermes-runtime-ops` | B3_sin_referencias, C_grandes | en el canon |
| `core/meta-ads-ops` | A2_vendor, B3_sin_referencias | en el canon |
| `core/oauth-connection-ops` | B3_sin_referencias, D_casi_duplicados | en el canon |
| `core/skill-library-ops` | B3_sin_referencias, C_grandes | en el canon |
| `core/video-reel-pipeline` | C_grandes, D_casi_duplicados | en el canon |
| `creative/openai-automation` | A2_vendor, B3_sin_referencias | en el canon |
| `creative/popular-web-designs` | A2_vendor, C_grandes | en el canon |
| `creative/unreal-mcp` | A2_vendor, B3_sin_referencias | en el canon |
| `devops/nix-best-practices` | B1_sin_referencias, D_casi_duplicados | en el canon |
| `devops/open-design-deployment` | A1_vendor, B1_sin_referencias | en el canon |
| `productivity/oauth-multi-tenant-integration` | B4_sin_referencias, D_casi_duplicados | en el canon |
| `productivity/oauth-multi-tenant-integrations` | B4_sin_referencias, D_casi_duplicados | en el canon |
| `productivity/specification-handoff` | A2_vendor, B4_sin_referencias | en el canon |
| `productivity/writing-skills` | A2_vendor, C_grandes | en el canon |
| `research/parallel-cli` | A2_vendor, B4_sin_referencias | en el canon |
| `software-development/amazon-sp-api` | B4_sin_referencias, D_casi_duplicados | en el canon |
| `software-development/ast-grep` | B4_sin_referencias, C_grandes | en el canon |
| `software-development/git-best-practices` | B4_sin_referencias, D_casi_duplicados | en el canon |
| `software-development/go-best-practices` | A2_vendor, D_casi_duplicados | en el canon |
| `software-development/googlebigquery-automation` | A2_vendor, B4_sin_referencias | en el canon |
| `software-development/onesignal_rest_api-automation` | A2_vendor, B4_sin_referencias | en el canon |
| `software-development/react-best-practices` | A2_vendor, D_casi_duplicados | en el canon |
| `software-development/service-agent-code-handoff` | A2_vendor, B4_sin_referencias | en el canon |
| `software-development/spec-best-practices` | B4_sin_referencias, D_casi_duplicados | en el canon |
| `software-development/zig-best-practices` | A2_vendor, D_casi_duplicados | en el canon |
| `specialists/ai-ml/dspy` | A1_vendor, B1_sin_referencias | en el canon |
| `specialists/ai-ml/pytorch-fsdp` | B1_sin_referencias, C_grandes | en el canon |
| `specialists/ai-ml/saelens` | A1_vendor, B1_sin_referencias | en el canon |
| `specialists/data-vector/rag-architecture-expert` | A1_vendor, D_casi_duplicados | en el canon |
| `specialists/devops-infra/oauth-connection-door` | B2_sin_referencias, D_casi_duplicados | en el canon |
| `specialists/general/creative-ideation` | B2_sin_referencias, C_grandes | en el canon |
| `specialists/general/gitnexus-explorer` | A2_vendor, B2_sin_referencias | en el canon |
| `specialists/hermes-internal/darwinian-evolver` | A1_vendor, B2_sin_referencias | en el canon |
| `specialists/hermes-internal/hermes-bible-study` | A1_vendor, B1_sin_referencias, C_grandes, D_casi_duplicados | en el canon |
| `specialists/hermes-internal/kanban-video-orchestrator` | B1_sin_referencias, C_grandes | en el canon |
| `specialists/hermes-internal/openclaw-migration` | B1_sin_referencias, C_grandes | en el canon |
| `specialists/hermes-internal/openhands` | A1_vendor, B1_sin_referencias | en el canon |
| `specialists/hermes-internal/page-agent` | A1_vendor, B1_sin_referencias | en el canon |
| `specialists/marketing/amazon-sp-api-listings` | B2_sin_referencias, D_casi_duplicados | en el canon |
| `specialists/marketing/apollo-automation` | A1_vendor, B2_sin_referencias | en el canon |
| `specialists/marketing/cron-runtime-verification` | A1_vendor, D_casi_duplicados | en el canon |
| `specialists/marketing/facebook-automation` | A1_vendor, B2_sin_referencias | en el canon |
| `specialists/marketing/googleads-automation` | A1_vendor, B2_sin_referencias | en el canon |
| `specialists/marketing/hermes-bible` | A1_vendor, C_grandes, D_casi_duplicados | en el canon |
| `specialists/marketing/hermes-cron-runtime-verification` | A1_vendor, D_casi_duplicados | en el canon |
| `specialists/marketing/merger-model` | A1_vendor, B2_sin_referencias | en el canon |
| `specialists/marketing/microsoft-clarity-automation` | A1_vendor, B2_sin_referencias | en el canon |
| `specialists/media-video/baoyu-article-illustrator` | B2_sin_referencias, C_grandes | en el canon |
| `specialists/monitoring-security/godmode` | A1_vendor, B1_sin_referencias, C_grandes | en el canon |
| `specialists/monitoring-security/unbroker` | B1_sin_referencias, C_grandes | en el canon |

## Lectura

Este documento cierra el punto D1 del expediente: el hueco deja de ser una
cifra declarada y pasa a ser una lista medida con su causa. **No se toca el
catálogo**: la consolidación de solapamientos entra en los lotes de F6 con
su firma y su ledger.
