# Censo editorial del canon de skills — informe final

**Autor:** Roshi (Ermitaño Tortuga) — asistente técnico de Jesús Díaz (CTO)
**Ejecutado:** 2026-09-24 (-05) · **Método:** 42 lotes + 4 del piloto + 1 barrido, con rúbrica única y cita obligatoria
**Estado:** análisis completo. **Nada mutado por este censo** (las mutaciones F7/F8 son actas aparte).

## 1. Cobertura y calidad

- **707 veredictos válidos sobre las 707 skills del canon = 100,0 % de cobertura**
- **0 huérfanos** (todo veredicto mapea a una skill real del canon)
- **0 veredictos sin cita textual** — la regla dura se cumplió sin una sola excepción
- **0 veredictos con campos faltantes**

## 2. Hallazgo principal: el canon NO está sobredimensionado, está subdescrito

| Recomendación | N | % |
|---|---:|---:|
| conservar | 432 | 61.1 % |
| reescribir-descripcion | 233 | 33.0 % |
| fusionar-en | 39 | 5.5 % |
| retirar | 3 | 0.4 % |

**Solo **42 de 707** skills (5.9 %) se proponen para fusión o retiro.
En cambio, **233** (33.0 %) solo necesitan una descripción que un retriever pueda encontrar.

## 3. Valor y naturaleza del contenido

| Valor | N | | Tipo de contenido | N |
|---|---:|---|---|---:|
| alto | 359 | | procedimiento | 557 |
| medio | 298 | | referencia | 64 |
| bajo | 47 | | paraguas | 47 |
| nulo | 3 | | prosa | 28 |
|  |  | | stub | 11 |

- **657 de 707 (92.9 %) con valor alto o medio.**
- **557 (78.8 %) son procedimiento real**, no prosa.
- Solo **11 stubs** y **3 con valor nulo** en todo el canon.

## 4. Las 42 propuestas de fusión o retiro

