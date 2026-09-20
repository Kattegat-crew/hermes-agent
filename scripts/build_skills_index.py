#!/usr/bin/env python3
"""
build_skills_index.py — Generador determinista del catálogo e índice canónico de skills.
Produce SKILLS_INDEX.md con las skills canónicas agrupadas por categorías.
Excluye los bundles de convenciones (prefijo `_`), que no son skills invocables.
"""
import os
import yaml
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path("/root/hermes-agent")
SKILLS_DIR = REPO_ROOT / "skills"

def generate_index():
    skills = []
    for root, dirs, files in os.walk(SKILLS_DIR):
        # Bundles de convenciones (prefijo "_", p.ej. specialists/hermes-internal/_shared)
        # NO son skills invocables: fuera del catálogo y del conteo.
        dirs[:] = [d for d in dirs if not d.startswith("_")]
        if "SKILL.md" in files:
            sm_path = Path(root) / "SKILL.md"
            rel = sm_path.parent.relative_to(SKILLS_DIR)
            category = rel.parts[0]
            name = sm_path.parent.name
            
            desc = ""
            try:
                content = sm_path.read_text(encoding="utf-8")
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        fm = yaml.safe_load(parts[1]) or {}
                        desc = fm.get("description", "")
            except Exception:
                pass
            
            desc_clean = str(desc).strip().replace("\n", " ").replace("|", "/")
            if len(desc_clean) > 95:
                desc_clean = desc_clean[:92] + "..."

            skills.append({
                "category": category,
                "name": name,
                "path": str(rel),
                "desc": desc_clean
            })

    skills.sort(key=lambda x: (x["category"], x["name"]))

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "# Índice Canónico de Skills — Flota Hermes",
        f"> **Última sincronización**: {now} | **Total de skills**: {len(skills)}"
        " (excluye bundles de convenciones con prefijo `_`)",
        "",
        "Este catálogo representa la **Fuente Única de Verdad (SSOT)** de habilidades operativas para todos los perfiles de la flota Hermes.",
        "Todas las skills se resuelven on-demand desde `/opt/hermes/skills` sin saturar la ventana de contexto.",
        "",
        "| Categoría | Skill | Descripción | Ruta Canónica |",
        "| :--- | :--- | :--- | :--- |"
    ]

    for s in skills:
        lines.append(f"| `{s['category']}` | **`{s['name']}`** | {s['desc']} | `{s['path']}` |")

    content = "\n".join(lines) + "\n"

    # Save to repo root
    (REPO_ROOT / "SKILLS_INDEX.md").write_text(content, encoding="utf-8")
    
    # Save to Roshi docs
    roshi_index = REPO_ROOT / "data" / "profiles" / "roshi" / "SKILLS_INDEX.md"
    if roshi_index.parent.exists():
        roshi_index.write_text(content, encoding="utf-8")

    print(f"✅ SKILLS_INDEX.md generado exitosamente con {len(skills)} skills canónicas.")

if __name__ == "__main__":
    generate_index()
