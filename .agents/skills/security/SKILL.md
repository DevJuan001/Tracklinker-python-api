---
name: security
description: Use when touching authentication, JWT tokens, passwords, role checks, rate limiting, CORS, cookies, or any secret material. Covers the bcrypt hashing contract, the JWT cookie pair, the RBAC middleware, and the rate-limit thresholds.
---

# Security Skill

This project handles authentication, authorization, and request throttling in **three** places: `app/core/security.py`, `app/middlewares/`, and the `Depends(...)` chain on each route.

## The JWT cookie pair

Two cookies are set on successful login and refresh:

| Cookie | Path | Max-Age | Used by |
| --- | --- | --- | --- |
| `access_token` | `/` | `ACCESS_TOKEN_EXPIRE * 60` seconds | Every authenticated endpoint |
| `refresh_token` | `/api/auth/refresh` | `REFRESH_TOKEN_EXPIRE * 86400` seconds | `POST /api/auth/refresh` only |

Both cookies are:
- `httponly=True` — not accessible from JavaScript (XSS-safe).
- `secure` — `True` only when `ENVIRONMENT == "production"`.
- `samesite` — `"none"` in production, `"lax"` in development.

`set_auth_cookies` in `app/core/security.py` is the **only** function that sets them. Do not call `response.set_cookie` directly anywhere else.

## Token contents

```python
{
    "sub": str(user_id),   # string, the user id
    "role": role_id,       # int, the role id (Admin=1, Almacén=2, Técnico=3, Cliente=4)
    "exp": <datetime>      # expiration
}
```

When a route depends on `verify_jwt`, the `payload` dict it receives has shape `{"user_id": ..., "role": ...}` (the keys are renamed by the middleware).

## `verify_jwt` middleware

`app/middlewares/jwt_middleware.py::verify_jwt` reads the `access_token` cookie, decodes it with `settings.ACCESS_TOKEN_SECRET_KEY`, and returns the payload. If the cookie is missing, invalid, or expired, it raises `HTTPException(401, "Token inválido o expirado")`.

`verify_jwt` does **not** check the role — that's `require_roles` job.

## `require_roles` RBAC middleware

```python
from app.middlewares.roles_middleware import require_roles

@router.get(
    "/admin-only",
    dependencies=[Depends(require_roles(["Admin"]))]
)
def admin_only_endpoint():
    ...
```

Rules:
- The list of role **names** (not ids) is compared against `payload["role"]`. The seed roles in `database/02_dml.sql` are exactly `"Admin"`, `"Almacén"`, `"Técnico"`, `"Cliente"`. Use these strings verbatim.
- Failure raises `HTTPException(403, "No puedes realizar esta acción")`.
- Always combine with `verify_jwt`: `Depends(verify_jwt)` for the user payload, then `Depends(require_roles([...]))` for the role gate.

## Password handling

- Hashing: `bcrypt` with `rounds=12`. The hash is a string stored in the `user_password` column.
- Verification: `verify_password(user_password_hash, plain_password)` from `app/core/security.py`. Returns `True` or raises `HTTPException(401, "Contraseña Incorrecta")`.
- Temporal passwords (for new users): `generate_temporal_password(length=12)` — guaranteed to include upper, lower, and digit, then shuffled.

**Never**:
- Log a password (even hashed).
- Return a password in a `*Response` model.
- Compare passwords with `==`. Use `bcrypt.checkpw`.

## Rate limiting

`FastAPILimiter` is initialized in `app/main.py`'s `lifespan` with the Redis client. To apply a limit to an endpoint:

```python
from fastapi_limiter.depends import RateLimiter

@router.post(
    "/login",
    dependencies=[Depends(RateLimiter(times=3, seconds=60))]
)
def login(...):
    ...
```

Current thresholds (taken from `routes/`):

| Endpoint type | `times` / `seconds` |
| --- | --- |
| `POST /api/auth/login` | `3 / 60` |
| `POST /api/auth/recover-password` | `3 / 60` |
| `POST /api/auth/refresh` | `30 / 60` |
| `POST /api/auth/verify-roles` | `50 / 60` |
| Most list endpoints | `30 / 60` |
| Most catalog reads (brands, models, statuses) | `50 / 60` |
| Password update | `10 / 60` |

Keep the same granularity when adding new endpoints.

## CORS

`app/main.py` allows these origins:
- `http://localhost:5173` (dev)
- `https://tracklinker-frontend-web.vercel.app` (prod)
- `https://tracklinker-frontend-web-project.onrender.com` (alt prod)

`allow_credentials=True` is required because we send cookies. Methods and headers are `*`.

## Secrets management

- All secrets are loaded from `.env` via `pydantic-settings` (see `app/core/config.py`).
- **Never** hardcode a secret in code.
- **Never** commit `.env`. `.gitignore` should already exclude it; verify before committing.
- The `.env.example` file ships with empty values — never put real secrets there.

## Input validation

Pydantic `BaseModel` schemas (in `models/schemas/*_schemas.py`) handle request validation. The `*Schema` suffix is mandatory.

`app/utils/base_schema.py::BaseSchema` is the project base — it has a validator that converts `date` instances to `str` automatically. Use it for any new schema that may receive a `date`:

```python
from app.utils.base_schema import BaseSchema

class CreateFooSchema(BaseSchema):
    name: str
    birth_date: date
```

## Reference paths

- `app/core/security.py` — JWT, bcrypt, cookies, password generator.
- `app/middlewares/jwt_middleware.py` — `verify_jwt`.
- `app/middlewares/roles_middleware.py` — `require_roles`.
- `app/middlewares/validate_request.py` — `validate_request` (catches client disconnects).
- `app/core/redis.py` — Redis client for rate limiting and cache.
- `app/main.py` — CORS and `lifespan` (init/close Redis + FastAPILimiter).