| # | Skill | Propuesta | Riesgo | Conf. |
|---:|---|---|---|---:|
| 1 | `oauth-connection-health-audit` | fusionar-en:activepieces-google-access | bajo | 0.8 |
| 2 | `docker-container-optimization` | retirar | bajo | 0.85 |
| 3 | `notion-integration` | fusionar-en:notion | bajo | 0.75 |
| 4 | `github-auth` | fusionar-en:github | medio | 0.8 |
| 5 | `github-pr-workflow` | fusionar-en:github | bajo | 0.8 |
| 6 | `github-code-review` | fusionar-en:github | bajo | 0.8 |
| 7 | `github-issues` | fusionar-en:github | bajo | 0.8 |
| 8 | `github-repo-management` | fusionar-en:github | bajo | 0.8 |
| 9 | `executing-plans` | fusionar-en:subagent-driven-development | bajo | 0.72 |
| 10 | `brain-graph-operations` | fusionar-en:brain-knowledge-ops | medio | 0.65 |
| 11 | `pptx-author` | fusionar-en:powerpoint | bajo | 0.6 |
| 12 | `web-performance-core-vitals` | fusionar-en:mobile-landing-optimization | bajo | 0.6 |
| 13 | `agent-roster-design` | fusionar-en:agent-roster-blueprint | medio | 0.6 |
| 14 | `content-performance-analytics` | fusionar-en:campaign-content-intelligence | medio | 0.7 |
| 15 | `skill-navigator` | fusionar-en:graphify | bajo | 0.66 |
| 16 | `ai-video-pricing-research` | fusionar-en:ai-video-model-costing | bajo | 0.68 |
| 17 | `campaign-content-intelligence` | fusionar-en:content-performance-analytics | medio | 0.66 |
| 18 | `vscode-ai-extension-configuration` | fusionar-en:external-openai-client-config | bajo | 0.6 |
| 19 | `finance-lead` | fusionar-en:specialists/marketing/cfo-advisor | bajo | 0.55 |
| 20 | `googleads-automation` | fusionar-en:rube-mcp-api-automation | bajo | 0.75 |
| 21 | `hermes-vps-home-bind` | fusionar-en:hermes-desktop-ssh-backend | bajo | 0.8 |
| 22 | `pipelines-con-gate-humano` | fusionar-en:flujos-con-gates-humanos | medio | 0.8 |
| 23 | `revenue-operations` | fusionar-en:revops | medio | 0.6 |
| 24 | `informes-ventas-cliente` | fusionar-en:informe-mensual-sheet-pdf | medio | 0.7 |
| 25 | `amazon-sp-api` | fusionar-en:amazon-spapi-integration | medio | 0.82 |
| 26 | `debugging-and-error-recovery` | fusionar-en:systematic-debugging | medio | 0.72 |
| 27 | `clean-architecture-patterns` | fusionar-en:domain-driven-design | bajo | 0.62 |
| 28 | `cs-product-analyst` | fusionar-en:product-analytics | bajo | 0.65 |
| 29 | `googlebigquery-automation` | fusionar-en:rube-mcp-api-automation | bajo | 0.8 |
| 30 | `google-oauth-reauth` | retirar | bajo | 0.88 |
| 31 | `activepieces-db-surgery` | fusionar-en:activepieces-flow-editing | medio | 0.6 |
| 32 | `bot-avatar-pipeline` | fusionar-en:bot-avatar-config | medio | 0.7 |
| 33 | `keyframe-script-qa` | fusionar-en:scene-keyframe-qa-lipsync | medio | 0.65 |
| 34 | `lucky-reel-voice-script` | fusionar-en:reel-voice-lipsync | medio | 0.6 |
| 35 | `poster-composition` | fusionar-en:campaign-poster-compositing | bajo | 0.7 |
| 36 | `baoyu-post-to-x` | retirar | medio | 0.6 |
| 37 | `service-agent-code-handoff` | fusionar-en:productivity/specification-handoff | bajo | 0.75 |
| 38 | `e2e` | fusionar-en:testing-best-practices | bajo | 0.65 |
| 39 | `telegram-channel-archaeology` | fusionar-en:locate-shared-resource | bajo | 0.72 |
| 40 | `web-content-extraction` | fusionar-en:embedded-payload-extraction | bajo | 0.62 |
| 41 | `youtube-content` | fusionar-en:youtube-full | medio | 0.6 |
| 42 | `blogwatcher` | fusionar-en:watchers | medio | 0.6 |

### Detalle con evidencia

**1. `oauth-connection-health-audit`** → fusionar-en:activepieces-google-access · riesgo bajo · conf 0.8
   - Es el skill mas corto del cluster y su contenido (fuentes de credenciales, prueba de refresh contra Google, reconexion) esta duplicado en activepieces-google-access/activepieces-connection-api; solo aporta el script verify_ap_refresh_tokens.py, que debe moverse junto con la fusion.
   - *Evidencia:* `El token local `google_token.json` esta REVOCADO. **NO re-autenticar token local.**`

**2. `docker-container-optimization`** → retirar · riesgo bajo · conf 0.85
   - Cinco bullets genericos (multi-stage, distroless/alpine, USER no-root, cache de capas, HEALTHCHECK) sin un solo comando, ruta o dato del stack de la agencia; es conocimiento que el modelo ya tiene y no aporta al retriever ni al canon.
   - *Evidencia:* `1. **Multi-Stage Builds**: Separate build tools and dependencies from runtime artifacts.`

**3. `notion-integration`** → fusionar-en:notion · riesgo bajo · conf 0.75
   - Solapa en sustancia con `notion` (search, leer blocks, crear página/DB, paginación) pero usa API vieja (2022-06-28). Su contenido único (bug de query de DB, estructura Notion de la agencia, script de sync wiki) es absorbible en `notion` sin pérdida.
   - *Evidencia:* `The `GET /v1/databases/{id}/query` endpoint can silently return 0 results even when pages exist in the database.`

