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


def test_menus_returns_controlled_values():
    status_code, body = get_json("/api/v2/pvq-next/menus")

    assert status_code == 200
    assert "Dropdown" in body["input_control"]
    assert "AUTO_SYSTEM_RULE" in body["review_route"]


def test_operational_window_returns_cycle_rule():
    status_code, body = get_json("/api/v2/pvq-next/operational-window")

    assert status_code == 200
    assert body["date_format"] == "MM/DD/YYYY"
    assert body["cycle_rule"]["cycle_start_day"] == 25


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


def test_areas_returns_field_contract_groups():
    status_code, body = get_json(f"{BASE_URL}/areas")

    assert status_code == 200
    assert body["state_id"] == STATE_ID
    assert body["area_count"] == 8

    area_ids = [area["area_id"] for area in body["areas"]]
    assert area_ids == [
        "identificacao",
        "dimensoes",
        "operacao",
        "dp-fpso",
        "maquinas",
        "documentos",
        "inspecoes-vetting",
        "nomeacao",
    ]

    assert sum(area["field_count"] for area in body["areas"]) == 75
    assert all(len(area["fields"]) == area["field_count"] for area in body["areas"])


def test_area_returns_counts_and_fields():
    status_code, body = get_json(f"{BASE_URL}/areas/identificacao")

    assert status_code == 200
    assert body["state_id"] == STATE_ID
    assert body["area_id"] == "identificacao"
    assert body["area_name"] == "Identificação"
    assert body["field_count"] == 15
    assert body["review_required_count"] == sum(
        field["review_route"] != "AUTO_SYSTEM_RULE" for field in body["fields"]
    )
    assert body["blocking_or_potential_blocking_count"] == sum(
        field["blocks_nomination"] in {"Sim", "Potencial"} for field in body["fields"]
    )


def test_full_archive_returns_392_items():
    status_code, body = get_json(f"{BASE_URL}/full-archive")

    assert status_code == 200
    assert len(body["source_392"]) == 392


def test_app_routes_are_read_only():
    mutation_methods = {"POST", "PUT", "PATCH", "DELETE"}

    for route in app.routes:
        assert not (getattr(route, "methods", set()) & mutation_methods)
