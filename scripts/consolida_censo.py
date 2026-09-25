#!/usr/bin/env python3
"""Consolidacion del canon de skills — CENSO-EDITORIAL-20260924.

FUSION: absorbe solo contenido novedoso del origen hacia el receptor:
  - secciones del SKILL.md origen que no existen (por heading) en el receptor
  - referencias/ y scripts/ cuyo contenido (por sha1) no exista ya en el receptor
RETIRA: mueve la carpeta a skills/_retirados/<nombre> (nada se borra).
GATE DURO: exige /root/hermes-agent/scripts/consolidacion_estado.json con
  {"aprobada_por": "Jesus", "aprobado": true, ...} creado/actualizado HOY.
RESPALDO: tar de todo lo tocado en scripts/respaldo_consolidacion_<fecha>.tar.gz
LEDGER: scripts/consolidacion_ledger.json append-only.
"""
import json,os,re,sys,shutil,hashlib,tarfile,datetime,subprocess

ROOT="/root/hermes-agent/skills"
REPO="/root/hermes-agent"
ESTADO="/root/hermes-agent/scripts/consolidacion_estado.json"
CENSO="/root/archive_tmp_dev/censo_editorial.json"

def gate():
    if not os.path.exists(ESTADO):
        print("GATE: falta",ESTADO); sys.exit(2)
    e=json.load(open(ESTADO))
    hoy=datetime.date.today().isoformat()
    if e.get("aprobada_por")!="Jesus" or not e.get("aprobado") or e.get("fecha")!=hoy:
        print("GATE CERRADO: se exige aprobada_por=Jesus, aprobado=true, fecha=hoy (%s). Estado: %s"%(hoy,e)); sys.exit(3)
    print("GATE ABIERTO: aprobado por Jesus el",e["fecha"])
    return e

def sha(b): return hashlib.sha1(b).hexdigest()

def novedades(origen_dir,receptor_dir):
    """devuelve (nuevos_archivos[(relpath,bytes)], secciones_nuevas[(heading,texto)])"""
    novos=[];secciones=[]
    o=os.path.join(ROOT,origen_dir); r=os.path.join(ROOT,receptor_dir)
    # archivos fuera de SKILL.md
    existing={}
    for dp,_,fns in os.walk(r):
        for fn in fns:
            p=os.path.join(dp,fn)
            existing[sha(open(p,"rb").read())]=os.path.relpath(p,r)
    for dp,_,fns in os.walk(o):
        for fn in fns:
            p=os.path.join(dp,fn)
            rel=os.path.relpath(p,o)
            if fn=="SKILL.md": continue
            b=open(p,"rb").read()
            if sha(b) not in existing:
                novos.append((rel,b))
    # secciones del SKILL.md origen no presentes en el receptor
    oskb=open(os.path.join(o,"SKILL.md"),encoding="utf-8").read()
    rskb=open(os.path.join(r,"SKILL.md"),encoding="utf-8").read()
    rheads=set(h.strip().lower() for h in re.findall(r"^#{1,4}\s+(.*)$",rskb,re.M))
    parts=re.split(r"^(#{1,4}\s+.*)$",oskb,flags=re.M)
    i=1
    while i<len(parts)-0:
        if i+1<=len(parts):
            head=parts[i].strip() if parts[i].startswith("#") else None
        # rebuild: split gives [pre, h1, body1, h2, body2...]
        break
    toks=re.split(r"^(#{1,4}\s+.*)$",oskb,flags=re.M)
    pre=toks[0]; j=1
    while j+1<len(toks)+1 and j<len(toks):
        h=toks[j]; body=toks[j+1] if j+1<len(toks) else ""
        htxt=h.lstrip("#").strip()
        if htxt.lower() not in rheads and len(body.strip())>80:
            secciones.append((h,body))
        j+=2
    return novos,secciones,oskb,rskb