**4. `github-auth`** → fusionar-en:github · riesgo medio · conf 0.8
   - Su contenido vive ya completo en github/references/auth.md del paraguas (mismas líneas, mismos scripts), así que mantenerlo duplica la entrada en el índice.
   - *Evidencia:* `This skill sets up authentication so the agent can work with GitHub repositories, PRs, issues, and CI.`

**5. `github-pr-workflow`** → fusionar-en:github · riesgo bajo · conf 0.8
   - Ciclo de PR completo ya presente como github/references/pr-workflow.md; duplicar la entrada solo repite resultados en el retriever.
   - *Evidencia:* `Complete guide for managing the PR lifecycle. Each section shows the `gh` way first, then the `git` + `curl` fallback for machines without `gh`.`

**6. `github-code-review`** → fusionar-en:github · riesgo bajo · conf 0.8
   - El flujo de review (diff local, comentarios inline, review atómico) ya vive completo en github/references/code-review.md.
   - *Evidencia:* `Perform code reviews on local changes before pushing, or review open PRs on GitHub.`

**7. `github-issues`** → fusionar-en:github · riesgo bajo · conf 0.8
   - Gestión de issues (crear, triar, etiquetar, cerrar, bulk) ya está completa en github/references/issues.md.
   - *Evidencia:* `Create, search, triage, and manage GitHub issues. Each section shows `gh` first, then the `curl` fallback.`

**8. `github-repo-management`** → fusionar-en:github · riesgo bajo · conf 0.8
   - Creación/clonado/fork/releases/secrets de repos ya completo en github/references/repo-management.md.
   - *Evidencia:* `Create, clone, fork, configure, and manage GitHub repositories. Each section shows `gh` first, then the `git` + `curl` fallback.`

**9. `executing-plans`** → fusionar-en:subagent-driven-development · riesgo bajo · conf 0.72
   - El propio texto se declara el fallback inferior de subagent-driven-development y su contenido (64 lineas) cabe como seccion de fallback en el skill principal sin perdida.
   - *Evidencia:* `If subagents are available, use superpowers:subagent-driven-development instead of this skill.`

**10. `brain-graph-operations`** → fusionar-en:brain-knowledge-ops · riesgo medio · conf 0.65
   - core/brain-knowledge-ops ya contiene una copia byte a byte de este SKILL.md y lo declara flujo centralizado: hay duplicación real, no solo puntero. La fusión debe arrastrar references/brain-graph-maintenance.md, que hoy existe SOLO en esta copia y no está en el umbrella.
   - *Evidencia:* `el grafo cae a 10.232 nodos | merge leyendo y escribiendo el MISMO path | `merge-graphs … --out <tercer archivo>` y luego `mv``

**11. `pptx-author`** → fusionar-en:powerpoint · riesgo bajo · conf 0.6
   - Es una variante ligera que la propia skill reconoce como subconjunto de `powerpoint` (create/read/edit con python-pptx y decks con plantilla de marca); lo único irrepetible (traza de cada cifra a la celda del workbook, checklist de pitch deck financiero) no aplica al negocio de la agencia y cabe como sección en `powerpoint`.
   - *Evidencia:* `Every number traces to the model ... Never transcribe numbers from memory or from a summary — open the workbook, read the named range, and bind the deck value to it programmatically when you can.`

**12. `web-performance-core-vitals`** → fusionar-en:mobile-landing-optimization · riesgo bajo · conf 0.6
   - Stub de 21 líneas con checklist genérica y umbrales que contradicen/duplican los de mobile-landing-optimization (mismo LCP y CLS medidos con targets distintos), sin nada propio de la casa; como sección de la skill de landings suman y se elimina la ambigüedad de ruteo.
   - *Evidencia:* `## Target Metrics
- **LCP (Largest Contentful Paint)**: < 2.5s
- **INP (Interaction to Next Paint)**: < 200ms`

