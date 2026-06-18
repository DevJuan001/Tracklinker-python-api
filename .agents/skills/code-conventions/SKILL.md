---
name: code-conventions
description: Use for any code edit. Covers naming (PascalCase classes, snake_case everything else), the strict `*Schema` / `*Response` / no-suffix Pydantic convention, the `(error, data)` repository return contract, error messages in Spanish, and the static-method style for services and repositories.
---

# Code Conventions Skill

These conventions are enforced by code review and by the layout of existing files. Match them exactly when adding or editing code.

## Naming

| Element | Style | Example |
| --- | --- | --- |
| Classes | `PascalCase` | `ProductsService`, `CategoriesRepository`, `WarrantiesController` |
| Functions / methods | `snake_case` | `get_all_products`, `find_user_by_email`, `verify_password` |
| Variables | `snake_case` | `user_name`, `warranty_id` |
| Constants | `UPPER_SNAKE_CASE` | `ACCESS_TOKEN_EXPIRE`, `WARRANTY_STATUS_PRODUCT_MAP` |
| Modules (`.py` files) | `snake_case` | `users_service.py`, `output_orders_repository.py` |
| Packages / folders | `snake_case` | `features/`, `repositories/`, `models/` |
| Class attributes (Pydantic) | `snake_case` | `user_id`, `product_status` |

## Pydantic model suffix convention (mandatory)

| Suffix | Lives in | Purpose | Example |
| --- | --- | --- | --- |
| `*Schema` | `models/schemas/` | **Request body / query / path** validation | `CreateUserSchema`, `ProductsFilterSchema` |
| `*Response` | `models/responses/` | **Response to the client** | `CategoryResponse`, `WarrantyByStatusResponse` |
| *(no suffix)* | `models/entities/` | Internal/domain models, used only between layers | `CreateProductDetailsEntity`, `UpdateOutputDetails` |

**Never**:
- Use `*Schema` for a response or `*Response` for a request.
- Skip the suffix on a public-facing Pydantic model.

Each `models/` subfolder can have its own `__init__.py` to re-export, but the file split is the simplest and preferred.

## Service and repository methods are `@staticmethod`

Every method in a `*Service` or `*Repository` class is decorated `@staticmethod`. There is no `self` or `cls`.

```python
class ProductsService:
    @staticmethod
    def get_all_products(filters: ProductsFilterSchema):
        ...
```

Controllers are also `@staticmethod` classes. Only the routes (FastAPI handlers) use `Depends(...)` and receive injected parameters.

## Repository return contract (mandatory)

Every repository method returns a tuple:

```python
# Single-value method
return None, data
return "Mensaje de error en español", None

# Two-value method (e.g. create returning the new id)
return None, success, new_id
return "Mensaje de error en español", False, None
```

The **first element is always a string error or `None`**, never a boolean or exception. Errors are already logged inside the repository.

## Service error handling

Services wrap repository calls in `try / except / finally`:

```python
@staticmethod
def create_thing(data: CreateThingSchema):
    connection = get_connection()
    try:
        error, existing = ThingsRepository.find_by_name(data.name, connection)
        if error or existing:
            raise ServiceError("Ya existe un thing con este nombre")

        error, success, message = ThingsRepository.create_thing(data, connection)
        if error or not success:
            raise ServiceError(error or "No se pudo crear el thing")

        connection.commit()
        return None, True, "Thing creado correctamente"

    except ServiceError as e:
        connection.rollback()
        return e.message, False, None
    except Exception as e:
        connection.rollback()
        logger.error("Error en create_thing: %s", e, exc_info=True)
        return "Error al intentar crear el thing", False, None
    finally:
        connection.close()
```

Three things to notice:
1. Use `ServiceError` to short-circuit on known validation failures.
2. `connection.rollback()` runs on **both** `ServiceError` and unexpected `Exception`.
3. `connection.close()` is in the `finally` — it always runs.

## Controller return pattern

Controllers convert `(error, success, ...)` into either an `HTTPException` or a success dict:

```python
@staticmethod
def get_by_id(id: int):
    error, data = ThingsService.get_by_id(id)
    if error:
        raise HTTPException(status_code=404, detail=error)
    return {"data": data}
```

| Status code | Use for |
| --- | --- |
| `400` | Bad input / business rule violation (duplicate, missing field, etc.) |
| `401` | Auth failure (invalid credentials, missing token) |
| `403` | Role denied (raised by `require_roles`, not controllers) |
| `404` | Resource not found |

## Error messages in Spanish

Every user-facing error string is **in Spanish**. The repository logs in Spanish too:

```python
return "Error al intentar obtener los productos", None
logger.error("Error en get_all_products: %s", e, exc_info=True)
```

