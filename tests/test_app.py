import asyncio

import httpx

from pvq_next.app import app


STATE_ID = "9feabb3fa9db4502907d290edc992df1"
BASE_URL = f"/api/v2/pvq-next/states/{STATE_ID}"


async def _get_json(path: str) -> tuple[int, dict]:
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get(path)
        return response.status_code, response.json()


def get_json(path: str) -> tuple[int, dict]:
    return asyncio.run(_get_json(path))


def test_health_returns_ok():
    status_code, body = get_json("/api/v2/pvq-next/health")

    assert status_code == 200
    assert body["status"] == "ok"


def test_summary_returns_madre_de_deus():
    status_code, body = get_json(f"{BASE_URL}/summary")

    assert status_code == 200
    assert body["vessel"]["name"] == "MADRE DE DEUS"


def test_nomination_core_returns_75_fields():
    status_code, body = get_json(f"{BASE_URL}/nomination-core")

    assert status_code == 200
    assert len(body["fields"]) == 75


def test_operational_state_returns_pre_apt_with_technical_review():
    status_code, body = get_json(f"{BASE_URL}/operational-state")

    assert status_code == 200
    assert (
        body["operational_state"]["final_operational_state"]
        == "PRE_APT_WITH_TECHNICAL_REVIEW"
    )


def test_evidence_returns_75_items():
    status_code, body = get_json(f"{BASE_URL}/evidence")

    assert status_code == 200
    assert len(body["evidence"]) == 75


def test_full_archive_returns_392_items():
    status_code, body = get_json(f"{BASE_URL}/full-archive")

    assert status_code == 200
    assert len(body["source_392"]) == 392


def test_app_routes_are_read_only():
    mutation_methods = {"POST", "PUT", "PATCH", "DELETE"}

    for route in app.routes:
        assert not (getattr(route, "methods", set()) & mutation_methods)
