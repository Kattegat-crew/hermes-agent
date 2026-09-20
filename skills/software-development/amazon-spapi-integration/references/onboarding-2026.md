# SP-API Onboarding 2026 — pasos verificados + respuestas de formulario

Fuente: docs oficiales SP-API (developer-docs.amazon.com/sp-api, índice llms.txt). Verificado 2026-08-18.

## Registro como Private Developer (self-developer)

1. **Preparar:** datos de la empresa (registro, dirección), ID gubernamental, use cases, y decidir roles (unrestricted vs restricted).
2. **Developer Profile:** entrar a Seller Central (para AU: sellercentral.amazon.com.au) → Apps and Services → Develop Apps → completar formulario:
   - Contact Information
   - Data Access → **"Private Developer: I build application(s) that integrate my own company with Amazon Services APIs"**
   - Roles + Use Cases + Security Controls
   - Aceptar SPP Agreement, AUP, DPP → Register
   - Amazon evalúa y crea un case; responder en ≤5 días si piden más info.
3. **App sandbox:** solutionproviderportal.amazon.com → Add new app client → API type: SP-API → Application type: Sandbox.
   - Credenciales: fila de la app → LWA credentials → View sandbox credentials (client identifier `amzn1.application-oa2-client.…`, client secret `amzn1.oa2-cs.v1.…`).
   - Refresh token sandbox: Action → Create Token → `Atzr|…`.
4. **Probar sandbox:** endpoint sandbox por región (EU: `https://sandbox.sellingpartnerapi-eu.amazon.com`); getOrders usa params estáticos tipo `TEST_CASE_200`.
5. **App producción:** Add new app client → Production → roles aprobados (queda en draft; no requiere publish para private).
6. **Self-authorization:** Action → Authorize app → genera refresh token de producción. No invalida tokens anteriores. Cada cuenta autorizada genera su propio refresh token.
7. **Runtime:** refresh token → access token (1h) → llamadas con header `x-amz-access-token`.

## Endpoints / datos de contexto

| Ítem | Valor |
|---|---|
| Auth server | `https://api.amazon.com/auth/o2/token` |
| NA prod | `https://sellingpartnerapi-na.amazon.com` |
| EU prod (incluye AU) | `https://sellingpartnerapi-eu.amazon.com` |
| FE prod | `https://sellingpartnerapi-fe.amazon.com` |
| Sandbox | `sandbox.sellingpartnerapi-<na|eu|fe>.amazon.com` |
| Marketplace ID AU | `A39IBJ37TRP1C6` |
| Marketplace ID US | `ATVPDKIKX0DER` |

## Respuestas de formulario (verificadas ≤500 chars)

### Actividad empresarial + uso de API (494 chars)
> J&N Digital Expressions LLC es una empresa de e-commerce de marca propia (Wyoming, EE. UU.) que vende productos para mascotas, como alfombras olfativas, en Amazon Australia con FBA. Como desarrollador privado que integra su empresa, usaremos la API de socios vendedores para automatizar operaciones: sincronizar inventario, crear y actualizar listings, procesar pedidos, ajustar precios y descargar reportes de ventas. Solo accederemos a nuestra cuenta y catálogo; sin datos de terceros ni PII.

### Casos de uso (416 chars)
> Aplicación interna DE-Snuffle-AU para nuestra propia tienda en Amazon Australia: sincronizar inventario FBA en tiempo real, crear y actualizar listings, procesar pedidos, monitorear precios contra la competencia y descargar reportes de ventas para análisis, conciliación y reposición de stock. Uso exclusivo interno de nuestra organización, solo con datos de nuestra cuenta, sin PII de clientes ni datos de terceros.

### Terceros (campo 8 seguridad)
> No compartimos información de Amazon con terceros. Todos los datos se procesan internamente y se almacenan en servidores propios.

## Técnica de lectura de docs
Los `.md` de developer-docs.amazon.com se leen limpio con curl:
```bash
curl -sL "https://developer-docs.amazon.com/sp-api/docs/<slug>.md" -H "User-Agent: Mozilla/5.0"
```
Descubrir slugs con: `curl -sL https://developer-docs.amazon.com/sp-api/llms.txt`
Nota: las URLs `.md` usan `developer-docs.amazon.com` (con .com) aunque el HTML cite `developer-docs.amazon` sin dominio.
