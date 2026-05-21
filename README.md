# Tracklinker API

API REST para el sistema de gestión de inventario **Tracklinker**, construida con **FastAPI**, **MySQL**, **Celery** y **Redis**. Gestiona productos, proveedores, órdenes de entrada/salida, garantías, usuarios, reportes y un panel de control administrativo.

---

## Tabla de Contenidos

- [Tech Stack](#tech-stack)
- [Prerrequisitos](#prerrequisitos)
- [Instalación](#instalación)
- [Base de Datos](#base-de-datos)
- [Variables de Entorno](#variables-de-entorno)
- [Ejecución](#ejecución)
- [Módulos de la API](#módulos-de-la-api)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Arquitectura](#arquitectura)
- [Seguridad](#seguridad)
- [Convenciones de Código](#convenciones-de-código)
- [Testing](#testing)
- [Contribuciones](#contribuciones)

---

## Tech Stack

| Tecnología | Versión | Descripción |
| --- | --- | --- |
| [Python](https://www.python.org/) | `3.13` | Lenguaje principal del backend |
| [uv](https://docs.astral.sh/uv/) | — | Gestor de entorno virtual y dependencias |
| [FastAPI](https://fastapi.tiangolo.com/) | `0.136.1` | Framework web asíncrono |
| [Uvicorn](https://www.uvicorn.org/) | `0.47.0` | Servidor ASGI |
| [Pydantic](https://docs.pydantic.dev/) | `2.13.4` | Validación de datos y configuración |
| [MySQL](https://www.mysql.com/) | `>= 8.0` | Base de datos relacional |
| [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/) | `9.7.0` | Driver de conexión a MySQL |
| [Redis](https://redis.io/) | `7.4.0` | Rate limiting, caché y broker de Celery |
| [Celery](https://docs.celeryq.dev/) | `5.6.3` | Tareas en segundo plano (correos) |
| [FastAPI-Mail](https://sabuhish.github.io/fastapi-mail/) | `1.6.4` | Envío de correos HTML |
| [FastAPI-Limiter](https://github.com/long2ice/fastapi-limiter) | `0.1.6` | Rate limiting por IP |
| [PyJWT](https://pyjwt.readthedocs.io/) | `2.12.1` | Tokens JWT (access y refresh) |
| [bcrypt](https://github.com/pyca/bcrypt/) | `5.0.0` | Hashing de contraseñas |
| [Docker](https://www.docker.com/) | — | Contenedorización (imagen Python 3.13 + uv) |

Las versiones exactas están fijadas en `uv.lock`.

---

## Prerrequisitos

Antes de comenzar, asegúrate de tener instalado:

- **Python** `3.13` → [Descargar](https://www.python.org/downloads/)
- **uv** → [Instalación](https://docs.astral.sh/uv/getting-started/installation/)
- **MySQL** `>= 8.0` → [Descargar](https://dev.mysql.com/downloads/)
- **Redis** → [Descargar](https://redis.io/downloads/)
- **Git** → [Descargar](https://git-scm.com/)

> [!NOTE]
> Redis se usa para **rate limiting** (FastAPI Limiter), **caché** de consultas y como **broker/backend de Celery** para el envío asíncrono de correos.

---

## Instalación

```bash
# 0. Instalar uv (si no lo tienes instalado)
# En macOS y Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh
# En Windows:
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

> [!WARNING]
> Tras instalar `uv`, reinicia la terminal (o el IDE) para que el comando quede disponible en el PATH.

```bash
# 1. Clonar el repositorio
git clone https://github.com/DevJuan001/Tracklinker-python-api.git
cd Tracklinker-python-api

# 2. Crear el entorno virtual
uv venv

# 3. Activar el entorno virtual
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

# 4. Instalar dependencias (según pyproject.toml y uv.lock)
uv sync

# 5. Configurar variables de entorno
# Windows:
copy .env.example .env
# macOS / Linux:
cp .env.example .env
```

> [!IMPORTANT]
> Completa **todas** las variables en `.env` antes de arrancar la API. `pydantic-settings` validará que no falte ninguna al iniciar.

---

## Base de Datos

Los scripts SQL viven en `database/` y deben ejecutarse en este orden:

| Archivo | Contenido |
| --- | --- |
| `01_database.sql` | DDL: creación del esquema `DB_TRACKLINKER` y tablas |
| `02_dml.sql` | DML: datos iniciales (roles, ciudades, usuarios de prueba, etc.) |
| `03_views.sql` | Vistas SQL para consultas agregadas |

```bash
# Ejemplo con el cliente de MySQL (ajusta usuario y host)
mysql -u root -p < database/01_database.sql
mysql -u root -p < database/02_dml.sql
mysql -u root -p < database/03_views.sql
```

### Roles del sistema

Definidos en los seeds (`02_dml.sql`):

| Rol | Descripción |
| --- | --- |
| `Admin` | Acceso completo al panel y gestión |
| `Almacen` | Gestión de inventario, productos y órdenes |
| `Tecnico` | Operaciones de garantías y salidas |
| `Cliente` | Rol de cliente final |

---

## Variables de Entorno

Crea un archivo `.env` en la raíz basándote en `.env.example`:

| Variable | Tipo | Descripción |
| --- | --- | --- |
| `DB_HOST` | `str` | Host de MySQL |
| `DB_PORT` | `int` | Puerto de MySQL |
| `DB_USER` | `str` | Usuario de la base de datos |
| `DB_PASSWORD` | `str` | Contraseña de la base de datos |
| `DB_NAME` | `str` | Nombre de la base de datos |
| `REDIS_URL` | `str` | URL de Redis (ej: `redis://localhost:6379`) |
| `ENVIRONMENT` | `str` | Entorno (`development` o `production`) |
| `ACCESS_TOKEN_SECRET_KEY` | `str` | Clave para firmar el Access Token JWT |
| `REFRESH_TOKEN_SECRET_KEY` | `str` | Clave para firmar el Refresh Token JWT |
| `ALGORITHM` | `str` | Algoritmo JWT (ej: `HS256`) |
| `ACCESS_TOKEN_EXPIRE` | `int` | Expiración del access token en **minutos** |
| `REFRESH_TOKEN_EXPIRE` | `int` | Expiración del refresh token en **días** |
| `MAIL_USERNAME` | `email` | Cuenta SMTP para envío de correos |
| `MAIL_PASSWORD` | `str` | Contraseña de la cuenta SMTP |
| `MAIL_FROM` | `email` | Dirección remitente |

> [!TIP]
> Puedes generar claves secretas con [Random Key Generator](https://www.vondy.com/random-key-generator--ZzGGMYgS?lc=5).

---

## Ejecución

### Servidor de la API

```bash
# Iniciar el servidor de FastAPI con recarga automática
uvicorn app.main:app --reload
```

| Recurso | URL |
| --- | --- |
| API | `http://localhost:8000` |
| Swagger UI | `http://localhost:8000/docs` |
| ReDoc | `http://localhost:8000/redoc` |
| Health check | `GET /` |
| Ping base de datos | `GET /ping-db` |

### Worker de Celery

En una **segunda terminal** (con el entorno virtual activado):

```bash
celery -A app.core.celery_app.celery worker --loglevel=info --pool=solo
```

> [!WARNING]
> En **Windows** usa `--pool=solo`. En Linux o macOS puedes omitirlo.

Tareas registradas en `app/tasks/email_tasks.py`:

- `send_welcome_email` — correo de bienvenida al crear usuario
- `recovery_password_email` — correo de recuperación de contraseña

### Con Docker

```bash
docker build -t tracklinker-api .
docker run -p 8000:8000 --env-file .env tracklinker-api
```

El `Dockerfile` usa **Python 3.13-slim**, instala dependencias con **uv** (`uv sync --frozen`) y expone el puerto `8000`.

### Gestión de dependencias

```bash
# Agregar una dependencia
uv add <nombre-paquete>

# Auditar vulnerabilidades (incluido en el proyecto)
pip-audit
```

### Desactivar el entorno virtual

```bash
deactivate
```

---

## Módulos de la API

Todos los endpoints de negocio están bajo el prefijo `/api`. La autenticación usa cookies **HTTP-Only** para los tokens JWT.

| Módulo | Prefijo | Descripción |
| --- | --- | --- |
| **Auth** | `/api/auth` | Login, refresh, logout, verificación de roles, recuperación de contraseña |
| **Users** | `/api/users` | CRUD de usuarios, perfil (`/me`), roles, ciudades, contraseña |
| **Products** | `/api/products` | Productos, marcas, modelos, órdenes de entrada, estados |
| **Categories** | `/api/categories` | Categorías de productos |
| **Subcategories** | `/api/subcategories` | Subcategorías vinculadas a categorías |
| **Suppliers** | `/api/suppliers` | Proveedores y entradas asociadas |
| **Output Orders** | `/api/output_orders` | Órdenes de salida de inventario |
| **Warranties** | `/api/warranty_incidents` | Incidentes de garantía |
| **Dashboard** | `/api/dashboard` | Métricas y estadísticas del panel administrativo |
| **Reports** | `/api/reports` | Reportes analíticos por período (usuarios, productos, categorías, etc.) |
| **Suggestions** | `/api/suggestions` | Envío de sugerencias por correo |

El frontend autorizado en CORS está configurado en `app/main.py`:

- `http://localhost:5173` (desarrollo local)
- `https://tracklinker-frontend-web.vercel.app` (producción)

---

## Estructura del Proyecto

```
Tracklinker-python-api/
│
├── .env.example              # Plantilla de variables de entorno
├── .gitignore
├── .python-version           # Python 3.13
├── Dockerfile                # Imagen Docker (uv + uvicorn)
├── pyproject.toml            # Dependencias y metadatos del proyecto
├── uv.lock                   # Lockfile de dependencias
├── README.md
│
├── app/
│   ├── main.py               # Punto de entrada FastAPI, CORS, routers
│   │
│   ├── core/                 # Configuración central
│   │   ├── cache.py          # Invalidación de caché en Redis
│   │   ├── celery_app.py     # Instancia y configuración de Celery
│   │   ├── config.py         # Settings (Pydantic) desde .env
│   │   ├── database.py       # Conexión MySQL
│   │   ├── exception.py      # Excepciones personalizadas (ServiceError)
│   │   ├── mail.py           # FastMail (SMTP)
│   │   ├── redis.py          # Cliente Redis (lifespan)
│   │   └── security.py       # JWT, bcrypt, cookies
│   │
│   ├── middlewares/
│   │   ├── jwt_middleware.py     # Verificación de JWT
│   │   ├── roles_middleware.py   # RBAC (require_roles)
│   │   └── validate_request.py   # Validación de peticiones
│   │
│   ├── features/             # Módulos de negocio (feature-based)
│   │   ├── auth/
│   │   ├── categories/
│   │   ├── dashboard/
│   │   ├── output_orders/
│   │   ├── products/         # Incluye marcas, modelos, input orders, serials
│   │   │   ├── controllers/
│   │   │   ├── models/
│   │   │   │   ├── entities/
│   │   │   │   ├── responses/
│   │   │   │   └── schemas/
│   │   │   ├── repositories/
│   │   │   ├── routes/
│   │   │   └── services/
│   │   ├── reports/
│   │   ├── subcategories/
│   │   ├── suggestions/
│   │   ├── suppliers/
│   │   ├── users/            # Incluye roles y ciudades
│   │   └── warranties/
│   │
│   ├── tasks/
│   │   └── email_tasks.py    # Tareas Celery (correos)
│   │
│   ├── templates/            # Plantillas HTML para emails
│   │   ├── recover_password.html
│   │   ├── suggestion_mail.html
│   │   └── welcome_mail.html
│   │
│   └── utils/
│       ├── base_schema.py
│       ├── date_formatter.py
│       ├── logger.py
│       └── periods.py
│
└── database/
    ├── 01_database.sql       # DDL
    ├── 02_dml.sql            # Seeds
    └── 03_views.sql          # Vistas SQL
```

Cada feature sigue la misma organización por capas cuando aplica:

```
routes/ → controllers/ → services/ → repositories/ → models/
```

---

## Arquitectura

El proyecto utiliza una **arquitectura por features** (modular) con una capa de servicios centralizada:

```
Ruta (Route) → Controlador (Controller) → Servicio (Service) → Repositorio (Repository) → MySQL
```

| Capa | Responsabilidad |
| --- | --- |
| **Routes** | Endpoints HTTP, middlewares (`require_roles`, `RateLimiter`) |
| **Controllers** | Entrada/salida HTTP; delega al servicio |
| **Services** | Lógica de negocio y orquestación |
| **Repositories** | Consultas SQL y acceso a datos |
| **Models** | Esquemas Pydantic (`Schema`, `Response`, entidades internas) |

### Flujo de arranque (`lifespan`)

1. Inicializa Redis (`init_redis`)
2. Configura FastAPI Limiter
3. Al cerrar la app, libera la conexión Redis (`close_redis`)

---

## Seguridad

- **JWT en cookies HTTP-Only**: access y refresh tokens no se devuelven en el body; mitiga XSS.
- **bcrypt**: hashing de contraseñas en registro y actualización.
- **RBAC**: middleware `require_roles` restringe endpoints por rol (`Admin`, `Almacen`, `Tecnico`, etc.).
- **Rate limiting**: Redis + FastAPI Limiter (ej. login: 3 req/min, listados: 30–50 req/min).
- **CORS**: orígenes explícitos para el frontend de Tracklinker.

---

## Convenciones de Código

| Tipo de elemento | Estilo | Ejemplo correcto | Ejemplo incorrecto |
| --- | --- | --- | --- |
| **Clases** | `PascalCase` | `class UserModel:` | `class user_model:` |
| **Funciones / métodos** | `snake_case` | `def get_all_users():` | `def GetAllUsers():` |
| **Variables** | `snake_case` | `user_name = "Juan"` | `UserName = "Juan"` |
| **Constantes** | `UPPER_CASE` | `DB_HOST = "localhost"` | `dbHost = "localhost"` |
| **Módulos (.py)** | `snake_case` | `user_model.py` | `UserModel.py` |
| **Paquetes** | `snake_case` | `core`, `models` | `Core`, `Models` |

### Nomenclatura de modelos (Pydantic)

| Sufijo | Uso | Ejemplo |
| --- | --- | --- |
| `Schema` | Body de entrada (request) | `CreateProductSchema` |
| `Response` | Respuesta al cliente | `ProductsAmountResponse` |
| *(sin sufijo)* | Modelos internos o de dominio | `ProductsAmount` |

Los modelos se agrupan en subcarpetas (`schemas/`, `responses/`, `entities/`) dentro de cada feature.

```python
# Respuesta de la API
class SupplierInputResponse(BaseModel): ...

# Modelo interno
class SupplierInput(BaseModel): ...

# Datos de entrada
class SupplierInputSchema(BaseModel): ...
```

---

## Testing

El proyecto declara **pytest** y **pytest-asyncio** en `pyproject.toml`. Para ejecutar pruebas cuando existan bajo una carpeta `test/`:

```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar solo pruebas unitarias
pytest test/unit/

# Ejecutar solo pruebas BDD
pytest test/bdd/
```

> [!NOTE]
> Aún no hay suite de tests en el repositorio; las dependencias están listas para cuando se agreguen.

---

## Contribuciones

Cualquier contribución es bienvenida. Si deseas colaborar con el proyecto, sigue estos pasos:

1. Haz un **fork** del repositorio
2. Crea una rama:
   ```bash
   git checkout -b feat/mi-nueva-feature
   ```
3. Sigue las [convenciones de código](#convenciones-de-código)
4. Commit:
   ```bash
   git commit -m "feat: descripción breve del cambio"
  ```
5. Sube tu rama:
  ```bash
   git push origin feat/mi-nueva-feature
  ```
6. Abre un **Pull Request** hacia la rama `main`

> [!NOTE]
> Asegúrate de que tu código sigue las convenciones del proyecto y de que las pruebas existentes siguen pasando antes de abrir un PR.

