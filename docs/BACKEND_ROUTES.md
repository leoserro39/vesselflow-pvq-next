# Backend Routes - PVQ Next

Versão inicial read-only.

## Endpoints

- `GET /api/v2/pvq-next/health`
- `GET /api/v2/pvq-next/menus`
- `GET /api/v2/pvq-next/operational-window`
- `GET /api/v2/pvq-next/states/{state_id}/summary`
- `GET /api/v2/pvq-next/states/{state_id}/nomination-core`
- `GET /api/v2/pvq-next/states/{state_id}/operational-state`
- `GET /api/v2/pvq-next/states/{state_id}/evidence`
- `GET /api/v2/pvq-next/states/{state_id}/areas`
- `GET /api/v2/pvq-next/states/{state_id}/areas/{area_id}`
- `GET /api/v2/pvq-next/states/{state_id}/full-archive`

## Areas

`area_id` é um slug estável derivado do valor `area` do contrato de campos.
Cada resposta de área inclui:

- `area_id`
- `area_name`
- `fields`
- `field_count`
- `review_required_count`
- `blocking_or_potential_blocking_count`

## Proibido nesta fase

- POST/PUT/PATCH/DELETE
- mutation de storage
- upload
- frontend
- alteração em `app.py` antes de validação import-only