**13. `agent-roster-design`** → fusionar-en:agent-roster-blueprint · riesgo medio · conf 0.6
   - Los tres bloques de esta skill (identidad/nombres, catálogos de skills, entrega) coinciden con los pasos 4-5-7 del blueprint, que además cubre el plan técnico y el registro; la fusión debe arrastrar el bloque de arquetipos/SOUL/avatares y `references/neuralcrew-8-especialistas-2026-08.md`.
   - *Evidencia:* `**"N skills" significa POR AGENTE, no en total.** ... ante "robustece", ampliar al máximo espectro`

**14. `content-performance-analytics`** → fusionar-en:campaign-content-intelligence · riesgo medio · conf 0.7
   - Tercera descripcion del mismo sistema (reel final + Composio + benchmark n>=10): el canon ya apunta a campaign-content-intelligence via core/campaign-ops y a reel-performance-analytics via core/video-reel-pipeline, dejando a esta sin umbrella; la fusion debe arrastrar el detalle de implementacion (pipeline.py, cron 1de9d6aa3d90, publicacion a wiki).
   - *Evidencia:* `- **IG insights el campo es `ig_media_id`, NO `media_id`** (`media_id` -> error de validacion "Unknown key media_id").`

**15. `skill-navigator`** → fusionar-en:graphify · riesgo bajo · conf 0.66
   - Su procedimiento apunta a un canon ajeno y obsoleto: vive en /root/.config/opencode/skills (ruta inexistente/acceso denegado), habla de "312 skills" cuando el canon tiene 707, y duplica los comandos de grafo que ya posee research/graphify, cuya ruta canónica es /opt/data/brain/graphify-out/graph.json. Fusionar conservando las 13 categorías de dominio como taxonomía de entrada del grafo.
   - *Evidencia:* `"Inspect `/root/.config/opencode/skills/SKILLS_INDEX.md` to identify the relevant technical domain" · "When unsure which of the 312 skills are best suited for the current task."`

**16. `ai-video-pricing-research`** → fusionar-en:ai-video-model-costing · riesgo bajo · conf 0.68
   - Dos skills responden la misma pregunta ('cuánto cuesta un clip de 6s y qué ruta conviene') con la misma disciplina de re-verificación y hojas de precio solapadas de agosto 2026; model-costing tiene además marco de decisión por nivel y default de producción, por lo que es el destino natural. Al fusionar hay que trasladar el método de extracción fal.ai/Replicate por curl (no existe en el destino) y 
   - *Evidencia:* `"Regla de oro: sacar el precio del sitio, no de memoria" · "NO usar cifras recordadas ni adivinadas como \"verificadas\": obtener el chip/billing de la página oficial con curl" · destino: "| **Hailuo-`

**17. `campaign-content-intelligence`** → fusionar-en:content-performance-analytics · riesgo medio · conf 0.66
   - Describe en prosa el mismo sistema que content-performance-analytics documenta con módulos y CLI (content-intel/: registry.py, features.py, harvest.py, analyze.py, pipeline.py), con idéntica unidad de análisis y clave de unión. La fusión debe preservar lo único de aquí: los 4 ejes medidos, la asignación de dueños (Freyja/Heimdall), el render por colección wiki del cliente y el playbook de renombre
   - *Evidencia:* `"Golden rule — the analysis unit is the FINAL PUBLISHED REEL ... The platform media_id is the join key." · destino: "JSONL `data/posts.jsonl`, idempotente por (platform, media_id)"`

**18. `vscode-ai-extension-configuration`** → fusionar-en:external-openai-client-config · riesgo bajo · conf 0.6
   - Ambas ensenan a apuntar un cliente externo (no-Hermes) a un endpoint OpenAI-compatible; la de VSCode es el caso Continue.dev dentro del alcance generico que ya declara la skill paraguas.
   - *Evidencia:* `**Use `config.json`, NOT `config.ts`**: TypeScript config (`config.ts`) requires compilation and can fail silently.`

