#!/usr/bin/env python3
"""
audit_7k_skills.py — Censo exhaustivo y auditoría determinista de todas las skills del VPS.
Escanea ~7.000 carpetas, calcula hashes md5, detecta cascarones, duplicados y dependencias.
Emite /root/hermes-agent/data/reports/censo_exhaustivo_7k.json.
"""

import os
import sys
import glob
import json
import hashlib
import re
from pathlib import Path
from collections import defaultdict, Counter

ROOT_DIRS = {
    "repo_builtin": "/root/hermes-agent/skills",
    "repo_optional": "/root/hermes-agent/optional-skills",
    "data_canon": "/root/hermes-agent/data/skills",
    "data_ext": "/root/hermes-agent/data/skills-ext",
    "data_especialistas": "/root/hermes-agent/data/skills-especialistas",
    "host_legacy": "/root/.hermes/skills"
}

SKIP_DIRS = {".git", ".venv", ".venv-agent-reach", ".venv-graphify", "node_modules", "__pycache__", ".archive", ".curator_backups"}

def md5_file(filepath):
    hasher = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            hasher.update(f.read())
        return hasher.hexdigest()
    except Exception:
        return None

def parse_frontmatter(content):
    name = None
    desc = ""
    match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if match:
        raw_fm = match.group(1)
        for line in raw_fm.split("\n"):
            if line.startswith("name:"):
                name = line.split("name:", 1)[1].strip().strip("'\"")
            elif line.startswith("description:"):
                desc = line.split("description:", 1)[1].strip().strip("'\"")
    return name, desc

