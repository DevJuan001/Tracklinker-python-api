---
name: architecture
description: Use when modifying the layered structure (routes → controllers → services → repositories → models), adding new features, or moving files between layers. Covers the strict vertical dependency rule, the "no service-to-service" rule, and the feature-based folder organization.
---

# Architecture Skill

Tracklinker API uses a **strictly layered, feature-based architecture**. Every change must respect the vertical flow and the isolation rules between features.

## The 5 layers (top to bottom)

```
Route → Controller → Service → Repository → MySQL
```

| Layer | Folder | Responsibility |
| --- | --- | --- |
| **Route** | `app/features/<feature>/routes/<feature>_routes.py` | Define HTTP endpoints, attach middlewares (`require_roles`, `RateLimiter`, `verify_jwt`), wire body/query/path params to controller methods. |
| **Controller** | `app/features/<feature>/controllers/<feature>_controller.py` | Receive the validated input, call the service, convert `(error, success, message)` into `HTTPException` or success JSON. |
| **Service** | `app/features/<feature>/services/<feature>_service.py` | Business logic, transactions, orchestration of multiple repositories. Owns the `connection` lifecycle. |
| **Repository** | `app/features/<feature>/repositories/<feature>_repository.py` | Pure SQL, returns `(error, data)` tuple. Never raises. |
| **Model** | `app/features/<feature>/models/{schemas,responses,entities}/` | Pydantic models: `*Schema` for input, `*Response` for output, no-suffix for internal. |

## Inviolable rules

### 1. Services NEVER call other services
A service must only import **repositories**. If a service needs data from another feature's table, it imports that feature's **repository** directly and reuses the same `connection`.

```python
# ❌ WRONG
from app.features.users.services.users_service import UsersService
error, user = UsersService.get_user_by_email(email)

# ✅ CORRECT
from app.features.users.repositories.users_repository import UsersRepository
error, user = UsersRepository.find_user_by_email(email, connection)
```

**Exception:** Controllers CAN call other feature's services. The only existing example is `SuggestionsController` calling `UsersService.get_user_by_id`.

### 2. No layer skipping
- A route must not call a repository or a service directly — always go through the controller.
- A repository must not import a service, a controller, or a route.

### 3. Transactional flows that cross repositories
When a service needs to write to multiple tables atomically (e.g. `WarrantiesService.create_warranty` creates an output order AND a warranty AND updates product status), it:

1. Opens **one** `connection = get_connection()`.
2. Calls each repository method passing the same `connection`.
3. Calls `connection.commit()` **once** at the end.
4. On any error, calls `connection.rollback()` and lets the `finally` close the connection.

```python
connection = get_connection()
try:
    error, product = ProductSerialsRepository.find_product_by_serial(serial, connection)
    # ... validations ...
    error, success, output_order_id = OutputOrdersRepository.create_output_order(connection)
    error, success, message = OutputDetailsRepository.create_output_details(output_order_id, ..., connection)
    error, success, message = ProductsRepository.update_product_status(product_id, status, connection)
    error, success, message = WarrantiesRepository.create_warranty(data, user_id, connection)
    connection.commit()
except ServiceError:
    connection.rollback()
finally:
    connection.close()
```

## Feature-based folder organization

Every feature lives under `app/features/<feature_name>/` and follows this structure **only if it has a repository**:

```
features/<feature>/
├── routes/         # routers (always present)
├── controllers/    # controllers (always present)
├── services/       # business logic (always present)
├── models/         # Pydantic schemas/responses (when applicable)
│   ├── schemas/    # *Schema (request body)
│   ├── responses/  # *Response (output)
│   └── entities/   # no-suffix internal models
└── repositories/   # SQL access (optional — some features skip it)
```

### Features that DO NOT have a repository
- `auth` — uses `UsersRepository` directly because users are the source of truth.
- `suggestions` — has no DB access; only sends an email via FastAPI-Mail.

### Features that DO NOT have models
- `reports` — reuses response models from other features (defined in their repositories' imports).

## When to add a new feature

1. Create `app/features/<name>/` with the 5 subfolders you need.
2. Add a router file and register it in `app/main.py` via `app.include_router(...)`.
3. Add a controller that translates `(error, data)` into `HTTPException` or JSON.
4. Add a service that opens the connection and orchestrates repositories.
5. Add a repository with the SQL.
6. Add Pydantic models in `models/schemas/`, `models/responses/`, or `models/entities/`.
7. **Never** import another feature's service.

## When to add a new endpoint to an existing feature

1. Add the route function in `<feature>_routes.py` with the right middlewares.
2. Add the controller method (delegates to the service).
3. Add the service method (owns the connection, calls the repository).
4. Add the repository method (pure SQL).
5. Add the Pydantic `Schema`/`Response` if needed.

## Reference paths

- `app/main.py` — router registration, CORS, lifespan.
- `app/core/database.py` — `get_connection()`.
- `app/core/exception.py` — `ServiceError`.
- `app/features/auth/services/auth_service.py` — canonical service that uses another feature's repository.
- `app/features/warranties/services/warranties_service.py` — canonical multi-repository transaction.
- `app/features/reports/services/reports_service.py` — canonical service that imports many feature repositories.
