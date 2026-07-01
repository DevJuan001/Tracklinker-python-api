---
name: database
description: Use when writing SQL queries, adding/modifying repositories, designing new tables, or touching migrations. Covers the MySQL schema, the cursor/connection pattern, the `*Repository` return-tuple contract, and the views in `database/03_views.sql`.
---

# Database Skill

Tracklinker uses **MySQL 8.0+** via `mysql-connector-python`. Every repository in `app/features/<feature>/repositories/` is the only place where SQL lives.

## Where the schema lives

| File | Purpose | When to run |
| --- | --- | --- |
| `database/01_database.sql` | DDL — `CREATE DATABASE` + all `CREATE TABLE` | First |
| `database/02_dml.sql` | DML — seeds (roles, cities, sample users, statuses) | Second |
| `database/03_views.sql` | Views used by reports | Third |

**Always read `01_database.sql` before writing a new repository method** so you know the exact column names, types, and foreign keys.

## Connection pattern

`app/core/database.py` exposes `get_connection()`. The pattern is:

```python
from app.core.database import get_connection

@staticmethod
def my_query(connection):
    cursor = connection.cursor()           # NEVER open a new connection here
    try:
        cursor.execute("SELECT ...", (param,))
        results = cursor.fetchall()
        return None, results                # (error, data) tuple
    except Exception as e:
        logger.error("Error en my_query: %s", e, exc_info=True)
        return "Mensaje de error en español", None
    finally:
        cursor.close()                      # ALWAYS close the cursor
```

Key points:
- The cursor is opened **inside** the repository method.
- The cursor is closed in the `finally` block.
- The connection is **NOT** opened or closed in the repository — the service owns the connection lifecycle.
- Every method must return `(error: str | None, data)`. **Never raise.**

## The `(error, data)` contract

| Outcome | Return value |
| --- | --- |
| Success, with data | `(None, data)` |
| Success, no data (e.g. UPDATE that affected 0 rows) | `("Mensaje de error específico", None)` |
| Exception | `("Error al intentar ...", None)` (already logged) |

The service then converts the error to `ServiceError` and the controller converts that to `HTTPException`.

## Common column conventions

| Pattern | Example | Notes |
| --- | --- | --- |
| `*_id` primary key, auto-increment | `product_id` | `INT AUTO_INCREMENT PRIMARY KEY` |
| `*_status` | `product_status` | `INT`, see `business-logic` skill for values |
| `*_date` | `warranty_date` | `DATETIME` or `DATE` |
| Soft-delete via status | `category_status = 1` | We do NOT use `is_deleted` flags |
| Foreign keys are `*_id` | `category_id`, `rol_id` | `INT NOT NULL` (usually) |

## Naming convention inside SQL

- **Table names**: `UPPERCASE_SNAKE_CASE` (`PRODUCT_SERIALS`, `WARRANTY_INCIDENTS`).
- **Column names**: `lowercase_snake_case` (`product_id`, `user_email`).
- **Aliases**: short, lowercase (`p` for `PRODUCTS`, `ps` for `PRODUCT_SERIALS`).

## JOINs — the common patterns

Most queries follow these JOIN shapes:

```sql
-- Product with brand, model, subcategory, category
PRODUCT_SERIALS ps
INNER JOIN PRODUCTS p            ON ps.product_id = p.product_id
INNER JOIN PRODUCT_DETAILS pd    ON p.product_details_id = pd.product_details_id
INNER JOIN PRODUCT_MODELS pm     ON pd.product_model_id = pm.product_model_id
INNER JOIN PRODUCT_BRANDS pb     ON pm.product_brand_id = pb.product_brand_id
INNER JOIN SUBCATEGORIES sc      ON p.subcategory_id = sc.subcategory_id
INNER JOIN CATEGORIES c          ON sc.category_id = c.category_id

-- Warranty with customer (USERS) and assigned technician (TECHNICAL)
WARRANTY_INCIDENTS wi
INNER JOIN CITIES c              ON wi.warranty_city = c.city_id
INNER JOIN USERS u               ON wi.created_by = u.user_id
LEFT  JOIN TECHNICAL t           ON wi.warranty_incidents_id = t.warranty_incidents_id
LEFT  JOIN USERS tech            ON t.user_id = tech.user_id

-- Output order with details, product, brand, model
OUTPUT_ORDERS oo
INNER JOIN OUTPUT_DETAILS od     ON oo.out_order_id = od.out_order_id
INNER JOIN PRODUCT_SERIALS ps    ON od.product_serial = ps.product_serial
INNER JOIN PRODUCTS p            ON ps.product_id = p.product_id
INNER JOIN PRODUCT_DETAILS pd    ON p.product_details_id = pd.product_details_id
INNER JOIN PRODUCT_MODELS pm     ON pd.product_model_id = pm.product_model_id
INNER JOIN PRODUCT_BRANDS pb     ON pm.product_brand_id = pb.product_brand_id
```

## Report views (`database/03_views.sql`)

Some features have their own report queries embedded in the repository (e.g. `find_recent_users`, `find_products_by_brand`, `find_outputs_growth`). They use:

- `period_map` from `app/utils/periods.py` for translating `7d` / `15d` / `30d` / `6m` / `1a` to SQL intervals.
- `daily_periods` for choosing between `DATE(col)` and `DATE_FORMAT(col, '%Y-%m')` grouping.
- `date_formatter` from `app/utils/date_formatter.py` to turn `DATETIME` into Spanish "Mes DD YYYY".

## Migrations

There is no migration framework (Alembic, etc.). Schema changes are made by:

1. Updating `database/01_database.sql` with the new DDL.
2. Manually running the diff against the live DB.
3. If views change, update `database/03_views.sql` too.

If a migration framework is added later, it should live under `database/migrations/` and not break the existing SQL files (which remain the source of truth for fresh installs).

## Cursor patterns

| Need | Pattern |
| --- | --- |
| Fetch all rows | `cursor.fetchall()` |
| Fetch one row | `cursor.fetchone()` (returns tuple or `None`) |
| Insert and get new id | `cursor.lastrowid` after `cursor.execute("INSERT ...")` |
| Buffered cursor (multiple statements) | `connection.cursor(buffered=True)` — used in some categories queries |
| Mapped results (dict per row) | Not used — repositories always return tuples; conversion to Pydantic happens in the same method |

## Reference paths

- `app/core/database.py` — `get_connection()` factory.
- `database/01_database.sql` — full DDL.
- `database/02_dml.sql` — seeds (roles, cities, users, statuses).
- `database/03_views.sql` — views.
- `app/utils/periods.py` — `period_map`, `daily_periods`.
- `app/utils/date_formatter.py` — Spanish date formatter.
- `app/features/users/repositories/users_repository.py` — canonical multi-table JOIN example.
- `app/features/products/repositories/products_repository.py` — biggest repository; covers the most JOINs.
