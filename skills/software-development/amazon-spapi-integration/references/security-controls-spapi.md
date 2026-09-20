# Controles de seguridad SP-API — auditoría real vs declarado + plan

La atestación de seguridad del Developer Profile es una declaración formal. Amazon puede auditar. Antes de marcar "Sí", auditar el estado real del VPS.

## Auditoría real (VPS NeuralCrew, 2026-08-18)

| # | Control | Estado real | Acción |
|---|---|---|---|
| 1 | Firewall, IDS/IPS, antivirus, segmentación | NO — sin ufw activo; Postgres 5432, Redis 6379, Qdrant 6333 expuestos en 0.0.0.0 | Fase 1: ufw + restringir puertos. Fase 2: clamav + auditd |
| 2 | Acceso restringido por rol | Parcial — `.env` 600, ACCESS.md | Documentar RBAC mínimo |
| 3 | Cifrado en tránsito | Parcial — HTTPS saliente; sin TLS interno | Fase 2: TLS vía nginx |
| 4 | Plan IR + roles + revisión 6m + notif 24h | Parcial — CRISIS.md Protocolo 1 básico | Fase 1: ampliar CRISIS.md + cron semestral |
| 5 | Reporte security@amazon.com ≤24h | NO documentado | Fase 1: agregar a CRISIS.md |
| 6 | Contraseñas 12+/MFA/rotación anual | NO documentado | Fase 1: política + checklist MFA |
| 7 | Credenciales seguras (sin repos públicos, sin hardcode) | Mayormente — `.env` 600; riesgo: contraseñas en notas/memoria | Fase 2: eliminar de notas, usar llaves |
| 8 | Terceros con datos Amazon | Ninguno | Respuesta: "No compartimos con terceros" |

## Plan de implementación por fases

### Fase 1 — Inmediata (esta semana, ~1-2h)
1. Activar ufw: allow 22, 80, 443, 3000, 8008, 3010, 9119; deny resto. **Cuidado:** firewall remoto puede dejar el VPS inaccesible — confirmar con el usuario antes.
2. Quitar exposición pública de Postgres/Redis/Qdrant (bind a red Docker interna o bloquear en ufw).
3. fail2ban (SSH brute force).
4. Ampliar CRISIS.md: Protocolo 1.1 — roles definidos, notificación security@amazon.com ≤24h, revisión semestral.
5. Política de contraseñas (mín. 12 chars + especiales, MFA obligatorio, rotación anual).
6. Checklist MFA: Amazon Seller Central, Google Workspace, GitHub.
7. Cron de revisión semestral del plan IR.

### Fase 2 — Corto plazo (2-4 semanas)
1. clamav + escaneo semanal (cron).
2. auditd (monitoreo de .env, config.yaml) como IDS ligero.
3. TLS en servicios expuestos (nginx + Let's Encrypt para 3000, 8008, 3010).
4. Eliminar credenciales de notas/memoria; migrar deploys a llaves SSH.
5. Backup cifrado de `.env` (age/gpg).
6. Documentar RBAC: quién puede leer .env, config.yaml, brain/.

### Fase 3 — Mantenimiento
1. Revisión semestral del IR (junio/diciembre).
2. Rotación anual de credenciales.
3. Auditoría trimestral: permisos, repos públicos, secrets expuestos.

## Comandos de auditoría rápida
```bash
# Firewall
sudo -n ufw status; iptables -L -n
# IDS/AV
which fail2ban clamav snort suricata auditd
# Puertos Docker expuestos
docker ps --format '{{.Names}} {{.Ports}}'
# Permisos críticos
stat -c '%a %n' /opt/data/.env /opt/data/config.yaml
# Secrets en repos
grep -rliE "sk-[a-zA-Z0-9]{20}|api[_-]?key|password|secret" --include="*.py" --include="*.yaml" --include="*.env*" .
```