**19. `finance-lead`** → fusionar-en:specialists/marketing/cfo-advisor · riesgo bajo · conf 0.55
   - Persona CFO en prosa con comandos /finance:* que cubre exactamente los mismos temas que cfo-advisor (fundraising, burn, unit economics, board), pero sin tablas de metricas ni red flags; su contenido cabe en las secciones de cfo-advisor.
   - *Evidencia:* `Startup CFO who builds models that survive contact with reality. Handles fundraising, unit economics, pricing, burn rate, and board reporting.`

**20. `googleads-automation`** → fusionar-en:rube-mcp-api-automation · riesgo bajo · conf 0.75
   - Es un caso por proveedor de la misma tecnica Rube MCP/Composio, y el paraguas ya absorbio su hermano metaads-automation como references/. Ademas su contenido real es GA4, no la API de Google Ads.
   - *Evidencia:* `> **Note**: Google Ads data is accessed through the Google Analytics toolkit integration.`

**21. `hermes-vps-home-bind`** → fusionar-en:hermes-desktop-ssh-backend · riesgo bajo · conf 0.8
   - Todo su cuerpo (bindear HERMES_HOME por PermitUserEnvironment + verificacion) es la Capa 2 integra de hermes-desktop-ssh-backend, con los mismos comandos; su unica referencia apunta al archivo de ese otro skill, que ella misma no contiene.
   - *Evidencia:* `- `references/caso-2026-08-20.md` (skill `hermes-desktop-ssh-backend`).`

**22. `pipelines-con-gate-humano`** → fusionar-en:flujos-con-gates-humanos · riesgo medio · conf 0.8
   - Ambas son la misma clase (el freno vive en el codigo, 2 vueltas por etapa, firma `--por NOMBRE`, prueba de genericidad, no-aprobado/) y citan las mismas dos correcciones de Yisus del 12-sep-2026. Al fusionar hay que arrastrar su unico activo exclusivo, references/auditoria-de-genericidad.md.
   - *Evidencia:* `**El freno se implementa, no se promete.**`

**23. `revenue-operations`** → fusionar-en:revops · riesgo medio · conf 0.6
   - Comparte dominio y formulas con revops (coverage ratio 3-4x, velocidad de pipeline, CAC/LTV:CAC) y solo aporta en exclusiva las metricas cuantitativas de forecast y GTM (MAPE, Magic Number, Rule of 40); sus scripts no existen en disco, asi que no se pierde nada ejecutable al concentrarlas en revops.
   - *Evidencia:* `⚠️ FALTA: references/revops-metrics-guide.md`

**24. `informes-ventas-cliente`** → fusionar-en:informe-mensual-sheet-pdf · riesgo medio · conf 0.7
   - Ambas describen la misma pipeline (correos KASSIUSS → historico.jsonl → Sheet con formato → PDF membretado) del mismo cliente; el destino ya cubre captura, cron, publicacion Drive y entrega multi-perfil, asi que basta portarle las secciones unicas (layout de graficas, gate de reviewer) para no perder contenido.
   - *Evidencia:* `Pipeline de clase para el informe mensual de ventas de un cliente (casino Golden es la instancia viva): correos fuente → parser → históricos → hoja de Google con formato real → PDF horizontal membrete`

**25. `amazon-sp-api`** → fusionar-en:amazon-spapi-integration · riesgo medio · conf 0.82
   - Duplica casi todo el dominio SP-API de amazon-spapi-integration (SPP, AU=Far East, trampa orgID, roles, diagnostico 403); fusionar preservando sus assets unicos (tabla de endpoints, production-app-activation.md, test_region_tokens.py) evita dos fuentes de verdad del mismo flujo verificado.
   - *Evidencia:* `**⚠️ AUSTRALIA = FAR EAST (fe), NO Europa — VERIFICADO 18/08/2026**`

