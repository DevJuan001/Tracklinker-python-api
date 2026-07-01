## Description

<!-- A short (1–3 sentences) summary of WHAT this PR does and WHY. -->

## Changes

<!-- Group the changes by area. Pick the sections that apply; delete the rest. -->

### Architecture
- <!-- e.g. Migrated `XService` to call `XRepository` directly instead of going through `YService`. -->

### Modeling
- <!-- e.g. Renamed `FooModel` → `FooSchema` and split into `models/schemas/foo_schemas.py`. -->

### Service layer
- <!-- e.g. `ProductsService.create_product` now opens one connection and shares it across the multi-step insert. -->

### Repository
- <!-- e.g. `ProductsRepository.find_all_products` rewrote the JOIN to fix the missing `product_brand_name` column. -->

### Routes
- <!-- e.g. Added `GET /api/products/recent` behind `require_roles(["Admin", "Almacén", "Técnico"])`. -->

### Security
- <!-- e.g. Added rate limit of `30/60s` to `GET /api/users`. -->

### Database
- <!-- e.g. Added index on `WARRANTY_INCIDENTS(product_serial)` to speed up `find_active_warranty_by_serial`. -->

### Documentation
- <!-- e.g. Updated `README.md` env var table. -->

### Cleanup
- <!-- e.g. Removed dead `from app.core.database import get_connection` import in `subcategories_repository.py`. -->

## Related issues / PRs

<!-- Link any related issue or PR. Use `Closes #123` or `Refs #45` to auto-link. -->
