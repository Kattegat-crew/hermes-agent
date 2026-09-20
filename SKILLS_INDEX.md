# Índice Canónico de Skills — Flota Hermes
> **Última sincronización**: 2026-09-20 03:00 | **Total de skills**: 716 (excluye bundles de convenciones con prefijo `_`)

Este catálogo representa la **Fuente Única de Verdad (SSOT)** de habilidades operativas para todos los perfiles de la flota Hermes.
Todas las skills se resuelven on-demand desde `/opt/hermes/skills` sin saturar la ventana de contexto.

| Categoría | Skill | Descripción | Ruta Canónica |
| :--- | :--- | :--- | :--- |
| `apple` | **`apple-notes`** | Manage Apple Notes via memo CLI: create, search, edit. | `apple/apple-notes` |
| `apple` | **`apple-reminders`** | Apple Reminders via remindctl: add, list, complete. | `apple/apple-reminders` |
| `apple` | **`findmy`** | Track Apple devices/AirTags via FindMy.app on macOS. | `apple/findmy` |
| `apple` | **`imessage`** | Send and receive iMessages/SMS via the imsg CLI on macOS. | `apple/imessage` |
| `autonomous-ai-agents` | **`agent-fork-adaptation`** | Proceso completo para hacer fork de un agente IA existente (Hermes, Codex, Claude Code) y ad... | `autonomous-ai-agents/agent-fork-adaptation` |
| `autonomous-ai-agents` | **`autonomous-loops`** | Patterns and architectures for autonomous loops — from simple sequential pipelines to RFC-dr... | `autonomous-ai-agents/autonomous-loops` |
| `autonomous-ai-agents` | **`claude-code`** | Delegate coding to Claude Code CLI (features, PRs). | `autonomous-ai-agents/claude-code` |
| `autonomous-ai-agents` | **`codex`** | Delegate coding to OpenAI Codex CLI (features, PRs). | `autonomous-ai-agents/codex` |
| `autonomous-ai-agents` | **`computer-use`** | Drive the desktop background-first; escalate on signal. | `autonomous-ai-agents/computer-use` |
| `autonomous-ai-agents` | **`decision-autonomy`** | Cuándo actuar sin preguntar y cuándo consultar al usuario. Evita loops de inacción (esperar ... | `autonomous-ai-agents/decision-autonomy` |
| `autonomous-ai-agents` | **`doubt-driven-development`** | Subjects every non-trivial decision to a fresh-context adversarial review before it stands. ... | `autonomous-ai-agents/doubt-driven-development` |
| `autonomous-ai-agents` | **`ecosystem-setup`** | Complete guide to setting up Ragnar's environment — pip bootstrap, GitHub CLI, Notion API, D... | `autonomous-ai-agents/ecosystem-setup` |
| `autonomous-ai-agents` | **`evidence-based-replies`** | evidence-based-replies — Compare a person's claim to a cited paper or source, isolate what t... | `autonomous-ai-agents/evidence-based-replies` |
| `autonomous-ai-agents` | **`executing-plans`** | Use when you have a written implementation plan to execute in a separate session with review... | `autonomous-ai-agents/executing-plans` |
| `autonomous-ai-agents` | **`external-model-review`** | external-model-review — Run reproducible independent reviews of plans, architectures, major ... | `autonomous-ai-agents/external-model-review` |
| `autonomous-ai-agents` | **`hermes-agent`** | Use, configure, theme, extend, and orchestrate Hermes Agent. | `autonomous-ai-agents/hermes-agent` |
| `autonomous-ai-agents` | **`llm-judge-gates`** | Diseño de gates con juez LLM en pipelines de contenido | `autonomous-ai-agents/llm-judge-gates` |
| `autonomous-ai-agents` | **`one-three-one-rule`** | 1-3-1 decision briefs: problem, three options, one pick. | `autonomous-ai-agents/one-three-one-rule` |
| `autonomous-ai-agents` | **`opencode`** | Delegate coding to OpenCode CLI (features, PR review). | `autonomous-ai-agents/opencode` |
| `autonomous-ai-agents` | **`rdd-defect-workflow`** | Trigger: RDD, receipt-driven development, review authority, receipt/lineage, correction/reco... | `autonomous-ai-agents/rdd-defect-workflow` |
| `autonomous-ai-agents` | **`sdd-apply`** | Implement SDD tasks from specs and design. Trigger: orchestrator launches apply for one or m... | `autonomous-ai-agents/sdd-apply` |
| `autonomous-ai-agents` | **`sdd-archive`** | Archive a completed SDD change by syncing delta specs. Trigger: orchestrator launches archiv... | `autonomous-ai-agents/sdd-archive` |
| `autonomous-ai-agents` | **`sdd-design`** | Create the SDD technical design and architecture approach. Trigger: orchestrator launches de... | `autonomous-ai-agents/sdd-design` |
| `autonomous-ai-agents` | **`sdd-explore`** | Explore SDD ideas before committing to a change. Trigger: orchestrator launches exploration ... | `autonomous-ai-agents/sdd-explore` |
| `autonomous-ai-agents` | **`sdd-init`** | Trigger: sdd init, iniciar sdd, openspec init. Initialize SDD context, testing capabilities,... | `autonomous-ai-agents/sdd-init` |
| `autonomous-ai-agents` | **`sdd-onboard`** | Walk users through the SDD workflow on the real codebase. Trigger: orchestrator launches onb... | `autonomous-ai-agents/sdd-onboard` |
| `autonomous-ai-agents` | **`sdd-propose`** | Create an SDD change proposal with intent, scope, and approach. Trigger: orchestrator launch... | `autonomous-ai-agents/sdd-propose` |
| `autonomous-ai-agents` | **`sdd-spec`** | Write SDD delta specs with requirements and scenarios. Trigger: orchestrator launches spec w... | `autonomous-ai-agents/sdd-spec` |
| `autonomous-ai-agents` | **`sdd-tasks`** | Break an SDD change into implementation tasks. Trigger: orchestrator launches task planning ... | `autonomous-ai-agents/sdd-tasks` |
| `autonomous-ai-agents` | **`sdd-verify`** | Trigger: SDD verification phase, verify change. Execute tests and prove implementation match... | `autonomous-ai-agents/sdd-verify` |
| `autonomous-ai-agents` | **`subagent-driven-development`** | Use when executing implementation plans with independent tasks in the current session | `autonomous-ai-agents/subagent-driven-development` |
| `autonomous-ai-agents` | **`system-onboarding`** | Process for onboarding Ragnar (the AI orchestrator) into a new environment. Covers identity ... | `autonomous-ai-agents/system-onboarding` |
| `autonomous-ai-agents` | **`writing-plans`** | Use when you have a spec or requirements for a multi-step task, before touching code | `autonomous-ai-agents/writing-plans` |
| `core` | **`agent-reach`** | MUST USE when user wants to 调研/research/搜索/search/查/找/look up anything on the internet — e.g... | `core/agent-reach` |
| `core` | **`agent-roster-ops`** | Paraguas consolidado para agent-roster-ops. verificado: roster-blueprint ~ roster-design ~ h... | `core/agent-roster-ops` |
| `core` | **`brain-knowledge-ops`** | Paraguas consolidado para brain-knowledge-ops. verificado: brain-graph-operations ~ brain-gr... | `core/brain-knowledge-ops` |
| `core` | **`campaign-ops`** | Paraguas consolidado para campaign-ops. operacion de campanas end-to-end | `core/campaign-ops` |
| `core` | **`capability-claim-verification`** | Use when a config/capability claim needs read-only proof. | `core/capability-claim-verification` |
| `core` | **`colombia-legal-ops`** | Paraguas consolidado para colombia-legal-ops. documentos legales/compliance Colombia | `core/colombia-legal-ops` |
| `core` | **`copy-quality-es`** | Paraguas consolidado para copy-quality-es. 8 reglas anti-slop/copy -> 1 guia de calidad edit... | `core/copy-quality-es` |
| `core` | **`docker-management`** | Manage Docker containers, images, volumes, and Compose. | `core/docker-management` |
| `core` | **`engram-memory-system`** | Use when setting up Engram MCP memory with Hermes. | `core/engram-memory-system` |
| `core` | **`github-workflow`** | Paraguas consolidado para github-workflow. 12 github-* -> 1 workflow + 1 forensics | `core/github-workflow` |
| `core` | **`google-workspace-ops`** | Paraguas consolidado para google-workspace-ops. verificado: 4 de ellas en un mismo cluster J... | `core/google-workspace-ops` |
| `core` | **`guardado-doble-memoria`** | Guarda en Engram + memoria al pedirlo o cerrar sesión. | `core/engram-memory-system/guardado-doble-memoria` |
| `core` | **`hermes-cron-ops`** | Paraguas consolidado para hermes-cron-ops. 3 de ellas ya daban Jaccard>=0.30 (duplicados sem... | `core/hermes-cron-ops` |
| `core` | **`hermes-desktop-ops`** | Paraguas consolidado para hermes-desktop-ops. 2 pares con Jaccard>=0.30 ya detectados | `core/hermes-desktop-ops` |
| `core` | **`hermes-fleet-operations`** | Paraguas consolidado para hermes-fleet-operations. 12 skills de flota/multiperfil -> 1 parag... | `core/hermes-fleet-operations` |
| `core` | **`hermes-provider-ops`** | Paraguas consolidado para hermes-provider-ops. curado: fallback y resilience son el mismo pr... | `core/hermes-provider-ops` |
| `core` | **`hermes-runtime-ops`** | Paraguas consolidado para hermes-runtime-ops. infra/observabilidad del runtime Hermes | `core/hermes-runtime-ops` |
| `core` | **`informes-cliente-pipeline`** | Paraguas consolidado para informes-cliente-pipeline. generacion/entrega de informes y render... | `core/informes-cliente-pipeline` |
| `core` | **`mapa-de-carpetas`** | Escanea carpetas y regula dónde va qué (VPS, repos, Drive). | `core/mapa-de-carpetas` |
| `core` | **`meta-ads-ops`** | Paraguas consolidado para meta-ads-ops. verificado: meta-ads-campaigns ~ meta-ads-operations | `core/meta-ads-ops` |
| `core` | **`multi-agent-collaboration`** | Paraguas consolidado para multi-agent-collaboration. colaboracion/handoff entre agentes | `core/multi-agent-collaboration` |
| `core` | **`nan-builders-api`** | NaN Builders API: base URL, auth, Cloudflare UA, images. | `core/nan-builders-api` |
| `core` | **`oauth-connection-ops`** | Paraguas consolidado para oauth-connection-ops. verificado: agent-connection-governance ~ oa... | `core/oauth-connection-ops` |
| `core` | **`skill-library-ops`** | Paraguas consolidado para skill-library-ops. gobierno del catalogo de skills (incluye la ski... | `core/skill-library-ops` |
| `core` | **`systematic-debugging`** | 4-phase root cause debugging: understand bugs before fixing. | `core/systematic-debugging` |
| `core` | **`vault-access`** | Access secrets from Vaultwarden. Use when you need an API key, token, password, or any secre... | `core/vault-access` |
| `core` | **`video-reel-pipeline`** | Paraguas consolidado para video-reel-pipeline. 22 skills de produccion de video -> 1 paragua... | `core/video-reel-pipeline` |
| `core` | **`vps-deployment-ops`** | Paraguas consolidado para vps-deployment-ops. despliegue en VPS | `core/vps-deployment-ops` |
| `core` | **`whatsapp-bridge-operations`** | Operar el bridge WhatsApp: allowlist, grupos, voz y debug. | `core/whatsapp-bridge-operations` |
| `creative` | **`ai-image-provider-api`** | Use when: APIs de imagen (flux-2-klein, fal.ai). | `creative/ai-image-provider-api` |
| `creative` | **`architecture-diagram`** | Dark-themed SVG architecture/cloud/infra diagrams as HTML. | `creative/architecture-diagram` |
| `creative` | **`ascii-art`** | ASCII art: pyfiglet, cowsay, boxes, image-to-ascii. | `creative/ascii-art` |
| `creative` | **`ascii-video`** | ASCII video: convert video/audio to colored ASCII MP4/GIF. | `creative/ascii-video` |
| `creative` | **`audio-video-transcription`** | Transcribe audio/video to text via NaN-Builders whisper API. | `creative/audio-video-transcription` |
| `creative` | **`baoyu-compress-image`** | Compresses images to WebP (default) or PNG with automatic tool selection. Use when user asks... | `creative/baoyu-compress-image` |
| `creative` | **`baoyu-cover-image`** | Generates article cover images with 5 dimensions (type, palette, rendering, text, mood) comb... | `creative/baoyu-cover-image` |
| `creative` | **`baoyu-infographic`** | Infographics: 21 layouts x 21 styles (信息图, 可视化). | `creative/baoyu-infographic` |
| `creative` | **`baoyu-post-to-x`** | Posts content and articles to X (Twitter). Supports regular posts with images/videos and X A... | `creative/baoyu-post-to-x` |
| `creative` | **`bot-avatar-config`** | Use when: instalar avatares bots crew + refresco Desktop. | `creative/bot-avatar-config` |
| `creative` | **`bot-avatar-pipeline`** | Use when: generar/validar/instalar avatares de bots. | `creative/bot-avatar-pipeline` |
| `creative` | **`claude-design`** | Design one-off HTML artifacts (landing, deck, prototype). | `creative/claude-design` |
| `creative` | **`content-production`** | Full content production pipeline — takes a topic from blank page to published-ready piece. U... | `creative/content-production` |
| `creative` | **`contract-and-proposal-writer`** | Generate professional, jurisdiction-aware business documents: freelance contracts, project p... | `creative/contract-and-proposal-writer` |
| `creative` | **`data-quality-auditor`** | Audit datasets for completeness, consistency, accuracy, and validity. Profile data distribut... | `creative/data-quality-auditor` |
| `creative` | **`design-md`** | Author/validate/export Google's DESIGN.md token spec files. | `creative/design-md` |
| `creative` | **`draw-your-font`** | Turn a handwriting photo into an installable TTF font. | `creative/draw-your-font` |
| `creative` | **`elevenlabs-voice-narration`** | Use when a reel needs ElevenLabs TTS/STTS voice. | `creative/elevenlabs-voice-narration` |
| `creative` | **`excalidraw`** | Hand-drawn Excalidraw JSON diagrams (arch, flow, seq). | `creative/excalidraw` |
| `creative` | **`gdpr-dsgvo-expert`** | GDPR and German DSGVO compliance automation. Scans codebases for privacy risks, generates DP... | `creative/gdpr-dsgvo-expert` |
| `creative` | **`general-counsel-advisor`** | General Counsel advisory for startups: contract review (MSA, SaaS, NDA, DPA, employment), IP... | `creative/general-counsel-advisor` |
| `creative` | **`guion-reel-lint-brief`** | Use when: escribir guiones que deben pasar lint y brief. | `creative/guion-reel-lint-brief` |
| `creative` | **`guion-reel-mesa-medida`** | Use when escribiendo o midiendo un guion de reel de campana. | `creative/guion-reel-mesa-medida` |
| `creative` | **`heartmula`** | HeartMuLa: Suno-like song generation from lyrics + tags. | `creative/heartmula` |
| `creative` | **`hermes-bot-avatars`** | Fix or set Hermes Desktop bot avatars; RPC, caps, cache. | `creative/hermes-bot-avatars` |
| `creative` | **`hermes-multiprofile-gateway-ops`** | Debug multi-profile Hermes gateway: routing, restart. | `creative/hermes-multiprofile-gateway-ops` |
| `creative` | **`humanizer`** | Humanize text: strip AI-isms and add real voice. | `creative/humanizer` |
| `creative` | **`hyperframes`** | Render MP4/WebM videos from HTML compositions. | `creative/hyperframes` |
| `creative` | **`image-enhancer`** | Improves the quality of images, especially screenshots, by enhancing resolution, sharpness, ... | `creative/image-enhancer` |
| `creative` | **`image-text-verification`** | Use when reading text from an image before acting on it. | `creative/image-text-verification` |
| `creative` | **`keyframe-script-qa`** | Use when: analizar keyframes de escenas contra el guion. | `creative/keyframe-script-qa` |
| `creative` | **`linkedin-content`** | Use when someone wants to write, edit, or lint a LinkedIn post — a story, how-to, opinion pi... | `creative/linkedin-content` |
| `creative` | **`llm-cost-optimizer`** | Use proactively whenever LLM API costs come up -- or should. Triggers include: 'my AI costs ... | `creative/llm-cost-optimizer` |
| `creative` | **`lucky-reel-voice-script`** | Guiones de voz para reels con lip-sync pos-generado. | `creative/lucky-reel-voice-script` |
| `creative` | **`manim-video`** | Manim CE animations: 3Blue1Brown math/algo videos. | `creative/manim-video` |
| `creative` | **`meme-generation`** | Create meme PNGs from templates with Pillow text overlay. | `creative/meme-generation` |
| `creative` | **`neuralcrew-bot-avatars`** | Use when: instalar/actualizar avatar de un bot NeuralCrew. | `creative/neuralcrew-bot-avatars` |
| `creative` | **`open-design`** | Use the Open Design workbench to create editable visual projects, prototypes, landing pages,... | `creative/open-design` |
| `creative` | **`openai-automation`** | Automate OpenAI API operations -- generate responses with multimodal and structured output s... | `creative/openai-automation` |
| `creative` | **`openai-image-gen`** | Generate visual assets, marketing graphics, and concept art using OpenAI image generation AP... | `creative/openai-image-gen` |
| `creative` | **`p5js`** | p5.js sketches: gen art, shaders, interactive, 3D. | `creative/p5js` |
| `creative` | **`pil-ffmpeg-rendering`** | Use when creating video clips with PIL + ffmpeg. | `creative/pil-ffmpeg-rendering` |
| `creative` | **`pixel-art`** | Pixel art w/ era palettes (NES, Game Boy, PICO-8). | `creative/pixel-art` |
| `creative` | **`popular-web-designs`** | 54 real design systems (Stripe, Linear, Vercel) as HTML/CSS. | `creative/popular-web-designs` |
| `creative` | **`poster-composition`** | Posters: keyart IA + texto en capas PIL. | `creative/poster-composition` |
| `creative` | **`reel-performance-analytics`** | Score published reels vs platform metrics via Composio. | `creative/reel-performance-analytics` |
| `creative` | **`reel-pipeline`** | Genera videos tipo reel verticales 9:16 con IA. Soporta texto-a-video e imagen-a-video. Usa ... | `creative/reel-pipeline` |
| `creative` | **`reel-produccion-pagina`** | Use when producir reel de campaña y página en portal reels. | `creative/reel-produccion-pagina` |
| `creative` | **`reel-voice-lipsync`** | Use when a reel needs correct pronunciation and lip-sync. | `creative/reel-voice-lipsync` |
| `creative` | **`referrals`** | When the user wants to create, optimize, or analyze a referral program, affiliate program, o... | `creative/referrals` |
| `creative` | **`sesion-pieza-por-pieza`** | Use when producing a campaign video piece-by-piece. | `creative/sesion-pieza-por-pieza` |
| `creative` | **`sketch`** | Throwaway HTML mockups: 2-3 design variants to compare. | `creative/sketch` |
| `creative` | **`social-content`** | When the user wants help creating, scheduling, or optimizing social media content for Linked... | `creative/social-content` |
| `creative` | **`social-story-production`** | Use when raw chat video must become an IG/FB story. | `creative/social-story-production` |
| `creative` | **`songwriting-and-ai-music`** | Songwriting craft and Suno AI music prompts. | `creative/songwriting-and-ai-music` |
| `creative` | **`tldraw-offline`** | Drive and script tldraw offline canvases with an agent. | `creative/tldraw-offline` |
| `creative` | **`touchdesigner-mcp`** | Control TouchDesigner via twozero MCP. | `creative/touchdesigner-mcp` |
| `creative` | **`unreal-mcp`** | Automate Unreal Engine editor scenes, actors, and renders. | `creative/unreal-mcp` |
| `creative` | **`video-ai-provider-integration`** | Use when wiring an AI video provider into the pipeline. | `creative/video-ai-provider-integration` |
| `creative` | **`video-tts-pronunciation-fix`** | Fix Spanish TTS pronunciation in video reels via respelling. | `creative/video-tts-pronunciation-fix` |
| `creative` | **`youtube-full`** | Use when the user needs YouTube transcripts, video search, channel browsing, playlist extrac... | `creative/youtube-full` |
| `devops` | **`activepieces-connection-api`** | Use when creating ActivePieces connections via REST API. | `devops/activepieces-connection-api` |
| `devops` | **`activepieces-db-surgery`** | Use when: crear/editar flows ActivePieces en su Postgres. | `devops/activepieces-db-surgery` |
| `devops` | **`activepieces-flow-editing`** | Edit AP flows/templates via DB and verify the run used it. | `devops/activepieces-flow-editing` |
| `devops` | **`activepieces-google-access`** | Use when accessing Google services via ActivePieces. | `devops/activepieces-google-access` |
| `devops` | **`activepieces-selfhost-ops`** | Operate self-hosted ActivePieces connections and MCP. | `devops/activepieces-selfhost-ops` |
| `devops` | **`agent-connection-governance`** | Per-agent OAuth connection enforcement (ActivePieces). | `devops/agent-connection-governance` |
| `devops` | **`atlas-best-practices`** | Atlas database schema management, declarative migrations, schema diffing, and database CI/CD... | `devops/atlas-best-practices` |
| `devops` | **`aws-solution-architect`** | Design AWS architectures for startups using serverless patterns and IaC templates. Use when ... | `devops/aws-solution-architect` |
| `devops` | **`change-attribution-reports`** | Use when asked who changed what in a project recently. | `devops/change-attribution-reports` |
| `devops` | **`cloudflare-access-api`** | Trigger: Cloudflare Access, Zero Trust, protect subdomain, Access policy, one-time PIN login... | `devops/cloudflare-access-api` |
| `devops` | **`cloudflare-dns-cutover`** | Trigger: Cloudflare DNS, A record, cutover, TTL 300, SSL mode full, zone DNS edit, origin IP... | `devops/cloudflare-dns-cutover` |
| `devops` | **`cloudflare-email-auth-dns`** | Trigger: SPF, DMARC, DKIM, MX records, email deliverability, Gmail spam, Cloudflare DNS TXT.... | `devops/cloudflare-email-auth-dns` |
| `devops` | **`coolify-secure-secrets`** | Use when deploying apps or databases in Coolify, managing encrypted secrets in Coolify's dat... | `devops/coolify-secure-secrets` |
| `devops` | **`devops-infrastructure`** | Manage server services and containers. | `devops/devops-infrastructure` |
| `devops` | **`docker-container-optimization`** | Docker container hardening, multi-stage builds, minimal base images, and caching layers. | `devops/docker-container-optimization` |
| `devops` | **`docker-service-tailscale`** | Access any service running inside Docker from outside via Tailscale — general purpose, not H... | `devops/docker-service-tailscale` |
| `devops` | **`docuseal-selfhost-ops`** | Trigger: docuseal, firma electronica, contrato roto, link de firma, firmante no puede firmar... | `devops/docuseal-selfhost-ops` |
| `devops` | **`formbricks-v5-selfhost`** | Trigger: Formbricks, formbricks v5, formbricks self-hosted, formbricks deploy/reset, error a... | `devops/formbricks-v5-selfhost` |
| `devops` | **`gcp-cloud-architect`** | Design GCP architectures for startups and enterprises. Use when asked to design Google Cloud... | `devops/gcp-cloud-architect` |
| `devops` | **`google-oauth-reauth`** | DEPRECATED — Use activepieces-google-access instead. Token local revocado. | `devops/google-oauth-reauth` |
| `devops` | **`hermes-desktop-gateway-support`** | Use when Hermes Desktop no conecta al gateway remoto. | `devops/hermes-desktop-gateway-support` |
| `devops` | **`hermes-multiprofile-deploy`** | Configura N perfiles multiplexados sin romper el gateway. | `devops/hermes-multiprofile-deploy` |
| `devops` | **`hermes-production-deployment`** | Production deployment of Hermes agents for multiple clients. Includes: full VPS setup plan w... | `devops/hermes-production-deployment` |
| `devops` | **`hermes-relocation-ops`** | Use when asked to relocate an agent: guild, token, or host. | `devops/hermes-relocation-ops` |
| `devops` | **`hermes-s6-container-supervision`** | Modify or debug s6 services in the Hermes Docker image. | `devops/hermes-s6-container-supervision` |
| `devops` | **`hermes-specialist-agents-deploy`** | Desplegar agentes especializados como perfiles Hermes. | `devops/hermes-specialist-agents-deploy` |
| `devops` | **`host-infra-forensics`** | Use when a service is unreachable from a remote client. | `devops/host-infra-forensics` |
| `devops` | **`independent-infra-audit`** | Use when auditing a deployed pipeline read-only. | `devops/independent-infra-audit` |
| `devops` | **`migration-architect`** | Zero-downtime migration planning, compatibility validation, and rollback strategy generation... | `devops/migration-architect` |
| `devops` | **`multi-profile-cron-reliability`** | Harden failing profile crons via pinning and skill links. | `devops/multi-profile-cron-reliability` |
| `devops` | **`nginx-proxy-manager-api`** | Trigger: NPM, Nginx Proxy Manager, proxy host, Let's Encrypt DNS challenge, certificate API,... | `devops/nginx-proxy-manager-api` |
| `devops` | **`nix-best-practices`** | Nix Flakes, reproducible dev environments, direnv integration, and declarative package manag... | `devops/nix-best-practices` |
| `devops` | **`oauth-connection-health-audit`** | Audit expired OAuth refresh tokens in ActivePieces; re-auth only the dead. | `devops/oauth-connection-health-audit` |
| `devops` | **`open-design-deployment`** | Use when deploying or operating OpenDesign (OD). | `devops/open-design-deployment` |
| `devops` | **`open-design-selfhost-ops`** | Deploy/run self-hosted OpenDesign (Docker+NPM+BYOK). | `devops/open-design-selfhost-ops` |
| `devops` | **`orbstack-best-practices`** | OrbStack fast container and Linux machine management, performance tuning, Rosetta 2 emulatio... | `devops/orbstack-best-practices` |
| `devops` | **`pinggy-tunnel`** | Zero-install localhost tunnels over SSH via Pinggy. | `devops/pinggy-tunnel` |
| `devops` | **`reel-gallery-deploy`** | Deploy public reel galleries under reels.neuralcrewlabs.com. | `devops/reel-gallery-deploy` |
| `devops` | **`sdlc-review`** | Review Kanban handoffs and route verified outcomes. | `devops/sdlc-review` |
| `devops` | **`senior-data-engineer`** | Data engineering skill for building scalable data pipelines, ETL/ELT systems, and data infra... | `devops/senior-data-engineer` |
| `devops` | **`slo-architect`** | Use when defining, reviewing, or operating SLOs/SLIs/error budgets. Triggers on "define an S... | `devops/slo-architect` |
| `devops` | **`terraform-patterns`** | Terraform infrastructure-as-code agent skill and plugin for Claude Code, Codex, Gemini CLI, ... | `devops/terraform-patterns` |
| `devops` | **`tilt`** | Tilt multi-service local development, live updates, health checks, and Kubernetes/Docker Com... | `devops/tilt` |
| `devops` | **`twenty-selfhost-auth`** | Trigger: Twenty CRM login, Twenty signup disabled, create Twenty user, twenty workspace role... | `devops/twenty-selfhost-auth` |
| `devops` | **`unify-service-logins`** | Trigger: único usuario, unify logins, cambiar admin, reset password, captain@neuralcrewlabs.... | `devops/unify-service-logins` |
| `devops` | **`vps-host-repo-access`** | Acceder a repos del host VPS desde el contenedor. | `devops/vps-host-repo-access` |
| `devops` | **`vps-web-deployment`** | Deploy static sites to VPS with NPM and migration. | `devops/vps-web-deployment` |
| `email` | **`email-inbox-triage`** | Triage an inbox: prioritize threads, draft replies safely. | `email/email-inbox-triage` |
| `email` | **`himalaya`** | Himalaya CLI: IMAP/SMTP email from terminal. | `email/himalaya` |
| `media` | **`gif-search`** | Search/download GIFs from Tenor via curl + jq. | `media/gif-search` |
| `media` | **`songsee`** | Audio spectrograms/features (mel, chroma, MFCC) via CLI. | `media/songsee` |
| `media` | **`youtube-content`** | YouTube transcripts to summaries, threads, blogs. | `media/youtube-content` |
| `note-taking` | **`obsidian`** | Read, search, create, and edit notes in the Obsidian vault. | `note-taking/obsidian` |
| `productivity` | **`agentmail`** | Give the agent its own inbox: send and receive email. | `productivity/agentmail` |
| `productivity` | **`airtable`** | Airtable REST API via curl. Records CRUD, filters, upserts. | `productivity/airtable` |
| `productivity` | **`blackbox`** | Delegate coding tasks to the Blackbox AI multi-model CLI. | `productivity/blackbox` |
| `productivity` | **`box`** | Box manages cloud files, sharing, search, and metadata. | `productivity/box` |
| `productivity` | **`canvas`** | Fetch Canvas LMS courses and assignments via API token. | `productivity/canvas` |
| `productivity` | **`character-sheet-locking`** | Lock canonical mascot model sheets: one figure per view. | `productivity/character-sheet-locking` |
| `productivity` | **`churn-prevention`** | When the user wants to reduce churn, build cancellation flows, set up save offers, recover f... | `productivity/churn-prevention` |
| `productivity` | **`colombia-juegos-promocionales`** | Usar al redactar compliance de promociones en Colombia. | `productivity/colombia-juegos-promocionales` |
| `productivity` | **`colombia-promociones-docs-multiempresa`** | Paquete legal separado por empresa en campañas multiempresa. | `productivity/colombia-promociones-docs-multiempresa` |
| `productivity` | **`composio-cli`** | Use when installing or automating with Composio CLI. | `productivity/composio-cli` |
| `productivity` | **`composio-integrations`** | Use when connecting tools via Composio: install, execute. | `productivity/composio-integrations` |
| `productivity` | **`data-driven-team-reports`** | Team reports from verified data, delivered to Discord. | `productivity/data-driven-team-reports` |
| `productivity` | **`document-digitization-ocr`** | Use cuando hay que OCRear o digitalizar documentos. | `productivity/document-digitization-ocr` |
| `productivity` | **`document-reader`** | Universal document reader that parses .docx, .xlsx, .pdf, .pptx, .odt, .ods, .odp, .rtf, .tx... | `productivity/document-reader` |
| `productivity` | **`document-to-action-items`** | Extract cited obligations, deadlines, tasks from documents. | `productivity/document-to-action-items` |
| `productivity` | **`documentos-legales-entregables`** | Entregables legales: verificar papeles, sin huecos, .docx. | `productivity/documentos-legales-entregables` |
| `productivity` | **`docx`** | Create, read, edit, template, and review Word .docx files. | `productivity/docx` |
| `productivity` | **`embedded-payload-extraction`** | Use when OG/meta truncate: extract hydration JSON. | `productivity/embedded-payload-extraction` |
| `productivity` | **`entregables-de-campana-versionado`** | Use when un dato del cliente llega tras el entregable. | `productivity/entregables-de-campana-versionado` |
| `productivity` | **`escalada-tecnica`** | Escala al agente tecnico tareas imposibles via buzon PROD. | `productivity/escalada-tecnica` |
| `productivity` | **`excel-author`** | Build auditable financial workbooks headless via openpyxl. | `productivity/excel-author` |
| `productivity` | **`fitness-nutrition`** | Workout planning, macros, and body metrics via wger/USDA. | `productivity/fitness-nutrition` |
| `productivity` | **`flujos-con-gates-humanos`** | Use when disenando flujos con gates humanos y firma. | `productivity/flujos-con-gates-humanos` |
| `productivity` | **`git-rebase-sync`** | Sincronizar una rama de trabajo con upstream por rebase, resolviendo conflictos y publicando... | `productivity/git-rebase-sync` |
| `productivity` | **`git-worktree-tidy`** | Listar, limpiar y podar git worktrees sin perder trabajo sin commitear ni dejar metadatos mu... | `productivity/git-worktree-tidy` |
| `productivity` | **`github-actions-failure-forensics`** | Use when a GitHub Actions/CI workflow run fails or is red. | `productivity/github-actions-failure-forensics` |
| `productivity` | **`github-push-container`** | Push a GitHub desde el contenedor: token y auditoría. | `productivity/github-push-container` |
| `productivity` | **`github-ro-mount-workflow`** | Use when repo mounts are read-only; push via token clone. | `productivity/github-ro-mount-workflow` |
| `productivity` | **`gmail-mailbox-organization`** | Label, archive and filter Gmail mailboxes safely, verified. | `productivity/gmail-mailbox-organization` |
| `productivity` | **`gmail-smtp-app-password`** | Trigger: SMTP, smtp.gmail.com, app password, send from, DocuSeal mail, Google Workspace emai... | `productivity/gmail-smtp-app-password` |
| `productivity` | **`google-docs-api`** | Work around Google Docs API limitations when creating documents with content. Key issue: doc... | `productivity/google-docs-api` |
| `productivity` | **`google-drive-access`** | Usar cuando pida acceder a archivos o links de Google Drive. | `productivity/google-drive-access` |
| `productivity` | **`google-oauth-reauth-ops`** | Reauth Google OAuth scopes; PKCE/PEP fallback; verify live. | `productivity/google-oauth-reauth-ops` |
| `productivity` | **`google-workspace`** | Gmail, Calendar, Drive, Docs, Sheets via gws CLI or Python. | `productivity/google-workspace` |
| `productivity` | **`gws-shared-access`** | Google Workspace via root token+venv from sub-profiles. | `productivity/gws-shared-access` |
| `productivity` | **`html-to-print-rendering`** | Render HTML assets to PDF + hi-res PNG via headless browser. | `productivity/html-to-print-rendering` |
| `productivity` | **`informe-mensual-sheet-pdf`** | Informe mensual vivo con Sheet acumulativo y PDF de cierre. | `productivity/informe-mensual-sheet-pdf` |
| `productivity` | **`informes-ventas-cliente`** | Informes de ventas: Sheet con formato + PDF membreteado. | `productivity/informes-ventas-cliente` |
| `productivity` | **`instant-notification-daemons`** | Use when building or fixing push-notification daemons. | `productivity/instant-notification-daemons` |
| `productivity` | **`judgment-day`** | Trigger: judgment day, dual review, adversarial review, juzgar. Run explicit blind dual revi... | `productivity/judgment-day` |
| `productivity` | **`knowledge-consolidation`** | Consolidate raw knowledge into searchable tables and docs. | `productivity/knowledge-consolidation` |
| `productivity` | **`legal-docs-from-meeting-decisions`** | Use when legal docs must track mutating meeting decisions. | `productivity/legal-docs-from-meeting-decisions` |
| `productivity` | **`local-headless-rendering`** | Use when un script renderiza HTML a frames headless. | `productivity/local-headless-rendering` |
| `productivity` | **`manual-operativo-promociones`** | Manual operativo de casino para cajeras y personal. | `productivity/manual-operativo-promociones` |
| `productivity` | **`maps`** | Geocode, POIs, routes, timezones via OpenStreetMap/OSRM. | `productivity/maps` |
| `productivity` | **`mascot-gif-animation`** | Use when creating a mascot waving GIF from a photo still. | `productivity/mascot-gif-animation` |
| `productivity` | **`meeting-action-items`** | Turn meeting notes into cited decisions, owners, tickets. | `productivity/meeting-action-items` |
| `productivity` | **`memento-flashcards`** | Spaced-repetition flashcards: create, review, quiz, export. | `productivity/memento-flashcards` |
| `productivity` | **`minecraft-modpack-server`** | Host modded Minecraft servers (CurseForge, Modrinth). | `productivity/minecraft-modpack-server` |
| `productivity` | **`nano-pdf`** | Edit text in existing PDFs via natural-language prompts. | `productivity/nano-pdf` |
| `productivity` | **`notion`** | Notion API + ntn CLI: pages, databases, markdown, Workers. | `productivity/notion` |
| `productivity` | **`notion-db-writes`** | Use when writing rows into Notion DBs from headless scripts. | `productivity/notion-db-writes` |
| `productivity` | **`notion-integration`** | Configure and interact with Notion API — search pages, read content, create databases, pages... | `productivity/notion-integration` |
| `productivity` | **`oauth-connection-gateway`** | Usar al construir puertas OAuth y conexiones multi-tenant. | `productivity/oauth-connection-gateway` |
| `productivity` | **`oauth-multi-tenant-integration`** | Designing multi-tenant OAuth connections. | `productivity/oauth-multi-tenant-integration` |
| `productivity` | **`oauth-multi-tenant-integrations`** | Manage multi-tenant OAuth connections and enforcement. | `productivity/oauth-multi-tenant-integrations` |
| `productivity` | **`observability-designer`** | Design production-ready observability strategies combining metrics, logs, and traces. Includ... | `productivity/observability-designer` |
| `productivity` | **`onboarding`** | When the user wants to optimize post-signup onboarding, user activation, first-run experienc... | `productivity/onboarding` |
| `productivity` | **`openhue`** | Control Philips Hue lights, scenes, rooms via OpenHue CLI. | `productivity/openhue` |
| `productivity` | **`paquetes-compliance-promociones`** | T&C multi-empresa: un documento legal por organizador. | `productivity/paquetes-compliance-promociones` |
| `productivity` | **`payment-receipt-alerts`** | Use when un pago por QR (Bre-B) debe alertar al equipo. | `productivity/payment-receipt-alerts` |
| `productivity` | **`pdf`** | PDF files: create, read, merge, fill, OCR, edit text. | `productivity/pdf` |
| `productivity` | **`pokemon-player`** | Play Pokemon via headless emulator + RAM reads. | `productivity/pokemon-player` |
| `productivity` | **`powerpoint`** | Create, read, edit .pptx decks with python-pptx. | `productivity/powerpoint` |
| `productivity` | **`product-price-monitor`** | Watch product, flight, or listing prices; alert on target. | `productivity/product-price-monitor` |
| `productivity` | **`repo-relocation-audit`** | Use when auditing a repo move, read-only. | `productivity/repo-relocation-audit` |
| `productivity` | **`repo-rename`** | Use when renaming a production-wired GitHub repo. | `productivity/repo-rename` |
| `productivity` | **`saas-metrics-coach`** | SaaS financial health advisor. Use when a user shares revenue or customer numbers, or mentio... | `productivity/saas-metrics-coach` |
| `productivity` | **`scan-to-epub-pipeline`** | Convert scanned PDFs to searchable PDF and EPUB via OCR. | `productivity/scan-to-epub-pipeline` |
| `productivity` | **`scheduled-job-diagnosis`** | Use when a scheduled job didn't do its expected action. | `productivity/scheduled-job-diagnosis` |
| `productivity` | **`security-scan-ops`** | Trigger: Strix scan or findings. Verify before fixing. | `productivity/security-scan-ops` |
| `productivity` | **`service-availability-forensics`** | Use when a service flakes or watchdog 'fix' looks false. | `productivity/service-availability-forensics` |
| `productivity` | **`session-librarian`** | Organize sessions by prompt: find, rename, archive, prune. | `productivity/session-librarian` |
| `productivity` | **`siyuan`** | Query and edit a SiYuan knowledge base via its API. | `productivity/siyuan` |
| `productivity` | **`slack-gif-creator`** | Toolkit for creating animated GIFs optimized for Slack, with validators for size constraints... | `productivity/slack-gif-creator` |
| `productivity` | **`slackbot-automation`** | Automate Slackbot tasks via Rube MCP (Composio). Always search tools first for current schemas. | `productivity/slackbot-automation` |
| `productivity` | **`specification-handoff`** | Prepara SPEC/PROMPT para editor de código externo (AGY). | `productivity/specification-handoff` |
| `productivity` | **`static-portal-generator`** | Build multi-client static portals from file inventories. | `productivity/static-portal-generator` |
| `productivity` | **`stripe-integration-expert`** | Production-grade Stripe integrations: subscriptions with trials and proration, one-time paym... | `productivity/stripe-integration-expert` |
| `productivity` | **`teams-meeting-pipeline`** | Teams meeting summaries, job replay, Graph subscriptions. | `productivity/teams-meeting-pipeline` |
| `productivity` | **`telegram-channel-archaeology`** | Use when searching past resources in Telegram channels. | `productivity/telegram-channel-archaeology` |
| `productivity` | **`ua-spoofing-eval`** | Use when a URL fetch is blocked (403/WAF/captcha). | `productivity/ua-spoofing-eval` |
| `productivity` | **`using-agent-skills`** | Discovers and invokes agent skills. Use when starting a session or when you need to discover... | `productivity/using-agent-skills` |
| `productivity` | **`using-superpowers`** | Use when starting any conversation - establishes how to find and use skills, requiring skill... | `productivity/using-superpowers` |
| `productivity` | **`voice-message-transcription`** | Use for voice messages (ptt); transcribe and reply directly. | `productivity/voice-message-transcription` |
| `productivity` | **`web-content-extraction`** | Usa cuando la página es SPA: busca alternate .md endpoint. | `productivity/web-content-extraction` |
| `productivity` | **`web-serving-diagnosis`** | Diagnose VPS web page access issues. | `productivity/web-serving-diagnosis` |
| `productivity` | **`weekly-review-planning`** | Weekly reset: commitments, stalled work, next-week plan. | `productivity/weekly-review-planning` |
| `productivity` | **`writing-skills`** | Use when creating new skills, editing existing skills, or verifying skills work before deplo... | `productivity/writing-skills` |
| `productivity` | **`xlsx`** | Create, read, edit Excel .xlsx workbooks and CSVs. | `productivity/xlsx` |
| `productivity` | **`zoho-automation`** | Automate Zoho tasks via Rube MCP (Composio). Always search tools first for current schemas. | `productivity/zoho-automation` |
| `research` | **`ai-chat-share-extraction`** | Use when reading a public AI-chat share link's content. | `research/ai-chat-share-extraction` |
| `research` | **`arxiv`** | Search arXiv papers by keyword, author, category, or ID. | `research/arxiv` |
| `research` | **`bioinformatics`** | Gateway to 400+ genomics and computational biology skills. | `research/bioinformatics` |
| `research` | **`blogwatcher`** | Monitor blogs and RSS/Atom feeds via blogwatcher-cli tool. | `research/blogwatcher` |
| `research` | **`brain-knowledge-base`** | Implement and maintain a compounding knowledge base (wiki) for business/agency context. Cove... | `research/brain-knowledge-base` |
| `research` | **`code-wiki`** | Generate wiki docs + Mermaid diagrams for any codebase. | `research/code-wiki` |
| `research` | **`competitor-news-monitor`** | Watch named companies for material news; cited digests. | `research/competitor-news-monitor` |
| `research` | **`domain-intel`** | Passive recon of subdomains, SSL certs, WHOIS, and DNS. | `research/domain-intel` |
| `research` | **`drug-discovery`** | Drug discovery: ChEMBL search, drug-likeness, interactions. | `research/drug-discovery` |
| `research` | **`flight-price-research`** | Use when researching flight prices or VPN/geo fares. | `research/flight-price-research` |
| `research` | **`graphify`** | Use for any question about a codebase, its architecture, file relationships, or project cont... | `research/graphify` |
| `research` | **`graphify-codebase-graph`** | Consultar codebases como grafos (sistema graphify) — dependencias, callers, callees, comunid... | `research/graphify-codebase-graph` |
| `research` | **`grounded-citations`** | Ground answers and documents in cited, verifiable sources. | `research/grounded-citations` |
| `research` | **`ingest-pipeline`** | Ingest X/TikTok/GitHub links into wiki + brain + graph. | `research/ingest-pipeline` |
| `research` | **`iterative-retrieval`** | Pattern for progressively refining context retrieval to solve the subagent context problem. ... | `research/iterative-retrieval` |
| `research` | **`knowledge-absorption`** | Absorber y transformar conocimiento desde fuentes externas (Notion, docs, web) hacia el Brai... | `research/knowledge-absorption` |
| `research` | **`llm-wiki`** | Karpathy's LLM Wiki: build/query interlinked markdown KB. | `research/llm-wiki` |
| `research` | **`parallel-cli`** | Agent-native web search, deep research, and enrichment. | `research/parallel-cli` |
| `research` | **`qmd`** | Hybrid local search over notes, docs, and transcripts. | `research/qmd` |
| `research` | **`scrapling`** | Scrape sites with stealth browsing and Cloudflare bypass. | `research/scrapling` |
| `research` | **`searxng-search`** | Free keyless meta-search aggregating 70+ engines. | `research/searxng-search` |
| `research` | **`watchers`** | Poll RSS, JSON APIs, and GitHub with watermark dedup. | `research/watchers` |
| `research` | **`web-fetch`** | HTTP scraping, API requests, and web content extraction with rate-limiting, headers manageme... | `research/web-fetch` |
| `social-media` | **`xurl`** | X/Twitter via xurl CLI: raw post search, posting, DM, media. | `social-media/xurl` |
| `software-development` | **`amazon-sp-api`** | Usar al conectar Seller Central a Amazon SP-API. | `software-development/amazon-sp-api` |
| `software-development` | **`amazon-spapi-integration`** | Use when setting up Amazon SP-API or seller API access. | `software-development/amazon-spapi-integration` |
| `software-development` | **`api-and-interface-design`** | Guides stable API and interface design. Use when designing APIs, module boundaries, or any p... | `software-development/api-and-interface-design` |
| `software-development` | **`ast-grep`** | AST-aware structural code search and rewrite via ast-grep. | `software-development/ast-grep` |
| `software-development` | **`bot-team-architecture`** | Use when designing Hermes multi-agent bot teams/rosters. | `software-development/bot-team-architecture` |
| `software-development` | **`browser-automation`** | Use when the user asks to automate browser tasks, scrape websites, fill forms, capture scree... | `software-development/browser-automation` |
| `software-development` | **`clean-architecture-patterns`** | Clean, Hexagonal, and Screaming Architecture patterns for decoupled, testable, and maintaina... | `software-development/clean-architecture-patterns` |
| `software-development` | **`code-review-and-quality`** | Conducts multi-axis code review. Use before merging any change. Use when reviewing code writ... | `software-development/code-review-and-quality` |
| `software-development` | **`code-simplification`** | Simplifies code for clarity. Use when refactoring code for clarity without changing behavior... | `software-development/code-simplification` |
| `software-development` | **`codebase-inspection`** | Inspect codebases w/ pygount: LOC, languages, ratios. | `software-development/codebase-inspection` |
| `software-development` | **`coljuegos-research`** | Busca en Coljuegos METs y fabricantes de tragamonedas. | `software-development/coljuegos-research` |
| `software-development` | **`cs-product-analyst`** | Product analytics agent for KPI definition, dashboard setup, experiment design, and test res... | `software-development/cs-product-analyst` |
| `software-development` | **`cs-ux-researcher`** | UX research agent for research planning, persona generation, journey mapping, and usability ... | `software-development/cs-ux-researcher` |
| `software-development` | **`database-designer`** | Use when the user asks to design database schemas, plan data migrations, optimize queries, c... | `software-development/database-designer` |
| `software-development` | **`debugging-and-error-recovery`** | Guides systematic root-cause debugging. Use when tests fail, builds break, behavior doesn't ... | `software-development/debugging-and-error-recovery` |
| `software-development` | **`docx-render-verification`** | Use when un DOCX necesita QA visual y LibreOffice no existe. | `software-development/docx-render-verification` |
| `software-development` | **`dogfood`** | Exploratory QA of web apps: find bugs, evidence, reports. | `software-development/dogfood` |
| `software-development` | **`domain-driven-design`** | Domain-Driven Design (DDD) principles: Bounded Contexts, Aggregates, Value Objects, and Ubiq... | `software-development/domain-driven-design` |
| `software-development` | **`duckduckgo-search`** | Free keyless web, news, and image search via ddgs. | `software-development/duckduckgo-search` |
| `software-development` | **`e2e`** | End-to-End testing architecture, multi-service orchestration, test database isolation, and r... | `software-development/e2e` |
| `software-development` | **`electrobun-best-practices`** | Electrobun desktop app development, native webview configurations, CEF bundling, and IPC bri... | `software-development/electrobun-best-practices` |
| `software-development` | **`finishing-a-development-branch`** | Use when implementation is complete, all tests pass, and you need to decide how to integrate... | `software-development/finishing-a-development-branch` |
| `software-development` | **`git-best-practices`** | Git workflow best practices, conventional commits, atomic changes, branch management, intera... | `software-development/git-best-practices` |
| `software-development` | **`git-history-secret-purge`** | Use when secrets (API keys, passwords, .env files, tokens) have been accidentally committed ... | `software-development/git-history-secret-purge` |
| `software-development` | **`git-release`** | Create consistent tagged releases, changelogs, and version bumps with gh release create. | `software-development/git-release` |
| `software-development` | **`github`** | GitHub via gh CLI: PRs, issues, reviews, repos, auth. | `software-development/github` |
| `software-development` | **`github-actions-ci-cd`** | GitHub Actions pipelines, workflow optimization, matrix builds, automated testing, and secur... | `software-development/github-actions-ci-cd` |
| `software-development` | **`github-auth`** | GitHub auth setup: HTTPS tokens, SSH keys, gh CLI login. | `software-development/github-auth` |
| `software-development` | **`github-code-review`** | Review PRs: diffs, inline comments via gh or REST. | `software-development/github-code-review` |
| `software-development` | **`github-issue-to-pr`** | Carry a GitHub issue to a verified PR with honest CI state. | `software-development/github-issue-to-pr` |
| `software-development` | **`github-issues`** | Create, triage, label, assign GitHub issues via gh or REST. | `software-development/github-issues` |
| `software-development` | **`github-pr-workflow`** | GitHub PR lifecycle: branch, commit, open, CI, merge. | `software-development/github-pr-workflow` |
| `software-development` | **`github-repo-ingestion`** | Ingest GitHub repos into Brain Wiki and the Outline wiki. | `software-development/github-repo-ingestion` |
| `software-development` | **`github-repo-management`** | Clone/create/fork repos; manage remotes, releases. | `software-development/github-repo-management` |
| `software-development` | **`go-best-practices`** | Idiomatic Go code, concurrency patterns with goroutines/channels, small interfaces, and robu... | `software-development/go-best-practices` |
| `software-development` | **`go-testing`** | Trigger: Go tests, go test coverage, Bubbletea teatest, golden files. Apply focused Go testi... | `software-development/go-testing` |
| `software-development` | **`google-drive-sheets-ops`** | Use when creating Google Sheets or accessing Drive via API. | `software-development/google-drive-sheets-ops` |
| `software-development` | **`googlebigquery-automation`** | Automate Google BigQuery tasks via Rube MCP (Composio): run SQL queries, explore datasets an... | `software-development/googlebigquery-automation` |
| `software-development` | **`hermes-agent-skill-authoring`** | Author in-repo SKILL.md files: frontmatter and structure. | `software-development/hermes-agent-skill-authoring` |
| `software-development` | **`hermes-desktop-remote-backend`** | Use for Hermes Desktop remote serve and bot profiles. | `software-development/hermes-desktop-remote-backend` |
| `software-development` | **`hermes-desktop-ssh-backend`** | Use when Hermes Desktop connects to a VPS backend via SSH (connection.json mode "ssh") and f... | `software-development/hermes-desktop-ssh-backend` |
| `software-development` | **`hermes-desktop-ssh-diagnostico`** | Use when to connect Hermes Desktop to a VPS backend via SSH and it fails with "remote instal... | `software-development/hermes-desktop-ssh-diagnostico` |
| `software-development` | **`hermes-gateway-http-api`** | Use when exposing Hermes gateway HTTP API for remote login. | `software-development/hermes-gateway-http-api` |
| `software-development` | **`inspecting-hermes-desktop-dom`** | Read the live Hermes desktop DOM/CSS over CDP. | `software-development/inspecting-hermes-desktop-dom` |
| `software-development` | **`memory-architecture`** | Use when routing a fact/procedure to the right memory layer. | `software-development/memory-architecture` |
| `software-development` | **`nextauth-betterauth-url-debug`** | Trigger: invalid callback url, invalid callbackURL, callback URL localhost, login redirect l... | `software-development/nextauth-betterauth-url-debug` |
| `software-development` | **`nextjs-app-router-expert`** | Next.js App Router mastery: Server Actions, Streaming, Parallel/Intercepting Routes, and cac... | `software-development/nextjs-app-router-expert` |
| `software-development` | **`node-inspect-debugger`** | Debug Node.js via --inspect + Chrome DevTools Protocol CLI. | `software-development/node-inspect-debugger` |
| `software-development` | **`onesignal_rest_api-automation`** | Automate OneSignal tasks via Rube MCP (Composio): push notifications, segments, templates, a... | `software-development/onesignal_rest_api-automation` |
| `software-development` | **`outline-wiki-ops`** | Use when operating the Outline wiki API, docs, or backups. | `software-development/outline-wiki-ops` |
| `software-development` | **`owasp-secure-coding`** | OWASP Top 10 prevention, secure coding guidelines, input validation, CSRF, XSS, and authoriz... | `software-development/owasp-secure-coding` |
| `software-development` | **`python-best-practices`** | Idiomatic Python 3.12+, async/await concurrency, Pydantic data modeling, and clean architect... | `software-development/python-best-practices` |
| `software-development` | **`python-debugpy`** | Debug Python: pdb REPL + debugpy remote (DAP). | `software-development/python-debugpy` |
| `software-development` | **`rag-architect`** | Use when the user asks to design a RAG pipeline, choose a chunking strategy or embedding mod... | `software-development/rag-architect` |
| `software-development` | **`ragnar-orchestration`** | Use when orquestando la flota: plan→subplan→worker. | `software-development/ragnar-orchestration` |
| `software-development` | **`react-best-practices`** | Modern React patterns, Server/Client components separation, hook architecture, and performance. | `software-development/react-best-practices` |
| `software-development` | **`receiving-code-review`** | Use when receiving code review feedback, before implementing suggestions, especially if feed... | `software-development/receiving-code-review` |
| `software-development` | **`requesting-code-review`** | Pre-commit review: security scan, quality gates, auto-fix. | `software-development/requesting-code-review` |
| `software-development` | **`rest-graphql-debug`** | Debug REST/GraphQL APIs: status codes, auth, schemas, repro. | `software-development/rest-graphql-debug` |
| `software-development` | **`senior-frontend`** | Frontend development skill for React, Next.js, TypeScript, and Tailwind CSS applications. Us... | `software-development/senior-frontend` |
| `software-development` | **`senior-fullstack`** | Fullstack development toolkit with project scaffolding for Next.js, FastAPI, MERN, and Djang... | `software-development/senior-fullstack` |
| `software-development` | **`senior-qa`** | Generates unit tests, integration tests, and E2E tests for React/Next.js applications. Scans... | `software-development/senior-qa` |
| `software-development` | **`service-agent-code-handoff`** | Use when handing task to AGY/OpenCode/Claude Code. | `software-development/service-agent-code-handoff` |
| `software-development` | **`simplify-code`** | Parallel 4-agent cleanup of recent code changes. | `software-development/simplify-code` |
| `software-development` | **`source-driven-development`** | Grounds every implementation decision in official documentation. Use when you want authorita... | `software-development/source-driven-development` |
| `software-development` | **`spec-best-practices`** | Technical specification design, RFC authoring, acceptance criteria definition, trade-off ana... | `software-development/spec-best-practices` |
| `software-development` | **`spike`** | Throwaway experiments to validate an idea before build. | `software-development/spike` |
| `software-development` | **`sql-database-assistant`** | Use when the user asks to write SQL queries, optimize database performance, generate migrati... | `software-development/sql-database-assistant` |
| `software-development` | **`statistical-analyst`** | Run hypothesis tests, analyze A/B experiment results, calculate sample sizes, and interpret ... | `software-development/statistical-analyst` |
| `software-development` | **`tamagui-best-practices`** | Tamagui UI framework best practices, compiler optimization, multiplatform design tokens, and... | `software-development/tamagui-best-practices` |
| `software-development` | **`test-driven-development`** | TDD: enforce RED-GREEN-REFACTOR, tests before code. | `software-development/test-driven-development` |
| `software-development` | **`testing-best-practices`** | Testing pyramid, unit and integration testing strategies, mocking, test coverage, and mutati... | `software-development/testing-best-practices` |
| `software-development` | **`typescript-best-practices`** | TypeScript strict guidelines, advanced generics, utility types, and type-safe patterns. | `software-development/typescript-best-practices` |
| `software-development` | **`ui-design-system`** | UI design system toolkit for Senior UI Designer including design token generation, component... | `software-development/ui-design-system` |
| `software-development` | **`using-git-worktrees`** | Use when starting feature work that needs isolation from current workspace or before executi... | `software-development/using-git-worktrees` |
| `software-development` | **`vps-ops`** | Unified VPS operations: run OpenCode, Agy, manage Orca worktrees, access host  files, check ... | `software-development/vps-ops` |
| `software-development` | **`websockets-realtime-ops`** | Real-time WebSocket architectures, reconnection strategies, heartbeat mechanisms, and pub/su... | `software-development/websockets-realtime-ops` |
| `software-development` | **`work-unit-commits`** | Plan commits as reviewable work units. Trigger: implementation, commit splitting, chained PR... | `software-development/work-unit-commits` |
| `software-development` | **`zig-best-practices`** | Idiomatic Zig programming, explicit memory allocation, comptime metaprogramming, and error h... | `software-development/zig-best-practices` |
| `specialists` | **`1password`** | Set up op CLI, sign in, and read or inject secrets. | `specialists/monitoring-security/1password` |
| `specialists` | **`3-statement-model`** | Build integrated IS/BS/CF financial workbooks in Excel. | `specialists/marketing/3-statement-model` |
| `specialists` | **`a11y-audit`** | Accessibility audit skill for scanning, fixing, and verifying WCAG 2.2 Level A and AA compli... | `specialists/marketing/a11y-audit` |
| `specialists` | **`ab-testing`** | When the user wants to plan, design, or implement an A/B test or experiment, or build a grow... | `specialists/marketing/ab-testing` |
| `specialists` | **`accelerate`** | Run PyTorch training across GPUs with minimal changes. | `specialists/ai-ml/accelerate` |
| `specialists` | **`activepieces-lead-automation`** | Use when automating lead capture flows in ActivePieces (webhook trigger, SMTP email, Google ... | `specialists/devops-infra/activepieces-lead-automation` |
| `specialists` | **`actual-setup`** | Set up Actual Computer (actual.inc) inference in Hermes. | `specialists/hermes-internal/actual-setup` |
| `specialists` | **`ad-creative`** | When the user wants to generate, iterate, or scale ad creative — headlines, descriptions, pr... | `specialists/marketing/ad-creative` |
| `specialists` | **`ad-library-research`** | Scrape Meta Ad Library and rank ads by longevity, no login. | `specialists/marketing-ads/ad-library-research` |
| `specialists` | **`admin-reporting`** | Reportes al Admin: formato limpio, [SILENT], verificar VPS. | `specialists/monitoring-security/admin-reporting` |
| `specialists` | **`ads`** | When the user wants help with paid advertising campaigns on Google Ads, Meta (Facebook/Insta... | `specialists/marketing/ads` |
| `specialists` | **`adversarial-ux-test`** | Roleplay a hostile user to find and triage UX pain points. | `specialists/general/adversarial-ux-test` |
| `specialists` | **`agent-fleet-botmaker-learnings`** | Use when building or auditing specialist Hermes bots. | `specialists/hermes-internal/agent-fleet-botmaker-learnings` |
| `specialists` | **`agent-roster-blueprint`** | When designing agent rosters: per-bot skills, naming, plan. | `specialists/hermes-internal/agent-roster-blueprint` |
| `specialists` | **`agent-roster-design`** | Design bot rosters: identity, skills, and final reports. | `specialists/hermes-internal/agent-roster-design` |
| `specialists` | **`agent-skill-cataloging`** | Catalog skills per agent/specialist bot (N per bot). | `specialists/hermes-internal/agent-skill-cataloging` |
| `specialists` | **`agent-worktree-orchestration`** | Use when varios agentes editan un repo en paralelo. | `specialists/hermes-internal/agent-worktree-orchestration` |
| `specialists` | **`ai-audio-pronunciation-qa`** | Use when verifying AI voice pronunciation vs a script. | `specialists/media-video/ai-audio-pronunciation-qa` |
| `specialists` | **`ai-seo`** | When the user wants to optimize content for AI search engines, get cited by LLMs, or appear ... | `specialists/marketing/ai-seo` |
| `specialists` | **`ai-video-model-costing`** | Use when comparing AI video model costs for reels. | `specialists/devops-systems/ai-video-model-costing` |
| `specialists` | **`ai-video-pricing-research`** | Video clip (6s) prices on fal.ai and Replicate via curl. | `specialists/devops-systems/ai-video-pricing-research` |
| `specialists` | **`akari-video-editing`** | Edit campaign videos with the Akari AI editor. | `specialists/marketing/akari-video-editing` |
| `specialists` | **`amazon-fba-profitability`** | Complete workflow for evaluating Amazon FBA product profitability: cost analysis, fee calcul... | `specialists/marketing/amazon-fba-profitability` |
| `specialists` | **`amazon-listing-optimization`** | Use when creating Amazon listings. Title, images, bullets. | `specialists/marketing/amazon-listing-optimization` |
| `specialists` | **`amazon-sp-api-listings`** | Trigger: Amazon SP-API, seller central, listing Amazon AU, snuffle mat, FBA fee, create/upda... | `specialists/marketing/amazon-sp-api-listings` |
| `specialists` | **`analytics`** | When the user wants to set up, improve, or audit analytics tracking and measurement. Also us... | `specialists/marketing/analytics` |
| `specialists` | **`analytics-tracking`** | Set up, audit, and debug analytics tracking implementation — GA4, Google Tag Manager, event ... | `specialists/marketing/analytics-tracking` |
| `specialists` | **`anti-ai-slop-writing`** | Produces human-sounding text that avoids detectable AI writing patterns. Activates on any wr... | `specialists/media-video/anti-ai-slop-writing` |
| `specialists` | **`anti-slop`** | Detect and remove AI writing tells ("slop") from prose while preserving the author's voice. ... | `specialists/marketing/anti-slop` |
| `specialists` | **`anti-slop-copy`** | Audita copy para quitar tells de IA antes de publicar. | `specialists/media-video/anti-slop-copy` |
| `specialists` | **`antigravity-cli`** | Operate the Antigravity CLI (agy): plugins, auth, sandbox. | `specialists/hermes-internal/antigravity-cli` |
| `specialists` | **`apollo-automation`** | Automate Apollo.io lead generation -- search organizations, discover contacts, enrich prospe... | `specialists/marketing/apollo-automation` |
| `specialists` | **`application-security-review`** | application-security-review — Review application repos for concrete security issues, especia... | `specialists/monitoring-security/application-security-review` |
| `specialists` | **`arcgis-geospatial-analysis`** | ArcGIS and geospatial analysis: Shapefiles (.shp), GeoJSON, KML, EPSG projections, spatial q... | `specialists/hermes-internal/arcgis-geospatial-analysis` |
| `specialists` | **`attribution`** | When the user wants to figure out which marketing actually drives conversions and revenue, c... | `specialists/marketing/attribution` |
| `specialists` | **`audiocraft-audio-generation`** | AudioCraft: MusicGen text-to-music, AudioGen text-to-sound. | `specialists/devops-systems/audiocraft-audio-generation` |
| `specialists` | **`auditoria-skills-hermes`** | Use when auditando o contando skills de una flota Hermes. | `specialists/hermes-internal/auditoria-skills-hermes` |
| `specialists` | **`axolotl`** | Axolotl: YAML LLM fine-tuning (LoRA, DPO, GRPO). | `specialists/ai-ml/axolotl` |
| `specialists` | **`baoyu-article-illustrator`** | Article illustrations: type × style × palette consistency. | `specialists/media-video/baoyu-article-illustrator` |
| `specialists` | **`baoyu-comic`** | Knowledge comics (知识漫画): educational, biography, tutorial. | `specialists/media-video/baoyu-comic` |
| `specialists` | **`baoyu-translate`** | This skill should be used when the user asks to "translate", "翻译", "精翻", "translate article"... | `specialists/marketing/baoyu-translate` |
| `specialists` | **`brain-graph-operations`** | Use when maintaining or querying the brain knowledge graph. | `specialists/hermes-internal/brain-graph-operations` |
| `specialists` | **`brain-graph-ops`** | Use when operando el grafo del brain. | `specialists/hermes-internal/brain-graph-ops` |
| `specialists` | **`brainstorming`** | You MUST use this before any creative work - creating features, building components, adding ... | `specialists/general/brainstorming` |
| `specialists` | **`branch-pr`** | Create Gentle AI pull requests with issue-first checks. Trigger: creating, opening, or prepa... | `specialists/general/branch-pr` |
| `specialists` | **`brand-art-prompt-briefs`** | Use when: prompts de renders para producer multi-marca. | `specialists/marketing/brand-art-prompt-briefs` |
| `specialists` | **`brand-asset-audit`** | Auditar identidad de marca desde Drive (personajes, reels). | `specialists/devops-systems/brand-asset-audit` |
| `specialists` | **`brand-guidelines`** | When the user wants to apply, document, or enforce brand guidelines for any product or compa... | `specialists/marketing/brand-guidelines` |
| `specialists` | **`brand-logo-composites`** | Combine multiple client logos into one brand image (PIL). | `specialists/marketing/brand-logo-composites` |
| `specialists` | **`browser-backend-replacement`** | Cadena de navegación web por defecto de Ragnar: Agent-Reach (primario) → Obscura (fallback) ... | `specialists/general/browser-backend-replacement` |
| `specialists` | **`campaign-analytics`** | Analyzes campaign performance with multi-touch attribution, funnel conversion analysis, and ... | `specialists/marketing/campaign-analytics` |
| `specialists` | **`campaign-content-intelligence`** | Use when analyzing published campaign content per client. | `specialists/marketing/campaign-content-intelligence` |
| `specialists` | **`campaign-poster-compositing`** | Use when: armar posters con cifras y texto variable. | `specialists/marketing/campaign-poster-compositing` |
| `specialists` | **`campaign-publish-automation`** | Use when automating campaign publishing with human approval. | `specialists/marketing/campaign-publish-automation` |
| `specialists` | **`campaign-script-revision`** | Use when: Revisar guiones con feedback del cliente. | `specialists/marketing/campaign-script-revision` |
| `specialists` | **`campanas-qa-integridad`** | Docs de campaña + gate QA-INTEGRIDAD para el equipo de bots. | `specialists/marketing-ads/campanas-qa-integridad` |
| `specialists` | **`canton-network-repos`** | Canton Network smart contract architecture, Daml integration, LocalNet development, and repo... | `specialists/hermes-internal/canton-network-repos` |
| `specialists` | **`casino-campaign-content`** | Use when writing casino campaign scripts, posters or copy. | `specialists/marketing/casino-campaign-content` |
| `specialists` | **`cfo-advisor`** | Financial leadership for startups and scaling companies. Financial modeling, unit economics,... | `specialists/marketing/cfo-advisor` |
| `specialists` | **`chained-pr`** | Trigger: PRs over 400 lines, stacked PRs, review slices. Split oversized changes into chaine... | `specialists/general/chained-pr` |
| `specialists` | **`channel-economics`** | Use when reviewing or rebalancing direct vs. partner-led channel economics — computing fully... | `specialists/marketing/channel-economics` |
| `specialists` | **`chroma`** | Embedding database for RAG and semantic search. | `specialists/data-vector/chroma` |
| `specialists` | **`client-agent-onboarding`** | Perfilar clientes y generar SOUL.md vía /soul por WhatsApp. | `specialists/hermes-internal/client-agent-onboarding` |
| `specialists` | **`client-agent-soul-survey`** | Encuesta /soul para perfilar clientes y armar su SOUL.md. | `specialists/hermes-internal/client-agent-soul-survey` |
| `specialists` | **`client-connection-flow`** | Use when a new client needs Google accounts connected. | `specialists/hermes-internal/client-connection-flow` |
| `specialists` | **`client-deliverable-manuals`** | Use when creating client operational manuals or guides. | `specialists/hermes-internal/client-deliverable-manuals` |
| `specialists` | **`clip`** | Zero-shot image classification and image-text search. | `specialists/ai-ml/clip` |
| `specialists` | **`cloudflare-temporary-deploy`** | Deploy a Worker live, no account, via wrangler --temporary. | `specialists/devops-infra/cloudflare-temporary-deploy` |
| `specialists` | **`cognitive-doc-design`** | Design docs that reduce cognitive load. Trigger: writing guides, READMEs, RFCs, onboarding, ... | `specialists/media-video/cognitive-doc-design` |
| `specialists` | **`cold-email`** | Write B2B cold emails and follow-up sequences that get replies. Use when the user wants to w... | `specialists/marketing/cold-email` |
| `specialists` | **`colombia-contratos-empresa`** | Contratos y constitución de empresa en Colombia. | `specialists/hermes-internal/colombia-contratos-empresa` |
| `specialists` | **`colombia-promociones-legales`** | Colombian promo legal docs: T&C, datos, juego responsable. | `specialists/marketing-ads/colombia-promociones-legales` |
| `specialists` | **`comfyui`** | Generate images, video, and audio via diffusion workflows. | `specialists/devops-systems/comfyui` |
| `specialists` | **`comment-writer`** | Write warm, direct collaboration comments. Trigger: PR feedback, issue replies, reviews, Sla... | `specialists/general/comment-writer` |
| `specialists` | **`commercial-forecaster`** | Use when building a quarterly bookings forecast, ARR projection, pipeline forecast, NRR proj... | `specialists/marketing/commercial-forecaster` |
| `specialists` | **`competitive-intel`** | Systematic competitor tracking that feeds CMO positioning, CRO battlecards, and CPO roadmap ... | `specialists/marketing/competitive-intel` |
| `specialists` | **`competitor-profiling`** | When the user wants to research, profile, or analyze competitors from their URLs. Also use w... | `specialists/marketing/competitor-profiling` |
| `specialists` | **`composio-social-publishing`** | Publish to Instagram/Facebook via Composio CLI. | `specialists/marketing/composio-social-publishing` |
| `specialists` | **`comps-analysis`** | Build comparable-company valuation workbooks in Excel. | `specialists/marketing/comps-analysis` |
| `specialists` | **`concept-diagrams`** | Generate flat, minimal educational SVG visuals as HTML. | `specialists/general/concept-diagrams` |
| `specialists` | **`content-humanizer`** | Makes AI-generated content sound genuinely human — not just cleaned up, but alive. Use when ... | `specialists/marketing/content-humanizer` |
| `specialists` | **`content-performance-analytics`** | Analyze campaign reel perf: features + platform insights. | `specialists/marketing/content-performance-analytics` |
| `specialists` | **`content-strategy`** | When the user wants to plan a content strategy, decide what content to create, or figure out... | `specialists/marketing/content-strategy` |
| `specialists` | **`context-engineering`** | Optimizes agent context setup. Use when starting a new session, when agent output quality de... | `specialists/hermes-internal/context-engineering` |
| `specialists` | **`context-monitoring`** | Monitor Hermes context window usage, token consumption, and session health via CLI commands ... | `specialists/monitoring-security/context-monitoring` |
| `specialists` | **`context-recovery`** | Recuperar la conversación después de un error del provider (JSON corrupto, 400 errors, conte... | `specialists/hermes-internal/context-recovery` |
| `specialists` | **`coolify-api-operations`** | Trigger: Coolify API, coolify deploy, API token, create admin, ports_mappings, private-deplo... | `specialists/devops-infra/coolify-api-operations` |
| `specialists` | **`copy-dialecto-local`** | Use when el copy debe sonar local (dialecto regional). | `specialists/comms/copy-dialecto-local` |
| `specialists` | **`copywriting`** | When the user wants to write, rewrite, or improve marketing copy for any page — including ho... | `specialists/marketing/copywriting` |
| `specialists` | **`creative-ideation`** | Generate ideas via named methods from creative practice. | `specialists/general/creative-ideation` |
| `specialists` | **`cro`** | When the user wants to optimize, improve, or increase conversions on any marketing page or f... | `specialists/marketing/cro` |
| `specialists` | **`cron-delivery-routing`** | Use when routing or debugging where cron output lands. | `specialists/marketing/cron-delivery-routing` |
| `specialists` | **`cron-fleet-audit`** | Use when auditing every Hermes cron job across profiles. | `specialists/marketing/cron-fleet-audit` |
| `specialists` | **`cron-runtime-verification`** | Use when creating or verifying Hermes cron jobs. | `specialists/marketing/cron-runtime-verification` |
| `specialists` | **`cron-watchdog-scripts`** | Use when creating/debugging Hermes no_agent cron watchdogs. | `specialists/devops-infra/cron-watchdog-scripts` |
| `specialists` | **`cs-demand-gen-specialist`** | Demand generation and acquisition-funnel specialist orchestrating the marketing-demand-acqui... | `specialists/marketing/cs-demand-gen-specialist` |
| `specialists` | **`cunas-de-audio-campana`** | Use when a campaign needs a perifoneo/radio cue. | `specialists/media-video/cunas-de-audio-campana` |
| `specialists` | **`customer-research`** | When the user wants to conduct, analyze, or synthesize customer research. Use when the user ... | `specialists/marketing/customer-research` |
| `specialists` | **`customer-success-manager`** | Monitors customer health, predicts churn risk, and identifies expansion opportunities using ... | `specialists/marketing/customer-success-manager` |
| `specialists` | **`darwinian-evolver`** | Evolve prompts/regex/SQL/code with Imbue's evolution loop. | `specialists/hermes-internal/darwinian-evolver` |
| `specialists` | **`dcf-model`** | Build discounted cash flow valuation workbooks in Excel. | `specialists/marketing/dcf-model` |
| `specialists` | **`dependency-auditor`** | Audit and manage dependencies across multi-language projects. Identifies vulnerabilities, li... | `specialists/marketing/dependency-auditor` |
| `specialists` | **`design-system`** | Captures the user's brand identity once via a 10-question onboarding wizard (primary/accent ... | `specialists/marketing/design-system` |
| `specialists` | **`discord-reporter`** | Send status reports, summaries, and notifications to Discord channels. Use when the user wan... | `specialists/hermes-internal/discord-reporter` |
| `specialists` | **`discord-server-admin`** | Create Discord channels and map them to Hermes profiles. | `specialists/comms/discord-server-admin` |
| `specialists` | **`dispatching-parallel-agents`** | Use when facing 2+ independent tasks that can be worked on without shared state or sequentia... | `specialists/hermes-internal/dispatching-parallel-agents` |
| `specialists` | **`documentation-and-adrs`** | Records decisions and documentation. Use when making architectural decisions, changing publi... | `specialists/devops-infra/documentation-and-adrs` |
| `specialists` | **`dspy`** | DSPy: declarative LM programs, auto-optimize prompts, RAG. | `specialists/ai-ml/dspy` |
| `specialists` | **`elevenlabs-brand-voice`** | Use when: configurar voz de marca ElevenLabs en AKARI. | `specialists/marketing/elevenlabs-brand-voice` |
| `specialists` | **`email-report-cron-aggregator`** | Use when agrego informes diarios y los envio por cron. | `specialists/monitoring-security/email-report-cron-aggregator` |
| `specialists` | **`emails`** | When the user wants to create or optimize an email sequence, drip campaign, automated email ... | `specialists/marketing/emails` |
| `specialists` | **`evaluating-llms-harness`** | lm-eval-harness: benchmark LLMs (MMLU, GSM8K, etc.). | `specialists/ai-ml/evaluating-llms-harness` |
| `specialists` | **`evm`** | Read-only EVM client: wallets, tokens, gas across 8 chains. | `specialists/hermes-internal/evm` |
| `specialists` | **`external-openai-client-config`** | Add OpenAI-compatible providers to Brave or AI clients. | `specialists/hermes-internal/external-openai-client-config` |
| `specialists` | **`facebook-automation`** | Automate Facebook Page management including post creation, scheduling, video uploads, Messen... | `specialists/marketing/facebook-automation` |
| `specialists` | **`faiss`** | Fast vector similarity search at billion scale. | `specialists/data-vector/faiss` |
| `specialists` | **`fastmcp`** | Build, test, and deploy Python MCP servers. | `specialists/hermes-internal/fastmcp` |
| `specialists` | **`finance-lead`** | Startup CFO who builds models that survive contact with reality. Handles fundraising, unit e... | `specialists/marketing/finance-lead` |
| `specialists` | **`flash-attention`** | Speed up long-sequence transformer training and inference. | `specialists/ai-ml/flash-attention` |
| `specialists` | **`form-cro`** | When the user wants to optimize any form that is NOT signup/registration — including lead ca... | `specialists/marketing/form-cro` |
| `specialists` | **`funnel-agendamiento-vsl-pipeline`** | Use when montar un funnel de agendamiento (AP + Twenty). | `specialists/marketing/funnel-agendamiento-vsl-pipeline` |
| `specialists` | **`funnel-deconstruction`** | Deconstruct a received marketing/email/webinar funnel. | `specialists/marketing/funnel-deconstruction` |
| `specialists` | **`gdrive-via-activepieces`** | Use when accessing client Google Drive programmatically. | `specialists/devops-systems/gdrive-via-activepieces` |
| `specialists` | **`gentle-ai-bench`** | Trigger: bench, journey, journeys, driven mode, gentle-ai-bench, journey corpus, j-numbers, ... | `specialists/ai-ml/gentle-ai-bench` |
| `specialists` | **`gitnexus-explorer`** | Serve an interactive codebase knowledge graph web UI. | `specialists/general/gitnexus-explorer` |
| `specialists` | **`godmode`** | Jailbreak LLMs: Parseltongue, GODMODE, ULTRAPLINIAN. | `specialists/monitoring-security/godmode` |
| `specialists` | **`googleads-automation`** | Automate Google Ads analytics tasks via Rube MCP (Composio): list Google Ads links, run GA4 ... | `specialists/marketing/googleads-automation` |
| `specialists` | **`grok`** | Delegate coding to xAI Grok Build CLI (features, PRs). | `specialists/hermes-internal/grok` |
| `specialists` | **`guidance`** | Constrain LLM output with grammars; guarantee valid JSON. | `specialists/ai-ml/guidance` |
| `specialists` | **`guion-validacion-y-brief`** | Use when validating a campaign reel guion before production. | `specialists/marketing/guion-validacion-y-brief` |
| `specialists` | **`guion-video-campana`** | Use when producing campaign reels: production page, prompts. | `specialists/marketing/guion-video-campana` |
| `specialists` | **`guiones-campana-por-canal`** | Use when writing or auditing campaign scripts by channel. | `specialists/marketing-ads/guiones-campana-por-canal` |
| `specialists` | **`handoff`** | Compact the current conversation into a handoff document for another agent to pick up. Save ... | `specialists/marketing/handoff` |
| `specialists` | **`har-derived-api-client`** | Record a site's XHR into a HAR, derive an HTTP client. | `specialists/general/har-derived-api-client` |
| `specialists` | **`here-now`** | Publish sites to {slug}.here.now and store files in Drives. | `specialists/hermes-internal/here-now` |
| `specialists` | **`hermes-admin-operations`** | Operate/config/audit Hermes Agent (provider/gateway). | `specialists/hermes-internal/hermes-admin-operations` |
| `specialists` | **`hermes-bible`** | Use when the user asks for community Hermes Agent knowledge: hidden features, real-world wor... | `specialists/marketing/hermes-bible` |
| `specialists` | **`hermes-bible-study`** | Use when the user asks for community Hermes Agent knowledge: hidden features, real-world wor... | `specialists/hermes-internal/hermes-bible-study` |
| `specialists` | **`hermes-bot-fleet-ops`** | Audit and wire Hermes bot fleets: models, engram, crons. | `specialists/marketing/hermes-bot-fleet-ops` |
| `specialists` | **`hermes-cron-runtime-verification`** | Use when deploying or verifying Hermes cron jobs. | `specialists/marketing/hermes-cron-runtime-verification` |
| `specialists` | **`hermes-desktop-plugins`** | Author, install, and verify Hermes Desktop plugins. | `specialists/hermes-internal/hermes-desktop-plugins` |
| `specialists` | **`hermes-desktop-remote-connection`** | Use when Hermes Desktop remote gateway connection fails. | `specialists/hermes-internal/hermes-desktop-remote-connection` |
| `specialists` | **`hermes-desktop-remote-gateway`** | Desktop to remote gateway: sessions not loading or dropping. | `specialists/hermes-internal/hermes-desktop-remote-gateway` |
| `specialists` | **`hermes-desktop-remote-setup`** | Use when setting up Hermes Desktop remote on a new PC. | `specialists/hermes-internal/hermes-desktop-remote-setup` |
| `specialists` | **`hermes-desktop-windows-troubleshooting`** | Use when Hermes Desktop install/update fails on Windows. | `specialists/hermes-internal/hermes-desktop-windows-troubleshooting` |
| `specialists` | **`hermes-ecosystem-tools`** | Discover/evaluate Hermes Agent community plugins and skills. | `specialists/hermes-internal/hermes-ecosystem-tools` |
| `specialists` | **`hermes-fleet-lifecycle`** | Recover Hermes profile gateways after container recreates. | `specialists/hermes-internal/hermes-fleet-lifecycle` |
| `specialists` | **`hermes-fleet-model-ops`** | Configurar modelos/compresión en flotas Hermes multiperfil. | `specialists/hermes-internal/hermes-fleet-model-ops` |
| `specialists` | **`hermes-gateway-lifecycle-forensics`** | Triage de caídas del gateway Hermes (blip s6 vs crash). | `specialists/hermes-internal/hermes-gateway-lifecycle-forensics` |
| `specialists` | **`hermes-gateway-ops`** | Trigger: perfiles multiplex, profile_routes, plugin install, hermes desktop ssh, ragnar, her... | `specialists/hermes-internal/hermes-gateway-ops` |
| `specialists` | **`hermes-gateway-s6-ops`** | Reinicio seguro del gateway de Hermes bajo s6 en el VPS. | `specialists/hermes-internal/hermes-gateway-s6-ops` |
| `specialists` | **`hermes-latency-diagnosis`** | Bot lento en tareas cortas: medir contexto, 429 y fallback. | `specialists/hermes-internal/hermes-latency-diagnosis` |
| `specialists` | **`hermes-memory-maintenance`** | Reparar memoria: locks/permisos de MEMORY.md y USER.md. | `specialists/hermes-internal/hermes-memory-maintenance` |
| `specialists` | **`hermes-model-rotation`** | Rotate Hermes profile models on new provider models. | `specialists/hermes-internal/hermes-model-rotation` |
| `specialists` | **`hermes-multiprofile-cron-ops`** | Use when running per-profile Hermes cron jobs on Docker VPS. | `specialists/marketing/hermes-multiprofile-cron-ops` |
| `specialists` | **`hermes-multiprofile-model-config`** | Modelos por perfil Hermes y diagnóstico de 401 por keys. | `specialists/hermes-internal/hermes-multiprofile-model-config` |
| `specialists` | **`hermes-permisos-optdata`** | Use when un path de /opt/data no deja escribir al gateway. | `specialists/hermes-internal/hermes-permisos-optdata` |
| `specialists` | **`hermes-prod-stack-operations`** | Use when auditing Hermes prod agents before proposing sends. | `specialists/hermes-internal/hermes-prod-stack-operations` |
| `specialists` | **`hermes-profile-inventory`** | Use when configuring Hermes profiles and their routing. | `specialists/hermes-internal/hermes-profile-inventory` |
| `specialists` | **`hermes-profile-routing`** | Use when routing Hermes profiles/bots across one channel. | `specialists/marketing/hermes-profile-routing` |
| `specialists` | **`hermes-provider-configuration`** | Use when adding providers in Hermes config.yaml. B.AI ref. | `specialists/hermes-internal/hermes-provider-configuration` |
| `specialists` | **`hermes-provider-fallback`** | Cascada de fallback multi-proveedor para bots Hermes. | `specialists/hermes-internal/hermes-provider-fallback` |
| `specialists` | **`hermes-provider-resilience`** | Redundancia y fallback multi-proveedor LLM para Hermes. | `specialists/hermes-internal/hermes-provider-resilience` |
| `specialists` | **`hermes-release-adoption`** | Use when updating Hermes or reporting version/novedades. | `specialists/hermes-internal/hermes-release-adoption` |
| `specialists` | **`hermes-roster-implementation`** | Use when building Hermes bot rosters (specialized agents). | `specialists/hermes-internal/hermes-roster-implementation` |
| `specialists` | **`hermes-scheduled-jobs`** | Use when creating or debugging Hermes cron jobs. | `specialists/comms/hermes-scheduled-jobs` |
| `specialists` | **`hermes-session-forensics`** | Use when a Hermes session expired and context is missing. | `specialists/hermes-internal/hermes-session-forensics` |
| `specialists` | **`hermes-skill-resolution`** | Use when a job runs without its skills (name collision). | `specialists/hermes-internal/hermes-skill-resolution` |
| `specialists` | **`hermes-skills-curator`** | Use when running/auditing the Hermes skills curator. | `specialists/hermes-internal/hermes-skills-curator` |
| `specialists` | **`hermes-skills-hub`** | Complete reference of all 649 Hermes Agent skills across 4 registries (71 Built-in, 57 Optio... | `specialists/hermes-internal/hermes-skills-hub` |
| `specialists` | **`hermes-skills-provisioning`** | Install skills into Hermes profiles from catalogs. | `specialists/hermes-internal/hermes-skills-provisioning` |
| `specialists` | **`hermes-team-ops`** | Roster del equipo y handoff de crons entre perfiles. | `specialists/marketing/hermes-team-ops` |
| `specialists` | **`hermes-usage-cost-audit`** | Audit where LLM tokens go across a Hermes fleet. | `specialists/devops-systems/hermes-usage-cost-audit` |
| `specialists` | **`hermes-vps-home-bind`** | Use when Hermes Desktop (or any SSH session) connects to a VPS but the backend uses the wron... | `specialists/marketing/hermes-vps-home-bind` |
| `specialists` | **`hermes-vps-update`** | Actualizar Hermes Agent en el VPS a upstream/main preservando la config. Triggers: update he... | `specialists/hermes-internal/hermes-vps-update` |
| `specialists` | **`hermes-windows-install`** | Hermes Desktop install fails on Windows (npm error). | `specialists/hermes-internal/hermes-windows-install` |
| `specialists` | **`hermes-workspace-setup`** | Install and configure the Hermes Workspace web UI (outsourc-e/hermes-workspace) as the manag... | `specialists/hermes-internal/hermes-workspace-setup` |
| `specialists` | **`honcho`** | Configure and troubleshoot Honcho memory for Hermes. | `specialists/hermes-internal/honcho` |
| `specialists` | **`huggingface-hub`** | HuggingFace hf CLI: search/download/upload models, datasets. | `specialists/general/huggingface-hub` |
| `specialists` | **`huggingface-tokenizers`** | Fast BPE/WordPiece tokenization and custom vocab training. | `specialists/general/huggingface-tokenizers` |
| `specialists` | **`human-gate`** | Runs the human-verification lane of an agent loop, and proves review happened before work is... | `specialists/marketing/human-gate` |
| `specialists` | **`hyperliquid`** | Hyperliquid market data, account history, trade review. | `specialists/marketing/hyperliquid` |
| `specialists` | **`identity-cleanup`** | Systematic cleanup and update of person identities across Brain Wiki — replacing old names, ... | `specialists/general/identity-cleanup` |
| `specialists` | **`image`** | When the user wants to create, generate, edit, or optimize images for marketing — blog heroe... | `specialists/marketing/image` |
| `specialists` | **`inference-sh-cli`** | Run 150+ AI apps (image, video, LLM) via inference.sh CLI. | `specialists/hermes-internal/inference-sh-cli` |
| `specialists` | **`influencer-marketing`** | When the user wants to run influencer, creator, or ambassador partnerships to promote their ... | `specialists/marketing/influencer-marketing` |
| `specialists` | **`infografia-cliente-html-png`** | Use when un cliente necesita una imagen explicativa. | `specialists/media-video/infografia-cliente-html-png` |
| `specialists` | **`instructor`** | Structured LLM outputs validated with Pydantic. | `specialists/ai-ml/instructor` |
| `specialists` | **`issue-creation`** | Create and triage GitHub issues from repository evidence. Trigger: issue creation, bug repor... | `specialists/hermes-internal/issue-creation` |
| `specialists` | **`jupyter-notebook`** | Iterative Python via live Jupyter kernel (hamelnb). | `specialists/hermes-internal/jupyter-notebook` |
| `specialists` | **`kanban-video-orchestrator`** | Plan and run multi-agent video production pipelines. | `specialists/hermes-internal/kanban-video-orchestrator` |
| `specialists` | **`kassiuss-informe-parser`** | KASSIUSS sales email HTML parser contract and compatibility | `specialists/hermes-internal/kassiuss-informe-parser` |
| `specialists` | **`lambda-labs`** | On-demand GPU cloud instances for ML training. | `specialists/ai-ml/lambda-labs` |
| `specialists` | **`lbo-model`** | Build leveraged buyout workbooks with IRR/MOIC in Excel. | `specialists/marketing/lbo-model` |
| `specialists` | **`lead-magnets`** | When the user wants to create, plan, or optimize a lead magnet for email capture or lead gen... | `specialists/marketing/lead-magnets` |
| `specialists` | **`linkedin-engagement`** | Use when someone wants to grow reach through comments, replies, groups, or outreach on Linke... | `specialists/hermes-internal/linkedin-engagement` |
| `specialists` | **`llama-cpp`** | llama.cpp local GGUF inference + HF Hub model discovery. | `specialists/ai-ml/llama-cpp` |
| `specialists` | **`llava`** | Vision-language chat: VQA, captioning, image dialogue. | `specialists/ai-ml/llava` |
| `specialists` | **`local-vision-toolkit`** | Autonomous local computer vision toolkit — OCR, image analysis, chart detection, infographic... | `specialists/hermes-internal/local-vision-toolkit` |
| `specialists` | **`locate-shared-resource`** | Find a repo/tweet shared via Telegram or Hermes Desktop. | `specialists/hermes-internal/locate-shared-resource` |
| `specialists` | **`market-research`** | Use when doing upstream market-research methodology — sizing a market as TAM/SAM/SOM compute... | `specialists/marketing/market-research` |
| `specialists` | **`marketing-calendar-publishing`** | Use when publishing bingo-sep2026 pieces via Composio. | `specialists/marketing/marketing-calendar-publishing` |
| `specialists` | **`marketing-campaign`** | Generate complete monthly content marketing plans for any casino, bar, restaurant, or entert... | `specialists/marketing/marketing-campaign` |
| `specialists` | **`marketing-campaign-generator-ops`** | Use when editing the marketing-campaign-generator repo. | `specialists/marketing/marketing-campaign-generator-ops` |
| `specialists` | **`marketing-campaign-pipeline`** | Orquesta campañas con bots: contrato, fábrica, review. | `specialists/media-video/marketing-campaign-pipeline` |
| `specialists` | **`marketing-plan`** | When the user needs a comprehensive marketing plan for a client, a company they advise, or t... | `specialists/marketing/marketing-plan` |
| `specialists` | **`marketing-psychology`** | When the user wants to apply psychological principles, mental models, or behavioral science ... | `specialists/marketing/marketing-psychology` |
| `specialists` | **`mcp-oauth-remote-gateway`** | Manual OAuth for remote MCP servers on headless gateways. | `specialists/hermes-internal/mcp-oauth-remote-gateway` |
| `specialists` | **`mcporter`** | List, auth, and call MCP servers/tools from the terminal. | `specialists/hermes-internal/mcporter` |
| `specialists` | **`merge-reconciler`** | Neutral third-party resolution of agent merge conflicts. | `specialists/general/merge-reconciler` |
| `specialists` | **`merger-model`** | Build M&A accretion/dilution workbooks in Excel. | `specialists/marketing/merger-model` |
| `specialists` | **`meta-ads-campaigns`** | Use for Meta Ads clients: campaigns, adsets, ads, pixel. | `specialists/marketing-ads/meta-ads-campaigns` |
| `specialists` | **`meta-ads-operations`** | Run Meta Ads: campaigns, geo, insights, pixel via Composio. | `specialists/marketing-ads/meta-ads-operations` |
| `specialists` | **`metaads-automation`** | Automate Metaads tasks via Rube MCP (Composio). Always search tools first for current schemas. | `specialists/marketing/metaads-automation` |
| `specialists` | **`microsoft-clarity-automation`** | Automate user behavior analytics with Microsoft Clarity -- export heatmap data, session metr... | `specialists/marketing/microsoft-clarity-automation` |
| `specialists` | **`modal`** | Serverless GPU cloud for ML jobs and model APIs. | `specialists/ai-ml/modal` |
| `specialists` | **`monid-seedance-clips`** | Use when generating image2video clips via Monid Seedance. | `specialists/devops-systems/monid-seedance-clips` |
| `specialists` | **`monthly-campaign-calendar-playbook`** | Use when setting up a monthly content campaign calendar. | `specialists/marketing/monthly-campaign-calendar-playbook` |
| `specialists` | **`mpp-agent`** | Pay HTTP 402 APIs via Machine Payments Protocol (MPP). | `specialists/hermes-internal/mpp-agent` |
| `specialists` | **`multi-agent-shared-channel`** | Use when several agents share a channel with no @mentions. | `specialists/hermes-internal/multi-agent-shared-channel` |
| `specialists` | **`nemo-curator`** | Curate LLM training data: dedupe, filter, PII redaction. | `specialists/ai-ml/nemo-curator` |
| `specialists` | **`neuralcrew-campaign-content`** | Copy and guiones for NeuralCrew casino campaigns (Colombia). | `specialists/marketing/neuralcrew-campaign-content` |
| `specialists` | **`neuralcrew-final-report`** | Use when: informe final de cliente en membrete NCL. | `specialists/marketing/neuralcrew-final-report` |
| `specialists` | **`neuralcrew-guion-series-ops`** | Use when: replicar o parafrasear guiones Bingo Millonario. | `specialists/media-video/neuralcrew-guion-series-ops` |
| `specialists` | **`neuralcrew-letterhead`** | Para DOCX de clientes NeuralCrew Labs con membrete. | `specialists/marketing/neuralcrew-letterhead` |
| `specialists` | **`neuroskill-bci`** | Use live BCI cognitive and mood state from NeuroSkill. | `specialists/hermes-internal/neuroskill-bci` |
| `specialists` | **`nginx-certbot-reverse-proxy`** | Use when adding HTTPS domains to apps running behind a shared nginx proxy on Coolify, config... | `specialists/devops-infra/nginx-certbot-reverse-proxy` |
| `specialists` | **`no-ai-slop`** | Edit drafts into sharper, more human writing while preserving the writer's personal voice, o... | `specialists/media-video/no-ai-slop` |
| `specialists` | **`node-webhook-systemd-service`** | Use when deploying Express webhook servers as systemd services on Linux, debugging webhook-t... | `specialists/monitoring-security/node-webhook-systemd-service` |
| `specialists` | **`notification-delivery-reliability`** | Use when a cron message or alert never reached the user. | `specialists/comms/notification-delivery-reliability` |
| `specialists` | **`oauth-connection-door`** | Client OAuth connect pages and per-tenant agent credentials. | `specialists/devops-infra/oauth-connection-door` |
| `specialists` | **`obliteratus`** | OBLITERATUS: abliterate LLM refusals (diff-in-means). | `specialists/monitoring-security/obliteratus` |
| `specialists` | **`ocr-and-documents`** | Extract text from PDFs/scans (pymupdf, marker-pdf). | `specialists/general/ocr-and-documents` |
| `specialists` | **`offers`** | When the user wants to design, construct, or improve an offer — the thing they actually sell... | `specialists/marketing/offers` |
| `specialists` | **`openclaw-migration`** | Import an OpenClaw setup (memories, skills) into Hermes. | `specialists/hermes-internal/openclaw-migration` |
| `specialists` | **`openhands`** | Delegate coding to OpenHands CLI (model-agnostic, LiteLLM). | `specialists/hermes-internal/openhands` |
| `specialists` | **`osint-investigation`** | Follow the money via public records and sanctions data. | `specialists/monitoring-security/osint-investigation` |
| `specialists` | **`oss-forensics`** | GitHub supply-chain forensics: recovery, IOCs, reporting. | `specialists/monitoring-security/oss-forensics` |
| `specialists` | **`outlines`** | Outlines: structured JSON/regex/Pydantic LLM generation. | `specialists/ai-ml/outlines` |
| `specialists` | **`page-agent`** | Embed an in-page natural-language GUI copilot in web apps. | `specialists/hermes-internal/page-agent` |
| `specialists` | **`paid-ads`** | When the user wants help with paid advertising campaigns on Google Ads, Meta (Facebook/Insta... | `specialists/marketing/paid-ads` |
| `specialists` | **`pdf-deliverables`** | Use when user wants a PDF. Generate and send via MEDIA:. | `specialists/monitoring-security/pdf-deliverables` |
| `specialists` | **`peer-agent-handoff`** | Use when handing work to or verifying a peer agent. | `specialists/hermes-internal/peer-agent-handoff` |
| `specialists` | **`peft`** | Fine-tune large LLMs with LoRA on limited GPU memory. | `specialists/ai-ml/peft` |
| `specialists` | **`performance-optimization`** | Optimizes application performance. Use when performance requirements exist, when you suspect... | `specialists/devops-infra/performance-optimization` |
| `specialists` | **`performance-profiler`** | Systematic performance profiling for Node.js, Python, and Go applications. Identifies CPU, m... | `specialists/marketing/performance-profiler` |
| `specialists` | **`persistent-task-manager`** | Manage persistent task tracking across sessions. Maintains Brain Wiki tasks file and syncs w... | `specialists/hermes-internal/persistent-task-manager` |
| `specialists` | **`pinecone`** | Managed vector DB for production RAG and search. | `specialists/data-vector/pinecone` |
| `specialists` | **`pinecone-research`** | Agent RAG and long-term memory with Pinecone. | `specialists/data-vector/pinecone-research` |
| `specialists` | **`pip-install-broken-env`** | Install pip and Python packages in environments where pip is missing, sudo is unavailable, c... | `specialists/hermes-internal/pip-install-broken-env` |
| `specialists` | **`pipeline-informes-ventas-multimarca`** | Runbook to onboard a new brand into the sales pipeline. | `specialists/marketing/pipeline-informes-ventas-multimarca` |
| `specialists` | **`pipelines-con-gate-humano`** | Use when construyendo un flujo por etapas con OK humano. | `specialists/devops-infra/pipelines-con-gate-humano` |
| `specialists` | **`plan`** | Write a markdown plan to .hermes/plans/; no execution. | `specialists/hermes-internal/plan` |
| `specialists` | **`playwright-best-practices`** | Reliable E2E browser automation, Page Object Model, semantic locators, and resilient test fi... | `specialists/hermes-internal/playwright-best-practices` |
| `specialists` | **`polymarket`** | Query Polymarket: markets, prices, orderbooks, history. | `specialists/marketing/polymarket` |
| `specialists` | **`popups`** | When the user wants to create or optimize popups, modals, overlays, slide-ins, or banners fo... | `specialists/marketing/popups` |
| `specialists` | **`postgres-performance-tuning`** | PostgreSQL query optimization, EXPLAIN ANALYZE, indexing strategies, connection pooling, and... | `specialists/devops-infra/postgres-performance-tuning` |
| `specialists` | **`pptx-author`** | Build PowerPoint decks headless with python-pptx. | `specialists/monitoring-security/pptx-author` |
| `specialists` | **`pretext`** | Build creative browser demos with DOM-free text layout. | `specialists/hermes-internal/pretext` |
| `specialists` | **`pricing`** | When the user wants help with pricing decisions, packaging, or monetization strategy. Also u... | `specialists/marketing/pricing` |
| `specialists` | **`product-analytics`** | Use when defining product KPIs, building metric dashboards, running cohort or retention anal... | `specialists/marketing/product-analytics` |
| `specialists` | **`prompt-engineer-toolkit`** | Turns marketing prompts into tested, versioned production assets: A/B prompt evaluation agai... | `specialists/marketing/prompt-engineer-toolkit` |
| `specialists` | **`prospecting`** | When the user wants to find, qualify, and build a list of prospects to reach out to — across... | `specialists/marketing/prospecting` |
| `specialists` | **`provider-manager`** | Manage AI LLM providers, models, context windows, and active defaults in Hermes Agent config... | `specialists/hermes-internal/provider-manager` |
| `specialists` | **`public-relations`** | When the user wants help with public relations, earned media, press coverage, journalist out... | `specialists/marketing/public-relations` |
| `specialists` | **`pytorch-fsdp`** | Fully sharded data-parallel training for large models. | `specialists/ai-ml/pytorch-fsdp` |
| `specialists` | **`pytorch-lightning`** | Clean training loops with built-in distributed support. | `specialists/ai-ml/pytorch-lightning` |
| `specialists` | **`qdrant`** | Vector search engine for production RAG systems. | `specialists/data-vector/qdrant` |
| `specialists` | **`raffle-winner-picker`** | Picks random winners from lists, spreadsheets, or Google Sheets for giveaways, raffles, and ... | `specialists/marketing/raffle-winner-picker` |
| `specialists` | **`rag-architecture-expert`** | Retrieval-Augmented Generation (RAG) architecture, hybrid search, reciprocal rank fusion, an... | `specialists/data-vector/rag-architecture-expert` |
| `specialists` | **`redis-caching-patterns`** | Redis caching patterns, distributed locking (Redlock), rate limiting, Pub/Sub, and TTL strat... | `specialists/devops-infra/redis-caching-patterns` |
| `specialists` | **`reel-audio-mixing`** | Use when mounting brand TTS voice onto a paid reel clip. | `specialists/marketing/reel-audio-mixing` |
| `specialists` | **`reel-brand-voice-dubbing`** | Voz de marca en reels: Monid → STTS ElevenLabs → CapCut. | `specialists/marketing/reel-brand-voice-dubbing` |
| `specialists` | **`reel-clip-qa`** | Use when approving or debugging a Seedance/Monid reel clip. | `specialists/ai-ml/reel-clip-qa` |
| `specialists` | **`reel-portal-protocol`** | Use when producing campaign reel pieces for the NC portal. | `specialists/marketing/reel-portal-protocol` |
| `specialists` | **`research-paper-writing`** | Write ML papers for NeurIPS/ICML/ICLR: design→submit. | `specialists/general/research-paper-writing` |
| `specialists` | **`revenue-operations`** | Analyzes sales pipeline health, revenue forecasting accuracy, and go-to-market efficiency me... | `specialists/marketing/revenue-operations` |
| `specialists` | **`revops`** | When the user wants help with revenue operations, lead lifecycle management, or marketing-to... | `specialists/marketing/revops` |
| `specialists` | **`saelens`** | Train sparse autoencoders to interpret model features. | `specialists/ai-ml/saelens` |
| `specialists` | **`sales-enablement`** | When the user wants to create sales collateral, pitch decks, one-pagers, objection handling ... | `specialists/marketing/sales-enablement` |
| `specialists` | **`scene-consistency-qa`** | QA de consistencia de personaje en stills de escenas IA. | `specialists/devops-systems/scene-consistency-qa` |
| `specialists` | **`scene-keyframe-qa-lipsync`** | Use when: QA keyframes 9:16 y prep de lip-sync Seedance. | `specialists/media-video/scene-keyframe-qa-lipsync` |
| `specialists` | **`security-and-hardening`** | Hardens code against vulnerabilities. Use when handling user input, authentication, data sto... | `specialists/monitoring-security/security-and-hardening` |
| `specialists` | **`segment-anything-model`** | SAM: zero-shot image segmentation via points, boxes, masks. | `specialists/general/segment-anything-model` |
| `specialists` | **`senior-architect`** | This skill should be used when the user asks to "design system architecture", "evaluate micr... | `specialists/marketing/senior-architect` |
| `specialists` | **`senior-data-scientist`** | World-class senior data scientist skill specialising in statistical modeling, experiment des... | `specialists/marketing/senior-data-scientist` |
| `specialists` | **`seo-audit`** | When the user wants to audit, review, or diagnose SEO issues on their site. Also use when th... | `specialists/marketing/seo-audit` |
| `specialists` | **`serving-llms-vllm`** | vLLM: high-throughput LLM serving, OpenAI API, quantization. | `specialists/ai-ml/serving-llms-vllm` |
| `specialists` | **`sherlock`** | Find accounts for a username across 400+ platforms. | `specialists/monitoring-security/sherlock` |
| `specialists` | **`shop`** | Shop catalog search, checkout, order tracking, returns. | `specialists/comms/shop` |
| `specialists` | **`shopify`** | Query Shopify Admin/Storefront GraphQL APIs via curl. | `specialists/marketing/shopify` |
| `specialists` | **`signup`** | When the user wants to optimize signup, registration, account creation, or trial activation ... | `specialists/marketing/signup` |
| `specialists` | **`simple-english`** | Rewrite text to ASD-STE100 Simplified Technical English. | `specialists/hermes-internal/simple-english` |
| `specialists` | **`simpo`** | Reference-free preference alignment, simpler than DPO. | `specialists/ai-ml/simpo` |
| `specialists` | **`site-architecture`** | When the user wants to plan, map, or restructure their website's page hierarchy, navigation,... | `specialists/marketing/site-architecture` |
| `specialists` | **`skill-auditor`** | skill-auditor — Use when auditing, reviewing, or grading Hermes skills for quality. Checks t... | `specialists/hermes-internal/skill-auditor` |
| `specialists` | **`skill-creator`** | Trigger: new skills, agent instructions, documenting AI usage patterns. Create LLM-first ski... | `specialists/hermes-internal/skill-creator` |
| `specialists` | **`skill-improver`** | Trigger: improve skills, audit skills, refactor skills, skill quality. Audit and upgrade exi... | `specialists/hermes-internal/skill-improver` |
| `specialists` | **`skill-navigator`** | Navigate, query, and compose skills and execution pipelines using the skills knowledge graph... | `specialists/hermes-internal/skill-navigator` |
| `specialists` | **`skill-registry`** | Trigger: update skills, skill registry, actualizar skills, after skill changes. Index availa... | `specialists/hermes-internal/skill-registry` |
| `specialists` | **`slime`** | RL post-training for LLMs with Megatron and SGLang. | `specialists/ai-ml/slime` |
| `specialists` | **`sms`** | When the user wants to plan, build, or optimize SMS or MMS marketing — including welcome flo... | `specialists/marketing/sms` |
| `specialists` | **`social`** | When the user wants help creating, scheduling, or optimizing social media content for Linked... | `specialists/marketing/social` |
| `specialists` | **`social-media-analyzer`** | Social media campaign analysis and performance tracking. Calculates engagement rates, ROI, a... | `specialists/marketing/social-media-analyzer` |
| `specialists` | **`social-media-content-calendar`** | Plan multi-platform social campaigns: briefs to posting. | `specialists/marketing/social-media-content-calendar` |
| `specialists` | **`social-piece-publishing-ops`** | Use when publishing or verifying social posts via Composio. | `specialists/marketing/social-piece-publishing-ops` |
| `specialists` | **`solana`** | Query Solana wallets, tokens, txs, and NFTs in USD. | `specialists/hermes-internal/solana` |
| `specialists` | **`soul`** | Encuesta /soul para perfilar al cliente y generar su SOUL.md sin desvíos conversacionales. | `specialists/hermes-internal/soul` |
| `specialists` | **`spanish-deliverable-proofreading`** | Check Spanish doc typos before delivering as PDF or DOCX. | `specialists/media-video/spanish-deliverable-proofreading` |
| `specialists` | **`spec-driven-development`** | Use when doing SDD or designing multi-agent rosters. | `specialists/hermes-internal/spec-driven-development` |
| `specialists` | **`ssot-context-document`** | Crear un documento integral Single Source of Truth (.md) consolidando toda la información di... | `specialists/hermes-internal/ssot-context-document` |
| `specialists` | **`stable-diffusion`** | Text-to-image generation, inpainting, and img2img. | `specialists/devops-systems/stable-diffusion` |
| `specialists` | **`stocks`** | Stock quotes, history, search, compare, crypto via Yahoo. | `specialists/marketing/stocks` |
| `specialists` | **`stripe-link-cli`** | Agent payments via Stripe Link — cards, SPT, approvals. | `specialists/hermes-internal/stripe-link-cli` |
| `specialists` | **`stripe-projects`** | Provision SaaS services + sync creds via Stripe Projects. | `specialists/hermes-internal/stripe-projects` |
| `specialists` | **`systemic-issue-triage`** | Trigger: new issue, bug report, triage, backlog, issue flood, community report, root cause, ... | `specialists/hermes-internal/systemic-issue-triage` |
| `specialists` | **`tailwind-design-system`** | Scalable Tailwind CSS systems, design tokens, component architecture, and accessibility comp... | `specialists/devops-infra/tailwind-design-system` |
| `specialists` | **`telephony`** | Provision Twilio numbers, SMS/MMS, and AI outbound calls. | `specialists/comms/telephony` |
| `specialists` | **`tensorrt-llm`** | High-throughput LLM inference on NVIDIA GPUs. | `specialists/ai-ml/tensorrt-llm` |
| `specialists` | **`tiktok-ingestion`** | Trigger: el grupo TikToks recibe un enlace de video corto. | `specialists/hermes-internal/tiktok-ingestion` |
| `specialists` | **`torchtitan`** | Pretrain LLMs at scale with PyTorch 4D parallelism. | `specialists/ai-ml/torchtitan` |
| `specialists` | **`trl-fine-tuning`** | TRL: SFT, DPO, GRPO, RLOO reward modeling for LLM RLHF. | `specialists/ai-ml/trl-fine-tuning` |
| `specialists` | **`twitter-telegram-ingestion`** | X/Twitter link in Links de X: extract, enrich, save, reply. | `specialists/hermes-internal/twitter-telegram-ingestion` |
| `specialists` | **`two-way-sync-state-integrity`** | Use when a canonical store syncs an editable mirror. | `specialists/devops-infra/two-way-sync-state-integrity` |
| `specialists` | **`unbroker`** | Autonomously remove your info from data-broker sites. | `specialists/monitoring-security/unbroker` |
| `specialists` | **`unsloth`** | Unsloth: 2-5x faster LoRA/QLoRA fine-tuning, less VRAM. | `specialists/ai-ml/unsloth` |
| `specialists` | **`vendor-pricing-research`** | Use when comparing live API/model pricing across providers. | `specialists/hermes-internal/vendor-pricing-research` |
| `specialists` | **`verification-before-completion`** | Use when about to claim work is complete, fixed, or passing, before committing or creating P... | `specialists/hermes-internal/verification-before-completion` |
| `specialists` | **`verification-loop`** | Comprehensive multi-phase verification system. Use after completing a feature, before creati... | `specialists/devops-infra/verification-loop` |
| `specialists` | **`video`** | When the user wants to create, generate, or produce video content using AI tools or programm... | `specialists/marketing/video` |
| `specialists` | **`video-ai-generator`** | End-to-end 9:16 vertical AI video generation pipeline (Reels, TikTok, Shorts) with ActivePie... | `specialists/comms/video-ai-generator` |
| `specialists` | **`video-content-strategist`** | Use when planning video content strategy, writing video scripts, optimizing YouTube channels... | `specialists/marketing/video-content-strategist` |
| `specialists` | **`vps-agent-deployer`** | Zero-friction, fully automated provisioning and deployment skill for multi-agent Docker arch... | `specialists/devops-infra/vps-agent-deployer` |
| `specialists` | **`vscode-ai-extension-configuration`** | Configure VSCode AI extensions (OpenCode, Continue, Copilot) and connect custom APIs like Na... | `specialists/hermes-internal/vscode-ai-extension-configuration` |
| `specialists` | **`web-pentest`** | Authorized web pentest: recon, proof-based exploits, report. | `specialists/monitoring-security/web-pentest` |
| `specialists` | **`web-performance-core-vitals`** | Web performance optimization, Core Web Vitals (LCP, INP, CLS), bundle analysis, and renderin... | `specialists/devops-infra/web-performance-core-vitals` |
| `specialists` | **`webhook-gateway-multiclient`** | Trigger: webhook gateway, widget chat, bridge Hermes, leads to postgres, ActivePieces notify... | `specialists/devops-infra/webhook-gateway-multiclient` |
| `specialists` | **`webinar-marketing`** | When the user wants to plan, promote, run, or improve a webinar or virtual event to generate... | `specialists/marketing/webinar-marketing` |
| `specialists` | **`weights-and-biases`** | W&B: log ML experiments, sweeps, model registry, dashboards. | `specialists/ai-ml/weights-and-biases` |
| `specialists` | **`whisper`** | Transcribe and translate speech in 99 languages. | `specialists/comms/whisper` |
| `specialists` | **`wiki-entry-creation`** | Create structured wiki entries from documentation, config files, and session knowledge when ... | `specialists/hermes-internal/wiki-entry-creation` |
| `specialists` | **`x-tweet-scrape`** | Extract tweet content from X/Twitter status URLs using fx(fixupx.com metadata extraction, Ni... | `specialists/hermes-internal/x-tweet-scrape` |
| `specialists` | **`x-twitter-growth`** | X/Twitter growth engine for building audience, crafting viral content, and analyzing engagem... | `specialists/marketing/x-twitter-growth` |
| `specialists` | **`yuanbao`** | Yuanbao (元宝) groups: @mention users, query info/members. | `specialists/hermes-internal/yuanbao` |
| `specialists` | **`zmx`** | Zellij and Tmux multiplexer session management, background task isolation, and multi-termina... | `specialists/hermes-internal/zmx` |
| `web` | **`blocked-page-recovery`** | Use when a fetch fails: 403/429, paywall, WAF, bot wall. | `web/blocked-page-recovery` |
