# Roadmap — NURA INTELLIGENCE

> Plataforma de Business Intelligence Conversacional, construida con **Django**, **React** y **Supabase**.

**Leyenda de estado:** `[ ]` pendiente · `[~]` en progreso · `[x]` completado

**Stack de referencia:**

- Frontend: React (Vite + pnpm + TypeScript + TailwindCSS)
- Backend: Django + Django REST Framework
- ORM: Django ORM
- Base de datos: PostgreSQL (Supabase)
- Integraciones LLM: Groq, Cerebras, OpenRouter

---

## 0. Infraestructura y Fundamentos

- [x] Estructura de carpetas (`docker/`, `frontend/`, `nura/`, `services/`)
- [x] Docker + Docker Compose (backend Django + frontend + nginx gateway)
- [x] Variables de entorno documentadas (`.env.example` backend y frontend — antes no existían)
- [x] Arranque en local sin Docker (fallback automático a SQLite si no hay `DATABASE_URL`)
- [x] Página de estado en la raíz del backend (`/`) en vez del 404 crudo de Django
- [x] Manejador 404 de API en JSON (para `DEBUG=False`)
- [x] Página 404 propia en el frontend (React Router, antes quedaba en blanco)
- [x] Gestor de paquetes **pnpm** en frontend y Docker (migrado desde npm)
- [x] Endpoints "profesionales" sin prefijo `/api/` (`/chat/`, `/auth/`, `/sessions/`, `/datasets/`, etc.)
- [x] README con instrucciones reales de instalación local
- [ ] CI/CD (lint, tests, build automático) — no existe ningún workflow
- [ ] Testing automatizado (unit/integration) — cero archivos de test en todo el repo
- [ ] Logging estructurado (hoy son `print()` sueltos, sin `LOGGING` en `settings.py`)
- [ ] Monitoring / observabilidad (Sentry, Prometheus, healthchecks reales)
- [ ] **Celery** — no existe en absoluto (ni en `requirements.txt`, ni en `docker-compose.yml`)
- [ ] **Redis** — no existe (ni como broker, ni como caché de sesiones/resultados)
- [ ] Despliegue real de `services/ai` y `services/analytics` como microservicios independientes (hoy sus funciones se importan directo dentro de Django; el `docker-compose.yml` solo levanta `chat-service`)

---

## 1. Módulo — Cuentas y Workspace

### Autenticación
- [x] Registro, login, recuperación de contraseña, verificación de email (Django-allauth + dj-rest-auth)
- [x] JWT (access/refresh) — **corregido**: antes se decodificaba sin verificar firma (`verify_signature: False`), permitiendo suplantar usuarios
- [x] Todos los endpoints de chat/sesiones/datasets exigen `IsAuthenticated` — **corregido**: antes `/chat/` y `/analyze/` no pedían token
- [x] Perfil de usuario editable

### Workspace
- [x] Workspace automático por usuario (1:1 con `User`)
- [x] Aislamiento de datos entre usuarios — **corregido**: bug crítico donde `session_id='default'` era compartido globalmente por *todos* los usuarios (fuga de datos entre cuentas); probado con dos usuarios simultáneos
- [x] `list_sessions` / `get_session_history` / `rename_session` / `delete_session` filtran por dueño — **corregido**: antes `list_sessions` devolvía las sesiones de *todos* los usuarios
- [x] Migración de base de datos corregida — **corregido**: `0002_add_workspace` duplicaba `0001_initial` y rompía cualquier instalación desde cero

### Archivos y cuotas
- [x] Carga de CSV/XLSX/JSON con validación (tipo, tamaño, integridad, encoding)
- [x] Metadata rica: tags, categorías, favoritos, archivado, hash para deduplicar
- [x] Cuotas por plan (free/pro/enterprise): mensajes/día, almacenamiento total, cantidad de datasets, tamaño máx. de archivo — **nuevo**: los campos `plan`/`daily_messages` existían sin usarse en ningún lado
- [x] Endpoint `GET /workspace/usage/` para mostrar uso vs. límites
- [ ] Roles y organizaciones (hoy es estrictamente 1 usuario = 1 workspace, sin jerarquías)
- [ ] Verificación en dos pasos / MFA

---

## 2. Módulo — Motor de Datos

- [x] Limpieza automática (detección de encabezados, normalización de números/fechas, duplicados, nulos, tipos)
- [x] Conversión CSV → dataset interno, con reintentos de encoding/separador
- [x] Conversión **XLSX** → dataset interno
- [x] Conversión **JSON** → dataset interno — **nuevo**: antes se aceptaba y validaba pero nunca se convertía de verdad (cualquier `.json` intentaba leerse como CSV y fallaba o producía basura). Ahora soporta lista de objetos, contenedores (`{"data": [...]}`), objeto único, dict de columnas y listas simples
- [x] Análisis automático al subir un dataset **también para JSON** — **corregido**: una lista blanca hardcodeada (`file_type in ['csv','xlsx']`) excluía `json` del análisis, aunque estuviera "permitido"
- [x] CRUD de datasets: crear, ver, actualizar, eliminar
- [x] Versionado de datasets (`DatasetVersion`, restaurar versión anterior)
- [x] Fusión (merge) de datasets
- [x] Exploración: preview, columnas, estadísticas, búsqueda, filtros
- [x] Deduplicación por hash de archivo
- [ ] Procesamiento **asíncrono** de archivos grandes (hoy todo corre síncrono dentro del request HTTP — requiere Celery/Redis, que no existen)
- [ ] Carga de datos desde fuentes externas (bases de datos, APIs) — solo archivos subidos manualmente
- [ ] Streaming/chunked upload para archivos muy grandes