**26. `debugging-and-error-recovery`** → fusionar-en:systematic-debugging · riesgo medio · conf 0.72
   - Ensenia la misma ley que systematic-debugging (root cause antes del fix, no adivinar, no saltarse el test rojo); su valor unico (arboles de triage por tipo de error, fallbacks seguros, error-output como dato no confiable) cabe como secciones de systematic-debugging sin perdida.
   - *Evidencia:* `Guessing wastes time. The triage checklist works for test failures, build errors, runtime bugs, and production incidents.`

**27. `clean-architecture-patterns`** → fusionar-en:domain-driven-design · riesgo bajo · conf 0.62
   - Stub de 16 lineas (4 capas + regla de dependencia) sin references ni scripts; el mismo eje Clean/Hexagonal ya esta cubierto por domain-driven-design y por el perfil backend-clean-ddd-cqrs de code-review-and-quality, asi que fusionarlo no pierde nada.
   - *Evidencia:* `## Layers & Dependency Inversion
1. **Domain Layer (Core)**: Entities, Value Objects, Domain Services, and Domain Events. ZERO external dependencies.`

**28. `cs-product-analyst`** → fusionar-en:product-analytics · riesgo bajo · conf 0.65
   - Es una definicion de agente mal ubicada en software-development: define workflows que product-analytics ya implementa, y 6 referencias de contenido estan marcadas como FALTA (/product-team/... inexistente). El contenido unico es el encuadre de agente, absorbible en 3 lineas.
   - *Evidencia:* `**Path:** `../../product-team/skills/product-analytics/scripts/metrics_calculator.py``

**29. `googlebigquery-automation`** → fusionar-en:rube-mcp-api-automation · riesgo bajo · conf 0.8
   - Es una instancia proveedor (toolkit metabase) de la clase que rube-mcp-api-automation ya declara como paraguas: mismos prerequisites, mismo setup y mismo patron de trabajo, sin logica propia fuera del catalogo de tools. Absorbible como references/metabase.md sin perder contenido.
   - *Evidencia:* `Always call `RUBE_SEARCH_TOOLS` first to get current tool schemas`

**30. `google-oauth-reauth`** → retirar · riesgo bajo · conf 0.88
   - La propia skill se declara obsoleta y revocada ('Esta skill está OBSOLETA. El token local `google_token.json` está revocado.') y delega todo en activepieces-google-access, ya existente en el catalogo. No hay procedimiento vivo que perder; solo el script scripts/reauth_google_token.py, atado a un token muerto.
   - *Evidencia:* `**Esta skill está OBSOLETA.** El token local `google_token.json` está revocado.`

**31. `activepieces-db-surgery`** → fusionar-en:activepieces-flow-editing · riesgo medio · conf 0.6
   - Mismo procedimiento (escribir flow_version/trigger en el Postgres de AP self-hosted) partido en dos skills. Lo unico exclusivo de esta — generacion de IDs base62 varchar(21), NOT NULL array vs jsonb de flow_version, pitfall notes={} que crashea la UI y la receta de quoting docker→ssh→bash→psql — debe conservarse integro al fusionar en activepieces-flow-editing.
   - *Evidencia:* `**NO usar `gen_random_uuid()`** (36 chars → error de longitud). Generar en Python: `secrets.choice(ALPHABET)` 21 veces.`

**32. `bot-avatar-pipeline`** → fusionar-en:bot-avatar-config · riesgo medio · conf 0.7
   - Lo propio es la generación+QA (gen_avatares.py, prompts endurecidos y el pareado etiqueta↔celda del contact sheet); los pasos de instalar/verificar avatar.png+avatar-<bot>.jpg y el caché del Desktop duplican bot-avatar-config. Portar la generación y el QA al destino antes de retirar.
   - *Evidencia:* `QA visual de CADA archivo con `vision_analyze` — NO fiarse del nombre del archivo.`

