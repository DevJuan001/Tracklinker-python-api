# AGENTS.md

> **Convenciones de nombre:** opencode reconoce `AGENTS.md` (mayúsculas) en la raíz del proyecto. Si tu editor/CLI no lo encuentra, renombra este archivo a `AGENTS.md`.

# Tracklinker Python API — Guía para Agentes AI

API REST para el sistema de gestión de inventario **Tracklinker**, construida con **FastAPI**, **MySQL**, **Celery** y **Redis**. Gestiona productos, proveedores, órdenes de entrada/salida, garantías, usuarios, reportes y un panel administrativo.

---

## Stack Técnico

| Capa | Tecnología | Versión |
| --- | --- | --- |
| Lenguaje | Python | `>= 3.13` |
| Framework web | FastAPI | `>= 0.136.1` |
| Servidor ASGI | Uvicorn | `>= 0.47.0` |
| Validación | Pydantic | `>= 2.13.4` |
| Base de datos | MySQL | `>= 8.0` |
| Driver MySQL | mysql-connector-python | `>= 9.7.0` |
| Caché / Rate limit / Broker | Redis | `>= 7.4.0` |
| Tareas en segundo plano | Celery | `>= 5.6.3` |
| Mailing | FastAPI-Mail | `>= 1.6.4` |
| Rate Limiter | FastAPI-Limiter | `0.1.6` |
| Auth | PyJWT + bcrypt | `>= 2.12.1` / `>= 5.0.0` |
| Gestor de dependencias | uv | última |

Las versiones exactas están fijadas en `uv.lock`.

---

## Skills disponibles en `.agents/skills/`

Este proyecto define skills especializadas que se cargan automáticamente para tareas específicas. **Carga la skill relevante antes de tocar su área.**

| Skill | Cuándo usarla |
| --- | --- |
| `.agents/skills/architecture/` | Modificar la estructura en capas, agregar features, mover archivos entre routes/controllers/services/repositories |
| `.agents/skills/business-logic/` | Tocar reglas de dominio (órdenes, garantías, productos, roles), crear/editar servicios |
| `.agents/skills/database/` | Escribir queries SQL, tocar repositories, entender el esquema (`database/01_database.sql`) |
| `.agents/skills/security/` | Tocar autenticación, JWT, roles, rate limiting, contraseñas, cookies |
| `.agents/skills/code-conventions/` | Cualquier edición de código (naming, sufijo de schemas, formato) |
| `.agents/skills/development-workflow/` | Correr el server, los tests, el worker de Celery, Docker, dependencias |

---

## Reglas arquitectónicas inviolables

Estas reglas las descubrió la búsqueda de service-to-service y deben respetarse siempre:

### 1. Los services NUNCA llaman a otros services
- Un service de un feature **solo** importa repositories (del propio feature o de otros, para joins/consultas).
- Si necesitas lógica de otro feature, **reutiliza el repository directamente** y maneja la transacción en el service actual (comparte `connection`).
- Excepción única: los **controllers** sí pueden llamar a services de otros features (ej. `SuggestionsController` usa `UsersService`).

### 2. La cadena de dependencias es estrictamente vertical
```
Route → Controller → Service → Repository → MySQL
```
- **No** saltar capas (un route no debe llamar a un repository directamente).
- **No** invertir el flujo (un repository no debe importar services).

### 3. Manejo de errores uniforme
- Los repositories **siempre** devuelven tuplas `(error: str | None, data)`.
- Los services **convierten** errores de repository en `ServiceError` y devuelven `(error, success, message)`.
- Los controllers **convierten** errores de service en `HTTPException`.

### 4. Conexiones a BD
- Cada método de service abre su propia `connection = get_connection()`.
- El try/except/finally cierra la conexión en el `finally`.
- Para flujos transaccionales que cruzan repositories, **comparte la misma `connection`** y haz un solo `connection.commit()`.

### 5. Validación con Pydantic
- Toda entrada de request va en un `*Schema` (sufijo `Schema`).
- Toda respuesta al cliente va en un `*Response` (sufijo `Response`).
- Modelos internos sin sufijo viven en `models/entities/`.

---

## Módulos de la API

