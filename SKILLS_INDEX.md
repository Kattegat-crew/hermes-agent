# Índice Canónico de Skills — Flota Hermes
> **Última sincronización**: 2026-09-20 01:58 | **Total de skills**: 431

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
| `creative` | **`architecture-diagram`** | Dark-themed SVG architecture/cloud/infra diagrams as HTML. | `creative/architecture-diagram` |
| `creative` | **`ascii-art`** | ASCII art: pyfiglet, cowsay, boxes, image-to-ascii. | `creative/ascii-art` |
| `creative` | **`ascii-video`** | ASCII video: convert video/audio to colored ASCII MP4/GIF. | `creative/ascii-video` |
| `creative` | **`baoyu-infographic`** | Infographics: 21 layouts x 21 styles (信息图, 可视化). | `creative/baoyu-infographic` |
| `creative` | **`claude-design`** | Design one-off HTML artifacts (landing, deck, prototype). | `creative/claude-design` |
| `creative` | **`design-md`** | Author/validate/export Google's DESIGN.md token spec files. | `creative/design-md` |
| `creative` | **`draw-your-font`** | Turn a handwriting photo into an installable TTF font. | `creative/draw-your-font` |
| `creative` | **`excalidraw`** | Hand-drawn Excalidraw JSON diagrams (arch, flow, seq). | `creative/excalidraw` |
| `creative` | **`guion-reel-mesa-medida`** | Use when escribiendo o midiendo un guion de reel de campana. | `creative/guion-reel-mesa-medida` |
| `creative` | **`heartmula`** | HeartMuLa: Suno-like song generation from lyrics + tags. | `creative/heartmula` |
| `creative` | **`humanizer`** | Humanize text: strip AI-isms and add real voice. | `creative/humanizer` |
| `creative` | **`hyperframes`** | Render MP4/WebM videos from HTML compositions. | `creative/hyperframes` |
| `creative` | **`manim-video`** | Manim CE animations: 3Blue1Brown math/algo videos. | `creative/manim-video` |
| `creative` | **`meme-generation`** | Create meme PNGs from templates with Pillow text overlay. | `creative/meme-generation` |
| `creative` | **`neuralcrew-bot-avatars`** | Use when: instalar/actualizar avatar de un bot NeuralCrew. | `creative/neuralcrew-bot-avatars` |
| `creative` | **`open-design`** | Use the Open Design workbench to create editable visual projects, prototypes, landing pages,... | `creative/open-design` |
| `creative` | **`openai-image-gen`** | Generate visual assets, marketing graphics, and concept art using OpenAI image generation AP... | `creative/openai-image-gen` |
| `creative` | **`p5js`** | p5.js sketches: gen art, shaders, interactive, 3D. | `creative/p5js` |
| `creative` | **`pixel-art`** | Pixel art w/ era palettes (NES, Game Boy, PICO-8). | `creative/pixel-art` |
| `creative` | **`popular-web-designs`** | 54 real design systems (Stripe, Linear, Vercel) as HTML/CSS. | `creative/popular-web-designs` |
| `creative` | **`reel-pipeline`** | Genera videos tipo reel verticales 9:16 con IA. Soporta texto-a-video e imagen-a-video. Usa ... | `creative/reel-pipeline` |
| `creative` | **`sesion-pieza-por-pieza`** | Use when producing a campaign video piece-by-piece. | `creative/sesion-pieza-por-pieza` |
| `creative` | **`sketch`** | Throwaway HTML mockups: 2-3 design variants to compare. | `creative/sketch` |
| `creative` | **`songwriting-and-ai-music`** | Songwriting craft and Suno AI music prompts. | `creative/songwriting-and-ai-music` |
| `creative` | **`tldraw-offline`** | Drive and script tldraw offline canvases with an agent. | `creative/tldraw-offline` |
| `creative` | **`touchdesigner-mcp`** | Control TouchDesigner via twozero MCP. | `creative/touchdesigner-mcp` |
| `creative` | **`unreal-mcp`** | Automate Unreal Engine editor scenes, actors, and renders. | `creative/unreal-mcp` |
| `creative` | **`video-tts-pronunciation-fix`** | Fix Spanish TTS pronunciation in video reels via respelling. | `creative/video-tts-pronunciation-fix` |
| `devops` | **`atlas-best-practices`** | Atlas database schema management, declarative migrations, schema diffing, and database CI/CD... | `devops/atlas-best-practices` |
| `devops` | **`change-attribution-reports`** | Use when asked who changed what in a project recently. | `devops/change-attribution-reports` |
| `devops` | **`cloudflare-access-api`** | Trigger: Cloudflare Access, Zero Trust, protect subdomain, Access policy, one-time PIN login... | `devops/cloudflare-access-api` |
| `devops` | **`cloudflare-dns-cutover`** | Trigger: Cloudflare DNS, A record, cutover, TTL 300, SSL mode full, zone DNS edit, origin IP... | `devops/cloudflare-dns-cutover` |
| `devops` | **`coolify-secure-secrets`** | Use when deploying apps or databases in Coolify, managing encrypted secrets in Coolify's dat... | `devops/coolify-secure-secrets` |
| `devops` | **`docuseal-selfhost-ops`** | Trigger: docuseal, firma electronica, contrato roto, link de firma, firmante no puede firmar... | `devops/docuseal-selfhost-ops` |
| `devops` | **`formbricks-v5-selfhost`** | Trigger: Formbricks, formbricks v5, formbricks self-hosted, formbricks deploy/reset, error a... | `devops/formbricks-v5-selfhost` |
| `devops` | **`hermes-desktop-gateway-support`** | Use when Hermes Desktop no conecta al gateway remoto. | `devops/hermes-desktop-gateway-support` |
| `devops` | **`hermes-production-deployment`** | Production deployment of Hermes agents for multiple clients. Includes: full VPS setup plan w... | `devops/hermes-production-deployment` |
| `devops` | **`hermes-relocation-ops`** | Use when asked to relocate an agent: guild, token, or host. | `devops/hermes-relocation-ops` |
| `devops` | **`hermes-s6-container-supervision`** | Modify or debug s6 services in the Hermes Docker image. | `devops/hermes-s6-container-supervision` |
| `devops` | **`host-infra-forensics`** | Use when a service is unreachable from a remote client. | `devops/host-infra-forensics` |
| `devops` | **`multi-profile-cron-reliability`** | Harden failing profile crons via pinning and skill links. | `devops/multi-profile-cron-reliability` |
| `devops` | **`nginx-proxy-manager-api`** | Trigger: NPM, Nginx Proxy Manager, proxy host, Let's Encrypt DNS challenge, certificate API,... | `devops/nginx-proxy-manager-api` |
| `devops` | **`nix-best-practices`** | Nix Flakes, reproducible dev environments, direnv integration, and declarative package manag... | `devops/nix-best-practices` |
| `devops` | **`orbstack-best-practices`** | OrbStack fast container and Linux machine management, performance tuning, Rosetta 2 emulatio... | `devops/orbstack-best-practices` |
| `devops` | **`pinggy-tunnel`** | Zero-install localhost tunnels over SSH via Pinggy. | `devops/pinggy-tunnel` |
| `devops` | **`sdlc-review`** | Review Kanban handoffs and route verified outcomes. | `devops/sdlc-review` |
| `devops` | **`tilt`** | Tilt multi-service local development, live updates, health checks, and Kubernetes/Docker Com... | `devops/tilt` |
| `devops` | **`twenty-selfhost-auth`** | Trigger: Twenty CRM login, Twenty signup disabled, create Twenty user, twenty workspace role... | `devops/twenty-selfhost-auth` |
| `devops` | **`unify-service-logins`** | Trigger: único usuario, unify logins, cambiar admin, reset password, captain@neuralcrewlabs.... | `devops/unify-service-logins` |
| `devops` | **`vps-host-repo-access`** | Acceder a repos del host VPS desde el contenedor. | `devops/vps-host-repo-access` |
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
| `productivity` | **`document-reader`** | Universal document reader that parses .docx, .xlsx, .pdf, .pptx, .odt, .ods, .odp, .rtf, .tx... | `productivity/document-reader` |
| `productivity` | **`document-to-action-items`** | Extract cited obligations, deadlines, tasks from documents. | `productivity/document-to-action-items` |
| `productivity` | **`docx`** | Create, read, edit, template, and review Word .docx files. | `productivity/docx` |
| `productivity` | **`excel-author`** | Build auditable financial workbooks headless via openpyxl. | `productivity/excel-author` |
| `productivity` | **`fitness-nutrition`** | Workout planning, macros, and body metrics via wger/USDA. | `productivity/fitness-nutrition` |
| `productivity` | **`flujos-con-gates-humanos`** | Use when disenando flujos con gates humanos y firma. | `productivity/flujos-con-gates-humanos` |
| `productivity` | **`gmail-mailbox-organization`** | Label, archive and filter Gmail mailboxes safely, verified. | `productivity/gmail-mailbox-organization` |
| `productivity` | **`gmail-smtp-app-password`** | Trigger: SMTP, smtp.gmail.com, app password, send from, DocuSeal mail, Google Workspace emai... | `productivity/gmail-smtp-app-password` |
| `productivity` | **`google-docs-api`** | Work around Google Docs API limitations when creating documents with content. Key issue: doc... | `productivity/google-docs-api` |
| `productivity` | **`google-workspace`** | Gmail, Calendar, Drive, Docs, Sheets via gws CLI or Python. | `productivity/google-workspace` |
| `productivity` | **`gws-shared-access`** | Google Workspace via root token+venv from sub-profiles. | `productivity/gws-shared-access` |
| `productivity` | **`maps`** | Geocode, POIs, routes, timezones via OpenStreetMap/OSRM. | `productivity/maps` |
| `productivity` | **`meeting-action-items`** | Turn meeting notes into cited decisions, owners, tickets. | `productivity/meeting-action-items` |
| `productivity` | **`memento-flashcards`** | Spaced-repetition flashcards: create, review, quiz, export. | `productivity/memento-flashcards` |
| `productivity` | **`minecraft-modpack-server`** | Host modded Minecraft servers (CurseForge, Modrinth). | `productivity/minecraft-modpack-server` |
| `productivity` | **`nano-pdf`** | Edit text in existing PDFs via natural-language prompts. | `productivity/nano-pdf` |
| `productivity` | **`notion`** | Notion API + ntn CLI: pages, databases, markdown, Workers. | `productivity/notion` |
| `productivity` | **`notion-integration`** | Configure and interact with Notion API — search pages, read content, create databases, pages... | `productivity/notion-integration` |
| `productivity` | **`openhue`** | Control Philips Hue lights, scenes, rooms via OpenHue CLI. | `productivity/openhue` |
| `productivity` | **`pdf`** | PDF files: create, read, merge, fill, OCR, edit text. | `productivity/pdf` |
| `productivity` | **`pokemon-player`** | Play Pokemon via headless emulator + RAM reads. | `productivity/pokemon-player` |
| `productivity` | **`powerpoint`** | Create, read, edit .pptx decks with python-pptx. | `productivity/powerpoint` |
| `productivity` | **`product-price-monitor`** | Watch product, flight, or listing prices; alert on target. | `productivity/product-price-monitor` |
| `productivity` | **`session-librarian`** | Organize sessions by prompt: find, rename, archive, prune. | `productivity/session-librarian` |
| `productivity` | **`siyuan`** | Query and edit a SiYuan knowledge base via its API. | `productivity/siyuan` |
| `productivity` | **`teams-meeting-pipeline`** | Teams meeting summaries, job replay, Graph subscriptions. | `productivity/teams-meeting-pipeline` |
| `productivity` | **`using-agent-skills`** | Discovers and invokes agent skills. Use when starting a session or when you need to discover... | `productivity/using-agent-skills` |
| `productivity` | **`using-superpowers`** | Use when starting any conversation - establishes how to find and use skills, requiring skill... | `productivity/using-superpowers` |
| `productivity` | **`weekly-review-planning`** | Weekly reset: commitments, stalled work, next-week plan. | `productivity/weekly-review-planning` |
| `productivity` | **`writing-skills`** | Use when creating new skills, editing existing skills, or verifying skills work before deplo... | `productivity/writing-skills` |
| `productivity` | **`xlsx`** | Create, read, edit Excel .xlsx workbooks and CSVs. | `productivity/xlsx` |
| `research` | **`ai-chat-share-extraction`** | Use when reading a public AI-chat share link's content. | `research/ai-chat-share-extraction` |
| `research` | **`arxiv`** | Search arXiv papers by keyword, author, category, or ID. | `research/arxiv` |
| `research` | **`bioinformatics`** | Gateway to 400+ genomics and computational biology skills. | `research/bioinformatics` |
| `research` | **`blogwatcher`** | Monitor blogs and RSS/Atom feeds via blogwatcher-cli tool. | `research/blogwatcher` |
| `research` | **`code-wiki`** | Generate wiki docs + Mermaid diagrams for any codebase. | `research/code-wiki` |
| `research` | **`competitor-news-monitor`** | Watch named companies for material news; cited digests. | `research/competitor-news-monitor` |
| `research` | **`domain-intel`** | Passive recon of subdomains, SSL certs, WHOIS, and DNS. | `research/domain-intel` |
| `research` | **`drug-discovery`** | Drug discovery: ChEMBL search, drug-likeness, interactions. | `research/drug-discovery` |
| `research` | **`graphify`** | Use for any question about a codebase, its architecture, file relationships, or project cont... | `research/graphify` |
| `research` | **`graphify-codebase-graph`** | Consultar codebases como grafos (sistema graphify) — dependencias, callers, callees, comunid... | `research/graphify-codebase-graph` |
| `research` | **`grounded-citations`** | Ground answers and documents in cited, verifiable sources. | `research/grounded-citations` |
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
| `software-development` | **`api-and-interface-design`** | Guides stable API and interface design. Use when designing APIs, module boundaries, or any p... | `software-development/api-and-interface-design` |
| `software-development` | **`ast-grep`** | AST-aware structural code search and rewrite via ast-grep. | `software-development/ast-grep` |
| `software-development` | **`clean-architecture-patterns`** | Clean, Hexagonal, and Screaming Architecture patterns for decoupled, testable, and maintaina... | `software-development/clean-architecture-patterns` |
| `software-development` | **`code-review-and-quality`** | Conducts multi-axis code review. Use before merging any change. Use when reviewing code writ... | `software-development/code-review-and-quality` |
| `software-development` | **`code-simplification`** | Simplifies code for clarity. Use when refactoring code for clarity without changing behavior... | `software-development/code-simplification` |
| `software-development` | **`codebase-inspection`** | Inspect codebases w/ pygount: LOC, languages, ratios. | `software-development/codebase-inspection` |
| `software-development` | **`debugging-and-error-recovery`** | Guides systematic root-cause debugging. Use when tests fail, builds break, behavior doesn't ... | `software-development/debugging-and-error-recovery` |
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
| `software-development` | **`hermes-agent-skill-authoring`** | Author in-repo SKILL.md files: frontmatter and structure. | `software-development/hermes-agent-skill-authoring` |
| `software-development` | **`inspecting-hermes-desktop-dom`** | Read the live Hermes desktop DOM/CSS over CDP. | `software-development/inspecting-hermes-desktop-dom` |
| `software-development` | **`nextauth-betterauth-url-debug`** | Trigger: invalid callback url, invalid callbackURL, callback URL localhost, login redirect l... | `software-development/nextauth-betterauth-url-debug` |
| `software-development` | **`nextjs-app-router-expert`** | Next.js App Router mastery: Server Actions, Streaming, Parallel/Intercepting Routes, and cac... | `software-development/nextjs-app-router-expert` |
| `software-development` | **`node-inspect-debugger`** | Debug Node.js via --inspect + Chrome DevTools Protocol CLI. | `software-development/node-inspect-debugger` |
| `software-development` | **`owasp-secure-coding`** | OWASP Top 10 prevention, secure coding guidelines, input validation, CSRF, XSS, and authoriz... | `software-development/owasp-secure-coding` |
| `software-development` | **`python-best-practices`** | Idiomatic Python 3.12+, async/await concurrency, Pydantic data modeling, and clean architect... | `software-development/python-best-practices` |
| `software-development` | **`python-debugpy`** | Debug Python: pdb REPL + debugpy remote (DAP). | `software-development/python-debugpy` |
| `software-development` | **`react-best-practices`** | Modern React patterns, Server/Client components separation, hook architecture, and performance. | `software-development/react-best-practices` |
| `software-development` | **`receiving-code-review`** | Use when receiving code review feedback, before implementing suggestions, especially if feed... | `software-development/receiving-code-review` |
| `software-development` | **`requesting-code-review`** | Pre-commit review: security scan, quality gates, auto-fix. | `software-development/requesting-code-review` |
| `software-development` | **`rest-graphql-debug`** | Debug REST/GraphQL APIs: status codes, auth, schemas, repro. | `software-development/rest-graphql-debug` |
| `software-development` | **`simplify-code`** | Parallel 4-agent cleanup of recent code changes. | `software-development/simplify-code` |
| `software-development` | **`source-driven-development`** | Grounds every implementation decision in official documentation. Use when you want authorita... | `software-development/source-driven-development` |
| `software-development` | **`spec-best-practices`** | Technical specification design, RFC authoring, acceptance criteria definition, trade-off ana... | `software-development/spec-best-practices` |
| `software-development` | **`spike`** | Throwaway experiments to validate an idea before build. | `software-development/spike` |
| `software-development` | **`tamagui-best-practices`** | Tamagui UI framework best practices, compiler optimization, multiplatform design tokens, and... | `software-development/tamagui-best-practices` |
| `software-development` | **`test-driven-development`** | TDD: enforce RED-GREEN-REFACTOR, tests before code. | `software-development/test-driven-development` |
| `software-development` | **`testing-best-practices`** | Testing pyramid, unit and integration testing strategies, mocking, test coverage, and mutati... | `software-development/testing-best-practices` |
| `software-development` | **`typescript-best-practices`** | TypeScript strict guidelines, advanced generics, utility types, and type-safe patterns. | `software-development/typescript-best-practices` |
| `software-development` | **`using-git-worktrees`** | Use when starting feature work that needs isolation from current workspace or before executi... | `software-development/using-git-worktrees` |
| `software-development` | **`websockets-realtime-ops`** | Real-time WebSocket architectures, reconnection strategies, heartbeat mechanisms, and pub/su... | `software-development/websockets-realtime-ops` |
| `software-development` | **`work-unit-commits`** | Plan commits as reviewable work units. Trigger: implementation, commit splitting, chained PR... | `software-development/work-unit-commits` |
| `software-development` | **`zig-best-practices`** | Idiomatic Zig programming, explicit memory allocation, comptime metaprogramming, and error h... | `software-development/zig-best-practices` |
| `specialists` | **`1password`** | Set up op CLI, sign in, and read or inject secrets. | `specialists/monitoring-security/1password` |
| `specialists` | **`3-statement-model`** | Build integrated IS/BS/CF financial workbooks in Excel. | `specialists/marketing/3-statement-model` |
| `specialists` | **`_shared`** | Shared SDD references for installed skills. Not invokable. | `specialists/hermes-internal/_shared` |
| `specialists` | **`accelerate`** | Run PyTorch training across GPUs with minimal changes. | `specialists/ai-ml/accelerate` |
| `specialists` | **`activepieces-lead-automation`** | Use when automating lead capture flows in ActivePieces (webhook trigger, SMTP email, Google ... | `specialists/devops-infra/activepieces-lead-automation` |
| `specialists` | **`actual-setup`** | Set up Actual Computer (actual.inc) inference in Hermes. | `specialists/hermes-internal/actual-setup` |
| `specialists` | **`ad-library-research`** | Scrape Meta Ad Library and rank ads by longevity, no login. | `specialists/marketing-ads/ad-library-research` |
| `specialists` | **`admin-reporting`** | Reportes al Admin: formato limpio, [SILENT], verificar VPS. | `specialists/monitoring-security/admin-reporting` |
| `specialists` | **`adversarial-ux-test`** | Roleplay a hostile user to find and triage UX pain points. | `specialists/general/adversarial-ux-test` |
| `specialists` | **`ai-audio-pronunciation-qa`** | Use when verifying AI voice pronunciation vs a script. | `specialists/media-video/ai-audio-pronunciation-qa` |
| `specialists` | **`ai-video-model-costing`** | Use when comparing AI video model costs for reels. | `specialists/devops-systems/ai-video-model-costing` |
| `specialists` | **`ai-video-pricing-research`** | Video clip (6s) prices on fal.ai and Replicate via curl. | `specialists/devops-systems/ai-video-pricing-research` |
| `specialists` | **`amazon-fba-profitability`** | Complete workflow for evaluating Amazon FBA product profitability: cost analysis, fee calcul... | `specialists/marketing/amazon-fba-profitability` |
| `specialists` | **`amazon-listing-optimization`** | Use when creating Amazon listings. Title, images, bullets. | `specialists/marketing/amazon-listing-optimization` |
| `specialists` | **`amazon-sp-api-listings`** | Trigger: Amazon SP-API, seller central, listing Amazon AU, snuffle mat, FBA fee, create/upda... | `specialists/marketing/amazon-sp-api-listings` |
| `specialists` | **`anti-ai-slop-writing`** | Produces human-sounding text that avoids detectable AI writing patterns. Activates on any wr... | `specialists/media-video/anti-ai-slop-writing` |
| `specialists` | **`anti-slop-copy`** | Audita copy para quitar tells de IA antes de publicar. | `specialists/media-video/anti-slop-copy` |
| `specialists` | **`antigravity-cli`** | Operate the Antigravity CLI (agy): plugins, auth, sandbox. | `specialists/hermes-internal/antigravity-cli` |
| `specialists` | **`application-security-review`** | application-security-review — Review application repos for concrete security issues, especia... | `specialists/monitoring-security/application-security-review` |
| `specialists` | **`arcgis-geospatial-analysis`** | ArcGIS and geospatial analysis: Shapefiles (.shp), GeoJSON, KML, EPSG projections, spatial q... | `specialists/hermes-internal/arcgis-geospatial-analysis` |
| `specialists` | **`audiocraft-audio-generation`** | AudioCraft: MusicGen text-to-music, AudioGen text-to-sound. | `specialists/devops-systems/audiocraft-audio-generation` |
| `specialists` | **`auditoria-skills-hermes`** | Use when auditando o contando skills de una flota Hermes. | `specialists/hermes-internal/auditoria-skills-hermes` |
| `specialists` | **`axolotl`** | Axolotl: YAML LLM fine-tuning (LoRA, DPO, GRPO). | `specialists/ai-ml/axolotl` |
| `specialists` | **`baoyu-article-illustrator`** | Article illustrations: type × style × palette consistency. | `specialists/media-video/baoyu-article-illustrator` |
| `specialists` | **`baoyu-comic`** | Knowledge comics (知识漫画): educational, biography, tutorial. | `specialists/media-video/baoyu-comic` |
| `specialists` | **`brainstorming`** | You MUST use this before any creative work - creating features, building components, adding ... | `specialists/general/brainstorming` |
| `specialists` | **`branch-pr`** | Create Gentle AI pull requests with issue-first checks. Trigger: creating, opening, or prepa... | `specialists/general/branch-pr` |
| `specialists` | **`brand-asset-audit`** | Auditar identidad de marca desde Drive (personajes, reels). | `specialists/devops-systems/brand-asset-audit` |
| `specialists` | **`browser-backend-replacement`** | Cadena de navegación web por defecto de Ragnar: Agent-Reach (primario) → Obscura (fallback) ... | `specialists/general/browser-backend-replacement` |
| `specialists` | **`campaign-publish-automation`** | Use when automating campaign publishing with human approval. | `specialists/marketing/campaign-publish-automation` |
| `specialists` | **`campanas-qa-integridad`** | Docs de campaña + gate QA-INTEGRIDAD para el equipo de bots. | `specialists/marketing-ads/campanas-qa-integridad` |
| `specialists` | **`canton-network-repos`** | Canton Network smart contract architecture, Daml integration, LocalNet development, and repo... | `specialists/hermes-internal/canton-network-repos` |
| `specialists` | **`chained-pr`** | Trigger: PRs over 400 lines, stacked PRs, review slices. Split oversized changes into chaine... | `specialists/general/chained-pr` |
| `specialists` | **`chroma`** | Embedding database for RAG and semantic search. | `specialists/data-vector/chroma` |
| `specialists` | **`clip`** | Zero-shot image classification and image-text search. | `specialists/ai-ml/clip` |
| `specialists` | **`cloudflare-temporary-deploy`** | Deploy a Worker live, no account, via wrangler --temporary. | `specialists/devops-infra/cloudflare-temporary-deploy` |
| `specialists` | **`cognitive-doc-design`** | Design docs that reduce cognitive load. Trigger: writing guides, READMEs, RFCs, onboarding, ... | `specialists/media-video/cognitive-doc-design` |
| `specialists` | **`colombia-contratos-empresa`** | Contratos y constitución de empresa en Colombia. | `specialists/hermes-internal/colombia-contratos-empresa` |
| `specialists` | **`colombia-promociones-legales`** | Colombian promo legal docs: T&C, datos, juego responsable. | `specialists/marketing-ads/colombia-promociones-legales` |
| `specialists` | **`comfyui`** | Generate images, video, and audio via diffusion workflows. | `specialists/devops-systems/comfyui` |
| `specialists` | **`comment-writer`** | Write warm, direct collaboration comments. Trigger: PR feedback, issue replies, reviews, Sla... | `specialists/general/comment-writer` |
| `specialists` | **`composio-social-publishing`** | Publish to Instagram/Facebook via Composio CLI. | `specialists/marketing/composio-social-publishing` |
| `specialists` | **`comps-analysis`** | Build comparable-company valuation workbooks in Excel. | `specialists/marketing/comps-analysis` |
| `specialists` | **`concept-diagrams`** | Generate flat, minimal educational SVG visuals as HTML. | `specialists/general/concept-diagrams` |
| `specialists` | **`content-performance-analytics`** | Analyze campaign reel perf: features + platform insights. | `specialists/marketing/content-performance-analytics` |
| `specialists` | **`context-engineering`** | Optimizes agent context setup. Use when starting a new session, when agent output quality de... | `specialists/hermes-internal/context-engineering` |
| `specialists` | **`context-monitoring`** | Monitor Hermes context window usage, token consumption, and session health via CLI commands ... | `specialists/monitoring-security/context-monitoring` |
| `specialists` | **`context-recovery`** | Recuperar la conversación después de un error del provider (JSON corrupto, 400 errors, conte... | `specialists/hermes-internal/context-recovery` |
| `specialists` | **`coolify-api-operations`** | Trigger: Coolify API, coolify deploy, API token, create admin, ports_mappings, private-deplo... | `specialists/devops-infra/coolify-api-operations` |
| `specialists` | **`copy-dialecto-local`** | Use when el copy debe sonar local (dialecto regional). | `specialists/comms/copy-dialecto-local` |
| `specialists` | **`creative-ideation`** | Generate ideas via named methods from creative practice. | `specialists/general/creative-ideation` |
| `specialists` | **`cron-watchdog-scripts`** | Use when creating/debugging Hermes no_agent cron watchdogs. | `specialists/devops-infra/cron-watchdog-scripts` |
| `specialists` | **`cunas-de-audio-campana`** | Use when a campaign needs a perifoneo/radio cue. | `specialists/media-video/cunas-de-audio-campana` |
| `specialists` | **`darwinian-evolver`** | Evolve prompts/regex/SQL/code with Imbue's evolution loop. | `specialists/hermes-internal/darwinian-evolver` |
| `specialists` | **`dcf-model`** | Build discounted cash flow valuation workbooks in Excel. | `specialists/marketing/dcf-model` |
| `specialists` | **`discord-reporter`** | Send status reports, summaries, and notifications to Discord channels. Use when the user wan... | `specialists/hermes-internal/discord-reporter` |
| `specialists` | **`discord-server-admin`** | Create Discord channels and map them to Hermes profiles. | `specialists/comms/discord-server-admin` |
| `specialists` | **`dispatching-parallel-agents`** | Use when facing 2+ independent tasks that can be worked on without shared state or sequentia... | `specialists/hermes-internal/dispatching-parallel-agents` |
| `specialists` | **`documentation-and-adrs`** | Records decisions and documentation. Use when making architectural decisions, changing publi... | `specialists/devops-infra/documentation-and-adrs` |
| `specialists` | **`dspy`** | DSPy: declarative LM programs, auto-optimize prompts, RAG. | `specialists/ai-ml/dspy` |
| `specialists` | **`email-report-cron-aggregator`** | Use when agrego informes diarios y los envio por cron. | `specialists/monitoring-security/email-report-cron-aggregator` |
| `specialists` | **`evaluating-llms-harness`** | lm-eval-harness: benchmark LLMs (MMLU, GSM8K, etc.). | `specialists/ai-ml/evaluating-llms-harness` |
| `specialists` | **`evm`** | Read-only EVM client: wallets, tokens, gas across 8 chains. | `specialists/hermes-internal/evm` |
| `specialists` | **`faiss`** | Fast vector similarity search at billion scale. | `specialists/data-vector/faiss` |
| `specialists` | **`fastmcp`** | Build, test, and deploy Python MCP servers. | `specialists/hermes-internal/fastmcp` |
| `specialists` | **`flash-attention`** | Speed up long-sequence transformer training and inference. | `specialists/ai-ml/flash-attention` |
| `specialists` | **`gdrive-via-activepieces`** | Use when accessing client Google Drive programmatically. | `specialists/devops-systems/gdrive-via-activepieces` |
| `specialists` | **`gentle-ai-bench`** | Trigger: bench, journey, journeys, driven mode, gentle-ai-bench, journey corpus, j-numbers, ... | `specialists/ai-ml/gentle-ai-bench` |
| `specialists` | **`gitnexus-explorer`** | Serve an interactive codebase knowledge graph web UI. | `specialists/general/gitnexus-explorer` |
| `specialists` | **`godmode`** | Jailbreak LLMs: Parseltongue, GODMODE, ULTRAPLINIAN. | `specialists/monitoring-security/godmode` |
| `specialists` | **`grok`** | Delegate coding to xAI Grok Build CLI (features, PRs). | `specialists/hermes-internal/grok` |
| `specialists` | **`guidance`** | Constrain LLM output with grammars; guarantee valid JSON. | `specialists/ai-ml/guidance` |
| `specialists` | **`guiones-campana-por-canal`** | Use when writing or auditing campaign scripts by channel. | `specialists/marketing-ads/guiones-campana-por-canal` |
| `specialists` | **`har-derived-api-client`** | Record a site's XHR into a HAR, derive an HTTP client. | `specialists/general/har-derived-api-client` |
| `specialists` | **`here-now`** | Publish sites to {slug}.here.now and store files in Drives. | `specialists/hermes-internal/here-now` |
| `specialists` | **`hermes-bible-study`** | Use when the user asks for community Hermes Agent knowledge: hidden features, real-world wor... | `specialists/hermes-internal/hermes-bible-study` |
| `specialists` | **`hermes-ecosystem-tools`** | Discover/evaluate Hermes Agent community plugins and skills. | `specialists/hermes-internal/hermes-ecosystem-tools` |
| `specialists` | **`hermes-gateway-lifecycle-forensics`** | Triage de caídas del gateway Hermes (blip s6 vs crash). | `specialists/hermes-internal/hermes-gateway-lifecycle-forensics` |
| `specialists` | **`hermes-gateway-ops`** | Trigger: perfiles multiplex, profile_routes, plugin install, hermes desktop ssh, ragnar, her... | `specialists/hermes-internal/hermes-gateway-ops` |
| `specialists` | **`hermes-scheduled-jobs`** | Use when creating or debugging Hermes cron jobs. | `specialists/comms/hermes-scheduled-jobs` |
| `specialists` | **`hermes-skills-hub`** | Complete reference of all 649 Hermes Agent skills across 4 registries (71 Built-in, 57 Optio... | `specialists/hermes-internal/hermes-skills-hub` |
| `specialists` | **`hermes-usage-cost-audit`** | Audit where LLM tokens go across a Hermes fleet. | `specialists/devops-systems/hermes-usage-cost-audit` |
| `specialists` | **`hermes-workspace-setup`** | Install and configure the Hermes Workspace web UI (outsourc-e/hermes-workspace) as the manag... | `specialists/hermes-internal/hermes-workspace-setup` |
| `specialists` | **`honcho`** | Configure and troubleshoot Honcho memory for Hermes. | `specialists/hermes-internal/honcho` |
| `specialists` | **`huggingface-hub`** | HuggingFace hf CLI: search/download/upload models, datasets. | `specialists/general/huggingface-hub` |
| `specialists` | **`huggingface-tokenizers`** | Fast BPE/WordPiece tokenization and custom vocab training. | `specialists/general/huggingface-tokenizers` |
| `specialists` | **`hyperliquid`** | Hyperliquid market data, account history, trade review. | `specialists/marketing/hyperliquid` |
| `specialists` | **`identity-cleanup`** | Systematic cleanup and update of person identities across Brain Wiki — replacing old names, ... | `specialists/general/identity-cleanup` |
| `specialists` | **`inference-sh-cli`** | Run 150+ AI apps (image, video, LLM) via inference.sh CLI. | `specialists/hermes-internal/inference-sh-cli` |
| `specialists` | **`infografia-cliente-html-png`** | Use when un cliente necesita una imagen explicativa. | `specialists/media-video/infografia-cliente-html-png` |
| `specialists` | **`instructor`** | Structured LLM outputs validated with Pydantic. | `specialists/ai-ml/instructor` |
| `specialists` | **`issue-creation`** | Create and triage GitHub issues from repository evidence. Trigger: issue creation, bug repor... | `specialists/hermes-internal/issue-creation` |
| `specialists` | **`jupyter-notebook`** | Iterative Python via live Jupyter kernel (hamelnb). | `specialists/hermes-internal/jupyter-notebook` |
| `specialists` | **`kanban-video-orchestrator`** | Plan and run multi-agent video production pipelines. | `specialists/hermes-internal/kanban-video-orchestrator` |
| `specialists` | **`kassiuss-informe-parser`** | KASSIUSS sales email HTML parser contract and compatibility | `specialists/hermes-internal/kassiuss-informe-parser` |
| `specialists` | **`lambda-labs`** | On-demand GPU cloud instances for ML training. | `specialists/ai-ml/lambda-labs` |
| `specialists` | **`lbo-model`** | Build leveraged buyout workbooks with IRR/MOIC in Excel. | `specialists/marketing/lbo-model` |
| `specialists` | **`llama-cpp`** | llama.cpp local GGUF inference + HF Hub model discovery. | `specialists/ai-ml/llama-cpp` |
| `specialists` | **`llava`** | Vision-language chat: VQA, captioning, image dialogue. | `specialists/ai-ml/llava` |
| `specialists` | **`local-vision-toolkit`** | Autonomous local computer vision toolkit — OCR, image analysis, chart detection, infographic... | `specialists/hermes-internal/local-vision-toolkit` |
| `specialists` | **`marketing-campaign-generator-ops`** | Use when editing the marketing-campaign-generator repo. | `specialists/marketing/marketing-campaign-generator-ops` |
| `specialists` | **`marketing-campaign-pipeline`** | Orquesta campañas con bots: contrato, fábrica, review. | `specialists/media-video/marketing-campaign-pipeline` |
| `specialists` | **`mcp-oauth-remote-gateway`** | Manual OAuth for remote MCP servers on headless gateways. | `specialists/hermes-internal/mcp-oauth-remote-gateway` |
| `specialists` | **`mcporter`** | List, auth, and call MCP servers/tools from the terminal. | `specialists/hermes-internal/mcporter` |
| `specialists` | **`merge-reconciler`** | Neutral third-party resolution of agent merge conflicts. | `specialists/general/merge-reconciler` |
| `specialists` | **`merger-model`** | Build M&A accretion/dilution workbooks in Excel. | `specialists/marketing/merger-model` |
| `specialists` | **`meta-ads-campaigns`** | Use for Meta Ads clients: campaigns, adsets, ads, pixel. | `specialists/marketing-ads/meta-ads-campaigns` |
| `specialists` | **`meta-ads-operations`** | Run Meta Ads: campaigns, geo, insights, pixel via Composio. | `specialists/marketing-ads/meta-ads-operations` |
| `specialists` | **`modal`** | Serverless GPU cloud for ML jobs and model APIs. | `specialists/ai-ml/modal` |
| `specialists` | **`monid-seedance-clips`** | Use when generating image2video clips via Monid Seedance. | `specialists/devops-systems/monid-seedance-clips` |
| `specialists` | **`mpp-agent`** | Pay HTTP 402 APIs via Machine Payments Protocol (MPP). | `specialists/hermes-internal/mpp-agent` |
| `specialists` | **`nemo-curator`** | Curate LLM training data: dedupe, filter, PII redaction. | `specialists/ai-ml/nemo-curator` |
| `specialists` | **`neuralcrew-campaign-content`** | Copy and guiones for NeuralCrew casino campaigns (Colombia). | `specialists/marketing/neuralcrew-campaign-content` |
| `specialists` | **`neuralcrew-final-report`** | Use when: informe final de cliente en membrete NCL. | `specialists/marketing/neuralcrew-final-report` |
| `specialists` | **`neuralcrew-guion-series-ops`** | Use when: replicar o parafrasear guiones Bingo Millonario. | `specialists/media-video/neuralcrew-guion-series-ops` |
| `specialists` | **`neuroskill-bci`** | Use live BCI cognitive and mood state from NeuroSkill. | `specialists/hermes-internal/neuroskill-bci` |
| `specialists` | **`nginx-certbot-reverse-proxy`** | Use when adding HTTPS domains to apps running behind a shared nginx proxy on Coolify, config... | `specialists/devops-infra/nginx-certbot-reverse-proxy` |
| `specialists` | **`no-ai-slop`** | Edit drafts into sharper, more human writing while preserving the writer's personal voice, o... | `specialists/media-video/no-ai-slop` |
| `specialists` | **`node-webhook-systemd-service`** | Use when deploying Express webhook servers as systemd services on Linux, debugging webhook-t... | `specialists/monitoring-security/node-webhook-systemd-service` |
| `specialists` | **`notification-delivery-reliability`** | Use when a cron message or alert never reached the user. | `specialists/comms/notification-delivery-reliability` |
| `specialists` | **`oauth-connection-door`** | Client OAuth connect pages and per-tenant agent credentials. | `specialists/devops-infra/oauth-connection-door` |
| `specialists` | **`obliteratus`** | OBLITERATUS: abliterate LLM refusals (diff-in-means). | `specialists/monitoring-security/obliteratus` |
| `specialists` | **`ocr-and-documents`** | Extract text from PDFs/scans (pymupdf, marker-pdf). | `specialists/general/ocr-and-documents` |
| `specialists` | **`openclaw-migration`** | Import an OpenClaw setup (memories, skills) into Hermes. | `specialists/hermes-internal/openclaw-migration` |
| `specialists` | **`openhands`** | Delegate coding to OpenHands CLI (model-agnostic, LiteLLM). | `specialists/hermes-internal/openhands` |
| `specialists` | **`osint-investigation`** | Follow the money via public records and sanctions data. | `specialists/monitoring-security/osint-investigation` |
| `specialists` | **`oss-forensics`** | GitHub supply-chain forensics: recovery, IOCs, reporting. | `specialists/monitoring-security/oss-forensics` |
| `specialists` | **`outlines`** | Outlines: structured JSON/regex/Pydantic LLM generation. | `specialists/ai-ml/outlines` |
| `specialists` | **`page-agent`** | Embed an in-page natural-language GUI copilot in web apps. | `specialists/hermes-internal/page-agent` |
| `specialists` | **`pdf-deliverables`** | Use when user wants a PDF. Generate and send via MEDIA:. | `specialists/monitoring-security/pdf-deliverables` |
| `specialists` | **`peft`** | Fine-tune large LLMs with LoRA on limited GPU memory. | `specialists/ai-ml/peft` |
| `specialists` | **`performance-optimization`** | Optimizes application performance. Use when performance requirements exist, when you suspect... | `specialists/devops-infra/performance-optimization` |
| `specialists` | **`persistent-task-manager`** | Manage persistent task tracking across sessions. Maintains Brain Wiki tasks file and syncs w... | `specialists/hermes-internal/persistent-task-manager` |
| `specialists` | **`pinecone`** | Managed vector DB for production RAG and search. | `specialists/data-vector/pinecone` |
| `specialists` | **`pinecone-research`** | Agent RAG and long-term memory with Pinecone. | `specialists/data-vector/pinecone-research` |
| `specialists` | **`pip-install-broken-env`** | Install pip and Python packages in environments where pip is missing, sudo is unavailable, c... | `specialists/hermes-internal/pip-install-broken-env` |
| `specialists` | **`pipeline-informes-ventas-multimarca`** | Runbook to onboard a new brand into the sales pipeline. | `specialists/marketing/pipeline-informes-ventas-multimarca` |
| `specialists` | **`pipelines-con-gate-humano`** | Use when construyendo un flujo por etapas con OK humano. | `specialists/devops-infra/pipelines-con-gate-humano` |
| `specialists` | **`plan`** | Write a markdown plan to .hermes/plans/; no execution. | `specialists/hermes-internal/plan` |
| `specialists` | **`playwright-best-practices`** | Reliable E2E browser automation, Page Object Model, semantic locators, and resilient test fi... | `specialists/hermes-internal/playwright-best-practices` |
| `specialists` | **`polymarket`** | Query Polymarket: markets, prices, orderbooks, history. | `specialists/marketing/polymarket` |
| `specialists` | **`postgres-performance-tuning`** | PostgreSQL query optimization, EXPLAIN ANALYZE, indexing strategies, connection pooling, and... | `specialists/devops-infra/postgres-performance-tuning` |
| `specialists` | **`pptx-author`** | Build PowerPoint decks headless with python-pptx. | `specialists/monitoring-security/pptx-author` |
| `specialists` | **`pretext`** | Build creative browser demos with DOM-free text layout. | `specialists/hermes-internal/pretext` |
| `specialists` | **`provider-manager`** | Manage AI LLM providers, models, context windows, and active defaults in Hermes Agent config... | `specialists/hermes-internal/provider-manager` |
| `specialists` | **`pytorch-fsdp`** | Fully sharded data-parallel training for large models. | `specialists/ai-ml/pytorch-fsdp` |
| `specialists` | **`pytorch-lightning`** | Clean training loops with built-in distributed support. | `specialists/ai-ml/pytorch-lightning` |
| `specialists` | **`qdrant`** | Vector search engine for production RAG systems. | `specialists/data-vector/qdrant` |
| `specialists` | **`rag-architecture-expert`** | Retrieval-Augmented Generation (RAG) architecture, hybrid search, reciprocal rank fusion, an... | `specialists/data-vector/rag-architecture-expert` |
| `specialists` | **`redis-caching-patterns`** | Redis caching patterns, distributed locking (Redlock), rate limiting, Pub/Sub, and TTL strat... | `specialists/devops-infra/redis-caching-patterns` |
| `specialists` | **`reel-clip-qa`** | Use when approving or debugging a Seedance/Monid reel clip. | `specialists/ai-ml/reel-clip-qa` |
| `specialists` | **`research-paper-writing`** | Write ML papers for NeurIPS/ICML/ICLR: design→submit. | `specialists/general/research-paper-writing` |
| `specialists` | **`saelens`** | Train sparse autoencoders to interpret model features. | `specialists/ai-ml/saelens` |
| `specialists` | **`scene-consistency-qa`** | QA de consistencia de personaje en stills de escenas IA. | `specialists/devops-systems/scene-consistency-qa` |
| `specialists` | **`scene-keyframe-qa-lipsync`** | Use when: QA keyframes 9:16 y prep de lip-sync Seedance. | `specialists/media-video/scene-keyframe-qa-lipsync` |
| `specialists` | **`security-and-hardening`** | Hardens code against vulnerabilities. Use when handling user input, authentication, data sto... | `specialists/monitoring-security/security-and-hardening` |
| `specialists` | **`segment-anything-model`** | SAM: zero-shot image segmentation via points, boxes, masks. | `specialists/general/segment-anything-model` |
| `specialists` | **`serving-llms-vllm`** | vLLM: high-throughput LLM serving, OpenAI API, quantization. | `specialists/ai-ml/serving-llms-vllm` |
| `specialists` | **`sherlock`** | Find accounts for a username across 400+ platforms. | `specialists/monitoring-security/sherlock` |
| `specialists` | **`shop`** | Shop catalog search, checkout, order tracking, returns. | `specialists/comms/shop` |
| `specialists` | **`shopify`** | Query Shopify Admin/Storefront GraphQL APIs via curl. | `specialists/marketing/shopify` |
| `specialists` | **`simple-english`** | Rewrite text to ASD-STE100 Simplified Technical English. | `specialists/hermes-internal/simple-english` |
| `specialists` | **`simpo`** | Reference-free preference alignment, simpler than DPO. | `specialists/ai-ml/simpo` |
| `specialists` | **`skill-auditor`** | skill-auditor — Use when auditing, reviewing, or grading Hermes skills for quality. Checks t... | `specialists/hermes-internal/skill-auditor` |
| `specialists` | **`skill-creator`** | Trigger: new skills, agent instructions, documenting AI usage patterns. Create LLM-first ski... | `specialists/hermes-internal/skill-creator` |
| `specialists` | **`skill-improver`** | Trigger: improve skills, audit skills, refactor skills, skill quality. Audit and upgrade exi... | `specialists/hermes-internal/skill-improver` |
| `specialists` | **`skill-navigator`** | Navigate, query, and compose skills and execution pipelines using the skills knowledge graph... | `specialists/hermes-internal/skill-navigator` |
| `specialists` | **`skill-registry`** | Trigger: update skills, skill registry, actualizar skills, after skill changes. Index availa... | `specialists/hermes-internal/skill-registry` |
| `specialists` | **`slime`** | RL post-training for LLMs with Megatron and SGLang. | `specialists/ai-ml/slime` |
| `specialists` | **`social-media-content-calendar`** | Plan multi-platform social campaigns: briefs to posting. | `specialists/marketing/social-media-content-calendar` |
| `specialists` | **`social-piece-publishing-ops`** | Use when publishing or verifying social posts via Composio. | `specialists/marketing/social-piece-publishing-ops` |
| `specialists` | **`solana`** | Query Solana wallets, tokens, txs, and NFTs in USD. | `specialists/hermes-internal/solana` |
| `specialists` | **`spanish-deliverable-proofreading`** | Check Spanish doc typos before delivering as PDF or DOCX. | `specialists/media-video/spanish-deliverable-proofreading` |
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
| `specialists` | **`video-ai-generator`** | End-to-end 9:16 vertical AI video generation pipeline (Reels, TikTok, Shorts) with ActivePie... | `specialists/comms/video-ai-generator` |
| `specialists` | **`vps-agent-deployer`** | Zero-friction, fully automated provisioning and deployment skill for multi-agent Docker arch... | `specialists/devops-infra/vps-agent-deployer` |
| `specialists` | **`vscode-ai-extension-configuration`** | Configure VSCode AI extensions (OpenCode, Continue, Copilot) and connect custom APIs like Na... | `specialists/hermes-internal/vscode-ai-extension-configuration` |
| `specialists` | **`web-pentest`** | Authorized web pentest: recon, proof-based exploits, report. | `specialists/monitoring-security/web-pentest` |
| `specialists` | **`web-performance-core-vitals`** | Web performance optimization, Core Web Vitals (LCP, INP, CLS), bundle analysis, and renderin... | `specialists/devops-infra/web-performance-core-vitals` |
| `specialists` | **`webhook-gateway-multiclient`** | Trigger: webhook gateway, widget chat, bridge Hermes, leads to postgres, ActivePieces notify... | `specialists/devops-infra/webhook-gateway-multiclient` |
| `specialists` | **`weights-and-biases`** | W&B: log ML experiments, sweeps, model registry, dashboards. | `specialists/ai-ml/weights-and-biases` |
| `specialists` | **`whisper`** | Transcribe and translate speech in 99 languages. | `specialists/comms/whisper` |
| `specialists` | **`wiki-entry-creation`** | Create structured wiki entries from documentation, config files, and session knowledge when ... | `specialists/hermes-internal/wiki-entry-creation` |
| `specialists` | **`x-tweet-scrape`** | Extract tweet content from X/Twitter status URLs using fx(fixupx.com metadata extraction, Ni... | `specialists/hermes-internal/x-tweet-scrape` |
| `specialists` | **`yuanbao`** | Yuanbao (元宝) groups: @mention users, query info/members. | `specialists/hermes-internal/yuanbao` |
| `specialists` | **`zmx`** | Zellij and Tmux multiplexer session management, background task isolation, and multi-termina... | `specialists/hermes-internal/zmx` |
| `web` | **`blocked-page-recovery`** | Use when a fetch fails: 403/429, paywall, WAF, bot wall. | `web/blocked-page-recovery` |