def audit_corpus():
    print("Iniciando censo exhaustivo de skills en todo el sistema...")
    records = []
    
    # 1. Recorrer directorios fijos
    for category, root in ROOT_DIRS.items():
        if not os.path.exists(root):
            continue
        print(f"Indexando {category} ({root})...")
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
            
            full_path = dirpath
            is_link = os.path.islink(full_path)
            link_target = os.readlink(full_path) if is_link else None
            link_valid = os.path.exists(full_path) if is_link else True
            
            has_skill_md = "SKILL.md" in filenames
            skill_md_path = os.path.join(full_path, "SKILL.md")
            
            if has_skill_md:
                size_bytes = 0
                lines = 0
                h_md5 = None
                fm_name = None
                fm_desc = ""
                
                try:
                    size_bytes = os.path.getsize(skill_md_path)
                    with open(skill_md_path, "r", encoding="utf-8", errors="replace") as f:
                        text = f.read()
                        lines = len(text.splitlines())
                        fm_name, fm_desc = parse_frontmatter(text)
                    h_md5 = md5_file(skill_md_path)
                except Exception as e:
                    pass

                # Detectar soporte
                has_scripts = os.path.isdir(os.path.join(full_path, "scripts")) and bool(os.listdir(os.path.join(full_path, "scripts")))
                has_references = os.path.isdir(os.path.join(full_path, "references")) and bool(os.listdir(os.path.join(full_path, "references")))
                has_templates = os.path.isdir(os.path.join(full_path, "templates")) and bool(os.listdir(os.path.join(full_path, "templates")))

                # Detección de cascarón
                is_cascaron = (size_bytes < 600 and not has_scripts and not has_references and lines < 20)

                records.append({
                    "category": category,
                    "dir": full_path,
                    "rel_name": os.path.basename(full_path),
                    "fm_name": fm_name or os.path.basename(full_path),
                    "description": fm_desc[:120],
                    "size_bytes": size_bytes,
                    "lines": lines,
                    "md5": h_md5,
                    "is_link": is_link,
                    "link_target": link_target,
                    "link_valid": link_valid,
                    "has_scripts": has_scripts,
                    "has_references": has_references,
                    "has_templates": has_templates,
                    "is_cascaron": is_cascaron
                })

    # 2. Recorrer perfiles
    profiles_root = "/root/hermes-agent/data/profiles"
    if os.path.exists(profiles_root):
        print(f"Indexando perfiles en {profiles_root}...")
        for prof in os.listdir(profiles_root):
            p_skills = os.path.join(profiles_root, prof, "skills")
            if not os.path.isdir(p_skills):
                continue
            for dirpath, dirnames, filenames in os.walk(p_skills):
                dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
                for d in list(dirnames):
                    full_p = os.path.join(dirpath, d)
                    if os.path.islink(full_p):
                        targ = os.readlink(full_p)
                        val = os.path.exists(full_p)
                        records.append({
                            "category": f"profile:{prof}",
                            "dir": full_p,
                            "rel_name": d,
                            "fm_name": d,
                            "description": "",
                            "size_bytes": 0,
                            "lines": 0,
                            "md5": None,
                            "is_link": True,
                            "link_target": targ,
                            "link_valid": val,
                            "has_scripts": False,
                            "has_references": False,
                            "has_templates": False,
                            "is_cascaron": False
                        })
                        dirnames.remove(d) # no descender
                if "SKILL.md" in filenames and os.path.basename(dirpath) != "skills":
                    sm = os.path.join(dirpath, "SKILL.md")
                    sz = os.path.getsize(sm) if os.path.exists(sm) else 0
                    h = md5_file(sm)
                    records.append({
                        "category": f"profile:{prof}",
                        "dir": dirpath,
                        "rel_name": os.path.basename(dirpath),
                        "fm_name": os.path.basename(dirpath),
                        "description": "",
                        "size_bytes": sz,
                        "lines": 0,
                        "md5": h,
                        "is_link": False,
                        "link_target": None,
                        "link_valid": True,
                        "has_scripts": False,
                        "has_references": False,
                        "has_templates": False,
                        "is_cascaron": sz < 600
                    })

    total_records = len(records)
    print(f"\nTotal registros indexados: {total_records}")

    # Agrupaciones y Análisis
    md5_to_records = defaultdict(list)
    name_to_records = defaultdict(list)
    cascarones = []
    broken_links = []
    
    for r in records:
        if r["md5"]:
            md5_to_records[r["md5"]].append(r)
        name_to_records[r["fm_name"]].append(r)
        if r["is_cascaron"]:
            cascarones.append(r)
        if r["is_link"] and not r["link_valid"]:
            broken_links.append(r)

    # Clasificación de 4 vías sugerida
    # 1. GUARDAR (Canon core o specialist)
    # 2. NUTRIR (Solape complementario)
    # 3. ARCHIVAR (Vendor externo pasivo)
    # 4. DESCARTAR (Cascarones vacíos o links rotos o duplicados idénticos)

    clasificacion = {
        "GUARDAR": 0,
        "NUTRIR": 0,
        "ARCHIVAR": 0,
        "DESCARTAR": 0
    }

    seen_md5 = set()
    for r in records:
        if r["is_cascaron"] or (r["is_link"] and not r["link_valid"]):
            r["clasificacion"] = "DESCARTAR"
            r["motivo"] = "Cascaron <600B o symlink roto"
            clasificacion["DESCARTAR"] += 1
        elif r["md5"] in seen_md5:
            r["clasificacion"] = "DESCARTAR"
            r["motivo"] = "Duplicado idéntico (mismo md5)"
            clasificacion["DESCARTAR"] += 1
        else:
            if r["md5"]:
                seen_md5.add(r["md5"])
            if r["category"] in ("repo_builtin", "repo_optional"):
                r["clasificacion"] = "GUARDAR"
                r["motivo"] = "Versionado nativo repo"
                clasificacion["GUARDAR"] += 1
            elif r["category"] == "data_canon":
                if r["has_scripts"] or r["has_references"] or r["size_bytes"] > 2000:
                    r["clasificacion"] = "GUARDAR"
                    r["motivo"] = "Canon activo probado con soporte"
                    clasificacion["GUARDAR"] += 1
                else:
                    r["clasificacion"] = "NUTRIR"
                    r["motivo"] = "Candidato a paraguas consolidado"
                    clasificacion["NUTRIR"] += 1
            elif r["category"] in ("data_ext", "host_legacy"):
                if r["has_scripts"]:
                    r["clasificacion"] = "NUTRIR"
                    r["motivo"] = "Vendor con scripts reutilizables para canon"
                    clasificacion["NUTRIR"] += 1
                else:
                    r["clasificacion"] = "ARCHIVAR"
                    r["motivo"] = "Vendor pasivo de terceros sin scripts"
                    clasificacion["ARCHIVAR"] += 1
            elif r["category"] == "data_especialistas":
                r["clasificacion"] = "DESCARTAR"
                r["motivo"] = "Granja de cascarones obsoleta"
                clasificacion["DESCARTAR"] += 1
            else:
                r["clasificacion"] = "GUARDAR"
                r["motivo"] = "Perfil local específico"
                clasificacion["GUARDAR"] += 1

    summary = {
        "total_registros": total_records,
        "hashes_unicos": len(md5_to_records),
        "nombres_unicos": len(name_to_records),
        "total_cascarones": len(cascarones),
        "total_symlinks_rotos": len(broken_links),
        "por_categoria": dict(Counter(r["category"] for r in records)),
        "clasificacion_4_vias": clasificacion
    }

    out_dir = "/root/hermes-agent/data/reports"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "censo_exhaustivo_7k.json")
    
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "records": records}, f, indent=2, ensure_ascii=False)

    print("\n" + "="*60)
    print("📊 RESUMEN EJECUTIVO DEL CENSO EXHAUSTIVO")
    print("="*60)
    print(f"Total registros analizados:       {total_records}")
    print(f"Hashes md5 únicos (contenido real):{len(md5_to_records)}")
    print(f"Nombres únicos:                   {len(name_to_records)}")
    print(f"Cascarones vacíos (<600B):         {len(cascarones)}")
    print(f"Symlinks rotos:                   {len(broken_links)}")
    print("\nDesglose por Ubicación:")
    for cat, cnt in Counter(r["category"] for r in records).most_common():
        print(f"  - {cat:25}: {cnt:>5}")
    print("\nPropuesta Matriz de 4 Vías:")
    for accion, cnt in clasificacion.items():
        print(f"  - {accion:12}: {cnt:>5} ({round(cnt/total_records*100, 1)}%)")
    print(f"\nReporte detallado guardado en: {out_file}")

if __name__ == "__main__":
    audit_corpus()