Todos los endpoints bajo el prefijo `/api`:

| Módulo | Prefijo | Descripción |
| --- | --- | --- |
| Auth | `/api/auth` | Login, refresh, logout, verificación de roles, recuperación de contraseña |
| Users | `/api/users` | CRUD de usuarios, perfil (`/me`), roles, ciudades, contraseña |
| Products | `/api/products` | Productos, marcas, modelos, órdenes de entrada, estados |
| Categories | `/api/categories` | Categorías de productos |
| Subcategories | `/api/subcategories` | Subcategorías vinculadas a categorías |
| Suppliers | `/api/suppliers` | Proveedores y entradas asociadas |
| Output Orders | `/api/output_orders` | Órdenes de salida de inventario |
| Warranties | `/api/warranty_incidents` | Incidentes de garantía |
| Dashboard | `/api/dashboard` | Métricas del panel administrativo |
| Reports | `/api/reports` | Reportes analíticos por período |
| Suggestions | `/api/suggestions` | Envío de sugerencias por correo |

---

## Variables de entorno (`.env`)

Antes de arrancar la API, todas estas variables son obligatorias (validadas por `pydantic-settings`):

- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`
- `REDIS_URL`
- `ENVIRONMENT` (`development` o `production`)
- `ACCESS_TOKEN_SECRET_KEY`, `REFRESH_TOKEN_SECRET_KEY`, `ALGORITHM`
- `ACCESS_TOKEN_EXPIRE` (minutos), `REFRESH_TOKEN_EXPIRE` (días)
- `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_FROM`

Copia `.env.example` y completa los valores.

---

## Comandos esenciales

```bash
# 1. Instalar dependencias
uv sync

# 2. Levantar el server (con autoreload)
uvicorn app.main:app --reload

# 3. Levantar el worker de Celery (Windows: --pool=solo)
celery -A app.core.celery_app.celery worker --loglevel=info --pool=solo

# 4. Tests
pytest

# 5. Docker
docker build -t tracklinker-api .
docker run -p 8000:8000 --env-file .env tracklinker-api
```

Endpoints útiles:
- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- Health: `GET /`
- DB ping: `GET /ping-db`

---

## Estructura del proyecto

```
Tracklinker-python-api/
├── app/
│   ├── main.py                # Entrypoint FastAPI, CORS, routers, lifespan
│   ├── core/                  # Config, DB, JWT, Celery, mail, Redis, cache, exceptions
│   ├── middlewares/           # JWT, roles, request validation
│   ├── features/              # Módulos de negocio (feature-based)
│   │   ├── auth/              # Sin repositorio propio (consume UsersRepository)
│   │   ├── categories/
│   │   ├── dashboard/
│   │   ├── output_orders/
│   │   ├── products/          # Incluye brands, models, input orders, serials
│   │   ├── reports/           # Sin modelos (consume repos de otros features)
│   │   ├── subcategories/
│   │   ├── suggestions/       # Sin repositorio ni service (envía mail directo)
│   │   ├── suppliers/
│   │   ├── users/             # Incluye roles y cities
│   │   └── warranties/        # Incluye technicians
│   ├── tasks/                 # Celery tasks (correos)
│   ├── templates/             # HTML para emails
│   └── utils/                 # logger, date_formatter, periods, base_schema
├── database/
│   ├── 01_database.sql        # DDL (ejecutar primero)
│   ├── 02_dml.sql             # Seeds (ejecutar segundo)
│   └── 03_views.sql           # Vistas para reports (ejecutar tercero)
└── test/                      # pytest (estructura lista, sin casos aún)
```

Cada feature sigue (cuando aplica) la organización:

```
routes/ → controllers/ → services/ → repositories/ → models/
```

---

## Antes de cualquier cambio

1. Lee la skill correspondiente a tu área.
2. Si tocas queries SQL, lee `database/01_database.sql` para entender el esquema.
3. Si tocas un flujo que cruza features (ej. warranty → output order → product status), revisa los services involucrados para entender la transacción.
4. Si agregas una dependencia, usa `uv add <paquete>` (no edites `pyproject.toml` a mano).
5. No commitees secretos ni el archivo `.env`.
