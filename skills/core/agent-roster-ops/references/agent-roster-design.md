---
name: agent-roster-design
description: "Design bot rosters: identity, skills, and final reports."
version: 1.0.0
author: Ragnar
triggers:
  - roster: equipo de bots / definir mejor al equipo / rosters / tripulación / personajes de los bots
  - identidad: nombre de los bots / personalidad / tono / jerga / SOUL / avatares de los agentes
  - catalogo: cuántas skills / N skills por bot / robustecer al agente / máximo espectro / bibliotecas de skills
  - entrega: informe final del plan / documento limpio / coautoría / borrar archivos intermedios
---

# Agent Roster Design — identidad, skills y entrega de planes de equipos de bots

Complementa a `bot-team-architecture` (arquitectura de capas/roster) y a `hermes-production-deployment` (despliegue). Este skill cubre la fase de **definición y documentación** del equipo cuando el Admin pide "define mejor a los bots", con tres bloques: (1) identidad/nombres/SOULs, (2) catálogos de skills por especialista, (3) entrega final limpia de informes.

## 1. Identidad por arquetipo (dioses antiguos)

- Usar un panteón coherente con la marca. En NeuralCrew el canon es nórdico (ya existen Ragnar, Mimir, Odín). Ejemplo validado 26/08/2026: Connect=Hermóðr, Web=Brokkr, Content=Bragi, Social=Freyja, Leads=Ullr, Ads=Vili, Analytics=Heimdall, Producer=Sindri.
- Descartar nombres ya ocupados por otros bots (Odín/Mimir) y cargas negativas (Loki); documentar el descarte con razón.
- **Convención de etiqueta:** display `Nombre (Módulo)` → `Hermóðr (Connect)` (paréntesis: limpio, no colisiona con canales `#` ni rutas); carpeta/perfil SIEMPRE slug ASCII sin acentos (`hermodr`); color ancla por bot para skins.
- **SOUL completa por bot:** campos personalidad / tono / jerga / muletillas prohibidas / ejemplo de voz + cuadro comparativo de voz. Alimenta directamente el `SOUL.md` del perfil.
- **Avatares:** ilustraciones de dominio público de mitología nórdica (Emil Doepler "Die Götterwelt der Germanen"/Walhall 1905, Lorenz Frølich "Nordens Guder" 1886; Wikimedia Commons/PICRYL/germanicmythology.com). Alternativa moderna: set uniforme con flux-2-klein cuando el bot de generación esté operativo.

## 2. Catálogos de skills por especialista

- **"N skills" significa POR AGENTE, no en total.** "Listar 100 skills para cada bot" = ~100 por bot. Y el número suele ser PISO, no techo: ante "robustece", ampliar al máximo espectro (lenguajes, arquitectura, DBs, plataformas, cumplimiento, herramientas). Ejemplo: tras la corrección se pasó de 800 a 1175 skills sin tocar techo.
- **Fuentes externas verificadas:** [CH] Corey Haines marketingskills (45.7k★, agnóstico de agente, 281.9K installs en skills.sh), [CP] ComposioHQ awesome-claude-skills (CRMs, TikTok/YouTube/HubSpot), [V] VoltAgent awesome-agent-skills (32k★, 1000+), [AZ] alirezarezvani claude-skills (24.9k★, compatible explícito con Hermes), [OW] OpenClaw/ClawHub (500+), [AN] Anthropic oficial (~927 vía mcpservers.org/agent-skills), [B] Baoyu (25.3k★). El formato SKILL.md es interoperable entre agentes.
- **Criterios de evaluación:** Compatibilidad Hermes 30% · Relevancia módulo 30% · Estructura 15% · Estrellas/adopción 15% · Seguridad 10%. Toda skill externa pasa `skill-security-auditor` / lectura del SKILL.md antes de instalarse (ecosistema de terceros = vector de ataque conocido).
- Entregar en tablas por bot (nº, skill, fuente, ★, por qué); separar en archivos si son cientos (`catalogo-<bot>-1/2.md` + `ampliacion-<bot>.md`).

## 3. Entrega de documentos finales (estilo)

- **Informe final CONSOLIDADO y LIMPIO:** sin rastro de iteraciones/ediciones ("v1", "corrección del Admin", "cambio de alcance"), sin placeholders de aprobación ("pendiente: que X apruebe…" — eso va a `brain/tasks/pending.md`, no al doc), coautoría tal como la pida el usuario (ej. "Autores: Ragnar & Jesús"), numeración limpia (1..N) e índice.
- **Limpiar intermedios:** tras ensamblar, borrar segmentos/catálogos/scripts de trabajo y dejar solo `.md` + `.docx` finales en el workspace.
- **Formato:** `.docx` (python-docx) para humanos + `.md` para repositorio (ver `hermes-production-deployment`).

## Pitfalls

- **write_file con contenido enorme agota el stream:** dividir en segmentos <~8K tokens por llamada y concatenar con `cat`; si pandoc no está instalado, convertir md→docx con `scripts/md2docx.py`.
- **Catálogos enormes rompen la numeración al concatenar:** postprocesar encabezados (h3/h4) y limpiar totales viejos antes de entregar; verificar con `grep -E "^## |^### "` que la jerarquía quedó plana.
- **Requisito ambiguo de cantidad:** ante "N skills por bot" preguntar una vez o asumir per-agent y anotarlo; nunca entregar una fracción (N total) que el Admin deba corregir.
- **No verificar el borrado:** tras eliminar intermedios, confirmar con `ls` que solo quedan los finales.

## Referencias

- `references/neuralcrew-8-especialistas-2026-08.md` — ejemplo completo: roster de 8 especialistas con dioses, SOULs, 1175 skills, etiqueta y avatares.
- `scripts/md2docx.py` — conversor markdown→docx sin pandoc (tablas, encabezados, listas, código).

## Relación con otras skills

- `bot-team-architecture` (user-owned; recomendar `hermes curator adopt` para poder actualizarla) — arquitectura de capas y proceso de diseño de rosters; esta skill la complementa con identidad/catálogos/entrega.
- `hermes-profile-routing` — enrutamiento de perfiles tras crear los bots.
- `hermes-production-deployment` — despliegue real de perfiles y preferencia .docx.