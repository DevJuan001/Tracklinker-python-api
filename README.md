# Tracklinker API

API REST para el sistema de gestión de inventario **Tracklinker**, construida con **FastAPI**, **MySQL**, **Celery** y **Redis**.

---

## Tabla de Contenidos

- [Tech Stack](#tech-stack)
- [Prerrequisitos](#prerrequisitos)
- [Instalación](#instalación)
- [Variables de Entorno](#variables-de-entorno)
- [Ejecución](#ejecución)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Arquitectura](#arquitectura)
- [Seguridad](#seguridad)
- [Convenciones de Código](#convenciones-de-código)
- [Testing](#testing)
- [Contribuciones](#contribuciones)

---

## Tech Stack


| Tecnología                               | Versión   | Descripción                                  |
| ---------------------------------------- | --------- | -------------------------------------------- |
| [Python](https://www.python.org/)        | `>= 3.13` | Lenguaje principal del backend               |
| [FastAPI](https://fastapi.tiangolo.com/) | `latest`  | Framework web asíncrono de alto rendimiento  |
| [Uvicorn](https://www.uvicorn.org/)      | `latest`  | Servidor ASGI para ejecutar la aplicación    |
| [MySQL](https://www.mysql.com/)          | `>= 8.0`  | Base de datos relacional                     |
| [Redis](https://redis.io/)               | `7.4.8`   | Broker de mensajes y caché en memoria        |
| [Celery](https://docs.celeryq.dev/)      | `5.6.3`   | Cola de tareas distribuidas en segundo plano |
| [Docker](https://www.docker.com/)        | `latest`  | Contenedorización de la aplicación           |


---

## Prerrequisitos

Antes de comenzar, asegúrate de tener instalado:

- **Python** `>= 3.13` → [Descargar](https://www.python.org/downloads/)
- **MySQL** `>= 8.0` → [Descargar](https://dev.mysql.com/downloads/)
- **Redis** `7.4.8` → [Descargar](https://redis.io/downloads/)
- **Git** → [Descargar](https://git-scm.com/)

> [!NOTE]
> Redis es necesario tanto para el **rate limiting** (FastAPI Limiter) como para el **broker de Celery** que gestiona las tareas asíncronas como el envío de correos.

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
> Una vez que se instale `uv`, debes **reiniciar tu terminal** (o cerrar y volver a abrir tu editor/IDE) para que el sistema reconozca el comando.

```bash
# 1. Clonar el repositorio
git clone https://github.com/DevJuan001/Tracklinker-python-api.git
cd Tracklinker-python-api

# 2. Crear el entorno virtual con uv
uv venv

# 3. Activar el entorno virtual
# En Windows:
.venv\Scripts\activate
# En Mac / Linux:
source .venv/bin/activate

# 4. Instalar todas las dependencias
uv sync

# 5. Configurar las variables de entorno
# Copiar el archivo de ejemplo y completar los valores
cp .env.example .env
```

> [!IMPORTANT]
> Antes de iniciar la API debes configurar **todas** las variables del archivo `.env`. Pydantic validará que no falte ninguna al arrancar.

---

## Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto basándote en `.env.example`:


| Variable                   | Tipo    | Descripción                                            |
| -------------------------- | ------- | ------------------------------------------------------ |
| `DB_HOST`                  | `str`   | Host de la base de datos MySQL                         |
| `DB_PORT`                  | `int`   | Puerto de conexión a MySQL                             |
| `DB_USER`                  | `str`   | Usuario de la base de datos                            |
| `DB_PASSWORD`              | `str`   | Contraseña de la base de datos                         |
| `DB_NAME`                  | `str`   | Nombre de la base de datos                             |
| `REDIS_URL`                | `str`   | URL de conexión a Redis (ej: `redis://localhost:6379`) |
| `ENVIRONMENT`              | `str`   | Entorno actual (`development` o `production`)          |
| `ACCESS_TOKEN_SECRET_KEY`  | `str`   | Clave secreta para firmar el Access Token JWT          |
| `REFRESH_TOKEN_SECRET_KEY` | `str`   | Clave secreta para firmar el Refresh Token JWT         |
| `ALGORITHM`                | `str`   | Algoritmo de cifrado JWT (ej: `HS256`)                 |
| `ACCESS_TOKEN_EXPIRE`      | `int`   | Tiempo de expiración del Access Token en **minutos**   |
| `REFRESH_TOKEN_EXPIRE`     | `int`   | Tiempo de expiración del Refresh Token en **días**     |
| `MAIL_USERNAME`            | `email` | Correo electrónico para enviar emails                  |
| `MAIL_PASSWORD`            | `str`   | Contraseña del correo electrónico                      |
| `MAIL_FROM`                | `email` | Dirección de correo del remitente                      |


> [!TIP]
> Puedes generar claves secretas seguras con herramientas como [Random Key Generator](https://www.vondy.com/random-key-generator--ZzGGMYgS?lc=5).

---

## ▶ Ejecución

### Servidor de la API

```bash
# Iniciar el servidor de FastAPI con recarga automática
uvicorn app.main:app --reload
```

La API estará disponible en `http://localhost:8000` y la documentación interactiva en `http://localhost:8000/docs`.

### Worker de Celery

En una **segunda terminal** (con el entorno virtual activado):

```bash
celery -A app.core.celery_app.celery worker --loglevel=info --pool=solo
```

> [!WARNING]
> El flag `--pool=solo` es necesario en **Windows**. En Linux o Mac puedes omitirlo.

### Con Docker

```bash
docker build -t tracklinker-api .
docker run -p 8000:8000 tracklinker-api
```

### Desactivar el entorno virtual

```bash
deactivate
```

### Actualizar dependencias

```bash
# Si agregas nuevas dependencias utiliza uv
uv add <nombre-paquete>
```

---

## Estructura del Proyecto

```
Tracklinker-python-api/
│
├── 📄 .env.example              # Plantilla de variables de entorno
├── 📄 .gitignore                 # Archivos y carpetas ignorados por Git
├── 📄 Dockerfile                # Configuración para contenedor Docker
├── 📄 README.md                  # Documentación del proyecto
├── 📄 requirements.txt           # Dependencias de Python
│
├── 📂 app/                       # ← Código fuente principal
│   ├── 📄 main.py                # Punto de entrada de la API (FastAPI app)
│   │
│   ├── 📂 core/                  # ← Configuración central de la aplicación
│   │   ├── 📄 cache.py           # Utilidad para invalidar caché en Redis
│   │   ├── 📄 celery_app.py      # Instancia y configuración de Celery
│   │   ├── 📄 config.py          # Carga y validación de variables de entorno (Pydantic)
│   │   ├── 📄 database.py        # Conexión a la base de datos MySQL
│   │   ├── 📄 exception.py       # Excepciones personalizadas (ServiceError)
│   │   ├── 📄 mail.py            # Configuración de FastMail para envío de correos
│   │   ├── 📄 redis.py           # Inicialización y gestión del cliente Redis
│   │   └── 📄 security.py        # JWT (access/refresh tokens), hashing, cookies
│   │
│   ├── 📂 middlewares/           # ← Middlewares de la API
│   │   ├── 📄 jwt_middleware.py      # Verificación de JWT en rutas protegidas
│   │   ├── 📄 roles_middleware.py    # Control de acceso basado en roles
│   │   └── 📄 validate_request.py   # Validación de peticiones (cancelación)
│   │
│   ├── 📂 features/             # ← Módulos de negocio (arquitectura por feature)
│   │   ├── 📂 auth/             # Autenticación (login, registro, refresh token)
│   │   │   ├── 📂 controllers/
│   │   │   ├── 📂 models/
│   │   │   ├── 📂 routes/
│   │   │   └── 📂 services/
│   │   │
│   │   ├── 📂 categories/       # Gestión de categorías de productos
│   │   │   ├── 📂 controllers/
│   │   │   ├── 📂 models/
│   │   │   ├── 📂 repositories/
│   │   │   ├── 📂 routes/
│   │   │   └── 📂 services/
│   │   │
│   │   ├── 📂 dashboard/        # Panel de control y estadísticas
│   │   │   ├── 📂 controllers/
│   │   │   ├── 📂 repositories/
│   │   │   ├── 📂 routes/
│   │   │   └── 📂 services/
│   │   │
│   │   ├── 📂 output_orders/    # Órdenes de salida de inventario
│   │   │   ├── 📂 controllers/
│   │   │   ├── 📂 models/
│   │   │   ├── 📂 repositories/
│   │   │   ├── 📂 routes/
│   │   │   └── 📂 services/
│   │   │
│   │   ├── 📂 products/         # Gestión de productos del inventario
│   │   │   ├── 📂 controllers/
│   │   │   ├── 📂 models/
│   │   │   ├── 📂 repositories/
│   │   │   ├── 📂 routes/
│   │   │   └── 📂 services/
│   │   │
│   │   ├── 📂 reports/          # Generación de reportes
│   │   │   ├── 📂 controllers/
│   │   │   ├── 📂 routes/
│   │   │   └── 📂 services/
│   │   │
│   │   ├── 📂 subcategories/    # Gestión de subcategorías
│   │   │   ├── 📂 controllers/
│   │   │   ├── 📂 models/
│   │   │   ├── 📂 repositories/
│   │   │   ├── 📂 routes/
│   │   │   └── 📂 services/
│   │   │
│   │   ├── 📂 suggestions/     # Módulo de ayuda y sugerencias
│   │   │   ├── 📂 controllers/
│   │   │   ├── 📂 models/
│   │   │   └── 📂 routes/
│   │   │
│   │   ├── 📂 suppliers/       # Gestión de proveedores
│   │   │   ├── 📂 controllers/
│   │   │   ├── 📂 models/
│   │   │   ├── 📂 repositories/
│   │   │   ├── 📂 routes/
│   │   │   └── 📂 services/
│   │   │
│   │   ├── 📂 users/           # Gestión de usuarios del sistema
│   │   │   ├── 📂 controllers/
│   │   │   ├── 📂 models/
│   │   │   ├── 📂 repositories/
│   │   │   ├── 📂 routes/
│   │   │   └── 📂 services/
│   │   │
│   │   └── 📂 warranties/      # Gestión de garantías
│   │       ├── 📂 controllers/
│   │       ├── 📂 models/
│   │       ├── 📂 repositories/
│   │       ├── 📂 routes/
│   │       └── 📂 services/
│   │
│   │
│   ├── 📂 tasks/                # ← Tareas asíncronas de Celery
│   │   └── 📄 email_tasks.py    # Envío de correos (bienvenida, recuperación)
│   │
│   ├── 📂 templates/            # ← Plantillas HTML para correos electrónicos
│   │   ├── 📄 recover_password.html   # Email de recuperación de contraseña
│   │   ├── 📄 suggestion_mail.html    # Email de sugerencias
│   │   └── 📄 welcome_mail.html       # Email de bienvenida al sistema
│   │
│   └── 📂 utils/                # ← Utilidades y funciones auxiliares
│       ├── 📄 date_formatter.py  # Formateo de fechas en español
│       ├── 📄 logger.py          # Logger personalizado con formato estándar
│       └── 📄 periods.py         # Mapeo de períodos para consultas temporales
│
├── 📂 database/                  # ← Scripts SQL para la base de datos
│   ├── 📄 01_database.sql        # DDL: Creación de tablas y estructura
│   ├── 📄 02_dml.sql             # DML: Datos iniciales (seeds)
│   └── 📄 03_views.sql           # Vistas SQL para consultas complejas
│
└── 📂 test/                      # ← Pruebas automatizadas
    ├── 📄 conftest.py            # Configuración compartida de pytest
    ├── 📂 bdd/                   # Pruebas de comportamiento (BDD)
    │   └── 📄 test_flujo_auth.py # Test del flujo completo de autenticación
    └── 📂 unit/                  # Pruebas unitarias
        └── 📄 test_user_models.py # Tests de modelos de usuario
```

---

## Arquitectura

El proyecto utiliza una **arquitectura por features** (modular) con una capa de servicios centralizada:

```
Ruta (Route) → Controlador (Controller) → Servicio (Service) → Repositorio (Repository) → Base de Datos
```


| Capa             | Responsabilidad                                        |
| ---------------- | ------------------------------------------------------ |
| **Routes**       | Definición de endpoints y middlewares aplicados        |
| **Controllers**  | Recepción de la petición HTTP y delegación al servicio |
| **Services**     | Lógica de negocio y orquestación de operaciones        |
| **Repositories** | Acceso a datos y consultas SQL                         |
| **Models**       | Esquemas de validación con Pydantic                    |


Cada módulo dentro de `features/` es autocontenido y sigue esta estructura de capas.

### Responsabilidades de las Capas

1.  **Routes**: Define los endpoints, métodos HTTP y aplica middlewares (seguridad, rate limiting).
2.  **Controllers**: Orquestan la entrada de datos, validan esquemas básicos y delegan la ejecución al servicio.
3.  **Services**: Capa de **Lógica de Negocio**. Aquí se toman las decisiones, se procesan datos y se gestionan transacciones atómicas. No conocen detalles de la persistencia.
4.  **Repositories**: Única capa que interactúa con la base de datos (SQL). Encapsula las consultas y devuelve datos crudos o modelos internos.
5.  **Models/Schemas**: Pydantic se encarga de la validación de entrada (`Schema`) y el modelado de salida (`Response`).

---

## Seguridad

La seguridad es una prioridad en Tracklinker, implementando estándares modernos:

- **JWT con Cookies Seguras**: No enviamos el token en el cuerpo de la respuesta. Utilizamos cookies **HTTP-Only** y **Secure** para mitigar ataques XSS.
- **Hashing**: Las contraseñas nunca se almacenan en texto plano, utilizamos `bcrypt` para un hashing robusto.
- **RBAC (Role Based Access Control)**: Middleware dedicado para restringir endpoints según el rol del usuario (`Admin`, `Técnico`, etc.).
- **Rate Limiting**: Protección contra ataques de fuerza bruta utilizando Redis para limitar las peticiones por IP en endpoints críticos.
- **CORS**: Configuración estricta de orígenes permitidos para proteger la integridad de la API.

---

## Convenciones de Código


| Tipo de elemento           | Estilo       | Ejemplo correcto        | Ejemplo incorrecto     |
| -------------------------- | ------------ | ----------------------- | ---------------------- |
| **Clases**                 | `PascalCase` | `class UserModel:`      | `class user_model:`    |
| **Funciones / métodos**    | `snake_case` | `def get_all_users():`  | `def GetAllUsers():`   |
| **Variables**              | `snake_case` | `user_name = "Juan"`    | `UserName = "Juan"`    |
| **Constantes**             | `UPPER_CASE` | `DB_HOST = "localhost"` | `dbHost = "localhost"` |
| **Módulos (archivos .py)** | `snake_case` | `user_model.py`         | `UserModel.py`         |
| **Paquetes (carpetas)**    | `snake_case` | `core`, `models`        | `Core`, `Models`       |


### Nomenclatura de Modelos (Pydantic)

Los modelos se nombran con un sufijo según su propósito:


| Sufijo (Clase) | Uso                                           | Ejemplo                  |
| -------------- | --------------------------------------------- | ------------------------ |
| `Response`     | Respuestas que devuelve la API al cliente     | `ProductsAmountResponse` |
| *(sin sufijo)* | Modelos internos o de Base de Datos           | `ProductsAmount`         |
| `Schema`       | Datos que se reciben en el body de la request | `ProductsAmountSchema`   |

> [!NOTE]
> Los archivos deben agruparse en subcarpetas (`schemas/`, `responses/`, `entities/`) y usar nombres en plural (ej: `users_schemas.py`, `categories_responses.py`).

```python
# Respuesta de la API → sufijo Response
class SupplierInputResponse(BaseModel):
    ...

# Modelo interno → sin sufijo
class SupplierInput(BaseModel):
    ...

# Datos de entrada (request body) → sufijo Schema
class SupplierInputSchema(BaseModel):
    ...
```

---

## Testing

```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar solo pruebas unitarias
pytest test/unit/

# Ejecutar solo pruebas BDD
pytest test/bdd/
```

---

## Contribuciones

Cualquier contribución es bienvenida. Si deseas colaborar con el proyecto, sigue estos pasos:

1. Haz un **fork** del repositorio
2. Crea una rama para tu feature o fix:
  ```bash
   git checkout -b feat/mi-nueva-feature
  ```
3. Realiza tus cambios siguiendo las [convenciones de código](#convenciones-de-código)
4. Haz commit de tus cambios:
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

