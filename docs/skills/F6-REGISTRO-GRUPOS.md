# F6 · Registro de triaje de los grupos de solape (cierre de la consolidación)

| Campo | Valor |
|---|---|
| Documento | `docs/skills/F6-REGISTRO-GRUPOS.md` |
| Fecha | 2026-09-23 |
| Fuente | `data/state/f6_metrica.json` (métrica oficial, umbral 0,45) |
| Estado | skills **707** · pares **56** · grupos **29** · implicadas **71 (10.04 %)** |

## Resumen del triaje

| Clase | Grupos |
|---|---|
| pendiente | 19 |
| diferido | 6 |
| falso positivo | 4 |

## Registro

| Grupo | Miembros | Sim. máx | Clase | Razón |
|---|---|---|---|---|
| grupo_01 | 10 | 0.6136 | falso positivo | Fases de un flujo con disparador propio; andamiaje ya factorizado en _shared/. |
| grupo_02 | 4 | 0.4793 | pendiente | Sin veredicto: exige lectura fina del cuerpo (no hay duplicación evidente: sim < 0,62). |
| grupo_03 | 3 | 0.4561 | pendiente | Sin veredicto: exige lectura fina del cuerpo (no hay duplicación evidente: sim < 0,62). |
| grupo_04 | 3 | 0.6850 | falso positivo | Herramientas distintas: FSDP (entrenamiento distribuido con sharding) frente a Unsloth (fine-tuning  |
| grupo_05 | 3 | 0.4519 | pendiente | Sin veredicto: exige lectura fina del cuerpo (no hay duplicación evidente: sim < 0,62). |
| grupo_06 | 2 | 0.5344 | diferido | Disparadores distintos; y `plan` genera /plan, que colisiona con un comando núcleo de Hermes. |
| grupo_07 | 2 | 0.4915 | pendiente | Sin veredicto: exige lectura fina del cuerpo (no hay duplicación evidente: sim < 0,62). |
| grupo_08 | 2 | 0.4773 | pendiente | Sin veredicto: exige lectura fina del cuerpo (no hay duplicación evidente: sim < 0,62). |
| grupo_09 | 2 | 0.4574 | pendiente | Sin veredicto: exige lectura fina del cuerpo (no hay duplicación evidente: sim < 0,62). |
| grupo_10 | 2 | 0.5029 | pendiente | Sin veredicto: exige lectura fina del cuerpo (no hay duplicación evidente: sim < 0,62). |
| grupo_11 | 2 | 0.5086 | pendiente | Sin veredicto: exige lectura fina del cuerpo (no hay duplicación evidente: sim < 0,62). |
| grupo_12 | 2 | 0.4846 | pendiente | Sin veredicto: exige lectura fina del cuerpo (no hay duplicación evidente: sim < 0,62). |
| grupo_13 | 2 | 0.4990 | pendiente | Sin veredicto: exige lectura fina del cuerpo (no hay duplicación evidente: sim < 0,62). |
| grupo_14 | 2 | 0.6354 | diferido | Complementarias, no duplicadas; además ambas con descripción VACÍA (limpieza de R5, no fusión). |
| grupo_15 | 2 | 0.4672 | pendiente | Sin veredicto: exige lectura fina del cuerpo (no hay duplicación evidente: sim < 0,62). |
| grupo_16 | 2 | 0.4790 | pendiente | Sin veredicto: exige lectura fina del cuerpo (no hay duplicación evidente: sim < 0,62). |
| grupo_17 | 2 | 0.4810 | pendiente | Sin veredicto: exige lectura fina del cuerpo (no hay duplicación evidente: sim < 0,62). |
| grupo_18 | 2 | 0.6221 | diferido | Ambas cargan scripts/ propios (riesgo de colisión) + referencia entrante desde amazon-sp-api-listing |
| grupo_19 | 2 | 0.4703 | pendiente | Sin veredicto: exige lectura fina del cuerpo (no hay duplicación evidente: sim < 0,62). |
| grupo_20 | 2 | 0.4730 | pendiente | Sin veredicto: exige lectura fina del cuerpo (no hay duplicación evidente: sim < 0,62). |
| grupo_21 | 2 | 0.4894 | pendiente | Sin veredicto: exige lectura fina del cuerpo (no hay duplicación evidente: sim < 0,62). |
| grupo_22 | 2 | 0.4633 | pendiente | Sin veredicto: exige lectura fina del cuerpo (no hay duplicación evidente: sim < 0,62). |
| grupo_23 | 2 | 0.5051 | diferido | Registrada en .hub/lock.json (instalación de hub) y su directorio carga scripts/ que exigen reubicac |
| grupo_24 | 2 | 0.9994 | diferido | SKILL.md casi idénticos (6 bytes) pero ~3,2 MB de bundles por lado y el updater referencia a hermes- |
| grupo_25 | 2 | 0.5059 | pendiente | Sin veredicto: exige lectura fina del cuerpo (no hay duplicación evidente: sim < 0,62). |
| grupo_26 | 2 | 0.5417 | falso positivo | Modelos financieros distintos (integrado IS/BS/CF vs LBO con IRR/MOIC). El parecido es del andamiaje |
| grupo_27 | 2 | 0.4651 | pendiente | Sin veredicto: exige lectura fina del cuerpo (no hay duplicación evidente: sim < 0,62). |
| grupo_28 | 2 | 0.5197 | falso positivo | Separación DELIBERADA: la descripción de form-cro dice "cualquier formulario que NO sea signup/regis |
| grupo_29 | 2 | 0.5118 | diferido | 21,8 KB vs 9,7 KB y papeles distintos (construir vs operar); exige lectura fina. |

## Lectura

Tras cinco lotes (0-4) la consolidación **mecánica** queda cerrada: los duplicados reales
(descripción y objeto idénticos) se absorbieron sin perder contenido, y lo que queda son
**grupos que la métrica agrupa por andamiaje compartido o por tema, no por duplicación**.

- Los `falso positivo` están declarados en `data/state/f6_falsos_positivos.json`:
  ningún lote automático debe fusionarlos por parecido.
- Los `diferido` están en `data/state/f6_diferidos.json`: cada uno espera plan propio.
- Los `pendiente` (todos por debajo de 0,62 salvo el par bíblico) exigen lectura fina
  del cuerpo antes de tocarlos; no hay duplicación evidente.
