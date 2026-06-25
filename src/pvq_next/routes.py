from __future__ import annotations

try:
    from fastapi import APIRouter
except Exception:  # pragma: no cover
    APIRouter = None

from . import service

if APIRouter is not None:
    router = APIRouter(prefix="/api/v2/pvq-next", tags=["PVQ Next"])

    @router.get("/health")
    def get_health():
        return service.health()

    @router.get("/states/{state_id}/summary")
    def get_summary(state_id: str):
        return service.summary(state_id)

    @router.get("/states/{state_id}/nomination-core")
    def get_nomination_core(state_id: str):
        return service.nomination_core(state_id)

    @router.get("/states/{state_id}/operational-state")
    def get_operational_state(state_id: str):
        return service.operational_state(state_id)

    @router.get("/states/{state_id}/evidence")
    def get_evidence(state_id: str):
        return service.evidence(state_id)

    @router.get("/states/{state_id}/full-archive")
    def get_full_archive(state_id: str):
        return service.full_archive(state_id)
else:
    router = None
