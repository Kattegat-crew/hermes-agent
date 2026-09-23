#!/usr/bin/env python3
"""
F5.2 - Retiro del arbol legado /opt/data del HOST.

Objetivo: dejar el host sin rutas de skills/perfiles/estado fuera del repositorio.

Fases (--fase):
  migrar   copia la CARGA VIVA del arbol legado a <repo>/data (preserva permisos)
  repoint  parchea las constantes /opt/data de los 2 scripts de cron y la crontab
  archivar tar verificado del arbol legado -> data/archive/ y retiro del directorio
  todo     las tres, en orden

Gate de firma (R12): sin --firma <token> valido contra /root/.sync-firma.sha256,
el script sale con exit 1 y CERO escrituras. --ensayo simula sin exigir firma.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

REPO = "/root/hermes-agent"
DATA = os.path.join(REPO, "data")
LEGACY = "/opt/data"
FIRMA_FILE = "/root/.sync-firma.sha256"
TS = time.strftime("%Y%m%d-%H%M%S")
BACKUP = os.path.join(DATA, "backups", "F52_%s" % TS)
ARCHIVE = os.path.join(DATA, "archive", "F52_%s" % TS)

# carga viva: (origen legacy, destino repo, es_directorio_a_mergear)
PAYLOAD = [
    ("/opt/data/vps-monitor.env", DATA + "/vps-monitor.env", False),
    ("/opt/data/backup-keys", DATA + "/backup-keys", True),
    ("/opt/data/home/.config/rclone", DATA + "/home/.config/rclone", True),
    ("/opt/data/backups", DATA + "/backups", True),
]
SCRIPTS = [DATA + "/scripts/vps_health_watchdog.py", DATA + "/scripts/vps_master_backup.py"]
# sueltos de /root: (ruta, vivo?)  update_soul.py apunta a un perfil inexistente -> muerto
SUELTOS = [("/root/patch_bridge.py", True), ("/root/update_soul.py", False)]

CRON_PAT = "/opt/data/scripts/"
CRON_NUEVO = REPO + "/data/scripts/"

log = []
escribio = False


def sh(c, timeout=180):
    return subprocess.run(c, shell=True, capture_output=True, text=True, timeout=timeout)


def p(msg):
    print(msg, flush=True)
    log.append(msg)


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def verificar_firma(token):
    if not token:
        return False, "sin --firma"
    try:
        esperado = open(FIRMA_FILE).read().strip()
    except Exception as e:
        return False, "no se pudo leer el archivo de firma: %s" % e
    dado = hashlib.sha256(token.strip().encode()).hexdigest()
    if dado != esperado:
        return False, "token no coincide con /root/.sync-firma.sha256"
    return True, "firma valida"


# ── FASE 1: migrar la carga viva ────────────────────────────────────────────
def fase_migrar(ensayo):
    p("\n=== FASE MIGRAR: carga viva -> repo/data ===")
    res = []
    for orig, dest, es_dir in PAYLOAD:
        existe = os.path.exists(orig)
        destino_existe = os.path.exists(dest)
        p("  %-40s -> %-46s origen=%-5s destino=%s" % (
            orig, dest.replace(REPO, "<repo>"), existe, destino_existe))
        if not existe:
            res.append({"origen": orig, "destino": dest, "accion": "origen ausente"})
            continue
        if ensayo:
            accion = "SIMULADO merge" if (destino_existe and es_dir) else "SIMULADO copiar"
            res.append({"origen": orig, "destino": dest, "accion": accion})
            continue
        if destino_existe and es_dir:
            # merge del contenido, sin pisar lo que ya vive en el repo
            r = sh("cp -an %s/. %s/" % (orig, dest))
            res.append({"origen": orig, "destino": dest,
                        "accion": "merge" if r.returncode == 0 else "ERROR: %s" % r.stderr.strip()})
        elif destino_existe:
            res.append({"origen": orig, "destino": dest, "accion": "ya existe en destino"})
        else:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            r = sh("cp -a %s %s" % (orig, dest))
            res.append({"origen": orig, "destino": dest,
                        "accion": "copiado" if r.returncode == 0 else "ERROR: %s" % r.stderr.strip()})
    # staging lo crea el backup solo si hace falta
    st = DATA + "/backups/staging"
    if not ensayo:
        os.makedirs(st, exist_ok=True)
    return res


# ── FASE 2: repoint de scripts y crontab ────────────────────────────────────
def fase_repoint(ensayo):
    p("\n=== FASE REPOINT: scripts y crontab ===")
    res = {"scripts": [], "crontab": {}, "sueltos": []}

    # 2.a scripts de cron: reemplazo de la raiz legacy por la del repo
    for sp in SCRIPTS:
        if not os.path.exists(sp):
            res["scripts"].append({"script": sp, "accion": "ausente"})
            continue
        txt = open(sp, encoding="utf-8").read()
        n = txt.count(LEGACY)
        bak = "%s.bak-f52-%s" % (sp, TS)
        if ensayo:
            res["scripts"].append({"script": os.path.basename(sp), "reemplazos": n,
                                   "accion": "SIMULADO"})
            continue
        sh("cp -a %s %s" % (sp, bak))
        nuevo = txt.replace(LEGACY, DATA)
        open(sp, "w", encoding="utf-8").write(nuevo)
        # quedan referencias a otros arboles (/opt/hermes/data) que NO se tocan
        otras = sorted(set([l.strip() for l in nuevo.splitlines()
                            if "/opt/hermes/data" in l]))
        res["scripts"].append({"script": os.path.basename(sp), "reemplazos": n,
                               "respaldo": os.path.basename(bak),
                               "otras_fuentes_no_tocadas": len(otras),
                               "compila": sh("python3 -m py_compile %s" % sp).returncode == 0})

    # 2.b crontab
    actual = sh("crontab -l").stdout
    lineas = actual.splitlines()
    objetivo = [l for l in lineas if CRON_PAT in l]
    nueva = [l.replace(CRON_PAT, CRON_NUEVO) if CRON_PAT in l else l for l in lineas]
    res["crontab"] = {"lineas_afectadas": len(objetivo),
                      "antes": objetivo,
                      "despues": [l for l in nueva if CRON_NUEVO in l]}
    if not ensayo:
        os.makedirs(BACKUP, exist_ok=True)
        open(os.path.join(BACKUP, "crontab_root.txt"), "w").write(actual)
        open("/tmp/f52_crontab_nueva.txt", "w").write("\n".join(nueva) + "\n")
        r = sh("crontab /tmp/f52_crontab_nueva.txt")
        res["crontab"]["rc"] = r.returncode
        res["crontab"]["stderr"] = r.stderr.strip()[:200]

    # 2.c scripts sueltos de /root
    for sp, vivo in SUELTOS:
        if not os.path.exists(sp):
            res["sueltos"].append({"script": sp, "accion": "ausente"})
            continue
        txt = open(sp, encoding="utf-8").read()
        n = txt.count(LEGACY)
        if n == 0:
            res["sueltos"].append({"script": sp, "accion": "sin referencias"})
            continue
        if not vivo:
            res["sueltos"].append({"script": sp, "reemplazos": n,
                                   "accion": "DECLARADO MUERTO (perfil destino inexistente): no se parchea"})
            continue
        if ensayo:
            res["sueltos"].append({"script": sp, "reemplazos": n, "accion": "SIMULADO"})
            continue
        sh("cp -a %s %s.bak-f52-%s" % (sp, sp, TS))
        open(sp, "w", encoding="utf-8").write(txt.replace(LEGACY, DATA))
        res["sueltos"].append({"script": sp, "reemplazos": n, "accion": "parcheado"})
    return res


# ── FASE 3: archivar y retirar ──────────────────────────────────────────────
ARBOLES = [
    ("/opt/data", "opt_data_legado"),                 # arbol legado del host
    ("/opt/hermes/skills", "hermes_skills_host"),     # espejo obsoleto (409 SKILL.md, sin consumidores)
]
SUELTOS_MUERTOS = ["/root/update_soul.py"]            # apunta a un perfil inexistente


def _tar_y_retirar(origen, etiqueta, ensayo, p, ARCHIVE):
    res = {"origen": origen, "etiqueta": etiqueta}
    if not os.path.exists(origen):
        res["accion"] = "ya no existe"
        return res
    fch = int(sh("find %s -type f 2>/dev/null | wc -l" % origen).stdout.strip() or 0)
    res["ficheros"] = fch
    if ensayo:
        res["accion"] = "SIMULADO"
        return res
    tar = os.path.join(ARCHIVE, "%s.tar.gz" % etiqueta)
    r = sh("tar czf %s -C %s %s 2>/dev/null" % (
        tar, os.path.dirname(origen), os.path.basename(origen)), timeout=3600)
    res["tar_rc"] = r.returncode
    res["tar_bytes"] = os.path.getsize(tar) if os.path.exists(tar) else 0
    res["tar_sha256_16"] = sha256(tar)[:16] if os.path.exists(tar) else None
    res["entradas_en_tar"] = int(sh("tar tzf %s | wc -l" % tar, timeout=1800).stdout.strip() or 0)
    res["coincide"] = res["entradas_en_tar"] >= fch
    # prueba de extracto real: 3 ficheros al azar, comparados por hash
    muestra = sh("tar tzf %s | grep -v '/$' | shuf -n 3" % tar).stdout.split()
    ok_muestra = []
    for m in muestra:
        sh("rm -rf /tmp/f52_probe && mkdir -p /tmp/f52_probe")
        sh("tar xzf %s -C /tmp/f52_probe %s 2>/dev/null" % (tar, shell_quote(m)))
        a = os.path.join("/tmp/f52_probe", m)
        b = os.path.join(os.path.dirname(origen), m)
        if os.path.exists(a) and os.path.exists(b):
            ok_muestra.append({"fichero": m, "sha_igual": sha256(a) == sha256(b)})
    res["prueba_extracto"] = ok_muestra
    res["extracto_ok"] = all(x["sha_igual"] for x in ok_muestra) if ok_muestra else None
    if not (res["coincide"] and res.get("extracto_ok") is not False):
        res["accion"] = "ABORTADO: verificacion fallida, no se retira nada"
        return res
    destino = os.path.join(ARCHIVE, etiqueta + ".original")
    sh("mv %s %s" % (origen, destino))
    res["accion"] = "archivado y retirado"
    res["en_archive"] = destino
    res["origen_sigue_existiendo"] = os.path.exists(origen)
    return res


def shell_quote(s):
    return "'" + s.replace("'", "'\\''") + "'"


def fase_archivar(ensayo):
    p("\n=== FASE ARCHIVAR: tar verificado y retiro ===")
    res = {"arboles": [], "sueltos_muertos": []}
    if not ensayo:
        os.makedirs(ARCHIVE, exist_ok=True)
    for origen, etq in ARBOLES:
        r = _tar_y_retirar(origen, etq, ensayo, p, ARCHIVE)
        p("  %-24s %s" % (origen, json.dumps(r, ensure_ascii=False)[:200]))
        res["arboles"].append(r)
    for sp in SUELTOS_MUERTOS:
        if not os.path.exists(sp):
            res["sueltos_muertos"].append({"script": sp, "accion": "ausente"})
            continue
        if ensayo:
            res["sueltos_muertos"].append({"script": sp, "accion": "SIMULADO mover"})
            continue
        dest = os.path.join(ARCHIVE, "sueltos_declarados_muertos")
        os.makedirs(dest, exist_ok=True)
        sh("mv %s %s/" % (sp, dest))
        res["sueltos_muertos"].append({"script": sp, "accion": "movido al archivo",
                                       "en_archive": os.path.join(dest, os.path.basename(sp))})
    return res


# ── FASE 4: verificar ───────────────────────────────────────────────────────
def fase_verificar():
    p("\n=== VERIFICACION ===")
    res = {}
    for s in ["vps_health_watchdog.py", "vps_master_backup.py"]:
        sp = DATA + "/scripts/" + s
        r = sh("python3 %s --dry-run 2>&1 | tail -4" % sp, timeout=300)
        res[s] = {"rc": r.returncode, "cola": r.stdout.strip().splitlines()[-3:]}
    res["crontab"] = sh("crontab -l | grep -c '%s'" % CRON_NUEVO).stdout.strip()
    res["legacy_refs_en_crontab"] = sh("crontab -l | grep -c '%s' || true" % LEGACY).stdout.strip()
    res["legacy_existe"] = os.path.exists(LEGACY)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fase", default="todo",
                    choices=["migrar", "repoint", "archivar", "todo"])
    ap.add_argument("--ensayo", action="store_true", help="simulacion sin firma ni escrituras")
    ap.add_argument("--firma", default="", help="token del dueño")
    a = ap.parse_args()

    ok, motivo = verificar_firma(a.firma)
    p("GATE DE FIRMA: %s%s" % ("OK" if ok else "BLOQUEADO", "" if ok else " (%s)" % motivo))
    if not ok and not a.ensayo:
        p("ABORTADO sin escribir nada (R12: el candado vive en el codigo).")
        sys.exit(1)

    informe = {"ts": TS, "ensayo": a.ensayo, "fase": a.fase, "firma": ok}
    fases = ["migrar", "repoint", "archivar"] if a.fase == "todo" else [a.fase]
    for f in fases:
        if f == "migrar":
            informe["migrar"] = fase_migrar(a.ensayo)
        elif f == "repoint":
            informe["repoint"] = fase_repoint(a.ensayo)
        elif f == "archivar":
            informe["archivar"] = fase_archivar(a.ensayo)

    if not a.ensayo:
        informe["verificacion"] = fase_verificar()
        os.makedirs(BACKUP, exist_ok=True)
        ruta = os.path.join(DATA, "state", "f52_%s.json" % TS)
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w") as fh:
            json.dump(informe, fh, ensure_ascii=False, indent=1)
        p("\ninforme: %s" % ruta)
    else:
        p("\n(ENSAYO: sin escrituras)")

    print("\n=== INFORME ===")
    print(json.dumps(informe, ensure_ascii=False, indent=1)[:4000])


if __name__ == "__main__":
    main()
