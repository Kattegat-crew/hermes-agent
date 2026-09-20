# Cron delivery forensics — recetas verificadas (2026-09-10)

Todo lo de abajo se ejecutó en este stack (DEV 147.93.3.250, gateway en contenedor + backend root del Desktop).

## 1. ¿Hubo corrida y hubo entrega?

```bash
# corridas (status, pid, error) — el registro autoritativo
ssh dev "docker exec hermes-agent python3 -c \"
import sqlite3; c=sqlite3.connect('/opt/data/cron/executions.db')
for r in c.execute(\\\"select job_id,pid,status,claimed_at,error from executions where job_id='<JOBID>' order by claimed_at desc limit 5\\\"): print(r)\""

# entrega (sobrevive a un last_status verde)
python3 -c "import json;d=json.load(open('/opt/data/cron/jobs.json'));print([(j['name'],j.get('last_status'),j.get('last_delivery_error')) for j in d['jobs'] if j.get('last_delivery_error')])"
grep -ahE "delivery error|WhatsApp send failed|Discord send failed" /opt/data/logs/agent.log | tail -20

# incidentes agrupados por firma
ssh dev "docker exec hermes-agent python3 -c \"import sqlite3;c=sqlite3.connect('/opt/data/cron/executions.db');print(list(c.execute('select job_id,error,failure_type,state,first_seen_at,last_seen_at from cron_incidents order by last_seen_at desc limit 15')))\""
```

`output/<job_id>/<fecha>.md` dice quién tickeó por el dueño del archivo: `hermes` = gateway (uid 10000), `root` = backend root del Desktop (por eso como uid 10000 da `Permission denied` → leer con `ssh dev`).

## 2. Qué ticker/namespace lo corrió

```bash
readlink /proc/self/ns/mnt                 # mi namespace
readlink /proc/<pid-de-executions>/ns/mnt
ls /proc/<pid>/root/opt/data/scripts/      # lo que ESE proceso realmente ve
```

Mismo id ⇒ corrió en mi vista. Distinto id + un `/opt/data` casi vacío bajo `/proc/<pid>/root/` ⇒ corrió en el ns host (backend root del Desktop), donde el `/opt/data` del host es OTRO árbol: los wrappers con ruta absoluta única fallan con `python3: can't open file '/opt/data/...': [Errno 2]` aunque el archivo exista para el gateway. Fix: probar ambos roots (`/opt/data/...` y `/root/hermes-agent/data/...`) como hacen los wrappers `calendario_*.sh`.

## 3. Discord: id → nombre de canal y permisos

```python
import json, urllib.request
TOK = [l.split('=',1)[1].strip() for l in open('/opt/data/.env') if l.startswith('DISCORD_BOT_TOKEN=')][0]
def api(p):
    r = urllib.request.Request('https://discord.com/api/v10'+p,
        headers={'Authorization': f'Bot {TOK}', 'User-Agent': 'DiscordBot (hermes,1.0)'})
    return json.load(urllib.request.urlopen(r, timeout=15))
print(api('/users/@me')['username'])                      # nombre del bot
for g in api('/users/@me/guilds'):
    for c in api(f"/guilds/{g['id']}/channels"):
        print(g['name'], c['id'], c.get('name'), c.get('topic'))
```

Permisos del bot: `api('/guilds/<gid>/members/<bot_id>')['roles']` + `api('/guilds/<gid>/roles')`; `ADMINISTRATOR` = bit 3, `SEND_MESSAGES` = bit 11.

Verificar entrega:
```python
api('/channels/<channel_id>/messages?limit=4')   # leer el canal, no confiar en el run
```

## 4. Webhook de Discord: validar el token y recuperar el real

```bash
curl -s -w '\nHTTP %{http_code}\n' "https://discord.com/api/webhooks/<id>/<token>"
# 401 {"message":"Invalid Webhook Token","code":50027} => token mal copiado o regenerado
```

Caso real: el token pegado difería en UN carácter al final (`…WuzB` vs el real `…WuzH`); con el correcto el POST devolvió 204 y el mensaje apareció en el canal como «Crons de posts».

```python
whs = api('/guilds/<guild_id>/webhooks')            # requiere MANAGE_WEBHOOKS
wh  = [w for w in whs if w['id'] == '<webhook_id>'][0]
print(wh['channel_id'], wh['name'], wh['token'])
```

El **id** de un webhook (snowflake) embebe su creación: `(int(id) >> 22) + 1420070400000` ms → sirve para saber si es nuevo o viejo. Para borrar mensajes de prueba propios: `DELETE /channels/<id>/messages/<msg_id>` (204).

## 5. Cambio de destino (procedimiento probado)

```bash
cp -a /opt/data/cron/jobs.json /opt/data/cron/jobs.json.bak-content-discord-$(date +%Y%m%d-%H%M%S)
```

Luego `cronjob_manage(action='update', job_id=<id>, deliver='discord:<channel_id>')` por job (devuelve el job con `deliver` aplicado; si el target no trae `:thread_id` avisa que caerá en el canal principal), releer `jobs.json`, disparar con `action='run'` y confirmar el mensaje leyendo el canal.

Al mover jobs de canal: enumerar en la respuesta qué jobs cambian y qué jobs NO (los que el usuario declare fuera), y decir dónde se aprueba ahora — así se corrige en un solo mensaje en lugar de re-preguntar.
