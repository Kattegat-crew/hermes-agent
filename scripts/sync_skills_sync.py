#!/usr/bin/env python3
"""sync_skills_sync.py — Motor de sincronización canónica Host <-> Contenedor.

Paridad por CONTENIDO (sha256 de SKILL.md y de todos los archivos de la skill),
no por conteo de carpetas. Ese fue el hueco P2: el sync anterior comparaba
nombres y borraba con `rm -rf` cualquier modificación hecha en el contenedor.

Contrato (ver scripts/sync_container_skills.sh):
  --mode check              dry-run, no muta nada
  --mode apply --firma T    muta; exige el token del dueño (sha256 vs archivo)
  --adopt-drift             promueve al canon el contenido del contenedor de skills
                            ya existentes (respaldando antes el canónico)
  --commit                  git add+commit de adopciones (NO hace push)

Nada se destruye sin respaldo: todo drift/nueva se archiva en
<repo>/data/archive/sync_<ts>/ antes de tocar el espejo.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

TAR_EXCLUDES = {".git", "__pycache__", ".DS_Store"}

PROBE = r"""
import hashlib, json, os, sys
root = sys.argv[1]
inv = {}
for dp, dn, fn in os.walk(root):
    if "SKILL.md" in fn:
        files = {}
        for d2, dn2, fn2 in os.walk(dp):
            dn2[:] = [d for d in dn2 if d not in ("__pycache__", ".git")]
            for f in fn2:
                p = os.path.join(d2, f)
                try:
                    files[os.path.relpath(p, dp)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
                except OSError:
                    files[os.path.relpath(p, dp)] = "ERR"
        inv[os.path.relpath(dp, root)] = {
            "digest": hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest(),
            "mtime": max(
                [os.path.getmtime(os.path.join(d2, f)) for d2, dn2, fn2 in os.walk(dp) for f in fn2] or [0]
            ),
        }
print(json.dumps(inv))
"""


def log(msg: str) -> None:
    print(msg, flush=True)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def skill_digest(skill_dir: Path) -> str:
    """Hash del contenido completo de la skill (todos los archivos, no solo SKILL.md)."""
    files = {}
    for dirpath, dirnames, filenames in os.walk(skill_dir):
        dirnames[:] = [d for d in dirnames if d not in TAR_EXCLUDES]
        for name in filenames:
            p = Path(dirpath) / name
            try:
                files[str(p.relative_to(skill_dir))] = sha256_file(p)
            except OSError:
                files[str(p.relative_to(skill_dir))] = "ERR"
    return hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()


def host_inventory(root: Path) -> dict:
    inv = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in TAR_EXCLUDES]
        if "SKILL.md" in filenames:
            d = Path(dirpath)
            mtimes = [
                os.path.getmtime(os.path.join(r, f))
                for r, _dn, fns in os.walk(d)
                for f in fns
            ] or [0]
            inv[str(d.relative_to(root))] = {
                "digest": skill_digest(d),
                "mtime": max(mtimes),
            }
    return inv


def as_digest(value) -> str:
    """Acepta tanto el formato nuevo {digest,mtime} como el plano {rel: digest}."""
    if isinstance(value, dict):
        return value.get("digest", "")
    return value


def as_mtime(value) -> float:
    if isinstance(value, dict):
        return float(value.get("mtime") or 0)
    return 0.0


def container_inventory(name: str, root: str) -> dict:
    out = subprocess.run(
        ["docker", "exec", name, "python3", "-c", PROBE, root],
        capture_output=True, text=True,
    )
    if out.returncode != 0:
        raise RuntimeError(f"No se pudo inventariar el contenedor: {out.stderr.strip()}")
    return json.loads(out.stdout.strip().splitlines()[-1])


def container_running(name: str) -> bool:
    out = subprocess.run(["docker", "ps", "--format", "{{.Names}}"], capture_output=True, text=True)
    return name in out.stdout.split()


def copy_from_container(name: str, src: str, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    cmd = f"docker exec {name} tar -C {src} -cf - . | tar -C {dest} -xf -"
    subprocess.run(cmd, shell=True, check=True)


def check_firma(firma: str, sha_file: Path) -> bool:
    if not sha_file.exists():
        log("")
        log("🔒 GATE DE FIRMA CERRADO — falta el token del dueño.")
        log(f"   El dueño debe crearlo una sola vez:")
        log(f"     printf '%s' 'TU_TOKEN_SECRETO' | sha256sum | awk '{{print $1}}' > {sha_file}")
        log(f"     chmod 600 {sha_file}")
        log(f"   Y después: $0 --apply --firma TU_TOKEN_SECRETO")
        log("   (Un agente NUNCA debe crear, leer ni guardar este token.)")
        return False
    expected = sha_file.read_text().strip().split()[0]
    got = hashlib.sha256(firma.encode()).hexdigest()
    if got != expected:
        log("")
        log("❌ FIRMA INVÁLIDA — el token no coincide con el autorizado por el dueño.")
        return False
    return True


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--mode", choices=["check", "apply"], default="check")
    ap.add_argument("--host", default="/root/hermes-agent/skills")
    ap.add_argument("--repo", default="/root/hermes-agent")
    ap.add_argument("--container", default="hermes-agent")
    ap.add_argument("--container-skills", default="/opt/hermes/skills")
    ap.add_argument("--firma", default="")
    ap.add_argument("--firma-sha-file", default="/root/.sync-firma.sha256")
    ap.add_argument("--adopt-drift", action="store_true")
    ap.add_argument("--commit", action="store_true")
    ap.add_argument("--json-out", default="")
    return ap.parse_args()


def main() -> int:
    a = parse_args()
    host_root = Path(a.host)
    repo = Path(a.repo)

    if not host_root.is_dir():
        log(f"❌ El canon no existe: {host_root}")
        return 1

    if not container_running(a.container):
        log(f"⚠️ Contenedor {a.container} no está corriendo. Nada que hacer.")
        return 0

    mods = sorted(p.name for p in repo.glob("skills/*/DESCRIPTION.md"))
    log(f"🔍 Inventariando contenido (sha256 por skill) — canon={host_root}, espejo={a.container_skills}")
    host = host_inventory(host_root)
    cont = container_inventory(a.container, a.container_skills)
    log(f"   canon: {len(host)} skills · espejo: {len(cont)} skills")

    new = sorted(set(cont) - set(host))
    missing = sorted(set(host) - set(cont))
    drift = sorted(
        k for k in (set(host) & set(cont)) if as_digest(host[k]) != as_digest(cont[k])
    )
    drift_hint = {}
    for rel in drift:
        hm, cm = as_mtime(host[rel]), as_mtime(cont[rel])
        if cm > hm + 1:
            drift_hint[rel] = "espejo más nuevo → edición de agente en el contenedor (candidata a --adopt-drift)"
        elif hm > cm + 1:
            drift_hint[rel] = "canon más nuevo → pendiente de despliegue (lo resuelve --apply)"
        else:
            drift_hint[rel] = "misma fecha → revisar a mano antes de decidir" 

    log("")
    log("📊 DIAGNÓSTICO (por contenido, no por conteo)")
    log(f"   nuevas en contenedor : {len(new)}")
    log(f"   drift (modificadas)  : {len(drift)}")
    log(f"   faltan en contenedor : {len(missing)}")
    # ¿Baja reciente del canon o skill creada por un agente?
    # Se usa el mtime del último commit del repo como frontera temporal.
    try:
        head_ts = float(
            subprocess.run(
                ["git", "-C", str(repo), "log", "-1", "--format=%ct"],
                capture_output=True, text=True, check=True,
            ).stdout.strip()
        )
    except Exception:
        head_ts = 0.0
    new_hint = {}
    for s in new:
        mt = as_mtime(cont.get(s))
        if head_ts and mt and mt < head_ts - 60:
            new_hint[s] = "anterior al último commit → probable baja del canon (se elimina al desplegar)"
        else:
            new_hint[s] = "posterior al último commit → probable creación de agente (candidata a adopción)"

    if new:
        log("   ── nuevas (solo en el espejo):")
        for s in new:
            log(f"      ⭐ {s}  [{new_hint.get(s, '')}]")
    if drift:
        log("   ── drift (mismo path, contenido distinto):")
        for s in drift:
            log(f"      ✏️  {s}  [{drift_hint.get(s, '')}]")
    if missing:
        log("   ── faltan en el espejo:")
        for s in missing:
            log(f"      📦 {s}")

    report = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "mode": a.mode,
        "canon_count": len(host),
        "container_count": len(cont),
        "new_in_container": new,
        "new_hint": new_hint,
        "drift": drift,
        "drift_hint": drift_hint,
        "missing_in_container": missing,
        "parity": not (new or drift or missing),
    }
    if a.json_out:
        Path(a.json_out).write_text(json.dumps(report, indent=2, ensure_ascii=False))

    if a.mode == "check":
        log("")
        if report["parity"]:
            log("✅ PARIDAD POR CONTENIDO: canon y espejo son idénticos (100%).")
            return 0
        log("⚠️ Diferencias detectadas. Para resolverlas:")
        log("   ./sync_container_skills.sh --apply --firma <TOKEN>            (adopta nuevas y despliega)")
        log("   ./sync_container_skills.sh --apply --firma <TOKEN> --adopt-drift  (además promueve drift al canon)")
        return 2

    # ── mode == apply ──────────────────────────────────────────────────────
    if not check_firma(a.firma, Path(a.firma_sha_file)):
        return 1

    if report["parity"]:
        log("")
        log("✅ Nada que sincronizar: paridad por contenido ya es 100%.")
        return 0

    stamp = time.strftime("%Y%m%d-%H%M%S")
    archive = repo / "data" / "archive" / f"sync_{stamp}"
    archive.mkdir(parents=True, exist_ok=True)
    log("")
    log(f"🗄️  Respaldo previo (nada se pierde): {archive}")

    # 1) rescatar TODO lo que vive en el contenedor y no está idéntico en el canon
    for rel in new + drift:
        log(f"   💾 respaldando {rel}")
        copy_from_container(a.container, f"{a.container_skills}/{rel}", archive / rel)

    # 2) adopción de skills nuevas → mismo path relativo en el canon
    for rel in new:
        dst = host_root / rel
        if dst.exists():
            log(f"   ⚠️ {rel} ya existe en el canon con otro contenido; se archiva y se omite.")
            continue
        log(f"   📥 adoptando nueva: {rel}")
        copy_from_container(a.container, f"{a.container_skills}/{rel}", dst)

    # 3) drift → política explícita
    if drift:
        if a.adopt_drift:
            for rel in drift:
                dst = host_root / rel
                if dst.exists():
                    (archive / "canon_previo" / rel).parent.mkdir(parents=True, exist_ok=True)
                    shutil.copytree(dst, archive / "canon_previo" / rel, dirs_exist_ok=True)
                log(f"   ♻️  promoviendo al canon el contenido del contenedor: {rel}")
                copy_from_container(a.container, f"{a.container_skills}/{rel}", dst)
        else:
            log("   ℹ️  drift NO promovido (usa --adopt-drift para promoverlo). Queda respaldado en el archivo.")

    # 4) permisos del canon (lectura para el runtime)
    log("🔒 Normalizando permisos del canon (dirs 775 / files 664)…")
    subprocess.run(f'find "{host_root}" -type d -exec chmod 775 {{}} +', shell=True, check=True)
    subprocess.run(f'find "{host_root}" -type f -exec chmod 664 {{}} +', shell=True, check=True)

    # 5) commit opcional de la adopción
    if a.commit:
        produced = new + (drift if a.adopt_drift else [])
        if produced:
            msg = f"chore(skills): sync adopta {len(produced)} skill(s) desde el contenedor ({stamp})"
            subprocess.run(f'cd "{repo}" && git add -A skills && git commit -m "{msg}"', shell=True, check=True)
            log(f"   ✅ commit: {msg}")

    # 6) despliegue del canon al espejo
    log("📦 Desplegando canon -> contenedor…")
    subprocess.run(f'docker exec {a.container} rm -rf "{a.container_skills}"/*', shell=True, check=True)
    cmd = f'tar -C "{host_root}" -cf - . | docker exec -i {a.container} tar -C "{a.container_skills}" -xf -'
    subprocess.run(cmd, shell=True, check=True)
    subprocess.run(f'docker exec {a.container} chown -R 10000:10000 "{a.container_skills}"', shell=True, check=True)
    subprocess.run(f'docker exec {a.container} chmod -R 775 "{a.container_skills}"', shell=True, check=True)

    # 7) verificación final POR CONTENIDO (no por conteo)
    log("🧪 Verificación final por contenido…")
    host2 = host_inventory(host_root)
    cont2 = container_inventory(a.container, a.container_skills)
    diffs = sorted(
        k for k in (set(host2) & set(cont2)) if as_digest(host2[k]) != as_digest(cont2[k])
    )
    only_h = sorted(set(host2) - set(cont2))
    only_c = sorted(set(cont2) - set(host2))
    if not diffs and not only_h and not only_c:
        log(f"🎉 PARIDAD POR CONTENIDO CONFIRMADA: {len(host2)} skills idénticas en canon y espejo.")
        log(f"   Respaldo de esta corrida: {archive}")
        return 0
    log("❌ Paridad NO confirmada tras sincronizar:")
    log(f"   drift: {diffs[:10]} · solo canon: {only_h[:10]} · solo espejo: {only_c[:10]}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