Keep messages short, lowercase-leaning, and free of accents in the variable names but **with** accents in the strings (e.g. `"Categoría"`, `"garantía"`).

## Logging

Use the project logger everywhere a `try/except Exception` exists:

```python
from app.utils.logger import get_logger

logger = get_logger("products.service")     # pass the dotted module name

try:
    ...
except Exception as e:
    logger.error("Error en get_all_products: %s", e, exc_info=True)
    return "Error al intentar ...", None
```

Never use `print()` for error reporting.

## Type hints

All function signatures **must** have type hints for parameters and (where reasonable) the return type. Pydantic models are imported from `models/schemas/...` or `models/responses/...`.

```python
@staticmethod
def create_category(category_data: CreateCategorySchema) -> tuple[str | None, bool, str | None]:
    ...
```

Tuple return types are encouraged on services and repositories for clarity, but the project does not enforce them with `mypy`.

## Module imports

Use **absolute** imports everywhere:

```python
# ✅
from app.features.users.repositories.users_repository import UsersRepository

# ❌
from .repositories.users_repository import UsersRepository
from ...repositories.users_repository import UsersRepository
```

Group imports in this order, separated by a blank line:
1. Standard library (`datetime`, `json`, ...).
2. Third-party (`fastapi`, `pydantic`, `bcrypt`, ...).
3. `app.*` (`app.core...`, `app.utils...`, `app.features...`).

## Comments

The project has very few comments. When you add one, keep it in Spanish and only when it explains **why**, not what the next line does. The code is meant to be self-documenting.

## Exception handling — one `try` per function

Use **a single** `try` block per function. The order of `except` clauses matters: list the most specific exception first, and **always re-raise `HTTPException` and `ServiceError`** before catching anything else, otherwise an intentional exception raised inside the `try` gets swallowed by a generic `except Exception` and the user gets a misleading error message.

The canonical pattern (used in `app/middlewares/jwt_middleware.py::verify_jwt` and every `*Service` in `app/features/`):

```python
try:
    # 1. side effect that can fail in its own way (e.g. Redis)
    # 2. business logic
    # 3. raise the project's domain exception on validation failures
    ...

except (HTTPException, ServiceError):
    raise                                # preserve the intentional error

except SpecificLibraryError:            # e.g. PyJWTError, mysql.Error
    raise domain_specific_exception

except Exception as e:
    logger.error("Contexto: %s", e, exc_info=True)
    raise HTTPException(500, "Mensaje genérico")   # or return (error, ...) in services
```

### Which exception to raise

| Layer | Exception to raise | Why |
| --- | --- | --- |
| Middleware / dependency (`app/middlewares/`) | `HTTPException` | Lives in the request path; FastAPI handles it directly. |
| Controller (`*_controller.py`) | `HTTPException` | Same — lives in the request path. |
| Service (`*_service.py`) | `ServiceError` (from `app/core/exception.py`) | The service does not know about HTTP. The controller converts `error` to `HTTPException`. |
| Repository (`*_repository.py`) | **Never** raises — returns `(error, data)` tuples. | The repository is the lowest layer; it must not leak exceptions. |
| Background task / Celery (`app/tasks/`) | `self.retry(exc=e, ...)` | The Celery task is the boundary; let the framework handle it. |

The two project exceptions:

- `app/core/exception.py::ServiceError(message: str)` — carries a single `message` attribute. The service catches it, returns `(e.message, success, message)`, and the controller maps `error` to `HTTPException`.
- `fastapi.HTTPException(status_code, detail)` — only raised in middlewares, controllers, and the `verify_jwt` path. Status codes per `architecture/SKILL.md`.

Anti-patterns:

- ❌ Two `try` blocks in the same function to handle two unrelated concerns — merge them and use the `except` chain above.
- ❌ `except Exception` **without** `except (HTTPException, ServiceError): raise` above it — the intentional exception gets logged as an "error" and re-raised with a wrong message.
- ❌ A bare `except:` — it catches `SystemExit` and `KeyboardInterrupt` too.
- ❌ Raising `HTTPException` from inside a `*Service` — services don't know about HTTP. Raise `ServiceError` and let the controller translate.
- ❌ Returning `(None, data)` from a `*Service` without a `try/except` — an unhandled exception bypasses the `(error, success, message)` contract the controllers expect.

## Reference paths

- `app/utils/logger.py` — `get_logger`.
- `app/core/exception.py` — `ServiceError`.
- `app/utils/base_schema.py` — `BaseSchema` for date serialization.
- `app/features/categories/services/categories_service.py` — canonical service with all conventions applied.
- `app/features/users/repositories/users_repository.py` — canonical repository.
- `app/features/warranties/controllers/warranties_controller.py` — canonical controller.
- `app/features/auth/routes/auth_routes.py` — canonical route with rate limiter + JWT.
