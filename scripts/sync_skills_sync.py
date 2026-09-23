#!/usr/bin/env python3
"""sync_skills_sync.py — Motor de sincronización canónica Host <-> Contenedor.

Paridad por CONTENIDO (sha256 de SKILL.md y de todos los archivos de la skill),
no por conteo de carpetas. Ese fue el hueco P2: el sync anterior comparaba
nombres y borraba con `rm -rf` cualquier modificación hecha en el contenedor.

Contrato (ver scripts/sync_container_skills.sh):
  --mode check              dry-run, no muta nada
  --mode apply --firma T    muta; exige el token del dueño (sha256 vs archivo)
  --adopt-sediment          promueve al canon las skills creadas por los agentes en los
                            sedimentos locales de los perfiles (dir local de cada perfil) y
                            limpia el sedimento tras respaldarlo
  --adopt-new               adopta al canon las skills que solo existen en el espejo
                            (por defecto NO se adoptan: un solo-espejo puede ser una
                            baja del canon, y se archiva + poda en vez de resucitarse)
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


SEDIMENT_DIRS = [
    "data/skills",                      # perfil default (HERMES_HOME=/opt/data)
    "data/profiles/roshi/skills",
    "data/profiles/bragi/skills",
    "data/profiles/brokkr/skills",
    "data/profiles/comms/skills",
    "data/profiles/freyja/skills",
    "data/profiles/heimdall/skills",
    "data/profiles/hermodr/skills",
    "data/profiles/sindri/skills",
    "data/profiles/ullr/skills",
    "data/profiles/vigia/skills",
    "data/profiles/vili/skills",
]


def sediment_inventory(repo: Path, canon_names: set, head_ts: float = 0.0) -> dict:
    """Skills creadas por los agentes en el dir local (sedimento) de cada perfil.

    Devuelve {'nuevas': [...], 'sombra': [...]} con paths repo-relativos.
    'sombra' = el nombre ya existe en el canon: crear así sombrearía la canónica.
    """
    nuevas, resiembra, sombra = [], [], []
    for rel_root in SEDIMENT_DIRS:
        root = repo / rel_root
        if not root.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
            if "SKILL.md" not in filenames:
                continue
            d = Path(dirpath)
            name = d.name
            if name.startswith("_") or name in TAR_EXCLUDES:
                continue
            rel = str(d.relative_to(repo))
            mt = os.path.getmtime(d / "SKILL.md")
            if name in canon_names:
                sombra.append(rel)
            elif head_ts and mt < head_ts - 60:
                # más vieja que el último commit: re-siembra bundled o algo ya resuelto
                resiembra.append(rel)
            else:
                nuevas.append(rel)
    return {"nuevas": sorted(nuevas), "resiembra": sorted(resiembra), "sombra": sorted(sombra)}


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
    ap.add_argument("--adopt-sediment", action="store_true")
    ap.add_argument("--adopt-new", action="store_true")
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

    # Frontera temporal: último commit del canon. Sirve para distinguir una skill
    # creada por un agente (posterior) de una re-siembra bundled o baja previa (anterior).
    try:
        head_ts = float(subprocess.run(
            ["git", "-C", str(repo), "log", "-1", "--format=%ct"],
            capture_output=True, text=True, check=True).stdout.strip())
    except Exception:
        head_ts = 0.0

    canon_names = {os.path.basename(k) for k in host}
    sedimento = sediment_inventory(repo, canon_names, head_ts)

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
    log("🌱 SEDIMENTO (skills creadas por agentes en los dirs locales de los perfiles)")
    log(f"   creadas por agentes    : {len(sedimento['nuevas'])}")
    log(f"   re-siembras bundled    : {len(sedimento.get('resiembra', []))}  (anteriores al último commit)")
    log(f"   sombras del canon      : {len(sedimento['sombra'])}")
    for s in sedimento["nuevas"]:
        log(f"      🌱 {s}")
    for s in sedimento.get("resiembra", []):
        log(f"      ♻️  {s}  [re-siembra: NO se promueve automáticamente]")
    for s in sedimento["sombra"]:
        log(f"      🚫 SOMBRA (nombre ya canónico): {s}")

    log("")
    log("📊 DIAGNÓSTICO (por contenido, no por conteo)")
    log(f"   nuevas en contenedor : {len(new)}")
    log(f"   drift (modificadas)  : {len(drift)}")
    log(f"   faltan en contenedor : {len(missing)}")
    # Hints de dirección para el solo-espejo (usa la frontera head_ts de arriba)
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
        "sedimento_nuevas": sedimento["nuevas"],
        "sedimento_resiembra": sedimento.get("resiembra", []),
        "sedimento_sombra": sedimento["sombra"],
        "parity": not (new or drift or missing),
    }
    if a.json_out:
        Path(a.json_out).write_text(json.dumps(report, indent=2, ensure_ascii=False))

    if a.mode == "check":
        log("")
        if report["parity"] and not sedimento["nuevas"] and not sedimento["sombra"] and not sedimento.get("resiembra"):
            log("✅ PARIDAD POR CONTENIDO + sedimentos limpios (100%).")
            return 0
        if sedimento["nuevas"] or sedimento["sombra"] or sedimento.get("resiembra"):
            log("🌱 Sedimento con hallazgos (promoción con: --apply --firma <TOKEN> --adopt-sediment)")
        if report["parity"]:
            log("✅ PARIDAD POR CONTENIDO: canon y espejo son idénticos (100%).")
            return 0
        log("⚠️ Diferencias detectadas. Para resolverlas:")
        log("   ./sync_container_skills.sh --apply --firma <TOKEN>               (despliega el canon; poda solo-espejo)")
        log("   ... --adopt-new    (adopta al canon las skills que solo viven en el espejo)")
        log("   ... --adopt-drift  (promueve al canon el drift detectado en el espejo)")
        return 2

    # ── mode == apply ──────────────────────────────────────────────────────
    if not check_firma(a.firma, Path(a.firma_sha_file)):
        return 1

    if (report["parity"] and not sedimento["nuevas"]
            and not sedimento["sombra"] and not sedimento.get("resiembra")):
        log("")
        log("✅ Nada que sincronizar: paridad por contenido ya es 100% y sedimentos limpios.")
        return 0

    stamp = time.strftime("%Y%m%d-%H%M%S")
    archive = repo / "data" / "archive" / f"sync_{stamp}"
    archive.mkdir(parents=True, exist_ok=True)

    # 0) promoción de sedimentos (skills creadas por agentes en dirs locales)
    if sedimento["nuevas"] or sedimento["sombra"]:
        if a.adopt_sediment:
            for rel in sedimento["nuevas"]:
                src = repo / rel
                name = src.name
                dst = host_root / "specialists" / name
                if dst.exists():
                    log(f"   ⚠️ {name} ya existe en el canon; se omite y queda en el sedimento.")
                    continue
                log(f"   🌱 promoviendo al canon: {name}  ({rel})")
                shutil.copytree(src, archive / "sedimento" / rel, dirs_exist_ok=True)
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(src, dst, dirs_exist_ok=True)
                shutil.rmtree(src)
                log(f"      ✅ adoptada en skills/specialists/{name} y sedimento limpio (respaldo en el archivo)")
            for rel in sedimento.get("resiembra", []):
                log(f"   ♻️  re-siembra NO promovida (anterior al último commit; revisar a mano): {rel}")
            for rel in sedimento["sombra"]:
                log(f"   🚫 sombra NO promovida (el nombre ya vive en el canon): {rel}")
        else:
            log("   ℹ️  hay sedimento sin promover (usa --adopt-sediment para promocionarlo).")
    log("")
    log(f"🗄️  Respaldo previo (nada se pierde): {archive}")

    # 1) rescatar TODO lo que vive en el contenedor y no está idéntico en el canon
    for rel in new + drift:
        log(f"   💾 respaldando {rel}")
        copy_from_container(a.container, f"{a.container_skills}/{rel}", archive / rel)

    # 2) adopción de skills nuevas → SOLO con --adopt-new (evita resucitar bajas del canon)
    if new and a.adopt_new:
        for rel in new:
            dst = host_root / rel
            if dst.exists():
                log(f"   ⚠️ {rel} ya existe en el canon con otro contenido; se archiva y se omite.")
                continue
            log(f"   📥 adoptando nueva: {rel}")
            copy_from_container(a.container, f"{a.container_skills}/{rel}", dst)
    elif new:
        log("   ℹ️  skills solo-espejo NO adoptadas (usa --adopt-new para adoptarlas).")
        log("       Si son bajas del canon, el despliegue las retira del espejo (ya están respaldadas).")

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
    # GUARD DE PUNTO DE MONTAJE (modelo A2, fase F2): si el destino es un montaje,
    # el espejo ES el canon. Barrerlo destruiría el catálogo y su historial git.
    _mnt = subprocess.run(
        f"docker exec {a.container} sh -c \"grep -c ' {a.container_skills} ' /proc/mounts || true\"",
        shell=True, capture_output=True, text=True).stdout.strip()
    if _mnt and _mnt != '0':
        log(f"   🛑 ABORTADO: {a.container_skills} es un PUNTO DE MONTAJE en {a.container}.")
        log("      Con el modelo A2 el espejo ES el canon: desplegar aquí borraría el catálogo.")
        log("      Los cambios se hacen en git y el runtime los ve al instante.")
        return 1
    log("📦 Desplegando canon -> contenedor…")
    # El glob se expande DENTRO del contenedor: si no, solo se borran las entradas
    # que también existen en el host y el espejo acumula residuos para siempre.
    subprocess.run(f'docker exec {a.container} sh -c "rm -rf {a.container_skills}/*"',
                   shell=True, check=True)
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
