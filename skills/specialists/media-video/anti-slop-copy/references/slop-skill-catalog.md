# Catálogo Anti-Slop — rank de @juampitech (2026-08-21)

Fuente: tweet https://x.com/juampitech/status/2090834948332655011
Extraído con skill `x-tweet-scrape` → `fixupx.com` + `tweet-scraper.py`.

## Las 10 skills del rank (instaladas / omitidas / rotas)

| # | Skill | Repo | Stars | Estado | Por qué |
|---|-------|------|-------|--------|---------|
| 1 | `stop-slop` | hardikpandya/stop-slop | — | omitida | cubierta por las otras + humanizer ya instalada |
| 2 | `no-ai-slop` | petergyang/no-ai-slop | 5.5K | ✅ instalada | edición mínima con voz + modo detect con evidencia |
| 3 | `humanizer` | blader/humanizer | — | ⚠️ YA instalada antes | humanize texto suelto |
| 4 | `unslop` | poteto/unslop | — | ❌ rota | 404 en skills.sh, repo removido |
| 5 | `slopbeth` | ehmo/slopkit | 77 | omitido | copa más estrecha, 7 installs |
| 6 | `humanizer` (2º) | Aboudjem/humanizer-skill | — | omitido | duplicado del humanizer ya presente |
| 7 | `deslop` | stephenturner/skills | 2 | omitido | baja adopción, prosa/científico no copy |
| 8 | `anti-slop` | elithrar/dotfiles | 197 | ✅ instalada | catálogo de tells + guardrail de no aplanar voz |
| 9 | `humanize` | aashaexo/soundShuman | 260 | omitido | 41 patrones pero cobertura cubierta por las 3 |
| 10 | `anti-ai-slop-writing` | jalaalrd/anti-ai-slop-writing | 384 | ✅ instalada | directiva v2 con banned-words (referencias/banned-words.md) |

## Método de instalación (validado)

skills.sh es una SPA: `urllib`/`git ls-remote` no dan el SKILL.md, y el slug del
tweet NO es la ruta real del repo (`raw.githubusercontent.com/<owner>/<slug>/SKILL.md`
da 404 aunque el repo exista).

Pasos que funcionaron:
1. `git clone --depth 1 https://github.com/<owner>/<repo>` a `/tmp/skills-src/`
2. `find <repo> -maxdepth 3 -name "SKILL.md"` → localizar la ruta real
3. Copiar SOLO el SKILL.md (+ references/ si aplica) a `/opt/data/skills/creative/<nombre>/`
4. Verificar con `skills_list(category="creative")`

## Dónde están instaladas

- `/opt/data/skills/creative/no-ai-slop/SKILL.md`
- `/opt/data/skills/creative/anti-ai-slop-writing/SKILL.md` + `references/banned-words.md`
- `/opt/data/skills/creative/anti-slop/SKILL.md`
- `/opt/data/skills/creative/humanizer/SKILL.md` (ya existía)

## Nota de alcance

Estas skills limpian TEXT (prosa, copy). NO detectan slop visual (glassmorphism
decorativo, grids genéricas, animaciones por defecto) — para diseño web usar
`popular-web-designs` y `claude-design` por separado.