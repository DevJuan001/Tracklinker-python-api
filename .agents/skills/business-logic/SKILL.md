---
name: business-logic
description: Use when touching domain rules — orders, warranties, products, input/output flows, role permissions, status transitions. Covers the product lifecycle, the warranty creation flow, and the role-based access matrix.
---

# Business Logic Skill

Tracklinker is an inventory management system. This skill documents the **domain rules** that any change to services, repositories, or controllers must respect.

## Domain entities and relationships

```
CATEGORY (1) ──< (N) SUBCATEGORY (1) ──< (N) PRODUCT
                                              │
                                              ├──< (N) PRODUCT_SERIAL  (per unit sold)
                                              │           │
                                              │           └──< (N) WARRANTY_INCIDENT
                                              │                       │
                                              │                       └──< (N) TECHNICAL (assignment)
                                              │
                                              └──< (1) PRODUCT_DETAIL ──> PRODUCT_MODEL ──> PRODUCT_BRAND
PRODUCT_SERIAL ──< (N) OUTPUT_DETAIL ──> (1) OUTPUT_ORDER
INPUT_ORDER (1) ──< (N) PRODUCT_SERIAL (provenance)
SUPPLIER (1) ──< (N) INPUT_ORDER
USER ──< (N) WARRANTY_INCIDENT (created_by)
USER ──< (N) TECHNICAL (assigned_technician)
USER >──> ROLE
USER >──> CITY
```

## Product lifecycle (the heart of the system)

The most important domain rule is the **state machine of a product**:

| `product_status` | Meaning | Who sets it | Allowed transitions |
| --- | --- | --- | --- |
| `1` | Disabled | Admin (`update_product_status`) | → `2` (enable) |
| `2` | Active / in stock | Default after `create_product`; or re-enable | → `1` (disable), `3` (sell), `4` (warranty) |
| `3` | Sold (output order) | `create_output_order` | — |
| `4` | In warranty | `create_warranty` | → `2` (warranty completed/cancelled) |

**Rules to enforce:**

1. A product with `status = 1` (disabled) **cannot** be sold (`status = 3`) or put under warranty (`status = 4`).
2. A product with an **active warranty** (`warranty_status IN (2, 3)`) **cannot** be disabled.
3. `create_product` starts at `status = 2` (active).
4. `create_warranty` and `create_output_order` are the only paths that move products OUT of `status = 2`.

## Warranty flow (most complex transaction)

`WarrantiesService.create_warranty` is the canonical multi-repository transaction. It must run atomically:

```
1. Find product by serial
   → if not found or status == 1, raise ServiceError
2. Check no active warranty exists for the serial
3. Create OUTPUT_ORDER (status = 2)
4. Create OUTPUT_DETAIL with the serial and warranty date
5. Update product status to 4 (in warranty)
6. Insert WARRANTY_INCIDENT
   → all in one transaction; rollback on any error
```

`WarrantiesService.update_warranty` has a state machine of its own:

```python
WARRANTY_STATUS_PRODUCT_MAP = {
    1: 2,   # warranty disabled → product back to active
    2: 4,   # warranty pending → product stays in warranty
    3: 4,   # warranty in progress → product stays in warranty
    4: 2,   # warranty completed → product back to active
}
```

And the **technician assignment** rules:

| Current `warranty_status` | New `warranty_status` | Side effect |
| --- | --- | --- |
| `1` (disabled) | `3` or `4` | Assign technician (`TechniciansRepository.assign_technician`) |
| `2` (pending) | `3` (in progress) | Assign technician |
| Any | `1` (disabled) | Unassign technician (`TechniciansRepository.unassign_technician`) |

## Roles and permissions matrix

| Role | Description | Allowed |
| --- | --- | --- |
| `Admin` | Full access | Everything |
| `Almacén` | Inventory management | Products, categories, subcategories, suppliers, input orders, output orders |
| `Técnico` | Warranty operations | Warranties, output orders, product lookup |
| `Cliente` | Final customer | Suggestions, profile |

The role list comes from `database/02_dml.sql` seeds. The middleware that enforces it is `app/middlewares/roles_middleware.py::require_roles`.

## Uniqueness / "already exists" rules

Every entity has a uniqueness invariant that the service must check **before** insert/update:

| Entity | Unique field | Repository method |
| --- | --- | --- |
| `User` | `email` | `UsersRepository.find_user_by_email` |
| `Category` | `name` (case-insensitive) | `CategoriesRepository.find_category_by_name` |
| `Subcategory` | `name` (case-insensitive) | `SubcategoriesRepository.find_subcategory_by_name` |
| `Supplier` | `name` | `SuppliersRepository.find_supplier_by_name` |
| `ProductSerial` | `serial` | `ProductSerialsRepository.find_product_by_serial` |

When the check fails, raise `ServiceError` with a human-friendly message ("Ya existe una X con este nombre…").

## Status fields (the `*_status` convention)

Most tables have a `*_status` column. The exact semantics differ per table; **always** check the SQL file and existing repositories before assuming:

| Column | Convention used |
| --- | --- |
| `category_status` | `1` = disabled, `2` = active |
| `subcategory_status` | `1` = disabled, `2` = active |
| `supplier_status` | `1` = disabled, `2` = active |
| `product_status` | `1` = disabled, `2` = active, `3` = sold, `4` = warranty |
| `out_order_status` | `2` = newly created (default after `create_output_order`) |
| `warranty_status` | `1` = disabled, `2` = pending, `3` = in progress, `4` = completed |
| `user_status` | `1` = disabled, `2` = active |

## Output order flow

`OutputOrdersService.create_output_order`:

1. For each serial in `product_serials`, verify the product exists.
2. Insert `OUTPUT_ORDERS` with `out_order_status = 2` (default pending).
3. For each serial, insert an `OUTPUT_DETAILS` row with the warranty date.

`update_output_order` allows changing the `output_product_garanty` (warranty date) and/or replacing the list of serials (delete + re-insert details).

## Suggestions flow

`SuggestionsController.send_suggestion_mail` is the only feature that:

- Has **no** repository (it just sends an email).
- Receives a JWT payload, looks up the user via `UsersService.get_user_by_id`, then sends an email to `settings.MAIL_FROM` using `app/templates/suggestion_mail.html`.

If you need persistence (e.g. save suggestions to a table), add a new feature with its own service + repository rather than expanding `suggestions`.

## Reference paths

- `app/features/products/services/products_service.py` — product status transitions.
- `app/features/warranties/services/warranties_service.py` — full warranty transaction + state machine.
- `app/features/output_orders/services/output_orders_service.py` — output order flow.
- `app/middlewares/roles_middleware.py` — `require_roles` enforcement.
- `database/01_database.sql` — source of truth for all table schemas and status enums.
- `database/02_dml.sql` — seeded roles (`Admin`, `Almacén`, `Técnico`, `Cliente`).
