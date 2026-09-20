#!/usr/bin/env python3
"""
promote_skills.py — Promueve determinísticamente skills valiosas desde el backup
(pre_purge_profiles_skills_20260920.tar.gz) y el ático (/root/hermes-agent/data/home/.hermes/skills)
al catálogo canónico de /root/hermes-agent/skills.
"""
import os
import shutil
import tarfile
import re
import yaml
from pathlib import Path

CANON_ROOT = Path("/root/hermes-agent/skills")
ARCHIVE_PATH = Path("/root/hermes-agent/data/archive/pre_purge_profiles_skills_20260920.tar.gz")
ATTIC_PATH = Path("/root/hermes-agent/data/home/.hermes/skills")

def categorize(name: str, desc: str) -> str:
    txt = (name + " " + desc).lower()
    if any(k in txt for k in ["ad ", "ads", "copywrit", "seo", "market", "brand", "funnel", "growth", "campaign", "landing", "ab-test", "attribution", "audience", "pricing", "revops", "cfo", "cold-email", "sales", "cro", "roas"]):
        return "specialists/marketing"
    if any(k in txt for k in ["aws", "terraform", "infra", "devops", "docker", "k8s", "kubernetes", "cloud", "linux", "deploy", "systemd", "nginx", "cloudflare", "db-surgery", "cron", "activepieces"]):
        return "devops"
    if any(k in txt for k in ["video", "media", "avatar", "audio", "image", "comic", "infographic", "art", "poster", "keyframe", "illustration", "lipsync", "reel", "song"]):
        return "creative"
    if any(k in txt for k in ["architect", "frontend", "backend", "fullstack", "database", "sql", "qa", "code", "engineer", "developer", "react", "python", "rag", "api", "graphql", "rest", "test"]):
        return "software-development"
    if any(k in txt for k in ["research", "intel", "scrape", "crawl", "paper", "wiki", "coljuegos"]):
        return "research"
    if any(k in txt for k in ["internal", "hermes", "agent-", "fleet", "roster", "soul", "brain", "client-", "governance"]):
        return "specialists/hermes-internal"
    return "productivity"

def main():
    print("=== INICIANDO PROMOCIÓN DE SKILLS ===")
    
    # 1. Identificar skills ya existentes en el canon
    canon_existing = set()
    for root, dirs, files in os.walk(CANON_ROOT):
        if "SKILL.md" in files:
            canon_existing.add(Path(root).name)
    print(f"📦 Skills existentes en el canon: {len(canon_existing)}")

    promoted_count = 0
    promoted_names = set()

    # 2. Promover desde el backup tar.gz (148 skills)
    if ARCHIVE_PATH.exists():
        print(f"📂 Inspeccionando archivo de backup: {ARCHIVE_PATH}")
        with tarfile.open(ARCHIVE_PATH, "r:gz") as tar:
            # Agrupar miembros por skill
            skill_members = {}
            for m in tar.getmembers():
                if m.isdir():
                    continue
                parts = m.name.strip("/").split("/")
                # Buscar dónde está SKILL.md o archivos de la skill
                for idx, part in enumerate(parts):
                    if part == "skills" and idx + 1 < len(parts):
                        # Caso perfil/skills/[categoria/]skill_name/...
                        subparts = parts[idx+1:]
                        if not subparts:
                            continue
                        # Si hay SKILL.md en el path
                        if "SKILL.md" in subparts:
                            s_idx = subparts.index("SKILL.md")
                            if s_idx > 0:
                                s_name = subparts[s_idx - 1]
                                prefix = "/".join(parts[:idx+1 + s_idx])
                                skill_members.setdefault(s_name, []).append((prefix, m))
                                break

            print(f"🔍 Skills encontradas en backup tar: {len(skill_members)}")
            
            for s_name, members_list in sorted(skill_members.items()):
                if s_name in canon_existing or s_name in promoted_names:
                    continue
                
                # Encontrar SKILL.md
                skill_md_member = None
                for prefix, m in members_list:
                    if m.name.endswith(f"/{s_name}/SKILL.md"):
                        if not skill_md_member or m.size > skill_md_member[1].size:
                            skill_md_member = (prefix, m)
                
                if not skill_md_member:
                    continue
                
                # Leer descripción para categorizar
                f = tar.extractfile(skill_md_member[1])
                content = f.read().decode("utf-8", errors="replace")
                desc = ""
                fm_match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
                if fm_match:
                    try:
                        fm = yaml.safe_load(fm_match.group(1)) or {}
                        desc = fm.get("description", "")
                    except Exception:
                        pass
                
                target_cat = categorize(s_name, desc)
                target_dir = CANON_ROOT / target_cat / s_name
                target_dir.mkdir(parents=True, exist_ok=True)
                
                # Extraer todos los archivos de esa skill
                chosen_prefix = skill_md_member[0]
                for prefix, m in members_list:
                    if prefix == chosen_prefix:
                        rel_in_skill = m.name[len(chosen_prefix):].lstrip("/")
                        if not rel_in_skill or any(b in rel_in_skill for b in [".bundled_manifest", "graphify-out", ".git"]):
                            continue
                        dest_file = target_dir / rel_in_skill
                        dest_file.parent.mkdir(parents=True, exist_ok=True)
                        with tar.extractfile(m) as src, open(dest_file, "wb") as dst:
                            shutil.copyfileobj(src, dst)
                
                promoted_names.add(s_name)
                promoted_count += 1
                print(f"  [Backup] Promovida -> {target_cat}/{s_name}")

    # 3. Promover desde el ático (/root/hermes-agent/data/home/.hermes/skills)
    if ATTIC_PATH.exists():
        print(f"📂 Inspeccionando ático: {ATTIC_PATH}")
        for root, dirs, files in os.walk(ATTIC_PATH):
            if "SKILL.md" in files:
                s_name = Path(root).name
                if s_name in canon_existing or s_name in promoted_names:
                    continue
                
                sm_path = Path(root) / "SKILL.md"
                content = sm_path.read_text(encoding="utf-8", errors="replace")
                sz = len(content.encode("utf-8"))
                has_aux = any(f != "SKILL.md" for f in files) or any(d not in ["__pycache__"] for d in dirs)
                
                # Ignorar stubs vacíos
                if sz < 400 and not has_aux:
                    continue
                
                desc = ""
                fm_match = re.search(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
                if fm_match:
                    try:
                        fm = yaml.safe_load(fm_match.group(1)) or {}
                        desc = fm.get("description", "")
                    except Exception:
                        pass
                
                target_cat = categorize(s_name, desc)
                target_dir = CANON_ROOT / target_cat / s_name
                
                # Copiar árbol completo
                shutil.copytree(
                    root,
                    target_dir,
                    dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns(".bundled_manifest", "graphify-out*", ".git*", "__pycache__")
                )
                
                promoted_names.add(s_name)
                promoted_count += 1
                print(f"  [Ático] Promovida -> {target_cat}/{s_name}")

    print(f"\n🎉 Total skills promovidas al canon: {promoted_count}")
    
    # 4. Normalizar permisos (775 dirs / 664 files)
    print("🔒 Normalizando permisos a 775 / 664...")
    for root, dirs, files in os.walk(CANON_ROOT):
        for d in dirs:
            os.chmod(os.path.join(root, d), 0o775)
        for f in files:
            os.chmod(os.path.join(root, f), 0o664)
            
    print("✅ Permisos normalizados.")

if __name__ == "__main__":
    main()
