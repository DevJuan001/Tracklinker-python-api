from contextlib import asynccontextmanager
from app.core.redis import init_redis, close_redis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import get_connection
from app.routes import user_routes, dashboard_routes, category_routes, subcategories_routes, auth_routes, output_details_routes, suggestion_routes, guarantees_routes, products_routes, reports_routes, suppliers_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicialización de recursos
    redis = await init_redis(app)
    await FastAPILimiter.init(redis)
    yield
    # Cierre de recursos
    await close_redis()

# Instancia principal de la app FastAPI
app = FastAPI(
    title="API con FastAPI y MySQL",
    description="Api para tracklinker",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint para probar conexión a la base de datos
@app.get("/ping-db")
def ping_db():
    connection = get_connection()
    if connection:
        connection.close()
        return {
            "status": "Conexion Exitosa a la base de datos"
        }
    else:
        return {
            "status": "Error al intentar conectarse a la base de datos"
        }

# Endpoint raíz para probar ejecución de la API
@app.get("/")
def root():
    return {
        "message": "API funcionando"
    }


# Rutas de autenticación
app.include_router(auth_routes.router)
# Rutas para el modúlo de Usuarios
app.include_router(user_routes.router)
# Rutas para el modúlo de Garantias
app.include_router(guarantees_routes.router)
# Rutas para tabla de detalles de salida
app.include_router(output_details_routes.router)
# Rutas para el modulo de categorias
app.include_router(category_routes.router)
# Rutas para el modulo de subcategorias
app.include_router(subcategories_routes.router)
# Rutas para el modúlo de Panel de control
app.include_router(dashboard_routes.router)
# Rutas para el modúlo de productos
app.include_router(products_routes.router)
# Rutas para el modúlo de reportes
app.include_router(reports_routes.router)
# Rutas para el modúlo de Proveedores
app.include_router(suppliers_routes.router)
# Rutas para el modúlo de Ayuda o sugerencias
app.include_router(suggestion_routes.router)
