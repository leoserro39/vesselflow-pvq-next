# Backend Routes - PVQ Next

Versão inicial read-only.

## Endpoints

- `GET /api/v2/pvq-next/health`
- `GET /api/v2/pvq-next/states/{state_id}/summary`
- `GET /api/v2/pvq-next/states/{state_id}/nomination-core`
- `GET /api/v2/pvq-next/states/{state_id}/operational-state`
- `GET /api/v2/pvq-next/states/{state_id}/evidence`
- `GET /api/v2/pvq-next/states/{state_id}/areas/{area_id}`
- `GET /api/v2/pvq-next/states/{state_id}/full-archive`

## Proibido nesta fase

- POST/PUT/PATCH/DELETE
- mutation de storage
- upload
- frontend
- alteração em `app.py` antes de validação import-only
