from __future__ import annotations

try:
    from fastapi import APIRouter, HTTPException
except Exception:  # pragma: no cover
    APIRouter = None
    HTTPException = None

from . import service

if APIRouter is not None:
    router = APIRouter(prefix="/api/v2/pvq-next", tags=["PVQ Next"])

    @router.get("/health")
    async def get_health():
        return service.health()

    @router.get("/menus")
    async def get_menus():
        return service.menus()

    @router.get("/operational-window")
    async def get_operational_window():
        return service.operational_window()

    @router.get("/states/{state_id}/summary")
    async def get_summary(state_id: str):
        return service.summary(state_id)

    @router.get("/states/{state_id}/nomination-core")
    async def get_nomination_core(state_id: str):
        return service.nomination_core(state_id)

    @router.get("/states/{state_id}/operational-state")
    async def get_operational_state(state_id: str):
        return service.operational_state(state_id)

    @router.get("/states/{state_id}/evidence")
    async def get_evidence(state_id: str):
        return service.evidence(state_id)

    @router.get("/states/{state_id}/areas")
    async def get_areas(state_id: str):
        return service.areas(state_id)

    @router.get("/states/{state_id}/areas/{area_id}")
    async def get_area(state_id: str, area_id: str):
        area = service.area(state_id, area_id)
        if area is None:
            raise HTTPException(status_code=404, detail="Area not found")
        return area

    @router.get("/states/{state_id}/full-archive")
    async def get_full_archive(state_id: str):
        return service.full_archive(state_id)
else:
    router = None
