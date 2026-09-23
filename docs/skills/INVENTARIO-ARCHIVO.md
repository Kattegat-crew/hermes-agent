# Inventario del archivo de skills

Generado el 2026-09-23 08:49 -0500 desde el disco (no de memoria). Regla R3 de la política: **nada se
borra; todo se archiva con respaldo**. Este documento es la respuesta al punto D2
del informe NC-2026-09-21-SK-01: publicar el inventario por grupo, con rutas, antes
de firmar cualquier limpieza.

Directorio raíz del archivo: `data/archive/`

## Grupos (directorios)

| Grupo | Tamaño | Entradas | SKILL.md |
|---|---|---|---|
| `F0_rescate_20260923-051701` | 560K | 94 | 12 |
| `F3_absorcion_20260923-055337` | 360K | 82 | 17 |
| `F3_absorcion_20260923-055356` | 132K | 27 | 2 |
| `F3_raices_locales_20260923-062556` | 101M | 225 | 3 |
| `F4_manifiesto_20260923-071930` | 44K | 1 | 0 |
| `F5_20260923-084421` | 1011M | 5099 | 194 |
| `gstack` | 48M | 779 | 47 |
| `pruebas_C_20260920` | 12K | 2 | 0 |
| `skills` | 24K | 5 | 3 |
| `sync_20260920-033231` | 88K | 14 | 5 |
| `sync_20260920-033311` | 24K | 4 | 1 |
| `sync_20260920-041039` | 48K | 6 | 1 |
| `sync_20260920-044217` | 32K | 7 | 1 |
| `sync_20260920-044242` | 16K | 3 | 1 |
| `sync_20260920-044251` | 52K | 6 | 1 |
| `sync_20260923-051733` | 72K | 15 | 2 |
| `video-gen` | 520M | 329 | 0 |

## Paquetes (tarballs)

| Paquete | Tamaño | Entradas | sha256 (16) |
|---|---|---|---|
| `attic_home_hermes_skills_20260920.tar.gz` | 64M | 3525 | `a3e6aa6a3edc0da6` |
| `canon_pre_F0_20260923-051324.tar.gz` | 9.8M | 3385 | `89cd22c2f071f8f5` |
| `pre_absorption_data_skills_20260920.tar.gz` | 71M | 4466 | `2a99932f444df1fd` |
| `pre_purge_data_skills_dups_20260920.tar.gz` | 16K | 10 | `f7704dbded55db51` |
| `pre_purge_data_skills_residue_20260920.tar.gz` | 2.1M | 986 | `e5707fcaa881b2dd` |
| `pre_purge_profiles_skills_20260920.tar.gz` | 25M | 8680 | `e5024831790f2fc6` |
| `vendor_skills_ext_20260920.tar.gz` | 71M | 11377 | `2f25daf41bdc8dca` |

## Lectura de D2

- La cifra «849 cascarones listos para papelera» del informe del 21-sep **no se
  reproduce**: el residuo verificable son los grupos `pre_purge_*` de la purga del
  20-sep, ya empaquetados y con inventario. Dimensionar una limpieza sobre aquella
  cifra habría borrado contenido en uso.
- Los grupos `sync_*` son instantáneas de cada corrida del motor de sincronización
  (el que F3 retiró): se conservan como bitácora, no como catálogo.
- `F5_*` recoge los tres árboles retirados el 23-sep (raíces locales, `/root/.agents/
  skills` y el `/opt/data/skills` del host) más sus tarballs verificados entrada por
  entrada (SKILL.md en disco == SKILL.md en el paquete).

## Restauración

```bash
tar xzf data/archive/<paquete>.tar.gz -C <destino>
# o, para los grupos retirados en F5:
mv data/archive/F5_<fecha>/<grupo>.original <ruta-original>
```

⚠️ **Aviso del 23-sep-2026:** `data/skills` NO era residuo: era el **punto de montaje**
de `/opt/data/skills` (el namespace del contenedor). Moverlo en el host desancló el
montaje y el perfil default se quedó sin raíz de skills hasta restaurarlo. Para
retirarlo de verdad hay que recrear el contenedor (Docker vuelve a crear el punto de
montaje) — nunca `mv` en caliente. El job de higiene lo detectó en la misma corrida
(V1 pasó de 12 rutas a 11 y V4 bajó a 0 alcanzables) y ahora informa la ruta ausente.
