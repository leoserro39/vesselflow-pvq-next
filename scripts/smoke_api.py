from __future__ import annotations

import asyncio
from collections.abc import Callable
from typing import Any

import httpx

from pvq_next.app import app


STATE_ID = "9feabb3fa9db4502907d290edc992df1"
BASE_PATH = "/api/v2/pvq-next"
STATE_BASE_PATH = f"{BASE_PATH}/states/{STATE_ID}"
MUTATION_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


def _assert_read_only_routes() -> None:
    for route in app.routes:
        methods = getattr(route, "methods", set())
        if methods & MUTATION_METHODS:
            raise AssertionError(f"Mutation route exposed: {methods} {route.path}")


async def _get_json(client: httpx.AsyncClient, path: str) -> dict[str, Any]:
    response = await client.get(path)
    if response.status_code != 200:
        raise AssertionError(f"GET {path} returned {response.status_code}: {response.text}")
    body = response.json()
    if not isinstance(body, dict):
        raise AssertionError(f"GET {path} did not return a JSON object")
    return body


async def _check(
    client: httpx.AsyncClient,
    name: str,
    path: str,
    predicate: Callable[[dict[str, Any]], bool],
) -> dict[str, Any]:
    body = await _get_json(client, path)
    if not predicate(body):
        raise AssertionError(f"Smoke check failed: {name}")
    print(f"ok {name}")
    return body


async def main() -> None:
    _assert_read_only_routes()

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://testserver",
    ) as client:
        await _check(
            client,
            "health",
            f"{BASE_PATH}/health",
            lambda body: body["status"] == "ok" and body["field_count"] == 75,
        )
        await _check(
            client,
            "menus",
            f"{BASE_PATH}/menus",
            lambda body: "AUTO_SYSTEM_RULE" in body["review_route"],
        )
        await _check(
            client,
            "operational-window",
            f"{BASE_PATH}/operational-window",
            lambda body: body["date_format"] == "MM/DD/YYYY",
        )
        await _check(
            client,
            "summary",
            f"{STATE_BASE_PATH}/summary",
            lambda body: body["counts"]["nomination_core_fields"] == 75
            and body["counts"]["source_archive_fields"] == 392,
        )
        await _check(
            client,
            "nomination-core",
            f"{STATE_BASE_PATH}/nomination-core",
            lambda body: len(body["fields"]) == 75,
        )
        await _check(
            client,
            "operational-state",
            f"{STATE_BASE_PATH}/operational-state",
            lambda body: body["operational_state"]["final_operational_state"]
            == "PRE_APT_WITH_TECHNICAL_REVIEW",
        )
        await _check(
            client,
            "evidence",
            f"{STATE_BASE_PATH}/evidence",
            lambda body: len(body["evidence"]) == 75,
        )
        areas = await _check(
            client,
            "areas",
            f"{STATE_BASE_PATH}/areas",
            lambda body: body["area_count"] == 8
            and sum(area["field_count"] for area in body["areas"]) == 75,
        )
        first_area = areas["areas"][0]
        await _check(
            client,
            "area-detail",
            f"{STATE_BASE_PATH}/areas/{first_area['area_id']}",
            lambda body: body["field_count"] == first_area["field_count"]
            and body["area_name"] == first_area["area_name"],
        )
        await _check(
            client,
            "full-archive",
            f"{STATE_BASE_PATH}/full-archive",
            lambda body: len(body["source_392"]) == 392,
        )

    print("smoke ok")


if __name__ == "__main__":
    asyncio.run(main())
