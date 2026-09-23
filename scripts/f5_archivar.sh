#!/usr/bin/env bash
# F5 · archivado de los árboles fuera del canon.
# Regla: empaquetar → verificar el tar → recién entonces mover.
set -uo pipefail
R=/root/hermes-agent
TS=$(date +%Y%m%d-%H%M%S)
A="$R/data/archive/F5_$TS"
mkdir -p "$A"

archiva() {  # origen etiqueta
  local src="$1" et="$2"
  if [ ! -e "$src" ]; then echo "  –  $et: no existe ($src)"; return 0; fi
  local tar="$A/${et}.tar.gz"
  echo "  · $et: empaquetando $(du -sh "$src" 2>/dev/null | cut -f1)…"
  tar czf "$tar" -C "$(dirname "$src")" "$(basename "$src")" 2>/dev/null
  if [ ! -s "$tar" ]; then echo "  ❌ tar vacío para $et — NO se mueve"; return 1; fi
  local lista; lista=$(tar tzf "$tar" | wc -l)
  local sha; sha=$(sha256sum "$tar" | cut -c1-16)
  printf '  ✅ %-22s tar=%s entradas=%s sha=%s\n' "$et" "$(du -h "$tar" | cut -f1)" "$lista" "$sha"
  echo "$et $tar $sha $lista" >> "$A/MANIFIESTO.txt"
  return 0
}

echo "=== empaquetado ==="
archiva "$R/data/skills"              "residuo_data_skills"   || exit 1
archiva "/root/.agents/skills"        "agents_skills"         || exit 1
archiva "/opt/data/skills"            "host_opt_data_skills"  || exit 1

echo
echo "=== verificación de que el contenido clave está en el tar ==="
for par in "residuo_data_skills:$R/data/skills" "agents_skills:/root/.agents/skills" "host_opt_data_skills:/opt/data/skills"; do
  et=${par%%:*}; src=${par#*:}
  [ -e "$src" ] || continue
  real=$(find "$src" -name SKILL.md | wc -l)
  en_tar=$(tar tzf "$A/${et}.tar.gz" | grep -c "SKILL.md$")
  printf '  %-22s SKILL.md en disco=%-4s en tar=%-4s %s\n' "$et" "$real" "$en_tar" \
    "$([ "$real" = "$en_tar" ] && echo OK || echo '⚠️ DIFERENCIA')"
done

echo
echo "=== moviendo los originales al archivo (nada se borra) ==="
for par in "residuo_data_skills:$R/data/skills" "agents_skills:/root/.agents/skills" "host_opt_data_skills:/opt/data/skills"; do
  et=${par%%:*}; src=${par#*:}
  [ -e "$src" ] || { echo "  –  $et ya movido"; continue; }
  mv "$src" "$A/${et}.original" && echo "  ✅ $et → $A/${et}.original"
done

echo
echo "=== quedan? ==="
for d in "$R/data/skills" /root/.agents/skills /opt/data/skills; do
  printf '  %-40s %s\n' "$d" "$([ -e "$d" ] && echo AÚN EXISTE || echo retirado)"
done
echo
echo "MANIFIESTO:"
cat "$A/MANIFIESTO.txt" 2>/dev/null
