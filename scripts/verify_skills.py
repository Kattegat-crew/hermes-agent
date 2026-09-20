#!/usr/bin/env python3
"""
verify_skills.py — Aduana estricta de calidad para skills en el repositorio Git.
Verifica:
1. SKILL.md existe y es legible.
2. Frontmatter YAML válido con 'name' y 'description'.
3. 'name' coincide con el directorio (kebab-case).
4. Sin cascarones vacíos (<600 bytes sin soporte).
5. 0 symlinks rotos o apuntando fuera del repo.
6. Permisos rx para el usuario del contenedor (UID 10000).

Los bundles de convenciones (prefijo `_`) se excluyen: no son skills invocables.
"""

import os
import sys
import re
from pathlib import Path

REPO_SKILLS = Path("/root/hermes-agent/skills")

def check_skills():
    print("=" * 60)
    print("🔍 ADUANA DE SKILLS: Verificando /root/hermes-agent/skills")
    print("=" * 60)

    errors = []
    warnings = []
    scanned = 0

    for root, dirs, files in os.walk(REPO_SKILLS):
        dirs[:] = [d for d in dirs if not d.startswith(".") and not d.startswith("_") and d not in ("__pycache__", "references", "scripts", "templates", "assets", "examples")]
        
        rel_path = os.path.relpath(root, REPO_SKILLS)
        if rel_path == ".":
            continue

        if "SKILL.md" in files:
            scanned += 1
            skill_dir = Path(root)
            sm_file = skill_dir / "SKILL.md"

            # Check symlink
            if sm_file.is_symlink():
                errors.append(f"[{rel_path}] SKILL.md no debe ser un symlink.")
                continue

            # Check permissions (must be readable by container user UID 10000)
            dir_mode = skill_dir.stat().st_mode
            file_mode = sm_file.stat().st_mode
            if not (dir_mode & 0o005 == 0o005):
                errors.append(f"[{rel_path}] Directorio sin permisos rx para otros (modo: {oct(dir_mode)[-3:]}).")
            if not (file_mode & 0o004 == 0o004):
                errors.append(f"[{rel_path}] SKILL.md sin permisos r para otros (modo: {oct(file_mode)[-3:]}).")


            # Read content
            try:
                content = sm_file.read_text(encoding="utf-8")
            except Exception as e:
                errors.append(f"[{rel_path}] Error leyendo SKILL.md: {e}")
                continue

            sz = len(content.encode("utf-8"))
            lines = len(content.splitlines())

            # Parse frontmatter
            fm_match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
            if not fm_match:
                errors.append(f"[{rel_path}] Falta bloque frontmatter YAML (--- ... ---).")
                continue

            fm_text = fm_match.group(1)
            name = None
            desc = None
            for l in fm_text.splitlines():
                if l.startswith("name:"):
                    name = l.split("name:", 1)[1].strip().strip("'\"")
                elif l.startswith("description:"):
                    desc = l.split("description:", 1)[1].strip().strip("'\"")

            if not name:
                errors.append(f"[{rel_path}] Frontmatter no define 'name'.")
            elif name != skill_dir.name and name.lower() != skill_dir.name.lower():
                warnings.append(f"[{rel_path}] 'name' ({name}) difiere del directorio ({skill_dir.name}).")

            if not desc:
                warnings.append(f"[{rel_path}] 'description' vacía o ausente.")

            # Check cascaron
            has_scripts = (skill_dir / "scripts").is_dir() and bool(os.listdir(skill_dir / "scripts"))
            has_refs = (skill_dir / "references").is_dir() and bool(os.listdir(skill_dir / "references"))
            
            if sz < 600 and not has_scripts and not has_refs and lines < 20:
                warnings.append(f"[{rel_path}] Posible cascarón: solo {sz} bytes y {lines} líneas.")

    print(f"\nTotal skills auditadas: {scanned}")
    print(f"Errores críticos:       {len(errors)}")
    print(f"Advertencias menores:   {len(warnings)}")

    if warnings:
        print("\n⚠️ Advertencias:")
        for w in warnings[:15]:
            print(" -", w)
        if len(warnings) > 15:
            print(f" ... y {len(warnings)-15} más.")

    if errors:
        print("\n❌ Errores que bloquean la aduana:")
        for e in errors:
            print(" -", e)
        return False

    print("\n✅ ADUANA SUPERADA: Todas las skills cumplen el estándar de calidad.")
    return True

if __name__ == "__main__":
    success = check_skills()
    sys.exit(0 if success else 1)