**33. `keyframe-script-qa`** → fusionar-en:scene-keyframe-qa-lipsync · riesgo medio · conf 0.65
   - Mismo encargo (QA de keyframes contra el guion maestro de la campaña Lucky), mismo checklist (identidad/drift, prop agarrado, signage, 9:16) y el MISMO workaround de visión (qwen3.6 en api.nan.builders con NAN_API_KEY). Portar antes de fusionar la tabla de veredicto cruzado y los 3 bloques de master prompt, que son lo único que el destino no tiene.
   - *Evidencia:* `Analizar **cada imagen con visión real** y cruzar contra el guion maestro.`

**34. `lucky-reel-voice-script`** → fusionar-en:reel-voice-lipsync · riesgo medio · conf 0.6
   - La receta (clip Seedance + sync-lipsync + voz ElevenLabs) ya está documentada con más detalle en reel-voice-lipsync (atempo, costos, QA con crop de cabeza); lo único propio son los números medidos de ritmo (2,2 pal/s, digits expandidos) y las reglas de SFX/música, que hay que portar al retirar.
   - *Evidencia:* `~2.2 palabras/seg (medido por Sindri 29/08; no fiarse de estimaciones de 2.7)`

**35. `poster-composition`** → fusionar-en:campaign-poster-compositing · riesgo bajo · conf 0.7
   - Mismo patrón exacto (arte sin tipografía + composición PIL por capas, scrim, variable fonts, loop de QA con visión); el destino ya trae el pitfall capital de no parchear un poster compuesto, mientras que aquí el reference citado (`references/nan-builders-image-api.md`) no existe. Portar la regla del overlay RGBA recortado para video.
   - *Evidencia:* `Nunca quemar tipografía en el modelo de imagen.`

**36. `baoyu-post-to-x`** → retirar · riesgo medio · conf 0.6
   - El documento entero es selección de modos para runtimes ajenos (Codex Chrome plugin / Computer Use) y TODAS sus rutas de ejecución están rotas: no existe `scripts/` ni `references/` en la carpeta. Antes de retirar, portar el flujo de X Articles (Insert→Media, placeholders XIMGPH_) a la skill de publicación que se use.
   - *Evidencia:* `All scripts are located in the `scripts/` subdirectory of this skill.`

**37. `service-agent-code-handoff`** → fusionar-en:productivity/specification-handoff · riesgo bajo · conf 0.75
   - Ambos describen el MISMO procedimiento (SPEC permanente + PROMPT temporal autocontenido para AGY/OpenCode, repo read-only, no ejecutar SQL, entregar en /opt/data/entregables) con el mismo caso Golden Game; uno sobra. Al fusionar, llevar `templates/prompt-handoff.md` (unico activo que el otro no tiene).
   - *Evidencia:* `"**PROMPT-<ASUNTO>-<FECHA>.md** — TEMPORAL y autocontenido para pegar entero al editor. El PROMPT exige entregar un INFORME FINAL y **borrarse a sí mismo al terminar** (el SPEC se conserva)."`

**38. `e2e`** → fusionar-en:testing-best-practices · riesgo bajo · conf 0.65
   - Documento fino (3 bullets) que es la capa E2E ya nombrada por testing-best-practices; sus 3 aportes (contenedores aislados DB/Redis, seeds idempotentes, polling en vez de timers) se absorben sin perdida como subseccion.
   - *Evidencia:* `"**Flakiness Elimination**: Replace arbitrary timers with explicit condition polling and event triggers."`

**39. `telegram-channel-archaeology`** → fusionar-en:locate-shared-resource · riesgo bajo · conf 0.72
   - Su procedimiento (IDs de canal, queries a state.db, ids de Notion, pitfalls de rg/JSON) ya esta cubierto casi literalmente por locate-shared-resource, que ademas aporta un script reutilizable y mas rutas de busqueda. Solo aporta en limpio el pitfall interno-vs-externo y la ruta channel_directory.json.
   - *Evidencia:* `Clase de tarea: "busca en Links de X / Repos Git / Tiktoks el recurso que compartimos" o "¿qué se subió a X?"`