---

## 3. Módulo — IA Conversacional + Analítica

- [x] Chat con contexto del dataset activo y del historial de la sesión
- [x] Router multi-proveedor de LLM con fallback en cascada (Groq → Cerebras → OpenRouter)
- [x] Sistema de agentes especializados (memoria, riesgo, insight, recomendación, ejecutivo, operaciones, forecast)
- [x] Enrutamiento de intención por LLM (`route_intent`) hacia el agente correcto
- [x] Orden de agentes por prioridad real — **corregido**: el campo `priority` existía pero nunca se leía en ningún lado
- [x] Prompt del router completo — **corregido**: faltaba la regla explícita para el agente de memoria (`context`)
- [x] Código muerto eliminado (`run_agent_system()`, importado pero nunca invocado)
- [x] Motor analítico: correlaciones, distribuciones, anomalías (Isolation Forest), KPIs automáticos
- [x] Detección proactiva de hallazgos (insights + señales de fraude) al analizar, sin que el usuario pregunte
- [x] Chat sobre contenido de documentos **.docx** — **nuevo**: existía una rama de código (`mode: "rag_document"`) que nunca se activaba porque nada generaba ese contexto; ahora se extrae el texto real con `python-docx`
- [ ] Chat sobre contenido de **.pdf** (falta una librería de extracción de texto, p. ej. `pdfplumber`/`PyMuPDF`, no incluida hoy en `requirements.txt`)
- [ ] Orquestación multi-agente real en paralelo (hoy corre un solo agente especializado por turno, pese a que el prompt dice "sistema multiagente")
- [ ] Memoria de largo plazo / embeddings vectoriales (la memoria hoy es resumen + historial reciente, no búsqueda semántica)

---

## 4. Módulo — Visualización y Reportes

- [x] Gráficos de barras, líneas y pie (Chart.js en el frontend)
- [x] Exportación de reportes a **PDF** — **nuevo**: el botón "exportar_reporte_pdf()" era texto decorativo sin ningún handler; ahora genera un PDF real con `reportlab` (resumen, KPIs, salud de datos, anomalías, correlaciones, hallazgos)
- [x] Exportación de reportes a **DOCX** — **nuevo**: `python-docx` estaba instalado sin usarse en ningún lugar del proyecto
- [x] Descarga funcional desde el frontend (loading/error states, blob download)
- [ ] Gráficos de **heatmap** y **scatter**
- [ ] Export de gráficos individuales a PNG/SVG
- [ ] Dashboards armables (drag & drop), manuales o generados por IA — hoy la navegación es por secciones fijas, no hay un builder
- [ ] Exportación a **PPTX**
- [ ] Reportes diferenciados por audiencia (ejecutivo / técnico / financiero) — hoy es un único formato de reporte

---

## 5. Módulo — Automatización y Colaboración

- [ ] Triggers configurables (archivo nuevo, anomalía detectada, fecha) → acciones automáticas
- [ ] Multiusuario real: organizaciones, roles (owner/admin/member)
- [ ] Compartir workspaces/datasets/reportes entre usuarios
- [ ] Comentarios sobre datasets/reportes
- [ ] Integraciones externas: bases de datos, Google Drive/Dropbox
- [ ] Integraciones externas: APIs REST/GraphQL de terceros

> Este módulo no tiene ninguna funcionalidad implementada todavía — es el que está más atrasado junto con el Módulo 6.

---

## 6. Módulo — IA Empresarial + Enterprise

- [~] Agentes especializados — existen 7 agentes especializados por *tipo de análisis* (riesgo, insight, ejecutivo, operaciones, forecast...), pero no específicamente organizados *por área de negocio* (finanzas, ventas, marketing) como pide la especificación original
- [~] Forecasting — existe un forecast lineal simple (`simple_forecast`), pero no simulaciones "qué pasa si..." con escenarios configurables
- [ ] Recomendaciones proactivas automáticas (fuera del flujo de chat/análisis inicial)
- [ ] SSO / MFA
- [ ] Multiempresa (tenancy más allá de "1 usuario = 1 workspace")
- [ ] API pública documentada (`drf-spectacular` está instalado pero no hay endpoint de Swagger/OpenAPI activado en `urls.py`)
- [ ] Caché (requiere Redis, inexistente)
- [ ] Balanceo de carga entre instancias del backend
- [ ] Escalabilidad real como microservicios (hoy `services/ai` y `services/analytics` no se despliegan de forma independiente)

---

## Notas finales

- Cada fase se considera "cerrada" cuando su entregable está funcionando en el entorno de desarrollo y ha sido validado manualmente contra los criterios de esta lista.
- Este documento es vivo: debe actualizarse marcando checkboxes y agregando notas de decisiones tomadas durante el desarrollo.