def fusionar(origen,receptor,ledger,dry=False):
    novos,secciones,oskb,rskb=novedades(origen,receptor)
    notas={"origen":origen,"receptor":receptor,
           "archivos_nuevos":[rel for rel,_ in novos],
           "secciones_absorbidas":[h.lstrip('#').strip() for h,_ in secciones]}
    if not dry:
        for rel,b in novos:
            dst=os.path.join(ROOT,receptor,rel); os.makedirs(os.path.dirname(dst),exist_ok=True)
            open(dst,"wb").write(b)
        if secciones:
            bloque="\n\n<!-- absorbido de %s (censo 2026-09-24) -->\n"%origen
            bloque+="".join(h+"\n"+b for h,b in secciones)
            open(os.path.join(ROOT,receptor,"SKILL.md"),"a",encoding="utf-8").write(bloque)
        # retirar el origen: mover a _retirados
        dstret=os.path.join(ROOT,"_retirados",origen.replace("/","__"))
        os.makedirs(os.path.dirname(dstret),exist_ok=True)
        shutil.move(os.path.join(ROOT,origen),dstret)
        notas["origen_movido_a"]=os.path.relpath(dstret,ROOT)
    ledger.append(notas)
    print("FUSION %-55s -> %-40s +%d archivos, +%d secciones"%(origen,receptor,len(novos),len(secciones)))

def retirar(origen,ledger,razon,dry=False):
    notas={"origen":origen,"receptor":None,"razon":razon,"archivos_nuevos":[],"secciones_absorbidas":[]}
    if not dry:
        dstret=os.path.join(ROOT,"_retirados",origen.replace("/","__"))
        os.makedirs(os.path.dirname(dstret),exist_ok=True)
        shutil.move(os.path.join(ROOT,origen),dstret)
        notas["origen_movido_a"]=os.path.relpath(dstret,ROOT)
    ledger.append(notas)
    print("RETIRA %-55s (%s)"%(origen,razon))

def main():
    modo=sys.argv[1] if len(sys.argv)>1 else "dry"
    dry = modo!="run"
    gate()
    d=json.load(open(CENSO))
    fusion=[v for v in d["veredictos"] if v["recomendacion"].startswith("fusionar-en:")]
    retiros=[v for v in d["veredictos"] if v["recomendacion"]=="retirar"]
    # receptores que a su vez son origen de otra fusion: resolver cadena
    origenes={v["nombre"] for v in fusion}
    invalidos=[v for v in fusion if v["recomendacion"].split(":",1)[1] in origenes]
    if invalidos:
        # resolver el par ciclico: gana el de MAYOR confianza; el perdedor apunta al ganador
        if len(invalidos)==2 and invalidos[0]["nombre"]==invalidos[1]["recomendacion"].split(":",1)[1]:
            a,b=invalidos
            win,lose=(a,b) if a["confianza"]>=b["confianza"] else (b,a)
            wdir=win["recomendacion"].split(":",1)[1]
            print("CICLO resuelto: %s (conf %.2f) gana sobre %s (conf %.2f) -> destino unico: %s"%(win["nombre"],win["confianza"],lose["nombre"],lose["confianza"],wdir))
            for v in fusion:
                if v is lose: v["recomendacion"]="fusionar-en:"+wdir
        else:
            print("ABORT: cadena no resoluble:",[v["nombre"] for v in invalidos]); sys.exit(4)
    # resolver dirs de receptores
    byname={v["nombre"]:v["_dir"] for v in d["veredictos"]}
    ledger=[]
    ts=datetime.datetime.now().isoformat()
    respaldo="/root/hermes-agent/scripts/respaldo_consolidacion_%s.tar.gz"%datetime.date.today().isoformat()
    if not dry:
        dirs=[v["_dir"] for v in fusion+retiros]+[v["recomendacion"].split(":",1)[1] for v in fusion]
        with tarfile.open(respaldo,"w:gz") as t:
            for dd in dirs:
                p=os.path.join(ROOT,dd)
                if os.path.isdir(p): t.add(p,arcname=dd)
        print("RESPALDO:",respaldo)
    for v in sorted(fusion,key=lambda x:x["nombre"]):
        rec=v["recomendacion"].split(":",1)[1]
        recdir=byname.get(rec,rec)
        if not os.path.isdir(os.path.join(ROOT,recdir)):
            print("SKIP: receptor inexistente:",rec); continue
        fusionar(v["_dir"],recdir,ledger,dry)
    for v in retiros:
        retirar(v["_dir"],ledger,v.get("justificacion","censo: valor nulo"),dry)
    if not dry:
        lp="/root/hermes-agent/scripts/consolidacion_ledger.json"
        old=json.load(open(lp)) if os.path.exists(lp) else []
        old.append({"ts":ts,"operaciones":ledger})
        json.dump(old,open(lp,"w"),ensure_ascii=False,indent=1)
        print("LEDGER:",lp,"operaciones:",len(ledger))
    else:
        print("DRY-RUN: nada tocado. Usa 'run' tras abrir el gate.")
if __name__=="__main__": main()

