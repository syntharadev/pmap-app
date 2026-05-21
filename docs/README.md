# PMAP.APP / Anti-gravity System Blueprint

**Filosofía Core**: Auditoría forense Zero-Knowledge (Local-first). Los datos del usuario nunca se escriben en disco.

**Métricas Clave**: Volumetría de turnos, ratio de código, e Índice de Amnesia (detección de degradación del contexto de la IA evaluada).

**Modelo de Negocio**: Híbrido. Nube efímera (Free) y Binario Soberano (Indie: 79€ | Pro: 124€/año | Enterprise: 249€/año) gestionado vía Gumroad.

**Estado Crítico Actual**: Transición del código fuente al empaquetado final B2B.

---

## Visión CODEGRAPH: Mapa de Dependencias (PMAP v3.1)

Actualmente, la arquitectura de PMAP.APP está dividida en dos grandes ecosistemas aislados que se comunican por un único puente (el License Heartbeat).

### [ECOSISTEMA NUBE / FREE-TIER]
```text
├── Nodo: Gumroad (MoR)
│   └── Edge: Webhook (POST) sobre ventas/licencias -> Apunta a Render.
├── Nodo: Render.com (Cloud Server)
│   └── Archivo: `cloud_server.py`
│   └── Dependencia: SDK de Supabase.
│   └── Función: Recibe el Webhook, inyecta la nueva licencia en la DB.
└── Nodo: Supabase (Identity Hub)
    └── Tabla: `sys_license` (Almacena keys y tiers).
```

### [ECOSISTEMA SOBERANO / PRO-TIER (Anti-gravity Core)]
```text
├── Nodo: Frontend & Trigger
│   ├── Archivo: `index.html` (UI B2B, Logos SVG, Dashboard Métricas).
│   └── Componente: `Bookmarklet (JS)` -> Scrapea la web, extrae el chat.
├── Nodo: Local Server (FastAPI)
│   ├── Archivo: `pmap_core/pmap/server.py`
│   ├── Dependencia 1: Ping (HTTP GET) a Supabase para validar licencia en el arranque.
│   └── Dependencia 2: Recibe el POST del Bookmarklet.
└── Nodo: Analizador Forense (DuckDB)
    ├── Archivo: `pmap_core/pmap/analyzer.py`
    ├── Función: Ingesta en RAM (`:memory:`), calcula `Amnesia Index`.
    └── Salida: Devuelve JSON al Bookmarklet para renderizar alertas.
```