**40. `web-content-extraction`** → fusionar-en:embedded-payload-extraction · riesgo bajo · conf 0.62
   - Su tecnica central (endpoint .md alternativo + UA Chrome) es el primer escalon del signal ladder de embedded-payload-extraction, que ya es el paraguas del caso; la cadena de fallback restante pertenece a blocked-page-recovery. Fusionar evita dos skills compitiendo por el mismo disparador SPA.
   - *Evidencia:* `Muchos sitios de documentación sirven una versión **markdown plana** de cada artículo aunque la app sea JS-heavy.`

**41. `youtube-content`** → fusionar-en:youtube-full · riesgo medio · conf 0.6
   - El parrafo de transcript de youtube-full declara la misma via local (youtube-transcript-api) que este skill implementa, o sea duplicado funcional que colisiona en el retriever. La fusion debe arrastrar scripts/fetch_transcript.py y references/output-formats.md (hilos/blog/capitulos, que youtube-full no cubre) y actualizar la referencia en tiktok-ingestion.
   - *Evidencia:* `Extract transcripts from YouTube videos and convert them into useful formats.`

**42. `blogwatcher`** → fusionar-en:watchers · riesgo medio · conf 0.6
   - Es un manual de una CLI externa (blogwatcher-cli) para el mismo caso de uso que watchers, que es el patron nativo del canon (scripts + watermark + cron). La fusion debe llevarse como referencia las piezas exclusivas: import OPML, estado read/unread y persistencia del SQLite/Docker; sin eso no se recomienda retirar.
   - *Evidencia:* `Track blog and RSS/Atom feed updates with the `blogwatcher-cli` tool.`

## 5. Descripciones propuestas

- **706 listas para aplicar** (`Use when …` y ≤60 caracteres)
- **0 exceden 60 caracteres** (el router sólo ve 57 + `...`)
- **1 no empiezan con `Use when`**

## 6. Tags propuestos

- **2194 tags distintos** sobre las 707 skills
- tags con acentos/tildes (deben ser 0 porque la búsqueda substring es ciega a ellos): **2** ['caché', '元宝']

## 7. Reparto por categoría

| Categoría | conservar | reescribir | fusionar/retirar |
|---|---:|---:|---:|
| specialists | 222 | 104 | 14 |
| productivity | 67 | 20 | 4 |
| software-development | 43 | 22 | 12 |
| creative | 35 | 19 | 5 |
| devops | 23 | 20 | 4 |
| core | 4 | 25 | 0 |
| autonomous-ai-agents | 19 | 9 | 1 |
| research | 17 | 5 | 1 |
| apple | 0 | 4 | 0 |
| media | 0 | 2 | 1 |
| email | 1 | 1 | 0 |
| note-taking | 0 | 1 | 0 |
| social-media | 0 | 1 | 0 |
| web | 1 | 0 | 0 |

## 8. Contexto: lo reparado antes de este censo (F7/F8)

- **F7:** 19 descripciones que eran ruido de auditoría reescritas a `Use when`; 159 referencias byte-idénticas a skills standalone reemplazadas por puntero; 25 skills con tags bilingües.
- **F8:** 296 enlaces a `references/` que nunca existieron, marcados como faltantes en 50 SKILL.md; 2 recuperados; 23 skills deshabilitadas del perfil roshi habilitadas.

## 9. Conclusión operativa

1. La señal de selección es el cuello de botella, no el volumen: **252 skills necesitan descripción-disparador** (233 propuestas + 19 ya aplicadas en F7).
2. **42 skills** (5,9 %) son candidatas reales a consolidación, y cada una con cita. Requieren decisión del CTO.
3. Los `stub`s (11) y las de valor nulo (3) son la única depuración sin debate.
4. Todo lo demás se conserva: **432 skills (61,1 %) no requieren ningún cambio**.